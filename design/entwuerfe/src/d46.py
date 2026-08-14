# -*- coding: utf-8 -*-
"""46 Malerblatt — nach dem gemalten Stillleben (23.54.59).

Die Vorlage sieht aus wie mit dem Spachtel gemalt: eine schwarze Schallplatte
mit blaugrünem Label, zwei Kassetten in Orange und Türkis, alles auf
beschriebenem Papier, mit sichtbarem Pinselzug und harten Schlagschatten.
Übertragen: Papier mit Handschrift als Grund, die Objekte als Stillleben,
und der Fortschritt als ein Strich, der aussieht wie mit der Hand gezogen.
"""
import math

from werkzeug import (A, biblio, kassette, mischen, nexti, platte, prev, schreibe,
                      tri, wiederholen, SANS, MONO)

PAPIER = '#e6e1d4'
TINTE = '#22201c'
STUMM = '#6f6a5e'
ORANGE = '#d95f2e'
TUERKIS = '#3f8f96'


def _handschrift(breite, hoehe, zeilen, saat=2):
    """Beschriebenes Papier: kurze, unregelmässige Striche als Textzeilen."""
    stk = []
    for z in range(zeilen):
        y = (z + .5) * (hoehe / zeilen)
        x = 0.0
        w = 0
        while x < breite * .94 and w < 40:
            laenge = (18 + abs(math.sin(z * 1.7 + w * .9 + saat)) * 62)
            stk.append(f'<path d="M{x:.0f} {y:.1f} q{laenge * .5:.0f} '
                       f'{-2.5 if w % 2 else 2.5} {laenge:.0f} 0" fill="none" '
                       f'stroke="#7d7566" stroke-width="2.1" stroke-linecap="round" '
                       f'opacity=".38"/>')
            x += laenge + 9 + abs(math.cos(z * 2.3 + w)) * 12
            w += 1
    return (f'<svg viewBox="0 0 {breite} {hoehe}" width="{breite}" height="{hoehe}" '
            f'preserveAspectRatio="none">{"".join(stk)}</svg>')


def _css(g):
    return f'''
.stage{{background:{PAPIER};font-family:{SANS};color:{TINTE}}}
.schrift{{position:absolute;inset:0;pointer-events:none}}
.schrift svg{{width:100%;height:100%;display:block}}

/* Pinselzug: zwei sehr weiche Lagen, die das Papier ungleichmäßig machen */
.zug{{position:absolute;inset:0;pointer-events:none;opacity:.55;
  background:
    radial-gradient(60% 40% at 22% 18%, rgba(255,252,244,.85) 0%, rgba(255,252,244,0) 60%),
    radial-gradient(50% 34% at 78% 74%, rgba(120,110,92,.22) 0%, rgba(120,110,92,0) 62%)}}

.objekt{{filter:drop-shadow({10 * g:.0f}px {16 * g:.0f}px {12 * g:.0f}px rgba(40,34,26,.45))}}

/* Der Fortschritt ist ein gezogener Strich, kein Balken */
.strich{{position:relative;height:{10 * g:.0f}px}}
.strich .grund{{position:absolute;inset:0;border-radius:{5 * g:.0f}px;
  background:rgba(34,32,28,.16)}}
.strich i{{position:absolute;left:0;top:0;bottom:0;border-radius:{5 * g:.0f}px;
  background:linear-gradient(90deg,{ORANGE},#e07a3c)}}
.strich b{{position:absolute;top:50%;transform:translate(-50%,-50%) rotate(-8deg);
  background:{TUERKIS};border-radius:{3 * g:.0f}px}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{STUMM};
  font-variant-numeric:tabular-nums}}

.taste{{flex-shrink:0;border-radius:50%;display:flex;align-items:center;justify-content:center;
  background:rgba(255,253,246,.72);
  box-shadow:{4 * g:.0f}px {6 * g:.0f}px {10 * g:.0f}px rgba(40,34,26,.30)}}
.taste.gross{{background:{ORANGE};
  box-shadow:{6 * g:.0f}px {9 * g:.0f}px {16 * g:.0f}px rgba(150,60,20,.45)}}
.bib{{display:inline-flex;align-items:center;border-radius:999px;
  background:rgba(255,253,246,.78);text-transform:uppercase;
  box-shadow:{4 * g:.0f}px {6 * g:.0f}px {12 * g:.0f}px rgba(40,34,26,.28)}}
'''


