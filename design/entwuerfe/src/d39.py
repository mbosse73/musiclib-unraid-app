# -*- coding: utf-8 -*-
"""39 Kippschalter — nach „MUSIC ON / WORLD OFF" (23.30.54).

Die Vorlage ist reine Typografie auf Schwarz: zwei Kippschalter, deren Kapsel
zugleich der erste Buchstabe des Wortes ist — der weisse Schalter bildet das O
von ON, der rote das O von OFF. Übertragen: der obere Schalter *ist* die
Wiedergabe, der untere schaltet die Welt ab (Stille). Sonst gibt es nichts als
Schrift, eine Haarlinie und die Zeiten.
"""
from werkzeug import A, biblio, schreibe, SANS, MONO

WEISS = '#f4f4f2'
ROT = '#e0342c'
GRAU = 'rgba(244,244,242,.45)'


def _css(g):
    return f'''
.stage{{background:#000;font-family:{SANS};color:{WEISS}}}
.wort{{display:flex;align-items:center;line-height:.86;font-weight:800;letter-spacing:-.03em}}

/* Die Kapsel ist der Buchstabe: sie sitzt bündig am Wort, kein Abstand */
.schalter{{position:relative;border-radius:999px;flex-shrink:0}}
.schalter b{{position:absolute;top:50%;transform:translateY(-50%);border-radius:50%;display:block}}
.an{{border:{5 * g:.0f}px solid {WEISS}}}
.an b{{background:{WEISS}}}
.aus{{border:{5 * g:.0f}px solid {ROT}}}
.aus b{{background:transparent;border:{4 * g:.0f}px solid {WEISS}}}

.ueber{{letter-spacing:{18 * g:.0f}px;font-weight:400;text-transform:uppercase;color:{WEISS}}}
.linie{{position:relative;height:{2 * g:.0f}px;background:rgba(244,244,242,.22)}}
.linie i{{position:absolute;left:0;top:0;bottom:0;background:{WEISS}}}
.linie b{{position:absolute;top:50%;transform:translate(-50%,-50%);border-radius:50%;
  background:{WEISS}}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{GRAU};
  font-variant-numeric:tabular-nums}}

/* Bibliothek: derselbe Umriss wie die Schalter, damit sie dazugehört */
.bib{{display:inline-flex;align-items:center;border-radius:999px;
  border:{2 * g:.0f}px solid rgba(244,244,242,.40);text-transform:uppercase}}
.pfeil{{background:none;display:flex;align-items:center;justify-content:center}}
'''


def _schalter(g, art, breite, hoehe, wort, schrift):
    """art: 'an' (Knopf rechts, weiss) oder 'aus' (Knopf links, rot)."""
    knopf = hoehe - int(20 * g)
    seite = (f'right:{int(8 * g)}px' if art == 'an' else f'left:{int(8 * g)}px')
    farbe = WEISS if art == 'an' else ROT
    return (f'<div class="wort" style="font-size:{schrift}px;color:{farbe}">'
            f'<span class="schalter {art}" style="width:{breite}px;height:{hoehe}px">'
            f'<b style="{seite};width:{knopf}px;height:{knopf}px"></b></span>'
            f'<span style="margin-left:{int(-6 * g)}px">{wort}</span></div>')


def _pfeile(g, size, farbe=WEISS):
    sw = 2.4 * g
    zurueck = (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
               f'stroke="{farbe}" stroke-width="{sw}" stroke-linecap="round" '
               f'stroke-linejoin="round"><path d="M15 5l-8 7 8 7"/></svg>')
    vor = (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
           f'stroke="{farbe}" stroke-width="{sw}" stroke-linecap="round" '
           f'stroke-linejoin="round"><path d="M9 5l8 7-8 7"/></svg>')
    return zurueck, vor


