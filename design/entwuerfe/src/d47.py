# -*- coding: utf-8 -*-
"""47 Redaktionsblatt — nach der Neuheitenliste von Tonspion (00.34.48).

Die Vorlage ist eine Webseite und trotzdem eine Bildsprache: weisses Papier,
ein fetter geschnittener Schriftzug oben links, eine Zeile Großbuchstaben
daneben, dann datierte Blöcke aus reinen Textzeilen — alles Anklickbare
unterstrichen. Übertragen: das Album ist ein datierter Block, seine Titel sind
die Zeilen, und der laufende Titel bekommt als Einziges eine zweite, dicke
Unterstreichung — die ist der Fortschritt. Keine Farbe, kein Bild, keine Taste
mit Rundung: was gedrückt wird, ist ein unterstrichenes Wort.
"""
from werkzeug import A, biblio, schreibe, IMPACT, MONO, SANS

PAPIER = '#ffffff'
TINTE = '#111111'
STUMM = '#6a6a6a'
LINIE = '#d8d8d8'

# Der datierte Block aus der Vorlage: dort Neuerscheinungen, hier die Sammlung
# in der Reihenfolge, in der sie dazugekommen ist.
ZULETZT = [
    ('Bill Evans', 'Sunday at the Village Vanguard'),
    ('John Coltrane', 'A Love Supreme'),
    ('Wayne Shorter', 'Speak No Evil'),
    ('Herbie Hancock', 'Maiden Voyage'),
    ('Cannonball Adderley', 'Somethin’ Else'),
    ('Sonny Rollins', 'Saxophone Colossus'),
    ('Charles Mingus', 'Mingus Ah Um'),
    ('Eric Dolphy', 'Out to Lunch'),
    ('Lee Morgan', 'The Sidewinder'),
    ('Horace Silver', 'Song for My Father'),
    ('Art Blakey', 'Moanin’'),
    ('Grant Green', 'Idle Moments'),
]


def _css(g):
    return f'''
.stage{{background:{PAPIER};font-family:{SANS};color:{TINTE}}}

/* Der Schriftzug: fett, eng, leicht gestaucht — wie ein gesetzter Kopf */
.marke{{font-family:{IMPACT};letter-spacing:-.01em;line-height:.82;
  transform:scaleX(1.06);transform-origin:left}}

.nav{{display:flex;flex-wrap:wrap;text-transform:uppercase;font-weight:700;
  color:{TINTE}}}
.nav span{{white-space:nowrap}}
.nav .aus{{color:{STUMM};font-weight:600}}

/* Bibliothek: derselbe schwarze Block wie der Schriftzug, nur klein */
.bib{{display:inline-flex;align-items:center;background:{TINTE};color:{PAPIER};
  text-transform:uppercase;font-weight:700}}

.strich{{border:0;border-top:1px solid {LINIE}}}
.block{{font-weight:800;letter-spacing:-.02em}}
.datum{{font-style:italic;font-weight:700}}

/* Jede Zeile ist ein Link — der laufende Titel ist der einzige fette */
.zeile{{text-decoration:underline;text-underline-offset:.18em;
  text-decoration-thickness:1px;color:{TINTE}}}
.zeile.still{{color:{STUMM}}}

/* Die zweite, dicke Unterstreichung ist die Fortschrittsleiste */
.lauf{{position:relative;display:block;font-weight:800;letter-spacing:-.02em}}
.lauf .bahn{{position:absolute;left:0;right:0;background:{LINIE}}}
.lauf .bahn i{{position:absolute;left:0;top:0;bottom:0;background:{TINTE}}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};
  color:{STUMM};font-variant-numeric:tabular-nums}}

/* Transport: unterstrichene Wörter, nichts sonst */
.wort{{text-decoration:underline;text-underline-offset:.22em;
  text-decoration-thickness:2px;font-weight:700;white-space:nowrap}}
.wort.jetzt{{text-decoration-thickness:5px}}
'''


def _kopf(g, marke_px, nav_px):
    return f'''<div class="marke" style="font-size:{marke_px}px">musiklib</div>
  <div class="nav" style="font-size:{nav_px}px;gap:{int(30 * g)}px;
    margin-top:{int(26 * g)}px;letter-spacing:{1.4 * g:.1f}px">
    <span>Alben</span><span class="aus">Interpreten</span>
    <span class="aus">Zuletzt</span><span class="aus">Suche</span></div>'''


def _bib(g, schrift, hoehe):
    return (f'<span class="bib" style="height:{hoehe}px;padding:0 {int(20 * g)}px;'
            f'gap:{int(12 * g)}px;font-size:{schrift}px;letter-spacing:{2.6 * g:.1f}px">'
            f'{biblio(int(schrift * 1.25), PAPIER)}Sammlung · {A["sammlung"]}</span>')


