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
    # Ein einziges Instrument, ohne Kanalbuchstabe: die Anzeige ist die Mitte
    # der rechten Spalte, nicht ein Paar am Rand.
    vufeld=lambda w,h:f'''<div style="background:#f2ecd0;border:1.5px solid #b9b39a;border-radius:5px;padding:12px">
      {vumeter(w,h,'#f7f2dc','#2a2a26','#6b6b62','',0.62)}</div>'''
    tasten=f'''<div style="width:100%;max-width:720px;display:flex;gap:11px">
            {sqbtn(rew(32,'#3a3a36'),'REW')}{sqbtn(tri(34,'#3a3a36'),'PLAY','#2ecc40')}{sqbtn(pausei(32,'#3a3a36'),'PAUSE','#f5c400')}
            {sqbtn(ffwd(32,'#3a3a36'),'F.FWD')}{sqbtn('<div style="width:20px;height:20px;background:#3a3a36"></div>','STOP')}
            {sqbtn(eject(32,'#d63a1e'),'LIBRARY')}</div>'''
    pc=f'''<div style="position:absolute;inset:0;background-color:#5c3a20;padding:24px">
      <div style="height:100%;background:{PANEL};border-radius:10px;padding:26px 34px;display:flex;flex-direction:column;box-shadow:0 12px 34px rgba(0,0,0,.5),inset 0 3px 4px #fff">
        <div style="display:flex;align-items:center;gap:40px;flex:1;min-height:0">
          <div style="display:flex;flex-direction:column;align-self:flex-start">{reels(300,22)}<div style="margin-top:16px">{''.join(f'<div style="display:flex;justify-content:space-between;padding:11px 4px;border-bottom:1px solid #bcbcb8;font-family:{SANS};font-size:20px;color:{"#2b2b28" if i==1 else "#7f7f7a"}"><span>{n}</span><span style="flex:1;text-align:left;margin-left:18px">{t}</span><span>{d}</span></div>' for i,(n,t,d) in enumerate([('01','Autobahn','7:12'),('02','Kometenmelodie','6:20'),('03','Mitternacht','3:44')]))}</div></div>
          <div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:30px;align-items:center;justify-content:center">
            {counter(52)}{vufeld(560,352)}{tasten}</div>
        </div>
        <div style="margin-top:auto;padding-top:26px">
          <div style="font-family:{SANS};font-size:44px;font-weight:600;color:#2b2b28">Autobahn</div>
          <div style="font-family:{SANS};font-size:21px;color:#6f6f6a;margin-top:5px">Kraftwerk · Reel B — 4 Track Stereo</div>
          <div style="margin-top:16px">{pbar(38,'#bcbcb8','#d63a1e',8,knob=20,kc='#fbfbfa')}{hb('00:54','07:12','#6f6f6a',20,MONO,1,8)}</div>
        </div></div></div>'''
    add('18','Akai-747','pc',pc)   # kein Hochformat: auf Wunsch des Eigentuemers entfallen
d18()


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
          <div style="flex:1;display:flex;flex-direction:column;justify-content:center">{ctrlbar(0)}</div>
          <div style="font-size:15px;letter-spacing:2px;color:{SUB};padding-top:14px">DOCUMENT NO. EA.032.1963</div>
        </div></div></div>'''
    add('22','EA-Archive','iphone',ph); add('22','EA-Archive','pc',pc)
d22()

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
        <div style="height:200px;display:flex;align-items:center;justify-content:center;gap:26px">
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
          <div style="height:190px;display:flex;align-items:center;justify-content:center;gap:26px">{rbtn(rew(30,'#fff'),78)}{rbtn(tri(36,'#fff'),98)}{rbtn(ffwd(30,'#fff'),78)}</div>
        </div></div></div>'''
    add('31','Vinyl-Rote-Tasten','iphone',ph); add('31','Vinyl-Rote-Tasten','pc',pc)
d31()

