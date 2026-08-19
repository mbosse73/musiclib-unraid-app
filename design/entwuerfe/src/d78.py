# -*- coding: utf-8 -*-
"""78 Schattenwurf — die Anzeige ist ein Schatten.

Erste von drei **Abweichungen**. Die drei sind ausdrücklich nicht nach dem
Kanon der Synthesen gebaut: sie teilen kein Maßband, keinen Satzspiegel und
keine Bedienreihe, weil genau das die Synthesen eingeebnet hat. Hier gilt nur
eine Regel, und die ist die Hausregel: **bewegt wird, was den Stand zeigt.**

Kein Vorbild im Register. Was hier steht, ist eine **waagerechte Sonnenuhr**:
eine helle Platte, ein Schattenwerfer am unteren Rand, und ein Fächer
eingravierter Linien darüber. Jede Linie ist eine Titelgrenze, jedes Feld
dazwischen ein Titel — und die Felder sind **unterschiedlich breit**, weil
sie im Verhältnis der echten Spielzeiten stehen. Ein langes Stück nimmt am
Himmel mehr Platz ein als ein kurzes.

Der Schatten ist die einzige bewegte Sache auf dem Blatt und die einzige
Anzeige. Er wandert im Lauf des Albums von links nach rechts über die Platte,
wie der Schatten im Lauf des Tages. In welchem Feld er steht, ist der Titel;
wo im Feld er steht, ist die Stelle im Titel. Es gibt keinen Balken, keinen
Ring und keine Prozentzahl — die gäbe es auf einer Sonnenuhr auch nicht.

Drei Dinge, die daraus folgen und die man nicht wegnehmen kann, ohne den
Entwurf zu verlieren:

- **Der Schatten hat einen weichen Rand.** Ein harter Zeiger wäre ein Zeiger;
  die Halbschatten-Kante ist das, was ihn zum Schatten macht. Sie ist auch
  ehrlich: eine Sekunde genau muss eine Musikanzeige nicht sein.
- **Gespult wird am Schatten selbst**, nicht an einer Leiste darunter. Man
  schiebt ihn wie einen Zeiger über die Felder; über Titelgrenzen hinweg,
  ohne abzusetzen.
- **Nichts leuchtet.** Das Licht kommt von schräg oben links und fällt auf
  Kalkputz. Alles Farbige auf dem Blatt ist Messing oder Gravur.

Abgegrenzt: K87 Anschlag hat auch eine Scheibe als Uhr, aber dort ist es ein
gedruckter Sektor auf einem Plakat. Hier ist nichts gedruckt — hier fällt
Licht auf eine Fläche, und was übrig bleibt, ist die Auskunft.
"""
import math

from kanon import LAEUFT, TITEL, marken
from werkzeug import A, biblio, laut, lupe, nexti, pausei, prev, schreibe
from werkzeug import MONO, SANS, SERIF

PUTZ = '#EAE3D4'
PUTZ2 = '#D7CDB8'
GRAVUR = '#6C6355'
TIEF = '#4A4335'
SCHATTEN = '#4E5B7A'
MESSING = '#A8843C'
MESSING2 = '#8A6A2C'


def _css(tel):
    k = 1.5 if tel else 1
    return f'''
.stage{{background:
    radial-gradient(120% 100% at 14% -8%,{PUTZ} 0%,{PUTZ2} 58%,#CEC3AC 100%);
  font-family:{SANS};color:{GRAVUR};-webkit-font-smoothing:antialiased}}
/* Kalk ist nicht glatt. Das Korn ist ein Muster, kein Bild — sonst waere es
   eine Textur-Datei, und die Blaetter haben keine. */
.stage::before{{content:'';position:absolute;inset:0;pointer-events:none;opacity:.5;
  background:
    repeating-linear-gradient(64deg,rgba(255,255,255,.5) 0 1px,rgba(0,0,0,.018) 1px 4px),
    repeating-linear-gradient(-21deg,rgba(0,0,0,.02) 0 1px,rgba(255,255,255,.32) 1px 3px)}}
.grav{{text-shadow:0 1px 0 rgba(255,255,255,.75)}}
.kap{{font-size:{int(13 * k)}px;letter-spacing:.30em;text-transform:uppercase;
  color:rgba(108,99,85,.62);text-shadow:0 1px 0 rgba(255,255,255,.75)}}
.werk{{font-family:{SERIF};font-size:{int(46 * k)}px;line-height:1.04;color:{TIEF};
  letter-spacing:-.012em;text-shadow:0 1px 0 rgba(255,255,255,.7)}}
.wer{{font-family:{SERIF};font-style:italic;font-size:{int(24 * k)}px;
  color:rgba(108,99,85,.78);margin-top:{int(10 * k)}px}}
.uhr{{font-family:{MONO};font-size:{int(20 * k)}px;color:{TIEF};
  font-variant-numeric:tabular-nums;text-shadow:0 1px 0 rgba(255,255,255,.7)}}
/* Ein Messingstift sitzt in der Platte: Loch, Rand, Kuppe. */
.stift{{display:flex;align-items:center;justify-content:center;border-radius:50%;
  background:radial-gradient(circle at 34% 28%,#E2C57E 0%,{MESSING} 46%,{MESSING2} 100%);
  box-shadow:0 1px 0 rgba(255,255,255,.7),inset 0 -1px 2px rgba(0,0,0,.35),
    0 0 0 1px rgba(0,0,0,.14),0 2px 5px rgba(74,67,53,.30)}}
'''


