# Bauanleitung je Konzept

Wozu: das Konzeptregister zeigt, *wie* ein Konzept aussieht. Diese Datei sagt,
*wie es sich bedient* — und das steht sonst nirgends. Vier Angaben je Konzept:

| | |
|---|---|
| **Spulen** | Welche Fläche die Spulfläche ist. In `player.html` trägt genau eine `data-spulen`, und `test_player_every_layout_offers_transport_seeking_and_settings` verlangt sie. |
| **Zustände** | Woran man sieht, was läuft, was gelaufen ist, was gedrückt wird. |
| **Bewegung** | Was sich bewegt. **Hausregel: sparsam.** Bewegt wird, was den Stand zeigt — kein Leerlauf-Animieren. Das ist der Charakter der App: die acht portierten Themen hatten in ihrer Vorlage null `@keyframes`. |
| **Bibliothek** | Wo Sammlung und Suche sitzen. Pflicht in jedem Layout, sonst reisst `test_player_library_and_search_are_reachable_in_every_layout`. |

**Drei Verlässlichkeitsgrade.** Bei den gebauten Konzepten ist das eine
Beschreibung, abgelesen aus dem Code. Bei den gezeichneten Blättern ist es aus
dem Blatt übernommen — die sind bedienbar und beantworten die Frage selbst.
Bei den Paket-Blättern, den eigenen Entwürfen und den drei Synthesen ist es
ein **Vorschlag**:
diese Blätter sind pixelgenaue Standbilder ohne Skript, ohne Übergänge, ohne
Zustände. Dort ist nichts abzulesen, dort ist zu entscheiden.

Erzeugt aus denselben Daten wie das Register. Wer hier etwas ändert, ändert es
in `daten_bau.py` und baut beides neu.


## Im Programm

### K01 · Gerät

*Blatt 06 · Die Platte — Telefon · Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Griffzone am Tonarm — gezogen wird am Arm, nicht an der Platte.
- **Zustände** — Die Platte hält an, wenn pausiert wird; der Tonarm steht auf der Rille der Position.
- **Bewegung** — Die Platte dreht sich, solange Ton läuft. Der Tonarm ist gerechnet, nicht geraten.
- **Bibliothek** — Knopf unten in der Skalenreihe, Blende über das Gerät.

### K02 · Werkstisch

*Blatt 06 · Die Platte — Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Griffzone am Tonarm.
- **Zustände** — Wie Gerät; zusätzlich ist der laufende Titel in der Textliste rechts markiert.
- **Bewegung** — Platte dreht bei Ton. Sonst nichts.
- **Bibliothek** — Dauerhaft sichtbar rechts, mit Suchzeile darüber — eine von zwei Ausnahmen.

### K03 · Vollbild

*Blatt 07 · Sternkarte — Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Platte selbst — an den Rillen gezogen.
- **Zustände** — Gespielte Ringe leuchten, der laufende Ring ist der äußerste helle.
- **Bewegung** — Keine. Der Stand ist der leuchtende Ring, nicht eine Drehung.
- **Bibliothek** — Knopf oben rechts, Blende über die Sternkarte.

### K04 · Deck

*Blatt 08 · Kassette — Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Bandleiste unter der Kassette.
- **Zustände** — Tasten haben Druckpunkt und bleiben gedrückt; der laufende Titel steht im Regal hell.
- **Bewegung** — Keine. Die Wickel stehen still — bewusst, sonst wäre es Zierrat.
- **Bibliothek** — Das Regal rechts steht offen, mit Suche — die zweite Ausnahme.

### K05 · Handgerät

*Blatt 08 · Kassette — Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Bandleiste, hier so breit wie ein Daumen.
- **Zustände** — Wie Deck.
- **Bewegung** — Keine.
- **Bibliothek** — Die Auswurftaste öffnet das Regal als Blende.

### K06 · Aufgeschlagen

*Blatt 10 · Weißraum — Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Der Faden — eine Haarlinie, sonst steht nichts da.
- **Zustände** — Nur die Haarlinie zeigt den Stand. Kein zweiter Hinweis.
- **Bewegung** — Keine. Der Tonarm folgt der Position, gerechnet.
- **Bibliothek** — Ein Knopf oben, Blende über die Seite.

### K07 · Register

*Blatt 10 · Weißraum — PC. gelesen aus `player.html`.*

- **Spulen** — Der Faden.
- **Zustände** — Zusätzlich die Warteschlange rechts in Haarlinien, laufender Titel hervorgehoben.
- **Bewegung** — Keine.
- **Bibliothek** — Ein Knopf oben, Blende über die Seite.

### K08 · Bedienteil

*Blatt 11 · Rack — Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Das Metallrad — gedreht, nicht gezogen.
- **Zustände** — Die laufende Hülle im Fach trägt den orangen Rand und „läuft"; die anderen stehen im Schatten.
- **Bewegung** — Keine. Das Rad dreht sich nur unter dem Finger.
- **Bibliothek** — Auswurftaste rechts in der Tastenreihe, Blende über das Gerät.

### K09 · Konsole

*Blatt 11 · Rack — Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Das Metallrad, hier größer.
- **Zustände** — Wie Bedienteil.
- **Bewegung** — Keine.
- **Bibliothek** — Wie Bedienteil.

### K10 · Pult

*Blatt 12 · Studiogerät — Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Das Band unter der Platte.
- **Zustände** — Der laufende Titel ist in der Titelliste links markiert.
- **Bewegung** — Platte dreht bei Ton; der Tonarm ist gerechnet.
- **Bibliothek** — Ein Schalter unten links, Blende über das Pult.

### K11 · Turm

*Blatt 13 · Nussbaum & Champagner — Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Laufleiste an der Frontplatte.
- **Zustände** — Zeiger stehen auf dem Pegel; der laufende Titel ist in der Vierer-Wahl hell.
- **Bewegung** — Die Zeiger folgen dem Pegel. Sonst nichts.
- **Bibliothek** — Knopf an der Bedienplatte, Blende über beide Geräte.

