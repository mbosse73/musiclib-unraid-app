# -*- coding: utf-8 -*-
"""54 Roséblech — nach der roségoldenen Bedienplatte (08.52.20).

Von allen Fotos im Ordner ist dieses schon fast ein Spieler: eine gebürstete
roségoldene Platte, oben ein Schieber mit Lautsprecherknopf, in der Mitte eine
fette Zeile „Interpret / Titel", darunter vier dicke Metalltasten — zurück, eine
rote in der Mitte, vor, und eine mit dem Listenzeichen — und ganz unten die
Dauer als Text. Übertragen ist daran wenig zu tun; die vierte Taste, im Foto
schon eine Liste, ist der Weg in die Sammlung. Dazugekommen ist eine zweite
Schiene für den Fortschritt, gebaut wie der Lautstärkeschieber, damit sie zur
Platte gehört statt auf ihr zu liegen.
"""
from werkzeug import A, biblio, laut, nexti, prev, pausei, schreibe, MONO, SANS

BLECH_H = '#e6c6ba'
BLECH = '#d3ac9f'
BLECH_D = '#b98c7c'
TINTE = '#241a16'
STUMM = 'rgba(36,26,22,.62)'
ROT = '#b8352c'
SILBER = ('#fbfaf9', '#d6d2ce', '#a19c97')


def _css(g):
    return f'''
/* Gebürstetes Blech, und zwar die ganze Fläche: ein Verlauf plus feine
   Striche in Laufrichtung */
.stage{{background:linear-gradient(158deg,{BLECH_H} 0%,{BLECH} 42%,{BLECH_D} 100%);
  font-family:{SANS};color:{TINTE}}}
.stage::before{{content:"";position:absolute;inset:0;opacity:.28;pointer-events:none;
  background:repeating-linear-gradient(112deg,rgba(255,255,255,.5) 0 1px,
    rgba(0,0,0,.05) 1px 3px)}}
.platte{{position:absolute;inset:0;display:flex}}

/* Schiene: links gefüllt, rechts dunkel — wie der Schieber im Foto */
.schiene{{position:relative;display:flex;align-items:center}}
.schiene .bahn{{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);
  border-radius:999px;background:#3b3330}}
.schiene .bahn i{{position:absolute;left:0;top:0;bottom:0;border-radius:999px;
  background:{ROT}}}
.griff{{position:relative;border-radius:50%;display:flex;align-items:center;
  justify-content:center;flex-shrink:0;
  background:radial-gradient(circle at 34% 26%,{SILBER[0]} 0%,{SILBER[1]} 48%,{SILBER[2]} 100%);
  box-shadow:0 {4 * g:.0f}px {9 * g:.0f}px rgba(0,0,0,.35),
             0 0 0 {2 * g:.0f}px rgba(255,255,255,.55)}}

.zeile{{font-weight:800;letter-spacing:-.02em;text-align:center}}
.dauer{{font-family:{MONO};font-weight:700;text-align:center;
  font-variant-numeric:tabular-nums}}

/* Die Tasten sind Metallzylinder: heller Ring, gewölbte Fläche, harter Schatten */
.taste{{position:relative;flex-shrink:0;border-radius:50%;display:flex;
  align-items:center;justify-content:center;
  background:radial-gradient(circle at 36% 26%,{SILBER[0]} 0%,{SILBER[1]} 52%,{SILBER[2]} 100%);
  box-shadow:0 {8 * g:.0f}px {16 * g:.0f}px rgba(0,0,0,.38),
             0 0 0 {5 * g:.0f}px rgba(255,255,255,.42),
             inset 0 {-3 * g:.0f}px {6 * g:.0f}px rgba(0,0,0,.22)}}
.taste.rot{{background:radial-gradient(circle at 36% 26%,#e0574c 0%,{ROT} 54%,#7e2119 100%);
  box-shadow:0 {8 * g:.0f}px {16 * g:.0f}px rgba(0,0,0,.42),
             0 0 0 {5 * g:.0f}px rgba(255,255,255,.32),
             inset 0 {-3 * g:.0f}px {6 * g:.0f}px rgba(0,0,0,.3)}}
'''


def _schiene(g, hoehe, griff, frac, zeichen=None):
    inhalt = zeichen or ''
    return (f'<div class="schiene" style="height:{griff}px">'
            f'<span class="bahn" style="height:{hoehe}px">'
            f'<i style="width:{frac * 100:.0f}%"></i></span>'
            f'<span class="griff" style="width:{griff}px;height:{griff}px;'
            f'margin-left:calc({frac * 100:.0f}% - {griff / 2:.0f}px)">{inhalt}</span>'
            f'</div>')


