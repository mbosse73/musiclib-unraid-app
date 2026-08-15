from lib import *
from lib2 import *
from designs3 import add, hb, pbar

NAVY='#1e2a4a'; TEAL='#4aa3c4'; OR='#e8622b'; SAND='#f2e9d8'; YEL='#f0b93a'; CREAM='#faf4e6'

def bolt(x,y,s,c,rot=0):
    return (f'<svg width="{s}" height="{s*1.6:.0f}" viewBox="0 0 24 38" style="position:absolute;left:{x}px;top:{y}px;'
            f'transform:rotate({rot}deg)"><path d="M14 0 L2 21 h8 L8 38 L22 15 h-9 Z" fill="{c}"/></svg>')

def boombox(w):
    h=w*0.62
    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<path d="M {w*0.30} {h*0.20} q {w*0.20} -{h*0.22} {w*0.40} 0" stroke="{YEL}" stroke-width="{w*0.035}" fill="none" stroke-linecap="round"/>
<rect x="{w*0.06}" y="{h*0.20}" width="{w*0.88}" height="{h*0.72}" rx="{w*0.03}" fill="{TEAL}" stroke="{NAVY}" stroke-width="3"/>
<rect x="{w*0.11}" y="{h*0.28}" width="{w*0.30}" height="{h*0.10}" rx="4" fill="{SAND}" stroke="{NAVY}" stroke-width="2"/>
<rect x="{w*0.45}" y="{h*0.28}" width="{w*0.38}" height="{h*0.06}" rx="3" fill="{OR}"/>
<circle cx="{w*0.88}" cy="{h*0.31}" r="{w*0.028}" fill="{NAVY}"/>
<circle cx="{w*0.245}" cy="{h*0.62}" r="{w*0.145}" fill="{NAVY}"/>
<circle cx="{w*0.245}" cy="{h*0.62}" r="{w*0.105}" fill="none" stroke="{TEAL}" stroke-width="3"/>
<circle cx="{w*0.245}" cy="{h*0.62}" r="{w*0.055}" fill="{TEAL}"/>
<circle cx="{w*0.755}" cy="{h*0.62}" r="{w*0.145}" fill="{NAVY}"/>
<circle cx="{w*0.755}" cy="{h*0.62}" r="{w*0.105}" fill="none" stroke="{TEAL}" stroke-width="3"/>
<circle cx="{w*0.755}" cy="{h*0.62}" r="{w*0.055}" fill="{TEAL}"/>
<rect x="{w*0.42}" y="{h*0.44}" width="{w*0.16}" height="{h*0.34}" rx="4" fill="{OR}" stroke="{NAVY}" stroke-width="2"/>
<rect x="{w*0.445}" y="{h*0.50}" width="{w*0.11}" height="{h*0.13}" rx="2" fill="{SAND}"/>
<circle cx="{w*0.47}" cy="{h*0.70}" r="{w*0.012}" fill="{NAVY}"/><circle cx="{w*0.53}" cy="{h*0.70}" r="{w*0.012}" fill="{NAVY}"/>
<ellipse cx="{w*0.5}" cy="{h*0.96}" rx="{w*0.40}" ry="{h*0.035}" fill="{OR}" opacity=".45"/></svg>'''

def star(size,txt=""):
    pts=''
    import math
    for i in range(16):
        r=size/2 if i%2==0 else size*0.34
        a=math.radians(i*22.5-90)
        pts+=f'{size/2+math.cos(a)*r:.1f},{size/2+math.sin(a)*r:.1f} '
    return (f'<div style="position:relative;width:{size}px;height:{size}px">'
            f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}"><polygon points="{pts}" fill="{TEAL}"/></svg>'
            f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;'
            f'font-family:{SANS};font-weight:800;color:{NAVY};font-size:{size*0.16:.0f}px;line-height:1.1">FREE<br>'
            f'<span style="font-size:{size*0.10:.0f}px;font-weight:600">ENTRY</span></div></div>')

def btn(ic,lab,solid=False):
    return (f'<div style="flex:1;border-radius:8px;padding:18px 0;display:flex;flex-direction:column;align-items:center;'
            f'gap:8px;background:{OR if solid else CREAM};border:2px solid {NAVY}">'
            f'{ic}<span style="font-family:{SANS};font-weight:700;font-size:17px;letter-spacing:2px;'
            f'color:{CREAM if solid else NAVY}">{lab}</span></div>')

def title(fs):
    return (f'<div style="text-align:center;font-family:{SANS};font-weight:300;color:{CREAM};line-height:.95">'
            f'<div style="font-size:{fs*0.30:.0f}px;letter-spacing:3px;margin-bottom:10px">Join Us For</div>'
            f'<div style="font-size:{fs}px;letter-spacing:-1px">WORLD</div>'
            f'<div style="font-size:{fs}px;font-weight:800;color:{YEL};letter-spacing:-1px">MUSIC</div>'
            f'<div style="font-size:{fs}px;letter-spacing:-1px">DAY</div></div>')

ph=f'''<div style="position:absolute;inset:0;background:{TEAL};padding:26px">
<div style="position:relative;height:100%;background:{NAVY};overflow:hidden;display:flex;flex-direction:column">
  {bolt(40,60,70,OR,-12)}{bolt(880,40,80,CREAM,14)}{bolt(60,540,60,SAND,8)}{bolt(860,900,64,YEL,-10)}
  <div style="position:relative;flex:1.25;display:flex;align-items:center;justify-content:center;padding:0 44px">
    {title(112)}
    <div style="position:absolute;right:40px;top:56%">{star(190)}</div>
  </div>
  <div style="position:relative;flex:1;background:{OR};display:flex;align-items:center;justify-content:center">{boombox(700)}</div>
  <div style="background:{CREAM};padding:34px 40px">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid {NAVY};padding-bottom:20px">
      <div><div style="font-family:{SANS};font-weight:800;font-size:40px;color:{TEAL};letter-spacing:1px">CORAL PARK</div>
        <div style="font-family:{SANS};font-size:26px;color:{OR};letter-spacing:6px;margin-top:2px">CALIFORNIA</div></div>
      <div style="text-align:right;font-family:{SANS};color:{OR}">
        <div style="font-size:20px;letter-spacing:2px">JUNE</div>
        <div style="font-size:46px;font-weight:800;color:{TEAL};line-height:1">21</div></div></div>
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:18px">
      <div><div style="font-family:{SANS};font-size:18px;letter-spacing:3px;color:{OR}">NOW PLAYING</div>
        <div style="font-family:{SANS};font-weight:700;font-size:32px;color:{NAVY};margin-top:4px">Peach Band — Sunset Set</div></div>
      <span style="font-family:{MONO};font-size:20px;color:#8a8a86">02:12 / 04:30</span></div>
    {pbar(49,'#ded6c4',OR,9,mt=16,knob=22,kc=TEAL)}
    <div style="display:flex;gap:11px;margin-top:20px">
      {btn(prev(28,NAVY),'PREV')}{btn(tri(32,CREAM),'PLAY',True)}{btn(pausei(28,NAVY),'PAUSE')}
      {btn(nexti(28,NAVY),'NEXT')}{btn(libicon(28,NAVY),'LINE-UP')}</div>
  </div></div></div>'''

pc=f'''<div style="position:absolute;inset:0;background:{TEAL};padding:22px">
<div style="position:relative;height:100%;background:{NAVY};overflow:hidden;display:flex">
  {bolt(30,40,58,OR,-12)}{bolt(660,30,64,CREAM,14)}{bolt(40,700,52,SAND,8)}
  <div style="position:relative;width:740px;display:flex;flex-direction:column">
    <div style="position:relative;flex:1;display:flex;align-items:center;justify-content:center;padding:0 36px">
      {title(88)}
      <div style="position:absolute;right:26px;top:56%">{star(150)}</div>
    </div>
    <div style="flex:0 0 46%;background:{OR};display:flex;justify-content:center;align-items:flex-end">{boombox(520)}</div>
  </div>
  <div style="flex:1;background:{CREAM};padding:40px 44px;display:flex;flex-direction:column">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid {NAVY};padding-bottom:20px">
      <div><div style="font-family:{SANS};font-weight:800;font-size:44px;color:{TEAL};letter-spacing:1px">CORAL PARK</div>
        <div style="font-family:{SANS};font-size:24px;color:{OR};letter-spacing:6px;margin-top:2px">CALIFORNIA</div></div>
      <div style="text-align:right;font-family:{SANS}">
        <div style="font-size:19px;letter-spacing:2px;color:{OR}">JUNE</div>
        <div style="font-size:52px;font-weight:800;color:{TEAL};line-height:1">21</div>
        <div style="font-size:19px;color:{OR};margin-top:2px">START 7 PM</div></div></div>
    <div style="margin-top:22px">
      {''.join(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:15px 0;border-bottom:1px solid #e2dac8;font-family:{SANS};font-size:23px;color:{NAVY if i==0 else "#8a8a86"}"><span style="font-weight:{700 if i==0 else 400}">{t}</span><span style="font-family:{MONO};font-size:19px">{d}</span></div>' for i,(t,d) in enumerate([('Peach Band — Sunset Set','4:30'),('Hope Band — Coral Waves','3:52'),('Heart DJ — Night Drive','5:14')]))}
    </div>
    <div style="margin-top:auto">
      <div style="font-family:{SANS};font-size:18px;letter-spacing:3px;color:{OR}">NOW PLAYING</div>
      <div style="font-family:{SANS};font-weight:700;font-size:34px;color:{NAVY};margin-top:4px">Peach Band — Sunset Set</div>
      {pbar(49,'#ded6c4',OR,9,mt=16,knob=20,kc=TEAL)}
      {hb('02:12','04:30','#8a8a86',19,MONO,1,10)}
      <div style="display:flex;gap:10px;margin-top:20px">
        {btn(prev(26,NAVY),'PREV')}{btn(tri(30,CREAM),'PLAY',True)}{btn(pausei(26,NAVY),'PAUSE')}
        {btn(nexti(26,NAVY),'NEXT')}{btn(libicon(26,NAVY),'LINE-UP')}</div>
    </div></div></div></div>'''

add('38','World-Music-Day','iphone',ph); add('38','World-Music-Day','pc',pc)