### K12 · Vollverstärker

*Blatt 13 · Nussbaum & Champagner — Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Laufleiste.
- **Zustände** — Wie Turm, auf einer Frontplatte statt zweier.
- **Bewegung** — Zeiger.
- **Bibliothek** — Wie Turm.

### K13 · Papier

*faden-cover.html · Fassung E — Telefon. gelesen aus `player.html`.*

- **Spulen** — Der Rand im rechten Bildschirmrand — ein Strich je Titel.
- **Zustände** — Der laufende Titel ist der helle Strich; Namen erscheinen nur beim Ziehen.
- **Bewegung** — Keine. Die Achse zeigt, sie bewegt sich nicht von selbst.
- **Bibliothek** — Zwei Knöpfe im Kopf: links Sammlung, rechts Suche — Browsen weckt die Tastatur nicht.

### K14 · Desert Rose

*faden-cover.html · Fassung F — Telefon. gelesen aus `player.html`.*

- **Spulen** — Dieselbe Achse, waagerecht als Skala unter dem Bild.
- **Zustände** — Wie Papier.
- **Bewegung** — Keine. Auf der Skala ist ein Tippen eindeutig ein Sprung — keine 8-px-Schwelle.
- **Bibliothek** — Wie Papier.

### K15 · Kissen

*Blatt 02 · Milchglas — Telefon. gelesen aus `player.html`.*

- **Spulen** — Die Balkenreihe.
- **Zustände** — Gelaufene Balken sind gefüllt, der laufende trägt den Akzent.
- **Bewegung** — Keine.
- **Bibliothek** — Wie Papier.

### K16 · Karte

*Blatt 03 · Antiqua & Ausschlag — Telefon. gelesen aus `player.html`.*

- **Spulen** — Der Ausschlag unter der Zeitüberschrift.
- **Zustände** — Kopflinie auf der Position; darunter die Warteschlange mit markiertem Titel.
- **Bewegung** — Keine.
- **Bibliothek** — Wie Papier.

### K17 · Kiesel

*Blatt 05 · Kieselliste — Telefon. gelesen aus `player.html`.*

- **Spulen** — Die Schiene in der Zeile des laufenden Titels.
- **Zustände** — Der Spieler *ist* die laufende Zeile; der nächste Titel wird angetippt.
- **Bewegung** — Keine.
- **Bibliothek** — Wie Papier.

### K18 · Album des Tages

*Blatt 14 · Sonnenscheibe, Variante 1 — Telefon · eigene Seite /tag. gelesen aus `player.html`.*

- **Spulen** — Gar nicht — es gibt genau einen Knopf.
- **Zustände** — Der Ring um den Knopf ist der Stand. Play/Pause am Knopf selbst.
- **Bewegung** — Keine.
- **Bibliothek** — Keine. Bewusst: keine Sammlung, keine Suche, kein zweiter Knopf.

### K19 · Der echte Abzug

*mockups/acht-themen · Familie Sofortbild — Telefon · Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Bahn unter Titel und Interpret.
- **Zustände** — Laufender Titel in „Danach" markiert; Taste gefüllt.
- **Bewegung** — Keine.
- **Bibliothek** — Zwei Knöpfe im Kopf, Blende über die Seite.

### K20 · Die Entwicklung

*mockups/acht-themen · Familie Sofortbild — Telefon · Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Bahn.
- **Zustände** — Wie Der echte Abzug.
- **Bewegung** — **Der Abzug entwickelt sich**: die Milchschicht geht zurück und das Bild gewinnt Farbe und Kontrast — beides über `--p`, den Stand im Titel. Das ist die einzige Bewegung und zugleich die zweite Standanzeige.
- **Bibliothek** — Wie Der echte Abzug.

### K21 · Milchglaszeilen

*mockups/acht-themen · Familie Zeilen — Telefon · Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Bahn unter der Liste.
- **Zustände** — Die laufende Zeile ist die hellere Scheibe.
- **Bewegung** — Keine. Das unscharfe Cover hinter der Seite wechselt mit dem Album, es bewegt sich nicht.
- **Bibliothek** — Wie Der echte Abzug.

### K22 · Programmheft

*mockups/acht-themen · Familie Zeilen — Telefon · Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Bahn.
- **Zustände** — Der laufende Titel liegt unter dem Textmarker und trägt einen Bleistifthaken.
- **Bewegung** — Keine.
- **Bibliothek** — Wie Der echte Abzug.

### K23 · Die Spur

*mockups/acht-themen · Familie Zeilen — Telefon · Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Bahn.
- **Zustände** — Jede Zeile trägt ihren eigenen Stand als Linie: vor der laufenden voll, danach leer.
- **Bewegung** — Nur die Linie der laufenden Zeile wächst. Kein zweiter bewegter Teil.
- **Bibliothek** — Wie Der echte Abzug.

### K24 · Emaille

*mockups/acht-themen · Familie Platten — Telefon · Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Bahn auf der Bedienplatte.
- **Zustände** — Laufender Titel auf der Listenplatte markiert; Haupttaste gefüllt.
- **Bewegung** — Keine.
- **Bibliothek** — Wie Der echte Abzug.

### K25 · Gespritzt

*mockups/acht-themen · Familie Platten — Telefon · Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Bahn.
- **Zustände** — Wie Emaille; die Haupttaste ist hier ein Ring statt einer Fläche.
- **Bewegung** — Keine.
- **Bibliothek** — Wie Der echte Abzug.

### K26 · Abreißkalender

*mockups/acht-themen · Familie Block — Telefon · Tablet · PC. gelesen aus `player.html`.*

