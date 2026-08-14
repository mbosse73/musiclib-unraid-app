# Musiklib

Eine minimalistische, schnelle Musikbibliothek für die eigene MP3-Sammlung. Läuft als kleiner Docker-Container auf dem NAS, scannt das Musikverzeichnis, und liefert eine einzelne HTML-Seite mit Suche und integriertem Player – aufrufbar von jedem Gerät im Netz, PC wie Handy.

Keine Datenbank. Alles, was die App weiß, liegt in `library.json`.

## Architektur in 30 Sekunden

```
┌──────────────────────────────────────────────────┐
│  unraid                                          │
│                                                  │
│   ┌────────────┐    scannt    ┌──────────────┐   │
│   │  app.py    │ ───────────▶ │  /music      │   │
│   │  FastAPI   │              │  read-only   │   │
│   └─────┬──────┘              └──────────────┘   │
│         │ schreibt                               │
│         ▼                                        │
│   ┌──────────────┐                               │
│   │ library.json │ ◀── /app/data (persistent)    │
│   │ covers/      │                               │
│   └──────────────┘                               │
│         │                                        │
│         │ HTTP :8080                             │
└─────────┼────────────────────────────────────────┘
          │
   ┌──────┴────────┐
   │ PC, Handy,    │   öffnen einfach
   │ Tablet …      │   http://<unraid-ip>:8080
   └───────────────┘
```

Der Dienst macht drei Dinge:

1. **Scannen** – `*.mp3` rekursiv unter `/music` finden, ID3-Tags (Titel, Interpret, Album, Coverbild …) per `mutagen` auslesen, in eine flache `library.json` schreiben. Cover landen als separate Dateien in `data/covers/`.
2. **Ausliefern** – Vier einzelne HTML-Dateien (je das ganze UI in einer Datei: `index.html` am Schreibtisch, `player.html` als Spieler für Handy, iPad und PC, `mobile.html` als bisherige Handy-Oberfläche unter `/mobil-alt`, `tag.html` als Spieler mit einem Knopf) plus JSON-Endpunkt.
3. **Streamen** – MP3-Dateien per HTTP-Range, damit Vor- und Zurückspulen auf dem Handy flüssig läuft.

## Installation auf unraid

Voraussetzung: Plugin **Compose Manager Plus** (von mstrhakr) aus dem Community-Apps-Store installiert.

Das Setup verzichtet bewusst auf einen Docker-Build. Statt ein eigenes Image zu bauen, wird das offizielle `python:3.12-slim` verwendet und der App-Code direkt aus `/mnt/user/appdata/musiklib` gemountet. Vorteile: kein Flash-Storage-Verbrauch, schnellere Updates (Datei austauschen reicht), keine Probleme mit Build-Contexts.

### 1. App-Dateien ablegen — per SMB

Per Windows-Explorer / macOS Finder auf den unraid-Server:

```
\\<unraid-ip>\appdata\
```

Dort einen neuen Ordner `musiklib` anlegen und fünf Dateien hineinkopieren:

```
\\<unraid-ip>\appdata\musiklib\
├── app.py
├── index.html
├── mobile.html
├── player.html
├── tag.html
└── requirements.txt
```

Falls der Share `appdata` bei dir anders heißt, in `docker-compose.yml` weiter unten in der ersten Volume-Definition die `source:`-Zeile (`/mnt/user/appdata/musiklib`) anpassen.

### 2. Musikpfad prüfen

In `docker-compose.yml` steht der Pfad zur Musiksammlung in der ausführlichen Syntax:

```yaml
- type: bind
  source: /mnt/user/Music
  target: /music
  read_only: true
```

Nur die `source:`-Zeile anpassen, falls dein Music-Share anders heißt (z. B. `/mnt/user/music` mit Kleinbuchstaben, `/mnt/user/Multimedia/Music` als verschachtelte Variante, oder ein eigener Disk-Mount-Punkt wie `/mnt/data/Daten/Medienbibliothek/Musik`). `target` und `read_only` bleiben unverändert — `/music` ist der Pfad innerhalb des Containers, den die App kennt.

### 3. Stack anlegen

