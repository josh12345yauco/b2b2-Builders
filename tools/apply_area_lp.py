#!/usr/bin/env python3
"""Authoring tool — applies the Fishtown-style landing page template to the
other six service-area pages: dark slideshow hero + lead form, fact nuggets,
builder promo strip, cost FAQ, and builder-focused CTA. Run once; output is
committed static HTML. Re-running is not idempotent — edit pages directly after.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIX = "https://static.wixstatic.com/media/dc69ab_"
IMG = "/Images/"

AREAS = [
    {
        "slug": "northern-liberties",
        "name": "Northern Liberties",
        "h1": 'General Contractor in <em class="accent">Northern Liberties</em>.',
        "sub": "Townhomes, converted lofts, and roof decks — a neighborhood where building well means handling the construction and the coordination: HOAs, COIs, and streets never designed for a lumber delivery.",
        "zip": "19123",
        "slides": [
            (WIX + "58a09638df8844398aef21b5015379da~mv2.png", 940),
            (WIX + "717fd78dc4a848d9b25c41d48cdb9158~mv2.jpg", 1067),
            (IMG + "vecteezy_white-and-wooden-bathroom-interior-design_23826214.jpg", 1067),
        ],
        "bullets": [
            ("shield", '<strong>Licensed &amp; insured</strong> — PA HIC #PA045678, with COIs ready before your association asks'),
            ("pin", '<strong>Ten minutes from our HQ</strong> — straight down Frankford Ave from 3146 Frankford'),
            ("doc", '<strong>Itemized free estimates</strong> — real numbers in writing, usually within 24 hours of the walkthrough'),
            ("person", '<strong>Owner on every project</strong> — see the finish level at <a href="/projects/luxury-townhome-kensington/">our custom build on Waterloo Street</a>'),
        ],
        "stats": [
            ("The townhome vintage we remodel most", "2000s"),
            ("Northern Liberties' ZIP, minutes from our HQ", "19123"),
            ("HOA paperwork ready at the proposal stage", "COI"),
            ("Jobs we'll run without an L&amp;I permit", "0"),
        ],
        "fact": "Fact worth knowing: most Northern Liberties associations require a certificate of insurance and an approved scope before any contractor starts — we prepare that package at the proposal stage so board approval never delays your start date.",
        "cost_q": "How much does a townhome remodel cost in Northern Liberties?",
        "cost_a": "Most Northern Liberties kitchen and bathroom remodels land between $25,000 and $60,000, whole-home refreshes of boom-era townhomes typically run $80,000 to $200,000, and roof deck rebuilds usually start around $20,000. Every estimate is free, itemized, and based on walking your actual home.",
    },
    {
        "slug": "east-kensington",
        "name": "East Kensington",
        "h1": 'General Contractor in <em class="accent">East Kensington</em>.',
        "sub": "Shells, long-vacant rowhomes, and empty lots turning back into homes. This is where we do our heaviest lifting — full systems replacement isn't the exception in East Kensington, it's the job description.",
        "zip": "19125",
        "slides": [
            (WIX + "f0f2c5b4b264485cb8651cadbb1cd684~mv2.jpg", 1067),
            (WIX + "1002c95c22bc4664b455e2ae4b82b2c8~mv2.jpg", 1067),
            (WIX + "635a04e5a5f14eb8bac5c24e3844729b~mv2.png", 940),
        ],
        "bullets": [
            ("shield", '<strong>Licensed &amp; insured</strong> — PA HIC #PA045678, Philadelphia L&amp;I permits pulled on every job'),
            ("pin", '<strong>We build on these blocks</strong> — ground-up at <a href="/projects/modern-custom-home-east-kensington/">Modern Custom Home</a>'),
            ("doc", '<strong>Itemized free estimates</strong> — shell rehabs priced with realistic allowances, not blank checks'),
            ("person", '<strong>Owner on every project</strong> — investor rehabs and family homes get the same site discipline'),
        ],
        "stats": [
            ("Ground-up builds on these blocks", "2"),
            ("Shell rehabs where we replace all systems", "100%"),
            ("The ZIP we share with our Frankford Ave HQ", "19125"),
            ("Jobs we'll run without an L&amp;I permit", "0"),
        ],
        "fact": "Fact worth knowing: East Kensington's brick shells are usually worth saving even after a decade of vacancy — the play is structure first, then all-new electric, plumbing, and HVAC inside the repaired shell. We'll tell you plainly when a building is a teardown instead.",
        "cost_q": "How much does it cost to renovate a shell in East Kensington?",
        "cost_a": "A full shell rehab with complete systems replacement typically runs $150,000 to $300,000 depending on size and structure, and standalone kitchens land between $25,000 and $60,000. Every estimate is free, itemized, and priced from walking the actual building — with allowances for what vacancy usually hides.",
    },
    {
        "slug": "port-richmond",
        "name": "Port Richmond",
        "h1": 'General Contractor in <em class="accent">Port Richmond</em>.',
        "sub": "Solid workers' rowhomes with good bones, and river-side blocks where new construction is filling in. We've built five new homes here and updated plenty of old ones — both kinds of work, done with respect for the block.",
        "zip": "19134",
        "slides": [
            (WIX + "d289858275cc4544a6beae9f3391d807~mv2.jpg", 1067),
            (WIX + "df8e128588c640d1a7a13feacc9f7233~mv2.png", 940),
            (WIX + "8cbe01d515744a96b5f90dd0a91f2455~mv2.png", 940),
        ],
        "bullets": [
            ("shield", '<strong>Licensed &amp; insured</strong> — PA HIC #PA045678, Philadelphia L&amp;I permits pulled on every job'),
            ("pin", '<strong>Our home ZIP</strong> — headquarters at 3146 Frankford Ave, minutes down the avenue'),
            ("doc", '<strong>Itemized free estimates</strong> — real numbers in writing, usually within 24 hours of the walkthrough'),
            ("person", '<strong>We built five homes here</strong> — see <a href="/projects/new-construction-port-richmond/">Five New Construction Homes</a>'),
        ],
        "stats": [
            ("New homes we built on Salmon Street alone", "5"),
            ("Our home ZIP — HQ at 3146 Frankford Ave", "19134"),
            ("Generations often under one rowhome roof here", "3"),
            ("Jobs we'll run without an L&amp;I permit", "0"),
        ],
        "fact": "Fact worth knowing: Philadelphia holds property owners responsible for their own sidewalks — and Port Richmond's heaved slabs are freeze-thaw damage. That's why our exterior concrete is always air-entrained mix on a properly compacted base, not just poured and hoped for.",
        "cost_q": "How much does a rowhome update cost in Port Richmond?",
        "cost_a": "Most Port Richmond kitchen remodels land between $25,000 and $60,000, bathrooms between $15,000 and $35,000, and a full gut renovation typically runs $150,000 to $300,000. Every estimate is free, itemized line by line, and priced from walking your actual house.",
    },
    {
        "slug": "queen-village",
        "name": "Queen Village",
        "h1": 'General Contractor in <em class="accent">Queen Village</em>.',
        "sub": "Some of the oldest housing stock in Philadelphia — which means some of the most demanding renovation work in the city. In Queen Village, craftsmanship isn't a selling point; it's the entry fee.",
        "zip": "19147",
        "slides": [
            (WIX + "584fb1338625441989e9ff04275078f2~mv2.jpg", 1067),
            (WIX + "d23f00c228b440e990dcc8fc045d2fe9~mv2.jpg", 1067),
            (WIX + "612b24a376a44e90ba3bfb42be6682ba~mv2.jpg", 1067),
        ],
        "bullets": [
            ("shield", '<strong>Licensed &amp; insured</strong> — PA HIC #PA045678, with historic-review experience where blocks require it'),
            ("pin", '<strong>We build here</strong> — our rehab with addition at <a href="/projects/property-rehab-queen-village/">Property Rehab &amp; Addition</a> is two blocks off the Delaware'),
            ("doc", '<strong>Itemized free estimates</strong> — old-house allowances priced honestly, not discovered later'),
            ("person", '<strong>Owner on every project</strong> — 200-year-old structures get the patience they demand'),
        ],
        "stats": [
            ("Age of the neighborhood's oldest housing stock", "200+ yrs"),
            ("The ZIP we serve, river to Passyunk", "19147"),
            ("Blocks off the Delaware — our rehab with a second-floor addition", "2"),
            ("Jobs we'll run without an L&amp;I permit", "0"),
        ],
        "fact": "Fact worth knowing: parts of Queen Village sit under historic-district review, where exterior changes need commission approval before L&I issues permits. We confirm your block's status at the estimate stage — before design gets ahead of approvals.",
        "cost_q": "How much does it cost to renovate a historic Queen Village home?",
        "cost_a": "Kitchens and bathrooms in Queen Village typically land between $30,000 and $70,000 — older structures trend higher than newer rowhomes — and whole-home renovations of historic houses usually run $200,000 to $400,000. Every estimate is free, itemized, and priced from walking the actual building.",
    },
    {
        "slug": "center-city",
        "name": "Center City",
        "h1": 'General Contractor in <em class="accent">Center City</em>.',
        "sub": "Condo and high-rise interior renovations, done by the book — because in a managed building, \"by the book\" is the only way work actually happens on schedule.",
        "zip": "19102",
        "slides": [
            (IMG + "vecteezy_modern-kitchen-with-wooden-cabinets-and-stainless-steel_74135527.jpeg", 940),
            (IMG + "vecteezy_white-and-wooden-bathroom-interior-design_23826214.jpg", 1067),
            (WIX + "717fd78dc4a848d9b25c41d48cdb9158~mv2.jpg", 1067),
        ],
        "bullets": [
            ("shield", '<strong>Licensed &amp; insured</strong> — COIs naming your association, ready before the management office asks'),
            ("pin", '<strong>Building paperwork handled</strong> — alteration agreements, elevator bookings, quiet-hours scheduling'),
            ("doc", '<strong>Itemized free estimates</strong> — real numbers in writing, usually within 24 hours of the walkthrough'),
            ("person", '<strong>Premium finish level</strong> — the standard from <a href="/projects/luxury-townhome-kensington/">our custom build on Waterloo Street</a>, brought upstairs'),
        ],
        "stats": [
            ("Insurance certificates ready before your building asks", "COI"),
            ("The ZIPs we work most downtown", "19102–03"),
            ("Realistic tower timeline for a 4-week rowhome job", "6 wks"),
            ("Jobs we'll run without a permit", "0"),
        ],
        "fact": "Fact worth knowing: in most Center City towers the freight elevator — not the crew — sets the pace. We pre-stage materials so every booked slot moves a full load, which is how a quoted schedule actually holds in a high-rise.",
        "cost_q": "How much does a condo renovation cost in Center City?",
        "cost_a": "Center City bathroom remodels typically land between $25,000 and $50,000, kitchens between $40,000 and $80,000, and full-unit renovations usually run $100,000 to $250,000 depending on finish level and what the building allows. Every estimate is free, itemized, and includes the building-coordination work in writing.",
    },
    {
        "slug": "montgomery-county",
        "name": "Montgomery County",
        "h1": 'General Contractor in <em class="accent">Montgomery County</em>.',
        "sub": "Ambler, Blue Bell, and Conshohocken — where the rowhome rules stop applying. Detached homes and twins, real lots, additions with actual footprints, and permits that run through townships instead of L&amp;I.",
        "zip": "19002",
        "slides": [
            (IMG + "vecteezy_modern-home-interior-design-with-wooden-flooring-and_24573293.jpg", 1140),
            (IMG + "vecteezy_modern-kitchen-with-wooden-cabinets-and-stainless-steel_74135527.jpeg", 940),
            (IMG + "vecteezy_white-and-wooden-bathroom-interior-design_23826214.jpg", 1067),
        ],
        "bullets": [
            ("shield", '<strong>Licensed &amp; insured</strong> — PA HIC #PA045678, permitted through your borough or township'),
            ("pin", '<strong>Township permitting handled</strong> — Ambler borough, Whitpain, Whitemarsh, and neighbors'),
            ("doc", '<strong>Itemized free estimates</strong> — real numbers in writing, usually within 24 hours of the walkthrough'),
            ("person", '<strong>Full-build proof</strong> — we ran <a href="/projects/new-construction-port-richmond/">five ground-up homes on one street</a> end to end'),
        ],
        "stats": [
            ("Boroughs &amp; townships we permit in most", "3+"),
            ("Ambler's ZIP — the heart of our suburban coverage", "19002"),
            ("Sides of access we finally get around a detached house", "4"),
            ("Jobs we'll run without a township permit", "0"),
        ],
        "fact": "Fact worth knowing: there's no L&I out here — Ambler is its own borough permit office, Blue Bell runs through Whitpain Township, and Conshohocken borders two more townships. Knowing whose counter you're standing at is half the schedule.",
        "cost_q": "How much does a home addition cost in Montgomery County?",
        "cost_a": "Additions in Ambler, Blue Bell, and Conshohocken typically run $150 to $300 per square foot depending on scope and finishes, and kitchen remodels land between $30,000 and $75,000. Every estimate is free, itemized, and includes the township permit path in the schedule.",
    },
]

ICONS = {
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 3v6c0 4.5-3.2 7.8-8 9-4.8-1.2-8-4.5-8-9V6l8-3z"/><path d="m9 12 2 2 4-4"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18"/><path d="M8 15h5"/></svg>',
    "person": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 21a8 8 0 0 0-16 0"/><circle cx="12" cy="9" r="4"/></svg>',
}


def build_hero(a):
    slides = ""
    for i, (src, h) in enumerate(a["slides"]):
        extra = ' fetchpriority="high"' if i == 0 else ' loading="lazy"'
        slides += f'        <img class="hero-slide" src="{src}" alt="" width="1600" height="{h}"{extra}>\n'
    bullets = ""
    for icon, text in a["bullets"]:
        bullets += f"""              <li>
                {ICONS[icon]}
                <span>{text}</span>
              </li>
