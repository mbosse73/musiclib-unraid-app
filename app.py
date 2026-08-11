"""
Musiklib service.

Scans a directory of MP3 files, extracts ID3 metadata and cover art,
writes a flat library.json (no database), and serves a single-page
HTML UI plus HTTP range streaming for playback.

Environment:
    MUSIC_DIR  Path to scan (default: /music)
    DATA_DIR   Where library.json and covers are stored (default: /data)
    PORT       HTTP port (default: 8080)
"""

import asyncio
import hashlib
import json
import logging
import os
import threading
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from mutagen.mp3 import MP3

MUSIC_DIR = Path(os.getenv("MUSIC_DIR", "/music"))
DATA_DIR = Path(os.getenv("DATA_DIR", "/data"))
COVERS_DIR = DATA_DIR / "covers"
LIBRARY_FILE = DATA_DIR / "library.json"
TRACKS_FILE = DATA_DIR / "tracks.json"  # internal: track_id -> filesystem path
APP_DIR = Path(__file__).parent

log = logging.getLogger("musiklib")

# Guards the check-then-set on scan_state["running"]. scan() runs in a worker
# thread while request handlers read the state, so the flag alone is not enough.
_scan_lock = threading.Lock()

# Strong references to startup tasks; asyncio only holds weak ones.
_startup_tasks: set = set()

scan_state = {
    "running": False,
    "progress": 0,
    "total": 0,
    "skipped": 0,  # files that could not be read and were left out
    "error": None,  # short, user-facing message — details go to the log
}