In der unraid-Web-UI:

1. **Docker** → ganz unten bei **Compose** → **Add new stack**.
2. Stack-Name: `musiklib` → **Submit**.
3. Rechts neben dem neuen Stack-Eintrag das **Zahnrad** → **Edit Stack**.
4. Den Inhalt von `docker-compose.yml` einfügen → **Save Changes**.
5. Wieder das Zahnrad → **Compose Up**.

Beim ersten Start zieht Docker das `python:3.12-slim`-Image und installiert beim Hochfahren des Containers die paar Python-Pakete (FastAPI, uvicorn, mutagen — ca. 15 Sekunden). Bei späteren Container-Starts geht's schneller.

### 4. App öffnen

```
http://<unraid-ip>:8080
```

Oder im unraid-Dashboard beim `musiklib`-Container auf **WebUI** klicken — das Label dafür ist im Compose-File gesetzt.

Beim allerersten Start scannt die App automatisch. Bei einer Sammlung mit ein paar tausend Titeln dauert das ein paar Minuten. Der Punkt oben rechts in der App zeigt den Fortschritt.

## Am Handy: die bisherige Oberfläche

> **Seit der dritten Etappe der Zusammenlegung liefert `/mobil` den Spieler**
> (nächster Abschnitt) — dessen fünf Telefon-Ansichten sind genau die
> Erscheinungsbilder, die hier beschrieben sind. Die alte Oberfläche bleibt
> vorerst erreichbar, als Rückweg:

```
http://<unraid-ip>:8080/mobil-alt
```

eine eigene, hellere Oberfläche fürs Handy. Sie greift auf dieselbe Sammlung zu und **spielt auf dem Gerät selbst** — installiert wird nichts, es ist eine normale Webseite.

- **Wie eine App:** in Safari auf _Teilen → Zum Home-Bildschirm_. Dann liegt ein Symbol auf dem Startbildschirm und die Seite startet ohne Browserleiste. Beim nächsten Öffnen ist automatisch die aktuelle Fassung da — es gibt nichts zu aktualisieren.
- **Absichtlich keine automatische Weiterleitung:** iPad-Safari meldet sich als Schreibtisch-Browser, eine Erkennung nach Gerät ginge schief. Die Adresse wird also bewusst von Hand aufgerufen (bzw. einmal als Lesezeichen abgelegt).
- **Drei Reiter:** Sammlung, Suche, Jetzt läuft. Ein Titel startet die Wiedergabe und wechselt in „Jetzt läuft".
- **Die Achse am rechten Rand** ist die ganze Warteschlange: eine Marke je Titel. Daran ziehen spult — auch über Titelgrenzen hinweg. Kurzes Antippen (oder der Zähler oben rechts) klappt die Titelliste auf.
- **Einstellungen** über das Zahnrad oben rechts in der Sammlung. Sie gelten nur für dieses Gerät und bleiben gespeichert:
  - **Thema:** fünf zur Wahl. Ein Thema ist mehr als die Farbe — es bestimmt die ganze Seite „Jetzt läuft"; Sammlung und Suche bleiben, wie sie sind.
    - _Papier_ (Elfenbein und Messing): die Warteschlange steht als Achse senkrecht im rechten Rand, eine Marke je Titel.
    - _Desert Rose_ (Sand und Burgunder): das Cover sitzt in einem Passepartout, die Seite steht auf einer Mittelachse, und dieselbe Warteschlange liegt als gravierte Skala waagerecht unter dem Bild. Gespult wird dort durch Ziehen auf der Skala; eine Sprechblase nennt dabei den Titel, in dem man landet.
    - _Kissen_ (weiches Weiß): ein Laufwerk als Bild, darunter der Ausschlag des Titels als Spulleiste, große gepolsterte Tasten.
    - _Karte_ (weiße Karte über Schwarz): die verstrichene Zeit ist so groß gesetzt wie der Titel, darunter der Ausschlag in Rot, im Dunkeln die Warteschlange.
    - _Kiesel_ (Grau in Grau): der Spieler ist die Zeile, die läuft — herausgehoben aus der Liste. Wer den nächsten Titel will, tippt ihn an statt „Weiter".
    - In den letzten drei stehen oben links die **Sammlung** und oben rechts die **Suche** als Knopf.
  - **Farbakzent:** färbt Abspielknopf, Achse und Hervorhebungen. Jedes Thema bringt eigene mit — Papier: Messing, Petrol, Grün; Desert Rose: Ton, Rosé; Kissen: Nebel, Flieder; Karte: Zinnober (nur einer — dieses Thema erlaubt genau eine Farbe); Kiesel: Graphit, Stahl.
  - **Untere Leiste:** _Dauerhaft_ (Voreinstellung) oder _Bei Bedarf_. Bei Bedarf liegt sie unter dem Bildschirmrand, die Sammlung bekommt den freien Platz. Unten in der Mitte bleibt ein kurzer Strich stehen — ein Tippen darauf holt die Leiste hervor, nach der Wahl eines Reiters (oder nach ein paar Sekunden) geht sie von selbst zurück.
