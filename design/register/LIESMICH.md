# Das Konzeptregister

Alle 91 Konzepte auf einem Blatt: je eine Karte mit Aufnahmen, Herkunft,
Formaten, Stand und Bauanleitung, dazu Filter, Suche und eine Lupe. Es ist die
Übersicht über alles, was für diese App je entworfen wurde — gebaut,
gezeichnet, geliefert, selbst gemacht — und zuletzt aus allem davor
zusammengezogen.

Das Register ist **kein Teil der App**. Der Container liefert es nicht aus, die
Tests fassen es nicht an; es ist Werkzeug für Entscheidungen.

## Bauen

```bash
.venv/bin/python design/register/aufnahmen.py   # ~6 min, braucht Pillow + Playwright
python3 design/register/bauen.py                # → konzeptregister.html
python3 design/register/anleitung.py            # → ../BAUANLEITUNG.md
```

`aufnahmen.py` ist der teure Schritt und nur nötig, wenn sich ein Entwurf oder
eine Auslage geändert hat. Wer bloß einen Text im Register korrigiert, baut nur
neu. Beide Bauskripte laufen von überall — sie leiten ihre Pfade aus
`__file__` ab.

Den Browser findet `aufnahmen.py` selbst; `MUSIKLIB_CHROME=/pfad/zu/chrome`
setzt ihn von Hand, dieselbe Variable wie in `test_frontend.py`.

## Was hier liegt

| Datei | Was |
|---|---|
| `daten_gruppen.py` | `GRUPPEN` — die fünf Gruppen und ihre Einträge, in Registerreihenfolge. **Die Nummern K01–K91 stehen nirgends: sie werden beim Bauen gezählt.** Wer einen Eintrag einfügt, verschiebt alle folgenden. |
| `daten_bau.py` | `BAU` — je Konzept Spulfläche, Zustände, Bewegung, Bibliothek. Geschlüsselt über die **erste Bildkennung**, nicht über den Namen: „Emaille" ist ein Blatt *und* eine Auslage. |
| `daten_offen.py` | `OFFEN` — was noch zu entscheiden ist, als Liste unter den Karten. |
| `bauen.py` | baut `konzeptregister.html`, Bilder inline als data-URI. |
| `anleitung.py` | baut `../BAUANLEITUNG.md` aus **denselben** Daten. |
| `aufnahmen.py` | nimmt alle 160 Bilder nach `kb/` auf. |
| `sammlung.py` | die Testsammlung dafür — 12 Alben, 107 Titel. |
| `kb/` | die Aufnahmen, gut 8 MB. Erzeugt, aber eingecheckt: sonst kostet jede Registeransicht sechs Minuten Aufnahme. |

`konzeptregister.html` ist **nicht** eingecheckt (siehe `.gitignore`): 10,8 MB,
in denen dieselben Bilder ein zweites Mal stecken, und bei jedem Bau ein neuer
Blob. Was das Register ausmacht — Texte, Reihenfolge, Aufnahmen — liegt hier
vollständig; die Seite ist daraus in Sekunden wieder da.

## Die Testsammlung ist Teil des Entwurfs

`sammlung.py` baut zwölf Alben mit fünf bis zwölf Titeln. Das ist kein Zufall:
mit vier Titeln je Album sah jede listenbasierte Auslage halb leer aus, und
zwei Runden lang habe ich den Fehler beim Entwurf gesucht. Der Leerraum war die
Sammlung. Wer die Aufnahmen neu macht, macht sie gegen diese Sammlung —
sonst sind zwei Registerstände nicht vergleichbar.

Sie entsteht mit denselben `write_mp3()`/`frames()` aus `conftest.py`, die auch
die Tests benutzen: rohe MPEG-Rahmen, keine echten Musikdateien. `aufnahmen.py`
legt sie in einen Temp-Ordner und räumt ihn wieder weg — die echte Musik wird
nie angefasst.

## Wenn ein Konzept dazukommt

1. Eintrag in `daten_gruppen.py`, in die richtige Gruppe, an die richtige Stelle.
2. Eintrag in `daten_bau.py` unter der **ersten Bildkennung** des neuen Eintrags —
   ohne den bricht `anleitung.py` ab und nennt die Nummer.
3. Bild besorgen: entweder liegt es schon (`design/previews/`,
   `mockups/acht-themen/`) oder `aufnahmen.py` nimmt es auf. Eine Kennung, zu
   der kein `kb/<name>.jpg` gehört, lässt `bauen.py` abbrechen.
4. Beides neu bauen. Die Nummern hinter der Einfügestelle verschieben sich —
   das ist beabsichtigt und der Grund, warum in `daten_bau.py` keine steht.
5. Eine **neue Gruppe** braucht zusätzlich drei Zeilen in `bauen.py`: einen
   Eintrag in `MARKE`, eine Farbe `--s-<schluessel>` in **allen drei** Paletten
   (hell, `prefers-color-scheme:dark`, `[data-theme="dark"]`) und je eine Regel
   für `.punkt[data-status=…]` und `.karte[data-status=…]`. Fehlt die Farbe in
   nur einer Palette, ist der Punkt dort unsichtbar und die Karte trägt die
   Kante der Gruppe davor.

## Die Synthese-Gruppe ist anders zu lesen

K89–K91 (Bogen, Nachtglas, Rundlauf) haben kein Vorbild; sie sind die 88 davor
noch einmal gelesen. Was sie teilen — Maßband, Schriftleiter, Satzspiegel,
Bedienreihe — steht in `../entwuerfe/src/kanon.py`, was sie unterscheidet ist
allein die Standanzeige. Wer eine davon streicht, streicht ein Material, keinen
Entwurf; wer zwei nimmt, hat zwei Fassungen derselben Sache.