def _tasten(g, size, gross_, luecke):
    return (f'<div style="display:flex;align-items:center;justify-content:center;'
            f'gap:{luecke}px">'
            f'<div class="taste" style="width:{size}px;height:{size}px">'
            f'{prev(int(size * .40), "#3a3330")}</div>'
            f'<div class="taste rot" style="width:{gross_}px;height:{gross_}px">'
            f'{pausei(int(gross_ * .38), "#fdeae7")}</div>'
            f'<div class="taste" style="width:{size}px;height:{size}px">'
            f'{nexti(int(size * .40), "#3a3330")}</div>'
            f'<div class="taste" style="width:{size}px;height:{size}px">'
            f'{biblio(int(size * .42), "#3a3330")}</div></div>')


def _zeilen(g, schrift, klein):
    return ''.join(
        f'<div style="display:flex;align-items:baseline;gap:{int(18 * g)}px;'
        f'padding:{int(12 * g)}px 0;border-top:1px solid rgba(36,26,22,.22);'
        f'font-size:{schrift}px'
        f'{";font-weight:800" if i == A["laeuft"] else ";color:" + STUMM}">'
        f'<span style="font-family:{MONO};font-size:{klein}px;color:{STUMM}">{nr}</span>'
        f'<span style="flex:1;overflow:hidden;white-space:nowrap;'
        f'text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:{klein}px;color:{STUMM}">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div class="platte" style="flex-direction:column;padding:90px 76px 96px">
  {_schiene(g, 10, 82, .48, laut(36, '#3a3330'))}

  <div class="zeile" style="font-size:62px;margin-top:auto;padding-top:76px">
    {A['interpret']} / {A['titel']}</div>
  <div class="zeile" style="font-size:30px;color:{STUMM};font-weight:500;
    margin-top:14px">{A['album']} · {A['jahr']}</div>

  <div style="margin-top:74px">{_tasten(g, 162, 190, 36)}</div>

  <div class="dauer" style="font-size:36px;margin-top:74px">
    Dauer: {A['pos']} / {A['dauer']}</div>

  <div style="margin-top:36px">{_schiene(g, 8, 48, A['frac'])}</div>

  <div style="display:flex;justify-content:space-between;font-family:{MONO};
    font-size:24px;color:{STUMM};margin-top:14px">
    <span>Titel {A['tracks'][A['laeuft']][0]} von 04</span>
    <span>Sammlung · {A['sammlung']}</span></div>

  <div style="margin-top:auto;padding-top:54px">{_zeilen(g, 31, 25)}
    <div style="border-top:1px solid rgba(36,26,22,.22)"></div></div>
</div>'''
    return css, body


def rechner():
    g = .78
    css = _css(g)
    zeilen = _zeilen(g, 21, 17)
    body = f'''<div class="platte" style="padding:64px 72px;gap:66px;align-items:stretch">
  <div style="flex:1;min-width:0;display:flex;flex-direction:column">
    {_schiene(g, 8, 62, .48, laut(26, '#3a3330'))}
    <div class="zeile" style="font-size:50px;margin-top:auto;padding-top:44px">
      {A['interpret']} / {A['titel']}</div>
    <div class="zeile" style="font-size:23px;color:{STUMM};font-weight:500;
      margin-top:10px">{A['album']} · {A['jahr']}</div>
    <div style="margin-top:auto;padding-top:44px">{_tasten(g, 122, 144, 28)}</div>
    <div class="dauer" style="font-size:27px;margin-top:auto;padding-top:42px">
      Dauer: {A['pos']} / {A['dauer']}</div>
    <div style="margin-top:24px">{_schiene(g, 7, 38, A['frac'])}</div>
  </div>

  <div style="width:490px;flex-shrink:0;display:flex;flex-direction:column">
    <div style="font-family:{MONO};font-size:17px;letter-spacing:.18em;
      text-transform:uppercase;color:{STUMM}">Sammlung · {A['sammlung']}</div>
    <div style="font-size:34px;font-weight:800;margin-top:12px;letter-spacing:-.02em">
      {A['album']}</div>
    <div style="margin:auto 0">{zeilen}
      <div style="border-top:1px solid rgba(36,26,22,.22)"></div></div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('54', 'Roseblech', art, css, body)
