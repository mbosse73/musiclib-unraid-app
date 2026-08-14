# -*- coding: utf-8 -*-
"""45 Kassettenhaufen — nach dem Berg bunter C60-Kassetten (23.56.47).

Die Vorlage ist ein Haufen: Dutzende Kassetten in allen Farben, kreuz und quer,
bis an alle vier Ränder. Darüber liegt Bedienung — links eine dunkle Pille, rechts
eine rote Taste. Übertragen: der Haufen *ist* die Sammlung, jede Kassette ein
Album. Darüber schwebt nur, was man wirklich braucht.
"""
import math

from werkzeug import A, biblio, kassette, mischen, nexti, prev, schreibe, tri, wiederholen, SANS, MONO

TINTE = '#141416'
WEISS = '#f7f6f3'
ROT = '#e0342c'

FARBEN = [
    ('#e8613f', '#f2b33c'), ('#3f7fb8', '#e8e4d8'), ('#f2c33c', '#e8613f'),
    ('#7a6fb0', '#e8e4d8'), ('#4aa89a', '#f2efe4'), ('#e05a86', '#f2c33c'),
    ('#d8d4c8', '#3f7fb8'), ('#2f4a72', '#e8613f'), ('#c9553c', '#f2efe4'),
    ('#6fae5a', '#f2c33c'), ('#8e8a84', '#e05a86'), ('#f2934a', '#2f4a72'),
]


def _css(g):
    return f'''
.stage{{background:#8f8b84;font-family:{SANS};color:{TINTE}}}
.haufen{{position:absolute;inset:0;overflow:hidden}}
.haufen > div{{position:absolute;filter:drop-shadow(0 {8 * g:.0f}px {14 * g:.0f}px rgba(0,0,0,.45))}}

/* Der Haufen wird nach unten hin abgedunkelt, damit die Leiste lesbar bleibt */
.schleier{{position:absolute;left:0;right:0;bottom:0;pointer-events:none;
  background:linear-gradient(180deg, rgba(10,10,12,0) 0%, rgba(10,10,12,.62) 55%,
    rgba(10,10,12,.86) 100%)}}

.pille{{display:inline-flex;align-items:center;border-radius:999px;
  background:rgba(18,18,20,.72);color:{WEISS};backdrop-filter:blur({14 * g:.0f}px);
  box-shadow:0 {8 * g:.0f}px {20 * g:.0f}px rgba(0,0,0,.4)}}
.knopfrot{{display:inline-flex;align-items:center;justify-content:center;
  background:{ROT};color:#fff;font-weight:700;
  box-shadow:0 {10 * g:.0f}px {24 * g:.0f}px rgba(180,35,28,.5)}}

.leiste{{position:relative;background:rgba(18,18,20,.62);
  border:1px solid rgba(255,255,255,.14);backdrop-filter:blur({22 * g:.0f}px);
  color:{WEISS}}}
.balken{{position:relative;border-radius:999px;background:rgba(255,255,255,.26)}}
.balken i{{position:absolute;left:0;top:0;bottom:0;border-radius:999px;background:{WEISS}}}
.balken b{{position:absolute;top:50%;transform:translate(-50%,-50%);border-radius:50%;
  background:{WEISS}}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};
  color:rgba(247,246,243,.66);font-variant-numeric:tabular-nums}}
.taste{{flex-shrink:0;border-radius:50%;display:flex;align-items:center;justify-content:center;
  background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.22)}}
.taste.gross{{background:{WEISS};border-color:transparent}}
'''


def _haufen(g, breite, hoehe, k_breite, spalten, zeilen, saat=3):
    """Kassetten in versetzten Reihen, jede eigen gedreht — deckt die ganze Fläche."""
    stk = []
    k_hoehe = k_breite * .62
    dx = breite / (spalten - .55)
    dy = hoehe / (zeilen - .75)
    for r in range(zeilen):
        for c in range(spalten):
            i = r * spalten + c
            w = math.sin(i * 2.4 + saat) * 26
            x = c * dx - (dx * .42 if r % 2 else 0) - k_breite * .12
            y = r * dy - k_hoehe * .18 + math.cos(i * 1.7 + saat) * (dy * .10)
            g1, g2 = FARBEN[i % len(FARBEN)]
            stk.append(f'<div style="left:{x:.0f}px;top:{y:.0f}px;'
                       f'transform:rotate({w:.1f}deg)">'
                       f'{kassette(k_breite, k_hoehe, g1, g2)}</div>')
    return f'<div class="haufen">{"".join(stk)}</div>'


