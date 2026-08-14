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


def waehle_einstellung(phone, gruppe, wert):
    # Der Knopf zu den Einstellungen steht im Kopf der Sammlung.
    phone.evaluate("setView('lib')")
    phone.wait_for_timeout(150)
    phone.click("#settings-btn")
    phone.wait_for_timeout(200)
    phone.click(f"#{gruppe} button[data-wert='{wert}']")
    phone.wait_for_timeout(200)
    phone.click("#settings-back")
    phone.wait_for_timeout(400)


def waehle_leiste(phone, wert):
    waehle_einstellung(phone, "leiste", wert)


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
    assert gespeichert == {"thema": "papier", "akzent": "petrol", "leiste": "bedarf",
                           "fortsetzung": "weiter", "wach": "aus"}
    # Genau das war der Sinn des einen Objekts: „fortsetzung" und „wach" sind
    # spaeter dazugekommen und haben keinen eigenen Schluessel gebraucht.
    schluessel = phone.evaluate(
        "Object.keys(localStorage).filter(k => k.startsWith('musiklib:')).sort()")
    assert "musiklib:leiste" not in schluessel and "musiklib:wach" not in schluessel


# --------------------------------------------------------------------------
# Themen: „Papier" und „Desert Rose"
# --------------------------------------------------------------------------

def waehle_thema(phone, wert):
    # Der Knopf zu den Einstellungen steht im Kopf der Sammlung — laeuft
    # gerade etwas, ist diese Seite nicht die sichtbare.
    phone.evaluate("setView('lib')")
    phone.wait_for_timeout(150)
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


# --------------------------------------------------------------------------
# Handy: die Themen mit eigenem Spieler
# --------------------------------------------------------------------------

EIGENE_SPIELER = ["kissen", "karte", "kiesel"]


@pytest.mark.parametrize("thema", EIGENE_SPIELER)
def test_mobile_own_player_replaces_the_built_in_one(phone, thema):
    """Drei Themen bringen eine ganze Oberflaeche mit, nicht nur Farben."""
    waehle_thema(phone, thema)
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.locator(".trk").first.click()
    phone.wait_for_function("!document.getElementById('audio').paused")

    assert phone.evaluate("document.documentElement.dataset.spieler") == thema
    assert sichtbar(phone, "#fremd")
    # Deckel, Buehne und Sockel des eingebauten Spielers treten zurueck.
    for teil in ("#view-now .lid", "#stage", "#view-now .foot"):
        assert not sichtbar(phone, teil), f"{teil} steht noch im Weg"
    assert phone.inner_text("#fremd [data-titel]") == "Autobahn"

    # Zurueck heisst wirklich zurueck.
    waehle_thema(phone, "papier")
    phone.evaluate("setView('now')")
    phone.wait_for_timeout(150)
    assert phone.evaluate("document.documentElement.hasAttribute('data-spieler')") is False
    assert sichtbar(phone, "#stage") and not sichtbar(phone, "#fremd")


@pytest.mark.parametrize("thema", EIGENE_SPIELER)
def test_mobile_own_player_button_follows_the_audio_element(phone, thema):
    """Der Knopf kommt aus dem Ereignis, nie aus der Annahme neben dem Klick."""
    waehle_thema(phone, thema)
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.locator(".trk").first.click()
    phone.wait_for_function("!document.getElementById('audio').paused")

    knopf = "#fremd [data-pp], #fremd .zeile.an [data-k]"
    phone.wait_for_selector(knopf)
    assert "M6.5 4h3.6" in phone.eval_on_selector(knopf, "el => el.innerHTML"), "Pause erwartet"

    # von aussen gesteuert — wie Sperrbildschirm oder Kopfhoerertaste
    phone.evaluate("document.getElementById('audio').pause()")
    phone.wait_for_timeout(200)
    assert "M8 5v14" in phone.eval_on_selector(knopf, "el => el.innerHTML"), "Abspielen erwartet"


