# -*- coding: utf-8 -*-
"""Zusaetzliche Bausteine fuer V3 (Bandmaschine, Kassette, Gitter, Leuchtkasten)."""
from lib import *
import math

# ---------- Bandmaschinen-Spule mit 3 Sichtfenstern (SONY/AKAI-Stil) ----------
def bigreel(size, face='#f4f4f2', tape='#4a3428', hub='#2a2a28', rim='#d8d8d5', wind=0.62):
    r=size/2; c=r
    win=''
    for k in range(3):
        a0=math.radians(k*120-60); a1=math.radians(k*120+60-  60)
        # dreieckige Fenster
        pts=[]
        for t in (0.30,0.62,0.62,0.30):
            pass
        a=math.radians(k*120-90)
        x=c+math.cos(a)*r*0.50; y=c+math.sin(a)*r*0.50
        win+=f'<path d="M {x-r*0.20:.1f} {y+r*0.16:.1f} Q {x:.1f} {y-r*0.26:.1f} {x+r*0.20:.1f} {y+r*0.16:.1f} Q {x:.1f} {y+r*0.24:.1f} {x-r*0.20:.1f} {y+r*0.16:.1f} Z" fill="{tape}" transform="rotate({k*120} {c} {c})"/>'
    return f'''<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">
<defs><radialGradient id="bg{size}" cx="40%" cy="34%" r="72%"><stop offset="0%" stop-color="#ffffff"/><stop offset="70%" stop-color="{face}"/><stop offset="100%" stop-color="{rim}"/></radialGradient></defs>
<circle cx="{c}" cy="{c}" r="{r}" fill="url(#bg{size})" stroke="{rim}" stroke-width="1.5"/>
<circle cx="{c}" cy="{c}" r="{r*0.985}" fill="none" stroke="rgba(0,0,0,.10)" stroke-width="1"/>
{win}
<circle cx="{c}" cy="{c}" r="{r*0.30}" fill="{tape}" opacity="0.92"/>
<circle cx="{c}" cy="{c}" r="{r*0.30}" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="1"/>
<circle cx="{c}" cy="{c}" r="{r*0.185}" fill="{hub}"/>
{''.join(f'<circle cx="{c+math.cos(math.radians(k*120-90))*r*0.085:.1f}" cy="{c+math.sin(math.radians(k*120-90))*r*0.085:.1f}" r="{r*0.035}" fill="#0d0d0c"/>' for k in range(3))}
<circle cx="{c}" cy="{c}" r="{r*0.055}" fill="#0d0d0c"/></svg>'''

# ---------- Kassetten-Shell (Draufsicht) ----------
def cassette(w, shell='#dcd6c2', label='#f6f2e6', stripes=None, title='MIX TAPE',
             sub='', script=False, hubfill='#efefe9', windowbg='#2a1c12', text='#2b2b28',
             screws='#b9b3a1', clear=False, labelh=0.40, side='A'):
    h=w*0.63
    st=''
    if stripes:
        n=len(stripes); band=h*0.16; y0=h*0.40
        for i,c in enumerate(stripes):
            st+=f'<rect x="{w*0.045}" y="{y0+i*band/n*1.0:.1f}" width="{w*0.91}" height="{band/n+0.6:.1f}" fill="{c}"/>'
    def hubw(cx):
        return f'''<circle cx="{cx}" cy="{h*0.50}" r="{w*0.082}" fill="{hubfill}" stroke="rgba(0,0,0,.28)" stroke-width="1.5"/>
<circle cx="{cx}" cy="{h*0.50}" r="{w*0.050}" fill="#fff" stroke="rgba(0,0,0,.35)" stroke-width="1.2"/>
{''.join(f'<rect x="{cx-2.5}" y="{h*0.50-w*0.050}" width="5" height="{w*0.020}" fill="rgba(0,0,0,.4)" transform="rotate({k*60} {cx} {h*0.50})"/>' for k in range(6))}'''
    scr=''.join(f'<circle cx="{x}" cy="{y}" r="{w*0.016}" fill="{screws}" stroke="rgba(0,0,0,.3)" stroke-width="1"/>'
                for x,y in [(w*0.055,h*0.075),(w*0.945,h*0.075),(w*0.055,h*0.925),(w*0.945,h*0.925)])
    fam = "'Brush Script MT','Segoe Script',cursive" if script else SANS
    fs = w*0.085 if script else w*0.055
    body_fill='rgba(225,228,230,.55)' if clear else shell
    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs><linearGradient id="cs{int(w)}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#ffffff" stop-opacity=".35"/><stop offset="45%" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs>
