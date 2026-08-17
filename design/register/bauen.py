# -*- coding: utf-8 -*-
"""Den Kontaktbogen bauen: je Konzept eine Karte, Aufnahmen inline als data-URI.

Die Daten stehen in daten_gruppen.py (GRUPPEN) und daten_offen.py (OFFEN);
die Bilder legt bogen_bilder3.py in kb/ ab.
"""
import base64
import html
import pathlib

from daten_gruppen import GRUPPEN
from daten_offen import OFFEN
from daten_bau import BAU

HIER = pathlib.Path(__file__).parent
KB = HIER / 'kb'
ZIEL = HIER / 'konzeptregister.html'

MARKE = {'gebaut': 'Im Programm', 'blatt': 'Blatt gezeichnet',
         'thema': 'Auf einem Zweig', 'paket': 'Zum Bau ausgewählt',
         'entwurf': 'Auswahl offen'}


def bild(name):
    p = KB / f'{name}.jpg'
    if not p.exists():
        raise SystemExit(f'fehlt: {p}')
    return 'data:image/jpeg;base64,' + base64.b64encode(p.read_bytes()).decode()


def e(t):
    return html.escape(t, quote=True)


karten, ledger, nr = [], [], 0
for status, titel, lede, hinweis, eintraege in GRUPPEN:
    stueck, erste = [], nr + 1
    for name, was, herkunft, formate, schritt, ansichten in eintraege:
        nr += 1
        kennung = f'K{nr:02d}'
        schuesse = ''
        for datei, lab in ansichten:
            hoch = 'hoch' in lab.lower() or 'telefon' in lab.lower() or 'iphone' in lab.lower()
            schuesse += (
                f'<figure class="{"hoch" if hoch else "quer"}">'
                f'<button type="button" class="lupe" '
                f'data-titel="{e(kennung + " · " + name + " · " + lab)}">'
                f'<img src="{bild(datei)}" alt="{e(name + " — " + lab)}" loading="lazy">'
                f'</button><figcaption>{lab}</figcaption></figure>')
        b = BAU.get(ansichten[0][0])
        if b:
            marke = {'gebaut': ('So ist es gebaut', 'gelesen'),
                     'blatt': ('So ist es gezeichnet', 'gelesen'),
                     'vorschlag': ('Vorschlag — bitte prüfen', 'offen')}[b['art']]
            bauteil = (f'<div class="bau {marke[1]}">'
                       f'<div class="bkopf">{marke[0]}</div>'
                       f'<p class="zeile"><span class="etikett">Spulen</span>{b["spulen"]}</p>'
                       f'<p class="zeile"><span class="etikett">Zustände</span>{b["zustaende"]}</p>'
                       f'<p class="zeile"><span class="etikett">Bewegung</span>{b["bewegung"]}</p>'
                       f'<p class="zeile"><span class="etikett">Bibliothek</span>{b["bib"]}</p>'
                       f'</div>')
        else:
            bauteil = ''
        stueck.append(f'''<article class="karte" data-status="{status}" id="{kennung.lower()}"
  data-suche="{e((name + " " + was + " " + herkunft + " " + formate).lower())}">
  <div class="meta">
    <div class="kopf"><span class="nr">{kennung}</span><h3>{name}</h3>
      <span class="marke">{MARKE[status]}</span></div>
    <p class="herkunft">{herkunft}</p>
    <p class="was">{was}</p>
    <p class="zeile"><span class="etikett">Formate</span>{formate}</p>
    <p class="zeile"><span class="etikett tun">Nächster Schritt</span>{schritt}</p>
    {bauteil}
  </div>
  <div class="schuesse">{schuesse}</div>
</article>''')
    ledger.append((status, titel, len(eintraege), f'K{erste:02d}–K{nr:02d}', hinweis))
    karten.append(f'''<section class="gruppe" id="{status}" data-status="{status}">
  <header class="ghead">
    <h2>{titel}</h2>
    <span class="zaehler">{len(eintraege)} Konzepte · K{erste:02d}–K{nr:02d}</span>
    <p class="glede">{lede}</p>
  </header>
  {''.join(stueck)}
</section>''')

