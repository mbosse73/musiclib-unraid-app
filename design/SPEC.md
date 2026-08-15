# SPEC — Entwurf für Entwurf

12 Konzepte, je eine iPhone- und eine PC-Variante — ausser **18**, das es nur als PC-Variante
gibt. Bühnengröße: iPhone 1080 × 2340, PC 1600 × 1000.

Geliefert waren 22. Die zehn, die der Eigentümer nicht bauen will, sind samt Dateien
entfernt (17, 19, 20, 21, 23, 28, 29, 30, 32, 33) — sie stehen in der Git-Historie.
Alle Entwürfe enthalten Transport (Zurück/Play/Pause/Weiter), Fortschritt mit Zeiten und einen Bibliotheks-Zugang.

| Nr. | Konzept | Charakter | Bibliotheks-Zugang | Besondere Bausteine |
|---|---|---|---|---|
| 18 | `Akai-747` | Silber-weisse Front, mittig das rote LED-Zählwerk über dem grossen VU-Paar, symmetrische Spulen, Holzwangen (**nur PC**) | Eject-Taste (LIBRARY) in der Tastenreihe | Bandspulen, LED-Zähler, VU-Paar, Lampen in Tasten |
| 22 | `EA-Archive` | Technisches Archivblatt, Spec-Raster, orange Akzente, Kassette als Objekt | ARCHIVE als fünftes Feld der Tastenleiste | Spec-Raster, Kassette, Rahmentabelle |
| 24 | `Mix-Tape-Klar` | Transparente Kassette auf Weiss, handschriftliche Beschriftung | Runder Button mit Bibliotheks-Icon neben Weiter | Klare Kassette, handschriftliche Liste, runde Tasten |
| 25 | `Audio-Tape-C90` | Creme mit rot-orange-gelben Streifen, Illustration statt Foto | Oranger Block LIBRARY am Ende der Tastenleiste | Kassette mit Streifen, Balkentasten, Titelliste |
| 26 | `True-Sound` | Beige Kassette mit Regenbogenstreifen, Schreibschrift auf Dunkel | Pille LIBRARY in der Tastenreihe | Kassette, farbcodierte Titelliste, Pillen-Tasten |
| 27 | `Stereo-60` | Blaue Vektor-Kassette, rot-gelber Streifen, klare Rahmen | Umrandeter Button LIBRARY | Kassette, gerahmte Liste, Rahmen-Tasten |
| 31 | `Vinyl-Rote-Tasten` | Schallplatte auf Creme, rote Rundtasten, Slider mit Sprechblase | Eigene Kachel mit Bibliotheks-Icon oben rechts | Schallplatte, Slider mit Tooltip, Rundtasten |
| 34 | `Retro-Party` | 70er-Poster, Strahlen in Petrol/Orange/Creme, Schallplatte, Rahmen | Rahmen-Button CRATE | Strahlen-Hintergrund, Schallplatte, Stempel, Rahmen-Tasten |
| 35 | `Music-Sounds-Better` | Minimales weisses Poster, die Schallplatte allein — links (PC) bzw. im oberen Bereich (iPhone) zentriert | Runder Button mit Bibliotheks-Icon | Schallplatte, Titelliste, Kreis-Tasten |
| 36 | `Song-Poster-Schwarz` | PC: gerahmtes Poster an der Wand. iPhone: das Plakat füllt das Blatt, der schwarze Rahmen entfällt. Spiraltext aus Albumtiteln, QR | Runder Button mit Bibliotheks-Icon neben Repeat | Spiral-Schallplatte, Tonarm, QR, Kreis-Tasten |
| 37 | `Song-Poster-Weiss` | Weiss gerahmtes Poster, wärmerer Ton, Spiraltext aus Albumtiteln. iPhone: das Plakat füllt das Blatt, der weisse Rahmen wird zum Blattrand | Button SAMMLUNG rechts in der Tastenreihe | Spiral-Schallplatte, Tonarm, QR, beschriftete Tasten |
| 38 | `World-Music-Day` | Festival-Plakat, Navy/Petrol/Orange, Boombox-Illustration, Blitze | Button LINE-UP am Ende der Tastenleiste | Boombox-Illustration, Blitze, Stern, Programmliste |

