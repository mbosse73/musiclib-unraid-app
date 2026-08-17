# -*- coding: utf-8 -*-
"""68 Fadertisch — die Warteschlange ist ein Pad-Feld, kein Verzeichnis.

Vorlage ist ein Controller in dunklem Grau: links ein hochkanter Bildschirm,
rechts fünf Fader, darunter ein Feld aus Pads und **eine grosse orange
Taste**, flankiert von zwei weissen. Nichts daran ist rund ausser zwei
Drehreglern; alles andere ist Rechteck.

Der Entwurf übernimmt die Aufteilung wörtlich, weil sie eine Aussage macht:

- **Links wird gelesen, rechts wird gegriffen.** Der Bildschirm zeigt Bild,
  Titel und Stand und wird nie berührt. Die ganze Bedienung liegt auf der
  rechten Hälfte, in Reichweite einer Hand.
- **Die Pads sind die Warteschlange.** Ein Pad je Titel, in Leserichtung; das
  laufende leuchtet. Antippen springt. Damit braucht dieser Entwurf keine
  Liste — bei mehr Titeln als Pads blättert die letzte Reihe weiter.
- **Genau eine Taste ist orange**, und sie ist die grösste: Abspielen und
  Anhalten. Die Vorlage macht das vor, und es ist die klarste Regel, die ein
  Bedienfeld haben kann.
- **Die fünf Fader sind keine Klangregelung.** Der erste ist die Lautstärke,
  die vier anderen sind **Sprungmarken im Album** — Viertel, Hälfte,
  Dreiviertel, Ende. Ein Fader, der nur eine Zahl verstellt, wäre auf einem
  Musikgerät ohne Klangregelung Zierrat.

Abgegrenzt: 12 Studiogerät hat auch einen langen Regler, aber dort ist er die
Spulleiste des Titels. Hier ist die Spulleiste die Bahn unter dem Bild, und
die Fader springen.
"""
from werkzeug import (A, biblio, cover, laut, lupe, nexti, pausei, prev,
                      schreibe, MONO, SANS)

SLAB = '#3A3D40'
SLAB2 = '#2A2D30'
PAD = '#42464A'
PAD_AN = '#F97316'
WEISS = '#F4F4F2'
TINTE = '#E8E9EA'
MATT = 'rgba(232,233,234,.60)'
STUMM = 'rgba(232,233,234,.34)'
SCHIRM = '#141618'

TITEL = ['So What', 'Freddie', 'Blue in Green', 'All Blues', 'Flamenco',
         'Teo', 'Fran-Dance', 'Love for Sale']
LAEUFT = 2
FADER = [('Ton', .72), ('¼', .25), ('½', .50), ('¾', .75), ('Ende', 1.0)]


