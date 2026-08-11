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
import os
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

DATA_DIR.mkdir(parents=True, exist_ok=True)
COVERS_DIR.mkdir(parents=True, exist_ok=True)

scan_state = {"running": False, "progress": 0, "total": 0, "error": None}


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
    except Exception:
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


def scan():
    """Walk MUSIC_DIR, build albums dict, write library.json + tracks.json."""
    if scan_state["running"]:
        return
    scan_state["running"] = True
    scan_state["progress"] = 0
    scan_state["total"] = 0
    scan_state["error"] = None

    try:
        mp3s = {p.resolve() for p in MUSIC_DIR.rglob("*.[mM][pP]3")}
        mp3s = sorted(mp3s)
        scan_state["total"] = len(mp3s)

        albums = {}
        tracks_by_id = {}

        for i, path in enumerate(mp3s):
            scan_state["progress"] = i
            tags = read_tags(path)
            if not tags:
                continue

            album_id = stable_id(tags["album_artist"], tags["album"])
            track_id = stable_id(str(path))

            if album_id not in albums:
                cover_filename = None
                if tags["cover_data"]:
                    mime = (tags["cover_mime"] or "").lower()
                    ext = "jpg" if "jpeg" in mime or "jpg" in mime else "png"
                    cover_filename = f"{album_id}.{ext}"
                    cover_path = COVERS_DIR / cover_filename
                    if not cover_path.exists():
                        try:
                            cover_path.write_bytes(tags["cover_data"])
                        except Exception:
                            cover_filename = None

                albums[album_id] = {
                    "id": album_id,
                    "title": tags["album"],
                    "artist": tags["album_artist"],
                    "year": tags["year"],
                    "cover": cover_filename,
                    "tracks": [],
                }

            albums[album_id]["tracks"].append({
                "id": track_id,
                "title": tags["title"],
                "artist": tags["artist"],
                "track_no": tags["track_no"],
                "duration": tags["duration"],
            })
            tracks_by_id[track_id] = str(path)

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
            "albums": sorted(
                albums.values(),
                key=lambda a: (a["artist"].lower(), (a["year"] or 0), a["title"].lower()),
            ),
        }

        # atomic write
        tmp = LIBRARY_FILE.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(library, ensure_ascii=False), encoding="utf-8")
        tmp.replace(LIBRARY_FILE)

        tmp = TRACKS_FILE.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(tracks_by_id, ensure_ascii=False), encoding="utf-8")
        tmp.replace(TRACKS_FILE)

        scan_state["progress"] = scan_state["total"]
    except Exception as e:
        scan_state["error"] = str(e)
    finally:
        scan_state["running"] = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not LIBRARY_FILE.exists() and MUSIC_DIR.exists():
        asyncio.create_task(asyncio.to_thread(scan))
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
    if scan_state["running"]:
        return {"status": "already_running", **scan_state}
    background_tasks.add_task(scan)
    return {"status": "started"}


@app.get("/api/scan/status")
def scan_status():
    return scan_state


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
