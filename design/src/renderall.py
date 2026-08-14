from playwright.sync_api import sync_playwright
import os, designs3, d34, d35, d36, d37, d38
OUT='/home/claude/player/v3'; os.makedirs(OUT,exist_ok=True)
# Handy-Layouts mit grosser Mittel-/Unterluecke: Abstaende gleichmaessig verteilen
FIX={'19','20','22','23','24','26','27','28','29','30','31','32','33','35'}
CSS = """
.stage > div{justify-content:space-between !important}
.stage div[style*="margin-top:auto"]{margin-top:24px !important}
.stage div[style*="margin:auto 0"]{margin:24px 0 !important}
"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for (n,name,plat,w,h,html) in designs3.D:
        if plat=='iphone' and n in FIX:
            html=html.replace('</style>', CSS+'</style>',1)
        f=f'/home/claude/player/_v3_{plat}_{n}.html'
        open(f,'w').write(html)
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=2)
        pg.goto('file://'+f); pg.wait_for_timeout(120)
        pg.screenshot(path=f'{OUT}/foto{n}_{name}_{plat}.png'); pg.close()
    b.close()
print('rendered', len(os.listdir(OUT)))
