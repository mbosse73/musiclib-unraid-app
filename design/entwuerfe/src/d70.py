# -*- coding: utf-8 -*-
"""70 Dezibel — zwei Zeigerfenster, und eines davon lügt nicht.

Vorlage ist der Eversolo T10: eine schwarze Front, in der zwei **hellblau
hinterleuchtete VU-Fenster** sitzen, jedes mit einer Skala aus dicken
schwarzen Segmenten, die am rechten Ende in Orange übergehen. Links und
rechts davon liegen Berührungszeichen ohne Rahmen.

Der Entwurf nimmt die Doppelung — und dreht sie um:

- **Links steht der Pegel, rechts die Position.** Ein zweites Pegelinstrument
  wäre die zweite Hälfte derselben Auskunft; ein Instrument für den Stand im
  Album ist eine andere. Beide sehen gleich aus, weil sie gleich abgelesen
  werden, und sie stehen nebeneinander, weil man beides zugleich wissen will.
- **Das Orange am Skalenende bedeutet in beiden dasselbe: es wird knapp.**
  Links Übersteuerung, rechts die letzten Minuten des Albums. Eine Farbe,
  eine Bedeutung — das ist die Bedingung dafür, dass die Doppelung nicht
  verwirrt.
- **Der Rest der Front ist unbeschriftet.** Die Zeichen links und rechts
  liegen frei auf dem Schwarz, ohne Rahmen und ohne Wort, wie in der Vorlage.

Gespult wird auf dem rechten Instrument: man zieht den Zeiger. Das ist die
einzige Stelle, an der ein Zeiger auch Eingabe ist, und sie ist es, weil dort
die Position steht.

Abgegrenzt: 13 Nussbaum hat auch Zeiger, aber beide zeigen Pegel und keiner
ist anfassbar. Hier ist einer die Spulfläche.
"""
import math

from werkzeug import (A, biblio, laut, lupe, nexti, pausei, prev, schreibe,
                      MONO, SANS)

SCHWARZ = '#0B0C0D'
FELD = '#8ED8F0'
FELD2 = '#6FC5E4'
TINTE = '#12181C'
ORANGE = '#F08A3C'
WEISS = '#EDEFF0'
MATT = 'rgba(237,239,240,.58)'
STUMM = 'rgba(237,239,240,.30)'


def _css(g):
    return f'''
.stage{{background:
    repeating-linear-gradient(90deg,rgba(255,255,255,.016) 0 1px,rgba(0,0,0,.05) 1px 3px),
    linear-gradient(180deg,#141618 0%,{SCHWARZ} 50%,#08090A 100%);
  font-family:{SANS};color:{WEISS};-webkit-font-smoothing:antialiased}}
.kap{{letter-spacing:.26em;text-transform:uppercase;color:{STUMM};font-weight:500}}

/* ── Das Fenster: hellblaues Blatt in einer schwarzen Fassung ── */
.werk{{position:relative;border-radius:{4 * g:.0f}px;overflow:hidden;
  background:radial-gradient(130% 150% at 50% 130%,{FELD} 0%,{FELD2} 100%);
  box-shadow:inset 0 0 0 {2 * g:.0f}px #05070A,
    inset 0 {5 * g:.0f}px {14 * g:.0f}px rgba(10,40,60,.30),
    0 {8 * g:.0f}px {22 * g:.0f}px rgba(0,0,0,.6)}}
.wlab{{position:absolute;left:0;right:0;text-align:center;font-family:{MONO};
  letter-spacing:.20em;text-transform:uppercase;color:rgba(18,24,28,.52)}}
.wname{{position:absolute;left:0;right:0;text-align:center;font-family:{MONO};
  letter-spacing:.26em;text-transform:uppercase;color:rgba(18,24,28,.78);font-weight:700}}
/* Berührungszeichen: kein Rahmen, keine Fläche — nur das Zeichen. */
.zeichen{{display:flex;align-items:center;justify-content:center;color:{MATT}}}
.zeit{{font-family:{MONO};color:{STUMM};font-variant-numeric:tabular-nums}}
.titel{{font-weight:300;letter-spacing:-.02em;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis}}
'''


