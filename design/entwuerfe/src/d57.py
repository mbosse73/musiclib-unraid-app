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
/* Das Pult füllt die Bühne — man sitzt davor, nicht daneben */
.stage{{background:linear-gradient(168deg,{PULT_H} 0%,{PULT} 18%,#0f1012 100%);
  font-family:{SANS};color:{WEISS}}}
.stage::before{{content:"";position:absolute;inset:0;pointer-events:none;
  box-shadow:inset 0 {2 * g:.0f}px 0 rgba(255,255,255,.14)}}
.pult{{position:absolute;inset:0;display:flex}}

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


def _schirm(g, pad, cover_px, nr_px, klein, kachel_px, kachel_s, spalten, reihen=2):
    kacheln = ''.join(
        f'<div class="kach" style="height:{kachel_px}px;font-size:{kachel_s}px">'
        f'<span>{n}</span></div>' for n in KACHELN[:spalten * reihen - 1])
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
    body = f'''<div class="pult" style="flex-direction:column;padding:56px 46px 64px">
  {_schirm(g, '44px 40px 46px', 264, 300, 29, 150, 22, 3, 3)}

  <div class="zeiten" style="font-size:25px;margin-top:auto;padding-top:56px">
    <span>{A['pos']}</span><span>{A['dauer']}</span></div>
  <div style="margin-top:14px">{_zeitschieber(g, 12, 48)}</div>

  <div style="display:flex;align-items:flex-end;margin-top:56px">
    {_schieber(g, 800, 12, 36, 21)}
  </div>

  <div style="margin-top:60px">{_pads(g, 152, 320, 168, 20, 50)}</div>
</div>'''
    return css, body


def rechner():
    g = .80
    css = _css(g)
    body = f'''<div class="pult" style="padding:44px 48px;gap:48px">
  <div style="width:700px;flex-shrink:0;display:flex;flex-direction:column">
    {_schirm(g, '34px 34px 36px', 196, 230, 23, 112, 16, 3, 3)}
    <div class="zeiten" style="font-size:19px;margin-top:auto;padding-top:26px">
      <span>{A['pos']}</span><span>{A['dauer']}</span></div>
    <div style="margin-top:10px">{_zeitschieber(g, 10, 40)}</div>
  </div>

  <div style="flex:1;min-width:0;display:flex;flex-direction:column">
    <div style="display:flex;flex:1;min-height:0;align-items:flex-end">
      {_schieber(g, 330, 10, 30, 17)}</div>
    <div style="margin-top:40px;display:flex;justify-content:center">
      {_pads(g, 128, 300, 148, 17, 44)}</div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('57', 'Mischpult', art, css, body)
