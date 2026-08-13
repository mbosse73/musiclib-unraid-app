"""Baut aus mockups/player/ eine einzelne, in sich geschlossene HTML-Datei:
   _seite.css und _demo.js eingebettet, Vorlagenfotos als data:-URI verkleinert,
   IDs je Blatt eindeutig gemacht, damit alle dreizehn auf einer Seite laufen."""
import base64, io, pathlib, re, urllib.parse
from PIL import Image

QUELLE = pathlib.Path('/home/user/musiclib-unraid-app/mockups/player')
FOTOS  = pathlib.Path('/home/user/musiclib-unraid-app/mckups_player')
ZIEL   = pathlib.Path('/home/user/musiclib-unraid-app/mockups/player/alle-blaetter.html')

def daten_uri(pfad, breite=760):
    im = Image.open(pfad).convert('RGB')
    im.thumbnail((breite, breite * 2), Image.LANCZOS)
    puffer = io.BytesIO()
    im.save(puffer, 'JPEG', quality=72, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(puffer.getvalue()).decode()

bilder = {}
for f in FOTOS.glob('*.png'):
    bilder[f.name] = daten_uri(f)
print('Fotos eingebettet:', len(bilder), 'Summe',
      sum(len(v) for v in bilder.values()) // 1024, 'kB')

def bild_ersetzen(text):
    def ersatz(m):
        name = urllib.parse.unquote(m.group(1))
        return 'src="' + bilder.get(name, '') + '"'
    return re.sub(r'src="\.\./\.\./mckups_player/([^"]+)"', ersatz, text)

blaetter = sorted(QUELLE.glob('[0-9][0-9]-*.html'))
stile, koerper, skripte, verzeichnis = [], [], [], []

for f in blaetter:
    roh = f.read_text()
    nr = f.name[:2]
    titel = re.search(r'<title>(.*?)</title>', roh).group(1)
    stil  = re.search(r'<style>(.*?)</style>', roh, re.S).group(1)
    rumpf = re.search(r'</style>\s*(<div class="seite">.*?</div>)\s*<script src="_demo\.js">', roh, re.S)
    rumpf = rumpf.group(1)
    skript = re.findall(r'<script>\n?(.*?)</script>', roh, re.S)[-1]

    # IDs eindeutig machen
    for kennung in ('v1', 'v2', 'w1', 'w2'):
        rumpf  = rumpf.replace(f'id="{kennung}"', f'id="b{nr}{kennung}"')
        skript = skript.replace(f"getElementById('{kennung}')", f"getElementById('b{nr}{kennung}')")

    # Rückverweise auf die Übersicht dieser Seite
    rumpf = rumpf.replace('href="index.html"', 'href="#verzeichnis"')
    rumpf = bild_ersetzen(rumpf)

    # Der Kopf jedes Blattes wird zum Anker
    rumpf = rumpf.replace('<div class="seite">',
                          f'<div class="seite blatt-abschnitt" id="blatt{nr}">', 1)

    stile.append(f'/* ── Blatt {nr} ── */\n' + stil)
    koerper.append(rumpf)
    skripte.append(f'/* ── Blatt {nr} ── */\n(() => {{\n{skript}\n}})();')
    name = re.sub(r'^\d\d · ', '', titel)
    verzeichnis.append((nr, name))

seite_css = (QUELLE / '_seite.css').read_text()
demo_js   = (QUELLE / '_demo.js').read_text().replace("'use strict';", '', 1)

# Übersicht aus index.html übernehmen (Text und Tafel), Verweise auf Anker umbiegen
index = (QUELLE / 'index.html').read_text()
index_stil   = re.search(r'<style>(.*?)</style>', index, re.S).group(1)
index_rumpf  = re.search(r'</style>\s*(<div class="seite">.*?</div>)\s*<script>', index, re.S).group(1)
index_skript = re.findall(r'<script>\n?(.*?)</script>', index, re.S)[-1]
index_skript = index_skript.replace('href="${nr}-${datei}.html"', 'href="#blatt${nr}"')
index_skript = index_skript.replace(
    'src="../../mckups_player/Bildschirmfoto%202026-08-13%20um%20${foto}.png"',
    'src="${BILDER[foto]}"')
index_rumpf = bild_ersetzen(index_rumpf)
index_rumpf = index_rumpf.replace('<div class="seite">', '<div class="seite" id="verzeichnis">', 1)

bilder_js = 'const BILDER = {' + ','.join(
    f'"{n.split("um ")[1].replace(".png","")}":"{v}"' for n, v in bilder.items()) + '};'

zusatz = """
/* ── Bündel: alle Blätter auf einer Seite ── */
.blatt-abschnitt{border-top:1px solid var(--line-2);margin-top:70px;padding-top:10px}
.nachoben{position:fixed;right:22px;bottom:22px;z-index:900;background:var(--paper);
  border:1px solid var(--line-2);border-radius:2px;padding:9px 15px;font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink-2);text-decoration:none;
  box-shadow:0 6px 20px rgba(36,30,24,.16)}
.nachoben:hover{color:var(--ink)}
@media print{.nachoben{display:none}}
"""

RUMPF = f"""
<title>Musiklib Spieler-Entwürfe</title>
<style>
{seite_css}
{index_stil}
{zusatz}
{"".join(stile)}
</style>
{index_rumpf}
{"".join(koerper)}
<a class="nachoben" href="#verzeichnis">↑ Übersicht</a>
<script>
'use strict';
{bilder_js}
{demo_js}
{index_skript}
{"".join(skripte)}
</script>
"""

# 1. eigenständige Datei (im Repo, zum Doppelklicken)
ZIEL.write_text('<!doctype html>\n<html lang="de"><head><meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
                + RUMPF.replace('</style>', '</style></head><body>', 1)
                + '</body></html>\n')
# 2. Fassung fürs Veröffentlichen (Gerüst kommt von außen)
pathlib.Path('/tmp/claude-0/-home-user-musiclib-unraid-app/'
             'fa937d59-b63b-5343-95a6-cb8e0b7803a8/scratchpad/artefakt.html').write_text(RUMPF)
print('geschrieben:', ZIEL, round(ZIEL.stat().st_size / 1024 / 1024, 2), 'MB')
