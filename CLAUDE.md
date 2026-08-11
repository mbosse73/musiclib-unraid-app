# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Musiklib: a minimal, fast music library for a personal MP3 collection. Runs as a small Docker container on an unraid NAS, scans a music directory, and serves a single HTML page with search and an integrated player, reachable from any device on the network. No database — everything the app knows lives in `library.json`.

The application is three files:
- `app.py` — FastAPI backend (~270 lines): scanning, JSON API, streaming.
- `index.html` — the entire frontend (~1100 lines): HTML + CSS + vanilla JS in one file, no build step, no framework.
- `requirements.txt` — pinned deps: `fastapi`, `starlette`, `mutagen`, `uvicorn`, `uvloop`, `httptools`. `starlette` is pinned explicitly even though it only arrives via FastAPI: it provides the `FileResponse` that implements Range streaming, and versions before 1.3.1 parse Range headers in quadratic time (a single request stalls the event loop for minutes). `uvicorn` is installed without the `[standard]` extra — `uvloop` and `httptools` are listed directly instead, so the unused `websockets`/`watchfiles`/`PyYAML`/`python-dotenv` don't get pulled in.

`docker-compose.yml` and `README.md` (in German) cover unraid deployment; not relevant to app logic.

## Running locally

No test suite, linter, or build step exists in this repo. Verification is manual: start the app and exercise the endpoints.

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
MUSIC_DIR=/path/to/some/mp3s DATA_DIR=./data .venv/bin/python app.py   # serves on :8080
```

```powershell
$env:MUSIC_DIR = "C:\path\to\some\mp3s"   # defaults to /music
$env:DATA_DIR = ".\data"                   # defaults to /data
python app.py                              # PORT env var to change the port
```

Open `http://localhost:8080`. Startup triggers a scan **only if `library.json` does not exist** — to force a re-scan during development, delete `DATA_DIR` or `POST /api/scan`.

A fresh checkout has no music to scan. To create test fixtures without any audio files on hand, write raw MPEG1 Layer III frames (a `\xff\xfb\x90\x00` header + zero padding to 417 bytes, repeated) and tag them with `mutagen.id3`; `MP3()` parses these fine and reports a duration. Cover a few cases at once — fully tagged, partially tagged, untagged (exercises the "Unbekanntes Album" fallbacks), and a non-MP3 file named `.mp3` (must be silently skipped).

