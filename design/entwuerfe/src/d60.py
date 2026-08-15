# -*- coding: utf-8 -*-
"""60 Klimaxfront — die Anzeige des Linn Klimax DSM (nächste Generation).

Kein Foto aus `player2/` oder `player3/`, sondern ein benanntes Gerät als
Vorlage, wie in der zweiten Mockup-Reihe: die Front des Klimax DSM ist eine
schwarze Spiegelscheibe, hinter der ein **1600 × 480** grosses Feld leuchtet.
Was Linn dort zeigt, ist der ganze Entwurf:

- **kein Cover.** Der Hersteller lässt es bewusst weg — die Anzeige trägt
  Quelle, Lautstärke, Titel, Interpret, Album und das Format, sonst nichts;
- **eine Schrift, zwei Grade Grau.** Weiss für das, was gilt, gedämpftes Grau
  für das, was es beschreibt. Keine Farbe, kein Akzent, keine Fläche;
- **Spiegel, wenn nichts läuft.** Im Ruhezustand steht nur der Schriftzug da,
  der Rest der Front ist schwarzes Glas.

Deshalb ist beim Rechner-Blatt **das Feld in Originalgrösse eingesetzt**: die
Bühne ist 1600 breit, das Anzeigefeld ist 1600 × 480 und sitzt mittig in der
Scheibe. Das Telefon bekommt dasselbe Feld im selben Seitenverhältnis (1080 ×
324) und darunter, in derselben Sprache, was ein Telefon zusätzlich braucht:
die Warteschlange.

**Zwei Abweichungen von der Vorlage, beide bewusst.** Der Schriftzug ist
unserer, nicht der des Herstellers — das Blatt ist ein Entwurf für Musiklib und
soll sich nicht als fremdes Gerät ausgeben. Und die Vorlage zeigt Quelle und
Lautstärke *statt* der Titelzeile, hier stehen sie zusammen: ein Spieler ohne
Titel wäre keiner. 44 Gerätezeile geht auf dasselbe Haus zurück (Selekt DSM),
ist aber die schmale Zeile — hier ist es die ganze Breite.
"""
from werkzeug import (A, biblio, laut, lupe, nexti, pausei, prev, schreibe,
                      MONO, SANS)

GLAS = '#08090A'
WEISS = '#F1F3F4'
STUMM = 'rgba(241,243,244,.56)'
LEISE = 'rgba(241,243,244,.26)'
KAUM = 'rgba(241,243,244,.13)'


def _css(g):
    return f'''
/* Die Front ist eine schwarze Spiegelscheibe: ein stehender Verlauf, ein
   schräger Lichtstreifen darüber. Mehr Material hat das Gerät nicht. */
.stage{{background:
    linear-gradient(118deg,rgba(255,255,255,.055) 0%,rgba(255,255,255,0) 26%,
      rgba(255,255,255,.03) 52%,rgba(255,255,255,0) 74%),
    linear-gradient(180deg,#101214 0%,{GLAS} 46%,#05060700 100%),
    {GLAS};
  font-family:{SANS};color:{WEISS};-webkit-font-smoothing:antialiased}}
.stage::after{{content:"";position:absolute;inset:0;pointer-events:none;
  box-shadow:inset 0 {1 * g:.0f}px 0 rgba(255,255,255,.07),
    inset 0 {-1 * g:.0f}px 0 rgba(255,255,255,.04)}}

/* Das Anzeigefeld selbst — es leuchtet nicht heller als das Glas, es steht
   nur nicht im Spiegel. Deshalb kein Rahmen, nur eine Spur weniger Reflex. */
.feld{{position:relative;display:flex;flex-direction:column;
  justify-content:space-between;flex:none;
  background:radial-gradient(120% 160% at 50% 50%,#0C0E10 0%,{GLAS} 70%)}}

.kap{{letter-spacing:.24em;text-transform:uppercase;color:{STUMM};
  font-weight:500}}
.titel{{font-weight:300;letter-spacing:-.02em;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}}
.unterzeile{{color:{STUMM};font-weight:300;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}}

/* Die Lautstärke ist die zweite Zahl des Geräts — gross, dünn, ohne Einheit */
.laut{{display:flex;flex-direction:column;align-items:flex-end;flex:none}}
.laut b{{font-weight:200;letter-spacing:-.03em;font-variant-numeric:tabular-nums;
  line-height:.92}}

.bahn{{position:relative;background:{KAUM}}}
.bahn i{{position:absolute;left:0;top:0;bottom:0;background:{WEISS}}}
.zeit{{font-family:{MONO};color:{STUMM};font-variant-numeric:tabular-nums}}
.taste{{display:flex;align-items:center;justify-content:center;color:{STUMM}}}
.taste.haupt{{color:{WEISS}}}
.bib{{display:inline-flex;align-items:center;color:{STUMM};
  letter-spacing:.24em;text-transform:uppercase;font-weight:500}}

/* Ruhezustand: der eingravierte Schriftzug in der blanken Scheibe */
.gravur{{letter-spacing:.42em;text-transform:uppercase;color:{LEISE};
  font-weight:500;text-align:center}}

.zeile{{display:flex;align-items:baseline;border-top:1px solid {KAUM}}}
.zeile:last-child{{border-bottom:1px solid {KAUM}}}
.zeile .nr{{font-family:{MONO};color:{LEISE};flex:none}}
.zeile .t{{flex:1;min-width:0;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis;color:{STUMM}}}
.zeile .d{{font-family:{MONO};color:{LEISE};flex:none}}
.zeile.an .t{{color:{WEISS}}}
.zeile.an .nr{{color:{WEISS}}}
'''


