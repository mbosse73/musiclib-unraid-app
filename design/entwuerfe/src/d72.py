# -*- coding: utf-8 -*-
"""72 Tastenreihe — die Beschriftung steht unter der Taste, nicht auf ihr.

Vorlage ist ein silberner Kassettenrekorder (SKR 700): zwei grosse
Lautsprecherkörbe, dazwischen ein beleuchtetes Kassettenfenster, und darunter
eine **Reihe mechanischer Klaviertasten** — sechs Stück, gerippt, jede mit
ihrem Wort in Grossbuchstaben *unter* der Taste. Über drei davon steht eine
gedruckte Klammer mit der Aufschrift SEARCH SYSTEM.

Drei Dinge daraus sind der Entwurf:

- **Das Wort steht unter der Taste.** Nichts ist auf die Tastenfläche
  gedruckt; die Fläche ist zum Drücken da, die Schrift zum Lesen. Damit
  bleibt jede Taste gleich aussehen, und die Reihe wird zu einem Feld statt
  zu einer Sammlung von Zeichen.
- **Gruppiert wird mit einer gedruckten Klammer.** Die drei Tasten, die
  innerhalb des Albums bewegen — zurück, spielen, vor —, stehen unter einer
  Klammer, die sie als eines ausweist. Das ist billiger und klarer als
  Abstände, und es steht auf dem Blech und nicht im Bildschirm.
- **Die Maschine ist symmetrisch.** Zwei Körbe links und rechts, in der
  Mitte das Fenster. Der Entwurf hält das durch: was arbeitet, steht mittig,
  was nicht arbeitet, ist beidseitig gleich.

Im Fenster liegt die Warteschlange als Band zwischen zwei Wickeln — und der
Wickel ist hier keine Zierde, sondern die Anzeige: links wächst er, rechts
wird er dünner.

Abgegrenzt: 04 Deck und 05 Handgerät sind auch Kassetten, aber dort ist die
Kassette das ganze Gerät. Hier ist sie ein Fenster in einer Maschine, und der
Entwurf ist die Tastenreihe darunter.
"""
import math

from werkzeug import (A, biblio, laut, lupe, schreibe, MONO, SANS)

BLECH = '#C6C6C2'
BLECH2 = '#A8A8A4'
DUNKEL = '#2B2B2A'
TINTE = '#26262A'
MATT = 'rgba(38,38,42,.62)'
STUMM = 'rgba(38,38,42,.42)'
FENSTER = '#E8E2C4'
BAND = '#3A2E22'

TASTEN = [('Halt', 'stop'), ('Merken', 'mark'), ('Zurück', 'prev'),
          ('Spielen', 'play'), ('Vor', 'next'), ('Pause', 'pause')]
KLAMMER = (2, 4)          # welche Tasten die Klammer zusammenfasst
GEDRUECKT = 3             # „Spielen" steht unten


