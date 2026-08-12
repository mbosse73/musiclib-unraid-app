# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Musiklib: a minimal, fast music library for a personal MP3 collection. Runs as a small Docker container on an unraid NAS, scans a music directory, and serves a single HTML page with search and an integrated player, reachable from any device on the network. No database — everything the app knows lives in `library.json`.

The application the container runs is still three files:
- `app.py` — FastAPI backend: scanning, JSON API, streaming.
- `index.html` — the entire frontend: HTML + CSS + vanilla JS in one file, no build step, no framework.
- `requirements.txt` — pinned deps: `fastapi`, `starlette`, `mutagen`, `uvicorn`, `uvloop`, `httptools`. `starlette` is pinned explicitly even though it only arrives via FastAPI: it provides the `FileResponse` that implements Range streaming, and versions before 1.3.1 parse Range headers in quadratic time (a single request stalls the event loop for minutes). `uvicorn` is installed without the `[standard]` extra — `uvloop` and `httptools` are listed directly instead, so the unused `websockets`/`watchfiles`/`PyYAML`/`python-dotenv` don't get pulled in.

`conftest.py`, `test_app.py`, `test_frontend.py` and `requirements-dev.txt` exist only for local development — the compose `command` installs `requirements.txt` alone, so none of them ever reaches the container. `docker-compose.yml` and `README.md` (in German) cover unraid deployment; not relevant to app logic.

## Running locally

There is no linter and no build step. There *is* a pytest suite; run it before and after changes.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m playwright install chromium   # once, for test_frontend.py
.venv/bin/python -m pytest -q            # 51 tests, ~16 s
.venv/bin/python -m pytest -q test_app.py        # backend only, <1 s
.venv/bin/python -m pytest -q -k session         # one group
MUSIC_DIR=/path/to/some/mp3s DATA_DIR=./data .venv/bin/python app.py   # serves on :8080
```

`test_app.py` covers the backend in-process via `TestClient`: Range requests returning 206, cover-endpoint path traversal, the guards that stop a scan from wiping the catalog, cover extraction from a non-first track and from folder images, the tag cache, and the scan lock.

`test_frontend.py` drives `index.html` in a real Chromium against `app.py` in a subprocess: search (incl. by track title), sorting, the player and its button/audio synchronisation, volume, shuffle, keyboard shortcuts, and session restore. Without the `playwright` package or a usable browser the whole module skips and the backend tests still run — so a missing browser is never a red suite. `MUSIKLIB_CHROME=/path/to/chrome` overrides browser discovery.

Both files share MP3 fixture builders and the `app_env` fixture from `conftest.py`; the suite needs no audio files of its own. The frontend context blocks `fonts.googleapis.com`, so the tests neither wait on the network nor depend on internet access — keep that when adding pages, or the suite slows down by more than an order of magnitude.

```powershell
$env:MUSIC_DIR = "C:\path\to\some\mp3s"   # defaults to /music
$env:DATA_DIR = ".\data"                   # defaults to /data
python app.py                              # PORT env var to change the port
```

Open `http://localhost:8080`. Startup triggers a scan **only if `library.json` does not exist** — to force a re-scan during development, delete `DATA_DIR` or `POST /api/scan`.

A fresh checkout has no music to scan. `conftest.py`'s `write_mp3()` / `frames()` build fixtures without any audio files on hand: raw MPEG1 Layer III frames (a `\xff\xfb\x90\x00` header + zero padding to 417 bytes, repeated) tagged with `mutagen.id3`; `MP3()` parses these fine and reports a duration. Use the same helpers when scanning a directory by hand.

One trap the frontend tests already ran into: fixture tracks must be **long enough that playback does not run past them** during a test (`TRACK_SECONDS = 30`). With one-second tracks the queue advances between assertions and failures look like real bugs.

`.venv/` and `data/` are gitignored.

## Architecture

