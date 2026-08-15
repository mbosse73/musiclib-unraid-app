# -*- coding: utf-8 -*-
"""V3 — pro neuem Referenzfoto je 1 iPhone + 1 PC Entwurf.
Regeln: nah am Original, voll bedienbar (Transport, Fortschritt, Zeiten),
Bibliotheks-Zugang in jedem Entwurf (bei HiFi als Eject/Panel-Taste),
Flaeche durchgestaltet."""
from lib import *
from lib2 import *
import math
PH=(1080,2340); PC=(1600,1000)
D=[]
def add(n,name,plat,html):
    w,h = PH if plat=='iphone' else PC
    D.append((n,name,plat,w,h,doc(w,h,'',html)))

def hb(l,r,color,fs,ff=MONO,ls=2,mt=0):
    return f'<div style="display:flex;justify-content:space-between;color:{color};font-size:{fs}px;font-family:{ff};letter-spacing:{ls}px;margin-top:{mt}px"><span>{l}</span><span>{r}</span></div>'

def pbar(frac,track,fill,h=6,mt=0,knob=0,kc='#fff',square=False):
    k=''
    if knob:
        shape='' if square else 'border-radius:50%;'
        k=f'<div style="position:absolute;left:{frac}%;top:50%;transform:translate(-50%,-50%);width:{knob}px;height:{int(knob*1.25) if square else knob}px;{shape}background:{kc};box-shadow:0 2px 6px rgba(0,0,0,.35)"></div>'
    return f'<div style="position:relative;height:{h}px;background:{track};border-radius:{h/2}px;margin-top:{mt}px"><div style="height:{h}px;width:{frac}%;background:{fill};border-radius:{h/2}px"></div>{k}</div>'

# =========================================================================
# 17 · SONY Bandmaschine (Holz, Silber-Panel, cremefarbene Tasten, VU)
# =========================================================================
def d17():
    WOOD='linear-gradient(180deg,#7a5433,#4e3520)'
    SILVER='linear-gradient(180deg,#efefec,#c8c8c4 45%,#dcdcd8 55%,#a9a9a5)'
    CREAM='linear-gradient(180deg,#f3efe2,#ddd7c4)'
    def deckbtn(ic,lab,active=False):
        return f'''<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:8px">
        <div style="width:100%;aspect-ratio:1.15;border-radius:8px;background:{CREAM};border:2px solid #9a958a;box-shadow:0 4px 0 #9a958a,0 7px 10px rgba(0,0,0,.35),inset 0 2px 2px #fff;display:flex;align-items:center;justify-content:center">{ic}</div>
        <span style="font-size:19px;color:#4a4a46;letter-spacing:1px;font-family:{SANS}">{lab}</span></div>'''
    def reelpair(s,gap):
        return f'<div style="display:flex;gap:{gap}px;justify-content:center">{bigreel(s)}{bigreel(s)}</div>'
    def headblock(w):
        return f'''<div style="background:{SILVER};border-radius:8px;padding:14px 26px;box-shadow:0 4px 10px rgba(0,0,0,.3),inset 0 2px 2px #fff;text-align:center;width:{w}px">
        <div style="font-family:{SANS};font-weight:700;letter-spacing:6px;font-size:26px;color:#2e2e2c">SONY</div>
        <div style="font-family:{SANS};font-size:15px;letter-spacing:2px;color:#6a6a66;margin-top:2px">CLOSED LOOP DUAL CAPSTAN</div></div>'''
    vus=lambda w,h:f'<div style="display:flex;gap:16px">{vumeter(w,h,"#f0e6c2","#2a2a26","#5a5a52","L",0.58)}{vumeter(w,h,"#f0e6c2","#2a2a26","#5a5a52","R",0.70)}</div>'
    ph=f'''<div style="position:absolute;inset:0;background:{WOOD};padding:30px">
      <div style="height:100%;background:{SILVER};border-radius:12px;padding:34px 30px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:inset 0 3px 6px #fff,0 10px 30px rgba(0,0,0,.5)">
        <div style="display:flex;justify-content:center">{reelpair(468,26)}</div>
        <div style="display:flex;justify-content:center;align-items:center;gap:24px;margin-top:26px">
          <div style="width:74px;height:74px;border-radius:50%;background:radial-gradient(circle at 38% 32%,#fff,#c2c2be 60%,#8e8e8a);box-shadow:0 4px 8px rgba(0,0,0,.35)"></div>
          {headblock(430)}
          <div style="width:74px;height:74px;border-radius:50%;background:radial-gradient(circle at 38% 32%,#fff,#c2c2be 60%,#8e8e8a);box-shadow:0 4px 8px rgba(0,0,0,.35)"></div></div>
        <div style="background:#1c1c1a;border-radius:8px;padding:14px 22px;margin-top:26px;display:flex;justify-content:space-between;align-items:center;box-shadow:inset 0 3px 8px #000">
          <span style="font-family:{MONO};color:#e8e2cc;font-size:34px;letter-spacing:5px">0 5 4 2</span>
          <span style="font-family:{SANS};color:#8d8a7c;font-size:20px;letter-spacing:3px">19 cm/s · TYPE II</span></div>
        <div style="margin-top:24px;text-align:center">
          <div style="font-family:{SANS};font-size:44px;color:#262624;font-weight:600">Take Five</div>
          <div style="font-family:{SANS};font-size:24px;color:#6a6a66;margin-top:6px">Dave Brubeck Quartet — Time Out</div></div>
        <div style="margin-top:20px">{pbar(46,'#a6a6a2','#8a5a2a',8,knob=22,kc='#f3efe2')}
          {hb('03:14','05:24','#6a6a66',21,MONO,1,10)}</div>
        <div style="display:flex;justify-content:center;margin-top:22px">{vus(340,172)}</div>
        <div style="margin-top:18px">
          {''.join(f'<div style="display:flex;justify-content:space-between;padding:15px 4px;border-bottom:1px solid #b6b6b2;font-family:{SANS};font-size:23px;color:{"#262624" if i==1 else "#7a7a76"}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:20px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('1','Blue Rondo','6:44'),('2','Take Five','5:24'),('3','Strange Meadow Lark','7:22')]))}</div>
        <div style="display:flex;gap:14px;margin-top:18px">
          {deckbtn(rew(38,'#3a3a36'),'REW')}{deckbtn(tri(40,'#3a3a36'),'PLAY')}{deckbtn(pausei(38,'#3a3a36'),'PAUSE')}
          {deckbtn(ffwd(38,'#3a3a36'),'F.FWD')}{deckbtn(stop_sq(24,'#3a3a36') if False else f'<div style="width:24px;height:24px;background:#3a3a36"></div>','STOP')}
          {deckbtn(eject(38,'#8a5a2a'),'LIBRARY')}</div>
      </div></div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{WOOD};padding:26px">
      <div style="height:100%;background:{SILVER};border-radius:12px;padding:30px 40px;display:flex;flex-direction:column;box-shadow:inset 0 3px 6px #fff,0 10px 30px rgba(0,0,0,.5)">
        <div style="display:flex;align-items:center;gap:36px">
          <div style="flex:1;display:flex;flex-direction:column;justify-content:center">{reelpair(330,30)}<div style="margin-top:16px">{''.join(f'<div style="display:flex;justify-content:space-between;padding:11px 4px;border-bottom:1px solid #b6b6b2;font-family:{SANS};font-size:20px;color:{"#262624" if i==1 else "#7a7a76"}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:18px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('1','Blue Rondo','6:44'),('2','Take Five','5:24'),('3','Strange Meadow Lark','7:22')]))}</div></div>
          <div style="width:400px;display:flex;flex-direction:column;gap:16px">
            {headblock(400)}
            <div style="background:#1c1c1a;border-radius:8px;padding:12px 20px;display:flex;justify-content:space-between;align-items:center;box-shadow:inset 0 3px 8px #000">
              <span style="font-family:{MONO};color:#e8e2cc;font-size:30px;letter-spacing:5px">0 5 4 2</span>
              <span style="font-family:{SANS};color:#8d8a7c;font-size:18px;letter-spacing:2px">19 cm/s</span></div>
            {vus(190,130)}
          </div></div>
        <div style="display:flex;align-items:flex-end;gap:40px;margin-top:auto">
          <div style="flex:1">
            <div style="font-family:{SANS};font-size:46px;color:#262624;font-weight:600">Take Five</div>
            <div style="font-family:{SANS};font-size:22px;color:#6a6a66;margin-top:6px">Dave Brubeck Quartet — Time Out · Reel 2</div>
            <div style="margin-top:18px">{pbar(46,'#a6a6a2','#8a5a2a',8,knob=20,kc='#f3efe2')}{hb('03:14','05:24','#6a6a66',20,MONO,1,8)}</div></div>
          <div style="width:660px;display:flex;gap:12px">
            {deckbtn(rew(34,'#3a3a36'),'REW')}{deckbtn(tri(36,'#3a3a36'),'PLAY')}{deckbtn(pausei(34,'#3a3a36'),'PAUSE')}
            {deckbtn(ffwd(34,'#3a3a36'),'F.FWD')}{deckbtn('<div style="width:22px;height:22px;background:#3a3a36"></div>','STOP')}
            {deckbtn(eject(34,'#8a5a2a'),'LIBRARY')}</div>
        </div></div></div>'''
    add('17','Sony-Bandmaschine','iphone',ph); add('17','Sony-Bandmaschine','pc',pc)
d17()

# =========================================================================
# 18 · AKAI 747 dbx (weiss/silber, rote LED-Anzeige, symmetrisch, Holz)
# =========================================================================
def d18():
    PANEL='linear-gradient(180deg,#f4f4f2,#d9d9d6 50%,#eaeae7 60%,#c6c6c2)'
    LED='#ff2a12'
    def sqbtn(ic,lab,lampcolor=None):
        lamp=f'<div style="width:14px;height:14px;border-radius:3px;background:{lampcolor};box-shadow:0 0 10px {lampcolor}"></div>' if lampcolor else ''
        return f'''<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:7px">
        <div style="width:100%;aspect-ratio:1.25;border-radius:5px;background:linear-gradient(180deg,#fbfbfa,#d4d4d0);border:1.5px solid #a8a8a4;box-shadow:0 3px 0 #a8a8a4,0 6px 8px rgba(0,0,0,.3),inset 0 2px 2px #fff;display:flex;align-items:center;justify-content:center;gap:6px">{ic}{lamp}</div>
        <span style="font-size:17px;color:#575752;letter-spacing:1px;font-family:{SANS}">{lab}</span></div>'''
    counter=lambda fs:f'''<div style="background:#160604;border-radius:6px;padding:12px 26px;box-shadow:inset 0 3px 9px #000;display:inline-block">
      <span style="font-family:{MONO};color:{LED};font-size:{fs}px;letter-spacing:8px;text-shadow:0 0 14px rgba(255,42,18,.85)">0:54:23</span></div>'''
    def reels(s,gap): return f'<div style="display:flex;gap:{gap}px;justify-content:center">{bigreel(s,face="#fbfbfa",tape="#3a3a38",rim="#d2d2ce")}{bigreel(s,face="#fbfbfa",tape="#3a3a38",rim="#d2d2ce")}</div>'
    vustrip=lambda w,h:f'''<div style="background:#f2ecd0;border:1.5px solid #b9b39a;border-radius:5px;padding:10px;display:flex;gap:10px">
      {vumeter(w,h,'#f7f2dc','#2a2a26','#6b6b62','L',0.55)}{vumeter(w,h,'#f7f2dc','#2a2a26','#6b6b62','R',0.68)}</div>'''
    pc=f'''<div style="position:absolute;inset:0;background-color:#5c3a20;padding:24px">
      <div style="height:100%;background:{PANEL};border-radius:10px;padding:26px 34px;display:flex;flex-direction:column;box-shadow:0 12px 34px rgba(0,0,0,.5),inset 0 3px 4px #fff">
        <div style="display:flex;align-items:center;gap:34px;flex:1;min-height:0">
          <div style="display:flex;flex-direction:column;align-self:flex-start">{reels(300,22)}<div style="margin-top:16px">{''.join(f'<div style="display:flex;justify-content:space-between;padding:11px 4px;border-bottom:1px solid #bcbcb8;font-family:{SANS};font-size:20px;color:{"#2b2b28" if i==1 else "#7f7f7a"}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:18px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('01','Autobahn','7:12'),('02','Kometenmelodie','6:20'),('03','Mitternacht','3:44')]))}</div></div>
          <div style="flex:1;display:flex;flex-direction:column;gap:34px;align-items:center;justify-content:center">
            {counter(52)}{vustrip(392,244)}</div>
        </div>
        <div style="display:flex;align-items:flex-end;gap:40px;margin-top:auto">
          <div style="flex:1">
            <div style="font-family:{SANS};font-size:44px;font-weight:600;color:#2b2b28">Autobahn</div>
            <div style="font-family:{SANS};font-size:21px;color:#6f6f6a;margin-top:5px">Kraftwerk · Reel B — 4 Track Stereo</div>
            <div style="margin-top:16px">{pbar(38,'#bcbcb8','#d63a1e',8,knob=20,kc='#fbfbfa')}{hb('00:54','07:12','#6f6f6a',20,MONO,1,8)}</div></div>
          <div style="width:700px;display:flex;gap:11px">
            {sqbtn(rew(32,'#3a3a36'),'REW')}{sqbtn(tri(34,'#3a3a36'),'PLAY','#2ecc40')}{sqbtn(pausei(32,'#3a3a36'),'PAUSE','#f5c400')}
            {sqbtn(ffwd(32,'#3a3a36'),'F.FWD')}{sqbtn('<div style="width:20px;height:20px;background:#3a3a36"></div>','STOP')}
            {sqbtn(eject(32,'#d63a1e'),'LIBRARY')}</div>
        </div></div></div>'''
    add('18','Akai-747','pc',pc)   # kein Hochformat: auf Wunsch des Eigentuemers entfallen