<rect x="0" y="0" width="{w}" height="{h}" rx="{w*0.035}" fill="{body_fill}" stroke="rgba(0,0,0,.22)" stroke-width="1.5"/>
<rect x="0" y="0" width="{w}" height="{h}" rx="{w*0.035}" fill="url(#cs{int(w)})"/>
<rect x="{w*0.045}" y="{h*0.075}" width="{w*0.91}" height="{h*labelh}" rx="{w*0.012}" fill="{label}" stroke="rgba(0,0,0,.18)"/>
<line x1="{w*0.075}" y1="{h*(0.075+labelh*0.60)}" x2="{w*0.925}" y2="{h*(0.075+labelh*0.60)}" stroke="rgba(0,0,0,.16)"/>
<text x="{w*0.085}" y="{h*(0.075+labelh*0.48)}" font-family="{fam}" font-size="{fs:.0f}" fill="{text}" letter-spacing="{0 if script else 2}">{title}</text>
<text x="{w*0.085}" y="{h*(0.075+labelh*0.88)}" font-family="{SANS}" font-size="{w*0.030:.0f}" fill="rgba(0,0,0,.5)" letter-spacing="1.5">{sub}</text>
<text x="{w*0.925}" y="{h*(0.075+labelh*0.45)}" font-family="{SANS}" font-size="{w*0.045:.0f}" font-weight="700" fill="{text}" text-anchor="end">{side}</text>
{st}
<rect x="{w*0.055}" y="{h*0.42}" width="{w*0.89}" height="{h*0.22}" rx="{w*0.02}" fill="rgba(0,0,0,.06)"/>
<rect x="{w*0.375}" y="{h*0.455}" width="{w*0.25}" height="{h*0.15}" rx="{w*0.008}" fill="{windowbg}"/>
{''.join(f'<line x1="{w*(0.40+i*0.033)}" y1="{h*0.485}" x2="{w*(0.40+i*0.033)}" y2="{h*0.575}" stroke="rgba(255,255,255,.35)" stroke-width="1.5"/>' for i in range(6))}
{hubw(w*0.265)}{hubw(w*0.735)}
<path d="M {w*0.14} {h} L {w*0.20} {h*0.70} L {w*0.80} {h*0.70} L {w*0.86} {h} Z" fill="rgba(0,0,0,.07)"/>
{''.join(f'<rect x="{w*x}" y="{h*0.80}" width="{w*0.035}" height="{h*0.055}" rx="2" fill="rgba(0,0,0,.35)"/>' for x in [0.26,0.36,0.60,0.70])}
<circle cx="{w*0.50}" cy="{h*0.78}" r="{w*0.014}" fill="rgba(0,0,0,.4)"/>
{scr}</svg>'''

# ---------- Lautsprecher-Gitter (Punktraster) ----------
def dotgrid(w,h,color='#2f2f2d',r=3.2,gap=15,op=1.0,fade=False):
    d=''
    cols=int(w//gap); rows=int(h//gap)
    for j in range(rows):
        for i in range(cols):
            o=op
            if fade: o=op*max(0.18, 1-(i/max(cols-1,1))*0.85)
            d+=f'<circle cx="{i*gap+gap/2:.1f}" cy="{j*gap+gap/2:.1f}" r="{r}" fill="{color}" opacity="{o:.2f}"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">{d}</svg>'

# ---------- Runder Lautsprecher (Boombox) ----------
def speaker(size, ring='#c9ccce', mesh='#141414', inner='#0c0c0c'):
    r=size/2
    return f'''<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">