@pytest.mark.parametrize("thema", EIGENE_SPIELER)
def test_mobile_own_player_reaches_library_and_search(phone, thema):
    """Sammlung und Suche bleiben aus jedem Spieler ueber einen Knopf erreichbar."""
    waehle_thema(phone, thema)
    phone.evaluate("setView('now')")
    phone.wait_for_timeout(150)

    phone.click("#fremd [data-zur-lib]")
    phone.wait_for_function("view === 'lib'")

    phone.evaluate("setView('now')")
    phone.wait_for_timeout(150)
    phone.click("#fremd [data-zur-suche]")
    phone.wait_for_function("view === 'search'")


def test_mobile_own_player_seeks_within_the_track(phone):
    """Die Leiste des eigenen Spielers spult, ohne den Titel zu wechseln."""
    waehle_thema(phone, "kiesel")
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.locator(".trk").first.click()
    phone.wait_for_function("!document.getElementById('audio').paused")
    phone.evaluate("document.getElementById('audio').pause()")

    r = phone.eval_on_selector("#fremd [data-bahn]", """el => {
      const b = el.getBoundingClientRect();
      return {x: b.x, y: b.y + b.height / 2, w: b.width};
    }""")
    phone.mouse.click(r["x"] + r["w"] * 0.5, r["y"])
    phone.wait_for_timeout(250)
    assert phone.evaluate("qIndex") == 0, "Spulen darf den Titel nicht wechseln"
    assert phone.evaluate("document.getElementById('audio').currentTime") > 5


# --------------------------------------------------------------------------
# Spieler fuer iPad und PC
# --------------------------------------------------------------------------

@pytest.fixture
def player(browser, server):
    """Eigener Kontext im Schreibtischformat, auf /pc."""
    context = browser.new_context(viewport={"width": 1280, "height": 860})
    pg = context.new_page()
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.goto(server + "/pc", wait_until="domcontentloaded")
    pg.wait_for_function("typeof LAYOUTS !== 'undefined' && document.querySelector('#buehne > *')")
    yield pg
    assert pg.errors == [], f"JavaScript-Fehler auf der Seite: {pg.errors}"
    context.close()


def layout_ids(pg):
    return pg.evaluate("LAYOUTS.map(l => l.id)")


def test_player_offers_twelve_layouts(player):
    ids = layout_ids(player)
    assert len(ids) == 12
    assert len(set(ids)) == 12, "Kennungen muessen eindeutig sein"
    assert player.title() == "Musiklib · Spieler"


def test_player_every_layout_plays_and_stops(player):
    """Jedes Layout baut, spielt ab und haelt wieder an."""
    for lid in layout_ids(player):
        player.evaluate("id => zeigeLayout(id)", lid)
        player.wait_for_selector("#buehne [data-pp]")
        player.click("#buehne [data-pp]")
        player.wait_for_function("!ton.paused", timeout=5000)
        player.click("#buehne [data-pp]")
        player.wait_for_function("ton.paused", timeout=5000)


def test_player_library_and_search_are_reachable_in_every_layout(player):
    """Die Regel aus den Entwuerfen: Sammlung und Suche hinter einem Knopf.

    Zwei Layouts sind die vereinbarte Ausnahme — dort liegt die Sammlung
    ohnehin offen daneben, und die Suchzeile steht direkt darueber.
    """
    offen = {"werkstisch", "deck"}
    for lid in layout_ids(player):
        player.evaluate("id => zeigeLayout(id)", lid)
        knopf = player.locator("#buehne [data-bib], #buehne [data-auswurf]")
        if lid in offen:
            assert knopf.count() == 0, f"{lid} braucht keinen Knopf"
        else:
            assert knopf.count() == 1, f"{lid} hat keinen Knopf zur Bibliothek"
            knopf.click()
            player.wait_for_timeout(250)
        feld = player.locator("#buehne [data-suche]")
        assert feld.count() == 1, f"{lid} hat kein Suchfeld"
        feld.fill("Mensch")
        player.wait_for_timeout(200)
        zeilen = player.locator(
            "#buehne [data-bibliothek] [data-alb], #buehne [data-regal] [data-alb],"
            " #buehne [data-liste] [data-t]")
        assert zeilen.count() >= 1, f"{lid}: Suche findet das Album nicht"
        zeilen.first.click()
        player.wait_for_function("deck.album && deck.album.t === 'Die Mensch-Maschine'",
                                 timeout=5000)
        player.evaluate("ton.pause()")
        player.keyboard.press("Escape")
        player.wait_for_timeout(150)


