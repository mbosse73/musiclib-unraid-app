# -*- coding: utf-8 -*-
"""41 Sonntagsblatt — nach der Story-Seite „chill, music for sunday" (23.34.02).

Die Vorlage ist ein Blatt Graupappe, auf dem alles liegt: eine fette
Schlagzeile in drei Zeilen mit einem orangefarbenen Wort, darunter ein
schmaler Spieler mit Haarlinie und fünf Tasten, und ganz unten die Objekte —
Kassette und Hülle, mit einem weissen Kontur­strich umrissen wie ausgeschnitten.
Übertragen: die Schlagzeile nennt das Album, der Kontur­strich bleibt.
"""
from werkzeug import (A, biblio, kassette, mischen, nexti, pausei, prev, schreibe,
                      wiederholen, SANS, MONO)

PAPPE = '#d7d3ca'
TINTE = '#26262a'
STUMM = '#7d7b76'
ORANGE = '#f08a2c'


def _css(g):
    return f'''
.stage{{background:
  radial-gradient(120% 90% at 30% 10%, #e0dcd3 0%, {PAPPE} 55%, #c9c5bc 100%);
  font-family:{SANS};color:{TINTE}}}

/* Die Pappe hat Korn — zwei sehr feine Streifenlagen über Kreuz */
.korn{{position:absolute;inset:0;pointer-events:none;opacity:.5;
  background:
    repeating-linear-gradient(58deg, rgba(0,0,0,.035) 0 1px, transparent 1px 4px),
    repeating-linear-gradient(-32deg, rgba(255,255,255,.05) 0 1px, transparent 1px 3px)}}

.kopfzeile{{display:flex;align-items:flex-start;justify-content:space-between}}
.marke{{display:flex;align-items:center;color:{STUMM};text-transform:uppercase;
  letter-spacing:{2.5 * g:.1f}px;line-height:1.25}}
.datum{{text-align:center;line-height:.95}}
.datum b{{display:block;font-weight:800}}
.datum span{{display:block;color:{STUMM}}}

/* Schlagzeile: eng gesetzt, drei Zeilen, die dritte orange */
.schlag{{font-weight:800;letter-spacing:-.035em;line-height:.88;text-align:center}}
.schlag .zwei{{display:block}}
.schlag .drei{{display:block;color:{ORANGE}}}

.linie{{position:relative;background:rgba(38,38,42,.28)}}
.linie i{{position:absolute;left:0;top:0;bottom:0;background:{TINTE}}}
.linie b{{position:absolute;top:50%;transform:translate(-50%,-50%);border-radius:50%;
  background:{TINTE}}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{STUMM};
  font-variant-numeric:tabular-nums}}
.tasten{{display:flex;align-items:center;justify-content:center}}
.ring{{border-radius:50%;border:{2.5 * g:.0f}px solid {TINTE};display:flex;
  align-items:center;justify-content:center}}

/* Die Objekte tragen den weissen Ausschneidestrich der Vorlage */
.objekt{{filter:drop-shadow(0 {14 * g:.0f}px {26 * g:.0f}px rgba(60,55,45,.32))}}
.objekt > div{{border-radius:{10 * g:.0f}px;
  box-shadow:0 0 0 {5 * g:.0f}px #fdfcfa}}
.bib{{display:inline-flex;align-items:center;border-radius:999px;
  border:{2 * g:.0f}px solid rgba(38,38,42,.35);text-transform:uppercase}}
.fuss{{text-align:center;color:{STUMM}}}
'''


def _kopf(g, schrift, tag, monat):
    return (f'<div class="kopfzeile">'
            f'<span class="marke" style="font-size:{schrift}px;gap:{int(10 * g)}px">'
            f'{biblio(int(schrift * 1.6), TINTE)}<span>musiklib<br>sammlung</span></span>'
            f'<span class="datum"><b style="font-size:{schrift * 2.2:.0f}px">{tag}</b>'
            f'<span style="font-size:{schrift * .95:.0f}px">{monat}</span></span></div>')


