# -*- coding: utf-8 -*-
"""67 Rasterschrift — alles aus einem Punktraster, auch die Zeit.

Vorlage ist der Gryphon Ethos: eine schwarze Glasfront, in der eine
**Punktmatrix** in Cyan leuchtet — Ziffern, Wörter und ein kleines Quadrat aus
Punkten, alles aus derselben Rasterzelle gebaut. Darunter sitzen die Tasten
als kaum sichtbare Markierungen im Glas.

Der Entwurf nimmt das Raster als Gesetz:

- **Es gibt nur eine Zeichenform.** Titel, Zeit, Fortschritt und die
  Warteschlange werden aus demselben Punktraster gezeichnet. Der Balken ist
  keine Linie, sondern eine Reihe Punkte, die angehen — die Anzeige kann
  gar nicht feiner sein als das Raster, und das ist ehrlich: eine Position
  auf zehn Sekunden genau abzulesen braucht niemand.
- **Cyan ist Licht, nicht Farbe.** Was aus ist, ist nicht grau, sondern
  *aus* — ein dunkler Punkt im Glas. Deshalb wirkt die Anzeige wie eine
  Röhre und nicht wie ein Bildschirm.
- **Die Tasten sind kaum da.** Vier Markierungen unten links, in Glas geätzt,
  ohne Kontur. Man findet sie über die Anordnung, nicht über eine Form.

Das Rot der Vorlage — dort ein Firmenzeichen — wird hier **der laufende
Titel**: ein einziger roter Punkt in der Warteschlange. Sonst kommt Rot nicht
vor.

Abgegrenzt: 68 Fadertisch nutzt dasselbe Schwarz, aber dort ist die
Bedienfläche der Entwurf. Hier ist es die Anzeige, und die Bedienung
verschwindet absichtlich.
"""
import math

from werkzeug import A, schreibe, MONO, SANS

GLAS = '#0A0B0C'
CYAN = '#3FD9F5'
CYAN_AUS = 'rgba(63,217,245,.10)'
ROT = '#E23A2E'
MATT = 'rgba(63,217,245,.52)'
STUMM = 'rgba(63,217,245,.28)'

# Fünf mal sieben Punkte je Zeichen — die Ziffern als Bitmuster, damit die
# Zeit wirklich aus dem Raster kommt und nicht aus einer Schrift.
ZIFFERN = {
 '0': ('01110', '10001', '10011', '10101', '11001', '10001', '01110'),
 '1': ('00100', '01100', '00100', '00100', '00100', '00100', '01110'),
 '2': ('01110', '10001', '00001', '00010', '00100', '01000', '11111'),
 '3': ('11111', '00010', '00100', '00010', '00001', '10001', '01110'),
 '4': ('00010', '00110', '01010', '10010', '11111', '00010', '00010'),
 '5': ('11111', '10000', '11110', '00001', '00001', '10001', '01110'),
 '6': ('00110', '01000', '10000', '11110', '10001', '10001', '01110'),
 '7': ('11111', '00001', '00010', '00100', '01000', '01000', '01000'),
 '8': ('01110', '10001', '10001', '01110', '10001', '10001', '01110'),
 '9': ('01110', '10001', '10001', '01111', '00001', '00010', '01100'),
 ':': ('00000', '00100', '00100', '00000', '00100', '00100', '00000'),
}


def _css(g):
    return f'''
.stage{{background:radial-gradient(130% 110% at 50% 20%,#191B1D 0%,{GLAS} 58%,#050506 100%);
  font-family:{SANS};color:{CYAN};-webkit-font-smoothing:antialiased}}
.kap{{letter-spacing:.30em;text-transform:uppercase;color:{STUMM};font-weight:500}}
.pkt{{position:absolute;border-radius:50%}}
.an{{background:{CYAN};box-shadow:0 0 {5 * g:.0f}px rgba(63,217,245,.85)}}
.aus{{background:{CYAN_AUS}}}
.rot{{background:{ROT};box-shadow:0 0 {7 * g:.0f}px rgba(226,58,46,.9)}}
.raster{{position:relative}}
.titel{{font-family:{MONO};letter-spacing:.22em;text-transform:uppercase;color:{CYAN};
  text-shadow:0 0 {14 * g:.0f}px rgba(63,217,245,.55);white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}}
.unter{{font-family:{MONO};letter-spacing:.20em;text-transform:uppercase;color:{MATT}}}
/* Die Tasten sind in das Glas geätzt: eine Spur heller als das Glas, sonst
   nichts. Kein Rahmen, keine Fläche. */
.geaetzt{{display:flex;align-items:center;justify-content:center;border-radius:{3 * g:.0f}px;
  background:rgba(255,255,255,.045);box-shadow:inset 0 1px 0 rgba(255,255,255,.07)}}
'''


def _matrix(g, muster, d, lueck, farbe='an'):
    """Ein Punktfeld aus Zeilen von '0'/'1'. d ist der Punktabstand."""
    r = d * .40
    p = []
    for y, zeile in enumerate(muster):
        for x, c in enumerate(zeile):
            k = farbe if c == '1' else 'aus'
            p.append(f'<span class="pkt {k}" style="left:{x * d:.1f}px;top:{y * d:.1f}px;'
                     f'width:{r * 2:.1f}px;height:{r * 2:.1f}px"></span>')
    b = len(muster[0]) * d
    h = len(muster) * d
    return (f'<span class="raster" style="display:inline-block;width:{b:.0f}px;'
            f'height:{h:.0f}px;margin-right:{lueck:.0f}px">{"".join(p)}</span>')


def _zeit(g, text, d):
    return ''.join(_matrix(g, ZIFFERN[c], d, d * .8) for c in text if c in ZIFFERN)