def _bib(g, schrift, hoehe):
    return (f'<span class="bib" style="height:{hoehe}px;padding:0 {int(30 * g)}px;'
            f'gap:{int(16 * g)}px;font-size:{schrift}px;letter-spacing:{4 * g:.1f}px">'
            f'{biblio(int(schrift * 1.25), WEISS)}Sammlung · {A["sammlung"]}</span>')


def telefon():
    g = 1.0
    zurueck, vor = _pfeile(g, 66)
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;padding:150px 76px 130px;
  display:flex;flex-direction:column">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <span class="ueber" style="font-size:23px">Musiklib</span>
    {_bib(g, 21, 68)}
  </div>

  <div style="margin-top:auto;margin-bottom:auto">
    <div class="ueber" style="font-size:38px;margin-bottom:26px">Musik</div>
    {_schalter(g, 'an', 235, 128, 'N', 168)}
    <div class="ueber" style="font-size:38px;margin:74px 0 26px">Welt</div>
    {_schalter(g, 'aus', 235, 128, 'FF', 168)}
  </div>

  <div style="font-size:52px;font-weight:700;letter-spacing:-.02em">{A['titel']}</div>
  <div style="font-size:30px;color:{GRAU};margin-top:12px">{A['interpret']} · {A['album']}</div>

  <div class="linie" style="margin-top:44px">
    <i style="width:{A['frac'] * 100:.0f}%"></i>
    <b style="left:{A['frac'] * 100:.0f}%;width:22px;height:22px"></b></div>
  <div class="zeiten" style="font-size:25px;margin-top:20px">
    <span>{A['pos']}</span><span>{A['dauer']}</span></div>

  <div style="display:flex;align-items:center;justify-content:center;gap:120px;margin-top:56px">
    <span class="pfeil">{zurueck}</span><span class="pfeil">{vor}</span></div>
</div>'''
    return css, body


def rechner():
    g = .72
    zurueck, vor = _pfeile(g, 48)
    css = _css(g)
    zeilen = ''.join(
        f'<div style="display:flex;align-items:center;gap:22px;padding:14px 0;'
        f'border-top:1px solid rgba(244,244,242,.14);font-size:24px'
        f'{";font-weight:700" if i == A["laeuft"] else f";color:{GRAU}"}">'
        f'<span style="font-family:{MONO};font-size:20px;color:{GRAU}">{nr}</span>'
        f'<span style="flex:1;overflow:hidden;white-space:nowrap;text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:20px;color:{GRAU}">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))

    body = f'''<div style="position:absolute;inset:0;padding:74px 92px;display:flex;
  flex-direction:column">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <span class="ueber" style="font-size:17px">Musiklib</span>
    {_bib(g, 15, 48)}
  </div>

  <div style="display:flex;gap:96px;align-items:center;flex:1;min-height:0">
    <div style="flex-shrink:0">
      <div class="ueber" style="font-size:26px;margin-bottom:18px">Musik</div>
      {_schalter(g, 'an', 168, 92, 'N', 120)}
      <div class="ueber" style="font-size:26px;margin:46px 0 18px">Welt</div>
      {_schalter(g, 'aus', 168, 92, 'FF', 120)}
    </div>

    <div style="flex:1;min-width:0">
      <div style="font-size:56px;font-weight:700;letter-spacing:-.02em">{A['titel']}</div>
      <div style="font-size:24px;color:{GRAU};margin-top:10px">
        {A['interpret']} · {A['album']} · {A['jahr']}</div>
      <div style="margin-top:26px">{zeilen}</div>
      <div class="linie" style="margin-top:34px">
        <i style="width:{A['frac'] * 100:.0f}%"></i>
        <b style="left:{A['frac'] * 100:.0f}%;width:16px;height:16px"></b></div>
      <div class="zeiten" style="font-size:19px;margin-top:14px">
        <span>{A['pos']}</span><span>{A['dauer']}</span></div>
      <div style="display:flex;align-items:center;gap:74px;margin-top:30px">
        <span class="pfeil">{zurueck}</span><span class="pfeil">{vor}</span></div>
    </div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('39', 'Kippschalter', art, css, body)