def _transport(g, klein, gross_, luecke):
    return (f'<div style="display:flex;align-items:center;justify-content:center;gap:{luecke}px">'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{mischen(int(klein * .40), "rgba(247,246,243,.7)")}</div>'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{prev(int(klein * .42), WEISS)}</div>'
            f'<div class="taste gross" style="width:{gross_}px;height:{gross_}px">'
            f'{tri(int(gross_ * .40), TINTE)}</div>'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{nexti(int(klein * .42), WEISS)}</div>'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{wiederholen(int(klein * .40), "rgba(247,246,243,.7)")}</div></div>')


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''{_haufen(g, 1080, 2340, 300, 5, 9)}
<div class="schleier" style="height:900px"></div>
<div style="position:absolute;inset:0;padding:120px 54px 90px;display:flex;flex-direction:column">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <span class="pille" style="height:78px;padding:0 32px;gap:16px;font-size:29px">
      {biblio(30, '#f2b33c')}Sammlung · {A['sammlung']}</span>
    <span class="knopfrot" style="height:78px;padding:0 38px;border-radius:20px;font-size:29px">
      Merken</span>
  </div>

  <div class="leiste" style="margin-top:auto;border-radius:44px;padding:36px 40px">
    <div style="font-size:44px;font-weight:700;overflow:hidden;white-space:nowrap;
      text-overflow:ellipsis">{A['titel']}</div>
    <div style="font-size:29px;color:rgba(247,246,243,.66);margin-top:8px">
      {A['interpret']} · {A['album']}</div>
    <div class="balken" style="height:10px;margin-top:32px">
      <i style="width:{A['frac'] * 100:.0f}%"></i>
      <b style="left:{A['frac'] * 100:.0f}%;width:26px;height:26px"></b></div>
    <div class="zeiten" style="font-size:25px;margin-top:18px">
      <span>{A['pos']}</span><span>{A['dauer']}</span></div>
    <div style="margin-top:34px">{_transport(g, 96, 140, 38)}</div>
  </div>
</div>'''
    return css, body


def rechner():
    g = .72
    css = _css(g)
    body = f'''{_haufen(g, 1600, 1000, 260, 8, 5, saat=6)}
<div class="schleier" style="height:520px"></div>
<div style="position:absolute;inset:0;padding:56px 70px;display:flex;flex-direction:column">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <span class="pille" style="height:58px;padding:0 26px;gap:14px;font-size:21px">
      {biblio(23, '#f2b33c')}Sammlung · {A['sammlung']} Alben</span>
    <span class="knopfrot" style="height:58px;padding:0 30px;border-radius:15px;font-size:21px">
      Merken</span>
  </div>

  <div class="leiste" style="margin-top:auto;border-radius:30px;padding:28px 34px;
    display:flex;align-items:center;gap:40px">
    <div style="flex:1;min-width:0">
      <div style="font-size:36px;font-weight:700;overflow:hidden;white-space:nowrap;
        text-overflow:ellipsis">{A['titel']}</div>
      <div style="font-size:21px;color:rgba(247,246,243,.66);margin-top:6px">
        {A['interpret']} · {A['album']} · {A['jahr']}</div>
      <div class="balken" style="height:7px;margin-top:20px">
        <i style="width:{A['frac'] * 100:.0f}%"></i>
        <b style="left:{A['frac'] * 100:.0f}%;width:18px;height:18px"></b></div>
      <div class="zeiten" style="font-size:17px;margin-top:12px">
        <span>{A['pos']}</span><span>{A['dauer']}</span></div>
    </div>
    <div style="flex-shrink:0">{_transport(g, 62, 92, 22)}</div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('45', 'Kassettenhaufen', art, css, body)
