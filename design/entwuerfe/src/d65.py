# -*- coding: utf-8 -*-
"""65 Milchlicht — die Skala ist Licht, nicht Farbe.

Zwei Vorlagen mit derselben Bauart: der Technics SA-5551 und der Yamaha
CR-700. Beide haben ein **hinterleuchtetes Fenster** in einer dunklen Blende
— milchiges Glas, das von innen glimmt, die Beschriftung als Aussparung
darin. Beim Technics ist das Licht kaltweiss, beim Yamaha tiefblau; die Form
ist dieselbe.

Der Entwurf macht daraus eine Regel:

- **Was gelaufen ist, ist dunkel; was kommt, leuchtet.** Die Warteschlange
  liegt als ein einziges Milchglasband da, und die Grenze zwischen hell und
  dunkel *ist* die Position. Kein Zeiger, kein Balken — die Beleuchtung
  selbst zeigt den Stand.
- **Die Titel stehen als Aussparung im Glas**, nicht darauf: sie sind dort
  lesbar, wo das Licht ist, und verschwinden im dunklen Teil fast. Damit
  liest man ohne ein einziges Symbol, wo man ist und was noch kommt.
- **Zwei kleine Fenster rechts** sind keine Pegel: das eine zählt die Titel,
  das andere die Restzeit. Sie liegen im selben Licht, also derselbe Zustand.

Die Blende ist Anthrazit, das Untergehäuse gebürstetes Aluminium, die
Bedienung eine Reihe schwarzer Druckknöpfe. Farbe gibt es keine — nur zwei
Temperaturen desselben Weiss.

Abgegrenzt: 19 Milchglaszeilen ist auch Milchglas, aber dort ist jede Zeile
eine eigene Scheibe. Hier ist das Glas *eine* Fläche, und geteilt wird sie
nicht von Kanten, sondern von der Beleuchtung.
"""
from werkzeug import (A, biblio, laut, lupe, nexti, pausei, prev, schreibe,
                      MONO, SANS)

BLENDE = '#3A3D40'
ALU = '#C9C7C2'
TINTE = '#222426'
LICHT = '#EAF4F8'
GLIMM = 'rgba(234,244,248,.20)'
MATT = 'rgba(34,36,38,.62)'
STUMM = 'rgba(34,36,38,.42)'
HELL = 'rgba(234,244,248,.86)'

TITEL = [('So What', 9.4), ('Freddie Freeloader', 9.8), ('Blue in Green', 5.6),
         ('All Blues', 11.6), ('Flamenco Sketches', 9.5)]
LAEUFT = 2
IM_TITEL = .40


def _frac():
    """Wie weit das Licht reicht: alle vollen Titel plus der Stand im laufenden."""
    ges = sum(d for _, d in TITEL)
    vor = sum(d for _, d in TITEL[:LAEUFT])
    return (vor + TITEL[LAEUFT][1] * IM_TITEL) / ges