- **Spulen** — Die Bahn auf dem obersten Blatt.
- **Zustände** — Das oberste Blatt ist der laufende Titel; die kommenden liegen gestaffelt darunter.
- **Bewegung** — Keine — auch kein Abreißen. Das hatte die Vorlage nicht, und es wäre eine Erfindung.
- **Bibliothek** — Wie Der echte Abzug.


## Blatt gezeichnet, nicht gebaut

### K27 · Skalenband

*Blatt 15 · Weltempfänger — Tablet quer. gelesen aus dem Blatt.*

- **Spulen** — Die Feinskala; das Band *wählt* das Album.
- **Zustände** — Das Skalenband zeigt die Nachbaralben; die Marke steht auf dem laufenden.
- **Bewegung** — Keine. Im Ruhezustand ist es ein lesbares, beschriftetes Skalenband.
- **Bibliothek** — Das Band selbst ist die Sammlung — Abstimmen ist Suchen.

### K28 · Abfahrtstafel

*Blatt 16 · Fallblatt, V1 — Tablet quer · PC. gelesen aus dem Blatt.*

- **Spulen** — Die laufende Zeile selbst.
- **Zustände** — Die Warteschlange ist die Tafel; der laufende Titel ist die oberste Zeile.
- **Bewegung** — **Beim Titelwechsel klappen die Zeichen um** — die einzige Bewegung, und die ist der ganze Entwurf. Ohne sie ist es keine Fallblattanzeige.
- **Bibliothek** — Knopf an der Tafel, Blende darüber.

### K29 · Emaille

*Blatt 16 · Fallblatt, V2 — Tablet quer · PC. gelesen aus dem Blatt.*

- **Spulen** — Wie Abfahrtstafel.
- **Zustände** — Wie Abfahrtstafel.
- **Bewegung** — Wie Abfahrtstafel, in Emaille und Messing statt Schwarz.
- **Bibliothek** — Wie Abfahrtstafel.

### K30 · Kontaktbogen

*Blatt 17 · Leuchttisch, V1 — PC · Tablet quer. gelesen aus dem Blatt.*

- **Spulen** — Der Filmstreifen unter dem Fadenkreuz.
- **Zustände** — Das laufende Dia liegt unter der Lupe, die übrigen daneben auf dem Milchglas.
- **Bewegung** — Keine. Die Lupe steht, der Streifen läuft unter ihr durch.
- **Bibliothek** — Der Leuchttisch selbst ist die Sammlung — die Dias liegen offen.

### K31 · Cyanotypie

*Blatt 17 · Leuchttisch, V2 — PC · Tablet quer. gelesen aus dem Blatt.*

- **Spulen** — Wie Kontaktbogen.
- **Zustände** — Wie Kontaktbogen.
- **Bewegung** — Keine.
- **Bibliothek** — Wie Kontaktbogen.

### K32 · Stenorette

*Blatt 18 · Zählwerk, V1 — Telefon. gelesen aus dem Blatt.*

- **Spulen** — Das Zählwerk hochdrehen.
- **Zustände** — Der Zählerstand *ist* die Position in der Schlange; vier Tasten mit Druckpunkt.
- **Bewegung** — Die Rollen drehen sich beim Spulen — nicht von selbst.
- **Bibliothek** — Knopf am Gehäuse, Blende darüber.

### K33 · Graupappe

*Blatt 18 · Zählwerk, V2 — Telefon. gelesen aus dem Blatt.*

- **Spulen** — Wie Stenorette.
- **Zustände** — Wie Stenorette.
- **Bewegung** — Wie Stenorette.
- **Bibliothek** — Wie Stenorette.

### K34 · Zinkguss

*Blatt 19 · Rechenscheibe, V1 — Tablet hoch. gelesen aus dem Blatt.*

- **Spulen** — Die Scheibe drehen — eine Umdrehung je Album.
- **Zustände** — Die rote Ablesemarke steht still, die Scheibe dreht sich unter ihr.
- **Bewegung** — Die Scheibe folgt der Position. Sonst nichts.
- **Bibliothek** — Knopf an der Achse, Blende darüber.

### K35 · Volvelle

*Blatt 19 · Rechenscheibe, V2 — Tablet hoch. gelesen aus dem Blatt.*

- **Spulen** — Wie Zinkguss.
- **Zustände** — Wie Zinkguss.
- **Bewegung** — Wie Zinkguss, als Papierdrehscheibe.
- **Bibliothek** — Wie Zinkguss.

### K36 · Filz auf Terrazzo

*Blatt 20 · Bespannung — Tablet quer. gelesen aus dem Blatt.*

- **Spulen** — Die gespannte Kordel; Knoten sitzen an den Titelgrenzen.
- **Zustände** — Der Pegel ist gestickt; der laufende Titel steht am Knoten.
- **Bewegung** — Keine.
- **Bibliothek** — Knopf auf der Terrazzoplatte, Blende darüber.

### K37 · Glutbank

*Blatt 21 · Glut, V1 — PC. gelesen aus dem Blatt.*

- **Spulen** — In jede Schiene greifen — auch in eine fremde, dann springt es dorthin.
- **Zustände** — Der laufende Titel glüht und trägt die Kapsel; gespielte sind matt warm aufgefüllt.
- **Bewegung** — Das Glühen folgt der Position. Kein Flackern.
- **Bibliothek** — Knopf über der Bank, Blende darüber.

### K38 · Glutleiste

*Blatt 21 · Glut, V2 — Tablet quer. gelesen aus dem Blatt.*

- **Spulen** — Über Titelgrenzen hinweg — `seekGlobal`.
- **Zustände** — Eine Schiene für die ganze Warteschlange, feine Marken an den Titelgrenzen.
- **Bewegung** — Wie Glutbank.
- **Bibliothek** — Wie Glutbank.

### K39 · Lupe

