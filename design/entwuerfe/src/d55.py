# -*- coding: utf-8 -*-
"""55 Tonartkarte — nach dem Akkordgerät „Cmajor" auf gelber Karte (08.56.30).

Die Vorlage ist ein schwarzer Riegel, der auf einer gelben Karte liegt: links
ein riesiges dünnes Wort, daneben ein Feld runder Tasten, von denen drei einen
farbigen Ring tragen, rechts eine PLAY-Pille, oben zwei geriffelte Knöpfe und
ein Lüftungsgitter, dazu Kleinstschrift, die niemand liest. Übertragen: das
grosse Wort ist der Titel, die runden Tasten sind die Titel des Albums, und der
farbige Ring sitzt auf dem, der läuft. Die gelbe Karte bleibt — sie ist der
Grund, auf dem das Gerät liegt, und trägt die Kleinschrift.
"""
from werkzeug import A, biblio, nexti, prev, pausei, schreibe, MONO, SANS

KARTE = '#d3b53c'
KARTE_D = '#a98d24'
SLAB = '#17181a'
SLAB_H = '#2a2c2f'
WEISS = '#f7f7f6'
STUMM = 'rgba(247,247,246,.52)'
LEISE = 'rgba(247,247,246,.20)'
RING = ('#e08a3c', '#dcc23f', '#4a9fd8')   # läuft, davor, danach


def _css(g):
    return f'''
/* Die gelbe Karte ist die Bühne; der Riegel liegt darauf und läuft an zwei
   Kanten aus dem Bild — wie im Foto, nur näher heran. */
.stage{{background:{KARTE};font-family:{SANS};color:{WEISS}}}
.karte{{position:absolute;inset:0}}
.karte .kmark{{position:absolute;font-family:{MONO};text-transform:uppercase;
  letter-spacing:.18em;color:rgba(30,24,4,.62)}}
.karte .geist{{position:absolute;font-weight:700;color:rgba(30,24,4,.16);
  line-height:.8;letter-spacing:-.04em}}

.riegel{{position:relative;border-radius:{40 * g:.0f}px;
  background:linear-gradient(160deg,{SLAB_H} 0%,{SLAB} 22%,#0d0e10 100%);
  box-shadow:0 {30 * g:.0f}px {64 * g:.0f}px rgba(20,20,20,.5),
             inset 0 {2 * g:.0f}px 0 rgba(255,255,255,.12)}}

.gross{{font-weight:300;letter-spacing:-.035em;line-height:.92}}
.pille{{display:inline-flex;align-items:center;border-radius:999px;
  border:{1.5 * g:.0f}px solid {LEISE};color:{STUMM};text-transform:uppercase;
  font-family:{MONO};letter-spacing:.16em}}

/* Die runden Tasten: dunkel mit hellem Ring, drei davon farbig */
.rt{{position:relative;border-radius:50%;display:flex;align-items:center;
  justify-content:center;flex-shrink:0;font-weight:400;
  background:linear-gradient(180deg,#303336 0%,#191b1d 62%,#0f1113 100%);
  box-shadow:0 0 0 {2 * g:.0f}px rgba(247,247,246,.55),
             0 {5 * g:.0f}px {12 * g:.0f}px rgba(0,0,0,.45)}}

.spiel{{display:flex;align-items:center;justify-content:center;
  border-radius:999px;background:#0e1012;color:{WEISS};
  box-shadow:0 0 0 {2 * g:.0f}px rgba(247,247,246,.65),
             inset 0 {2 * g:.0f}px {6 * g:.0f}px rgba(255,255,255,.08)}}
.rund{{display:flex;align-items:center;justify-content:center;border-radius:50%;
  background:#0e1012;flex-shrink:0;
  box-shadow:0 0 0 {2 * g:.0f}px rgba(247,247,246,.55)}}

/* Geriffelter Knopf wie im Foto oben rechts */
.knopf{{position:relative;border-radius:{10 * g:.0f}px;overflow:hidden;flex-shrink:0;
  background:linear-gradient(180deg,#3d4145 0%,#1c1f22 55%,#0d0f11 100%);
  box-shadow:0 {5 * g:.0f}px {12 * g:.0f}px rgba(0,0,0,.5)}}
.knopf::after{{content:"";position:absolute;inset:0;
  background:repeating-linear-gradient(90deg,rgba(255,255,255,.14) 0 {2 * g:.0f}px,
    rgba(0,0,0,.32) {2 * g:.0f}px {5 * g:.0f}px)}}
.knopf span{{position:relative;z-index:1;display:block;text-align:center;
  font-family:{MONO};color:{WEISS}}}
.gitter{{border-radius:{8 * g:.0f}px;
  background:repeating-linear-gradient(180deg,#0c0d0f 0 {4 * g:.0f}px,
    #24272a {4 * g:.0f}px {9 * g:.0f}px)}}

.haar{{position:relative;height:{2 * g:.0f}px;background:{LEISE}}}
.haar i{{position:absolute;left:0;top:0;bottom:0;background:{WEISS}}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{STUMM};
  font-variant-numeric:tabular-nums}}
.klein{{font-family:{MONO};color:{LEISE};line-height:1.5;letter-spacing:.04em}}
.bib{{display:inline-flex;align-items:center;border-radius:999px;
  border:{1.5 * g:.0f}px solid rgba(247,247,246,.5);color:{WEISS};
  text-transform:uppercase;font-family:{MONO};letter-spacing:.14em}}
'''


