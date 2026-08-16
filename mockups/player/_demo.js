'use strict';
/* ══════════════════════════════════════════════════════════════════════════
   _demo.js — gemeinsamer Unterbau der Spieler-Entwürfe.

   Die Entwürfe sind Attrappen: keine API, keine Audiodatei, kein
   localStorage. Was sie brauchen, ist immer dasselbe — eine Sammlung, eine
   Warteschlange, eine Uhr, die läuft, und ein paar Zeichen. Genau das steht
   hier, damit in den Entwurfsdateien nur noch der Entwurf steht.

   Diese Datei landet nie im Container: gebaut wird am Ende eine einzelne
   ipad.html bzw. pc.html, so wie mobile.html eine einzelne Datei ist.
   ══════════════════════════════════════════════════════════════════════════ */

/* ═════════ Daten (dieselbe Sammlung wie in mockups/handy.html) ═════════ */
const ALBUMS = [
  {id:'sat', t:'Gymnopédies & Gnossiennes', ar:'Erik Satie',     y:1988, c:['#C9A96E','#8A6E3C'],
   tr:[['Gymnopédie No. 1',224],['Gymnopédie No. 2',241],['Gymnopédie No. 3',232],
       ['Gnossienne No. 1',322],['Gnossienne No. 3',288]]},
  {id:'bac', t:'Wohltemperiertes Klavier I', ar:'J. S. Bach',    y:1963, c:['#9FB0B8','#5E7480'],
   tr:[['Präludium C-Dur',134],['Fuge C-Dur',123],['Präludium c-Moll',96],['Fuge c-Moll',112],
       ['Präludium Cis-Dur',108]]},
  {id:'koe', t:'The Köln Concert',           ar:'Keith Jarrett', y:1975, c:['#C29A8C','#8A5A4C'],
   tr:[['Part I',406],['Part II a',354],['Part II b',433],['Part II c',428]]},
  {id:'kob', t:'Kind of Blue',               ar:'Miles Davis',   y:1959, c:['#8FA6BE','#4F6A88'],
   tr:[['So What',562],['Freddie Freeloader',586],['Blue in Green',337],['All Blues',693],
       ['Flamenco Sketches',566]]},
  {id:'par', t:'Spiegel im Spiegel',         ar:'Arvo Pärt',     y:1999, c:['#AEBCAE','#6E8474'],
   tr:[['Spiegel im Spiegel',624],['Für Alina',132],['Fratres',668]]},
  {id:'blu', t:'Blue',                       ar:'Joni Mitchell', y:1971, c:['#A8B4CE','#63719A'],
   tr:[['All I Want',214],['Blue',185],['A Case of You',262],['River',244],['California',231]]},
  {id:'ohi', t:'Ohia',                        ar:'Songs: Ohia',  y:2002, c:['#B8A48F','#7A6450'],
   tr:[['Farewell Transmission',432],['Just Be Simple',291],['Almost Was Good Enough',258]]},
  {id:'ryu', t:'Async',                       ar:'Ryuichi Sakamoto', y:2017, c:['#9EA7A0','#5B6660'],
   tr:[['andata',345],['disintegration',271],['solari',262],['ZURE',201]]},
];

const TRACKS = {}, TLIST = [];
ALBUMS.forEach(a => a.tr.forEach(([t,d],i) => {
  const o = {id:`${a.id}-${i}`, t, d, al:a.id, no:i+1};
  TRACKS[o.id] = o; TLIST.push(o);
}));

/* Suchblob je Album — Titel, Interpret und alle Titelnamen, einmal gebaut.
   Genau wie a._q in index.html: danach ist Suchen ein includes() je Album. */
ALBUMS.forEach(a => a._q =
  (a.t + ' ' + a.ar + ' ' + a.y + ' ' + a.tr.map(t => t[0]).join(' ')).toLowerCase());
const suche = text => {
  const q = String(text || '').trim().toLowerCase();
  return q ? ALBUMS.filter(a => a._q.includes(q)) : ALBUMS.slice();
};

