# -*- coding: utf-8 -*-
"""design/BAUANLEITUNG.md aus denselben Daten bauen wie das Register.

Das Register (bauen.py) zeigt, wie ein Konzept aussieht; diese Datei sagt,
wie es sich bedient. Beides kommt aus daten_gruppen.py (Reihenfolge, Namen,
Herkunft, Formate) und daten_bau.py (die vier Angaben je Konzept) — wer
etwas ändert, ändert es dort und baut beides neu:

    python3 design/register/bauen.py
    python3 design/register/anleitung.py
"""
import pathlib
import re

from daten_gruppen import GRUPPEN
from daten_bau import BAU

HIER = pathlib.Path(__file__).parent
ZIEL = HIER.parent / 'BAUANLEITUNG.md'

# Der Verlässlichkeitsgrad steht hinter der Herkunft, nicht als eigene Zeile:
# er gehört zur Aussage, nicht daneben.
GRAD = {'gebaut': 'gelesen aus `player.html`.',
        'blatt': 'gelesen aus dem Blatt.',
        'vorschlag': '**Vorschlag — bitte prüfen**.'}

# Die Daten tragen die Auszeichnung des Registers, also HTML. Hier wird Markdown
# daraus — dieselben drei Sorten, die in den Texten überhaupt vorkommen.
AUSZEICHNUNG = [(r'</?b>', '**'), (r'</?i>', '*'), (r'</?code>', '`')]


def md(t):
    for muster, zeichen in AUSZEICHNUNG:
        t = re.sub(muster, zeichen, t)
    return t


KOPF = '''# Bauanleitung je Konzept

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
Bei den Paket-Blättern und den eigenen Entwürfen ist es ein **Vorschlag**:
diese Blätter sind pixelgenaue Standbilder ohne Skript, ohne Übergänge, ohne
Zustände. Dort ist nichts abzulesen, dort ist zu entscheiden.

Erzeugt aus denselben Daten wie das Register. Wer hier etwas ändert, ändert es
in `daten_bau.py` und baut beides neu.
'''

teile, nr, fehlt = [KOPF], 0, []
for status, titel, lede, hinweis, eintraege in GRUPPEN:
    teile.append(f'\n## {titel}\n')
    for name, was, herkunft, formate, schritt, ansichten in eintraege:
        nr += 1
        b = BAU.get(ansichten[0][0])
        if not b:
            fehlt.append(f'K{nr:02d} {name}')
            continue
        teile.append(
            f'### K{nr:02d} · {name}\n\n'
            f'*{herkunft} — {formate}. {GRAD[b["art"]]}*\n\n'
            f'- **Spulen** — {md(b["spulen"])}\n'
            f'- **Zustände** — {md(b["zustaende"])}\n'
            f'- **Bewegung** — {md(b["bewegung"])}\n'
            f'- **Bibliothek** — {md(b["bib"])}\n')

if fehlt:
    raise SystemExit('ohne Bauanleitung: ' + ', '.join(fehlt))

ZIEL.write_text('\n'.join(teile), encoding='utf-8')
print(ZIEL, nr, 'Konzepte,', f'{ZIEL.stat().st_size / 1024:.0f} KB')