"""
    stats = ""
    for label, value in a["stats"]:
        stats += f'          <div class="stat"><dt>{label}</dt><dd>{value}</dd></div>\n'
    return f"""    <!-- Split hero: auto-cycling background, pitch left, lead form right -->
    <section class="lp-hero lp-hero-dark">
      <div class="hero-slides" aria-hidden="true">
        <!-- TODO: optimize/compress hero images before launch (serve ~1600px webp); self-host any wixstatic images -->
{slides}      </div>
      <div class="hero-overlay" aria-hidden="true"></div>
      <div class="container">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li><a href="/service-areas/">Service Areas</a></li>
            <li><span aria-current="page">{a["name"]}</span></li>
          </ol>
        </nav>
        <div class="lp-hero-grid">
          <div>
            <p class="eyebrow">[ {a["name"]} General Contractor ]</p>
            <h1>{a["h1"]}</h1>
            <p class="page-hero-sub">{a["sub"]}</p>
            <ul class="lp-bullets">
{bullets}            </ul>
            <div class="lp-hero-cta-row">
              <a class="btn btn-primary btn-lg" href="/#project-builder">Price Your Project in 60 Seconds</a>
              <a class="nav-phone" href="tel:+12158884384" style="font-weight: 700;">or call 215-888-4384</a>
            </div>
          </div>

          <!-- Lead form -->
          <form class="builder lead-card" id="area-lead-form" data-area="{a["name"]}" novalidate>
            <h2>Get Your Free {a["name"]} Estimate</h2>
            <p class="lead-card-sub">Tell us the basics — we'll call you back within one business day with next steps and a walkthrough time.</p>
            <div class="field-row" style="margin-top: 1.25rem;">
              <div class="field">
                <label for="lf-name">Name</label>
                <input type="text" id="lf-name" name="name" autocomplete="name" required>
              </div>
              <div class="field">
                <label for="lf-phone">Phone</label>
                <input type="tel" id="lf-phone" name="phone" autocomplete="tel" required>
              </div>
            </div>
            <div class="field-row">
              <div class="field">
                <label for="lf-type">Project type</label>
                <select id="lf-type" name="projectType">
                  <option>Kitchen</option>
                  <option>Bathroom</option>
                  <option>Full Build / Remodel</option>
                  <option>Addition / Roof Deck</option>
                  <option>Concrete</option>
                  <option>Framing / Structural</option>
                  <option>Something else</option>
                </select>
              </div>
              <div class="field">
                <label for="lf-zip">ZIP code</label>
                <input type="text" id="lf-zip" name="zip" inputmode="numeric" autocomplete="postal-code" placeholder="{a["zip"]}" required>
              </div>
            </div>
            <div class="field-row">
              <div class="field">
                <label for="lf-budget">Budget range</label>
                <select id="lf-budget" name="budget">
                  <option>Not sure yet</option>
                  <option>Under $25k</option>
                  <option>$25k–$75k</option>
                  <option>$75k–$150k</option>
                  <option>$150k+</option>
                </select>
              </div>
              <div class="field">
                <label for="lf-timeline">How soon?</label>
                <select id="lf-timeline" name="timeline">
                  <option>ASAP</option>
                  <option>1–3 months</option>
                  <option>3–6 months</option>
                  <option>Just planning</option>
                </select>
              </div>
            </div>
            <div class="field">
              <label for="lf-notes">Anything we should know?</label>
              <textarea id="lf-notes" name="notes" style="min-height: 90px;" placeholder="Street, current condition, what you want done…"></textarea>
            </div>
            <p class="builder-error" hidden>Add your name, phone, and ZIP so we can reach you.</p>
            <div class="builder-controls">
              <button type="submit" class="btn btn-primary btn-lg">Get My Free Estimate</button>
            </div>
            <div class="form-success" hidden>
              <p>Got it — we'll reach out within one business day. Or call us now: <a href="tel:+12158884384"><strong>215-888-4384</strong></a></p>
            </div>
            <p class="lead-card-alt">Prefer a faster answer? <a href="/#project-builder"><strong>Price your project in 60 seconds →</strong></a></p>
          </form>
        </div>
      </div>
    </section>

    <!-- Fact nuggets -->
    <section class="section" style="padding-top: 0;">
      <div class="container">
        <div class="section-head" data-reveal>
          <div>
            <p class="eyebrow">[ {a["name"]}, By the Numbers ]</p>
            <h2>We Know This Territory Cold<em class="accent">.</em></h2>
          </div>
        </div>
        <!-- TODO: verify each fact claim with owner before launch -->
        <dl class="numbers-stats" data-reveal>
{stats}        </dl>
        <p class="fact-note" data-reveal>{a["fact"]} <!-- TODO: verify with owner --></p>
      </div>
    </section>
