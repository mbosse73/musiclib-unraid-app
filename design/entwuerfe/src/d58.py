# -*- coding: utf-8 -*-
"""58 Zeigerfront — aus zwei Fotos derselben Gerätefront (09.18.44 / 09.20.06).

Beide zeigen dasselbe Gerät: links eine breite schwarze Anzeige, rechts eine
Spalte kleiner Tasten und ein grosser silberner Lautstärkering. Nur der Inhalt
der Anzeige wechselt — einmal Cover, Titel und ein blauer Fortschrittsbalken,
einmal zwei Zeigerinstrumente mit rotem Endbereich. Wie schon bei 44 bekommt
deshalb nicht jedes Foto ein eigenes Blatt: der Rechner zeigt die Titelanzeige,
das Telefon die Zeiger. Dieselbe Front, zwei Betriebsarten — genau das, was ein
solcher Verstärker tatsächlich kann.
"""
from werkzeug import (A, biblio, cover, laut, lupe, mischen, nexti, prev, pausei,
                      schreibe, vumeter, MONO, SANS)

FRONT = '#0a0b0c'
GEHAEUSE = '#121315'
WEISS = '#eef0f2'
STUMM = 'rgba(238,240,242,.56)'
LEISE = 'rgba(238,240,242,.22)'
BLAU = '#4fb3e8'
SILBER = ('#f4f5f6', '#c8ccd0', '#6e7377')


def _css(g):
    return f'''
.stage{{background:linear-gradient(165deg,#1c1e20 0%,#0b0c0d 60%,#141618 100%);
  font-family:{SANS};color:{WEISS}}}

.front{{position:relative;background:linear-gradient(180deg,{GEHAEUSE} 0%,#0a0b0c 100%);
  border-radius:{4 * g:.0f}px;
  box-shadow:0 {24 * g:.0f}px {58 * g:.0f}px rgba(0,0,0,.65),
             inset 0 {1 * g:.0f}px 0 rgba(255,255,255,.10)}}
.anzeige{{background:{FRONT};box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(255,255,255,.06)}}

/* Die Tastenspalte sitzt zwischen Anzeige und Ring, mit Fugen dazwischen */
.spalte{{display:flex;flex-direction:column;justify-content:space-between;
  align-items:center}}
.spalte i{{display:flex;align-items:center;justify-content:center;width:100%;
  border-bottom:1px solid rgba(238,240,242,.10)}}
.spalte i:last-child{{border-bottom:0}}

/* Der Ring: gedrehtes Aluminium, innen dunkel */
.ring{{position:relative;border-radius:50%;flex-shrink:0;
  background:conic-gradient({SILBER[1]} 0deg,{SILBER[0]} 60deg,{SILBER[2]} 140deg,
    {SILBER[0]} 220deg,{SILBER[2]} 300deg,{SILBER[1]} 360deg)}}
.ring span{{position:absolute;border-radius:50%;background:{GEHAEUSE};
  box-shadow:inset 0 0 {14 * g:.0f}px rgba(0,0,0,.8)}}

.bahn{{position:relative;background:rgba(238,240,242,.16)}}
.bahn i{{position:absolute;left:0;top:0;bottom:0;background:{BLAU}}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{STUMM};
  font-variant-numeric:tabular-nums}}
.bib{{display:inline-flex;align-items:center;color:{STUMM};font-family:{MONO};
  text-transform:uppercase}}
'''


def _spalte(g, breite, hoehe, zeichen):
    """Die kleinen Tasten am rechten Rand der Anzeige — wie im Foto sechs."""
    stk = [pausei(zeichen, WEISS), prev(zeichen, STUMM), nexti(zeichen, STUMM),
           mischen(zeichen, STUMM), biblio(zeichen, WEISS), lupe(zeichen, STUMM)]
    return (f'<div class="spalte" style="width:{breite}px;height:{hoehe}px">'
            + ''.join(f'<i style="height:{hoehe // len(stk)}px">{s}</i>' for s in stk)
            + '</div>')


def _ring(g, size):
    loch = int(size * .62)
    return (f'<div class="ring" style="width:{size}px;height:{size}px">'
            f'<span style="left:{(size - loch) // 2}px;top:{(size - loch) // 2}px;'
            f'width:{loch}px;height:{loch}px"></span></div>')


