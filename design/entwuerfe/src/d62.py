# -*- coding: utf-8 -*-
"""62 Leuchtmarke — die Skala ist scharf, wo man steht.

Vorlage ist eine Nahaufnahme: eine schwarze Skala mit feinen weissen Strichen
und Zahlen, die von rechts nach links kleiner werden, und darauf ein **roter,
von innen leuchtender Keil** als Marke. Die Aufnahme hat sehr wenig
Schärfentiefe — nur ein Streifen um den Keil steht klar, beide Enden laufen
in Unschärfe aus.

Genau das ist der Entwurf, und es ist keine Dekoration:

- **Die Skala trägt die ganze Warteschlange in Minuten**, nicht einen Titel.
  Die Zahlen sind die verbleibenden Minuten — deshalb werden sie nach rechts
  kleiner, wie in der Vorlage.
- **Scharf ist nur, wo die Marke steht.** Zum einen Ende hin verliert die
  Skala Kontrast und Zeichnung. Das ist die Übersetzung der Schärfentiefe in
  eine Aussage: *neben der Gegenwart liest man Sekunden ab, am Rand nur noch
  ungefähr.* Eine Skala, die überall gleich scharf wäre, verspräche eine
  Genauigkeit, die beim Ziehen niemand braucht.
- **Der Keil ist das einzige Licht.** Er leuchtet aus sich heraus und wirft
  einen Schein auf das Blech darunter. Rot kommt sonst nirgends vor — nicht
  im Titel, nicht in den Tasten. Wo Rot ist, ist die Gegenwart.

Die Titelgrenzen stehen als **hohe Striche** zwischen den feinen: man sieht,
wie weit es bis zum nächsten Stück ist, ohne eine Liste zu lesen. Gespult wird
auf der Skala selbst, über Titelgrenzen hinweg.

Abgegrenzt: 15 Weltempfänger hat auch ein Band mit Skala, aber dort *wählt*
das Band das Album. Hier wählt es nichts — es zeigt, wo man in der
Warteschlange steht, und ist zugleich die Spulfläche.
"""
from werkzeug import (A, biblio, laut, lupe, nexti, pausei, prev, schreibe,
                      MONO, SANS)

BLECH = '#101113'
STRICH = 'rgba(236,238,240,.88)'
FEIN = 'rgba(236,238,240,.42)'
ZAHL = 'rgba(236,238,240,.80)'
WEISS = '#ECEEF0'
MATT = 'rgba(236,238,240,.60)'
STUMM = 'rgba(236,238,240,.34)'
ROT = '#FF2D16'

# Die Warteschlange als Minuten. Die Marke steht bei 60 wie in der Vorlage,
# gezählt wird von links (mehr Rest) nach rechts (weniger).
ZAHLEN = [85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30]
MARKE = 60          # wo der Keil steht
GRENZEN = [78, 66, 51, 39]   # Titelgrenzen, in derselben Einheit


# Die Skala läuft nicht bis an ihre eigene Kante: die erste und die letzte
# Zahl stehen sonst zur Hälfte draussen und werden abgeschnitten.
RAND = 5.0


def _anteil(wert):
    """Von der Minutenzahl auf die Position in der Skala, in Prozent."""
    hoch, tief = ZAHLEN[0], ZAHLEN[-1]
    return RAND + (hoch - wert) / (hoch - tief) * (100 - 2 * RAND)


