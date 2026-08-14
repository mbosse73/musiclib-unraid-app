# -*- coding: utf-8 -*-
"""43 Sonnenglas — nach der Glaskarte vor dem Sonnenuntergang (23.38.31).

Die Vorlage legt eine Karte aus Milchglas über ein Foto: oben glüht der Himmel,
unten steht der Horizont schwarz. Durch das Glas scheint beides gedämpft
hindurch. Die Zeiten stehen als „verstrichen" und „−verbleibend", die
Zufallstaste ist gelb, alles andere weiss.

Sechs Fassungen, die zwei Dinge gegeneinander durchspielen: **die Farbwelt hinter
dem Glas** und **die Dicke des Glases selbst**. Dick heisst hier nicht nur mehr
Weichzeichnung, sondern auch mehr Eigenfarbe, ein hellerer Rand und ein
kräftigerer Innenglanz — so wie echtes Glas mit der Dicke milchiger wird.
"""
from werkzeug import (A, biblio, mischen, nexti, pausei, prev, schreibe,
                      wiederholen, SANS, MONO)


# Jede Fassung: Himmel, Horizont, Glasrezept, Schrift, Akzent, Coverfarben.
FASSUNGEN = {
    '': dict(
        name='Sonnenglas', titel='Abendrot, mittleres Glas',
        himmel=['#f0913c 0%', '#d9662c 26%', '#7a3418 48%', '#23150e 62%', '#0b0906 100%'],
        boden='#0d0906', huegel='#140d08',
        glas=dict(blur=26, weiss=.13, rand=.24, kante=.34, glanz=0, saettigung=1.0),
        tinte='#ffffff', stumm='rgba(255,255,255,.68)', akzent='#f2d64b',
        cover=('#f6a24a', '#dd6a2c', '#8a3a1a', '#ffe6b0', '#1b120c'),
    ),
    'a': dict(
        name='Milchglas', titel='Dasselbe Abendrot, doppelt so dickes Glas',
        himmel=['#f0913c 0%', '#d9662c 26%', '#7a3418 48%', '#23150e 62%', '#0b0906 100%'],
        boden='#0d0906', huegel='#140d08',
        glas=dict(blur=64, weiss=.26, rand=.44, kante=.62, glanz=.22, saettigung=1.1),
        tinte='#fffaf4', stumm='rgba(255,250,244,.72)', akzent='#ffd94f',
        cover=('#f6a24a', '#dd6a2c', '#8a3a1a', '#ffe6b0', '#1b120c'),
    ),
    'b': dict(
        name='Blaue Stunde', titel='Kühle Dämmerung, hauchdünnes Glas',
        himmel=['#2f5f9e 0%', '#22406f 24%', '#16294a 46%', '#0c1526 66%', '#05080f 100%'],
        boden='#04070d', huegel='#080d18',
        glas=dict(blur=9, weiss=.06, rand=.14, kante=.20, glanz=0, saettigung=1.0),
        tinte='#eef3fb', stumm='rgba(238,243,251,.60)', akzent='#7fd4ff',
        cover=('#4d84c8', '#2b4f8a', '#132844', '#cfe4ff', '#070c16'),
    ),
    'c': dict(
        name='Morgenmilch', titel='Blasser Morgen, sehr dickes Glas, dunkle Schrift',
        himmel=['#eef3f4 0%', '#dbe6e8 30%', '#c3d3d6 52%', '#a9bcc0 72%', '#8fa4a8 100%'],
        boden='#7b9095', huegel='#8ca1a5',
        glas=dict(blur=86, weiss=.46, rand=.72, kante=.86, glanz=.30, saettigung=1.0),
        tinte='#1e2a2c', stumm='rgba(30,42,44,.62)', akzent='#c2662a',
        cover=('#dfeaec', '#b9cbcf', '#8ba1a6', '#ffffff', '#61787d'),
    ),
    'd': dict(
        name='Gewitter', titel='Sturmviolett, mittleres Glas mit hartem Glanz',
        himmel=['#6b5b86 0%', '#4a3f63 24%', '#2e2942 46%', '#17151f 68%', '#08070b 100%'],
        boden='#07060a', huegel='#0d0b12',
        glas=dict(blur=22, weiss=.11, rand=.52, kante=.78, glanz=.34, saettigung=1.2),
        tinte='#f4f2f8', stumm='rgba(244,242,248,.62)', akzent='#5fe0b0',
        cover=('#8b76a8', '#584a75', '#2a2440', '#ded4f0', '#100e18'),
    ),
    'e': dict(
        name='Neonnacht', titel='Nachtstadt, eingefärbtes Glas statt weissem',
        himmel=['#c0357f 0%', '#7a2270 22%', '#3d1a55 44%', '#181233 66%', '#06050f 100%'],
        boden='#05040c', huegel='#0a0816',
        glas=dict(blur=34, weiss=.10, rand=.30, kante=.46, glanz=.10, saettigung=1.5,
                  ton='rgba(80,220,255,'),
        tinte='#eafaff', stumm='rgba(234,250,255,.62)', akzent='#41e6ff',
        cover=('#d1478d', '#7a2270', '#2a1547', '#ffd6ef', '#0b0818'),
    ),
}