def _stillleben(g, breite):
    """Platte oben links, zwei Kassetten darunter — leicht gedreht wie hingelegt."""
    p = breite * .60
    k1 = breite * .58
    k2 = breite * .44
    return f'''<div style="position:relative;width:{breite:.0f}px;height:{breite * .92:.0f}px">
  <div class="objekt" style="position:absolute;left:0;top:0;transform:rotate(-3deg)">
    {platte(p, TUERKIS, rille='#2a2a2c', grund='#131315')}</div>
  <div class="objekt" style="position:absolute;right:{breite * .02:.0f}px;
    top:{breite * .20:.0f}px;transform:rotate(-16deg)">
    {kassette(k2, k2 * .62, '#2f3336', ORANGE, etikett='#e8e3d6')}</div>
  <div class="objekt" style="position:absolute;left:{breite * .12:.0f}px;
    bottom:0;transform:rotate(9deg)">
    {kassette(k1, k1 * .62, TUERKIS, ORANGE, etikett='#f2eee2')}</div>
</div>'''


def _transport(g, klein, gross_, luecke):
    return (f'<div style="display:flex;align-items:center;justify-content:center;gap:{luecke}px">'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{mischen(int(klein * .40), STUMM)}</div>'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{prev(int(klein * .42), TINTE)}</div>'
            f'<div class="taste gross" style="width:{gross_}px;height:{gross_}px">'
            f'{tri(int(gross_ * .40), "#fffdf6")}</div>'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{nexti(int(klein * .42), TINTE)}</div>'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{wiederholen(int(klein * .40), STUMM)}</div></div>')


def _bib(g, schrift, hoehe):
    return (f'<span class="bib" style="height:{hoehe}px;padding:0 {int(28 * g)}px;'
            f'gap:{int(14 * g)}px;font-size:{schrift}px;letter-spacing:{3.2 * g:.1f}px">'
            f'{biblio(int(schrift * 1.3), ORANGE)}Sammlung · {A["sammlung"]}</span>')


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div class="schrift">{_handschrift(1080, 2340, 30)}</div>
<div class="zug"></div>
<div style="position:absolute;inset:0;padding:120px 66px 96px;display:flex;flex-direction:column">
  <div style="display:flex;justify-content:flex-end">{_bib(g, 21, 66)}</div>

  <div style="display:flex;justify-content:center;margin:auto 0">{_stillleben(g, 940)}</div>

  <div style="margin-top:auto">
    <div style="font-size:62px;font-weight:800;letter-spacing:-.02em">{A['titel']}</div>
    <div style="font-size:31px;color:{STUMM};margin-top:12px">
      {A['interpret']} · {A['album']} · {A['jahr']}</div>

    <div class="strich" style="margin-top:44px"><span class="grund"></span>
      <i style="width:{A['frac'] * 100:.0f}%"></i>
      <b style="left:{A['frac'] * 100:.0f}%;width:34px;height:34px"></b></div>
    <div class="zeiten" style="font-size:25px;margin-top:20px">
      <span>{A['pos']}</span><span>{A['dauer']}</span></div>

    <div style="margin-top:44px">{_transport(g, 100, 146, 40)}</div>
  </div>
</div>'''
    return css, body


def rechner():
    g = .72
    css = _css(g)
    body = f'''<div class="schrift">{_handschrift(1600, 1000, 20, saat=5)}</div>
<div class="zug"></div>
<div style="position:absolute;inset:0;padding:58px 76px;display:flex;gap:64px;align-items:center">
  <div style="flex-shrink:0">{_stillleben(g, 640)}</div>

  <div style="flex:1;min-width:0;align-self:stretch;display:flex;flex-direction:column">
    <div style="display:flex;justify-content:flex-end">{_bib(g, 15, 48)}</div>
    <div style="margin-top:auto">
      <div style="font-size:60px;font-weight:800;letter-spacing:-.02em">{A['titel']}</div>
      <div style="font-size:24px;color:{STUMM};margin-top:10px">
        {A['interpret']} · {A['album']} · {A['jahr']}</div>
      <div class="strich" style="margin-top:34px"><span class="grund"></span>
        <i style="width:{A['frac'] * 100:.0f}%"></i>
        <b style="left:{A['frac'] * 100:.0f}%;width:26px;height:26px"></b></div>
      <div class="zeiten" style="font-size:19px;margin-top:14px">
        <span>{A['pos']}</span><span>{A['dauer']}</span></div>
      <div style="margin-top:32px;display:flex">{_transport(g, 68, 100, 28)}</div>
    </div>
    <div style="margin-top:auto"></div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('46', 'Malerblatt', art, css, body)