d18()

# =========================================================================
# 19 · ON AIR Leuchtkasten (Backstein, schwarzer Rahmen, rote Lettern)
# =========================================================================
def d19():
    BRICK='#c9c4bd'
    brickpat='''background-color:#cfcac3;background-image:repeating-linear-gradient(0deg,rgba(0,0,0,.10) 0 2px,transparent 2px 58px),repeating-linear-gradient(90deg,rgba(0,0,0,.10) 0 2px,transparent 2px 120px)'''
    def box(fs,pad,txt='ON AIR',lit=True):
        glow='box-shadow:0 0 60px rgba(255,220,160,.45),0 18px 40px rgba(0,0,0,.45)' if lit else 'box-shadow:0 18px 40px rgba(0,0,0,.45)'
        face='linear-gradient(180deg,#fdf3d8,#f3e2b8)' if lit else 'linear-gradient(180deg,#4a4844,#3a3835)'
        col='#d8342a' if lit else '#6a6663'
        return f'''<div style="background:#1e1e1c;border-radius:8px;padding:16px;{glow}">
        <div style="background:{face};border-radius:4px;padding:{pad};text-align:center">
          <span style="font-family:{IMPACT};font-size:{fs}px;letter-spacing:4px;color:{col}">{txt}</span></div></div>'''
    def plate(ic,lab):
        return f'''<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:9px">
        <div style="width:100%;aspect-ratio:1.1;background:#1e1e1c;border-radius:8px;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 18px rgba(0,0,0,.4)">{ic}</div>
        <span style="font-family:{SANS};font-size:18px;letter-spacing:2px;color:#5c5750">{lab}</span></div>'''
    ph=f'''<div style="position:absolute;inset:0;{brickpat};padding:70px 60px;display:flex;flex-direction:column">
      <div style="margin-top:20px">{box(120,'44px 20px')}</div>
      <div style="margin-top:40px">{box(46,'22px 16px','STUDIO 2 · LIVE',False)}</div>
      <div style="background:#f3efe8;border-radius:14px;padding:44px 40px;margin-top:46px;box-shadow:0 14px 34px rgba(0,0,0,.22)">
        <div style="font-family:{SANS};font-size:22px;letter-spacing:5px;color:#a09a92">NOW BROADCASTING</div>
        <div style="font-family:{SANS};font-size:56px;font-weight:700;color:#26241f;margin-top:12px">Night Shift</div>
        <div style="font-family:{SANS};font-size:26px;color:#7d776e;margin-top:8px">Gilles Peterson · Worldwide FM</div>
        <div style="margin-top:32px">{waveform(880,120,'#d8342a',60,op=.85)}</div>
        {pbar(52,'#ddd7cd','#d8342a',8,mt=24,knob=22,kc='#d8342a')}
        {hb('01:12:40','02:00:00','#a09a92',22,MONO,1,12)}
      </div>
      <div style="display:flex;gap:18px;margin-top:auto">
        {plate(prev(38,'#f3e2b8'),'PREV')}{plate(tri(42,'#f3e2b8'),'PLAY')}{plate(pausei(38,'#f3e2b8'),'PAUSE')}
        {plate(nexti(38,'#f3e2b8'),'NEXT')}{plate(libicon(38,'#d8342a'),'LIBRARY')}</div>
    </div>'''
    pc=f'''<div style="position:absolute;inset:0;{brickpat};padding:56px 70px;display:flex;gap:60px;align-items:center">
      <div style="flex:1;display:flex;flex-direction:column;gap:26px">
        {box(96,'38px 20px')}
        {box(38,'18px 14px','STUDIO 2 · LIVE',False)}
        <div style="display:flex;gap:14px">{plate(prev(34,'#f3e2b8'),'PREV')}{plate(tri(38,'#f3e2b8'),'PLAY')}{plate(pausei(34,'#f3e2b8'),'PAUSE')}{plate(nexti(34,'#f3e2b8'),'NEXT')}{plate(libicon(34,'#d8342a'),'LIBRARY')}</div>
      </div>
      <div style="width:660px;background:#f3efe8;border-radius:16px;padding:48px 44px;box-shadow:0 14px 34px rgba(0,0,0,.22)">
        <div style="font-family:{SANS};font-size:21px;letter-spacing:5px;color:#a09a92">NOW BROADCASTING</div>
        <div style="font-family:{SANS};font-size:62px;font-weight:700;color:#26241f;margin-top:10px">Night Shift</div>
        <div style="font-family:{SANS};font-size:26px;color:#7d776e;margin-top:8px">Gilles Peterson · Worldwide FM</div>
        <div style="margin-top:30px">{waveform(560,130,'#d8342a',56,op=.85)}</div>
        {pbar(52,'#ddd7cd','#d8342a',8,mt=22,knob=20,kc='#d8342a')}
        {hb('01:12:40','02:00:00','#a09a92',21,MONO,1,12)}
        <div style="margin-top:26px;border-top:1px solid #e2dcd2;padding-top:16px">
          {''.join(f'<div style="display:flex;justify-content:space-between;font-family:{SANS};font-size:22px;color:{"#26241f" if i==0 else "#a09a92"};padding:9px 0"><span>{t}</span><span>{d}</span></div>' for i,(t,d) in enumerate([('Night Shift — live','now'),('Deep Cuts','21:00'),('Sunrise Set','23:00')]))}
        </div></div></div>'''
    add('19','On-Air-Leuchtkasten','iphone',ph); add('19','On-Air-Leuchtkasten','pc',pc)
d19()

# =========================================================================
# 20 · Philips Roehrenradio (Mahagoni, blaues Panel, Rattan-Gitter)
# =========================================================================
def d20():
    MAH='linear-gradient(160deg,#7d2f26,#5a1f18)'
    BLUE='linear-gradient(180deg,#3c5c78,#2c4459)'
    RATTAN='#e6dcc0'
    def grille(w,h):
        return f'''<div style="width:{w};height:{h}px;border-radius:6px;background-color:{RATTAN};
        background-image:repeating-linear-gradient(0deg,rgba(120,100,60,.45) 0 2px,transparent 2px 9px),repeating-linear-gradient(90deg,rgba(120,100,60,.45) 0 2px,transparent 2px 9px);
        box-shadow:inset 0 2px 6px rgba(0,0,0,.3)"></div>'''
    marks=['15','12','10','8','7','6','5']
    def knobrow(size):
        return f'''<div style="display:flex;align-items:center;gap:26px">
        {knurl(size,accent='#e8e2d0')}
        <div style="display:flex;flex-direction:column;gap:6px;font-family:{SANS};color:#cfd8e2;font-size:20px;letter-spacing:2px"><span>TUNING</span><span style="color:#8fa3b6;font-size:17px">MW · UKW</span></div></div>'''
    ph=f'''<div style="position:absolute;inset:0;background:{MAH};padding:40px 34px;display:flex;flex-direction:column">
      <div style="background:{BLUE};border-radius:8px;padding:26px 24px;box-shadow:inset 0 2px 6px rgba(0,0,0,.35)">
        {tunescale(940,150,marks,'#e8e2d0','#d8452e',0.44)}
        <div style="display:flex;justify-content:space-between;font-family:{SANS};color:#a8bccd;font-size:20px;letter-spacing:3px;margin-top:10px"><span>kHz</span><span>MW / UKW</span></div>
      </div>
      <div style="display:flex;gap:24px;margin-top:26px;align-items:stretch">
        <div style="flex:1">{grille('100%',420)}</div>
        <div style="width:230px;background:{BLUE};border-radius:8px;display:flex;flex-direction:column;align-items:center;justify-content:space-around;padding:24px 0;box-shadow:inset 0 2px 6px rgba(0,0,0,.35)">
          {knurl(150,accent='#e8e2d0')}
          <div style="font-family:{SANS};color:#cfd8e2;font-size:18px;letter-spacing:3px">TUNING</div>
          <div style="width:74px;height:74px;border-radius:50%;background:radial-gradient(circle at 38% 32%,#f4f4f0,#b8b8b2);box-shadow:0 4px 10px rgba(0,0,0,.4)"></div>
          <div style="font-family:{SANS};color:#8fa3b6;font-size:16px;letter-spacing:2px">VOLUME</div>
        </div>
      </div>
      <div style="background:#f0e9d8;border-radius:10px;padding:34px 30px;margin-top:26px">
        <div style="font-family:{SANS};font-size:20px;letter-spacing:4px;color:#9a8f78">JETZT AUF 98.4 MHz</div>
        <div style="font-family:{SERIF};font-size:52px;color:#3c2a20;margin-top:10px">Nachtprogramm</div>
        <div style="font-family:{SANS};font-size:24px;color:#8a7c66;margin-top:6px">Radio Bremen · Jazz um Mitternacht</div>
        {pbar(58,'#ddd3bb','#7d2f26',7,mt=26,knob=20,kc='#7d2f26')}
        {hb('00:42','01:30','#9a8f78',21,MONO,1,10)}
      </div>
      <div style="display:flex;gap:16px;margin-top:auto">
        {''.join(f'<div style="flex:1;background:{BLUE};border-radius:8px;padding:22px 0;display:flex;flex-direction:column;align-items:center;gap:8px;box-shadow:inset 0 2px 4px rgba(0,0,0,.3)">{ic}<span style="font-family:{SANS};font-size:17px;color:#a8bccd;letter-spacing:2px">{lab}</span></div>' for ic,lab in [(prev(36,'#e8e2d0'),'PREV'),(tri(40,'#e8e2d0'),'PLAY'),(pausei(36,'#e8e2d0'),'PAUSE'),(nexti(36,'#e8e2d0'),'NEXT'),(libicon(36,'#f0c46a'),'ARCHIV')])}
      </div></div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{MAH};padding:36px 44px;display:flex;flex-direction:column;gap:22px">
      <div style="background:{BLUE};border-radius:8px;padding:22px 26px;box-shadow:inset 0 2px 6px rgba(0,0,0,.35);display:flex;align-items:center;gap:36px">
        <div style="flex:1">{tunescale(880,130,marks,'#e8e2d0','#d8452e',0.44)}</div>
        <div style="display:flex;align-items:center;gap:20px">{knurl(120,accent='#e8e2d0')}
          <div style="font-family:{SANS};color:#cfd8e2;font-size:19px;letter-spacing:2px;line-height:1.6">TUNING<br><span style="color:#8fa3b6;font-size:16px">98.4 MHz</span></div></div>
      </div>
      <div style="display:flex;gap:24px;flex:1">
        <div style="width:420px">{grille('100%',None) if False else f'<div style="height:100%">{grille("100%",320)}</div>'}</div>
        <div style="flex:1;background:#f0e9d8;border-radius:10px;padding:34px 32px;display:flex;flex-direction:column">
          <div style="font-family:{SANS};font-size:19px;letter-spacing:4px;color:#9a8f78">JETZT AUF 98.4 MHz</div>
          <div style="font-family:{SERIF};font-size:54px;color:#3c2a20;margin-top:8px">Nachtprogramm</div>
          <div style="font-family:{SANS};font-size:23px;color:#8a7c66;margin-top:6px">Radio Bremen · Jazz um Mitternacht</div>
          <div style="margin-top:auto">{pbar(58,'#ddd3bb','#7d2f26',7,knob=20,kc='#7d2f26')}{hb('00:42','01:30','#9a8f78',20,MONO,1,10)}</div>
        </div>
      </div>
      <div style="display:flex;gap:14px">
        {''.join(f'<div style="flex:1;background:{BLUE};border-radius:8px;padding:18px 0;display:flex;align-items:center;justify-content:center;gap:12px;box-shadow:inset 0 2px 4px rgba(0,0,0,.3)">{ic}<span style="font-family:{SANS};font-size:18px;color:#a8bccd;letter-spacing:2px">{lab}</span></div>' for ic,lab in [(prev(32,'#e8e2d0'),'PREV'),(tri(36,'#e8e2d0'),'PLAY'),(pausei(32,'#e8e2d0'),'PAUSE'),(nexti(32,'#e8e2d0'),'NEXT'),(libicon(32,'#f0c46a'),'ARCHIV')])}
      </div></div>'''
    add('20','Philips-Radio','iphone',ph); add('20','Philips-Radio','pc',pc)
