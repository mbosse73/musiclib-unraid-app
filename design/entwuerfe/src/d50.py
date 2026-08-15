# -*- coding: utf-8 -*-
"""50 Fallblatt — nach dem orangen Klappzahlenwecker (08.39.21).

Die Vorlage: ein oranger Kunststoffkasten, vorn ein dunkles Fenster mit zwei
Fallblättern, daneben eine schmale Spalte mit kleinen Blättchen, rechts ein
schwarzer Drehknopf. Übertragen: die grossen Blätter zeigen nicht die Uhrzeit,
sondern die verstrichene Minute und Sekunde; die schmale Spalte zeigt die
Titelnummer, so wie sie im Foto den Wochentag zeigt. Der Knopf ist die
Lautstärke. Gefallene Blätter haben eine Naht in der Mitte — die bleibt, sie ist
das Kennzeichen der Bauform.
"""
from werkzeug import A, biblio, mischen, nexti, prev, pausei, schreibe, MONO, SANS

ORANGE = '#cf5f1e'
ORANGE_H = '#e8843f'
ORANGE_D = '#9d4413'
FENSTER = '#131313'
BLATT = '#2c2c2c'
WEISS = '#f4f2ee'
TINTE = '#3a1a06'


def _css(g):
    return f'''
.stage{{background:linear-gradient(155deg,#dfe0dc 0%,#b7b9b4 52%,#d6d8d3 100%);
  font-family:{SANS};color:{TINTE}}}

.kasten{{position:relative;border-radius:{30 * g:.0f}px;
  background:linear-gradient(168deg,{ORANGE_H} 0%,{ORANGE} 30%,{ORANGE_D} 100%);
  box-shadow:0 {30 * g:.0f}px {66 * g:.0f}px rgba(60,30,10,.42),
             inset 0 {3 * g:.0f}px 0 rgba(255,255,255,.42)}}

/* Das Fenster ist eingelassen, nicht aufgesetzt */
.fenster{{background:{FENSTER};border-radius:{12 * g:.0f}px;
  box-shadow:inset 0 {4 * g:.0f}px {14 * g:.0f}px rgba(0,0,0,.85),
             0 0 0 {3 * g:.0f}px rgba(0,0,0,.28)}}

/* Ein Fallblatt: Karte mit Naht in der Mitte und zwei Scharnieren */
.blatt{{position:relative;border-radius:{8 * g:.0f}px;overflow:hidden;
  background:linear-gradient(180deg,{BLATT} 0%,#252525 49.6%,#1c1c1c 50.4%,#2a2a2a 100%);
  display:flex;align-items:center;justify-content:center;color:{WEISS};
  font-weight:500;font-variant-numeric:tabular-nums;line-height:1}}
.blatt::after{{content:"";position:absolute;left:0;right:0;top:50%;height:{2 * g:.0f}px;
  transform:translateY(-50%);background:rgba(0,0,0,.75);
  box-shadow:0 {1 * g:.0f}px 0 rgba(255,255,255,.12)}}
.blatt b{{position:absolute;top:50%;transform:translateY(-50%);width:{7 * g:.0f}px;
  height:{18 * g:.0f}px;background:#8d8d8d;border-radius:{2 * g:.0f}px}}

.spalte{{display:flex;flex-direction:column;justify-content:center;
  color:rgba(244,242,238,.72);font-family:{MONO};font-variant-numeric:tabular-nums;
  text-align:center}}
.spalte .jetzt{{color:{WEISS}}}

/* Der Knopf: schwarz, mit dem eingeprägten Pfeil aus dem Foto */
.knopf{{position:relative;border-radius:50%;flex-shrink:0;
  background:radial-gradient(circle at 34% 28%,#5a5a5a 0%,#1d1d1d 46%,#0a0a0a 100%);
  box-shadow:0 {8 * g:.0f}px {16 * g:.0f}px rgba(40,20,5,.5)}}

.bahn{{position:relative;background:rgba(58,26,6,.26);border-radius:999px}}
.bahn i{{position:absolute;left:0;top:0;bottom:0;border-radius:999px;background:{TINTE}}}
.zeiten{{display:flex;justify-content:space-between;font-family:{MONO};
  color:rgba(58,26,6,.62);font-variant-numeric:tabular-nums}}

/* Die Tasten sind flach in den Kunststoff gesetzt */
.taste{{flex-shrink:0;display:flex;align-items:center;justify-content:center;
  border-radius:{6 * g:.0f}px;background:rgba(58,26,6,.20);
  box-shadow:inset 0 {2 * g:.0f}px {4 * g:.0f}px rgba(0,0,0,.22)}}
.bib{{display:inline-flex;align-items:center;border-radius:999px;background:{WEISS};
  color:{TINTE};text-transform:uppercase;font-weight:700}}
.marke{{text-transform:uppercase;font-weight:800;color:rgba(58,26,6,.42)}}
'''


