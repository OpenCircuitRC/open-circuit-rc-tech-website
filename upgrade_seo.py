from pathlib import Path
import re, json
root=Path('/mnt/data/seo_work/public')

def head_meta(title, description, url, image='assets/logo.png'):
    return f'''<meta name="description" content="{description}">\n  <meta name="robots" content="index,follow,max-image-preview:large">\n  <link rel="canonical" href="{url}">\n  <meta property="og:title" content="{title}">\n  <meta property="og:description" content="{description}">\n  <meta property="og:type" content="website">\n  <meta property="og:url" content="{url}">\n  <meta property="og:image" content="https://opencircuitrc.com/{image}">\n  <meta property="og:site_name" content="Open Circuit RC &amp; Tech">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="{title}">\n  <meta name="twitter:description" content="{description}">\n  <meta name="twitter:image" content="https://opencircuitrc.com/{image}">'''

# Upgrade home page metadata and structured data
p=root/'index.html'
s=p.read_text()
s=s.replace('<meta name="description" content="Open Circuit RC & Tech - RC cars, boats, drones, tech reviews, tests and builds.">\n  <title>Open Circuit RC & Tech</title>',
'''<meta name="description" content="Open Circuit RC &amp; Tech features hands-on RC car, RC boat, drone and technology reviews, tests, tips, and free Windows and Android apps.">\n  <meta name="robots" content="index,follow,max-image-preview:large">\n  <link rel="canonical" href="https://opencircuitrc.com/">\n  <meta property="og:title" content="Open Circuit RC &amp; Tech | RC, Drones, Tech &amp; Apps">\n  <meta property="og:description" content="Hands-on RC car, boat, drone and technology reviews plus practical Windows and Android apps from Open Circuit RC &amp; Tech.">\n  <meta property="og:type" content="website">\n  <meta property="og:url" content="https://opencircuitrc.com/">\n  <meta property="og:image" content="https://opencircuitrc.com/assets/banner.png">\n  <meta property="og:site_name" content="Open Circuit RC &amp; Tech">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="Open Circuit RC &amp; Tech | RC, Drones, Tech &amp; Apps">\n  <meta name="twitter:description" content="Hands-on RC car, boat, drone and technology reviews plus practical Windows and Android apps.">\n  <meta name="twitter:image" content="https://opencircuitrc.com/assets/banner.png">\n  <title>Open Circuit RC &amp; Tech | RC, Drones, Tech &amp; Apps</title>''')
s=s.replace('href="tools.html">Software &amp; Apps', 'href="/tools">Software &amp; Apps')
s=s.replace('href="tools.html">Software &amp; Apps', 'href="/tools">Software &amp; Apps')
# add descriptive app hub callout before footer
needle='''    <section class="subscribe">'''
if '<!-- SEO app hub -->' not in s:
    s=s.replace(needle, '''    <!-- SEO app hub -->\n    <section class="section dark-band seo-app-hub" aria-labelledby="software-apps-heading">\n      <div class="section-heading compact"><div><p class="kicker">FREE SOFTWARE &amp; APPS</p><h2 id="software-apps-heading">Tools for <span>RC, tech &amp; more</span></h2></div></div>\n      <p class="seo-hub-copy">Explore free Windows and Android apps from Open Circuit RC &amp; Tech, including a Windows file extension changer, RC calculators, an astrophotography sky planner, and a simple Android solitaire game.</p>\n      <a class="btn btn-primary" href="/tools">EXPLORE SOFTWARE &amp; APPS ↗</a>\n    </section>\n\n'''+needle)
# structured data before </head>
schema='''  <script type="application/ld+json">\n  {\n    "@context":"https://schema.org",\n    "@type":"WebSite",\n    "name":"Open Circuit RC & Tech",\n    "url":"https://opencircuitrc.com/",\n    "description":"Hands-on RC car, RC boat, drone and technology reviews plus free Windows and Android apps."\n  }\n  </script>\n'''
if '"@type":"WebSite"' not in s:
    s=s.replace('  <link rel="stylesheet" href="styles.css">', '  <link rel="stylesheet" href="styles.css">\n'+schema)
