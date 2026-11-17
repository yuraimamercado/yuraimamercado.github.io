import re,os,json,sys
sys.path.insert(0,''+__import__('os').path.dirname(__import__('os').path.abspath(__file__))+'')
src=open(''+__import__('os').path.dirname(__import__('os').path.abspath(__file__))+'/tr.py').read()
T=eval(src[src.index('T={')+2:src.index('\nNUM=')])
from t2 import T2
S2=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'s2.json')))
for a,b in zip(S2,T2): T.setdefault(a,b)
MAP={'/':'/en/','/sobre-mi/':'/en/about/','/pensamiento/':'/en/thinking/','/agencia/':'/en/agency/','/conferencias/':'/en/speaking/','/formacion/':'/en/training/','/prensa/':'/en/press/','/contacto/':'/en/contact/','/red/':'/en/network/','/ia/':'/en/data/'}
FILE={'/':'index.html'}
for k in MAP:
    if k!='/': FILE[k]=k.strip('/')+'/index.html'
for k in list(T):
    v=T[k]
    for x in ['(Spanish)',' (Spanish)']: pass
    T[k]=v.replace(' (Spanish)','')
SITE='https://yuraimamercado.com'
def langlink(es,en,to_en):
    return f'<a class="lang" href="{en}" hreflang="en" lang="en">EN</a>' if to_en else f'<a class="lang" href="{es}" hreflang="es" lang="es">ES</a>'
def fix_es(es,en):
    f=FILE[es]; t=open(f).read()
    t=re.sub(r'<a class="lang" href="[^"]*" hreflang="en" lang="en">EN</a>',langlink(es,en,True),t)
    t=re.sub(r'<link rel="alternate" hreflang="(es|en)" href="[^"]*">\n?','',t)
    t=t.replace('</head>',f'<link rel="alternate" hreflang="es" href="{SITE}{es}">\n<link rel="alternate" hreflang="en" href="{SITE}{en}">\n</head>',1)
    open(f,'w').write(t)
NUM={'2.495':'2,495','1.162':'1,162','1.718':'1,718','1.000':'1,000'}
def build(es,en):
    t=open(FILE[es]).read()
    keep=[]
    def prot(m): keep.append(m.group(0)); return f'\x01{len(keep)-1}\x01'
    t=re.sub(r'<(style|script)[^>]*>.*?</\1>',prot,t,flags=re.S)
    for a in sorted(T,key=len,reverse=True):
        b=T[a]
        t=re.sub(r'>(\s*)'+re.escape(a)+r'(\s*)<',lambda m:'>'+m.group(1)+b+m.group(2)+'<',t)
        t=t.replace('="'+a+'"','="'+b+'"')
    for a,b in NUM.items(): t=t.replace('<b>'+a+'<','<b>'+b+'<')
    def href(m):
        u=m.group(1); base,_,frag=u.partition('#'); 
        if base in MAP: return f'href="{MAP[base]}'+('#'+frag if frag else '')+'"'
        return m.group(0)
    t=re.sub(r'href="(/[^"]*)"',href,t)
    t=t.replace('<html lang="es"','<html lang="en"')
    t=t.replace(f'{SITE}{es}"',f'{SITE}{en}"').replace(f'{SITE}{es}?',f'{SITE}{en}?')
    t=re.sub(r'<a class="lang" href="[^"]*" hreflang="en" lang="en">EN</a>',langlink(es,en,False),t)
    t=re.sub(r'\x01(\d+)\x01',lambda m:keep[int(m.group(1))],t)
    t=t.replace("b.textContent='Enviando…'","b.textContent='Sending…'").replace("b.textContent='Enviar mi postulación'","b.textContent='Submit my application'")
    t=re.sub(r'<link rel="alternate" hreflang="(es|en)" href="[^"]*">\n?','',t)
    t=t.replace('</head>',f'<link rel="alternate" hreflang="es" href="{SITE}{es}">\n<link rel="alternate" hreflang="en" href="{SITE}{en}">\n</head>',1)
    out=en.strip('/')+'/index.html'
    os.makedirs(os.path.dirname(out),exist_ok=True); open(out,'w').write(t)
    body=re.sub(r'<(style|script)[^>]*>.*?</\1>','',t,flags=re.S)
    left=[x.strip()[:50] for x in re.findall(r'>([^<>]*[áéíóúñ¿¡][^<>]*)<',body) if x.strip()]
    print(out,'| con acentos:',left[:12])
for es,en in MAP.items():
    build(es,en); fix_es(es,en)
sm=open('sitemap.xml').read()
for en in MAP.values():
    u=SITE+en
    if u not in sm: sm=sm.replace('</urlset>',f'  <url><loc>{u}</loc></url>\n</urlset>')
open('sitemap.xml','w').write(sm)
