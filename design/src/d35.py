from lib import *
from lib2 import *
from designs3 import add, hb, pbar

BG='#ffffff'; INK='#141414'; RED='#c0272d'; SUB='#a8a8a5'; LINE='#e6e6e3'

def framebox(fs,pad):
    words=['MUSIC','SOUNDS','BETTER','WITH','YOU']
    inner=''.join(f'<div style="font-family:{SANS};font-size:{fs}px;letter-spacing:{fs*0.42:.0f}px;'
                  f'color:{INK};line-height:1.9;text-align:center;text-indent:{fs*0.42:.0f}px">{w}</div>' for w in words)
    return f'<div style="border:1.5px solid {INK};padding:{pad};display:inline-block">{inner}</div>'

def cbtn(ic,size=88,fill='#fff',bd=LINE):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{fill};border:1.5px solid {bd};'
            f'display:flex;align-items:center;justify-content:center">{ic}</div>')

def trow(n,t,d,cur=False):
    return (f'<div style="display:flex;justify-content:space-between;align-items:center;padding:17px 0;'
            f'border-bottom:1px solid {LINE};font-family:{SANS};font-size:22px;color:{INK if cur else SUB}">'
            f'<span style="letter-spacing:3px">{n}</span>'
            f'<span style="flex:1;text-align:left;margin-left:24px;letter-spacing:{3 if cur else 1}px">{t}</span>'
            f'<span style="font-family:{MONO};font-size:19px">{d}</span></div>')

ph=f'''<div style="position:absolute;inset:0;background:{BG};padding:64px 58px;display:flex;flex-direction:column;justify-content:space-between">
  <div style="display:flex;justify-content:space-between;align-items:center;font-family:{SANS};font-size:19px;
    letter-spacing:4px;color:{SUB}"><span>SIDE A · 33⅓</span><span>FLAC · 24 BIT</span></div>
  <div style="display:flex;justify-content:center;margin-top:38px">{framebox(30,'30px 46px')}</div>
  <div style="display:flex;justify-content:center;margin-top:34px">{vinyl(780,RED)}</div>
  <div style="margin-top:34px">{trow('01','Music Sounds Better','4:56',True)}{trow('02','One More Time','5:20')}{trow('03','Digital Love','4:58')}{trow('04','Around The World','7:09')}{trow('05','Da Funk','5:28')}</div>
  {pbar(52,'#ececea',RED,5,mt=26,knob=20,kc=RED)}
  {hb('02:34','04:56',SUB,20,MONO,1,12)}
  <div style="display:flex;justify-content:center;align-items:center;gap:28px;margin-top:auto;margin-bottom:8px">
    {cbtn(shuffle(26,SUB),74)}{cbtn(prev(30,INK),86)}{cbtn(tri(38,'#fff'),120,RED,RED)}
    {cbtn(nexti(30,INK),86)}{cbtn(libicon(26,RED),74)}</div>
</div>'''

pc=f'''<div style="position:absolute;inset:0;background:{BG};padding:56px 80px;display:flex;gap:80px;align-items:center">
  <div style="flex:1;display:flex;flex-direction:column;align-items:center">
    {framebox(26,'26px 40px')}
    <div style="margin-top:34px">{vinyl(470,RED)}</div>
  </div>
  <div style="flex:1;display:flex;flex-direction:column">
    <div style="font-family:{SANS};font-size:19px;letter-spacing:4px;color:{SUB}">NOW PLAYING · SIDE A</div>
    <div style="font-family:{SANS};font-size:56px;font-weight:600;color:{INK};margin-top:12px;line-height:1.1">Music Sounds<br>Better With You</div>
    <div style="font-family:{SANS};font-size:22px;color:{SUB};margin-top:10px;letter-spacing:1px">Stardust · 1998</div>
    <div style="margin-top:30px">{trow('01','Music Sounds Better','4:56',True)}{trow('02','One More Time','5:20')}{trow('03','Digital Love','4:58')}{trow('04','Around The World','7:09')}</div>
    {pbar(52,'#ececea',RED,5,mt=26,knob=18,kc=RED)}
    {hb('02:34','04:56',SUB,19,MONO,1,10)}
    <div style="display:flex;align-items:center;gap:24px;margin-top:32px">
      {cbtn(shuffle(24,SUB),68)}{cbtn(prev(28,INK),78)}{cbtn(tri(34,'#fff'),104,RED,RED)}
      {cbtn(nexti(28,INK),78)}{cbtn(libicon(24,RED),68)}</div>
  </div></div>'''

add('35','Music-Sounds-Better','iphone',ph); add('35','Music-Sounds-Better','pc',pc)