*Blatt 22 · Lupe, V1 — PC. gelesen aus dem Blatt.*

- **Spulen** — Am Lichtsaum unter der Pille.
- **Zustände** — Der Schein wächst mit der Zeit — das ist die Anzeige.
- **Bewegung** — Der Schein. Sonst nichts.
- **Bibliothek** — Das Suchfeld steht in der Mitte und ist der Zugang — wie in der Vorlage.

### K40 · Lupe, aufgeschlagen

*Blatt 22 · Lupe, V2 — Tablet quer. gelesen aus dem Blatt.*

- **Spulen** — Am Lichtsaum unter der Tafel.
- **Zustände** — Wie Lupe.
- **Bewegung** — Wie Lupe.
- **Bibliothek** — Die Sammlung liegt offen daneben, die Suchzeile direkt darüber.

### K41 · Plaketten

*Blatt 23 · Plaketten, V1 — PC. gelesen aus dem Blatt.*

- **Spulen** — An der dunklen Bahn unter dem Spieler.
- **Zustände** — Jeder Titel eine Plakette, **genau eine ist hell** — das ist die ganze Zustandslehre.
- **Bewegung** — Keine.
- **Bibliothek** — Eine Plakette in der Reihe führt hinein.

### K42 · Plakettenpult

*Blatt 23 · Plaketten, V2 — Tablet quer. gelesen aus dem Blatt.*

- **Spulen** — Wie Plaketten.
- **Zustände** — Wie Plaketten.
- **Bewegung** — Keine.
- **Bibliothek** — Hinter einer Plakette, nicht offen.

### K43 · Stapel

*Blatt 24 · Stapel, V1 — PC. gelesen aus dem Blatt.*

- **Spulen** — Am Streifen in der Zeile des laufenden Titels.
- **Zustände** — Kalt ist, was gespielt wurde; warm ist, was läuft. Die laufende Karte ist aufgeklappt.
- **Bewegung** — Keine.
- **Bibliothek** — Der Stapel rechts ist die Sammlung.

### K44 · Stapel, schräg

*Blatt 24 · Stapel, V2 — Tablet quer. gelesen aus dem Blatt.*

- **Spulen** — Am Streifen der vorderen Karte.
- **Zustände** — Je weiter ein Titel von der Gegenwart weg ist, desto tiefer steht er im Raum.
- **Bewegung** — Keine.
- **Bibliothek** — Wie Stapel.

### K45 · Eisblau

*Blatt 25 · Eisblau, V1 — Tablet quer. gelesen aus dem Blatt.*

- **Spulen** — Im Ausschlag, 66 px hoch.
- **Zustände** — Gelaufene Balken dunkel, der laufende orange. Orange sitzt an genau zwei Stellen.
- **Bewegung** — Die Platte dreht sich nur, solange Ton läuft — die zweite Anzeige.
- **Bibliothek** — Knopf oben rechts, Blende darüber.

### K46 · Eisblau, weit

*Blatt 25 · Eisblau, V2 — PC. gelesen aus dem Blatt.*

- **Spulen** — Über Titelgrenzen hinweg — `seekGlobal`.
- **Zustände** — Das Band trägt die ganze Warteschlange, feine Striche an den Grenzen.
- **Bewegung** — Wie Eisblau.
- **Bibliothek** — Wie Eisblau.

### K47 · Eisblau, hochkant

*Blatt 25 · Eisblau, V3 — Telefon. gelesen aus dem Blatt.*

- **Spulen** — Im Ausschlag, 60 px hoch — Daumenbreite.
- **Zustände** — Wie Eisblau.
- **Bewegung** — Wie Eisblau.
- **Bibliothek** — Knopf oben rechts; die Blende ist hier einspaltig.


## Paket, zum Bau ausgewählt

### K48 · Akai 747

*Paket 18 · nur Querformat — PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Der Zeitstrahl unter dem Titel, über die volle Breite.
- **Zustände** — Tasten mit Lampe: PLAY grün, PAUSE gelb, sonst dunkel. Der laufende Titel steht in der Spulenliste links hell.
- **Bewegung** — Der VU-Zeiger folgt dem Pegel — das ist bei einem Bandgerät die Anzeige und kein Zierrat. **Die Spulen drehen sich nicht**: zwei laufende Wickel wären reine Dekoration und der einzige Dauerläufer im ganzen Satz.
- **Bibliothek** — Die Taste LIBRARY am Ende der Tastenreihe, Blende über die Frontplatte.

### K49 · Glass ohne Kreise

*Paket 33a · Abwandlung von 33 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn unter dem Titel.
- **Zustände** — Der laufende Titel in der Liste hell, die übrigen gedämpft; Haupttaste gefüllt.
- **Bewegung** — Keine. Das Blatt lebt von der Ruhe der Milchglaskarte.
- **Bibliothek** — Der Glaskreis oben rechts, Blende über die Karte.

### K50 · Glass mit dezenten Kreisen

*Paket 33b · Abwandlung von 33 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn.
- **Zustände** — Wie Glass ohne Kreise.
- **Bewegung** — Keine. **Offen zu entscheiden:** ob die Farbwolken beim Albumwechsel die Cover-Farben annehmen. Das wäre eine Bewegung je Album, nicht je Sekunde — vertretbar, aber neu.
- **Bibliothek** — Wie Glass ohne Kreise.

### K51 · EA Archive

*Paket 22 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die orange Bahn unter „NOW PLAYING".
- **Zustände** — PLAY ist das orange gefüllte Feld der Leiste; der laufende Titel im Spec-Raster fett.
- **Bewegung** — Keine. Ein Archivblatt bewegt sich nicht.
- **Bibliothek** — ARCHIVE als fünftes Feld der Tastenleiste, Blende über das Blatt.

### K52 · Mix Tape Klar

