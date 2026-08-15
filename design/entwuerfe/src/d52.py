# -*- coding: utf-8 -*-
"""52 Meldetafel — nach der Störmeldetafel eines Maschinenhauses (08.43.56).

Die Vorlage ist ein Feld aus beschrifteten Leuchtkacheln in einem dunklen
Rahmen: die meisten grau und tot, wenige gelb, rot oder grün — man liest den
Zustand einer ganzen Anlage auf einen Blick. Übertragen: die Kacheln sind die
Sammlung. Grau heisst „liegt da", grün „zuletzt dazugekommen", bernstein „läuft
gerade" — es gibt genau eine bernsteinfarbene. Der Fortschritt ist eine Reihe
kleiner Lampen unter dem Feld, die von links her anspringt; Transport und
Sammlung sind selbst Kacheln, nur breiter.
"""
from werkzeug import A, biblio, nexti, prev, pausei, schreibe, COND, MONO, SANS

RAHMEN = '#26282a'
RAHMEN_H = '#3a3d40'
GRAU = '#8f9599'
GRUEN = '#4fbe63'
BERNSTEIN = '#e8a52c'
ROT = '#d3402f'
STAHL = '#41454a'
TINTE = '#101112'
WEISS = '#eceef0'

# Die Sammlung, so kurz, wie eine Kachel es zulässt.
KACHELN = [
    'Kind of Blue', 'A Love Supreme', 'Speak No Evil', 'Maiden Voyage',
    'Somethin’ Else', 'Saxophone Colossus', 'Mingus Ah Um', 'Out to Lunch',
    'Blue Train', 'Moanin’', 'Cool Struttin’', 'Go!',
    'Sunday at the Vanguard', 'Waltz for Debby', 'Undercurrent', 'Empyrean Isles',
    'The Sidewinder', 'Song for My Father', 'Page One', 'Idle Moments',
    'Point of Departure', 'Unit Structures', 'Free for All', 'Search for the New Land',
    'Sketches of Spain', 'Milestones', 'Round About Midnight', 'Workin’',
    'Giant Steps', 'Crescent', 'Ascension', 'Meditations',
    'The Black Saint', 'Mingus Mingus', 'Let My Children Hear', 'Pithecanthropus',
    'Somethin’ Cool', 'Lady in Satin', 'Ella in Berlin', 'At Carnegie Hall',
]
GRUENE = {1, 4, 9, 17, 22}   # zuletzt dazugekommen
LAEUFT = 0


def _css(g):
    return f'''
.stage{{background:linear-gradient(160deg,#1a1c1e 0%,#0e0f10 100%);
  font-family:{SANS};color:{WEISS}}}

/* Der Rahmen ist Blech, nicht Rand: er hat eine helle Oberkante */
.tafel{{position:relative;background:{RAHMEN};
  box-shadow:inset 0 {3 * g:.0f}px 0 {RAHMEN_H},
             inset 0 0 0 {2 * g:.0f}px rgba(0,0,0,.45)}}

.gitter{{display:grid}}
.kachel{{position:relative;display:flex;align-items:center;justify-content:center;
  text-align:center;border-radius:{3 * g:.0f}px;font-family:{COND};font-weight:700;
  text-transform:uppercase;line-height:1.06;color:{TINTE};
  box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(0,0,0,.5),
             inset 0 {2 * g:.0f}px {3 * g:.0f}px rgba(255,255,255,.28)}}
.kachel.tot{{background:{GRAU};color:rgba(16,17,18,.72)}}
.kachel.gruen{{background:{GRUEN}}}
.kachel.bernstein{{background:{BERNSTEIN};
  box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(0,0,0,.5),
             inset 0 {2 * g:.0f}px {3 * g:.0f}px rgba(255,255,255,.34),
             0 0 {26 * g:.0f}px rgba(232,165,44,.55)}}
.kachel.stahl{{background:{STAHL};color:{WEISS}}}
.kachel.rot{{background:{ROT};color:{WEISS}}}

/* Die Lampenreihe ist der Fortschritt — dieselbe Bauform, nur klein */
.lampen{{display:flex}}
.lampe{{flex:1;border-radius:{2 * g:.0f}px;background:#2f3235;
  box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(0,0,0,.5)}}
.lampe.an{{background:{BERNSTEIN};box-shadow:inset 0 0 0 {1 * g:.0f}px rgba(0,0,0,.5),
  0 0 {10 * g:.0f}px rgba(232,165,44,.5)}}

.schild{{font-family:{MONO};text-transform:uppercase;letter-spacing:.18em;
  color:rgba(236,238,240,.5)}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};
  color:rgba(236,238,240,.5);font-variant-numeric:tabular-nums}}
'''


