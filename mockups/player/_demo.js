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

/* Cover als Verlauf mit Initial — im echten Spieler steht dort /api/cover. */
function coverHTML(a, cls = 'cov', extra = ''){
  return `<div class="${cls}" style="background:${grad(a)}"${extra}><span class="ini">${ini(a)}</span></div>`;
}