*Paket 24 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die rote Bahn unter der Titelliste.
- **Zustände** — Der laufende Titel trägt den roten Punkt, die übrigen einen grauen.
- **Bewegung** — Keine. **Zu entscheiden:** ob die Wickel der durchsichtigen Kassette mitlaufen — hier wäre es ausnahmsweise Anzeige und nicht Zierrat, weil man durch die Schale sieht, wie viel Band noch übrig ist.
- **Bibliothek** — Der runde Knopf mit Bibliothekszeichen neben Weiter.

### K53 · Audio Tape C90

*Paket 25 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn unter der Kassette.
- **Zustände** — Balkentasten sind gedrückt oder nicht; laufender Titel in der Liste hervorgehoben.
- **Bewegung** — Keine.
- **Bibliothek** — Der orange Block LIBRARY am Ende der Tastenleiste.

### K54 · True Sound

*Paket 26 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn.
- **Zustände** — Die Titelliste ist farbcodiert; der laufende Titel trägt den vollen Ton, die übrigen einen blassen.
- **Bewegung** — Keine.
- **Bibliothek** — Die Pille LIBRARY in der Tastenreihe.

### K55 · Stereo 60

*Paket 27 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn im gerahmten Feld.
- **Zustände** — Rahmen-Tasten mit sichtbarem Druckzustand; laufender Titel im Rahmen markiert.
- **Bewegung** — Keine.
- **Bibliothek** — Der umrandete Knopf LIBRARY.

### K56 · Vinyl Rote Tasten

*Paket 31 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Der Slider — die Sprechblase darüber ist die Zeit und wandert mit.
- **Zustände** — Die drei roten Rundtasten haben einen Druckzustand; laufender Titel in der Liste fett.
- **Bewegung** — Die Sprechblase folgt dem Griff. **Die Platte dreht sich nicht** — sie ist hier Bild, nicht Laufwerk; es gibt keinen Tonarm, der eine Drehung erklären würde.
- **Bibliothek** — Die eigene Kachel mit Bibliothekszeichen oben rechts.

### K57 · Retro Party

*Paket 34 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn unter dem Plakat.
- **Zustände** — Rahmen-Tasten mit Druckzustand; der laufende Titel im Programm hervorgehoben.
- **Bewegung** — Keine. **Zu entscheiden:** ob die Strahlen im Hintergrund sich drehen. Ich rate ab — ein Dauerläufer hinter Text macht ihn schwer lesbar.
- **Bibliothek** — Der Rahmen-Knopf CRATE.

### K58 · Music Sounds Better

*Paket 35 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die rote Bahn unter der Titelliste.
- **Zustände** — Die gefüllte rote Kreis-Taste ist Play/Pause; der laufende Titel steht gesperrt und dunkel, die übrigen grau.
- **Bewegung** — Keine. Das Blatt ist der Pilot gerade deshalb: es hat nichts, worüber man streiten müsste.
- **Bibliothek** — Der runde Knopf mit Bibliothekszeichen in der Reihe.

### K59 · Song-Poster schwarz

*Paket 36 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn unter dem Spiraltext.
- **Zustände** — Kreis-Tasten mit Druckzustand; im Rahmen sitzt der Tonarm auf der Position.
- **Bewegung** — **Zu entscheiden:** Der Spiraltext *ist* die Rille — die Platte zu drehen wäre hier ausnahmsweise sinnvoll, weil der Tonarm sonst über stehendem Text schwebt. Mein Vorschlag: der Tonarm wandert, die Platte steht. Eine Drehung würde den Text unlesbar machen.
- **Bibliothek** — Der runde Knopf mit Bibliothekszeichen neben Repeat.

### K60 · Song-Poster weiß

*Paket 37 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn.
- **Zustände** — Beschriftete Tasten (SHUFFLE, PREV, PLAY, NEXT, REPEAT) mit Druckzustand.
- **Bewegung** — Wie Song-Poster schwarz.
- **Bibliothek** — Der Knopf SAMMLUNG rechts in der Tastenreihe.

### K61 · World Music Day

*Paket 38 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn im Programmfeld.
- **Zustände** — Der laufende Titel im Line-up hervorgehoben; Tasten mit Druckzustand.
- **Bewegung** — Keine. Blitze und Stern sind Plakat, nicht Anzeige.
- **Bibliothek** — Der Knopf LINE-UP am Ende der Tastenleiste.


## Eigene Entwürfe, Auswahl offen

### K62 · Kippschalter

*Entwurf 39 · Foto 23.30.54 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — **Offen — hier fehlt am meisten.** Der Entwurf ist reine Typografie; eine Bahn gibt es nicht. Vorschlag: die Grundlinie unter dem Titel wird zur Spulfläche.
- **Zustände** — Die beiden Kippschalter sind oben oder unten — das ist Wiedergabe/Pause und zugleich das Bild.
- **Bewegung** — Der Kippschalter kippt beim Umschalten. Das ist die eine Bewegung, und sie ist die Bedienung selbst, nicht ihre Verzierung.
- **Bibliothek** — Vorschlag: ein dritter Schalter oder ein Wort in der Kopfzeile — im Blatt nicht vorgesehen.

### K63 · Sonnenglas

*Entwurf 43 · Foto 23.38.31 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn auf der Glaskarte.
- **Zustände** — Die Karte trägt Titel und Zeit; der laufende Titel in der Liste hell.
- **Bewegung** — Keine. Der Himmel ist Grund und darf nicht wandern.
- **Bibliothek** — Die Glaspille über der Karte.

### K64 · Klarglas

*Entwurf 43b · Fassung von 43 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn auf der Karte.
- **Zustände** — Wie Sonnenglas.
- **Bewegung** — Keine. **Zu entscheiden:** ob der Spiegelstreifen beim Ziehen mitwandert — das wäre eine schöne Rückmeldung und kostet fast nichts.
- **Bibliothek** — Die Glaspille über der Karte.