def _css(g):
    return f'''
.stage{{background:linear-gradient(180deg,#D6D6D2 0%,#BFBFBB 46%,#AAAAA6 100%);
  font-family:{SANS};color:{TINTE};-webkit-font-smoothing:antialiased}}
.kap{{letter-spacing:.24em;text-transform:uppercase;color:{STUMM};font-weight:500}}
.gebuerstet{{background:
    repeating-linear-gradient(90deg,rgba(255,255,255,.17) 0 1px,rgba(0,0,0,.05) 1px 3px),
    linear-gradient(180deg,#D8D8D4 0%,{BLECH} 44%,{BLECH2} 100%)}}

/* ── Der Lautsprecherkorb: ein Punktraster hinter einem Ring ── */
.korb{{position:relative;border-radius:50%;
  background:radial-gradient(circle at 38% 32%,#3E3E3C,#161616 76%);
  box-shadow:inset 0 0 0 {5 * g:.0f}px #B4B4B0,inset 0 0 0 {7 * g:.0f}px #8E8E8A,
    0 {6 * g:.0f}px {16 * g:.0f}px rgba(0,0,0,.35)}}
.korb::after{{content:'';position:absolute;inset:{7 * g:.0f}px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,255,255,.10) 0 1px,rgba(0,0,0,.55) 1px 3px);
  background-size:{6 * g:.0f}px {6 * g:.0f}px}}

/* ── Das Fenster: beleuchtetes Elfenbein hinter Glas ── */
.fenster{{position:relative;overflow:hidden;border-radius:{3 * g:.0f}px;
  background:linear-gradient(180deg,#F4EFD6 0%,{FENSTER} 52%,#D8D2B4 100%);
  box-shadow:inset 0 0 0 {4 * g:.0f}px #9A9A96,inset 0 {4 * g:.0f}px {12 * g:.0f}px rgba(90,80,50,.28),
    0 {5 * g:.0f}px {14 * g:.0f}px rgba(0,0,0,.35)}}
.flab{{position:absolute;font-family:{MONO};letter-spacing:.16em;text-transform:uppercase;
  color:rgba(58,46,34,.55)}}

/* ── Die Klaviertaste: gerippt, silbern, mit Druckpunkt ── */
.taste{{position:relative;border-radius:{3 * g:.0f}px;
  background:repeating-linear-gradient(90deg,#EDEDE9 0 2px,#B2B2AE 2px 4px);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.9),inset 0 -2px 0 rgba(0,0,0,.28),
    0 {4 * g:.0f}px {8 * g:.0f}px rgba(0,0,0,.34)}}
.taste.unten{{background:repeating-linear-gradient(90deg,#B2B2AE 0 2px,#8E8E8A 2px 4px);
  box-shadow:inset 0 2px 5px rgba(0,0,0,.45),0 1px 2px rgba(0,0,0,.3)}}
.tlab{{font-family:{MONO};letter-spacing:.14em;text-transform:uppercase;color:{TINTE};
  text-align:center}}
.taste.unten + .tlab{{font-weight:700}}
/* Die Klammer ist gedruckt: zwei Winkel und ein Wort dazwischen. */
.klammer{{position:absolute;border-top:{2 * g:.0f}px solid {MATT};
  border-left:{2 * g:.0f}px solid {MATT};border-right:{2 * g:.0f}px solid {MATT}}}
.klab{{position:absolute;left:50%;transform:translateX(-50%);font-family:{MONO};
  letter-spacing:.18em;text-transform:uppercase;color:{MATT};background:{BLECH};
  padding:0 {8 * g:.0f}px}}
.zeit{{font-family:{MONO};color:{MATT};font-variant-numeric:tabular-nums}}
'''


def _wickel(g, r, gefuellt):
    """Ein Wickel: Nabe, Band bis zum Füllgrad, Ring. Der Durchmesser zählt."""
    rb = r * (.34 + .60 * gefuellt)
    return (f'<svg viewBox="0 0 {r * 2} {r * 2}" width="{r * 2}" height="{r * 2}">'
            f'<circle cx="{r}" cy="{r}" r="{r}" fill="none" stroke="rgba(58,46,34,.35)" '
            f'stroke-width="{1.4 * g:.1f}"/>'
            f'<circle cx="{r}" cy="{r}" r="{rb:.1f}" fill="{BAND}" opacity=".82"/>'
            f'<circle cx="{r}" cy="{r}" r="{r * .30:.1f}" fill="#DAD6C4" '
            f'stroke="rgba(58,46,34,.5)" stroke-width="{1.2 * g:.1f}"/>'
            + ''.join(
                f'<line x1="{r + math.cos(math.radians(k * 120)) * r * .12:.1f}" '
                f'y1="{r + math.sin(math.radians(k * 120)) * r * .12:.1f}" '
                f'x2="{r + math.cos(math.radians(k * 120)) * r * .28:.1f}" '
                f'y2="{r + math.sin(math.radians(k * 120)) * r * .28:.1f}" '
                f'stroke="rgba(58,46,34,.6)" stroke-width="{2 * g:.1f}"/>' for k in range(3))
            + '</svg>')


def _fenster(g, b, h):
    r = int(h * .30)
    return f'''<div class="fenster" style="width:{b}px;height:{h}px;
  display:flex;align-items:center;justify-content:center;gap:{int(b * .10)}px">
  {_wickel(g, r, A['frac'])}{_wickel(g, r, 1 - A['frac'])}
  <span class="flab" style="left:{int(b * .06)}px;top:{int(h * .10)}px;
    font-size:{h * .075:.0f}px">Warteschlange</span>
  <span class="flab" style="right:{int(b * .06)}px;top:{int(h * .10)}px;
    font-size:{h * .075:.0f}px">Titel 3 von 5</span>
  <span class="flab" style="left:0;right:0;bottom:{int(h * .09)}px;text-align:center;
    font-size:{h * .085:.0f}px;letter-spacing:.06em">{A['titel']} · {A['interpret']}</span>
</div>'''


