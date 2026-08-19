# -*- coding: utf-8 -*-
"""80 Klepsydra — das Album läuft in ein Glas.

Dritte von drei **Abweichungen**. Kein Vorbild im Register und wieder kein
Gerät: das Blatt ist ein **Messzylinder**, und was darin steigt, ist das
Album.

Die Fortschrittsanzeige steht senkrecht und ist eine Flüssigkeit. Auf dem
Glas sind die Titelgrenzen als **geätzte Marken** eingeteilt — im Verhältnis
der echten Spielzeiten, also in ungleichen Abständen —, dazwischen die feine
Minutenteilung. Der Meniskus, die nach oben gezogene Kante der Flüssigkeit,
ist die Gegenwart. Man liest sie ab wie an einem Laborglas: an der
Unterkante der Wölbung.

Warum senkrecht, und warum das überhaupt etwas anderes ist als ein gekippter
Balken:

- **Ein Balken ist leer und füllt sich. Ein Glas ist ein Gefäss und läuft
  voll.** Der Unterschied ist nicht die Richtung, sondern dass hier etwas
  *bleibt*: das Gehörte sammelt sich sichtbar unten, statt hinter einem
  Fortschrittspunkt zu verschwinden.
- **Die Titelliste ist die Skala.** Die Namen stehen rechts neben ihrer
  eigenen Marke, mit einer Anschlusslinie ans Glas — sie sind nicht eine
  Liste *neben* der Anzeige, sie *sind* die Anzeige. Der lange Titel bekommt
  ein breites Band, der kurze ein schmales, und das sieht man vor jeder Zahl.
- **Gespult wird am Meniskus**, senkrecht gezogen. Es gibt keine zweite
  Fläche dafür.

Zwei Farben und Messing: kaltes Glasgrau, Tintenblau für die Flüssigkeit,
Messing für Halsring und Fuss. Die einzige Stelle, an der es hell wird, ist
der Glanzstreifen auf dem Glas — und der steht still, denn er zeigt nichts.

Abgegrenzt: K79 Milchlicht und K90 Nachtglas arbeiten auch mit einer Kante
zwischen zwei Zuständen, aber dort ist es Licht auf einer waagerechten Bahn.
Hier ist es Masse in einem Gefäss, und das Gefäss hat einen Boden.
"""
from kanon import LAEUFT, TITEL, gesamtzeit, marken
from werkzeug import A, biblio, laut, lupe, nexti, pausei, prev, schreibe
from werkzeug import MONO, SANS, SERIF

GRUND = '#E9EBEC'
GRUND2 = '#D5D9DB'
GLASRAND = '#8C979C'
AETZ = '#5D686D'
TINTE = '#1D3E63'
TINTE2 = '#2E5D8C'
SCHRIFT = '#23292C'
STUMM = 'rgba(35,41,44,.52)'
MESSING = '#B08D45'
MESSING2 = '#8C6E2E'


def _css(tel):
    k = 1.5 if tel else 1
    return f'''
.stage{{background:
    radial-gradient(120% 90% at 50% 0%,#F2F4F5 0%,{GRUND} 46%,{GRUND2} 100%);
  font-family:{SANS};color:{SCHRIFT};-webkit-font-smoothing:antialiased}}
.kap{{font-size:{int(12 * k)}px;letter-spacing:.30em;text-transform:uppercase;
  color:{STUMM}}}
.werk{{font-family:{SERIF};font-size:{int(52 * k)}px;line-height:1.02;
  letter-spacing:-.016em;color:{SCHRIFT}}}
.wer{{font-family:{SERIF};font-style:italic;font-size:{int(25 * k)}px;color:{STUMM};
  margin-top:{int(12 * k)}px}}
/* Messingfassung: Halsring und Fuss sind aus demselben Material, also aus
   demselben Verlauf. */
.mess{{display:flex;align-items:center;justify-content:center;
  background:linear-gradient(180deg,#E4CF95 0%,{MESSING} 38%,{MESSING2} 100%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.55),inset 0 -2px 3px rgba(0,0,0,.30),
    0 2px 6px rgba(29,62,99,.22);border-radius:{int(5 * k)}px}}
.taste{{width:{int(70 * k)}px;height:{int(48 * k)}px}}
.klein{{width:{int(46 * k)}px;height:{int(40 * k)}px}}
'''