def _css(g):
    return f'''
.stage{{background:linear-gradient(160deg,#4A4E52 0%,{SLAB} 40%,{SLAB2} 100%);
  font-family:{SANS};color:{TINTE};-webkit-font-smoothing:antialiased}}
.kap{{letter-spacing:.24em;text-transform:uppercase;color:{STUMM};font-weight:500}}

/* ── Der Bildschirm: eine schwarze Scheibe, bündig eingelassen ── */
.schirm{{position:relative;background:{SCHIRM};border-radius:{4 * g:.0f}px;overflow:hidden;
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.6),inset 0 {6 * g:.0f}px {18 * g:.0f}px rgba(0,0,0,.6),
    0 1px 0 rgba(255,255,255,.10)}}
.bahn{{position:relative;height:{6 * g:.0f}px;border-radius:{3 * g:.0f}px;
  background:rgba(255,255,255,.12);overflow:hidden}}
.bahn i{{position:absolute;left:0;top:0;bottom:0;background:{PAD_AN};border-radius:inherit}}

/* ── Pads: Rechtecke mit weicher Kante, gedrückt heisst leuchtet ── */
.pads{{display:grid;gap:{int(10 * g)}px}}
.pad{{position:relative;border-radius:{5 * g:.0f}px;background:linear-gradient(180deg,#4E5256,{PAD});
  box-shadow:inset 0 1px 0 rgba(255,255,255,.13),0 {3 * g:.0f}px {7 * g:.0f}px rgba(0,0,0,.35);
  display:flex;align-items:flex-end;padding:{int(9 * g)}px;overflow:hidden}}
.pad span{{font-family:{MONO};letter-spacing:.04em;color:{MATT};white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis;width:100%}}
.pad.an{{background:linear-gradient(180deg,#FFA657,{PAD_AN});
  box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 0 {18 * g:.0f}px rgba(249,115,22,.45)}}
.pad.an span{{color:rgba(28,16,4,.86);font-weight:700}}
.pad.gespielt{{background:linear-gradient(180deg,#3A3E42,#2E3236)}}
.pad.gespielt span{{color:{STUMM}}}

/* ── Fader: eine Nut, ein Knopf. Der Knopf ist schwarz und rund oben. ── */
.fader{{display:flex;flex-direction:column;align-items:center;gap:{int(9 * g)}px}}
.nut{{position:relative;width:{8 * g:.0f}px;border-radius:{4 * g:.0f}px;
  background:linear-gradient(90deg,#232629,#171A1C);
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.5),inset 0 2px 5px rgba(0,0,0,.7)}}
.griff{{position:absolute;left:50%;transform:translate(-50%,-50%);border-radius:{5 * g:.0f}px;
  background:linear-gradient(180deg,#3D4145 0%,#15171A 60%,#2A2D30 100%);
  box-shadow:0 {3 * g:.0f}px {7 * g:.0f}px rgba(0,0,0,.55),
    inset 0 1px 0 rgba(255,255,255,.22)}}
.flab{{font-family:{MONO};font-size:{13 * g:.0f}px;letter-spacing:.12em;color:{STUMM}}}

/* ── Die drei Transporttasten: gross, flach, zwei weiss, eine orange ── */
.tk{{display:flex;align-items:center;justify-content:center;border-radius:{6 * g:.0f}px;
  box-shadow:0 {4 * g:.0f}px {10 * g:.0f}px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.3)}}
.tk.hell{{background:linear-gradient(180deg,#FFFFFF,#DCDCD8)}}
.tk.orange{{background:linear-gradient(180deg,#FFA657,{PAD_AN})}}
/* Zwei Drehregler — das einzige Runde auf der ganzen Fläche. */
.rund{{border-radius:50%;position:relative}}
.rund.weiss{{background:radial-gradient(circle at 36% 30%,#FFFFFF,#C9C9C4);
  box-shadow:0 {4 * g:.0f}px {9 * g:.0f}px rgba(0,0,0,.4)}}
.rund.schwarz{{background:radial-gradient(circle at 36% 30%,#3A3E42,#0E1012);
  box-shadow:0 {4 * g:.0f}px {9 * g:.0f}px rgba(0,0,0,.5)}}
.titel{{font-weight:300;letter-spacing:-.02em;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis}}
.zeit{{font-family:{MONO};color:{STUMM};font-variant-numeric:tabular-nums}}
'''


def _schirm(g, b, h, hoch=True):
    cs = int(min(b, h) * (.52 if hoch else .38))
    return f'''<div class="schirm" style="width:{b}px;height:{h}px;padding:{int(26 * g)}px;
  display:flex;flex-direction:column;justify-content:space-between;gap:{int(20 * g)}px">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <span class="kap" style="font-size:{13 * g:.0f}px">Musiklib</span>
    <span class="kap" style="font-size:{13 * g:.0f}px">{A['sammlung']} Alben</span>
  </div>
  <div style="display:flex;justify-content:center">
    {cover(cs, int(cs * .04), '#2E4A6B', '#8E5B8A', klasse='cv')}</div>
  <div>
    <div class="titel" style="font-size:{28 * g:.0f}px">{A['titel']}</div>
    <div style="color:{MATT};font-size:{17 * g:.0f}px;margin-top:{int(7 * g)}px">
      {A['interpret']} · {A['album']}</div>
    <div class="bahn" style="margin-top:{int(18 * g)}px">
      <i style="width:{A['frac'] * 100:.0f}%"></i></div>
    <div style="display:flex;justify-content:space-between;margin-top:{int(10 * g)}px">
      <span class="zeit" style="font-size:{15 * g:.0f}px">{A['pos']}</span>
      <span class="zeit" style="font-size:{15 * g:.0f}px">{A['rest']}</span></div>
  </div>
</div>'''