Worth checking after backend changes, since nothing else will catch a regression:
- `curl -H 'Range: bytes=0-99' .../api/stream/{id}` must return `206` with a `Content-Range` header — seeking on mobile depends on it.
- `/api/cover/{name}` must reject `..`, `/` and `\` with a 404.

`.venv/` and `data/` are gitignored.

## Architecture

**Backend (`app.py`)** does three things:
1. **Scan** (`scan()`) — walks `MUSIC_DIR` recursively for `*.mp3`, reads ID3 tags via `mutagen`, groups tracks into albums (album identity = `stable_id(album_artist, album)`, a truncated SHA1), extracts embedded cover art to `DATA_DIR/covers/{album_id}.{jpg|png}`, and atomically writes two files:
   - `DATA_DIR/library.json` — the public, flat album/track structure served to the frontend as-is via `FileResponse`.
   - `DATA_DIR/tracks.json` — an internal `track_id -> absolute filesystem path` map, never exposed to the client; used only by `/api/stream/{track_id}` to resolve playback paths.
   Scan state (`scan_state` global dict: running/progress/total/error) is polled by the frontend during a scan and is **not** persisted — it resets on restart.
2. **Serve** — `/` returns `index.html` as-is; `/api/library` returns `library.json` as-is (no per-request transformation, no pagination — the frontend receives and filters the whole collection client-side).
3. **Stream** — `/api/stream/{track_id}` resolves the id via `tracks.json` and returns a `FileResponse`; Starlette's `FileResponse` handles HTTP Range requests natively, which is what makes seeking work.

Scans are triggered two ways: automatically on startup if `library.json` doesn't exist yet (`lifespan` handler, runs in a background thread via `asyncio.to_thread`), or manually via `POST /api/scan` (also backgrounded, via `BackgroundTasks`). There is deliberately no periodic/automatic re-scan — it's manual only, to avoid waking an idle NAS. Re-running the app never triggers a rescan once `library.json` exists, even if the source files changed.

Because there's no database, `scan()` is the single source of truth for how raw ID3 tags become album/track records — read this function fully before changing library shape or the JSON schema the frontend consumes.

### Consequences of the no-database design

These follow from the code above and are easy to trip over:

- **`track_id` is a hash of the absolute file path.** Moving or renaming an MP3 gives it a new id on the next scan, invalidating anything that stored the old one. Nothing currently persists track ids across scans — keep it that way, or the assumption breaks.
- **Nothing is ever deleted from `DATA_DIR`.** `scan()` only writes. Covers for albums that no longer exist stay on disk, and a cover file is written only when one doesn't already exist at that path — so a changed cover for an unchanged album is *not* picked up by a re-scan. A full rebuild means deleting `DATA_DIR`.
- **A scan refuses to replace a non-empty catalog with an empty one.** If `MUSIC_DIR` is not a directory, or if it yields zero MP3s while `library.json` still lists albums, `run_claimed_scan()` reports an error in `scan_state["error"]` and writes nothing. Without that guard an unmounted or renamed music share would silently wipe the catalog, because `Path.rglob()` on a missing directory returns an empty iterator instead of raising. Deliberately emptying the library therefore means deleting `DATA_DIR`, not scanning an empty folder.
- **Skipped files are counted, not silent.** `read_tags()` still returns `None` on any exception, but `scan()` now counts those files into `scan_state["skipped"]` and `library.json`'s `skipped_count`, and logs one line per file. The frontend surfaces the count in the header.
- **Album-level fields come from whichever track carries them first**, not from the album's first track. Cover art and `year` are filled in the first time any track of that album supplies them — an intro track without embedded art no longer leaves the whole album coverless.
- **`scan_state` is guarded by `_scan_lock`.** `_claim_scan()` does the check-and-set atomically and `POST /api/scan` claims the slot *before* returning, so a status poll issued immediately after the POST always observes `running: true`. Don't reintroduce a bare flag check.
- **`/api/stream` re-reads and JSON-parses all of `tracks.json` on every request**, including every Range request while seeking. It's the hot path if streaming ever feels slow.
- **`scan_state["error"]` is a short, user-facing German message**, rendered as-is in the UI. Exception detail goes to the log via `log.exception`, not into the API response.

**Frontend (`index.html`)** is one file with three parts in this order: `<style>` (CSS custom properties at the top of `:root` centralize theme — colors, fonts, `--player-h` — change those instead of scattering literal values), the DOM skeleton, then a single `<script>` with no modules/bundler. Key frontend concepts:
- `library` (fetched from `/api/library`) is the full in-memory dataset; `filtered` is the current search-filtered subset; both are plain arrays of album objects re-rendered on every filter/tab change (no virtual DOM/diffing).
- `queue` + `qIndex` model the play queue: clicking a track loads the whole album into `queue` starting at that index, so next/prev just moves `qIndex`.
- Playback state is driven off the single `<audio>` element's native events; there is no separate player state object. The play/pause button is updated **only** from the `play`/`pause` events via `setPlayButton()` — never set it optimistically next to an `audio.play()` call, or it desyncs the moment playback is controlled from outside the page (lockscreen, media keys, blocked autoplay). `playCurrent()` is the one place that changes what's playing; it also refreshes the Media Session metadata. `playNext()`/`playPrev()`/`togglePlay()` are shared by the player buttons and the Media Session action handlers, so lockscreen controls move the same queue.
- The `error` event on `<audio>` reports a track whose file moved since the last scan (the stream 404s). Without a handler the player just stops silently, so keep one.
- `groupByArtist()` derives the artist view from `library.albums` on the fly — there is no separate artists endpoint or artist data structure server-side.
- `albumMatches()` decides what the search finds: album title, album artist, and every track title/artist. It runs over the whole collection on each keystroke (debounced 80 ms) — cheap string matching, but it is the first thing to feel slow on a very large library.
- `pollScan()` re-polls `/api/scan/status` every 600ms while a scan runs and calls `loadLibrary()` once it finishes; this is the only path that refreshes the library after startup.
- The page loads IBM Plex Mono from Google Fonts (`<link>` in `<head>`). A NAS without internet access falls back to the system monospace — the layout survives, but don't assume the webfont is present.

**Data flow contract**: the backend never mutates `library.json` structure per-request and the frontend never talks to the filesystem — all album/track shape decisions belong in `scan()`/`read_tags()`, and all display/filtering logic belongs in `index.html`. Keep that boundary when adding fields (e.g., a new ID3 tag needs to flow through `read_tags` → `scan` → `library.json` → frontend render code, in that order).

## Conventions worth preserving

- No database, no ORM — flat JSON files by design (see README "Was die App nicht macht"). Don't introduce one for small features.
- No build tooling for the frontend — keep `index.html` a single static file editable via SMB and reloadable without a container restart (per README, this is a deployment requirement, not just a style choice).
- Deployment installs dependencies at container start (`pip install -r requirements.txt` in the compose `command`, no image build), so adding a dependency requires a full container stop/start, not a restart. Keep `requirements.txt` small and pinned.
- Cover filenames are content-addressed (`{album_id}.{ext}`) and validated against path traversal in `/api/cover/{name}` (rejects `/`, `\`, `..`) — preserve that check if touching that endpoint.
- User-facing strings in `index.html` are German; the backend's tag fallbacks (`"Unbekanntes Album"`, `"Unbekannter Interpret"`) are too. Match that when adding UI text.
- `README.md` is in German and documents unraid-specific deployment/troubleshooting in detail; consult it before changing deployment-relevant behavior (env vars, ports, volume expectations).
