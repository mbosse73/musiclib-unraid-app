# -*- coding: utf-8 -*-
"""64 Gyrorad — gespult wird an einem Schwungrad, nicht an einer Leiste.

Zwei Vorlagen, ein Gedanke: der Marantz 2216 B mit seinem **Gyro-Touch**-Rad
und der Pioneer SX-650 mit zwei Zeigerwerken auf Champagnerblech. Beide sind
Empfänger in gebürstetem Gold-Silber mit Holzwangen; das eine bringt das Rad,
das andere die Zeiger.

Der Entwurf nimmt das Rad ernst, und daraus folgt alles Übrige:

- **Ein Rad hat kein Ende.** Man kann endlos drehen, also kann das Rad selbst
  nicht anzeigen, wo man ist. Es ist reine Geste — gerippt, schwer, mit
  Nachlauf: einmal angeschoben läuft es aus und kommt zur Ruhe. Deshalb
  braucht dieser Entwurf zwingend eine zweite Anzeige.
- **Das ist der Zeiger.** Links steht ein Zeigerwerk, das nicht den Pegel
  zeigt, sondern die **Position im Titel** — die einzige Stelle, an der man
  abliest, wohin das Drehen geführt hat. Es ist damit Anzeige und nicht
  Zierrat, und es ist der einzige bewegte Teil.
- **Die Skala darüber ist das Album**, nicht der Titel: neun Grenzen, eine
  Marke. Sie wird nicht angefasst — wer springen will, dreht.

Das Blech ist Champagner, die Schrift dunkelbraun, die Wangen Nussbaum. Rot
gibt es genau einmal: die Marke auf der Albumskala.

Abgegrenzt: 11 Rack hat auch ein Metallrad, aber dort wählt es aus dem
Plattenfach. Hier spult es innerhalb des Titels, und der Nachlauf ist Teil
der Sache — ein Rad ohne Trägheit ist ein Knopf.
"""
from werkzeug import (A, biblio, laut, lupe, nexti, pausei, prev, schreibe,
                      MONO, SANS)

BLECH = '#D8D2C0'
BLECH2 = '#B9B29C'
HOLZ = '#5A3A22'
TINTE = '#33291C'
MATT = 'rgba(51,41,28,.62)'
STUMM = 'rgba(51,41,28,.40)'
GLAS = '#1C1A16'
CREME = '#EFE9D6'
ROT = '#B4341E'

GRENZEN = [0, 9, 19, 24, 36, 44, 52, 61, 70]
MARKE = 21.5
ENDE = 78
RAND = 5.0


def _x(w):
    return RAND + w / ENDE * (100 - 2 * RAND)