def _tasten(g, size, schrift, luecke, spalten):
    """Ein Feld runder Tasten: die Titel des Albums, danach leere Plätze."""
    stk = []
    for i in range(spalten * 2):
        if i < len(A['tracks']):
            nr = A['tracks'][i][0]
            ring = (RING[0] if i == A['laeuft']
                    else RING[1] if i == 0 else RING[2] if i == 3 else None)
        else:
            nr, ring = '·', None
        rand = (f'box-shadow:0 0 0 {3 * g:.0f}px {ring};' if ring else '')
        stk.append(f'<div class="rt" style="width:{size}px;height:{size}px;'
                   f'font-size:{schrift}px;{rand}">{nr}</div>')
    return (f'<div style="display:grid;grid-template-columns:repeat({spalten},{size}px);'
            f'gap:{luecke}px">{"".join(stk)}</div>')


def _kopfzeile(g, knopf_b, knopf_h, schrift, gitter_b, gitter_h):
    return (f'<div style="display:flex;align-items:center;gap:{int(16 * g)}px">'
            f'<div class="gitter" style="width:{gitter_b}px;height:{gitter_h}px"></div>'
            f'<div class="knopf" style="width:{knopf_b}px;height:{knopf_h}px;'
            f'padding-top:{int(knopf_h * .32)}px">'
            f'<span style="font-size:{schrift}px">60</span></div>'
            f'<div class="knopf" style="width:{knopf_b}px;height:{knopf_h}px;'
            f'padding-top:{int(knopf_h * .32)}px">'
            f'<span style="font-size:{schrift}px">{A["jahr"]}</span></div></div>')


def _bib(g, schrift, hoehe):
    return (f'<span class="bib" style="height:{hoehe}px;padding:0 {int(22 * g)}px;'
            f'gap:{int(12 * g)}px;font-size:{schrift}px">'
            f'{biblio(int(schrift * 1.3), WEISS)}Sammlung · {A["sammlung"]}</span>')


