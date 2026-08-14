# -*- coding: utf-8 -*-
"""42 Druckgrafik — nach dem Kunstdruck von MINIM (23.34.53).

Die Vorlage ist ein gedrucktes Blatt: cremefarbenes Papier, darauf ein
Plattenspieler von oben in nur drei Farben — Blau, Ziegelrot, Papierweiss —,
die Rillen als feine helle Striche, der Tonarm als Winkel. Unten links ein
Schieber, unten rechts zwei Drehknöpfe. Übertragen: der Schieber ist die
Lautstärke, der Tonarm zeigt die Spielposition, die Knöpfe sind Vor und Zurück.
"""
import math

from werkzeug import A, biblio, schreibe, SANS, MONO

PAPIER = '#efe8da'
BLAU = '#5b83a8'
ZIEGEL = '#d4653c'
TINTE = '#3a3630'
STUMM = '#8b857a'


def _css(g):
    return f'''
.stage{{background:{PAPIER};font-family:{SANS};color:{TINTE}}}
.korn{{position:absolute;inset:0;pointer-events:none;opacity:.45;
  background:
    repeating-linear-gradient(0deg, rgba(0,0,0,.028) 0 1px, transparent 1px 3px),
    repeating-linear-gradient(90deg, rgba(0,0,0,.022) 0 1px, transparent 1px 4px)}}

/* Bibliothek: die Marke oben links ist der Zugang, wie die Signatur des Drucks */
.marke{{display:flex;align-items:center}}
.markentext{{text-transform:uppercase;letter-spacing:{4 * g:.1f}px;line-height:1.35}}
.markentext b{{display:block;font-weight:700;letter-spacing:{5 * g:.1f}px}}
.markentext span{{display:block;color:{STUMM};font-size:.68em}}

.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{STUMM};
  font-variant-numeric:tabular-nums}}
.spur{{position:relative;height:{3 * g:.0f}px;background:rgba(58,54,48,.20)}}
.spur i{{position:absolute;left:0;top:0;bottom:0;background:{ZIEGEL}}}

/* Schieber und Knöpfe sind gedruckt, nicht plastisch: flache Flächen, harte Kanten */
.schieber{{position:relative;background:{BLAU};border-radius:{4 * g:.0f}px}}
.schieber .schlitz{{position:absolute;left:50%;transform:translateX(-50%);
  background:#7b3524;border-radius:2px}}
.schieber .griff{{position:absolute;left:50%;transform:translate(-50%,-50%);
  background:{ZIEGEL};border-radius:{3 * g:.0f}px;box-shadow:0 0 0 {3 * g:.0f}px {PAPIER}}}
.knopf{{position:relative;border-radius:50%;display:flex;align-items:center;
  justify-content:center}}
.knopf i{{position:absolute;background:#7b3524;border-radius:2px;transform-origin:center}}
'''


def _teller(g, size):
    """Plattenspieler von oben: blaue Scheibe mit Rillenstrichen, roter Spiegel, Tonarm."""
    r = size / 2
    rillen = ''.join(
        f'<circle cx="{r}" cy="{r}" r="{r * .34 + i * (r * .62 / 34):.1f}" fill="none" '
        f'stroke="#e9eef3" stroke-width="{1.1 if i % 4 else 1.8}" '
        f'opacity="{.30 if i % 4 else .55}"/>' for i in range(34))
    # Tonarm: Winkel von der Achse oben rechts zur Nadel auf der Platte
    ax, ay = r * 1.52, r * .30
    wink = math.radians(150 + A['frac'] * 40)
    nx, ny = r + math.cos(wink) * r * .62, r + math.sin(wink) * r * .62
    kx, ky = ax, ay + r * .70
    return f'''<svg viewBox="0 0 {size * 1.22:.0f} {size * 1.12:.0f}"
  width="{size * 1.22:.0f}" height="{size * 1.12:.0f}">
<ellipse cx="{r + size * .022:.0f}" cy="{r + size * .030:.0f}" rx="{r}" ry="{r}"
  fill="{ZIEGEL}" opacity=".55"/>
<circle cx="{r}" cy="{r}" r="{r}" fill="{BLAU}"/>
{rillen}
<circle cx="{r}" cy="{r}" r="{r * .30:.1f}" fill="{ZIEGEL}"/>
<circle cx="{r}" cy="{r}" r="{r * .028:.1f}" fill="{PAPIER}"/>
<circle cx="{ax:.1f}" cy="{ay:.1f}" r="{r * .17:.1f}" fill="{ZIEGEL}"/>
<circle cx="{ax:.1f}" cy="{ay:.1f}" r="{r * .085:.1f}" fill="#3b3129"/>
<circle cx="{ax * .97:.1f}" cy="{ay * .60:.1f}" r="{r * .055:.1f}" fill="#3b3129"/>
<path d="M{ax:.1f} {ay:.1f} L{kx:.1f} {ky:.1f} L{nx:.1f} {ny:.1f}"
  fill="none" stroke="{PAPIER}" stroke-width="{max(3, size * .016):.1f}"
  stroke-linejoin="round" stroke-linecap="round"/>
<rect x="{nx - size * .045:.1f}" y="{ny - size * .012:.1f}" width="{size * .085:.1f}"
  height="{size * .062:.1f}" rx="{size * .008:.1f}" fill="{ZIEGEL}"
  transform="rotate(-26 {nx:.1f} {ny:.1f})"/>
<circle cx="{nx - size * .018:.1f}" cy="{ny + size * .016:.1f}" r="{size * .009:.1f}" fill="{PAPIER}"/>
<circle cx="{nx + size * .006:.1f}" cy="{ny + size * .014:.1f}" r="{size * .009:.1f}" fill="{PAPIER}"/>
</svg>'''


