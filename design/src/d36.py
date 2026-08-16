from lib import *
from lib2 import *
from spiral import spiral_vinyl
from designs3 import add, hb, pbar

# Foto 36 — Song-Poster im SCHWARZEN Galerierahmen (Wand), Spiraltext = Albumtitel
# Auf dem Telefon ist der Rahmen entfallen: dort ist das Blatt selbst das Plakat.
WALL='#e4e2de'; FRAME='#141414'; PAPER='#ffffff'; INK='#111111'; SUB='#9a9a97'; RED='#e0453a'

def ctrl(size,ic,ring=False):
    b=f'border:2.5px solid {INK};' if ring else ''
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;{b}'
            f'display:flex;align-items:center;justify-content:center">{ic}</div>')

def bogen(w, scale=1.0):
    """Der Inhalt des Plakats: Platte, Titel, Balken, Zeiten, Tasten, Fusszeile.

    Sechs Bloecke, die als direkte Kinder einer Spalte stehen — im Rahmen tragen
    ihre eigenen Abstaende die Hoehe, ueber das ganze Blatt verteilt sie
    `justify-content:space-between` zusaetzlich auf die freie Flaeche."""
    s=lambda v: v*scale
    return f'''<div style="display:flex;justify-content:center">{spiral_vinyl(w)}</div>
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-top:{s(30):.0f}px">
          <div><div style="font-family:{SANS};font-weight:800;font-size:{s(40):.0f}px;color:{INK}">Kind of Blue</div>
            <div style="font-family:{SANS};font-size:{s(22):.0f}px;color:{SUB};margin-top:{s(6):.0f}px">Miles Davis · 1959</div></div></div>
        {pbar(38,'#e8e8e6',INK,int(s(5)),mt=int(s(24)),knob=int(s(17)),kc=INK)}
        <div style="display:flex;justify-content:space-between;font-family:{MONO};font-size:{s(17):.0f}px;color:{SUB};margin-top:{s(9):.0f}px"><span>03:24</span><span>09:22</span></div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:{s(24):.0f}px">
          {ctrl(s(40),shuffle(int(s(24)),INK))}{ctrl(s(44),prev(int(s(26)),INK))}
          {ctrl(s(72),pausei(int(s(30)),INK),True)}
          {ctrl(s(44),nexti(int(s(26)),INK))}{ctrl(s(40),repeat(int(s(24)),INK))}
          {ctrl(s(44),libicon(int(s(26)),RED))}</div>
        <div style="text-align:center;font-family:{SANS};font-size:{s(19):.0f}px;color:{INK};margin-top:{s(26):.0f}px;letter-spacing:1px">Aus meiner Sammlung — 240 Alben</div>'''

def poster(w, scale=1.0):
    """Gerahmt an der Wand — so haengt das Plakat auf dem Rechner-Blatt."""
    s=lambda v: v*scale
    return f'''<div style="background:{FRAME};padding:{s(26):.0f}px;box-shadow:0 {s(26):.0f}px {s(60):.0f}px rgba(0,0,0,.34)">
      <div style="background:{PAPER};padding:{s(40):.0f}px {s(36):.0f}px {s(34):.0f}px">
        {bogen(w, scale)}
      </div></div>'''

# Telefon: kein Rahmen, keine Wand — das Papier ist der Bildschirm.
ph=f'''<div style="position:absolute;inset:0;background:{PAPER};padding:76px 56px 64px;
  display:flex;flex-direction:column;justify-content:space-between">
  {bogen(900, 1.55)}</div>'''

pc=f'''<div style="position:absolute;inset:0;background:{WALL};display:flex;align-items:center;gap:60px;padding:44px 70px">
  <div style="flex-shrink:0">{poster(430,0.78)}</div>
  <div style="flex:1;display:flex;flex-direction:column">
    <div style="font-family:{SANS};font-size:19px;letter-spacing:5px;color:{SUB}">MEINE SAMMLUNG · 240 ALBEN</div>
    <div style="font-family:{SANS};font-weight:800;font-size:60px;color:{INK};margin-top:10px;line-height:1.05">Kind of Blue</div>
    <div style="font-family:{SANS};font-size:24px;color:{SUB};margin-top:8px">Miles Davis · Columbia, 1959</div>
    <div style="margin-top:30px">
      {''.join(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:15px 0;border-bottom:1px solid #dcdcd9;font-family:{SANS};font-size:22px;color:{INK if i==1 else SUB}"><span style="width:44px">{n}</span><span style="flex:1;text-align:left">{t}</span><span style="font-family:{MONO};font-size:19px">{d}</span></div>' for i,(n,t,d) in enumerate([('01','So What','9:22'),('02','Freddie Freeloader','9:46'),('03','Blue in Green','5:37'),('04','All Blues','11:33')]))}
    </div>
    {pbar(38,'#e0e0dd',INK,6,mt=26,knob=18,kc=INK)}
    {hb('03:24','09:46',SUB,19,MONO,1,10)}
    <div style="position:relative;display:flex;align-items:center;gap:26px;margin-top:30px;justify-content:center">
      {ctrl(46,shuffle(26,INK))}{ctrl(50,prev(28,INK))}{ctrl(86,pausei(34,INK),True)}
      {ctrl(50,nexti(28,INK))}{ctrl(46,repeat(26,INK))}
      <div style="position:absolute;right:0;top:50%;transform:translateY(-50%)">{ctrl(56,libicon(30,RED),True)}</div></div>
  </div></div>'''

add('36','Song-Poster-Schwarz','iphone',ph); add('36','Song-Poster-Schwarz','pc',pc)
