# -*- coding: utf-8 -*-
"""63 Glasgravur — nichts steht auf der Fläche, alles steht in ihr.

Vorlage ist der McIntosh MX110: eine schwarze Glasscheibe, in die die Skala
**graviert** ist — weisse Zahlen und Striche, die von hinten angeleuchtet
werden —, darunter eine gebürstete Blende aus Aluminium mit gerändelten
Knöpfen und schwarzen Kippschaltern. Und **ein** Stück Farbe im ganzen Gerät:
ein kurzer blauer Balken hinter dem Glas.

Der Entwurf nimmt genau das:

- **Die Warteschlange ist die Gravur.** Jeder Titel ein Strich, jede fünfte
  Grenze eine Zahl. Weiss auf Schwarz, aber nicht gedruckt: die Zeichen
  sitzen *hinter* der Scheibe, mit einer hellen Oberkante und einem Schatten
  darunter, wie ausgefräst.
- **Der blaue Balken ist die Gegenwart** und das Einzige, was leuchtet. Er
  liegt hinter dem Glas, also weicher als die Gravur — Licht streut, Schrift
  nicht. Rot und Gelb kommen nirgends vor.
- **Bedient wird auf der Blende, nicht auf dem Glas.** Das Glas ist Anzeige;
  die Kippschalter darunter sind Transport, der gerändelte Knopf ist die
  Lautstärke. Gespult wird trotzdem am Glas — dort steht ja, wo man ist.

Abgegrenzt: 76 Leuchtmarke hat auch eine Skala mit Marke, aber dort ist die
Marke ein glühender Keil auf Blech und die Schärfe wandert mit. Hier gibt es
keine Unschärfe: Glas ist überall gleich klar, und das ist der Unterschied
zwischen einer Nahaufnahme und einem Gerät, das man aus zwei Metern liest.
"""
from werkzeug import (A, biblio, laut, lupe, nexti, pausei, prev, schreibe,
                      MONO, SANS)

GLAS = '#0A0B0D'
BLENDE = '#B9B7B0'
GRAVUR = '#F4F2EC'
FEIN = 'rgba(244,242,236,.46)'
MATT = 'rgba(244,242,236,.62)'
STUMM = 'rgba(244,242,236,.34)'
BLAU = '#4FC3F7'
TINTE = '#26262A'

# Die Warteschlange in Minuten seit dem Anfang — die Skala zählt aufwärts,
# wie die Frequenzskala der Vorlage.
GRENZEN = [0, 9, 19, 24, 36, 44, 52, 61, 70]   # Titelanfänge
MARKE = 21.5                                    # wo wir stehen
ENDE = 78
RAND = 4.5


def _x(wert):
    return RAND + wert / ENDE * (100 - 2 * RAND)


