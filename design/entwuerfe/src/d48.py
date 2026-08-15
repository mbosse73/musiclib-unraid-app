# -*- coding: utf-8 -*-
"""48 Siebdruck — nach dem Plakat „VINYL ROOM" (08.38.27).

Die Vorlage ist ein Dreifarben-Siebdruck: oranger Grund, gelbe Versalien im
Anschnitt, darunter ein Plattenladen als schwarzer Holzschnitt mit cremefarbenen
Lichtern. Übertragen: der Titel steht oben im selben Gelb und derselben Enge,
das Regal darunter ist die Sammlung — jede Platte im Bild ist ein Album, die
laufende trägt als einzige das rote Label. Die Fortschrittsleiste ist ein
Farbstreifen wie aus dem Rakel gezogen, mit sichtbarem Passerversatz.
"""
from werkzeug import A, biblio, lupe, nexti, prev, pausei, schreibe, COND, MONO, SANS

ORANGE = '#d4502a'
GELB = '#e9b43e'
SCHWARZ = '#17150f'
CREME = '#ead8ac'
ROT = '#c0301c'


def _css(g):
    return f'''
.stage{{background:{ORANGE};font-family:{SANS};color:{SCHWARZ}}}

/* Gelbe Versalien, eng gesetzt und im Anschnitt — wie gedruckt, nicht gesetzt */
.kopf{{font-family:{COND};font-weight:800;color:{GELB};line-height:.84;
  letter-spacing:-.01em;text-transform:uppercase}}

/* Passerversatz: dieselbe Zeile ein Haar daneben in Schwarz */
.passer{{position:relative}}
.passer .unter{{position:absolute;left:{3 * g:.0f}px;top:{4 * g:.0f}px;
  color:{SCHWARZ};opacity:.30}}

.tafel{{background:{CREME};position:relative}}
.tafel .korn{{position:absolute;inset:0;opacity:.16;
  background:repeating-linear-gradient(90deg,{SCHWARZ} 0 1px,transparent 1px 5px)}}

.balken{{position:relative;background:rgba(23,21,15,.22)}}
.balken i{{position:absolute;left:0;top:0;bottom:0;background:{ROT}}}
.balken i::after{{content:"";position:absolute;left:0;right:0;top:0;
  height:{3 * g:.0f}px;background:{GELB};opacity:.75}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};
  color:rgba(23,21,15,.62);font-variant-numeric:tabular-nums}}

.taste{{flex-shrink:0;border-radius:50%;background:{SCHWARZ};display:flex;
  align-items:center;justify-content:center}}
.taste.hell{{background:{CREME}}}
.bib{{display:inline-flex;align-items:center;background:{GELB};color:{SCHWARZ};
  text-transform:uppercase;font-weight:800;border-radius:999px}}
'''


def _laden(w, h, aktiv=2):
    """Der Plattenladen als Holzschnitt: Wandrahmen, Regal, drei Plattenspieler."""
    s = []
    # Wand: Reihe kleiner Rahmen, ein paar mit cremefarbenem Innenleben
    rb, rh = w * .118, h * .215
    for i in range(7):
        x = w * .02 + i * (rb + w * .015)
        y = h * .04 + (i % 3) * h * .012
        s.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{rb:.0f}" height="{rh:.0f}" '
                 f'fill="{SCHWARZ}"/>')
        if i % 2:
            s.append(f'<rect x="{x + rb * .16:.0f}" y="{y + rh * .14:.0f}" '
                     f'width="{rb * .68:.0f}" height="{rh * .52:.0f}" fill="{CREME}"/>')
            s.append(f'<circle cx="{x + rb * .5:.0f}" cy="{y + rh * .40:.0f}" '
                     f'r="{rb * .17:.0f}" fill="{SCHWARZ}"/>')
    # Regalbrett
    s.append(f'<rect x="0" y="{h * .30:.0f}" width="{w}" height="{h * .045:.0f}" '
             f'fill="{SCHWARZ}"/>')
    # Drei Plattenspieler nebeneinander, der mittlere gross und vorn
    for k, (cx, cw, cy) in enumerate(((w * .035, w * .28, h * .40),
                                      (w * .350, w * .33, h * .355),
                                      (w * .695, w * .28, h * .40))):
        ch = cw * .74
        s.append(f'<rect x="{cx:.0f}" y="{cy:.0f}" width="{cw:.0f}" height="{ch:.0f}" '
                 f'rx="{cw * .03:.0f}" fill="{CREME}" stroke="{SCHWARZ}" '
                 f'stroke-width="{max(2, w * .004):.0f}"/>')
        pr = ch * .40
        px, py = cx + cw * .46, cy + ch * .52
        s.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{pr:.0f}" fill="{SCHWARZ}"/>')
        for i in range(5):
            s.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{pr * (.42 + i * .11):.1f}" '
                     f'fill="none" stroke="{CREME}" stroke-width="1.4" opacity=".45"/>')
        s.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{pr * .30:.0f}" '
                 f'fill="{ROT if k == 1 else CREME}"/>')
        # Tonarm
        s.append(f'<path d="M{cx + cw * .88:.0f} {cy + ch * .18:.0f} '
                 f'L{px + pr * .70:.0f} {py - pr * .22:.0f}" stroke="{SCHWARZ}" '
                 f'stroke-width="{max(3, w * .006):.0f}" stroke-linecap="round"/>')
    # Vordere Kiste mit aufgestellten Platten
    ky = h * .695
    s.append(f'<rect x="{w * .06:.0f}" y="{ky:.0f}" width="{w * .88:.0f}" '
             f'height="{h - ky:.0f}" fill="{SCHWARZ}"/>')
    for i in range(14):
        x = w * .085 + i * (w * .845 / 14)
        s.append(f'<rect x="{x:.0f}" y="{ky + h * .045:.0f}" width="{w * .033:.0f}" '
                 f'height="{h * .215:.0f}" fill="{CREME if i % 3 else ORANGE}"/>')
    # Holzschnitt-Schraffur quer über alles
    for i in range(int(w / 26)):
        x = i * 26
        s.append(f'<path d="M{x} {h} L{x + h * .34:.0f} 0" stroke="{SCHWARZ}" '
                 f'stroke-width="1" opacity=".10"/>')
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">'
            f'{"".join(s)}</svg>')


