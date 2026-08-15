# Arbeitsauftrag: Player-Designs im musiclib-Repo umsetzen

Adressiert an den umsetzenden Agenten bzw. die Entwicklerin. Das Paket liegt unter
`musicplayer-designs/`. Verbindliche Quelle sind die Dateien in `html/`, die PNGs in
`previews/` dienen dem visuellen Abgleich.

---

## 0. Zuerst klären (nicht raten)

Dieses Paket ist bewusst **stack-neutral**. Vor der Umsetzung im Repo prüfen:

- Welches Framework nutzt musiclib (React / Vue / Svelte / SwiftUI / plain)?
- Gibt es bereits ein Design-System, Theme-Tokens oder eine Komponentenbibliothek?
- Wie sieht das Datenmodell aus (Track, Album, Artist, Playlist, Queue)?
- Woher kommen Wiedergabestatus und Fortschritt (eigener Player-Store? `<audio>`? MediaSession?)

Erst danach entscheiden, ob Entwürfe als Themes eines gemeinsamen Players oder als
eigenständige Skins umgesetzt werden (Empfehlung siehe Abschnitt 2).

---

## 1. Empfohlenes Vorgehen

1. **Einen Entwurf als Pilot wählen.** Der Eigentümer hat entschieden:
   `foto35_Music-Sounds-Better` (reduziert, typografisch) — siehe `AUSWAHL.md`.
2. Den Piloten sauber in Komponenten zerlegen (Abschnitt 3) und mit echten Daten verbinden.
3. Erst wenn der Pilot steht, weitere Entwürfe als **Themes** ergänzen — nicht alle zwölf auf
   einmal.

---

## 2. Architekturvorschlag: ein Player, viele Skins

Die Konzepte unterscheiden sich stark in Optik, aber kaum in Funktion. Sie teilen
dieselben Bausteine. Deshalb:

- **Ein** Player-Kern (Zustand, Queue, Transport, Fortschritt) — frei von Optik.
- **Skins** liefern nur Layout und Tokens. Ein Skin bekommt die gleichen Props und
  entscheidet, wie er sie anordnet.
- Skins sind austauschbar (Einstellung „Erscheinungsbild"), nicht alternative Codepfade.

Grober Zuschnitt:

```
PlayerProvider          Zustand: track, queue, position, duration, isPlaying, shuffle, repeat
  usePlayer()           Aktionen: play, pause, next, prev, seek, toggleShuffle, toggleRepeat
  <PlayerSkin name>     wählt das Skin, reicht Zustand + Aktionen durch
```

---

## 3. Wiederkehrende Bausteine (in allen Entwürfen)

| Baustein | Aufgabe | Anmerkung zur Umsetzung |
|---|---|---|
| `TransportBar` | Zurück / Play / Pause / Weiter | Play und Pause sind in einigen Entwürfen getrennte Tasten, in anderen eine umschaltende |
| `ProgressBar` | Position, Dauer, Springen | Klick und Ziehen; Zeiten links/rechts |
| `TimeLabels` | verstrichen / gesamt | einheitlich `m:ss` |
| `TrackList` | Titelliste mit Markierung des laufenden Titels | Zeilen sind anklickbar |
| `LibraryAction` | Sprung in die Bibliothek | **Pflicht in jedem Skin**, Form je Skin (siehe `SPEC.md`) |
| `NowPlaying` | Titel, Interpret, Album | Textlängen begrenzen, Umbruch bedenken |
| `ArtVisual` | Schallplatte / Kassette / Spule / Cover | inline SVG, per Token einfärbbar |

Optional, nur in manchen Skins: `VUMeter`, `Waveform`, `TuningScale`, `Knob`, `LcdDisplay`,
`SpeakerGrille`, `SegmentArc`.

---

## 4. Zustände, die die Entwürfe noch nicht zeigen

Die Entwürfe zeigen jeweils **einen** Moment. Für die Umsetzung fehlen und sind zu ergänzen:

- Play ↔ Pause als sichtbarer Wechsel derselben Fläche
- Fokus- und Hover-Zustände aller Bedienelemente
- Aktiv/Inaktiv für Shuffle und Repeat (inkl. „Titel wiederholen")
- Ladezustand und Fehlerfall (Datei fehlt, Format nicht unterstützt)
- Leere Bibliothek / leere Warteschlange
- Sehr lange Titel und Interpretennamen (Kürzung oder Lauftext)

---

## 5. Barrierefreiheit — bitte nicht überspringen

Die Entwürfe sind rein visuell. Bei der Umsetzung mindestens:

- Alle Bedienelemente als echte `<button>` mit sprechendem, übersetztem Label
  (nicht nur ein Icon): „Abspielen", „Pause", „Nächster Titel", „Bibliothek öffnen".
- Fortschrittsbalken als `role="slider"` mit `aria-valuenow` / `aria-valuemin` /
  `aria-valuemax` und Bedienbarkeit per Pfeiltasten.
- Sichtbarer Fokusring — mehrere Skins sind sehr kontrastarm gestaltet.
- Kontraste prüfen. Wo ein Skin dunkles Grau auf Schwarz setzt, liegt das als reine Deko
  unter 4,5:1. Für Text, der gelesen werden muss, dort nachschärfen.
- `prefers-reduced-motion` beachten, falls Laufschrift oder rotierende Platte animiert wird.

---

## 6. Maßstab und Einheiten

Die HTML-Dateien sind in **Gerätepixeln der Bühne** ausgelegt:

- iPhone-Entwürfe: 1080 × 2340 (entspricht 3× von 360 × 780 dp)
- PC-Entwürfe: 1600 × 1000 (1× Desktop)

Für die Umsetzung Werte durch 3 teilen (Mobil) bzw. direkt übernehmen (Desktop) und in
`rem`/`pt` überführen. Nicht die Pixelwerte hart übernehmen.

---

## 7. Was inhaltlich bleiben muss

- **Der Bibliotheks-Zugang** ist in jedem Skin vorhanden und darf beim Vereinfachen nicht
  wegfallen. Bei Geräte-Skins ist er als Eject-Taste in die Tastenreihe integriert.
- **Keine echten Songtexte** in den Poster-Skins (36, 37). Dort läuft eine Folge von
  Albumtiteln durch die Rille. Wird die Spirale mit Nutzerdaten befüllt, dürfen es
  Albumtitel, Interpreten oder eigene Texte sein — keine lizenzierten Liedtexte.
- Alle gezeigten Titel, Interpreten und Zeiten sind **Platzhalter** und gegen echte
  Bibliotheksdaten zu tauschen.

---

## 8. Abnahme

Ein umgesetzter Skin gilt als fertig, wenn:

- er neben dem passenden PNG aus `previews/` bei gleicher Breite optisch übereinstimmt,
- Transport, Springen im Titel und der Bibliotheks-Zugang funktionieren,
- die Zustände aus Abschnitt 4 abgedeckt sind,
- Tastaturbedienung und Screenreader-Labels aus Abschnitt 5 sitzen.
