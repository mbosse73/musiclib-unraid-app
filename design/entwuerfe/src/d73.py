# -*- coding: utf-8 -*-
"""73 Anschlag — der Spieler ist ein Plakat, und die Scheibe ist die Uhr.

Vorlage ist kein Gerät, sondern ein **Plakat**: cremefarbener Grund, eine
grosse orange Scheibe, oben rechts eine schwarze Schallplatte, links eine
riesige Schrift, unten ein kleiner, eng gesetzter Textblock und die
Zeichnung eines Plattenspielers.

Das ist der erste Entwurf im Register, der keine Maschine nachbaut, und die
Regeln kommen entsprechend aus der Typografie:

- **Der Albumtitel ist die Überschrift eines Plakats**, nicht eine Zeile in
  einem Feld: so gross, dass er die Fläche trägt, gebrochen wie ein Satz und
  nicht abgeschnitten wie ein Etikett.
- **Die orange Scheibe ist die Uhr.** Sie ist die stärkste Form im Bild,
  also bekommt sie die wichtigste Auskunft: der abgespielte Teil des Albums
  steht als dunklerer Sektor darin. Ein Plakat mit einem Fortschrittsbalken
  wäre ein Plakat mit einem Fremdkörper.
- **Die Titelliste ist der Fliesstext.** Klein, eng, zweispaltig, wie der
  Blocksatz unter der Überschrift — der laufende Titel ist der einzige, der
  fett steht. Man liest ihn, man tippt ihn nicht.
- **Drei Farben, keine vierte:** Creme, Schwarz, Orange. Auch die Bedienung
  hat keine eigene — sie ist schwarz auf Creme wie alles andere.

Gespult wird am Rand der Scheibe: der Sektor folgt dem Finger. Der Anfang
liegt oben, gedreht wird im Uhrzeigersinn — das ist die einzige Stelle, an
der das Plakat ein Gerät ist.

Abgegrenzt: 10 Weissraum ist auch ruhig und typografisch, aber dort ist die
Ruhe das Ziel. Hier ist es Lautstärke: eine Überschrift, die schreit, und
darunter ein Blocksatz, den man leise liest.
"""
import math

from werkzeug import (A, biblio, laut, lupe, nexti, pausei, prev, schreibe,
                      MONO, SANS, IMPACT)

CREME = '#EFE7D6'
CREME2 = '#E5DBC6'
SCHWARZ = '#141210'
ORANGE = '#E8613A'
ORANGE2 = '#C24A28'
MATT = 'rgba(20,18,16,.62)'
STUMM = 'rgba(20,18,16,.40)'

TITEL = [('01', 'So What', '9:22'), ('02', 'Freddie Freeloader', '9:46'),
         ('03', 'Blue in Green', '5:37'), ('04', 'All Blues', '11:33'),
         ('05', 'Flamenco Sketches', '9:26')]
LAEUFT = 2


def _css(g):
    return f'''
.stage{{background:linear-gradient(180deg,{CREME} 0%,{CREME2} 100%);
  font-family:{SANS};color:{SCHWARZ};-webkit-font-smoothing:antialiased}}
.kap{{letter-spacing:.26em;text-transform:uppercase;color:{STUMM};font-weight:600}}
/* Die Überschrift: so fett und so eng, wie es ohne eigene Schriftdatei geht. */
.schlag{{font-family:{IMPACT};font-weight:900;line-height:.86;letter-spacing:-.03em;
  text-transform:uppercase;text-wrap:balance}}
/* Der Blocksatz: die Titelliste als Fliesstext, zweispaltig. */
.satz{{column-gap:{28 * g:.0f}px;text-align:justify;hyphens:auto}}
.zeile{{display:flex;gap:{9 * g:.0f}px;break-inside:avoid;color:{MATT};
  border-bottom:1px solid rgba(20,18,16,.14);padding:{5 * g:.0f}px 0}}
.zeile .nr{{font-family:{MONO};color:{STUMM};flex:none}}
.zeile .na{{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.zeile .da{{font-family:{MONO};color:{STUMM};flex:none;font-variant-numeric:tabular-nums}}
.zeile.jetzt{{color:{SCHWARZ};font-weight:700;border-bottom-color:{SCHWARZ}}}
.zeile.jetzt .nr,.zeile.jetzt .da{{color:{ORANGE2}}}
.platte{{position:relative;border-radius:50%;background:
    repeating-radial-gradient(circle,#111 0 2px,#1D1B19 2px 4px),
    radial-gradient(circle at 34% 28%,#3A3734,#0B0A09 70%)}}
.platte::after{{content:'';position:absolute;inset:39%;border-radius:50%;background:{CREME};
  box-shadow:inset 0 0 0 1px rgba(20,18,16,.4)}}
.platte::before{{content:'';position:absolute;left:50%;top:50%;width:{4 * g:.0f}px;
  height:{4 * g:.0f}px;margin:-{2 * g:.0f}px 0 0 -{2 * g:.0f}px;border-radius:50%;
  background:{SCHWARZ};z-index:2}}
.taste{{display:flex;align-items:center;justify-content:center;color:{SCHWARZ}}}
.zeit{{font-family:{MONO};color:{MATT};font-variant-numeric:tabular-nums}}
'''