def _reihe(g, tb, th):
    """Sechs Tasten, sechs Wörter darunter, eine gedruckte Klammer darüber."""
    lueck = int(tb * .34)
    schritt = tb + lueck
    k0, k1 = KLAMMER
    kl_links = k0 * schritt - lueck * .35
    kl_breite = (k1 - k0) * schritt + tb + lueck * .7
    tasten = ''.join(
        f'<div style="width:{tb}px;display:flex;flex-direction:column;'
        f'align-items:center;gap:{int(10 * g)}px">'
        f'<span class="taste{" unten" if i == GEDRUECKT else ""}" '
        f'style="width:{tb}px;height:{th}px"></span>'
        f'<span class="tlab" style="font-size:{tb * .21:.0f}px">{lab}</span></div>'
        for i, (lab, _) in enumerate(TASTEN))
    return f'''<div style="position:relative;padding-top:{int(46 * g)}px">
  <span class="klammer" style="left:{kl_links:.0f}px;top:{int(22 * g)}px;
    width:{kl_breite:.0f}px;height:{int(18 * g)}px"></span>
  <span class="klab" style="top:{int(13 * g)}px;left:{kl_links + kl_breite / 2:.0f}px;
    font-size:{tb * .19:.0f}px">Suchlauf</span>
  <div style="display:flex;gap:{lueck}px">{tasten}</div>
</div>'''


def _kopf(g, px=18):
    return f'''<div style="display:flex;align-items:baseline;justify-content:space-between">
  <span class="kap" style="font-size:{px}px">Musiklib · SKR</span>
  <span class="kap" style="font-size:{px}px">Sammlung {A['sammlung']} · {A['album']}</span>
</div>'''


def rechner():
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  padding:44px 60px 0;gap:26px">
  {_kopf(g)}
  <div class="gebuerstet" style="flex:1;margin:0 -60px;padding:30px 60px 40px;
    display:flex;align-items:center;gap:40px;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.8),inset 0 -1px 0 rgba(0,0,0,.25)">
    <span class="korb" style="width:230px;height:230px;flex:none"></span>
    <div style="flex:1;min-width:0;display:flex;flex-direction:column;
      align-items:center;gap:34px">
      {_fenster(g, 660, 250)}
      {_reihe(g, 104, 74)}
      <div style="display:flex;align-items:center;justify-content:space-between;width:100%">
        <span class="zeit" style="font-size:20px">{A['pos']}</span>
        <div style="display:flex;gap:{int(26 * g)}px">
          {biblio(24, MATT)}{lupe(22, MATT, 2.2)}{laut(22, MATT)}</div>
        <span class="zeit" style="font-size:20px">{A['rest']}</span>
      </div>
    </div>
    <span class="korb" style="width:230px;height:230px;flex:none"></span>
  </div>
</div>'''
    return _css(g), body


def telefon():
    """Hochkant stehen die Körbe über- statt nebeneinander — die Symmetrie
    bleibt, sie kippt nur. Die Tastenreihe wird zweizeilig: sechs Tasten
    nebeneinander wären auf 1080 px je 130 px breit und damit schmaler als
    ein Daumen."""
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  padding:92px 48px 0;gap:30px">
  {_kopf(g, 19)}
  <div class="gebuerstet" style="flex:1;margin:0 -48px;padding:44px 48px 60px;
    display:flex;flex-direction:column;align-items:center;gap:40px;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.8)">
    <span class="korb" style="width:340px;height:340px;flex:none"></span>
    {_fenster(g, 940, 250)}
    <div style="display:flex;flex-direction:column;gap:{int(28 * g)}px;align-items:center">
      {_reihe(g, 150, 92)}
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;width:100%">
      <span class="zeit" style="font-size:23px">{A['pos']}</span>
      <div style="display:flex;gap:{int(34 * g)}px">
        {biblio(30, MATT)}{lupe(28, MATT, 2.2)}{laut(28, MATT)}</div>
      <span class="zeit" style="font-size:23px">{A['rest']}</span>
    </div>
  </div>
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('72', 'Tastenreihe', art, css, body)
