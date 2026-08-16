# -*- coding: utf-8 -*-
"""61 Fernanzeige — die Anzeige, die man aus drei Metern liest.

Vorlage ist eine Bildschirmanzeige, wie sie ein Gerät einblendet, während es
spielt: ein grauer Schleier über die ganze Fläche, mittig der Titel in zwei
Zeilen, darunter der Interpret, eine Haarlinie als Stand, und in den beiden
unteren Ecken genau zwei Zeichen — links die Lautstärke als Zahl, rechts die
Wiedergabe. Sonst nichts.

Drei Dinge daran sind der Entwurf:

- **Kein Bild, aber auch kein leerer Grund.** Der Schleier *ist* das Cover,
  nur so weit weggezogen, dass nichts mehr davon zu erkennen ist. Deshalb ist
  er kein flaches Grau, sondern ein weicher Verlauf mit einer hellen Stelle —
  ein Bild, das man nicht mehr sieht, aber noch spürt. Hier ist er aus
  Verläufen gebaut, nicht aus einer Datei: dieselbe Regel wie überall im Satz.
- **Der Titel ist die Anzeige.** Er steht mittig, gross, dünn und darf zwei
  Zeilen brauchen — lange Werktitel („Goldberg Variations, BWV 988, Arr. …“)
  sind der Normalfall und nicht der Ausnahmefall, der abgeschnitten wird.
- **Zwei Zeichen, so weit auseinander wie möglich.** Lautstärke links unten,
  Wiedergabe rechts unten. Was dazwischen liegt, ist Anzeige und keine
  Bedienung. Die Lautstärke steht als **Zahl**, nicht als Regler: eine Zahl
  liest man aus drei Metern, einen Reglerstand nicht.

Der Zugang zur Sammlung ist die einzige Zutat gegenüber der Vorlage — er muss
in jedem Blatt vorkommen. Er sitzt als schmale Zeile oben in der Mitte, wo bei
einem Gerät der Quellenname steht, und stört die untere Reihe damit nicht.

Verwandt, aber nicht dasselbe: 44 Gerätezeile ist eine schmale Zeile am Gerät,
60 Klimaxfront ein Feld in Originalgrösse hinter Glas. Dies hier ist die
Einblendung über der ganzen Fläche — kein Gerät, nur Anzeige.
"""
from werkzeug import A, biblio, laut, schreibe, tri, MONO, SANS

# Ein einziges Grau in vier Stufen. Der Schleier hat eine helle Stelle links
# der Mitte — dort, wo im Original das weggezogene Bild am hellsten war.
HELL = '#F4F5F6'
MATT = 'rgba(244,245,246,.72)'
STUMM = 'rgba(244,245,246,.46)'
LEISE = 'rgba(244,245,246,.26)'
BAHN = 'rgba(244,245,246,.30)'


def _css(g):
    return f'''
/* Der Schleier: zwei weiche Lichter über einem mittleren Grau, dazu ein
   Abdunkeln zu den Rändern. Kein Rahmen, keine Kante, keine Karte — die
   Anzeige hat keinen Ort, sie liegt über allem. */
.stage{{background:
    radial-gradient(78% 96% at 34% 34%,rgba(255,255,255,.30) 0%,rgba(255,255,255,0) 62%),
    radial-gradient(66% 80% at 78% 74%,rgba(255,255,255,.13) 0%,rgba(255,255,255,0) 58%),
    radial-gradient(120% 130% at 50% 46%,#9B9DA0 0%,#85878B 52%,#6C6E72 100%);
  font-family:{SANS};color:{HELL};-webkit-font-smoothing:antialiased}}

/* Die Quellenzeile — hier führt sie in die Sammlung. Klein, gesperrt, matt:
   sie soll da sein, aber nicht mitlesen. */
.quelle{{display:inline-flex;align-items:center;color:{STUMM};letter-spacing:.26em;
  text-transform:uppercase;font-weight:500}}

/* Der Titel darf umbrechen und tut es mittig. Dünn geschnitten, weil er gross
   ist: ein fetter Schnitt in dieser Grösse wäre ein Schild, keine Anzeige. */
.titel{{font-weight:300;letter-spacing:-.021em;line-height:1.14;text-align:center;
  text-wrap:balance}}
.unter{{color:{MATT};font-weight:300;text-align:center}}

/* Die Haarlinie. Der gelaufene Teil ist heller, nicht farbig — in dieser
   Anzeige gibt es keine zweite Farbe. */
.bahn{{position:relative;background:{LEISE}}}
.bahn i{{position:absolute;left:0;top:0;bottom:0;background:{BAHN}}}
.bahn i b{{position:absolute;inset:0;background:{HELL}}}

.reihe{{display:flex;align-items:center;justify-content:space-between}}
.pegel{{display:inline-flex;align-items:center;color:{MATT}}}
.pegel b{{font-weight:400;font-variant-numeric:tabular-nums;letter-spacing:.02em}}
.zeit{{font-family:{MONO};color:{STUMM};font-variant-numeric:tabular-nums}}
'''


