# -*- coding: utf-8 -*-
"""44 Gerätezeile — nach dem Display des Linn Selekt DSM (23.43.04 / 23.43.13).

Zwei Fotos, ein Entwurf: dasselbe Display einmal schwarz, einmal silbern. Es ist
das Kargste im ganzen Satz — Titel und Interpret mittig, eine Haarlinie, links
die Lautstärke als Zahl, rechts ein Dreieck, unten rechts der Schriftzug. Kein
Cover, keine runden Tasten, kein Rahmen. Übertragen: das iPhone bekommt die
schwarze Fassung, der Rechner die silberne — so bleiben beide Fotos erhalten.
"""
from werkzeug import A, biblio, laut, nexti, prev, schreibe, tri, SANS, MONO


def _css(g, dunkel):
    tinte = '#f2f2f2' if dunkel else '#3a3a3c'
    stumm = 'rgba(242,242,242,.62)' if dunkel else 'rgba(58,58,60,.62)'
    leise = 'rgba(242,242,242,.30)' if dunkel else 'rgba(58,58,60,.28)'
    grund = ('linear-gradient(105deg,#000 0%,#000 38%,#2a2a2c 62%,#0a0a0b 100%)'
             if dunkel else
             'linear-gradient(105deg,#9d9d9f 0%,#c9c9cb 34%,#a8a8aa 62%,#8e8e90 100%)')
    return f'''
.stage{{background:{grund};font-family:{SANS};color:{tinte}}}
.titel{{font-weight:400;letter-spacing:-.01em;text-align:center}}
.interpret{{color:{stumm};text-align:center;font-weight:300}}
.haar{{position:relative;height:1px;background:{leise}}}
.haar i{{position:absolute;left:0;top:0;bottom:0;background:{tinte}}}
.fuss{{display:flex;align-items:center;justify-content:space-between}}
.laut{{display:flex;align-items:center;color:{stumm};font-variant-numeric:tabular-nums}}
.wort{{text-transform:uppercase;color:{leise};font-weight:600}}
.bib{{display:inline-flex;align-items:center;color:{stumm};text-transform:uppercase}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{stumm};
  font-variant-numeric:tabular-nums}}
'''


def _zeile(g, dunkel, titel_px, interpret_px, klein_px, wort_spacing):
    tinte = '#f2f2f2' if dunkel else '#3a3a3c'
    stumm = 'rgba(242,242,242,.62)' if dunkel else 'rgba(58,58,60,.62)'
    return f'''<div class="titel" style="font-size:{titel_px}px">{A['titel']}</div>
  <div class="interpret" style="font-size:{interpret_px}px;margin-top:{int(10 * g)}px">
    {A['interpret']}</div>

  <div class="haar" style="margin-top:{int(46 * g)}px">
    <i style="width:{A['frac'] * 100:.0f}%"></i></div>
  <div class="zeiten" style="font-size:{klein_px * .86:.0f}px;margin-top:{int(14 * g)}px">
    <span>{A['pos']}</span><span>{A['dauer']}</span></div>

  <div class="fuss" style="margin-top:{int(22 * g)}px">
    <span class="laut" style="gap:{int(12 * g)}px;font-size:{klein_px}px">
      {laut(int(klein_px * 1.15), stumm)}60</span>
    <span style="display:flex;align-items:center;gap:{int(40 * g)}px">
      {prev(int(klein_px * 1.05), stumm)}
      {tri(int(klein_px * 1.35), tinte)}
      {nexti(int(klein_px * 1.05), stumm)}
    </span>
    <span class="wort" style="font-size:{klein_px * .62:.0f}px;
      letter-spacing:{wort_spacing}px">Musiklib</span>
  </div>'''


def _bib(g, schrift, dunkel):
    stumm = 'rgba(242,242,242,.62)' if dunkel else 'rgba(58,58,60,.62)'
    return (f'<span class="bib" style="gap:{int(12 * g)}px;font-size:{schrift}px;'
            f'letter-spacing:{4 * g:.1f}px">{biblio(int(schrift * 1.4), stumm)}'
            f'Sammlung · {A["sammlung"]}</span>')


def telefon():
    """Schwarze Fassung, wie das erste der beiden Fotos."""
    g = 1.0
    css = _css(g, dunkel=True)
    body = f'''<div style="position:absolute;inset:0;padding:150px 80px 130px;
  display:flex;flex-direction:column">
  <div style="display:flex;justify-content:center">{_bib(g, 21, True)}</div>
  <div style="margin-top:auto;margin-bottom:auto;width:100%">
    {_zeile(g, True, 74, 38, 30, 9)}
  </div>
</div>'''
    return css, body


def rechner():
    """Silberne Fassung, wie das zweite Foto — dieselbe Zeile, anderer Ton."""
    g = .80
    css = _css(g, dunkel=False)
    body = f'''<div style="position:absolute;inset:0;padding:74px 150px;
  display:flex;flex-direction:column">
  <div style="display:flex;justify-content:center">{_bib(g, 16, False)}</div>
  <div style="margin-top:auto;margin-bottom:auto;width:100%">
    {_zeile(g, False, 62, 32, 24, 8)}
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('44', 'Geraetezeile', art, css, body)
