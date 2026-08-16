# Acht Telefon-Themen, die es einmal gab

`mobile.html` in diesem Ordner ist **kein Entwurf und keine Vorlage**, sondern
eine Kopie: die Datei, wie sie am Ende des Zweigs
`claude/player-ui-integration-mockups-pzjhw1` stand. Sie ist byte-identisch mit
dessen Stand und liegt hier **nur zur Sicherung**.

Der Grund ist unangenehm einfach: der Code dieser acht Erscheinungen existierte
bis dahin an genau einer Stelle auf der Welt — auf einem Zweig, der nie gemergt
wurde. Zwei solche Zweige sind übersehen worden, und aus dem einen sind
fünf Blätter, zehn Spieler und eine ganze Reihe Korrekturen an `player.html`
zurückgeholt worden. Ein Zweig ist kein Archiv. Deshalb steht die Datei jetzt
hier, wo sie ein `git clone` mitbringt.

## Die acht

Alle laufen im Ansichtszustand „Jetzt läuft". Die Aufnahmen daneben sind aus
dieser Datei selbst gemacht, gegen dieselbe Testsammlung wie alles andere.

| Datei | Thema | Form | Was es ist |
|---|---|---|---|
| `thema_abzug.jpg` | Der echte Abzug | `karte` | Ein Sofortbild mit breiter Kinnlade: Bild, Titel, Bahn und Knöpfe auf einer Karte, gerade gelegt, rechte Winkel |
| `thema_entwicklung.jpg` | Die Entwicklung | `karte` | Dasselbe Sofortbild — nur kommt das Bild erst, während der Titel läuft. Die Position ist die Entwicklungszeit |
| `thema_milchglas.jpg` | Milchglaszeilen | `liste` | Die Warteschlange *ist* der Bildschirm: jede Zeile eine Scheibe Glas, oben eine schmale Jetzt-Zeile |
| `thema_programmheft.jpg` | Programmheft | `liste` | Gedruckte Liste mit Bleistifthaken und Textmarker — der laufende Titel ist angestrichen |
| `thema_spur.jpg` | Die Spur | `liste` | Dieselbe Liste, aber jede Zeile trägt ihren eigenen Stand als Linie unter dem Titel |
| `thema_emaille.jpg` | Emaille | `platten` | Drei Platten übereinander: Bild, Bedienung, Liste. Harte Kanten, tiefe Farbe |
| `thema_gespritzt.jpg` | Gespritzt | `platten` | Dieselben Platten, aber genarbt — und der Knopf sitzt in einem Ring statt auf der Fläche |
| `thema_kalender.jpg` | Abreißkalender | `block` | Der laufende Titel steht auf dem obersten Blatt, darunter der Stapel dessen, was noch kommt |

## Warum sie nicht einfach eingebaut sind

Diese Datei stammt **von vor der Konsolidierung**. Damals war das Telefon eine
eigene Datei mit einer `THEMEN`-Liste; ein Thema trug eine Palette *und* eine
`form`, und `form` entschied, wie „Jetzt läuft" aufgebaut ist.

Seit Etappe 3 gilt das nicht mehr. Das Telefon bekommt sein Aussehen aus
`player.html`, als Auslage (`layout({…})`), und `mobile.html` im
Wurzelverzeichnis ist nur noch die Rückfallseite unter `/mobil-alt`, die
ohnehin verschwinden soll.

Diese Datei über die heutige `mobile.html` zu kopieren wäre deshalb **keine
Wiederherstellung, sondern ein Rückschritt**: die acht Erscheinungen lägen dann
in einer Datei, die niemand mehr benutzt, und die heutige Rückfallseite wäre
kaputt, weil hier noch die alte Architektur davorsteht.

**Eine dieser acht zu benutzen heißt: sie als Auslage in `player.html` neu
bauen** — ein CSS-Block auf einer eigenen Wurzelklasse plus ein
`layout({id, name, ziele:['telefon'], klasse, bau(w, deck)})`. Genau diesen Weg
sind *Papier*, *Desert Rose*, *Kissen*, *Karte* und *Kiesel* schon gegangen;
das waren auch einmal Themen in `mobile.html`. Der Aufwand entspricht dem einer
Portierung aus einem gezeichneten Blatt — nur liegt hier eine laufende Fassung
als Vorlage daneben statt einer Zeichnung.

## Wie man sie laufen sieht

Die Datei ist **kein eigenständiges Mockup**: anders als alles andere unter
`mockups/` erfindet sie keine Sammlung, sondern spricht mit der echten API
(`/api/library`, `/api/stream/…`). Ein Doppelklick im Dateimanager zeigt
deshalb eine leere Seite.

Zwei Wege, beide ohne Änderung am Repo:

**Kurz und schmutzig** — die Seite unter ihrer alten Adresse ausliefern:

```bash
cp mobile.html /tmp/mobile-heute.html          # heutige Fassung beiseite
cp mockups/acht-themen/mobile.html mobile.html # alte einsetzen
MUSIC_DIR=… DATA_DIR=… .venv/bin/python app.py # /mobil-alt öffnen
cp /tmp/mobile-heute.html mobile.html          # danach zurück!
```

**Sauber** — die Datei im Browser unterschieben, ohne das Repo anzufassen: eine
Playwright-Route auf `/mobil-alt` abfangen und mit dieser Datei beantworten.
So sind die Aufnahmen oben entstanden.

In beiden Fällen wählt man das Thema über die Einstellungen der Seite oder
direkt:

```js
localStorage.setItem('musiklib:einstellungen',
  JSON.stringify({thema: 'kalender', akzent: 'chromopapier', leiste: 'dauerhaft'}));
```

Ein Akzent gehört immer zu genau einem Thema — Messing auf Sand wäre keine
Wahl, sondern ein Fehler. Wer einen fremden oder erfundenen Namen einträgt,
bekommt deshalb den ersten Akzent des Themas; `gewaehlt()` prüft jeden Wert
und fällt still auf den Standard zurück. So sind die Aufnahmen hier entstanden,
sie zeigen also jeweils den **ersten** Akzent.

| Thema | `thema` | `form` | Akzente (`akzent`) |
|---|---|---|---|
| Der echte Abzug | `abzug` | `karte` | `seidenmatt`, `hochglanz`, `lacktropfen` |
| Die Entwicklung | `entwicklung` | `karte` | `schiefer` |
| Milchglaszeilen | `milchglas` | `liste` | `klarglas`, `fluessig`, `seeglas`, `perlmutt`, `rauchquarz` |
| Programmheft | `programmheft` | `liste` | `kunstdruck`, `kreide` |
| Die Spur | `spur` | `liste` | `emaillelack` |
| Emaille | `emaille` | `platten` | `hochglanzemail`, `glasknopf` |
| Gespritzt | `gespritzt` | `platten` | `chromring` |
| Abreißkalender | `kalender` | `block` | `chromopapier` |

Dazu die beiden, die es auf `main` geschafft haben und dort bis heute laufen:
`papier` (`messing`, `petrol`, `gruen`) und `wueste` (`ton`, `rose`).

## Was hier nicht passieren darf

Diese Datei wird **nicht gepflegt**. Sie ist ein Stand von einem Tag, kein
Zweitsystem. Wer an `mobile.html` im Wurzelverzeichnis etwas ändert, ändert
hier nichts — und soll hier auch nichts ändern. Wenn eines der acht Themen
gebaut wird, ist das Ergebnis eine Auslage in `player.html`, und diese Kopie
bleibt trotzdem stehen, als Beleg dafür, wie die Vorlage aussah.
