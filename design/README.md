# Music Player — Design-Paket (44 Entwürfe)

Übergabepaket für das **musiclib**-Repo. Enthält 22 Player-Konzepte, jeweils als
**iPhone-Variante (Hochformat)** und **PC-Variante (Querformat)** — 44 Entwürfe insgesamt.

Jeder Entwurf ist aus einem realen Referenzfoto (Hardware oder Grafik) abgeleitet und als
**pixelgenaues, in sich geschlossenes HTML** vorhanden. Das HTML ist die verbindliche Quelle:
kein Framework, keine externen Assets, keine Web-Fonts, keine Bilddateien — alles ist CSS + inline SVG.

---

## Inhalt

```
musicplayer-designs/
├─ README.md                  ← diese Datei
├─ IMPLEMENTATION_BRIEF.md    ← Arbeitsauftrag für den umsetzenden Agenten / Entwickler
├─ SPEC.md                    ← Entwurf für Entwurf: Komponenten, Zustände, Bibliotheks-Zugang
├─ tokens.json                ← Design-Tokens (Farben, Schrift, Radien) je Entwurf
├─ previews/                  ← 44 PNGs, 2× Auflösung (Referenzbilder zum Abgleich)
├─ html/                      ← 44 eigenständige HTML-Dateien (die eigentliche Quelle)
└─ src/                       ← Python-Generator, der die HTML erzeugt (optional)
```

### Namensschema

`fotoNN_Konzeptname_plattform`

- `NN` = Nummer des Referenzfotos (17–38)
- `plattform` = `iphone` (1080 × 2340) oder `pc` (1600 × 1000)

Beispiel: `foto28_Rewind-Boombox_iphone.html` ↔ `foto28_Rewind-Boombox_iphone.png`

---

## Schnellstart

```bash
# Einen Entwurf im Browser ansehen
open html/foto30_iPod-Weiss_pc.html

# Alle Entwürfe nebeneinander
python3 -m http.server 8000 --directory html
# → http://localhost:8000
```

Die HTML-Dateien sind auf eine **feste Bühnengröße** ausgelegt (`.stage`, siehe unten).
Sie sind bewusst *nicht* responsiv — sie definieren das Ziel-Layout je Formfaktor.

---

## Aufbau einer HTML-Datei

```html
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1080px;height:2340px;overflow:hidden}
  .stage{position:relative;width:1080px;height:2340px;overflow:hidden}
</style>
<div class="stage"> … Layout … </div>
```

Alles innerhalb von `.stage` ist reines Flexbox-Layout mit Inline-Styles.
Wiederkehrende Grafiken (Schallplatte, Bandspule, VU-Meter, Kassette, Lautsprecher,
Wellenform, Icons) sind **inline SVG** und damit frei skalier- und einfärbbar.

---

## Verbindliche Regeln, die in allen 44 Entwürfen gelten

1. **Jeder Entwurf ist vollständig bedienbar gedacht.** Vorhanden sind immer:
   Zurück · Play · Pause · Weiter, ein Fortschrittsbalken mit Position, sowie
   verstrichene und Gesamtzeit.
2. **Jeder Entwurf hat einen Zugang zur Musikbibliothek.** Bei Geräten mit Bedienpanel
   ist das die **Eject-Taste** in der Tastenreihe (Bandmaschine, Kassettendeck, Radio);
   sonst ein eigener Button, der sich ins jeweilige Designsystem einfügt
   (z. B. „CRATE", „ARCHIV", „LINE-UP", „SAMMLUNG"). Siehe `SPEC.md`, Spalte *Bibliothek*.
3. **Fläche ist durchgestaltet.** Leerräume gibt es nur dort, wo sie zum Stil gehören
   (etwa die Wand um ein gerahmtes Poster).
4. **Keine echten Songtexte.** In den beiden Poster-Entwürfen (36, 37) läuft bewusst eine
   Folge bekannter **Albumtitel** spiralförmig durch die Rille — kein geschützter Liedtext.
   Diese Regel bitte bei der Umsetzung beibehalten.
5. **Inhalte sind Platzhalter.** Titel, Interpreten, Laufzeiten und Cover dienen nur der
   Darstellung und sind gegen echte Daten aus der Bibliothek zu ersetzen.

---

## Was dieses Paket *nicht* ist

- Kein lauffähiger Player: es gibt keine Audio-Logik, keinen Zustand, keine Datenanbindung.
- Kein responsives Layout: die Entwürfe zeigen zwei feste Formfaktoren.
- Keine Komponentenbibliothek: die Zerlegung in Komponenten ist Teil der Umsetzung
  (Vorschlag dazu in `IMPLEMENTATION_BRIEF.md`).

---

## Neu erzeugen (optional)

```bash
cd src
pip install playwright
python3 renderall.py     # schreibt PNGs nach ../previews
```

Der Generator ist Python + Playwright/Chromium. Er ist beigelegt, damit Varianten
schnell durchgespielt werden können — für die Umsetzung im Repo wird er nicht gebraucht.
