# -*- coding: utf-8 -*-
"""57 Mischpult — nach dem schwarzen Bedienpult mit Fadern und Pads (09.12.56).

Die Vorlage ist ein Tischgerät: links ein Bildschirm mit Cover, einer riesigen
angeschnittenen Nummer und einem Feld kleiner Kacheln, rechts fünf Schieber,
weisse Sprungtasten, ein breites oranges Pad und ein Haufen dunkler Pads.
Übertragen: die Kacheln sind die Sammlung, das orange Pad ist die Wiedergabe,
und die Schieber bleiben Schieber — sie sind der Klang, nicht die Zeit. Für die
Zeit ist ein sechster Schieber dazugekommen, der quer liegt: dieselbe Bauform,
um 90 Grad gedreht.
"""
from werkzeug import A, biblio, cover, nexti, prev, pausei, schreibe, MONO, SANS

PULT = '#1b1c1e'
PULT_H = '#303338'
SCHIRM = '#0b0c0d'
PAD = '#232629'
ORANGE = '#e86a1e'
WEISS = '#f2f3f4'
STUMM = 'rgba(242,243,244,.55)'
LEISE = 'rgba(242,243,244,.20)'

BAENDER = [('60', .30), ('250', .62), ('1k', .48), ('4k', .70), ('12k', .38)]


def _css(g):
    return f'''
.stage{{background:linear-gradient(160deg,#e9eaec 0%,#c9ccd0 54%,#dfe1e4 100%);
  font-family:{SANS};color:{WEISS}}}

.pult{{position:relative;border-radius:{20 * g:.0f}px;
  background:linear-gradient(168deg,{PULT_H} 0%,{PULT} 18%,#0f1012 100%);
  box-shadow:0 {30 * g:.0f}px {70 * g:.0f}px rgba(30,34,40,.45),
             inset 0 {2 * g:.0f}px 0 rgba(255,255,255,.14)}}

.schirm{{position:relative;overflow:hidden;background:{SCHIRM};
  border-radius:{12 * g:.0f}px;
  box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(255,255,255,.07)}}
.nr{{position:absolute;font-weight:800;color:{ORANGE};line-height:.78;
  letter-spacing:-.05em;opacity:.9}}

/* Die Kacheln sind die Sammlung — quadratisch, mit einem Namen darunter */
.kacheln{{display:grid}}
.kach{{border-radius:{7 * g:.0f}px;background:{PAD};display:flex;
  align-items:flex-end;padding:{7 * g:.0f}px;overflow:hidden;
  box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(255,255,255,.06)}}
.kach span{{font-size:inherit;color:{STUMM};line-height:1.15;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap;width:100%}}
.kach.bib{{background:{ORANGE}}}
.kach.bib span{{color:#1a0d03;font-weight:700}}

/* Schieber: Nut, Kappe, Beschriftung — senkrecht wie waagerecht dieselbe Form */
.nut{{position:relative;background:#0c0d0e;border-radius:999px;
  box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(255,255,255,.08)}}
.kappe{{position:absolute;border-radius:{4 * g:.0f}px;
  background:linear-gradient(180deg,#4b4f54 0%,#1e2124 60%,#101214 100%);
  box-shadow:0 {3 * g:.0f}px {7 * g:.0f}px rgba(0,0,0,.55)}}
.band{{font-family:{MONO};color:{LEISE};text-align:center}}

.pad{{border-radius:{9 * g:.0f}px;background:{PAD};display:flex;
  align-items:center;justify-content:center;
  box-shadow:inset 0 {1 * g:.0f}px 0 rgba(255,255,255,.10),
             0 {3 * g:.0f}px {7 * g:.0f}px rgba(0,0,0,.4)}}
.pad.weiss{{background:#eef0f1}}
.pad.orange{{background:{ORANGE}}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{STUMM};
  font-variant-numeric:tabular-nums}}
'''


KACHELN = ['A Love Supreme', 'Speak No Evil', 'Maiden Voyage', 'Blue Train',
           'Moanin’', 'Waltz for Debby', 'Idle Moments', 'Page One']