p.write_text(s)

# Upgrade tools page metadata, cards, internal links
p=root/'tools.html'; s=p.read_text()
s=re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Free Windows and Android software from Open Circuit RC &amp; Tech: File Extension Changer, RC Toolbox, Astro Sky Planner, and Simply Solitaire.">', s, count=1)
s=re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="https://opencircuitrc.com/tools">', s, count=1)
s=s.replace('<meta property="og:title" content="Open Circuit Tools & Downloads">', '<meta property="og:title" content="Software &amp; Apps | Free Windows &amp; Android Tools | Open Circuit RC &amp; Tech">')
s=s.replace('<meta property="og:description" content="Free utilities and app downloads from Open Circuit RC & Tech.">', '<meta property="og:description" content="Free Windows and Android apps from Open Circuit RC &amp; Tech, including File Extension Changer, RC Toolbox, Astro Sky Planner, and Simply Solitaire.">')
s=s.replace('<title>Tools & Downloads | Open Circuit RC & Tech</title>', '<meta property="og:url" content="https://opencircuitrc.com/tools"><meta property="og:image" content="https://opencircuitrc.com/assets/banner.png"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Software &amp; Apps | Open Circuit RC &amp; Tech"><meta name="twitter:description" content="Free Windows and Android apps from Open Circuit RC &amp; Tech."><meta name="twitter:image" content="https://opencircuitrc.com/assets/banner.png"><title>Software &amp; Apps | Free Windows &amp; Android Tools | Open Circuit RC &amp; Tech</title>')
s=s.replace('<h1>TOOLS <span>&amp;</span> DOWNLOADS</h1>', '<h1>SOFTWARE <span>&amp;</span> APPS</h1>')
s=s.replace('<a href="tools.html" aria-current="page">Software &amp; Apps</a>', '<a href="/tools" aria-current="page">Software &amp; Apps</a>')
# Add intro semantic copy
s=s.replace('<p>Free utilities and apps made for practical problems, whether you\'re working with RC gear, files, or everyday tech.</p>', '<p>Free Windows and Android software from Open Circuit RC &amp; Tech for file management, RC calculations, astrophotography planning, and casual gaming.</p>')
# add learn more links to each card after buttons if absent
repls=[
('DOWNLOAD HERE <span>→</span></a>\n      </article>','DOWNLOAD HERE <span>→</span></a>\n        <a class="tool-detail-link" href="/file-extension-changer">LEARN MORE ABOUT FILE EXTENSION CHANGER →</a>\n      </article>',1),
('DOWNLOAD HERE <span>→</span></a>\n      </article>','DOWNLOAD HERE <span>→</span></a>\n        <a class="tool-detail-link" href="/rc-toolbox">LEARN MORE ABOUT RC TOOLBOX →</a>\n      </article>',1),
('DOWNLOAD HERE <span>→</span></a>\n      </article>','DOWNLOAD HERE <span>→</span></a>\n        <a class="tool-detail-link" href="/astro-sky-planner">LEARN MORE ABOUT ASTRO SKY PLANNER →</a>\n      </article>',1),
('Download here <span>→</span></a>\n      </article>','Download here <span>→</span></a>\n        <a class="tool-detail-link" href="/simply-solitaire">LEARN MORE ABOUT SIMPLY SOLITAIRE →</a>\n      </article>',1),
]
for old,new,count in repls:
    s=s.replace(old,new,count)
# add page schema
schema='''  <script type="application/ld+json">\n  {\n    "@context":"https://schema.org",\n    "@type":"CollectionPage",\n    "name":"Software & Apps | Open Circuit RC & Tech",\n    "url":"https://opencircuitrc.com/tools",\n    "description":"Free Windows and Android apps from Open Circuit RC & Tech.",\n    "isPartOf":{"@type":"WebSite","name":"Open Circuit RC & Tech","url":"https://opencircuitrc.com/"}\n  }\n  </script>\n'''
if '"@type":"CollectionPage"' not in s:
    s=s.replace('  <link rel="stylesheet" href="styles.css">', '  <link rel="stylesheet" href="styles.css">\n'+schema)
