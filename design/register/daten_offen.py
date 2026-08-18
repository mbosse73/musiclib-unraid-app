# -*- coding: utf-8 -*-
OFFEN = [
 ('Einundvierzig Bauanleitungen sind Vorschläge, keine Entscheidungen',
  'Bei K48–K88 steht auf jeder Karte, was ich zu Spulfläche, Zuständen und Bewegung '
  '<b>vorschlage</b> — diese Blätter sind Standbilder ohne Skript, dort ist nichts abzulesen. '
  'An acht Stellen habe ich die Frage ausdrücklich offen gelassen statt sie zu entscheiden '
  '(unter anderem: drehen sich die Wickel bei K52 Mix Tape Klar, dreht sich die Spiralplatte '
  'bei K59/K60, dimmt K74 Klimaxfront im Ruhezustand auf schwarzes Glas). '
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
  '<code>.github/workflows/tests.yml</code> lässt die 164 Tests jetzt bei jedem Push auf jedem Zweig '
  'laufen, mit Chromium, und bricht ab, sobald ein Test <b>übersprungen</b> wird — ohne Browser '
  'überspringt sich <code>test_frontend.py</code> nämlich geschlossen und ein Lauf wäre grün, ohne '
  'die Oberflächen angefasst zu haben. Offen ist nur noch das, was man im Repo nicht bauen kann: '
  '<b>eine Branch-Protection-Regel auf <code>main</code></b>, die einen roten Lauf am Merge hindert. '
  'Das sind zwei Haken in den GitHub-Einstellungen und muss von Hand gesetzt werden.'),
]
