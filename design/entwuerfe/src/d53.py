# -*- coding: utf-8 -*-
"""53 Fokusmodul — nach dem Bedienmodul mit Kuppelanzeige (08.48.50).

Die Vorlage ist ein kleines schwarzes Modul: oben zwei geriffelte Knöpfe, in der
Mitte ein Fenster mit dünnen Ziffern und darunter eine orange leuchtende Kuppel
mit einem weissen Strich darin, ganz unten vier runde Gummitasten. Die Kuppel
ist das Merkwürdige daran — sie ist kein Balken und kein Ring, sondern eine
Halbscheibe, über die ein Zeiger wandert. Genau die wird hier zur
Fortschrittsanzeige: der Strich steht dort, wo der Titel steht.
"""
import math

from werkzeug import A, biblio, nexti, prev, pausei, schreibe, MONO, SANS

KORPUS = '#212325'
KORPUS_H = '#34373a'
FENSTER = '#0a0b0c'
WEISS = '#f0f1f2'
STUMM = 'rgba(240,241,242,.55)'
LEISE = 'rgba(240,241,242,.22)'
ORANGE = '#f26a12'
# Die Kuppel leuchtet von unten: hell in der Mitte, dunkel am Rand.
KUPPEL = ('#ffb15a', '#f0610b', '#8c2f04')


def _css(g):
    return f'''
.stage{{background:linear-gradient(155deg,#c7c9cb 0%,#9fa2a5 46%,#bcbfc2 100%);
  font-family:{SANS};color:{WEISS}}}

.modul{{position:relative;border-radius:{26 * g:.0f}px;
  background:linear-gradient(168deg,{KORPUS_H} 0%,{KORPUS} 26%,#141618 100%);
  box-shadow:0 {28 * g:.0f}px {62 * g:.0f}px rgba(20,22,24,.5),
             inset 0 {2 * g:.0f}px 0 rgba(255,255,255,.16)}}

/* Das Fenster liegt tiefer als das Gehäuse */
.fenster{{background:{FENSTER};border-radius:{14 * g:.0f}px;
  box-shadow:inset 0 {3 * g:.0f}px {12 * g:.0f}px rgba(0,0,0,.9),
             0 0 0 {1 * g:.0f}px rgba(255,255,255,.06)}}

.zeile{{display:flex;justify-content:space-between;font-family:{MONO};
  color:{STUMM};text-transform:uppercase;letter-spacing:.1em}}
.zahl{{font-weight:200;line-height:1;text-align:center;
  font-variant-numeric:tabular-nums;letter-spacing:.02em}}
.wort{{text-align:center;color:{STUMM};font-weight:400}}

/* Geriffelter Knopf: Zylinder mit Rillen, wie im Foto oben */
.knopf{{position:relative;border-radius:999px;flex-shrink:0;overflow:hidden;
  background:linear-gradient(180deg,#4b4f53 0%,#25282b 52%,#101214 100%);
  box-shadow:0 {6 * g:.0f}px {14 * g:.0f}px rgba(0,0,0,.5)}}
.knopf::after{{content:"";position:absolute;inset:0;
  background:repeating-linear-gradient(90deg,rgba(255,255,255,.16) 0 {2 * g:.0f}px,
    rgba(0,0,0,.30) {2 * g:.0f}px {5 * g:.0f}px)}}
.knopf span{{position:absolute;left:0;right:0;bottom:{6 * g:.0f}px;z-index:1;
  text-align:center;font-family:{MONO};color:{WEISS}}}

/* Gummitasten: matt, mit einem Lichtsaum an der Oberkante */
.taste{{flex-shrink:0;border-radius:50%;display:flex;align-items:center;
  justify-content:center;
  background:linear-gradient(180deg,#3c4044 0%,#1b1e20 60%,#111315 100%);
  box-shadow:0 {5 * g:.0f}px {12 * g:.0f}px rgba(0,0,0,.5),
             inset 0 {1.5 * g:.0f}px 0 rgba(255,255,255,.22)}}
.taste.warm{{background:linear-gradient(180deg,#ff8b3a 0%,{ORANGE} 60%,#b8450a 100%)}}
.bib{{display:inline-flex;align-items:center;color:{STUMM};font-family:{MONO};
  text-transform:uppercase}}
'''


def _kuppel(w, frac):
    """Halbscheibe mit Zeiger: die eine Anzeige, die dieses Gerät ausmacht."""
    h = w * .52
    r = w / 2
    a = math.pi * (1 - frac)          # von links (frac 0) nach rechts (frac 1)
    zx, zy = r + math.cos(a) * r * .80, h - math.sin(a) * r * .80
    return f'''<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">
<defs><radialGradient id="ku{int(w)}" cx="50%" cy="100%" r="100%">
<stop offset="0%" stop-color="{KUPPEL[0]}"/><stop offset="52%" stop-color="{KUPPEL[1]}"/>
<stop offset="100%" stop-color="{KUPPEL[2]}"/></radialGradient></defs>
<path d="M0 {h:.0f} A{r:.0f} {r:.0f} 0 0 1 {w:.0f} {h:.0f} Z" fill="url(#ku{int(w)})"/>
<line x1="{r:.0f}" y1="{h:.0f}" x2="{zx:.1f}" y2="{zy:.1f}" stroke="#ffffff"
  stroke-width="{max(3, w * .016):.0f}" stroke-linecap="round"/>
<line x1="{r + math.cos(math.pi * .34) * r * .60:.1f}"
  y1="{h - math.sin(math.pi * .34) * r * .60:.1f}"
  x2="{r + math.cos(math.pi * .34) * r * .82:.1f}"
  y2="{h - math.sin(math.pi * .34) * r * .82:.1f}" stroke="rgba(255,255,255,.6)"
  stroke-width="{max(1.5, w * .006):.0f}" stroke-linecap="round"/></svg>'''


