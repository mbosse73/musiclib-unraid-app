# -*- coding: utf-8 -*-
"""74 Bandteller — der Durchmesser der Wickel ist der Fortschritt.

Vorlage ist eine Revox-Bandmaschine: zwei grosse **blaue Spulen** auf einem
schwarzen Chassis, darunter eine silberne Frontplatte mit schwarzen
Wipptasten, zwei rot gefassten Zeigerinstrumenten, zwei Reglern und einem
vierstelligen Zählwerk.

Der Entwurf hat genau eine Idee, und sie kommt aus der Physik des Bandes:

- **Es gibt keinen Fortschrittsbalken, weil es keinen braucht.** Band
  wandert von links nach rechts; links wächst der Wickel, rechts wird er
  dünner. Der Durchmesser *ist* die Anzeige, und er ist von der anderen
  Seite des Zimmers ablesbar. Ein Balken darunter wäre dieselbe Auskunft ein
  zweites Mal.
- **Das Zählwerk ist die Position im Titel.** Vier Stellen, mechanisch, ohne
  Einheit — wie am Gerät. Wer genau wissen will, wo er ist, liest dort; wer
  ungefähr wissen will, wie weit das Album ist, schaut auf die Spulen.
- **Die roten Fassungen sind die einzige Farbe.** Zwei Instrumente, zwei rote
  Rahmen, und ein roter Wipphebel für „Merken". Blau haben nur die Spulen,
  und das ist Material und keine Auszeichnung.

Gespult wird an den Spulen selbst: man dreht eine, das Band wandert. Die
Wipptasten darunter sind Zustandsschalter, keine Knöpfe — einer steht immer.

Abgegrenzt: 04 Deck hat auch Wickel, aber dort sind sie Zierde in einer
Kassette. Hier tragen sie die einzige Fortschrittsanzeige, die der Entwurf
besitzt.
"""
import math

from werkzeug import (A, biblio, laut, lupe, schreibe, MONO, SANS)

CHASSIS = '#17181A'
FRONT = '#3E4145'
SILBER = '#C4C6C8'
TINTE = '#E9EBEC'
DUNKEL = '#1A1C1E'
MATT = 'rgba(233,235,236,.60)'
STUMM = 'rgba(233,235,236,.34)'
BLAU = '#2B57C8'
BLAU2 = '#1E3E96'
ROT = '#C42B22'
ZAEHLER = '3 1 4 2'

WIPPEN = [('Zurück', False), ('Vor', False), ('Spielen', True), ('Halt', False),
          ('Merken', False)]


def _css(g):
    return f'''
.stage{{background:linear-gradient(180deg,#232527 0%,{CHASSIS} 55%,#0E0F11 100%);
  font-family:{SANS};color:{TINTE};-webkit-font-smoothing:antialiased}}
.kap{{letter-spacing:.24em;text-transform:uppercase;color:{STUMM};font-weight:500}}

/* ── Die Frontplatte: gebürstetes Aluminium über dunklem Feld ── */
.front{{position:relative;background:linear-gradient(180deg,#4A4D51 0%,{FRONT} 60%,#303336 100%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.22),inset 0 -1px 0 rgba(0,0,0,.6),
    0 {10 * g:.0f}px {26 * g:.0f}px rgba(0,0,0,.55)}}
.leiste{{background:
    repeating-linear-gradient(90deg,rgba(255,255,255,.16) 0 1px,rgba(0,0,0,.05) 1px 3px),
    linear-gradient(180deg,#D6D8DA 0%,{SILBER} 46%,#A2A4A6 100%);
  color:{DUNKEL};box-shadow:inset 0 1px 0 rgba(255,255,255,.85)}}

/* ── Die Wipptaste: schwarzer Hebel in einer Nut, gekippt heisst „steht" ── */
.wippe{{position:relative;border-radius:{2 * g:.0f}px;
  background:linear-gradient(180deg,#2A2C2F 0%,#0E1012 62%,#212326 100%);
  box-shadow:0 {3 * g:.0f}px {7 * g:.0f}px rgba(0,0,0,.6),
    inset 0 1px 0 rgba(255,255,255,.16)}}
.wippe.an{{background:linear-gradient(180deg,#0E1012 0%,#2A2C2F 62%,#3A3D40 100%);
  box-shadow:inset 0 3px 6px rgba(0,0,0,.7)}}
.wippe.rot{{background:linear-gradient(180deg,#E0483C 0%,{ROT} 60%,#8E1E17 100%)}}
.wlab{{font-family:{MONO};letter-spacing:.14em;text-transform:uppercase;color:{STUMM};
  text-align:center}}
.wippe.an + .wlab{{color:{TINTE};font-weight:700}}

/* ── Das Instrument: cremefarbenes Blatt in rotem Rahmen ── */
.werk{{position:relative;overflow:hidden;
  background:linear-gradient(180deg,#F2EEE2 0%,#DAD5C6 100%);
  box-shadow:inset 0 0 0 {3 * g:.0f}px {ROT},0 1px 0 rgba(255,255,255,.2)}}

/* ── Das Zählwerk: vier Walzen hinter einem Fenster ── */
.zaehler{{display:flex;gap:{2 * g:.0f}px;background:{DUNKEL};padding:{4 * g:.0f}px;
  border-radius:{2 * g:.0f}px;box-shadow:inset 0 2px 6px rgba(0,0,0,.8)}}
.zaehler span{{font-family:{MONO};font-weight:700;color:#EDE9DC;
  background:linear-gradient(180deg,#3C3E41,#191B1D 52%,#2E3033);
  padding:{3 * g:.0f}px {7 * g:.0f}px;border-radius:1px;font-variant-numeric:tabular-nums}}

.regler{{border-radius:50%;position:relative;
  background:radial-gradient(circle at 34% 28%,#F2F4F5,#9EA0A2 78%);
  box-shadow:inset 0 0 0 {2 * g:.0f}px #D8DADC,0 {3 * g:.0f}px {8 * g:.0f}px rgba(0,0,0,.5)}}
.regler::after{{content:'';position:absolute;left:50%;top:{5 * g:.0f}px;width:{2 * g:.0f}px;
  height:36%;transform:translateX(-50%);background:{DUNKEL};border-radius:1px}}
.zeit{{font-family:{MONO};color:{STUMM};font-variant-numeric:tabular-nums}}
.titel{{font-weight:300;letter-spacing:-.02em;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis}}
'''


