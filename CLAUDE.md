# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Musiklib: a minimal, fast music library for a personal MP3 collection. Runs as a small Docker container on an unraid NAS, scans a music directory, and serves a single HTML page with search and an integrated player, reachable from any device on the network. No database — everything the app knows lives in `library.json`.

The entire project is three files:
- `app.py` — FastAPI backend (~270 lines): scanning, JSON API, streaming.
- `index.html` — the entire frontend: HTML + CSS + vanilla JS in one file, no build step, no framework.
- `requirements.txt` — pinned deps: `fastapi`, `uvicorn[standard]`, `mutagen`.

`docker-compose.yml` and `README.md` (in German) cover unraid deployment; not relevant to app logic.

## Running locally

No test suite, linter, or build step exists in this repo.

```powershell
pip install -r requirements.txt
$env:MUSIC_DIR = "C:\path\to\some\mp3s"   # defaults to /music
$env:DATA_DIR = ".\data"                   # defaults to /data
python app.py                              # serves on :8080 (PORT env var to change)
```

Open `http://localhost:8080`. First request with no existing `library.json` triggers an automatic background scan.

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

**Frontend (`index.html`)** is one file with three parts in this order: `<style>` (CSS custom properties at the top of `:root` centralize theme — colors, fonts, `--player-h` — change those instead of scattering literal values), the DOM skeleton, then a single `<script>` with no modules/bundler. Key frontend concepts:
- `library` (fetched from `/api/library`) is the full in-memory dataset; `filtered` is the current search-filtered subset; both are plain arrays of album objects re-rendered on every filter/tab change (no virtual DOM/diffing).
- `queue` + `qIndex` model the play queue: clicking a track loads the whole album into `queue` starting at that index, so next/prev just moves `qIndex`.
- Playback state is driven off the single `<audio>` element's native events (`timeupdate`, `ended`); there is no separate player state object.
- `groupByArtist()` derives the artist view from `library.albums` on the fly — there is no separate artists endpoint or artist data structure server-side.

**Data flow contract**: the backend never mutates `library.json` structure per-request and the frontend never talks to the filesystem — all album/track shape decisions belong in `scan()`/`read_tags()`, and all display/filtering logic belongs in `index.html`. Keep that boundary when adding fields (e.g., a new ID3 tag needs to flow through `read_tags` → `scan` → `library.json` → frontend render code, in that order).

## Conventions worth preserving

- No database, no ORM — flat JSON files by design (see README "Was die App nicht macht"). Don't introduce one for small features.
- No build tooling for the frontend — keep `index.html` a single static file editable via SMB and reloadable without a container restart (per README, this is a deployment requirement, not just a style choice).
- Cover filenames are content-addressed (`{album_id}.{ext}`) and validated against path traversal in `/api/cover/{name}` (rejects `/`, `\`, `..`) — preserve that check if touching that endpoint.
- `README.md` is in German and documents unraid-specific deployment/troubleshooting in detail; consult it before changing deployment-relevant behavior (env vars, ports, volume expectations).