def _css(g):
    return f'''
.stage{{background:linear-gradient(180deg,#EFEADA 0%,#DED8C6 100%);
  font-family:{SANS};color:{TINTE};-webkit-font-smoothing:antialiased}}
.kap{{letter-spacing:.24em;text-transform:uppercase;color:{STUMM};font-weight:500}}
.bib{{display:inline-flex;align-items:center;color:{MATT};letter-spacing:.22em;
  text-transform:uppercase;font-weight:500}}

/* ── Die Front: gebürstetes Champagnerblech mit Holzwangen ── */
.front{{position:relative;background:
    repeating-linear-gradient(90deg,rgba(255,255,255,.16) 0 1px,rgba(0,0,0,.05) 1px 3px),
    linear-gradient(180deg,#EDE7D6 0%,{BLECH} 40%,{BLECH2} 100%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.85),inset 0 -1px 0 rgba(0,0,0,.22),
    0 {14 * g:.0f}px {34 * g:.0f}px rgba(60,45,25,.28)}}
.wange{{position:absolute;top:0;bottom:0;width:{26 * g:.0f}px;
  background:repeating-linear-gradient(180deg,rgba(0,0,0,.16) 0 2px,rgba(255,255,255,.05) 2px 7px),
    linear-gradient(90deg,#6B462A,{HOLZ});
  box-shadow:inset 0 0 {8 * g:.0f}px rgba(0,0,0,.5)}}

/* ── Das Fenster: dunkles Glas in einer Fassung ── */
.fenster{{position:relative;overflow:hidden;border-radius:{3 * g:.0f}px;
  background:linear-gradient(180deg,#2A2721 0%,{GLAS} 40%,#141310 100%);
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.6),inset 0 {8 * g:.0f}px {18 * g:.0f}px rgba(0,0,0,.6),
    0 1px 0 rgba(255,255,255,.6)}}
.tick{{position:absolute;background:rgba(239,233,214,.45);transform:translateX(-50%)}}
.tick.gross{{background:{CREME}}}
.zahl{{position:absolute;font-family:{MONO};color:{CREME};transform:translateX(-50%);
  font-variant-numeric:tabular-nums}}
.marke{{position:absolute;transform:translateX(-50%);background:{ROT};border-radius:1px;
  box-shadow:0 0 {10 * g:.0f}px rgba(180,52,30,.8)}}
.flab{{position:absolute;font-family:{MONO};letter-spacing:.14em;text-transform:uppercase;
  color:rgba(239,233,214,.52)}}

/* ── Das Zeigerwerk: cremefarbenes Blatt, ein Zeiger, kein roter Bogen ──
   Es zeigt die Position im Titel — das ist die Anzeige, die das Rad nicht
   geben kann. */
.werk{{position:relative;border-radius:{3 * g:.0f}px;overflow:hidden;
  background:linear-gradient(180deg,#F6F1DE 0%,{CREME} 62%,#DED7C0 100%);
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.35),inset 0 {5 * g:.0f}px {12 * g:.0f}px rgba(90,70,40,.22)}}

/* ── Das Rad: gerippt, rund, mit Tiefe. Die Rippen sind gezeichnet. ── */
.rad{{position:relative;border-radius:50%;background:
    repeating-conic-gradient(from 0deg,#3A342A 0deg 3deg,#15120E 3deg 6deg),
    radial-gradient(circle at 36% 30%,#4A4238,#0E0C0A 72%);
  box-shadow:inset 0 0 0 {5 * g:.0f}px #241F18,
    inset 0 {6 * g:.0f}px {16 * g:.0f}px rgba(0,0,0,.8),
    0 {8 * g:.0f}px {20 * g:.0f}px rgba(60,45,25,.45)}}
.rad::after{{content:'';position:absolute;inset:{22 * g:.0f}%;border-radius:50%;
  background:radial-gradient(circle at 38% 32%,#6B6255,#221E18);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.2)}}
.radlab{{font-family:{MONO};letter-spacing:.18em;text-transform:uppercase;color:{STUMM};
  text-align:center}}

/* ── Drehknöpfe der unteren Reihe ── */
.dreh{{position:relative;border-radius:50%;background:
    radial-gradient(circle at 34% 28%,#FFFDF4,#B7B09A 78%);
  box-shadow:inset 0 0 0 {2 * g:.0f}px #E4DECB,0 {3 * g:.0f}px {8 * g:.0f}px rgba(60,45,25,.4)}}
.dreh::after{{content:'';position:absolute;left:50%;top:{6 * g:.0f}px;width:{2 * g:.0f}px;
  height:38%;transform:translateX(-50%);background:{TINTE};border-radius:1px}}
.dlab{{font-family:{MONO};letter-spacing:.14em;text-transform:uppercase;color:{STUMM};
  text-align:center}}
.zeit{{font-family:{MONO};color:{MATT};font-variant-numeric:tabular-nums}}
'''