const albOf  = t => ALBUMS.find(a => a.id === t.al);
const grad   = a => `linear-gradient(150deg,${a.c[0]},${a.c[1]})`;
const ini    = a => a.t.trim().charAt(0).toUpperCase();
const albDur = a => a.tr.reduce((n,t) => n + t[1], 0);
const esc    = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const clamp  = (v,a,b) => Math.min(b, Math.max(a,v));
const fmt    = s => { s = Math.max(0, Math.round(s)); return Math.floor(s/60)+':'+String(s%60).padStart(2,'0'); };
const fmt2   = s => { s = Math.max(0, Math.round(s));
  return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0'); };
const fmtLang= s => { s = Math.round(s); const h = Math.floor(s/3600), m = Math.round(s%3600/60);
  return h ? `${h} Std ${m} Min` : `${m} Min`; };

/* Ausschlag: pro Titel immer derselbe, damit die Wellenform beim Wechsel
   nicht flackert — echte Werte gäbe es erst mit einer Analyse beim Scan. */
function wave(seed, n){
  let x = 0; for (const ch of String(seed)) x = (x*31 + ch.charCodeAt(0)) >>> 0;
  const out = [];
  for (let i = 0; i < n; i++){
    x = (x*1103515245 + 12345) >>> 0;
    const r = ((x >>> 16) & 0x7fff) / 0x7fff;
    const bogen = Math.sin(Math.PI * (i+.5) / n);          // leiser Anfang, leises Ende
    out.push(.18 + .82 * (0.35 + 0.65*r) * (0.45 + 0.55*bogen));
  }
  return out;
}

/* ═════════ Zeichen ═════════ */
const sv = (w, inner, sw=1.6) => `<svg width="${w}" height="${w}" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${inner}</svg>`;
const I = {
  play:  w => `<svg width="${w}" height="${w}" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>`,
  pause: w => `<svg width="${w}" height="${w}" viewBox="0 0 24 24" fill="currentColor"><path d="M6.5 4h3.6v16H6.5zM13.9 4h3.6v16h-3.6z"/></svg>`,
  prev:  w => `<svg width="${w}" height="${w}" viewBox="0 0 24 24" fill="currentColor"><path d="M19 20L9 12l10-8v16zM5 4h2.2v16H5z"/></svg>`,
  next:  w => `<svg width="${w}" height="${w}" viewBox="0 0 24 24" fill="currentColor"><path d="M5 4l10 8-10 8V4zm13.8 0H21v16h-2.2z"/></svg>`,
  stop:  w => `<svg width="${w}" height="${w}" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="1.5"/></svg>`,
  shuffle: w => sv(w,'<polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="4" y1="4" x2="9" y2="9"/>'),
  repeat:  w => sv(w,'<polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>'),
  search:  w => sv(w,'<circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.7" y2="16.7"/>'),
  x:       w => sv(w,'<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>'),
  list:    w => sv(w,'<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="4" cy="6" r=".9" fill="currentColor"/><circle cx="4" cy="12" r=".9" fill="currentColor"/><circle cx="4" cy="18" r=".9" fill="currentColor"/>'),
  grid:    w => sv(w,'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>'),
  disc:    w => sv(w,'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.3"/>'),
  note:    w => sv(w,'<circle cx="7" cy="18" r="3"/><circle cx="18" cy="15.5" r="2.6"/><path d="M10 18V6l10.6-2.4v12"/>'),
  heart:   w => sv(w,'<path d="M12 20.4S3.6 15 3.6 9.2A4.6 4.6 0 0 1 12 6.6a4.6 4.6 0 0 1 8.4 2.6c0 5.8-8.4 11.2-8.4 11.2z"/>'),
  vol:     w => sv(w,'<path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M17 8.5a5 5 0 0 1 0 7"/>'),
  back:    w => sv(w,'<polyline points="15 18 9 12 15 6"/>'),
  fwd:     w => sv(w,'<polyline points="9 18 15 12 9 6"/>'),
  down:    w => sv(w,'<polyline points="6 9 12 15 18 9"/>'),
  dots:    w => `<svg width="${w}" height="${w}" viewBox="0 0 24 24" fill="currentColor"><circle cx="5" cy="12" r="1.7"/><circle cx="12" cy="12" r="1.7"/><circle cx="19" cy="12" r="1.7"/></svg>`,
  slider:  w => sv(w,'<line x1="4" y1="8" x2="20" y2="8"/><line x1="4" y1="16" x2="20" y2="16"/><circle cx="15" cy="8" r="2.4" fill="currentColor" stroke="none"/><circle cx="9" cy="16" r="2.4" fill="currentColor" stroke="none"/>'),
};

/* ═════════ Laufwerk ═════════
   Eine Warteschlange, eine Uhr. Kein <audio>: die Uhr ist ein Intervall, das
   die Position hochzählt — in der echten Seite käme sie aus timeupdate.
   Alle Entwürfe hängen über deck.onRender an derselben Mechanik.          */
class Deck {
  constructor(albumId = 'kob', opts = {}){
    const a = ALBUMS.find(x => x.id === albumId) || ALBUMS[0];
    this.queue   = a.tr.map((_,i) => `${a.id}-${i}`);
    this.qi      = opts.qi != null ? opts.qi : 1;
    this.pos     = opts.pos != null ? opts.pos : 74;
    this.playing = opts.playing !== false;
    this.vol     = opts.vol != null ? opts.vol : .72;
    this.shuffle = false;
    this.repeat  = false;
    this.speed   = opts.speed || 1;      // schnellere Uhr für die Vorführung
    this.onRender = () => {};
    this._t = setInterval(() => this.tick(.25), 250);
  }
  get track(){ return TRACKS[this.queue[this.qi]]; }
  get album(){ return albOf(this.track); }
  get dur(){ return this.track.d; }
  get frac(){ return clamp(this.pos / this.dur, 0, 1); }
  get rest(){ return Math.max(0, this.dur - this.pos); }
  get offs(){ let o = [], s = 0; for (const id of this.queue){ o.push(s); s += TRACKS[id].d; } return o; }
  get total(){ return this.queue.reduce((s,id) => s + TRACKS[id].d, 0); }
  get gpos(){ return this.offs[this.qi] + this.pos; }

  tick(dt){
    if (this.playing){
      this.pos += dt * this.speed;
      if (this.pos >= this.dur){ this.pos = 0; this.step(1); }
    }
    this.render();
  }
  render(){ this.onRender(this); }

  toggle(){ this.playing = !this.playing; this.render(); }
  play(){ this.playing = true; this.render(); }
  step(n){ this.qi = (this.qi + n + this.queue.length) % this.queue.length; this.render(); }
  next(){ this.pos = 0; this.step(1); }
  prev(){ if (this.pos > 4){ this.pos = 0; this.render(); return; } this.pos = 0; this.step(-1); }
  jump(i){ this.qi = clamp(i, 0, this.queue.length-1); this.pos = 0; this.playing = true; this.render(); }
  seek(f){ this.pos = clamp(f, 0, 1) * this.dur; this.render(); }
  seekGlobal(v){                                   // über Titelgrenzen hinweg
    v = clamp(v, 0, this.total - .5);
    const o = this.offs;
    let i = 0; for (let k = o.length-1; k >= 0; k--) if (v >= o[k]){ i = k; break; }
    this.qi = i; this.pos = v - o[i]; this.render();
  }
  setVol(v){ this.vol = clamp(v, 0, 1); this.render(); }
}

/* Ziehen auf einer Leiste: liefert 0…1 bei Klick, Zug und Tastatur.
   opts.achse 'x' | 'y', opts.schwelle: erst ab n Pixeln gilt es als Zug. */
function bindDrag(el, cb, opts = {}){
  const achse = opts.achse || 'x';
  const schwelle = opts.schwelle || 0;
  let ziehend = false, start = 0, gezogen = false;
  const wert = ev => {
    const r = el.getBoundingClientRect();
    const f = achse === 'x' ? (ev.clientX - r.left) / r.width : (ev.clientY - r.top) / r.height;
    return clamp(opts.umgekehrt ? 1 - f : f, 0, 1);
  };
  el.addEventListener('pointerdown', ev => {
    ziehend = true; gezogen = schwelle === 0;
    start = achse === 'x' ? ev.clientX : ev.clientY;
    el.setPointerCapture(ev.pointerId);
    if (gezogen) cb(wert(ev), 'start');
    ev.preventDefault();
  });
  el.addEventListener('pointermove', ev => {
    if (!ziehend) return;
    if (!gezogen){
      const d = Math.abs((achse === 'x' ? ev.clientX : ev.clientY) - start);
      if (d < schwelle) return;
      gezogen = true;
    }
    cb(wert(ev), 'move');
  });
  const ende = ev => {
    if (!ziehend) return;
    ziehend = false;
    cb(wert(ev), gezogen ? 'end' : 'tap');
  };
  el.addEventListener('pointerup', ende);
  el.addEventListener('pointercancel', ende);
}

/* ═════════ Bibliothek ═════════
   Jedes Blatt bringt sein eigenes Aussehen mit — eine Blende, ein Suchfeld,
   eine Liste, ein Knopf. Filtern, Zeichnen, Markieren und Öffnen ist überall
   dasselbe und steht deshalb hier.

   o = {knopf, zu, blende, feld, liste, treffer, deck, zeile(album), leer} */
function bindBibliothek(o){
  const markiere = () => [...o.liste.children].forEach(el =>
    el.classList.toggle('an', el.dataset.alb === o.deck.album.id));

  const zeichne = () => {
    const treffer = suche(o.feld.value);
    o.liste.innerHTML = treffer.map(o.zeile).join('') || (o.leer || '');
    if (o.treffer) o.treffer.textContent = o.feld.value.trim()
      ? `${treffer.length} von ${ALBUMS.length} Alben` : `${ALBUMS.length} Alben`;
    [...o.liste.children].forEach(el => el.dataset.alb && (el.onclick = () => {
      const a = ALBUMS.find(x => x.id === el.dataset.alb);
      o.deck.queue = a.tr.map((_,i) => `${a.id}-${i}`);
      o.deck.qi = 0; o.deck.pos = 0; o.deck.playing = true; o.deck.render();
      zeige(false);
    }));
    markiere();
  };

  const zeige = auf => {
    o.blende.classList.toggle('auf', auf);
    if (o.knopf) o.knopf.classList.toggle('an', auf);
    if (auf) setTimeout(() => o.feld.focus(), 60);      // erst sichtbar, dann Fokus
  };

  if (o.knopf) o.knopf.onclick = () => zeige(!o.blende.classList.contains('auf'));
  if (o.zu)    o.zu.onclick    = () => zeige(false);
  o.feld.oninput = zeichne;
  o.feld.addEventListener('keydown', ev => { if (ev.key === 'Escape') zeige(false); });
  zeichne();
  return {zeichne, markiere, zeige};
}

/* Cover als Verlauf mit Initial — im echten Spieler steht dort /api/cover. */
function coverHTML(a, cls = 'cov', extra = ''){
  return `<div class="${cls}" style="background:${grad(a)}"${extra}><span class="ini">${ini(a)}</span></div>`;
}

/* ══════════════════════════════════════════════════════════════════════════
   Die fünfundzwanzig Auslagen — nur für die Blätter 26 und 27.

   Das sind die Entwürfe für den Einstellungsdialog selbst; sie brauchen
   nicht einen Spieler, sondern die Liste aller Spieler. Namen, Formate,
   Familien und Akzente stehen hier so, wie sie in `player.html` registriert
   sind — wer dort eine Auslage hinzufügt, ergänzt hier eine Zeile.

   `signet()` zeichnet die Familie als Strichbild. Im Programm ist die
   Voransicht keine Zeichnung, sondern die Auslage selbst (siehe Blatt 26,
   „Was das im Code bedeutet"); hier fehlen dafür schlicht die Auslagen.
   ══════════════════════════════════════════════════════════════════════════ */
const AUSLAGEN = [
 {id:'geraet',   name:'Gerät',        fam:'Die Platte',  ger:'iPad hoch', ziele:['telefon','tablet','pc'],
  text:'Ein Laufwerk ohne ein Wort, quadratisch über die volle Breite. Der Tonarm ist die Spulleiste.'},
 {id:'werkstisch', name:'Werkstisch', fam:'Die Platte',  ger:'PC', ziele:['tablet','pc'],
  text:'Dasselbe Laufwerk links, rechts die Sammlung als reine Textliste mit Suchzeile.'},
 {id:'vollbild', name:'Vollbild',     fam:'Die Platte',  ger:'iPad quer', ziele:['tablet','pc'],
  text:'Nachtblau, die Platte nur aus Rillen — gespielte Ringe leuchten. Gezogen wird am Ring.'},
 {id:'deck',     name:'Deck',         fam:'Die Kassette',ger:'PC', ziele:['tablet','pc'],
  text:'Die Kassette in der Mitte, Tasten mit Druckpunkt, rechts die Sammlung als Regal mit Suche.'},
 {id:'handgeraet', name:'Handgerät',  fam:'Die Kassette',ger:'iPad quer', ziele:['tablet','pc'],
  text:'Dieselbe Kassette, fast randlos, Tasten so breit wie Daumen. Die Auswurftaste öffnet das Regal.'},
 {id:'aufgeschlagen', name:'Aufgeschlagen', fam:'Der Satz', ger:'iPad quer', ziele:['tablet','pc'],
  text:'Links die Platte, rechts der Satz. Eine Haarlinie ist die Position, mehr steht nicht da.'},
 {id:'register', name:'Register',     fam:'Der Satz',    ger:'PC', ziele:['pc'],
  text:'Dieselbe Ruhe, dazu die Warteschlange in Haarlinien am rechten Rand.'},
 {id:'bedienteil', name:'Bedienteil', fam:'Das Rack',    ger:'PC', ziele:['tablet','pc'],
  text:'Gebürstetes Metall, die Sammlung als Plattenfach in Regalordnung, ein Metallrad zum Spulen.'},
 {id:'konsole',  name:'Konsole',      fam:'Das Rack',    ger:'iPad quer', ziele:['tablet','pc'],
  text:'Dasselbe Gerät für die Hand: flacheres Fach, größeres Rad, breitere Tasten.'},
 {id:'pult',     name:'Pult',         fam:'Das Pult',    ger:'PC', ziele:['tablet','pc'],
  text:'Salbei und Terracotta: links ein langer Regler und die Titelliste, rechts die Platte.'},
 {id:'turm',     name:'Turm',         fam:'Das Möbel',   ger:'PC', ziele:['tablet','pc'],
  text:'Holz und Champagner, zwei Geräte übereinander: oben die Zeiger, unten die Bedienplatte.'},
 {id:'vollverstaerker', name:'Vollverstärker', fam:'Das Möbel', ger:'iPad quer', ziele:['tablet','pc'],
  text:'Ein Gerät statt zwei: Zeiger, Anzeige und Bedienung auf einer Frontplatte.'},
 {id:'papier',   name:'Papier',       fam:'Das Telefon', ger:'iPhone hoch', ziele:['telefon'],
  text:'Elfenbein und Messing, Serifen. Die Warteschlange ist eine Achse im rechten Rand.',
  ak:[['messing','#8A6534'],['petrol','#2E5F63'],['gruen','#4A6B3A']]},
 {id:'wueste',   name:'Desert Rose',  fam:'Das Telefon', ger:'iPhone hoch', ziele:['telefon'],
  text:'Sand und Burgunder, Bild im Passepartout, alles auf der Mittelachse. Die Achse liegt hier waagerecht.',
  ak:[['ton','#A9663F'],['rose','#8C3B4A']]},
 {id:'kissen',   name:'Kissen',       fam:'Das Telefon', ger:'iPhone hoch', ziele:['telefon'],
  text:'Weiches Weiß, Knöpfe treten aus der Fläche heraus. Der Ausschlag ist die Spulleiste.',
  ak:[['nebel','#7C8794'],['flieder','#7A6E96']]},
 {id:'karte',    name:'Karte',        fam:'Das Telefon', ger:'iPhone hoch', ziele:['telefon'],
  text:'Weiße Karte über Schwarz, die Zeit als Überschrift, ein roter Ausschlag.',
  ak:[['zinnober','#C4402A']]},
 {id:'kiesel',   name:'Kiesel',       fam:'Das Telefon', ger:'iPhone hoch', ziele:['telefon'],
  text:'Grau in Grau, weiche Kiesel. Der Spieler ist die Zeile, die läuft.',
  ak:[['graphit','#4A4A46'],['stahl','#5C6B74']]},
 {id:'abzug',    name:'Der echte Abzug', fam:'Sofortbild', ger:'iPhone hoch · PC', ziele:['telefon','tablet','pc'],
  text:'Ein Sofortbild mit breiter Kinnlade, gerade gelegt, rechte Winkel.',
  ak:[['seidenmatt','#8E8578'],['hochglanz','#2B2B2B'],['lacktropfen','#B2472F']]},
 {id:'entwicklung', name:'Die Entwicklung', fam:'Sofortbild', ger:'iPhone hoch · PC', ziele:['telefon','tablet','pc'],
  text:'Dasselbe Sofortbild — nur kommt das Bild erst, während der Titel läuft.',
  ak:[['schiefer','#4A5259']]},
 {id:'milchglas', name:'Milchglaszeilen', fam:'Zeilen', ger:'iPhone hoch · PC', ziele:['telefon','tablet','pc'],
  text:'Die Warteschlange ist der Bildschirm: jede Zeile eine Scheibe Glas.',
  ak:[['klarglas','#7FA3B0'],['fluessig','#5E8C93'],['seeglas','#6E9E86'],['perlmutt','#A79CB0'],['rauchquarz','#7A6E67']]},
 {id:'programmheft', name:'Programmheft', fam:'Zeilen', ger:'iPhone hoch · PC', ziele:['telefon','tablet','pc'],
  text:'Gedruckte Liste mit Bleistifthaken und Textmarker — der laufende Titel ist angestrichen.',
  ak:[['kunstdruck','#C2A03A'],['kreide','#6E7B86']]},
 {id:'spur',     name:'Die Spur',     fam:'Zeilen',      ger:'iPhone hoch · PC', ziele:['telefon','tablet','pc'],
  text:'Dieselbe Liste, aber jede Zeile trägt ihren eigenen Stand als Linie unter dem Titel.',
  ak:[['emaillelack','#2F6B72']]},
 {id:'emaille',  name:'Emaille',      fam:'Platten',     ger:'iPhone hoch · PC', ziele:['telefon','tablet','pc'],
  text:'Drei Platten übereinander: Bild, Bedienung, Liste. Harte Kanten, tiefe Farbe.',
  ak:[['hochglanzemail','#1F5C6B'],['glasknopf','#C9553F']]},
 {id:'gespritzt', name:'Gespritzt',   fam:'Platten',     ger:'iPhone hoch · PC', ziele:['telefon','tablet','pc'],
  text:'Dieselben Platten, aber genarbt — und der Knopf sitzt in einem Ring statt auf der Fläche.',
  ak:[['chromring','#8C9298']]},
 {id:'kalender', name:'Abreißkalender', fam:'Block',     ger:'iPhone hoch · PC', ziele:['telefon','tablet','pc'],
  text:'Der laufende Titel steht auf dem obersten Blatt, darunter der Stapel dessen, was noch kommt.'},
];

const ZIELE = [
  {id:'telefon', name:'Telefon',      text:'Hochkant in einer Hand.'},
  {id:'tablet',  name:'Tablet',       text:'iPad, hoch oder quer, mit dem Finger.'},
  {id:'pc',      name:'Schreibtisch', text:'Großes Fenster, Maus und Tastatur.'},
];
const zielName = id => (ZIELE.find(z => z.id === id) || ZIELE[0]).name;
const fuerZiel = z => AUSLAGEN.filter(L => L.ziele.includes(z));

/* ── Signet: die Familie als Strichbild ──────────────────────────────────
   Ein Rechteck ist die Fläche, die Striche sind, wo etwas steht. Mehr soll
   es nicht sein — bei 46 px Breite ist alles andere Grafik ohne Aussage. */
const SIGNET = {
 'Die Platte':   '<circle cx="34" cy="31" r="17"/><circle cx="34" cy="31" r="4"/><path d="M74 13 60 36"/>',
 'Die Kassette': '<rect x="14" y="15" width="72" height="32" rx="2"/><circle cx="36" cy="31" r="6"/><circle cx="64" cy="31" r="6"/><path d="M22 54h56"/>',
 'Der Satz':     '<circle cx="26" cy="31" r="14"/><path d="M52 20h34M52 28h34M52 36h22"/><path d="M52 50h34"/>',
 'Das Rack':     '<rect x="12" y="12" width="46" height="26" rx="1"/><path d="M12 25h46"/><circle cx="76" cy="25" r="10"/><path d="M12 48h64"/>',
 'Das Pult':     '<path d="M12 20h40M12 30h40M12 40h26"/><rect x="12" y="50" width="40" height="5" rx="2"/><circle cx="74" cy="31" r="16"/>',
 'Das Möbel':    '<rect x="12" y="10" width="76" height="20" rx="1"/><circle cx="32" cy="20" r="6"/><circle cx="52" cy="20" r="6"/><rect x="12" y="36" width="76" height="20" rx="1"/><path d="M22 46h32"/>',
 'Das Telefon':  '<rect x="34" y="6" width="32" height="52" rx="4"/><rect x="40" y="12" width="20" height="18" rx="1"/><path d="M40 38h20M40 44h14"/><path d="M74 12v40"/>',
 'Sofortbild':   '<rect x="30" y="6" width="40" height="52" rx="1"/><rect x="35" y="11" width="30" height="26"/><path d="M38 44h24"/><circle cx="50" cy="52" r="4"/>',
 'Zeilen':       '<path d="M14 12h72M14 22h72M14 32h72M14 42h72M14 52h48"/><rect x="12" y="28" width="76" height="8" rx="1" fill="currentColor" fill-opacity=".18" stroke="none"/>',
 'Platten':      '<rect x="20" y="6" width="60" height="16" rx="1"/><rect x="20" y="25" width="60" height="14" rx="1"/><circle cx="50" cy="32" r="4"/><rect x="20" y="42" width="60" height="16" rx="1"/>',
 'Block':        '<rect x="24" y="8" width="52" height="26" rx="1"/><path d="M28 40h44M31 47h38M34 54h32"/>',
};
function signet(fam, w = 46){
  return `<svg class="sig" viewBox="0 0 100 64" width="${w}" height="${Math.round(w * .64)}"
    fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"
    aria-hidden="true">${SIGNET[fam] || ''}</svg>`;
}

/* Jede Familie hat einen Grund, eine Tinte und einen Akzent. Das ist keine
   Palette der Auslage, sondern ihr Wiedererkennungswert im Kleinen: in einer
   Voransicht von 90 px ist die Farbe das Erste, was ankommt. */
const FAMILIENFARBEN = {
 'Die Platte':   ['#EFEFEC','#1A1A16','#8A6534'],
 'Die Kassette': ['#2A2A28','#F2EFE7','#C8A24A'],
 'Der Satz':     ['#FBF9F5','#241E18','#8A6534'],
 'Das Rack':     ['#B7BABC','#23262A','#C4402A'],
 'Das Pult':     ['#DCE3D4','#2C3327','#B4593A'],
 'Das Möbel':    ['#4A3628','#F0E4D0','#D9C48A'],
 'Das Telefon':  ['#F5F0E4','#2A2419','#8A6534'],
 'Sofortbild':   ['#E8E6E1','#1F1D1A','#B2472F'],
 'Zeilen':       ['#E4EAEE','#26333E','#5E8C93'],
 'Platten':      ['#16505C','#EAF2F2','#C9553F'],
 'Block':        ['#F2EDE2','#2A2620','#C24A32'],
};
/* Grund, Tinte, Akzent — der gewählte Akzent schlägt den der Familie. */
function farbenFuer(L, akzentId){
  const [bg, ink, akz] = FAMILIENFARBEN[L.fam] || FAMILIENFARBEN['Der Satz'];
  const eigen = ((L.ak || []).find(a => a[0] === akzentId) || [])[1];
  return [bg, ink, eigen || akz];
}
