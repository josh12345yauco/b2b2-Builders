#!/usr/bin/env python3
"""Authoring tool — generates the 7 project pages from one template.
Output is committed static HTML; edit data here and re-run, or edit pages directly.
Run: python3 tools/gen_project_pages.py  (then tools/inject_partials.py)
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIX = "https://static.wixstatic.com/media/dc69ab_"

SERVICE_LINKS = {
    "kitchen": '<a href="/services/kitchen-bathroom-remodeling/">Custom kitchen</a>',
    "bathrooms": '<a href="/services/kitchen-bathroom-remodeling/">custom bathrooms</a>',
    "stairs": '<a href="/services/framing/">custom stairs</a>',
    "fullbuild": '<a href="/services/full-builds-remodeling/">full build</a>',
}

PROJECTS = [
    {
        "slug": "1502-hancock-street",
        "address": "1502 Hancock Street",
        "area": "Fishtown",
        "area_slug": "fishtown",
        "type": "Full Build",
        "scope_html": '<a href="/services/kitchen-bathroom-remodeling/">Custom kitchen</a>, <a href="/services/kitchen-bathroom-remodeling/">custom bathrooms</a>, <a href="/services/framing/">custom stairs</a>',
        "hero_img": ("58a09638df8844398aef21b5015379da~mv2.png", "Street view of the completed full build at 1502 Hancock Street in Fishtown"),
        "gallery": [
            ("e84e9c093ada4984a8384c1e2abda728~mv2.png", "Open living space with custom stairs at 1502 Hancock Street"),
            ("3ff41089664044d0b53d9e33a20258b8~mv2.png", "Custom white kitchen with island and stainless appliances"),
            ("e74a63f2dd9840cda488bc6dbdd96786~mv2.png", "Kitchen with custom cabinetry and pendant lighting"),
            ("602d411d7b4c4b8cb1a2966014cab539~mv2.png", "Custom bathroom with freestanding tub"),
            ("4700d96463914c44a1912149f4924ad3~mv2.png", "Glass-enclosed tiled shower in a custom bathroom"),
            ("5dc3f24376c34e6e8dd8e05c64067ba0~mv2.png", "Facade detail of the new construction at 1502 Hancock Street"),
        ],
        "narrative": [
            "A large project constructed on one of the busiest corridors in Fishtown — the kind of block where the neighborhood watches a build go up in real time. We built 1502 Hancock Street from the ground up: structure, systems, and every finish inside.",
            "The interior program was custom throughout — a custom kitchen with a full island, custom bathrooms including a freestanding tub and glass-enclosed shower, and stairs our carpenters built on site rather than ordering from a catalog. Open living spaces put the stair work on display, so there was nowhere for sloppy carpentry to hide.",
            "Fishtown full builds run through Philadelphia L&I permitting with inspections at every phase, and this one passed them on schedule. It now stands as our calling card in the neighborhood where we're headquartered.",
        ],
        "todo": "owner to confirm/add real project details — starting condition of the lot, program (units/floors), one challenge solved during the build",
        "similar": ["1855-e-huntingdon-street", "1745-waterloo-street"],
    },
    {
        "slug": "1855-e-huntingdon-street",
        "address": "1855 E Huntingdon Street",
        "area": "East Kensington",
        "area_slug": "east-kensington",
        "type": "Full Build",
        "scope_html": '<a href="/services/kitchen-bathroom-remodeling/">Custom kitchen</a>, <a href="/services/kitchen-bathroom-remodeling/">custom bathrooms</a>, <a href="/services/framing/">custom stairs</a>',
        "hero_img": ("f0f2c5b4b264485cb8651cadbb1cd684~mv2.jpg", "Dark modern facade of the ground-up build at 1855 E Huntingdon Street"),
        "gallery": [
            ("635a04e5a5f14eb8bac5c24e3844729b~mv2.png", "Framed and sheathed structure of 1855 E Huntingdon Street mid-construction"),
            ("1002c95c22bc4664b455e2ae4b82b2c8~mv2.jpg", "Custom black kitchen with island seating"),
            ("1875d5efdb47455ca6782d9962702fac~mv2.jpg", "Open-riser custom stairs beside the living space"),
            ("e150fd19dfa441c69bbf9ec6e180e7f2~mv2.jpg", "Custom bathroom with double vanity"),
            ("feb92d25afb249f09fc7d46aca2861e7~mv2.jpg", "Freestanding tub with matte black fixtures"),
            ("80934035ea134bf9869f5e990e469498~mv2.jpg", "Roof deck with pilot house access"),
        ],
        "narrative": [
            "A ground-up construction for a client, fully customized to their wants and needs — and a true stand-out property in the East Kensington area. This build started as their wish list and ended as their address.",
            "The finish palette runs dark and confident: a custom black kitchen with island seating, bathrooms with double vanities and matte black fixtures, and open-riser stairs that turn circulation into architecture. We framed the structure ourselves — the green-sheathed shell was a neighborhood landmark for a season — so every dimension the finish work depended on was ours to get right.",
            "Building custom for a client is a different discipline from building on spec: every selection is a conversation, and the schedule has to hold anyway. This one did, from foundation to the roof deck.",
        ],
        "todo": "owner to confirm/add real project details — timeline, one client-driven customization story, one challenge solved",
        "similar": ["1502-hancock-street", "2172-firth-street"],
    },
    {
        "slug": "1745-waterloo-street",
        "address": "1745 Waterloo Street",
        "area": "Kensington",
        "area_slug": "east-kensington",
        "type": "Full Build",
        "scope_html": '<a href="/services/kitchen-bathroom-remodeling/">Custom kitchen</a>, <a href="/services/kitchen-bathroom-remodeling/">custom bathrooms</a>, <a href="/services/framing/">custom stairs</a>',
        "hero_img": ("546b1126b7a94ce3a45bc9d0751c0b4e~mv2.jpg", "Custom Dryvit stucco exterior with real wood entry at 1745 Waterloo Street"),
        "gallery": [
            ("717fd78dc4a848d9b25c41d48cdb9158~mv2.jpg", "Custom white kitchen with marble-look counters and gold fixtures"),
            ("f2736598c0454d51888581dbd3c2b51e~mv2.jpg", "Kitchen island with waterfall counter and custom cabinetry"),
            ("663718f7767c4e73ae27f727f621a53a~mv2.png", "Custom open stairs over polished concrete floors"),
            ("2c4a33ffbd854226987f90a4d777fb92~mv2.jpg", "Custom bathroom with double round mirrors and freestanding tub"),
            ("209e74343afe4c188d4acb5640bffa2e~mv2.jpg", "Double-height living space with polished concrete floors"),
            ("689131f1aaab476dbcacb8958ee34853~mv2.jpg", "Roof deck view over the Philadelphia skyline"),
        ],
        "narrative": [
            "A unique gem of a building in the heart of Philadelphia — designed and built completely by B2B2 Builders. The exterior alone breaks the rowhome mold: Dryvit stucco, custom-sized windows, and a real wood custom door and entry facade.",
            "Inside, the customization runs deeper than finishes. Built-in speakers, integrated washer and dryer, polished concrete floors through a double-height living space, custom open stairs, and a white kitchen with waterfall counters and gold hardware. The bathrooms carry the same intent — freestanding tub, double round mirrors, stone-look tile walls.",
            "Waterloo Street is what we point to when a client asks what 'fully custom' means from our crew: a building where the design, the structure, and every interior decision came from one shop.",
        ],
        "todo": "owner to confirm/add real project details — design intent, timeline, one challenge solved (custom window sourcing, concrete floor finishing, etc.)",
        "similar": ["1855-e-huntingdon-street", "766-s-front-street"],
    },
    {
        "slug": "2172-firth-street",
        "address": "2172 Firth Street",
        "area": "Kensington",
        "area_slug": "east-kensington",
        "type": "Property Rehab",
        "scope_html": '<a href="/services/kitchen-bathroom-remodeling/">Custom kitchen</a>, <a href="/services/kitchen-bathroom-remodeling/">custom bathrooms</a>, <a href="/services/framing/">custom stairs</a>',
        "hero_img": ("783e73794a7448b1adedcc422906629d~mv2.jpg", "Distinctive rehabbed facade with garage and wood balcony at 2172 Firth Street"),
        "gallery": [
            ("82514fb7b6834ec19794f4c1b4a1d14a~mv2.jpg", "Front facade with custom garage door and balcony detail"),
            ("b15929ca459d491a98da67cbabf28491~mv2.jpg", "Custom kitchen with black cabinetry against exposed brick"),
            ("8acbed2e08d44ada9f5cbb456b37f989~mv2.jpg", "Custom floating stairs with wood treads"),
            ("bcd4e5eaf94d496a97fc5d6df4ffb0d9~mv2.webp", "Double vanity with brass fixtures in a custom bathroom"),
            ("d7c7d114ef894e8db7a70068f9338245~mv2.jpg", "Rear yard with brick patio after the rehab"),
            ("a711604113b64991b4ddc4a5cc0131ca~mv2.webp", "Living space with exposed brick and new wood flooring"),
        ],
        "narrative": [
            "A property rehab fully designed and built by B2B2 Builders in the Fishtown/Kensington area — with an exterior that stops people on the sidewalk: custom garage door, wood balcony, and a facade that looks nothing like the tired building we started with.",
            "Inside, the rehab kept the best of the original — exposed brick walls — and rebuilt everything around it: a custom black kitchen set against the brick, floating stairs with wood treads, and bathrooms with brass fixtures and double vanities. The mix of preserved texture and new construction is what gives the house its character.",
            "Rehabs like this are equal parts demolition judgment and rebuild discipline: deciding what stays, making what stays sound, and building the new work to a standard the old brick deserves.",
        ],
        "todo": "owner to confirm/add real project details — starting condition, what was preserved vs replaced, one challenge solved",
        "similar": ["3312-salmon-street", "766-s-front-street"],
    },
    {
        "slug": "3312-salmon-street",
        "address": "3312 Salmon Street",
        "area": "Port Richmond",
        "area_slug": "port-richmond",
        "type": "Property Rehab",
        "scope_html": '<a href="/services/kitchen-bathroom-remodeling/">Custom kitchen</a>, <a href="/services/full-builds-remodeling/">addition &amp; facade changes</a>',
        "hero_img": ("af97b51b2a6f4624954588d75d2eba35~mv2.png", "Rehabbed home with addition and new facade at 3312 Salmon Street"),
        "gallery": [
            ("d46a13a2c38340cf93628a4c39b08a69~mv2.png", "Addition under construction at 3312 Salmon Street"),
            ("df8e128588c640d1a7a13feacc9f7233~mv2.png", "Custom white kitchen after the renovation"),
            ("6b5b0190f10f4a4b851874fd67a4af82~mv2.png", "Kitchen island with seating and stainless appliances"),
            ("1eb4126f801b48fd91c0fda6390775ce~mv2.png", "Living space with open stairs and new flooring"),
            ("6087660590c046faaa56e382fcab0984~mv2.png", "Rear deck and outdoor space after the rehab"),
            ("01701671954043e78be252c593ff8f50~mv2.png", "Rear elevation showing the new addition"),
        ],
        "narrative": [
            "This home rehab in Port Richmond was customized with an addition, facade changes, and a full interior renovation — the three biggest moves you can make on an existing rowhome, all on one project.",
            "The addition bought the house the space its layout always wanted, and the interior was rebuilt around it: a custom white kitchen with island seating, open stairs, new flooring throughout, and a rear deck connecting the house to its outdoor space.",
            "Additions on occupied blocks are sequencing work — structure opened, weathered in, and closed without leaving the house exposed. It's the kind of project where having the same crew do the framing, the concrete, and the finishes pays for itself.",
        ],
        "todo": "owner to confirm/add real project details — addition size/purpose, starting condition, one challenge solved",
        "similar": ["2172-firth-street", "3330-38-salmon-street"],
    },
    {
        "slug": "3330-38-salmon-street",
        "address": "3330-38 Salmon Street",
        "area": "Port Richmond",
        "area_slug": "port-richmond",
        "type": "Full Build ×5",
        "scope_html": '<a href="/services/full-builds-remodeling/">Ground-up construction</a>, <a href="/services/kitchen-bathroom-remodeling/">custom kitchens &amp; bathrooms</a>, <a href="/services/concrete/">foundations</a>',
        "hero_img": ("d289858275cc4544a6beae9f3391d807~mv2.jpg", "Row of five colorful new construction homes at 3330-38 Salmon Street"),
        "gallery": [
            ("76efc24b32bc4d3699d32753a1b352b3~mv2.jpg", "Street elevation of the five new homes in Port Richmond"),
            ("2bf6432ff2b043eba179ea774038920d~mv2.jpg", "Facade detail with colored metal panels"),
            ("8cbe01d515744a96b5f90dd0a91f2455~mv2.png", "Custom kitchen with range hood and tile backsplash"),
            ("31048097878349c49a69bf2a34dd4449~mv2.png", "Kitchen island with pendant lighting in one of the five homes"),
            ("71c2355ef9894950a26a51fdf3aa8d6f~mv2.png", "Bathroom with freestanding tub and marble-look tile"),
            ("087e06276d2c4cad8ee6c549f82d847b~mv2.jpg", "Interior with open stairs and natural light"),
        ],
        "narrative": [
            "Fully designed and built by B2B2 Builders, these five homes stand tall among the surrounding blocks of Port Richmond. In a nod to the neighborhood's historic ports, the exteriors carry a unique panelized design — five siblings, not five clones.",
            "Every home got its own custom kitchen, its own bathroom finishes, and its own flooring selections — a deliberate choice to serve five different future owners instead of copy-pasting one spec sheet. The build ran from foundations to final walkthroughs under our single schedule.",
            "Multi-home projects are where a builder's systems show: five foundations, five framing packages, five inspection tracks, one crew keeping them all moving. It remains one of the projects we're proudest of.",
        ],
        "todo": "owner to confirm/add real project details — build timeline, sales outcome, one challenge solved across the five homes",
        "similar": ["3312-salmon-street", "1502-hancock-street"],
    },
    {
        "slug": "766-s-front-street",
        "address": "766 S Front Street",
        "area": "Queen Village",
        "area_slug": "queen-village",
        "type": "Property Rehab",
        "scope_html": '<a href="/services/kitchen-bathroom-remodeling/">Custom kitchen</a>, <a href="/services/full-builds-remodeling/">second-floor addition</a>',
        "hero_img": ("584fb1338625441989e9ff04275078f2~mv2.jpg", "Double-height living space with interior balcony at 766 S Front Street"),
        "gallery": [
            ("d23f00c228b440e990dcc8fc045d2fe9~mv2.jpg", "Green custom kitchen against original brick at 766 S Front Street"),
            ("3f77e04ff7ac411389ee560b4131945b~mv2.jpg", "Living area with exposed structure and garden views"),
            ("218158792e044569acd4170c03cd017df000.jpg", "Green tiled bathroom after the renovation"),
            ("612b24a376a44e90ba3bfb42be6682ba~mv2.jpg", "Sunroom opening to the rear garden"),
            ("871cc8c7ed1b4668b4a1641c661db400~mv2.jpg", "Open living space with new flooring and garden light"),
            ("61c6bcd72bfa44d39ad90c800ca5bd0d~mv2.jpg", "Mosaic wall detail preserved in the renovation"),
        ],
        "narrative": [
            "A beautiful client rehab two blocks off the Delaware in Queen Village, with a second-floor extension constructed above the original footprint. The interior was fully renovated to the client's taste and choice — and their taste was worth building.",
            "The house is anything but standard: a double-height living space with an interior balcony, a green custom kitchen set against original brick, a green-tiled bath, and a sunroom opening to the rear garden. Even a mosaic wall was kept and worked around rather than demolished — in a neighborhood this old, character is the asset.",
            "Additions in Queen Village mean building new structure onto very old structure, and making the seam invisible. That seam — where 200-year-old bones meet new framing — is where this project earned its keep.",
        ],
        "todo": "owner to confirm/add real project details — what the extension added, starting condition, one challenge solved joining old and new structure",
        "similar": ["2172-firth-street", "1745-waterloo-street"],
    },
]

BY_SLUG = {p["slug"]: p for p in PROJECTS}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{address} — {type} in {area} | B2B2 Builders</title>
  <meta name="description" content="{meta_desc}">
  <!-- TODO: replace placeholder domain before launch -->
  <link rel="canonical" href="https://b2b2builders.com/projects/{slug}/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{address} — {type} in {area} | B2B2 Builders">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="https://b2b2builders.com/projects/{slug}/">
  <meta property="og:image" content="{hero_url}">
  <meta name="twitter:card" content="summary_large_image">
<!-- HEAD-COMMON-START -->
<!-- HEAD-COMMON-END -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://b2b2builders.com/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Projects", "item": "https://b2b2builders.com/projects/" }},
      {{ "@type": "ListItem", "position": 3, "name": "{address}", "item": "https://b2b2builders.com/projects/{slug}/" }}
    ]
  }}
  </script>
</head>
<body>
<!-- SITE-HEADER-START -->
<!-- SITE-HEADER-END -->

  <main id="main">
    <section class="page-hero">
      <div class="container">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li><a href="/projects/">Projects</a></li>
            <li><span aria-current="page">{address}</span></li>
          </ol>
        </nav>
        <p class="eyebrow">[ {type} ]</p>
        <h1>{address}, <em class="accent">{area}</em>.</h1>
        <dl class="project-meta" style="max-width: 640px; margin-top: 2rem;">
          <div><dt>Neighborhood</dt><dd><a href="/service-areas/{area_slug}/">{area}</a></dd></div>
          <div><dt>Project type</dt><dd>{type}</dd></div>
          <div><dt>Scope</dt><dd>{scope_html}</dd></div>
        </dl>
      </div>
    </section>

    <section class="section" style="padding-top: 0;">
      <div class="container">
        <!-- TODO: real photos — self-host and optimize before launch; currently hot-linked from the existing Wix site -->
        <div class="gallery-grid" data-reveal>
          <img src="{hero_url}" alt="{hero_alt}" width="1200" height="600" loading="lazy">
{gallery_imgs}        </div>
      </div>
    </section>

    <section class="section" style="padding-top: 0;">
      <div class="container">
        <div class="prose" data-reveal>
          <h2>About This Project</h2>
          <!-- TODO: {todo} -->
{narrative}          <p>This project sits in {area} — see everything we build there on our <a href="/service-areas/{area_slug}/">{area} service area page</a>, or start your own project with a <a href="/contact/">free estimate</a>.</p>
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
{similar_cards}        </ul>
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
"""