def _css(g):
    return f'''
.stage{{background:linear-gradient(180deg,#2E3134 0%,#232628 100%);
  font-family:{SANS};color:{HELL};-webkit-font-smoothing:antialiased}}
.kap{{letter-spacing:.24em;text-transform:uppercase;color:rgba(234,244,248,.40);
  font-weight:500}}
.bib{{display:inline-flex;align-items:center;color:rgba(234,244,248,.52);
  letter-spacing:.22em;text-transform:uppercase;font-weight:500}}

/* ── Die Blende: mattes Anthrazit, in das die Fenster eingelassen sind ── */
.blende{{position:relative;background:linear-gradient(180deg,#44474A 0%,{BLENDE} 50%,#2E3134 100%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.14),inset 0 -1px 0 rgba(0,0,0,.5),
    0 {12 * g:.0f}px {30 * g:.0f}px rgba(0,0,0,.42)}}

/* ── Das Milchglas ──────────────────────────────────────────────────────
   Ein Band. Die linke Hälfte ist erloschen, die rechte glimmt. Der Übergang
   ist weich, weil Licht hinter Milchglas keine Kante hat. */
.glas{{position:relative;overflow:hidden;border-radius:{2 * g:.0f}px;
  box-shadow:inset 0 0 0 {3 * g:.0f}px #1A1C1E,
    inset 0 {6 * g:.0f}px {16 * g:.0f}px rgba(0,0,0,.55),
    0 1px 0 rgba(255,255,255,.14)}}
.grund{{position:absolute;inset:0;background:linear-gradient(180deg,#1E2225,#141718)}}
.leuchte{{position:absolute;inset:0}}
.tr{{position:absolute;top:0;bottom:0;display:flex;align-items:center;
  padding:0 {14 * g:.0f}px;overflow:hidden}}
.tr + .tr{{box-shadow:inset 1px 0 0 rgba(0,0,0,.55)}}
.tn{{font-family:{MONO};font-size:{17 * g:.0f}px;letter-spacing:.14em;
  text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
/* Die Schrift ist Aussparung: dunkel im Licht, kaum sichtbar im Dunkeln. */
.tr.hell .tn{{color:rgba(16,20,22,.78)}}
.tr.dunkel .tn{{color:rgba(234,244,248,.26)}}
.tr.jetzt .tn{{font-weight:700;color:rgba(10,14,16,.92)}}
.kante{{position:absolute;top:0;bottom:0;width:{2 * g:.0f}px;background:{LICHT};
  box-shadow:0 0 {14 * g:.0f}px {4 * g:.0f}px rgba(234,244,248,.55)}}
/* Dieselben Zeilen, nur senkrecht gestapelt — fuer das Hochformat. */
.tz{{position:absolute;left:0;right:0;display:flex;align-items:center;
  padding:0 {20 * g:.0f}px;overflow:hidden}}
.tz + .tz{{box-shadow:inset 0 1px 0 rgba(0,0,0,.55)}}
.tz.hell .tn{{color:rgba(16,20,22,.78)}}
.tz.dunkel .tn{{color:rgba(234,244,248,.26)}}
.tz.jetzt .tn{{font-weight:700;color:rgba(10,14,16,.92)}}
.kantew{{position:absolute;left:0;right:0;height:{2 * g:.0f}px;background:{LICHT};
  box-shadow:0 0 {14 * g:.0f}px {4 * g:.0f}px rgba(234,244,248,.55)}}

/* ── Die zwei kleinen Fenster ── dasselbe Licht, kleinere Scheibe ── */
.klein{{position:relative;border-radius:{2 * g:.0f}px;overflow:hidden;
  background:radial-gradient(120% 140% at 50% 120%,rgba(234,244,248,.92),rgba(234,244,248,.60));
  box-shadow:inset 0 0 0 {2 * g:.0f}px #1A1C1E,0 1px 0 rgba(255,255,255,.14);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  color:rgba(16,20,22,.86)}}
.klein .wert{{font-family:{MONO};font-variant-numeric:tabular-nums;font-weight:700}}
.klein .lab{{font-family:{MONO};letter-spacing:.18em;text-transform:uppercase;
  color:rgba(16,20,22,.52)}}

/* ── Aluminium und Druckknöpfe ── */
.alu{{position:relative;background:
    repeating-linear-gradient(90deg,rgba(255,255,255,.14) 0 1px,rgba(0,0,0,.05) 1px 3px),
    linear-gradient(180deg,#DEDCD7 0%,{ALU} 44%,#A9A7A2 100%);
  color:{TINTE};
  box-shadow:inset 0 1px 0 rgba(255,255,255,.8),inset 0 -1px 0 rgba(0,0,0,.3)}}
.druck{{border-radius:50%;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(circle at 36% 30%,#4A4C4F,#141618 76%);
  box-shadow:0 {3 * g:.0f}px {7 * g:.0f}px rgba(0,0,0,.45),
    inset 0 1px 0 rgba(255,255,255,.18)}}
.dlab{{font-family:{MONO};letter-spacing:.14em;text-transform:uppercase;color:{STUMM};
  text-align:center}}
.zeit{{font-family:{MONO};color:rgba(234,244,248,.5);font-variant-numeric:tabular-nums}}
'''