def _css(g):
    return f'''
.stage{{background:linear-gradient(180deg,#17171A 0%,#0E0E10 34%,#141416 100%);
  font-family:{SANS};color:{GRAVUR};-webkit-font-smoothing:antialiased}}
.kap{{letter-spacing:.26em;text-transform:uppercase;color:{STUMM};font-weight:500}}
.bib{{display:inline-flex;align-items:center;color:{STUMM};letter-spacing:.24em;
  text-transform:uppercase;font-weight:500}}

/* ── Die Scheibe ────────────────────────────────────────────────────────
   Schwarzes Glas: oben ein schmaler Lichtreflex, sonst tief. Was darauf
   liegt, liegt in Wahrheit dahinter — deshalb die helle Oberkante an jedem
   Strich und der Schatten darunter. */
.glas{{position:relative;overflow:hidden;background:
    linear-gradient(180deg,rgba(255,255,255,.10) 0%,rgba(255,255,255,.015) 9%,
      rgba(0,0,0,0) 26%),{GLAS};
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.09),
    inset 0 {14 * g:.0f}px {30 * g:.0f}px rgba(0,0,0,.75),
    0 {12 * g:.0f}px {34 * g:.0f}px rgba(0,0,0,.55)}}
.gr{{position:absolute;background:{FEIN};transform:translateX(-50%);
  box-shadow:0 -1px 0 rgba(255,255,255,.30),0 1px 2px rgba(0,0,0,.9)}}
.gr.gross{{background:{GRAVUR}}}
.zahl{{position:absolute;font-family:{MONO};color:{GRAVUR};transform:translateX(-50%);
  font-variant-numeric:tabular-nums;
  text-shadow:0 -1px 0 rgba(255,255,255,.35),0 1px 3px rgba(0,0,0,.95)}}
.marke{{position:absolute;transform:translateX(-50%);border-radius:2px;
  background:linear-gradient(180deg,#8FDCFF 0%,{BLAU} 55%,#1E88C7 100%);
  box-shadow:0 0 {22 * g:.0f}px {6 * g:.0f}px rgba(79,195,247,.55),
    0 0 {60 * g:.0f}px {18 * g:.0f}px rgba(79,195,247,.22)}}
.schrift{{position:absolute;font-family:{MONO};letter-spacing:.10em;
  text-transform:uppercase;color:{MATT}}}

/* ── Die Blende ── gebürstetes Aluminium, waagerechte Faser. */
.blende{{position:relative;background:
    repeating-linear-gradient(90deg,rgba(255,255,255,.10) 0 1px,
      rgba(0,0,0,.05) 1px 3px),
    linear-gradient(180deg,#D3D1CA 0%,{BLENDE} 46%,#9C9A93 100%);
  color:{TINTE};
  box-shadow:inset 0 1px 0 rgba(255,255,255,.75),inset 0 -1px 0 rgba(0,0,0,.35),
    0 {6 * g:.0f}px {18 * g:.0f}px rgba(0,0,0,.45)}}
.blende .kap{{color:rgba(38,38,42,.55)}}

/* Der Kippschalter: ein schwarzer Hebel in einer gefrästen Nut. Gedrückt
   heisst hier oben — die Haupttaste steht anders als die anderen. */
.kipp{{position:relative;display:flex;align-items:flex-end;justify-content:center;
  border-radius:{3 * g:.0f}px;background:linear-gradient(180deg,#8E8C85,#C6C4BD);
  box-shadow:inset 0 1px 3px rgba(0,0,0,.55)}}
.kipp i{{display:block;border-radius:{2 * g:.0f}px;
  background:linear-gradient(180deg,#3A3A3E 0%,#111113 60%,#26262A 100%);
  box-shadow:0 2px 5px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.16)}}
.kipp.an i{{background:linear-gradient(180deg,#26262A 0%,#111113 40%,#3A3A3E 100%)}}
.kipplab{{font-family:{MONO};letter-spacing:.16em;text-transform:uppercase;
  color:rgba(38,38,42,.62);text-align:center}}

/* Der gerändelte Knopf — die Rändelung ist gezeichnet, nicht behauptet. */
.knopf{{border-radius:50%;position:relative;background:
    repeating-conic-gradient(from 0deg,#EDEBE4 0deg 2deg,#A8A69F 2deg 4deg),
    radial-gradient(circle at 34% 28%,#FFFFFF,#9B9992);
  box-shadow:inset 0 0 0 {3 * g:.0f}px #CFCDC6,0 {4 * g:.0f}px {10 * g:.0f}px rgba(0,0,0,.45)}}
.knopf::after{{content:'';position:absolute;left:50%;top:{9 * g:.0f}px;width:{2 * g:.0f}px;
  height:34%;transform:translateX(-50%);background:{TINTE};border-radius:1px}}
.zeit{{font-family:{MONO};color:{STUMM};font-variant-numeric:tabular-nums}}
'''


def _glas(g, hoehe):
    """Striche, Zahlen, Titelgrenzen, der blaue Balken, die eingeätzte Schrift."""
    t = []
    n = 78
    for i in range(n + 1):
        x = RAND + i / n * (100 - 2 * RAND)
        gross = i % 5 == 0
        h = hoehe * (.20 if gross else .12)
        b = max(1, int((2.2 if gross else 1.3) * g))
        t.append(f'<span class="gr{" gross" if gross else ""}" style="left:{x:.3f}%;'
                 f'top:{hoehe * .30:.0f}px;width:{b}px;height:{h:.0f}px"></span>')
    for wert in GRENZEN:
        t.append(f'<span class="gr gross" style="left:{_x(wert):.2f}%;'
                 f'top:{hoehe * .22:.0f}px;width:{max(1, int(2.6 * g))}px;'
                 f'height:{hoehe * .34:.0f}px"></span>')
        t.append(f'<span class="zahl" style="left:{_x(wert):.2f}%;top:{hoehe * .07:.0f}px;'
                 f'font-size:{30 * g:.0f}px">{wert}</span>')
    t.append(f'<span class="marke" style="left:{_x(MARKE):.2f}%;top:{hoehe * .64:.0f}px;'
             f'width:{max(3, int(7 * g))}px;height:{hoehe * .22:.0f}px"></span>')
    t.append(f'<span class="schrift" style="left:{RAND}%;bottom:{16 * g:.0f}px;'
             f'font-size:{19 * g:.0f}px">Warteschlange · Minuten</span>')
    t.append(f'<span class="schrift" style="right:{RAND}%;bottom:{16 * g:.0f}px;'
             f'font-size:{19 * g:.0f}px">{A["album"]} · {A["jahr"]}</span>')
    return f'<div class="glas" style="height:{hoehe}px">{"".join(t)}</div>'


def _kipp(g, zeichen, label, an=False, breite=54, hoehe=104):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;'
            f'gap:{int(10 * g)}px">'
            f'<span class="kipp{" an" if an else ""}" '
            f'style="width:{breite * g:.0f}px;height:{hoehe * g:.0f}px;'
            f'padding:{5 * g:.0f}px">'
            f'<i style="width:{(breite - 16) * g:.0f}px;height:{hoehe * .56 * g:.0f}px;'
            f'display:flex;align-items:center;justify-content:center">{zeichen}</i></span>'
            f'<span class="kipplab" style="font-size:{15 * g:.0f}px">{label}</span></div>')


