# -*- coding: utf-8 -*-
"""40 Neonschild — nach „Feel the Music" über dem Plattenspieler (23.31.26).

Die Vorlage ist ein dunkler, warmer Raum: an der Wand ein Leuchtschild, dessen
Licht die Wand aufhellt, darunter ein Plattenspieler mit offener Haube auf einem
Sideboard. Übertragen: das Leuchtschild trägt den laufenden Titel, die
Fortschrittsleiste ist die Neonröhre darunter, und der Plattenspieler steht
tatsächlich da — mit einer Platte, die sich mitdreht.
"""
from werkzeug import A, biblio, mischen, nexti, platte, prev, schreibe, tri, wiederholen, SANS, MONO

TINTE = '#f6e3c8'
STUMM = 'rgba(246,227,200,.55)'
NEON = '#ffcf7a'
ROHR = 'rgba(255,190,110,'


def _css(g):
    return f'''
.stage{{background:
  radial-gradient(70% 50% at 32% 26%, #4a2c18 0%, #2a1710 45%, #150c08 100%);
  font-family:{SANS};color:{TINTE}}}

/* Das Licht des Schildes auf der Wand */
.wandlicht{{position:absolute;border-radius:50%;pointer-events:none;
  background:radial-gradient(circle,{ROHR}.32) 0%,{ROHR}.10) 40%,{ROHR}0) 70%)}}

/* Neon: Kern weiss, Hülle bernstein — vier Schattenlagen machen die Röhre */
.neon{{color:#fff6e2;font-weight:800;letter-spacing:-.01em;line-height:1.04;
  text-shadow:0 0 {6 * g:.0f}px #fff4dd, 0 0 {18 * g:.0f}px {NEON},
    0 0 {44 * g:.0f}px {ROHR}.85), 0 0 {96 * g:.0f}px {ROHR}.45)}}
.neonklein{{color:{NEON};letter-spacing:{6 * g:.1f}px;text-transform:uppercase;
  text-shadow:0 0 {8 * g:.0f}px {ROHR}.9), 0 0 {26 * g:.0f}px {ROHR}.5)}}

/* Die Röhre unter dem Schild ist zugleich die Spulleiste */
.rohr{{position:relative;border-radius:999px;background:rgba(255,207,122,.16)}}
.rohr i{{position:absolute;left:0;top:0;bottom:0;border-radius:999px;background:{NEON};
  box-shadow:0 0 {14 * g:.0f}px {ROHR}.95), 0 0 {40 * g:.0f}px {ROHR}.55)}}
.rohr b{{position:absolute;top:50%;transform:translate(-50%,-50%);border-radius:50%;
  background:#fff6e2;box-shadow:0 0 {16 * g:.0f}px {ROHR}.95)}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};color:{STUMM};
  font-variant-numeric:tabular-nums}}

/* Sideboard und Gerät */
.brett{{position:absolute;background:linear-gradient(180deg,#5a3venue,#3a2416)}}
.geraet{{position:relative;background:linear-gradient(180deg,#c9a271,#9c7746);
  box-shadow:0 {26 * g:.0f}px {50 * g:.0f}px rgba(0,0,0,.55)}}
.haube{{position:absolute;border:{2 * g:.0f}px solid rgba(255,190,120,.42);
  border-bottom:none;background:linear-gradient(180deg,rgba(255,190,120,.10),rgba(255,190,120,.02))}}
.front{{position:absolute;left:0;right:0;bottom:0;background:#1d150e;
  border-top:1px solid rgba(255,190,120,.20)}}

.taste{{flex-shrink:0;border-radius:50%;display:flex;align-items:center;justify-content:center;
  border:{2 * g:.0f}px solid rgba(255,190,120,.35);background:rgba(255,190,120,.06)}}
.taste.gross{{background:rgba(255,207,122,.16);border-color:{NEON};
  box-shadow:0 0 {24 * g:.0f}px {ROHR}.55), inset 0 0 {20 * g:.0f}px {ROHR}.28)}}
.bib{{display:inline-flex;align-items:center;border-radius:999px;
  border:{2 * g:.0f}px solid rgba(255,190,120,.35)}}
'''.replace('#5a3venue', '#5a3a22')