def _glas(g, hoehe):
    ges = sum(d for _, d in TITEL)
    f = _frac() * 100
    teile = [f'<span class="grund"></span>',
             f'<span class="leuchte" style="background:linear-gradient(90deg,'
             f'rgba(234,244,248,.05) 0%,rgba(234,244,248,.05) {max(0, f - 5):.1f}%,'
             f'rgba(234,244,248,.94) {min(100, f + 2):.1f}%,rgba(234,244,248,.86) 100%)"></span>']
    x = 0.0
    for i, (name, d) in enumerate(TITEL):
        b = d / ges * 100
        hell = (x + b / 2) > f
        klasse = 'jetzt' if i == LAEUFT else ('hell' if hell else 'dunkel')
        teile.append(f'<span class="tr {klasse}" style="left:{x:.2f}%;width:{b:.2f}%">'
                     f'<span class="tn">{name}</span></span>')
        x += b
    teile.append(f'<span class="kante" style="left:{f:.2f}%"></span>')
    return f'<div class="glas" style="height:{hoehe}px">{"".join(teile)}</div>'


def _glas_hoch(g, hoehe):
    """Hochkant steht das Band senkrecht: die Titel liegen untereinander, die
    Leuchtkante läuft waagerecht durch. Dieselbe Regel, gekippt."""
    ges = sum(d for _, d in TITEL)
    f = _frac() * 100
    teile = ['<span class="grund"></span>',
             f'<span class="leuchte" style="background:linear-gradient(180deg,'
             f'rgba(234,244,248,.05) 0%,rgba(234,244,248,.05) {max(0, f - 4):.1f}%,'
             f'rgba(234,244,248,.94) {min(100, f + 2):.1f}%,rgba(234,244,248,.86) 100%)"></span>']
    y = 0.0
    for i, (name, d) in enumerate(TITEL):
        h = d / ges * 100
        hell = (y + h / 2) > f
        klasse = 'jetzt' if i == LAEUFT else ('hell' if hell else 'dunkel')
        teile.append(f'<span class="tz {klasse}" style="top:{y:.2f}%;height:{h:.2f}%">'
                     f'<span class="tn">{name}</span></span>')
        y += h
    teile.append(f'<span class="kantew" style="top:{f:.2f}%"></span>')
    return f'<div class="glas" style="height:{hoehe}px">{"".join(teile)}</div>'


def _klein(g, wert, lab, b=120, h=88):
    return (f'<div class="klein" style="width:{b * g:.0f}px;height:{h * g:.0f}px;'
            f'gap:{int(5 * g)}px">'
            f'<span class="wert" style="font-size:{30 * g:.0f}px">{wert}</span>'
            f'<span class="lab" style="font-size:{13 * g:.0f}px">{lab}</span></div>')


def _druck(g, zeichen, lab, d=62):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;'
            f'gap:{int(9 * g)}px"><span class="druck" '
            f'style="width:{d * g:.0f}px;height:{d * g:.0f}px">{zeichen}</span>'
            f'<span class="dlab" style="font-size:{13 * g:.0f}px">{lab}</span></div>')


def _kopf(g):
    return f'''<div style="display:flex;align-items:baseline;justify-content:space-between">
  <span class="bib" style="gap:{int(12 * g)}px;font-size:{19 * g:.0f}px">
    {biblio(int(20 * g), 'rgba(234,244,248,.52)')}Sammlung · {A['sammlung']} Alben</span>
  <span class="kap" style="font-size:{18 * g:.0f}px">{A['album']} · {A['jahr']}</span>
</div>'''


def _schrift(g, px):
    return f'''<div>
  <div style="font-weight:300;letter-spacing:-.02em;font-size:{px * g:.0f}px;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{A['titel']}</div>
  <div style="color:rgba(234,244,248,.58);font-weight:300;margin-top:{int(10 * g)}px;
    font-size:{27 * g:.0f}px">{A['interpret']}</div>
</div>'''


