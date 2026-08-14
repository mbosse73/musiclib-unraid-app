"""
Gemeinsame Test-Fixtures fuer test_app.py und test_frontend.py.

Es liegen keine echten MP3s im Repo. Die Helfer hier schreiben rohe
MPEG1-Layer-III-Frames (Header + Nullen, 417 Byte pro Frame) und taggen sie
mit mutagen — mutagen liest die anstandslos und meldet eine Spieldauer.
"""

import importlib
import sys

import pytest
from mutagen.id3 import ID3, APIC, TALB, TDRC, TIT2, TPE1, TPE2, TRCK

# 1x1 PNG, schwarz — reicht als Coverbild fuer mutagen und den Browser.
PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000d49444154789c63606060f80f00010401005fe5c34b0000000049454e44ae426082"
)
# Zweites, sichtbar anderes Bild — fuer den Test auf ausgetauschte Cover.
PNG_ALT = bytes.fromhex(
    "89504e470d0a1a0a0000000d494844520000000200000002080600000072b60d24"
    "0000001149444154789c63f8cfc0f01f8419600c0047ca07f967596eb70000000049454e44ae426082"
)

_FRAME = b"\xff\xfb\x90\x00" + b"\x00" * 413  # 417 Byte, ~26 ms
SILENT_FRAMES = _FRAME * 40                   # ~1 s, reicht fuers Backend


def frames(seconds: float) -> bytes:
    """Stille MP3-Daten der ungefaehren Laenge.

    Der Frontend-Test braucht Titel, die waehrend der Pruefschritte nicht
    durchlaufen — sonst wandert die Wiedergabe weiter und die Zusicherungen
    beziehen sich auf einen anderen Titel als gedacht.
    """
    return _FRAME * max(1, int(seconds / 0.026))


def write_mp3(path, *, title="Titel", artist="Interpret", album="Album",
              album_artist=None, track="1", year=None, cover=None,
              data=SILENT_FRAMES):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    tags = ID3()
    tags.add(TIT2(encoding=3, text=title))
    tags.add(TPE1(encoding=3, text=artist))
    tags.add(TALB(encoding=3, text=album))
    tags.add(TPE2(encoding=3, text=album_artist or artist))
    if track:
        tags.add(TRCK(encoding=3, text=track))
    if year:
        tags.add(TDRC(encoding=3, text=str(year)))
    if cover:
        tags.add(APIC(encoding=3, mime="image/png", type=3, desc="c", data=cover))
    tags.save(path)
    return path


@pytest.fixture
def app_env(tmp_path, monkeypatch):
    """Frisch importiertes app-Modul mit eigenem MUSIC_DIR und DATA_DIR."""
    music = tmp_path / "music"
    data = tmp_path / "data"
    music.mkdir()
    data.mkdir()
    monkeypatch.setenv("MUSIC_DIR", str(music))
    monkeypatch.setenv("DATA_DIR", str(data))
    sys.modules.pop("app", None)
    app_module = importlib.import_module("app")
    app_module.ensure_dirs()
    return app_module, music, data
