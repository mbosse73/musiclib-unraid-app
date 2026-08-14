"""
Backend-Tests fuer app.py.

Laufen nur lokal, nie im Container:

    .venv/bin/pip install -r requirements.txt -r requirements-dev.txt
    .venv/bin/python -m pytest -q
    .venv/bin/python -m pytest -q -k cover      # einzelne Gruppe

Fixture-Helfer und das app_env-Fixture stehen in conftest.py.
"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from conftest import PNG, PNG_ALT, SILENT_FRAMES, write_mp3


# --------------------------------------------------------------------------
# Scan: Gruppierung und Tag-Fallbacks
# --------------------------------------------------------------------------

def test_scan_groups_tracks_into_albums(app_env):
    app, music, data = app_env
    write_mp3(music / "a/01.mp3", title="Eins", album="Werk", artist="Band", track="1")
    write_mp3(music / "a/02.mp3", title="Zwei", album="Werk", artist="Band", track="2")
    app.scan()

    lib = json.loads((data / "library.json").read_text())
    assert lib["album_count"] == 1
    assert lib["track_count"] == 2
    assert [t["title"] for t in lib["albums"][0]["tracks"]] == ["Eins", "Zwei"]


def test_untagged_file_uses_german_fallbacks(app_env):
    app, music, data = app_env
    (music / "namenlos.mp3").write_bytes(SILENT_FRAMES)
    app.scan()

    album = json.loads((data / "library.json").read_text())["albums"][0]
    assert album["title"] == "Unbekanntes Album"
    assert album["artist"] == "Unbekannter Interpret"
    assert album["tracks"][0]["title"] == "namenlos"


def test_unreadable_file_is_skipped_and_counted(app_env):
    app, music, data = app_env
    write_mp3(music / "gut.mp3")
    (music / "kaputt.mp3").write_bytes(b"kein mp3")
    app.scan()

    lib = json.loads((data / "library.json").read_text())
    assert lib["track_count"] == 1
    assert lib["skipped_count"] == 1
    assert lib["skipped_files"] == ["kaputt.mp3"]
    assert app.scan_state["skipped"] == 1


def test_skipped_paths_are_relative_never_absolute(app_env):
    app, music, data = app_env
    write_mp3(music / "gut.mp3")
    (music / "unter/tief/kaputt.mp3").parent.mkdir(parents=True)
    (music / "unter/tief/kaputt.mp3").write_bytes(b"kein mp3")
    app.scan()

    reported = json.loads((data / "library.json").read_text())["skipped_files"]
    assert reported == ["unter/tief/kaputt.mp3"]
    assert not any(str(music) in p for p in reported)


# --------------------------------------------------------------------------
# Katalogschutz
# --------------------------------------------------------------------------

def test_missing_music_dir_does_not_wipe_catalog(app_env, monkeypatch):
    app, music, data = app_env
    write_mp3(music / "a.mp3", album="Werk")
    app.scan()
    assert json.loads((data / "library.json").read_text())["album_count"] == 1

    monkeypatch.setattr(app, "MUSIC_DIR", Path("/gibt/es/nicht"))
    app.scan()

    assert json.loads((data / "library.json").read_text())["album_count"] == 1
    assert "nicht gefunden" in app.scan_state["error"]


def test_empty_music_dir_does_not_wipe_catalog(app_env, tmp_path, monkeypatch):
    app, music, data = app_env
    write_mp3(music / "a.mp3", album="Werk")
    app.scan()

    leer = tmp_path / "leer"
    leer.mkdir()
    monkeypatch.setattr(app, "MUSIC_DIR", leer)
    app.scan()

    assert json.loads((data / "library.json").read_text())["album_count"] == 1
    assert "nicht ueberschrieben" in app.scan_state["error"]


def test_empty_music_dir_is_allowed_without_existing_catalog(app_env):
    app, music, data = app_env
    app.scan()

    assert json.loads((data / "library.json").read_text())["album_count"] == 0
    assert app.scan_state["error"] is None


# --------------------------------------------------------------------------
# Cover
# --------------------------------------------------------------------------

def test_cover_is_taken_from_any_track_not_just_the_first(app_env):
    app, music, data = app_env
    write_mp3(music / "w/01.mp3", album="Werk", track="1", cover=None)
    write_mp3(music / "w/02.mp3", album="Werk", track="2", cover=PNG)
    app.scan()

    album = json.loads((data / "library.json").read_text())["albums"][0]
    assert album["cover"], "Album mit Artwork in Track 2 darf nicht coverlos bleiben"
    assert (data / "covers" / album["cover"]).exists()


def test_folder_image_is_used_when_nothing_is_embedded(app_env):
    app, music, data = app_env
    write_mp3(music / "w/01.mp3", album="Werk", cover=None)
    (music / "w/cover.jpg").write_bytes(PNG)
    app.scan()

    album = json.loads((data / "library.json").read_text())["albums"][0]
    assert album["cover"]
    assert (data / "covers" / album["cover"]).read_bytes() == PNG


def test_changed_cover_is_picked_up_on_rescan(app_env):
    app, music, data = app_env
    track = write_mp3(music / "w/01.mp3", album="Werk", cover=PNG)
    app.scan()
    album = json.loads((data / "library.json").read_text())["albums"][0]
    assert (data / "covers" / album["cover"]).read_bytes() == PNG

    write_mp3(track, album="Werk", cover=PNG_ALT)
    app.scan()

    album = json.loads((data / "library.json").read_text())["albums"][0]
    assert (data / "covers" / album["cover"]).read_bytes() == PNG_ALT


def test_orphaned_covers_are_removed(app_env):
    app, music, data = app_env
    write_mp3(music / "w/01.mp3", album="Werk", cover=PNG)
    app.scan()
    assert len(list((data / "covers").iterdir())) == 1

    (music / "w/01.mp3").unlink()
    write_mp3(music / "x/01.mp3", album="Anderes", cover=PNG)
    app.scan()

    covers = list((data / "covers").iterdir())
    album = json.loads((data / "library.json").read_text())["albums"][0]
    assert [c.name for c in covers] == [album["cover"]]


# --------------------------------------------------------------------------
# Tag-Cache (inkrementeller Scan)
# --------------------------------------------------------------------------

def test_second_scan_reuses_cached_tags(app_env, monkeypatch):
    app, music, data = app_env
    for i in range(3):
        write_mp3(music / f"{i}.mp3", title=f"T{i}", album="Werk")
    app.scan()

    calls = []
    original = app.read_tags
    monkeypatch.setattr(app, "read_tags", lambda p: (calls.append(p), original(p))[1])
    app.scan()

    assert calls == [], "unveraenderte Dateien duerfen nicht erneut geparst werden"


def test_changed_file_bypasses_the_cache(app_env, monkeypatch):
    app, music, data = app_env
    a = write_mp3(music / "a.mp3", title="Alt", album="Werk")
    write_mp3(music / "b.mp3", title="B", album="Werk")
    app.scan()

    write_mp3(a, title="Neu", album="Werk")
    calls = []
    original = app.read_tags
    monkeypatch.setattr(app, "read_tags", lambda p: (calls.append(p), original(p))[1])
    app.scan()

    assert calls == [a]
    titles = {t["title"] for t in json.loads((data / "library.json").read_text())["albums"][0]["tracks"]}
    assert "Neu" in titles and "Alt" not in titles


def test_cache_version_mismatch_forces_full_reread(app_env, monkeypatch):
    app, music, data = app_env
    write_mp3(music / "a.mp3", album="Werk")
    app.scan()

    raw = json.loads((data / "tagcache.json").read_text())
    raw["version"] = app.TAGCACHE_VERSION + 1
    (data / "tagcache.json").write_text(json.dumps(raw))

    calls = []
    original = app.read_tags
    monkeypatch.setattr(app, "read_tags", lambda p: (calls.append(p), original(p))[1])
    app.scan()

    assert len(calls) == 1


def test_deleted_files_drop_out_of_the_cache(app_env):
    app, music, data = app_env
    write_mp3(music / "a.mp3", album="Werk")
    write_mp3(music / "b.mp3", album="Werk")
    app.scan()

    (music / "b.mp3").unlink()
    app.scan()

    entries = json.loads((data / "tagcache.json").read_text())["entries"]
    assert len(entries) == 1
    assert not any(k.endswith("b.mp3") for k in entries)


# --------------------------------------------------------------------------
# Scan-Steuerung
# --------------------------------------------------------------------------

def test_running_scan_blocks_a_second_one(app_env):
    app, music, data = app_env
    assert app._claim_scan() is True
    assert app._claim_scan() is False, "zweiter Scan darf den Slot nicht bekommen"
    app._release_scan()
    assert app._claim_scan() is True
    app._release_scan()


def test_post_scan_reports_running_before_returning(app_env):
    app, music, data = app_env
    write_mp3(music / "a.mp3")
    # Erst scannen, damit library.json existiert — sonst startet der Lifespan
    # beim Oeffnen des TestClient selbst einen Scan und belegt den Slot.
    app.scan()

    with TestClient(app.app) as client:
        body = client.post("/api/scan").json()

    # Der Slot muss beim Erzeugen der Antwort schon belegt sein. Sonst saehe
    # der erste Status-Poll running=False und wuerde das Polling einstellen,
    # bevor der Scan ueberhaupt begonnen hat.
    # (Ein Folge-Poll laesst sich hier nicht pruefen: TestClient arbeitet den
    # BackgroundTask noch vor der naechsten Anfrage ab.)
    assert body["status"] == "started"
    assert body["running"] is True


def test_progress_counts_up_to_total(app_env):
    app, music, data = app_env
    for i in range(4):
        write_mp3(music / f"{i}.mp3")
    app.scan()

    assert app.scan_state["progress"] == app.scan_state["total"] == 4


# --------------------------------------------------------------------------
# HTTP-Endpunkte
# --------------------------------------------------------------------------

@pytest.fixture
def client(app_env):
    app, music, data = app_env
    write_mp3(music / "w/01.mp3", title="Eins", album="Werk", cover=PNG)
    app.scan()
    with TestClient(app.app) as c:
        yield c, app, data


def test_library_endpoint_is_served(client):
    c, app, data = client
    lib = c.get("/api/library").json()
    assert lib["album_count"] == 1


def test_player_page_is_served_at_every_address(client):
    """Eine Datei, vier Adressen — seit Etappe 4 gehoert auch / dazu.

    Die Adresse ist nur die Voreinstellung des Formats; welche Ansicht
    gebaut wird, entscheidet der Browser aus dem localStorage.
    """
    c, app, data = client
    seiten = []
    for pfad in ("/", "/ipad", "/pc", "/mobil"):
        r = c.get(pfad)
        assert r.status_code == 200
        assert "text/html" in r.headers["content-type"]
        seiten.append(r.text)
    assert len(set(seiten)) == 1, "alle Adressen liefern dieselbe Datei"
    assert "<title>Musiklib · Spieler</title>" in seiten[0]
    # Ohne diese Zeile startet "Zum Home-Bildschirm" mit Safari-Leiste.
    assert 'name="apple-mobile-web-app-capable"' in seiten[0]


@pytest.mark.parametrize("pfad,titel", [
    ("/mobil-alt", "<title>Musiklib</title>"),
    ("/klassisch", "<title>Musiklib</title>"),
])
def test_the_old_surfaces_stay_reachable(client, pfad, titel):
    """Beide Rueckwege bleiben, solange die Dateien mitkommen.

    Das laeuft auf einem NAS: ein Spieler, der klemmt, heisst keine Musik.
    Sie teilen sich alle Schluessel mit der neuen Seite, man kann also
    mitten im Lied wechseln.
    """
    c, app, data = client
    r = c.get(pfad)
    assert r.status_code == 200
    assert titel in r.text


def test_missing_page_file_says_which_one(client, tmp_path, monkeypatch):
    """Eine vergessene Datei ist ein Kopierfehler, kein Serverabsturz.

    Der Code wird per SMB kopiert; bleibt dabei eine Oberflaeche liegen,
    muss der Browser sagen welche — nicht „Internal Server Error".
    """
    c, app, data = client
    monkeypatch.setattr(app, "APP_DIR", tmp_path)
    r = c.get("/tag")
    assert r.status_code == 404
    assert "tag.html" in r.json()["detail"]


def test_day_page_is_served(client):
    """Vierte Oberflaeche: /tag liefert den Spieler mit einem Knopf."""
    c, app, data = client
    r = c.get("/tag")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "<title>Musiklib · Album des Tages</title>" in r.text
    # Ohne diese Zeile startet "Zum Home-Bildschirm" mit Safari-Leiste.
    assert 'name="apple-mobile-web-app-capable"' in r.text


def test_stream_supports_range_requests(client):
    c, app, data = client
    track_id = next(iter(json.loads((data / "tracks.json").read_text())))
    r = c.get(f"/api/stream/{track_id}", headers={"Range": "bytes=0-99"})

    # Ohne 206 + Content-Range funktioniert das Spulen auf dem Handy nicht.
    assert r.status_code == 206
    assert r.headers["content-range"].startswith("bytes 0-99/")
    assert len(r.content) == 100


def test_stream_rejects_unknown_track(client):
    c, app, data = client
    assert c.get("/api/stream/gibtesnicht").status_code == 404


@pytest.mark.parametrize("name", ["../app.py", "..%2f..%2fapp.py", "....//app.py",
                                  "sub/../app.py", "..\\app.py"])
def test_cover_endpoint_rejects_path_traversal(client, name):
    c, app, data = client
    assert c.get(f"/api/cover/{name}").status_code == 404


def test_cover_endpoint_serves_real_cover(client):
    c, app, data = client
    album = c.get("/api/library").json()["albums"][0]
    r = c.get(f"/api/cover/{album['cover']}")
    assert r.status_code == 200
    assert "max-age" in r.headers.get("cache-control", "")


def test_scan_error_message_carries_no_traceback(app_env, monkeypatch):
    app, music, data = app_env

    def boom(*a, **k):
        raise RuntimeError("interner Pfad /geheim/pfad")

    monkeypatch.setattr(app, "_collect_mp3s", boom)
    app.scan()

    assert "geheim" not in app.scan_state["error"]
    assert "Container-Log" in app.scan_state["error"]
