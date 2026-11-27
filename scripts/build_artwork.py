from pathlib import Path
import math
root = Path(__file__).resolve().parents[1]
(root/'assets').mkdir(exist_ok=True)

# Shared ornate SVG vocabulary: midnight enamel, antique gold, amethyst, glacial blue.
def svg(w,h,body,defs=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{defs}</defs>{body}</svg>'''

# Atmospheric panoramic banner, drawn as vector architecture rather than a flat gradient.
banner_defs='''<linearGradient id="sky" x2="0" y2="1"><stop stop-color="#101629"/><stop offset=".58" stop-color="#26334f"/><stop offset="1" stop-color="#080b17"/></linearGradient><linearGradient id="glass"><stop stop-color="#8f72c8"/><stop offset=".5" stop-color="#b6d8ef"/><stop offset="1" stop-color="#34284e"/></linearGradient><linearGradient id="beam"><stop stop-color="#e9e5ff" stop-opacity=".0"/><stop offset=".5" stop-color="#dce8ff" stop-opacity=".2"/><stop offset="1" stop-color="#e9e5ff" stop-opacity="0"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'''
body=['<rect width="1600" height="440" fill="url(#sky)"/>']
# moon + shafts
body += ['<circle cx="280" cy="82" r="42" fill="#e8e5ff" opacity=".9" filter="url(#glow)"/>']
for x in [280,320,370,430]: body.append(f'<path d="M{x} 95 L{x+250} 440 L{x+90} 440 Z" fill="url(#beam)"/>')
# distant skyline
for i in range(38):
    x=i*44-15; ht=90+(i*71%160); y=350-ht
    body.append(f'<path d="M{x} 350 V{y+24} l18 -24 l18 24 V350Z" fill="#171e31" stroke="#52617c" stroke-width="2"/>')
    body.append(f'<rect x="{x+12}" y="{y+42}" width="12" height="25" fill="url(#glass)" opacity=".8"/>')
# grand central towers
for x,base,ht in [(600,365,260),(790,370,330),(1010,365,285),(1250,365,235)]:
    body.append(f'<path d="M{x} {base} V{base-ht+55} l34 -55 l34 55 V{base}Z" fill="#101827" stroke="#7e7796" stroke-width="3"/>')
    body.append(f'<path d="M{x+24} {base-ht+70} V{base-35} M{x+45} {base-ht+70} V{base-35}" stroke="url(#glass)" stroke-width="12" opacity=".9"/>')
    body.append(f'<path d="M{x-12} {base-ht+56} H{x+80}" stroke="#a28bbd" stroke-width="4"/>')
# bridges
for y in [255,315]:
    body.append(f'<path d="M0 {y} Q800 {y-80} 1600 {y}" fill="none" stroke="#090e1a" stroke-width="18"/><path d="M0 {y-7} Q800 {y-87} 1600 {y-7}" fill="none" stroke="#8b829d" stroke-width="3"/>')
# bridge arches
for x in [240,650,1080,1430]:
    body.append(f'<path d="M{x-110} 365 Q{x} 180 {x+110} 365" fill="none" stroke="#0b101c" stroke-width="14"/><path d="M{x-110} 365 Q{x} 180 {x+110} 365" fill="none" stroke="#77758d" stroke-width="3"/>')
# foreground rooftops and windows
body += ['<path d="M0 350 L170 260 L330 350 L470 315 L620 440 H0Z" fill="#090d18" stroke="#51465d" stroke-width="4"/>','<path d="M1120 440 L1300 310 L1450 360 L1600 270 V440Z" fill="#090d18" stroke="#51465d" stroke-width="4"/>']
for x in range(40,1550,85):
    body.append(f'<rect x="{x}" y="375" width="18" height="34" rx="2" fill="#9fc9e8" opacity=".7"/>')
# airships
for x,y,s in [(500,130,1),(1170,115,.8),(1370,205,.55)]:
    body.append(f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="55" ry="15" fill="#0b1220" stroke="#a9a4bb" stroke-width="2"/><path d="M-25 0 Q0 -22 28 0 Q0 19 -25 0" fill="#54466f"/><path d="M-4 13 V25 M8 13 V25" stroke="#b6a5c9" stroke-width="2"/></g>')
# waterfall streaks
for x in [710,730,750,1120,1145]: body.append(f'<path d="M{x} 365 Q{x-8} 395 {x+4} 440" stroke="#a9d4f0" stroke-width="5" opacity=".48"/>')
# subtle stars
for i in range(70):
    x=(i*193+41)%1600; y=(i*67+19)%240
    body.append(f'<circle cx="{x}" cy="{y}" r="{1+(i%3)*.5}" fill="#e8e4ff" opacity=".7"/>')
body.append('<rect x="2" y="2" width="1596" height="436" rx="18" fill="none" stroke="#b59bce" stroke-width="3" opacity=".65"/>')
(root/'assets/arcane-banner.svg').write_text(svg(1600,440,''.join(body),banner_defs))

# Nameplate and decorative dividers
(root/'assets/nameplate.svg').write_text(svg(1200,150,'''<rect x="3" y="3" width="1194" height="144" rx="12" fill="#0d1220" stroke="#a98cc7" stroke-width="3"/><path d="M28 75 H220 M980 75 H1172" stroke="#b89bce" stroke-width="2"/><path d="M220 75 l24 -16 v32z M980 75 l-24 -16 v32z" fill="#b89bce"/><text x="600" y="78" fill="#f1eaff" text-anchor="middle" font-family="Georgia,serif" font-size="54" letter-spacing="12">SHADE555</text><text x="600" y="117" fill="#a9c6df" text-anchor="middle" font-family="Georgia,serif" font-size="16" letter-spacing="5">KEEPER OF THE ARCANE SYSTEMS ARCHIVE</text>'''))
(root/'assets/divider.svg').write_text(svg(1200,46,'''<path d="M0 23 H510 M690 23 H1200" stroke="#625879" stroke-width="2"/><path d="M600 4 L619 23 L600 42 L581 23Z" fill="#171b2b" stroke="#b69bce" stroke-width="2"/><circle cx="600" cy="23" r="5" fill="#d9c8ef"/><path d="M530 23 l12 -8 l12 8 l-12 8z M646 23 l12 -8 l12 8 l-12 8z" fill="#8d7ca8"/>'''))
(root/'assets/closing-gate.svg').write_text(svg(1200,210,'''<rect x="2" y="2" width="1196" height="206" rx="14" fill="#0b101c" stroke="#8f79aa" stroke-width="3"/><path d="M430 185 V85 Q600 -65 770 85 V185 M470 185 V95 Q600 -18 730 95 V185" fill="none" stroke="#9b8ab2" stroke-width="5"/><path d="M510 185 V110 Q600 25 690 110 V185" fill="#1b2034" stroke="#b6a0d0" stroke-width="3"/><path d="M550 185 V125 Q600 80 650 125 V185" fill="#4b3d68" stroke="#c5aee0" stroke-width="2"/><circle cx="600" cy="91" r="13" fill="#d8c5f0"/><path d="M600 30 V5 M580 48 l-18 -20 M620 48 l18 -20" stroke="#c5aee0" stroke-width="2"/><text x="600" y="197" fill="#d7c7e9" text-anchor="middle" font-family="Georgia,serif" font-size="15" letter-spacing="5">THE ARCHIVE REMAINS OPEN</text>'''))

# Sigils
sigils={
'curiosity':'<path d="M5 18 Q18 -2 31 18 Q18 38 5 18Z"/><circle cx="18" cy="18" r="5"/>',
'engineering':'<path d="M18 2 L32 10 V26 L18 34 L4 26 V10Z"/><path d="M18 8 V28 M8 18 H28"/>',
'insight':'<circle cx="18" cy="18" r="13"/><path d="M18 5 V31 M5 18 H31 M9 9 L27 27 M27 9 L9 27"/>',
'iteration':'<path d="M7 12 A12 12 0 0 1 28 9 L31 13 M31 13 V5 M31 13 H23 M29 24 A12 12 0 0 1 8 27 L5 23 M5 23 V31 M5 23 H13"/>'}
for name,shape in sigils.items():
    (root/f'assets/sigils/{name}.svg').parent.mkdir(parents=True,exist_ok=True)
    (root/f'assets/sigils/{name}.svg').write_text(svg(36,36,f'<g fill="none" stroke="#c6a9df" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{shape}</g>'))

# Nine unique stained-glass panels, with lead came geometry and restrained SMIL shimmer.
projects=[
('digipico','DigiPico','#70b7d2','#c4a4e8','companion'),('frameon','Frameon','#8ec8d7','#c5a2dc','gallery'),
('proofpocket','ProofPocket','#d4b978','#a9c8dc','document'),('patchwork','Patchwork AI','#d68caa','#9fb8dc','patch'),
('interbrew','InterBrew','#d6a36f','#b5a0df','cup'),('signalwatch','Mumbai Signal Watch','#86b6d2','#a88fce','signal'),
('bluetooth-trackpad','Bluetooth Trackpad','#75c8df','#b5a0df','bluetooth'),('startup-intelligence','Startup Intelligence','#d2ad72','#8caed8','intelligence'),('experiments','More Experiments','#b29bda','#85b8d0','stars')]
for slug,title,c1,c2,motif in projects:
    defs=f'''<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{c1}" stop-opacity=".62"/><stop offset="1" stop-color="{c2}" stop-opacity=".25"/></linearGradient><linearGradient id="shine"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><filter id="soft"><feGaussianBlur stdDeviation="4"/></filter>'''
    b=[ '<rect width="720" height="260" rx="18" fill="#0c1220"/>', '<path d="M18 242 V85 L360 15 L702 85 V242Z" fill="url(#glass)" stroke="#b8a2c9" stroke-width="5"/>', '<path d="M30 235 V91 L360 27 L690 91 V235Z" fill="none" stroke="#3c4055" stroke-width="7"/>', '<path d="M360 20 V240 M25 145 H695 M110 70 L250 240 M610 70 L470 240 M250 42 L110 235 M470 42 L610 235" stroke="#171b2b" stroke-width="9"/>', '<path d="M360 20 V240 M25 145 H695 M110 70 L250 240 M610 70 L470 240" stroke="#b69ecb" stroke-width="2" opacity=".8"/>']
    # central sigil variants
    if motif=='companion': icon='<circle cx="360" cy="120" r="62"/><path d="M330 126 Q360 65 390 126 Q360 160 330 126Z"/><circle cx="360" cy="115" r="12"/>'
    elif motif=='gallery': icon='<path d="M315 65 H405 V170 H315Z M330 80 H390 V155 H330Z"/><circle cx="360" cy="112" r="18"/><path d="M340 170 L360 145 L380 170"/>'
    elif motif=='document': icon='<path d="M330 58 H380 L405 83 V180 H315 V58Z M380 58 V84 H405 M337 105 H383 M337 124 H383 M337 143 H370"/>'
    elif motif=='patch': icon='<path d="M315 82 L345 52 L375 82 L405 52 L435 82 L405 112 L435 142 L405 172 L375 142 L345 172 L315 142 L345 112Z"/><path d="M345 112 H405 M375 82 V142"/>'
    elif motif=='cup': icon='<path d="M325 75 H395 L385 160 H335Z M395 90 Q440 88 415 130 H390 M340 175 H390"/><path d="M350 62 Q340 42 355 32 M375 62 Q365 42 380 32"/>'
    elif motif=='signal': icon='<circle cx="360" cy="115" r="58"/><path d="M360 55 V175 M300 115 H420 M318 73 L402 157 M402 73 L318 157"/><circle cx="360" cy="115" r="18"/>'
    elif motif=='bluetooth': icon='<path d="M360 42 V188 L414 145 L306 85 L414 42 L360 86"/><path d="M360 115 L306 175 M360 115 L414 175"/><circle cx="360" cy="115" r="74" stroke-dasharray="8 10"/><path d="M285 205 H435" stroke-width="5"/>'
    elif motif=='intelligence': icon='<path d="M360 45 L425 82 V148 L360 185 L295 148 V82Z"/><circle cx="360" cy="115" r="28"/><path d="M360 66 V87 M360 143 V164 M311 115 H332 M388 115 H409 M326 81 L341 96 M379 134 L394 149 M394 81 L379 96 M341 134 L326 149"/><circle cx="360" cy="115" r="62" stroke-dasharray="4 8"/>'
    elif motif=='orbit': icon='<circle cx="360" cy="115" r="20"/><ellipse cx="360" cy="115" rx="76" ry="30" transform="rotate(-28 360 115)"/><ellipse cx="360" cy="115" rx="76" ry="30" transform="rotate(55 360 115)"/><circle cx="418" cy="82" r="7"/>'
    else: icon='<path d="M360 48 L375 100 L430 115 L375 130 L360 182 L345 130 L290 115 L345 100Z"/><circle cx="360" cy="115" r="20"/>'
    b += [f'<g fill="none" stroke="#e1d5ed" stroke-width="3" stroke-linejoin="round" filter="url(#soft)" opacity=".28">{icon}</g>',f'<g fill="none" stroke="#e4d8ef" stroke-width="3" stroke-linejoin="round">{icon}</g>', '<path d="M18 18 H702 V242 H18Z" fill="none" stroke="#d5c4e4" stroke-width="2"/>', '<path d="M30 30 L690 30" stroke="#fff" stroke-opacity=".25"/>', '<rect x="-80" y="0" width="55" height="260" fill="url(#shine)" opacity=".22"><animate attributeName="x" values="-80;760" dur="8s" repeatCount="indefinite"/></rect>', f'<text x="360" y="218" fill="#f3eafa" text-anchor="middle" font-family="Georgia,serif" font-size="24" letter-spacing="5">{title.upper()}</text>', '<text x="360" y="239" fill="#c5b7d5" text-anchor="middle" font-family="monospace" font-size="10" letter-spacing="3">ARCHIVE WINDOW · OPEN</text>']
    (root/f'assets/projects/{slug}.svg').write_text(svg(720,260,''.join(b),defs))

# Technology section plaques
for file,label,sub in [('languages','LANGUAGE CONSTELLATION','THE GRAMMAR OF MACHINES'),('intelligence','INTELLIGENCE & DATA','PATTERNS · MODELS · SIGNALS'),('engineering','APPLICATION ENGINEERING','WEB · MOBILE · BACKEND'),('infrastructure','THE INFRASTRUCTURE WING','DATA STORES · TOOLING · SYSTEMS')]:
    (root/f'assets/tech/{file}.svg').parent.mkdir(parents=True,exist_ok=True)
    (root/f'assets/tech/{file}.svg').write_text(svg(1200,64,f'<path d="M0 32 H240 M960 32 H1200" stroke="#665a7b" stroke-width="2"/><path d="M250 32 l12 -12 l12 12 l-12 12z M950 32 l-12 -12 l-12 12 l12 12z" fill="#a98cc7"/><text x="600" y="28" text-anchor="middle" fill="#e5d8f1" font-family="Georgia,serif" font-size="20" letter-spacing="5">{label.replace('&', '&amp;')}</text><text x="600" y="49" text-anchor="middle" fill="#9daac2" font-family="monospace" font-size="9" letter-spacing="3">{sub}</text>'))

# Initial stats instruments: honest, explicitly waiting for workflow data.
def stat_panel(title,subtitle,extra=''):
    return svg(1200,220,f'''<rect x="2" y="2" width="1196" height="216" rx="16" fill="#0c1220" stroke="#88739f" stroke-width="3"/><path d="M25 45 H1175 M25 190 H1175" stroke="#514963" stroke-width="1"/><text x="42" y="34" fill="#d7c5e8" font-family="Georgia,serif" font-size="20" letter-spacing="4">{title}</text><text x="600" y="105" fill="#e7ddf0" text-anchor="middle" font-family="Georgia,serif" font-size="30">AWAITING FIRST OBSERVATION</text><text x="600" y="140" fill="#9eabc0" text-anchor="middle" font-family="monospace" font-size="15">{subtitle}</text><text x="600" y="174" fill="#8c7c9f" text-anchor="middle" font-family="monospace" font-size="11">{extra or 'The scheduled archive workflow will populate this instrument.'}</text>''')
(root/'assets/stats/github-ledger.svg').write_text(stat_panel('THE GITHUB LEDGER','PROFILE METRICS · REPOSITORIES · FOLLOWERS'))
(root/'assets/stats/contribution-constellation.svg').write_text(stat_panel('THE CONTRIBUTION CONSTELLATION','A YEAR OF PUBLIC CONTRIBUTION ACTIVITY'))
(root/'assets/stats/language-astrolabe.svg').write_text(stat_panel('THE LANGUAGE ASTROLABE','TOP LANGUAGES BY REPOSITORY BYTE COUNT'))
(root/'assets/stats/leetcode-seal.svg').write_text(stat_panel('THE LEETCODE TRIAL SEAL','SOLVED CHALLENGES · DIFFICULTY · CONTEST RANK','LeetCode public profile endpoint has not been queried yet.'))
print('Artwork generated')

from animate_svgs import animate_all
print(f'Applied motion to {animate_all()} SVG assets.')
