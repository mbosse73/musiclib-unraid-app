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
/* Die Front füllt die Bühne — man steht davor, nicht im Zimmer daneben */
.stage{{background:linear-gradient(180deg,{GEHAEUSE} 0%,#0a0b0c 100%);
  font-family:{SANS};color:{WEISS}}}
.stage::before{{content:"";position:absolute;inset:0;pointer-events:none;
  box-shadow:inset 0 {1 * g:.0f}px 0 rgba(255,255,255,.10)}}
.front{{position:absolute;inset:0;display:flex}}
.anzeige{{background:{FRONT};box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(255,255,255,.06)}}
/* Hochkant füllen die beiden Instrumente den Platz, der übrig bleibt */
.mess{{flex:1;min-height:0}}
.mess svg{{flex:1;min-height:0;width:100%;height:100%}}

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


def _spalte(g, breite, hoehe, zeichen, stil=''):
    """Die kleinen Tasten am rechten Rand der Anzeige — wie im Foto sechs."""
    stk = [pausei(zeichen, WEISS), prev(zeichen, STUMM), nexti(zeichen, STUMM),
           mischen(zeichen, STUMM), biblio(zeichen, WEISS), lupe(zeichen, STUMM)]
    hoch = f'height:{hoehe}px;' if hoehe else ''
    fach = (f'height:{hoehe // len(stk)}px' if hoehe else 'flex:1')
    return (f'<div class="spalte" style="width:{breite}px;{hoch}{stil}">'
            + ''.join(f'<i style="{fach}">{s}</i>' for s in stk)
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
  <div style="flex:1;min-width:0;display:flex;flex-direction:column;align-self:stretch">
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


def _zeiger(g, pad, breite, hoehe, klein, liste='', stil='', hoch=False):
    """Die zweite Betriebsart: zwei Instrumente statt Cover und Balken.

    Hochkant stehen sie übereinander — nebeneinander bliebe die halbe Fläche leer.
    """
    return f'''<div class="anzeige" style="flex:1;min-width:0;padding:{pad};{stil}">
  <div class="{'mess' if hoch else ''}" style="display:flex;gap:{int(16 * g)}px;
    {'flex-direction:column' if hoch else ''}">
    {vumeter(breite, hoehe, '#e9e9e7', '#1a1a1a', '#3a3a3a', 'L', A['frac'])}
    {vumeter(breite, hoehe, '#e9e9e7', '#1a1a1a', '#3a3a3a', 'R', A['frac'] * .92)}
  </div>

  <div style="font-size:{klein * 1.7:.0f}px;font-weight:500;
    margin-top:{int(44 * g)}px">{A['titel']}</div>
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

  {f'<div style="margin-top:{int(40 * g)}px">{liste}'
    f'<div style="border-top:1px solid rgba(238,240,242,.12)"></div></div>' if liste else ''}
</div>'''


def telefon():
    """Die Zeiger-Betriebsart — hochkant, wie man ein Gerät auf den Tisch stellt."""
    g = 1.0
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0">
  <div class="front" style="flex-direction:column;padding:40px;gap:36px">
    <div style="display:flex;gap:26px;flex:1;min-height:0">
      {_zeiger(g, '44px 42px 46px', 638, 400, 30, _liste(g, 29, 23),
               'display:flex;flex-direction:column', hoch=True)}
      {_spalte(g, 104, 0, 40, 'align-self:stretch')}
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;
      padding:0 18px 12px;flex-shrink:0">
      <span style="font-family:{MONO};font-size:24px;letter-spacing:.22em;
        text-transform:uppercase;color:{LEISE}">Musiklib</span>
      {_ring(g, 260)}
    </div>
  </div>
</div>'''
    return css, body


def rechner():
    """Die Titel-Betriebsart — die breite Front, wie sie im Rack steht."""
    g = .80
    css = _css(g)
    body = f'''<div class="front" style="padding:34px;align-items:stretch;gap:26px">
  {_titelanzeige(g, '44px 46px', 470, 56, 27)}
  {_spalte(g, 86, 0, 32, 'align-self:stretch')}
  <div style="display:flex;align-items:center;padding-left:26px;
    border-left:1px solid rgba(238,240,242,.08)">{_ring(g, 420)}</div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('58', 'Zeigerfront', art, css, body)