<defs><pattern id="mp{int(size)}" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="1.5" fill="#2e2e2e"/></pattern></defs>
<circle cx="{r}" cy="{r}" r="{r}" fill="{ring}"/>
<circle cx="{r}" cy="{r}" r="{r*0.90}" fill="{mesh}"/>
<circle cx="{r}" cy="{r}" r="{r*0.90}" fill="url(#mp{int(size)})"/>
<circle cx="{r}" cy="{r}" r="{r*0.26}" fill="{inner}"/>
<circle cx="{r}" cy="{r}" r="{r*0.26}" fill="none" stroke="rgba(255,255,255,.10)" stroke-width="2"/></svg>'''

# ---------- Orange VU (We Are Rewind) ----------
def vu_amber(w,h,frac=0.30,face='#f5a623',ink='#2a1a06'):
    cx=w/2; cy=h*1.06; r=h*0.88
    a0=math.radians(203); a1=math.radians(337)
    ticks=''
    labs=['60','50','40','30','20','10','3','0','+']
    for i in range(9):
        a=a0+(a1-a0)*i/8
        r1=r*0.80; r2=r*0.90
        ticks+=f'<line x1="{cx+math.cos(a)*r1:.1f}" y1="{cy+math.sin(a)*r1:.1f}" x2="{cx+math.cos(a)*r2:.1f}" y2="{cy+math.sin(a)*r2:.1f}" stroke="{ink}" stroke-width="1.8"/>'
        lx=cx+math.cos(a)*r*0.70; ly=cy+math.sin(a)*r*0.70
        ticks+=f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="{SANS}" font-size="{h*0.10:.0f}" fill="{ink}" text-anchor="middle">{labs[i]}</text>'
    an=a0+(a1-a0)*frac
    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<rect x="0" y="0" width="{w}" height="{h}" rx="6" fill="{face}" stroke="#c07f14" stroke-width="3"/>
<rect x="4" y="4" width="{w-8}" height="{h-8}" rx="4" fill="none" stroke="rgba(255,255,255,.45)" stroke-width="2"/>
{ticks}
<text x="{cx}" y="{h*0.72}" font-family="{SANS}" font-size="{h*0.15:.0f}" fill="{ink}" text-anchor="middle" letter-spacing="2">VU</text>
<text x="{w*0.90}" y="{h*0.55}" font-family="{SANS}" font-size="{h*0.085:.0f}" fill="{ink}" text-anchor="end">dB</text>
<text x="{w*0.88}" y="{h*0.76}" font-family="{SANS}" font-size="{h*0.075:.0f}" fill="{ink}" text-anchor="end">POWER</text>
<line x1="{cx}" y1="{cy}" x2="{cx+math.cos(an)*r*0.86:.1f}" y2="{cy+math.sin(an)*r*0.86:.1f}" stroke="{ink}" stroke-width="2.2"/></svg>'''

# ---------- Skalen-Leiste (Radio-Tuning) ----------
def tunescale(w,h,marks,color='#e8e4d8',accent='#c9422e',pos=0.46,sub=None):
    t=''
    n=len(marks)
    for i,m in enumerate(marks):
        x=w*0.06+ (w*0.88)*i/(n-1)
        t+=f'<line x1="{x:.1f}" y1="{h*0.42}" x2="{x:.1f}" y2="{h*0.56}" stroke="{color}" stroke-width="1.6"/>'
        t+=f'<text x="{x:.1f}" y="{h*0.34}" font-family="{SANS}" font-size="{h*0.26:.0f}" fill="{color}" text-anchor="middle">{m}</text>'
        if i<n-1:
            for k in range(1,4):
                xm=x+(w*0.88)/(n-1)*k/4
                t+=f'<line x1="{xm:.1f}" y1="{h*0.46}" x2="{xm:.1f}" y2="{h*0.56}" stroke="{color}" stroke-width="1" opacity=".55"/>'
    px=w*0.06+(w*0.88)*pos
    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">
{t}
<rect x="{w*0.05}" y="{h*0.68}" width="{w*0.90}" height="{h*0.14}" rx="{h*0.07}" fill="rgba(255,255,255,.85)"/>
<rect x="{px-3:.1f}" y="{h*0.60}" width="6" height="{h*0.30}" rx="3" fill="{accent}"/></svg>'''

# ---------- Riffel-Knopf (Alu) ----------
def knurl(size, accent=None, dark=False):
    base = 'repeating-conic-gradient(#3a3a38 0deg 3deg,#565654 3deg 6deg)' if dark else 'repeating-conic-gradient(#c9c9c6 0deg 3deg,#f2f2ef 3deg 6deg)'
    face = 'radial-gradient(circle at 38% 32%,#6a6a68,#2e2e2c)' if dark else 'radial-gradient(circle at 38% 32%,#ffffff,#dcdcd8 60%,#b9b9b5)'
    mark=f'<div style="position:absolute;left:50%;top:{size*0.10:.0f}px;width:4px;height:{size*0.20:.0f}px;background:{accent};transform:translateX(-50%);border-radius:2px"></div>' if accent else ''
    return f'''<div style="position:relative;width:{size}px;height:{size}px;border-radius:50%;background:{base};box-shadow:0 {size*0.05:.0f}px {size*0.14:.0f}px rgba(0,0,0,.42)">