def _saeule(w, h, tx, tw, k, namen=True):
    """Der Messzylinder: Glas, Flüssigkeit, Ätzung, Namen.

    Alles in einem SVG, weil die Namen **auf der Höhe ihrer Marke** stehen
    müssen. Zwei getrennte Ebenen — Glas als Bild, Liste als HTML — würden
    genau das nicht garantieren.
    """
    grenzen, stand = marken()
    ty, tb = 8 * k, h - 8 * k               # oberer und unterer Rand des Glases
    innen_o, innen_u = ty + 26 * k, tb - 26 * k
    hoehe = innen_u - innen_o

    def y(f):
        return innen_u - f * hoehe

    spiegel = y(stand)
    r = tw * .10

    # Ätzung: feine Minutenteilung, dazu die Titelgrenzen als lange Marken.
    fein = ''.join(
        f'<line x1="{tx + tw * .66:.1f}" y1="{y(i / 40):.1f}" x2="{tx + tw * .88:.1f}" '
        f'y2="{y(i / 40):.1f}" stroke="{AETZ}" stroke-width="{1 * k:.1f}" '
        f'opacity="{.38 if i % 5 == 0 else .18}"/>' for i in range(41))
    marken_ = ''
    for i, f in enumerate(grenzen):
        yy = y(f)
        marken_ += (f'<line x1="{tx + tw * .12:.1f}" y1="{yy:.1f}" x2="{tx + tw * .88:.1f}" '
                    f'y2="{yy:.1f}" stroke="{AETZ}" stroke-width="{1.5 * k:.1f}" opacity=".62"/>'
                    f'<line x1="{tx + tw * .12:.1f}" y1="{yy + 1:.1f}" '
                    f'x2="{tx + tw * .88:.1f}" y2="{yy + 1:.1f}" stroke="#FFFFFF" '
                    f'stroke-width="{1 * k:.1f}" opacity=".45"/>')

    beschriftung = ''
    if namen:
        for i, (nr, na, da) in enumerate(TITEL):
            ym = (y(grenzen[i]) + y(grenzen[i + 1])) / 2
            jetzt = i == LAEUFT
            fett = " font-weight='600'" if jetzt else ''
            lx = tx + tw + 74 * k
            beschriftung += (
                f'<line x1="{tx + tw + 10 * k:.1f}" y1="{ym:.1f}" x2="{lx - 16 * k:.1f}" '
                f'y2="{ym:.1f}" stroke="{AETZ}" stroke-width="1" opacity=".38"/>'
                f'<text x="{lx:.1f}" y="{ym - 4 * k:.1f}" font-family="{SERIF}" '
                f'font-size="{int((23 if jetzt else 21) * k)}" '
                f'fill="{TINTE if jetzt else SCHRIFT}" opacity="{1 if jetzt else .78}"'
                f'{fett}>{na}</text>'
                f'<text x="{lx:.1f}" y="{ym + 21 * k:.1f}" font-family="{MONO}" '
                f'font-size="{int(13 * k)}" fill="{TINTE2 if jetzt else AETZ}" '
                f'opacity="{1 if jetzt else .55}">{nr} · {da}</text>')

    # Der Meniskus zieht sich an den Wänden hoch — daran liest man den Stand
    # ab, und deshalb ist die Ablesekante die *untere* Kante der Wölbung.
    mh = tw * .045
    fluss = (f'<path d="M{tx:.1f} {spiegel - mh:.1f} '
             f'Q{tx + tw / 2:.1f} {spiegel + mh * 1.8:.1f} {tx + tw:.1f} {spiegel - mh:.1f} '
             f'L{tx + tw:.1f} {innen_u + 18 * k:.1f} L{tx:.1f} {innen_u + 18 * k:.1f} Z" '
             f'fill="url(#fl{int(w)})"/>')
    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
  <linearGradient id="fl{int(w)}" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{TINTE}"/><stop offset="34%" stop-color="{TINTE2}"/>
    <stop offset="62%" stop-color="{TINTE}"/><stop offset="100%" stop-color="#16304D"/>
  </linearGradient>
  <linearGradient id="gl{int(w)}" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="rgba(255,255,255,.62)"/>
    <stop offset="16%" stop-color="rgba(255,255,255,.16)"/>
    <stop offset="52%" stop-color="rgba(255,255,255,.05)"/>
    <stop offset="84%" stop-color="rgba(255,255,255,.30)"/>
    <stop offset="100%" stop-color="rgba(255,255,255,.55)"/>
  </linearGradient>
  <clipPath id="rohr{int(w)}">
    <path d="M{tx:.1f} {ty:.1f} L{tx + tw:.1f} {ty:.1f} L{tx + tw:.1f} {tb - r:.1f}
      Q{tx + tw:.1f} {tb:.1f} {tx + tw - r:.1f} {tb:.1f}
      L{tx + r:.1f} {tb:.1f} Q{tx:.1f} {tb:.1f} {tx:.1f} {tb - r:.1f} Z"/>
  </clipPath>
</defs>
<g clip-path="url(#rohr{int(w)})">
  <rect x="{tx:.1f}" y="{ty:.1f}" width="{tw:.1f}" height="{tb - ty:.1f}"
    fill="rgba(255,255,255,.42)"/>
  {fluss}
  <rect x="{tx:.1f}" y="{ty:.1f}" width="{tw:.1f}" height="{tb - ty:.1f}"
    fill="url(#gl{int(w)})"/>
</g>
{fein}{marken_}
<path d="M{tx:.1f} {ty:.1f} L{tx + tw:.1f} {ty:.1f} L{tx + tw:.1f} {tb - r:.1f}
  Q{tx + tw:.1f} {tb:.1f} {tx + tw - r:.1f} {tb:.1f}
  L{tx + r:.1f} {tb:.1f} Q{tx:.1f} {tb:.1f} {tx:.1f} {tb - r:.1f} Z"
  fill="none" stroke="{GLASRAND}" stroke-width="{2 * k:.1f}" opacity=".85"/>