def _fan(w, h, k, halb, apex, R, basis=0.0, radial=False):
    """Der Fächer: Gravur, Schattenwerfer, Schatten.

    `halb` ist die halbe Fächeröffnung in Grad, `basis` die Richtung der
    Mittellinie (0 = nach oben). Am Telefon steht der Werfer nicht unten,
    sondern **links in halber Höhe**, und der Schatten wandert von oben nach
    unten statt von links nach rechts: eine hochkante Fläche hat den Platz
    für den Fächer in der Länge, nicht in der Breite. Das ist die einzige
    Stelle, an der die beiden Fassungen sich unterscheiden.
    """
    grenzen, stand = marken()
    cx, cy = apex
    ri = R * .17                           # innen bleibt der Werfer frei
    rl = R * .81                           # auf diesem Radius stehen die Namen

    def punkt(grad, r):
        a = math.radians(basis + grad)
        return cx + math.sin(a) * r, cy - math.cos(a) * r

    def grad(f):
        return -halb + 2 * halb * f

    # Der Bogen schliesst den Fächer und trägt die feine Teilung. Ohne ihn
    # sind es fünf Striche im Nichts; mit ihm ist es ein Zifferblatt.
    ax0, ay0 = punkt(-halb, R)
    ax1, ay1 = punkt(halb, R)
    # Die Platte selbst: heller Stein auf dem dunkleren Grund. Ohne diese
    # Fläche sind es Linien auf einer Wand statt einer Uhr, die daliegt.
    bogen = (f'<path d="M{cx:.1f} {cy:.1f} L{ax0:.1f} {ay0:.1f} '
             f'A{R:.1f} {R:.1f} 0 0 1 {ax1:.1f} {ay1:.1f} Z" '
             f'fill="rgba(255,253,246,.62)"/>')
    bogen += (f'<path d="M{ax0:.1f} {ay0:.1f} A{R:.1f} {R:.1f} 0 0 1 {ax1:.1f} {ay1:.1f}" '
             f'fill="none" stroke="{GRAVUR}" stroke-width="{1.4 * k:.1f}" opacity=".42"/>'
             f'<path d="M{ax0 + 1:.1f} {ay0 + 1:.1f} A{R:.1f} {R:.1f} 0 0 1 '
             f'{ax1 + 1:.1f} {ay1 + 1:.1f}" fill="none" stroke="#FFFFFF" '
             f'stroke-width="{1 * k:.1f}" opacity=".55"/>')
    for i in range(61):
        g = grad(i / 60)
        lang = i % 5 == 0
        t1 = R - (14 if lang else 8) * k
        x1, y1 = punkt(g, t1)
        x2, y2 = punkt(g, R)
        bogen += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                  f'stroke="{GRAVUR}" stroke-width="{1 * k:.1f}" '
                  f'opacity="{.40 if lang else .22}"/>')

    linien = ''
    for i, f in enumerate(grenzen):
        g = grad(f)
        x1, y1 = punkt(g, ri)
        x2, y2 = punkt(g, R)
        rand = i in (0, len(grenzen) - 1)
        linien += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                   f'stroke="{GRAVUR}" stroke-width="{1.6 * k if rand else 1 * k:.1f}" '
                   f'opacity="{.55 if rand else .30}"/>')
        # Die Gravur hat einen Lichtsaum, sonst liegt sie auf statt drin.
        linien += (f'<line x1="{x1 + 1:.1f}" y1="{y1 + 1:.1f}" x2="{x2 + 1:.1f}" '
                   f'y2="{y2 + 1:.1f}" stroke="#FFFFFF" stroke-width="{1 * k:.1f}" '
                   f'opacity=".55"/>')

    namen = ''
    for i, (nr, na, da) in enumerate(TITEL):
        g = grad((grenzen[i] + grenzen[i + 1]) / 2)
        x, y = punkt(g, rl)
        # Zwei Leserichtungen, und die Wahl haengt am Format. Quer stehen die
        # Namen quer zur Linie wie auf einem Zifferblatt; hochkant laufen sie
        # **entlang** der Linie nach aussen, weil sie sonst ab der Mitte des
        # Faechers kippen und die Reihe an einer willkuerlichen Stelle bricht.
        dreh = basis + g - (90 if radial else 0)
        vz = 1
        if not radial and abs(dreh) > 90:
            dreh, vz = dreh + 180, -1
        jetzt = i == LAEUFT
        fett = ' font-weight="600"' if jetzt else ''
        namen += (
            f'<g transform="rotate({dreh:.2f} {x:.1f} {y:.1f})">'
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" '
            f'font-family="{SERIF}" font-size="{int((21 if jetzt else 19) * k)}" '
            f'fill="{TIEF if jetzt else GRAVUR}" opacity="{1 if jetzt else .72}"'
            f'{fett}>{na}</text>'
            f'<text x="{x:.1f}" y="{y + vz * 26 * k:.1f}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="{int(13 * k)}" fill="{MESSING2 if jetzt else GRAVUR}" '
            f'opacity="{1 if jetzt else .48}">{nr} · {da}</text></g>')

    # Der Schatten: ein Keil, der nach aussen breiter wird — so wirft eine
    # Kante ihren Halbschatten, und deshalb ist die Spitze scharf und das
    # Ende weich.
    gs = grad(stand)
    sx0, sy0 = punkt(gs - .75, ri * .30)
    sx1, sy1 = punkt(gs + .75, ri * .30)
    sx2, sy2 = punkt(gs + 2.5, R * 1.00)
    sx3, sy3 = punkt(gs - 2.5, R * 1.00)
    tipx, tipy = punkt(gs, R * .92)

    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
  <filter id="wolke{int(w)}" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="{4.5 * k:.1f}"/></filter>
  <linearGradient id="sch{int(w)}" gradientUnits="userSpaceOnUse"
    x1="{cx:.0f}" y1="{cy:.0f}" x2="{tipx:.0f}" y2="{tipy:.0f}">
    <stop offset="0%" stop-color="{SCHATTEN}" stop-opacity=".78"/>
    <stop offset="50%" stop-color="{SCHATTEN}" stop-opacity=".54"/>
    <stop offset="100%" stop-color="{SCHATTEN}" stop-opacity=".16"/></linearGradient>
  <radialGradient id="knopf{int(w)}" cx="34%" cy="26%" r="74%">
    <stop offset="0%" stop-color="#E8CE8B"/><stop offset="52%" stop-color="{MESSING}"/>
    <stop offset="100%" stop-color="{MESSING2}"/></radialGradient>
