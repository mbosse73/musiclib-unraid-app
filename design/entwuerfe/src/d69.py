# -*- coding: utf-8 -*-
"""69 Halbmond — zwei Knöpfe, ein Schlitz, sonst schwarze Fläche.

Vorlage ist eine AVM-Front: gebürstetes Schwarz, in der Mitte ein
**briefkastenschmales Display** mit Titel, Interpret und einem Fortschritts-
strich, links und rechts je ein grosser verchromter Knopf, dessen Kappe halb
poliert und halb schwarz ist — der **Halbmond**. Darunter fünf winzige
Tasten, kaum grösser als ein Punkt.

Der Entwurf hält sich an das, was daran ungewöhnlich ist:

- **Die Anzeige ist absichtlich klein.** Sie steht in einem Schlitz von der
  Höhe dreier Zeilen, mitten in einer grossen leeren Fläche. Das ist keine
  Sparsamkeit, sondern eine Haltung: ein Verstärker zeigt an, was gerade
  läuft, und nicht, was es sonst noch gibt. Wer die Sammlung will, drückt.
- **Der Halbmond ist die Stellungsanzeige.** Die Kappe ist halb hell, halb
  dunkel; wie weit sie gedreht ist, sieht man an der Kante zwischen beiden —
  ohne Strich, ohne Skala. Links steht die Quelle, rechts die Lautstärke.
- **Die fünf Punkte darunter sind die ganze übrige Bedienung.** Sie tragen
  keine Beschriftung; über ihnen steht im Schlitz, was sie gerade tun.

Gespult wird auf dem Fortschrittsstrich im Schlitz — er ist nur wenige Pixel
hoch, aber er ist die einzige Stelle, an der eine Position steht.

Abgegrenzt: 74 Klimaxfront ist auch schwarzes Glas mit weisser Schrift, aber
dort füllt die Anzeige die Fläche. Hier ist die Fläche leer, und genau das
ist der Entwurf.
"""
import math

from werkzeug import (A, biblio, laut, lupe, nexti, pausei, prev, schreibe,
                      MONO, SANS)

BLECH = '#131415'
WEISS = '#F2F3F4'
MATT = 'rgba(242,243,244,.62)'
STUMM = 'rgba(242,243,244,.30)'
SCHLITZ = '#08090A'


def _css(g):
    return f'''
.stage{{background:
    repeating-linear-gradient(90deg,rgba(255,255,255,.020) 0 1px,rgba(0,0,0,.05) 1px 3px),
    radial-gradient(140% 120% at 50% 40%,#1E2021 0%,{BLECH} 58%,#0A0B0C 100%);
  font-family:{SANS};color:{WEISS};-webkit-font-smoothing:antialiased}}
.kap{{letter-spacing:.26em;text-transform:uppercase;color:{STUMM};font-weight:500}}

/* ── Der Halbmond ───────────────────────────────────────────────────────
   Ein Chromring, darin eine Kappe, die zur Hälfte poliert und zur Hälfte
   schwarz ist. Die Kante zwischen beiden Hälften ist die Stellung — deshalb
   ist sie gerade und nicht gezackt. */
.mond{{position:relative;border-radius:50%;
  background:conic-gradient(from 90deg,#E9EAEC 0deg 180deg,#111213 180deg 360deg);
  box-shadow:0 0 0 {5 * g:.0f}px #C6C8CB,0 0 0 {7 * g:.0f}px #4A4C4F,
    0 {10 * g:.0f}px {26 * g:.0f}px rgba(0,0,0,.6),
    inset 0 {4 * g:.0f}px {12 * g:.0f}px rgba(255,255,255,.28)}}
.mond::after{{content:'';position:absolute;inset:0;border-radius:50%;
  background:linear-gradient(160deg,rgba(255,255,255,.32) 0%,rgba(255,255,255,0) 46%)}}
.mlab{{font-family:{MONO};letter-spacing:.22em;text-transform:uppercase;color:{STUMM};
  text-align:center}}

/* ── Der Schlitz: schmales Display, in das Blech eingelassen ── */
.schlitz{{position:relative;background:{SCHLITZ};border-radius:{2 * g:.0f}px;overflow:hidden;
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.9),inset 0 {4 * g:.0f}px {14 * g:.0f}px rgba(0,0,0,.9),
    0 1px 0 rgba(255,255,255,.09)}}
.stitel{{font-weight:500;letter-spacing:-.01em;text-align:center;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}}
.sunter{{color:{MATT};text-align:center;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis}}
.szeit{{font-family:{MONO};color:{MATT};font-variant-numeric:tabular-nums}}
.sbahn{{position:relative;background:rgba(242,243,244,.16);border-radius:1px;overflow:hidden}}
.sbahn i{{position:absolute;left:0;top:0;bottom:0;background:{WEISS}}}

/* ── Die fünf Punkte ── kleiner geht es nicht, und das ist die Aussage. ── */
.punkt{{border-radius:50%;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(circle at 36% 30%,#C9CBCE,#6E7175 70%,#3A3C3F);
  box-shadow:0 1px 3px rgba(0,0,0,.7),inset 0 1px 0 rgba(255,255,255,.4)}}
.marke{{position:absolute;left:50%;transform:translateX(-50%);font-family:{MONO};
  letter-spacing:.3em;text-transform:uppercase;color:{STUMM}}}
'''


