# Abwandlungen der gelieferten Entwürfe

Hier liegen Fassungen, die von einem Blatt aus `design/html/` abgeleitet sind.
Das gelieferte Paket selbst bleibt unangetastet — es ist die Referenz, gegen die
sich vergleichen lässt. Was für Etappe 5 gilt, steht in `design/AUSWAHL.md`.

Namensschema wie im Paket, mit einem Buchstaben hinter der Nummer:
`fotoNNx_Konzeptname_plattform.html`.

Alle Dateien hier sind **aus dem Original erzeugt, nicht von Hand nachgebaut** —
jede unterscheidet sich vom gelieferten Blatt in wenigen Zeilen, damit ein
`diff` gegen `design/html/` die Änderung vollständig zeigt.

## 31 Vinyl Rote Tasten — nur PC

Die drei roten Tasten standen linksbündig unter einer Fortschrittsleiste, die
über die ganze Spalte läuft. `foto31a_…-Zentriert_pc.html` setzt
`justify-content:center` auf die Tastenreihe; sonst ändert sich nichts.

Das iPhone-Blatt ist unverändert und liegt deshalb nicht hier — dort gilt
weiterhin `design/html/foto31_Vinyl-Rote-Tasten_iphone.html`.

## 33 Glass Musiknote — zwei Fassungen zur Auswahl

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

## 36 / 37 Song-Poster schwarz und weiß — beide Plattformen

Zwei Änderungen, je Blatt:

1. **QR-Code entfernt.** Er saß im Poster rechts neben dem Albumtitel (ein SVG
   aus 37 Rechtecken). Ersatzlos gestrichen; der Titelblock rückt nach.
2. **Nur PC: die Tastenreihe unter der Fortschrittsleiste zentriert.** Die
   Transporttasten standen linksbündig, der Bibliotheksknopf per
   `margin-left:auto` ganz rechts. Jetzt steht die Reihe auf
   `justify-content:center`, und der Bibliotheksknopf hält seinen Platz am
   rechten Rand über `position:absolute` — er bleibt also erreichbar, ohne die
   Mitte zu verschieben.

Die iPhone-Blätter bekommen nur Änderung 1; ihre Tastenreihe war schon mittig.