p.write_text(s)

# Apps page is retained as legacy directory but canonicalized to the main software page
p=root/'apps.html'; s=p.read_text()
s=re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Free Windows and Android apps from Open Circuit RC &amp; Tech. Browse File Extension Changer, RC Toolbox, Astro Sky Planner, and Simply Solitaire.">', s, count=1)
s=re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="https://opencircuitrc.com/tools">', s, count=1)
s=s.replace('<title>Apps & Downloads | Windows & Android | Open Circuit RC & Tech</title>', '<title>Software &amp; Apps | Open Circuit RC &amp; Tech</title>')
s=s.replace('<a href="tools.html">Software &amp; Apps</a>', '<a href="/tools">Software &amp; Apps</a>')
s=s.replace('<a class="back-link" href="tools.html">← BACK TO TOOLS</a>', '<a class="back-link" href="/tools">← BACK TO SOFTWARE &amp; APPS</a>')
p.write_text(s)

# Dedicated SEO pages
pages={
'file-extension-changer.html':{
'title':'File Extension Changer for Windows | Bulk Rename File Extensions | Open Circuit RC & Tech',
'desc':'Free Windows file extension changer for bulk renaming. Change existing file extensions, add extensions to files without one, and preview changes before renaming.',
'url':'https://opencircuitrc.com/file-extension-changer', 'badge':'Windows App', 'h1':'File Extension Changer',
'copy':'''File Extension Changer is a free Windows utility for bulk-changing file extensions without changing the contents of the files. It is useful when many files need the same extension change or when a collection of files is missing an extension.<br><br>Choose a folder, enter the new extension, preview the proposed filenames, and then rename the files. The app can also add an extension to files that currently have none. It is designed as a portable Windows EXE, so there is no traditional installer to manage.''',
'img':'assets/file-extension-changer-preview.png','alt':'File Extension Changer Windows app screenshot showing folder selection, rename settings and preview',
'download':'https://github.com/OpenCircuitRC/open-circuit-rc-tech-website/releases/download/v1.0.0/ExtensionChanger.exe','download_text':'DOWNLOAD FOR WINDOWS',
'features':[('Bulk extension changes','Rename large groups of files in one operation.'),('Missing extensions','Add an extension to files that do not currently have one.'),('Preview before rename','Review current and new filenames before committing changes.'),('Portable EXE','Run the utility directly without a traditional installer.')],
'faqs':[('Does File Extension Changer convert files?','No. It changes the filename extension only. It does not convert, transcode, or modify the file contents.'),('Can I preview the changes first?','Yes. The app can show the current filename and proposed new filename before the rename operation is performed.')],
},
'rc-toolbox.html':{
'title':'RC Toolbox Android App | RC Calculators for Cars, Boats & More | Open Circuit RC & Tech',
'desc':'RC Toolbox is a free Android app with practical RC calculators for LiPo batteries, volts, amps, watts, gear ratios, motor RPM and RC vehicle top speed.',
'url':'https://opencircuitrc.com/rc-toolbox','badge':'Android App','h1':'RC Toolbox',
'copy':'''RC Toolbox is a practical Android app built for radio-controlled vehicles. It puts commonly needed RC calculations in one place so you can work out battery current, charge time, electrical values, gearing, motor RPM, and theoretical vehicle speed.<br><br>The app is aimed at RC car, RC truck, RC boat, and other hobby users who want quick calculations without reaching for a calculator and a notebook every time.''',
'img':'assets/rc-toolbox-preview.jpg','alt':'RC Toolbox Android app screenshot showing LiPo, speed and drivetrain calculators',
'download':'https://drive.google.com/file/d/1vV8w6mz_6OqEIOA8BLZjFXE29fUuCOen/view?usp=drive_link','download_text':'DOWNLOAD HERE',
'features':[('LiPo & power','Calculate battery current, charging time, volts, amps and watts.'),('Drivetrain & speed','Work with external gear ratio and theoretical top speed.'),('Motor RPM','Estimate theoretical RPM for brushed and brushless motors.'),('RC-focused','Designed around practical calculations used in the RC hobby.')],
'faqs':[('What is RC Toolbox?','RC Toolbox is an Android calculator app focused on common radio-controlled vehicle calculations.'),('Is RC Toolbox only for RC cars?','No. Many calculations are useful across RC cars, trucks, boats and other hobby vehicles.')],
},
'astro-sky-planner.html':{
'title':'Astro Sky Planner Android App | Astrophotography Planning Tool | Open Circuit RC & Tech',
'desc':'Astro Sky Planner is a free Android astrophotography companion that helps find the best sky objects for your location and conditions, with forecasts and Bortle Class information.',
'url':'https://opencircuitrc.com/astro-sky-planner','badge':'Android App','h1':'Astro Sky Planner',
'copy':'''Astro Sky Planner is an astrophotography companion Android app that helps you decide what is worth photographing from your location and on a given night. It brings together local sky conditions, a forecast, recommended targets, and Bortle Class information in one planning tool.<br><br>For astrophotographers, the idea is simple: spend less time figuring out what is visible and more time capturing it. The app is designed to help you choose promising targets based on where you are and the conditions you have.''',
'img':'assets/astro-sky-planner-icon-mockup.png','alt':'Astro Sky Planner Android app icon and branding mockup',
'download':'https://drive.google.com/file/d/1Z4X4zSVtpeZYjjzGJAEkfb-Mw8x3cjHn/view?usp=drive_link','download_text':'DOWNLOAD HERE',
'features':[('Target planning','Find promising sky objects for your location and night.'),('Local forecast','Use the forecast and conditions when planning an observing session.'),('Bortle Class','See the light-pollution class associated with the location.'),('Astrophotography focused','Built as a practical companion for people planning imaging sessions.')],
'faqs':[('What is Astro Sky Planner?','It is an Android astrophotography planning app that combines location, sky conditions, forecasts, targets and Bortle Class information.'),('Does it tell me what to photograph?','The app is designed to help identify good sky targets for the selected location and conditions.')],
},
'simply-solitaire.html':{
'title':'Simply Solitaire Android App | Free Simple Solitaire Game | Open Circuit RC & Tech',
'desc':'Simply Solitaire is a free, simple Android solitaire game with draw-one and draw-three play, drag-and-drop cards and a clean interface.',
'url':'https://opencircuitrc.com/simply-solitaire','badge':'Android App','h1':'Simply Solitaire',
'copy':'''Simply Solitaire is a simple Android solitaire app built around classic Klondike-style card play. It keeps the interface focused on the game, with draw-one and draw-three options, movable cards, foundation play, and a new-game control.<br><br>The goal is straightforward: a lightweight solitaire game that is easy to understand and quick to play without unnecessary menus or clutter.''',
'img':'assets/simply-solitaire-preview.jpg','alt':'Simply Solitaire Android game screenshot showing cards, draw options and game controls',
'download':'https://drive.google.com/file/d/1GDB3TyQPQXAv4PUwfIHdvGpGc3RukcRB/view?usp=sharing','download_text':'DOWNLOAD HERE',
'features':[('Draw 1 or Draw 3','Choose between the two common stock-draw styles.'),('Simple controls','Tap to select and move cards, with drag-and-drop support.'),('Foundation play','Double-tap a card to move it to a foundation when possible.'),('Lightweight Android game','A focused solitaire experience without unnecessary complexity.')],
'faqs':[('Is Simply Solitaire free?','Yes. The app is provided as a free Android download.'),('How do you play Simply Solitaire?','Select cards and move them between columns or foundations. The app supports draw-one and draw-three stock options.')],
}
}