def _pads(g, spalten, pw, ph):
    z = []
    for i, name in enumerate(TITEL):
        k = 'an' if i == LAEUFT else ('gespielt' if i < LAEUFT else '')
        z.append(f'<span class="pad {k}" style="height:{ph * g:.0f}px">'
                 f'<span style="font-size:{13 * g:.0f}px">{name}</span></span>')
    return (f'<div class="pads" style="grid-template-columns:repeat({spalten},'
            f'{pw * g:.0f}px)">{"".join(z)}</div>')


def _fader(g, hoehe):
    z = []
    for lab, stand in FADER:
        y = (1 - stand) * (hoehe - 24) + 12
        z.append(f'''<div class="fader">
  <span class="nut" style="height:{hoehe * g:.0f}px">
    <span class="griff" style="top:{y * g:.0f}px;width:{26 * g:.0f}px;
      height:{16 * g:.0f}px"></span></span>
  <span class="flab">{lab}</span></div>''')
    return (f'<div style="display:flex;gap:{int(22 * g)}px;align-items:flex-start">'
            + ''.join(z) + '</div>')


def _transport(g, b, h):
    return f'''<div style="display:flex;gap:{int(12 * g)}px">
  <span class="tk hell" style="width:{b * .5 * g:.0f}px;height:{h * g:.0f}px">
    {prev(int(h * .34 * g), '#2A2D30')}</span>
  <span class="tk orange" style="flex:1;height:{h * g:.0f}px">
    {pausei(int(h * .40 * g), '#FFFFFF')}</span>
  <span class="tk hell" style="width:{b * .5 * g:.0f}px;height:{h * g:.0f}px">
    {nexti(int(h * .34 * g), '#2A2D30')}</span>
</div>'''


def rechner():
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;gap:52px;padding:56px 64px">
  {_schirm(g, 440, 888)}
  <div style="flex:1;min-width:0;display:flex;flex-direction:column;
    justify-content:space-between">
    <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:40px">
      {_fader(g, 210)}
      <div style="display:flex;flex-direction:column;align-items:flex-end;gap:{int(14 * g)}px">
        <span class="kap" style="font-size:{14:.0f}px">Fadertisch</span>
        <div style="display:flex;gap:{int(16 * g)}px">
          <span class="rund weiss" style="width:{62:.0f}px;height:{62:.0f}px"></span>
          <span class="rund schwarz" style="width:{62:.0f}px;height:{62:.0f}px"></span></div>
      </div>
    </div>
    {_transport(g, 220, 96)}
    <div>
      <div class="kap" style="font-size:{14:.0f}px;margin-bottom:{14:.0f}px">
        Warteschlange · antippen springt</div>
      {_pads(g, 4, 208, 92)}
    </div>
    <div style="display:flex;align-items:center;gap:{int(26 * g)}px">
      <span class="kap" style="font-size:{14:.0f}px">Sammlung</span>
      {biblio(int(24 * g), MATT)}{lupe(int(22 * g), MATT, 2.2)}{laut(int(22 * g), MATT)}
    </div>
  </div>
</div>'''
    return _css(g), body


def telefon():
    """Hochkant liegt der Bildschirm oben, das Feld unten — dieselbe Trennung
    zwischen Lesen und Greifen, nur um 90 Grad gedreht. Die Pads werden auf
    zwei Spalten breit, damit ein Titelname noch lesbar ist."""
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  gap:44px;padding:96px 56px 92px">
  {_schirm(g, 968, 900)}
  <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:30px">
    {_fader(g, 190)}
    <div style="display:flex;gap:{int(18 * g)}px">
      <span class="rund weiss" style="width:{84:.0f}px;height:{84:.0f}px"></span>
      <span class="rund schwarz" style="width:{84:.0f}px;height:{84:.0f}px"></span></div>
  </div>
  {_transport(g, 300, 132)}
  <div>
    <div class="kap" style="font-size:{16:.0f}px;margin-bottom:{14:.0f}px">
      Warteschlange · antippen springt</div>
    {_pads(g, 2, 470, 104)}
  </div>
  <div style="display:flex;align-items:center;gap:{int(34 * g)}px;margin-top:auto">
    <span class="kap" style="font-size:{16:.0f}px">Sammlung</span>
    {biblio(int(30 * g), MATT)}{lupe(int(28 * g), MATT, 2.2)}{laut(int(28 * g), MATT)}
  </div>
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('68', 'Fadertisch', art, css, body)
