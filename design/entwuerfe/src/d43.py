# -*- coding: utf-8 -*-
"""43 Sonnenglas — nach der Glaskarte vor dem Sonnenuntergang (23.38.31).

Die Vorlage legt eine Karte aus Milchglas über ein Foto: oben glüht der Himmel,
unten steht der Horizont schwarz. Durch das Glas scheint beides gedämpft
hindurch. Die Zeiten stehen als „verstrichen" und „−verbleibend", die
Zufallstaste ist gelb, alles andere weiss. Übertragen: das Cover liefert die
Farbe des Himmels, die Karte bleibt Glas.
"""
from werkzeug import (A, biblio, mischen, nexti, pausei, prev, schreibe,
                      wiederholen, SANS, MONO)

TINTE = '#ffffff'
STUMM = 'rgba(255,255,255,.68)'
GELB = '#f2d64b'


def _css(g):
    return f'''
.stage{{background:
  linear-gradient(180deg, #f0913c 0%, #d9662c 26%, #7a3418 48%, #23150e 62%, #0b0906 100%);
  font-family:{SANS};color:{TINTE}}}

/* Der Horizont: eine dunkle Kante mit weichem Ansatz, kein Foto */
.horizont{{position:absolute;left:0;right:0;background:#0d0906}}
.huegel{{position:absolute;border-radius:50%;background:#140d08}}

.glas{{position:relative;background:rgba(255,255,255,.13);
  border:1px solid rgba(255,255,255,.24);backdrop-filter:blur({26 * g:.0f}px);
  -webkit-backdrop-filter:blur({26 * g:.0f}px);
  box-shadow:0 {26 * g:.0f}px {60 * g:.0f}px rgba(0,0,0,.38),
    inset 0 1px 0 rgba(255,255,255,.34)}}

.linie{{position:relative;border-radius:999px;background:rgba(255,255,255,.34)}}
.linie i{{position:absolute;left:0;top:0;bottom:0;border-radius:999px;background:{TINTE}}}
.linie b{{position:absolute;top:50%;transform:translate(-50%,-50%);border-radius:50%;
  background:{TINTE};box-shadow:0 {2 * g:.0f}px {6 * g:.0f}px rgba(0,0,0,.35)}}
.zeiten{{display:flex;justify-content:space-between;font-variant-numeric:tabular-nums;
  font-family:{MONO}}}
.tasten{{display:flex;align-items:center;justify-content:space-between}}
.bib{{display:inline-flex;align-items:center;border-radius:999px;
  background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.26);
  backdrop-filter:blur({18 * g:.0f}px);text-transform:uppercase}}
'''


def _himmelcover(size, radius):
    """Das Cover ist ein Ausschnitt desselben Himmels — Sonne über dunkler Kante."""
    kn = int(size)
    return f'''<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">
<defs><linearGradient id="hg{kn}" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#f6a24a"/><stop offset="52%" stop-color="#dd6a2c"/>
<stop offset="100%" stop-color="#8a3a1a"/></linearGradient></defs>
<rect x="0" y="0" width="{size}" height="{size}" rx="{radius}" fill="url(#hg{kn})"/>
<circle cx="{size * .50:.1f}" cy="{size * .62:.1f}" r="{size * .085:.1f}" fill="#ffe6b0"/>
<path d="M0 {size * .70:.1f} Q {size * .30:.1f} {size * .58:.1f} {size * .55:.1f} {size * .68:.1f}
  T {size} {size * .63:.1f} L{size} {size} L0 {size} Z" fill="#1b120c"/>
</svg>'''


def _transport(g, size, luecke):
    return (f'<div class="tasten" style="gap:{luecke}px">'
            f'{mischen(int(size * .92), GELB, 2.6 * g)}'
            f'{prev(size, TINTE)}'
            f'{pausei(int(size * 1.05), TINTE)}'
            f'{nexti(size, TINTE)}'
            f'{wiederholen(int(size * .92), TINTE, 2.4 * g)}</div>')


def _bib(g, schrift, hoehe):
    return (f'<span class="bib" style="height:{hoehe}px;padding:0 {int(26 * g)}px;'
            f'gap:{int(14 * g)}px;font-size:{schrift}px;letter-spacing:{3.4 * g:.1f}px">'
            f'{biblio(int(schrift * 1.3), TINTE)}Sammlung · {A["sammlung"]}</span>')


def _karte(g, breite, rund, cover_px, titel_px, luecke_oben):
    return f'''<div class="glas" style="width:{breite}px;border-radius:{rund}px;
  padding:{int(38 * g)}px {int(40 * g)}px {int(34 * g)}px">
  <div style="display:flex;align-items:center;gap:{int(30 * g)}px">
    <div style="line-height:0;flex-shrink:0">{_himmelcover(cover_px, cover_px * .22)}</div>
    <div style="flex:1;min-width:0">
      <div style="font-size:{titel_px}px;font-weight:700;overflow:hidden;
        white-space:nowrap;text-overflow:ellipsis">{A['titel']}</div>
      <div style="font-size:{titel_px * .62:.0f}px;color:{STUMM};margin-top:{int(8 * g)}px;
        overflow:hidden;white-space:nowrap;text-overflow:ellipsis">{A['interpret']}</div>
    </div>
  </div>
  <div class="zeiten" style="font-size:{titel_px * .48:.0f}px;margin-top:{luecke_oben}px">
    <span>{A['pos']}</span><span>{A['rest']}</span></div>
  <div class="linie" style="height:{int(7 * g)}px;margin-top:{int(16 * g)}px">
    <i style="width:{A['frac'] * 100:.0f}%"></i>
    <b style="left:{A['frac'] * 100:.0f}%;width:{int(22 * g)}px;height:{int(22 * g)}px"></b></div>
  <div style="margin-top:{int(36 * g)}px">{_transport(g, int(46 * g), int(10 * g))}</div>
</div>'''


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div class="horizont" style="top:1520px;bottom:0"></div>
<div class="huegel" style="left:-260px;top:1360px;width:1000px;height:420px"></div>
<div class="huegel" style="right:-200px;top:1430px;width:820px;height:360px"></div>
<div style="position:absolute;inset:0;padding:150px 62px 130px;display:flex;
  flex-direction:column;align-items:center">
  {_bib(g, 21, 68)}
  <div style="margin-top:auto;margin-bottom:auto;width:100%;display:flex;justify-content:center">
    {_karte(g, 956, 52, 220, 54, 40)}
  </div>
</div>'''
    return css, body


def rechner():
    g = .74
    css = _css(g)
    body = f'''<div class="horizont" style="top:640px;bottom:0"></div>
<div class="huegel" style="left:-300px;top:520px;width:1100px;height:340px"></div>
<div class="huegel" style="right:-260px;top:580px;width:960px;height:300px"></div>
<div style="position:absolute;inset:0;padding:56px 74px;display:flex;
  flex-direction:column;align-items:center">
  <div style="align-self:flex-start">{_bib(g, 15, 48)}</div>
  <div style="margin-top:auto;margin-bottom:auto">
    {_karte(g, 900, 40, 168, 44, 30)}
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('43', 'Sonnenglas', art, css, body)