### K65 · Rauchglas

*Entwurf 43f · Fassung von 43 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn auf der Karte.
- **Zustände** — Wie Sonnenglas.
- **Bewegung** — Wie Klarglas.
- **Bibliothek** — Die Glaspille über der Karte.

### K66 · Gerätezeile

*Entwurf 44 · Fotos 23.43.04/13 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Haarlinie.
- **Zustände** — Das Dreieck zeigt Wiedergabe; bei Pause steht ein Doppelstrich. Mehr gibt die Zeile nicht her.
- **Bewegung** — Keine. Das ist das kargste Display im Satz und soll es bleiben.
- **Bibliothek** — Vorschlag: ein Wort links in der Zeile — im Blatt nicht vorgesehen, muss dazu.

### K67 · Malerblatt

*Entwurf 46 · Foto 23.54.59 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Der gezogene Strich unter dem Stillleben.
- **Zustände** — Der Strich ist der Fortschritt; er ist gemalt und endet dort, wo die Position steht.
- **Bewegung** — Keine. **Zu entscheiden:** ob der Strich beim Wachsen wie gemalt ausläuft. Das wäre die einzige Stelle, an der eine Bewegung dem Entwurf etwas hinzufügt.
- **Bibliothek** — Vorschlag: ein Wort am Blattrand — im Blatt nicht vorgesehen.

### K68 · Siebdruck

*Entwurf 48 · Foto 08.38.27 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn unter den Versalien.
- **Zustände** — Zwei Farben, kein Grau: gelaufener Teil gelb, Rest oranger Grund.
- **Bewegung** — Keine. Ein Siebdruck bewegt sich nicht.
- **Bibliothek** — Vorschlag: ein Wort in der Fußzeile — im Blatt nicht vorgesehen.

### K69 · Fallblatt

*Entwurf 50 · Foto 08.39.21 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn unter den Fallblättern.
- **Zustände** — Die beiden Fallblätter zeigen Titelnummer und Laufzeit.
- **Bewegung** — **Beim Titelwechsel klappen die Blätter um** — wie beim gezeichneten Blatt 16. Ohne das ist es ein Wecker ohne Klappzahlen.
- **Bibliothek** — Der Drehknopf öffnet die Sammlung.

### K70 · Tastenfeld

*Entwurf 51 · Foto 08.43.15 — Telefon. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn im Glasfeld oben.
- **Zustände** — Die Quadrate unten sind die Bedienung; das gedrückte ist gefüllt.
- **Bewegung** — Keine.
- **Bibliothek** — Die grüne Taste ist die Sammlung — im Blatt bereits vorgesehen.

### K71 · Fokusmodul

*Entwurf 53 · Foto 08.48.50 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn im Modul.
- **Zustände** — Das Modul zeigt genau einen Zustand hell.
- **Bewegung** — Keine.
- **Bibliothek** — Vorschlag: eine Kachel im Modul — im Blatt zu prüfen.

### K72 · Punktring

*Entwurf 56 · Foto 08.58.02 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Der Ring — gezogen wird auf dem Kreis.
- **Zustände** — Der Punkt auf dem Ring ist die Position; gelaufener Bogen kräftiger.
- **Bewegung** — Der Punkt wandert auf dem Ring. Sonst nichts.
- **Bibliothek** — Vorschlag: die Mitte des Rings öffnet die Sammlung.

### K73 · Zeigerfront

*Entwurf 58 · Fotos 09.18.44/09.20.06 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Der Zeitstrahl unter der Tastenreihe.
- **Zustände** — Die waagerechte Tastenreihe zeigt den gedrückten Knopf; der Ring rechts ist die Lautstärke.
- **Bewegung** — Die beiden VU-Zeiger folgen dem Pegel — dafür sind sie da.
- **Bibliothek** — Vorschlag: eine Taste in der Reihe — im Blatt zu prüfen.

### K74 · Klimaxfront

*Anzeige des Linn Klimax DSM — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Haarlinie unter Titel und Lautstärke.
- **Zustände** — Weiss für das, was gilt, gedämpftes Grau für das, was es beschreibt. Kein Akzent, keine Farbe.
- **Bewegung** — Keine. Die Vorlage dimmt im Ruhezustand auf schwarzes Glas — **zu entscheiden**, ob wir das übernehmen. Es wäre die einzige Bewegung und ein starkes Bild.
- **Bibliothek** — Die Quellenzeile links im Feld: die Sammlung ist eine Quelle wie jede andere.

### K75 · Fernanzeige

*Bildschirmeinblendung — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Haarlinie über der unteren Reihe.
- **Zustände** — Nur zwei Zeichen: Lautstärke als Zahl links, Wiedergabe rechts. Kein dritter Zustand.
- **Bewegung** — Keine. Eine Einblendung, die sich bewegt, ist keine Einblendung mehr.
- **Bibliothek** — Die Quellenzeile oben in der Mitte, wo an einem Gerät der Quellenname stünde.

### K76 · Leuchtmarke

*Nahaufnahme einer Skala — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Skala selbst — über Titelgrenzen hinweg, `seekGlobal`.
- **Zustände** — Der rote Keil ist die Gegenwart; Rot kommt sonst nirgends vor. Titelgrenzen stehen als hohe Striche zwischen den feinen.
- **Bewegung** — **Der Keil wandert, und die Schärfe wandert mit ihm**: der Schleier ist dort durchsichtig, wo er steht. Das ist Anzeige, nicht Zierrat — neben der Gegenwart liest man genau ab, am Rand nur ungefähr.
- **Bibliothek** — Die Quellenzeile oben links.

### K77 · Glasgravur