d20()

# =========================================================================
# 21 · YAMAHA Tuner (dunkles Holz, weisse Front, 3 Knoebe, kleines VU)
# =========================================================================
def d21():
    WOOD='#4a2f1e'; FACE='#f2f1ec'; INK='#3a3a36'; SUB='#8d8b84'
    marks=['5.4','6','7','8','9','10','12','14','16']
    def bigknob(lab,size):
        return f'''<div style="display:flex;flex-direction:column;align-items:center;gap:12px">
        <span style="font-family:{SANS};font-size:17px;letter-spacing:3px;color:{SUB}">{lab}</span>
        <div style="width:{size}px;height:{size}px;border-radius:50%;background:radial-gradient(circle at 36% 30%,#ffffff,#e8e7e2 55%,#c4c3bd);box-shadow:0 8px 16px rgba(0,0,0,.28),inset 0 2px 3px #fff;position:relative">
          <div style="position:absolute;left:50%;top:10px;width:3px;height:{size*0.22:.0f}px;background:#9a9992;transform:translateX(-50%);border-radius:2px"></div></div></div>'''
    ph=f'''<div style="position:absolute;inset:0;background:{WOOD};padding:34px 30px;display:flex;flex-direction:column">
      <div style="background:{FACE};border-radius:6px;padding:44px 34px;flex:1;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 12px 30px rgba(0,0,0,.45)">
        <div style="display:flex;align-items:flex-start;gap:24px">
          <div style="flex:1">{tunescale(620,120,marks,'#5a5952','#c9422e',0.42)}</div>
          <div style="width:200px;border:2px solid #c8c7c1;border-radius:6px;padding:6px;background:#faf9f5">{vumeter(180,90,'#faf9f5','#33332f','#8d8b84','',0.60)}</div>
        </div>
        <div style="font-family:{SANS};font-size:30px;letter-spacing:10px;color:{INK};text-align:center;margin-top:26px">YAMAHA</div>
        <div style="margin-top:34px;text-align:center">
          <div style="font-family:{SANS};font-size:24px;letter-spacing:4px;color:{SUB}">NOW PLAYING · FM 89.6</div>
          <div style="font-family:{SANS};font-size:52px;font-weight:600;color:{INK};margin-top:12px">Morning Pass</div>
          <div style="font-family:{SANS};font-size:24px;color:{SUB};margin-top:8px">Hiroshi Yoshimura — GREEN</div>
        </div>
        <div style="margin-top:26px">{pbar(41,'#dedcd5','#c9422e',7,knob=20,kc=INK)}{hb('02:14','05:26',SUB,21,MONO,1,10)}</div>
        <div style="margin-top:22px">
          {''.join(f'<div style="display:flex;justify-content:space-between;padding:16px 2px;border-bottom:1px solid #e2e0d9;font-family:{SANS};font-size:24px;color:{INK if i==1 else SUB}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:20px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('01','Creek','4:02'),('02','Morning Pass','5:26'),('03','Sheep','6:10')]))}</div>
        <div style="display:flex;justify-content:space-around;margin-top:22px;margin-bottom:14px">
          {bigknob('GAIN CONT',182)}{bigknob('PASS BAND',182)}{bigknob('TUNING',182)}</div>
        <div style="display:flex;gap:14px">
          {''.join(f'<div style="flex:1;border:1.5px solid #d2d1cb;border-radius:6px;padding:20px 0;display:flex;flex-direction:column;align-items:center;gap:7px;background:#fafaf7">{ic}<span style="font-family:{SANS};font-size:16px;letter-spacing:2px;color:{SUB}">{lab}</span></div>' for ic,lab in [(prev(32,INK),'PREV'),(tri(36,INK),'PLAY'),(pausei(32,INK),'PAUSE'),(nexti(32,INK),'NEXT'),(libicon(32,'#c9422e'),'LIBRARY')])}
        </div></div></div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{WOOD};padding:30px 40px">
      <div style="height:100%;background:{FACE};border-radius:6px;padding:38px 46px;display:flex;flex-direction:column;box-shadow:0 12px 30px rgba(0,0,0,.45)">
        <div style="display:flex;align-items:flex-start;gap:40px">
          <div style="flex:1">{tunescale(700,120,marks,'#5a5952','#c9422e',0.42)}</div>
          <div style="font-family:{SANS};font-size:30px;letter-spacing:10px;color:{INK};margin-top:26px">YAMAHA</div>
          <div style="width:210px;border:2px solid #c8c7c1;border-radius:6px;padding:6px;background:#faf9f5">{vumeter(190,86,'#faf9f5','#33332f','#8d8b84','',0.60)}</div>
        </div>
        <div style="display:flex;gap:50px;align-items:center;margin-top:auto">
          <div style="flex:1">
            <div style="font-family:{SANS};font-size:20px;letter-spacing:4px;color:{SUB}">NOW PLAYING · FM 89.6</div>
            <div style="font-family:{SANS};font-size:54px;font-weight:600;color:{INK};margin-top:8px">Morning Pass</div>
            <div style="font-family:{SANS};font-size:22px;color:{SUB};margin-top:6px">Hiroshi Yoshimura — GREEN</div>
            <div style="margin-top:16px">{''.join(f'<div style="display:flex;justify-content:space-between;padding:11px 4px;border-bottom:1px solid #e2e0d9;font-family:{SANS};font-size:20px;color:{INK if i==1 else SUB}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:18px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('01','Creek','4:02'),('02','Morning Pass','5:26'),('03','Sheep','6:10')]))}</div><div style="margin-top:18px">{pbar(41,'#dedcd5','#c9422e',7,knob=18,kc=INK)}{hb('02:14','05:26',SUB,20,MONO,1,8)}</div>
          </div>
          <div style="display:flex;gap:40px">{bigknob('GAIN CONT',140)}{bigknob('PASS BAND',140)}{bigknob('TUNING',140)}</div>
        </div>
        <div style="display:flex;gap:12px;margin-top:30px">
          {''.join(f'<div style="flex:1;border:1.5px solid #d2d1cb;border-radius:6px;padding:16px 0;display:flex;align-items:center;justify-content:center;gap:12px;background:#fafaf7">{ic}<span style="font-family:{SANS};font-size:17px;letter-spacing:2px;color:{SUB}">{lab}</span></div>' for ic,lab in [(prev(30,INK),'PREV'),(tri(34,INK),'PLAY'),(pausei(30,INK),'PAUSE'),(nexti(30,INK),'NEXT'),(libicon(30,'#c9422e'),'LIBRARY')])}
        </div></div></div>'''
    add('21','Yamaha-Tuner','iphone',ph); add('21','Yamaha-Tuner','pc',pc)
d21()

print('V3 part A:', len(D))