def _css(g, f):
    gl = f['glas']
    ton = gl.get('ton', 'rgba(255,255,255,')
    glanz = (f'''
.glas::after{{content:"";position:absolute;left:0;right:0;top:0;height:38%;
  border-radius:inherit;pointer-events:none;
  background:linear-gradient(180deg, rgba(255,255,255,{gl["glanz"]}) 0%,
    rgba(255,255,255,0) 100%)}}''' if gl['glanz'] else '')
    return f'''
.stage{{background:linear-gradient(180deg, {", ".join(f["himmel"])});
  font-family:{SANS};color:{f["tinte"]}}}

/* Der Horizont: eine dunkle Kante mit weichem Ansatz, kein Foto */
.horizont{{position:absolute;left:0;right:0;background:{f["boden"]}}}
.huegel{{position:absolute;border-radius:50%;background:{f["huegel"]}}}

/* Glasdicke: Weichzeichnung, Eigenfarbe, Randhelligkeit und Innenglanz
   wachsen gemeinsam — dünnes Glas ist fast nur eine Tönung. */
.glas{{position:relative;background:{ton}{gl["weiss"]});
  border:1px solid {ton}{gl["rand"]});
  border-top-color:{ton}{gl["kante"]});
  backdrop-filter:blur({gl["blur"] * g:.0f}px) saturate({gl["saettigung"]});
  -webkit-backdrop-filter:blur({gl["blur"] * g:.0f}px) saturate({gl["saettigung"]});
  box-shadow:0 {26 * g:.0f}px {60 * g:.0f}px rgba(0,0,0,.38),
    inset 0 1px 0 {ton}{gl["kante"]})}}{glanz}

.linie{{position:relative;border-radius:999px;background:{f["tinte"]}59}}
.linie i{{position:absolute;left:0;top:0;bottom:0;border-radius:999px;background:{f["tinte"]}}}
.linie b{{position:absolute;top:50%;transform:translate(-50%,-50%);border-radius:50%;
  background:{f["tinte"]};box-shadow:0 {2 * g:.0f}px {6 * g:.0f}px rgba(0,0,0,.35)}}
.zeiten{{display:flex;justify-content:space-between;font-variant-numeric:tabular-nums;
  font-family:{MONO}}}
.tasten{{display:flex;align-items:center;justify-content:space-between}}
.bib{{display:inline-flex;align-items:center;border-radius:999px;
  background:{ton}{min(gl["weiss"] + .04, .5):.2f});border:1px solid {ton}{gl["rand"]});
  backdrop-filter:blur({max(10, gl["blur"] * .7) * g:.0f}px);text-transform:uppercase}}
.marke{{letter-spacing:{4 * g:.1f}px;text-transform:uppercase;color:{f["stumm"]}}}
'''


def _himmelcover(f, size, radius):
    """Das Cover ist ein Ausschnitt desselben Himmels — Sonne über dunkler Kante."""
    oben, mitte, unten, sonne, land = f['cover']
    kn = f'{int(size)}{oben[1:4]}'
    return f'''<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">
<defs><linearGradient id="hg{kn}" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="{oben}"/><stop offset="52%" stop-color="{mitte}"/>
<stop offset="100%" stop-color="{unten}"/></linearGradient></defs>
<rect x="0" y="0" width="{size}" height="{size}" rx="{radius}" fill="url(#hg{kn})"/>
<circle cx="{size * .50:.1f}" cy="{size * .62:.1f}" r="{size * .085:.1f}" fill="{sonne}"/>
<path d="M0 {size * .70:.1f} Q {size * .30:.1f} {size * .58:.1f} {size * .55:.1f} {size * .68:.1f}
  T {size} {size * .63:.1f} L{size} {size} L0 {size} Z" fill="{land}"/>
</svg>'''


