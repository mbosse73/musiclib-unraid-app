# -*- coding: utf-8 -*-
"""51 Tastenfeld — nach dem Raumthermostat (08.43.15).

Die Vorlage teilt das Gerät sauber in zwei Hälften: oben eine schwarze
Glasfläche, die nur anzeigt, unten ein Feld aus weissen Quadraten, das nur
bedient. Nichts überlagert sich, nichts leuchtet ausser einer einzigen grünen
Beschriftung. Übertragen: das Glas zeigt die verstrichene Zeit so gross wie dort
die Temperatur, und das grüne Feld — im Foto das einzige farbige — ist der Weg
in die Sammlung. Der Fortschritt liegt als Haarlinie an der Unterkante des
Glases: sie gehört zur Anzeige, nicht zu den Tasten.
"""
from werkzeug import (A, biblio, lupe, mischen, nexti, prev, pausei, schreibe,
                      wiederholen, MONO, SANS)

BLECH = '#e9e9e7'
BLECH_D = '#cfcfcc'
TASTE = '#fbfbfa'
GLAS = '#0d0e0f'
WEISS = '#f4f5f4'
STUMM = 'rgba(244,245,244,.52)'
LEISE = 'rgba(244,245,244,.20)'
GRAU = '#7c8084'
GRUEN = '#31b356'


def _css(g):
    return f'''
.stage{{background:linear-gradient(150deg,#f4f4f2 0%,#dcdcda 50%,#ececeb 100%);
  font-family:{SANS};color:#2c2e30}}

.geraet{{position:relative;border-radius:{22 * g:.0f}px;overflow:hidden;
  background:linear-gradient(180deg,{BLECH} 0%,{BLECH_D} 100%);
  box-shadow:0 {26 * g:.0f}px {60 * g:.0f}px rgba(40,44,48,.28),
             inset 0 {1 * g:.0f}px 0 rgba(255,255,255,.9)}}

/* Die Glasfläche endet nicht mit einer Kante, sondern mit der Fortschrittslinie */
.glas{{position:relative;background:{GLAS};color:{WEISS}}}
.glas .bahn{{position:absolute;left:0;right:0;bottom:0;height:{3 * g:.0f}px;
  background:{LEISE}}}
.glas .bahn i{{position:absolute;left:0;top:0;bottom:0;background:{WEISS}}}
.marke{{text-transform:uppercase;color:{STUMM};letter-spacing:.2em;font-weight:500}}
.zahl{{font-weight:200;line-height:1;font-variant-numeric:tabular-nums;
  letter-spacing:-.03em}}

/* Das Tastenfeld: Quadrate mit einer Fuge, kein Rahmen um das einzelne Feld */
.feld{{display:grid;background:{BLECH_D}}}
.k{{background:{TASTE};display:flex;align-items:center;justify-content:center;
  gap:{10 * g:.0f}px;color:{GRAU};text-transform:uppercase;font-weight:600;
  box-shadow:inset 0 {1 * g:.0f}px 0 rgba(255,255,255,.9)}}
.k.gruen{{color:{GRUEN}}}
.k.zeichen{{font-size:0}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{STUMM};
  font-variant-numeric:tabular-nums}}
'''


def _glas(g, pad, marke_px, zahl_px, klein_px):
    return f'''<div class="glas" style="padding:{pad}">
  <div style="display:flex;align-items:flex-start;justify-content:space-between">
    <div>
      <div class="marke" style="font-size:{marke_px}px">Spielt</div>
      <div class="marke" style="font-size:{marke_px}px;margin-top:{int(6 * g)}px;
        color:{LEISE}">Titel {A['tracks'][A['laeuft']][0]} von 04</div>
    </div>
    <div style="display:flex;gap:{int(22 * g)}px;align-items:center">
      {mischen(int(klein_px * 1.5), STUMM)}
      {wiederholen(int(klein_px * 1.5), LEISE)}
    </div>
  </div>

  <div class="zahl" style="font-size:{zahl_px}px;margin-top:{int(18 * g)}px">
    {A['pos']}</div>

  <div style="font-size:{klein_px * 1.5:.0f}px;margin-top:{int(20 * g)}px;
    font-weight:300">{A['titel']}</div>
  <div style="font-size:{klein_px}px;color:{STUMM};margin-top:{int(8 * g)}px">
    {A['interpret']} · {A['album']} · {A['jahr']}</div>

  <div class="zeiten" style="font-size:{klein_px * .86:.0f}px;
    margin-top:{int(18 * g)}px">
    <span>{A['pos']}</span><span>{A['dauer']}</span></div>

  <span class="bahn"><i style="width:{A['frac'] * 100:.0f}%"></i></span>
</div>'''


