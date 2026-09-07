from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
root=Path(__file__).parent
out=root/'dist'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.links=[];self.images=[];self.h1=0;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        if tag in ['a','link'] and a.get('href'):self.links.append(a['href'])
        if tag=='img':self.images.append(a.get('src'))
        if tag=='h1':self.h1+=1
pages={p.name:Page(p.read_text(encoding='utf-8')) for p in out.glob('*.html')}
for name,page in pages.items():
    for href in page.links:
        u=urlsplit(href)
        if u.scheme or u.netloc:continue
        target=unquote(u.path) or name
        assert (out/target).exists(),(name,href)
        if u.fragment:assert u.fragment in pages[target].ids,(name,href)
    if name!='inicio.html':assert page.h1==1,name
    for src in page.images:
        assert not urlsplit(src).scheme,('Expected local image',name,src)
        assert (out/src).is_file(),(name,src)
research=(out/'research.html').read_text(encoding='utf-8')
for n in range(1,24):assert f'conference-{n}' in pages['research.html'].ids,n
assert research.count('<details>')==2
for idx in [7,11]:
    b=json.loads((root/'content/research.json').read_text(encoding='utf-8'))[idx]
    assert b['html'].removeprefix('Abstract: ').strip() in research
home=(out/'index.html').read_text(encoding='utf-8')
for dest in ['x.com/juanfranbp4','linkedin.com/in/juan-francisco-blazquiz-pulido','scholar.google.es/citations?user=8MHfUIMAAAAJ','github.com/juanfranbp4','orcid.org/0000-0001-9426-1583','researchgate.net/profile/Juan-Francisco-Blazquiz-Pulido']:assert dest in home,dest
contact=(out/'contact.html').read_text(encoding='utf-8')
for email in ['jf.blazquizpulido@imtlucca.it','juanfrancisco.blazquiz@ua.es']:assert 'mailto:'+email in contact
assert (out/'assets/CV_Juanfran_Blazquiz.pdf').read_bytes().startswith(b'%PDF')
images=json.loads((root/'content/images.json').read_text(encoding='utf-8'))
for key in ['inicio','research','teaching','cv','contact']:
    assert images[key] in pages[('index' if key=='inicio' else key)+'.html'].images
    assert not urlsplit(images[key]).scheme,('Background must be local',key)
    assert (out/images[key]).is_file(),key
assert images['portrait'] in pages['index.html'].images
socials=json.loads((root/'content/socials.json').read_text(encoding='utf-8'))
assert len(socials)==7
assert [s['name'] for s in socials][:2]==['X','Bluesky']
for social in socials:
    assert social['url'] in pages['index.html'].links
    assert social['icon'] in pages['index.html'].images
assert '>Home</a>' in home
assert home.index('Welcome to my academic webpage.') < home.index('ABOUT ME')
assert home.index('You can call me Juanfran') < home.index('ABOUT ME')
assert '<!-- HOME_HERO_TAGLINE:' in home
assert home.index('class="social-icons"') < home.index('</aside>')
assert 'class="brand-photo"' in home
assert 'research.html#publications' in pages['index.html'].links
assert 'mailto:jf.blazquizpulido@imtlucca.it' in pages['index.html'].links
assert '<br>Previously known as' in research
assert 'Piazza S. Francesco' not in contact
assert contact.index('EMAIL') < contact.index('ADDRESS / SPAIN')
assert images['contact_photo'] in pages['contact.html'].images
assert 'Graduate and undergraduate courses' not in (out/'teaching.html').read_text(encoding='utf-8')
for social in socials:assert social['icon'] in pages['contact.html'].images
for url in json.loads((root/'content/coauthors.json').read_text(encoding='utf-8')).values():assert url in pages['research.html'].links
print('PASS: internal links, local images, five pages, 23 conferences, both abstracts, seven profiles and icons, both emails, local CV, updated Home layout and commented tagline.')
print('No browser visual test was performed.')