def _spieler(g, schrift, linie_h, punkt, ring_gross, ring_klein, luecke):
    return f'''<div style="font-weight:700;font-size:{schrift}px">{A['titel']}</div>
  <div style="font-size:{schrift * .74:.0f}px;color:{STUMM};margin-top:{int(4 * g)}px">
    {A['interpret']} · {A['album']}</div>
  <div class="linie" style="height:{linie_h}px;margin-top:{int(18 * g)}px">
    <i style="width:{A['frac'] * 100:.0f}%"></i>
    <b style="left:{A['frac'] * 100:.0f}%;width:{punkt}px;height:{punkt}px"></b></div>
  <div class="zeiten" style="font-size:{schrift * .58:.0f}px;margin-top:{int(10 * g)}px">
    <span>{A['pos']}</span><span>{A['dauer']}</span></div>
  <div class="tasten" style="gap:{luecke}px;margin-top:{int(26 * g)}px">
    {mischen(int(ring_klein * .72), TINTE, 2.4 * g)}
    {prev(int(ring_klein * .78), TINTE)}
    <span class="ring" style="width:{ring_gross}px;height:{ring_gross}px">
      {pausei(int(ring_gross * .40), TINTE)}</span>
    {nexti(int(ring_klein * .78), TINTE)}
    {wiederholen(int(ring_klein * .72), TINTE, 2.4 * g)}
  </div>'''


def _objekte(g, breite):
    """Hülle und Kassette, leicht gedreht, mit weissem Konturstrich."""
    h_b = breite * .46
    k_b = breite * .52
    return f'''<div style="position:relative;width:{breite:.0f}px;height:{breite * .58:.0f}px">
  <div class="objekt" style="position:absolute;left:0;top:{breite * .03:.0f}px;
    transform:rotate(-4deg)">
    <div style="width:{h_b:.0f}px;height:{h_b * 1.12:.0f}px;overflow:hidden;
      background:linear-gradient(150deg,#2f4a3a,#16241c)">
      <div style="padding:{breite * .045:.0f}px;color:#e8e3d6;font-family:{SANS}">
        <div style="font-size:{breite * .052:.0f}px;letter-spacing:{breite * .012:.1f}px;
          font-weight:600">{A['album'].upper()}</div>
        <div style="font-size:{breite * .034:.0f}px;opacity:.75;margin-top:{breite * .012:.0f}px;
          font-style:italic">{A['interpret']}</div>
      </div>
    </div>
  </div>
  <div class="objekt" style="position:absolute;right:0;bottom:0;transform:rotate(7deg)">
    <div style="width:{k_b:.0f}px;height:{k_b * .63:.0f}px;overflow:hidden">
      {kassette(k_b, k_b * .63, '#cfd2d6', '#8d939a', etikett='#f4f2ec')}
    </div>
  </div>
</div>'''


def _bib(g, schrift, hoehe):
    return (f'<span class="bib" style="height:{hoehe}px;padding:0 {int(24 * g)}px;'
            f'gap:{int(12 * g)}px;font-size:{schrift}px;letter-spacing:{3 * g:.1f}px">'
            f'Sammlung · {A["sammlung"]} Alben</span>')


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div class="korn"></div>
<div style="position:absolute;inset:0;padding:110px 74px 84px;display:flex;
  flex-direction:column;justify-content:space-between">
  {_kopf(g, 22, '24', 'Dez')}

  <div class="schlag" style="font-size:118px">
    heute,<span class="zwei">Musik für</span><span class="drei">{A['album']}</span></div>

  <div>
    {_spieler(g, 42, 3, 20, 96, 52, 54)}
  </div>

  <div style="display:flex;justify-content:center">{_objekte(g, 900)}</div>

  <div style="display:flex;justify-content:center">{_bib(g, 21, 64)}</div>
  <div class="fuss" style="font-size:20px;margin-top:22px">musiklib · {A['jahr']}</div>
</div>'''
    return css, body


def rechner():
    g = .72
    css = _css(g)
    body = f'''<div class="korn"></div>
<div style="position:absolute;inset:0;padding:58px 78px;display:flex;gap:64px">
  <div style="flex:1;min-width:0;display:flex;flex-direction:column">
    {_kopf(g, 16, '24', 'Dez')}
    <div class="schlag" style="font-size:88px;margin-top:40px;text-align:left">
      heute,<span class="zwei">Musik für</span><span class="drei">{A['album']}</span></div>
    <div style="margin-top:44px">
      {_spieler(g, 30, 2, 14, 68, 38, 40)}
    </div>
    <div style="margin-top:auto;display:flex;align-items:center;gap:22px">
      {_bib(g, 15, 46)}
      <span class="fuss" style="font-size:15px">musiklib · {A['jahr']}</span>
    </div>
  </div>
  <div style="flex-shrink:0;display:flex;align-items:center">{_objekte(g, 600)}</div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('41', 'Sonntagsblatt', art, css, body)