def _scheibe(g, d, frac):
    """Die orange Scheibe mit dem abgespielten Sektor. Anfang oben, im
    Uhrzeigersinn — der Rand ist zugleich die Spulfläche."""
    r = d / 2
    a = 2 * math.pi * frac
    x, y = r + math.sin(a) * r, r - math.cos(a) * r
    gross = 1 if frac > .5 else 0
    sektor = (f'<path d="M {r} {r} L {r} 0 A {r} {r} 0 {gross} 1 {x:.1f} {y:.1f} Z" '
              f'fill="{ORANGE2}" opacity=".55"/>') if frac > 0 else ''
    return (f'<svg viewBox="0 0 {d} {d}" width="{d}" height="{d}">'
            f'<circle cx="{r}" cy="{r}" r="{r}" fill="{ORANGE}"/>{sektor}'
            f'<line x1="{r}" y1="0" x2="{r}" y2="{r * .18:.0f}" stroke="{CREME}" '
            f'stroke-width="{3 * g:.1f}"/>'
            f'<line x1="{r}" y1="{r}" x2="{x:.1f}" y2="{y:.1f}" stroke="{SCHWARZ}" '
            f'stroke-width="{2.2 * g:.1f}"/></svg>')


def _liste(g, px):
    return ('<div class="satz" style="column-count:2;font-size:%dpx">' % px + ''.join(
        f'<div class="zeile{" jetzt" if i == LAEUFT else ""}">'
        f'<span class="nr">{nr}</span><span class="na">{na}</span>'
        f'<span class="da">{da}</span></div>'
        for i, (nr, na, da) in enumerate(TITEL)) + '</div>')


def _transport(g, d=34):
    return (f'<div style="display:flex;align-items:center;gap:{int(d * 1.1)}px">'
            f'<span class="taste">{prev(d, SCHWARZ)}</span>'
            f'<span class="taste">{pausei(int(d * 1.25), SCHWARZ)}</span>'
            f'<span class="taste">{nexti(d, SCHWARZ)}</span>'
            f'<span class="taste">{lupe(int(d * .82), MATT, 2.2)}</span>'
            f'<span class="taste">{biblio(int(d * .82), MATT)}</span>'
            f'<span class="taste">{laut(int(d * .82), MATT)}</span></div>')


def rechner():
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;padding:56px 72px">
  <div style="position:absolute;left:640px;top:60px">
    {_scheibe(g, 560, A['frac'])}</div>
  <div class="platte" style="position:absolute;right:78px;top:44px;
    width:240px;height:240px"></div>
  <div style="position:relative;display:flex;flex-direction:column;height:100%;
    justify-content:space-between">
    <div style="display:flex;align-items:baseline;justify-content:space-between">
      <span class="kap" style="font-size:17px">Musiklib · {A['sammlung']} Alben</span>
      <span class="kap" style="font-size:17px">{A['jahr']}</span>
    </div>
    <div style="max-width:560px">
      <div class="schlag" style="font-size:126px">{A['album']}</div>
      <div style="margin-top:22px;font-size:26px;color:{MATT}">{A['interpret']}</div>
    </div>
    <div style="display:flex;align-items:flex-end;gap:56px">
      <div style="width:600px">{_liste(g, 15)}</div>
      <div style="flex:1;display:flex;flex-direction:column;gap:20px;align-items:flex-start">
        {_transport(g)}
        <div style="display:flex;gap:26px">
          <span class="zeit" style="font-size:20px">{A['pos']}</span>
          <span class="zeit" style="font-size:20px">{A['rest']}</span></div>
      </div>
    </div>
  </div>
</div>'''
    return _css(g), body


def telefon():
    """Hochkant behält das Plakat seine Ordnung: Überschrift, Scheibe,
    Blocksatz. Die Liste wird einspaltig — zwei Spalten auf 1080 px sind
    keine Spalten mehr, sondern zwei zu kurze Zeilen."""
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;padding:104px 56px 110px;
  display:flex;flex-direction:column;justify-content:space-between">
  <div class="platte" style="position:absolute;right:56px;top:180px;
    width:210px;height:210px"></div>
  <div style="display:flex;align-items:baseline;justify-content:space-between">
    <span class="kap" style="font-size:19px">Musiklib · {A['sammlung']} Alben</span>
    <span class="kap" style="font-size:19px">{A['jahr']}</span>
  </div>
  <div style="max-width:720px">
    <div class="schlag" style="font-size:132px">{A['album']}</div>
    <div style="margin-top:20px;font-size:28px;color:{MATT}">{A['interpret']}</div>
  </div>
  <div style="display:flex;justify-content:center">{_scheibe(g, 620, A['frac'])}</div>
  <div>{_liste(g, 19)}</div>
  <div style="display:flex;align-items:center;justify-content:space-between">
    <span class="zeit" style="font-size:23px">{A['pos']}</span>
    {_transport(g, 42)}
    <span class="zeit" style="font-size:23px">{A['rest']}</span>
  </div>
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('73', 'Anschlag', art, css, body)
