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
/* Das Modul ist die Bühne: Korpus bis an alle vier Kanten */
.stage{{background:linear-gradient(168deg,{KORPUS_H} 0%,{KORPUS} 26%,#141618 100%);
  font-family:{SANS};color:{WEISS}}}
.stage::before{{content:"";position:absolute;inset:0;pointer-events:none;
  box-shadow:inset 0 {2 * g:.0f}px 0 rgba(255,255,255,.16)}}
.modul{{position:absolute;inset:0;display:flex}}

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


def _fenster(g, pad, klein, zahl_px, wort_px, kuppel_b, stil=''):
    return f'''<div class="fenster" style="padding:{pad};{stil}">
  <div class="zeile" style="font-size:{klein}px">
    <span>{A['titel']}<br>{A['tracks'][A['laeuft']][0]}</span>
    <span style="text-align:right">{A['dauer']}<br>An</span>
  </div>
  <div class="zahl" style="font-size:{zahl_px}px;margin-top:auto;
    padding-top:{int(26 * g)}px">{A['pos'].replace(':', '.')}</div>
  <div style="display:flex;justify-content:center;margin-top:{int(34 * g)}px">
    {_kuppel(kuppel_b, A['frac'])}</div>
  <div class="wort" style="font-size:{wort_px}px;margin-top:{int(16 * g)}px;
    margin-bottom:auto">titel</div>
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
    zeilen = ''.join(
        f'<div style="display:flex;align-items:baseline;gap:18px;padding:14px 0;'
        f'border-top:1px solid rgba(240,241,242,.12);font-size:29px'
        f'{";color:" + WEISS if i == A["laeuft"] else ";color:" + STUMM}">'
        f'<span style="font-family:{MONO};font-size:23px;color:{LEISE}">{nr}</span>'
        f'<span style="flex:1;overflow:hidden;white-space:nowrap;'
        f'text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:23px;color:{LEISE}">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))

    body = f'''<div class="modul" style="flex-direction:column;padding:64px 56px 72px">
  <div style="display:flex;align-items:center;justify-content:space-between;
    flex-shrink:0">
    {_bib(g, 23)}
    {_knoepfe(g, 156, 78, 23, 24)}
  </div>

  <div style="margin-top:52px;flex:1;min-height:0;display:flex">
    {_fenster(g, '54px 48px 46px', 26, 176, 28, 560,
              'flex:1;display:flex;flex-direction:column')}
  </div>

  <div style="margin-top:46px;flex-shrink:0">{zeilen}
    <div style="border-top:1px solid rgba(240,241,242,.12)"></div></div>

  <div style="margin-top:52px;flex-shrink:0">{_tasten(g, 134, 172, 42)}</div>
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

    body = f'''<div class="modul" style="padding:52px 56px;gap:56px;
  align-items:stretch">
    <div style="width:470px;flex-shrink:0;display:flex">
      {_fenster(g, '40px 36px 34px', 19, 128, 21, 396,
                'flex:1;display:flex;flex-direction:column')}
    </div>

    <div style="flex:1;min-width:0;display:flex;flex-direction:column">
      <div style="display:flex;align-items:center;justify-content:space-between">
        {_bib(g, 16)}
        {_knoepfe(g, 112, 56, 16, 18)}
      </div>
      <div style="font-size:48px;font-weight:300;margin-top:auto;
        padding-top:30px;letter-spacing:-.01em">{A['titel']}</div>
      <div style="font-size:23px;color:{STUMM};margin-top:8px">
        {A['interpret']} · {A['album']}</div>
      <div style="margin-top:30px">{zeilen}
        <div style="border-top:1px solid rgba(240,241,242,.12)"></div></div>
      <div style="margin-top:auto;padding-top:34px">{_tasten(g, 104, 134, 32)}</div>
    </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('53', 'Fokusmodul', art, css, body)
