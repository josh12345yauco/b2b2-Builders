#!/usr/bin/env python3
"""Authoring tool — generates all project pages AND the projects hub from one data set.
Output is committed static HTML; edit data here and re-run, then run tools/inject_partials.py.
Run: python3 tools/gen_project_pages.py && python3 tools/inject_partials.py

Conventions:
- Local images live in /Images/projects/<slug>/ with SEO filenames (1600px, q75 JPEG).
- Gallery items are (src, alt) tuples. src starting with "http" is a legacy Wix
  hot-link (TODO: self-host before launch). A dict item {"video":..., "poster":..., "alt":...}
  renders a lazy <video> tile.
- "categories" drives the hub filter chips (data-project-type). First category is
  also used for the card tag label via TYPE_LABELS.
- Category showcase pages (kitchens/baths/concrete/framing) reuse the parent
  project's image folder — no duplicate files on disk.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://b2b2builders.com"  # TODO: replace placeholder domain before launch

SVC = {
    "kitchen": '<a href="/services/kitchen-remodeling/">Custom kitchen</a>',
    "kitchens": '<a href="/services/kitchen-remodeling/">custom kitchens</a>',
    "bathrooms": '<a href="/services/bathroom-remodeling/">custom bathrooms</a>',
    "stairs": '<a href="/services/framing/">custom stairs</a>',
    "framing": '<a href="/services/framing/">framing</a>',
    "concrete": '<a href="/services/concrete/">concrete</a>',
    "fullbuild": '<a href="/services/full-builds-remodeling/">ground-up construction</a>',
    "gc": '<a href="/services/general-contracting/">general contracting</a>',
}


def img(slug, name, alt):
    return (f"/Images/projects/{slug}/{name}.jpg", alt)


def vid(slug, name, alt):
    return {
        "video": f"/Images/projects/{slug}/{name}.mp4",
        "poster": f"/Images/projects/{slug}/{name}-poster.jpg",
        "alt": alt,
    }


# Project data lives in server/projects-data.json — the single source of truth,
# edited from the /admin dashboard (reorder, featured image, media uploads).
# Array order = "All Projects" base order before the category round-robin.
import json

with open(ROOT / "server" / "projects-data.json", encoding="utf-8") as _fh:
    PROJECTS = json.load(_fh)

BY_SLUG = {p["slug"]: p for p in PROJECTS}

TYPE_LABELS = {
    "full-build": "Full Builds",
    "property-rehab": "Property Rehabs",
    "kitchen": "Custom Kitchens",
    "bathroom": "Custom Bathrooms",
    "concrete": "Concrete",
    "framing": "Framing",
}


def esc_plain(html_text):
    """Strip the few entities we use in titles for plain-text contexts."""
    return html_text.replace("&amp;", "&")


def gallery_item(item, first=False):
    if isinstance(item, dict):  # video tile
        return (
            f'          <video controls preload="none" poster="{item["poster"]}" '
            f'width="600" height="450" aria-label="{item["alt"]}">\n'
            f'            <source src="{item["video"]}" type="video/mp4">\n'
            f'          </video>'
        )
    src, alt = item
    size = 'width="1200" height="600"' if first else 'width="600" height="450"'
    return f'          <img src="{src}" alt="{alt}" {size} loading="lazy">'


def similar_card(p, heading="h3"):
    hero_src = p["hero_img"][0] if not isinstance(p["hero_img"], dict) else p["hero_img"]["poster"]
    tag = f'{esc_plain(p["type"])} · {p["area"]}'
    return f'''          <li class="hub-card" data-reveal>
            <img src="{hero_src}" alt="{p["hero_img"][1]}" width="480" height="300" loading="lazy">
            <div class="hub-card-body">
              <span class="hub-card-tag">{tag}</span>
              <{heading}><a href="/projects/{p["slug"]}/">{p["title"]}</a></{heading}>
              <a class="text-link" href="/projects/{p["slug"]}/">View this project <span aria-hidden="true">→</span></a>
            </div>
          </li>'''


def hub_card(p):
    # card_img lets a parent project show a different card image than its
    # page hero, so it never looks like a duplicate of its kitchen/bath
    # showcase on the hub.
    card_src, card_alt = p.get("card_img", p["hero_img"])
    tag = f'{esc_plain(p["type"])} · {p["area"]}'
    types = " ".join(p["categories"])

    # Swipeable card gallery: lead image + up to 3 more from the project
    # gallery (photos only, no repeats of the lead image).
    slides = [(card_src, card_alt)]
    for item in [p["hero_img"]] + p["gallery"]:
        if isinstance(item, dict):
            continue
        if item[0] == card_src or any(s[0] == item[0] for s in slides):
            continue
        slides.append(item)
        if len(slides) == 4:
            break
    slides_html = "\n".join(
        f'                <img src="{src}" alt="{alt}" width="480" height="300" loading="lazy">'
        for src, alt in slides
    )
    dots_html = "".join('<span' + (' class="on"' if i == 0 else '') + '></span>' for i in range(len(slides)))
    arrow_svg = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    return f'''          <li class="hub-card" data-project-type="{types}" data-reveal>
            <div class="hub-swipe">
              <div class="hub-swipe-track">
{slides_html}
              </div>
              <button type="button" class="hs-arrow hs-prev" aria-label="Previous photo">{arrow_svg}<path d="M15 6l-6 6 6 6"/></svg></button>
              <button type="button" class="hs-arrow hs-next" aria-label="Next photo">{arrow_svg}<path d="M9 6l6 6-6 6"/></svg></button>
              <div class="hub-swipe-dots" aria-hidden="true">{dots_html}</div>
            </div>
            <div class="hub-card-body">
              <span class="hub-card-tag">{tag}</span>
              <h2><a href="/projects/{p["slug"]}/">{p["title"]}</a></h2>
              <p>{p["card_blurb"]}</p>
              <a class="text-link" href="/projects/{p["slug"]}/">View this project <span aria-hidden="true">→</span></a>
            </div>
          </li>'''


def page_html(p):
    plain_title = esc_plain(p["title"])
    title_tag = f'{p["title"]} — {p["type"]} in {p["area"]} | B2B2 Builders'
    meta_desc = (
        f'{plain_title} in {p["area"]}, Philadelphia — {esc_plain(p["type"]).lower()} by B2B2 Builders. '
        f'See the photos, scope, and story behind this project.'
    )
    url = f"{DOMAIN}/projects/{p['slug']}/"
    hero_src, hero_alt = p["hero_img"]
    og_image = hero_src if hero_src.startswith("http") else DOMAIN + hero_src
    todo = f'\n        <!-- TODO: {p["todo"]} -->' if p.get("todo") else ""

    gallery_items = [gallery_item(p["hero_img"], first=True)]
    gallery_items += [gallery_item(it) for it in p["gallery"]]
    gallery_html = "\n".join(gallery_items)

    similar_html = "\n".join(similar_card(BY_SLUG[s]) for s in p["similar"])

    narrative_html = "\n".join(f"          <p>{para}</p>" for para in p["narrative"])
    parent_note = ""
    if p.get("parent"):
        parent = BY_SLUG[p["parent"]]
        parent_note = (
            f'\n          <p>This work is part of our {parent["title"]} project — '
            f'<a href="/projects/{parent["slug"]}/">see the full project</a>, or start your own with a '
            f'<a href="/contact/">free estimate</a>.</p>'
        )
    else:
        parent_note = (
            f'\n          <p>This project sits in {p["area"]} — see everything we build there on our '
            f'<a href="/service-areas/{p["area_slug"]}/">{"Montgomery County" if p["area_slug"] == "montgomery-county" else p["area"]} service area page</a>, '
            f'or start your own project with a <a href="/contact/">free estimate</a>.</p>'
        )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_tag}</title>
  <meta name="description" content="{meta_desc}">
  <!-- TODO: replace placeholder domain before launch -->
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title_tag}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
<!-- HEAD-COMMON-START -->
<!-- HEAD-COMMON-END -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{DOMAIN}/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Projects", "item": "{DOMAIN}/projects/" }},
      {{ "@type": "ListItem", "position": 3, "name": "{plain_title}", "item": "{url}" }}
    ]
  }}
  </script>
</head>
<body>
<!-- SITE-HEADER-START -->
<!-- SITE-HEADER-END -->

  <main id="main">
    <section class="page-hero page-hero-dark">
      <img class="page-hero-bg" src="{hero_src}" alt="" width="1600" height="900" loading="eager" aria-hidden="true">
      <div class="page-hero-overlay" aria-hidden="true"></div>
      <div class="container">
        <p class="eyebrow">[ {p["type"]} ]</p>
        <h1>{p["title"]}, <em class="accent">{p["area"]}</em>.</h1>
        <dl class="project-meta" style="max-width: 640px; margin-top: 2rem;">
          <div><dt>Neighborhood</dt><dd><a href="/service-areas/{p["area_slug"]}/">{p["area"]}</a></dd></div>
          <div><dt>Project type</dt><dd>{p["type"]}</dd></div>
          <div><dt>Scope</dt><dd>{p["scope_html"]}</dd></div>
        </dl>
      </div>
    </section>

    <section class="section" style="padding-top: 0;">
      <div class="container">{todo}
        <div class="gallery-grid" data-reveal>
{gallery_html}
        </div>
      </div>
    </section>

    <section class="section" style="padding-top: 0;">
      <div class="container">
        <div class="prose" data-reveal>
          <h2>About This Project</h2>
{narrative_html}{parent_note}
        </div>
      </div>
    </section>

    <section class="section" style="padding-top: 0;">
      <div class="container">
        <div class="section-head" data-reveal>
          <div>
            <p class="eyebrow">[ More Work ]</p>
            <h2>Similar <em class="accent">Projects</em>.</h2>
          </div>
          <a class="text-link" href="/projects/">View all projects <span aria-hidden="true">→</span></a>
        </div>
        <ul class="hub-grid hub-grid-2">
{similar_html}
        </ul>
      </div>
    </section>

    <section class="cta-band">
      <div class="container">
        <h2>Want a Build Like <em class="accent-light">This</em>?</h2>
        <p>Free estimates. Real proof, block by block. A builder who picks up the phone.</p>
        <div class="cta-band-actions">
          <a class="btn btn-orange btn-lg" href="/contact/">Get a Free Estimate</a>
          <a class="btn btn-ghost-light btn-lg" href="tel:+12158884384">Call 215-888-4384</a>
        </div>
        <!-- TODO: if owner signs with a financing partner (e.g. Wisetack-style), build /financing/ page with payment comparison table and pre-qual link -->
        <p class="cta-band-note">Ask about financing options when you call.</p>
      </div>
    </section>
  </main>

<!-- SITE-FOOTER-START -->
<!-- SITE-FOOTER-END -->
</body>
</html>
'''


def hub_html():
    chips = ['          <button type="button" class="filter-chip" data-filter="all" aria-pressed="true">All Projects</button>']
    for key, label in TYPE_LABELS.items():
        chips.append(f'          <button type="button" class="filter-chip" data-filter="{key}" aria-pressed="false">{label}</button>')
    chips_html = "\n".join(chips)
    # "All Projects" order: round-robin one project per category —
    # kitchen, bathroom, concrete, framing, full build, rehab — and repeat.
    rotation = ["kitchen", "bathroom", "concrete", "framing", "full-build", "property-rehab"]
    buckets = {c: [p for p in PROJECTS if p["categories"][0] == c] for c in rotation}
    ordered = []
    while any(buckets.values()):
        for c in rotation:
            if buckets[c]:
                ordered.append(buckets[c].pop(0))
    cards_html = "\n".join(hub_card(p) for p in ordered)
    hero = "/Images/projects/new-construction-port-richmond/open-concept-living-stairs.jpg"
    meta_desc = ("Full builds, property rehabs, custom kitchens and bathrooms, concrete, and framing — "
                 "real B2B2 Builders projects across Philadelphia's River Wards and beyond.")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Our Work — Philadelphia Construction Projects | B2B2 Builders</title>
  <meta name="description" content="{meta_desc}">
  <!-- TODO: replace placeholder domain before launch -->
  <link rel="canonical" href="{DOMAIN}/projects/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Our Work — Philadelphia Construction Projects | B2B2 Builders">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="{DOMAIN}/projects/">
  <meta property="og:image" content="{DOMAIN}{hero}">
  <meta name="twitter:card" content="summary_large_image">
<!-- HEAD-COMMON-START -->
<!-- HEAD-COMMON-END -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{DOMAIN}/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Projects", "item": "{DOMAIN}/projects/" }}
    ]
  }}
  </script>
</head>
<body>
<!-- SITE-HEADER-START -->
<!-- SITE-HEADER-END -->

  <main id="main">
    <section class="page-hero page-hero-dark">
      <img class="page-hero-bg" src="{hero}" alt="" width="1600" height="900" loading="eager" aria-hidden="true">
      <div class="page-hero-overlay" aria-hidden="true"></div>
      <div class="container">
        <p class="eyebrow">[ Our Work ]</p>
        <h1>Recent <em class="accent">Projects</em>.</h1>
        <p class="page-hero-sub">Real streets, real results — full builds, property rehabs, custom kitchens and baths, concrete, and framing across Philadelphia's River Wards and Queen Village. Every project here was built by our crew, with the owner on site.</p>
      </div>
    </section>

    <section class="section" style="padding-top: 0;">
      <div class="container">
        <div class="filter-chips" id="project-filters" role="group" aria-label="Filter projects by type">
{chips_html}
        </div>

        <ul class="hub-grid">
{cards_html}
        </ul>
      </div>
    </section>

    <section class="cta-band">
      <div class="container">
        <h2>Want Yours on This <em class="accent-light">Page</em>?</h2>
        <p>Free estimates. Real proof, block by block. A builder who picks up the phone.</p>
        <div class="cta-band-actions">
          <a class="btn btn-orange btn-lg" href="/contact/">Get a Free Estimate</a>
          <a class="btn btn-ghost-light btn-lg" href="tel:+12158884384">Call 215-888-4384</a>
        </div>
        <!-- TODO: if owner signs with a financing partner (e.g. Wisetack-style), build /financing/ page with payment comparison table and pre-qual link -->
        <p class="cta-band-note">Ask about financing options when you call.</p>
      </div>
    </section>
  </main>

<!-- SITE-FOOTER-START -->
<!-- SITE-FOOTER-END -->
</body>
</html>
'''


def main():
    for p in PROJECTS:
        out = ROOT / "projects" / p["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_html(p), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")
    hub = ROOT / "projects" / "index.html"
    hub.write_text(hub_html(), encoding="utf-8")
    print(f"wrote {hub.relative_to(ROOT)}")
    print("\nSitemap URLs:")
    print(f"  {DOMAIN}/projects/")
    for p in PROJECTS:
        print(f"  {DOMAIN}/projects/{p['slug']}/")
    print("\nNow run: python3 tools/inject_partials.py")


if __name__ == "__main__":
    main()
