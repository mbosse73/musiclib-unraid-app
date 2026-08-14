# Zweiter Satz: vier Spieler aus dem Ordner `player2/`

Vier Entwürfe, gebaut aus den Fotos in `player2/` im Wurzelverzeichnis. Sie sind
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
| 43 | Sonnenglas | 23.38.31 | Glühender Himmel, schwarzer Horizont, Karte aus Milchglas | Glaspille über der Karte |
| 44 | Gerätezeile | 23.43.04 + 23.43.13 | Kargstes Display: Titel, Haarlinie, Lautstärkezahl, Dreieck | Schriftzug oben mittig |
| 46 | Malerblatt | 23.54.59 | Gemaltes Stillleben auf beschriebenem Papier | Pille oben rechts |

**Zwei Fotos, ein Entwurf:** 23.43.04 (schwarz) und 23.43.13 (silbern) zeigen
dasselbe Display in zwei Tönen. Statt zwei fast gleicher Blätter bekommt in 44
das iPhone die schwarze und der Rechner die silberne Fassung — so bleiben beide
Fotos erhalten.

## 43 Sonnenglas — sechs Fassungen

Von 43 gibt es fünf zusätzliche Fassungen. Sie spielen **zwei Achsen** gegen­
einander durch: die Farbwelt hinter dem Glas und die Dicke des Glases selbst.
Dick heisst dabei nicht nur mehr Weichzeichnung, sondern auch mehr Eigenfarbe,
ein hellerer Rand und ein kräftigerer Innenglanz — echtes Glas wird mit der
Dicke milchiger, nicht bloss unschärfer.

| Nr | Name | Farbwelt | Glasrezept |
|---|---|---|---|
| 43 | Sonnenglas | Abendrot (die Vorlage) | Weichzeichnung 26 px · Eigenfarbe 13 % · Rand 24 % |
| 43a | Milchglas | dasselbe Abendrot | 64 px · 26 % · Rand 44 % — das Bild dahinter verschwimmt fast ganz |
| 43b | Blaue Stunde | kühle Dämmerung | 9 px · 6 % · Rand 14 % — kaum mehr als eine Tönung |
| 43c | Morgenmilch | blasser kalter Morgen | 86 px · 46 % · Rand 72 %, **dunkle Schrift** |
| 43d | Gewitter | Sturmviolett, grüner Akzent | 22 px · 11 % · Kante 78 % · Glanzlage 34 % — spiegelt statt zu streuen |
| 43e | Neonnacht | Magenta/Violett, cyan Akzent | 34 px · **cyan eingefärbtes Glas** · Sättigung ×1,5 |

Zwei Erkenntnisse aus der Reihe, die beim Portieren zählen:

- **Ab etwa 40 px Weichzeichnung trägt weisse Schrift auf hellem Grund nicht
  mehr.** 43c musste deshalb auf dunkle Schrift wechseln — eine Glasdicke ist
  also keine reine Geschmacksfrage, sie zieht die Schriftfarbe mit.
- **Eingefärbtes Glas (43e) ersetzt den Akzent nicht, es verstärkt ihn.** Der
  cyanfarbene Ton im Glas und die cyanfarbene Zufallstaste sind dieselbe
  Entscheidung, nicht zwei.

Alle sechs liegen in einer Datei (`d43.py`); `FASSUNGEN` hält Himmel, Horizont,
Glasrezept, Schrift, Akzent und Coverfarben je Fassung. Eine siebte anzulegen
ist ein Eintrag in diesem Wörterbuch, sonst nichts.

**Ein Foto ist nicht verwertet:** 23.56.39 ist ein 15 KB grosses Vorschaubild,
auf dem nur eine Ecke mit einem „A" zu erkennen ist. Daraus lässt sich keine
Bildsprache ableiten.

Die Übertragung folgt in jedem Fall demselben Gedanken: **nicht das Foto
nachzeichnen, sondern seine Bausprache übernehmen** und den ganzen Spieler
daraus bauen. Bei 39 heisst das, dass der Schalter nicht *neben* der Wiedergabe
sitzt, sondern *die* Wiedergabe ist; bei 46, dass der Fortschritt ein gezogener
Strich ist und kein Balken.

39 und 46 gehen auf Grafiken ohne jede Bedienung zurück; dort ist mehr erfunden
als übertragen. 43 und 44 waren dagegen schon fast fertige Oberflächen — die
sind eher Port als Entwurf.

## Verworfen

Vier weitere Entwürfe sind auf Wunsch des Eigentümers wieder entfernt worden:
**40 Neonschild**, **41 Sonntagsblatt**, **42 Druckgrafik** und
**45 Kassettenhaufen**. Anders als bei den gestrichenen Blättern des Pakets sind
hier auch die Dateien weg — sie waren Entwürfe, keine Lieferung. In der
Git-Historie stehen sie im Commit „Acht Spieler aus den Fotos in player2".

## Neu bauen

```bash
cd design/entwuerfe/src
python3 baualle.py          # schreibt alle 18 Dateien nach ../html/
```

`werkzeug.py` hält, was alle vier teilen: das eine Beispielalbum, die Zeichen
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

Diese vier sind **Entwürfe zum Ansehen**, noch kein Layout in `player.html`.
Ob und welche davon portiert werden, steht in `design/AUSWAHL.md` — dort sind
sie bisher nicht eingetragen, weil die Auswahl beim Eigentümer liegt.
