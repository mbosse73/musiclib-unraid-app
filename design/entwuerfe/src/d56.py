# -*- coding: utf-8 -*-
"""56 Punktring — nach dem runden Lautsprecherdeckel mit Leuchtpunkten (08.58.02).

Die Vorlage zeigt eine schwarze Scheibe mit einem Metallrand, auf der ein Kranz
kleiner grüner Punkte sitzt; ein paar davon sind mit Zahlen beschriftet, in der
Mitte steht ein winziges Wiedergabezeichen. Es ist eine Uhr ohne Zeiger: man
liest, wie weit es ist, an den Punkten, die leuchten. Übertragen: der Kranz ist
der laufende Titel, ein Punkt je Viertelminute, und die beschrifteten Punkte
tragen die Minuten. Der Kranz ist zugleich die Spulfläche — man tippt auf den
Punkt, an den man will.
"""
import math

from werkzeug import A, biblio, nexti, prev, pausei, schreibe, MONO, SANS

GRUEN = '#5ce06a'
GRUEN_D = '#1d3a22'
SCHEIBE = '#141516'
RAND = '#2e3133'
WEISS = '#eceeef'
STUMM = 'rgba(236,238,239,.54)'
LEISE = 'rgba(236,238,239,.22)'


def _css(g):
    return f'''
.stage{{background:linear-gradient(170deg,#26282a 0%,#151617 58%,#0d0e0f 100%);
  font-family:{SANS};color:{WEISS}}}

/* Der Rand ist gedrehtes Metall, die Fläche darin ist stumpf */
.scheibe{{position:relative;border-radius:50%;
  background:radial-gradient(circle at 42% 34%,#1e2022 0%,{SCHEIBE} 58%,#0c0d0e 100%);
  box-shadow:0 0 0 {10 * g:.0f}px {RAND},
             0 0 0 {12 * g:.0f}px rgba(0,0,0,.6),
             0 {26 * g:.0f}px {60 * g:.0f}px rgba(0,0,0,.62),
             inset 0 {2 * g:.0f}px {2 * g:.0f}px rgba(255,255,255,.10)}}
/* Nur der Kranz liegt über der Fläche — nicht jedes SVG darin */
.scheibe > svg{{position:absolute;inset:0;display:block}}
.mitte{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  display:flex;align-items:center;gap:{14 * g:.0f}px;white-space:nowrap}}
.mitte .wort{{color:{STUMM};letter-spacing:.06em}}

.taste{{flex-shrink:0;border-radius:50%;display:flex;align-items:center;
  justify-content:center;background:#1c1e20;
  box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(236,238,239,.16)}}
.taste.an{{background:{GRUEN_D};box-shadow:inset 0 0 0 {1 * g:.0f}px {GRUEN}}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{STUMM};
  font-variant-numeric:tabular-nums}}
.bib{{display:inline-flex;align-items:center;border-radius:999px;
  border:{1.5 * g:.0f}px solid rgba(236,238,239,.28);color:{WEISS};
  text-transform:uppercase;font-family:{MONO};letter-spacing:.14em}}
'''


def _kranz(size, frac, punkte=24, marke=4):
    """Ein Punkt je Viertelminute; jeder vierte trägt seine Minute."""
    r = size / 2
    rr = r * .80
    pr = max(3.2, size * .0125)
    stk = []
    for i in range(punkte):
        a = math.radians(-90 + i * 360 / punkte)
        x, y = r + math.cos(a) * rr, r + math.sin(a) * rr
        an = i / punkte <= frac
        stk.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{pr:.1f}" '
                   f'fill="{GRUEN if an else "#2a2d2f"}" '
                   f'opacity="{.95 if an else .9}"/>')
        if i % marke == 0:
            lx, ly = r + math.cos(a) * rr * .80, r + math.sin(a) * rr * .80
            stk.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="rgba(236,238,239,.42)" '
                       f'font-family="{MONO}" font-size="{size * .030:.0f}" '
                       f'text-anchor="middle" dominant-baseline="central">'
                       f'{i // marke}</text>')
    return (f'<svg viewBox="0 0 {size:.0f} {size:.0f}" width="{size:.0f}" '
            f'height="{size:.0f}">{"".join(stk)}</svg>')


