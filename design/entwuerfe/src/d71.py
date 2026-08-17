# -*- coding: utf-8 -*-
"""71 Silberkasten — eine Platte, ein Knopf, mehr gibt es nicht.

Vorlage ist eine Eversolo-Front: eine schwarze, senkrecht gebürstete Fläche,
in die **eine einzige silberne Platte** eingelassen ist. Darin zwei Zeiger
mit feinen Strichen und der Firmenschriftzug. Unter der Platte, weit ab,
**ein runder Knopf** mit einem Ein-Zeichen — und sonst ist die Fläche leer.

Der Entwurf nimmt die Kargheit als Regel:

- **Alles, was das Gerät sagt, steht auf der einen Platte.** Titel,
  Interpret, Stand, Restzeit, Warteschlange — nichts davon liegt daneben. Was
  nicht auf die Platte passt, gibt es nicht.
- **Es gibt genau einen Knopf**, und er ist ein Umschalter: drücken spielt,
  drücken hält an. Alles andere passiert auf der Platte selbst — dort wird
  gespult, dort wird der nächste Titel angetippt.
- **Die Platte ist warm, die Fläche ist kalt.** Silber mit einem Stich ins
  Champagner in schwarzem, senkrecht gebürstetem Blech: der Kontrast trägt
  den ganzen Entwurf, es gibt keine dritte Farbe. Rot steht nur am
  Skalenende, wie in der Vorlage.

Das ist ein Verwandter von 18 Album des Tages: dort ein Knopf und keine Wahl,
hier ein Knopf und die ganze Auskunft auf einer Fläche. Der Unterschied ist,
dass hier eine Warteschlange sichtbar bleibt.

Abgegrenzt: 70 Dezibel kommt aus demselben Haus und hat auch Zeiger, aber
dort sind es zwei getrennte Fenster in einer sonst beschrifteten Front. Hier
ist die Platte das ganze Gerät.
"""
import math

from werkzeug import (A, biblio, laut, lupe, nexti, pausei, prev, schreibe,
                      MONO, SANS)

BLECH = '#0D0E0F'
PLATTE = '#DCD8CC'
PLATTE2 = '#B6B2A5'
TINTE = '#26241E'
MATT = 'rgba(38,36,30,.62)'
STUMM = 'rgba(38,36,30,.40)'
ROT = '#C0392B'
HELL = 'rgba(240,240,238,.72)'
DUNKELSTUMM = 'rgba(240,240,238,.30)'

TITEL = [('So What', 9.4), ('Freddie Freeloader', 9.8), ('Blue in Green', 5.6),
         ('All Blues', 11.6), ('Flamenco Sketches', 9.5)]
LAEUFT = 2


def _css(g):
    return f'''
.stage{{background:
    repeating-linear-gradient(0deg,rgba(255,255,255,.020) 0 1px,rgba(0,0,0,.06) 1px 4px),
    linear-gradient(180deg,#151617 0%,{BLECH} 46%,#08090A 100%);
  font-family:{SANS};color:{HELL};-webkit-font-smoothing:antialiased}}
.kap{{letter-spacing:.28em;text-transform:uppercase;color:{DUNKELSTUMM};font-weight:500}}

/* ── Die Platte: gebürstetes Champagnersilber, gewölbt, mit weicher Kante ── */
.platte{{position:relative;border-radius:{10 * g:.0f}px;overflow:hidden;color:{TINTE};
  background:
    repeating-linear-gradient(90deg,rgba(255,255,255,.20) 0 1px,rgba(0,0,0,.045) 1px 3px),
    linear-gradient(180deg,#F1EDE1 0%,{PLATTE} 40%,{PLATTE2} 100%);
  box-shadow:inset 0 {2 * g:.0f}px 0 rgba(255,255,255,.9),
    inset 0 -{2 * g:.0f}px 0 rgba(0,0,0,.28),
    0 0 0 {2 * g:.0f}px #3A3B3C,0 {14 * g:.0f}px {34 * g:.0f}px rgba(0,0,0,.7)}}
.plab{{font-family:{MONO};letter-spacing:.24em;text-transform:uppercase;color:{STUMM}}}
.ptitel{{font-weight:400;letter-spacing:-.01em;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis}}
.pzeit{{font-family:{MONO};color:{MATT};font-variant-numeric:tabular-nums}}

/* Die Warteschlange auf der Platte: Striche, einer davon voll. */
.qz{{display:flex;align-items:flex-end;gap:{int(4 * g)}px}}
.qz i{{display:block;border-radius:1px;background:rgba(38,36,30,.26)}}
.qz i.vor{{background:rgba(38,36,30,.52)}}
.qz i.jetzt{{background:{TINTE}}}

/* ── Der eine Knopf: ein Ring, sonst nichts. ── */
.knopf{{position:relative;border-radius:50%;display:flex;align-items:center;
  justify-content:center;background:transparent;
  box-shadow:inset 0 0 0 {2 * g:.0f}px rgba(240,240,238,.72),
    0 0 {26 * g:.0f}px rgba(240,240,238,.10)}}
.klab{{font-family:{MONO};letter-spacing:.26em;text-transform:uppercase;
  color:{DUNKELSTUMM};text-align:center}}
'''


