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
TAGCACHE_FILE = DATA_DIR / "tagcache.json"  # internal: path -> cached tags
APP_DIR = Path(__file__).parent

# Bump whenever read_tags() changes its output shape — every cached entry
# is then discarded and the next scan re-reads all files.
TAGCACHE_VERSION = 1

# Checked next to the audio files when an album has no embedded cover art.
FOLDER_COVER_STEMS = ("cover", "folder", "front", "albumart", "album")
FOLDER_COVER_EXTS = (".jpg", ".jpeg", ".png")

# Unreadable files are reported by name in the UI, but only up to this many.
MAX_SKIPPED_REPORTED = 50

log = logging.getLogger("musiklib")

# Guards the check-then-set on scan_state["running"]. scan() runs in a worker
# thread while request handlers read the state, so the flag alone is not enough.
_scan_lock = threading.Lock()

# Strong references to startup tasks; asyncio only holds weak ones.
_startup_tasks: set = set()

# tracks.json is read on every stream request, including every Range request
# while seeking — keep it parsed in memory and refresh it only when it changes.
_tracks_cache = {"key": None, "data": {}}

scan_state = {
    "running": False,
    "progress": 0,
    "total": 0,
    "skipped": 0,  # files that could not be read and were left out
    "skipped_files": [],  # first MAX_SKIPPED_REPORTED of them, relative to MUSIC_DIR
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


# --------------------------------------------------------------------------
# reading tags
# --------------------------------------------------------------------------

def read_tags(filepath: Path):
    """Text metadata for one MP3, or None if it cannot be read.

    Deliberately excludes the cover image: everything returned here is
    JSON-serialisable and therefore cacheable across scans. Cover bytes are
    fetched separately by read_cover(), and only for albums that need one.
    """
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

    return {
        "title": title,
        "artist": artist,
        "album": album,
        "album_artist": album_artist,
        "track_no": track_no,
        "year": year,
        "duration": int(audio.info.length) if audio.info else 0,
        "has_cover": any(k.startswith("APIC") for k in tags.keys()),
    }


def read_cover(filepath: Path):
    """Return (bytes, mime) of the first embedded cover, or None."""
    try:
        tags = MP3(filepath).tags or {}
        for k in list(tags.keys()):
            if k.startswith("APIC"):
                pic = tags[k]
                return pic.data, pic.mime
    except Exception:
        log.warning("Cover konnte nicht gelesen werden: %s", filepath)
    return None


def find_folder_cover(directory: Path):
    """Find cover.jpg / folder.jpg / ... next to the audio files.

    Many collections keep artwork as a file instead of embedding it; without
    this those albums would render as a bare letter placeholder.
    """
    try:
        entries = list(directory.iterdir())
    except OSError:
        return None
    for entry in entries:
        if not entry.is_file():
            continue
        if entry.suffix.lower() not in FOLDER_COVER_EXTS:
            continue
        if entry.stem.lower() in FOLDER_COVER_STEMS:
            return entry
    return None


# --------------------------------------------------------------------------
# cover storage
# --------------------------------------------------------------------------

def _cover_filename(album_id: str, mime_or_suffix: str) -> str:
    m = (mime_or_suffix or "").lower()
    ext = "jpg" if "jpeg" in m or "jpg" in m else "png"
    return f"{album_id}.{ext}"


def _write_cover(album_id: str, data: bytes, mime_or_suffix: str):
    """Write cover bytes unless an identical file is already there."""
    filename = _cover_filename(album_id, mime_or_suffix)
    path = COVERS_DIR / filename
    try:
        if path.exists() and path.stat().st_size == len(data):
            # Same size is not proof — compare content so a swapped cover of an
            # otherwise unchanged album actually gets picked up.
            if path.read_bytes() == data:
                return filename
        path.write_bytes(data)
    except Exception:
        log.warning("Cover konnte nicht geschrieben werden: %s", path, exc_info=False)
        return None
    return filename


def store_embedded_cover(album_id: str, filepath: Path):
    found = read_cover(filepath)
    if not found:
        return None
    data, mime = found
    return _write_cover(album_id, data, mime)


def store_folder_cover(album_id: str, directory: Path):
    image = find_folder_cover(directory)
    if not image:
        return None
    try:
        data = image.read_bytes()
    except OSError:
        return None
    return _write_cover(album_id, data, image.suffix)


def prune_covers(keep: set) -> int:
    """Delete cover files that no album references any more."""
    removed = 0
    try:
        entries = list(COVERS_DIR.iterdir())
    except OSError:
        return 0
    for entry in entries:
        if entry.is_file() and entry.name not in keep:
            try:
                entry.unlink()
                removed += 1
            except OSError:
                pass
    return removed


# --------------------------------------------------------------------------
# tag cache
# --------------------------------------------------------------------------

def load_tagcache() -> dict:
    """Previously read tags, keyed by path. Empty dict if unusable."""
    try:
        raw = json.loads(TAGCACHE_FILE.read_text(encoding="utf-8"))
        if raw.get("version") != TAGCACHE_VERSION:
            log.info("Tag-Cache verworfen (Version %s statt %s).",
                     raw.get("version"), TAGCACHE_VERSION)
            return {}
        return raw.get("entries") or {}
    except FileNotFoundError:
        return {}
    except Exception:
        log.warning("Tag-Cache unlesbar, wird neu aufgebaut.")
        return {}


def save_tagcache(entries: dict) -> None:
    _write_json_atomic(TAGCACHE_FILE, {"version": TAGCACHE_VERSION, "entries": entries})


# --------------------------------------------------------------------------
# scanning
# --------------------------------------------------------------------------

def _claim_scan() -> bool:
    """Reserve the scan slot. False if a scan is already running."""
    with _scan_lock:
        if scan_state["running"]:
            return False
        scan_state.update(running=True, progress=0, total=0, skipped=0,
                          skipped_files=[], error=None)
        return True


def _release_scan() -> None:
    with _scan_lock:
        scan_state["running"] = False


def scan():
    """Run a full scan. No-op if one is already running."""
    if not _claim_scan():
        return
    run_claimed_scan()


def _guard_music_dir() -> str | None:
    """Return an error message if scanning would destroy the catalog."""
    # Path.rglob() on a missing directory yields nothing instead of raising,
    # so an unmounted share would silently look like an empty collection.
    if not MUSIC_DIR.is_dir():
        return f"Musikverzeichnis nicht gefunden: {MUSIC_DIR}"
    return None


def _collect_mp3s() -> list:
    return sorted({p.resolve() for p in MUSIC_DIR.rglob("*.[mM][pP]3")})


def _relative_to_music(path: Path) -> str:
    """Path as shown in the UI — never an absolute filesystem path."""
    for base in (MUSIC_DIR, MUSIC_DIR.resolve()):
        try:
            return str(path.relative_to(base))
        except ValueError:
            continue
    return path.name


def _build_albums(paths: list, cache: dict) -> dict:
    """Group files into albums, reusing cached tags for unchanged files."""
    albums = {}
    tracks_by_id = {}
    album_dirs = {}
    fresh_cache = {}
    skipped_names = []
    skipped = 0
    cache_hits = 0

    for i, path in enumerate(paths):
        key = str(path)
        try:
            st = path.stat()
        except OSError:
            skipped += 1
            if len(skipped_names) < MAX_SKIPPED_REPORTED:
                skipped_names.append(_relative_to_music(path))
            scan_state["skipped"] = skipped
            scan_state["progress"] = i + 1
            continue

        cached = cache.get(key)
        if cached and cached.get("mtime_ns") == st.st_mtime_ns and cached.get("size") == st.st_size:
            tags = cached["tags"]
            cache_hits += 1
        else:
            tags = read_tags(path)
            if not tags:
                skipped += 1
                if len(skipped_names) < MAX_SKIPPED_REPORTED:
                    skipped_names.append(_relative_to_music(path))
                scan_state["skipped"] = skipped
                scan_state["skipped_files"] = list(skipped_names)
                scan_state["progress"] = i + 1
                continue

        fresh_cache[key] = {"mtime_ns": st.st_mtime_ns, "size": st.st_size, "tags": tags}

        album_id = stable_id(tags["album_artist"], tags["album"])
        track_id = stable_id(key)

        if album_id not in albums:
            albums[album_id] = {
                "id": album_id,
                "title": tags["album"],
                "artist": tags["album_artist"],
                "year": None,
                "cover": None,
                "added_at": 0,
                "tracks": [],
            }
            album_dirs[album_id] = []

        album = albums[album_id]
        if path.parent not in album_dirs[album_id]:
            album_dirs[album_id].append(path.parent)

        # Album-level metadata comes from whichever track carries it first,
        # not necessarily the first track of the album.
        if album["cover"] is None and tags.get("has_cover"):
            album["cover"] = store_embedded_cover(album_id, path)
        if album["year"] is None:
            album["year"] = tags["year"]
        album["added_at"] = max(album["added_at"], int(st.st_mtime))

        album["tracks"].append({
            "id": track_id,
            "title": tags["title"],
            "artist": tags["artist"],
            "track_no": tags["track_no"],
            "duration": tags["duration"],
        })
        tracks_by_id[track_id] = key
        scan_state["progress"] = i + 1

    scan_state["skipped"] = skipped
    scan_state["skipped_files"] = list(skipped_names)
    return {
        "albums": albums,
        "tracks_by_id": tracks_by_id,
        "album_dirs": album_dirs,
        "fresh_cache": fresh_cache,
        "skipped_names": skipped_names,
        "cache_hits": cache_hits,
    }


def _finalise_albums(albums: dict, album_dirs: dict) -> None:
    """Sort tracks and fill in cover art from folder images where needed."""
    for album_id, album in albums.items():
        album["tracks"].sort(key=lambda t: (
            t["track_no"] is None,
            t["track_no"] or 0,
            t["title"].lower(),
        ))
        if album["cover"] is None:
            for directory in album_dirs.get(album_id, []):
                album["cover"] = store_folder_cover(album_id, directory)
                if album["cover"]:
                    break


def run_claimed_scan():
    """Scan body. The caller must have reserved the slot via _claim_scan()."""
    try:
        ensure_dirs()

        error = _guard_music_dir()
        if error:
            scan_state["error"] = error
            log.error("Scan abgebrochen: %s", error)
            return

        paths = _collect_mp3s()
        scan_state["total"] = len(paths)

        # Same protection for a share that is mounted but empty.
        if not paths and _library_has_albums():
            scan_state["error"] = (
                f"Keine MP3s unter {MUSIC_DIR} gefunden — bestehender Katalog "
                f"wurde nicht ueberschrieben. Zum Leeren DATA_DIR loeschen."
            )
            log.error("Leerer Scan bei vorhandenem Katalog — Abbruch, nichts geschrieben.")
            return

        result = _build_albums(paths, load_tagcache())
        albums = result["albums"]
        _finalise_albums(albums, result["album_dirs"])

        library = {
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "album_count": len(albums),
            "track_count": sum(len(a["tracks"]) for a in albums.values()),
            "skipped_count": scan_state["skipped"],
            "skipped_files": result["skipped_names"],
            "albums": sorted(
                albums.values(),
                key=lambda a: (a["artist"].lower(), (a["year"] or 0), a["title"].lower()),
            ),
        }

        _write_json_atomic(LIBRARY_FILE, library)
        _write_json_atomic(TRACKS_FILE, result["tracks_by_id"])
        save_tagcache(result["fresh_cache"])

        removed = prune_covers({a["cover"] for a in albums.values() if a["cover"]})

        scan_state["progress"] = scan_state["total"]
        log.info("Scan fertig: %d Alben, %d Titel, %d aus Cache, %d uebersprungen, "
                 "%d verwaiste Cover geloescht.",
                 library["album_count"], library["track_count"], result["cache_hits"],
                 scan_state["skipped"], removed)
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


def _load_tracks() -> dict:
    """tracks.json, parsed at most once per change."""
    try:
        st = TRACKS_FILE.stat()
    except OSError:
        _tracks_cache["key"] = None
        _tracks_cache["data"] = {}
        return {}
    key = (st.st_mtime_ns, st.st_size)
    if _tracks_cache["key"] != key:
        try:
            _tracks_cache["data"] = json.loads(TRACKS_FILE.read_text(encoding="utf-8"))
            _tracks_cache["key"] = key
        except Exception:
            log.exception("tracks.json unlesbar")
            return {}
    return _tracks_cache["data"]


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_dirs()
    if not LIBRARY_FILE.exists() and MUSIC_DIR.exists():
        task = asyncio.create_task(asyncio.to_thread(scan))
        _startup_tasks.add(task)
        task.add_done_callback(_startup_tasks.discard)
    yield


app = FastAPI(lifespan=lifespan)


def _seite(name: str) -> FileResponse:
    """Eine der vier Oberflaechen ausliefern.

    Der Code wird per SMB kopiert, Datei fuer Datei — dabei bleibt leicht
    eine liegen. Ohne diese Pruefung wirft FileResponse tief im Server einen
    RuntimeError, und im Browser steht nur „Internal Server Error"; welche
    Datei fehlt, sieht man erst im Containerlog. Ein Satz, der sie beim
    Namen nennt, ist an dieser Stelle mehr wert.
    """
    p = APP_DIR / name
    if not p.is_file():
        log.error("Oberflaeche %s fehlt in %s", name, APP_DIR)
        raise HTTPException(
            404, f"{name} liegt nicht im Ordner der App ({APP_DIR}) — Datei nachkopieren.")
    return FileResponse(p, media_type="text/html")


@app.get("/")
def index():
    return _seite("index.html")


@app.get("/mobil")
def mobile():
    """Handy-Oberflaeche — dieselben Endpunkte, eigene Bedienung.

    Bewusst keine Weiterleitung nach Geraetekennung: iPad-Safari meldet sich
    als Schreibtisch, die Erkennung ginge also schief. Wer sie will, ruft
    /mobil auf und legt sie auf den Home-Bildschirm.
    """
    return _seite("mobile.html")


@app.get("/ipad")
@app.get("/pc")
def player():
    """Spieler fuer iPad und Schreibtisch — eine Datei, zwoelf Ansichten.

    Zwei Adressen auf dieselbe Datei: welche Ansicht passt, entscheidet nicht
    das Geraet, sondern der Benutzer (auch hier meldet sich iPad-Safari als
    Schreibtisch). Die Wahl liegt im localStorage, die Adresse ist nur der
    Weg dorthin.
    """
    return _seite("player.html")


@app.get("/tag")
def tag():
    """Album des Tages — ein Spieler mit genau einem Knopf.

    Die kleinste der vier Oberflaechen: kein Scan, keine Bibliothek, keine
    Suche, kein Weiter. Gespielt wird ein Album, das der Browser aus dem
    Datum errechnet — der Server weiss davon nichts und braucht dafuer auch
    kein Feld in library.json.
    """
    return _seite("tag.html")


@app.get("/api/library")
def get_library():
    if not LIBRARY_FILE.exists():
        return JSONResponse({
            "scanned_at": None,
            "albums": [],
            "album_count": 0,
            "track_count": 0,
            "skipped_count": 0,
            "skipped_files": [],
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
    path = _load_tracks().get(track_id)
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
