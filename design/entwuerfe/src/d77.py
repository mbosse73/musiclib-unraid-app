# -*- coding: utf-8 -*-
"""77 Rundlauf — Metall. Ein Rad, eine gravierte Skala, sonst nichts.

Dritte der drei Synthesen (75 Papier, 76 Glas, 77 Metall); der gemeinsame
Aufbau steht in `kanon.py`.

Woher die Teile kommen:

- **Das geriffelte Schwungrad als Spulfläche** ist K78 Gyrorad, dort noch mit
  Holzwangen und Zeigerwerk daneben.
- **Champagner als Farbe der Frontplatte** ist K11/K12 Turm und
  Vollverstärker, der Nussbaum darunter ebenfalls — hier auf einen Sockel
  zusammengeschrumpft, weil ein ganzes Gehäuse aus Holz das Blatt zu einem
  Möbel macht.
- **Die in Glas gravierte Skala mit dem Lichtbalken dahinter** ist K77
  Glasgravur.
- **Die silberne Platte, die die ganze Auskunft trägt**, ist K85
  Silberkasten.
- **Kein Cover** ist K83 Halbmond: „ein Verstärker zeigt, was läuft, nicht
  was es gibt.“

Die Synthese ist eine Aufteilung, die alle vier Vorlagen nur halb haben:
**oben wird gelesen, unten wird angefasst, und dazwischen liegt eine Kante.**
Über der Kante steht nichts, was man drücken könnte, und unter ihr steht
nichts, was man lesen müsste. Das ist der Grund, warum ein Gerät aus den
Siebzigern im Dunkeln bedienbar ist und eine Glasfläche nicht: die Hand
findet die Zone, bevor das Auge die Beschriftung liest.

Die drei Tasten sind deshalb echte Tasten mit Kante und Lichtsaum, keine
Zeichen auf der Fläche — und das Rad ist so gross, dass der Daumen es trifft,
ohne hinzusehen. Am Telefon ist es das grösste Ding auf dem Blatt.

Genau eine Farbe: Bernstein. Sie steht auf dem Skalenzeiger und auf dem
laufenden Titel, nirgends sonst. Alles andere ist Metall, Gravur und Licht.
"""
import math

from kanon import RAND, gesamtzeit, grade, leise, m, marken, zeichenreihe
from kanon import LAEUFT, TITEL
from werkzeug import A, schreibe, MONO, SANS

BLECH = '#DAD5C9'
BLECH2 = '#C9C3B4'
PLATTE = '#CFC9BB'
GRAVUR = '#3B382F'
STUMM = 'rgba(59,56,47,.52)'
GLAS = '#17150F'
LICHT = '#F3E9D2'
LICHT2 = 'rgba(243,233,210,.46)'
BERNSTEIN = '#C8802E'
NUSS = '#4A3524'


