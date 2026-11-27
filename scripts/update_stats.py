#!/usr/bin/env python3
"""Refresh the Arcane Systems Archive's SVG observatory.

GitHub data is fetched from the authenticated GraphQL API. LeetCode is queried
through its public GraphQL endpoint; if it is unavailable, the panel explicitly
reports that rather than displaying invented or stale numbers.
"""
import json, os, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'stats'
USER = os.getenv('GITHUB_USER', 'Shade555')
TOKEN = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')


def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def write_svg(name, title, body, height=250):
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}"><defs><linearGradient id="panel" x2="1" y2="1"><stop stop-color="#111a2b"/><stop offset="1" stop-color="#171329"/></linearGradient><linearGradient id="gold"><stop stop-color="#8c789e"/><stop offset=".5" stop-color="#d6c0e5"/><stop offset="1" stop-color="#8c789e"/></linearGradient></defs><rect x="2" y="2" width="1196" height="{height-4}" rx="16" fill="url(#panel)" stroke="#9a83b0" stroke-width="3"/><path d="M28 50 H1172 M28 {height-25} H1172" stroke="#514963"/><text x="40" y="34" fill="#d9c8e8" font-family="Georgia,serif" font-size="20" letter-spacing="4">{esc(title)}</text>{body}</svg>'''
    (OUT/name).write_text(content, encoding='utf-8')

def text(x,y,value,size=22,color='#eee5f7',anchor='middle',family='Georgia,serif'):
    return f'<text x="{x}" y="{y}" fill="{color}" text-anchor="{anchor}" font-family="{family}" font-size="{size}">{esc(value)}</text>'

def request_json(url, payload, headers=None, timeout=25):
    data=json.dumps(payload).encode()
    req=urllib.request.Request(url,data=data,headers={'Content-Type':'application/json','User-Agent':'ArcaneSystemsArchive/3',**(headers or {})})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return json.loads(r.read().decode())

def unavailable(title, detail):
    write_svg('leetcode-seal.svg', title, text(600,115,'THE SEAL COULD NOT BE READ',28)+text(600,155,detail,15,'#aeb7ca',family='monospace'),190)

def github():
    if not TOKEN:
        raise RuntimeError('GH_TOKEN is missing')
    query='''query($login:String!){user(login:$login){name login followers{totalCount} repositories(ownerAffiliations:OWNER,first:100,privacy:PUBLIC,orderBy:{field:UPDATED_AT,direction:DESC}){totalCount nodes{stargazerCount languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}} contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}}}}}'''
    data=request_json('https://api.github.com/graphql',{'query':query,'variables':{'login':USER}},{'Authorization':f'Bearer {TOKEN}'})
    if data.get('errors'): raise RuntimeError(data['errors'][0].get('message','GitHub GraphQL error'))
    u=data['data']['user']
    repos=u['repositories']['nodes']; stars=sum(r['stargazerCount'] for r in repos)
    weeks=u['contributionsCollection']['contributionCalendar']['weeks']
    days=[d for w in weeks for d in w['contributionDays']]
    langs={}
    for repo in repos:
        for edge in repo['languages']['edges']:
            langs[edge['node']['name']]=langs.get(edge['node']['name'],0)+edge['size']
    total=u['contributionsCollection']['contributionCalendar']['totalContributions']
    vals=[('CONTRIBUTIONS',total),('PUBLIC REPOSITORIES',u['repositories']['totalCount']),('STARS EARNED',stars),('FOLLOWERS',u['followers']['totalCount'])]
    cells=''
    for i,(label,val) in enumerate(vals):
        x=165+i*290
        cells += f'<rect x="{x-112}" y="75" width="224" height="88" rx="12" fill="#1b2034" stroke="#7e6a94"/><text x="{x}" y="115" fill="#f0e6fa" text-anchor="middle" font-family="Georgia,serif" font-size="34">{val:,}</text><text x="{x}" y="143" fill="#b8a8ca" text-anchor="middle" font-family="monospace" font-size="12" letter-spacing="2">{label}</text>'
    cells += text(600,195,'LIVE PROFILE DATA · @'+USER,12,'#8e9bb3',family='monospace')
    write_svg('github-ledger.svg','THE GITHUB LEDGER',cells,220)
    # Contribution heatmap: 53 columns x 7 rows, color intensity reflects actual daily count.
    maxv=max([d['contributionCount'] for d in days] or [1]); heat=''
    for i,d in enumerate(days[-371:]):
        col=i//7; row=i%7; v=d['contributionCount']; opacity=.14 if v==0 else .28+.68*(v/maxv)
        heat += f'<rect x="{40+col*20}" y="78+{row*17}" width="13" height="12" rx="3" fill="#b69ad2" opacity="{opacity:.2f}"/>'
    # Correct SVG y coordinates (no arithmetic in attributes)
    heat=''
    for i,d in enumerate(days[-371:]):
        col=i//7; row=i%7; v=d['contributionCount']; opacity=.12 if v==0 else .25+.72*(v/maxv)
        heat += f'<rect x="{40+col*20}" y="{78+row*17}" width="13" height="12" rx="3" fill="#b69ad2" opacity="{opacity:.2f}"/>'
    heat += text(1145,210,f'{total:,} contributions in the current calendar year',12,'#9eabc0','end','monospace')
    write_svg('contribution-constellation.svg','THE CONTRIBUTION CONSTELLATION',heat,235)
    # Language proportions from byte counts across the first 100 public owned repos.
    top=sorted(langs.items(),key=lambda x:x[1],reverse=True)[:6]; total_bytes=sum(v for _,v in top) or 1
    chart=''; colors=['#b69ad2','#88b7d2','#c99ab4','#c9b27c','#8eb6a6','#8b91c8']
    for i,(name,size) in enumerate(top):
        y=78+i*25; pct=size/total_bytes; chart += f'<text x="45" y="{y+15}" fill="#e4d8ef" font-family="monospace" font-size="14">{esc(name)}</text><rect x="245" y="{y}" width="760" height="15" rx="7" fill="#24283b"/><rect x="245" y="{y}" width="{760*pct:.1f}" height="15" rx="7" fill="{colors[i]}"/><text x="1050" y="{y+14}" fill="#b9abc9" font-family="monospace" font-size="13">{pct*100:.1f}%</text>'
    if not top: chart=text(600,125,'NO PUBLIC LANGUAGE DATA FOUND',18)
    write_svg('language-astrolabe.svg','THE LANGUAGE ASTROLABE',chart,245)

