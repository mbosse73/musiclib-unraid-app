# -*- coding: utf-8 -*-
"""43 Sonnenglas — nach der Glaskarte vor dem Sonnenuntergang (23.38.31).

Die Vorlage legt eine Karte aus Milchglas über ein Foto: oben glüht der Himmel,
unten steht der Horizont schwarz. Durch das Glas scheint beides gedämpft
hindurch. Die Zeiten stehen als „verstrichen" und „−verbleibend", die
Zufallstaste ist gelb, alles andere weiss.

Sieben Fassungen bei **immer derselben Abendfarbe**. Was sich ändert, ist allein
die Scheibe: ihre **Dicke** (von 3 px Weichzeichnung bis 130) und ihre
**Oberfläche** — poliert, matt geätzt, rauchgetönt, geschliffen. Beides hängt
zusammen: dickes Glas streut mehr und wird milchiger, poliertes spiegelt
stattdessen, geätztes hat Korn und gar keinen Glanz. Die letzte Fassung zeigt,
dass dick nicht milchig heissen muss: klares Glas verrät seine Stärke über die
Kante und den Schatten, nicht über die Trübung.
"""
from werkzeug import (A, biblio, mischen, nexti, pausei, prev, schreibe,
                      wiederholen, SANS, MONO)


# Jede Fassung: Himmel, Horizont, Glasrezept, Schrift, Akzent, Coverfarben.
HIMMEL = ['#f0913c 0%', '#d9662c 26%', '#7a3418 48%', '#23150e 62%', '#0b0906 100%']
COVER = ('#f6a24a', '#dd6a2c', '#8a3a1a', '#ffe6b0', '#1b120c')


def _f(name, titel, glas, tinte='#ffffff', stumm='rgba(255,255,255,.68)', akzent='#f2d64b'):
    """Immer derselbe Himmel — nur die Scheibe ist anders."""
    return dict(name=name, titel=titel, himmel=HIMMEL, boden='#0d0906', huegel='#140d08',
                glas=glas, tinte=tinte, stumm=stumm, akzent=akzent, cover=COVER)


# glas: blur = Dicke, weiss = Eigenfarbe, rand/kante = Kanten, saettigung = Durchblick.
# glanz = weicher Lichtverlauf oben, streif = harter Spiegelstreifen quer,
# koern = geätztes Korn, riffel = Rippenabstand in px, dicke = sichtbare Glasstärke,
# licht = Richtung des Lichteinfalls, schatten = eigener Schlagschatten (x,y,blur,deckung).
FASSUNGEN = {
    '': _f('Sonnenglas', 'Die Vorlage — mittleres Glas, leicht satiniert',
           dict(blur=26, weiss=.13, rand=.24, kante=.34, saettigung=1.0)),

    'a': _f('Milchglas', 'Dieselbe Scheibe, doppelt so dick',
            dict(blur=64, weiss=.26, rand=.44, kante=.62, glanz=.22, saettigung=1.1)),

    'b': _f('Klarglas', 'Dünn und poliert — der Himmel bleibt scharf, das Glas spiegelt',
            dict(blur=3, weiss=.05, rand=.50, kante=.92, streif=.55, saettigung=1.05)),

    'c': _f('Mattglas', 'Geätzt: kein Glanz, dafür Korn — Licht wird gestreut, nicht geworfen',
            dict(blur=48, weiss=.30, rand=.16, kante=.20, koern=.14, saettigung=.85)),

    'f': _f('Rauchglas', 'Dunkel getönt und poliert — die Scheibe dämpft, statt aufzuhellen',
            dict(blur=12, weiss=.36, rand=.26, kante=.44, streif=.42, saettigung=1.15,
                 ton='rgba(18,10,8,'), stumm='rgba(255,255,255,.60)'),

    # 43b als Vorlage: dieselbe polierte Kante, aber ohne den Spiegelstreifen
    # und um ein Vielfaches dicker.
    'h': _f('Vitrinenglas',
            'Wie Klarglas poliert, aber ohne Spiegelstreifen und um ein Vielfaches dicker',
            dict(blur=46, weiss=.15, rand=.62, kante=.98, saettigung=1.20, dicke=20)),
}