def _css(tel):
    g = grade(tel)
    return f'''
.stage{{background:linear-gradient(180deg,{BLECH} 0%,{BLECH2} 100%);
  font-family:{SANS};color:{GRAVUR};-webkit-font-smoothing:antialiased}}
/* Gebürstet: feine Striche, nicht als Bild, sondern als Verlaufsmuster. */
.stage::before{{content:'';position:absolute;inset:0;pointer-events:none;
  background:repeating-linear-gradient(90deg,rgba(255,255,255,.30) 0 1px,
    rgba(0,0,0,.03) 1px 3px);opacity:.35}}
/* Gravur heisst: die Schrift steht tiefer als die Platte, also ein weisser
   Lichtsaum unten. Ohne den ist es Aufdruck. */
.grav{{text-shadow:0 1px 0 rgba(255,255,255,.62)}}
.kap{{font-size:{g['mark']}px;letter-spacing:.30em;text-transform:uppercase;
  color:{STUMM};font-weight:600;text-shadow:0 1px 0 rgba(255,255,255,.62)}}
.glas{{position:relative;background:
    linear-gradient(180deg,#1E1B14 0%,{GLAS} 46%,#100E09 100%);
  border-radius:{m(0, tel) // 2}px;overflow:hidden;
  box-shadow:inset 0 2px {m(1, tel)}px rgba(0,0,0,.85),
    inset 0 -1px 0 rgba(255,255,255,.07),0 1px 0 rgba(255,255,255,.55)}}
.glas::after{{content:'';position:absolute;left:0;right:0;top:0;height:34%;
  background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,0))}}
.lauf{{font-size:{g['titel']}px;font-weight:300;color:{LICHT};letter-spacing:-.01em}}
.unter{{font-size:{g['lauf']}px;font-weight:300;color:{LICHT2};margin-top:{m(0, tel)}px}}
.stand{{font-family:{MONO};font-size:{g['titel']}px;color:{LICHT};
  font-variant-numeric:tabular-nums;letter-spacing:-.02em}}
.rest{{font-family:{MONO};font-size:{g['klein']}px;color:{LICHT2};
  font-variant-numeric:tabular-nums}}
/* Die Platte liegt in der Front, nicht darauf: innen Schatten, aussen Licht. */
.plat{{background:{PLATTE};border-radius:{m(0, tel) // 2}px;
  box-shadow:inset 0 2px 5px rgba(0,0,0,.20),inset 0 -1px 0 rgba(255,255,255,.55),
    0 1px 0 rgba(255,255,255,.55)}}
.z{{display:flex;align-items:center;gap:{m(2, tel)}px;
  border-bottom:1px solid rgba(59,56,47,.13)}}
.z:last-child{{border-bottom:0}}
.z .nr{{font-family:{MONO};font-size:{g['mark']}px;color:{STUMM};flex:none;
  font-variant-numeric:tabular-nums}}
.z .na{{font-size:{g['lauf']}px;color:{GRAVUR};flex:1;min-width:0;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}}
.z .da{{font-family:{MONO};font-size:{g['klein']}px;color:{STUMM};flex:none;
  font-variant-numeric:tabular-nums}}
.z.jetzt .na{{color:{BERNSTEIN};font-weight:500}}
.z.jetzt .nr{{color:{BERNSTEIN}}}
/* Eine Taste hat eine Kante, sonst ist sie ein Zeichen auf einer Fläche. */
.taste{{display:flex;align-items:center;justify-content:center;
  background:linear-gradient(180deg,#3A362E 0%,#232019 100%);
  border-radius:{m(0, tel) // 2}px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 2px 3px rgba(0,0,0,.28),
    0 1px 0 rgba(255,255,255,.5)}}
'''


def _skala(w, tel):
    """Die gravierte Skala: feine Striche über das ganze Album, hohe Striche
    an den Titelgrenzen, ein Lichtbalken in Bernstein auf der Gegenwart."""
    grenzen, stand = marken()
    fein, hoch = (9, 22) if tel else (6, 15)
    fs = 17 if tel else 12
    grund = fein + hoch + fs + (14 if tel else 10)
    h = grund + (6 if tel else 4)
    y = hoch + (8 if tel else 5)
    feine = ''.join(
        f'<line x1="{w * i / 60:.1f}" y1="{y - fein}" x2="{w * i / 60:.1f}" y2="{y}" '
        f'stroke="{LICHT}" stroke-width="1" opacity=".22"/>' for i in range(61))
    hohe = ''.join(
        f'<line x1="{max(.5, w * f):.1f}" y1="{y - hoch}" x2="{max(.5, w * f):.1f}" y2="{y}" '
        f'stroke="{LICHT}" stroke-width="1.4" opacity=".55"/>' for f in grenzen)
    ziffern = ''.join(
        f'<text x="{w * (grenzen[i] + grenzen[i + 1]) / 2:.1f}" y="{grund}" '
        f'font-family="{MONO}" font-size="{fs}" text-anchor="middle" '
        f'fill="{BERNSTEIN if i == LAEUFT else LICHT}" '
        f'opacity="{1 if i == LAEUFT else .40}">{nr}</text>'
        for i, (nr, _, _) in enumerate(TITEL))
    x = w * stand
    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs><filter id="gl{int(w)}" x="-40%" y="-40%" width="180%" height="180%">
  <feGaussianBlur stdDeviation="{4 if tel else 2.6}"/></filter></defs>
<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{LICHT}" stroke-width="1" opacity=".18"/>
{feine}{hohe}{ziffern}
<rect x="{x - (3 if tel else 2):.1f}" y="{y - hoch - (6 if tel else 4)}"
  width="{6 if tel else 4}" height="{hoch + (10 if tel else 7)}" rx="{2 if tel else 1.5}"
  fill="{BERNSTEIN}" filter="url(#gl{int(w)})"/>