def _feld(g, hoehe, schrift, zeichen, spalten='repeat(3,1fr)'):
    """Die Tastenreihen. Die grüne Taste ist die Sammlung — wie °C|°F im Foto."""
    fuge = max(2, int(3 * g))
    return f'''<div class="feld" style="grid-template-columns:{spalten};
  gap:{fuge}px;padding:{fuge}px 0 0">
  <div class="k zeichen" style="height:{hoehe}px">{mischen(zeichen, GRAU)}</div>
  <div class="k gruen" style="height:{hoehe}px;font-size:{schrift}px;
    letter-spacing:{2 * g:.1f}px">{biblio(zeichen, GRUEN)}Sammlung · {A['sammlung']}</div>
  <div class="k zeichen" style="height:{hoehe}px">{lupe(zeichen, GRAU)}</div>

  <div class="k zeichen" style="height:{hoehe}px">{prev(zeichen, '#3a3d40')}</div>
  <div class="k zeichen" style="height:{hoehe}px">{pausei(int(zeichen * 1.15), '#3a3d40')}</div>
  <div class="k zeichen" style="height:{hoehe}px">{nexti(zeichen, '#3a3d40')}</div>

  <div class="k" style="height:{hoehe}px;font-size:{schrift}px;
    letter-spacing:{2 * g:.1f}px">Leiser</div>
  <div class="k" style="height:{hoehe}px;font-size:{schrift}px;
    letter-spacing:{2 * g:.1f}px">Anzeige</div>
  <div class="k" style="height:{hoehe}px;font-size:{schrift}px;
    letter-spacing:{2 * g:.1f}px">Lauter</div>
</div>'''


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:80px 56px">
  <div class="geraet" style="width:968px">
    {_glas(g, '78px 66px 62px', 24, 216, 32)}
    {_feld(g, 176, 22, 46, 'repeat(3,1fr)')}
  </div>
</div>'''
    return css, body


def rechner():
    g = .78
    css = _css(g)
    zeilen = ''.join(
        f'<div style="display:flex;align-items:baseline;gap:16px;padding:10px 0;'
        f'border-top:1px solid rgba(244,245,244,.14);font-size:20px'
        f'{";color:" + WEISS if i == A["laeuft"] else ";color:" + STUMM}">'
        f'<span style="font-family:{MONO};font-size:16px;color:{LEISE}">{nr}</span>'
        f'<span style="flex:1;overflow:hidden;white-space:nowrap;text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:16px;color:{LEISE}">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))

    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:60px 76px">
  <div class="geraet" style="width:1448px;display:grid;
    grid-template-columns:1fr 520px">
    <div style="position:relative">{_glas(g, '52px 48px 46px', 18, 168, 24)}</div>
    <div style="background:{GLAS};padding:52px 44px 46px;color:{WEISS};
      border-left:3px solid {BLECH_D}">
      <div class="marke" style="font-size:18px">Album</div>
      <div style="font-size:30px;font-weight:300;margin-top:12px">{A['album']}</div>
      <div style="margin-top:20px">{zeilen}
        <div style="border-top:1px solid rgba(244,245,244,.14)"></div></div>
    </div>
    <div style="grid-column:1/-1">{_feld(g, 132, 17, 36)}</div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('51', 'Tastenfeld', art, css, body)
