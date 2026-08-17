# -*- coding: utf-8 -*-
"""66 Automatik — fünf Merkplätze, in einem Griff erreichbar.

Vorlage ist ein schwarzer Receiver mit türkis leuchtender Skala und, rechts
daneben, einer Spalte aus fünf senkrechten Schiebern unter der Aufschrift
**FM AUTOMATIC TUNING**: die Stationstasten. Jeder Schieber steht auf einer
eigenen kleinen Skala, jeder trägt eine orange Marke.

Genau diese Spalte ist der Entwurf, und sie ist das Einzige darin, was es in
der App bisher nicht gibt:

- **Fünf Merkplätze für Alben.** Was man oft hört, schiebt man auf einen
  Platz und erreicht es von da an mit einem Griff — ohne Sammlung, ohne
  Suche, ohne Liste. Das ist keine Wiedergabeliste: fünf Plätze, mehr nicht,
  und ein sechstes Album verdrängt eines davon.
- **Der Schieber steht dort, wo das Album steht.** Er ist zugleich Merkplatz
  und Standanzeige: oben heisst Anfang, unten heisst Schluss. Wer einen Platz
  antippt, springt dorthin — wer den Schieber zieht, spult darin.
- **Türkis ist Anzeige, Orange ist Besitz.** Die Skala und die Schrift
  leuchten türkis, die fünf Marken sind orange. Zwei Farben, zwei Bedeutungen,
  und keine dritte.

Die grosse Skala links trägt weiter die Warteschlange; sie ist die Fläche,
auf der ohne Merkplatz gespult wird.

Abgegrenzt: kein anderer Entwurf im Register hat einen Direktzugriff, der die
Sammlung überspringt. Das ist der Grund, ihn zu bauen — oder ausdrücklich
sein zu lassen.
"""
from werkzeug import (A, biblio, laut, lupe, nexti, pausei, prev, schreibe,
                      MONO, SANS)

SCHWARZ = '#0C0D0F'
PANEL = '#17191C'
TUERKIS = '#4FE0D8'
TUERKIS2 = 'rgba(79,224,216,.42)'
ORANGE = '#FF7A2F'
HELL = '#E8EEF0'
MATT = 'rgba(232,238,240,.58)'
STUMM = 'rgba(232,238,240,.34)'

PLAETZE = [('Kind of Blue', .38), ('Autobahn', .00), ('Blue', .72),
           ('OK Computer', .21), ('Graceland', .55)]
AKTIV = 0
RAND = 5.0


def _css(g):
    return f'''
.stage{{background:linear-gradient(180deg,#1B1E21 0%,{SCHWARZ} 46%,#111315 100%);
  font-family:{SANS};color:{HELL};-webkit-font-smoothing:antialiased}}
.kap{{letter-spacing:.26em;text-transform:uppercase;color:{STUMM};font-weight:500}}
.bib{{display:inline-flex;align-items:center;color:{MATT};letter-spacing:.22em;
  text-transform:uppercase;font-weight:500}}

/* ── Die grosse Skala: türkis auf Schwarz, hinter Glas ── */
.skala{{position:relative;overflow:hidden;border-radius:{2 * g:.0f}px;background:{PANEL};
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.07),
    inset 0 {8 * g:.0f}px {20 * g:.0f}px rgba(0,0,0,.6)}}
.tick{{position:absolute;background:{TUERKIS2};transform:translateX(-50%)}}
.tick.gross{{background:{TUERKIS};box-shadow:0 0 {6 * g:.0f}px rgba(79,224,216,.7)}}
.zahl{{position:absolute;font-family:{MONO};color:{TUERKIS};transform:translateX(-50%);
  font-variant-numeric:tabular-nums;text-shadow:0 0 {10 * g:.0f}px rgba(79,224,216,.6)}}
.nadel{{position:absolute;transform:translateX(-50%);background:{ORANGE};border-radius:1px;
  box-shadow:0 0 {14 * g:.0f}px {3 * g:.0f}px rgba(255,122,47,.7)}}
.slab{{position:absolute;font-family:{MONO};letter-spacing:.16em;text-transform:uppercase;
  color:{TUERKIS2}}}

/* ── Die Merkplätze: fünf Schienen mit oranger Marke ─────────────────────
   Jede Schiene ist eine eigene kleine Skala; die Marke ist Platz und Stand
   in einem. */
.plaetze{{display:flex;gap:{int(16 * g)}px}}
.platz{{display:flex;flex-direction:column;align-items:center;gap:{int(10 * g)}px}}
.schiene{{position:relative;border-radius:{3 * g:.0f}px;background:
    linear-gradient(180deg,#0A0B0C,#16181B);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.08),inset 0 2px 6px rgba(0,0,0,.7)}}
.schiene i{{position:absolute;left:50%;transform:translateX(-50%);width:{2 * g:.0f}px;
  top:{8 * g:.0f}px;bottom:{8 * g:.0f}px;background:{TUERKIS2}}}
.marke{{position:absolute;left:50%;transform:translate(-50%,-50%);border-radius:{2 * g:.0f}px;
  background:linear-gradient(180deg,#FFA268,{ORANGE});
  box-shadow:0 0 {10 * g:.0f}px rgba(255,122,47,.6),0 1px 2px rgba(0,0,0,.7)}}
.platz.an .schiene{{box-shadow:inset 0 0 0 1px rgba(79,224,216,.55),
    inset 0 2px 6px rgba(0,0,0,.7),0 0 {14 * g:.0f}px rgba(79,224,216,.22)}}
.pnr{{font-family:{MONO};color:{TUERKIS};font-variant-numeric:tabular-nums}}
.pname{{font-family:{MONO};letter-spacing:.06em;color:{STUMM};text-align:center;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}}
.platz.an .pname{{color:{MATT}}}

.taste{{display:flex;align-items:center;justify-content:center;border-radius:50%;
  background:radial-gradient(circle at 36% 30%,#33373B,#0E1012 78%);
  box-shadow:0 {3 * g:.0f}px {8 * g:.0f}px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.14)}}
.zeit{{font-family:{MONO};color:{STUMM};font-variant-numeric:tabular-nums}}
'''


