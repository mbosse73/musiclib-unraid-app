# -*- coding: utf-8 -*-
"""75 Bogen — Papier. Eine einzige Haarlinie trägt das ganze Album.

Erste der drei Synthesen (75 Papier, 76 Glas, 77 Metall); der gemeinsame
Aufbau steht in `kanon.py`.

Woher die Teile kommen:

- **Die Haarlinie als einzige Anzeige** ist K06 Aufgeschlagen: „Eine Haarlinie
  ist die Position, mehr steht nicht da.“
- **Die Warteschlange als Achse mit einem Strich je Titel** ist K13 Papier,
  wo sie im rechten Rand steht.
- **Elfenbein, Messing, Serifen und gesperrte Kapitälchen** sind ebenfalls
  K13, das Passepartout um das Bild ist K14 Desert Rose.
- **Der Blocksatz-Ernst der Titelliste** ist K87 Anschlag.

Die Synthese ist, dass aus zwei Anzeigen eine wird. In K06 zeigt der Faden
den Stand im Titel, in K13 zeigt die Randachse den Stand in der Schlange —
zwei Linien für dieselbe Frage. Hier ist es **eine** Linie über die volle
Satzbreite: die feinen Striche sind die Titelgrenzen, die Raute ist die
Gegenwart. Man liest daran beides ab, ohne den Blick zu wechseln, und
gespult wird über Titelgrenzen hinweg an derselben Linie. Weil die Striche
im Verhältnis der echten Spielzeiten stehen, ist die Linie zugleich das
Bild des Albums: „So What“ und „All Blues“ sind lang, „Blue in Green“ ist
kurz, und das sieht man, bevor man eine Zahl liest.

Nur zwei Farben und eine dritte für den Stand. Messing steht **nur** dort,
wo etwas gilt: auf der abgespielten Strecke, auf der Raute, auf der Ziffer
des laufenden Titels. Alles andere ist Tinte auf Papier.
"""
from kanon import GOLD, RAND, gesamtzeit, grade, leise, m, marken, transport
from kanon import LAEUFT, TITEL
from werkzeug import A, cover, schreibe, MONO, SANS, SERIF

PAPIER = '#F4F0E6'
PAPIER2 = '#EBE4D3'
TINTE = '#1C1A16'
MESSING = '#9A7638'
MATT = 'rgba(28,26,22,.56)'
STUMM = 'rgba(28,26,22,.34)'
LINIE = 'rgba(28,26,22,.15)'


def _css(tel):
    g = grade(tel)
    return f'''
.stage{{background:
    radial-gradient(120% 80% at 30% 0%,{PAPIER} 0%,{PAPIER2} 100%);
  font-family:{SANS};color:{TINTE};-webkit-font-smoothing:antialiased}}
.kap{{font-size:{g['mark']}px;letter-spacing:.28em;text-transform:uppercase;
  color:{STUMM};font-weight:600}}
.titel{{font-family:{SERIF};font-size:{g['titel']}px;line-height:1.02;
  letter-spacing:-.012em;text-wrap:balance}}
.wer{{font-family:{SERIF};font-size:{g['gross']}px;color:{MATT};font-style:italic}}
/* Passepartout: das Bild sitzt nicht auf dem Papier, es liegt darin. */
.paspa{{background:{PAPIER};box-shadow:0 1px 0 rgba(255,255,255,.7) inset,
    0 {m(0, tel)}px {m(2, tel)}px rgba(28,26,22,.07);
  border:1px solid {LINIE};display:flex;flex-direction:column;align-items:center}}
.paspa .bild{{flex:none;box-shadow:0 0 0 1px rgba(28,26,22,.22)}}
.danach{{font-family:{SERIF};font-size:{g['klein']}px;color:{MATT}}}
.danach b{{font-weight:400;color:{TINTE}}}
/* Die Titelliste: gesetzt, nicht gelistet. Linien nur zwischen den Zeilen. */
.satz .z{{display:flex;align-items:baseline;gap:{m(2, tel)}px;
  padding:{m(1, tel)}px 0;border-bottom:1px solid {LINIE}}}
.satz .z:first-child{{border-top:1px solid {LINIE}}}
.satz .nr{{font-family:{MONO};font-size:{g['mark']}px;color:{STUMM};flex:none;
  font-variant-numeric:tabular-nums}}
.satz .na{{font-family:{SERIF};font-size:{g['lauf']}px;color:{MATT};flex:1;
  min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.satz .da{{font-family:{MONO};font-size:{g['klein']}px;color:{STUMM};flex:none;
  font-variant-numeric:tabular-nums}}
.satz .z.jetzt .na{{color:{TINTE}}}
.satz .z.jetzt .nr{{color:{MESSING}}}
.zeit{{font-family:{MONO};font-size:{g['klein']}px;color:{MATT};
  font-variant-numeric:tabular-nums}}
'''


