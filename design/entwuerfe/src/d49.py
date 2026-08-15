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
.stage{{background:linear-gradient(150deg,#c9cdc6 0%,#9aa096 44%,#c6cac3 100%);
  font-family:{SANS};color:{WEISS}}}

/* Das Gehäuse: Kunststoff mit weicher Kante und einem hellen Grat oben */
.schale{{position:relative;border-radius:{26 * g:.0f}px;
  background:linear-gradient(168deg,{GRUEN_H} 0%,{GRUEN} 24%,{GRUEN_D} 100%);
  box-shadow:0 {26 * g:.0f}px {60 * g:.0f}px rgba(30,40,20,.42),
             inset 0 {2 * g:.0f}px 0 rgba(255,255,255,.45)}}

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
    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:70px 44px">
  <div class="schale" style="width:992px;padding:40px 40px 52px">
    <div class="rippen" style="height:64px;margin:6px 0 40px"></div>

    <div class="glas" style="padding:92px 62px 76px">
      <div style="display:flex;justify-content:center">{_bib(g, 28)}</div>

      <div class="uhr" style="font-size:292px;text-align:center;margin-top:40px">
        {A['pos']}</div>

      <div class="zeile" style="font-size:52px;text-align:center;margin-top:52px">
        {A['interpret']}</div>
      <div class="zeile klein" style="font-size:40px;text-align:center;margin-top:16px">
        Jetzt: {A['titel']}</div>

      <div class="bahn" style="height:4px;margin-top:76px">
        <i style="width:{A['frac'] * 100:.0f}%"></i></div>
      <div class="zeiten" style="font-size:25px;margin-top:20px">
        <span>{A['album']} · {A['jahr']}</span><span>{A['dauer']}</span></div>

      <div style="margin-top:70px">{_transport(g, 100, 140, 46)}</div>

      <div style="margin-top:70px">{_liste(g, 30, 24)}
        <div style="border-top:1px solid rgba(246,247,245,.14)"></div></div>
    </div>

    <div class="rippen" style="height:30px;margin-top:40px;opacity:.55"></div>
  </div>
</div>'''
    return css, body


def rechner():
    g = .78
    css = _css(g)
    zeilen = _liste(g, 21, 17)
    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:56px 70px">
  <div class="schale" style="width:1440px;padding:26px;display:flex;gap:26px">
    <div class="rippen quer" style="width:52px;flex-shrink:0"></div>

    <div class="glas" style="flex:1;min-width:0;padding:44px 52px 42px;display:flex;
      gap:56px;align-items:center">
      <div style="flex-shrink:0">
        {_bib(g, 19)}
        <div class="uhr" style="font-size:176px;margin-top:20px">{A['pos']}</div>
        <div class="zeiten" style="font-size:18px;margin-top:14px;width:430px">
          <span>{A['album']} · {A['jahr']}</span><span>{A['dauer']}</span></div>
        <div class="bahn" style="height:3px;margin-top:12px;width:430px">
          <i style="width:{A['frac'] * 100:.0f}%"></i></div>
        <div style="margin-top:34px;width:430px">{_transport(g, 68, 94, 30)}</div>
      </div>

      <div style="flex:1;min-width:0">
        <div class="zeile" style="font-size:40px">{A['interpret']}</div>
        <div class="zeile klein" style="font-size:26px;margin-top:10px">
          Jetzt: {A['titel']}</div>
        <div style="margin-top:24px">{zeilen}
          <div style="border-top:1px solid rgba(246,247,245,.14)"></div></div>
      </div>
    </div>

    <div class="rippen quer" style="width:52px;flex-shrink:0"></div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('49', 'Weckdock', art, css, body)