"""


PROMO = """    <!-- Project Builder promo strip -->
    <section class="section" style="padding-top: 0;">
      <div class="container">
        <div class="builder-promo" data-reveal>
          <div>
            <h2>Price Your {name} Project in 60 Seconds.</h2>
            <p>Four quick questions, no obligation — the fastest way to get a real ballpark before we ever visit.</p>
          </div>
          <div class="builder-promo-actions">
            <a class="btn btn-primary btn-lg" href="/#project-builder">Open the Project Builder</a>
            <a class="btn btn-ghost btn-lg" href="tel:+12158884384">Call 215-888-4384</a>
          </div>
        </div>
      </div>
    </section>

"""

for a in AREAS:
    path = ROOT / "service-areas" / a["slug"] / "index.html"
    h = path.read_text()

    # 1. Replace the old hero with the dark slideshow hero + fact nuggets
    h, n = re.subn(r'    <section class="page-hero">.*?</section>\n', build_hero(a), h, count=1, flags=re.S)
    assert n == 1, f"hero not replaced in {a['slug']}"

    # 2. Split the prose at "Services in X" and slot the builder promo between:
    #    close the local-knowledge section, insert promo, reopen a section.
    splice = (
        "        </div>\n"
        "      </div>\n"
        "    </section>\n\n"
        + PROMO.replace("{name}", a["name"])
        + '    <section class="section" style="padding-top: 0;">\n'
        '      <div class="container">\n'
        '        <div class="prose" data-reveal>\n'
        "          <h2>Services in "
    )
    h, n = re.subn(r"\n          <h2>Services in ", "\n" + splice, h, count=1)
    assert n == 1, f"promo not inserted in {a['slug']}"

    # 3. Prepend cost FAQ to the visible accordion
    cost_details = f"""          <details class="faq-item">
            <summary><h3>{a["cost_q"]}</h3><span class="faq-icon" aria-hidden="true"></span></summary>
            <!-- TODO: FILLER ranges — confirm real numbers with owner before launch -->
            <div class="faq-answer"><p>{a["cost_a"]}</p></div>
          </details>
"""
    h, n = re.subn(r'(        <div class="faq-list" data-reveal>\n)', r"\1" + cost_details, h, count=1)
    assert n == 1, f"faq not inserted in {a['slug']}"

    # 4. Mirror the cost FAQ in the FAQPage JSON-LD (strip HTML entities for JSON)
    q_json = json.dumps(a["cost_q"].replace("&amp;", "&"))
    a_json = json.dumps(a["cost_a"].replace("&amp;", "&"))
    new_entity = f'{{ "@type": "Question", "name": {q_json}, "acceptedAnswer": {{ "@type": "Answer", "text": {a_json} }} }},\n      '
    h, n = re.subn(r'("mainEntity": \[\n)(      )', r"\1\2" + new_entity.replace("\\", "\\\\"), h, count=1)
    assert n == 1, f"schema not updated in {a['slug']}"

    # 5. Point the final CTA orange button at the Project Builder
    h = h.replace(
        '<a class="btn btn-orange btn-lg" href="/contact/">Get a Free Estimate</a>',
        '<a class="btn btn-orange btn-lg" href="/#project-builder">Price Your Project in 60 Seconds</a>',
    )

    path.write_text(h)
    print("applied:", a["slug"])
