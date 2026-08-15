from lib import *
from lib2 import *
from spiral import spiral_vinyl
from designs3 import add, hb, pbar

# Foto 37 — Song-Poster im WEISSEN Rahmen, an die Wand gelehnt, waermerer Ton.
# Auf dem Telefon fuellt das Plakat das ganze Blatt; der weisse Rahmen bleibt,
# er ist jetzt der Rand des Bildschirms.
WALL='linear-gradient(180deg,#efece7 0%,#e6e2db 72%,#d6d0c6 72%,#cec7ba 100%)'
FRAME='#fbfbf9'; PAPER='#ffffff'; INK='#1a1a18'; SUB='#a29e97'; RED='#e0453a'; ACC='#c9422e'

def pill(ic,lab=None,size=52,solid=False):
    t=f'<span style="font-family:{SANS};font-size:16px;letter-spacing:2px;color:{SUB}">{lab}</span>' if lab else ''
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:7px">'
            f'<div style="width:{size}px;height:{size}px;border-radius:50%;'
            f'background:{INK if solid else "transparent"};border:{"none" if solid else f"2px solid {INK}"};'
            f'display:flex;align-items:center;justify-content:center">{ic}</div>{t}</div>')

def bogen(w, scale=1.0):
    """Der Inhalt des Plakats — sechs Bloecke als direkte Kinder einer Spalte."""
    s=lambda v: v*scale
    return f'''<div style="display:flex;justify-content:center">{spiral_vinyl(w,label=RED)}</div>
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-top:{s(30):.0f}px">
          <div><div style="font-family:{SANS};font-weight:800;font-size:{s(38):.0f}px;color:{INK}">Rumours</div>
            <div style="font-family:{SANS};font-size:{s(21):.0f}px;color:{SUB};margin-top:{s(5):.0f}px">Fleetwood Mac · 1977</div></div>
          <div style="background:#fff;padding:{s(4):.0f}px">{qr(int(s(88)))}</div></div>
        {pbar(46,'#eceae6',ACC,int(s(5)),mt=int(s(22)),knob=int(s(16)),kc=ACC)}
        <div style="display:flex;justify-content:space-between;font-family:{MONO};font-size:{s(16):.0f}px;color:{SUB};margin-top:{s(8):.0f}px"><span>01:58</span><span>04:19</span></div>
        <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:{s(22):.0f}px">
          {pill(shuffle(int(s(22)),INK),None,s(38))}{pill(prev(int(s(24)),INK),None,s(42))}
          {pill(tri(int(s(28)),'#fff'),None,s(70),True)}
          {pill(nexti(int(s(24)),INK),None,s(42))}{pill(repeat(int(s(22)),INK),None,s(38))}
          {pill(libicon(int(s(24)),ACC),None,s(42))}</div>
        <div style="text-align:center;font-family:{SANS};font-size:{s(18):.0f}px;color:{SUB};margin-top:{s(24):.0f}px;letter-spacing:1px">Meine Plattensammlung · Regal B</div>'''

def poster(w, scale=1.0):
    """Gerahmt an die Wand gelehnt — so steht das Plakat auf dem Rechner-Blatt."""
    s=lambda v: v*scale
    return f'''<div style="background:{FRAME};padding:{s(30):.0f}px;border:1px solid #e2ded6;
      box-shadow:0 {s(30):.0f}px {s(56):.0f}px rgba(90,80,66,.28)">
      <div style="background:{PAPER};padding:{s(40):.0f}px {s(38):.0f}px {s(32):.0f}px">
        {bogen(w, scale)}
      </div></div>'''

# Telefon: das Plakat fuellt das Blatt. Der weisse Rahmen bleibt als Rand stehen,
# eine Haarlinie trennt ihn vom Papier — sonst faende das Auge die Kante nicht.
ph=f'''<div style="position:absolute;inset:0;background:{FRAME};padding:26px">
  <div style="height:100%;background:{PAPER};box-shadow:inset 0 0 0 1px #eae6de;
    padding:66px 50px 58px;display:flex;flex-direction:column;justify-content:space-between">
    {bogen(860, 1.48)}</div></div>'''

pc=f'''<div style="position:absolute;inset:0;background:{WALL};display:flex;align-items:center;gap:64px;padding:40px 72px">
  <div style="flex-shrink:0">{poster(410,0.76)}</div>
  <div style="flex:1;display:flex;flex-direction:column">
    <div style="font-family:{SANS};font-size:18px;letter-spacing:5px;color:{SUB}">PLATTENSAMMLUNG · REGAL B</div>
    <div style="font-family:{SANS};font-weight:800;font-size:62px;color:{INK};margin-top:10px;line-height:1.05">Rumours</div>
    <div style="font-family:{SANS};font-size:23px;color:{SUB};margin-top:8px">Fleetwood Mac · Warner Bros., 1977</div>
    <div style="margin-top:28px">
      {''.join(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid #ddd8cf;font-family:{SANS};font-size:22px;color:{INK if i==2 else SUB}"><span style="width:44px">{n}</span><span style="flex:1;text-align:left">{t}</span><span style="font-family:{MONO};font-size:19px">{d}</span></div>' for i,(n,t,d) in enumerate([('A1','Second Hand News','2:56'),('A2','Dreams','4:14'),('A3','Never Going Back Again','2:14'),('A4','Go Your Own Way','3:38')]))}
    </div>
    {pbar(46,'#dfdad1',ACC,6,mt=24,knob=18,kc=ACC)}
    {hb('01:58','04:19',SUB,19,MONO,1,10)}
    <div style="display:flex;align-items:flex-end;gap:26px;margin-top:28px">
      {pill(shuffle(24,INK),'SHUFFLE',44)}{pill(prev(26,INK),'PREV',48)}
      {pill(tri(30,'#fff'),'PLAY',82,True)}
      {pill(nexti(26,INK),'NEXT',48)}{pill(repeat(24,INK),'REPEAT',44)}
      <div style="margin-left:auto">{pill(libicon(26,ACC),'SAMMLUNG',52)}</div></div>
  </div></div>'''

add('37','Song-Poster-Weiss','iphone',ph); add('37','Song-Poster-Weiss','pc',pc)
