# -*- coding: utf-8 -*-
"""Die Abwandlungen von 36 und 37 aus den gelieferten Blättern ableiten.

    python3 _ableiten.py

Beide Fassungen unterscheiden sich vom Original in genau zwei Handgriffen: der
QR-Code fällt weg, und auf dem Rechner steht die Tastenreihe mittig statt
linksbündig. Weil die Vorlagen in `../html/` sich ändern können, wird hier nicht
von Hand nachgebaut, sondern jedes Mal neu abgeleitet — die `assert` schlagen
an, sobald das Original nicht mehr die erwartete Form hat.

`foto31a_…` liegt nicht hier drin: es ist von Hand aus dem Original erzeugt und
seither unverändert.
"""
import pathlib
import re

HTML = pathlib.Path(__file__).resolve().parents[1] / 'html'
HIER = pathlib.Path(__file__).resolve().parent

# Nummer, Name im Paket, Name der Abwandlung, und je Rechner-Blatt die beiden
# Zeilen, die die Tastenreihe in die Mitte holen — 36 richtet auf der Mitte aus,
# 37 auf der Grundlinie, deshalb steht der Bibliotheksknopf einmal mittig und
# einmal unten am Rand.
BLAETTER = [
    ('36', 'Song-Poster-Schwarz', 'Song-Poster-Schwarz-Ohne-QR',
     'align-items:center;gap:26px;margin-top:30px',
     'top:50%;transform:translateY(-50%)'),
    ('37', 'Song-Poster-Weiss', 'Song-Poster-Weiss-Ohne-QR',
     'align-items:flex-end;gap:26px;margin-top:28px',
     'bottom:0'),
]

QR = re.compile(r'\s*<div style="background:#fff;padding:\d+px">\s*<svg[^>]*>.*?</svg></div>',
                re.S)


def ohne_qr(html):
    neu, n = QR.subn('', html)
    assert n == 1, f'QR-Block nicht eindeutig gefunden ({n}×)'
    return neu


def reihe_mittig(html, reihe, halt):
    """Nur Rechner: Transporttasten in die Mitte, Bibliothek bleibt am Rand."""
    alt_reihe = f'<div style="display:flex;{reihe}">'
    neu_reihe = f'<div style="position:relative;display:flex;{reihe};justify-content:center">'
    alt_bib = '<div style="margin-left:auto">'
    neu_bib = f'<div style="position:absolute;right:0;{halt}">'
    for alt in (alt_reihe, alt_bib):
        assert html.count(alt) == 1, f'nicht eindeutig: {alt[:40]}…'
    return html.replace(alt_reihe, neu_reihe).replace(alt_bib, neu_bib)


def bau():
    for nr, name, neuer_name, reihe, halt in BLAETTER:
        for art in ('iphone', 'pc'):
            html = (HTML / f'foto{nr}_{name}_{art}.html').read_text(encoding='utf-8')
            html = ohne_qr(html)
            if art == 'pc':
                html = reihe_mittig(html, reihe, halt)
            ziel = HIER / f'foto{nr}a_{neuer_name}_{art}.html'
            ziel.write_text(html, encoding='utf-8')
            yield ziel


if __name__ == '__main__':
    for pfad in bau():
        print(f'{pfad.name}  {pfad.stat().st_size / 1024:.1f} KB')