nav='''<header class="site-header">\n    <a class="brand" href="index.html" aria-label="Open Circuit RC & Tech home"><img src="assets/logo.png" alt="Open Circuit RC & Tech logo"></a>\n    <button class="menu-toggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>\n    <nav class="nav">\n      <a href="index.html#reviews">Playlists</a>\n      <a href="https://www.youtube.com/@OpenCircuitRC/shorts">Shorts</a>\n      <a href="/tools" aria-current="page">Software &amp; Apps</a>\n      <a href="index.html#about">About</a>\n      <a class="nav-social" href="https://www.youtube.com/@OpenCircuitRC" target="_blank" rel="noopener noreferrer" aria-label="YouTube" title="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8ZM9.6 15.9V8.1l6.5 3.9-6.5-3.9Z"/></svg></a>\n      <a class="nav-social" href="https://www.facebook.com/OpenCircuitRCTech" target="_blank" rel="noopener noreferrer" aria-label="Facebook" title="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 22v-8h2.7l.4-3h-3.1V9.1c0-.9.3-1.6 1.7-1.6h1.8V4.8c-.3 0-1.4-.1-2.6-.1-2.6 0-4.3 1.6-4.3 4.4V11H7.4v3h2.7v8h3.4Z"/></svg></a>\n    </nav>\n  </header>'''
footer='''<footer class="site-footer">\n    <div class="footer-brand"><img src="assets/logo.png" alt="Open Circuit RC & Tech"><span>© <span id="year"></span> Open Circuit RC & Tech</span></div>\n    <div class="footer-links"><a href="index.html#reviews">Playlists</a><a href="/tools">Software &amp; Apps</a><a href="index.html#about">About</a><a href="https://www.youtube.com/@OpenCircuitRC" target="_blank" rel="noopener">YouTube ↗</a><a href="https://www.facebook.com/OpenCircuitRCTech" target="_blank" rel="noopener">Facebook ↗</a></div>\n  </footer>\n  <script src="site-config.js"></script><script src="script.js"></script>'''
for fn,d in pages.items():
    feats=''.join(f'<div class="app-feature"><h3>{a}</h3><p>{b}</p></div>' for a,b in d['features'])
    faqs=''.join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q,a in d['faqs'])
    schema={"@context":"https://schema.org","@type":"SoftwareApplication","name":d['h1'],"applicationCategory":"UtilitiesApplication","operatingSystem":"Android" if 'Android' in d['badge'] else "Windows 11","description":re.sub('<br><br>',' ',d['copy']).replace('<br>',' '),'url':d['url'],"image":"https://opencircuitrc.com/"+d['img'],"offers":{"@type":"Offer","price":"0","priceCurrency":"USD","availability":"https://schema.org/InStock"},"publisher":{"@type":"Organization","name":"Open Circuit RC & Tech","url":"https://opencircuitrc.com/"}}
    if d['h1']=='File Extension Changer': schema['downloadUrl']=d['download']
    html=f'''<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <title>{d['title']}</title>\n  {head_meta(d['title'],d['desc'],d['url'],d['img'])}\n  <link rel="stylesheet" href="styles.css">\n  <script type="application/ld+json">{json.dumps(schema,separators=(',',':'))}</script>\n</head>\n<body>\n  <div class="top-glow"></div>\n  {nav}\n  <main class="page-shell app-page">\n    <section class="page-hero">\n      <p class="eyebrow">OPEN CIRCUIT • SOFTWARE &amp; APPS</p>\n      <h1>{d['h1']}</h1>\n      <p>{d['desc']}</p>\n    </section>\n    <section class="app-detail">\n      <div class="app-detail-media"><img src="{d['img']}" alt="{d['alt']}" loading="eager"></div>\n      <div class="app-detail-copy">\n        <span class="tool-badge">{d['badge']}</span>\n        <h2>About {d['h1']}</h2>\n        <p>{d['copy']}</p>\n        <div class="tool-meta">{'<span>Free</span><span>Android</span>' if 'Android' in d['badge'] else '<span>Free</span><span>Windows 11</span><span>Portable EXE</span>'}</div>\n        <a class="btn btn-primary" href="{d['download']}" target="_blank" rel="noopener noreferrer">{d['download_text']} <span>→</span></a>\n      </div>\n    </section>\n    <section class="app-features" aria-labelledby="features-heading">\n      <div class="section-heading compact"><div><p class="kicker">FEATURES</p><h2 id="features-heading">What it <span>does</span></h2></div></div>\n      <div class="app-feature-grid">{feats}</div>\n    </section>\n    <section class="seo-copy" aria-labelledby="faq-heading">\n      <h2 id="faq-heading">Frequently asked questions</h2>\n      <div class="faq-grid">{faqs}</div>\n    </section>\n    <a class="back-link" href="/tools">← BACK TO SOFTWARE &amp; APPS</a>\n  </main>\n  {footer}\n</body>\n</html>\n'''
    (root/fn).write_text(html)