def test_player_search_matches_track_titles_too(player):
    player.evaluate("zeigeLayout('werkstisch')")
    player.fill("#buehne [data-suche]", "Kometenmelodie")
    player.wait_for_timeout(200)
    assert player.evaluate("suche('Kometenmelodie').map(a => a.t)") == ["Autobahn"]


def test_player_layout_choice_survives_reload(player, server):
    player.evaluate("zeigeLayout('konsole')")
    assert player.evaluate("localStorage.getItem('musiklib:layout')") == '"konsole"'
    player.reload(wait_until="domcontentloaded")
    player.wait_for_function("typeof aktuell !== 'undefined' && aktuell")
    assert player.evaluate("aktuell.id") == "konsole"


def test_player_shares_the_session_with_the_desktop_page(player, server):
    """Dieselben Schluessel, dieselbe Form — die Sitzung laeuft weiter."""
    player.evaluate("zeigeLayout('aufgeschlagen')")
    player.evaluate("""() => {
      const a = ALBUMS.find(x => x.t === 'Autobahn');
      deck.ladeAlbum(a, 1);
    }""")
    player.wait_for_function("!ton.paused", timeout=5000)
    player.evaluate("ton.pause()")

    gespeichert = json.loads(player.evaluate("localStorage.getItem('musiklib:session')"))
    assert gespeichert["qIndex"] == 1
    assert len(gespeichert["items"][0]) == 2, "Form muss [albumId, trackId] bleiben"

    player.goto(server, wait_until="domcontentloaded")   # Schreibtischseite
    player.wait_for_selector(".album")
    player.wait_for_function("document.getElementById('now-title').textContent !== '—'")
    assert player.inner_text("#now-title") == "Kometenmelodie"


def test_player_reports_a_moved_file_instead_of_stopping_silently(player):
    """Ein Titel, dessen Datei verschwunden ist, sagt das — er schweigt nicht."""
    player.evaluate("zeigeLayout('aufgeschlagen')")
    player.evaluate("""() => {
      ton.src = '/api/stream/gibtsnicht';
      ton.load();
    }""")
    player.wait_for_function("deck.fehler !== ''", timeout=5000)
    player.wait_for_function(
        "document.querySelector('#buehne [data-alb]').textContent.includes('nicht abspielbar')",
        timeout=5000)


# --------------------------------------------------------------------------
# Dass die Wiedergabe nicht von allein aufhoert
# --------------------------------------------------------------------------

def test_mobile_continues_with_the_next_album_at_the_end(phone):
    """Eine Warteschlange ist ein Album — danach geht es weiter."""
    phone.locator(".card", has_text="Die Mensch-Maschine").first.click()
    phone.locator(".trk").first.click()
    phone.wait_for_function("!document.getElementById('audio').paused")

    # ans Ende des letzten Titels stellen und den Wechsel ausloesen
    phone.evaluate("""() => {
      qIndex = queue.length - 1;
      audio.dispatchEvent(new Event('ended'));
    }""")
    phone.wait_for_function(
        "queue.length && queue[0].album.title !== 'Die Mensch-Maschine'", timeout=5000)
    assert phone.evaluate("qIndex") == 0


def test_mobile_repeats_the_queue_when_asked(phone):
    waehle_einstellung(phone, "fortsetzung", "wiederholen")
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.locator(".trk").first.click()
    phone.wait_for_function("!document.getElementById('audio').paused")
    titel = phone.evaluate("queue[0].album.title")

    phone.evaluate("""() => {
      qIndex = queue.length - 1;
      audio.dispatchEvent(new Event('ended'));
    }""")
    phone.wait_for_function("qIndex === 0", timeout=5000)
    assert phone.evaluate("queue[0].album.title") == titel