for p in PROJECTS:
    hero_url = WIX + p["hero_img"][0]
    gallery_imgs = ""
    for fname, alt in p["gallery"]:
        gallery_imgs += f'          <img src="{WIX}{fname}" alt="{alt}" width="600" height="450" loading="lazy">\n'
    narrative = ""
    for para in p["narrative"]:
        clean = " ".join(para.split())
        narrative += f"          <p>{clean}</p>\n"
    similar_cards = ""
    for slug in p["similar"]:
        s = BY_SLUG[slug]
        s_url = WIX + s["hero_img"][0]
        similar_cards += f"""          <li class="hub-card" data-reveal>
            <img src="{s_url}" alt="{s['hero_img'][1]}" width="480" height="300" loading="lazy">
            <div class="hub-card-body">
              <span class="hub-card-tag">{s['type']} · {s['area']}</span>
              <h3><a href="/projects/{s['slug']}/">{s['address']}</a></h3>
              <a class="text-link" href="/projects/{s['slug']}/">View the {s['address']} project <span aria-hidden="true">→</span></a>
            </div>
          </li>
"""
    meta_desc = f"{p['address']} in {p['area']}, Philadelphia — a {p['type'].lower()} by B2B2 Builders. See the photos, scope, and story behind this project."
    html = TEMPLATE.format(
        address=p["address"], area=p["area"], area_slug=p["area_slug"], type=p["type"],
        slug=p["slug"], scope_html=p["scope_html"], hero_url=hero_url,
        hero_alt=p["hero_img"][1], gallery_imgs=gallery_imgs, narrative=narrative,
        similar_cards=similar_cards, todo=p["todo"], meta_desc=meta_desc,
    )
    out = ROOT / "projects" / p["slug"] / "index.html"
    out.write_text(html)
    print("wrote", out.relative_to(ROOT))