def _blaetter(g, karte_b, karte_h, schrift, spalte_b, spalte_s):
    mm, ss = A['pos'].split(':')
    nr = A['tracks'][A['laeuft']][0]
    scharnier = (f'<b style="left:{-3.5 * g:.0f}px"></b>'
                 f'<b style="right:{-3.5 * g:.0f}px"></b>')
    return f'''<div style="display:flex;align-items:center;justify-content:center;
    gap:{int(18 * g)}px">
    <div class="blatt" style="width:{karte_b}px;height:{karte_h}px;font-size:{schrift}px">
      {mm}{scharnier}</div>
    <div class="spalte" style="width:{spalte_b}px;font-size:{spalte_s}px;
      gap:{int(10 * g)}px">
      <span>04</span><span class="jetzt">{nr}</span><span>02</span></div>
    <div class="blatt" style="width:{karte_b}px;height:{karte_h}px;font-size:{schrift}px">
      {ss}{scharnier}</div>
  </div>'''


def _knopf(g, size):
    r = size / 2
    return (f'<div class="knopf" style="width:{size}px;height:{size}px">'
            f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
            f'style="position:absolute;inset:0">'
            f'<path d="M{r * .55:.0f} {r * .70:.0f} A{r * .58:.0f} {r * .58:.0f} 0 1 1 '
            f'{r * .62:.0f} {r * 1.42:.0f}" fill="none" stroke="#8a8a8a" '
            f'stroke-width="{max(2, size * .035):.0f}" stroke-linecap="round"/>'
            f'<path d="M{r * .48:.0f} {r * 1.24:.0f} l{r * .16:.0f} {r * .20:.0f} '
            f'l{r * .22:.0f} {-r * .10:.0f}" fill="#8a8a8a"/></svg></div>')


def _bib(g, schrift, hoehe):
    return (f'<span class="bib" style="height:{hoehe}px;padding:0 {int(24 * g)}px;'
            f'gap:{int(12 * g)}px;font-size:{schrift}px;letter-spacing:{2.4 * g:.1f}px">'
            f'{biblio(int(schrift * 1.25), TINTE)}Sammlung · {A["sammlung"]}</span>')


def _tasten(g, size, luecke):
    return (f'<div style="display:flex;gap:{luecke}px">'
            f'<div class="taste" style="width:{size}px;height:{size}px">'
            f'{prev(int(size * .42), WEISS)}</div>'
            f'<div class="taste" style="width:{int(size * 1.5)}px;height:{size}px">'
            f'{pausei(int(size * .40), WEISS)}</div>'
            f'<div class="taste" style="width:{size}px;height:{size}px">'
            f'{nexti(int(size * .42), WEISS)}</div>'
            f'<div class="taste" style="width:{size}px;height:{size}px">'
            f'{mischen(int(size * .40), "rgba(244,242,238,.66)")}</div></div>')