- **Bewusst nicht enthalten:** Scannen, die Liste übersprungener Dateien und die Sortierwahl — das bleibt am Schreibtisch. Ohne WLAN zum NAS gibt es keine Musik; einen Offline-Betrieb kann die Seite über `http://` nicht bieten.
- Wiedergabe, Pause und Titelwechsel funktionieren auch über Sperrbildschirm und Kopfhörertasten. Öffnet man auf demselben Gerät beide Ansichten, läuft die Sitzung nahtlos weiter.

## Am iPad und am Schreibtisch: der Spieler

Neben Schreibtischseite und Handyseite liegt unter

```
http://<unraid-ip>:8080/ipad      (dieselbe Seite auch unter /pc und /mobil)
```

der Spieler. Alle drei Adressen liefern dieselbe Datei — welche Ansicht passt, entscheidet nicht das Gerät, sondern man selbst. Seit der ersten Etappe der Zusammenlegung kann er alles, was auch die Schreibtischseite kann: sortieren, nach Interpreten gruppieren, neu einlesen und die übersprungenen Dateien nachsehen.

- **Zwölf Ansichten zur Wahl.** Der kleine Knopf unten rechts (oder die Taste **L**) öffnet die **Einstellungen**. Was gerade läuft, läuft beim Wechsel weiter.
- **Erst das Format, dann die Ansicht.** Ganz oben im Dialog steht *Format*: **Telefon**, **Tablet** oder **Schreibtisch**. Die Liste darunter zeigt nur die Ansichten, die für dieses Format gezeichnet **und nachgemessen** sind — jede wurde auf Telefon hoch, Tablet hoch, Tablet quer und Schreibtisch daraufhin geprüft, ob etwas über den Rand ragt und ob Abspieltaste und Bibliotheksknopf ganz im Bild sind. Zwei Fälle sind nicht an der Messung gescheitert, sondern am Hinsehen: *Werkstisch* verliert am Telefon die Titel aus seiner Liste, *Register* schiebt hochkant die Mitte der Platte aus dem Bild. Beide fehlen dort deshalb.
- **Die Filterung ist ein Rat, kein Zaun.** Der Schalter *Auch Ansichten zeigen, die für dieses Format nicht gezeichnet sind* gibt die ganze Liste wieder frei.
- **Jedes Format merkt sich seine eigene Ansicht.** Am Schreibtisch *Pult*, am iPad *Konsole* — dieselbe Datei, zwei Gedächtnisse. Ohne das änderte ein Wechsel am PC das Aussehen auf dem iPad. Eine Wahl aus der Zeit davor wird einmalig übernommen.
- **Die Adresse ist die Voreinstellung, keine Geräteerkennung.** `/ipad` startet im Format *Tablet*, `/pc` im Format *Schreibtisch*, `/mobil` im Format *Telefon*. Nur ein sehr kleiner Bildschirm sticht das: ein Telefon bleibt ein Telefon, gleich welche Adresse man tippt. Danach entscheidet allein die Wahl im Dialog.