def _spule(g, d, gefuellt, kn=0):
    """Eine Spule von vorn. Das blaue Blatt hat drei Fenster, und durch die
    Fenster sieht man den Bandwickel — der Wickel wächst, das Blatt nicht.
    Genau das ist die Anzeige: voll heisst braun bis fast zum Rand."""
    r = d / 2
    rb = r * (.32 + .60 * gefuellt)      # Radius des Wickels
    stopp = min(.98, rb / (r * .90))     # wo im Fenster das Band aufhört
    fenster = ''.join(
        f'<path d="M {r + math.cos(math.radians(a - 24)) * r * .40:.1f} '
        f'{r + math.sin(math.radians(a - 24)) * r * .40:.1f} '
        f'A {r * .40:.1f} {r * .40:.1f} 0 0 1 '
        f'{r + math.cos(math.radians(a + 24)) * r * .40:.1f} '
        f'{r + math.sin(math.radians(a + 24)) * r * .40:.1f} '
        f'L {r + math.cos(math.radians(a + 15)) * r * .84:.1f} '
        f'{r + math.sin(math.radians(a + 15)) * r * .84:.1f} '
        f'A {r * .84:.1f} {r * .84:.1f} 0 0 0 '
        f'{r + math.cos(math.radians(a - 15)) * r * .84:.1f} '
        f'{r + math.sin(math.radians(a - 15)) * r * .84:.1f} Z" '
        f'fill="url(#bw{kn})"/>'
        for a in (-90, 30, 150))
    return (f'<svg viewBox="0 0 {d} {d}" width="{d}" height="{d}">'
            f'<defs><radialGradient id="bw{kn}" cx="50%" cy="50%" r="{r * .90:.1f}"'
            f' gradientUnits="userSpaceOnUse">'
            f'<stop offset="0%" stop-color="#4A3524"/>'
            f'<stop offset="{stopp * 100:.1f}%" stop-color="#6B4C31"/>'
            f'<stop offset="{stopp * 100:.1f}%" stop-color="#121315"/>'
            f'<stop offset="100%" stop-color="#0C0D0F"/></radialGradient></defs>'
            f'<circle cx="{r}" cy="{r}" r="{r * .97:.1f}" fill="#141517"/>'
            f'<circle cx="{r}" cy="{r}" r="{rb:.1f}" fill="#6B4C31"/>'
            f'<circle cx="{r}" cy="{r}" r="{r * .90:.1f}" fill="{BLAU}"/>'
            f'<circle cx="{r}" cy="{r}" r="{r * .90:.1f}" fill="none" stroke="{BLAU2}" '
            f'stroke-width="{d * .022:.1f}"/>'
            f'{fenster}'
            f'<circle cx="{r}" cy="{r}" r="{r * .40:.1f}" fill="{BLAU}"/>'
            f'<circle cx="{r}" cy="{r}" r="{r * .17:.1f}" fill="#2A2C2E" '
            f'stroke="#4A4C4E" stroke-width="{max(1, d * .008):.1f}"/>'
            f'<circle cx="{r}" cy="{r}" r="{r * .05:.1f}" fill="#8A8C8E"/></svg>')


