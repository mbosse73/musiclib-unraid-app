# SPEC — Entwurf für Entwurf

22 Konzepte, je eine iPhone- und eine PC-Variante. Bühnengröße: iPhone 1080 × 2340, PC 1600 × 1000.
Alle Entwürfe enthalten Transport (Zurück/Play/Pause/Weiter), Fortschritt mit Zeiten und einen Bibliotheks-Zugang.

| Nr. | Konzept | Charakter | Bibliotheks-Zugang | Besondere Bausteine |
|---|---|---|---|---|
| 17 | `Sony-Bandmaschine` | Bandmaschine, Nussbaum + Silberpanel, cremefarbene Tasten, zwei VU-Meter | Eject-Taste (LIBRARY) in der Tastenreihe | Bandspulen, VU-Meter, Zählwerk, Titelliste |
| 18 | `Akai-747` | Silber-weisse Front, rote LED-Zeitanzeige, symmetrische Spulen, Holzwangen | Eject-Taste (LIBRARY) in der Tastenreihe | Bandspulen, LED-Zähler, VU-Paar, Lampen in Tasten |
| 19 | `On-Air-Leuchtkasten` | Leuchtkasten auf Backsteinwand, rote Lettern auf warmem Milchglas | Eigener Button LIBRARY als schwarze Platte | Leuchtkasten, Sendungsliste, Wellenform |
| 20 | `Philips-Radio` | Mahagoni-Gehäuse, blaues Bedienfeld, Rattan-Gitter, Skalenanzeige | Eigener Button ARCHIV im blauen Panel | Tuning-Skala, Riffelknopf, Lautsprechergitter |
| 21 | `Yamaha-Tuner` | Dunkles Holz, weisse Front, drei grosse Drehknöpfe, kleines VU | Eigener Button LIBRARY in der Tastenreihe | Skala, VU, drei Drehknöpfe, Titelliste |
| 22 | `EA-Archive` | Technisches Archivblatt, Spec-Raster, orange Akzente, Kassette als Objekt | ARCHIVE als fünftes Feld der Tastenleiste | Spec-Raster, Kassette, Rahmentabelle |
| 23 | `Magnetola` | Pinke Kassette im dunklen Gehäuse, beschriftete Tastenleiste | Eigene Taste LIBRARY in der zweiten Tastenreihe | Kassette, LCD-Band, beschriftete Tasten |
| 24 | `Mix-Tape-Klar` | Transparente Kassette auf Weiss, handschriftliche Beschriftung | Runder Button mit Bibliotheks-Icon neben Weiter | Klare Kassette, handschriftliche Liste, runde Tasten |
| 25 | `Audio-Tape-C90` | Creme mit rot-orange-gelben Streifen, Illustration statt Foto | Oranger Block LIBRARY am Ende der Tastenleiste | Kassette mit Streifen, Balkentasten, Titelliste |
| 26 | `True-Sound` | Beige Kassette mit Regenbogenstreifen, Schreibschrift auf Dunkel | Pille LIBRARY in der Tastenreihe | Kassette, farbcodierte Titelliste, Pillen-Tasten |
| 27 | `Stereo-60` | Blaue Vektor-Kassette, rot-gelber Streifen, klare Rahmen | Umrandeter Button LIBRARY | Kassette, gerahmte Liste, Rahmen-Tasten |
| 28 | `Rewind-Boombox` | Schwarze Boombox, zwei orange VU, gelbe REC-Taste, runde Lautsprecher | STOP/EJECT-Taste der Gerätereihe | Lautsprecher, orange VU, Kassettenfenster, Gummitasten |
| 29 | `Rewind-Deck` | Nahaufnahme des Decks, orange VU über Kassettenfenster | STOP/EJECT-Taste der Gerätereihe | VU-Paar, Kassettenfenster, Kapitel-Liste |
| 30 | `iPod-Weiss` | Weisse App-Optik, Punktraster-Gitter, Klickrad, orange Akzente | Bibliotheks-Icon im unteren Segment des Klickrads | Punktraster, Klickrad, Bibliotheksliste |
| 31 | `Vinyl-Rote-Tasten` | Schallplatte auf Creme, rote Rundtasten, Slider mit Sprechblase | Eigene Kachel mit Bibliotheks-Icon oben rechts | Schallplatte, Slider mit Tooltip, Rundtasten |
| 32 | `Seattle-Skeuo` | Schwarze Hardware-Optik, Kassette mit weissen Naben, grünes LCD | Materialtaste mit Bibliotheks-Icon | Kassette, LCD-Titelband, Metalltasten |
| 33 | `Glass-Musiknote` | Milchglas-Karte auf Dunkel, orange-rote Farbwolken | Glaskreis mit Bibliotheks-Icon oben rechts | Glaskarte, Farbwolken, Kreis-Tasten |
| 34 | `Retro-Party` | 70er-Poster, Strahlen in Petrol/Orange/Creme, Schallplatte, Rahmen | Rahmen-Button CRATE | Strahlen-Hintergrund, Schallplatte, Stempel, Rahmen-Tasten |
| 35 | `Music-Sounds-Better` | Minimales weisses Poster, gesperrte Typo im Kasten, Schallplatte | Runder Button mit Bibliotheks-Icon | Typo-Kasten, Schallplatte, Kreis-Tasten |
| 36 | `Song-Poster-Schwarz` | Gerahmtes Poster an der Wand, Spiraltext aus Albumtiteln, QR | Runder Button mit Bibliotheks-Icon neben Repeat | Spiral-Schallplatte, Tonarm, QR, Kreis-Tasten |
| 37 | `Song-Poster-Weiss` | Weiss gerahmtes Poster, wärmerer Ton, Spiraltext aus Albumtiteln | Button SAMMLUNG rechts in der Tastenreihe | Spiral-Schallplatte, Tonarm, QR, beschriftete Tasten |
| 38 | `World-Music-Day` | Festival-Plakat, Navy/Petrol/Orange, Boombox-Illustration, Blitze | Button LINE-UP am Ende der Tastenleiste | Boombox-Illustration, Blitze, Stern, Programmliste |

