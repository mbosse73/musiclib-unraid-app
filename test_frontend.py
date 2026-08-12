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


# --------------------------------------------------------------------------
# Handy-Oberflaeche (/mobil)
# --------------------------------------------------------------------------

@pytest.fixture
def phone(browser, server):
    """Eigener Kontext im Handy-Format — mit Beruehrung statt Maus."""
    context = browser.new_context(viewport={"width": 390, "height": 844},
                                  device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = context.new_page()
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.goto(server + "/mobil", wait_until="domcontentloaded")
    pg.wait_for_selector(".card")
    yield pg
    assert pg.errors == [], f"JavaScript-Fehler auf der Seite: {pg.errors}"
    context.close()


def test_mobile_library_renders(phone):
    assert phone.locator(".card").count() == 3
    # inner_text liefert die per CSS gesetzten Versalien zurueck
    assert "3 ALBEN" in phone.inner_text("#lib-sub").upper()


def test_mobile_grid_never_scrolls_sideways(phone):
    """Ein langer Interpretenname darf die Spalte nicht ueber den Rand schieben.

    Rasterelemente sind von sich aus mindestens so breit wie ihr laengster
    unumbrechbarer Inhalt. Die Interpretenzeile laeuft mit white-space:nowrap —
    ohne min-width:0 an der Kachel wurde die Sammlung dadurch waagerecht
    scrollbar. Die Namen werden hier zur Laufzeit gesetzt, damit die Sammlung
    der uebrigen Tests unveraendert bleibt.
    """
    phone.evaluate("""() => {
      library.albums[0].artist = 'Ein aussergewoehnlich langer Interpretenname';
      library.albums[0].title = 'Donaudampfschifffahrtsgesellschaftskapitaenspatent';
      renderGrid();
    }""")
    phone.wait_for_timeout(100)

    breit = phone.evaluate("""() => {
      const b = document.querySelector('#view-lib .body');
      return { scroll: b.scrollWidth, sicht: b.clientWidth,
               fenster: window.innerWidth,
               karte: document.querySelector('.card').getBoundingClientRect().width };
    }""")
    assert breit["scroll"] <= breit["sicht"], "Sammlung scrollt waagerecht"
    assert breit["karte"] <= breit["fenster"] / 2, "Kachel breiter als eine halbe Spalte"


def test_mobile_search_finds_track_and_plays_it(phone):
    phone.click("button[data-view='search']")
    phone.fill("#q", "Kometenmelodie")
    phone.wait_for_timeout(200)
    phone.locator(".row[data-track]").first.click()

    phone.wait_for_function("!document.getElementById('audio').paused")
    # Ein gestarteter Titel wechselt in die Ansicht, in der man ihn bedient.
    assert phone.evaluate("view") == "now"
    assert phone.inner_text("#np-title") == "Kometenmelodie"


def test_mobile_rail_seeks_across_a_track_boundary(phone):
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.wait_for_selector(".trk")
    phone.locator(".trk").first.click()
    phone.wait_for_function("!document.getElementById('audio').paused")
    assert phone.evaluate("qIndex") == 0

    # Ziel liegt im zweiten Titel — der Faden muss dafuer den Titel wechseln.
    phone.evaluate("springeZu(offsets()[1] + 5)")
    phone.wait_for_function("qIndex === 1")
    assert phone.inner_text("#np-title") == "Kometenmelodie"


def test_mobile_queue_unfolds_and_folds_again(phone):
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.locator(".trk").first.click()
    phone.wait_for_function("!document.getElementById('audio').paused")

    phone.click("#qbtn")
    phone.wait_for_timeout(300)
    assert phone.get_attribute("#qbtn", "aria-expanded") == "true"
    assert phone.locator(".qitem").count() == 2

    phone.click("#qbtn")
    phone.wait_for_timeout(300)
    assert phone.get_attribute("#qbtn", "aria-expanded") == "false"


@pytest.mark.parametrize("akzent,farbe", [
    ("petrol", "rgb(31, 100, 112)"),
    ("gruen", "rgb(79, 138, 70)"),
])
def test_mobile_accent_changes_and_survives_reload(phone, server, akzent, farbe):
    phone.click("#settings-btn")
    phone.wait_for_timeout(200)
    phone.click(f"#accents button[data-akzent='{akzent}']")
    phone.wait_for_timeout(200)

    assert phone.evaluate("document.documentElement.dataset.akzent") == akzent
    assert phone.eval_on_selector("#play-btn", "el => getComputedStyle(el).borderColor") == farbe

    phone.reload(wait_until="domcontentloaded")
    phone.wait_for_selector(".card")
    assert phone.evaluate("document.documentElement.dataset.akzent") == akzent


def waehle_leiste(phone, wert):
    phone.click("#settings-btn")
    phone.wait_for_timeout(200)
    phone.click(f"#leiste button[data-wert='{wert}']")
    phone.wait_for_timeout(200)
    phone.click("#settings-back")
    phone.wait_for_timeout(400)


def test_mobile_bar_stays_put_by_default(phone):
    assert phone.evaluate("document.documentElement.dataset.leiste") == "dauerhaft"
    assert phone.eval_on_selector("#tabs", "el => getComputedStyle(el).visibility") == "visible"
    assert phone.eval_on_selector("#grip", "el => getComputedStyle(el).display") == "none"


def test_mobile_bar_on_demand_hides_and_can_be_summoned(phone):
    hoehe = lambda: phone.eval_on_selector("#view-lib", "el => el.getBoundingClientRect().height")
    vorher = hoehe()
    waehle_leiste(phone, "bedarf")

    # Weg — und die Sammlung bekommt den frei gewordenen Platz.
    assert phone.eval_on_selector("#tabs", "el => getComputedStyle(el).visibility") == "hidden"
    assert hoehe() > vorher

    # Der Griff bleibt sichtbar: eine Geste, die man nicht sieht, ist keine.
    assert phone.eval_on_selector("#grip", "el => getComputedStyle(el).display") != "none"
    phone.click("#grip")
    phone.wait_for_timeout(400)
    assert phone.eval_on_selector("#tabs", "el => getComputedStyle(el).visibility") == "visible"

    # Nach der Wahl eines Reiters geht sie von selbst zurueck.
    phone.click("button[data-view='search']")
    phone.wait_for_timeout(800)
    assert phone.evaluate("view") == "search"
    assert phone.eval_on_selector("#tabs", "el => getComputedStyle(el).visibility") == "hidden"


def test_mobile_bar_setting_survives_reload_and_can_be_undone(phone):
    waehle_leiste(phone, "bedarf")
    phone.reload(wait_until="domcontentloaded")
    phone.wait_for_selector(".card")
    assert phone.evaluate("document.documentElement.dataset.leiste") == "bedarf"
    assert phone.eval_on_selector("#tabs", "el => getComputedStyle(el).visibility") == "hidden"

    waehle_leiste(phone, "dauerhaft")
    assert phone.eval_on_selector("#tabs", "el => getComputedStyle(el).visibility") == "visible"
    assert phone.eval_on_selector("#grip", "el => getComputedStyle(el).display") == "none"


def test_mobile_settings_are_one_object_in_storage(phone):
    """Spaetere Optionen sollen keinen neuen Schluessel brauchen."""
    waehle_leiste(phone, "bedarf")
    phone.click("#settings-btn")
    phone.wait_for_timeout(200)
    phone.click("#accents button[data-akzent='petrol']")
    phone.wait_for_timeout(200)

    gespeichert = json.loads(phone.evaluate("localStorage.getItem('musiklib:einstellungen')"))
    assert gespeichert == {"thema": "papier", "akzent": "petrol", "leiste": "bedarf"}


# --------------------------------------------------------------------------
# Themen: „Papier" und „Desert Rose"
# --------------------------------------------------------------------------

def waehle_thema(phone, wert):
    phone.click("#settings-btn")
    phone.wait_for_timeout(200)
    phone.click(f"#themen button[data-wert='{wert}']")
    phone.wait_for_timeout(250)
    phone.click("#settings-back")
    phone.wait_for_timeout(400)


def sichtbar(phone, sel):
    return phone.eval_on_selector(sel, "el => getComputedStyle(el).display") != "none"


def test_mobile_theme_swaps_palette_and_axis(phone):
    """Ein Thema ist mehr als Farbe: mit ihm wechselt die Achse."""
    assert sichtbar(phone, "#rail") and not sichtbar(phone, "#skala")

    waehle_thema(phone, "wueste")
    assert phone.evaluate("document.documentElement.dataset.thema") == "wueste"
    assert phone.eval_on_selector("body", "el => getComputedStyle(el).backgroundColor") \
        == "rgb(232, 213, 196)"
    # Die Warteschlange liegt jetzt waagerecht unter dem Bild.
    assert sichtbar(phone, "#skala") and not sichtbar(phone, "#rail")
    # Auch die Statusleiste des Geraets gehoert zum Thema.
    assert phone.get_attribute('meta[name="theme-color"]', "content") == "#E8D5C4"

    waehle_thema(phone, "papier")
    assert sichtbar(phone, "#rail") and not sichtbar(phone, "#skala")
    assert phone.get_attribute('meta[name="theme-color"]', "content") == "#FBF9F5"


def test_mobile_theme_brings_its_own_accents(phone):
    akzente = lambda: phone.eval_on_selector_all(
        "#accents button", "els => els.map(e => e.dataset.akzent)")
    phone.click("#settings-btn")
    phone.wait_for_timeout(200)
    assert akzente() == ["messing", "petrol", "gruen"]

    phone.click("#themen button[data-wert='wueste']")
    phone.wait_for_timeout(250)
    # Messing auf Sand waere keine Wahl, sondern ein Fehler.
    assert akzente() == ["ton", "rose"]
    assert phone.evaluate("document.documentElement.dataset.akzent") == "ton"

    phone.click("#accents button[data-akzent='rose']")
    phone.wait_for_timeout(200)
    assert phone.eval_on_selector("#sdone", "el => getComputedStyle(el).backgroundColor") \
        == "rgb(212, 165, 165)"

    # Zurueck: der Akzent des anderen Themas gilt hier nicht.
    phone.click("#themen button[data-wert='papier']")
    phone.wait_for_timeout(250)
    assert akzente() == ["messing", "petrol", "gruen"]
    assert phone.evaluate("document.documentElement.dataset.akzent") == "messing"


def test_mobile_theme_survives_reload(phone):
    waehle_thema(phone, "wueste")
    phone.reload(wait_until="domcontentloaded")
    phone.wait_for_selector(".card")
    assert phone.evaluate("document.documentElement.dataset.thema") == "wueste"
    assert sichtbar(phone, "#skala")


def test_mobile_scale_seeks_across_a_track_boundary(phone):
    """Dieselbe Bewegung wie am Rand, nur waagerecht — und erst beim Loslassen."""
    waehle_thema(phone, "wueste")
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.wait_for_selector(".trk")
    phone.locator(".trk").first.click()
    phone.wait_for_function("!document.getElementById('audio').paused")
    assert phone.evaluate("qIndex") == 0

    r = phone.eval_on_selector("#ruler", """el => {
      const b = el.getBoundingClientRect();
      return {x: b.x, y: b.y + b.height / 2, w: b.width};
    }""")
    phone.mouse.move(r["x"] + r["w"] * 0.05, r["y"])
    phone.mouse.down()
    phone.mouse.move(r["x"] + r["w"] * 0.70, r["y"], steps=6)
    phone.wait_for_timeout(150)
    # Waehrend des Ziehens bewegt sich nur die Anzeige, nicht die Wiedergabe.
    assert phone.evaluate("qIndex") == 0
    assert "Kometenmelodie" in phone.inner_text("#sbubble")

    phone.mouse.up()
    phone.wait_for_function("qIndex === 1")
    assert phone.inner_text("#np-title") == "Kometenmelodie"


def test_mobile_shares_the_session_with_the_desktop_page(phone, server):
    """Beide Ansichten benutzen denselben Schluessel und dieselbe Form."""
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.locator(".trk").nth(1).click()
    phone.wait_for_function("!document.getElementById('audio').paused")
    phone.evaluate("document.getElementById('audio').pause()")
    phone.evaluate("saveSession()")

    gespeichert = json.loads(phone.evaluate("localStorage.getItem('musiklib:session')"))
    assert gespeichert["qIndex"] == 1
    assert len(gespeichert["items"][0]) == 2, "Form muss [albumId, trackId] bleiben"

    phone.goto(server, wait_until="domcontentloaded")   # dieselbe Herkunft: Schreibtischseite
    phone.wait_for_selector(".album")
    phone.wait_for_function("document.getElementById('now-title').textContent !== '—'")
    assert phone.inner_text("#now-title") == "Kometenmelodie"