*McIntosh MX110 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Das Glas selbst — die Warteschlange in Minuten, über Titelgrenzen hinweg.
- **Zustände** — Die Gravur ist überall gleich hell; nur der blaue Balken bewegt sich. Gelaufenes sieht aus wie Kommendes — bewusst: die Skala ist ein Massstab, kein Verlauf.
- **Bewegung** — Nur der blaue Balken wandert. **Zu entscheiden:** ob er beim Ziehen mitleuchtet oder erst am Ende springt.
- **Bibliothek** — Vorschlag: der Kippschalter „Suche" auf der Blende — die Blende trägt sonst keine Taste dafür.

### K78 · Gyrorad

*Marantz 2216 B & Pioneer SX-650 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Das Rad — endlos drehbar. Die Albumskala darüber wird nicht angefasst.
- **Zustände** — Der Zeiger links steht auf der Position im Titel, die rote Marke auf der Albumskala.
- **Bewegung** — **Das Rad läuft nach** und kommt zur Ruhe; der Zeiger folgt. Ohne Trägheit ist es ein Knopf, und dann braucht es kein Rad. **Zu entscheiden:** wie stark die Reibung ist.
- **Bibliothek** — Vorschlag: das Buchzeichen in der Tastenreihe links.

### K79 · Milchlicht

*Technics SA-5551 & Yamaha CR-700 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Das Milchglasband — die Grenze zwischen dunkel und hell ist die Position.
- **Zustände** — Gelaufenes ist dunkel, Kommendes leuchtet; der laufende Titel steht fett und liegt auf der Grenze. Zwei kleine Fenster zählen Titel und Restzeit.
- **Bewegung** — **Die Leuchtkante wandert**, sonst nichts. Das ist die ganze Bewegung und zugleich die ganze Anzeige.
- **Bibliothek** — Der Druckknopf „Sammlung" in der Reihe auf dem Aluminium.

### K80 · Automatik

*Receiver mit FM Automatic Tuning — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die grosse türkise Skala; wer einen Merkplatz nimmt, springt statt zu spulen.
- **Zustände** — Fünf Schieber, jeder ein gemerktes Album; der aktive Platz ist türkis umrandet, seine Marke steht auf dem Stand im Album.
- **Bewegung** — Die orange Nadel wandert auf der Skala. **Zu entscheiden:** ob ein Schieber beim Springen nachfährt — das wäre die zweite Bewegung.
- **Bibliothek** — Die Merkplätze sind der schnelle Weg; daneben Buchzeichen und Lupe in der Tastenreihe unten.

### K81 · Rasterschrift

*Gryphon Ethos — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Punktreihe unter der Anzeige — so fein wie das Raster, nicht feiner.
- **Zustände** — Cyan heisst an, dunkel heisst aus. Der laufende Titel ist der einzige rote Punkt.
- **Bewegung** — Punkte gehen an und aus, sonst nichts — ein Raster blendet nicht über.
- **Bibliothek** — Vorschlag: das vierte geätzte Zeichen unten links.

### K82 · Fadertisch

*Morror Art — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Bahn unter dem Bild; die vier unteren Fader springen auf Viertel, Hälfte, Dreiviertel und Ende.
- **Zustände** — Ein Pad je Titel: Gespieltes dunkler, Laufendes orange. Genau eine Taste ist orange, und sie ist die grösste.
- **Bewegung** — Keine. **Zu entscheiden:** ob ein Pad beim Antippen kurz aufleuchtet — das wäre Rückmeldung und kein Zierrat.
- **Bibliothek** — Die Zeichen unten rechts neben „Sammlung". Das Pad-Feld blättert in der letzten Reihe weiter.

### K83 · Halbmond

*AVM — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Der Fortschrittsstrich im Schlitz — wenige Pixel hoch, aber die einzige Stelle mit einer Position.
- **Zustände** — Die Kante zwischen heller und dunkler Kappenhälfte ist die Stellung des Knopfes. Im Schlitz steht, was die fünf Punkte gerade tun.
- **Bewegung** — Der Halbmond dreht sich beim Verstellen. **Zu entscheiden:** ob der Schlitz beim Titelwechsel überblendet oder hart umschaltet.
- **Bibliothek** — Der fünfte Punkt unter dem Schlitz.

### K84 · Dezibel

*Eversolo T10 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Das rechte Zeigerfenster — man zieht den Zeiger.
- **Zustände** — Links Pegel, rechts Stand im Album; Orange am Skalenende heisst in beiden „es wird knapp".
- **Bewegung** — **Beide Zeiger bewegen sich, und beide zeigen etwas** — der linke den Pegel, der rechte die Position. Keiner läuft leer.
- **Bibliothek** — Die freistehenden Zeichen rechts, ohne Rahmen und ohne Wort.

### K85 · Silberkasten

*Eversolo, Silberplatte — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Warteschlangenleiste auf der Platte; der laufende Titel ist der volle Strich.
- **Zustände** — Alles steht auf der einen Platte. Der Ring unten ist gedrückt oder nicht — mehr Zustand hat er nicht.
- **Bewegung** — Nur der Zeiger. Die Platte selbst bleibt still: sie ist Blech, kein Bildschirm.
- **Bibliothek** — **Offen.** Der Entwurf hat bewusst einen einzigen Knopf. Vorschlag: langes Drücken auf die Platte öffnet die Sammlung — sonst braucht es eine zweite Marke auf der Platte.

### K86 · Tastenreihe

*Kassettenrekorder SKR 700 — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Das Fenster: der Bandlauf zwischen den beiden Wickeln, über Titelgrenzen hinweg.
- **Zustände** — Genau eine Taste steht unten, und ihr Wort steht fett — mehr Zustand braucht eine mechanische Reihe nicht. Der Wickel links wächst, der rechte wird dünner.
- **Bewegung** — Die Wickel ändern ihren Durchmesser. Die Taste federt beim Drücken. Sonst nichts — ein Klaviertastenwerk ist still, bis man es anfasst.
- **Bibliothek** — Das Buchzeichen unter der Tastenreihe, neben Lupe und Lautstärke.