def _zeiger(g, b, h, frac, lab, rot_ab=.86):
    cx, cy, r = b / 2, h * 1.10, h * .80
    a0, a1 = math.radians(214), math.radians(326)
    st = []
    n = 26
    for i in range(n + 1):
        aa = a0 + (a1 - a0) * i / n
        gross = i % 5 == 0
        farbe = ROT if i / n >= rot_ab else TINTE
        r1 = r * (.80 if gross else .86)
        st.append(f'<line x1="{cx + math.cos(aa) * r1:.1f}" y1="{cy + math.sin(aa) * r1:.1f}" '
                  f'x2="{cx + math.cos(aa) * r * .96:.1f}" '
                  f'y2="{cy + math.sin(aa) * r * .96:.1f}" stroke="{farbe}" '
                  f'stroke-width="{(1.9 if gross else 1.0) * g:.1f}" '
                  f'opacity="{.9 if gross else .55}"/>')
    az = a0 + (a1 - a0) * frac
    return f'''<div style="position:relative;width:{b}px;height:{h}px">
  <svg viewBox="0 0 {b} {h}" width="{b}" height="{h}">
    {''.join(st)}
    <line x1="{cx}" y1="{cy}" x2="{cx + math.cos(az) * r * 1.02:.1f}"
      y2="{cy + math.sin(az) * r * 1.02:.1f}" stroke="{TINTE}" stroke-width="{1.5 * g:.1f}"/>
  </svg>
  <span class="plab" style="position:absolute;left:0;right:0;bottom:0;text-align:center;
    font-size:{b * .072:.0f}px">{lab}</span>
</div>'''


def _queue(g, hoehe):
    ges = sum(d for _, d in TITEL)
    s = []
    for i, (_, d) in enumerate(TITEL):
        k = 'jetzt' if i == LAEUFT else ('vor' if i < LAEUFT else '')
        s.append(f'<i class="{k}" style="width:{d / ges * 100:.1f}%;'
                 f'height:{hoehe * (1 if i == LAEUFT else .55):.0f}px"></i>')
    return f'<div class="qz" style="width:100%">{"".join(s)}</div>'


def _platte(g, b, h):
    return f'''<div class="platte" style="width:{b}px;height:{h}px;
  padding:{int(30 * g)}px {int(40 * g)}px;display:flex;flex-direction:column;
  justify-content:space-between">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:{int(30 * g)}px">
    <div style="min-width:0">
      <div class="plab" style="font-size:{h * .042:.0f}px">Es läuft</div>
      <div class="ptitel" style="font-size:{h * .115:.0f}px;margin-top:{int(8 * g)}px">
        {A['titel']}</div>
      <div class="pzeit" style="font-size:{h * .055:.0f}px;margin-top:{int(6 * g)}px">
        {A['interpret']} · {A['album']}</div>
    </div>
    {_zeiger(g, int(b * .26), int(h * .40), A['frac'], 'Stand')}
  </div>
  <div>
    {_queue(g, int(h * .10))}
    <div style="display:flex;align-items:baseline;justify-content:space-between;
      margin-top:{int(10 * g)}px">
      <span class="pzeit" style="font-size:{h * .050:.0f}px">{A['pos']}</span>
      <span class="plab" style="font-size:{h * .040:.0f}px">
        Titel {LAEUFT + 1} von {len(TITEL)} · Sammlung {A['sammlung']}</span>
      <span class="pzeit" style="font-size:{h * .050:.0f}px">{A['rest']}</span>
    </div>
  </div>
</div>'''


def rechner():
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:96px;padding:60px">
  <div style="position:absolute;top:52px;left:0;right:0;display:flex;
    justify-content:space-between;padding:0 74px">
    <span class="kap" style="font-size:17px">Musiklib</span>
    <span class="kap" style="font-size:17px">Silberkasten</span>
  </div>
  {_platte(g, 1180, 300)}
  <div style="display:flex;flex-direction:column;align-items:center;gap:20px">
    <span class="knopf" style="width:96px;height:96px">{pausei(30, HELL)}</span>
    <span class="klab" style="font-size:15px">Spielen · Anhalten</span>
  </div>
</div>'''
    return _css(g), body


def telefon():
    """Hochkant wird die Platte hoch statt breit, und der Knopf rutscht dorthin,
    wo der Daumen ohnehin liegt. Auf der Platte wandern Zeiger und Schrift
    untereinander — nebeneinander bliebe für den Titel nichts."""
    g = 1.0
    b, h = 968, 640
    platte = f'''<div class="platte" style="width:{b}px;height:{h}px;
  padding:{int(46 * g)}px {int(52 * g)}px;display:flex;flex-direction:column;
  justify-content:space-between">
  <div>
    <div class="plab" style="font-size:{22:.0f}px">Es läuft</div>
    <div class="ptitel" style="font-size:{56:.0f}px;margin-top:{14:.0f}px">{A['titel']}</div>
    <div class="pzeit" style="font-size:{26:.0f}px;margin-top:{10:.0f}px">
      {A['interpret']} · {A['album']}</div>
  </div>
  <div style="display:flex;justify-content:center">
    {_zeiger(g, 420, 210, A['frac'], 'Stand')}</div>
  <div>
    {_queue(g, 34)}
    <div style="display:flex;align-items:baseline;justify-content:space-between;
      margin-top:{14:.0f}px">
      <span class="pzeit" style="font-size:{24:.0f}px">{A['pos']}</span>
      <span class="plab" style="font-size:{18:.0f}px">
        Titel {LAEUFT + 1} von {len(TITEL)}</span>
      <span class="pzeit" style="font-size:{24:.0f}px">{A['rest']}</span>
    </div>
  </div>
</div>'''
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:space-between;padding:106px 56px 130px">
  <div style="width:100%;display:flex;justify-content:space-between">
    <span class="kap" style="font-size:19px">Musiklib</span>
    <span class="kap" style="font-size:19px">Silberkasten</span>
  </div>
  {platte}
  <div style="display:flex;flex-direction:column;align-items:center;gap:24px">
    <span class="knopf" style="width:180px;height:180px">{pausei(56, HELL)}</span>
    <span class="klab" style="font-size:18px">Spielen · Anhalten</span>
  </div>
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('71', 'Silberkasten', art, css, body)