- **Fürs Telefon sind es sechs Ansichten.** Seit der dritten Etappe sind die fünf Erscheinungsbilder der alten Handy-Oberfläche ganz normale Ansichten mit Format *Telefon*: **Papier** (Elfenbein und Messing, die Warteschlange als Achse im rechten Rand), **Desert Rose** (Sand und Burgunder, dieselbe Achse waagerecht als Skala), **Kissen**, **Karte** und **Kiesel**. Dazu kommt *Gerät*. `/mobil` liefert deshalb jetzt diese Datei.
- **Akzentfarben** gehören zur Ansicht, nicht zur Seite: Messing gibt es in *Papier*, Ton und Rosé in *Desert Rose*, und so fort. Sie stehen in den Einstellungen unter der Ansichtsliste — aber nur, wenn die gewählte Ansicht mehr als eine anbietet. *Karte* lässt genau eine Farbe zu und fragt deshalb nicht.
- **Die alte Handy-Oberfläche bleibt** unter `http://<unraid-ip>:8080/mobil-alt` erreichbar, solange sich die neue beweisen muss. Beide teilen sich Sitzung, Lautstärke, Stumm, Zufall und Fortsetzung — man kann mitten im Lied hin- und herwechseln. Deine dortige Einstellung (Thema und Akzent) wird beim ersten Öffnen der neuen Seite einmalig übernommen.

  | Ansicht | Gedacht für | Gespult wird … |
  |---|---|---|
  | **Gerät** | iPad hoch | am Drehtonarm — schwenken heißt spulen |
  | **Werkstisch** | PC | am selben Tonarm; rechts liegt die Sammlung als Textliste offen daneben |
  | **Vollbild** | iPad quer | an den Rillen der Platte; gespielte Ringe leuchten |
  | **Deck** | PC | an der Bandleiste unter der Kassette; links wächst der Wickel, rechts wird er dünner |
  | **Handgerät** | iPad quer | ebenso, nur fast randlos und mit Tasten so breit wie Daumen |
  | **Aufgeschlagen** | iPad quer | an einer Haarlinie; sonst steht fast nichts auf dem Bildschirm |
  | **Register** | PC | ebenso, dazu links die Warteschlange in Haarlinien |
  | **Bedienteil** | PC | am Metallrad — drehen; oben drei Cover als Leuchtflächen |
  | **Konsole** | iPad quer | ebenso, größeres Rad, zwei Leuchtflächen |
  | **Pult** | PC | an der Leiste unter der Platte; links Lautstärke und Titelliste |
  | **Turm** | PC | an der Leiste an der Frontplatte; die Zeiger schlagen nur aus, solange Ton läuft |
  | **Vollverstärker** | iPad quer | ebenso, alles auf einer Frontplatte statt auf zwei Geräten |

