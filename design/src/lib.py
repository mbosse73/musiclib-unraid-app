# -*- coding: utf-8 -*-
"""Shared building blocks for music-player mockups."""

SANS="'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO="ui-monospace,'SFMono-Regular',Menlo,'Courier New',monospace"
SERIF="Georgia,'Times New Roman',ui-serif,serif"
COND="'Arial Narrow','Helvetica Neue Condensed',Arial,sans-serif"
IMPACT="Impact,Haettenschweiler,'Arial Narrow Bold',sans-serif"

def doc(w,h,css,body):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{w}px;height:{h}px;overflow:hidden}}
.stage{{position:relative;width:{w}px;height:{h}px;overflow:hidden}}
{css}
</style></head><body><div class="stage">{body}</div></body></html>'''

# ---- SVG motifs -------------------------------------------------------------
def vinyl(size, label, grooves='#111', base='#0a0a0a', shine=True):
    r=size/2
    sh=f'<radialGradient id="vs" cx="38%" cy="32%" r="75%"><stop offset="0%" stop-color="#4a4a4a"/><stop offset="18%" stop-color="#111"/><stop offset="100%" stop-color="{base}"/></radialGradient>' if shine else ''
    rings=''.join(f'<circle cx="{r}" cy="{r}" r="{r*0.30+ i*(r*0.66/22)}" fill="none" stroke="{grooves}" stroke-width="0.7" opacity="0.55"/>' for i in range(22))
    return f'''<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">
<defs>{sh}</defs>
<circle cx="{r}" cy="{r}" r="{r}" fill="{'url(#vs)' if shine else base}"/>
{rings}
<circle cx="{r}" cy="{r}" r="{r*0.28}" fill="{label}"/>
<circle cx="{r}" cy="{r}" r="{r*0.028}" fill="#0a0a0a"/></svg>'''

def reel(size, stroke, spokes='belt', fill='none', sw=2.2):
    r=size/2; c=r
    outer=f'<circle cx="{c}" cy="{c}" r="{r-sw}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    hub=f'<circle cx="{c}" cy="{c}" r="{r*0.14}" fill="none" stroke="{stroke}" stroke-width="{sw}"/>'
    teeth=''
    import math
    if spokes=='conc':
        rings=''.join(f'<circle cx="{c}" cy="{c}" r="{r*0.16+i*(r*0.8/16)}" fill="none" stroke="{stroke}" stroke-width="0.8" opacity="0.5"/>' for i in range(16))
        return f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">{outer}{rings}{hub}</svg>'
    for k in range(3):
        a=math.radians(k*120-90)
        x1=c+math.cos(a)*r*0.2; y1=c+math.sin(a)*r*0.2
        x2=c+math.cos(a)*r*0.72; y2=c+math.sin(a)*r*0.72
        teeth+=f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"/>'
    return f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">{outer}{teeth}{hub}<circle cx="{c}" cy="{c}" r="{r*0.045}" fill="{stroke}"/></svg>'

def waveform(w,h,color,n=60,seed=7,op=1.0,radius=2):
    import math
    bars=''
    for i in range(n):
        v=(math.sin(i*0.5+seed)*0.5+0.5)*(0.35+0.65*abs(math.sin(i*0.27+seed*1.3)))
        bh=max(3,v*h)
        x=i*(w/n); bw=(w/n)*0.55
        y=(h-bh)/2
        bars+=f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="{radius}" fill="{color}" opacity="{op}"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">{bars}</svg>'

def vumeter(w,h,face,needle,tick,label='',frac=0.62):
    import math
    cx=w/2; cy=h*0.98; r=h*0.86
    a0=math.radians(210); a1=math.radians(330)
    ticks=''
    for i in range(11):
        a=a0+(a1-a0)*i/10
        r2=r; r1=r*(0.86 if i%5 else 0.78)
        col=tick if i<7 else '#c9402e'
        ticks+=f'<line x1="{cx+math.cos(a)*r1:.1f}" y1="{cy+math.sin(a)*r1:.1f}" x2="{cx+math.cos(a)*r2:.1f}" y2="{cy+math.sin(a)*r2:.1f}" stroke="{col}" stroke-width="{2.4 if i%5 else 1.4}"/>'
    an=a0+(a1-a0)*frac
    nx=cx+math.cos(an)*r*0.92; ny=cy+math.sin(an)*r*0.92
    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<rect x="0" y="0" width="{w}" height="{h}" rx="10" fill="{face}"/>
{ticks}
<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{needle}" stroke-width="2.6"/>
<circle cx="{cx}" cy="{cy}" r="5" fill="{needle}"/>
<text x="{cx}" y="{h*0.5}" fill="{tick}" font-family="{SANS}" font-size="{h*0.13:.0f}" text-anchor="middle" opacity="0.7">{label}</text>
<text x="{w*0.16}" y="{h*0.34}" fill="{tick}" font-family="{SANS}" font-size="{h*0.1:.0f}" opacity="0.6">-</text>
<text x="{w*0.84}" y="{h*0.34}" fill="#c9402e" font-family="{SANS}" font-size="{h*0.1:.0f}" text-anchor="end">+</text></svg>'''

def tri(size,color):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="{color}"/></svg>'
def pausei(size,color):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24"><rect x="6" y="5" width="4" height="14" fill="{color}"/><rect x="14" y="5" width="4" height="14" fill="{color}"/></svg>'
def prev(size,color):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24"><path d="M7 5v14M20 5v14l-11-7z" stroke="{color}" stroke-width="2" fill="{color}" stroke-linejoin="round"/></svg>'
def nexti(size,color):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24"><path d="M17 5v14M4 5v14l11-7z" stroke="{color}" stroke-width="2" fill="{color}" stroke-linejoin="round"/></svg>'
def heart(size,color):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24"><path d="M12 21C5 15 3 11 3 8a5 5 0 0 1 9-3 5 5 0 0 1 9 3c0 3-2 7-9 13z" fill="{color}"/></svg>'
