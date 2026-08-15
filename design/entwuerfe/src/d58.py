# -*- coding: utf-8 -*-
"""58 Zeigerfront — aus zwei Fotos derselben Gerätefront (09.18.44 / 09.20.06).

Beide zeigen dasselbe Gerät: eine breite schwarze Anzeige, eine Spalte kleiner
Tasten und ein grosser silberner Lautstärkering. Nur der Inhalt der Anzeige
wechselt — einmal Cover, Titel und ein blauer Fortschrittsbalken, einmal zwei
Zeigerinstrumente mit rotem Endbereich. Wie schon bei 44 bekommt deshalb nicht
jedes Foto ein eigenes Blatt: **das Telefon zeigt Cover und Titel, der Rechner
die beiden Zeiger.** Dieselbe Front, zwei Betriebsarten — genau das, was ein
solcher Verstärker tatsächlich kann.

Die Verteilung folgt dem Format, nicht dem Zufall: ein Cover ist quadratisch und
steht im Hochformat, wo es die ganze Breite bekommt; zwei Zeigerinstrumente
stehen **nebeneinander** und brauchen dafür das Querformat. Im Rechner-Blatt ist
deshalb alles um sie herum angeordnet — die Tasten liegen als Zeile unter der
Anzeige statt als Spalte daneben, damit die beiden Instrumente die volle Breite
der Front bekommen.
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

/* Die Tasten: hochkant eine Spalte neben der Anzeige, quer eine Zeile
   darunter — dieselben sechs Zeichen, dieselben Fugen, nur gedreht. */
.spalte{{display:flex;flex-direction:column;justify-content:space-between;
  align-items:center}}
.spalte i{{display:flex;align-items:center;justify-content:center;width:100%;
  border-bottom:1px solid rgba(238,240,242,.10)}}
.spalte i:last-child{{border-bottom:0}}
.reihe{{display:flex;align-items:stretch}}
.reihe i{{flex:1;display:flex;align-items:center;justify-content:center;
  border-right:1px solid rgba(238,240,242,.10)}}
.reihe i:last-child{{border-right:0}}

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
.marke{{font-family:{MONO};letter-spacing:.22em;text-transform:uppercase;
  color:{LEISE}}}
'''


def _zeichen(zeichen):
    """Die sechs Tastenzeichen — in beiden Betriebsarten dieselben."""
    return [pausei(zeichen, WEISS), prev(zeichen, STUMM), nexti(zeichen, STUMM),
            mischen(zeichen, STUMM), biblio(zeichen, WEISS), lupe(zeichen, STUMM)]


def _spalte(g, breite, zeichen, stil=''):
    """Hochkant: die kleinen Tasten am rechten Rand der Anzeige — wie im Foto sechs."""
    return (f'<div class="spalte" style="width:{breite}px;{stil}">'
            + ''.join(f'<i style="flex:1">{s}</i>' for s in _zeichen(zeichen))
            + '</div>')


def _reihe(g, hoehe, zeichen, stil=''):
    """Quer: dieselben sechs Tasten als Zeile, damit die Anzeige die Breite behält."""
    return (f'<div class="reihe" style="height:{hoehe}px;{stil}">'
            + ''.join(f'<i>{s}</i>' for s in _zeichen(zeichen))
            + '</div>')


def _ring(g, size):
    loch = int(size * .62)
    return (f'<div class="ring" style="width:{size}px;height:{size}px">'
            f'<span style="left:{(size - loch) // 2}px;top:{(size - loch) // 2}px;'
            f'width:{loch}px;height:{loch}px"></span></div>')


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


def _fuss(g, klein, mit_laut=True):
    """Die Zeile unter allem: Bibliothek links, Lautstärke rechts."""
    rechts = (f'<span style="display:flex;gap:{int(16 * g)}px;align-items:center">'
              f'{laut(int(klein * 1.1), STUMM)}'
              f'<span style="font-family:{MONO};font-size:{klein * .82:.0f}px;'
              f'color:{STUMM}">60</span></span>') if mit_laut else (
        f'<span style="font-family:{MONO};font-size:{klein * .82:.0f}px;color:{STUMM}">'
        f'{A["jahr"]} · Titel {A["tracks"][A["laeuft"]][0]}</span>')
    return (f'<div style="display:flex;align-items:center;justify-content:space-between">'
            f'<span class="bib" style="gap:{int(10 * g)}px;'
            f'font-size:{klein * .82:.0f}px;letter-spacing:.14em">'
            f'{biblio(int(klein), STUMM)}Sammlung · {A["sammlung"]}</span>{rechts}</div>')


def _titelanzeige(g, pad, cover_px, gross, klein, liste=''):
    """Betriebsart Cover — hochkant: das Bild steht oben und nimmt die ganze Breite."""
    return f'''<div class="anzeige" style="flex:1;min-width:0;padding:{pad};
  display:flex;flex-direction:column;justify-content:space-between">
  <div style="display:flex;justify-content:center">
    {cover(cover_px, int(cover_px * .02), '#8f2f22', '#2a0d08')}</div>

  <div>
    <div style="font-size:{gross}px;font-weight:500;letter-spacing:-.01em">
      {A['titel']}</div>
    <div style="font-size:{klein * 1.25:.0f}px;color:{WEISS};margin-top:{int(10 * g)}px">
      {A['interpret']}</div>
    <div style="font-size:{klein}px;color:{STUMM};margin-top:{int(4 * g)}px">
      {A['album']} · {A['jahr']}</div>
    {f'<div style="margin-top:{int(46 * g)}px">{liste}'
      f'<div style="border-top:1px solid rgba(238,240,242,.12)"></div></div>' if liste else ''}
  </div>

  <div>
    <div class="bahn" style="height:{int(10 * g)}px">
      <i style="width:{A['frac'] * 100:.0f}%"></i></div>
    <div class="zeiten" style="font-size:{klein * .9:.0f}px;
      margin-top:{int(12 * g)}px">
      <span style="color:{BLAU}">{A['pos']}</span><span>{A['dauer']}</span></div>
    <div style="margin-top:{int(20 * g)}px">{_fuss(g, klein)}</div>
  </div>
</div>'''


def _zeigeranzeige(g, pad, breite, hoehe, luecke, gross, klein):
    """Betriebsart Zeiger — quer: die beiden Instrumente nebeneinander, so gross,
    wie die Front hergibt. Titel, Balken und Zeiten stehen als eine Zeile
    darunter, damit sie den Instrumenten keine Höhe wegnehmen."""
    return f'''<div class="anzeige" style="flex:1;min-height:0;padding:{pad};
  display:flex;flex-direction:column">
  <div style="display:flex;gap:{luecke}px;justify-content:center">
    {vumeter(breite, hoehe, '#e9e9e7', '#1a1a1a', '#3a3a3a', 'L', A['frac'])}
    {vumeter(breite, hoehe, '#e9e9e7', '#1a1a1a', '#3a3a3a', 'R', A['frac'] * .92)}
  </div>

  <div style="margin-top:auto;display:flex;align-items:flex-end;
    gap:{int(56 * g)}px">
    <div style="min-width:0">
      <div style="font-size:{gross}px;font-weight:500;letter-spacing:-.01em">
        {A['titel']}</div>
      <div style="font-size:{klein}px;color:{STUMM};margin-top:{int(8 * g)}px">
        {A['interpret']} · {A['album']} · {A['jahr']}</div>
    </div>
    <div style="flex:1;min-width:0">
      <div class="bahn" style="height:{int(10 * g)}px">
        <i style="width:{A['frac'] * 100:.0f}%"></i></div>
      <div class="zeiten" style="font-size:{klein * .86:.0f}px;
        margin-top:{int(12 * g)}px">
        <span style="color:{BLAU}">{A['pos']}</span><span>{A['dauer']}</span></div>
    </div>
  </div>
  <div style="margin-top:{int(22 * g)}px">{_fuss(g, klein)}</div>
</div>'''


def telefon():
    """Betriebsart Cover — hochkant, wie man ein Gerät auf den Tisch stellt."""
    g = 1.0
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0">
  <div class="front" style="flex-direction:column;padding:40px;gap:36px">
    <div style="display:flex;gap:26px;flex:1;min-height:0">
      {_titelanzeige(g, '46px 42px 48px', 786, 66, 33, _liste(g, 33, 25))}
      {_spalte(g, 104, 40, 'align-self:stretch')}
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;
      padding:0 18px 12px;flex-shrink:0">
      <span class="marke" style="font-size:24px">Musiklib</span>
      {_ring(g, 260)}
    </div>
  </div>
</div>'''
    return css, body


def rechner():
    """Betriebsart Zeiger — die breite Front, wie sie im Rack steht."""
    g = .80
    css = _css(g)
    body = f'''<div class="front" style="flex-direction:column;padding:30px;gap:24px">
  {_zeigeranzeige(g, '34px 40px 30px', 720, 470, 20, 46, 24)}
  <div style="display:flex;align-items:center;gap:30px;flex-shrink:0">
    <span class="marke" style="font-size:20px;width:150px">Musiklib</span>
    {_reihe(g, 190, 40, 'flex:1;min-width:0')}
    {_ring(g, 190)}
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('58', 'Zeigerfront', art, css, body)