---

## Farbwerte je Entwurf

Vollständig maschinenlesbar in `tokens.json`. Kurzfassung:

| Nr. | Konzept | Farben |
|---|---|---|
| 18 | `Akai-747` | panel `#e6e6e3` · led `#ff2a12` · holz `#5c3a20` · akzent `#d63a1e` · taste `#fbfbfa` |
| 22 | `EA-Archive` | papier `#eeece5` · tinte `#191917` · akzent `#d4602a` · linie `#c8c5bc` |
| 24 | `Mix-Tape-Klar` | grund `#f7f7f5` · tinte `#1c1c1a` · akzent `#e03127` · grau `#a5a5a0` |
| 25 | `Audio-Tape-C90` | grund `#f4efe2` · creme `#e8dfc4` · rot `#c3402a` · orange `#e0752a` · gelb `#e8b93e` |
| 26 | `True-Sound` | grund `#2e2f31` · kassette `#d8cfa8` · schrift `#2f7bd0` · streifen `#5aa832` |
| 27 | `Stereo-60` | grund `#e8eaf2` · blau `#3a4d9e` · rot `#d8412e` · gelb `#e8bb3a` |
| 31 | `Vinyl-Rote-Tasten` | grund `#f2ede2` · tinte `#2e2b26` · rot `#c9403c` · linie `#ddd6c8` |
| 34 | `Retro-Party` | grund `#e8e0c8` · petrol `#3d8a8a` · orange `#e0672a` · creme `#f2e9cf` · tinte `#2b2620` |
| 35 | `Music-Sounds-Better` | grund `#ffffff` · tinte `#141414` · rot `#c0272d` · linie `#e6e6e3` |
| 36 | `Song-Poster-Schwarz` | wand `#e4e2de` · rahmen `#141414` · papier `#ffffff` · label `#e0453a` |
| 37 | `Song-Poster-Weiss` | wand `#e6e2db` · rahmen `#fbfbf9` · papier `#ffffff` · akzent `#c9422e` |
| 38 | `World-Music-Day` | navy `#1e2a4a` · petrol `#4aa3c4` · orange `#e8622b` · creme `#faf4e6` · gelb `#f0b93a` |

---

## Hinweise zu einzelnen Entwürfen

**18** ist die einzige verbliebene Geräte-Nachbildung mit Bedienpanel. Der Bibliotheks-Zugang
ist dort bewusst als **Eject-Taste** in die Tastenreihe integriert, nicht als Fremdkörper.

**36 und 37** zeigen eine Schallplatte, deren Rille mit Text gefüllt ist. Dort stehen
**Albumtitel** — bewusst keine Songtexte, da Liedtexte urheberrechtlich geschützt sind.
Diese Entscheidung bitte beibehalten; als Datenquelle eignen sich Albumtitel, Interpreten
oder frei gewählte Texte der Nutzerin.

**35, 36, 37, 38 und 18** sind nach der Lieferung auf Wunsch des Eigentümers geändert worden:
bei **35** ist der Typo-Kasten über der Schallplatte weg und die Platte dafür zentriert; bei
**36 und 37** füllt das Plakat auf dem Telefon das ganze Blatt; bei **38** stehen Titel und
Radio jeweils mittig in ihrem Farbfeld; bei **18** ist der AKAI-Schriftzug weg, Zählwerk und
VU-Paar stehen mittig auf der rechten Hälfte und sind grösser. **33** ist ganz entfallen, ebenso die neun nicht gewählten Blätter.

**35** ist der Pilot für die Zerlegung in Komponenten — das schlichteste der zwölf Blätter
(siehe `AUSWAHL.md`).