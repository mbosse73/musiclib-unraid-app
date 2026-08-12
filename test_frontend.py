"""
Frontend-Tests: steuern index.html in einem echten Chromium.

Diese Tests decken ab, was der Backend-Suite grundsaetzlich entgeht — Player,
Suche, Sortierung, Tastatur und die in localStorage gemerkte Sitzung.

Voraussetzung ist einmalig ein Browser:

    .venv/bin/python -m playwright install chromium
    .venv/bin/python -m pytest -q test_frontend.py

Ist Playwright oder der Browser nicht da, ueberspringt sich die Datei
geschlossen — die Backend-Tests laufen weiter. Liegt der Browser an einer
ungewoehnlichen Stelle, hilft MUSIKLIB_CHROME=/pfad/zu/chrome.

    .venv/bin/python -m pytest -q -k player      # einzelne Gruppe
"""

import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

from conftest import PNG, frames, write_mp3

sync_playwright = pytest.importorskip(
    "playwright.sync_api", reason="playwright nicht installiert"
).sync_playwright

# Lang genug, dass waehrend der Pruefschritte kein Titel durchlaeuft.
TRACK_SECONDS = 30


# --------------------------------------------------------------------------
# Browser und Server
# --------------------------------------------------------------------------

def _launch(pw):
    """Chromium starten — mit Ausweichpfaden statt einer harten Annahme."""
    explicit = os.environ.get("MUSIKLIB_CHROME")
    attempts = [{"executable_path": explicit}] if explicit else []
    attempts.append({})  # der von playwright install verwaltete Browser
    for root in ("/opt/pw-browsers", os.path.expanduser("~/.cache/ms-playwright")):
        attempts += [{"executable_path": str(p)}
                     for p in sorted(Path(root).glob("chromium-*/chrome-linux/chrome"))]
    last = None
    for kwargs in attempts:
        try:
            return pw.chromium.launch(**kwargs)
        except Exception as exc:
            last = exc
    pytest.skip(f"Kein startbarer Chromium gefunden ({last}). "
                f"Einmalig: python -m playwright install chromium")


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def library(tmp_path_factory):
    """Kleine, aber vielfaeltige Sammlung: zwei Interpreten, drei Alben."""
    root = tmp_path_factory.mktemp("frontend")
    music, data = root / "music", root / "data"
    music.mkdir()
    data.mkdir()
    long_audio = frames(TRACK_SECONDS)

    write_mp3(music / "KW/Autobahn/01.mp3", title="Autobahn", artist="Kraftwerk",
              album="Autobahn", track="1", year=1974, cover=PNG, data=long_audio)
    write_mp3(music / "KW/Autobahn/02.mp3", title="Kometenmelodie", artist="Kraftwerk",
              album="Autobahn", track="2", year=1974, cover=PNG, data=long_audio)
    write_mp3(music / "KW/Mensch/01.mp3", title="Die Roboter", artist="Kraftwerk",
              album="Die Mensch-Maschine", track="1", year=1978, cover=PNG, data=long_audio)
    # ohne eingebettetes Cover, aber mit Ordnerbild
    write_mp3(music / "AB/Eins/01.mp3", title="Erstes Lied", artist="Andere Band",
              album="Erstes Album", track="1", year=2001, data=long_audio)
    (music / "AB/Eins/cover.jpg").write_bytes(PNG)
    # unlesbar — muss als uebersprungen gemeldet werden
    (music / "defekt.mp3").write_bytes(b"kein mp3")
    return music, data


@pytest.fixture(scope="module")
def server(library):
    """app.py als eigener Prozess, wie im Container."""
    music, data = library
    port = _free_port()
    env = {**os.environ, "MUSIC_DIR": str(music), "DATA_DIR": str(data), "PORT": str(port)}
    proc = subprocess.Popen([sys.executable, "app.py"], env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(100):
            if proc.poll() is not None:
                pytest.fail(f"Server beendet:\n{proc.stdout.read().decode(errors='replace')}")
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.1)
        else:
            pytest.fail("Server nicht erreichbar")

        # Startscan abwarten, sonst rendert die Seite eine leere Bibliothek.
        deadline = time.time() + 30
        while time.time() < deadline:
            if (data / "library.json").exists():
                break
            time.sleep(0.1)
        yield base
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as pw:
        br = _launch(pw)
        yield br
        br.close()


@pytest.fixture
def ctx(browser):
    """Eigener Kontext je Test — frischer localStorage."""
    context = browser.new_context()
    # Der Webfont von Google darf die Tests weder verlangsamen noch von einer
    # Internetverbindung abhaengig machen. Die App faellt sauber auf die
    # System-Monospace zurueck, genau wie auf einem NAS ohne Internet.
    context.route("**://fonts.googleapis.com/**", lambda route: route.abort())
    context.route("**://fonts.gstatic.com/**", lambda route: route.abort())
    yield context
    context.close()