<rect x="{x - (1.5 if tel else 1):.1f}" y="{y - hoch - (6 if tel else 4)}"
  width="{3 if tel else 2}" height="{hoch + (10 if tel else 7)}" rx="{1.5 if tel else 1}"
  fill="{BERNSTEIN}"/></svg>'''


def _rad(d):
    """Das geriffelte Rad. Die Riffelung ist gezeichnet, nicht gerastert:
    je Kerbe ein dunkler und ein heller Strich, damit sie eine Kante hat."""
    r = d / 2
    kerben = ''
    for i in range(84):
        a = math.radians(i * 360 / 84)
        for versatz, farbe, deck in ((0, '#26231C', .45), (.020, '#FFFFFF', .45)):
            c, s = math.cos(a + versatz), math.sin(a + versatz)
            kerben += (f'<line x1="{r + c * r * .862:.1f}" y1="{r + s * r * .862:.1f}" '
                       f'x2="{r + c * r * .994:.1f}" y2="{r + s * r * .994:.1f}" '
                       f'stroke="{farbe}" stroke-width="{r * .014:.1f}" opacity="{deck}"/>')
    return f'''<svg viewBox="0 0 {d} {d}" width="{d}" height="{d}">
<defs>
 <linearGradient id="rd{int(d)}" x1="0" y1="0" x2=".4" y2="1">
  <stop offset="0%" stop-color="#F1EDE4"/><stop offset="42%" stop-color="#CFC9BB"/>
  <stop offset="72%" stop-color="#AFA898"/><stop offset="100%" stop-color="#D5CFC1"/>
 </linearGradient>
 <linearGradient id="ri{int(d)}" x1=".2" y1="0" x2=".8" y2="1">
  <stop offset="0%" stop-color="#E6E1D5"/><stop offset="55%" stop-color="#C4BEAF"/>
  <stop offset="100%" stop-color="#B3AC9C"/>
 </linearGradient>
</defs>
<circle cx="{r}" cy="{r}" r="{r - 1}" fill="url(#rd{int(d)})"
  stroke="rgba(0,0,0,.22)" stroke-width="1"/>
{kerben}
<circle cx="{r}" cy="{r}" r="{r * .845:.1f}" fill="url(#ri{int(d)})"
  stroke="rgba(0,0,0,.22)" stroke-width="{r * .012:.1f}"/>
<circle cx="{r}" cy="{r + r * .010:.1f}" r="{r * .845:.1f}" fill="none"
  stroke="rgba(255,255,255,.60)" stroke-width="1"/>
<circle cx="{r}" cy="{r}" r="{r * .085:.1f}" fill="#BDB6A6"
  stroke="rgba(0,0,0,.20)" stroke-width="1"/>
