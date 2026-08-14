# Abwandlungen der gelieferten Entwürfe

Hier liegen Fassungen, die von einem Blatt aus `design/html/` abgeleitet sind.
Das gelieferte Paket selbst bleibt unangetastet — es ist die Referenz, gegen die
sich vergleichen lässt.

Namensschema wie im Paket, mit einem Buchstaben hinter der Nummer:
`fotoNNx_Konzeptname_plattform.html`.

## 33 Glass Musiknote

Im Original liegen drei Farbscheiben (`linear-gradient(150deg,#f2703c,#e0455f)`)
mit nur 2 px Weichzeichnung hinter der Milchglaskarte. Auf beiden Plattformen
sitzt mindestens eine davon genau unter der Titelliste und den Zeitangaben —
dort verliert die weiße Schrift ihren Halt.

| Datei | Was anders ist |
|---|---|
| `foto33a_Glass-Musiknote-Ohne_*` | Die drei Scheiben sind ersatzlos entfernt. Übrig bleibt die Milchglaskarte auf Anthrazit — vollständig lesbar, aber ohne jede Farbe. |
| `foto33b_Glass-Musiknote-Dezent_*` | Gleiche Lage, gleiche Farbe, gleiche Größe. Nur `filter:blur(2px)` wird zu `filter:blur(90px);opacity:.72` — aus der Scheibe wird ein Schein. |

Für 33b wurden drei Stärken gegeneinander angesehen: 90 px/72 %, 100 px/62 %
und 120 px/55 %. Die beiden weicheren sind zwar am besten lesbar, nehmen dem
Entwurf aber fast die ganze Farbe; 90 px/72 % hält den warmen Ton und lässt die
Zeiten trotzdem klar stehen.

Erzeugt aus dem Original, nicht von Hand nachgebaut — die Dateien
unterscheiden sich vom gelieferten Blatt in genau einer Zeile.