def leetcode():
    query='''query userProfile($username: String!) { matchedUser(username: $username) { username submitStats { acSubmissionNum { difficulty count submissions } } } userContestRanking(username: $username) { rating globalRanking } }'''
    data=request_json('https://leetcode.com/graphql/',{'query':query,'variables':{'username':'shade555'}},{'Referer':'https://leetcode.com','Origin':'https://leetcode.com'})
    u=data.get('data',{}).get('matchedUser')
    if not u: raise RuntimeError('Public profile data was not returned')
    stats=u['submitStats']['acSubmissionNum']; by={x['difficulty']:x['count'] for x in stats}
    ranking=data.get('data',{}).get('userContestRanking') or {}
    total=by.get('All',sum(v for k,v in by.items() if k!='All'))
    vals=[('TOTAL SOLVED',total),('EASY',by.get('Easy',0)),('MEDIUM',by.get('Medium',0)),('HARD',by.get('Hard',0))]
    body=''
    for i,(label,val) in enumerate(vals):
        x=160+i*290
        body += f'<path d="M{x-94} 80 L{x} 61 L{x+94} 80 V157 L{x} 176 L{x-94} 157Z" fill="#1b2034" stroke="#aa91c1" stroke-width="2"/><text x="{x}" y="119" fill="#f0e6fa" text-anchor="middle" font-family="Georgia,serif" font-size="34">{val}</text><text x="{x}" y="143" fill="#b8a8ca" text-anchor="middle" font-family="monospace" font-size="12">{label}</text>'
    rank=ranking.get('globalRanking')
    rating=ranking.get('rating')
    footer=(f"CONTEST RANK #{rank:,} · RATING {rating:.0f}" if rank and rating else 'CONTEST RANKING NOT AVAILABLE')
    body += text(600,202,footer,13,'#9eabc0',family='monospace')
    write_svg('leetcode-seal.svg','THE LEETCODE TRIAL SEAL',body,225)

OUT.mkdir(parents=True,exist_ok=True)
try:
    github()
except Exception as e:
    # Keep an explicit error state; do not manufacture statistics.
    for name,title in [('github-ledger.svg','THE GITHUB LEDGER'),('contribution-constellation.svg','THE CONTRIBUTION CONSTELLATION'),('language-astrolabe.svg','THE LANGUAGE ASTROLABE')]:
        write_svg(name,title,text(600,115,'OBSERVATORY AWAITING VALID DATA',26)+text(600,155,str(e)[:110],14,'#aeb7ca',family='monospace'),190)
try:
    leetcode()
except Exception as e:
    unavailable('THE LEETCODE TRIAL SEAL',str(e)[:110])
print('Statistics refresh completed; unavailable sources are marked explicitly.')
