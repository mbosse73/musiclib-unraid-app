# Stand vor der Konsolidierung

Vollständige Kopie aller Dateien der App, so wie sie vor dem Zusammenlegen der
Oberflächen liefen. Zweck: ein Ordner, den man ohne Git-Kenntnisse per SMB
zurückkopieren kann, wenn nach einem Update etwas nicht stimmt.

Gleicher Stand auch als Git-Marke: `stand-vor-konsolidierung`.

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

Dazu `docker-compose.yml` sowie die Testdateien (`conftest.py`, `test_app.py`,
`test_frontend.py`, `requirements-dev.txt`), die nur lokal gebraucht werden und
nie in den Container kommen.

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
