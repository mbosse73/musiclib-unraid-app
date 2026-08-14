from lib import *
from lib2 import *
from designs3 import add, hb, pbar

BG='#e8e0c8'; TEAL='#3d8a8a'; OR='#e0672a'; CREAM='#f2e9cf'; INK='#2b2620'; SUB='#8a7f6a'

def rays(w,h):
    cols=[TEAL,CREAM,OR,'#e8c46a',TEAL,CREAM,OR]
    s=''
    for i,c in enumerate(cols):
        x0=w*i/len(cols); x1=w*(i+1)/len(cols)
        s+=f'<path d="M {w*0.5} {h*0.42} L {x0:.0f} {h} L {x1:.0f} {h} Z" fill="{c}" opacity=".85"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="position:absolute;inset:0">{s}</svg>'

def stamp(txt,size):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{INK};color:{CREAM};'
            f'display:flex;align-items:center;justify-content:center;text-align:center;font-family:{IMPACT};'
            f'font-size:{size*0.19:.0f}px;line-height:1.05;letter-spacing:1px">{txt}</div>')

def btn(ic,lab,solid=False):
    return (f'<div style="flex:1;border:3px solid {INK};border-radius:6px;padding:18px 0;display:flex;'
            f'flex-direction:column;align-items:center;gap:8px;background:{OR if solid else CREAM}">'
            f'{ic}<span style="font-family:{IMPACT};font-size:19px;letter-spacing:2px;'
            f'color:{CREAM if solid else INK}">{lab}</span></div>')

def head(fs):
    return (f'<div style="text-align:center"><div style="font-family:{IMPACT};font-size:{fs}px;color:{INK};'
            f'letter-spacing:2px;text-shadow:3px 3px 0 {OR}">RETRO PARTY</div>'
            f'<div style="font-family:{IMPACT};font-size:{fs*0.42:.0f}px;color:{TEAL};letter-spacing:5px;'
            f'margin-top:6px">60\'s &nbsp;70\'s &nbsp;80\'s</div></div>')

ph=f'''<div style="position:absolute;inset:0;background:{BG};padding:30px">
<div style="position:relative;height:100%;border:5px solid {INK};border-radius:4px;overflow:hidden;background:{CREAM}">
  {rays(1020,2280)}
  <div style="position:relative;padding:46px 40px;height:100%;display:flex;flex-direction:column">
    {head(80)}
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-top:20px">
      {stamp('FREE<br>ENTRY',120)}
      <div style="text-align:right;font-family:{IMPACT};font-size:26px;color:{INK};letter-spacing:2px;line-height:1.4">
        ONLY THE BEST<br><span style="color:{OR}">MUSIC</span></div></div>
    <div style="display:flex;justify-content:center;margin:24px 0">{vinyl(620,OR,grooves='#e8c46a',shine=False)}</div>
    <div style="background:{CREAM};border:4px solid {INK};border-radius:6px;padding:26px 24px">
      <div style="font-family:{IMPACT};font-size:22px;letter-spacing:4px;color:{OR}">NOW SPINNING</div>
      <div style="font-family:{IMPACT};font-size:46px;color:{INK};margin-top:8px">DANCING QUEEN</div>
      <div style="font-family:{COND};font-size:24px;color:{SUB};margin-top:4px">ABBA · Arrival — 1976</div>
      {pbar(58,'#d8ceb2',OR,10,mt=20,knob=24,kc=TEAL)}
      {hb('02:48','04:52',SUB,21,COND,1,10)}
    </div>
    <div style="margin-top:18px">
      {''.join(f'<div style="display:flex;justify-content:space-between;padding:13px 16px;background:{CREAM if i==1 else "transparent"};border:3px solid {INK if i==1 else "transparent"};border-radius:5px;margin-bottom:7px;font-family:{COND};font-size:24px;color:{INK if i==1 else SUB}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:18px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('01','Le Freak','3:34'),('02','Dancing Queen','4:52'),('03','Stayin Alive','4:45')]))}
    </div>
    <div style="display:flex;gap:12px;margin-top:auto">
      {btn(prev(30,INK),'PREV')}{btn(tri(34,CREAM),'PLAY',True)}{btn(pausei(30,INK),'PAUSE')}
      {btn(nexti(30,INK),'NEXT')}{btn(libicon(30,INK),'CRATE')}</div>
  </div></div></div>'''

pc=f'''<div style="position:absolute;inset:0;background:{BG};padding:26px">
<div style="position:relative;height:100%;border:5px solid {INK};border-radius:4px;overflow:hidden;background:{CREAM}">
  {rays(1548,948)}
  <div style="position:relative;padding:34px 44px;height:100%;display:flex;gap:44px">
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center">
      {head(66)}
      <div style="margin:22px 0">{vinyl(430,OR,grooves='#e8c46a',shine=False)}</div>
      <div style="display:flex;gap:20px;align-items:center">{stamp('FREE<br>ENTRY',100)}
        <span style="font-family:{IMPACT};font-size:24px;color:{INK};letter-spacing:2px;line-height:1.4">ONLY THE BEST<br><span style="color:{OR}">MUSIC</span></span></div>
    </div>
    <div style="width:640px;display:flex;flex-direction:column;justify-content:center">
      <div style="background:{CREAM};border:4px solid {INK};border-radius:6px;padding:26px">
        <div style="font-family:{IMPACT};font-size:21px;letter-spacing:4px;color:{OR}">NOW SPINNING</div>
        <div style="font-family:{IMPACT};font-size:52px;color:{INK};margin-top:8px">DANCING QUEEN</div>
        <div style="font-family:{COND};font-size:23px;color:{SUB};margin-top:4px">ABBA · Arrival — 1976</div>
        {pbar(58,'#d8ceb2',OR,10,mt=20,knob=22,kc=TEAL)}
        {hb('02:48','04:52',SUB,20,COND,1,10)}</div>
      <div style="margin-top:16px">
        {''.join(f'<div style="display:flex;justify-content:space-between;padding:12px 16px;background:{CREAM if i==1 else "transparent"};border:3px solid {INK if i==1 else "transparent"};border-radius:5px;margin-bottom:6px;font-family:{COND};font-size:23px;color:{INK if i==1 else SUB}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:16px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('01','Le Freak','3:34'),('02','Dancing Queen','4:52'),('03','Stayin Alive','4:45'),('04','I Feel Love','5:52')]))}
      </div>
      <div style="display:flex;gap:11px;margin-top:18px">
        {btn(prev(28,INK),'PREV')}{btn(tri(32,CREAM),'PLAY',True)}{btn(pausei(28,INK),'PAUSE')}
        {btn(nexti(28,INK),'NEXT')}{btn(libicon(28,INK),'CRATE')}</div>
    </div></div></div></div>'''

add('34','Retro-Party','iphone',ph); add('34','Retro-Party','pc',pc)