def _gitter(g, spalten, anzahl, hoehe, schrift, stil=''):
    stk = []
    for i in range(anzahl):
        name = KACHELN[i % len(KACHELN)]
        art = ('bernstein' if i == LAEUFT else 'gruen' if i in GRUENE else 'tot')
        hoch = f'height:{hoehe}px;' if hoehe else ''
        stk.append(f'<div class="kachel {art}" style="{hoch}'
                   f'font-size:{schrift}px;padding:0 {int(6 * g)}px">{name}</div>')
    auto = '' if hoehe else 'grid-auto-rows:1fr;'
    return (f'<div class="gitter" style="grid-template-columns:repeat({spalten},1fr);'
            f'{auto}gap:{max(3, int(5 * g))}px;{stil}">{"".join(stk)}</div>')


def _leiste(g, hoehe, schrift, zeichen):
    """Transport und Sammlung sind Kacheln — nur breiter und aus Stahl."""
    return f'''<div class="gitter" style="grid-template-columns:1fr 1fr 1fr 2fr;
  gap:{max(3, int(5 * g))}px">
  <div class="kachel stahl" style="height:{hoehe}px">{prev(zeichen, WEISS)}</div>
  <div class="kachel rot" style="height:{hoehe}px">{pausei(zeichen, WEISS)}</div>
  <div class="kachel stahl" style="height:{hoehe}px">{nexti(zeichen, WEISS)}</div>
  <div class="kachel gruen" style="height:{hoehe}px;gap:{int(12 * g)}px;
    font-size:{schrift}px;letter-spacing:{1.6 * g:.1f}px">
    {biblio(zeichen, TINTE)}Sammlung · {A['sammlung']}</div>
</div>'''


def _lampen(g, hoehe, n=32):
    stk = ''.join(f'<span class="lampe{" an" if i / n < A["frac"] else ""}" '
                  f'style="height:{hoehe}px"></span>' for i in range(n))
    return f'<div class="lampen" style="gap:{max(2, int(4 * g))}px">{stk}</div>'


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column">
  <div style="display:flex;align-items:baseline;justify-content:space-between;
    padding:52px 44px 26px;flex-shrink:0">
    <span class="schild" style="font-size:23px">Musiklib · Bestand</span>
    <span class="schild" style="font-size:23px">{A['sammlung']} Alben</span>
  </div>

  <div class="tafel" style="flex:1;min-height:0;padding:26px;display:flex;
    flex-direction:column">
    {_gitter(g, 4, 36, None, 22, 'flex:1;min-height:0')}
    <div style="margin-top:26px;flex-shrink:0">{_lampen(g, 22)}</div>
    <div class="zeiten" style="font-size:24px;margin-top:16px;flex-shrink:0">
      <span>{A['pos']}</span><span>{A['dauer']}</span></div>
    <div style="margin-top:26px;flex-shrink:0">{_leiste(g, 126, 22, 44)}</div>
  </div>

  <div style="padding:34px 44px 52px;flex-shrink:0">
    <div style="font-size:50px;font-weight:700;letter-spacing:-.02em">{A['titel']}</div>
    <div style="font-size:28px;color:rgba(236,238,240,.6);margin-top:10px">
      {A['interpret']} · {A['album']} · {A['jahr']}</div>
  </div>
</div>'''
    return css, body


def rechner():
    g = .74
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;display:flex">
  <div class="tafel" style="flex:1;min-width:0;padding:22px;display:flex;
    flex-direction:column">
    {_gitter(g, 7, 42, None, 16, 'flex:1;min-height:0')}
    <div style="margin-top:20px;flex-shrink:0">{_lampen(g, 16, 40)}</div>
  </div>

  <div style="width:440px;flex-shrink:0;padding:56px 48px;display:flex;
    flex-direction:column">
    <span class="schild" style="font-size:16px">Läuft gerade</span>
    <div style="font-size:42px;font-weight:700;letter-spacing:-.02em;margin-top:14px">
      {A['titel']}</div>
    <div style="font-size:23px;color:rgba(236,238,240,.6);margin-top:10px">
      {A['interpret']}<br>{A['album']} · {A['jahr']}</div>
    <div class="zeiten" style="font-size:19px;margin-top:auto">
      <span>{A['pos']}</span><span>{A['dauer']}</span></div>
    <div style="margin-top:14px">{_lampen(g, 14, 24)}</div>
    <div style="margin-top:30px">{_leiste(g, 100, 15, 32)}</div>
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('52', 'Meldetafel', art, css, body)