def _schieber(g, breite, hoehe):
    return (f'<div class="schieber" style="width:{breite}px;height:{hoehe}px">'
            f'<div class="schlitz" style="top:{int(hoehe * .07)}px;width:{int(breite * .16)}px;'
            f'height:{int(hoehe * .86)}px"></div>'
            f'<div class="griff" style="top:{int(hoehe * .30)}px;width:{int(breite * .52)}px;'
            f'height:{int(breite * .38)}px"></div></div>')


def _knopf(g, size, winkel, farbe):
    return (f'<div class="knopf" style="width:{size}px;height:{size}px;background:{farbe}">'
            f'<i style="width:{int(size * .40)}px;height:{max(2, int(size * .085))}px;'
            f'transform:rotate({winkel}deg) translateX({int(size * .16)}px)"></i></div>')


def _marke(g, schrift):
    return (f'<div class="marke" style="gap:{int(14 * g)}px">'
            f'{biblio(int(schrift * 2.1), ZIEGEL)}'
            f'<span class="markentext" style="font-size:{schrift}px">'
            f'<b>Musiklib</b><span>Sammlung · {A["sammlung"]} Alben</span></span></div>')


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div class="korn"></div>
<div style="position:absolute;inset:0;padding:120px 80px 96px;display:flex;flex-direction:column">
  {_marke(g, 26)}

  <div style="display:flex;justify-content:center;margin-top:48px">{_teller(g, 740)}</div>

  <div style="font-size:56px;font-weight:700;margin-top:64px;letter-spacing:-.02em">
    {A['titel']}</div>
  <div style="font-size:30px;color:{STUMM};margin-top:12px">
    {A['interpret']} · {A['album']} · {A['jahr']}</div>

  <div class="spur" style="margin-top:38px"><i style="width:{A['frac'] * 100:.0f}%"></i></div>
  <div class="zeiten" style="font-size:25px;margin-top:16px">
    <span>{A['pos']}</span><span>{A['dauer']}</span></div>

  <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-top:auto">
    {_schieber(g, 92, 300)}
    <div style="display:flex;align-items:flex-end;gap:44px">
      {_knopf(g, 96, 200, ZIEGEL)}
      {_knopf(g, 126, -20, BLAU)}
    </div>
  </div>
</div>'''
    return css, body


def rechner():
    g = .72
    css = _css(g)
    body = f'''<div class="korn"></div>
<div style="position:absolute;inset:0;padding:60px 80px;display:flex;gap:70px;align-items:center">
  <div style="flex-shrink:0">{_teller(g, 640)}</div>

  <div style="flex:1;min-width:0;display:flex;flex-direction:column;
    align-self:stretch;padding:12px 0">
    {_marke(g, 19)}
    <div style="margin-top:auto">
      <div style="font-size:60px;font-weight:700;letter-spacing:-.02em">{A['titel']}</div>
      <div style="font-size:24px;color:{STUMM};margin-top:10px">
        {A['interpret']} · {A['album']} · {A['jahr']}</div>
      <div class="spur" style="margin-top:30px"><i style="width:{A['frac'] * 100:.0f}%"></i></div>
      <div class="zeiten" style="font-size:19px;margin-top:14px">
        <span>{A['pos']}</span><span>{A['dauer']}</span></div>
    </div>
    <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-top:auto">
      {_schieber(g, 66, 200)}
      <div style="display:flex;align-items:flex-end;gap:32px">
        {_knopf(g, 68, 200, ZIEGEL)}
        {_knopf(g, 90, -20, BLAU)}
      </div>
    </div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('42', 'Druckgrafik', art, css, body)
