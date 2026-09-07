"""Build the dependency-free academic website for GitHub Pages."""
import json, re, shutil
from pathlib import Path
from html import escape

ROOT=Path(__file__).parent
DATA=ROOT/'content'
OUT=ROOT/'dist'
OUT.mkdir(exist_ok=True)
def copy_changed(src,dst):
    # Avoid rewriting unchanged large photos while the preview serves them.
    if Path(dst).is_file() and Path(src).read_bytes()==Path(dst).read_bytes():
        return str(dst)
    return shutil.copy2(src,dst)
shutil.copytree(ROOT/'public',OUT,dirs_exist_ok=True,copy_function=copy_changed)
shutil.copy2(ROOT/'styles.css',OUT/'styles.css')
shutil.copy2(ROOT/'custom.css',OUT/'custom.css')
pages=[('index','Home'),('research','Research'),('teaching','Teaching'),('cv','CV'),('contact','Contact')]
socials=json.loads((DATA/'socials.json').read_text(encoding='utf-8'))
coauthors=json.loads((DATA/'coauthors.json').read_text(encoding='utf-8'))
assets=json.loads((DATA/'images.json').read_text(encoding='utf-8'))
def blocks(page):return json.loads((DATA/(page+'.json')).read_text(encoding='utf-8'))
def clean(s): return s.replace('\xa0',' ').strip()
def para(s,cls=''):return f'<p class="{cls}">{clean(s)}</p>'
def profiles(icons=False):
    if icons:
        return '<div class="social-icons">'+''.join(f'<a href="{escape(s["url"],quote=True)}"><img src="{escape(s["icon"],quote=True)}" alt="" width="32" height="32"><span>{escape(s["name"])}</span></a>' for s in socials)+'</div>'
    return '<div class="profiles">'+''.join(f'<a href="{escape(s["url"],quote=True)}">{escape(s["name"])}<span aria-hidden="true"> ↗</span></a>' for s in socials)+'</div>'
def conference_refs(s):
    s=re.sub(r'\s+Previously known as', '<br>Previously known as', s)
    return re.sub(r'(?<!\w)(\d{1,2})(?!\w)',lambda m:f'<a href="#conference-{m[1]}">{m[1]}</a>',s)