def _werk(g, b, h, frac, lab, name, orange_ab=.78):
    """Skala aus dicken Segmenten, Zeiger, zwei Beschriftungen.

    `orange_ab` ist der Anteil, ab dem die Segmente orange werden — links
    Übersteuerung, rechts die letzten Minuten."""
    cx, cy, r = b / 2, h * 1.06, h * .74
    a0, a1 = math.radians(206), math.radians(334)
    seg = []
    n = 22
    for i in range(n):
        aa = a0 + (a1 - a0) * (i + .5) / n
        farbe = ORANGE if i / n >= orange_ab else TINTE
        x1, y1 = cx + math.cos(aa) * r * .93, cy + math.sin(aa) * r * .93
        seg.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" '
                   f'x2="{cx + math.cos(aa) * r * 1.0:.1f}" '
                   f'y2="{cy + math.sin(aa) * r * 1.0:.1f}" stroke="{farbe}" '
                   f'stroke-width="{b * .026:.1f}" stroke-linecap="round"/>')
    zahlen = []
    for wert, p in (('-20', .02), ('-10', .26), ('-5', .44), ('-3', .56),
                    ('0', .80), ('+3', .94)):
        aa = a0 + (a1 - a0) * p
        zahlen.append(f'<text x="{cx + math.cos(aa) * r * .78:.1f}" '
                      f'y="{cy + math.sin(aa) * r * .78:.1f}" text-anchor="middle" '
                      f'font-family={MONO!r} font-size="{b * .052:.0f}" '
                      f'fill="rgba(18,24,28,.72)">{wert}</text>')
    az = a0 + (a1 - a0) * frac
    return f'''<div class="werk" style="width:{b}px;height:{h}px">
  <svg viewBox="0 0 {b} {h}" width="{b}" height="{h}">
    {''.join(seg)}{''.join(zahlen)}
    <line x1="{cx}" y1="{cy}" x2="{cx + math.cos(az) * r * 1.15:.1f}"
      y2="{cy + math.sin(az) * r * 1.15:.1f}" stroke="{TINTE}"
      stroke-width="{b * .008:.1f}"/>
  </svg>
  <span class="wlab" style="top:{h * .13:.0f}px;font-size:{b * .044:.0f}px">{lab}</span>
  <span class="wname" style="top:{h * .70:.0f}px;font-size:{b * .062:.0f}px">{name}</span>
</div>'''


def _zeichen(g, links=True, gross=False):
    d = int((30 if gross else 22) * g)
    z = ([prev(d, MATT), pausei(int(d * 1.15), WEISS), nexti(d, MATT)] if links
         else [lupe(d, MATT, 2.2), biblio(d, MATT), laut(d, MATT)])
    return (f'<div style="display:flex;flex-direction:column;align-items:center;'
            f'gap:{int((44 if gross else 34) * g)}px">'
            + ''.join(f'<span class="zeichen">{x}</span>' for x in z) + '</div>')


def _kopf(g, px=18):
    return f'''<div style="display:flex;align-items:baseline;justify-content:space-between">
  <span class="kap" style="font-size:{px}px">Musiklib · Streaming Transport</span>
  <span class="kap" style="font-size:{px}px">{A['sammlung']} Alben</span>
</div>'''


def _schrift(g, px):
    return f'''<div style="text-align:center">
  <div class="titel" style="font-size:{px * g:.0f}px">{A['titel']}</div>
  <div style="color:{MATT};font-weight:300;margin-top:{int(9 * g)}px;
    font-size:{25 * g:.0f}px">{A['interpret']} · {A['album']}</div>
</div>'''


def rechner():
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:52px 70px 60px">
  {_kopf(g)}
  <div style="display:flex;align-items:center;justify-content:center;gap:60px">
    {_zeichen(g, True)}
    {_werk(g, 420, 250, .58, 'Volume Unit Meter', 'Pegel')}
    {_werk(g, 420, 250, A['frac'], 'Position im Album', 'Stand')}
    {_zeichen(g, False)}
  </div>
  <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:40px">
    <span class="zeit" style="font-size:21px">{A['pos']}</span>
    {_schrift(g, 46)}
    <span class="zeit" style="font-size:21px">{A['rest']}</span>
  </div>
</div>'''
    return _css(g), body


def telefon():
    """Hochkant stehen die Fenster übereinander — nebeneinander wäre jedes
    380 px breit, und dann ist die Skala nicht mehr abzulesen."""
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:100px 56px 110px">
  {_kopf(g, 19)}
  <div style="display:flex;flex-direction:column;gap:40px">
    {_werk(g, 968, 380, .58, 'Volume Unit Meter', 'Pegel')}
    {_werk(g, 968, 380, A['frac'], 'Position im Album', 'Stand')}
  </div>
  {_schrift(g, 52)}
  <div style="display:flex;align-items:center;justify-content:space-between">
    <span class="zeit" style="font-size:23px">{A['pos']}</span>
    <div style="display:flex;align-items:center;gap:{int(52 * g)}px">
      {prev(int(34 * g), MATT)}{pausei(int(44 * g), WEISS)}{nexti(int(34 * g), MATT)}
      {lupe(int(30 * g), MATT, 2.2)}{biblio(int(30 * g), MATT)}</div>
    <span class="zeit" style="font-size:23px">{A['rest']}</span>
  </div>
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('70', 'Dezibel', art, css, body)
