# -*- coding: utf-8 -*-
"""76 Nachtglas — Glas. Das Licht selbst ist der Stand.

Zweite der drei Synthesen (75 Papier, 76 Glas, 77 Metall); der gemeinsame
Aufbau steht in `kanon.py`.

Woher die Teile kommen:

- **Die Milchglaskarte auf reinem Anthrazit, ohne Farbwolken** ist K49 Glass
  ohne Kreise — dort war das die Abwandlung, die das Blatt gerettet hat.
- **Die Warteschlange als Reihe einzelner Glasscheiben** ist K21
  Milchglaszeilen.
- **Die hinterleuchtete Bahn, an der die Lichtkante die Position ist**, ist
  K79 Milchlicht.
- **Eisblau als einziger kalter Ton** ist K84 Dezibel, das nächtliche
  Grundblau K03 Vollbild.

Zwei Entscheidungen sind die Synthese:

**Die Lichtkante läuft andersherum als bei Milchlicht.** Dort ist dunkel,
was gelaufen ist. Hier leuchtet, was gelaufen ist — die Polung von K03
Vollbild, wo die gespielten Rillen glühen. Grund: das Auge geht zur
hellsten Stelle. Läuft das Licht dem Finger voraus, zieht es den Blick
dorthin, wo nichts passiert ist; läuft es hinterher, steht die Kante genau
auf der Gegenwart, und die Gegenwart ist die einzige Auskunft, die man im
Vorbeigehen braucht.

**Die Bahn zeigt nur den Titel, nicht das Album.** Das ist der bewusste
Gegenentwurf zu 75 Bogen, wo eine Linie beides trägt: hier tragen die
Glaszeilen darunter das Album ohnehin schon, jede mit ihrer eigenen Kante.
Eine Anzeige zweimal zu bauen ist keine Redundanz, sondern eine Frage zu
viel — man müsste erst herausfinden, welche der beiden gerade gemeint ist.

**Die einzige Farbe im Bild kommt vom Album.** Alles andere ist grauer
Schleier auf Nacht; das Cover leuchtet hinter dem Glas durch und färbt es.
Ein Blatt, das seine Farbe von seinem Inhalt bekommt, sieht bei jedem Album
anders aus, ohne dass jemand eine Palette pflegt.
"""
from kanon import RAND, grade, leise, m, transport
from kanon import IM_TITEL, LAEUFT, TITEL, sekunden
from werkzeug import A, cover, schreibe, MONO, SANS

NACHT = '#080A0D'
NACHT2 = '#0E131A'
EIS = '#9CC7EA'
EIS2 = '#5E8FB8'
GLUT = '#2E5D86'          # die Farbe des Covers, die hinter dem Glas steht
WEISS = '#F2F5F8'
MATT = 'rgba(242,245,248,.62)'
STUMM = 'rgba(242,245,248,.34)'

FRAC = IM_TITEL / sekunden(TITEL[LAEUFT][2])


def _css(tel):
    g = grade(tel)
    r = m(3, tel)
    return f'''
.stage{{background:
    radial-gradient(120% 90% at 50% 8%,{NACHT2} 0%,{NACHT} 62%),
    {NACHT};
  font-family:{SANS};color:{WEISS};-webkit-font-smoothing:antialiased}}
/* Der Schein steht hinter dem Glas, nicht darauf — deshalb ein eigenes
   Element unter der Karte und kein Schatten an ihr. */
.schein{{position:absolute;border-radius:50%;filter:blur({m(4, tel)}px);
  background:radial-gradient(closest-side,{GLUT} 0%,rgba(46,93,134,0) 100%);
  opacity:.62}}
.glas{{position:relative;border-radius:{r}px;
  background:linear-gradient(152deg,rgba(255,255,255,.10) 0%,rgba(255,255,255,.035) 100%);
  border:1px solid rgba(255,255,255,.13);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.22),0 {m(2, tel)}px {m(5, tel)}px rgba(0,0,0,.55)}}
.kap{{font-size:{g['mark']}px;letter-spacing:.26em;text-transform:uppercase;
  color:{STUMM};font-weight:600}}
.titel{{font-size:{g['titel']}px;font-weight:300;letter-spacing:-.02em;line-height:1.05}}
.wer{{font-size:{g['gross']}px;font-weight:300;color:{MATT};margin-top:{m(0, tel)}px}}
.zeit{{font-family:{MONO};font-size:{g['klein']}px;color:{STUMM};
  font-variant-numeric:tabular-nums}}
/* Jede Zeile eine eigene Scheibe — K21. Die laufende ist die einzige, die
   von hinten Licht bekommt. */
.zeile{{display:flex;align-items:center;gap:{m(2, tel)}px;border-radius:{m(1, tel)}px;
  padding:0 {m(2, tel)}px;background:rgba(255,255,255,.045);
  border:1px solid rgba(255,255,255,.06);position:relative;overflow:hidden}}
.zeile .nr{{font-family:{MONO};font-size:{g['mark']}px;color:{STUMM};flex:none;
  font-variant-numeric:tabular-nums}}
.zeile .na{{font-size:{g['lauf']}px;font-weight:300;color:{MATT};flex:1;min-width:0;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.zeile .da{{font-family:{MONO};font-size:{g['klein']}px;color:{STUMM};flex:none;
  font-variant-numeric:tabular-nums}}
.zeile.gelaufen .na{{color:{STUMM}}}
.zeile.jetzt{{background:rgba(255,255,255,.10);border-color:rgba(156,199,234,.30)}}
.zeile.jetzt .na{{color:{WEISS};font-weight:400}}
.zeile.jetzt .nr,.zeile.jetzt .da{{color:{EIS}}}
.zeile.jetzt::before{{content:'';position:absolute;left:0;top:0;bottom:0;
  width:{m(0, tel) // 3 + 2}px;background:{EIS};box-shadow:0 0 {m(2, tel)}px {EIS2}}}
'''


