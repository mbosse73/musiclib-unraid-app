# -*- coding: utf-8 -*-
"""Gemeinsame Bausteine der Entwürfe aus den Ordnern player2/ und player3/.

Dieselben Regeln wie im gelieferten Paket: eigenständiges HTML, kein Framework,
keine externen Dateien, keine Webfonts — alles CSS und inline SVG. Dokument,
Wellenform, Zeigerinstrument und die Transportzeichen kommen aus
design/src/lib.py, damit beide Sätze dieselbe Sprache sprechen.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'src'))
from lib import (doc, waveform, vumeter, tri, pausei, prev, nexti,  # noqa: E402
                 SANS, MONO, SERIF, COND, IMPACT)

TEL = (1080, 2340)
PC = (1600, 1000)

# Ein Album für alle Blätter — so vergleicht man Form, nicht Inhalt.
A = dict(
    titel='Blue in Green', interpret='Miles Davis', album='Kind of Blue', jahr='1959',
    pos='02:14', rest='-03:23', dauer='05:37', frac=0.40, sammlung=240,
    tracks=[('01', 'So What', '9:22'), ('02', 'Freddie Freeloader', '9:46'),
            ('03', 'Blue in Green', '5:37'), ('04', 'All Blues', '11:33')],
    laeuft=2,
)


# ---- Zeichen ---------------------------------------------------------------
def biblio(size, color):
    """Der Bibliotheks-Zugang trägt überall dasselbe Zeichen: drei Buchrücken."""
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24">'
            f'<rect x="3" y="4" width="3" height="16" rx="1" fill="{color}"/>'
            f'<rect x="8" y="4" width="3" height="16" rx="1" fill="{color}"/>'
            f'<path d="M14.5 5.4 L18.2 4.5 L21.5 19 L17.8 19.9 Z" fill="{color}"/></svg>')


def lupe(size, color, sw=2):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round">'
            f'<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5 L21 21"/></svg>')


def mischen(size, color, sw=2):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round">'
            f'<path d="M3 6h4l4 12h6M3 18h4l2-6"/><path d="M17 3l4 3-4 3M17 15l4 3-4 3"/></svg>')


def wiederholen(size, color, sw=2):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round">'
            f'<path d="M4 9a5 5 0 0 1 5-5h9"/><path d="M15 1l3 3-3 3"/>'
            f'<path d="M20 15a5 5 0 0 1-5 5H6"/><path d="M9 23l-3-3 3-3"/></svg>')


def laut(size, color, sw=1.8):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round"><path d="M4 9v6h4l5 4V5L8 9z" fill="{color}"/>'
            f'<path d="M17 9.5a4 4 0 0 1 0 5"/><path d="M19.5 7a7.5 7.5 0 0 1 0 10"/></svg>')


def cover(size, radius, a, b, strich='#ffffff', deckung=.9, klasse=''):
    """Abstraktes Albumbild: Verlauf, ein Kreis, zwei Linien — kein Foto."""
    r = size / 2
    kn = f'{int(size)}{a[1:4]}{b[1:4]}'
    return f'''<svg class="{klasse}" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
<defs><linearGradient id="cg{kn}" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="{a}"/><stop offset="100%" stop-color="{b}"/></linearGradient></defs>
<rect x="0" y="0" width="{size}" height="{size}" rx="{radius}" fill="url(#cg{kn})"/>
<circle cx="{r * 1.06:.1f}" cy="{r * .82:.1f}" r="{r * .40:.1f}" fill="none"
  stroke="{strich}" stroke-width="{max(1.2, size * .008):.1f}" opacity="{deckung * .55}"/>
<path d="M{r * .30:.1f} {r * 1.42:.1f} L{r * 1.72:.1f} {r * 1.42:.1f}" stroke="{strich}"
  stroke-width="{max(1.2, size * .006):.1f}" opacity="{deckung * .35}"/>
<path d="M{r * .30:.1f} {r * 1.60:.1f} L{r * 1.30:.1f} {r * 1.60:.1f}" stroke="{strich}"
  stroke-width="{max(1.2, size * .006):.1f}" opacity="{deckung * .22}"/></svg>'''


def platte(size, label, rille='#2a2a2c', grund='#0b0b0c', ringe=26, glanz=True):
    """Schallplatte von oben. Die Rillen sind einzelne Kreise, kein Bild."""
    r = size / 2
    kn = f'{int(size)}{label[1:4]}'
    gl = (f'<radialGradient id="pg{kn}" cx="36%" cy="30%" r="76%">'
          f'<stop offset="0%" stop-color="#4d4d51"/><stop offset="20%" stop-color="#161618"/>'
          f'<stop offset="100%" stop-color="{grund}"/></radialGradient>') if glanz else ''
    rs = ''.join(
        f'<circle cx="{r}" cy="{r}" r="{r * .31 + i * (r * .64 / ringe):.1f}" fill="none" '
        f'stroke="{rille}" stroke-width="{.9 if i % 3 else 1.5}" opacity="{.5 if i % 3 else .8}"/>'
        for i in range(ringe))
    return (f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">'
            f'<defs>{gl}</defs>'
            f'<circle cx="{r}" cy="{r}" r="{r}" fill="{f"url(#pg{kn})" if glanz else grund}"/>'
            f'{rs}<circle cx="{r}" cy="{r}" r="{r * .28:.1f}" fill="{label}"/>'
            f'<circle cx="{r}" cy="{r}" r="{r * .028:.1f}" fill="#f2f2f0"/></svg>')


def kassette(b, h, gehaeuse, streifen, etikett='#f2efe6', rand='#1a1a1a'):
    """Eine Kassette von vorn — Gehäuse, Etikett, zwei Wickel, fünf Schrauben."""
    rw = b * .155
    return f'''<svg viewBox="0 0 {b} {h}" width="{b}" height="{h}">
<rect x="0" y="0" width="{b}" height="{h}" rx="{h * .09:.1f}" fill="{gehaeuse}"
  stroke="{rand}" stroke-width="{max(1, b * .006):.1f}"/>
<rect x="{b * .05:.1f}" y="{h * .07:.1f}" width="{b * .90:.1f}" height="{h * .30:.1f}"
  rx="{h * .03:.1f}" fill="{etikett}"/>
<rect x="{b * .05:.1f}" y="{h * .40:.1f}" width="{b * .90:.1f}" height="{h * .07:.1f}"
  fill="{streifen}"/>
<rect x="{b * .16:.1f}" y="{h * .52:.1f}" width="{b * .68:.1f}" height="{h * .26:.1f}"
  rx="{h * .03:.1f}" fill="#17171a"/>
<circle cx="{b * .30:.1f}" cy="{h * .65:.1f}" r="{rw:.1f}" fill="{etikett}"
  stroke="{rand}" stroke-width="{max(1, b * .005):.1f}"/>
<circle cx="{b * .70:.1f}" cy="{h * .65:.1f}" r="{rw:.1f}" fill="{etikett}"
  stroke="{rand}" stroke-width="{max(1, b * .005):.1f}"/>
<circle cx="{b * .30:.1f}" cy="{h * .65:.1f}" r="{rw * .42:.1f}" fill="#17171a"/>
<circle cx="{b * .70:.1f}" cy="{h * .65:.1f}" r="{rw * .42:.1f}" fill="#17171a"/>
{''.join(f'<circle cx="{b * x:.1f}" cy="{h * .87:.1f}" r="{b * .017:.1f}" fill="{rand}"/>'
         for x in (.20, .35, .50, .65, .80))}</svg>'''


def welle(w, h, color, aktiv, frac, n=48, seed=5, rund=None):
    """Wellenform als Spulleiste: was gespielt ist, steht kräftig, der Rest blass."""
    rund = h * .5 if rund is None else rund
    stk = []
    for i in range(n):
        v = (math.sin(i * .7 + seed) * .5 + .5) * (.30 + .70 * abs(math.sin(i * .31 + seed * 1.7)))
        bh = max(h * .10, v * h)
        x = i * (w / n)
        bw = (w / n) * .46
        stk.append(f'<rect x="{x:.1f}" y="{(h - bh) / 2:.1f}" width="{bw:.1f}" '
                   f'height="{bh:.1f}" rx="{min(rund, bw / 2):.1f}" '
                   f'fill="{aktiv if i / n <= frac else color}"/>')
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">{"".join(stk)}</svg>'


def schreibe(nr, name, art, css, body):
    """Ein Blatt ablegen — Name und Maße nach dem Schema des Pakets."""
    w, h = TEL if art == 'iphone' else PC
    ziel = (pathlib.Path(__file__).resolve().parents[1] / 'html'
            / f'foto{nr}_{name}_{art}.html')
    ziel.write_text(doc(w, h, css, body), encoding='utf-8')
    return ziel