def _schirm(g, pad, cover_px, nr_px, klein, kachel_px, kachel_s, spalten):
    kacheln = ''.join(
        f'<div class="kach" style="height:{kachel_px}px;font-size:{kachel_s}px">'
        f'<span>{n}</span></div>' for n in KACHELN[:spalten * 2 - 1])
    return f'''<div class="schirm" style="padding:{pad}">
  <span class="nr" style="right:{int(-14 * g)}px;top:{int(-10 * g)}px;
    font-size:{nr_px}px">{A['tracks'][A['laeuft']][0]}</span>
  <div style="position:relative;display:flex;gap:{int(22 * g)}px;align-items:flex-end">
    {cover(cover_px, int(cover_px * .03), '#2f6f8f', '#123044')}
    <div style="min-width:0">
      <div style="font-size:{klein * 1.5:.0f}px;font-weight:600;overflow:hidden;
        white-space:nowrap;text-overflow:ellipsis">{A['titel']}</div>
      <div style="font-size:{klein}px;color:{STUMM};margin-top:{int(6 * g)}px">
        {A['interpret']}<br>{A['album']} · {A['jahr']}</div>
    </div>
  </div>

  <div class="kacheln" style="grid-template-columns:repeat({spalten},1fr);
    gap:{int(9 * g)}px;margin-top:{int(24 * g)}px;position:relative">
    <div class="kach bib" style="height:{kachel_px}px;font-size:{kachel_s}px">
      <span>Sammlung · {A['sammlung']}</span></div>
    {kacheln}
  </div>
</div>'''


def _schieber(g, hoehe, breite, kappe_h, schrift):
    stk = []
    for name, wert in BAENDER:
        stk.append(f'''<div style="flex:1;display:flex;flex-direction:column;
      align-items:center;gap:{int(10 * g)}px">
      <div class="nut" style="width:{breite}px;height:{hoehe}px">
        <span class="kappe" style="left:{-breite:.0f}px;width:{breite * 3:.0f}px;
          height:{kappe_h}px;bottom:calc({wert * 100:.0f}% - {kappe_h / 2:.0f}px)"></span>
      </div>
      <span class="band" style="font-size:{schrift}px">{name}</span></div>''')
    return (f'<div style="display:flex;width:100%;gap:{int(30 * g)}px;'
            f'align-items:flex-end">{"".join(stk)}</div>')


def _zeitschieber(g, hoehe, kappe_b):
    """Derselbe Schieber, quer gelegt: das ist die Spulfläche."""
    return (f'<div class="nut" style="position:relative;height:{hoehe}px">'
            f'<span class="kappe" style="top:{-hoehe:.0f}px;height:{hoehe * 3:.0f}px;'
            f'width:{kappe_b}px;left:calc({A["frac"] * 100:.0f}% - '
            f'{kappe_b / 2:.0f}px)"></span></div>')


def _pads(g, hoehe, spiel_b, klein_b, luecke, zeichen):
    return (f'<div style="display:flex;gap:{luecke}px">'
            f'<div class="pad weiss" style="width:{klein_b}px;height:{hoehe}px">'
            f'{prev(zeichen, "#26292c")}</div>'
            f'<div class="pad orange" style="width:{spiel_b}px;height:{hoehe}px">'
            f'{pausei(int(zeichen * 1.2), "#1a0d03")}</div>'
            f'<div class="pad weiss" style="width:{klein_b}px;height:{hoehe}px">'
            f'{nexti(zeichen, "#26292c")}</div>'
            f'<div class="pad" style="width:{klein_b}px;height:{hoehe}px">'
            f'{biblio(zeichen, WEISS)}</div></div>')


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:74px 46px">
  <div class="pult" style="width:988px;padding:44px 42px 52px">
    {_schirm(g, '38px 36px 40px', 210, 240, 27, 108, 20, 3)}

    <div class="zeiten" style="font-size:24px;margin-top:38px">
      <span>{A['pos']}</span><span>{A['dauer']}</span></div>
    <div style="margin-top:14px">{_zeitschieber(g, 12, 46)}</div>

    <div style="display:flex;align-items:flex-end;justify-content:space-between;
      margin-top:56px">
      {_schieber(g, 250, 12, 34, 20)}
    </div>

    <div style="margin-top:52px">{_pads(g, 128, 300, 156, 18, 46)}</div>
  </div>
</div>'''
    return css, body


def rechner():
    g = .80
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:52px 62px">
  <div class="pult" style="width:1476px;padding:38px 40px;display:flex;gap:44px">
    <div style="width:600px;flex-shrink:0">
      {_schirm(g, '30px 30px 32px', 168, 196, 21, 84, 15, 3)}
      <div class="zeiten" style="font-size:18px;margin-top:24px">
        <span>{A['pos']}</span><span>{A['dauer']}</span></div>
      <div style="margin-top:10px">{_zeitschieber(g, 10, 38)}</div>
    </div>

    <div style="flex:1;min-width:0;display:flex;flex-direction:column;
      justify-content:space-between">
      <div style="display:flex;justify-content:center">
        {_schieber(g, 262, 10, 28, 16)}</div>
      <div style="margin-top:34px;display:flex;justify-content:center">
        {_pads(g, 104, 262, 128, 15, 38)}</div>
    </div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('57', 'Mischpult', art, css, body)
