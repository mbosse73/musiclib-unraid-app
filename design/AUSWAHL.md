# Auswahl für Etappe 5

Das Design-Paket lieferte 22 Konzepte. Der Eigentümer hat daraus **12 ausgewählt;
die anderen zehn sind samt Dateien entfernt**. Diese Datei hält den Stand fest,
damit später niemand raten muss, warum ein Blatt in der Historie steht, aber in
`player.html` nie auftaucht.

Gestrichen heißt hier also **gelöscht**: unter `design/html/` und
`design/previews/` liegen nur noch die zwölf, die gebaut werden. Was weg ist,
ist nicht verloren — es steht vollständig in der Git-Historie und lässt sich mit
einem `git show` zurückholen. Von **18 Akai 747** ist zusätzlich das Hochformat
weg; das Konzept selbst bleibt.

## Wird gebaut

| Familie | Entwürfe |
|---|---|
| Kassette | 22 EA Archive · 24 Mix Tape Klar · 25 Audio Tape C90 · 26 True Sound · 27 Stereo 60 |
| Gerät | 18 Akai 747 |
| Poster | 34 Retro Party · 35 Music Sounds Better · 36 Song-Poster schwarz · 37 Song-Poster weiß · 38 World Music Day |
| Einzelstücke | 31 Vinyl Rote Tasten |

**35 Music Sounds Better** ist der Pilot: das schlichteste Blatt, an dem sich das
Portierungsrezept festzurren lässt, bevor die aufwendigeren folgen.

## Entfernt

| | | |
|---|---|---|
| 17 Sony Bandmaschine | 19 On-Air-Leuchtkasten | 20 Philips Radio |
| 21 Yamaha Tuner | 23 Magnetola | 28 Rewind Boombox |
| 29 Rewind Deck | 30 iPod Weiß | 32 Seattle Skeuo |
| 33 Glass Musiknote | | |

Die ersten neun in einem Zug, 33 schon vorher (dort waren zwei Fassungen zur
Auswahl offen, und die Frage hat sich mit dem Löschen erledigt). Mit ihnen sind
`d17` bis `d32` aus `design/src/designs3.py` verschwunden — der Generator baut
nur noch, was es noch gibt.

Damit bleibt von der Familie *Gerät* nur ein Blatt übrig — und das nur im
Querformat. Die Gruppierung nach Familien im Einstellungsdialog lohnt sich
dadurch weniger als geplant; bei 12 Einträgen plus den 17 vorhandenen Layouts
entscheidet sich das erst beim Bauen.

## Wird angepasst gebaut

Drei Blätter kommen nicht so in die App, wie sie geliefert wurden. Die
angepassten Fassungen liegen unter `design/varianten/`, die Begründung je
Änderung steht in `design/varianten/LIESMICH.md`.

| Entwurf | Änderung |
|---|---|
| 31 Vinyl Rote Tasten | PC: die drei roten Tasten mittig unter die Fortschrittsleiste. iPhone unverändert. |
| 36 Song-Poster schwarz | Beide: QR-Code raus. PC: Tastenreihe unter der Fortschrittsleiste zentriert. |
| 37 Song-Poster weiß | Beide: QR-Code raus. PC: Tastenreihe unter der Fortschrittsleiste zentriert. |

## Am Paket selbst geändert

Fünf Blätter sind nicht abgewandelt, sondern **im Paket geändert** worden — die
Dateien unter `design/html/` und `design/previews/` sind die neue Fassung, die
alte steht nur noch in der Git-Historie. Der Unterschied zu den Abwandlungen
oben ist Absicht: dort steht eine Entscheidung noch offen, hier nicht.

| Entwurf | Änderung |
|---|---|
| 18 Akai 747 | AKAI-Schild weg; Zählwerk und VU-Paar stehen mittig auf der rechten Hälfte und sind deutlich grösser. Das Hochformat ist entfallen. |
| 35 Music Sounds Better | Der Typo-Kasten über der Platte ist weg; die Platte steht dafür links (PC) bzw. im oberen Bereich (iPhone) zentriert. |
| 36 Song-Poster schwarz | iPhone: das Plakat füllt das Blatt, der schwarze Rahmen ist entfallen. |
| 37 Song-Poster weiß | iPhone: das Plakat füllt das Blatt, der weisse Rahmen ist der Blattrand. |
| 38 World Music Day | „World Music Day" steht in beiden Fassungen mittig im blauen Feld; auf dem iPhone steht auch das Radio mittig im orangen. |

## Eigene Entwürfe aus den Ordnern `player2/` und `player3/`

Aus den Fotos in `player2/` sind vier Spieler entstanden — 39 Kippschalter,
43 Sonnenglas, 44 Gerätezeile, 46 Malerblatt. Vier weitere (40 Neonschild,
41 Sonntagsblatt, 42 Druckgrafik, 45 Kassettenhaufen) sind auf Wunsch wieder
verworfen und samt Dateien entfernt. Von **43 gibt es drei Fassungen** (gleiche
Farbe, unterschiedliche Glasdicke und -oberfläche, siehe LIESMICH); welche davon
gilt, ist offen.

Aus den fünfzehn Fotos in `player3/` sind zunächst dreizehn weitere entstanden;
nach der Durchsicht durch den Eigentümer sind acht davon geblieben —
48 Siebdruck, 50 Fallblatt, 51 Tastenfeld, 53 Fokusmodul, 56 Punktring,
57 Mischpult, 58 Zeigerfront, 59 Skalenblech (nur PC). 58 fasst zwei Fotos
desselben Geräts zusammen, wie es 44 schon vormacht.

Alle zwölf liegen unter
`design/entwuerfe/`, halten dieselben Regeln ein wie das Paket und sind bisher
**nicht** Teil der Auswahl oben: welche davon gebaut werden, ist noch nicht
entschieden. Begründung je Entwurf in `design/entwuerfe/LIESMICH.md`.

## Was das für die Bibliothek heißt

Jeder Entwurf im Paket benennt, wo Sammlung und Suche hinkommen (`SPEC.md`,
Zeile *Bibliothek* je Blatt). Dieser Zugang ist keine Zutat, sondern Bedingung:
ein Layout ohne ihn wäre in `player.html` unvollständig und würde
`test_player_library_and_search_are_reachable_in_every_layout` reißen.
