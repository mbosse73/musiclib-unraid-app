# Auftrag: `tag.html` — der Spieler mit einem Knopf

**Stand:** **umgesetzt** — `tag.html` und die Route `/tag` stehen, Tests in
`test_app.py` und `test_frontend.py` (`-k day`). Was hier steht, gilt weiter:
es ist die Begründung hinter dem Code. Die drei offenen Fragen sind unten
beantwortet.
**Vorlage:** `mockups/player/14-album-des-tages.html`, **Variante 1 · Ring**.
Variante 2 („Sonnenaufgang") ist **verworfen** — sie steht im Blatt nur noch als
Begründung, warum der Ring gewonnen hat. Nichts aus Variante 2 wird gebaut.

Dieses Blatt ist eine Attrappe: erfundene Sammlung, gefälschte Uhr, kein Ton,
kein `localStorage`. Es zeigt, **wie es aussieht und wie es sich anfühlt**.
Was hier steht, ist der Rest: was es tun muss.

---

## 1. In einem Satz

Eine vierte Oberfläche unter `/tag`, eine einzelne Datei `tag.html`: ein
Spieler fürs iPhone, der **nichts auswählt**. Er spielt das **Album des
Tages** — per Zufall aus der Sammlung, den ganzen Tag lang immer wieder,
am nächsten Tag ein anderes. Bedient wird er mit **einem einzigen Knopf**.

## 2. Was ausdrücklich nicht gebaut wird

Das ist kein Sparprogramm, das ist der Entwurf:

- **keine Bibliothek, keine Suche, keine Sortierung, kein Scan** (auch nicht
  hinter einem Knopf, auch nicht als Blende);
- **kein Weiter, kein Zurück, kein Spulgriff, kein Lautstärkeregler**;
- **keine Cover** — das Album ist hier ein Name, kein Bild. `/api/cover` wird
  von dieser Seite nicht aufgerufen;
- **kein zweiter Knopf**, auch kein kleiner in der Ecke;
- **kein neues Feld in `library.json`**, keine neue API, kein Datenbankgedanke;
- **keine zweite Datei**: kein Bauwerkzeug, kein Modul, kein CSS daneben.
  `tag.html` ist eine Datei, über SMB zu ändern, ohne Neustart des Containers —
  dieselbe Regel wie für `index.html`, `mobile.html`, `player.html`.

## 3. Route und Datei

```python
@app.get("/tag")
def tag():
    """Spieler mit einem Knopf — das Album des Tages.

    Wie /mobil und /ipad: die Datei wird unveraendert ausgeliefert, keine
    Geraetekennung, keine Weiterleitung. Wer sie will, legt /tag auf den
    Home-Bildschirm.
    """
    return FileResponse(APP_DIR / "tag.html", media_type="text/html")
```

Gebraucht werden genau zwei Endpunkte: `/api/library` und
`/api/stream/{track_id}`.

## 4. Bedienung — der einzige Knopf

Die rote Scheibe ist ein echtes `<button>`, 248 px, in der Mitte der Karte.

- **Tippen schaltet um, sofort.** Einmal drücken = spielt, noch einmal =
  hält an, noch einmal = spielt weiter. Kein erkannter Doppeltipp: der
  müsste ~250 ms warten, ob ein zweiter kommt, und diese Verzögerung vor
  jedem Abspielen ist bei einem Knopf, der sonst nichts kann, nicht
  zu rechtfertigen.
- **Fünf Tipper innerhalb von je 700 ms** (`FENSTER`, gemessen von Tipp zu
  Tipp) wählen ein **neues Album für heute**. Gezählt wird *nebenher*,
  während längst geschaltet wurde; der fünfte Tipp überschreibt das
  Ergebnis: neues Album, spielt.
- **Der Wechsel ist einmal am Tag erlaubt.** Der zweite Versuch am selben
  Tag zeigt die Kerben durchgestrichen und die Zeile „Heute schon
  gewechselt", sonst passiert nichts.
- **Rückmeldung:** ab dem *zweiten* Tipp erscheinen unter der Scheibe fünf
  Kerben, die sich rot füllen; nach 700 ms ohne Tipp verschwinden sie
  wieder. Wer nur abspielt, sieht sie nie.
- **Tastatur:** Leertaste = derselbe Umschalter. `aria-pressed` und ein
  `aria-label`, das mitwandert („*Album* von *Interpret* abspielen" /
  „*Album* anhalten"). Sonst gibt es auf der Seite kein Fokusziel.

Zählwerk aus dem Blatt übernehmen — es ist getestet:

```js
let n = 0, fenster = null;
knopf.addEventListener('click', () => {
  deck.toggle();                                  // sofort, ohne Warten
  n++; kerben(n);
  clearTimeout(fenster);
  fenster = setTimeout(() => { n = 0; kerben(0); }, FENSTER);
  if (n >= NOETIG){                               // NOETIG = 5
    n = 0; clearTimeout(fenster);
    if (gewechselt){ kerbenVerbraucht(); hinweis('Heute schon gewechselt'); }
    else { gewechselt = true; schub++; setzeAlbum(albumDesTages(...), true);
           hinweis('Neues Album für heute'); }
  }
});
```

## 5. Das Album des Tages

**Berechnet, nicht gewürfelt.** FNV-1a über den Tagesschlüssel, modulo der
Länge der Sammlung — dieselbe Zahl auf jedem Gerät, ohne Server, ohne
gespeicherten Zufall:

```js
function hash(s){
  let x = 2166136261 >>> 0;
  for (const ch of String(s)){ x ^= ch.charCodeAt(0); x = Math.imul(x, 16777619) >>> 0; }
  return x >>> 0;
}
function albumDesTages(iso, schub, ausser){
  const n = ALBUMS.length;
  let i = hash(iso + '#' + schub) % n;
  if (n > 1 && ausser && ALBUMS[i].id === ausser) i = (i + 1) % n;  // nie zweimal dasselbe
  return ALBUMS[i];
}
```

- `iso` ist `YYYY-MM-DD` **lokaler Zeit** (nicht UTC — der Tag ist der Tag
  des Benutzers).
- `schub` zählt hoch statt neu zu würfeln: auch das zweite Album eines
  Tages ist damit reproduzierbar.
- `ausser` ist das Album, das gerade steht (gestern bzw. vor dem Wechsel).
  Bei acht Alben käme sonst jeder achte Tag dasselbe wie gestern — und das
  sieht aus wie ein Fehler, nicht wie Zufall.
- **Reihenfolge festnageln:** `ALBUMS` muss vor der Wahl in einer stabilen
  Ordnung stehen (dieselbe Sortierung wie in `player.html`s `uebernimm()`),
  sonst hängt die Wahl an der Laune der Sammlung.

**Gespeichert wird trotzdem**, unter `musiklib:tag`:

```js
{ datum: '2026-08-14', albumId: 'a1b2c3…', schub: 0, gewechselt: false }
```

Der gespeicherte `albumId` **gewinnt**, solange er sich auflösen lässt: Sonst
tauschte ein Scan mitten am Tag das Album unter den Füßen aus, weil sich die
Länge der Liste geändert hat. Löst er sich nicht mehr auf (Album gelöscht),
wird für denselben Tag neu gerechnet. `gewechselt` gilt nur für `datum`;
ein neuer Tag setzt alles zurück.

**Der Tageswechsel kommt, während die App offen ist** — ein Telefon liegt
nachts auf dem Nachttisch. Geprüft wird bei `visibilitychange`, am Ende
jedes Titels und in einem Minutentakt; **kein** Timer auf Mitternacht, den
iOS im Hintergrund ohnehin nicht feuert. Läuft gerade Ton, wird der
laufende Titel **zu Ende gespielt**, das neue Album kommt danach.

## 6. Was angezeigt wird

Unten links, in dieser Reihenfolge (Größen und Farben stehen im Blatt):

1. `ALBUM DES TAGES` — kleine gesperrte Versalien, unveränderlich;
2. **Albumtitel**, groß, Versalien, höchstens drei Zeilen;
3. **Interpret**, gesperrte Versalien, einzeilig mit Ellipse;
4. **laufender Titel**.

Dazu die Scheibe selbst:

- **voll und rot, solange Ton läuft**; angehalten bleibt der Kreis stehen,
  wird aber leer — Papier mit roter Linie und Dreieck darin. Das ist der
  ganze Zustandsanzeiger und aus zwei Metern zu lesen;
- **ein Ring um die Scheibe** trägt die Position **im Album**
  (`gpos / total`), ein voller Umlauf ist ein Durchlauf;
- **kein Datum, keine Fäden, kein Zählwerk.** Bewusst gestrichen: Welcher
  Tag ist, sagt das Album; wie weit es ist, sagt der Ring.

Zustand kommt aus den Ereignissen des `<audio>`-Elements, **nie** aus einer
Annahme neben dem Aufruf — dieselbe Regel wie in `index.html`, aus demselben
Grund (Sperrbildschirm, Medientasten, blockiertes Autoplay).

## 7. Warteschlange, Sitzung, Schlüssel

- **Die Warteschlange ist das Album, und sie endet nie.** Nach dem letzten
  Titel geht es zum ersten zurück. Das entspricht
  `musiklib:fortsetzung = "wiederholen"`; diese Seite **schreibt den
  Schlüssel nicht und liest ihn nicht** — ihre Fortsetzung ist der Tag.
- `musiklib:session`, `volume`, `muted` behalten **Form und Bedeutung** der
  anderen drei Oberflächen (`test_frontend.py` prüft das für `mobile.html`
  gegen `index.html`; für `tag.html` sinngemäß dasselbe).
- `musiklib:shuffle` wird **nicht gelesen**: Ein Album des Tages in
  zufälliger Reihenfolge wäre ein anderes Versprechen.
- `musiklib:tag` ist neu und gehört dieser Seite allein.
- **Angehalten heißt angehalten, auch über einen Neustart der Seite hinweg.**
  Die Stelle steht in `musiklib:session`; wiederhergestellt wird sie, gespielt
  wird erst auf den Knopf — **nie Autoplay**, wie in `index.html`. Ein neuer
  Tag setzt die Stelle zurück, weil er die Warteschlange austauscht.

## 8. Was aus `player.html` unverändert mitkommt

Nicht neu schreiben, **übernehmen** (Abschnitte „Unterbau" in `player.html`,
Zeilen um 1040–1530) — hier ist es wichtiger als anderswo, weil ein Spieler
ohne zweiten Knopf keinen Weg hat, sich von Hand zu erholen:

| Was | Warum |
| --- | --- |
| `nachdruck()` samt `tonGewuenscht`, `NACH_VERZUG`, `NACH_MAX` | iOS lehnt `play()` beim Titelwechsel im Hintergrund ab. `tonGewuenscht` ist der einzige Unterschied zwischen „abgelehnt" und „der Benutzer hat angehalten" |
| `heilungPlanen()` / `versucheWeiter()`, `waiting`/`stalled`/`timeupdate` | hängender Strom bei gedrosseltem WLAN oder schlafender NAS-Platte |
| `error`-Behandlung nur für Code 2/3 | Code 4 ist eine verschobene Datei — die kommt durch keinen Versuch zurück |
| `ladeVor()` (256 KB, 25 s vor dem Ende) | weckt die Platte, bevor sie gebraucht wird |
| Media Session (`play`/`pause`; **kein** `nexttrack`/`previoustrack`) | der Sperrbildschirm bedient denselben einen Knopf |
| `store()`/`restore()` mit stillem Fehlschlag | eine Browsersitzung ohne Speicher muss trotzdem laufen |
| `uebernimm()` | flache API-Alben einmal in die Form der Entwürfe bringen |
| `HEIL_VERZUG`/`NACH_VERZUG` als `let` | damit die Tests nicht Sekunden warten |

**Bildschirm wach:** `musiklib:wach` ist der geteilte Schlüssel und der
Grund, warum iOS bei dunklem Schirm nicht das WLAN drosselt. `tag.html`
**liest** ihn und hält die Sperre entsprechend, bekommt aber **keinen
eigenen Schalter** — gestellt wird er auf `/mobil` oder `/ipad`. (Siehe
offene Frage 1.)

## 9. Fehlerfälle

- **Sammlung nicht erreichbar:** eine Zeile auf der Karte, kein Dialog.
  Deutsch, wie überall.
- **Noch keine Alben:** „Noch keine Alben — gescannt wird am Schreibtisch"
  mit Verweis auf `/`.
- **Genau ein Album:** funktioniert, der Wechsel bringt dasselbe zurück.
  Der Hinweis muss das sagen, nicht so tun, als hätte er gewechselt.
- **Titel nicht abspielbar (Code 4):** Text auf der Karte, kein endloser
  Versuch. Der Knopf muss bedienbar bleiben.

## 10. Tests

`test_app.py`:
- `/tag` antwortet 200 und liefert HTML (analog zu den Tests für `/mobil`
  und `/ipad`).

`test_frontend.py` (Chromium gegen `app.py` im Unterprozess, Muster der
vorhandenen Tests, `TRACK_SECONDS = 30` beachten):
- ein Tipp spielt, der zweite hält an, der dritte spielt weiter;
- fünf Tipper innerhalb des Fensters wechseln das Album, der zweite Versuch
  am selben Tag nicht;
- der Ring wächst, während gespielt wird;
- Album, Interpret und laufender Titel stehen auf der Karte;
- `musiklib:session` hat dieselbe Form wie bei den anderen Oberflächen;
- am Ende des letzten Titels beginnt das Album von vorn.

**Damit das prüfbar ist**, müssen zwei Dinge von außen erreichbar sein —
nach dem Muster von `HEIL_VERZUG`:

```js
let FENSTER = 700;                 // Tippfenster, im Test kürzer
let heute = () => new Date();      // im Test ersetzbar: () => new Date('2026-08-15T10:00')
```

Beides `let` auf oberster Ebene des Skripts, sonst wird der Tageswechsel
nur mit einer echten Nacht prüfbar.

## 11. Abnahme

- [ ] `/tag` liefert `tag.html`; `index.html`, `mobile.html`, `player.html`
      und `app.py` sind sonst unverändert.
- [ ] Eine Datei, kein Bauwerkzeug, alle Texte deutsch.
- [ ] Ein sichtbares Bedienelement. Ein Fokusziel.
- [ ] Umschalten ohne spürbare Verzögerung.
- [ ] Fünf Tipper wechseln, einmal am Tag; die Kerben erklären das ohne Text.
- [ ] Derselbe Tag ergibt auf zwei Geräten dasselbe Album.
- [ ] Über Mitternacht hinweg wechselt das Album, ohne den laufenden Titel
      abzuschneiden.
- [ ] Titelwechsel bei dunklem Bildschirm hält durch (`nachdruck()`).
- [ ] Bestehende Testsuite bleibt grün, neue Tests kommen dazu.
- [ ] `CLAUDE.md` und `README.md` kennen die vierte Oberfläche.

## 12. Die drei Fragen — so entschieden

Gebaut ist jeweils der Vorschlag. Wer eine davon anders will, ändert eine
Stelle; wo, steht dabei.

1. **Bildschirm wach: kein eigener Schalter.** `tag.html` liest
   `musiklib:wach` und hält die Sperre entsprechend; gestellt wird sie auf
   `/mobil` oder `/ipad`. Kein langes Drücken — eine zweite verborgene Geste
   neben dem Fünffachtipp wäre eine zu viel für einen Knopf.
   (`wachGewuenscht()` in `tag.html`.)
2. **Titelnummer: weg.** Die dritte Zeile trägt nur den Titelnamen. Wer
   „So What · 3/5" will, ändert eine Zeile in `zeichne()`.
3. **Neuer Tag bei laufendem Ton: es läuft weiter.** Der laufende Titel wird
   zu Ende gespielt, dann kommt das neue Album — und es spielt, weil vorher
   auch gespielt wurde. Wer stattdessen anhalten will, ruft
   `wechsleAufNeuenTag(false)` im `ended`-Zweig.

## 13. Was beim Bauen dazukam

Zwei Dinge, die im Auftrag nicht standen und im Code stehen, mit Grund:

- **`tippe()` zeichnet sofort neu.** Nicht auf Verdacht — `ton.paused` hat
  zu diesem Zeitpunkt bereits umgeschaltet, das Ereignis kommt einen
  Wimpernschlag später. Ohne das hinkt der Knopf hinterher; ein Test hat es
  gefunden. Gelesen wird weiterhin nur das Element, nie eine Annahme.
- **Der Fortschrittsring bekommt seinen Versatz schon beim Laden.** Ohne
  ihn steht der Bogen bis zum ersten Zeichnen auf „voll", und der Ring
  blitzt beim Öffnen einmal ganz auf.