def _bahn(w, tel):
    """Die hinterleuchtete Bahn: gelaufen leuchtet, kommend ist dunkles Glas,
    und die Kante dazwischen ist die Gegenwart."""
    h = m(1, tel) + 3
    x = w * FRAC
    return f'''<div style="position:relative;width:{w}px;height:{h}px;border-radius:{h / 2}px;
  background:rgba(255,255,255,.07);box-shadow:inset 0 1px 0 rgba(255,255,255,.10);
  overflow:visible">
  <div style="position:absolute;left:0;top:0;bottom:0;width:{x:.0f}px;
    border-radius:{h / 2}px;background:linear-gradient(90deg,{EIS2} 0%,{EIS} 100%);
    box-shadow:0 0 {m(1, tel)}px rgba(156,199,234,.5)"></div>
  <div style="position:absolute;left:{x:.0f}px;top:{-h * .55:.1f}px;bottom:{-h * .55:.1f}px;
    width:2px;margin-left:-1px;background:{WEISS};border-radius:1px;
    box-shadow:0 0 {m(2, tel)}px rgba(242,245,248,.9)"></div>
</div>'''


def _zeilen(hoehe, tel):
    return ''.join(
        f'<div class="zeile{" jetzt" if i == LAEUFT else " gelaufen" if i < LAEUFT else ""}" '
        f'style="height:{hoehe}px"><span class="nr">{nr}</span>'
        f'<span class="na">{na}</span><span class="da">{da}</span></div>'
        for i, (nr, na, da) in enumerate(TITEL))


def rechner():
    tel = False
    kb, kh = 1180, 800
    pad = m(4)
    innen = kb - 2 * pad                      # 1070
    bild = 380
    rechts = innen - bild - m(4)
    zeile, spalt = 48, m(0)
    liste = len(TITEL) * zeile + (len(TITEL) - 1) * spalt
    oben = kh - 2 * pad - liste - m(3)
    body = f'''<div class="schein" style="left:{(1600 - kb) // 2 + pad - 210}px;
  top:{(1000 - kh) // 2 + pad - 210}px;width:{bild + 420}px;height:{bild + 420}px"></div>
<div class="glas" style="position:absolute;left:{(1600 - kb) // 2}px;
  top:{(1000 - kh) // 2}px;width:{kb}px;height:{kh}px;padding:{pad}px">
  <div style="display:flex;gap:{m(4)}px;height:{oben}px">
    {cover(bild, m(2), '#3A6E96', '#101C28', '#DCE8F2', .85)}
    <div style="width:{rechts}px;display:flex;flex-direction:column;
      justify-content:space-between">
      <div style="display:flex;align-items:center;justify-content:space-between">
        <span class="kap">Musiklib · {A['sammlung']} Alben</span>
        {leise(MATT, 30)}
      </div>
      <div>
        <div class="titel">{TITEL[LAEUFT][1]}</div>
        <div class="wer">{A['interpret']} · {A['album']} · {A['jahr']}</div>
      </div>
      <div>
        {_bahn(rechts, tel)}
        <div style="display:flex;justify-content:space-between;margin-top:{m(1)}px">
          <span class="zeit">{A['pos']}</span><span class="zeit">{A['rest']}</span>
        </div>
      </div>
      <div style="display:flex;justify-content:center">{transport(WEISS, 40)}</div>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;gap:{spalt}px;margin-top:{m(3)}px">
    {_zeilen(zeile, tel)}
  </div>
</div>'''
    return _css(tel), body


def telefon():
    """Hochkant wird aus der Karte die ganze Scheibe: eine Glasplatte über
    der Nacht, Bild oben, Schlange unten, die Lichtkante dazwischen."""
    tel = True
    kb, kh = 1080 - 2 * RAND, 2340 - 2 * RAND
    pad = m(3, tel)
    innen = kb - 2 * pad
    zeile, spalt = 76, m(0, tel)
    body = f'''<div class="schein" style="left:{RAND - 160}px;top:{RAND + 60}px;
  width:{innen + 320}px;height:{innen + 320}px"></div>
<div class="glas" style="position:absolute;left:{RAND}px;top:{RAND}px;
  width:{kb}px;height:{kh}px;padding:{pad}px;display:flex;flex-direction:column;
  justify-content:space-between">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <span class="kap">Musiklib · {A['sammlung']} Alben</span>
    {leise(MATT, 42)}
  </div>
  {cover(innen, m(2, tel), '#3A6E96', '#101C28', '#DCE8F2', .85)}
  <div>
    <div class="titel">{TITEL[LAEUFT][1]}</div>
    <div class="wer">{A['interpret']} · {A['album']} · {A['jahr']}</div>
  </div>
  <div>
    {_bahn(innen, tel)}
    <div style="display:flex;justify-content:space-between;margin-top:{m(1, tel)}px">
      <span class="zeit">{A['pos']}</span><span class="zeit">{A['rest']}</span>
    </div>
  </div>
  <div style="display:flex;justify-content:center">{transport(WEISS, 62)}</div>
  <div style="display:flex;flex-direction:column;gap:{spalt}px">
    {_zeilen(zeile, tel)}
  </div>
</div>'''
    return _css(tel), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('76', 'Nachtglas', art, css, body)
