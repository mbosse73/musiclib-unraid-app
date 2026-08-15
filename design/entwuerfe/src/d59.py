# -*- coding: utf-8 -*-
"""59 Skalenblech — nach der Kassettendeck-Front mit Senderskala (09.25.44).

Die Vorlage ist ein weiss lackiertes Gerät mit Chromkanten: links die
Kassettenklappe mit dem kleinen Fenster und dem Wort AUTO STOP, rechts ein
winziges Zeigerinstrument und darunter die Senderskala — zwei Zahlenreihen, AM
und FM, quer darüber ein roter Strich. Übertragen ist der rote Strich der
Fortschritt: er steht nicht auf einer Frequenz, sondern auf der Minute. Die
Skala trägt oben die Minuten und unten die Titelnummern, und weil man auf einer
Skala immer auf einen Punkt zeigt, ist genau sie die Spulfläche.
"""
from werkzeug import (A, biblio, kassette, nexti, prev, pausei, schreibe,
                      vumeter, MONO, SANS)

BLECH = '#eceae4'
BLECH_D = '#d3d0c8'
CHROM = ('#ffffff', '#c8c6c0', '#8e8b85')
TINTE = '#2f2e2b'
STUMM = 'rgba(47,46,43,.58)'
ROT = '#cc2a22'
FENSTER = '#17181a'


def _css(g):
    return f'''
/* Die Frontplatte ist die Bühne, oben und unten von einer Chromleiste begrenzt */
.stage{{background:linear-gradient(180deg,{BLECH} 0%,{BLECH_D} 100%);
  font-family:{SANS};color:{TINTE}}}
.geraet{{position:absolute;inset:0;display:flex;flex-direction:column}}

/* Chromleiste: drei Streifen, hell-dunkel-hell — mehr braucht es nicht */
.chrom{{background:linear-gradient(180deg,{CHROM[0]} 0%,{CHROM[1]} 46%,
  {CHROM[2]} 54%,{CHROM[0]} 100%)}}

.klappe{{position:relative;background:linear-gradient(180deg,#f6f5f1 0%,{BLECH} 100%);
  border-radius:{3 * g:.0f}px;
  box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(0,0,0,.16),
             0 {2 * g:.0f}px {4 * g:.0f}px rgba(0,0,0,.10)}}
.sicht{{background:{FENSTER};border-radius:{2 * g:.0f}px;overflow:hidden;
  display:flex;align-items:center;justify-content:center;
  box-shadow:inset 0 0 {10 * g:.0f}px rgba(0,0,0,.9)}}
.wort{{text-transform:uppercase;letter-spacing:.2em;color:{STUMM}}}

/* Die Skala: zwei Zahlenreihen, Teilstriche dazwischen, ein roter Strich quer */
.skala{{position:relative;background:#fbfaf7;border-radius:{2 * g:.0f}px;
  box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(0,0,0,.18)}}
.skala .reihe{{display:flex;justify-content:space-between;font-family:{MONO};
  color:{TINTE};font-variant-numeric:tabular-nums}}
.skala .striche{{display:flex;justify-content:space-between;align-items:center}}
.skala .striche i{{width:1px;background:rgba(47,46,43,.45)}}
.skala .zeiger{{position:absolute;top:0;bottom:0;width:{3 * g:.0f}px;background:{ROT};
  box-shadow:0 0 {6 * g:.0f}px rgba(204,42,34,.6)}}

/* Kippschalter: Chromhülse mit schwarzem Hebel */
.kipp{{display:flex;flex-direction:column;align-items:center;gap:{8 * g:.0f}px}}
.huelse{{position:relative;border-radius:{4 * g:.0f}px;
  background:linear-gradient(180deg,{CHROM[0]} 0%,{CHROM[1]} 50%,{CHROM[2]} 100%);
  box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(0,0,0,.2)}}
.huelse b{{position:absolute;left:50%;transform:translateX(-50%);border-radius:999px;
  background:linear-gradient(180deg,#4a4a48 0%,#1b1b1a 100%)}}

.taste{{flex-shrink:0;display:flex;align-items:center;justify-content:center;
  border-radius:{4 * g:.0f}px;
  background:linear-gradient(180deg,#fbfaf7 0%,#dedbd4 100%);
  box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(0,0,0,.18),
             0 {2 * g:.0f}px {4 * g:.0f}px rgba(0,0,0,.14)}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{STUMM};
  font-variant-numeric:tabular-nums}}
.bib{{display:inline-flex;align-items:center;border-radius:{3 * g:.0f}px;
  background:linear-gradient(180deg,#fbfaf7 0%,#dedbd4 100%);color:{TINTE};
  text-transform:uppercase;font-weight:700;
  box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(0,0,0,.18)}}
'''


def _skala(g, hoehe, schrift, strich_h):
    minuten = ''.join(f'<span>{m}</span>' for m in range(0, 6))
    titel = ''.join(f'<span>{n}</span>' for n, _, _ in A['tracks'])
    striche = ''.join(f'<i style="height:{strich_h if i % 5 else strich_h * 1.7:.0f}px">'
                      f'</i>' for i in range(41))
    return f'''<div class="skala" style="padding:{int(12 * g)}px {int(16 * g)}px">
  <div class="reihe" style="font-size:{schrift}px">
    <span class="wort" style="font-size:{schrift * .8:.0f}px">Min</span>{minuten}</div>
  <div class="striche" style="height:{hoehe}px">{striche}</div>
  <div class="reihe" style="font-size:{schrift}px">
    <span class="wort" style="font-size:{schrift * .8:.0f}px">Titel</span>{titel}</div>
  <span class="zeiger" style="left:calc({A['frac'] * 100:.0f}% - {1.5 * g:.0f}px)"></span>
</div>'''