def _blende(g, hoehe):
    reihe = ''.join([
        _kipp(g, prev(int(20 * g), '#E8E6DF'), 'Zurück'),
        _kipp(g, pausei(int(22 * g), '#E8E6DF'), 'Halt', an=True),
        _kipp(g, nexti(int(20 * g), '#E8E6DF'), 'Weiter'),
        _kipp(g, lupe(int(19 * g), '#E8E6DF', 2.2), 'Suche'),
    ])
    return f'''<div class="blende" style="height:{hoehe}px;display:flex;align-items:center;
  justify-content:space-between;padding:0 {int(52 * g)}px">
  <div style="display:flex;align-items:center;gap:{int(34 * g)}px">{reihe}</div>
  <div style="display:flex;align-items:center;gap:{int(40 * g)}px">
    <div style="display:flex;flex-direction:column;align-items:center;gap:{int(10 * g)}px">
      <span class="knopf" style="width:{92 * g:.0f}px;height:{92 * g:.0f}px"></span>
      <span class="kipplab" style="font-size:{15 * g:.0f}px">Lautstärke</span></div>
  </div>
</div>'''


def _kopf(g):
    return f'''<div style="display:flex;align-items:baseline;justify-content:space-between;gap:{int(30 * g)}px">
  <span class="bib" style="gap:{int(12 * g)}px;font-size:{19 * g:.0f}px">
    {biblio(int(20 * g), STUMM)}Sammlung · {A['sammlung']} Alben</span>
  <span class="kap" style="font-size:{18 * g:.0f}px">MX · Warteschlange</span>
</div>'''


def _schrift(g, px):
    return f'''<div>
  <div style="font-weight:300;letter-spacing:-.02em;font-size:{px * g:.0f}px;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{A['titel']}</div>
  <div style="color:{MATT};font-weight:300;margin-top:{int(11 * g)}px;
    font-size:{28 * g:.0f}px">{A['interpret']}</div>
</div>'''


def rechner():
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:56px 72px 0">
  {_kopf(g)}
  <div style="display:flex;flex-direction:column;gap:44px">
    {_schrift(g, 66)}
    {_glas(g, 250)}
    <div style="display:flex;justify-content:space-between">
      <span class="zeit" style="font-size:{22:.0f}px">{A['pos']}</span>
      <span class="zeit" style="font-size:{22:.0f}px">{A['rest']}</span></div>
  </div>
  <div style="margin:0 -72px">{_blende(g, 210)}</div>
</div>'''
    return _css(g), body


def telefon():
    """Hochkant bleibt die Reihenfolge: Glas oben, Blende unten. Die Blende
    wird zweizeilig, weil vier Kippschalter und ein Knopf nebeneinander auf
    1080 px nicht mehr in Daumenbreite stehen."""
    g = .92
    reihe = ''.join([
        _kipp(g, prev(int(24 * g), '#E8E6DF'), 'Zurück', breite=124, hoehe=118),
        _kipp(g, pausei(int(28 * g), '#E8E6DF'), 'Halt', an=True, breite=124, hoehe=118),
        _kipp(g, nexti(int(24 * g), '#E8E6DF'), 'Weiter', breite=124, hoehe=118),
        _kipp(g, lupe(int(22 * g), '#E8E6DF', 2.2), 'Suche', breite=124, hoehe=118),
    ])
    blende = f'''<div class="blende" style="padding:{int(40 * g)}px {int(44 * g)}px;
  display:flex;flex-direction:column;gap:{int(34 * g)}px;align-items:center">
  <div style="display:flex;gap:{int(26 * g)}px">{reihe}</div>
  <div style="display:flex;align-items:center;gap:{int(26 * g)}px;width:100%">
    <span class="knopf" style="width:{104 * g:.0f}px;height:{104 * g:.0f}px;flex:none"></span>
    <span class="kipplab" style="font-size:{19 * g:.0f}px;text-align:left">Lautstärke</span>
    <span style="margin-left:auto">{laut(int(30 * g), 'rgba(38,38,42,.62)')}</span>
  </div>
</div>'''
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:92px 56px 0">
  {_kopf(g)}
  <div style="flex:1;min-height:0;display:flex;align-items:center">
    <div style="width:100%;display:flex;flex-direction:column;gap:{int(58 * g)}px">
      {_schrift(g, 62)}
      {_glas(g, 300)}
      <div style="display:flex;justify-content:space-between">
        <span class="zeit" style="font-size:{24 * g:.0f}px">{A['pos']}</span>
        <span class="zeit" style="font-size:{24 * g:.0f}px">{A['rest']}</span></div>
    </div>
  </div>
  <div style="margin:0 -56px">{blende}</div>
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('63', 'Glasgravur', art, css, body)