**Backend (`app.py`)** does three things:
1. **Scan** (`scan()` → `run_claimed_scan()`) — walks `MUSIC_DIR` recursively for `*.mp3`, reads ID3 tags via `mutagen`, groups tracks into albums (album identity = `stable_id(album_artist, album)`, a truncated SHA1), stores cover art to `DATA_DIR/covers/{album_id}.{jpg|png}`, and atomically writes three files:
   - `DATA_DIR/library.json` — the public, flat album/track structure served to the frontend as-is via `FileResponse`.
   - `DATA_DIR/tracks.json` — an internal `track_id -> absolute filesystem path` map, never exposed to the client; used only by `/api/stream/{track_id}` to resolve playback paths.
   - `DATA_DIR/tagcache.json` — an internal `path -> {mtime_ns, size, tags}` map so the next scan can skip files that have not changed. Guarded by `TAGCACHE_VERSION`: **bump it whenever `read_tags()` changes its output shape**, otherwise stale entries silently survive.
   Scan state (`scan_state` global dict: running/progress/total/skipped/skipped_files/error) is polled by the frontend during a scan and is **not** persisted — it resets on restart.

   `run_claimed_scan()` is deliberately split: `_guard_music_dir()`, `_collect_mp3s()`, `_build_albums()` (the loop, incl. cache lookups), `_finalise_albums()` (track sorting + folder-cover fallback), then writing and `prune_covers()`. Cover art is fetched by `read_cover()` separately from `read_tags()` — that keeps `read_tags()`'s return value JSON-serialisable and therefore cacheable, which is the whole basis of the incremental scan. Don't merge them back.
2. **Serve** — `/` returns `index.html` as-is; `/api/library` returns `library.json` as-is (no per-request transformation, no pagination — the frontend receives and filters the whole collection client-side).
3. **Stream** — `/api/stream/{track_id}` resolves the id via `tracks.json` and returns a `FileResponse`; Starlette's `FileResponse` handles HTTP Range requests natively, which is what makes seeking work.

Scans are triggered two ways: automatically on startup if `library.json` doesn't exist yet (`lifespan` handler, runs in a background thread via `asyncio.to_thread`), or manually via `POST /api/scan` (also backgrounded, via `BackgroundTasks`). There is deliberately no periodic/automatic re-scan — it's manual only, to avoid waking an idle NAS. Re-running the app never triggers a rescan once `library.json` exists, even if the source files changed.

Because there's no database, `scan()` is the single source of truth for how raw ID3 tags become album/track records — read this function fully before changing library shape or the JSON schema the frontend consumes.

### Consequences of the no-database design

These follow from the code above and are easy to trip over:

- **`track_id` is a hash of the absolute file path.** Moving or renaming an MP3 gives it a new id on the next scan, invalidating anything that stored the old one. Nothing currently persists track ids across scans — keep it that way, or the assumption breaks.
- **`DATA_DIR` is now maintained, not just appended to.** `prune_covers()` deletes cover files no album references any more, and `_write_cover()` compares content before writing, so a swapped cover of an otherwise unchanged album *is* picked up. Deleting `DATA_DIR` is still the way to force a full rebuild, but it is no longer needed for routine cover changes.
- **Rescans are incremental.** Files whose `mtime_ns` and `size` match `tagcache.json` are not re-parsed. That makes repeated scans cheap, and it is why the cache version guard matters: a change to `read_tags()` without a `TAGCACHE_VERSION` bump would leave stale data in the catalog indefinitely.
- **Album cover art has two sources.** Embedded `APIC` first; if no track in the album carries one, `_finalise_albums()` falls back to `cover.jpg`/`folder.jpg`/`front.jpg`/`albumart.*`/`album.*` in the directories that album's files live in.
- **A scan refuses to replace a non-empty catalog with an empty one.** If `MUSIC_DIR` is not a directory, or if it yields zero MP3s while `library.json` still lists albums, `run_claimed_scan()` reports an error in `scan_state["error"]` and writes nothing. Without that guard an unmounted or renamed music share would silently wipe the catalog, because `Path.rglob()` on a missing directory returns an empty iterator instead of raising. Deliberately emptying the library therefore means deleting `DATA_DIR`, not scanning an empty folder.
- **Skipped files are counted and named, not silent.** `read_tags()` still returns `None` on any exception, but the scan counts those files into `scan_state["skipped"]` / `library.json`'s `skipped_count` and records the first `MAX_SKIPPED_REPORTED` names in `skipped_files`, logging one line each. Those names are always relative to `MUSIC_DIR` (`_relative_to_music()`) — `library.json` goes to the browser, so never put an absolute path in it.
- **Album-level fields come from whichever track carries them first**, not from the album's first track. Cover art and `year` are filled in the first time any track of that album supplies them — an intro track without embedded art no longer leaves the whole album coverless.
- **`scan_state` is guarded by `_scan_lock`.** `_claim_scan()` does the check-and-set atomically and `POST /api/scan` claims the slot *before* returning, so a status poll issued immediately after the POST always observes `running: true`. Don't reintroduce a bare flag check.
- **`/api/stream` resolves paths through `_load_tracks()`**, which keeps `tracks.json` parsed in memory and reloads only when its mtime/size change. Don't go back to reading the file per request — every Range request during seeking hits this path.
- **`scan_state["error"]` is a short, user-facing German message**, rendered as-is in the UI. Exception detail goes to the log via `log.exception`, not into the API response.