ledger_html = ''.join(
    f'''<button class="lz" data-filter="{s}" type="button" aria-pressed="false">
      <span class="punkt" data-status="{s}"></span><span class="lname">{t}</span>
      <span class="lzahl">{n}</span><span class="lspanne">{sp}</span>
      <span class="lschritt">{hw}</span></button>''' for s, t, n, sp, hw in ledger)

offen_html = ''.join(f'<li><h3>{t}</h3><p>{txt}</p></li>' for t, txt in OFFEN)

SEITE = f'''<title>Musiklib Konzeptregister</title>
<style>
:root{{
  --paper:#FBF9F5; --stage:#EFEBE3; --karte:#FFFFFF;
  --ink:#241E18; --ink-2:#6B6155; --ink-3:#A0968A;
  --line:rgba(36,30,24,.11); --line-2:rgba(36,30,24,.24);
  --brass:#8A6534;
  --s-gebaut:#3E6B4C; --s-blatt:#42607A; --s-thema:#5B5A7E; --s-paket:#8A6534;
  --s-entwurf:#7A4F63;
  --serif:ui-serif,'Iowan Old Style','Palatino Linotype',Palatino,Georgia,'Times New Roman',serif;
  --sans:ui-sans-serif,-apple-system,'Helvetica Neue','Segoe UI',Roboto,Arial,sans-serif;
  --mono:ui-monospace,'SF Mono','IBM Plex Mono',Menlo,Consolas,monospace;
}}
@media (prefers-color-scheme:dark){{
  :root:not([data-theme="light"]){{
    --paper:#1B1712; --stage:#141110; --karte:#221D18;
    --ink:#EFE8DC; --ink-2:#B4A896; --ink-3:#867A6C;
    --line:rgba(239,232,220,.12); --line-2:rgba(239,232,220,.24);
    --brass:#CA9C5E;
    --s-gebaut:#7FB58E; --s-blatt:#8AAFCE; --s-thema:#A3A1D0; --s-paket:#CA9C5E;
    --s-entwurf:#C892A6;
  }}
}}
:root[data-theme="dark"]{{
  --paper:#1B1712; --stage:#141110; --karte:#221D18;
  --ink:#EFE8DC; --ink-2:#B4A896; --ink-3:#867A6C;
  --line:rgba(239,232,220,.12); --line-2:rgba(239,232,220,.24);
  --brass:#CA9C5E;
  --s-gebaut:#7FB58E; --s-blatt:#8AAFCE; --s-thema:#A3A1D0; --s-paket:#CA9C5E;
    --s-entwurf:#C892A6;
}}
*,*::before,*::after{{box-sizing:border-box}}
body{{margin:0;background:var(--stage);color:var(--ink);font-family:var(--sans);
  font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased}}
::selection{{background:rgba(138,101,52,.22)}}
:focus-visible{{outline:2px solid var(--brass);outline-offset:3px}}
img{{display:block;max-width:100%}}
code{{font-family:var(--mono);font-size:.88em;color:var(--ink-2)}}
.seite{{max-width:1280px;margin:0 auto;padding:0 clamp(16px,4vw,36px) 96px}}
.caps{{font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink-3)}}

/* ── Kopf ── */
.kopfz{{padding:clamp(44px,8vw,84px) 0 34px;border-bottom:1px solid var(--line-2)}}
.kopfz h1{{font-family:var(--serif);font-weight:400;font-size:clamp(34px,5.4vw,56px);
  line-height:1.03;letter-spacing:-.018em;margin:18px 0 0;text-wrap:balance}}
.kopfz h1 em{{font-style:italic;color:var(--brass)}}
.lede{{margin:18px 0 0;color:var(--ink-2);font-size:16.5px;max-width:64ch}}
.lede b{{color:var(--ink);font-weight:600}}

/* ── Übersicht: vier Zeilen, die zugleich der Filter sind ── */
.ledger{{margin-top:36px;border-top:1px solid var(--line);display:flex;flex-direction:column}}
.lz{{display:grid;grid-template-columns:14px minmax(150px,1fr) 42px 92px minmax(0,2.1fr);
  gap:16px;align-items:baseline;width:100%;text-align:left;font:inherit;color:inherit;
  background:none;border:0;border-bottom:1px solid var(--line);padding:15px 6px;cursor:pointer}}
.lz:hover{{background:var(--paper)}}
.lz[aria-pressed="true"]{{background:var(--paper);box-shadow:inset 2px 0 0 var(--brass)}}
.punkt{{width:9px;height:9px;border-radius:50%;background:var(--s-gebaut);
  align-self:center;justify-self:center}}
.punkt[data-status="blatt"]{{background:var(--s-blatt)}}
.punkt[data-status="thema"]{{background:var(--s-thema)}}
.punkt[data-status="paket"]{{background:var(--s-paket)}}
.punkt[data-status="entwurf"]{{background:var(--s-entwurf)}}
.lname{{font-family:var(--serif);font-size:19px}}
.lzahl{{font-family:var(--mono);font-size:15px;font-variant-numeric:tabular-nums;text-align:right}}
.lspanne{{font-family:var(--mono);font-size:12px;color:var(--ink-3)}}
.lschritt{{font-size:13.5px;color:var(--ink-2)}}
/* Die Bauanleitung sitzt unter dem naechsten Schritt und ist abgesetzt:
   was gelesen ist, steht ruhig da; was ein Vorschlag ist, traegt eine
   Kante in der Warnfarbe, damit man es nicht fuer gesetzt haelt. */
.bau{{margin-top:16px;padding:13px 15px 4px;border-radius:8px;background:var(--stage);
  border-left:3px solid var(--line)}}
.bau.offen{{border-left-color:var(--s-entwurf)}}
.bau .bkopf{{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-3);
  margin-bottom:9px}}
.bau.offen .bkopf{{color:var(--s-entwurf)}}
.bau .zeile{{margin-bottom:9px}}
@media (max-width:820px){{
  .lz{{grid-template-columns:14px 1fr 42px;row-gap:6px}}
  .lspanne,.lschritt{{grid-column:2/4}}
}}

/* ── Werkzeugleiste ── */
.werkzeug{{position:sticky;top:0;z-index:8;display:flex;flex-wrap:wrap;gap:10px 14px;
  align-items:center;padding:13px 0;margin-top:14px;background:var(--stage);
  border-bottom:1px solid var(--line)}}
.werkzeug input{{flex:1;min-width:170px;font:inherit;color:inherit;background:var(--paper);
  border:1px solid var(--line-2);border-radius:2px;padding:9px 12px}}
.werkzeug input::placeholder{{color:var(--ink-3)}}
.zuruecksetzen{{font:inherit;font-size:13px;color:var(--brass);background:none;border:0;
  border-bottom:1px solid var(--line-2);padding:0 0 2px;cursor:pointer}}
.treffer{{font-family:var(--mono);font-size:12.5px;color:var(--ink-3);
  font-variant-numeric:tabular-nums}}

/* ── Gruppen ── */
.gruppe{{padding-top:52px}}
.gruppe[hidden]{{display:none}}
.ghead{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px 20px;
  align-items:baseline;padding-bottom:20px;margin-bottom:22px;
  border-bottom:1px solid var(--line-2)}}
.ghead h2{{font-family:var(--serif);font-weight:400;font-size:clamp(24px,3.2vw,32px);
  letter-spacing:-.012em;margin:0}}
.zaehler{{font-family:var(--mono);font-size:12px;color:var(--ink-3);white-space:nowrap}}
.glede{{grid-column:1/-1;margin:0;color:var(--ink-2);font-size:14.5px;max-width:76ch}}

/* ── Karte: links was zu tun ist, rechts wie es aussieht ── */
.karte{{background:var(--karte);border:1px solid var(--line);
  border-left:3px solid var(--s-gebaut);
  display:grid;grid-template-columns:minmax(230px,320px) minmax(0,1fr);
  gap:14px 34px;align-items:start;padding:20px 24px 22px;margin-bottom:16px}}
.karte[data-status="blatt"]{{border-left-color:var(--s-blatt)}}
.karte[data-status="thema"]{{border-left-color:var(--s-thema)}}
.karte[data-status="paket"]{{border-left-color:var(--s-paket)}}
.karte[data-status="entwurf"]{{border-left-color:var(--s-entwurf)}}
.karte[hidden]{{display:none}}
.meta{{min-width:0}}
.kopf{{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap;margin-bottom:5px}}
.nr{{font-family:var(--mono);font-size:12px;font-variant-numeric:tabular-nums;
  color:var(--brass);border:1px solid var(--line-2);border-radius:2px;padding:2px 7px}}
.kopf h3{{font-family:var(--serif);font-weight:400;font-size:22px;letter-spacing:-.01em;margin:0}}
.marke{{font-size:8.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3);
  border:1px solid var(--line);padding:2px 6px;white-space:nowrap}}
.herkunft{{margin:0 0 8px;font-family:var(--mono);font-size:12px;color:var(--ink-3)}}
.was{{margin:0 0 14px;font-size:14px;color:var(--ink-2);max-width:46ch}}
.zeile{{margin:0 0 9px;font-size:13.5px;color:var(--ink-2);display:flex;
  align-items:baseline;gap:9px;flex-wrap:wrap}}
.zeile:last-child{{margin-bottom:0}}
.etikett{{font-family:var(--mono);font-size:9px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--ink-3);border-left:2px solid var(--line-2);padding-left:8px;white-space:nowrap}}
.etikett.tun{{color:var(--brass);border-left-color:var(--brass)}}
.zeile b{{color:var(--ink);font-weight:600}}

/* ── Aufnahmen: ein Klick zeigt sie gross ── */
.schuesse{{display:flex;gap:20px;align-items:flex-end;flex-wrap:wrap}}
.schuesse figure{{margin:0;min-width:0}}
.lupe{{display:block;padding:0;border:1px solid var(--line-2);background:var(--stage);
  cursor:zoom-in;line-height:0;overflow:hidden}}
.lupe:hover{{border-color:var(--brass)}}
.quer .lupe img{{height:clamp(150px,23vh,244px);width:auto;max-width:100%}}
.hoch .lupe img{{height:clamp(230px,34vh,344px);width:auto}}
.schuesse figcaption{{margin-top:7px;font-family:var(--mono);font-size:9.5px;
  letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3)}}
@media (max-width:860px){{
  .karte{{grid-template-columns:1fr;padding:17px 16px 18px}}
  .quer .lupe img{{height:170px}} .hoch .lupe img{{height:250px}}
}}

/* ── Lupe ── */
dialog{{border:none;padding:0;background:var(--stage);color:var(--ink);
  width:100%;height:100%;max-width:100vw;max-height:100vh}}
dialog::backdrop{{background:rgba(0,0,0,.86)}}
.dinnen{{height:100%;display:flex;flex-direction:column}}
.dkopf{{display:flex;align-items:center;gap:14px;padding:11px 18px;
  border-bottom:1px solid var(--line-2);flex:none}}
.dtitel{{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--ink-2)}}
.dzu{{margin-left:auto;font-family:var(--mono);font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;background:none;border:1px solid var(--line-2);border-radius:2px;
  color:var(--ink);padding:6px 12px;cursor:pointer}}
.dzu:hover{{border-color:var(--brass);color:var(--brass)}}
.dfeld{{flex:1;overflow:auto;display:flex;align-items:flex-start;justify-content:center;
  padding:18px}}
.dfeld img{{max-width:100%;height:auto;border:1px solid var(--line-2)}}

/* ── Was sonst offen ist ── */
.offen{{margin-top:74px;padding-top:36px;border-top:1px solid var(--line-2)}}
.offen h2{{font-family:var(--serif);font-weight:400;font-size:clamp(24px,3.2vw,32px);
  letter-spacing:-.012em;margin:0 0 8px}}
.offen>p{{color:var(--ink-2);max-width:70ch;margin:0 0 10px}}
.offen ol{{list-style:none;counter-reset:o;margin:24px 0 0;padding:0;
  display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:0 34px}}
.offen li{{counter-increment:o;border-top:1px solid var(--line);padding:18px 0}}
.offen li h3{{font-family:var(--sans);font-size:15px;font-weight:600;margin:0 0 5px}}
.offen li h3::before{{content:counter(o,decimal-leading-zero);font-family:var(--mono);
  font-size:11.5px;color:var(--brass);margin-right:10px;font-weight:400}}
.offen li p{{margin:0;font-size:14px;color:var(--ink-2)}}
.fuss{{margin-top:52px;padding-top:20px;border-top:1px solid var(--line);
  font-size:12.5px;color:var(--ink-3)}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;animation:none!important}}}}
</style>

<div class="seite">
  <header class="kopfz">
    <div class="caps">Musiklib · Stand 17. August 2026 · die Auswahl ist eine Anprobe</div>
    <h1>Sechsundsiebzig Spieler, <em>vier</em> Zustände</h1>
    <p class="lede">Alle Konzepte aus vier Quellen — dem gebauten Programm, den Mockup-Blättern,
    dem gelieferten Design-Paket und den eigenen Entwürfen — in <b>einer</b>
    Nummernfolge. Die Nummer <code>K01</code>–<code>K76</code> ist
    durchgehend und wird nach jeder Streichung und jedem Fund neu gezogen — die alte Herkunft steht
    auf jeder Karte, damit trotzdem nichts verlorengeht.</p>
    <p class="lede">Jede Karte zeigt <b>beide Formate</b>, quer und hoch, so weit es sie gibt.
    <b>Ein Klick auf eine Aufnahme zeigt sie in voller Größe</b> — Esc schließt wieder.
    Eine Zeile der Übersicht anklicken zeigt nur diese Gruppe.</p>
    <p class="lede"><b>Die acht Themen sind gebaut.</b> Sie lagen zuletzt nur noch als
    eingefrorene Kopie unter <code>mockups/acht-themen/</code>; jetzt stehen sie als
    <b>K19–K26</b> im Programm — vier Familien mit einem gemeinsamen Markup, jede zusätzlich
    im Querformat, das die Vorlagen gar nicht hatten. Damit ist der fünfte Zustand „auf einem
    Zweig" wieder verschwunden: es gibt ihn nicht mehr.</p>
    <p class="lede"><b>Jede Karte trägt jetzt eine Bauanleitung</b> — Spulfläche, Zustände,
    Bewegung, Bibliothek. Bei den gebauten ist sie aus dem Code gelesen, bei den gezeichneten
    Blättern aus dem Blatt; bei den <b>29 Standbildern (K48–K76) ist sie ein Vorschlag</b> und
    trägt deshalb eine farbige Kante. Diese Blätter haben kein Skript, keine Übergänge, keine
    Zustände — dort ist nichts abzulesen, dort ist zu entscheiden. Hausregel für Bewegung:
    sparsam, bewegt wird nur, was den Stand zeigt. Dieselben Angaben liegen als
    <code>design/BAUANLEITUNG.md</code> im Repo.</p>
    <p class="lede"><b>Ausgewählt wird jetzt durch Aufsetzen.</b> Der Einstellungsdialog bot die
    Auslagen als Textkacheln an — Name, Gerät, ein Satz —, man wählte blind und der Dialog schloss
    sich sofort. Seit dieser Fassung führt ein Tor in die <b>Anprobe</b>: die Ansicht steht sofort
    über den ganzen Schirm, mit dem laufenden Titel darin, unten blättert ein nach <b>Familien</b>
    gegliederter Streifen weiter, am Ende steht Behalten oder Abbrechen. Für dieses Register heisst
    das zweierlei — eine Portierung lässt sich künftig <i>ansehen</i> statt beschreiben, und jede
    neue Auslage braucht neben CSS und <code>layout({{…}})</code> eine Zeile in
    <code>SIGNETE</code>, sonst bleibt ihre Kachel im Streifen leer. Gebaut nach
    <code>mockups/player/27-anprobe.html</code>; der Gegenentwurf 26 „Schaukasten" steht daneben
    und ist nicht genommen.</p>
    <p class="lede">Alles hier steht auf <code>main</code>, und seit dieser Woche prüft das ein
    Workflow bei jedem Push: die Testsuite ist von 148 auf <b>167</b> gewachsen und darf in der CI
    keinen einzigen Test überspringen — ohne Browser überspränge sich die halbe Suite still und
    meldete trotzdem grün.</p>
    <div class="ledger">{ledger_html}</div>
  </header>

  <div class="werkzeug">
    <input type="search" id="suche" placeholder="Suchen — Name, Herkunft, Format"
      aria-label="Konzepte durchsuchen">
    <span class="treffer" id="treffer">76 von 76</span>
    <button class="zuruecksetzen" id="reset" type="button">Alles zeigen</button>
  </div>

  {''.join(karten)}

  <section class="offen">
    <h2>Was darüber hinaus offen ist</h2>
    <p>Nicht am einzelnen Konzept, sondern am Ganzen.</p>
    <ol>{offen_html}</ol>
  </section>

  <p class="fuss">Aufnahmen: die Layouts aus dem laufenden Programm gegen eine Test-Bibliothek —
  deshalb steht dort „Thunder Road" und nicht dein eigener Bestand. Blätter und Entwürfe kommen
  aus ihren HTML-Dateien, in genau den Bühnenmaßen, für die sie gezeichnet sind.</p>
</div>

<dialog id="lupe">
  <div class="dinnen">
    <div class="dkopf">
      <span class="dtitel" id="dtitel"></span>
      <button class="dzu" id="dzu" type="button">Schließen · Esc</button>
    </div>
    <div class="dfeld"><img id="dbild" alt=""></div>
  </div>
</dialog>

<script>
(() => {{
  const karten = [...document.querySelectorAll('.karte')];
  const gruppen = [...document.querySelectorAll('.gruppe')];
  const zeilen = [...document.querySelectorAll('.lz')];
  const feld = document.getElementById('suche');
  const treffer = document.getElementById('treffer');
  let filter = null;

  const zeichne = () => {{
    const q = feld.value.trim().toLowerCase();
    let n = 0;
    karten.forEach(k => {{
      const passt = (!filter || k.dataset.status === filter)
        && (!q || k.dataset.suche.includes(q));
      k.hidden = !passt;
      if (passt) n++;
    }});
    gruppen.forEach(g => {{
      g.hidden = ![...g.querySelectorAll('.karte')].some(k => !k.hidden);
    }});
    zeilen.forEach(z => z.setAttribute('aria-pressed', String(z.dataset.filter === filter)));
    treffer.textContent = n + ' von ' + karten.length;
  }};

  zeilen.forEach(z => z.addEventListener('click', () => {{
    filter = filter === z.dataset.filter ? null : z.dataset.filter;
    zeichne();
    if (filter) document.getElementById(filter).scrollIntoView({{behavior:'smooth', block:'start'}});
  }}));
  feld.addEventListener('input', zeichne);
  document.getElementById('reset').addEventListener('click', () => {{
    filter = null; feld.value = ''; zeichne();
    window.scrollTo({{top:0, behavior:'smooth'}});
  }});
  zeichne();

  // ── Lupe: dieselbe Aufnahme, nur so gross, wie der Schirm hergibt ──
  const dlg = document.getElementById('lupe');
  const dbild = document.getElementById('dbild');
  const dtitel = document.getElementById('dtitel');
  document.querySelectorAll('.lupe').forEach(b => b.addEventListener('click', () => {{
    const img = b.querySelector('img');
    dbild.src = img.src;
    dbild.alt = img.alt;
    dtitel.textContent = b.dataset.titel;
    dlg.showModal();
  }}));
  document.getElementById('dzu').addEventListener('click', () => dlg.close());
  dlg.addEventListener('click', ev => {{ if (ev.target === dlg) dlg.close(); }});
}})();
</script>
'''

ZIEL.write_text(SEITE, encoding='utf-8')
print(ZIEL, f'{ZIEL.stat().st_size / 1024 / 1024:.2f} MB', nr, 'Konzepte')