# Sitemap and clean URL rewrites
(root/'sitemap.xml').write_text('''<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>https://opencircuitrc.com/</loc></url>\n  <url><loc>https://opencircuitrc.com/tools</loc></url>\n  <url><loc>https://opencircuitrc.com/file-extension-changer</loc></url>\n  <url><loc>https://opencircuitrc.com/rc-toolbox</loc></url>\n  <url><loc>https://opencircuitrc.com/astro-sky-planner</loc></url>\n  <url><loc>https://opencircuitrc.com/simply-solitaire</loc></url>\n</urlset>\n''')
(root/'_redirects').write_text('''/tools /tools.html 200\n/apps /tools 301\n/apps.html /tools 301\n/tools.html /tools 301\n/file-extension-changer /file-extension-changer.html 200\n/rc-toolbox /rc-toolbox.html 200\n/astro-sky-planner /astro-sky-planner.html 200\n/simply-solitaire /simply-solitaire.html 200\n''')

# Styles appended for SEO detail pages and hub
css=root/'styles.css'; s=css.read_text()
if '.app-detail{' not in s:
    s += '''\n\n/* SEO-focused software detail pages */\n.seo-app-hub{margin-top:60px}\n.seo-hub-copy{max-width:820px;color:var(--muted);margin:0 0 22px}\n.tool-detail-link{display:block;margin-top:16px;color:#aaa;font-size:.7rem;font-weight:900;letter-spacing:.09em;text-transform:uppercase}\n.tool-detail-link:hover{color:var(--orange)}\n.app-detail{display:grid;grid-template-columns:minmax(320px,.9fr) minmax(0,1.1fr);gap:42px;margin-top:46px;align-items:center}\n.app-detail-media{background:#090909;border:1px solid var(--line);padding:14px;overflow:hidden}\n.app-detail-media img{display:block;width:100%;max-height:600px;object-fit:contain;margin:0 auto}\n.app-detail-copy h2{margin:14px 0 12px;font-family:'Barlow Condensed';font-size:2.8rem;text-transform:uppercase}\n.app-detail-copy p{color:#c7c7c7;font-size:1rem;line-height:1.7}\n.app-detail-copy .btn{margin-top:4px}\n.app-features{margin-top:70px;padding-top:30px;border-top:1px solid var(--line)}\n.app-feature-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:28px}\n.app-feature{background:#0d0d0d;border:1px solid var(--line);padding:24px}\n.app-feature h3{margin:0 0 8px;font-family:'Barlow Condensed';font-size:1.45rem;text-transform:uppercase;color:var(--orange)}\n.app-feature p{margin:0;color:var(--muted);font-size:.9rem;line-height:1.55}\n@media(max-width:900px){.app-detail{grid-template-columns:1fr;gap:26px}.app-feature-grid{grid-template-columns:1fr}}\n'''
css.write_text(s)

print('SEO upgrade complete')