**Frontend (`index.html`)** is one file with three parts in this order: `<style>` (CSS custom properties at the top of `:root` centralize theme — colors, fonts, `--player-h` — change those instead of scattering literal values), the DOM skeleton, then a single `<script>` with no modules/bundler. Key frontend concepts:
- `library` (fetched from `/api/library`) is the full in-memory dataset; `filtered` is the current search-filtered subset; both are plain arrays of album objects re-rendered on every filter/tab change (no virtual DOM/diffing).
- `queue` + `qIndex` model the play queue: clicking a track loads the whole album into `queue` starting at that index, so next/prev just moves `qIndex`.
- Playback state is driven off the single `<audio>` element's native events; there is no separate player state object. The play/pause button is updated **only** from the `play`/`pause` events via `setPlayButton()` — never set it optimistically next to an `audio.play()` call, or it desyncs the moment playback is controlled from outside the page (lockscreen, media keys, blocked autoplay). `playCurrent()` is the one place that changes what's playing; it also refreshes the Media Session metadata. `playNext()`/`playPrev()`/`togglePlay()` are shared by the player buttons and the Media Session action handlers, so lockscreen controls move the same queue.
- The `error` event on `<audio>` reports a track whose file moved since the last scan (the stream 404s). Without a handler the player just stops silently, so keep one.
- `groupByArtist()` derives the artist view from `library.albums` on the fly — there is no separate artists endpoint or artist data structure server-side.
- Search matches against `a._q`, a lowercase blob of album title, album artist and every track title/artist built once per load by `indexLibrary()`. Rebuild it whenever `library` is replaced; matching per keystroke is then a single `includes()` per album. `applyFilter()` also sorts, always into a **new** array — `library.albums` itself must stay in backend order.
- `SORTERS` holds the sort modes offered in the header; the chosen one is persisted under `musiklib:sort`. "Zuletzt hinzugefügt" reads `album.added_at`, which the backend derives from file mtimes.
- `loadQueue()` is the only place a queue is established — it applies shuffle by keeping the chosen track first and shuffling the rest. `playFromAlbum()` and `playArtist()` both go through it.
- Session continuity lives in `localStorage` under `musiklib:*` (`session`, `volume`, `muted`, `shuffle`, `sort`). `restoreSession()` rebuilds the queue from stored `[albumId, trackId]` pairs and silently drops entries that no longer resolve — which is what happens after files move, since `track_id` is path-derived. It never autoplays. All storage access goes through `store()`/`restore()`, which swallow failures: a browser with storage disabled must still run the app.
- `.album` carries `content-visibility: auto` with `contain-intrinsic-size`. If you change the card layout, update that size hint too, or scrolling a large library will jump.
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