def _css(g, f):
    gl = f['glas']
    ton = gl.get('ton', 'rgba(255,255,255,')
    hell = 'rgba(255,255,255,'

    # Oberflaeche 1: weicher Lichtverlauf oben (satiniert) oder harter
    # Spiegelstreifen quer (poliert). Geaetztes Glas bekommt beides nicht.
    lagen = []
    if gl.get('licht') == 'links':
        # Heller Ansatz links, Abfall nach rechts — der Verlauf macht die Richtung.
        lagen.append(f'linear-gradient(96deg, {hell}.30) 0%, {hell}.08) 20%, '
                     f'{hell}0) 46%, rgba(0,0,0,.10) 74%, rgba(0,0,0,.20) 100%)')
    if gl.get('glanz'):
        lagen.append(f'linear-gradient(180deg, {hell}{gl["glanz"]}) 0%, {hell}0) 62%)')
    if gl.get('streif'):
        lagen.append(f'linear-gradient(116deg, {hell}0) 30%, {hell}{gl["streif"]}) 44%, '
                     f'{hell}{gl["streif"] * .45:.2f}) 50%, {hell}0) 58%)')
    nach = (f'''
.glas::after{{content:"";position:absolute;inset:0;border-radius:inherit;
  pointer-events:none;background:{", ".join(lagen)}}}''' if lagen else '')

    # Oberflaeche 2: Rippen (gegossen) oder Korn (geaetzt) liegen unter dem Glanz.
    vor = ''
    if gl.get('riffel'):
        r = gl['riffel'] * g
        vor = f'''
.glas::before{{content:"";position:absolute;inset:0;border-radius:inherit;
  pointer-events:none;backdrop-filter:blur({gl["blur"] * g * .55:.0f}px);
  -webkit-backdrop-filter:blur({gl["blur"] * g * .55:.0f}px);
  background:repeating-linear-gradient(90deg,
    {hell}.16) 0 {r * .10:.1f}px, {hell}0) {r * .10:.1f}px {r * .46:.1f}px,
    rgba(0,0,0,.13) {r * .46:.1f}px {r * .56:.1f}px, {hell}0) {r * .56:.1f}px {r:.1f}px)}}'''
    elif gl.get('koern'):
        vor = f'''
.glas::before{{content:"";position:absolute;inset:0;border-radius:inherit;
  pointer-events:none;opacity:{gl["koern"]};
  background:
    repeating-linear-gradient(37deg, {hell}.9) 0 1px, {hell}0) 1px 3px),
    repeating-linear-gradient(-53deg, rgba(0,0,0,.7) 0 1px, {hell}0) 1px 4px)}}'''

    # Sichtbare Glasstaerke. Ohne Lichtrichtung ein gleichmaessiger Innenring;
    # mit Licht von links wird die linke Innenflaeche hell und die rechte dunkel —
    # das ist es, was dickes klares Glas von dickem milchigem unterscheidet.
    d = gl.get('dicke', 0) * g
    if not d:
        dicke = ''
    elif gl.get('licht') == 'links':
        dicke = (f', inset {d:.0f}px 0 {d * 1.4:.0f}px {hell}.40)'
                 f', inset {-d:.0f}px 0 {d * 1.6:.0f}px rgba(0,0,0,.40)'
                 f', inset 0 {d * .5:.0f}px {d:.0f}px {hell}.14)')
    else:
        dicke = (f', inset 0 0 0 {d:.0f}px {hell}.14)'
                 f', inset 0 {d:.0f}px {d * 1.8:.0f}px rgba(0,0,0,.22)')

    # Schlagschatten: standardmaessig mittig unter der Karte, sonst wie angegeben.
    if gl.get('schatten'):
        sx, sy, sb, sa = gl['schatten']
        wurf = f'{sx * g:.0f}px {sy * g:.0f}px {sb * g:.0f}px rgba(0,0,0,{sa})'
    else:
        wurf = f'0 {26 * g:.0f}px {60 * g:.0f}px rgba(0,0,0,.38)'

    # Licht von links: linke Kante leuchtet, rechte laeuft ins Dunkle.
    seiten = (f'\n  border-left-color:{hell}.95);border-right-color:rgba(0,0,0,.30);'
              if gl.get('licht') == 'links' else '')

    return f'''
.stage{{background:linear-gradient(180deg, {", ".join(f["himmel"])});
  font-family:{SANS};color:{f["tinte"]}}}

/* Der Horizont: eine dunkle Kante mit weichem Ansatz, kein Foto */
.horizont{{position:absolute;left:0;right:0;background:{f["boden"]}}}
.huegel{{position:absolute;border-radius:50%;background:{f["huegel"]}}}

/* Die Scheibe: Dicke steckt in blur und Eigenfarbe, die Oberflaeche in den
   beiden Pseudo-Lagen darueber. Alles andere bleibt ueber alle Fassungen gleich. */
.glas{{position:relative;background:{ton}{gl["weiss"]});
  border:1px solid {ton if ton.startswith("rgba(255") else hell}{gl["rand"]});
  border-top-color:{hell}{gl["kante"]});{seiten}
  backdrop-filter:blur({gl["blur"] * g:.0f}px) saturate({gl["saettigung"]});
  -webkit-backdrop-filter:blur({gl["blur"] * g:.0f}px) saturate({gl["saettigung"]});
  box-shadow:{wurf},
    inset 0 1px 0 {hell}{gl["kante"]}){dicke}}}{vor}{nach}
.glas > *{{position:relative;z-index:1}}

.linie{{position:relative;border-radius:999px;background:{f["tinte"]}59}}
.linie i{{position:absolute;left:0;top:0;bottom:0;border-radius:999px;background:{f["tinte"]}}}
.linie b{{position:absolute;top:50%;transform:translate(-50%,-50%);border-radius:50%;
  background:{f["tinte"]};box-shadow:0 {2 * g:.0f}px {6 * g:.0f}px rgba(0,0,0,.35)}}
.zeiten{{display:flex;justify-content:space-between;font-variant-numeric:tabular-nums;
  font-family:{MONO}}}
.tasten{{display:flex;align-items:center;justify-content:space-between}}
.bib{{display:inline-flex;align-items:center;border-radius:999px;
  background:{ton}{min(gl["weiss"] + .04, .5):.2f});border:1px solid {hell}{gl["rand"]});
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