# =========================================================================
# 22 · EA Technology Archive (Papier, Spec-Grid, orange Akzente)
# =========================================================================
def d22():
    PAPER='#eeece5'; INK='#191917'; OR='#d4602a'; SUB='#8b8880'; LINE='#c8c5bc'
    def field(l,v,w='auto'):
        return f'<div style="flex:1"><div style="font-family:{SANS};font-size:17px;letter-spacing:2px;color:{OR};font-weight:700">{l}</div><div style="font-family:{SANS};font-size:22px;color:{INK};margin-top:5px;font-weight:600">{v}</div></div>'
    stampbox=f'''<div style="border:2px solid {INK};font-family:{SANS};font-size:19px;letter-spacing:3px;font-weight:700">
      <div style="padding:9px 18px;border-bottom:2px solid {INK}">EA</div>
      <div style="padding:9px 18px;border-bottom:2px solid {INK}">ARCHIVE</div>
      <div style="padding:9px 18px">OBJECT</div></div>'''
    globe=f'<svg width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="{OR}" stroke-width="1.5"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 9h18M3 15h18"/></svg>'
    def ctrlbar(pad):
        return f'''<div style="border:2px solid {INK};display:flex;align-items:stretch;margin-top:{pad}px">
        {''.join(f'<div style="flex:1;padding:20px 0;display:flex;flex-direction:column;align-items:center;gap:7px;{"border-right:2px solid "+INK if i<4 else ""};{bg}">{ic}<span style="font-family:{SANS};font-size:15px;letter-spacing:2px;color:{col}">{lab}</span></div>' for i,(ic,lab,bg,col) in enumerate([(prev(30,INK),'PREV','',SUB),(tri(34,'#fff'),'PLAY',f'background:{OR}','#fff'),(pausei(30,INK),'PAUSE','',SUB),(nexti(30,INK),'NEXT','',SUB),(libicon(30,OR),'ARCHIVE','',SUB)]))}</div>'''
    ph=f'''<div style="position:absolute;inset:0;background:{PAPER};padding:56px 50px;display:flex;flex-direction:column;font-family:{SANS};color:{INK}">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div><div style="font-size:20px;letter-spacing:3px;font-weight:700">OBJECT</div>
          <div style="font-size:82px;font-weight:800;color:{OR};line-height:.9;margin-top:2px">032</div></div>
        {stampbox}</div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:22px">
        <div style="font-size:20px;letter-spacing:2px;font-weight:700;line-height:1.5">TECHNOLOGY ARCHIVE<br><span style="color:{SUB};font-weight:400">ESCAPEARCHIVE COLLECTION</span></div>{globe}</div>
      <div style="height:2px;background:{INK};margin:20px 0"></div>
      <div style="font-size:52px;font-weight:800;letter-spacing:-1px">COMPACT CASSETTE</div>
      <div style="font-size:24px;color:{SUB};margin-top:4px">AUDIO HOME SYSTEM</div>
      <div style="font-size:30px;font-weight:700;margin-top:6px">1963</div>
      <div style="margin-top:24px;display:flex;justify-content:center">{cassette(880,shell='#26262a',label='#efece2',text='#26262a',hubfill='#d8d6cc',screws='#4a4a4e',title='EA-032',sub='MAGNETIC TAPE · TYPE I',side='A')}</div>
      <div style="height:2px;background:{INK};margin:22px 0 16px"></div>
      <div style="display:flex;gap:20px">{field('ERA','1960s')}{field('ORIGIN','JAPAN')}{field('FORMAT','TYPE I')}{field('STATUS','ARCHIVED')}</div>
      <div style="height:1px;background:{LINE};margin:16px 0"></div>
      <div style="display:flex;justify-content:space-between;align-items:baseline">
        <div><div style="font-size:17px;letter-spacing:2px;color:{OR};font-weight:700">NOW PLAYING</div>
          <div style="font-size:30px;font-weight:700;margin-top:5px">Side A · Track 03 — Kioku</div></div>
        <span style="font-family:{MONO};font-size:22px;color:{SUB}">02:41 / 04:58</span></div>
      {pbar(54,'#d8d5cc',OR,8,mt=16,knob=0)}
      {ctrlbar(20)}
      <div style="display:flex;justify-content:space-between;font-size:16px;letter-spacing:2px;color:{SUB};margin-top:auto;padding-top:18px">
        <span>DOCUMENT NO. EA.032.1963</span><span>VOL.03 · ITEM.032</span></div>
    </div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{PAPER};padding:48px 60px;display:flex;flex-direction:column;font-family:{SANS};color:{INK}">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div style="display:flex;align-items:baseline;gap:26px">
          <div><div style="font-size:19px;letter-spacing:3px;font-weight:700">OBJECT</div>
            <div style="font-size:74px;font-weight:800;color:{OR};line-height:.9">032</div></div>
          <div style="font-size:19px;letter-spacing:2px;font-weight:700;line-height:1.5">TECHNOLOGY ARCHIVE<br><span style="color:{SUB};font-weight:400">ESCAPEARCHIVE COLLECTION</span></div></div>
        <div style="display:flex;gap:22px;align-items:flex-start">{globe}{stampbox}</div></div>
      <div style="height:2px;background:{INK};margin:18px 0"></div>
      <div style="display:flex;gap:50px;flex:1">
        <div style="flex:1.05;display:flex;flex-direction:column">
          <div style="font-size:46px;font-weight:800;letter-spacing:-1px">COMPACT CASSETTE</div>
          <div style="font-size:22px;color:{SUB};margin-top:3px">AUDIO HOME SYSTEM · 1963</div>
          <div style="margin-top:20px">{cassette(640,shell='#26262a',label='#efece2',text='#26262a',hubfill='#d8d6cc',screws='#4a4a4e',title='EA-032',sub='MAGNETIC TAPE · TYPE I',side='A')}</div>
          <div style="height:1px;background:{LINE};margin:18px 0"></div>
          <div style="display:flex;gap:18px">{field('ERA','1960s')}{field('ORIGIN','JAPAN')}{field('FORMAT','TYPE I')}{field('STATUS','ARCHIVED')}</div>
        </div>
        <div style="width:2px;background:{INK}"></div>
        <div style="width:520px;display:flex;flex-direction:column">
          <div style="font-size:17px;letter-spacing:2px;color:{OR};font-weight:700">NOW PLAYING</div>
          <div style="font-size:40px;font-weight:800;margin-top:8px;line-height:1.1">Kioku</div>
          <div style="font-size:22px;color:{SUB};margin-top:6px">Side A · Track 03 — Archive Reissue</div>
          <div style="margin-top:24px">
            {''.join(f'<div style="display:flex;justify-content:space-between;padding:15px 0;border-bottom:1px solid {LINE};font-size:21px;color:{INK if i==2 else SUB}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:22px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('01','Hajimari','3:12'),('02','Yoru','4:20'),('03','Kioku','4:58'),('04','Owari','3:44')]))}
          </div>
          {pbar(54,'#d8d5cc',OR,8,mt=22)}
          {hb('02:41','04:58',SUB,20,MONO,1,10)}
          {ctrlbar(18)}
          <div style="font-size:15px;letter-spacing:2px;color:{SUB};margin-top:auto;padding-top:14px">DOCUMENT NO. EA.032.1963</div>
        </div></div></div>'''
    add('22','EA-Archive','iphone',ph); add('22','EA-Archive','pc',pc)
d22()

# =========================================================================
# 23 · MAGNETOLA (pinke Kassette, beschriftete Tastenleiste)
# =========================================================================
def d23():
    BODY='linear-gradient(180deg,#4a4a4c,#333336)'; PINK='#e8397e'
    PANEL='linear-gradient(180deg,#d8d6d0,#b8b6b0)'
    def key(ic,lab,wide=False,active=False):
        bg='linear-gradient(180deg,#eceae4,#c8c6c0)' if not active else 'linear-gradient(180deg,#d4d2cc,#b0aea8)'
        return f'''<div style="flex:{2 if wide else 1};display:flex;flex-direction:column;align-items:center;gap:7px">
        <span style="font-family:{SANS};font-size:17px;letter-spacing:2px;color:#4a4a48;font-weight:600">{lab}</span>
        <div style="width:100%;aspect-ratio:{1.05 if wide else 0.9};background:{bg};border:1.5px solid #8e8c86;border-radius:5px;box-shadow:0 4px 0 #8e8c86,0 7px 9px rgba(0,0,0,.35),inset 0 2px 2px #fff;display:flex;align-items:center;justify-content:center">{ic}</div>
        <div style="width:60%;height:3px;background:#8e8c86;border-radius:2px"></div></div>'''
    def tapeblock(w):
        return f'''<div style="background:{BODY};border-radius:14px;padding:26px;box-shadow:inset 0 3px 8px rgba(255,255,255,.10),0 10px 26px rgba(0,0,0,.45)">
        {cassette(w,shell='#3e3e42',label='#fbfbf8',text='#2b4a9e',hubfill='#e8e8e4',screws='#5a5a5e',
                  title='Another Brick in the Wall, Pt. 1',sub='Pink Floyd · The Wall',stripes=[PINK,PINK,PINK],side='A')}
        <div style="text-align:center;margin-top:14px;font-family:{SANS};font-size:20px;letter-spacing:3px;color:#b9b7b2">
          <span style="color:{PINK};font-weight:700">MAGNETOLA</span> MUSIC PLAYER <span style="color:#f0c400;font-weight:700">1.0</span></div></div>'''
    ph=f'''<div style="position:absolute;inset:0;background:{BODY};padding:44px 36px;display:flex;flex-direction:column">
      {tapeblock(940)}
      <div style="background:#2b2b2e;border-radius:10px;padding:26px 28px;margin-top:26px;box-shadow:inset 0 3px 10px #000">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-family:{MONO};color:{PINK};font-size:26px;letter-spacing:3px">▶ SIDE A · TRACK 01</span>
          <span style="font-family:{MONO};color:#9a9a96;font-size:24px">03:21 / 03:52</span></div>
        {pbar(86,'#414145',PINK,8,mt=18,knob=20,kc=PINK)}
        <div style="margin-top:18px">{waveform(880,90,'#6a6a6e',56,op=.9)}</div>
      </div>
      <div style="background:{PANEL};border-radius:10px;padding:30px 22px;margin-top:auto;box-shadow:0 10px 24px rgba(0,0,0,.4),inset 0 2px 3px #fff">
        <div style="display:flex;gap:12px">
          {key(prev(32,'#3a3a38'),'PREV')}{key(rew(32,'#3a3a38'),'REWIND')}{key('<div style="width:22px;height:22px;background:#3a3a38"></div>','STOP')}
          {key(tri(34,'#3a3a38'),'PLAY',active=True)}{key(ffwd(32,'#3a3a38'),'F.F.')}{key(nexti(32,'#3a3a38'),'NEXT')}</div>
        <div style="display:flex;gap:12px;margin-top:22px">
          {key(libicon(32,PINK),'LIBRARY',wide=True)}{key(shuffle(30,'#3a3a38'),'SHUFFLE',wide=True)}{key(repeat(30,'#3a3a38'),'REPEAT',wide=True)}</div>
      </div></div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{BODY};padding:38px 46px;display:flex;gap:44px">
      <div style="flex:1.15;display:flex;flex-direction:column;justify-content:center">{tapeblock(700)}</div>
      <div style="flex:1;display:flex;flex-direction:column">
        <div style="background:#2b2b2e;border-radius:10px;padding:26px;box-shadow:inset 0 3px 10px #000">
          <div style="font-family:{SANS};color:#e6e6e2;font-size:34px;font-weight:600">Another Brick in the Wall, Pt. 1</div>
          <div style="font-family:{SANS};color:{PINK};font-size:22px;margin-top:6px">Pink Floyd · The Wall — Side A</div>
          {pbar(86,'#414145',PINK,8,mt=20,knob=20,kc=PINK)}
          {hb('03:21','03:52','#9a9a96',20,MONO,1,10)}
          <div style="margin-top:16px">{waveform(560,80,'#6a6a6e',54,op=.9)}</div></div>
        <div style="margin-top:20px;background:#2b2b2e;border-radius:10px;padding:8px 22px;box-shadow:inset 0 3px 10px #000">
          {''.join(f'<div style="display:flex;justify-content:space-between;padding:13px 0;border-bottom:1px solid #3c3c40;font-family:{SANS};font-size:20px;color:{"#e6e6e2" if i==0 else "#8e8e8a"}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:20px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('A1','Another Brick Pt.1','3:52'),('A2','The Thin Ice','2:27'),('A3','Mother','5:32')]))}</div>
        <div style="background:{PANEL};border-radius:10px;padding:24px 20px;margin-top:auto;box-shadow:0 10px 24px rgba(0,0,0,.4),inset 0 2px 3px #fff">
          <div style="display:flex;gap:10px">
            {key(prev(28,'#3a3a38'),'PREV')}{key(rew(28,'#3a3a38'),'REWIND')}{key('<div style="width:20px;height:20px;background:#3a3a38"></div>','STOP')}
            {key(tri(30,'#3a3a38'),'PLAY',active=True)}{key(ffwd(28,'#3a3a38'),'F.F.')}{key(nexti(28,'#3a3a38'),'NEXT')}{key(libicon(28,PINK),'LIBRARY')}</div></div>
      </div></div>'''
    add('23','Magnetola','iphone',ph); add('23','Magnetola','pc',pc)
d23()

