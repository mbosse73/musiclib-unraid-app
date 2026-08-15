# Abwandlungen der gelieferten Entwürfe

Hier liegen Fassungen, die von einem Blatt aus `design/html/` abgeleitet sind.
Das gelieferte Paket selbst bleibt unangetastet — es ist die Referenz, gegen die
sich vergleichen lässt. Was für Etappe 5 gilt, steht in `design/AUSWAHL.md`.

Namensschema wie im Paket, mit einem Buchstaben hinter der Nummer:
`fotoNNx_Konzeptname_plattform.html`.

Alle Dateien hier sind **aus dem Original erzeugt, nicht von Hand nachgebaut** —
jede unterscheidet sich vom gelieferten Blatt in wenigen Zeilen, damit ein
`diff` gegen `design/html/` die Änderung vollständig zeigt. Für 36 und 37
erledigt das `_ableiten.py` (`python3 _ableiten.py`): es liest die aktuellen
Blätter aus `../html/` und wendet die beiden Handgriffe darauf an. Wer am
Original etwas ändert, lässt danach dieses Skript laufen — sonst zeigt der
`diff` plötzlich mehr als die gewollte Abweichung.

## 31 Vinyl Rote Tasten — nur PC

Die drei roten Tasten standen linksbündig unter einer Fortschrittsleiste, die
über die ganze Spalte läuft. `foto31a_…-Zentriert_pc.html` setzt
`justify-content:center` auf die Tastenreihe; sonst ändert sich nichts.

Das iPhone-Blatt ist unverändert und liegt deshalb nicht hier — dort gilt
weiterhin `design/html/foto31_Vinyl-Rote-Tasten_iphone.html`.

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

Seit die beiden Telefon-Blätter das ganze Blatt füllen (kein Rahmen bei 36, der
Rahmen als Blattrand bei 37), sitzt der QR-Code dort nicht mehr neben dem
Albumtitel im Papier, sondern neben dem Titel auf dem Bildschirm — die Änderung
bleibt aber dieselbe: der Block fällt ersatzlos weg, der Titel rückt nach.