def _scheibe(g, size, mitte_px):
    return f'''<div class="scheibe" style="width:{size}px;height:{size}px">
  {_kranz(size, A['frac'])}
  <div class="mitte">
    {pausei(int(mitte_px * 1.5), GRUEN)}
    <span class="wort" style="font-size:{mitte_px}px">{A['titel']}</span>
  </div>
</div>'''


def _transport(g, size, gross_, luecke):
    return (f'<div style="display:flex;align-items:center;justify-content:center;'
            f'gap:{luecke}px">'
            f'<div class="taste" style="width:{size}px;height:{size}px">'
            f'{prev(int(size * .42), WEISS)}</div>'
            f'<div class="taste an" style="width:{gross_}px;height:{gross_}px">'
            f'{pausei(int(gross_ * .38), GRUEN)}</div>'
            f'<div class="taste" style="width:{size}px;height:{size}px">'
            f'{nexti(int(size * .42), WEISS)}</div></div>')


def _bib(g, schrift, hoehe):
    return (f'<span class="bib" style="height:{hoehe}px;padding:0 {int(22 * g)}px;'
            f'gap:{int(12 * g)}px;font-size:{schrift}px">'
            f'{biblio(int(schrift * 1.3), GRUEN)}Sammlung · {A["sammlung"]}</span>')


def telefon():
    g = 1.0
    css = _css(g)
    zeilen = ''.join(
        f'<div style="display:flex;align-items:baseline;gap:18px;padding:14px 0;'
        f'border-top:1px solid rgba(236,238,239,.12);font-size:30px;text-align:left'
        f'{";color:" + WEISS if i == A["laeuft"] else ";color:" + STUMM}">'
        f'<span style="font-family:{MONO};font-size:24px;'
        f'color:{GRUEN if i == A["laeuft"] else LEISE}">{nr}</span>'
        f'<span style="flex:1;overflow:hidden;white-space:nowrap;'
        f'text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:24px;color:{LEISE}">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))

    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;padding:96px 56px 104px">
  {_bib(g, 22, 66)}

  <div style="margin:auto 0">{_scheibe(g, 968, 32)}</div>

  <div style="width:100%;text-align:center">
    <div style="font-size:58px;font-weight:600;letter-spacing:-.02em">{A['titel']}</div>
    <div style="font-size:30px;color:{STUMM};margin-top:12px">
      {A['interpret']} · {A['album']} · {A['jahr']}</div>
    <div style="margin-top:46px">{zeilen}
      <div style="border-top:1px solid rgba(236,238,239,.12)"></div></div>
    <div class="zeiten" style="font-size:26px;margin-top:42px">
      <span>{A['pos']}</span><span>{A['dauer']}</span></div>
    <div style="margin-top:42px">{_transport(g, 110, 148, 48)}</div>
  </div>
</div>'''
    return css, body


def rechner():
    g = .78
    css = _css(g)
    zeilen = ''.join(
        f'<div style="display:flex;align-items:baseline;gap:16px;padding:11px 0;'
        f'border-top:1px solid rgba(236,238,239,.12);font-size:21px'
        f'{";color:" + WEISS if i == A["laeuft"] else ";color:" + STUMM}">'
        f'<span style="font-family:{MONO};font-size:17px;'
        f'color:{GRUEN if i == A["laeuft"] else LEISE}">{nr}</span>'
        f'<span style="flex:1;overflow:hidden;white-space:nowrap;text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:17px;color:{LEISE}">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))

    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  gap:70px;padding:46px 70px">
  <div style="flex-shrink:0">{_scheibe(g, 856, 24)}</div>

  <div style="flex:1;min-width:0;align-self:stretch;display:flex;
    flex-direction:column;padding:24px 0">
    {_bib(g, 15, 46)}
    <div style="font-size:56px;font-weight:600;letter-spacing:-.02em;margin-top:auto;
      padding-top:26px">{A['titel']}</div>
    <div style="font-size:24px;color:{STUMM};margin-top:10px">
      {A['interpret']} · {A['album']} · {A['jahr']}</div>
    <div style="margin-top:auto;padding-top:26px">{zeilen}
      <div style="border-top:1px solid rgba(236,238,239,.12)"></div></div>
    <div class="zeiten" style="font-size:19px;margin-top:auto;padding-top:26px">
      <span>{A['pos']}</span><span>{A['dauer']}</span></div>
    <div style="margin-top:24px;display:flex">{_transport(g, 86, 114, 34)}</div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('56', 'Punktring', art, css, body)