# =========================================================================
# 24 · MIX TAPE transparent (weiss, handschriftlich, roter Punkt)
# =========================================================================
def d24():
    BG='#f7f7f5'; INK='#1c1c1a'; RED='#e03127'; SUB='#a5a5a0'
    HAND="'Bradley Hand','Segoe Print','Comic Sans MS',cursive"
    def rowh(n,t,cur=False):
        return f'''<div style="display:flex;align-items:center;gap:20px;padding:19px 0;border-bottom:1px solid #e4e4e0">
        <div style="width:14px;height:14px;border-radius:50%;background:{RED if cur else '#dcdcd8'}"></div>
        <span style="font-family:{HAND};font-size:31px;color:{INK if cur else SUB};flex:1">{t}</span>
        <span style="font-family:{MONO};font-size:20px;color:{SUB}">{n}</span></div>'''
    def circbtn(ic,size=100,fill='#fff',border='#dcdcd8'):
        return f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{fill};border:1.5px solid {border};display:flex;align-items:center;justify-content:center;box-shadow:0 6px 16px rgba(0,0,0,.10)">{ic}</div>'
    ph=f'''<div style="position:absolute;inset:0;background:{BG};padding:70px 60px;display:flex;flex-direction:column;justify-content:space-between">
      <div style="display:flex;justify-content:space-between;align-items:center;font-family:{SANS};font-size:22px;letter-spacing:3px;color:{SUB}">
        <span>C60 · TYPE I</span><span>SIDE A</span></div>
      <div style="margin-top:40px;display:flex;justify-content:center">
        {cassette(940,shell='#e4e4e2',label='#faf8f0',text=INK,hubfill='#f2f2ee',screws='#c8c8c4',clear=True,
                  title='MIX TAPE',sub='AOYAMA · JEVED · ROCKS',side='A')}</div>
      <div style="margin-top:36px">{rowh('3:12','Sunday Drive')}{rowh('4:05','Neon Rain',True)}{rowh('2:58','Late Ferry')}{rowh('5:20','Blue Hour')}{rowh('4:31','Harbour Lights')}{rowh('3:44','Last Train')}</div>
      {pbar(44,'#e4e4e0',RED,6,mt=28,knob=22,kc=RED)}
      {hb('01:48','04:05',SUB,22,MONO,1,12)}
      <div style="display:flex;justify-content:center;align-items:center;gap:34px;margin-top:auto;margin-bottom:10px">
        {circbtn(shuffle(30,SUB),84)}{circbtn(prev(34,INK),96)}
        {circbtn(tri(44,'#fff'),132,RED,RED)}
        {circbtn(nexti(34,INK),96)}{circbtn(libicon(30,RED),84)}</div>
    </div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{BG};padding:60px 80px;display:flex;gap:70px;align-items:center">
      <div style="flex:1.1">
        {cassette(720,shell='#e4e4e2',label='#faf8f0',text=INK,hubfill='#f2f2ee',screws='#c8c8c4',clear=True,
                  title='MIX TAPE',sub='AOYAMA · JEVED · ROCKS',side='A')}
        <div style="display:flex;justify-content:space-between;font-family:{SANS};font-size:20px;letter-spacing:3px;color:{SUB};margin-top:22px"><span>C60 · TYPE I</span><span>SIDE A · 4 TRACKS</span></div>
      </div>
      <div style="flex:1;display:flex;flex-direction:column">
        <div style="font-family:{HAND};font-size:62px;color:{INK}">Neon Rain</div>
        <div style="font-family:{SANS};font-size:22px;color:{SUB};margin-top:6px;letter-spacing:1px">Track 02 — aus „Mix Tape"</div>
        <div style="margin-top:28px">{rowh('3:12','Sunday Drive')}{rowh('4:05','Neon Rain',True)}{rowh('2:58','Late Ferry')}{rowh('5:20','Blue Hour')}</div>
        {pbar(44,'#e4e4e0',RED,6,mt=28,knob=20,kc=RED)}
        {hb('01:48','04:05',SUB,20,MONO,1,10)}
        <div style="display:flex;align-items:center;gap:26px;margin-top:34px">
          {circbtn(shuffle(28,SUB),76)}{circbtn(prev(30,INK),86)}
          {circbtn(tri(40,'#fff'),116,RED,RED)}
          {circbtn(nexti(30,INK),86)}{circbtn(libicon(28,RED),76)}</div>
      </div></div>'''
    add('24','Mix-Tape-Klar','iphone',ph); add('24','Mix-Tape-Klar','pc',pc)
d24()

# =========================================================================
# 25 · AUDIO TAPE C90 (Creme/Gelb/Orange Illustration, flach)
# =========================================================================
def d25():
    BG='#f4efe2'; CREAM='#e8dfc4'; OR='#e0752a'; RED='#c3402a'; YEL='#e8b93e'; INK='#3a3128'
    def tape(w):
        return cassette(w,shell='#e6dcc0',label='#f7f2e2',text=INK,hubfill='#f2ece0',screws='#c9bfa2',
                        stripes=[RED,OR,YEL],title='DIRE STRAITS · BROTHERS IN ARMS',sub='AUDIO TAPE — C90',side='A')
    def flatbtn(ic,lab,bg,fg):
        return f'''<div style="flex:1;background:{bg};border-radius:8px;padding:20px 0;display:flex;flex-direction:column;align-items:center;gap:8px">
        {ic}<span style="font-family:{COND};font-weight:700;font-size:18px;letter-spacing:2px;color:{fg}">{lab}</span></div>'''
    ph=f'''<div style="position:absolute;inset:0;background:{BG};padding:64px 52px;display:flex;flex-direction:column;justify-content:space-between">
      <div style="display:flex;justify-content:space-between;align-items:baseline">
        <span style="font-family:{IMPACT};font-size:56px;color:{INK};letter-spacing:2px">AUDIO TAPE</span>
        <span style="font-family:{IMPACT};font-size:44px;color:{RED}">C90</span></div>
      <div style="height:6px;background:{RED};margin-top:12px"></div>
      <div style="height:6px;background:{OR};margin-top:4px"></div>
      <div style="height:6px;background:{YEL};margin-top:4px"></div>
      <div style="margin-top:44px">{tape(960)}</div>
      <div style="background:{CREAM};border-radius:10px;padding:32px 30px;margin-top:36px">
        <div style="font-family:{COND};font-weight:700;font-size:22px;letter-spacing:4px;color:{OR}">NOW PLAYING · SIDE A</div>
        <div style="font-family:{IMPACT};font-size:52px;color:{INK};margin-top:10px;letter-spacing:1px">BROTHERS IN ARMS</div>
        <div style="font-family:{COND};font-size:26px;color:#8a7c66;margin-top:4px">Dire Straits · 1985</div>
        {pbar(62,'#d4c9a8',RED,9,mt=26,knob=22,kc=RED)}
        {hb('04:12','06:58','#8a7c66',21,MONO,1,10)}
      </div>
      <div style="margin-top:26px">
        {''.join(f'<div style="display:flex;justify-content:space-between;padding:16px 0;border-bottom:1px solid #ded3b8;font-family:{COND};font-size:26px;color:{INK if i==1 else "#8a7c66"}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:22px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('A1','So Far Away','5:12'),('A2','Brothers in Arms','6:58'),('A3','Money for Nothing','8:26'),('A4','Walk of Life','4:12'),('A5','Your Latest Trick','6:33')]))}
      </div>
      <div style="display:flex;gap:12px;margin-top:24px">
        {flatbtn(prev(32,INK),'PREV',CREAM,INK)}{flatbtn(tri(36,'#fff'),'PLAY',RED,'#fff')}{flatbtn(pausei(32,INK),'PAUSE',CREAM,INK)}
        {flatbtn(nexti(32,INK),'NEXT',CREAM,INK)}{flatbtn(libicon(32,'#fff'),'LIBRARY',OR,'#fff')}</div>
    </div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{BG};padding:52px 66px;display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:baseline">
        <span style="font-family:{IMPACT};font-size:52px;color:{INK};letter-spacing:2px">AUDIO TAPE</span>
        <div style="flex:1;margin:0 30px"><div style="height:5px;background:{RED}"></div><div style="height:5px;background:{OR};margin-top:3px"></div><div style="height:5px;background:{YEL};margin-top:3px"></div></div>
        <span style="font-family:{IMPACT};font-size:40px;color:{RED}">C90</span></div>
      <div style="display:flex;gap:50px;flex:1;margin-top:30px">
        <div style="flex:1.1;display:flex;flex-direction:column;justify-content:center">{tape(680)}</div>
        <div style="flex:1;display:flex;flex-direction:column">
          <div style="background:{CREAM};border-radius:10px;padding:28px">
            <div style="font-family:{COND};font-weight:700;font-size:20px;letter-spacing:4px;color:{OR}">NOW PLAYING · SIDE A</div>
            <div style="font-family:{IMPACT};font-size:46px;color:{INK};margin-top:8px">BROTHERS IN ARMS</div>
            <div style="font-family:{COND};font-size:24px;color:#8a7c66;margin-top:4px">Dire Straits · 1985</div>
            {pbar(62,'#d4c9a8',RED,9,mt=22,knob=20,kc=RED)}
            {hb('04:12','06:58','#8a7c66',20,MONO,1,10)}</div>
          <div style="margin-top:18px">
            {''.join(f'<div style="display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid #ded3b8;font-family:{COND};font-size:24px;color:{INK if i==1 else "#8a7c66"}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:20px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('A1','So Far Away','5:12'),('A2','Brothers in Arms','6:58'),('A3','Money for Nothing','8:26'),('A4','Walk of Life','4:12')]))}</div>
          <div style="display:flex;gap:11px;margin-top:auto">
            {flatbtn(prev(30,INK),'PREV',CREAM,INK)}{flatbtn(tri(34,'#fff'),'PLAY',RED,'#fff')}{flatbtn(pausei(30,INK),'PAUSE',CREAM,INK)}
            {flatbtn(nexti(30,INK),'NEXT',CREAM,INK)}{flatbtn(libicon(30,'#fff'),'LIBRARY',OR,'#fff')}</div>
        </div></div></div>'''
    add('25','Audio-Tape-C90','iphone',ph); add('25','Audio-Tape-C90','pc',pc)
d25()

# =========================================================================
# 26 · TRUE SOUND (beige Kassette, Regenbogenstreifen, Schreibschrift)
# =========================================================================
def d26():
    BG='#2e2f31'; BEIGE='#d8cfa8'; INK='#3a3a38'; BLUE='#2f7bd0'
    RB=['#5aa832','#e8b93e','#e07a2a','#c9402e','#8a4bc9','#2f7bd0']
    SCRIPT="'Brush Script MT','Segoe Script',cursive"
    def tape(w):
        return cassette(w,shell='#d8cfa8',label='#f7f4ea',text=INK,hubfill='#e8e2cc',screws='#a89e78',
                        stripes=RB,title='to my love',sub='',script=True,side='A')
    def pill(ic,lab,active=False):
        return f'''<div style="flex:1;border-radius:40px;padding:20px 0;display:flex;flex-direction:column;align-items:center;gap:8px;
        background:{'#f2eddc' if active else 'rgba(216,207,168,.14)'};border:1.5px solid {'#f2eddc' if active else 'rgba(216,207,168,.35)'}">
        {ic}<span style="font-family:{SANS};font-size:17px;letter-spacing:2px;color:{'#2e2f31' if active else '#c9c0a0'}">{lab}</span></div>'''
    ph=f'''<div style="position:absolute;inset:0;background:{BG};padding:60px 48px;display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:center;font-family:{SANS};font-size:21px;letter-spacing:3px;color:#9a9488">
        <span>A SIDE</span><span style="display:flex;gap:6px">{''.join(f'<div style="width:26px;height:8px;border-radius:4px;background:{c}"></div>' for c in RB)}</span></div>
      <div style="margin-top:34px">{tape(984)}</div>
      <div style="margin-top:34px;text-align:center">
        <div style="font-family:{SCRIPT};font-size:74px;color:{BLUE}">to my love</div>
        <div style="font-family:{SANS};font-size:24px;letter-spacing:5px;color:#9a9488;margin-top:8px">TRUE SOUND · MIXTAPE 07</div></div>
      <div style="margin-top:30px">
        {''.join(f'<div style="display:flex;align-items:center;gap:18px;padding:16px 0;border-bottom:1px solid #3d3e40"><div style="width:10px;height:26px;border-radius:5px;background:{RB[i]}"></div><span style="flex:1;font-family:{SANS};font-size:25px;color:{"#f2eddc" if i==2 else "#9a9488"}">{t}</span><span style="font-family:{MONO};font-size:20px;color:#7e786c">{d}</span></div>' for i,(t,d) in enumerate([('First Light','3:04'),('Slow Dance','4:12'),('To My Love','5:26'),('Rewind','3:48')]))}
      </div>
      {pbar(48,'#434446',BLUE,8,mt=28,knob=22,kc='#f2eddc')}
      {hb('02:38','05:26','#9a9488',21,MONO,1,12)}
      <div style="display:flex;gap:12px;margin-top:auto">
        {pill(prev(30,'#c9c0a0'),'PREV')}{pill(tri(34,'#2e2f31'),'PLAY',True)}{pill(pausei(30,'#c9c0a0'),'PAUSE')}
        {pill(nexti(30,'#c9c0a0'),'NEXT')}{pill(libicon(30,'#c9c0a0'),'LIBRARY')}</div>
    </div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{BG};padding:48px 60px;display:flex;gap:56px;align-items:center">
      <div style="flex:1.15">{tape(720)}
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:22px;font-family:{SANS};font-size:19px;letter-spacing:3px;color:#9a9488">
          <span>A SIDE · TRUE SOUND</span><span style="display:flex;gap:5px">{''.join(f'<div style="width:24px;height:7px;border-radius:4px;background:{c}"></div>' for c in RB)}</span></div></div>
      <div style="flex:1;display:flex;flex-direction:column">
        <div style="font-family:{SCRIPT};font-size:76px;color:{BLUE};line-height:1">to my love</div>
        <div style="font-family:{SANS};font-size:21px;letter-spacing:5px;color:#9a9488;margin-top:8px">MIXTAPE 07 · TRACK 03</div>
        <div style="margin-top:26px">
          {''.join(f'<div style="display:flex;align-items:center;gap:16px;padding:14px 0;border-bottom:1px solid #3d3e40"><div style="width:9px;height:24px;border-radius:5px;background:{RB[i]}"></div><span style="flex:1;font-family:{SANS};font-size:23px;color:{"#f2eddc" if i==2 else "#9a9488"}">{t}</span><span style="font-family:{MONO};font-size:19px;color:#7e786c">{d}</span></div>' for i,(t,d) in enumerate([('First Light','3:04'),('Slow Dance','4:12'),('To My Love','5:26'),('Rewind','3:48')]))}</div>
        {pbar(48,'#434446',BLUE,8,mt=24,knob=20,kc='#f2eddc')}
        {hb('02:38','05:26','#9a9488',20,MONO,1,10)}
        <div style="display:flex;gap:11px;margin-top:28px">
          {pill(prev(28,'#c9c0a0'),'PREV')}{pill(tri(32,'#2e2f31'),'PLAY',True)}{pill(pausei(28,'#c9c0a0'),'PAUSE')}
          {pill(nexti(28,'#c9c0a0'),'NEXT')}{pill(libicon(28,'#c9c0a0'),'LIBRARY')}</div>
      </div></div>'''
    add('26','True-Sound','iphone',ph); add('26','True-Sound','pc',pc)
