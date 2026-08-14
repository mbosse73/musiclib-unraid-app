# Zweiter Satz: acht Spieler aus dem Ordner `player2/`

Acht Entwürfe, gebaut aus den Fotos in `player2/` im Wurzelverzeichnis. Sie sind
kein Teil des gelieferten Design-Pakets, halten sich aber an dessen Regeln, weil
sie am Ende durch dieselbe Portierung gehen sollen:

- **eigenständiges HTML**, kein Framework, keine externen Dateien, keine
  Webfonts, keine Bilddateien — alles CSS und inline SVG;
- **feste Bühnenmaße** wie im Paket: iPhone 1080 × 2340, PC 1600 × 1000;
- **Namensschema** `fotoNN_Konzeptname_plattform.html`, Nummern 39–46 als
  Fortsetzung der 17–38 aus dem Paket;
- **jedes Blatt hat Transport, Fortschritt, Zeiten und einen Bibliotheks-Zugang.**
  Der Zugang ist Pflicht, nicht Zierde: ein Layout ohne ihn wäre in `player.html`
  unvollständig.

## Woraus was entstanden ist

| Nr | Name | Foto | Was die Vorlage hergibt | Bibliotheks-Zugang |
|---|---|---|---|---|
| 39 | Kippschalter | 23.30.54 | Schwarz, reine Typografie, zwei Kippschalter als Buchstaben | Umrisspille oben rechts |
| 40 | Neonschild | 23.31.26 | Dunkler warmer Raum, Leuchtschrift, Plattenspieler | Leuchtpille oben rechts |
| 41 | Sonntagsblatt | 23.34.02 | Graupappe, fette Schlagzeile, Objekte mit weissem Konturstrich | Umrisspille am Fuss |
| 42 | Druckgrafik | 23.34.53 | Kunstdruck in drei Farben, Teller von oben, Schieber und Knöpfe | Signatur oben links |
| 43 | Sonnenglas | 23.38.31 | Glühender Himmel, schwarzer Horizont, Karte aus Milchglas | Glaspille über der Karte |
| 44 | Gerätezeile | 23.43.04 + 23.43.13 | Kargstes Display: Titel, Haarlinie, Lautstärkezahl, Dreieck | Schriftzug oben mittig |
| 45 | Kassettenhaufen | 23.56.47 | Berg bunter C60-Kassetten, dunkle Pille, rote Taste | Dunkle Pille — und der Haufen selbst |
| 46 | Malerblatt | 23.54.59 | Gemaltes Stillleben auf beschriebenem Papier | Pille oben rechts |

**Zwei Fotos, ein Entwurf:** 23.43.04 (schwarz) und 23.43.13 (silbern) zeigen
dasselbe Display in zwei Tönen. Statt zwei fast gleicher Blätter bekommt in 44
das iPhone die schwarze und der Rechner die silberne Fassung — so bleiben beide
Fotos erhalten.

**Ein Foto ist nicht verwertet:** 23.56.39 ist ein 15 KB grosses Vorschaubild,
auf dem nur eine Ecke mit einem „A" zu erkennen ist. Daraus lässt sich keine
Bildsprache ableiten.

Die Übertragung folgt in jedem Fall demselben Gedanken: **nicht das Foto
nachzeichnen, sondern seine Bausprache übernehmen** und den ganzen Spieler
daraus bauen. Bei 39 heisst das, dass der Schalter nicht *neben* der Wiedergabe
sitzt, sondern *die* Wiedergabe ist; bei 45, dass der Haufen nicht Hintergrund
ist, sondern die Sammlung; bei 42, dass kein Bauteil plastisch sein darf, weil
ein Druck keine Schatten wirft.

Drei der acht Vorlagen (39, 41, 45) sind Grafiken ohne jede Bedienung; dort ist
mehr erfunden als übertragen. 43 und 44 waren dagegen schon fast fertige
Oberflächen — die sind eher Port als Entwurf.

## Neu bauen

```bash
cd design/entwuerfe/src
python3 baualle.py          # schreibt alle 16 Dateien nach ../html/
```

`werkzeug.py` hält, was alle acht teilen: das eine Beispielalbum, die Zeichen
(Bibliothek, Lupe, Mischen, Wiederholen, Lautstärke), das abstrakte Cover, die
Schallplatte, die Kassette und die Wellenform. Dokumentgerüst und die
Transportzeichen kommen aus `../../src/lib.py`, also aus dem Paket selbst —
damit beide Sätze dieselbe Sprache sprechen und ein späterer Port nicht zwei
Vokabulare lernen muss.

Jede `dNN.py` liefert `telefon()` und `rechner()`, beide geben `(css, body)`
zurück. Der Faktor `g` in `_css(g)` ist der einzige Unterschied zwischen den
Plattformen bei den Maßen der Bauteile — die Anordnung ist je Plattform von Hand
gesetzt, nicht skaliert.

## Was noch offen ist

Diese acht sind **Entwürfe zum Ansehen**, noch kein Layout in `player.html`.
Ob und welche davon portiert werden, steht in `design/AUSWAHL.md` — dort sind
sie bisher nicht eingetragen, weil die Auswahl beim Eigentümer liegt.