def _reihe(g):
    return (f'<div style="display:flex;align-items:center;gap:{int(34 * g)}px">'
            + _druck(g, prev(int(21 * g), '#E6E8EA'), 'Zurück')
            + _druck(g, pausei(int(24 * g), '#E6E8EA'), 'Halt')
            + _druck(g, nexti(int(21 * g), '#E6E8EA'), 'Weiter')
            + _druck(g, lupe(int(19 * g), '#E6E8EA', 2.2), 'Suche')
            + _druck(g, biblio(int(19 * g), '#E6E8EA'), 'Sammlung')
            + _druck(g, laut(int(19 * g), '#E6E8EA'), 'Ton')
            + '</div>')


def rechner():
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:54px 68px 0">
  {_kopf(g)}
  <div style="display:flex;flex-direction:column;gap:38px">
    {_schrift(g, 62)}
    <div class="blende" style="margin:0 -68px;padding:34px 68px;display:flex;
      align-items:stretch;gap:30px">
      <div style="flex:1;min-width:0">{_glas(g, 116)}</div>
      {_klein(g, f'{LAEUFT + 1}/{len(TITEL)}', 'Titel', 120, 116)}
      {_klein(g, A['rest'].lstrip('-'), 'Rest', 150, 116)}
    </div>
    <div style="display:flex;justify-content:space-between">
      <span class="zeit" style="font-size:{21:.0f}px">{A['pos']}</span>
      <span class="zeit" style="font-size:{21:.0f}px">{A['rest']}</span></div>
  </div>
  <div class="alu" style="margin:0 -68px;padding:30px 68px;display:flex;
    align-items:center;justify-content:space-between">
    {_reihe(g)}
    <span class="dlab" style="font-size:{14:.0f}px">SA · Milchlicht</span>
  </div>
</div>'''
    return _css(g), body


def telefon():
    """Hochkant wird das Band höher statt breiter — sonst stehen fünf Titel auf
    1080 px nebeneinander und keiner ist mehr zu lesen."""
    g = .92
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:94px 52px 0">
  {_kopf(g)}
  <div style="display:flex;flex-direction:column;gap:{int(44 * g)}px">
    {_schrift(g, 58)}
    <div class="blende" style="margin:0 -52px;padding:{int(36 * g)}px {int(52 * g)}px;
      display:flex;flex-direction:column;gap:{int(24 * g)}px">
      {_glas_hoch(g, 620)}
      <div style="display:flex;gap:{int(20 * g)}px">
        {_klein(g, f'{LAEUFT + 1}/{len(TITEL)}', 'Titel', 200, 104)}
        {_klein(g, A['rest'].lstrip('-'), 'Rest', 240, 104)}
        <div style="flex:1"></div>
      </div>
    </div>
    <div style="display:flex;justify-content:space-between">
      <span class="zeit" style="font-size:{23 * g:.0f}px">{A['pos']}</span>
      <span class="zeit" style="font-size:{23 * g:.0f}px">{A['rest']}</span></div>
  </div>
  <div class="alu" style="margin:0 -52px;padding:{int(40 * g)}px {int(40 * g)}px
    {int(52 * g)}px;display:flex;align-items:center;justify-content:center">
    <div style="display:flex;align-items:center;gap:{int(30 * g)}px">
      {_druck(g, prev(int(26 * g), '#E6E8EA'), 'Zurück', 96)}
      {_druck(g, pausei(int(30 * g), '#E6E8EA'), 'Halt', 96)}
      {_druck(g, nexti(int(26 * g), '#E6E8EA'), 'Weiter', 96)}
      {_druck(g, lupe(int(24 * g), '#E6E8EA', 2.2), 'Suche', 96)}
      {_druck(g, biblio(int(24 * g), '#E6E8EA'), 'Sammlung', 96)}
    </div>
  </div>
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('65', 'Milchlicht', art, css, body)