d26()

print('V3 A+B:', len(D))

# =========================================================================
# 27 · STEREO 60 (blaue Kassette, rot/gelber Streifen, Vektor-Look)
# =========================================================================
def d27():
    BLUE='#3a4d9e'; DEEP='#2b3a7a'; CREAM='#efeade'; RED='#d8412e'; YEL='#e8bb3a'; INK='#2a2a30'
    BG='#e8eaf2'
    def tape(w):
        return cassette(w,shell='#3a4d9e',label='#efeade',text=INK,hubfill='#f0c46a',screws='#8e97c4',
                        stripes=[RED,YEL],title='STEREO',sub='2 X 30 MIN',side='A')
    def btn(ic,lab,solid=False):
        return f'''<div style="flex:1;border-radius:10px;padding:20px 0;display:flex;flex-direction:column;align-items:center;gap:8px;
        background:{BLUE if solid else '#fff'};border:2px solid {BLUE};box-shadow:0 4px 0 {DEEP}">
        {ic}<span style="font-family:{SANS};font-weight:700;font-size:17px;letter-spacing:2px;color:{'#fff' if solid else BLUE}">{lab}</span></div>'''
    ph=f'''<div style="position:absolute;inset:0;background:{BG};padding:60px 50px;display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:baseline">
        <span style="font-family:{SANS};font-weight:800;font-size:44px;color:{BLUE};letter-spacing:-1px">STEREO 60</span>
        <span style="font-family:{SANS};font-size:22px;color:#8a90ab;letter-spacing:3px">2×30 MIN</span></div>
      <div style="height:5px;background:{RED};margin-top:14px"></div><div style="height:5px;background:{YEL};margin-top:3px"></div>
      <div style="margin-top:40px">{tape(960)}</div>
      <div style="background:#fff;border:2px solid {BLUE};border-radius:12px;padding:30px 28px;margin-top:36px">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-family:{SANS};font-weight:700;font-size:21px;letter-spacing:3px;color:{RED}">▶ SIDE A · 02</span>
          <span style="font-family:{MONO};font-size:22px;color:#8a90ab">02:44 / 04:18</span></div>
        <div style="font-family:{SANS};font-weight:800;font-size:46px;color:{INK};margin-top:12px">Blue Monday</div>
        <div style="font-family:{SANS};font-size:23px;color:#8a90ab;margin-top:4px">New Order · Power, Corruption &amp; Lies</div>
        {pbar(64,'#dfe2ee',BLUE,10,mt:=24 if False else 24,knob=24,kc=RED)}
      </div>
      <div style="margin-top:26px">
        {''.join(f'<div style="display:flex;justify-content:space-between;padding:16px 20px;border-radius:8px;margin-bottom:8px;background:{"#fff" if i==1 else "transparent"};border:2px solid {BLUE if i==1 else "transparent"};font-family:{SANS};font-size:24px;color:{INK if i==1 else "#8a90ab"}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:20px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('01','Age of Consent','5:15'),('02','Blue Monday','4:18'),('03','The Village','4:36')]))}
      </div>
      <div style="display:flex;gap:12px;margin-top:auto">
        {btn(prev(30,BLUE),'PREV')}{btn(tri(34,'#fff'),'PLAY',True)}{btn(pausei(30,BLUE),'PAUSE')}{btn(nexti(30,BLUE),'NEXT')}{btn(libicon(30,BLUE),'LIBRARY')}</div>
    </div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{BG};padding:50px 64px;display:flex;flex-direction:column">
      <div style="display:flex;align-items:baseline;gap:26px">
        <span style="font-family:{SANS};font-weight:800;font-size:42px;color:{BLUE};letter-spacing:-1px">STEREO 60</span>
        <div style="flex:1"><div style="height:5px;background:{RED}"></div><div style="height:5px;background:{YEL};margin-top:3px"></div></div>
        <span style="font-family:{SANS};font-size:20px;color:#8a90ab;letter-spacing:3px">2×30 MIN</span></div>
      <div style="display:flex;gap:50px;flex:1;margin-top:28px">
        <div style="flex:1.1;display:flex;align-items:center">{tape(690)}</div>
        <div style="flex:1;display:flex;flex-direction:column">
          <div style="background:#fff;border:2px solid {BLUE};border-radius:12px;padding:26px">
            <span style="font-family:{SANS};font-weight:700;font-size:19px;letter-spacing:3px;color:{RED}">▶ SIDE A · 02</span>
            <div style="font-family:{SANS};font-weight:800;font-size:44px;color:{INK};margin-top:10px">Blue Monday</div>
            <div style="font-family:{SANS};font-size:22px;color:#8a90ab;margin-top:4px">New Order · Power, Corruption &amp; Lies</div>
            {pbar(64,'#dfe2ee',BLUE,10,mt=22,knob=22,kc=RED)}
            {hb('02:44','04:18','#8a90ab',20,MONO,1,10)}</div>
          <div style="margin-top:18px">
            {''.join(f'<div style="display:flex;justify-content:space-between;padding:14px 18px;border-radius:8px;margin-bottom:7px;background:{"#fff" if i==1 else "transparent"};border:2px solid {BLUE if i==1 else "transparent"};font-family:{SANS};font-size:22px;color:{INK if i==1 else "#8a90ab"}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:18px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('01','Age of Consent','5:15'),('02','Blue Monday','4:18'),('03','The Village','4:36')]))}</div>
          <div style="display:flex;gap:11px;margin-top:auto">
            {btn(prev(28,BLUE),'PREV')}{btn(tri(32,'#fff'),'PLAY',True)}{btn(pausei(28,BLUE),'PAUSE')}{btn(nexti(28,BLUE),'NEXT')}{btn(libicon(28,BLUE),'LIBRARY')}</div>
        </div></div></div>'''
    add('27','Stereo-60','iphone',ph); add('27','Stereo-60','pc',pc)
d27()

# =========================================================================
# 28 · WE ARE REWIND Boombox (schwarz, orange VU, gelbe REC-Taste, Speaker)
# =========================================================================
def d28():
    BLK='#141414'; PANEL='#1c1c1c'; YEL='#f0d000'; GREY='#8e8e8a'
    def deckwin(w):
        return f'''<div style="background:#0e0e0e;border-radius:10px;padding:26px;box-shadow:inset 0 3px 10px #000">
        <div style="text-align:center;font-family:{SANS};font-size:24px;letter-spacing:2px;color:#e6e6e2;margin-bottom:18px">
          <span style="color:{YEL};font-size:30px">◗◗</span> we are rew<span style="color:{YEL}">i</span>nd</div>
        <div style="background:rgba(210,205,180,.16);border:1px solid #33332f;border-radius:6px;padding:16px">
          {cassette(w,shell='#c9c2a4',label='#efeade',text='#2b2b28',hubfill='#2a2a28',screws='#8e8874',
                    title='UND DER SUPER-PAPAGEI',sub='STUDIO EUROPA · SEITE 1',side='1')}</div>
        <div style="display:flex;justify-content:center;align-items:center;gap:12px;margin-top:16px;font-family:{SANS};font-size:19px;letter-spacing:3px;color:{GREY}">
          FULL AUTO STOP <span style="font-size:24px">⟶</span></div></div>'''
    def rbtn(lab,ic,yellow=False):
        return f'''<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:9px">
        <span style="font-family:{SANS};font-size:16px;letter-spacing:1px;color:#cfcfcb;display:flex;align-items:center;gap:5px">{lab}{ic}</span>
        <div style="width:100%;height:74px;border-radius:6px;background:{'linear-gradient(180deg,#f5d800,#d8bb00)' if yellow else 'linear-gradient(180deg,#2b2b2b,#1a1a1a)'};
        border:1px solid {'#c9ae00' if yellow else '#333'};box-shadow:0 4px 0 {'#b89e00' if yellow else '#0c0c0c'},inset 0 2px 3px rgba(255,255,255,{'.5' if yellow else '.08'})"></div></div>'''
    vus=lambda w,h:f'<div style="display:flex;gap:18px;justify-content:center">{vu_amber(w,h,0.28)}{vu_amber(w,h,0.40)}</div>'
    ph=f'''<div style="position:absolute;inset:0;background:{BLK};padding:50px 40px;display:flex;flex-direction:column">
      {vus(450,170)}
      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:30px">
        {speaker(210)}
        <div style="flex:1;padding:0 20px;text-align:center">
          <div style="font-family:{SANS};font-size:38px;color:#f2f2ee;font-weight:600">Die drei ???</div>
          <div style="font-family:{SANS};font-size:22px;color:{GREY};margin-top:6px">Folge 41 · Seite 1</div></div>
        {speaker(210)}</div>
      <div style="margin-top:26px">{deckwin(820)}</div>
      {pbar(34,'#2b2b2b',YEL,8,mt=26,knob=22,kc=YEL)}
      {hb('12:44','44:20',GREY,21,MONO,1,12)}
      <div style="display:flex;gap:10px;margin-top:auto">
        {rbtn('REC','<span style="color:#e04030">●</span>',True)}{rbtn('PLAY',f'<span style="color:{YEL}">▶</span>')}
        {rbtn('REW','<span>◀◀</span>')}{rbtn('F.FWD','<span>▶▶</span>')}
        {rbtn('STOP<br>EJECT','<span style="color:'+YEL+'">■▲</span>')}{rbtn('PAUSE','<span>❚❚</span>')}</div>
    </div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{BLK};padding:44px 54px;display:flex;align-items:center;gap:40px">
      {speaker(300)}
      <div style="flex:1;display:flex;flex-direction:column;gap:22px">
        {vus(340,150)}
        {deckwin(600)}
        <div>{pbar(34,'#2b2b2b',YEL,8,knob=20,kc=YEL)}{hb('12:44','44:20',GREY,20,MONO,1,10)}</div>
        <div style="display:flex;gap:9px">
          {rbtn('REC','<span style="color:#e04030">●</span>',True)}{rbtn('PLAY',f'<span style="color:{YEL}">▶</span>')}
          {rbtn('REW','<span>◀◀</span>')}{rbtn('F.FWD','<span>▶▶</span>')}
          {rbtn('STOP EJECT','<span style="color:'+YEL+'">■▲</span>')}{rbtn('PAUSE','<span>❚❚</span>')}</div>
      </div>
      {speaker(300)}</div>'''
    add('28','Rewind-Boombox','iphone',ph); add('28','Rewind-Boombox','pc',pc)