def _block(g, kopf, unter, paare, schrift, luecke, kopf_px, unter_px):
    """Ein datierter Block wie in der Vorlage: Überschrift, Datumszeile, Zeilen."""
    zeilen = ''.join(f'<div style="margin-top:{luecke}px"><span class="zeile still">'
                     f'{a} – {b}</span></div>' for a, b in paare)
    return f'''<div class="block" style="font-size:{kopf_px}px">{kopf}</div>
  <div class="datum" style="font-size:{unter_px}px;color:{STUMM};
    margin-top:{int(12 * g)}px">{unter}</div>
  <div style="font-size:{schrift}px;line-height:1.5;margin-top:{int(24 * g)}px">
    {zeilen}</div>'''


def _laufend(g, schrift, bahn_h):
    return f'''<div class="lauf" style="font-size:{schrift}px;
    padding-bottom:{int(bahn_h * 2.4)}px">
    <span class="zeile" style="text-decoration-thickness:0">{A['titel']}</span>
    <span class="bahn" style="bottom:0;height:{bahn_h}px">
      <i style="width:{A['frac'] * 100:.0f}%"></i></span></div>'''


def _transport(g, schrift, luecke):
    return (f'<div style="display:flex;gap:{luecke}px;font-size:{schrift}px">'
            f'<span class="wort">Zurück</span>'
            f'<span class="wort jetzt">Pause</span>'
            f'<span class="wort">Weiter</span>'
            f'<span class="wort" style="color:{STUMM}">Zufall</span></div>')


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;padding:130px 74px 118px;
  display:flex;flex-direction:column">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:30px">
    <div style="min-width:0">{_kopf(g, 92, 25)}</div>
    {_bib(g, 20, 62)}
  </div>

  <hr class="strich" style="margin:44px 0 40px">

  {_block(g, A['album'], f"{A['interpret']} · {A['jahr']}",
          [(A['interpret'], t) for i, (nr, t, d) in enumerate(A['tracks'])
           if i != A['laeuft']], 33, 14, 46, 30)}

  <hr class="strich" style="margin:46px 0 40px">

  {_block(g, 'Zuletzt hinzugefügt', '14.08.26', ZULETZT, 33, 14, 46, 30)}

  <div style="margin-top:auto">
    <hr class="strich" style="margin-bottom:34px">
    {_laufend(g, 56, 9)}
    <div class="zeiten" style="font-size:25px;margin-top:18px">
      <span>{A['pos']}</span><span>{A['dauer']}</span></div>
    <div style="margin-top:46px">{_transport(g, 31, 44)}</div>
  </div>
</div>'''
    return css, body


def rechner():
    g = .72
    css = _css(g)
    zeilen = ''.join(
        f'<div style="display:flex;align-items:baseline;gap:20px;'
        f'padding:{"13px 0" if i != A["laeuft"] else "13px 0"};'
        f'border-top:1px solid {LINIE};font-size:26px'
        f'{";font-weight:800" if i == A["laeuft"] else f";color:{STUMM}"}">'
        f'<span style="font-family:{MONO};font-size:19px;color:{STUMM}">{nr}</span>'
        f'<span class="zeile{"" if i == A["laeuft"] else " still"}" '
        f'style="flex:1;overflow:hidden;white-space:nowrap;text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:19px;color:{STUMM}">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))

    body = f'''<div style="position:absolute;inset:0;padding:70px 88px;display:flex;
  gap:76px">
  <div style="width:420px;flex-shrink:0;display:flex;flex-direction:column">
    {_kopf(g, 64, 17)}
    <hr class="strich" style="margin:30px 0 26px">
    {_block(g, 'Zuletzt hinzugefügt', '14.08.26', ZULETZT, 22, 11, 32, 20)}
    <div style="margin-top:auto">{_bib(g, 15, 46)}</div>
  </div>

  <div style="flex:1;min-width:0;display:flex;flex-direction:column">
    <div style="font-family:{MONO};font-size:16px;letter-spacing:.18em;
      text-transform:uppercase;color:{STUMM};margin-bottom:16px">Läuft gerade</div>
    {_laufend(g, 62, 8)}
    <div class="zeiten" style="font-size:19px;margin-top:14px">
      <span>{A['pos']}</span><span>{A['dauer']}</span></div>

    <div style="margin-top:34px">{zeilen}
      <div style="border-top:1px solid {LINIE}"></div></div>

    <div style="margin-top:auto">{_transport(g, 23, 38)}</div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('47', 'Redaktionsblatt', art, css, body)