KLEIN = ('Musiklib · lokale Sammlung · kein Netz · kein Konto · keine Werbung<br>'
         'Alben werden beim Einlesen aus den Dateien gelesen, nicht aus dem Netz<br>'
         'Fortsetzung: weiter · Zufall: aus · Wiederholen: aus')


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0">
  <div class="karte">
    <span class="kmark" style="left:36px;top:30px;font-size:21px">musiklib.local</span>
    <span class="kmark" style="right:36px;top:30px;font-size:21px">01</span>
    <span class="geist" style="left:24px;top:120px;font-size:300px">C</span>
  </div>

  <div class="riegel" style="position:absolute;left:74px;top:158px;right:-40px;
    bottom:-40px;padding:62px 56px;display:flex;flex-direction:column">
    <div style="display:flex;align-items:center;justify-content:space-between">
      {_bib(g, 19, 58)}
      {_kopfzeile(g, 112, 68, 21, 112, 56)}
    </div>

    <div class="gross" style="font-size:118px;margin-top:auto;
      padding-top:56px">{A['titel']}</div>
    <div style="display:flex;align-items:center;gap:22px;margin-top:22px">
      <span class="pille" style="height:44px;padding:0 20px;font-size:19px">
        Titel {A['tracks'][A['laeuft']][0]} / 04</span>
      <span style="font-size:27px;color:{STUMM}">{A['interpret']} · {A['album']}</span>
    </div>

    <div class="haar" style="margin-top:40px">
      <i style="width:{A['frac'] * 100:.0f}%"></i></div>
    <div class="zeiten" style="font-size:24px;margin-top:16px">
      <span>{A['pos']}</span><span>{A['dauer']}</span></div>

    <div style="margin-top:76px">{_tasten(g, 128, 35, 28, 5)}</div>

    <div style="display:flex;align-items:center;gap:26px;margin-top:auto;
      padding-top:58px;padding-right:60px">
      <div class="rund" style="width:104px;height:104px">{prev(42, WEISS)}</div>
      <div class="spiel" style="flex:1;height:104px;gap:20px;font-size:26px;
        letter-spacing:.24em;font-family:{MONO}">{pausei(38, WEISS)}Pause</div>
      <div class="rund" style="width:104px;height:104px">{nexti(42, WEISS)}</div>
    </div>

    <div class="klein" style="font-size:18px;margin-top:auto;
      padding-top:44px;padding-bottom:52px">{KLEIN}</div>
  </div>
</div>'''
    return css, body


def rechner():
    g = .78
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0">
  <div class="karte">
    <span class="kmark" style="left:30px;top:24px;font-size:16px">musiklib.local</span>
    <span class="kmark" style="right:30px;top:24px;font-size:16px">01</span>
    <span class="geist" style="left:22px;top:86px;font-size:230px">C</span>
  </div>

  <div class="riegel" style="position:absolute;left:132px;top:96px;right:-40px;
    bottom:-40px;padding:52px 56px;display:flex;gap:56px">
    <div style="flex:1;min-width:0;display:flex;flex-direction:column">
      <div class="gross" style="font-size:92px">{A['titel']}</div>
      <div style="display:flex;align-items:center;gap:18px;margin-top:18px">
        <span class="pille" style="height:34px;padding:0 16px;font-size:15px">
          Titel {A['tracks'][A['laeuft']][0]} / 04</span>
        <span style="font-size:21px;color:{STUMM}">{A['interpret']} · {A['album']}</span>
      </div>
      <div class="haar" style="margin-top:30px">
        <i style="width:{A['frac'] * 100:.0f}%"></i></div>
      <div class="zeiten" style="font-size:18px;margin-top:12px">
        <span>{A['pos']}</span><span>{A['dauer']}</span></div>
      <div style="margin-top:auto;padding-top:36px">{_tasten(g, 100, 28, 22, 4)}</div>
      <div class="klein" style="font-size:14px;margin-top:auto;
        padding-bottom:44px">{KLEIN}</div>
    </div>

    <div style="width:360px;flex-shrink:0;display:flex;flex-direction:column;
      align-items:flex-end;padding-right:56px;padding-bottom:52px">
      {_kopfzeile(g, 92, 56, 17, 92, 46)}
      <div style="margin-top:auto;width:100%">
        <div class="spiel" style="height:104px;gap:18px;font-size:22px;
          letter-spacing:.24em;font-family:{MONO}">{pausei(32, WEISS)}Pause</div>
        <div style="display:flex;gap:18px;margin-top:22px">
          <div class="rund" style="width:82px;height:82px">{prev(32, WEISS)}</div>
          <div class="rund" style="width:82px;height:82px">{nexti(32, WEISS)}</div>
          <div style="flex:1"></div>
        </div>
        <div style="margin-top:26px">{_bib(g, 15, 46)}</div>
      </div>
    </div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('55', 'Tonartkarte', art, css, body)
