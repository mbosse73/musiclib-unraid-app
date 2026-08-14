# Auswahl für Etappe 5

Das Design-Paket liefert 22 Konzepte. Der Eigentümer hat daraus ausgewählt: **13
werden gebaut, 9 fallen weg**. Diese Datei hält den Stand fest, damit später
niemand raten muss, warum ein Blatt in `design/html/` liegt, aber in
`player.html` nie auftaucht.

Gestrichen heißt **nicht bauen**, nicht *gelöscht*: die gelieferten Dateien
bleiben vollständig unter `design/html/` liegen.

## Wird gebaut

| Familie | Entwürfe |
|---|---|
| Kassette | 22 EA Archive · 24 Mix Tape Klar · 25 Audio Tape C90 · 26 True Sound · 27 Stereo 60 |
| Gerät | 18 Akai 747 |
| Poster | 34 Retro Party · 35 Music Sounds Better · 36 Song-Poster schwarz · 37 Song-Poster weiß · 38 World Music Day |
| Einzelstücke | 31 Vinyl Rote Tasten · 33 Glass Musiknote |

**35 Music Sounds Better** ist der Pilot: das schlichteste Blatt, an dem sich das
Portierungsrezept festzurren lässt, bevor die aufwendigeren folgen.

## Fällt weg

| | | |
|---|---|---|
| 17 Sony Bandmaschine | 19 On-Air-Leuchtkasten | 20 Philips Radio |
| 21 Yamaha Tuner | 23 Magnetola | 28 Rewind Boombox |
| 29 Rewind Deck | 30 iPod Weiß | 32 Seattle Skeuo |

Damit bleibt von der Familie *Gerät* nur ein Blatt übrig. Die Gruppierung nach
Familien im Einstellungsdialog lohnt sich dadurch weniger als geplant — bei 13
Einträgen plus den 17 vorhandenen Layouts entscheidet sich das erst beim Bauen.

## Wird angepasst gebaut

Drei Blätter kommen nicht so in die App, wie sie geliefert wurden. Die
angepassten Fassungen liegen unter `design/varianten/`, die Begründung je
Änderung steht in `design/varianten/LIESMICH.md`.

| Entwurf | Änderung |
|---|---|
| 31 Vinyl Rote Tasten | PC: die drei roten Tasten mittig unter die Fortschrittsleiste. iPhone unverändert. |
| 36 Song-Poster schwarz | Beide: QR-Code raus. PC: Tastenreihe unter der Fortschrittsleiste zentriert. |
| 37 Song-Poster weiß | Beide: QR-Code raus. PC: Tastenreihe unter der Fortschrittsleiste zentriert. |

## Offen: 33 Glass Musiknote

Für 33 liegen **zwei Fassungen zur Auswahl** vor, weil die Farbscheiben im
Original unter der Titelliste und den Zeiten sitzen und die Lesbarkeit
wegbricht:

- **33a — ohne Kreise**: voll lesbar, aber der Entwurf verliert seine Farbe.
- **33b — dezente Kreise**: Scheibe wird zu weichem Schein, warmer Ton bleibt.

Welche der beiden gebaut wird, ist noch nicht entschieden. Solange das offen
ist, wird 33 nicht portiert.

## Zweiter Satz: vier Entwürfe aus dem Ordner `player2/`

Aus den Fotos in `player2/` sind vier Spieler entstanden — 39 Kippschalter,
43 Sonnenglas, 44 Gerätezeile, 46 Malerblatt. Vier weitere (40 Neonschild,
41 Sonntagsblatt, 42 Druckgrafik, 45 Kassettenhaufen) sind auf Wunsch wieder
verworfen und samt Dateien entfernt. Von **43 gibt es sieben Fassungen** (gleiche
Farbe, unterschiedliche Glasdicke und -oberfläche, siehe LIESMICH); welche davon
gilt, ist offen. Die verbliebenen
liegen unter
`design/entwuerfe/`, halten dieselben Regeln ein wie das Paket und sind bisher
**nicht** Teil der Auswahl oben: welche davon gebaut werden, ist noch nicht
entschieden. Begründung je Entwurf in `design/entwuerfe/LIESMICH.md`.

## Was das für die Bibliothek heißt

Jeder Entwurf im Paket benennt, wo Sammlung und Suche hinkommen (`SPEC.md`,
Zeile *Bibliothek* je Blatt). Dieser Zugang ist keine Zutat, sondern Bedingung:
ein Layout ohne ihn wäre in `player.html` unvollständig und würde
`test_player_library_and_search_are_reachable_in_every_layout` reißen.