<div style="position:absolute;inset:{size*0.13:.0f}px;border-radius:50%;background:{face};box-shadow:inset 0 2px 3px rgba(255,255,255,.6)"></div>{mark}</div>'''

# ---------- Ikonen ----------
def eject(size,color):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24"><path d="M12 4 L20 13 H4 Z" fill="{color}"/><rect x="4" y="16" width="16" height="3" rx="1" fill="{color}"/></svg>'
def libicon(size,color):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none">
<rect x="3" y="4" width="3" height="16" rx="1" fill="{color}"/><rect x="8" y="4" width="3" height="16" rx="1" fill="{color}"/>
<path d="M14.5 5.4 L18.2 4.5 L21.5 19 L17.8 19.9 Z" fill="{color}"/></svg>'''
def listicon(size,color):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
{''.join(f'<circle cx="4" cy="{6+i*6}" r="1.6" fill="{color}"/><rect x="8" y="{4.8+i*6}" width="12" height="2.4" rx="1.2" fill="{color}"/>' for i in range(3))}</svg>'''
def rew(size,color):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24"><path d="M11 12 L20 6 v12 Z M2 12 L11 6 v12 Z" fill="{color}"/></svg>'
def ffwd(size,color):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24"><path d="M13 12 L4 6 v12 Z M22 12 L13 6 v12 Z" fill="{color}"/></svg>'
def shuffle(size,color):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round">
<path d="M3 6h4l4 12h6M3 18h4l2-6"/><path d="M17 3l4 3-4 3M17 15l4 3-4 3"/></svg>'''
def repeat(size,color):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round">
<path d="M4 9a5 5 0 0 1 5-5h9"/><path d="M15 1l3 3-3 3"/><path d="M20 15a5 5 0 0 1-5 5H6"/><path d="M9 23l-3-3 3-3"/></svg>'''
def qr(size,dark='#111'):
    import hashlib
    cells=[]
    seed='qr'
    for y in range(9):
        for x in range(9):
            hv=int(hashlib.md5(f'{x}{y}{seed}'.encode()).hexdigest(),16)
            if (x<3 and y<3) or (x>5 and y<3) or (x<3 and y>5): continue
            if hv%2: cells.append(f'<rect x="{x*(size/9):.1f}" y="{y*(size/9):.1f}" width="{size/9:.1f}" height="{size/9:.1f}" fill="{dark}"/>')
    def finder(ox,oy):
        u=size/9
        return (f'<rect x="{ox}" y="{oy}" width="{u*3:.1f}" height="{u*3:.1f}" fill="{dark}"/>'
                f'<rect x="{ox+u*0.55:.1f}" y="{oy+u*0.55:.1f}" width="{u*1.9:.1f}" height="{u*1.9:.1f}" fill="#fff"/>'
                f'<rect x="{ox+u*1.05:.1f}" y="{oy+u*1.05:.1f}" width="{u*0.9:.1f}" height="{u*0.9:.1f}" fill="{dark}"/>')
    u=size/9
    return f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">{"".join(cells)}{finder(0,0)}{finder(u*6,0)}{finder(0,u*6)}</svg>'