</defs>
{bogen}{linien}{namen}
<path d="M{sx0:.1f} {sy0:.1f} L{sx1:.1f} {sy1:.1f} L{sx2:.1f} {sy2:.1f} L{sx3:.1f} {sy3:.1f} Z"
  fill="url(#sch{int(w)})" filter="url(#wolke{int(w)})"/>
<circle cx="{tipx:.1f}" cy="{tipy:.1f}" r="{5 * k:.1f}" fill="{SCHATTEN}" opacity=".30"
  filter="url(#wolke{int(w)})"/>
<!-- Der Werfer selbst: eine stehende Messingschneide, von oben gesehen. Sie
     dreht mit der Fächerrichtung, sonst zeigt sie am Telefon nach oben und
     der Schatten nach rechts. -->
<g transform="rotate({basis:.1f} {cx:.1f} {cy:.1f})">
  <ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{ri * .40:.1f}" ry="{ri * .13:.1f}"
    fill="{SCHATTEN}" opacity=".22" filter="url(#wolke{int(w)})"/>
  <path d="M{cx:.1f} {cy - ri * .92:.1f} L{cx + ri * .17:.1f} {cy:.1f}
    L{cx - ri * .17:.1f} {cy:.1f} Z" fill="url(#knopf{int(w)})"
    stroke="rgba(0,0,0,.22)" stroke-width="1"/>
  <circle cx="{cx:.1f}" cy="{cy - ri * .92:.1f}" r="{5.5 * k:.1f}"
    fill="url(#knopf{int(w)})" stroke="rgba(0,0,0,.20)" stroke-width="1"/>
</g>
</svg>'''


def _stifte(k, d, zeichen):
    return ''.join(
        f'<span class="stift" style="width:{int(sz * k)}px;height:{int(sz * k)}px">{z}</span>'
        for z, sz in zeichen)


def rechner():
    """Der Werfer steht unten in der Mitte, der Fächer nimmt die ganze Fläche.
    Die vier Ecken bleiben frei — das ist kein Rest, sondern der Platz, den
    eine Sonnenuhr für ihre Inschriften hat."""
    tel, k = False, 1
    W, H = 1600, 1000
    halb, apex = 63, (W / 2, H - 62)
    R = min(H - 150, (W / 2 - 40) / math.sin(math.radians(halb)))
    zeichen = [(prev(30, '#3E3320'), 62), (pausei(36, '#3E3320'), 76),
               (nexti(30, '#3E3320'), 62)]
    leise = [(lupe(24, '#3E3320', 2), 50), (biblio(24, '#3E3320'), 50),
             (laut(24, '#3E3320'), 50)]
    body = f'''<div style="position:absolute;inset:0">{_fan(W, H, k, halb, apex, R)}</div>
<div style="position:absolute;left:70px;top:66px;max-width:430px">
  <div class="kap">Musiklib · {A['sammlung']} Alben</div>
  <div class="werk" style="margin-top:24px">{A['album']}</div>
  <div class="wer">{A['interpret']} · {A['jahr']}</div>
</div>
<div style="position:absolute;right:70px;top:66px;text-align:right">
  <div class="kap">Stand</div>
  <div class="uhr" style="font-size:46px;margin-top:14px">{A['pos']}</div>
  <div class="uhr" style="opacity:.55;margin-top:4px">{A['rest']}</div>
  <div class="kap" style="margin-top:12px">{TITEL[LAEUFT][1]}</div>
</div>
<div style="position:absolute;left:70px;bottom:62px;display:flex;align-items:center;
  gap:30px">{_stifte(1, 0, zeichen)}</div>
<div style="position:absolute;right:70px;bottom:66px;display:flex;align-items:center;
  gap:24px">{_stifte(1, 0, leise)}</div>'''
    return _css(tel), body


def telefon():
    """Hochkant wird die Uhr **gekippt**: der Werfer steht links auf halber
    Höhe, und der Schatten wandert von oben nach unten. Eine hochkante Fläche
    hat ihren Platz in der Länge — ein Fächer, der nach oben aufmacht, wäre
    hier unten breit und oben leer."""
    tel, k = True, 1.5
    W, H = 1080, 2340
    halb = 58
    # Der Faecher lebt zwischen Kopfzeile und Textblock; sein Mittelpunkt ist
    # die Mitte dieses Streifens, nicht die Mitte des Blattes.
    oben, unten = 180, 1800
    apex = (74, (oben + unten) / 2)
    R = min(W - 140, ((unten - oben) / 2) / math.sin(math.radians(halb)))
    zeichen = [(prev(44, '#3E3320'), 92), (pausei(54, '#3E3320'), 116),
               (nexti(44, '#3E3320'), 92)]
    leise = [(lupe(34, '#3E3320', 2), 72), (biblio(34, '#3E3320'), 72),
             (laut(34, '#3E3320'), 72)]
    body = f'''<div style="position:absolute;inset:0">
  {_fan(W, H, k, halb, apex, R, basis=90, radial=True)}</div>
<div style="position:absolute;left:78px;right:78px;top:74px;display:flex;
  align-items:baseline;justify-content:space-between">
  <span class="kap">Musiklib · {A['sammlung']} Alben</span>
  <span class="kap">{A['jahr']}</span>
</div>
<div style="position:absolute;left:78px;right:78px;bottom:104px">
  <div class="werk">{A['album']}</div>
  <div class="wer">{A['interpret']}</div>
  <div style="display:flex;align-items:baseline;gap:26px;margin-top:30px">
    <span class="uhr" style="font-size:44px">{A['pos']}</span>
    <span class="uhr" style="opacity:.55">{A['rest']}</span>
  </div>
  <div style="display:flex;align-items:center;justify-content:space-between;
    margin-top:40px">
    <div style="display:flex;align-items:center;gap:34px">{_stifte(1, 0, zeichen)}</div>
    <div style="display:flex;align-items:center;gap:22px">{_stifte(1, 0, leise)}</div>
  </div>
</div>'''
    return _css(tel), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('78', 'Schattenwurf', art, css, body)