def _knoepfe(g, breite, hoehe, schrift, luecke):
    return (f'<div style="display:flex;gap:{luecke}px">'
            f'<div class="knopf" style="width:{breite}px;height:{hoehe}px">'
            f'<span style="font-size:{schrift}px">Ton 60</span></div>'
            f'<div class="knopf" style="width:{breite}px;height:{hoehe}px">'
            f'<span style="font-size:{schrift}px">{A["jahr"]}</span></div></div>')


def _fenster(g, pad, klein, zahl_px, wort_px, kuppel_b):
    return f'''<div class="fenster" style="padding:{pad}">
  <div class="zeile" style="font-size:{klein}px">
    <span>{A['titel']}<br>{A['tracks'][A['laeuft']][0]}</span>
    <span style="text-align:right">{A['dauer']}<br>An</span>
  </div>
  <div class="zahl" style="font-size:{zahl_px}px;margin-top:{int(26 * g)}px">
    {A['pos'].replace(':', '.')}</div>
  <div style="display:flex;justify-content:center;margin-top:{int(26 * g)}px">
    {_kuppel(kuppel_b, A['frac'])}</div>
  <div class="wort" style="font-size:{wort_px}px;margin-top:{int(16 * g)}px">titel</div>
</div>'''


def _tasten(g, size, gross_, luecke):
    return (f'<div style="display:flex;align-items:center;justify-content:center;'
            f'gap:{luecke}px">'
            f'<div class="taste" style="width:{size}px;height:{size}px">'
            f'{prev(int(size * .40), WEISS)}</div>'
            f'<div class="taste warm" style="width:{gross_}px;height:{gross_}px">'
            f'{pausei(int(gross_ * .38), "#1b1006")}</div>'
            f'<div class="taste" style="width:{size}px;height:{size}px">'
            f'{nexti(int(size * .40), WEISS)}</div>'
            f'<div class="taste" style="width:{size}px;height:{size}px">'
            f'{biblio(int(size * .40), WEISS)}</div></div>')


def _bib(g, schrift):
    return (f'<span class="bib" style="gap:{int(10 * g)}px;font-size:{schrift}px;'
            f'letter-spacing:{2.4 * g:.1f}px">{biblio(int(schrift * 1.3), STUMM)}'
            f'Sammlung · {A["sammlung"]}</span>')


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:80px 60px">
  <div class="modul" style="width:940px;padding:52px 54px 62px">
    <div style="display:flex;align-items:center;justify-content:space-between">
      {_bib(g, 22)}
      {_knoepfe(g, 148, 74, 22, 22)}
    </div>

    <div style="margin-top:48px">{_fenster(g, '46px 44px 40px', 25, 168, 27, 520)}</div>

    <div style="margin-top:56px">{_tasten(g, 130, 168, 40)}</div>
  </div>
</div>'''
    return css, body


def rechner():
    g = .78
    css = _css(g)
    zeilen = ''.join(
        f'<div style="display:flex;align-items:baseline;gap:16px;padding:11px 0;'
        f'border-top:1px solid rgba(240,241,242,.12);font-size:21px'
        f'{";color:" + WEISS if i == A["laeuft"] else ";color:" + STUMM}">'
        f'<span style="font-family:{MONO};font-size:17px;color:{LEISE}">{nr}</span>'
        f'<span style="flex:1;overflow:hidden;white-space:nowrap;text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:17px;color:{LEISE}">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))

    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:56px 74px">
  <div class="modul" style="width:1452px;padding:44px 48px;display:flex;gap:52px;
    align-items:center">
    <div style="width:430px;flex-shrink:0">
      {_fenster(g, '34px 32px 30px', 18, 118, 20, 366)}
    </div>

    <div style="flex:1;min-width:0">
      <div style="display:flex;align-items:center;justify-content:space-between">
        {_bib(g, 16)}
        {_knoepfe(g, 112, 56, 16, 18)}
      </div>
      <div style="font-size:44px;font-weight:300;margin-top:26px;letter-spacing:-.01em">
        {A['titel']}</div>
      <div style="font-size:22px;color:{STUMM};margin-top:8px">
        {A['interpret']} · {A['album']}</div>
      <div style="margin-top:22px">{zeilen}
        <div style="border-top:1px solid rgba(240,241,242,.12)"></div></div>
      <div style="margin-top:30px">{_tasten(g, 96, 124, 30)}</div>
    </div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('53', 'Fokusmodul', art, css, body)