d28()

# =========================================================================
# 29 · WE ARE REWIND Deck-Nahaufnahme (nur Panel, hochkant)
# =========================================================================
def d29():
    BLK='#0f0f0f'; YEL='#f0d000'; GREY='#8e8e8a'; AMB='#f5a623'
    def key(lab,sym,yellow=False,wide=1):
        return f'''<div style="flex:{wide};display:flex;flex-direction:column;align-items:center;gap:10px">
        <span style="font-family:{SANS};font-size:17px;letter-spacing:1px;color:#d4d4d0;white-space:nowrap">{lab} {sym}</span>
        <div style="width:100%;height:92px;border-radius:8px;background:{'linear-gradient(180deg,#f5d800,#d4b800)' if yellow else 'radial-gradient(ellipse at 50% 30%,#2e2e2e,#161616)'};
        border:1px solid {'#c9ae00' if yellow else '#2e2e2e'};box-shadow:0 5px 0 {'#b09800' if yellow else '#080808'},inset 0 2px 4px rgba(255,255,255,{'.55' if yellow else '.07'})"></div></div>'''
    ph=f'''<div style="position:absolute;inset:0;background:{BLK};padding:54px 44px;display:flex;flex-direction:column">
      <div style="display:flex;gap:20px">{vu_amber(470,190,0.26)}{vu_amber(470,190,0.38)}</div>
      <div style="text-align:center;margin-top:44px;font-family:{SANS};font-size:34px;letter-spacing:2px;color:#eceae4">
        <span style="color:{YEL};font-size:40px">◗◗</span> we are rew<span style="color:{YEL}">i</span>nd</div>
      <div style="background:#151515;border:1px solid #2a2a2a;border-radius:12px;padding:28px;margin-top:30px">
        <div style="background:rgba(214,208,178,.18);border-radius:8px;padding:18px">
          {cassette(880,shell='#c9c2a4',label='#f0ebda',text='#2b2b28',hubfill='#2a2a28',screws='#8e8874',
                    title='UND DER SUPER-PAPAGEI',sub='Ein Studio EUROPA-Produktion · STEREO',side='1')}</div>
        <div style="display:flex;justify-content:center;align-items:center;gap:14px;margin-top:20px;font-family:{SANS};font-size:21px;letter-spacing:4px;color:{GREY}">
          FULL AUTO STOP <span style="font-size:26px">⟶</span></div></div>
      <div style="margin-top:32px">
        <div style="display:flex;justify-content:space-between;align-items:baseline">
          <span style="font-family:{SANS};font-size:34px;color:#f2f2ee;font-weight:600">Der super Papagei</span>
          <span style="font-family:{MONO};font-size:22px;color:{GREY}">12:44 / 44:20</span></div>
        {pbar(29,'#262626',AMB,8,mt=16,knob=22,kc=AMB)}</div>
      <div style="display:flex;gap:10px;margin-top:auto">
        {key('REC','<span style="color:#e04030">●</span>',True)}{key('PLAY',f'<span style="color:{YEL}">▶</span>')}
        {key('REW','◀◀')}{key('F.FWD','▶▶')}{key('STOP<br>EJECT',f'<span style="color:{YEL}">■▲</span>')}{key('PAUSE','❚❚')}</div>
    </div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{BLK};padding:44px 60px;display:flex;gap:50px">
      <div style="flex:1.1;display:flex;flex-direction:column;justify-content:center;gap:24px">
        <div style="display:flex;gap:16px">{vu_amber(330,160,0.26)}{vu_amber(330,160,0.38)}</div>
        <div style="background:#151515;border:1px solid #2a2a2a;border-radius:12px;padding:22px">
          <div style="text-align:center;font-family:{SANS};font-size:26px;letter-spacing:2px;color:#eceae4;margin-bottom:14px">
            <span style="color:{YEL};font-size:30px">◗◗</span> we are rew<span style="color:{YEL}">i</span>nd</div>
          <div style="background:rgba(214,208,178,.18);border-radius:8px;padding:14px">
            {cassette(600,shell='#c9c2a4',label='#f0ebda',text='#2b2b28',hubfill='#2a2a28',screws='#8e8874',
                      title='UND DER SUPER-PAPAGEI',sub='Studio EUROPA · STEREO',side='1')}</div></div>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
        <div style="font-family:{SANS};font-size:44px;color:#f2f2ee;font-weight:600;line-height:1.1">Der super<br>Papagei</div>
        <div style="font-family:{SANS};font-size:22px;color:{GREY};margin-top:10px">Die drei ??? · Folge 41 — Seite 1</div>
        <div style="margin-top:26px">
          {''.join(f'<div style="display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid #262626;font-family:{SANS};font-size:21px;color:{"#f2f2ee" if i==1 else GREY}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:18px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('01','Kapitel 1','11:20'),('02','Kapitel 2','12:40'),('03','Kapitel 3','10:05')]))}</div>
        {pbar(29,'#262626',AMB,8,mt=22,knob=20,kc=AMB)}
        {hb('12:44','44:20',GREY,20,MONO,1,10)}
        <div style="display:flex;gap:9px;margin-top:26px">
          {key('REC','<span style="color:#e04030">●</span>',True)}{key('PLAY',f'<span style="color:{YEL}">▶</span>')}
          {key('REW','◀◀')}{key('F.FWD','▶▶')}{key('STOP EJECT',f'<span style="color:{YEL}">■▲</span>')}{key('PAUSE','❚❚')}</div>
      </div></div>'''
    add('29','Rewind-Deck','iphone',ph); add('29','Rewind-Deck','pc',pc)
d29()

# =========================================================================
# 30 · Weisser iPod-App-Look (Punktraster-Grille, Clickwheel, orange Akzent)
# =========================================================================
def d30():
    BG='#f2f0ed'; CARD='#faf9f7'; INK='#3a3a38'; OR='#e8681a'; SUB='#a8a6a1'; LINE='#e4e2de'
    def wheel(size):
        inner=size*0.34
        return f'''<div style="position:relative;width:{size}px;height:{size}px">
        <div style="position:absolute;inset:0;border-radius:50%;border:1.5px solid #dcdad6;background:radial-gradient(circle at 40% 32%,#ffffff,#f2f0ec)"></div>
        <div style="position:absolute;left:50%;top:{size*0.07:.0f}px;transform:translateX(-50%)">{pausei(size*0.10,SUB)}</div>
        <div style="position:absolute;right:{size*0.07:.0f}px;top:50%;transform:translateY(-50%)">{nexti(size*0.10,SUB)}</div>
        <div style="position:absolute;left:{size*0.07:.0f}px;top:50%;transform:translateY(-50%)">{prev(size*0.10,SUB)}</div>
        <div style="position:absolute;left:50%;bottom:{size*0.07:.0f}px;transform:translateX(-50%)">{libicon(size*0.10,OR)}</div>
        <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:{inner}px;height:{inner}px;border-radius:50%;
          background:radial-gradient(circle at 40% 34%,#ffffff,#e8e6e2);border:1.5px solid #dcdad6;display:flex;align-items:center;justify-content:center">{tri(inner*0.34,INK)}</div>
        <div style="position:absolute;left:{size*0.28:.0f}px;top:{size*0.20:.0f}px">{tri(size*0.075,OR)}</div></div>'''
    def nowbar(w):
        return f'''<div style="background:#eceae6;border:1px solid {LINE};border-radius:8px;padding:16px 20px">
        <div style="font-family:{SANS};font-size:18px;color:{OR};letter-spacing:1px">Now playing</div>
        <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:6px">
          <span style="font-family:{SANS};font-size:26px;color:{INK}">John Lennon — Imagine</span>
          <span style="font-family:{MONO};font-size:22px;color:{SUB}">0:32</span></div></div>'''
    def track(a,t,d,cur=False):
        return f'''<div style="display:flex;align-items:center;gap:18px;padding:16px 18px;border-bottom:1px solid {LINE};background:{'#f6f4f0' if cur else 'transparent'}">
        <div style="width:44px;height:44px;border-radius:6px;background:#e8e6e2;display:flex;align-items:center;justify-content:center;font-family:{SANS};font-size:20px;color:{SUB}">♪</div>
        <div style="flex:1"><div style="font-family:{SANS};font-size:19px;color:{OR}">{a}</div>
          <div style="font-family:{SANS};font-size:24px;color:{INK};margin-top:2px">{t}</div></div>
        <span style="font-family:{MONO};font-size:20px;color:{SUB}">{d}</span></div>'''
    ph=f'''<div style="position:absolute;inset:0;background:{BG};padding:46px 40px;display:flex;flex-direction:column">
      <div style="background:{CARD};border:1px solid {LINE};border-radius:20px;padding:34px 30px;box-shadow:0 12px 30px rgba(0,0,0,.10)">
        <div style="display:flex;justify-content:center">{dotgrid(600,300,'#3a3a38',5.5,26,1,True)}</div>
        <div style="margin-top:24px">{nowbar(600)}</div>
        <div style="display:flex;justify-content:center;margin-top:30px">{wheel(430)}</div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:24px">
          {listicon(38,SUB)}<div style="flex:1;margin:0 22px">{pbar(22,'#e4e2de',OR,6,knob=18,kc=OR)}</div>{shuffle(34,SUB)}</div>
      </div>
      <div style="background:{CARD};border:1px solid {LINE};border-radius:16px;margin-top:24px;flex:1;overflow:hidden">
        <div style="padding:18px 20px;border-bottom:1px solid {LINE};display:flex;justify-content:space-between;font-family:{SANS};font-size:21px;color:{SUB};letter-spacing:1px">
          <span>LIBRARY · A–Z</span><span style="color:{OR}">Rank</span></div>
        {track('John Lennon','Imagine','2:55',True)}{track('The Beatles','Lucy in The Sky','3:21')}
        {track('Pink Floyd','Proper Education','5:32')}{track('Janis Joplin','Summertime','5:32')}{track('Pink Floyd','Money','5:32')}
        {track('The Doors','Riders on the Storm','7:09')}{track('Fleetwood Mac','Dreams','4:14')}{track('Bowie','Heroes','6:07')}
      </div></div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{BG};padding:44px 56px;display:flex;gap:36px">
      <div style="width:460px;background:{CARD};border:1px solid {LINE};border-radius:20px;padding:32px 28px;box-shadow:0 12px 30px rgba(0,0,0,.10);display:flex;flex-direction:column">
        <div style="display:flex;justify-content:center">{dotgrid(390,190,'#3a3a38',5,24,1,True)}</div>
        <div style="margin-top:20px">{nowbar(390)}</div>
        <div style="display:flex;justify-content:center;margin-top:auto">{wheel(330)}</div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:22px">
          {listicon(34,SUB)}<div style="flex:1;margin:0 18px">{pbar(22,'#e4e2de',OR,6,knob=16,kc=OR)}</div>{shuffle(30,SUB)}</div>
      </div>
      <div style="flex:1;background:{CARD};border:1px solid {LINE};border-radius:20px;overflow:hidden;display:flex;flex-direction:column">
        <div style="padding:22px 26px;border-bottom:1px solid {LINE};display:flex;justify-content:space-between;align-items:center">
          <div><div style="font-family:{SANS};font-size:26px;color:{OR}">Geographer</div>
            <div style="font-family:{SANS};font-size:34px;color:{INK};font-weight:600">Myth</div>
            <div style="font-family:{SANS};font-size:19px;color:{SUB};margin-top:2px">10 songs, 42 minutes</div></div>
          <div style="display:flex;gap:14px">{libicon(34,OR)}{shuffle(32,SUB)}</div></div>
        {track('Geographer','Life Of Crime','4:29')}{track('Geographer','The Myth Of Youth','4:08')}
        {track('Geographer','Kaleidoscope','4:37')}{track('Geographer','Blinders','3:44',True)}{track('Geographer','Lover’s Game','3:53')}
        <div style="margin-top:auto;padding:20px 26px;border-top:1px solid {LINE};display:flex;align-items:center;gap:20px">
          {prev(30,INK)}{tri(34,INK)}{nexti(30,INK)}
          <div style="flex:1">{pbar(48,'#e4e2de',OR,6,knob=16,kc=OR)}</div>
          <span style="font-family:{MONO};font-size:19px;color:{SUB}">1:47 / 3:44</span></div>
      </div></div>'''
    add('30','iPod-Weiss','iphone',ph); add('30','iPod-Weiss','pc',pc)