def _schlitz(g, b, h):
    return f'''<div class="schlitz" style="width:{b}px;height:{h}px;padding:{int(14 * g)}px
  {int(26 * g)}px;display:flex;flex-direction:column;justify-content:center;
  gap:{int(6 * g)}px">
  <div class="stitel" style="font-size:{h * .30:.0f}px">{A['titel']}</div>
  <div class="sunter" style="font-size:{h * .19:.0f}px">{A['interpret']}</div>
  <div style="display:flex;align-items:center;gap:{int(14 * g)}px;margin-top:{int(6 * g)}px">
    <span class="szeit" style="font-size:{h * .15:.0f}px">{A['pos']}</span>
    <span class="sbahn" style="flex:1;height:{max(2, int(h * .045))}px">
      <i style="width:{A['frac'] * 100:.0f}%"></i></span>
    <span class="szeit" style="font-size:{h * .15:.0f}px">{A['dauer']}</span>
  </div>
</div>'''


def _mond(g, d, lab):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;'
            f'gap:{int(20 * g)}px">'
            f'<span class="mlab" style="font-size:{15 * g:.0f}px">{lab}</span>'
            f'<span class="mond" style="width:{d * g:.0f}px;height:{d * g:.0f}px"></span>'
            f'</div>')


def _punkte(g, d=22):
    z = [prev(int(d * .5 * g), '#1A1C1E'), pausei(int(d * .55 * g), '#1A1C1E'),
         nexti(int(d * .5 * g), '#1A1C1E'), lupe(int(d * .45 * g), '#1A1C1E', 2.4),
         biblio(int(d * .45 * g), '#1A1C1E')]
    return (f'<div style="display:flex;align-items:center;gap:{int(d * 1.1 * g)}px">'
            + ''.join(f'<span class="punkt" style="width:{d * g:.0f}px;'
                      f'height:{d * g:.0f}px">{x}</span>' for x in z) + '</div>')


def rechner():
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:40px;padding:70px">
  <div style="position:absolute;top:56px;left:0;right:0;display:flex;
    justify-content:space-between;padding:0 78px">
    <span class="kap" style="font-size:17px">Musiklib</span>
    <span class="kap" style="font-size:17px">{A['sammlung']} Alben</span>
  </div>
  <div style="display:flex;align-items:center;gap:96px">
    {_mond(g, 210, 'Quelle')}
    <div style="display:flex;flex-direction:column;align-items:center;gap:30px">
      {_schlitz(g, 560, 150)}
      {_punkte(g, 24)}
    </div>
    {_mond(g, 210, 'Lautstärke')}
  </div>
  <span class="marke" style="bottom:70px;font-size:26px;font-weight:300">Halbmond</span>
</div>'''
    return _css(g), body


def telefon():
    """Hochkant stehen die Halbmonde nebeneinander unter dem Schlitz — auf
    einem Telefon sind zwei Knöpfe links und rechts vom Text nicht zu greifen,
    ohne die Anzeige zu verdecken."""
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:space-between;padding:110px 60px 120px">
  <div style="width:100%;display:flex;justify-content:space-between">
    <span class="kap" style="font-size:19px">Musiklib</span>
    <span class="kap" style="font-size:19px">{A['sammlung']} Alben</span>
  </div>
  <div style="display:flex;flex-direction:column;align-items:center;gap:70px;width:100%">
    {_schlitz(g, 940, 210)}
    {_punkte(g, 54)}
  </div>
  <div style="display:flex;align-items:center;gap:90px">
    {_mond(g, 300, 'Quelle')}
    {_mond(g, 300, 'Lautstärke')}
  </div>
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('69', 'Halbmond', art, css, body)