def _transport(f, g, size, luecke):
    return (f'<div class="tasten" style="gap:{luecke}px">'
            f'{mischen(int(size * .92), f["akzent"], 2.6 * g)}'
            f'{prev(size, f["tinte"])}'
            f'{pausei(int(size * 1.05), f["tinte"])}'
            f'{nexti(size, f["tinte"])}'
            f'{wiederholen(int(size * .92), f["tinte"], 2.4 * g)}</div>')


def _bib(f, g, schrift, hoehe):
    return (f'<span class="bib" style="height:{hoehe}px;padding:0 {int(26 * g)}px;'
            f'gap:{int(14 * g)}px;font-size:{schrift}px;letter-spacing:{3.4 * g:.1f}px">'
            f'{biblio(int(schrift * 1.3), f["tinte"])}Sammlung · {A["sammlung"]}</span>')


def _karte(f, g, breite, rund, cover_px, titel_px, luecke_oben):
    return f'''<div class="glas" style="width:{breite}px;border-radius:{rund}px;
  padding:{int(38 * g)}px {int(40 * g)}px {int(34 * g)}px">
  <div style="display:flex;align-items:center;gap:{int(30 * g)}px">
    <div style="line-height:0;flex-shrink:0">{_himmelcover(f, cover_px, cover_px * .22)}</div>
    <div style="flex:1;min-width:0">
      <div style="font-size:{titel_px}px;font-weight:700;overflow:hidden;
        white-space:nowrap;text-overflow:ellipsis">{A['titel']}</div>
      <div style="font-size:{titel_px * .62:.0f}px;color:{f['stumm']};
        margin-top:{int(8 * g)}px;overflow:hidden;white-space:nowrap;
        text-overflow:ellipsis">{A['interpret']}</div>
    </div>
  </div>
  <div class="zeiten" style="font-size:{titel_px * .48:.0f}px;margin-top:{luecke_oben}px">
    <span>{A['pos']}</span><span>{A['rest']}</span></div>
  <div class="linie" style="height:{int(7 * g)}px;margin-top:{int(16 * g)}px">
    <i style="width:{A['frac'] * 100:.0f}%"></i>
    <b style="left:{A['frac'] * 100:.0f}%;width:{int(22 * g)}px;height:{int(22 * g)}px"></b></div>
  <div style="margin-top:{int(36 * g)}px">{_transport(f, g, int(46 * g), int(10 * g))}</div>
</div>'''


def telefon(f):
    g = 1.0
    body = f'''<div class="horizont" style="top:1520px;bottom:0"></div>
<div class="huegel" style="left:-260px;top:1360px;width:1000px;height:420px"></div>
<div class="huegel" style="right:-200px;top:1430px;width:820px;height:360px"></div>
<div style="position:absolute;inset:0;padding:150px 62px 130px;display:flex;
  flex-direction:column;align-items:center">
  {_bib(f, g, 21, 68)}
  <div style="margin-top:auto;margin-bottom:auto;width:100%;display:flex;justify-content:center">
    {_karte(f, g, 956, 52, 220, 54, 40)}
  </div>
  <div class="marke" style="font-size:20px">{f['titel']}</div>
</div>'''
    return _css(g, f), body


def rechner(f):
    g = .74
    body = f'''<div class="horizont" style="top:640px;bottom:0"></div>
<div class="huegel" style="left:-300px;top:520px;width:1100px;height:340px"></div>
<div class="huegel" style="right:-260px;top:580px;width:960px;height:300px"></div>
<div style="position:absolute;inset:0;padding:56px 74px;display:flex;
  flex-direction:column;align-items:center">
  <div style="align-self:flex-start">{_bib(f, g, 15, 48)}</div>
  <div style="margin-top:auto;margin-bottom:auto">
    {_karte(f, g, 900, 40, 168, 44, 30)}
  </div>
  <div class="marke" style="font-size:15px">{f['titel']}</div>
</div>'''
    return _css(g, f), body


def bau():
    for kuerzel, f in FASSUNGEN.items():
        for art, fn in (('iphone', telefon), ('pc', rechner)):
            css, body = fn(f)
            yield schreibe('43' + kuerzel, f['name'].replace(' ', '-'), art, css, body)