d30()

print('V3 A+B+C:', len(D))

# =========================================================================
# 31 · Vinyl auf Creme (rote Runde Tasten, Slider mit Tooltip, Logo-Kachel)
# =========================================================================
def d31():
    BG='#f2ede2'; INK='#2e2b26'; RED='#c9403c'; SUB='#a09a8e'; LINE='#ddd6c8'
    logo=f'''<div style="display:flex;align-items:center;gap:18px">
      <div style="width:76px;height:76px;background:{RED};border-radius:6px;display:flex;align-items:center;justify-content:center">
        <span style="font-family:{SERIF};font-size:44px;color:#fff">♪</span></div>
      <div style="font-family:{IMPACT};font-size:26px;line-height:1.15;color:{INK};letter-spacing:1px">PIEN FEITH<br>BETTY FORD<br>TOUGH LOVE</div></div>'''
    def rbtn(ic,size=86):
        return f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:linear-gradient(180deg,#d8514c,{RED});box-shadow:0 5px 12px rgba(160,50,45,.45),inset 0 2px 3px rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center">{ic}</div>'
    def tooltip(txt):
        return f'''<div style="position:relative;display:inline-block">
        <div style="background:#fbf8f0;border:1px solid {LINE};border-radius:6px;padding:8px 16px;font-family:{MONO};font-size:22px;color:{INK};box-shadow:0 3px 8px rgba(0,0,0,.10)">{txt}</div>
        <div style="position:absolute;left:50%;bottom:-7px;transform:translateX(-50%) rotate(45deg);width:12px;height:12px;background:#fbf8f0;border-right:1px solid {LINE};border-bottom:1px solid {LINE}"></div></div>'''
    def slider(w):
        return f'''<div style="position:relative;height:22px;border-radius:11px;background:linear-gradient(180deg,#d8d2c4,#eae5d8);box-shadow:inset 0 2px 5px rgba(0,0,0,.22)">
        <div style="position:absolute;left:0;top:0;height:22px;width:68%;border-radius:11px;background:linear-gradient(180deg,#8e8878,#b4ae9e)"></div>
        <div style="position:absolute;left:68%;top:50%;transform:translate(-50%,-50%);width:36px;height:36px;border-radius:50%;background:radial-gradient(circle at 38% 32%,#fff,#ddd7c9);box-shadow:0 3px 8px rgba(0,0,0,.3)"></div></div>'''
    ph=f'''<div style="position:absolute;inset:0;background:{BG};padding:56px 50px;display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">{logo}
        <div style="width:76px;height:76px;border:1.5px solid {LINE};border-radius:8px;display:flex;align-items:center;justify-content:center;background:#fbf8f0">{libicon(34,RED)}</div></div>
      <div style="height:1px;background:{LINE};margin:26px 0"></div>
      <div style="display:flex;justify-content:center;margin-top:10px">{vinyl(780,RED)}</div>
      <div style="text-align:center;margin-top:30px">
        <div style="font-family:{SANS};font-size:44px;font-weight:600;color:{INK}">Tough Love</div>
        <div style="font-family:{SANS};font-size:24px;color:{SUB};margin-top:6px">Pien Feith · Betty Ford — 33⅓ RPM</div></div>
      <div style="display:flex;justify-content:flex-end;margin-top:auto">{tooltip('03:23')}</div>
      <div style="margin-top:10px">{slider(940)}</div>
      <div style="display:flex;justify-content:center;gap:30px;margin-top:34px">
        {rbtn(rew(34,'#fff'))}{rbtn(tri(40,'#fff'),110)}{rbtn(ffwd(34,'#fff'))}</div>
      <div style="display:flex;justify-content:center;gap:56px;margin-top:24px">
        <span style="font-family:{SANS};font-size:19px;letter-spacing:2px;color:{SUB}">SHUFFLE</span>
        <span style="font-family:{SANS};font-size:19px;letter-spacing:2px;color:{SUB}">REPEAT</span>
        <span style="font-family:{SANS};font-size:19px;letter-spacing:2px;color:{RED}">LIBRARY</span></div>
    </div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{BG};padding:48px 64px;display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">{logo}
        <div style="display:flex;gap:14px">
          <div style="width:70px;height:70px;border:1.5px solid {LINE};border-radius:8px;display:flex;align-items:center;justify-content:center;background:#fbf8f0">{shuffle(30,SUB)}</div>
          <div style="width:70px;height:70px;border:1.5px solid {LINE};border-radius:8px;display:flex;align-items:center;justify-content:center;background:#fbf8f0">{libicon(32,RED)}</div></div></div>
      <div style="height:1px;background:{LINE};margin:22px 0"></div>
      <div style="display:flex;gap:70px;flex:1;align-items:center">
        <div>{vinyl(520,RED)}</div>
        <div style="flex:1;display:flex;flex-direction:column">
          <div style="font-family:{SANS};font-size:52px;font-weight:600;color:{INK}">Tough Love</div>
          <div style="font-family:{SANS};font-size:23px;color:{SUB};margin-top:6px">Pien Feith · Betty Ford — 33⅓ RPM</div>
          <div style="margin-top:26px">
            {''.join(f'<div style="display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid {LINE};font-family:{SANS};font-size:22px;color:{INK if i==1 else SUB}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:20px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('A1','Betty Ford','4:02'),('A2','Tough Love','5:18'),('A3','Golden','3:44')]))}</div>
          <div style="display:flex;justify-content:flex-end;margin-top:22px">{tooltip('03:23')}</div>
          <div style="margin-top:8px">{slider(640)}</div>
          <div style="display:flex;gap:26px;margin-top:28px">{rbtn(rew(30,'#fff'),78)}{rbtn(tri(36,'#fff'),98)}{rbtn(ffwd(30,'#fff'),78)}</div>
        </div></div></div>'''
    add('31','Vinyl-Rote-Tasten','iphone',ph); add('31','Vinyl-Rote-Tasten','pc',pc)
d31()

# =========================================================================
# 32 · Schwarzer Skeuomorph (Kassette mit weissen Naben, LCD-Titelband)
# =========================================================================
def d32():
    BLK='linear-gradient(180deg,#26262a,#141418)'; LCD='#0d1a16'; GREEN='#7fe8b0'; STEEL='#5a5a60'
    def lcdbar(w,vertical=False):
        rot='writing-mode:vertical-rl;transform:rotate(180deg);' if vertical else ''
        return f'''<div style="background:{LCD};border:1px solid #2e3a36;border-radius:6px;padding:18px 22px;box-shadow:inset 0 3px 10px #000;{rot}">
        <div style="font-family:{MONO};font-size:18px;letter-spacing:3px;color:#3f6f5c">TITLE</div>
        <div style="font-family:{MONO};font-size:30px;letter-spacing:2px;color:{GREEN};margin-top:6px;text-shadow:0 0 12px rgba(127,232,176,.5)">NIRVANA — NEGATIVE CREEP</div>
        <div style="font-family:{MONO};font-size:22px;color:#4f8f74;margin-top:6px">· 04:34</div></div>'''
    def mbtn(ic,size=100):
        return f'''<div style="width:{size}px;height:{size}px;border-radius:12px;background:linear-gradient(180deg,#3a3a40,#232328);
        border:1px solid #4a4a52;box-shadow:0 5px 0 #17171b,0 9px 16px rgba(0,0,0,.5),inset 0 2px 3px rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center">{ic}</div>'''
    ph=f'''<div style="position:absolute;inset:0;background:{BLK};padding:48px 40px;display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:center;font-family:{MONO};font-size:20px;letter-spacing:3px;color:#7a7a82">
        <span>SEATTLE SOUND · MIX A</span><span style="color:{GREEN}">▶ PLAY</span></div>
      <div style="background:#1a1a1e;border:1px solid #303038;border-radius:14px;padding:26px;margin-top:22px;box-shadow:inset 0 3px 12px #000">
        {cassette(900,shell='#8e9098',label='#e8eaee',text='#2b2b30',hubfill='#f2f2f4',screws='#5a5a60',
                  title='SEATTLE SOUND',sub='MIX TAPE · TYPE II',side='A')}</div>
      {lcdbar(900)}
      {pbar(56,'#2a2a30',GREEN,8,mt=22,knob=22,kc=GREEN)}
      {hb('02:34','04:34','#7a7a82',21,MONO,1,12)}
      <div style="margin-top:24px">
        {''.join(f'<div style="display:flex;justify-content:space-between;padding:15px 18px;border-radius:8px;margin-bottom:8px;background:{"#22222a" if i==1 else "transparent"};font-family:{MONO};font-size:21px;color:{GREEN if i==1 else "#7a7a82"}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:20px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('A1','SCHOOL','2:42'),('A2','NEGATIVE CREEP','4:34'),('A3','ABOUT A GIRL','2:48')]))}</div>
      <div style="display:flex;justify-content:space-between;margin-top:auto">
        {mbtn(rew(36,'#c8c8d0'))}{mbtn(tri(40,GREEN))}{mbtn(pausei(36,'#c8c8d0'))}{mbtn(ffwd(36,'#c8c8d0'))}{mbtn(libicon(36,GREEN))}</div>
    </div>'''
    pc=f'''<div style="position:absolute;inset:0;background:{BLK};padding:44px 56px;display:flex;gap:44px;align-items:center">
      <div style="flex:1.15;background:#1a1a1e;border:1px solid #303038;border-radius:14px;padding:26px;box-shadow:inset 0 3px 12px #000">
        {cassette(700,shell='#8e9098',label='#e8eaee',text='#2b2b30',hubfill='#f2f2f4',screws='#5a5a60',
                  title='SEATTLE SOUND',sub='MIX TAPE · TYPE II',side='A')}</div>
      <div style="flex:1;display:flex;flex-direction:column">
        {lcdbar(560)}
        {pbar(56,'#2a2a30',GREEN,8,mt=20,knob=20,kc=GREEN)}
        {hb('02:34','04:34','#7a7a82',20,MONO,1,10)}
        <div style="margin-top:20px">
          {''.join(f'<div style="display:flex;justify-content:space-between;padding:13px 16px;border-radius:8px;margin-bottom:7px;background:{"#22222a" if i==1 else "transparent"};font-family:{MONO};font-size:20px;color:{GREEN if i==1 else "#7a7a82"}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:18px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('A1','SCHOOL','2:42'),('A2','NEGATIVE CREEP','4:34'),('A3','ABOUT A GIRL','2:48')]))}</div>
        <div style="display:flex;gap:14px;margin-top:26px">
          {mbtn(rew(32,'#c8c8d0'),88)}{mbtn(tri(36,GREEN),88)}{mbtn(pausei(32,'#c8c8d0'),88)}{mbtn(ffwd(32,'#c8c8d0'),88)}{mbtn(libicon(32,GREEN),88)}</div>
      </div></div>'''
    add('32','Seattle-Skeuo','iphone',ph); add('32','Seattle-Skeuo','pc',pc)
d32()

print('V3 A-D:', len(D))