<line x1="{tx + tw * .17:.1f}" y1="{ty + 14 * k:.1f}" x2="{tx + tw * .17:.1f}"
  y2="{tb - 22 * k:.1f}" stroke="#FFFFFF" stroke-width="{2.5 * k:.1f}" opacity=".62"/>
<!-- Die Ablesekante: eine feine helle Linie auf der Unterkante der Woelbung -->
<path d="M{tx:.1f} {spiegel - mh:.1f} Q{tx + tw / 2:.1f} {spiegel + mh * 1.8:.1f}
  {tx + tw:.1f} {spiegel - mh:.1f}" fill="none" stroke="#CFE3F4"
  stroke-width="{2.2 * k:.1f}" opacity=".95"/>
<text x="{tx - 14 * k:.1f}" y="{spiegel - 8 * k:.1f}" text-anchor="end"
  font-family="{MONO}" font-size="{int(21 * k)}" fill="{TINTE}">{A['pos']}</text>
<text x="{tx - 14 * k:.1f}" y="{spiegel + 16 * k:.1f}" text-anchor="end"
  font-family="{MONO}" font-size="{int(13 * k)}" fill="{AETZ}">{A['rest']}</text>
<ellipse cx="{tx + tw / 2:.1f}" cy="{ty:.1f}" rx="{tw / 2:.1f}" ry="{tw * .085:.1f}"
  fill="none" stroke="{GLASRAND}" stroke-width="{2 * k:.1f}" opacity=".85"/>
<ellipse cx="{tx + tw / 2:.1f}" cy="{ty:.1f}" rx="{tw / 2 - 4 * k:.1f}"
  ry="{tw * .062:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{1.4 * k:.1f}"
  opacity=".55"/>
<ellipse cx="{tx + tw / 2:.1f}" cy="{tb + 10 * k:.1f}" rx="{tw * .62:.1f}"
  ry="{tw * .075:.1f}" fill="rgba(29,62,99,.14)"/>
{beschriftung}
</svg>'''


def _tasten(k):
    return (f'<div class="mess taste">{prev(int(24 * k), "#2A2312")}</div>'
            f'<div class="mess taste" style="width:{int(92 * k)}px">'
            f'{pausei(int(28 * k), "#2A2312")}</div>'
            f'<div class="mess taste">{nexti(int(24 * k), "#2A2312")}</div>')


def _leise(k):
    return (f'<div class="mess klein">{lupe(int(20 * k), "#2A2312", 2)}</div>'
            f'<div class="mess klein">{biblio(int(20 * k), "#2A2312")}</div>'
            f'<div class="mess klein">{laut(int(20 * k), "#2A2312")}</div>')


def rechner():
    """Links steht, was es ist, in der Mitte steht das Glas, rechts steht die
    Skala — und die Skala ist die Titelliste. Die drei Spalten sind nicht
    Gestaltung, sondern die Ablesefolge: Was? Wie weit? Was gerade?"""
    tel, k = False, 1
    body = f'''<div style="position:absolute;left:90px;top:80px" class="kap">Musiklib · {A['sammlung']} Alben</div>
<div style="position:absolute;left:90px;top:50%;transform:translateY(-50%);width:420px">
  <div class="werk">{A['album']}</div>
  <div class="wer">{A['interpret']} · {A['jahr']}</div>
  <div class="kap" style="margin-top:24px">{len(TITEL)} Titel · {gesamtzeit()}</div>
  <div style="display:flex;gap:14px;margin-top:44px">{_tasten(k)}</div>
</div>
<div style="position:absolute;right:90px;top:76px;display:flex;gap:12px">{_leise(k)}</div>
<div style="position:absolute;left:540px;right:56px;top:56px;bottom:56px">
  {_saeule(1004, 888, 110, 240, k)}
</div>'''
    return _css(tel), body


def telefon():
    """Hochkant bleibt alles, wie es ist — ein Zylinder ist von Natur aus
    hochkant. Er wird nur länger, und die Namen rücken näher."""
    tel, k = True, 1.5
    body = f'''<div style="position:absolute;left:76px;right:76px;top:80px;
  display:flex;align-items:baseline;justify-content:space-between">
  <span class="kap">Musiklib</span>
  <span class="kap">{len(TITEL)} Titel · {gesamtzeit()}</span>
</div>
<div style="position:absolute;left:76px;right:76px;top:132px">
  <div class="werk">{A['album']}</div>
  <div class="wer">{A['interpret']} · {A['jahr']}</div>
</div>
<div style="position:absolute;left:0;right:0;top:330px;bottom:250px">
  {_saeule(1080, 1760, 200, 190, k)}
</div>
<div style="position:absolute;left:76px;right:76px;bottom:88px;display:flex;
  align-items:center;justify-content:space-between">
  <div style="display:flex;gap:20px">{_tasten(k)}</div>
  <div style="display:flex;gap:14px">{_leise(k)}</div>
</div>'''
    return _css(tel), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('80', 'Klepsydra', art, css, body)
