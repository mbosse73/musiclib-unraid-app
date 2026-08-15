# -*- coding: utf-8 -*-
"""Alle Blätter des Pakets neu erzeugen.

    python3 baualle.py                    # nur ../html/
    python3 baualle.py --vorschau         # zusätzlich ../previews/ (braucht Playwright)
    python3 baualle.py --vorschau 18 35   # nur diese Nummern neu aufnehmen

Die HTML-Dateien sind die verbindliche Quelle (siehe ../README.md); dieses
Skript ist der Weg, sie aus den Generatoren zurückzugewinnen. `MUSIKLIB_CHROME`
überschreibt die Browsersuche, wie in der Testsuite.
"""
import os
import pathlib
import sys

import designs3
import d34, d35, d36, d37, d38  # noqa: F401  — der Import registriert die Blätter

HTML = pathlib.Path(__file__).resolve().parents[1] / 'html'
VORSCHAU = pathlib.Path(__file__).resolve().parents[1] / 'previews'

# Hochformate mit grosser Mittel-/Unterlücke: Abstände gleichmässig verteilen.
AUSGLEICH = {'19', '20', '22', '23', '24', '26', '27', '28', '29', '30', '31', '32', '35'}
AUSGLEICH_CSS = """
.stage > div{justify-content:space-between !important}
.stage div[style*="margin-top:auto"]{margin-top:24px !important}
.stage div[style*="margin:auto 0"]{margin:24px 0 !important}
"""


def blaetter():
    for (nr, name, plat, w, h, html) in designs3.D:
        if plat == 'iphone' and nr in AUSGLEICH:
            html = html.replace('</style>', AUSGLEICH_CSS + '</style>', 1)
        yield nr, name, plat, w, h, html


def schreibe():
    HTML.mkdir(exist_ok=True)
    for nr, name, plat, w, h, html in blaetter():
        ziel = HTML / f'foto{nr}_{name}_{plat}.html'
        ziel.write_text(html, encoding='utf-8')
        yield ziel


def vorschau(nummern=()):
    """PNG in doppelter Auflösung. Ohne `nummern` alle Blätter, sonst nur diese —
    ein neuer Browser rendert nicht Pixel für Pixel wie der alte, deshalb wird
    nur neu aufgenommen, was sich wirklich geändert hat."""
    from playwright.sync_api import sync_playwright
    VORSCHAU.mkdir(exist_ok=True)
    chrome = os.environ.get('MUSIKLIB_CHROME')
    with sync_playwright() as p:
        b = p.chromium.launch(**({'executable_path': chrome} if chrome else {}))
        for nr, name, plat, w, h, _ in blaetter():
            if nummern and nr not in nummern:
                continue
            quelle = HTML / f'foto{nr}_{name}_{plat}.html'
            pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
            pg.goto('file://' + str(quelle))
            pg.wait_for_timeout(150)
            ziel = VORSCHAU / f'foto{nr}_{name}_{plat}.png'
            pg.screenshot(path=str(ziel))
            pg.close()
            yield ziel
        b.close()


if __name__ == '__main__':
    for pfad in schreibe():
        print(f'{pfad.name}  {pfad.stat().st_size / 1024:.1f} KB')
    if '--vorschau' in sys.argv:
        for pfad in vorschau([a for a in sys.argv[1:] if not a.startswith('--')]):
            print(f'{pfad.name}  {pfad.stat().st_size / 1024:.1f} KB')
