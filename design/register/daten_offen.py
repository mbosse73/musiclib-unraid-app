# -*- coding: utf-8 -*-
OFFEN = [
 ('Siebenundvierzig Bauanleitungen sind Vorschläge, keine Entscheidungen',
  'Bei K48–K94 steht auf jeder Karte, was ich zu Spulfläche, Zuständen und Bewegung '
  '<b>vorschlage</b> — diese Blätter sind Standbilder ohne Skript, dort ist nichts abzulesen. '
  'An dreizehn Stellen habe ich die Frage ausdrücklich offen gelassen statt sie zu entscheiden '
  '(unter anderem: drehen sich die Wickel bei K52 Mix Tape Klar, dreht sich die Spiralplatte '
  'bei K59/K60, dimmt K74 Klimaxfront im Ruhezustand auf schwarzes Glas, trägt bei K90 '
  'Nachtglas jede Glaszeile ihren eigenen Stand). '
  'Vier Entwürfe haben zudem <b>gar keinen Bibliotheks-Zugang im Blatt</b> — K62 Kippschalter, '
  'K66 Gerätezeile, K67 Malerblatt, K68 Siebdruck; dort muss einer dazu, sonst reisst der Test.'),
 ('Fünf Entwurfsseiten sind zurück, aber unbewertet',
  '<code>mockups/vorbilder.html</code> (19 Entwürfe), <code>varianten.html</code>, '
  '<code>farben.html</code>, <code>glanz.html</code>, <code>kassette.html</code> — die Suche, aus '
  'der <i>Papier</i>, <i>Desert Rose</i> und die acht Themen oben hervorgingen. Sie stehen bewusst '
  '<b>nicht</b> im Register: das sind Studien in Reihen, keine einzelnen Konzepte. Wenn eine davon '
  'ein Konzept werden soll, sag welche.'),
 ('Einundzwanzig gezeichnete Blätter warten auf eine Entscheidung',
  'K27–K47 sind fertig durchgezeichnet und keines portiert. Von allem hier ist das der billigste '
  'Zuwachs: ein CSS-Block, ein <code>layout({…})</code> — und seit der Anprobe eine dritte '
  'Kleinigkeit: eine Zeile in <code>SIGNETE</code> für die Familie, sonst bleibt die Kachel im '
  'Auswahlstreifen leer. K39 Eisblau hochkant ist die einzige Telefon-Fassung darunter.'),
 ('Etappe 5 ist nicht angefangen',
  'Vierzehn Paket-Konzepte (K48–K61), kein einziges portiert. Pilot ist K58 Music Sounds Better. K49 und K50 sind die Sonderfälle: die zwei überlebenden Fassungen des gestrichenen Blattes 33 — dort ist zuerst zu entscheiden, ob eine davon 33 ersetzt.'),
 ('Siebenundzwanzig eigene Entwürfe warten auf eine Entscheidung',
  'K62–K88 sind gebaut, aber keiner ist ausgewählt. <b>K77–K88 sind neu</b> — zwölf aus dem dritten Vorlagensatz, darunter mit <i>Automatik</i> der einzige Entwurf im ganzen Register, der einen Direktzugriff an der Sammlung vorbei anbietet. K63–K65 sind dieselbe Karte in drei Scheiben — Sonnenglas, Klarglas, Rauchglas —, davon gilt genau eine.'),
 ('Die beiden Übergangsseiten',
  '<code>/klassisch</code> (index.html) und <code>/mobil-alt</code> (mobile.html) sollten „eine '
  'Release“ bleiben. Die Release ist durch — sie können weg, sobald du sie nicht mehr brauchst. '
  'Seit die acht Themen als Auslagen gebaut sind, hängt an <code>mobile.html</code> '
  'auch nichts Einmaliges mehr.'),
 ('CI läuft — der Schutz davor fehlt noch',
  '<code>.github/workflows/tests.yml</code> lässt die 167 Tests jetzt bei jedem Push auf jedem Zweig '
  'laufen, mit Chromium, und bricht ab, sobald ein Test <b>übersprungen</b> wird — ohne Browser '
  'überspringt sich <code>test_frontend.py</code> nämlich geschlossen und ein Lauf wäre grün, ohne '
  'die Oberflächen angefasst zu haben. Offen ist nur noch das, was man im Repo nicht bauen kann: '
  '<b>eine Branch-Protection-Regel auf <code>main</code></b>, die einen roten Lauf am Merge hindert. '
  'Das sind zwei Haken in den GitHub-Einstellungen und muss von Hand gesetzt werden.'),
 ('Drei Synthesen — und die Frage ist nicht dreimal dieselbe',
  'K89 Bogen, K90 Nachtglas und K91 Rundlauf haben kein Vorbild, sondern sind die 88 davor '
  'noch einmal gelesen: <b>ein Aufbau in drei Materialien</b>. Sie teilen Maßband, '
  'Schriftleiter, Satzspiegel und Bedienreihe (<code>design/entwuerfe/src/kanon.py</code>) und '
  'unterscheiden sich nur darin, was den Stand zeigt — Haarlinie, Lichtkante, Zeiger. '
  'Deshalb ist hier <b>nicht dreimal „bauen oder streichen“</b> zu entscheiden, sondern '
  '<b>einmal, welches Material</b>: was der Kanon regelt, ist bei allen dreien schon '
  'entschieden. Wer zwei davon nimmt, hat zwei Fassungen derselben Sache — davon hat das '
  'Register genug.'),
 ('Drei Abweichungen — und die sind absichtlich unbequem',
  'K92 Schattenwurf, K93 Lesezeichen und K94 Klepsydra sind gebaut, nachdem die Synthesen '
  'zu brav ausgefallen waren. Sie teilen <b>nichts</b> miteinander und halten <b>eine</b> '
  'Regel ein: bewegt wird, was den Stand zeigt. Keines hat eine Fortschrittsleiste. '
  'Zu entscheiden ist bei jedem einzeln — und zwei Punkte darin sind ausdrücklich offen '
  'gelassen: ob der Umschlag bei K93 zeichenweise springt oder weich gleitet, und ob die '
  'Feinteilung bei K94 links oder rechts im Glas steht. <b>K93 ist der einzige Entwurf im '
  'ganzen Register ohne Bild und ohne eigene Anzeigefläche</b>.'),
]