def _faden(w, tel):
    """Die eine Linie. Voll: die gelaufene Strecke in Messing, feine Striche
    an den Titelgrenzen, eine Raute auf der Gegenwart, darunter die Ziffern.

    Die Höhe ist gerechnet, nicht gesetzt — sonst fallen die Ziffern unter
    dem Blattrand heraus, sobald der Grad sich ändert."""
    grenzen, stand = marken()
    hoch = 11 if tel else 8
    fs = 19 if tel else 13
    y = hoch + (6 if tel else 4)
    grund = y + hoch + (26 if tel else 18)
    h = grund + (6 if tel else 4)
    x = w * stand
    striche = ''.join(
        f'<line x1="{w * f:.1f}" y1="{y - hoch:.1f}" x2="{w * f:.1f}" y2="{y + hoch:.1f}" '
        f'stroke="{TINTE}" stroke-width="1" opacity="{.34 if 0 < i < len(grenzen) - 1 else .5}"/>'
        for i, f in enumerate(grenzen))
    ziffern = ''.join(
        f'<text x="{w * (grenzen[i] + grenzen[i + 1]) / 2:.1f}" y="{grund}" '
        f'font-family="{MONO}" font-size="{fs}" text-anchor="middle" '
        f'fill="{MESSING if i == LAEUFT else "rgba(28,26,22,.34)"}">{nr}</text>'
        for i, (nr, _, _) in enumerate(TITEL))
    r = 7 if tel else 5
    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{TINTE}" stroke-width="1" opacity=".18"/>
<line x1="0" y1="{y}" x2="{x:.1f}" y2="{y}" stroke="{MESSING}" stroke-width="{2.2 if tel else 1.6}"/>
{striche}{ziffern}
<path d="M{x:.1f} {y - r} L{x + r:.1f} {y} L{x:.1f} {y + r} L{x - r:.1f} {y} Z" fill="{MESSING}"/>
</svg>'''


def _liste(tel):
    return '<div class="satz">' + ''.join(
        f'<div class="z{" jetzt" if i == LAEUFT else ""}"><span class="nr">{nr}</span>'
        f'<span class="na">{na}</span><span class="da">{da}</span></div>'
        for i, (nr, na, da) in enumerate(TITEL)) + '</div>'


def _bild(maxw, maxh, tel):
    """Bild im Passepartout, darunter die Bildunterschrift — wie im Katalog.

    Der untere Rand ist anderthalbmal so breit wie die seitlichen; das
    gleicht aus, dass das Auge eine mittig gesetzte Fläche nach unten
    gezogen sieht. Die Kartonmaße folgen dem Bild, nicht umgekehrt: gegeben
    sind nur die zwei Grenzen, und es gilt die engere von beiden."""
    g = grade(tel)
    spalt, cap = m(1, tel), int(g['mark'] * 1.4)
    innen = int(min(maxw / 1.20, (maxh - spalt - cap) / 1.26))
    seit, unten = int(innen * .10), int(innen * .16)
    return f'''<div class="paspa" style="width:{innen + 2 * seit}px;
  padding:{seit}px {seit}px {unten}px">
  {cover(innen, 0, '#2E4A63', '#0E1E2E', '#EDE6D6', .8, 'bild')}
  <div class="kap" style="margin-top:{spalt}px">{A['jahr']} · {len(TITEL)} Titel · {gesamtzeit()}</div>