def _kopf(g, schrift, z1, z2):
    return (f'<div class="passer">'
            f'<div class="kopf unter" style="font-size:{schrift}px">{z1}<br>{z2}</div>'
            f'<div class="kopf" style="font-size:{schrift}px">{z1}<br>{z2}</div></div>')


def _bib(g, schrift, hoehe):
    return (f'<span class="bib" style="height:{hoehe}px;padding:0 {int(26 * g)}px;'
            f'gap:{int(13 * g)}px;font-size:{schrift}px;letter-spacing:{2.4 * g:.1f}px">'
            f'{biblio(int(schrift * 1.3), SCHWARZ)}Sammlung · {A["sammlung"]}</span>')


def _tafel(g, breite_px, gross, klein, taste, tastegross):
    return f'''<div class="tafel" style="padding:{int(34 * g)}px {int(34 * g)}px {int(32 * g)}px">
  <span class="korn"></span>
  <div style="position:relative">
    <div style="font-size:{gross}px;font-weight:800;letter-spacing:-.02em">
      {A['interpret']}</div>
    <div style="font-size:{klein}px;color:rgba(23,21,15,.66);margin-top:{int(8 * g)}px">
      {A['album']} · {A['jahr']} · Titel {A['tracks'][A['laeuft']][0]} von 04</div>

    <div class="balken" style="height:{int(16 * g)}px;margin-top:{int(26 * g)}px">
      <i style="width:{A['frac'] * 100:.0f}%"></i></div>
    <div class="zeiten" style="font-size:{klein * .86:.0f}px;margin-top:{int(12 * g)}px">
      <span>{A['pos']}</span><span>{A['rest']}</span></div>

    <div style="display:flex;align-items:center;justify-content:center;
      gap:{int(30 * g)}px;margin-top:{int(28 * g)}px">
      <div class="taste" style="width:{taste}px;height:{taste}px">
        {prev(int(taste * .42), CREME)}</div>
      <div class="taste" style="width:{tastegross}px;height:{tastegross}px">
        {pausei(int(tastegross * .40), GELB)}</div>
      <div class="taste" style="width:{taste}px;height:{taste}px">
        {nexti(int(taste * .42), CREME)}</div>
      <div class="taste hell" style="width:{taste}px;height:{taste}px">
        {lupe(int(taste * .40), SCHWARZ)}</div>
    </div>
  </div>
</div>'''


def _regal(g, schrift, klein):
    """Die Titel des Albums als Reihe im Regal — schwarz auf Creme."""
    return ''.join(
        f'<div style="display:flex;align-items:baseline;gap:{int(16 * g)}px;'
        f'padding:{int(9 * g)}px 0;border-top:1px solid rgba(23,21,15,.22);'
        f'font-size:{schrift}px'
        f'{";font-weight:800" if i == A["laeuft"] else ";color:rgba(23,21,15,.62)"}">'
        f'<span style="font-family:{MONO};font-size:{klein}px">{nr}</span>'
        f'<span style="flex:1;overflow:hidden;white-space:nowrap;'
        f'text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:{klein}px">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column">
  <div style="padding:88px 66px 0">
    <div style="display:flex;justify-content:flex-end;margin-bottom:24px">{_bib(g, 21, 64)}</div>
    {_kopf(g, 172, 'Blue in', 'Green')}
  </div>

  <div style="margin-top:38px;line-height:0">{_laden(1080, 1170)}</div>

  <div style="padding:36px 66px 84px">{_tafel(g, 948, 52, 27, 96, 132)}</div>
</div>'''
    return css, body


def rechner():
    g = .74
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;display:flex">
  <div style="width:790px;flex-shrink:0;padding:58px 0 54px 72px;display:flex;
    flex-direction:column">
    {_kopf(g, 124, 'Blue in', 'Green')}
    <div style="margin-top:26px;display:flex;align-items:center;gap:26px">
      {_bib(g, 16, 50)}
      <span style="font-family:{MONO};font-size:15px;letter-spacing:.16em;
        text-transform:uppercase;color:rgba(23,21,15,.55)">Kind of Blue · 1959</span>
    </div>
    <div style="margin-top:22px;padding-right:56px">{_regal(g, 21, 16)}
      <div style="border-top:1px solid rgba(23,21,15,.22)"></div></div>
    <div style="margin-top:auto">{_tafel(g, 700, 40, 21, 70, 96)}</div>
  </div>
  <div style="flex:1;min-width:0;display:flex;align-items:flex-end;line-height:0">
    {_laden(810, 1000)}
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('48', 'Siebdruck', art, css, body)