def test_mobile_stops_at_the_end_when_asked(phone):
    waehle_einstellung(phone, "fortsetzung", "halt")
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.locator(".trk").first.click()
    phone.wait_for_function("!document.getElementById('audio').paused")

    phone.evaluate("""() => {
      qIndex = queue.length - 1;
      audio.dispatchEvent(new Event('ended'));
    }""")
    phone.wait_for_timeout(400)
    assert phone.evaluate("queue[0].album.title") == "Autobahn"
    assert phone.evaluate("tonGewuenscht") is False


def test_mobile_insists_when_a_track_change_is_refused(phone):
    """Der Fall vom iPhone: play() wird im Hintergrund abgewiesen.

    Hier nachgestellt, indem das Element angehalten wird, waehrend Ton
    gewuenscht ist — nachdruck() muss von selbst wieder anfahren.
    """
    phone.evaluate("NACH_VERZUG = 150")
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.locator(".trk").first.click()
    phone.wait_for_function("!document.getElementById('audio').paused")

    phone.evaluate("""() => {
      audio.pause();          // wie eine abgewiesene Wiedergabe
      nachVersuche = 0;
      nachdruck();
    }""")
    phone.wait_for_function("!document.getElementById('audio').paused", timeout=5000)


def test_mobile_does_not_fight_a_deliberate_pause(phone):
    """Eine gewollte Pause bleibt eine Pause — sonst waere der Knopf kaputt."""
    phone.evaluate("NACH_VERZUG = 150")
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.locator(".trk").first.click()
    phone.wait_for_function("!document.getElementById('audio').paused")

    phone.click("#play-btn")                       # Pause von Hand
    phone.wait_for_timeout(900)
    assert phone.evaluate("document.getElementById('audio').paused") is True


def test_mobile_recovers_from_a_stalled_stream(phone):
    """Bleibt der Stream stehen, laedt die Seite ihn an derselben Stelle neu."""
    phone.evaluate("HEIL_VERZUG = 200")
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.locator(".trk").first.click()
    phone.wait_for_function("document.getElementById('audio').currentTime > 1")
    stelle = phone.evaluate("document.getElementById('audio').currentTime")

    phone.evaluate("versucheWeiter()")
    phone.wait_for_function("!document.getElementById('audio').paused", timeout=5000)
    phone.wait_for_function(f"document.getElementById('audio').currentTime > {stelle - 0.5}",
                            timeout=5000)


def test_mobile_prefetches_the_next_track(phone, server):
    """Vor dem Wechsel wird der Anfang des naechsten Titels schon geholt."""
    phone.locator(".card", has_text="Autobahn").first.click()
    phone.locator(".trk").first.click()
    phone.wait_for_function("!document.getElementById('audio').paused")
    naechste = phone.evaluate("queue[1].track.id")

    with phone.expect_request(f"**/api/stream/{naechste}", timeout=5000):
        phone.evaluate("ladeVor()")


def test_player_continues_with_the_next_album_at_the_end(player):
    player.evaluate("""() => {
      const a = ALBUMS.find(x => x.t === 'Die Mensch-Maschine');
      deck.ladeAlbum(a, 0);
    }""")
    player.wait_for_function("!ton.paused", timeout=5000)
    player.evaluate("""() => {
      deck.qi = deck.queue.length - 1;
      ton.dispatchEvent(new Event('ended'));
    }""")
    player.wait_for_function("deck.album && deck.album.t !== 'Die Mensch-Maschine'", timeout=5000)
    player.evaluate("ton.pause()")