def _fenster(g, hoehe):
    t = []
    n = 52
    for i in range(n + 1):
        x = RAND + i / n * (100 - 2 * RAND)
        gross = i % 4 == 0
        t.append(f'<span class="tick{" gross" if gross else ""}" style="left:{x:.3f}%;'
                 f'top:{hoehe * .44:.0f}px;width:{max(1, int((2 if gross else 1.2) * g))}px;'
                 f'height:{hoehe * (.22 if gross else .13):.0f}px"></span>')
    for w in GRENZEN:
        t.append(f'<span class="zahl" style="left:{_x(w):.2f}%;top:{hoehe * .14:.0f}px;'
                 f'font-size:{26 * g:.0f}px">{w}</span>')
    t.append(f'<span class="marke" style="left:{_x(MARKE):.2f}%;top:{hoehe * .10:.0f}px;'
             f'width:{max(2, int(3 * g))}px;height:{hoehe * .62:.0f}px"></span>')
    t.append(f'<span class="flab" style="left:{RAND}%;bottom:{10 * g:.0f}px;'
             f'font-size:{17 * g:.0f}px">Album · Minuten</span>')
    t.append(f'<span class="flab" style="right:{RAND}%;bottom:{10 * g:.0f}px;'
             f'font-size:{17 * g:.0f}px">{A["album"]}</span>')
    return f'<div class="fenster" style="height:{hoehe}px">{"".join(t)}</div>'


def _werk(g, b, h, frac):
    """Ein Zeiger auf cremefarbenem Blatt. Der Ausschlag ist die Position."""
    import math
    cx, cy, r = b / 2, h * 1.02, h * .88
    a = math.radians(212 + (328 - 212) * frac)
    x2, y2 = cx + math.cos(a) * r * .93, cy + math.sin(a) * r * .93
    striche = []
    for i in range(11):
        aa = math.radians(212 + (328 - 212) * i / 10)
        r1 = r * (.80 if i % 5 else .72)
        striche.append(
            f'<line x1="{cx + math.cos(aa) * r1:.1f}" y1="{cy + math.sin(aa) * r1:.1f}" '
            f'x2="{cx + math.cos(aa) * r * .90:.1f}" y2="{cy + math.sin(aa) * r * .90:.1f}" '
            f'stroke="{TINTE}" stroke-width="{(2.2 if i % 5 == 0 else 1.1) * g:.1f}" '
            f'opacity="{.85 if i % 5 == 0 else .5}"/>')
    return f'''<div class="werk" style="width:{b}px;height:{h}px">
  <svg viewBox="0 0 {b} {h}" width="{b}" height="{h}">
    {''.join(striche)}
    <line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{TINTE}"
      stroke-width="{1.8 * g:.1f}"/>
    <circle cx="{cx}" cy="{cy}" r="{5 * g:.1f}" fill="{TINTE}"/>
    <text x="{cx}" y="{h * .58:.0f}" text-anchor="middle" font-family={MONO!r}
      font-size="{13 * g:.0f}" fill="{MATT}" letter-spacing="2">IM TITEL</text>
  </svg>
</div>'''


def _dreh(g, label, d=64):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;'
            f'gap:{int(9 * g)}px"><span class="dreh" '
            f'style="width:{d * g:.0f}px;height:{d * g:.0f}px"></span>'
            f'<span class="dlab" style="font-size:{14 * g:.0f}px">{label}</span></div>')


def _tasten(g):
    return (f'<div style="display:flex;align-items:center;gap:{int(38 * g)}px">'
            f'{prev(int(26 * g), TINTE)}{pausei(int(32 * g), TINTE)}'
            f'{nexti(int(26 * g), TINTE)}{lupe(int(24 * g), MATT, 2.2)}'
            f'{biblio(int(24 * g), MATT)}</div>')


def _kopf(g):
    return f'''<div style="display:flex;align-items:baseline;justify-content:space-between">
  <span class="bib" style="gap:{int(12 * g)}px;font-size:{19 * g:.0f}px">
    {biblio(int(20 * g), MATT)}Sammlung · {A['sammlung']} Alben</span>
  <span class="kap" style="font-size:{18 * g:.0f}px">Stereophonic Receiver</span>
</div>'''