def _bahn(g, breite, d, frac):
    """Der Fortschritt als Punktreihe — feiner als das Raster geht es nicht."""
    n = int(breite // d)
    p = []
    for i in range(n):
        an = i / n <= frac
        p.append(f'<span class="pkt {"an" if an else "aus"}" style="left:{i * d:.1f}px;'
                 f'top:0;width:{d * .58:.1f}px;height:{d * .58:.1f}px"></span>')
    return (f'<span class="raster" style="display:block;width:{n * d:.0f}px;'
            f'height:{d * .58:.0f}px">{"".join(p)}</span>')


def _queue(g, d, n=5, laeuft=2):
    """Die Warteschlange: je Titel eine Punktsäule, der laufende rot."""
    p = []
    for i in range(n):
        hoehe = 3 + (i % 3)
        for y in range(hoehe):
            k = 'rot' if i == laeuft else ('an' if i < laeuft else 'aus')
            p.append(f'<span class="pkt {k}" style="left:{i * d * 1.8:.1f}px;'
                     f'top:{(4 - y) * d:.1f}px;width:{d * .58:.1f}px;'
                     f'height:{d * .58:.1f}px"></span>')
    return (f'<span class="raster" style="display:inline-block;width:{n * d * 1.8:.0f}px;'
            f'height:{5 * d:.0f}px">{"".join(p)}</span>')


def _geaetzt(g, gross=False):
    z = [('◀◀', 'Zurück'), ('▮▮', 'Halt'), ('▶▶', 'Weiter'), ('◎', 'Sammlung')]
    s = int((46 if gross else 30) * g)
    return ''.join(
        f'<span class="geaetzt" style="width:{s}px;height:{s}px;font-size:{s * .34:.0f}px;'
        f'color:{MATT}" title="{lab}">{zei}</span>' for zei, lab in z)


def _feld(g, d, breite):
    """Der eigentliche Anzeigeblock — Titelnummer, Raster, Gesamtzeit."""
    return f'''<div style="margin-top:{int(52 * g)}px;display:flex;align-items:flex-start;
  gap:{int(72 * g)}px;flex-wrap:wrap">
  <div>
    <div class="unter" style="font-size:{15 * g:.0f}px;margin-bottom:{int(9 * g)}px">Titel</div>
    <div style="display:flex;align-items:flex-start">{_zeit(g, '03', d)}</div>
    <div class="unter" style="font-size:{14 * g:.0f}px;margin-top:{int(9 * g)}px">von 05</div>
  </div>
  <div>
    <div class="unter" style="font-size:{15 * g:.0f}px;margin-bottom:{int(9 * g)}px">Warteschlange</div>
    <div style="height:{7 * d:.0f}px;display:flex;align-items:flex-end">{_queue(g, d)}</div>
    <div class="unter" style="font-size:{14 * g:.0f}px;margin-top:{int(9 * g)}px">rot = läuft</div>
  </div>
  <div>
    <div class="unter" style="font-size:{15 * g:.0f}px;margin-bottom:{int(9 * g)}px">Restzeit</div>
    <div style="display:flex;align-items:flex-start">{_zeit(g, '03:23', d)}</div>
    <div class="unter" style="font-size:{14 * g:.0f}px;margin-top:{int(9 * g)}px">
      PCM 44K1 · {A['album']}</div>
  </div>
</div>
<div style="margin-top:{int(34 * g)}px">{_bahn(g, breite, d * 1.1, A['frac'])}</div>'''


def rechner():
    g, d = 1.0, 13
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:64px 88px 70px">
  <div style="display:flex;align-items:baseline;justify-content:space-between">
    <span class="kap" style="font-size:{18:.0f}px">Musiklib · Sammlung {A['sammlung']}</span>
    <span class="kap" style="font-size:{18:.0f}px">Rasterschrift</span>
  </div>
  <div>
    <div class="titel" style="font-size:{40:.0f}px">{A['titel']}</div>
    <div class="unter" style="font-size:{20:.0f}px;margin-top:{14:.0f}px">{A['interpret']}</div>
    {_feld(g, d, 1180)}
  </div>
  <div style="display:flex;align-items:center;gap:{int(26 * g)}px">{_geaetzt(g)}</div>
</div>'''
    return _css(g), body


def telefon():
    """Hochkant wird das Raster grober — dieselbe Zelle, weniger Zellen. Die
    geätzten Tasten werden zu Daumenflächen, sonst findet sie niemand."""
    g, d = 1.0, 17
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:104px 60px 110px">
  <div style="display:flex;align-items:baseline;justify-content:space-between">
    <span class="kap" style="font-size:{19:.0f}px">Sammlung {A['sammlung']}</span>
    <span class="kap" style="font-size:{19:.0f}px">Raster</span>
  </div>
  <div>
    <div class="titel" style="font-size:{40:.0f}px">{A['titel']}</div>
    <div class="unter" style="font-size:{21:.0f}px;margin-top:{16:.0f}px">{A['interpret']}</div>
    <div style="margin-top:{54:.0f}px;display:flex;flex-direction:column;gap:{44:.0f}px">
      <div>
        <div class="unter" style="font-size:{17:.0f}px;margin-bottom:{12:.0f}px">Titel 03 von 05</div>
        {_queue(g, d)}
      </div>
      <div>
        <div class="unter" style="font-size:{17:.0f}px;margin-bottom:{12:.0f}px">Restzeit</div>
        <div style="display:flex;align-items:flex-start">{_zeit(g, '03:23', d)}</div>
      </div>
      {_bahn(g, 940, d * 1.15, A['frac'])}
    </div>
  </div>
  <div style="display:flex;align-items:center;justify-content:space-between">
    {_geaetzt(g, gross=True)}
  </div>
</div>'''
    return _css(g), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('67', 'Rasterschrift', art, css, body)