def document(page,title,body,subtitle='',home=False):
    plain_title=re.sub('<[^>]+>',' ',title)
    nav=''.join(f'<a href="{p}.html"'+(' aria-current="page"' if p==page else '')+f'>{n}</a>' for p,n in pages)
    desc=('Juan Francisco Blázquiz Pulido — Ph.D. student in Economics at IMT Lucca and the University of Alicante. Behavioral and experimental economics, game theory and neuroeconomics.' if home else f'{plain_title} — Juan Francisco Blázquiz Pulido, economics researcher at IMT Lucca and the University of Alicante.')
    image=escape(assets['inicio' if home else page],quote=True)
    if home:
        title = 'Juan Francisco <span class="surname">Blázquiz Pulido</span>'
    analytics = json.loads((DATA/'analytics.json').read_text(encoding='utf-8'))
    token = analytics.get('cloudflare_token', '').strip()
    analytics_script = ''
    if token:
        if not re.fullmatch(r'[a-fA-F0-9]{32}', token):
            raise ValueError('Cloudflare beacon token must contain 32 hexadecimal characters')
        settings = json.dumps({'token': token})
        host = json.dumps(analytics['hostname'])
        analytics_script = f"<script>if(location.hostname==={host}){{const s=document.createElement('script');s.defer=true;s.src='https://static.cloudflareinsights.com/beacon.min.js';s.setAttribute('data-cf-beacon',JSON.stringify({settings}));document.body.appendChild(s);}}</script>"
    # HOME_HERO_TAGLINE: remove the HTML comment delimiters below to restore it.
    # Edit the words here to replace the optional line above your name.
    tagline='<!-- HOME_HERO_TAGLINE: <p class="eyebrow">ECONOMICS · BEHAVIOUR · DECISIONS</p> -->' if home else ''
    topics='<div class="research-tags"><span>Unethical behavior</span><span>Punishment</span><span>Social norms</span><span>Strategic sophistication</span></div>' if home else ''
    if page == 'research':
        fields = [
            ('Behavioral & Experimental Economics', ['Unethical behavior', 'Punishment', 'Social norms', 'Strategic sophistication']),
            ('Game Theory', ['Evolution', 'Learning']),
        ]
        topics = '<div id="fields" class="research-field-rows">' + ''.join(
            '<div class="research-field-row"><strong>' + escape(field) + '</strong><div class="research-tags">'
            + ''.join(f'<span>{escape(tag)}</span>' for tag in tags) + '</div></div>'
            for field, tags in fields
        ) + '</div>'
    hero=f'<section class="hero hero-{page} {"hero-home" if home else ""}" aria-labelledby="page-title"><img class="hero-image hero-image-{page}" src="{image}" alt="" fetchpriority="high"><div class="hero-shade"></div><div class="hero-content wrap">{tagline}<h1 id="page-title">{title}</h1>{para(subtitle,"hero-subtitle") if subtitle else ""}{topics}</div></section>'
    html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{'Juan Francisco Blázquiz Pulido | Economics' if home else plain_title+' | Juan Francisco Blázquiz Pulido'}</title><meta name="description" content="{escape(desc,quote=True)}"><meta name="color-scheme" content="light dark"><meta name="theme-color" media="(prefers-color-scheme: light)" content="#ffffff"><meta name="theme-color" media="(prefers-color-scheme: dark)" content="#101b29"><meta property="og:title" content="{escape(plain_title,quote=True)}"><meta property="og:description" content="{escape(desc,quote=True)}"><meta property="og:type" content="website"><script src="theme.js"></script><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="custom.css"><script src="header.js" defer></script><link rel="icon" href="{escape(assets['portrait'],quote=True)}" type="image/jpeg"></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="index.html"><img class="brand-photo" src="{escape(assets['portrait'],quote=True)}" alt="" width="52" height="52"><span>Juanfran <span class="surname">Blázquiz Pulido</span></span></a><nav aria-label="Main navigation">{nav}<button id="theme-toggle" class="theme-toggle" type="button" hidden aria-label="Colour theme: Auto">◐</button></nav></div></header><main id="main">{hero}{body}</main><footer><div class="wrap"><div class="footer-top"><div><a class="footer-name" href="index.html">Juan Francisco Blázquiz Pulido</a><p>IMT School for Advanced Studies Lucca<br>University of Alicante</p></div><div><p class="footer-label">Find me online</p>{profiles()}</div></div><div class="footer-bottom"><span>Content last updated: 3 September 2026</span><a href="mailto:jf.blazquizpulido@imtlucca.it">Get in touch <span aria-hidden="true">↗</span></a></div></div></footer>{analytics_script}</body></html>'''
    (OUT/(page+'.html')).write_text(html,encoding='utf-8')

def news_section():
    entries = json.loads((DATA/'news.json').read_text(encoding='utf-8'))
    items = []
    for entry in entries:
        title = escape(entry['title'])
        url = entry.get('url', '')
        if url:
            if not (url.startswith(('https://', 'http://')) or re.fullmatch(r'[a-z-]+\.html(?:#[a-z0-9-]+)?', url)):
                raise ValueError('News links must use HTTP(S) or a local HTML page')
            title = f'<a href="{escape(url, quote=True)}">{title}</a>'
        label = escape(entry.get('label', entry.get('date', '')))
        title = escape(entry.get('prefix', '')) + title
        detail = escape(entry.get('text', ''))
        detail_html = f'<p>{detail}</p>' if detail else ''
        items.append(f'<li><span class="news-label">{label}</span><div><p class="news-title">{title}</p>{detail_html}</div></li>')
    content = '<ul class="news-list">' + ''.join(items) + '</ul>' if items else '<p class="news-empty">Conference appearances, new papers and publication updates will appear here.</p>'
    return '<section class="home-news" aria-label="Announcements">' + content + '</section>'

home=blocks('inicio')
body=f'''<div class="wrap about-layout"><aside class="profile"><img class="portrait" src="{escape(assets['portrait'],quote=True)}" alt="Juan Francisco Blázquiz Pulido" width="1280" height="1280"><div class="profile-caption"><span class="eyebrow">PHD STUDENT IN ECONOMICS</span><p>Lucca, Italy · Alicante, Spain</p></div><div class="profile-actions"><a class="button" href="research.html#publications">Publications</a><a class="button" href="cv.html">CV</a><a class="button" href="mailto:jf.blazquizpulido@imtlucca.it">Email</a></div><div class="profile-section"><h3>Academic &amp; social profiles</h3>{profiles(icons=True)}</div></aside><article class="biography"><h2>Welcome to my academic webpage.</h2><p class="intro-note">You can call me <strong>Juanfran</strong>, a Spanish short form of Juan Francisco.</p><p class="eyebrow accent">ABOUT ME</p>{''.join(para(home[i]['html']) for i in [3,4,5])}{news_section()}<div class="text-actions"><a href="research.html">Explore my research <span aria-hidden="true">→</span></a><a href="contact.html">Contact me <span aria-hidden="true">↗</span></a></div></article></div>'''
document('index','Juan Francisco Blázquiz Pulido',body,'Ph.D. student in Economics · IMT Lucca &amp; University of Alicante',True)

b=blocks('research')
def paper(title,meta,note,abstract=None,link=None):
    for name,url in coauthors.items():
        meta=meta.replace(name, f'<a href="{escape(url,quote=True)}">{escape(name)}</a>')
    title=f'<a href="{link}">{title}<span class="paper-arrow" aria-hidden="true"> ↗</span></a>' if link else title
    return f'<article class="paper"><h3>{title}</h3><p class="paper-meta">{meta}</p>{para(conference_refs(note),"paper-note") if note else ""}'+(f'<details><summary>Read abstract</summary>{para(abstract.removeprefix("Abstract: "),"abstract")}</details>' if abstract else '')+'</article>'
research='<div class="wrap research-layout"><aside class="section-nav" aria-label="Research sections"><p class="eyebrow">ON THIS PAGE</p>'+''.join(f'<a href="#{i}">{t}</a>' for i,t in [('publications','Publications'),('working-papers','Working papers'),('work-in-progress','Work in progress'),('conferences','Conferences'),('seminars','Seminars')])+'</aside><div class="research-content">'
research+='<section id="publications" class="content-section"><div class="section-heading"><h2>Publications</h2><span>01</span></div>'+paper("Who's the deceiver? Identifying deceptive intentions in communication",'With L. Polonio and E. Bilancini · <em>Games and Economic Behavior</em>, 2024',b[6]['html'],b[7]['html'],'https://doi.org/10.1016/j.geb.2024.02.006')+'</section>'
research+='<section id="working-papers" class="content-section"><div class="section-heading"><h2>Working papers</h2><span>01</span></div>'+paper('Evolution of Conventions in Uncertain Environments','With E. Bilancini and L. Boncinelli',b[10]['html'],b[11]['html'],'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4360114')+'</section>'
research+='<section id="work-in-progress" class="content-section"><div class="section-heading"><h2>Work in progress</h2><span>04</span></div>'
research+=paper('Shooting the Messenger? The Role of Consequences and (Dis)Honesty in Punishment','<span class="tag">Job-market paper</span> Single-authored · Draft soon',b[14]['html'])
research+=paper('Unlocking strategic sophistication: How do we learn from different individuals and transfer it to new environments?','With S. Di Guida and L. Polonio · Collecting data',b[16]['html'])
research+=paper('Identity, Norms, and Anti-Social Behavior','With D. Aycinena and I. Rodríguez-Lara · Collecting data','')
research+=paper('The Role of Instructions on Strategic Sophistication','With T. Celadin, F. Panizza, E. Bilancini and L. Polonio · Drafting phase','')+'</section>'
research+='<section id="conferences" class="content-section"><div class="section-heading"><h2>Conferences</h2><span>2021–2026</span></div>'
opened=False
for block in b[20:50]:
    txt=clean(block['text']);html=clean(block['html'])
    if not txt:continue
    if re.fullmatch(r'20\d{2}',txt):
        if opened:research+='</ol></div>'
        research+=f'<div class="conference-year"><h3>{txt}</h3><ol class="conference-list">';opened=True
    else:
        match=re.match(r'(\d+)\)\s*',txt)
        if match:
            n=match[1];html=re.sub(r'^\d+\)\s*','',html)
            research+=f'<li id="conference-{n}"><span class="conference-number">{n.zfill(2)}</span><p>{html}</p></li>'
if opened:research+='</ol></div>'
research+='</section><section id="seminars" class="content-section"><h2>Seminars</h2>'+para(b[51]['html'])+'</section></div></div>'
document('research','Research',research)

courses=[('Graduate','Evolutionary Game Theory','Ph.D. in Economics','IMT School for Advanced Studies Lucca','Spring 2022','English'),('Undergraduate','Introduction to microeconomics','BSc in Tourism and Business Administration','University of Alicante','Fall 2025','Spanish'),('Undergraduate','Statistics and introduction to econometrics','BSc in Business Administration','University of Alicante','Fall 2025','Spanish'),('Undergraduate','Quantitative methods for international relations','BSc in Law and International Relations','University of Alicante','Spring 2024','Spanish'),('Undergraduate','Introduction to statistics','BSc in Tourism and Business Administration','University of Alicante','Spring 2019','Spanish')]
teaching='<div class="wrap teaching-content">'
for level in ['Graduate','Undergraduate']:
    teaching+=f'<section class="teaching-section"><div><p class="eyebrow accent">TEACHING EXPERIENCE</p><h2>{level} level</h2></div><div>'
    for c in [c for c in courses if c[0]==level]:
        teaching+=f'<article class="course"><div class="course-meta"><span>{c[4]}</span><span>Taught in {c[5]}</span></div><h3>{c[1]}</h3><p>{c[2]}<br><span class="muted">{c[3]}</span></p></article>'
    teaching+='</div></section>'
teaching+='</div>'
document('teaching','Teaching',teaching)

cv='''<div class="wrap cv-content"><div class="cv-intro"><div><p class="eyebrow accent">CURRICULUM VITAE</p><h2>My academic experience.</h2><p>You can download my CV in PDF format below.</p></div><a class="button" href="assets/CV_Juanfran_Blazquiz.pdf" download>Download CV <span aria-hidden="true">↓</span></a></div><object class="cv-preview" data="assets/CV_Juanfran_Blazquiz.pdf" type="application/pdf" aria-label="Curriculum vitae PDF"><p><a href="assets/CV_Juanfran_Blazquiz.pdf">Open the CV (PDF)</a></p></object><p class="muted"><a href="assets/CV_Juanfran_Blazquiz.pdf">Open PDF in your browser ↗</a></p></div>'''
document('cv','Curriculum vitae',cv)

contact=f'''<div class="wrap contact-content"><div class="contact-grid"><div class="contact-information"><section><span class="contact-number">EMAIL</span><h3>Email addresses</h3><div class="contact-emails"><a class="email" href="mailto:jf.blazquizpulido@imtlucca.it">jf.blazquizpulido@imtlucca.it ↗</a><a class="email" href="mailto:juanfrancisco.blazquiz@ua.es">juanfrancisco.blazquiz@ua.es ↗</a></div></section><section><span class="contact-number">ADDRESS / SPAIN</span><h3>University of Alicante</h3><address>Department of Economics, Universidad de Alicante<br>03690 San Vicente del Raspeig (Alicante), Spain</address></section></div><figure class="contact-photo"><img src="{escape(assets['contact_photo'],quote=True)}" alt="Hand sculpture on the University of Alicante campus" width="620" height="368" loading="lazy"></figure></div><section class="contact-socials"><h2>Academic &amp; social profiles</h2>{profiles(icons=True)}</section></div>'''
document('contact','Contact',contact,'Alicante, Spain')
(OUT/'.nojekyll').write_text('')
# Retain the original home-page name for bookmarks and migrated links.
(OUT/'inicio.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=index.html"><title>Juan Francisco Blázquiz Pulido</title><a href="index.html">Go to the homepage</a></html>',encoding='utf-8')
print('Built five pages, home alias, stylesheet and assets in dist/')

