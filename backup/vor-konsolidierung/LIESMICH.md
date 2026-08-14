# Stand vor der Konsolidierung

Vollständige Kopie aller Dateien der App, so wie sie vor dem Zusammenlegen der
Oberflächen liefen. Zweck: ein Ordner, den man ohne Git-Kenntnisse per SMB
zurückkopieren kann, wenn nach einem Update etwas nicht stimmt.

Gleicher Stand in der Git-Historie: Commit **`ed0f1b0`** („neue ui") ist der
letzte, in dem die App-Dateien unverändert sind — alles danach betrifft
zunächst nur `design/` und diesen Backup-Ordner.

```bash
git show ed0f1b0:player.html > player.html      # eine Datei zurückholen
git checkout ed0f1b0 -- app.py index.html mobile.html player.html tag.html
```

## Was hier liegt

Die sechs Dateien, die im Container laufen:

| Datei | Adresse |
|---|---|
| `app.py` | Backend — Scan, API, Streaming |
| `index.html` | `/` |
| `mobile.html` | `/mobil` |
| `player.html` | `/ipad` und `/pc` |
| `tag.html` | `/tag` |
| `requirements.txt` | Abhängigkeiten, werden beim Containerstart installiert |

Dazu `docker-compose.yml`.

Die Testdateien (`conftest.py`, `test_app.py`, `test_frontend.py`,
`requirements-dev.txt`) liegen hier bewusst **nicht**: sie kommen nie in den
Container, und eine zweite Kopie im Baum bringt pytest durcheinander (es
sammelt dann denselben Modulnamen zweimal ein und bricht ab). Wer sie
braucht, holt sie aus der Historie:
`git checkout ed0f1b0 -- conftest.py test_app.py test_frontend.py`

Geprüfter Zustand dieses Stands: `pytest` → 111 Tests, alle grün
(einmal flatterte `test_session_is_restored_without_autoplay` unter Volllast,
allein ausgeführt läuft er durch — ein Zeitproblem im Test, kein Fehler in
der App).

## Zurückspielen

**Nur die Oberfläche zurück** (häufigster Fall, ein Design macht Ärger):

1. Die betreffende `.html` nach `\\<unraid-ip>\appdata\musiklib\` kopieren.
2. Im Browser neu laden. **Kein Container-Neustart nötig.**

**Alles zurück:**

1. `app.py` und alle vier `.html` nach `\\<unraid-ip>\appdata\musiklib\` kopieren.
2. unraid → Container `musiklib` → **Restart** (wegen `app.py`).

`requirements.txt` hat sich nicht geändert — ein voller Stop/Start ist also
nicht nötig, ein Restart genügt.

## Was hier bewusst NICHT liegt

Der Ordner `data/` — der gescannte Katalog (`library.json`, `tracks.json`,
`tagcache.json`, `covers/`). Der liegt ausschließlich auf der unraid unter
`/mnt/user/appdata/musiklib/data/` und wird von keiner Änderung an den
Oberflächen angefasst. Sein Backup läuft über *CA Appdata Backup / Restore*
(siehe `README.md`, Abschnitt „Speicherort des Katalogs & Backup einspielen").

Ein Zurückspielen dieses Ordners löst **keinen** neuen Scan aus: der läuft nur,
wenn `library.json` fehlt.
