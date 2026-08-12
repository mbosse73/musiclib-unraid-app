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
2. **Ausliefern** – Eine einzige `index.html` (das ganze UI in einer Datei) plus JSON-Endpunkt.
3. **Streamen** – MP3-Dateien per HTTP-Range, damit Vor- und Zurückspulen auf dem Handy flüssig läuft.

## Installation auf unraid

Voraussetzung: Plugin **Compose Manager Plus** (von mstrhakr) aus dem Community-Apps-Store installiert.

Das Setup verzichtet bewusst auf einen Docker-Build. Statt ein eigenes Image zu bauen, wird das offizielle `python:3.12-slim` verwendet und der App-Code direkt aus `/mnt/user/appdata/musiklib` gemountet. Vorteile: kein Flash-Storage-Verbrauch, schnellere Updates (Datei austauschen reicht), keine Probleme mit Build-Contexts.

### 1. App-Dateien ablegen — per SMB

Per Windows-Explorer / macOS Finder auf den unraid-Server:

```
\\<unraid-ip>\appdata\
```

Dort einen neuen Ordner `musiklib` anlegen und vier Dateien hineinkopieren:

```
\\<unraid-ip>\appdata\musiklib\
├── app.py
├── index.html
├── mobile.html
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

## Am Handy und am iPad

Neben der Schreibtischseite liegt unter

```
http://<unraid-ip>:8080/mobil
```

eine eigene, hellere Oberfläche fürs Handy. Sie greift auf dieselbe Sammlung zu und **spielt auf dem Gerät selbst** — installiert wird nichts, es ist eine normale Webseite.

- **Wie eine App:** in Safari auf _Teilen → Zum Home-Bildschirm_. Dann liegt ein Symbol auf dem Startbildschirm und die Seite startet ohne Browserleiste. Beim nächsten Öffnen ist automatisch die aktuelle Fassung da — es gibt nichts zu aktualisieren.
- **Absichtlich keine automatische Weiterleitung:** iPad-Safari meldet sich als Schreibtisch-Browser, eine Erkennung nach Gerät ginge schief. Die Adresse `/mobil` wird also bewusst von Hand aufgerufen (bzw. einmal als Lesezeichen abgelegt).
- **Drei Reiter:** Sammlung, Suche, Jetzt läuft. Ein Titel startet die Wiedergabe und wechselt in „Jetzt läuft".
- **Die Achse am rechten Rand** ist die ganze Warteschlange: eine Marke je Titel. Daran ziehen spult — auch über Titelgrenzen hinweg. Kurzes Antippen (oder der Zähler oben rechts) klappt die Titelliste auf.
- **Farbakzent** über das Zahnrad oben rechts in der Sammlung: Messing, Petrol oder Grün. Die Wahl gilt nur für dieses Gerät und bleibt gespeichert.
- **Bewusst nicht enthalten:** Scannen, die Liste übersprungener Dateien und die Sortierwahl — das bleibt am Schreibtisch. Ohne WLAN zum NAS gibt es keine Musik; einen Offline-Betrieb kann die Seite über `http://` nicht bieten.
- Wiedergabe, Pause und Titelwechsel funktionieren auch über Sperrbildschirm und Kopfhörertasten. Öffnet man auf demselben Gerät beide Ansichten, läuft die Sitzung nahtlos weiter.

## Bedienung

- Die **Suche** filtert Alben, Interpreten und Titel gleichzeitig in Echtzeit. Wird ein Album wegen eines Titels gefunden, ist dieser Titel beim Öffnen des Albums golden markiert.
- **Alben** zeigt die Sammlung als Cover-Raster, **Interpreten** eine aufklappbare Liste. Über **Sortierung** rechts lässt sich zwischen Interpret, Albumtitel, Jahr und „Zuletzt hinzugefügt" wechseln; die Wahl bleibt gespeichert.
- Klick auf ein Album öffnet die Trackliste. Klick auf einen Titel startet die Wiedergabe. Der Rest des Albums hängt automatisch in der Warteschlange. In der Interpreten-Ansicht spielt **„Alles abspielen"** sämtliche Alben eines Interpreten am Stück.
- Der Player unten bleibt sichtbar, auch beim Stöbern. Er hat Zufallswiedergabe und einen Lautstärkeregler (am Handy ausgeblendet, dort regeln die Hardwaretasten).
- Am PC per Tastatur: **Leertaste** Wiedergabe/Pause, **←/→** 10 Sekunden springen, **n**/**p** nächster/vorheriger Titel, **s** Zufallswiedergabe, **/** springt ins Suchfeld, **Esc** schließt das Album.
- Beim erneuten Öffnen setzt die App dort fort, wo sie zuletzt war — gleicher Titel, gleiche Position, angehalten. Praktisch am Handy, wo der Tab ständig geschlossen wird.
- Auf dem Sperrbildschirm bzw. über die Medientasten funktionieren Wiedergabe, Pause und Titelwechsel.
- Wenn sich die Sammlung ändert: Knopf **„Neu scannen"** oben rechts. Der Scan läuft im Hintergrund, das UI bleibt benutzbar. Nur geänderte Dateien werden neu eingelesen, weitere Scans dauern daher meist nur Sekunden.

## Updates und Wartung

**Code-Änderungen einfach per SMB einspielen**: `app.py`, `index.html` oder `mobile.html` in `/mnt/user/appdata/musiklib/` ersetzen, dann:

- **HTML-Änderung**: nur Browser-Reload, kein Container-Neustart nötig.
- **Python-Änderung**: Container neu starten (unraid → musiklib → Restart).
- **Neue Python-Dependency in `requirements.txt`**: Container **stoppen und neu starten** (nicht nur Restart) — nur dann läuft der `pip install`-Schritt im Command wieder.

**Container-Logs anschauen** bei Problemen: In unraid auf den `musiklib`-Container klicken → **Logs**. Beim ersten Start sieht man dort den pip-install-Schritt und danach die Uvicorn-Startmeldung.

## Speicherort des Katalogs & Backup einspielen

Der komplette Katalog liegt unterhalb von `DATA_DIR` (im Compose-File auf `/app/data` gesetzt). Weil `/app` per Bind-Mount auf `/mnt/user/appdata/musiklib` zeigt, landet das beim Scannen 1:1 auf dem unraid-Dateisystem:

```
/mnt/user/appdata/musiklib/
├── app.py
├── index.html
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