---

## Farbwerte je Entwurf

Vollständig maschinenlesbar in `tokens.json`. Kurzfassung:

| Nr. | Konzept | Farben |
|---|---|---|
| 17 | `Sony-Bandmaschine` | holz `#5a3d24` · panel `#c8c8c4` · taste `#f3efe2` · akzent `#8a5a2a` · lcd `#e8e2cc` |
| 18 | `Akai-747` | panel `#e6e6e3` · led `#ff2a12` · holz `#5c3a20` · akzent `#d63a1e` · taste `#fbfbfa` |
| 19 | `On-Air-Leuchtkasten` | wand `#cfcac3` · kasten `#1e1e1c` · licht `#f3e2b8` · schrift `#d8342a` |
| 20 | `Philips-Radio` | gehaeuse `#7d2f26` · panel `#3c5c78` · gitter `#e6dcc0` · skala `#e8e2d0` · akzent `#d8452e` |
| 21 | `Yamaha-Tuner` | holz `#4a2f1e` · front `#f2f1ec` · schrift `#3a3a36` · akzent `#c9422e` |
| 22 | `EA-Archive` | papier `#eeece5` · tinte `#191917` · akzent `#d4602a` · linie `#c8c5bc` |
| 23 | `Magnetola` | gehaeuse `#3a3a3c` · akzent `#e8397e` · panel `#d8d6d0` · gelb `#f0c400` |
| 24 | `Mix-Tape-Klar` | grund `#f7f7f5` · tinte `#1c1c1a` · akzent `#e03127` · grau `#a5a5a0` |
| 25 | `Audio-Tape-C90` | grund `#f4efe2` · creme `#e8dfc4` · rot `#c3402a` · orange `#e0752a` · gelb `#e8b93e` |
| 26 | `True-Sound` | grund `#2e2f31` · kassette `#d8cfa8` · schrift `#2f7bd0` · streifen `#5aa832` |
| 27 | `Stereo-60` | grund `#e8eaf2` · blau `#3a4d9e` · rot `#d8412e` · gelb `#e8bb3a` |
| 28 | `Rewind-Boombox` | gehaeuse `#141414` · vu `#f5a623` · gelb `#f0d000` · grau `#8e8e8a` |
| 29 | `Rewind-Deck` | gehaeuse `#0f0f0f` · vu `#f5a623` · gelb `#f0d000` · akzent `#f5a623` |
| 30 | `iPod-Weiss` | grund `#f2f0ed` · karte `#faf9f7` · tinte `#3a3a38` · akzent `#e8681a` |
| 31 | `Vinyl-Rote-Tasten` | grund `#f2ede2` · tinte `#2e2b26` · rot `#c9403c` · linie `#ddd6c8` |
| 32 | `Seattle-Skeuo` | gehaeuse `#1a1a1e` · lcd `#0d1a16` · gruen `#7fe8b0` · stahl `#5a5a60` |
| 33 | `Glass-Musiknote` | grund `#141416` · wolke1 `#f2703c` · wolke2 `#e0455f` · glas `rgba(255,255,255,.10)` |
| 34 | `Retro-Party` | grund `#e8e0c8` · petrol `#3d8a8a` · orange `#e0672a` · creme `#f2e9cf` · tinte `#2b2620` |
| 35 | `Music-Sounds-Better` | grund `#ffffff` · tinte `#141414` · rot `#c0272d` · linie `#e6e6e3` |
| 36 | `Song-Poster-Schwarz` | wand `#e4e2de` · rahmen `#141414` · papier `#ffffff` · label `#e0453a` |
| 37 | `Song-Poster-Weiss` | wand `#e6e2db` · rahmen `#fbfbf9` · papier `#ffffff` · akzent `#c9422e` |
| 38 | `World-Music-Day` | navy `#1e2a4a` · petrol `#4aa3c4` · orange `#e8622b` · creme `#faf4e6` · gelb `#f0b93a` |

---

## Hinweise zu einzelnen Entwürfen

**17, 18, 20, 28, 29** sind Geräte-Nachbildungen mit Bedienpanel. Der Bibliotheks-Zugang
ist dort bewusst als **Eject-Taste** in die Tastenreihe integriert, nicht als Fremdkörper.

**36 und 37** zeigen eine Schallplatte, deren Rille mit Text gefüllt ist. Dort stehen
**Albumtitel** — bewusst keine Songtexte, da Liedtexte urheberrechtlich geschützt sind.
Diese Entscheidung bitte beibehalten; als Datenquelle eignen sich Albumtitel, Interpreten
oder frei gewählte Texte der Nutzerin.

**29 und 32** sind sehr dunkel gehalten. Beschriftungen, die tatsächlich gelesen werden
müssen, brauchen bei der Umsetzung mehr Kontrast als im Entwurf (siehe Brief, Abschnitt 5).

**30** ist der strukturell vollständigste Entwurf (Bibliotheksliste + Now-Playing +
Steuerkreuz) und eignet sich gut als Pilot für die Zerlegung in Komponenten.