def _schrift(g, px):
    return f'''<div>
  <div style="font-weight:300;letter-spacing:-.02em;font-size:{px * g:.0f}px;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{A['titel']}</div>
  <div style="color:{MATT};font-weight:300;margin-top:{int(10 * g)}px;
    font-size:{27 * g:.0f}px">{A['interpret']} · {A['jahr']}</div>
</div>'''


def rechner():
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;padding:52px 64px 0;display:flex;
  flex-direction:column;gap:36px">
  {_kopf(g)}
  {_schrift(g, 60)}
  <div class="front" style="position:relative;flex:1;min-height:0;margin:0 -64px;
    padding:44px 90px 40px;display:flex;flex-direction:column;
    justify-content:space-between">
    <span class="wange" style="left:0"></span><span class="wange" style="right:0"></span>
    <div style="display:flex;align-items:flex-end;gap:44px">
      {_werk(g, 250, 168, A['frac'])}
      <div style="flex:1;min-width:0">{_fenster(g, 168)}</div>
    </div>
    <div style="display:flex;align-items:center;gap:52px">
      {_tasten(g)}
      <div style="display:flex;gap:{int(38 * g)}px;margin-left:auto">
        {_dreh(g, 'Bass', 74)}{_dreh(g, 'Höhen', 74)}{_dreh(g, 'Lautstärke', 74)}</div>
      <div style="display:flex;flex-direction:column;align-items:center;gap:{int(11 * g)}px">
        <span class="rad" style="width:{176 * g:.0f}px;height:{176 * g:.0f}px"></span>
        <span class="radlab" style="font-size:{16 * g:.0f}px">Spulen</span></div>
    </div>
    <div style="display:flex;justify-content:space-between">
      <span class="zeit" style="font-size:{21 * g:.0f}px">{A['pos']}</span>
      <span class="zeit" style="font-size:{21 * g:.0f}px">{A['rest']}</span></div>
  </div>
</div>'''
    return _css(g), body


def telefon():
    """Hochkant wandert das Rad nach unten in Daumenreichweite und wird gross —
    es ist die einzige Fläche, die man wirklich anfasst. Zeiger und Fenster
    stehen darüber, weil man sie liest und nicht berührt."""
    g = .94
    body = f'''<div style="position:absolute;inset:0;padding:92px 52px 0;display:flex;
  flex-direction:column;gap:{int(40 * g)}px">
  {_kopf(g)}
  {_schrift(g, 58)}
  <div class="front" style="position:relative;flex:1;min-height:0;margin:0 -52px;
    padding:{int(40 * g)}px {int(70 * g)}px;display:flex;flex-direction:column;
    gap:{int(36 * g)}px;align-items:center">
    <span class="wange" style="left:0"></span><span class="wange" style="right:0"></span>
    {_werk(g, 300, 168, A['frac'])}
    <div style="width:100%">{_fenster(g, 148)}</div>
    <div style="display:flex;justify-content:space-between;width:100%">
      <span class="zeit" style="font-size:{23 * g:.0f}px">{A['pos']}</span>
      <span class="zeit" style="font-size:{23 * g:.0f}px">{A['rest']}</span></div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:{int(12 * g)}px">
      <span class="rad" style="width:{280 * g:.0f}px;height:{280 * g:.0f}px"></span>
      <span class="radlab" style="font-size:{18 * g:.0f}px">Spulen · drehen</span></div>
    <div style="display:flex;align-items:center;gap:{int(46 * g)}px;margin-top:auto;
      padding-bottom:{int(30 * g)}px">
      {prev(int(34 * g), TINTE)}{pausei(int(44 * g), TINTE)}{nexti(int(34 * g), TINTE)}
      {lupe(int(30 * g), MATT, 2.2)}{laut(int(30 * g), MATT)}</div>
  </div>
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('64', 'Gyrorad', art, css, body)