def _spieler(g, breite):
    """Plattenspieler mit offener Haube, Platte und Tonarm."""
    h = breite * .60
    haube_h = breite * .40
    p = breite * .34
    return f'''<div style="position:relative;width:{breite:.0f}px;height:{h + haube_h:.0f}px">
  <div class="haube" style="left:{breite * .06:.0f}px;top:0;width:{breite * .78:.0f}px;
    height:{haube_h:.0f}px;transform:perspective(900px) rotateX(24deg);
    transform-origin:bottom center;border-radius:{breite * .012:.0f}px"></div>
  <div class="geraet" style="position:absolute;left:0;bottom:0;width:{breite:.0f}px;
    height:{h:.0f}px;border-radius:{breite * .015:.0f}px">
    <div style="position:absolute;left:{breite * .10:.0f}px;top:{h * .09:.0f}px">
      {platte(p, '#e08a3c', rille='#2e2e30', glanz=True)}</div>
    <div style="position:absolute;right:{breite * .13:.0f}px;top:{h * .12:.0f}px;
      width:{breite * .012:.0f}px;height:{p * .74:.0f}px;background:#d8cdbd;
      transform:rotate(24deg);transform-origin:top center;border-radius:2px"></div>
    <div style="position:absolute;right:{breite * .115:.0f}px;top:{h * .07:.0f}px;
      width:{breite * .045:.0f}px;height:{breite * .045:.0f}px;border-radius:50%;
      background:#2a2118"></div>
    <div class="front" style="height:{h * .30:.0f}px;border-radius:0 0
      {breite * .015:.0f}px {breite * .015:.0f}px"></div>
  </div>
</div>'''


def _transport(g, klein, gross_, luecke):
    return (f'<div style="display:flex;align-items:center;justify-content:center;gap:{luecke}px">'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{mischen(int(klein * .38), STUMM)}</div>'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{prev(int(klein * .40), TINTE)}</div>'
            f'<div class="taste gross" style="width:{gross_}px;height:{gross_}px">'
            f'{tri(int(gross_ * .38), NEON)}</div>'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{nexti(int(klein * .40), TINTE)}</div>'
            f'<div class="taste" style="width:{klein}px;height:{klein}px">'
            f'{wiederholen(int(klein * .38), STUMM)}</div></div>')


def _bib(g, schrift, hoehe):
    return (f'<span class="bib" style="height:{hoehe}px;padding:0 {int(28 * g)}px;'
            f'gap:{int(14 * g)}px"><span class="neonklein" style="font-size:{schrift}px">'
            f'Sammlung · {A["sammlung"]}</span></span>')


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div class="wandlicht" style="left:-160px;top:60px;width:1400px;height:1400px"></div>
<div style="position:absolute;inset:0;padding:140px 78px 120px;display:flex;flex-direction:column">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <span class="neonklein" style="font-size:22px">Jetzt läuft</span>
    {_bib(g, 20, 66)}
  </div>

  <div class="neon" style="font-size:112px;margin-top:96px">{A['titel']}</div>
  <div style="font-size:33px;color:{STUMM};margin-top:26px">{A['interpret']} · {A['album']}</div>

  <div class="rohr" style="height:14px;margin-top:56px">
    <i style="width:{A['frac'] * 100:.0f}%"></i>
    <b style="left:{A['frac'] * 100:.0f}%;width:30px;height:30px"></b></div>
  <div class="zeiten" style="font-size:25px;margin-top:22px">
    <span>{A['pos']}</span><span>{A['dauer']}</span></div>

  <div style="margin-top:56px;display:flex;justify-content:center">{_spieler(g, 780)}</div>

  <div style="margin-top:auto">{_transport(g, 100, 148, 42)}</div>
</div>'''
    return css, body


def rechner():
    g = .72
    css = _css(g)
    body = f'''<div class="wandlicht" style="left:-220px;top:-180px;width:1250px;height:1250px"></div>
<div style="position:absolute;inset:0;padding:70px 88px;display:flex;flex-direction:column">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <span class="neonklein" style="font-size:16px">Jetzt läuft</span>
    {_bib(g, 15, 48)}
  </div>

  <div style="display:flex;gap:70px;align-items:flex-end;flex:1;min-height:0;margin-top:34px">
    <div style="flex:1;min-width:0;padding-bottom:26px">
      <div class="neon" style="font-size:86px">{A['titel']}</div>
      <div style="font-size:25px;color:{STUMM};margin-top:18px">
        {A['interpret']} · {A['album']} · {A['jahr']}</div>
      <div class="rohr" style="height:10px;margin-top:40px">
        <i style="width:{A['frac'] * 100:.0f}%"></i>
        <b style="left:{A['frac'] * 100:.0f}%;width:22px;height:22px"></b></div>
      <div class="zeiten" style="font-size:19px;margin-top:16px">
        <span>{A['pos']}</span><span>{A['dauer']}</span></div>
      <div style="margin-top:36px;display:flex">{_transport(g, 68, 100, 30)}</div>
    </div>
    <div style="flex-shrink:0">{_spieler(g, 520)}</div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('40', 'Neonschild', art, css, body)