def test_player_end_of_queue_setting_is_shared_with_the_phone(player):
    """Ein Schluessel, drei Oberflaechen — dieselben drei Werte."""
    player.evaluate("setzeFortsetzung('wiederholen')")
    assert player.evaluate("localStorage.getItem('musiklib:fortsetzung')") == '"wiederholen"'
    player.evaluate("setzeFortsetzung('weiter')")


def test_player_insists_when_a_track_change_is_refused(player):
    player.evaluate("NACH_VERZUG = 150")
    player.evaluate("deck.ladeAlbum(ALBUMS[0], 0)")
    player.wait_for_function("!ton.paused", timeout=5000)
    player.evaluate("""() => { ton.pause(); nachVersuche = 0; nachdruck(); }""")
    player.wait_for_function("!ton.paused", timeout=5000)
    player.evaluate("nachdruckEnde(); ton.pause()")


# --------------------------------------------------------------------------
# Album des Tages — der Spieler mit einem Knopf
# --------------------------------------------------------------------------

@pytest.fixture
def tagseite(browser, server):
    """Eigener Kontext im Telefonformat, auf /tag."""
    context = browser.new_context(viewport={"width": 390, "height": 844})
    pg = context.new_page()
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.goto(server + "/tag", wait_until="domcontentloaded")
    pg.wait_for_function("typeof albumJetzt !== 'undefined' && albumJetzt")
    yield pg
    assert pg.errors == [], f"JavaScript-Fehler auf der Seite: {pg.errors}"
    context.close()


def test_day_page_shows_album_artist_and_track(tagseite):
    """Drei Zeilen, mehr sagt die Karte nicht — aber die sagt sie."""
    assert tagseite.title() == "Musiklib · Album des Tages"
    # text_content statt inner_text: Album und Interpret stehen in Versalien,
    # aber das macht das Stylesheet — im Text steht der echte Name.
    assert tagseite.text_content("#alb") == tagseite.evaluate("albumJetzt.t")
    assert tagseite.text_content("#ar") == tagseite.evaluate("albumJetzt.ar")
    assert tagseite.text_content("#tl") == tagseite.evaluate("deck.track.t")
    # Genau ein Bedienelement, und es ist ein Knopf.
    assert tagseite.locator("button").count() == 1


def test_day_ring_is_concentric_with_the_disc(tagseite):
    """Der Fortschrittsring liegt um die Scheibe, nicht daneben.

    Auf dem iPhone sass er einmal links oben neben ihr: <svg class="ring"> hat
    kein width/height, ist damit ein ersetztes Element mit width:auto, und
    WebKit spannt so eins nicht ueber vier gesetzte Kanten auf — es nimmt 100%
    des Knopfes und verschiebt das Ergebnis um das negative left/top. Blink
    zeigt den Fehler nicht, und ein WebKit steht hier nicht zur Verfuegung.
    Darum prueft der Test beides: die Lage, die jeder Browser zeigt, und die
    Regel selbst, die ihre Masse ausschreiben muss statt sie ableiten zu lassen.
    """
    lage = tagseite.evaluate("""() => {
      const mitte = el => { const r = el.getBoundingClientRect();
        return [(r.left + r.right) / 2, (r.top + r.bottom) / 2, r.width]; };
      const [kx, ky, kb] = mitte(document.getElementById('knopf'));
      const [rx, ry, rb] = mitte(document.querySelector('.ring'));
      return {versatz: [Math.abs(rx - kx), Math.abs(ry - ky)], knopf: kb, ring: rb};
    }""")
    assert lage["versatz"][0] < 1 and lage["versatz"][1] < 1, (
        f"Ring liegt um {lage['versatz']} px versetzt")
    # Der Ring steht 7,5 % der Scheibe weiter aussen — an jeder Seite.
    assert abs(lage["ring"] - lage["knopf"] * 1.15) < 1

    ausgeschrieben = tagseite.evaluate("""() => {
      for (const bl of document.styleSheets)
        for (const rg of bl.cssRules)
          if (rg.selectorText === '.ring')
            return [rg.style.width, rg.style.height, rg.style.left, rg.style.top];
      return null;
    }""")
    assert ausgeschrieben and all(ausgeschrieben), (
        f".ring muss Breite, Hoehe und Ecke selbst nennen, hat aber {ausgeschrieben}")