- **Bibliothek und Suche gibt es in jeder Ansicht**, immer hinter *einem* Knopf und immer als Blende über dem Gerät, nie als eigene Seite: Auswurftaste am Kassettendeck, am Rack und am Verstärker, Rasterzeichen im Weißraum, Schalter mit Lampe am Pult, Listenzeichen an den Drehreglern der Platte. Gesucht wird überall über Albumtitel, Interpret, Jahr und alle Titelnamen. Einzige Ausnahme sind **Werkstisch** und **Deck**: dort liegt die Sammlung ohnehin offen daneben, und die Suchzeile steht direkt darüber.
- **Sortieren und Gruppieren gelten überall.** In den Einstellungen unter *Sammlung*: fünf Ordnungen (Interpret, Albumtitel, Jahr auf- und absteigend, zuletzt hinzugefügt) und die Wahl zwischen *Alben* und *Interpreten*. Beides wirkt sofort in der Liste jeder Ansicht — in der Interpreten-Ansicht steht über jedem Block eine Überschrift mit einem Knopf **Alles**, der alle Alben dieses Interpreten hintereinander spielt (steht etwas im Suchfeld, spielt er genau das, was daneben steht). Die Sortierung teilt sich den Speicherplatz mit der Schreibtischseite: dort eingestellt, hier schon so vorgefunden.
- **Neu einlesen ohne Umweg über den Schreibtisch.** Ebenfalls unter *Sammlung*: Anzahl der Alben und Titel, Datum des letzten Scans, der Knopf **Neu einlesen** mit Fortschritt, und darunter — falls es welche gab — die Liste der übersprungenen, nicht lesbaren Dateien. Ausgelöst wird ein Scan **nur** über diesen Knopf; das bloße Öffnen der Seite weckt die Platte im NAS nicht. Läuft gerade ein Scan (etwa der beim ersten Containerstart), zeigt der Dialog ihn an und lädt die Sammlung danach von selbst nach. Wer dabei Musik hört, merkt vom Scan nichts.
- **Tastatur:** **Leertaste** Wiedergabe/Pause, **←/→** 5 Sekunden, **↑/↓** Lautstärke, **n**/**p** Titelwechsel, **L** Einstellungen, **Esc** schließt Bibliothek und Dialog.
- Sperrbildschirm und Medientasten bedienen dieselbe Warteschlange. Die Sitzung wird mit den beiden anderen Oberflächen geteilt: auf demselben Gerät läuft sie zwischen Schreibtisch, Handy und Spieler weiter.

## Am iPhone: das Album des Tages

Die kleinste der vier Oberflächen liegt unter

```
http://<unraid-ip>:8080/tag
```

und hat **einen einzigen Knopf**. Sie wählt nichts aus: Sie spielt das **Album des Tages** — jeden Tag ein anderes, per Zufall aus der Sammlung, den ganzen Tag lang immer wieder dasselbe. Gedacht ist sie für den Home-Bildschirm des Telefons: aufmachen, tippen, Musik.

- **Tippen heißt abspielen.** Noch einmal tippen hält an, noch einmal tippen spielt weiter. Mehr Bedienung gibt es nicht — kein Weiter, kein Zurück, kein Spulen, keine Suche.
- **Die rote Scheibe ist der Knopf** und zugleich die Anzeige: voll, solange Ton läuft; angehalten bleibt der Kreis stehen, wird aber leer. Der dünne Ring darum ist die Position im Album — ein voller Umlauf ist ein Durchlauf. Danach fängt das Album wieder von vorn an, bis der Tag um ist.
- **Unten stehen drei Zeilen:** Album, Interpret und der laufende Titel. Sonst nichts.
- **Ein anderes Album für heute:** **fünfmal kurz hintereinander** auf die Scheibe tippen. Ab dem zweiten Tippen zeigen fünf Kerben unter der Scheibe, wie weit du bist; beim fünften geht die Sonne unter und mit einem neuen Album wieder auf. Das geht **einmal am Tag** — der zweite Versuch sagt „Heute schon gewechselt".
- **Jeden Tag ein anderes, und nie zweimal dasselbe hintereinander.** Welches Album es ist, wird aus dem Datum errechnet, nicht gewürfelt: Auf zwei Geräten mit derselben Sammlung ist es am selben Tag dasselbe Album, ganz ohne Absprache. Der Wechsel kommt um Mitternacht, schneidet aber keinen laufenden Titel ab.
- **Angehalten bleibt angehalten**, auch wenn die Seite neu geladen wird: Es geht dort weiter, wo du aufgehört hast — losgespielt wird erst auf den Knopf.
- **Bewusst nicht enthalten:** Scannen, Bibliothek, Suche, Cover, Lautstärkeregler, Titelnummern, Einstellungen. Wer wählen will, nimmt `/mobil`, `/ipad` oder die Schreibtischseite. Auch *Bildschirm anlassen* hat hier keinen eigenen Schalter — die Seite befolgt, was am Handy oder im Spieler eingestellt ist.
- Sperrbildschirm und Kopfhörertasten bedienen denselben Knopf (nur Wiedergabe und Pause, nichts anderes).

## Wenn die Wiedergabe von allein aufhört

Ein Browser, der Musik von einem NAS streamt, hat drei Stellen, an denen es abreißen kann. Alle drei sind behandelt — was übrig bleibt, sind zwei Schalter.

- **Am Titelwechsel** (der häufigste Fall am iPhone). Am Ende eines Titels bekommt das Audio-Element eine neue Quelle, und iOS wertet das im Hintergrund als *neuen* Start, nicht als Fortsetzung — und weist ihn ab. Die Seiten fragen jetzt nach: solange Ton gewünscht ist und keiner läuft, alle 1,2 Sekunden erneut, und noch einmal, sobald die Seite wieder im Vordergrund ist. Eine Pause, die du selbst gedrückt hast, bleibt davon unberührt.
- **Mitten im Titel**, wenn der Stream hängt (WLAN gedrosselt, Platte im NAS eingeschlafen). Bleibt das Element stehen, wird die Quelle nach ein paar Sekunden an derselben Stelle neu geladen — bis zu fünfmal. Zusätzlich wird 25 Sekunden vor dem Ende der Anfang des nächsten Titels schon geholt: das weckt die Platte und hält die Verbindung warm.
- **Am Ende des Albums.** Eine Warteschlange ist ein Album; bisher war danach Schluss. Jetzt läuft standardmäßig das **nächste Album der Sammlung** weiter. Einstellbar in drei Stufen — am Handy unter *Einstellungen → Am Ende der Warteschlange*, im Spieler in den Einstellungen, am Schreibtisch über den Knopf rechts neben ▶ (Weiter · Wdh. · Halt). Die Wahl gilt für diese drei Oberflächen; `/tag` fragt nicht danach, dort ist das Ende des Albums immer der Anfang desselben Albums.

Bleibt es trotzdem stehen, hilft **Bildschirm anlassen** (am Handy wie im Spieler in den Einstellungen): Solange Musik läuft, bleibt der Bildschirm an — und damit auch das WLAN auf voller Leistung. Das kostet Akku und wirkt nur, solange die Seite sichtbar ist; iOS gibt die Sperre frei, sobald du die App verlässt. Braucht iOS 16.4 oder neuer.

## Bedienung

- Die **Suche** filtert Alben, Interpreten und Titel gleichzeitig in Echtzeit. Wird ein Album wegen eines Titels gefunden, ist dieser Titel beim Öffnen des Albums golden markiert.
- **Alben** zeigt die Sammlung als Cover-Raster, **Interpreten** eine aufklappbare Liste. Über **Sortierung** rechts lässt sich zwischen Interpret, Albumtitel, Jahr und „Zuletzt hinzugefügt" wechseln; die Wahl bleibt gespeichert.
- Klick auf ein Album öffnet die Trackliste. Klick auf einen Titel startet die Wiedergabe. Der Rest des Albums hängt automatisch in der Warteschlange. In der Interpreten-Ansicht spielt **„Alles abspielen"** sämtliche Alben eines Interpreten am Stück.
- Der Player unten bleibt sichtbar, auch beim Stöbern. Er hat Zufallswiedergabe und einen Lautstärkeregler (am Handy ausgeblendet, dort regeln die Hardwaretasten).
- Am PC per Tastatur: **Leertaste** Wiedergabe/Pause, **←/→** 10 Sekunden springen, **n**/**p** nächster/vorheriger Titel, **s** Zufallswiedergabe, **/** springt ins Suchfeld, **Esc** schließt das Album.
- Beim erneuten Öffnen setzt die App dort fort, wo sie zuletzt war — gleicher Titel, gleiche Position, angehalten. Praktisch am Handy, wo der Tab ständig geschlossen wird.
- Auf dem Sperrbildschirm bzw. über die Medientasten funktionieren Wiedergabe, Pause und Titelwechsel.
- Wenn sich die Sammlung ändert: Knopf **„Neu scannen"** oben rechts — oder unter `/ipad` bzw. `/pc` in den Einstellungen (**L**) der Knopf **Neu einlesen**. Der Scan läuft im Hintergrund, das UI bleibt benutzbar. Nur geänderte Dateien werden neu eingelesen, weitere Scans dauern daher meist nur Sekunden.

## Updates und Wartung

**Code-Änderungen einfach per SMB einspielen**: `app.py`, `index.html`, `mobile.html`, `player.html` oder `tag.html` in `/mnt/user/appdata/musiklib/` ersetzen, dann:

- **HTML-Änderung**: nur Browser-Reload, kein Container-Neustart nötig.
- **Eine Adresse antwortet mit „liegt nicht im Ordner der App"**: genau das steht dann auch da — die genannte Datei fehlt neben `app.py` und wird nachkopiert, mehr ist nicht zu tun. `/` läuft in diesem Fall weiter, weil `index.html` ja da ist. Kommt stattdessen ein nacktes `{"detail":"Not Found"}`, ist die Adresse selbst unbekannt: dann läuft im Container noch ein älteres `app.py`.
- **Python-Änderung**: Container neu starten (unraid → musiklib → Restart).
- **Neue Python-Dependency in `requirements.txt`**: Container **stoppen und neu starten** (nicht nur Restart) — nur dann läuft der `pip install`-Schritt im Command wieder.

**Container-Logs anschauen** bei Problemen: In unraid auf den `musiklib`-Container klicken → **Logs**. Beim ersten Start sieht man dort den pip-install-Schritt und danach die Uvicorn-Startmeldung.

## Speicherort des Katalogs & Backup einspielen

Der komplette Katalog liegt unterhalb von `DATA_DIR` (im Compose-File auf `/app/data` gesetzt). Weil `/app` per Bind-Mount auf `/mnt/user/appdata/musiklib` zeigt, landet das beim Scannen 1:1 auf dem unraid-Dateisystem:

```
/mnt/user/appdata/musiklib/
├── app.py
├── index.html                 ← /
├── mobile.html                ← /mobil-alt (bisherige Handy-Oberfläche)
├── player.html                ← /mobil, /ipad und /pc
├── tag.html                   ← /tag
├── requirements.txt
└── data/                      ← DATA_DIR, wird beim ersten Start automatisch angelegt
    ├── library.json           ← der Katalog: Alben, Interpreten, Titel
    ├── tracks.json            ← interne Zuordnung Track-ID → Dateipfad (fürs Streaming)
    ├── tagcache.json          ← intern: gelesene Tags je Datei, macht weitere Scans schnell
    └── covers/
        └── <hash>.jpg / .png  ← Coverbilder, eine Datei pro Album
```

Coverbilder kommen bevorzugt aus dem MP3 selbst. Enthält kein einziger Titel eines Albums ein eingebettetes Bild, sucht die App im selben Ordner nach `cover.jpg`, `folder.jpg`, `front.jpg` oder `albumart.jpg` (auch als `.png`).

Die MP3-Dateien selbst werden nie kopiert oder verändert (`/music` ist `read_only`) — `library.json` verweist nur auf ihre Pfade. Der gesamte `data/`-Ordner ist deshalb typischerweise nur wenige MB groß, auch bei tausenden Titeln.

**Backup**: Da Code und Daten zusammen unter `/mnt/user/appdata/musiklib` liegen, reicht es, diesen einen Ordner zu sichern — z. B. mit dem Plugin **CA Appdata Backup / Restore** aus dem Community-Apps-Store, das die meisten unraid-Nutzer ohnehin für alle Container-Appdata-Ordner laufen lassen. Ein separates Backup-Setup nur für Musiklib ist nicht nötig.

**Backup zurückspielen**:

1. Container stoppen (unraid → `musiklib` → **Stop**).
2. Den gesicherten `musiklib/`-Ordner (inklusive `data/`) zurück nach `/mnt/user/appdata/` kopieren und den vorhandenen Ordner dabei überschreiben.
3. Container wieder starten (**Start** bzw. **Compose Up**).

Da `data/library.json` nach dem Restore bereits existiert, löst die App **keinen** automatischen Re-Scan aus (der läuft nur, wenn diese Datei fehlt) — der wiederhergestellte Katalog erscheint sofort. Hat sich die Musiksammlung seit dem Backup geändert, oben rechts auf **„Neu scannen"** klicken.

**Katalog verwerfen und neu aufbauen**: `library.json` enthält keine manuellen Eingaben, nur aus ID3-Tags abgeleitete Daten. Es reicht daher, den `data/`-Ordner zu löschen und den Container neu zu starten — der Katalog wird beim nächsten Start automatisch neu aus der Musiksammlung aufgebaut.

Für den Alltag ist das aber selten nötig: Ein normaler Scan räumt Coverbilder verschwundener Alben von selbst weg und übernimmt ausgetauschte Cover. Nur wenn wirklich alles von Grund auf neu soll, den Ordner löschen.

## Troubleshooting

**Container startet endlos neu (Status: restarting)**
Logs anschauen. Häufigste Ursachen:
- `app.py` oder `requirements.txt` fehlt unter `/mnt/user/appdata/musiklib`
- Tippfehler in `requirements.txt`
- Internet auf dem NAS war beim ersten Start nicht da → pip konnte die Pakete nicht laden → einfach nochmal `Compose Up`

**`invalid volume specification ... mount path must be absolute`**
Beim Anpassen des Music-Pfads wurde die Volume-Definition zu kurz. In der ausführlichen Syntax (so wie in der mitgelieferten Datei) gehören drei Zeilen zusammen: `source:` (Pfad auf dem NAS), `target:` (immer `/music`) und `read_only: true`. Es darf nur die `source:`-Zeile geändert werden.

**App findet keine MP3s, scan zeigt 0 Titel**
Der Pfad zum Music-Share stimmt nicht. In `docker-compose.yml` die Volume-Zeile `/mnt/user/Music:/music:ro` prüfen. Auf der unraid-Konsole testen mit:
```
ls /mnt/user/Music
```
Wenn das leer ist, ist `Music` nicht der richtige Sharename.

Ein bereits aufgebauter Katalog geht dabei **nicht** verloren: Findet ein Scan das Musikverzeichnis nicht oder keine einzige MP3 darin, bricht er ab, ohne `library.json` zu überschreiben, und zeigt oben rechts eine Meldung statt „Bereit". Die Bibliothek bleibt also sichtbar, bis der Pfad wieder stimmt. Wer die Bibliothek wirklich leeren will, löscht den Ordner `data/`.

**Oben rechts steht „Bereit — n Datei(en) übersprungen"**
So viele Dateien konnten nicht gelesen werden und fehlen in der Bibliothek — meist defekte Downloads oder Dateien, die nur `.mp3` heißen. Welche es sind, steht im Container-Log (unraid → `musiklib` → **Logs**), eine Zeile pro Datei.

**Beim `Compose Up`: `top-level object must be a mapping`**
Die `docker-compose.yml` wurde wahrscheinlich über den Stack-Editor verändert (Sonderzeichen, Quotes weg). Lösung: Inhalt nochmal sauber aus der Originaldatei einkopieren.

**Logs zeigen `ModuleNotFoundError: No module named 'fastapi'`**
Der pip-install-Schritt ist nicht durchgelaufen. Den Container einmal stoppen und neu starten (nicht Restart) — beim erneuten Hochfahren läuft das Command wieder vom Anfang.

## Was die App _nicht_ macht

Bewusst weggelassen, damit es schlicht bleibt:

- Keine Playlisten, keine Benutzerkonten, kein „Zuletzt gespielt".
- Kein automatischer Re-Scan im Hintergrund (würde im Leerlauf das NAS unnötig aufwecken). Re-Scan ist manuell.
- Keine Lyrics, keine Empfehlungen, kein „Discover".
- Keine HTTPS-Auslieferung — wenn die App von außerhalb des Heimnetzes erreichbar sein soll, einen Reverse Proxy (SWAG, Caddy, Traefik) davor setzen.

## Erweitern

Da die UI eine einzige `index.html` ist, lässt sie sich problemlos selbst anpassen — Schriftarten, Farben, Layout sind über CSS-Variablen ganz oben in `<style>` zentralisiert. Die Backend-Logik ist gut 300 Zeilen Python und behandelt nur das Nötigste.

Für Änderungen gibt es eine Testsuite, die lokal läuft und nie im Container landet:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m playwright install chromium   # einmalig, für die Frontend-Tests
.venv/bin/python -m pytest -q
```

Sie prüft das Backend im Prozess und das Frontend in einem echten Browser und braucht dafür keine eigenen MP3s — die Testdateien erzeugt sie selbst. Ohne installierten Browser überspringt sie den Frontend-Teil und läuft trotzdem durch.