<circle cx="{r}" cy="{r * .28:.1f}" r="{r * .036:.1f}" fill="{GRAVUR}" opacity=".50"/>
</svg>'''


def _tasten(tel, b, h, d):
    """Zurück · Wiedergabe · Vor in der Reihenfolge des Kanons, jedes Zeichen
    in einer eigenen Taste. Die mittlere ist breiter, nicht nur ihr Zeichen."""
    zeichen = zeichenreihe(LICHT, d)
    breiten = (b, int(b * 1.34), b)
    return (f'<div style="display:flex;gap:{m(1, tel)}px">' + ''.join(
        f'<div class="taste" style="width:{bb}px;height:{h}px">{z}</div>'
        for z, bb in zip(zeichen, breiten)) + '</div>')


def _liste(tel, hoehe):
    return ''.join(
        f'<div class="z{" jetzt" if i == LAEUFT else ""}" style="height:{hoehe}px">'
        f'<span class="nr">{nr}</span><span class="na">{na}</span>'
        f'<span class="da">{da}</span></div>'
        for i, (nr, na, da) in enumerate(TITEL))


def _sockel(tel):
    """Der Nussbaum ist auf einen Sockel geschrumpft — ein ganzes Gehäuse aus
    Holz macht aus dem Blatt ein Möbel."""
    h = m(2, tel)
    return f'''<div style="position:absolute;left:0;right:0;bottom:0;height:{h}px;
  background:linear-gradient(180deg,{NUSS} 0%,#33241A 100%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.14),0 -1px 0 rgba(0,0,0,.30)"></div>'''


def rechner():
    tel = False
    breite = 1600 - 2 * RAND
    sockel = m(2)
    hoehe = 1000 - 2 * RAND - sockel
    kopf, schirm, luft = 30, 214, m(4)
    unten = hoehe - kopf - schirm - 2 * luft
    plat = int(breite * .618)
    rechts = breite - plat - m(4)
    body = f'''{_sockel(tel)}
<div style="position:absolute;left:{RAND}px;right:{RAND}px;top:{RAND}px;
  height:{hoehe}px;display:flex;flex-direction:column;gap:{luft}px">
  <div style="height:{kopf}px;display:flex;align-items:center;
    justify-content:space-between">
    <span class="kap">Musiklib · {A['sammlung']} Alben</span>
    {leise(STUMM, 30)}
  </div>
  <div class="glas" style="height:{schirm}px;padding:{m(3)}px {m(4)}px {m(2)}px">
    <div style="position:relative;display:flex;align-items:flex-start;
      justify-content:space-between">
      <div>
        <div class="lauf">{TITEL[LAEUFT][1]}</div>
        <div class="unter">{A['interpret']} · {A['album']} · {A['jahr']}</div>
      </div>
      <div style="text-align:right">
        <div class="stand">{A['pos']}</div>
        <div class="rest">{A['rest']}</div>
      </div>
    </div>
    <div style="position:absolute;left:{m(4)}px;right:{m(4)}px;bottom:{m(2)}px">
      {_skala(breite - 2 * m(4), tel)}</div>
  </div>
  <div style="height:{unten}px;display:flex;gap:{m(4)}px">
    <div class="plat" style="width:{plat}px;padding:0 {m(3)}px">
      <div class="kap" style="height:{m(4)}px;display:flex;align-items:center;
        border-bottom:1px solid rgba(59,56,47,.20)">{A['album']} · {A['interpret']}
        · {len(TITEL)} Titel · {gesamtzeit()}</div>
      {_liste(tel, (unten - m(4) - 2) // len(TITEL))}</div>
    <div style="width:{rechts}px;display:flex;flex-direction:column;
      align-items:center;justify-content:space-between">
      <div style="text-align:center">
        {_rad(unten - 120)}
        <div class="kap" style="margin-top:{m(1)}px">Spulen</div>
      </div>
      {_tasten(tel, 86, 54, 26)}
    </div>
  </div>
</div>'''
    return _css(tel), body


def telefon():
    """Hochkant steht dieselbe Ordnung übereinander — lesen oben, greifen
    unten. Das Rad wird zum grössten Ding auf dem Blatt, weil der Daumen es
    treffen soll, ohne dass das Auge hinkommt."""
    tel = True
    breite = 1080 - 2 * RAND
    sockel = m(2, tel)
    schirm, rad = 340, 600
    body = f'''{_sockel(tel)}
<div style="position:absolute;left:{RAND}px;right:{RAND}px;top:{RAND}px;
  bottom:{sockel + m(3, tel)}px;display:flex;flex-direction:column;
  justify-content:space-between">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <span class="kap">Musiklib · {A['sammlung']} Alben</span>
    {leise(STUMM, 42)}
  </div>
  <div class="glas" style="height:{schirm}px;padding:{m(3, tel)}px {m(3, tel)}px {m(2, tel)}px">
    <div style="position:relative">
      <div class="lauf">{TITEL[LAEUFT][1]}</div>
      <div style="display:flex;align-items:baseline;justify-content:space-between">
        <div class="unter">{A['interpret']} · {A['album']}</div>
        <div style="text-align:right">
          <span class="stand" style="font-size:{grade(tel)['gross']}px">{A['pos']}</span>
          <span class="rest" style="margin-left:{m(1, tel)}px">{A['rest']}</span>
        </div>
      </div>
    </div>
    <div style="position:absolute;left:{m(3, tel)}px;right:{m(3, tel)}px;bottom:{m(2, tel)}px">
      {_skala(breite - 2 * m(3, tel), tel)}</div>
  </div>
  <div class="plat" style="padding:0 {m(3, tel)}px">
    <div class="kap" style="height:{m(4, tel)}px;display:flex;align-items:center;
      border-bottom:1px solid rgba(59,56,47,.20)">{A['album']}
      · {len(TITEL)} Titel · {gesamtzeit()}</div>
    {_liste(tel, 104)}</div>
  <div style="text-align:center">
    {_rad(rad)}
    <div class="kap" style="margin-top:{m(1, tel)}px">Spulen</div>
  </div>
  <div style="display:flex;justify-content:center">{_tasten(tel, 200, 120, 52)}</div>
</div>'''
    return _css(tel), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('77', 'Rundlauf', art, css, body)