def test_day_page_never_autoplays(tagseite):
    """Wiederhergestellt wird die Stelle, gespielt wird erst auf den Knopf."""
    tagseite.wait_for_timeout(300)
    assert tagseite.evaluate("ton.paused") is True


def test_day_button_plays_stops_and_resumes(tagseite):
    """Einmal druecken = spielt, noch einmal = haelt an, noch einmal = weiter."""
    tagseite.click("#knopf")
    tagseite.wait_for_function("!ton.paused", timeout=5000)
    assert tagseite.get_attribute("#knopf", "aria-pressed") == "true"

    tagseite.click("#knopf")
    tagseite.wait_for_function("ton.paused", timeout=5000)
    assert tagseite.get_attribute("#knopf", "aria-pressed") == "false"

    tagseite.click("#knopf")
    tagseite.wait_for_function("!ton.paused", timeout=5000)
    tagseite.evaluate("ton.pause()")


def test_day_five_taps_choose_a_new_album_only_once_a_day(tagseite):
    """Die einzige Ausnahme des Tages — und sie gilt nur einmal."""
    tagseite.evaluate("FENSTER = 5000")          # der Test tippt langsamer als ein Finger
    vorher = tagseite.evaluate("albumJetzt.id")

    for _ in range(5):
        tagseite.click("#knopf")
    tagseite.wait_for_function("id => albumJetzt.id !== id", arg=vorher, timeout=5000)
    assert tagseite.evaluate("JSON.parse(localStorage.getItem('musiklib:tag')).gewechselt") is True
    nachher = tagseite.evaluate("albumJetzt.id")

    for _ in range(5):
        tagseite.click("#knopf")
    tagseite.wait_for_function(
        "document.getElementById('hinweis').textContent.includes('Heute schon')", timeout=5000)
    assert tagseite.evaluate("albumJetzt.id") == nachher, "zweiter Wechsel am selben Tag"
    tagseite.evaluate("ton.pause()")


def test_day_choice_is_the_same_on_every_device(browser, server, tagseite):
    """Berechnet, nicht gewuerfelt: derselbe Tag ergibt dasselbe Album."""
    tage = ["2026-08-14", "2027-01-01", "2030-06-30"]
    hier = tagseite.evaluate("t => t.map(iso => albumDesTages(iso, 0, null).id)", tage)

    context = browser.new_context(viewport={"width": 390, "height": 844})
    pg = context.new_page()                      # frischer localStorage = fremdes Geraet
    pg.goto(server + "/tag", wait_until="domcontentloaded")
    pg.wait_for_function("typeof albumJetzt !== 'undefined' && albumJetzt")
    dort = pg.evaluate("t => t.map(iso => albumDesTages(iso, 0, null).id)", tage)
    context.close()

    assert hier == dort
    assert len(set(hier)) > 1, "immer dasselbe Album waere kein Zufall"


def test_day_never_repeats_yesterdays_album(tagseite):
    """Zwei gleiche Tage hintereinander saehen aus wie ein Fehler."""
    paare = tagseite.evaluate("""() => {
      const aus = [];
      let vorher = null;
      for (let n = 0; n < 40; n++){
        const iso = `2026-09-${String(n % 30 + 1).padStart(2,'0')}`;
        const a = albumDesTages(iso, 0, vorher);
        aus.push([vorher, a.id]);
        vorher = a.id;
      }
      return aus;
    }""")
    assert all(vorher != jetzt for vorher, jetzt in paare)