def _css(g):
    return f'''
.stage{{background:
    radial-gradient(150% 120% at 50% 42%,#222427 0%,{BLECH} 62%,#08090A 100%);
  font-family:{SANS};color:{WEISS};-webkit-font-smoothing:antialiased}}

.kap{{letter-spacing:.26em;text-transform:uppercase;color:{STUMM};font-weight:500}}
.bib{{display:inline-flex;align-items:center;color:{STUMM};letter-spacing:.26em;
  text-transform:uppercase;font-weight:500}}
.titel{{font-weight:300;letter-spacing:-.02em;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis}}
.unter{{color:{MATT};font-weight:300;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis}}

/* ── Die Skala ──────────────────────────────────────────────────────────
   Ein gefrästes Blech: oben eine helle Kante, unten Schatten. Die Striche
   sitzen darauf, nicht darin. */
.skala{{position:relative;border-radius:{4 * g:.0f}px;
  background:linear-gradient(180deg,#1A1C1F 0%,#0C0D0F 46%,#141619 100%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.16),inset 0 -1px 0 rgba(0,0,0,.8),
    0 {10 * g:.0f}px {26 * g:.0f}px rgba(0,0,0,.6)}}
.strich{{position:absolute;top:0;background:{FEIN};transform:translateX(-50%)}}
.strich.gross{{background:{STRICH}}}
/* Die Titelgrenze ist der einzige Strich, der durchgeht. */
.strich.grenze{{background:{STRICH};opacity:.55}}
.zahl{{position:absolute;font-family:{MONO};color:{ZAHL};transform:translateX(-50%);
  font-variant-numeric:tabular-nums}}

/* Die Schärfentiefe: ein Schleier, der genau dort durchsichtig ist, wo der
   Keil steht, und zu beiden Enden hin zumacht. Er liegt ÜBER den Strichen und
   nimmt ihnen den Kontrast — ein blur() auf der Skala würde auch den Keil
   weichzeichnen, und der ist das Einzige, was scharf bleiben muss.
   Deshalb wandert die klare Stelle mit der Marke: die Schärfe gehört zur
   Gegenwart, nicht zur Mitte des Blechs. */
.tiefe{{position:absolute;inset:0;pointer-events:none;border-radius:inherit}}

/* ── Der Keil ── Das einzige Licht im Bild. Kein Rahmen, keine Fläche:
   ein Dreieck, das glüht, und der Schein, den es auf das Blech wirft. */
.keil{{position:absolute;transform:translateX(-50%)}}
.keil .glut{{position:absolute;left:50%;transform:translateX(-50%);border-radius:50%;
  background:radial-gradient(circle,rgba(255,45,22,.60) 0%,rgba(255,45,22,0) 70%)}}
.keil .spitze{{position:relative;
  background:linear-gradient(180deg,#FF6A4E 0%,{ROT} 42%,#B01608 100%);
  clip-path:polygon(50% 0%,100% 100%,0% 100%);
  filter:drop-shadow(0 0 {9 * g:.0f}px rgba(255,45,22,.9))}}

.taste{{display:flex;align-items:center;justify-content:center;color:{MATT}}}
.taste.haupt{{color:{WEISS}}}
.zeit{{font-family:{MONO};color:{STUMM};font-variant-numeric:tabular-nums}}
'''


