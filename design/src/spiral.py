# -*- coding: utf-8 -*-
"""Vinyl mit spiralfoermig gesetztem Text (hier: Albumtitel statt Songtext)."""
import math

ALBEN = ("KIND OF BLUE · RUMOURS · THRILLER · NEVERMIND · OK COMPUTER · ABBEY ROAD · "
         "BACK TO BLACK · THE WALL · PURPLE RAIN · BLUE · REMAIN IN LIGHT · UNKNOWN PLEASURES · "
         "PET SOUNDS · HOUNDS OF LOVE · THE VELVET UNDERGROUND · SGT. PEPPER · LONDON CALLING · "
         "GRACELAND · TRANS EUROPA EXPRESS · SELECTED AMBIENT WORKS · IN RAINBOWS · HORSES · "
         "THE DARK SIDE OF THE MOON · BLUE TRAIN · SONGS OF LEONARD COHEN · TAPESTRY · "
         "LED ZEPPELIN IV · MUSIC FOR AIRPORTS · TIME OUT · A LOVE SUPREME · GREEN · ")

def spiral_vinyl(size, label='#e0453a', turns=7.0, fs=None, text=None,
                 ink='#f2f2f0', base='#101010', arm=True):
    """Schallplatte, deren Rillenbereich mit umlaufendem Text gefuellt ist."""
    r = size / 2
    fs = fs or size * 0.0175
    text = (text or ALBEN)
    r_out = r * 0.955
    r_in = r * 0.325
    pts = []
    steps = int(turns * 90)
    for i in range(steps + 1):
        t = i / steps
        ang = t * turns * 2 * math.pi - math.pi / 2
        rad = r_out - (r_out - r_in) * t
        pts.append(f'{r + math.cos(ang) * rad:.1f},{r + math.sin(ang) * rad:.1f}')
    path = 'M ' + ' L '.join(pts)
    reps = max(1, int((turns * 2 * math.pi * (r_out + r_in) / 2) / (fs * 0.56 * 28)) + 2)
    body = (text * reps)[:int(turns * 2 * math.pi * (r_out + r_in) / 2 / (fs * 0.52))]
    rings = ''.join(
        f'<circle cx="{r}" cy="{r}" r="{r_in + (r_out - r_in) * k / 9:.1f}" fill="none" '
        f'stroke="rgba(255,255,255,.045)" stroke-width="1"/>' for k in range(10))
    armsvg = ''
    if arm:
        x0, y0 = r * 1.74, r * 0.16
        armsvg = (f'<g opacity=".95">'
                  f'<circle cx="{x0:.0f}" cy="{y0:.0f}" r="{size*0.052:.0f}" fill="#d8d8d6" stroke="#a8a8a4" stroke-width="2"/>'
                  f'<circle cx="{x0:.0f}" cy="{y0:.0f}" r="{size*0.018:.0f}" fill="#8e8e8a"/>'
                  f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{r*1.06:.0f}" y2="{r*1.10:.0f}" '
                  f'stroke="#c6c6c2" stroke-width="{size*0.016:.0f}" stroke-linecap="round"/>'
                  f'<rect x="{r*0.99:.0f}" y="{r*1.05:.0f}" width="{size*0.052:.0f}" height="{size*0.030:.0f}" '
                  f'rx="3" fill="#b4b4b0" transform="rotate(42 {r*1.02:.0f} {r*1.08:.0f})"/></g>')
    return f'''<svg viewBox="0 0 {size*1.06:.0f} {size} " width="{size*1.06:.0f}" height="{size}">
<defs><path id="sp{int(size)}" d="{path}"/>
<radialGradient id="vg{int(size)}" cx="38%" cy="30%" r="78%">
<stop offset="0%" stop-color="#3c3c3c"/><stop offset="22%" stop-color="#161616"/><stop offset="100%" stop-color="{base}"/></radialGradient></defs>
<circle cx="{r}" cy="{r}" r="{r}" fill="url(#vg{int(size)})"/>
{rings}
<text font-family="'Helvetica Neue',Helvetica,Arial,sans-serif" font-size="{fs:.1f}" fill="{ink}" letter-spacing="0.5" opacity=".92">
<textPath href="#sp{int(size)}" startOffset="0">{body}</textPath></text>
<circle cx="{r}" cy="{r}" r="{r*0.295}" fill="{label}"/>
<circle cx="{r}" cy="{r}" r="{r*0.215}" fill="none" stroke="rgba(0,0,0,.18)" stroke-width="1.5"/>
<circle cx="{r}" cy="{r}" r="{r*0.028}" fill="#f4f4f2"/>
{armsvg}</svg>'''