def ensure_dirs() -> None:
    """Create DATA_DIR/covers. Called at startup and before every scan."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    COVERS_DIR.mkdir(parents=True, exist_ok=True)


def stable_id(*parts) -> str:
    h = hashlib.sha1()
    for p in parts:
        h.update(str(p).encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()[:16]


def read_tags(filepath: Path):
    """Read ID3 tags from an MP3 and return a flat dict, or None on failure."""
    try:
        audio = MP3(filepath)
    except Exception as exc:
        # One compact line per file — a full traceback per broken file would
        # drown the container log on a collection with many stray files.
        log.warning("Datei uebersprungen (%s): %s", exc.__class__.__name__, filepath)
        return None

    tags = audio.tags or {}

    def get_text(key):
        try:
            v = tags.get(key)
            if v is None:
                return None
            if hasattr(v, "text") and v.text:
                return str(v.text[0]).strip() or None
            return str(v).strip() or None
        except Exception:
            return None

    title = get_text("TIT2") or filepath.stem
    artist = get_text("TPE1") or "Unbekannter Interpret"
    album = get_text("TALB") or "Unbekanntes Album"
    album_artist = get_text("TPE2") or artist

    track_no = None
    track_str = get_text("TRCK")
    if track_str:
        try:
            track_no = int(track_str.split("/")[0])
        except (ValueError, IndexError):
            pass

    year = None
    year_str = get_text("TDRC") or get_text("TYER")
    if year_str:
        try:
            year = int(str(year_str)[:4])
        except ValueError:
            pass

    duration = int(audio.info.length) if audio.info else 0

    cover_data = None
    cover_mime = None
    for k in list(tags.keys()):
        if k.startswith("APIC"):
            pic = tags[k]
            cover_data = pic.data
            cover_mime = pic.mime
            break

    return {
        "title": title,
        "artist": artist,
        "album": album,
        "album_artist": album_artist,
        "track_no": track_no,
        "year": year,
        "duration": duration,
        "cover_data": cover_data,
        "cover_mime": cover_mime,
    }


def store_cover(album_id: str, tags) -> str | None:
    """Write embedded cover art to COVERS_DIR and return its filename."""
    if not tags["cover_data"]:
        return None
    mime = (tags["cover_mime"] or "").lower()
    ext = "jpg" if "jpeg" in mime or "jpg" in mime else "png"
    filename = f"{album_id}.{ext}"
    cover_path = COVERS_DIR / filename
    if cover_path.exists():
        return filename
    try:
        cover_path.write_bytes(tags["cover_data"])
    except Exception:
        log.warning("Cover konnte nicht geschrieben werden: %s", cover_path, exc_info=True)
        return None
    return filename


def _claim_scan() -> bool:
    """Reserve the scan slot. False if a scan is already running."""
    with _scan_lock:
        if scan_state["running"]:
            return False
        scan_state.update(running=True, progress=0, total=0, skipped=0, error=None)
        return True


def _release_scan() -> None:
    with _scan_lock:
        scan_state["running"] = False


def scan():
    """Run a full scan. No-op if one is already running."""
    if not _claim_scan():
        return
    run_claimed_scan()


def run_claimed_scan():
    """Scan body. The caller must have reserved the slot via _claim_scan()."""
    try:
        ensure_dirs()

        # Without this guard a missing music share (unmounted, renamed) would
        # look like an empty collection and overwrite a good library.json.
        if not MUSIC_DIR.is_dir():
            scan_state["error"] = f"Musikverzeichnis nicht gefunden: {MUSIC_DIR}"
            log.error("MUSIC_DIR ist kein Verzeichnis: %s", MUSIC_DIR)
            return

        mp3s = {p.resolve() for p in MUSIC_DIR.rglob("*.[mM][pP]3")}
        mp3s = sorted(mp3s)
        scan_state["total"] = len(mp3s)

        # Same protection for a share that is mounted but empty.
        if not mp3s and _library_has_albums():
            scan_state["error"] = (
                f"Keine MP3s unter {MUSIC_DIR} gefunden — bestehender Katalog "
                f"wurde nicht ueberschrieben. Zum Leeren DATA_DIR loeschen."
            )
            log.error("Leerer Scan bei vorhandenem Katalog — Abbruch, nichts geschrieben.")
            return

        albums = {}
        tracks_by_id = {}
        skipped = 0

        for i, path in enumerate(mp3s):
            tags = read_tags(path)
            if not tags:
                skipped += 1
                scan_state["skipped"] = skipped
                scan_state["progress"] = i + 1
                continue

            album_id = stable_id(tags["album_artist"], tags["album"])
            track_id = stable_id(str(path))

            if album_id not in albums:
                albums[album_id] = {
                    "id": album_id,
                    "title": tags["album"],
                    "artist": tags["album_artist"],
                    "year": None,
                    "cover": None,
                    "tracks": [],
                }

            album = albums[album_id]
            # Album-level metadata comes from whichever track carries it first,
            # not necessarily the first track of the album.
            if album["cover"] is None:
                album["cover"] = store_cover(album_id, tags)
            if album["year"] is None:
                album["year"] = tags["year"]

            album["tracks"].append({
                "id": track_id,
                "title": tags["title"],
                "artist": tags["artist"],
                "track_no": tags["track_no"],
                "duration": tags["duration"],
            })
            tracks_by_id[track_id] = str(path)
            scan_state["progress"] = i + 1

        for a in albums.values():
            a["tracks"].sort(key=lambda t: (
                t["track_no"] is None,
                t["track_no"] or 0,
                t["title"].lower(),
            ))

        library = {
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "album_count": len(albums),
            "track_count": sum(len(a["tracks"]) for a in albums.values()),
            "skipped_count": skipped,
            "albums": sorted(
                albums.values(),
                key=lambda a: (a["artist"].lower(), (a["year"] or 0), a["title"].lower()),
            ),
        }

        _write_json_atomic(LIBRARY_FILE, library)
        _write_json_atomic(TRACKS_FILE, tracks_by_id)

        scan_state["progress"] = scan_state["total"]
        if skipped:
            log.warning("Scan beendet, %d Datei(en) uebersprungen.", skipped)
    except Exception:
        # Keep filesystem details out of the API response; log them instead.
        log.exception("Scan fehlgeschlagen")
        scan_state["error"] = "Scan fehlgeschlagen — Details siehe Container-Log."
    finally:
        _release_scan()


def _library_has_albums() -> bool:
    """True if a non-empty catalog already exists on disk."""
    try:
        data = json.loads(LIBRARY_FILE.read_text(encoding="utf-8"))
        return bool(data.get("albums"))
    except Exception:
        return False


def _write_json_atomic(target: Path, payload) -> None:
    tmp = target.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    tmp.replace(target)


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_dirs()
    if not LIBRARY_FILE.exists() and MUSIC_DIR.exists():
        task = asyncio.create_task(asyncio.to_thread(scan))
        _startup_tasks.add(task)
        task.add_done_callback(_startup_tasks.discard)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index():
    return FileResponse(APP_DIR / "index.html", media_type="text/html")


@app.get("/api/library")
def get_library():
    if not LIBRARY_FILE.exists():
        return JSONResponse({
            "scanned_at": None,
            "albums": [],
            "album_count": 0,
            "track_count": 0,
            "skipped_count": 0,
        })
    return FileResponse(LIBRARY_FILE, media_type="application/json")


@app.get("/api/cover/{name}")
def get_cover(name: str):
    # filenames are always {hash}.{jpg|png} — reject anything else
    if "/" in name or "\\" in name or ".." in name:
        raise HTTPException(404)
    p = COVERS_DIR / name
    if not p.is_file():
        raise HTTPException(404)
    return FileResponse(p, headers={"Cache-Control": "public, max-age=86400"})


@app.get("/api/stream/{track_id}")
def stream(track_id: str):
    if not TRACKS_FILE.exists():
        raise HTTPException(404)
    tracks = json.loads(TRACKS_FILE.read_text(encoding="utf-8"))
    path = tracks.get(track_id)
    if not path:
        raise HTTPException(404)
    p = Path(path)
    if not p.is_file():
        raise HTTPException(404)
    # FastAPI/Starlette FileResponse handles HTTP Range requests for seeking
    return FileResponse(p, media_type="audio/mpeg")


@app.post("/api/scan")
def trigger_scan(background_tasks: BackgroundTasks):
    # Claim the slot here, not in the background task: BackgroundTasks only run
    # after the response is sent, so a status poll issued right after this POST
    # would otherwise still see running=False and stop polling.
    if not _claim_scan():
        return {"status": "already_running", **scan_state}
    background_tasks.add_task(run_claimed_scan)
    return {"status": "started", **scan_state}


@app.get("/api/scan/status")
def scan_status():
    return scan_state


if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