def _skala(g, breite, hoehe):
    """Striche, Zahlen, Titelgrenzen, Schleier, Keil — in dieser Reihenfolge."""
    teile = []
    n = (len(ZAHLEN) - 1) * 5          # fünf feine Striche je Zahl
    for i in range(n + 1):
        # Dieselbe Abbildung wie die Zahlen, sonst steht die 85 nicht auf
        # ihrem Strich — der Fehler wäre am Rand am grössten und genau dort
        # am sichtbarsten.
        x = RAND + i / n * (100 - 2 * RAND)
        gross = i % 5 == 0
        h = hoehe * (.46 if gross else .27)
        b = max(1, int((2.4 if gross else 1.4) * g))
        teile.append(f'<span class="strich{" gross" if gross else ""}" '
                     f'style="left:{x:.3f}%;width:{b}px;height:{h:.0f}px"></span>')
    for wert in ZAHLEN:
        teile.append(f'<span class="zahl" style="left:{_anteil(wert):.2f}%;'
                     f'top:{hoehe * .52:.0f}px;font-size:{25 * g:.0f}px">{wert}</span>')
    for wert in GRENZEN:
        teile.append(f'<span class="strich grenze" style="left:{_anteil(wert):.2f}%;'
                     f'width:{max(1, int(2 * g))}px;height:{hoehe * .84:.0f}px"></span>')

    m = _anteil(MARKE)
    klar = 19.0          # so weit reicht die Schärfe zu beiden Seiten
    teile.append(
        f'<span class="tiefe" style="background:linear-gradient(90deg,'
        f'rgba(16,17,19,.92) 0%,rgba(16,17,19,0) {max(0, m - klar):.1f}%,'
        f'rgba(16,17,19,0) {min(100, m + klar):.1f}%,rgba(16,17,19,.92) 100%)"></span>')

    kb, kh = int(46 * g), int(40 * g)
    glut = int(150 * g)
    teile.append(
        f'<span class="keil" style="left:{m:.2f}%;'
        f'top:{hoehe * .30:.0f}px;width:{kb}px;height:{kh}px">'
        f'<span class="glut" style="top:{-glut * .34:.0f}px;width:{glut}px;'
        f'height:{glut}px"></span>'
        f'<span class="spitze" style="display:block;width:{kb}px;height:{kh}px"></span>'
        f'</span>')
    return (f'<div class="skala" style="width:{breite};height:{hoehe}px">'
            + ''.join(teile) + '</div>')


def _kopf(g):
    return f'''<div style="display:flex;align-items:baseline;justify-content:space-between;
  gap:{int(40 * g)}px">
  <span class="bib" style="gap:{int(13 * g)}px;font-size:{20 * g:.0f}px">
    {biblio(int(21 * g), STUMM)}Sammlung · {A['sammlung']} Alben</span>
  <span class="kap" style="font-size:{19 * g:.0f}px">Warteschlange · Minuten</span>
</div>'''


def _schrift(g, titel_px):
    return f'''<div>
  <div class="titel" style="font-size:{titel_px * g:.0f}px">{A['titel']}</div>
  <div class="unter" style="font-size:{30 * g:.0f}px;margin-top:{int(12 * g)}px">
    {A['interpret']} · {A['album']} · {A['jahr']}</div>
</div>'''


def _transport(g):
    return f'''<div style="display:flex;align-items:center;justify-content:space-between">
  <span class="zeit" style="font-size:{22 * g:.0f}px">{A['pos']}</span>
  <div style="display:flex;align-items:center;gap:{int(52 * g)}px">
    <span class="taste">{prev(int(30 * g), MATT)}</span>
    <span class="taste haupt">{pausei(int(38 * g), WEISS)}</span>
    <span class="taste">{nexti(int(30 * g), MATT)}</span>
    <span class="taste">{lupe(int(26 * g), MATT)}</span>
    <span class="taste">{laut(int(26 * g), MATT)}</span>
  </div>
  <span class="zeit" style="font-size:{22 * g:.0f}px">{A['rest']}</span>
</div>'''


def rechner():
    """Die Skala über die ganze Breite — so nah wie die Vorlage."""
    g = 1.0
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:64px 96px 72px">
  {_kopf(g)}
  <div style="display:flex;flex-direction:column;gap:56px">
    {_schrift(g, 74)}
    {_skala(g, '100%', 216)}
  </div>
  {_transport(g)}
</div>'''
    return _css(g), body


def telefon():
    """Hochkant bleibt die Skala waagerecht — eine gedrehte Zahl liest niemand.

    Sie wird dafür schmaler und trägt jede zweite Zahl; die Striche bleiben,
    weil sie die Form der Skala tragen und nicht die Beschriftung."""
    g = .86
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:96px 56px 120px">
  {_kopf(g)}
  <div style="flex:1;min-height:0;display:flex;align-items:center">
    <div style="width:100%;display:flex;flex-direction:column;gap:{int(70 * g)}px">
      {_schrift(g, 66)}
      {_skala(g, '100%', 300)}
    </div>
  </div>
  {_transport(g)}
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('62', 'Leuchtmarke', art, css, body)