def _feld(g, breite, hoehe):
    """Das Anzeigefeld — im Rechner-Blatt 1600 × 480, also Originalgrösse."""
    p_x, p_y = int(56 * g), int(42 * g)
    return f'''<div class="feld" style="width:{breite}px;height:{hoehe}px;
  padding:{p_y}px {p_x}px">

  <div style="display:flex;align-items:baseline;justify-content:space-between;
    gap:{int(40 * g)}px">
    <span class="bib" style="gap:{int(12 * g)}px;font-size:{20 * g:.0f}px">
      {biblio(int(21 * g), STUMM)}Sammlung · {A['sammlung']} Alben</span>
    <span class="kap" style="font-size:{20 * g:.0f}px">FLAC · 24 Bit · 96 kHz</span>
  </div>

  <div style="display:flex;align-items:flex-end;justify-content:space-between;
    gap:{int(56 * g)}px;min-width:0">
    <div style="min-width:0">
      <div class="titel" style="font-size:{78 * g:.0f}px">{A['titel']}</div>
      <div class="unterzeile" style="font-size:{30 * g:.0f}px;
        margin-top:{int(12 * g)}px">
        {A['interpret']} · {A['album']} · {A['jahr']}</div>
    </div>
    <div class="laut">
      <span class="kap" style="font-size:{17 * g:.0f}px;
        margin-bottom:{int(10 * g)}px">Lautstärke</span>
      <b style="font-size:{116 * g:.0f}px">60</b>
    </div>
  </div>

  <div>
    <div class="bahn" style="height:{max(2, int(3 * g))}px">
      <i style="width:{A['frac'] * 100:.0f}%"></i></div>
    <div style="display:flex;align-items:center;justify-content:space-between;
      margin-top:{int(20 * g)}px">
      <span class="zeit" style="font-size:{22 * g:.0f}px">{A['pos']}</span>
      <div style="display:flex;align-items:center;gap:{int(52 * g)}px">
        <span class="taste">{prev(int(30 * g), STUMM)}</span>
        <span class="taste haupt">{pausei(int(38 * g), WEISS)}</span>
        <span class="taste">{nexti(int(30 * g), STUMM)}</span>
        <span class="taste">{lupe(int(26 * g), STUMM)}</span>
        <span class="taste" style="gap:{int(10 * g)}px">
          {laut(int(26 * g), STUMM)}</span>
      </div>
      <span class="zeit" style="font-size:{22 * g:.0f}px">{A['rest']}</span>
    </div>
  </div>
</div>'''


def _liste(g, schrift, klein):
    return ''.join(
        f'<div class="zeile{" an" if i == A["laeuft"] else ""}" '
        f'style="gap:{int(24 * g)}px;padding:{int(17 * g)}px {int(4 * g)}px;'
        f'font-size:{schrift}px">'
        f'<span class="nr" style="font-size:{klein}px;width:{int(34 * g)}px">{nr}</span>'
        f'<span class="t">{t}</span>'
        f'<span class="d" style="font-size:{klein}px">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))


def _quellen(g):
    """Am Gerät wählt der Drehknopf die Quelle — auf dem Telefon die Zeile.

    Das ist zugleich der Bibliotheks-Zugang: die Sammlung ist eine Quelle wie
    jede andere, nicht ein Knopf, den es am Klimax nicht gibt."""
    posten = [(biblio(20, WEISS), 'Sammlung', f'{A["sammlung"]} Alben', True),
              (lupe(20, STUMM), 'Suche', 'Titel, Album, Interpret', False),
              (laut(20, STUMM), 'Interpreten', '63 Namen', False)]
    return ''.join(
        f'<div class="zeile{" an" if an else ""}" style="gap:{int(24 * g)}px;'
        f'padding:{int(19 * g)}px {int(4 * g)}px;font-size:32px;align-items:center">'
        f'<span style="flex:none;display:flex">{zeichen}</span>'
        f'<span class="t">{name}</span>'
        f'<span class="d" style="font-size:24px">{wert}</span></div>'
        for zeichen, name, wert, an in posten)


def rechner():
    """Die Front in Originalgrösse: 1600 breit, das Feld 1600 × 480."""
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;
  flex-direction:column;align-items:center;justify-content:space-between;
  padding:64px 0 58px">
  <div class="gravur" style="font-size:19px">Musiklib</div>
  {_feld(g, 1600, 480)}
  <div class="gravur" style="font-size:15px">Anzeigefeld 1600 × 480</div>
</div>'''
    return _css(g), body


def telefon():
    """Dasselbe Feld im selben Verhältnis (1080 × 324), darunter die Schlange."""
    g = .675
    body = f'''<div style="position:absolute;inset:0;display:flex;
  flex-direction:column;padding:56px 0 60px">
  <div class="gravur" style="font-size:17px;padding-bottom:38px">Musiklib</div>
  {_feld(g, 1080, 324)}
  <div style="flex:1;min-height:0;display:flex;flex-direction:column;
    padding:0 56px">
    <div class="kap" style="font-size:18px;padding:52px 0 10px">Warteschlange</div>
    {_liste(g, 32, 24)}
    <div class="kap" style="font-size:18px;padding:44px 0 10px">Quellen</div>
    {_quellen(g)}
    <div style="margin-top:auto;display:flex;align-items:center;
      justify-content:space-between">
      <span class="kap" style="font-size:17px">Klimaxfront</span>
      <span class="kap" style="font-size:17px">Anzeigefeld 1080 × 324</span>
    </div>
  </div>
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('60', 'Klimaxfront', art, css, body)