def test_day_queue_starts_over_at_the_end_of_the_album(tagseite):
    """Die Warteschlange endet nicht — sie endet mit dem Tag."""
    tagseite.click("#knopf")
    tagseite.wait_for_function("!ton.paused", timeout=5000)
    album = tagseite.evaluate("albumJetzt.id")
    tagseite.evaluate("""() => {
      deck.qi = deck.queue.length - 1;
      ton.dispatchEvent(new Event('ended'));
    }""")
    tagseite.wait_for_function("deck.qi === 0", timeout=5000)
    assert tagseite.evaluate("albumJetzt.id") == album, "das Album bleibt, der Tag entscheidet"
    tagseite.evaluate("ton.pause()")


def test_day_change_waits_for_the_running_track(tagseite):
    """Mitternacht schneidet keinen Titel ab."""
    vorher = tagseite.evaluate("albumJetzt.id")
    tagseite.click("#knopf")
    tagseite.wait_for_function("!ton.paused", timeout=5000)

    tagseite.evaluate("heute = () => new Date(2026, 7, 15, 9, 0)")   # naechster Tag
    tagseite.evaluate("pruefeTag()")
    assert tagseite.evaluate("tagWartet") is True
    assert tagseite.evaluate("albumJetzt.id") == vorher, "der laufende Titel wird zu Ende gespielt"

    tagseite.evaluate("ton.dispatchEvent(new Event('ended'))")
    tagseite.wait_for_function("id => albumJetzt.id !== id", arg=vorher, timeout=5000)
    assert tagseite.evaluate(
        "JSON.parse(localStorage.getItem('musiklib:tag')).datum") == "2026-08-15"
    tagseite.evaluate("ton.pause()")


def test_day_shares_the_session_shape_with_the_other_pages(tagseite):
    """Ein Schluessel, vier Oberflaechen — dieselbe Form."""
    tagseite.click("#knopf")
    tagseite.wait_for_function("!ton.paused", timeout=5000)
    tagseite.evaluate("ton.pause()")
    gespeichert = json.loads(tagseite.evaluate("localStorage.getItem('musiklib:session')"))
    assert gespeichert["qIndex"] == 0
    assert len(gespeichert["items"][0]) == 2, "Form muss [albumId, trackId] bleiben"
    assert gespeichert["items"][0][0] == tagseite.evaluate("albumJetzt.id")


def test_day_ignores_a_session_that_belongs_to_another_album(ctx, server):
    """Eine Sitzung von gestern darf nicht spielen, was die Karte nicht zeigt."""
    pg = ctx.new_page()
    pg.goto(server + "/tag", wait_until="domcontentloaded")
    pg.wait_for_function("typeof albumJetzt !== 'undefined' && albumJetzt")
    fremd = pg.evaluate("""() => {
      const a = ALBUMS.find(x => x.id !== albumJetzt.id);
      return {items: a.ids.map(id => [a.id, id]), qIndex: 1, position: 7, id: a.id};
    }""")
    pg.evaluate("s => localStorage.setItem('musiklib:session', JSON.stringify(s))", fremd)
    pg.reload(wait_until="domcontentloaded")
    pg.wait_for_function("typeof albumJetzt !== 'undefined' && albumJetzt")
    assert pg.evaluate("deck.queue[0]") == pg.evaluate("albumJetzt.ids[0]")
    assert pg.evaluate("deck.qi") == 0


def test_day_insists_when_a_track_change_is_refused(tagseite):
    """Ohne zweiten Knopf gibt es keinen Weg, sich von Hand zu erholen."""
    tagseite.evaluate("NACH_VERZUG = 150")
    tagseite.click("#knopf")
    tagseite.wait_for_function("!ton.paused", timeout=5000)
    tagseite.evaluate("""() => { ton.pause(); nachVersuche = 0; nachdruck(); }""")
    tagseite.wait_for_function("!ton.paused", timeout=5000)
    tagseite.evaluate("nachdruckEnde(); ton.pause()")


def test_day_reports_a_moved_file_instead_of_stopping_silently(tagseite):
    tagseite.evaluate("""() => { ton.src = '/api/stream/gibtsnicht'; ton.load(); }""")
    tagseite.wait_for_function("deck.fehler !== ''", timeout=5000)
    assert "nicht abspielbar" in tagseite.inner_text("#tl")