def _titelanzeige(g, pad, cover_px, gross, klein):
    return f'''<div class="anzeige" style="flex:1;min-width:0;padding:{pad};
  display:flex;gap:{int(30 * g)}px;align-items:flex-start">
  {cover(cover_px, int(cover_px * .02), '#8f2f22', '#2a0d08')}
  <div style="flex:1;min-width:0;display:flex;flex-direction:column;height:{cover_px}px">
    <div style="font-size:{gross}px;font-weight:500;letter-spacing:-.01em">
      {A['titel']}</div>
    <div style="font-size:{klein * 1.25:.0f}px;color:{WEISS};margin-top:{int(4 * g)}px">
      {A['interpret']}</div>
    <div style="font-size:{klein}px;color:{STUMM}">{A['album']}</div>

    <div style="margin-top:auto">
      <div style="font-size:{klein * .9:.0f}px;color:{STUMM};
        margin-bottom:{int(10 * g)}px">{A['titel'].lower()}</div>
      <div class="bahn" style="height:{int(10 * g)}px">
        <i style="width:{A['frac'] * 100:.0f}%"></i></div>
      <div class="zeiten" style="font-size:{klein * .9:.0f}px;
        margin-top:{int(10 * g)}px">
        <span style="color:{BLAU}">{A['pos']}</span><span>{A['dauer']}</span></div>
      <div style="display:flex;align-items:center;justify-content:space-between;
        margin-top:{int(14 * g)}px">
        <span class="bib" style="gap:{int(10 * g)}px;
          font-size:{klein * .82:.0f}px;letter-spacing:.14em">
          {biblio(int(klein), STUMM)}Sammlung · {A['sammlung']}</span>
        <span style="font-family:{MONO};font-size:{klein * .82:.0f}px;color:{STUMM}">
          {A['jahr']} · Titel {A['tracks'][A['laeuft']][0]}</span>
      </div>
    </div>
  </div>
</div>'''


def _liste(g, schrift, klein):
    return ''.join(
        f'<div style="display:flex;align-items:baseline;gap:{int(16 * g)}px;'
        f'padding:{int(12 * g)}px 0;border-top:1px solid rgba(238,240,242,.12);'
        f'font-size:{schrift}px'
        f'{";color:" + WEISS if i == A["laeuft"] else ";color:" + STUMM}">'
        f'<span style="font-family:{MONO};font-size:{klein}px;'
        f'color:{BLAU if i == A["laeuft"] else LEISE}">{nr}</span>'
        f'<span style="flex:1;overflow:hidden;white-space:nowrap;'
        f'text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:{klein}px;color:{LEISE}">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))


def _zeiger(g, pad, breite, hoehe, klein, liste=''):
    """Die zweite Betriebsart: zwei Instrumente statt Cover und Balken."""
    return f'''<div class="anzeige" style="flex:1;min-width:0;padding:{pad}">
  <div style="display:flex;gap:{int(16 * g)}px">
    {vumeter(breite, hoehe, '#e9e9e7', '#1a1a1a', '#3a3a3a', 'L', A['frac'])}
    {vumeter(breite, hoehe, '#e9e9e7', '#1a1a1a', '#3a3a3a', 'R', A['frac'] * .92)}
  </div>

  <div style="font-size:{klein * 1.7:.0f}px;font-weight:500;margin-top:{int(30 * g)}px">
    {A['titel']}</div>
  <div style="font-size:{klein}px;color:{STUMM};margin-top:{int(8 * g)}px">
    {A['interpret']} · {A['album']} · {A['jahr']}</div>

  <div class="bahn" style="height:{int(9 * g)}px;margin-top:{int(26 * g)}px">
    <i style="width:{A['frac'] * 100:.0f}%"></i></div>
  <div class="zeiten" style="font-size:{klein * .86:.0f}px;margin-top:{int(12 * g)}px">
    <span style="color:{BLAU}">{A['pos']}</span><span>{A['dauer']}</span></div>

  <div style="display:flex;align-items:center;justify-content:space-between;
    margin-top:{int(22 * g)}px">
    <span class="bib" style="gap:{int(10 * g)}px;font-size:{klein * .82:.0f}px;
      letter-spacing:.14em">{biblio(int(klein), STUMM)}Sammlung · {A['sammlung']}</span>
    <span style="display:flex;gap:{int(16 * g)}px;align-items:center">
      {laut(int(klein * 1.1), STUMM)}
      <span style="font-family:{MONO};font-size:{klein * .82:.0f}px;color:{STUMM}">60</span>
    </span>
  </div>

  {f'<div style="margin-top:{int(30 * g)}px">{liste}'
    f'<div style="border-top:1px solid rgba(238,240,242,.12)"></div></div>' if liste else ''}
</div>'''


def telefon():
    """Die Zeiger-Betriebsart — hochkant, wie man ein Gerät auf den Tisch stellt."""
    g = 1.0
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:80px 46px">
  <div class="front" style="width:988px;padding:32px;display:flex;
    flex-direction:column;gap:30px">
    <div style="display:flex;gap:24px">
      {_zeiger(g, '34px 34px 38px', 396, 268, 29, _liste(g, 28, 22))}
      {_spalte(g, 96, 810, 38)}
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;
      padding:0 16px 10px">
      <span style="font-family:{MONO};font-size:23px;letter-spacing:.22em;
        text-transform:uppercase;color:{LEISE}">Musiklib</span>
      {_ring(g, 230)}
    </div>
  </div>
</div>'''
    return css, body


def rechner():
    """Die Titel-Betriebsart — die breite Front, wie sie im Rack steht."""
    g = .80
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:74px 56px">
  <div class="front" style="width:1488px;padding:26px;display:flex;
    align-items:stretch;gap:22px">
    {_titelanzeige(g, '30px 34px', 300, 46, 23)}
    {_spalte(g, 74, 360, 28)}
    <div style="display:flex;align-items:center;padding-left:20px;
      border-left:1px solid rgba(238,240,242,.08)">{_ring(g, 300)}</div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('58', 'Zeigerfront', art, css, body)
