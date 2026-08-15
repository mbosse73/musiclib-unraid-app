# -*- coding: utf-8 -*-
"""49 Weckdock — aus zwei Fotos: der grünen Dockstation (08.39.08) und dem
schwarzen Radiodisplay (09.26.59).

Das erste Foto gibt das Gehäuse: ein grüner Kunststoffblock mit gerippter
Oberseite, in den vorn eine schwarze Glasfläche eingelassen ist. Das zweite gibt
den Inhalt dieser Fläche: eine kleine Zeile oben, darunter eine grosse dünne
Uhrzeit und zwei ruhige Textzeilen. Zusammen ergeben sie einen Wecker, der
Musik spielt: die grosse Zahl ist nicht die Uhrzeit, sondern die verstrichene
Zeit, und die kleine Zeile oben — dort, wo im Foto „Internet radio" steht — ist
der Weg in die Sammlung.
"""
from werkzeug import A, biblio, mischen, nexti, prev, pausei, schreibe, MONO, SANS

GRUEN = '#86c232'
GRUEN_D = '#63901f'
GRUEN_H = '#a3d95a'
GLAS = '#08090a'
WEISS = '#f6f7f5'
STUMM = 'rgba(246,247,245,.56)'
LEISE = 'rgba(246,247,245,.26)'


def _css(g):
    return f'''
/* Das Gehäuse ist die ganze Fläche: der Kunststoff liegt auf der Bühne selbst,
   nicht als Gerät auf einem Tisch. */
.stage{{background:linear-gradient(168deg,{GRUEN_H} 0%,{GRUEN} 24%,{GRUEN_D} 100%);
  font-family:{SANS};color:{WEISS}}}
.stage::before{{content:"";position:absolute;inset:0;pointer-events:none;
  box-shadow:inset 0 {3 * g:.0f}px 0 rgba(255,255,255,.45),
             inset 0 {-3 * g:.0f}px {30 * g:.0f}px rgba(20,30,10,.28)}}

/* Die Rippen der Oberseite — im Foto das einzige Muster am ganzen Block */
.rippen{{border-radius:{8 * g:.0f}px;
  background:repeating-linear-gradient(90deg,
    rgba(0,0,0,.16) 0 {5 * g:.0f}px,rgba(255,255,255,.20) {5 * g:.0f}px {12 * g:.0f}px)}}
.rippen.quer{{background:repeating-linear-gradient(180deg,
    rgba(0,0,0,.16) 0 {5 * g:.0f}px,rgba(255,255,255,.20) {5 * g:.0f}px {12 * g:.0f}px)}}

/* Die Glasfläche sitzt im Kunststoff, nicht darauf */
.glas{{position:relative;background:{GLAS};border-radius:{14 * g:.0f}px;
  box-shadow:inset 0 0 0 {2 * g:.0f}px rgba(0,0,0,.55),
             inset 0 {3 * g:.0f}px {10 * g:.0f}px rgba(0,0,0,.9),
             0 0 0 {2 * g:.0f}px rgba(255,255,255,.22)}}

.uhr{{font-weight:200;letter-spacing:-.02em;font-variant-numeric:tabular-nums;
  line-height:1}}
.zeile{{font-weight:300}}
.klein{{color:{STUMM};font-weight:400}}

.bahn{{position:relative;background:{LEISE}}}
.bahn i{{position:absolute;left:0;top:0;bottom:0;background:{WEISS}}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{STUMM};
  font-variant-numeric:tabular-nums}}

/* Bibliothek: die kleine Zeile über der Uhr, wie „Internet radio" im Foto */
.bib{{display:inline-flex;align-items:center;color:{WEISS};font-weight:400}}
.taste{{flex-shrink:0;display:flex;align-items:center;justify-content:center;
  border-radius:50%;background:rgba(246,247,245,.10)}}
'''


def _bib(g, schrift):
    return (f'<span class="bib" style="gap:{int(12 * g)}px;font-size:{schrift}px;'
            f'letter-spacing:{1.6 * g:.1f}px">{biblio(int(schrift * 1.2), WEISS)}'
            f'Sammlung · {A["sammlung"]}</span>')