def _kopf(g):
    """Die Quellenzeile — der Weg in die Sammlung, oben in der Mitte."""
    return (f'<div style="text-align:center"><span class="quelle" '
            f'style="gap:{int(13 * g)}px;font-size:{20 * g:.0f}px">'
            f'{biblio(int(21 * g), STUMM)}Sammlung · {A["sammlung"]} Alben</span></div>')


def _mitte(g, titel_px):
    return f'''<div>
  <div class="titel" style="font-size:{titel_px * g:.0f}px">{A['titel']}</div>
  <div class="unter" style="font-size:{34 * g:.0f}px;margin-top:{int(26 * g)}px">
    {A['interpret']} · {A['album']} · {A['jahr']}</div>
</div>'''


def _fuss(g):
    """Haarlinie, darunter die beiden Zeichen in den Ecken.

    Die Zeiten stehen an den Enden der Linie und nicht bei den Zeichen: so
    liest sich die Linie mit ihren Zahlen als ein Ding, und die untere Reihe
    bleibt das, was sie in der Vorlage ist — links Ton, rechts Wiedergabe."""
    strich = max(1, int(2 * g))
    return f'''<div>
  <div class="bahn" style="height:{strich}px">
    <i style="width:{A['frac'] * 100:.0f}%"><b></b></i></div>
  <div class="reihe" style="margin-top:{int(16 * g)}px">
    <span class="zeit" style="font-size:{22 * g:.0f}px">{A['pos']}</span>
    <span class="zeit" style="font-size:{22 * g:.0f}px">{A['rest']}</span>
  </div>
  <div class="reihe" style="margin-top:{int(38 * g)}px">
    <span class="pegel" style="gap:{int(16 * g)}px">
      {laut(int(34 * g), MATT)}<b style="font-size:{38 * g:.0f}px">60</b></span>
    <span style="display:inline-flex">{tri(int(46 * g), HELL)}</span>
  </div>
</div>'''


def rechner():
    """Querformat: der Titel steht über der Mitte, die untere Reihe hat Luft.

    Nicht `space-between` über die ganze Höhe: die Vorlage klebt weder oben
    noch unten am Rand — sie ist eine Einblendung und lässt ringsum Fläche
    stehen. Der Titel sitzt bei rund einem Drittel, die beiden Zeichen bei
    rund vier Fünfteln."""
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  padding:74px 120px 168px">
  {_kopf(g)}
  <div style="margin-top:132px;display:flex;justify-content:center">
    <div style="width:1120px;max-width:100%">{_mitte(g, 92)}</div>
  </div>
  <div style="margin-top:auto">{_fuss(g)}</div>
</div>'''
    return _css(g), body


def telefon():
    """Hochformat: dieselbe Anzeige, dieselbe Reihenfolge, nichts dazu.

    Der Titel steht etwas über der Mitte, weil die untere Hälfte eines
    Telefons in der Hand liegt und die obere gelesen wird."""
    g = .92
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  padding:130px 84px 260px">
  {_kopf(g)}
  <div style="flex:1;min-height:0;display:flex;align-items:center;
    padding-bottom:{int(230 * g)}px">
    <div style="width:100%">{_mitte(g, 78)}</div>
  </div>
  {_fuss(g)}
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('61', 'Fernanzeige', art, css, body)