</div>'''


def rechner():
    """Der Goldene Schnitt teilt die Satzbreite: links das Bild, rechts der
    Satz. Beide Spalten enden auf derselben Linie — darum steht unten rechts,
    was nach dem Album kommt, statt dass dort nichts steht."""
    tel = False
    breite, hoehe = 1600 - 2 * RAND, 1000 - 2 * RAND
    kopf, boden, luft = 30, 105, m(4)
    mitte = hoehe - kopf - boden - 2 * luft
    bild = int(breite * GOLD)
    rechts = breite - bild - m(4)
    body = f'''<div style="position:absolute;inset:0;padding:{RAND}px;display:flex;
  flex-direction:column;gap:{luft}px">
  <div style="height:{kopf}px;display:flex;align-items:center;
    justify-content:space-between">
    <span class="kap">Musiklib · {A['sammlung']} Alben</span>
    {leise(MATT, 30)}
  </div>
  <div style="height:{mitte}px;display:flex;gap:{m(4)}px">
    <div style="width:{bild}px;display:flex;justify-content:center">
      {_bild(bild, mitte, tel)}</div>
    <div style="width:{rechts}px;display:flex;flex-direction:column">
      <div class="titel">{A['album']}</div>
      <div class="wer" style="margin-top:{m(1)}px">{A['interpret']}</div>
      <div style="margin-top:{m(4)}px">{_liste(tel)}</div>
      <div class="danach" style="margin-top:auto">
        <span class="kap" style="margin-right:{m(1)}px">Danach</span>
        <b>Milestones</b> · Miles Davis</div>
    </div>
  </div>
  <div style="height:{boden}px">
    {_faden(breite, tel)}
    <div style="display:flex;align-items:center;justify-content:space-between;
      margin-top:{m(2)}px">
      <span class="zeit">{A['pos']}</span>
      {transport(TINTE, 42)}
      <span class="zeit">{A['rest']}</span>
    </div>
  </div>
</div>'''
    return _css(tel), body


def telefon():
    """Hochkant fällt die Teilung weg: eine Spalte, alles auf der Mittelachse
    — das ist K14 Desert Rose. Die Linie bleibt, was sie ist."""
    tel = True
    breite = 1080 - 2 * RAND
    body = f'''<div style="position:absolute;inset:0;padding:{RAND}px {RAND}px {int(RAND * 1.2)}px;
  display:flex;flex-direction:column;align-items:center;justify-content:space-between">
  <div style="width:100%;display:flex;align-items:center;justify-content:space-between">
    <span class="kap">Musiklib · {A['sammlung']} Alben</span>
    {leise(MATT, 40)}
  </div>
  {_bild(breite, 1100, tel)}
  <div style="text-align:center">
    <div class="titel">{A['album']}</div>
    <div class="wer" style="margin-top:{m(1, tel)}px">{A['interpret']}</div>
  </div>
  <div style="width:100%">{_liste(tel)}</div>
  <div class="danach">
    <span class="kap" style="margin-right:{m(1, tel)}px">Danach</span>
    <b>Milestones</b> · Miles Davis</div>
  <div style="width:100%">
    {_faden(breite, tel)}
    <div style="display:flex;align-items:center;justify-content:space-between;
      margin-top:{m(2, tel)}px">
      <span class="zeit">{A['pos']}</span>
      {transport(TINTE, 48)}
      <span class="zeit">{A['rest']}</span>
    </div>
  </div>
</div>'''
    return _css(tel), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('75', 'Bogen', art, css, body)
