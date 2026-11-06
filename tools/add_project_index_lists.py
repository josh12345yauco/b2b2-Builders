#!/usr/bin/env python3
"""Add a full "every <type> project" link list under the Recent Work grid on each service page,
and an "every project in <area>" list on service-area pages.

Why (GSC 2026-11-06): 24 of 39 project pages were "Discovered – currently not indexed".
Service pages linked only 3 hand-picked cards each (the kitchen page linked none of the six
kitchen project pages), so most projects were only linked from other uncrawled project pages.
After this, every project is linked from at least one indexed service page.

Idempotent: replaces the block between PROJECT-INDEX markers. Data: server/projects-data.json.
Run: python3 tools/add_project_index_lists.py
"""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P = json.loads((ROOT / 'server/projects-data.json').read_text())

SERVICES = {
    'kitchen-remodeling':     (['kitchen'], 'kitchen'),
    'bathroom-remodeling':    (['bathroom'], 'bathroom'),
    'full-builds-remodeling': (['full-build', 'property-rehab'], 'full build &amp; rehab'),
    'concrete':               (['concrete', 'decks-patios'], 'concrete &amp; outdoor'),
    'framing':                (['framing'], 'framing &amp; structural'),
    'general-contracting':    (['property-rehab', 'finishing', 'decks-patios', 'full-build'], 'general contracting'),
}
# area page -> project areas to list (each item shows its real neighborhood)
AREAS = {
    'fishtown':          ['Fishtown', 'Kensington', 'East Kensington'],
    'east-kensington':   ['East Kensington', 'Kensington', 'Fishtown'],
    'port-richmond':     ['Port Richmond'],
    'queen-village':     ['Queen Village'],
    'montgomery-county': ['Greater Philadelphia'],
}
START = '<!-- PROJECT-INDEX:START (tools/add_project_index_lists.py) -->'
END = '<!-- PROJECT-INDEX:END -->'
CSS = """
/* ---------- Project index list (tools/add_project_index_lists.py) ---------- */
.project-index { margin-top: clamp(32px, 4vw, 48px); padding-top: clamp(24px, 3vw, 32px); border-top: 1px solid var(--line); }
.project-index .eyebrow { margin-bottom: 14px; }
.pi-list { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0 32px; }
.pi-list li { border-bottom: 1px solid var(--line); }
.pi-list a { display: flex; justify-content: space-between; align-items: baseline; gap: 16px; padding: 14px 0; color: var(--ink); text-decoration: none; font-weight: 600; }
.pi-list a:hover { color: var(--blue); }
.pi-list .pi-area { flex-shrink: 0; font-size: 0.85rem; font-weight: 500; color: var(--muted); }
"""


def block(label, items):
    lis = '\n'.join(
        f'            <li><a href="/projects/{p["slug"]}/">{html.escape(html.unescape(p["title"]))} '
        f'<span class="pi-area">{html.escape(html.unescape(p["area"]))}</span></a></li>' for p in items)
    return (f'{START}\n        <div class="project-index">\n'
            f'          <p class="eyebrow">[ {label} ]</p>\n'
            f'          <ul class="pi-list">\n{lis}\n          </ul>\n        </div>\n        {END}')


def insert(path, heading_re, label, items):
    t = path.read_text()
    if START in t:
        t2 = re.sub(re.escape(START) + r'[\s\S]*?' + re.escape(END), block(label, items), t)
    else:
        m = re.search(heading_re, t)
        if not m:
            print('  !! heading not found', path); return False
        ul_end = t.find('</ul>', t.find('<ul class="hub-grid"', m.end()))
        if ul_end < 0:
            print('  !! grid not found', path); return False
        ul_end += len('</ul>')
        t2 = t[:ul_end] + '\n        ' + block(label, items) + t[ul_end:]
    if t2 != t:
        path.write_text(t2)
    return True


covered = set()
for svc, (cats, noun) in SERVICES.items():
    items = [p for p in P if set(cats) & set(p['categories'])]
    if insert(ROOT / f'services/{svc}/index.html', r"\[ Recent Work \]", f'Every {noun} project', items):
        covered |= {p['slug'] for p in items}
        print(f'services/{svc}: {len(items)} projects')

for area, names in AREAS.items():
    items = sorted([p for p in P if p['area'] in names], key=lambda p: names.index(p['area']))
    if items and insert(ROOT / f'service-areas/{area}/index.html', r'<h2>(Projects in|Recent Projects)',
                        'Every project in and near ' + names[0] if len(names) > 1 else f'Every project in {names[0]}', items):
        covered |= {p['slug'] for p in items}
        print(f'service-areas/{area}: {len(items)} projects')

css = ROOT / 'styles.css'
if '.project-index {' not in css.read_text():
    css.write_text(css.read_text().rstrip() + '\n' + CSS)

missing = [p['slug'] for p in P if p['slug'] not in covered]
print('projects not linked from any service/area page:', missing or 'none')
