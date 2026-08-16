# -*- coding: utf-8 -*-
"""Alle Aufnahmen fuers Konzeptregister nach kb/ — gross genug zum Vergroessern.

Fuenf Quellen, in dieser Reihenfolge:
  A  design/previews/*.png        die gelieferten Paket-Vorschauen, nur umkopiert
     design/html/*.html           die vier Paket-Blaetter ohne geliefertes PNG
  B  design/entwuerfe/html/*.html eigene Entwuerfe, beide Buehnen
  C  mockups/player/1[5-9]|2[0-5] die gezeichneten Blaetter, je Variante ein Bild
  D  das laufende Programm        jede Auslage in player.html plus /tag
  E  mockups/acht-themen/*.jpg    die Vorlagen der acht portierten Themen

Fuer D laeuft app.py gegen eine eigene Testsammlung (sammlung.py) in einem
Temp-Ordner — die echte Musik wird nie angefasst. Braucht Pillow und
Playwright; den Browser findet MUSIKLIB_CHROME, sonst wird gesucht.

    .venv/bin/python design/register/aufnahmen.py
    python3 design/register/bauen.py       # Register neu bauen
"""
import os
import pathlib
import shutil
import socket
import subprocess
import sys
import tempfile
import time

HIER = pathlib.Path(__file__).resolve().parent
REPO = HIER.parent.parent
sys.path.insert(0, str(HIER))
sys.path.insert(0, str(REPO))

from PIL import Image
from playwright.sync_api import sync_playwright

import sammlung

KB = HIER / 'kb'
QUER, HOCH, GUETE = 1400, 700, 78

TEL, TABHOCH, PC = (390, 844), (1024, 1366), (1440, 900)
PFAD = {'telefon': '/mobil', 'tablet': '/ipad', 'pc': '/pc'}

# Je Auslage, welche Aufnahmen. Der Zusatz steht so im Register (daten_gruppen.py):
# ohne Zusatz sind die reinen Telefon-Auslagen, alles andere traegt _quer/_hoch.
APP = [
    ('geraet',          [('pc', '_quer', PC), ('telefon', '_hoch', TEL)]),
    ('werkstisch',      [('pc', '_quer', PC), ('tablet', '_hoch', TABHOCH)]),
    ('vollbild',        [('pc', '_quer', PC), ('tablet', '_hoch', TABHOCH)]),
    ('deck',            [('pc', '_quer', PC), ('tablet', '_hoch', TABHOCH)]),
    ('handgeraet',      [('pc', '_quer', PC), ('tablet', '_hoch', TABHOCH)]),
    ('aufgeschlagen',   [('pc', '_quer', PC), ('tablet', '_hoch', TABHOCH)]),
    ('register',        [('pc', '_quer', PC)]),          # hochkant nicht gezeichnet
    ('bedienteil',      [('pc', '_quer', PC), ('tablet', '_hoch', TABHOCH)]),
    ('konsole',         [('pc', '_quer', PC), ('tablet', '_hoch', TABHOCH)]),
    ('pult',            [('pc', '_quer', PC), ('tablet', '_hoch', TABHOCH)]),
    ('turm',            [('pc', '_quer', PC), ('tablet', '_hoch', TABHOCH)]),
    ('vollverstaerker', [('pc', '_quer', PC), ('tablet', '_hoch', TABHOCH)]),
    ('papier',          [('telefon', '', TEL)]),
    ('wueste',          [('telefon', '', TEL)]),
    ('kissen',          [('telefon', '', TEL)]),
    ('karte',           [('telefon', '', TEL)]),
    ('kiesel',          [('telefon', '', TEL)]),
    # die acht aus mockups/acht-themen, je Telefon und PC
    ('abzug',           [('telefon', '_hoch', TEL), ('pc', '_quer', PC)]),
    ('entwicklung',     [('telefon', '_hoch', TEL), ('pc', '_quer', PC)]),
    ('milchglas',       [('telefon', '_hoch', TEL), ('pc', '_quer', PC)]),
    ('programmheft',    [('telefon', '_hoch', TEL), ('pc', '_quer', PC)]),
    ('spur',            [('telefon', '_hoch', TEL), ('pc', '_quer', PC)]),
    ('emaille',         [('telefon', '_hoch', TEL), ('pc', '_quer', PC)]),
    ('gespritzt',       [('telefon', '_hoch', TEL), ('pc', '_quer', PC)]),
    ('kalender',        [('telefon', '_hoch', TEL), ('pc', '_quer', PC)]),
]

# Ein Album antippen, damit die Auslagen nicht im Leerlauf aufgenommen werden.
STARTEN = """() => {
  const el = [...document.querySelectorAll('[data-alb]')].find(e => e.dataset.alb);
  if (el) el.click();
}"""


def standbild(b, datei, name):
    """Ein Standbild ohne Skript: _iphone hochkant, alles andere quer."""
    hoch = '_iphone' in datei.name
    w, h = (1080, 2340) if hoch else (1600, 1000)
    pg = b.new_page(viewport={'width': w, 'height': h},
                    device_scale_factor=1 if hoch else 2)
    pg.goto('file://' + str(datei))
    pg.wait_for_timeout(150)
    pg.screenshot(path=str(KB / 'tmp.png'))
    pg.close()
    ablegen(KB / 'tmp.png', name)


def browser_pfad():
    p = os.environ.get('MUSIKLIB_CHROME')
    if p:
        return p
    for muster in ('/opt/pw-browsers/chromium*/chrome-linux/chrome',
                   '/opt/pw-browsers/chromium*/chrome-linux64/chrome'):
        treffer = sorted(pathlib.Path('/').glob(muster.lstrip('/')))
        if treffer:
            return str(treffer[-1])
    return None            # dann sucht Playwright selbst