def _transport(g, klein, gross_, luecke):
    return (f'<div style="display:flex;align-items:center;justify-content:center;'
            f'gap:{luecke}px">'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{mischen(int(klein * .40), STUMM)}</div>'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{prev(int(klein * .42), WEISS)}</div>'
            f'<div class="taste" style="width:{gross_}px;height:{gross_}px;'
            f'background:rgba(246,247,245,.16)">{pausei(int(gross_ * .38), WEISS)}</div>'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{nexti(int(klein * .42), WEISS)}</div>'
            f'<div class="taste" style="width:{klein}px;height:{klein}px;opacity:.0"></div>'
            f'</div>')


def _liste(g, schrift, klein):
    return ''.join(
        f'<div style="display:flex;align-items:baseline;gap:{int(18 * g)}px;'
        f'padding:{int(13 * g)}px 0;border-top:1px solid rgba(246,247,245,.14);'
        f'font-size:{schrift}px'
        f'{";color:" + WEISS if i == A["laeuft"] else ";color:" + STUMM}">'
        f'<span style="font-family:{MONO};font-size:{klein}px;color:{LEISE}">{nr}</span>'
        f'<span style="flex:1;overflow:hidden;white-space:nowrap;'
        f'text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:{klein}px;color:{LEISE}">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  padding:46px 40px 52px">
  <div class="rippen" style="height:84px;flex-shrink:0"></div>

  <div class="glas" style="flex:1;min-height:0;margin:40px 0;padding:96px 66px 84px;
    display:flex;flex-direction:column">
    <div style="display:flex;justify-content:center">{_bib(g, 29)}</div>

    <div class="uhr" style="font-size:340px;text-align:center;margin-top:auto">
      {A['pos']}</div>

    <div class="zeile" style="font-size:56px;text-align:center;margin-top:56px">
      {A['interpret']}</div>
    <div class="zeile klein" style="font-size:42px;text-align:center;margin-top:18px">
      Jetzt: {A['titel']}</div>

    <div class="bahn" style="height:4px;margin-top:76px">
      <i style="width:{A['frac'] * 100:.0f}%"></i></div>
    <div class="zeiten" style="font-size:26px;margin-top:22px">
      <span>{A['album']} · {A['jahr']}</span><span>{A['dauer']}</span></div>

    <div style="margin-top:64px">{_transport(g, 106, 148, 48)}</div>

    <div style="margin-top:72px">{_liste(g, 31, 25)}
      <div style="border-top:1px solid rgba(246,247,245,.14)"></div></div>
  </div>

  <div class="rippen" style="height:44px;flex-shrink:0;opacity:.55"></div>
</div>'''
    return css, body


def rechner():
    g = .78
    css = _css(g)
    zeilen = _liste(g, 21, 17)
    body = f'''<div style="position:absolute;inset:0;display:flex;gap:26px;padding:26px">
  <div class="rippen quer" style="width:60px;flex-shrink:0"></div>

  <div class="glas" style="flex:1;min-width:0;padding:52px 60px 50px;display:flex;
    gap:64px;align-items:stretch">
    <div style="width:520px;flex-shrink:0;display:flex;flex-direction:column">
      {_bib(g, 20)}
      <div class="uhr" style="font-size:212px;margin-top:auto">{A['pos']}</div>
      <div class="zeiten" style="font-size:19px;margin-top:22px">
        <span>{A['album']} · {A['jahr']}</span><span>{A['dauer']}</span></div>
      <div class="bahn" style="height:3px;margin-top:12px">
        <i style="width:{A['frac'] * 100:.0f}%"></i></div>
      <div style="margin-top:auto;padding-top:40px">{_transport(g, 74, 102, 32)}</div>
    </div>

    <div style="flex:1;min-width:0;display:flex;flex-direction:column">
      <div class="zeile" style="font-size:46px">{A['interpret']}</div>
      <div class="zeile klein" style="font-size:28px;margin-top:10px">
        Jetzt: {A['titel']}</div>
      <div style="margin-top:auto;padding-top:32px">{zeilen}
        <div style="border-top:1px solid rgba(246,247,245,.14)"></div></div>
    </div>
  </div>

  <div class="rippen quer" style="width:60px;flex-shrink:0"></div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('49', 'Weckdock', art, css, body)