def _skala(g, hoehe):
    t = []
    n = 60
    for i in range(n + 1):
        x = RAND + i / n * (100 - 2 * RAND)
        gross = i % 5 == 0
        t.append(f'<span class="tick{" gross" if gross else ""}" style="left:{x:.3f}%;'
                 f'top:{hoehe * .48:.0f}px;width:{max(1, int((2.2 if gross else 1.2) * g))}px;'
                 f'height:{hoehe * (.20 if gross else .12):.0f}px"></span>')
    for k, wert in enumerate([0, 9, 19, 24, 36, 44, 52, 61, 70]):
        x = RAND + wert / 78 * (100 - 2 * RAND)
        t.append(f'<span class="zahl" style="left:{x:.2f}%;top:{hoehe * .14:.0f}px;'
                 f'font-size:{34 * g:.0f}px">{wert}</span>')
    x = RAND + 21.5 / 78 * (100 - 2 * RAND)
    t.append(f'<span class="nadel" style="left:{x:.2f}%;top:{hoehe * .08:.0f}px;'
             f'width:{max(2, int(3 * g))}px;height:{hoehe * .70:.0f}px"></span>')
    t.append(f'<span class="slab" style="left:{RAND}%;bottom:{9 * g:.0f}px;'
             f'font-size:{16 * g:.0f}px">Warteschlange · Minuten</span>')
    return f'<div class="skala" style="height:{hoehe}px">{"".join(t)}</div>'


def _plaetze(g, hoehe, breite=54):
    s = []
    for i, (name, stand) in enumerate(PLAETZE):
        y = 8 + stand * (hoehe - 16)
        s.append(f'''<div class="platz{" an" if i == AKTIV else ""}"
  style="width:{breite * g:.0f}px">
  <span class="pnr" style="font-size:{15 * g:.0f}px">{i + 1}</span>
  <span class="schiene" style="width:{breite * g:.0f}px;height:{hoehe * g:.0f}px">
    <i></i><span class="marke" style="top:{y * g:.0f}px;width:{(breite - 16) * g:.0f}px;
      height:{13 * g:.0f}px"></span></span>
  <span class="pname" style="font-size:{12 * g:.0f}px;width:{breite * g:.0f}px">{name}</span>
</div>''')
    return f'<div class="plaetze">{"".join(s)}</div>'


def _kopf(g):
    return f'''<div style="display:flex;align-items:baseline;justify-content:space-between">
  <span class="bib" style="gap:{int(12 * g)}px;font-size:{19 * g:.0f}px">
    {biblio(int(20 * g), MATT)}Sammlung · {A['sammlung']} Alben</span>
  <span class="kap" style="font-size:{18 * g:.0f}px">Automatic Tuning</span>
</div>'''


def _schrift(g, px):
    return f'''<div>
  <div style="font-weight:300;letter-spacing:-.02em;font-size:{px * g:.0f}px;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{A['titel']}</div>
  <div style="color:{MATT};font-weight:300;margin-top:{int(10 * g)}px;
    font-size:{27 * g:.0f}px">{A['interpret']} · {A['album']}</div>
</div>'''


def _tasten(g, d=64):
    z = [prev(int(22 * g), HELL), pausei(int(26 * g), HELL), nexti(int(22 * g), HELL),
         lupe(int(20 * g), HELL, 2.2), biblio(int(20 * g), HELL), laut(int(20 * g), HELL)]
    return (f'<div style="display:flex;align-items:center;gap:{int(22 * g)}px">'
            + ''.join(f'<span class="taste" style="width:{d * g:.0f}px;'
                      f'height:{d * g:.0f}px">{x}</span>' for x in z) + '</div>')


def rechner():
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:56px 72px 60px">
  {_kopf(g)}
  {_schrift(g, 64)}
  <div style="display:flex;align-items:flex-end;gap:56px">
    <div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:20px">
      {_skala(g, 190)}
      <div style="display:flex;justify-content:space-between">
        <span class="zeit" style="font-size:21px">{A['pos']}</span>
        <span class="zeit" style="font-size:21px">{A['rest']}</span></div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:{int(14 * g)}px">
      <span class="kap" style="font-size:{15 * g:.0f}px">Merkplätze</span>
      {_plaetze(g, 190)}
    </div>
  </div>
  {_tasten(g)}
</div>'''
    return _css(g), body


def telefon():
    """Hochkant liegen die Merkplätze unter der Skala und werden breiter — am
    Telefon ist ein Platz eine Daumenfläche und keine Schiene."""
    g = .92
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:94px 52px 96px">
  {_kopf(g)}
  {_schrift(g, 58)}
  <div style="display:flex;flex-direction:column;gap:{int(20 * g)}px">
    {_skala(g, 230)}
    <div style="display:flex;justify-content:space-between">
      <span class="zeit" style="font-size:{23 * g:.0f}px">{A['pos']}</span>
      <span class="zeit" style="font-size:{23 * g:.0f}px">{A['rest']}</span></div>
  </div>
  <div style="display:flex;flex-direction:column;gap:{int(16 * g)}px">
    <span class="kap" style="font-size:{17 * g:.0f}px">Merkplätze</span>
    {_plaetze(g, 300, 172)}
  </div>
  {_tasten(g, 120)}
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('66', 'Automatik', art, css, body)