### K87 · Anschlag

*Plattenspieler-Plakat — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Der Rand der orangen Scheibe — der Sektor folgt dem Finger, im Uhrzeigersinn ab zwölf Uhr.
- **Zustände** — Der laufende Titel ist der einzige fett gesetzte im Blocksatz; der abgespielte Teil des Albums steht als dunklerer Sektor in der Scheibe.
- **Bewegung** — Der Sektor wächst. **Zu entscheiden:** ob die schwarze Platte oben rechts sich dreht, solange Ton läuft — sie zeigt dann nichts, was der Sektor nicht schon sagt, wäre aber das einzige Lebenszeichen in einem sonst starren Plakat.
- **Bibliothek** — Das Buchzeichen in der Zeichenreihe unten; die Titelliste selbst ist Text und kein Menü.

### K88 · Bandteller

*Revox-Bandmaschine — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Spulen selbst: man dreht eine, das Band wandert.
- **Zustände** — Der Durchmesser der beiden Wickel ist der Stand im Album; das Zählwerk zeigt die Position im Titel. Von den Wipptasten steht immer genau eine.
- **Bewegung** — **Die Wickel wachsen und schrumpfen** — das ist die einzige Fortschrittsanzeige des Entwurfs und deshalb Pflicht. Die beiden Zeiger folgen Pegel und Stand. Ob sich die Spulen zusätzlich *drehen*, ist **zu entscheiden**: es wäre der einzige Dauerläufer.
- **Bibliothek** — Das Buchzeichen rechts auf der Frontplatte, neben Lupe und Lautstärke.


## Synthese — aus allen 88 gezogen

### K89 · Bogen

*Synthese aus K06 Aufgeschlagen, K13 Papier, K14 Desert Rose, K87 Anschlag — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die Haarlinie unten über die volle Satzbreite — sie trägt das ganze Album, nicht den Titel, also spult man über Titelgrenzen hinweg an derselben Linie. Das ist `bindAchse()` und nicht `bindDrag()`: Ziel in `deck._gziel` parken, erst beim Loslassen anwenden.
- **Zustände** — Der laufende Titel ist der einzige mit Tinte statt Grau, seine Ziffer steht in Messing. Auf der Linie: die gelaufene Strecke messingfarben, die Raute auf der Gegenwart. Messing steht nirgends sonst — das ist die ganze Zustandslehre des Blattes.
- **Bewegung** — Nur die Raute wandert und die messingfarbene Strecke wächst. Kein Blättern, kein Aufblenden. **Zu entscheiden:** ob die Raute beim Titelwechsel merklich über den hohen Strich springt oder einfach weiterläuft — ersteres macht die Grenze hörbar sichtbar, letzteres ist ruhiger.
- **Bibliothek** — Die drei leisen Zeichen oben rechts; die Sammlung als Blende über das Blatt. Die Titelliste ist Text und trotzdem antippbar — sie ist die Warteschlange, nicht die Sammlung.

### K90 · Nachtglas

*Synthese aus K49 Glass ohne Kreise, K21 Milchglaszeilen, K79 Milchlicht, K84 Dezibel — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Die hinterleuchtete Bahn unter dem Titel. Sie zeigt **nur den laufenden Titel**; für das Album sind die Glaszeilen darunter zuständig, und jede davon kann ihre eigene Kante tragen (dann wäre es K23 Die Spur in Glas — das ist offen, siehe Bewegung).
- **Zustände** — Gelaufenes leuchtet, Kommendes ist dunkles Glas, die weisse Kante steht auf der Gegenwart. In der Schlange: gelaufene Zeilen matt, die laufende heller mit eisblauem Balken an der linken Kante. Gedrückt wird an einer kurz aufhellenden Scheibe erkennbar.
- **Bewegung** — Die Lichtkante wandert, sonst nichts. **Zu entscheiden:** ob jede Glaszeile ihren eigenen Stand als Kante trägt — das wäre schön und wäre zugleich fünf bewegte Kanten statt einer, also gegen die Hausregel, dass nur die Gegenwart sich bewegt.
- **Bibliothek** — Die drei leisen Zeichen oben rechts in der Karte; die Sammlung als Blende, die als weitere Glasscheibe über die Karte fährt.

### K91 · Rundlauf

*Synthese aus K78 Gyrorad, K11/K12 Turm & Vollverstärker, K77 Glasgravur, K85 Silberkasten, K83 Halbmond — Telefon · PC. **Vorschlag — bitte prüfen**.*

- **Spulen** — Das geriffelte Rad rechts (am Telefon unten in der Mitte) — gedreht, nicht gezogen; und die gravierte Skala im Anzeigefenster ist die zweite, feinere Spulfläche. Nur eine der beiden darf `data-spulen` tragen: das Rad, weil es die grössere Fläche ist und ohne Blick getroffen wird.
- **Zustände** — Der Bernsteinbalken steht auf der Gegenwart, die hohen Striche sind die Titelgrenzen, die Ziffer des laufenden Titels ist die einzige helle. In der Silberplatte steht der laufende Titel in Bernstein. Die Tasten haben eine Kante und einen Lichtsaum, damit ein Druck als Einsinken darstellbar ist.
- **Bewegung** — Der Bernsteinbalken wandert. Das Rad dreht sich **nur unter dem Finger**, mit Nachlauf wie bei K78 Gyrorad — ohne Trägheit ist es ein Knopf. Sonst steht alles: eine Frontplatte ist still, bis man sie anfasst.
- **Bibliothek** — Die drei leisen Zeichen oben rechts, graviert in die Frontplatte; die Sammlung als Blende über das Gerät. Die Silberplatte zeigt die Warteschlange, nicht die Sammlung.