def _zeilen(g, schrift, klein):
    return ''.join(
        f'<div style="display:flex;align-items:baseline;gap:{int(18 * g)}px;'
        f'padding:{int(12 * g)}px 0;border-top:1px solid rgba(58,26,6,.18);'
        f'font-size:{schrift}px'
        f'{";font-weight:700" if i == A["laeuft"] else ";color:rgba(58,26,6,.62)"}">'
        f'<span style="font-family:{MONO};font-size:{klein}px;'
        f'color:rgba(58,26,6,.48)">{nr}</span>'
        f'<span style="flex:1;overflow:hidden;white-space:nowrap;'
        f'text-overflow:ellipsis">{t}</span>'
        f'<span style="font-family:{MONO};font-size:{klein}px;'
        f'color:rgba(58,26,6,.48)">{d}</span></div>'
        for i, (nr, t, d) in enumerate(A['tracks']))


def telefon():
    g = 1.0
    css = _css(g)
    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:70px 54px">
  <div class="kasten" style="width:996px;padding:56px 52px 62px">
    <div style="display:flex;align-items:center;justify-content:space-between">
      {_bib(g, 21, 66)}
      <span class="marke" style="font-size:25px;letter-spacing:5px">Musiklib</span>
    </div>

    <div style="display:flex;align-items:center;gap:34px;margin-top:52px">
      <div class="fenster" style="flex:1;min-width:0;padding:44px 30px">
        {_blaetter(g, 272, 400, 230, 64, 27)}
      </div>
      {_knopf(g, 140)}
    </div>

    <div style="margin-top:62px;font-size:56px;font-weight:700;letter-spacing:-.02em">
      {A['titel']}</div>
    <div style="font-size:30px;color:rgba(58,26,6,.68);margin-top:12px">
      {A['interpret']} · {A['album']} · {A['jahr']}</div>

    <div class="bahn" style="height:10px;margin-top:40px">
      <i style="width:{A['frac'] * 100:.0f}%"></i></div>
    <div class="zeiten" style="font-size:25px;margin-top:16px">
      <span>{A['pos']}</span><span>{A['dauer']}</span></div>

    <div style="margin-top:46px">{_zeilen(g, 30, 24)}
      <div style="border-top:1px solid rgba(58,26,6,.18)"></div></div>

    <div style="margin-top:54px;display:flex;justify-content:center">
      {_tasten(g, 100, 28)}</div>
  </div>
</div>'''
    return css, body


def rechner():
    g = .76
    css = _css(g)
    zeilen = _zeilen(g, 21, 17)
    body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:52px 64px">
  <div class="kasten" style="width:1472px;padding:38px 42px;display:flex;gap:46px;
    align-items:center">
    <div class="fenster" style="flex-shrink:0;padding:30px 24px">
      {_blaetter(g, 186, 228, 142, 46, 19)}
    </div>

    <div style="flex:1;min-width:0">
      <div style="display:flex;align-items:center;justify-content:space-between">
        {_bib(g, 15, 46)}
        <span class="marke" style="font-size:17px;letter-spacing:4px">Musiklib</span>
      </div>
      <div style="margin-top:22px;font-size:42px;font-weight:700;letter-spacing:-.02em">
        {A['titel']}</div>
      <div style="font-size:22px;color:rgba(58,26,6,.68);margin-top:8px">
        {A['interpret']} · {A['album']} · {A['jahr']}</div>
      <div style="margin-top:18px">{zeilen}
        <div style="border-top:1px solid rgba(58,26,6,.18)"></div></div>
      <div class="bahn" style="height:8px;margin-top:24px">
        <i style="width:{A['frac'] * 100:.0f}%"></i></div>
      <div class="zeiten" style="font-size:18px;margin-top:12px">
        <span>{A['pos']}</span><span>{A['dauer']}</span></div>
      <div style="margin-top:24px">{_tasten(g, 68, 20)}</div>
    </div>

    {_knopf(g, 116)}
  </div>
</div>'''
    return css, body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('50', 'Fallblatt', art, css, body)