def _kipp(g, breite, hoehe, hebel, schrift, name, an):
    oben = f'top:{int(hoehe * .12)}px' if an else f'bottom:{int(hoehe * .12)}px'
    return (f'<div class="kipp"><div class="huelse" style="width:{breite}px;'
            f'height:{hoehe}px"><b style="{oben};width:{hebel}px;'
            f'height:{int(hoehe * .46)}px"></b></div>'
            f'<span class="wort" style="font-size:{schrift}px">{name}</span></div>')


def _klappe(g, breite, hoehe, wort_px):
    band = kassette(int(breite * .80), int(breite * .80 * .62), '#2f3336', '#d9702c')
    hoch = f'height:{hoehe}px;' if hoehe else 'align-self:stretch;'
    return f'''<div class="klappe" style="width:{breite}px;{hoch}
  padding:{int(20 * g)}px;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:{int(18 * g)}px">
  <span class="wort" style="font-size:{wort_px}px">Kind of Blue</span>
  <div class="sicht" style="width:{int(breite * .88)}px;
    height:{int(hoehe * .46) if hoehe else int(breite * .62)}px">
    {band}</div>
  <span class="wort" style="font-size:{wort_px}px">Auto weiter</span>
</div>'''


def _tasten(g, breite, hoehe, zeichen, luecke):
    return (f'<div style="display:flex;gap:{luecke}px">'
            f'<div class="taste" style="width:{breite}px;height:{hoehe}px">'
            f'{prev(zeichen, TINTE)}</div>'
            f'<div class="taste" style="width:{int(breite * 1.6)}px;height:{hoehe}px">'
            f'{pausei(zeichen, TINTE)}</div>'
            f'<div class="taste" style="width:{breite}px;height:{hoehe}px">'
            f'{nexti(zeichen, TINTE)}</div></div>')


def _bib(g, schrift, hoehe):
    return (f'<span class="bib" style="height:{hoehe}px;padding:0 {int(20 * g)}px;'
            f'gap:{int(11 * g)}px;font-size:{schrift}px;letter-spacing:{2.2 * g:.1f}px">'
            f'{biblio(int(schrift * 1.3), TINTE)}Sammlung · {A["sammlung"]}</span>')


def _zeilen(g, schrift, klein):
    return ''.join(
        f'<div style="display:flex;align-items:baseline;gap:{int(16 * g)}px;'
        f'padding:{int(11 * g)}px 0;border-top:1px solid rgba(47,46,43,.20);'
        f'font-size:{schrift}px'
        f'{";font-weight:700" if i == A["laeuft"] else ";color:" + STUMM}">'
        f'<span style="font-family:{MONO};font-size:{klein}px;color:{STUMM}">{nr}</span>'
        f'<span style="flex:1;overflow:hidden;white-space:nowrap;'
        f'text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:{klein}px;color:{STUMM}">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))


def rechner():
    g = .78
    css = _css(g)
    zeilen = _zeilen(g, 21, 17)
    body = f'''<div class="geraet">
  <div class="chrom" style="height:8px;flex-shrink:0"></div>
  <div style="flex:1;min-height:0;padding:44px 48px 48px;display:flex;gap:44px">
      {_klappe(g, 470, 0, 17)}

      <div style="flex:1;min-width:0;display:flex;flex-direction:column">
        <div style="display:flex;align-items:flex-start;gap:30px">
          <div style="flex:1;min-width:0">
            <div style="font-size:40px;font-weight:700;letter-spacing:-.02em">
              {A['titel']}</div>
            <div style="font-size:21px;color:{STUMM};margin-top:8px">
              {A['interpret']} · {A['album']} · {A['jahr']}</div>
            <div style="margin-top:16px">{zeilen}
              <div style="border-top:1px solid rgba(47,46,43,.20)"></div></div>
          </div>
          {vumeter(260, 130, '#f4f3ef', '#1a1a1a', '#3a3a3a', '', A['frac'])}
        </div>

        <div style="margin-top:auto;padding-top:30px">{_skala(g, 34, 20, 9)}</div>
        <div class="zeiten" style="font-size:19px;margin-top:12px">
          <span>{A['pos']}</span><span>{A['dauer']}</span></div>

        <div style="display:flex;align-items:center;justify-content:space-between;
          margin-top:auto;padding-top:30px">
          <div style="display:flex;align-items:center;gap:32px">
            {_tasten(g, 94, 76, 34, 16)}
            {_kipp(g, 38, 78, 14, 14, 'Zufall', False)}
            {_kipp(g, 38, 78, 14, 14, 'Wdh.', True)}
          </div>
          {_bib(g, 16, 56)}
        </div>
      </div>
  </div>
  <div class="chrom" style="height:8px;flex-shrink:0"></div>
</div>'''
    return css, body


def bau():
    # Nur der Rechner: das Hochformat ist auf Wunsch des Eigentuemers entfallen.
    css, body = rechner()
    yield schreibe('59', 'Skalenblech', 'pc', css, body)