def open_page(ctx, server):
    """Seite oeffnen und warten, bis die Bibliothek gerendert ist."""
    pg = ctx.new_page()
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.goto(server, wait_until="domcontentloaded")
    pg.wait_for_selector(".album")
    return pg


@pytest.fixture
def page(ctx, server):
    pg = open_page(ctx, server)
    yield pg
    assert pg.errors == [], f"JavaScript-Fehler auf der Seite: {pg.errors}"


def album_titles(pg):
    return [t.strip() for t in pg.locator(".album .title").all_inner_texts()]


def wait_for_search(pg, term):
    """Suchbegriff eintippen und warten, bis die Entprellung durch ist."""
    pg.fill("#search", term)
    pg.wait_for_timeout(200)


# --------------------------------------------------------------------------
# Grundgeruest
# --------------------------------------------------------------------------

def test_library_renders(page):
    assert page.locator(".album").count() == 3
    assert page.title() == "Musiklib"


def test_album_without_embedded_art_uses_folder_image(page):
    wait_for_search(page, "Erstes Album")
    assert page.locator(".album .cover img").count() == 1, "Ordner-Cover fehlt"


# --------------------------------------------------------------------------
# Suche
# --------------------------------------------------------------------------

def test_search_finds_album_by_track_title(page):
    wait_for_search(page, "Kometenmelodie")
    assert album_titles(page) == ["Autobahn"]


def test_search_marks_the_matching_track(page):
    wait_for_search(page, "Kometenmelodie")
    page.locator(".album").first.click()
    page.wait_for_selector(".track")
    assert page.locator(".track.match").count() == 1
    assert "Kometenmelodie" in page.inner_text(".track.match")


def test_search_without_hits_shows_empty_state(page):
    wait_for_search(page, "gibtesnichtimkatalog")
    assert "Nichts gefunden" in page.inner_text("#empty")


# --------------------------------------------------------------------------
# Sortierung
# --------------------------------------------------------------------------

@pytest.mark.parametrize("mode,first", [
    ("year-asc", "Autobahn"),
    ("year-desc", "Erstes Album"),
    ("title", "Autobahn"),
])
def test_sort_modes_reorder_the_grid(page, mode, first):
    page.select_option("#sort", mode)
    page.wait_for_timeout(200)
    assert album_titles(page)[0] == first


def test_sort_choice_survives_reload(page, ctx, server):
    page.select_option("#sort", "year-desc")
    page.wait_for_timeout(200)
    again = open_page(ctx, server)
    assert again.eval_on_selector("#sort", "el => el.value") == "year-desc"
    assert album_titles(again)[0] == "Erstes Album"
    again.close()


# --------------------------------------------------------------------------
# Player
# --------------------------------------------------------------------------

def test_player_starts_track_and_button_follows_audio(page):
    page.locator(".album", has_text="Autobahn").first.click()
    page.locator(".track").first.click()

    # Auf den Button warten, nicht auf audio.paused: der Button wird bewusst
    # erst vom play-Event gesetzt, das kurz nach dem Zustandswechsel feuert.
    # Ein Vergleich direkt nach "nicht mehr pausiert" waere ein Wettlauf.
    page.wait_for_function("document.getElementById('play-btn').textContent === '❚❚'")

    # Von aussen pausieren (wie Sperrbildschirm oder Medientaste)
    page.evaluate("document.getElementById('audio').pause()")
    page.wait_for_function("document.getElementById('play-btn').textContent === '▶'")


def test_player_reports_a_dead_stream(page):
    page.evaluate("""() => {
        const a = document.getElementById('audio');
        a.src = '/api/stream/gibtesnicht';
        a.load();
    }""")
    page.wait_for_timeout(800)
    assert "nicht abspielbar" in page.inner_text("#now-artist")


def test_volume_and_mute(page):
    page.eval_on_selector("#volume", "el => { el.value = 40; el.dispatchEvent(new Event('input')); }")
    page.wait_for_timeout(150)
    assert abs(page.evaluate("document.getElementById('audio').volume") - 0.4) < 0.01

    page.click("#mute-btn")
    page.wait_for_timeout(150)
    assert page.evaluate("document.getElementById('audio').muted") is True
    page.click("#mute-btn")
    page.wait_for_timeout(150)
    assert page.evaluate("document.getElementById('audio').muted") is False


def test_play_all_by_artist_spans_albums(page):
    page.click(".tab[data-view='artists']")
    page.wait_for_selector(".artist-row")
    page.locator(".artist-row", has_text="Kraftwerk").locator(".play-all").click()
    page.wait_for_function("!document.getElementById('audio').paused")
    assert page.evaluate("queue.length") == 3, "Warteschlange muss albumuebergreifend sein"


def test_shuffle_toggles_and_persists(page, ctx, server):
    page.click("#shuffle-btn")
    page.wait_for_timeout(150)
    assert page.get_attribute("#shuffle-btn", "aria-pressed") == "true"

    again = open_page(ctx, server)
    assert again.get_attribute("#shuffle-btn", "aria-pressed") == "true"
    again.close()