def _werk(g, b, h, frac):
    cx, cy, r = b / 2, h * 1.02, h * .80
    a0, a1 = math.radians(212), math.radians(328)
    st = ''.join(
        f'<line x1="{cx + math.cos(a0 + (a1 - a0) * i / 10) * r * .78:.1f}" '
        f'y1="{cy + math.sin(a0 + (a1 - a0) * i / 10) * r * .78:.1f}" '
        f'x2="{cx + math.cos(a0 + (a1 - a0) * i / 10) * r * .92:.1f}" '
        f'y2="{cy + math.sin(a0 + (a1 - a0) * i / 10) * r * .92:.1f}" '
        f'stroke="{"#C42B22" if i > 7 else DUNKEL}" '
        f'stroke-width="{(2 if i % 5 == 0 else 1.1) * g:.1f}"/>' for i in range(11))
    az = a0 + (a1 - a0) * frac
    return (f'<div class="werk" style="width:{b}px;height:{h}px">'
            f'<svg viewBox="0 0 {b} {h}" width="{b}" height="{h}">{st}'
            f'<line x1="{cx}" y1="{cy}" x2="{cx + math.cos(az) * r * .95:.1f}" '
            f'y2="{cy + math.sin(az) * r * .95:.1f}" stroke="{DUNKEL}" '
            f'stroke-width="{1.6 * g:.1f}"/></svg></div>')


def _wippen(g, b, h):
    return (f'<div style="display:flex;gap:{int(b * .42)}px">' + ''.join(
        f'<div style="display:flex;flex-direction:column;align-items:center;'
        f'gap:{int(9 * g)}px">'
        f'<span class="wippe{" an" if an else ""}{" rot" if lab == "Merken" else ""}" '
        f'style="width:{b}px;height:{h}px"></span>'
        f'<span class="wlab" style="font-size:{b * .30:.0f}px">{lab}</span></div>'
        for lab, an in WIPPEN) + '</div>')


def _zaehlwerk(g, px):
    return ('<div class="zaehler">' + ''.join(
        f'<span style="font-size:{px}px">{z}</span>' for z in ZAEHLER.split()) + '</div>')


def _kopf(g, px=18):
    return f'''<div style="display:flex;align-items:baseline;justify-content:space-between">
  <span class="kap" style="font-size:{px}px">Musiklib · Bandmaschine</span>
  <span class="kap" style="font-size:{px}px">Sammlung {A['sammlung']}</span>
</div>'''


def rechner():
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  padding:44px 64px 0;gap:22px">
  {_kopf(g)}
  <div style="flex:1;min-height:0;display:flex;align-items:center;justify-content:center;
    gap:70px">
    {_spule(g, 330, A['frac'], 1)}
    <div style="text-align:center">
      <div class="titel" style="font-size:44px">{A['titel']}</div>
      <div style="color:{MATT};font-size:22px;margin-top:10px">
        {A['interpret']} · {A['album']}</div>
      <div style="display:flex;justify-content:center;margin-top:26px">
        {_zaehlwerk(g, 30)}</div>
      <div class="kap" style="font-size:13px;margin-top:12px">Zählwerk · im Titel</div>
    </div>
    {_spule(g, 330, 1 - A['frac'], 2)}
  </div>
  <div class="front" style="margin:0 -64px;padding:30px 64px 40px;display:flex;
    align-items:center;gap:56px">
    {_wippen(g, 62, 78)}
    <div style="display:flex;gap:22px;margin-left:auto">
      {_werk(g, 150, 84, .58)}{_werk(g, 150, 84, A['frac'])}
    </div>
    <div style="display:flex;gap:26px;align-items:center">
      <span class="regler" style="width:70px;height:70px"></span>
      <span class="regler" style="width:70px;height:70px"></span>
      <div style="display:flex;gap:18px;margin-left:10px">
        {biblio(24, MATT)}{lupe(22, MATT, 2.2)}{laut(22, MATT)}</div>
    </div>
  </div>
</div>'''
    return _css(g), body


def telefon():
    """Hochkant stehen die Spulen nebeneinander und werden gross — sie sind
    die Anzeige und zugleich die Spulfläche, also brauchen sie Fläche. Die
    Frontplatte rutscht ganz nach unten, wo die Hand ohnehin ist."""
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  padding:96px 48px 0;gap:30px">
  {_kopf(g, 19)}
  <div style="display:flex;justify-content:center;gap:36px">
    {_spule(g, 440, A['frac'], 3)}{_spule(g, 440, 1 - A['frac'], 4)}
  </div>
  <div style="text-align:center">
    <div class="titel" style="font-size:50px">{A['titel']}</div>
    <div style="color:{MATT};font-size:26px;margin-top:12px">
      {A['interpret']} · {A['album']}</div>
    <div style="display:flex;justify-content:center;margin-top:30px">
      {_zaehlwerk(g, 40)}</div>
    <div class="kap" style="font-size:16px;margin-top:14px">Zählwerk · im Titel</div>
  </div>
  <div class="front" style="margin:auto -48px 0;padding:40px 48px 64px;display:flex;
    flex-direction:column;align-items:center;gap:34px">
    {_wippen(g, 116, 128)}
    <div style="display:flex;gap:26px;align-items:center">
      {_werk(g, 200, 104, .58)}{_werk(g, 200, 104, A['frac'])}
      <span class="regler" style="width:92px;height:92px"></span>
    </div>
    <div style="display:flex;gap:34px;align-items:center">
      {biblio(30, MATT)}{lupe(28, MATT, 2.2)}{laut(28, MATT)}
      <span class="zeit" style="font-size:22px">{A['pos']} / {A['dauer']}</span>
    </div>
  </div>
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('74', 'Bandteller', art, css, body)