def ablegen(png, name):
    """Aufnahme verkleinern und als JPEG ablegen — hoch und quer verschieden."""
    im = Image.open(png).convert('RGB')
    grenze = (QUER, QUER) if im.width >= im.height else (HOCH, HOCH * 3)
    im.thumbnail(grenze, Image.LANCZOS)
    im.save(KB / f'{name}.jpg', quality=GUETE, optimize=True, subsampling=1)


def warte_auf(port, sekunden=30):
    ende = time.time() + sekunden
    while time.time() < ende:
        try:
            socket.create_connection(('127.0.0.1', port), .3).close()
            return True
        except OSError:
            time.sleep(.25)
    return False


def app_schuss(b, lay, ziel, mass, name, port):
    w, h = mass
    ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2)
    ctx.route('**fonts.googleapis.com**', lambda r: r.abort())
    pg = ctx.new_page()
    pg.add_init_script(f"""
      localStorage.setItem('musiklib:ziel', '{ziel}');
      localStorage.setItem('musiklib:alleansichten', '1');
      localStorage.setItem('musiklib:layout', JSON.stringify({{{ziel}: '{lay}'}}));""")
    pg.goto(f'http://127.0.0.1:{port}{PFAD[ziel]}')
    pg.wait_for_timeout(1100)
    pg.evaluate(STARTEN)
    pg.wait_for_timeout(1800)
    pg.screenshot(path=str(KB / 'tmp.png'))
    ctx.close()
    ablegen(KB / 'tmp.png', name)


def main():
    KB.mkdir(exist_ok=True)
    for alt in KB.glob('*.jpg'):
        alt.unlink()

    arbeit = pathlib.Path(tempfile.mkdtemp(prefix='musiklib-register-'))
    alben, titel = sammlung.baue(arbeit / 'musik')
    print(f'Sammlung: {alben} Alben, {titel} Titel')

    port = 8095
    srv = subprocess.Popen(
        [sys.executable, 'app.py'], cwd=REPO,
        env={**os.environ, 'MUSIC_DIR': str(arbeit / 'musik'),
             'DATA_DIR': str(arbeit / 'daten'), 'PORT': str(port)},
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not warte_auf(port):
        srv.terminate()
        raise SystemExit(f'app.py kam auf Port {port} nicht hoch')
    time.sleep(3)          # der erste Scan laeuft im Hintergrund

    try:
        # ── A · Paket: die gelieferten Vorschauen, nur umkopiert ─────────
        for p in sorted((REPO / 'design/previews').glob('*.png')):
            ablegen(p, p.stem.replace('_pc', ''))

        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=browser_pfad(),
                                  args=['--autoplay-policy=no-user-gesture-required'])

            # Zu vier Paket-Blaettern gibt es kein geliefertes PNG (die zwei
            # ueberlebenden Fassungen des gestrichenen Blattes 33, je zwei
            # Buehnen) — die werden aus ihrem HTML aufgenommen.
            for f in sorted((REPO / 'design/html').glob('*.html')):
                if (REPO / 'design/previews' / (f.stem + '.png')).exists():
                    continue
                standbild(b, f, f.stem.replace('_pc', ''))

            # ── B · eigene Entwuerfe, beide Buehnen ──────────────────────
            for f in sorted((REPO / 'design/entwuerfe/html').glob('*.html')):
                standbild(b, f, f.stem.replace('_pc', ''))

            # ── C · gezeichnete Blaetter 15–25, je Variante ein Bild ─────
            for f in sorted((REPO / 'mockups/player').glob('[12][0-9]-*.html')):
                if not 15 <= int(f.name[:2]) <= 25:
                    continue
                pg = b.new_page(viewport={'width': 1500, 'height': 1100},
                                device_scale_factor=2)
                pg.goto('file://' + str(f))
                pg.wait_for_timeout(400)
                for i, el in enumerate(pg.query_selector_all('.entwurf .rahmen'), 1):
                    el.screenshot(path=str(KB / 'tmp.png'))
                    ablegen(KB / 'tmp.png', f'blatt{f.name[:2]}v{i}')
                pg.close()

            # ── D · das laufende Programm ────────────────────────────────
            for lay, schuesse in APP:
                for ziel, zusatz, mass in schuesse:
                    app_schuss(b, lay, ziel, mass, f'app_{lay}{zusatz}', port)

            ctx = b.new_context(viewport={'width': 390, 'height': 844},
                                device_scale_factor=2)
            ctx.route('**fonts.googleapis.com**', lambda r: r.abort())
            pg = ctx.new_page()
            pg.goto(f'http://127.0.0.1:{port}/tag')
            pg.wait_for_timeout(3500)
            pg.screenshot(path=str(KB / 'tmp.png'))
            ctx.close()
            ablegen(KB / 'tmp.png', 'app_tag')
            b.close()

        # ── E · die Vorlagen der acht portierten Themen ──────────────────
        # Der Ordner ist eine eingefrorene Sicherung; die Aufnahmen liegen
        # dort schon fertig, hier werden sie nur aufs Registermass gebracht.
        for f in sorted((REPO / 'mockups/acht-themen').glob('thema_*.jpg')):
            ablegen(f, f.stem)
    finally:
        srv.terminate()
        shutil.rmtree(arbeit, ignore_errors=True)

    (KB / 'tmp.png').unlink(missing_ok=True)
    bilder = sorted(KB.glob('*.jpg'))
    gesamt = sum(p.stat().st_size for p in bilder)
    print(len(bilder), 'Bilder,', gesamt // 1024, 'KB roh,',
          round(gesamt * 4 / 3 / 1024 / 1024, 2), 'MB als data-URI')


if __name__ == '__main__':
    main()