def test_shuffle_keeps_the_current_track(page):
    page.locator(".album", has_text="Autobahn").first.click()
    page.locator(".track").first.click()
    page.wait_for_function("!document.getElementById('audio').paused")
    before = page.inner_text("#now-title")

    page.evaluate("toggleShuffle()")
    page.wait_for_timeout(200)
    assert page.inner_text("#now-title") == before, "laufender Titel darf nicht wechseln"


# --------------------------------------------------------------------------
# Tastatur
# --------------------------------------------------------------------------

def test_space_toggles_playback(page):
    page.locator(".album").first.click()
    page.locator(".track").first.click()
    page.wait_for_function("!document.getElementById('audio').paused")
    page.keyboard.press("Escape")

    page.keyboard.press("Space")
    page.wait_for_function("document.getElementById('audio').paused")
    page.keyboard.press("Space")
    page.wait_for_function("!document.getElementById('audio').paused")


def test_n_and_p_move_through_the_queue(page):
    page.locator(".album", has_text="Autobahn").first.click()
    page.locator(".track").first.click()
    page.wait_for_function("!document.getElementById('audio').paused")
    page.keyboard.press("Escape")

    page.keyboard.press("n")
    page.wait_for_function("qIndex === 1")
    page.keyboard.press("p")
    page.wait_for_function("qIndex === 0")


def test_slash_focuses_search_and_typing_does_not_trigger_shortcuts(page):
    page.keyboard.press("/")
    page.wait_for_timeout(150)
    assert page.evaluate("document.activeElement.id") == "search"

    # Im Suchfeld duerfen die Kuerzel nicht greifen
    page.keyboard.type("ns ")
    page.wait_for_timeout(250)
    assert page.eval_on_selector("#search", "el => el.value") == "ns "
    assert page.get_attribute("#shuffle-btn", "aria-pressed") == "false"


# --------------------------------------------------------------------------
# Sitzung
# --------------------------------------------------------------------------

def test_session_is_restored_without_autoplay(page, ctx, server):
    page.locator(".album", has_text="Autobahn").first.click()
    page.locator(".track").nth(1).click()
    page.wait_for_function("!document.getElementById('audio').paused")
    page.evaluate("document.getElementById('audio').pause()")
    page.evaluate("document.getElementById('audio').currentTime = 12")
    page.wait_for_timeout(200)
    page.evaluate("saveSession()")
    title = page.inner_text("#now-title")

    again = open_page(ctx, server)
    again.wait_for_function("document.getElementById('now-title').textContent !== '—'")

    assert again.inner_text("#now-title") == title
    assert again.evaluate("qIndex") == 1
    assert abs(again.evaluate("document.getElementById('audio').currentTime") - 12) < 2
    assert again.evaluate("document.getElementById('audio').paused"), "darf nie automatisch starten"
    again.close()


def test_session_with_vanished_tracks_is_discarded(page, ctx, server):
    # Genau das passiert nach dem Verschieben von Dateien: track_id ist der
    # Hash des Pfades, gespeicherte IDs zeigen dann ins Leere.
    page.evaluate("""localStorage.setItem('musiklib:session', JSON.stringify(
        {items: [['weg', 'weg'], ['auchweg', 'auchweg']], qIndex: 1, position: 5}))""")

    again = open_page(ctx, server)
    again.wait_for_timeout(400)

    assert again.errors == []
    assert again.inner_text("#now-title").strip() == "—"
    assert again.evaluate("queue.length") == 0
    again.close()


def test_storage_failure_does_not_break_the_app(ctx, server):
    """Ein Browser mit abgeschaltetem Speicher muss die App trotzdem zeigen."""
    ctx.add_init_script("""
        const boom = () => { throw new Error('storage disabled'); };
        Object.defineProperty(window, 'localStorage', {
            get: () => ({ getItem: boom, setItem: boom, removeItem: boom }),
        });
    """)
    pg = open_page(ctx, server)

    assert pg.errors == []
    assert pg.locator(".album").count() == 3
    pg.close()


# --------------------------------------------------------------------------
# Uebersprungene Dateien und Performance-Zusicherung
# --------------------------------------------------------------------------

def test_skipped_files_are_listed(page):
    toggle = page.locator("#skipped-toggle")
    assert toggle.is_visible()
    assert "1" in toggle.inner_text()

    toggle.click()
    page.wait_for_timeout(200)
    assert "defekt.mp3" in page.inner_text("#skipped-list")


def test_album_cards_keep_content_visibility(page):
    # Ohne das rendert eine grosse Sammlung jede Karte, auch ausserhalb des Bildes.
    assert page.eval_on_selector(".album", "el => getComputedStyle(el).contentVisibility") == "auto"
    assert page.eval_on_selector(".album", "el => getComputedStyle(el).containIntrinsicSize") != "none"
