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


PROJECTS = [
    # ================= FULL PROJECTS =================
    {
        "slug": "custom-home-build-fishtown",
        "title": "Custom Home Build",
        "area": "Fishtown",
        "area_slug": "fishtown",
        "type": "Full Build",
        "categories": ["full-build", "kitchen", "bathroom"],
        "card_blurb": "Large ground-up build — custom kitchen, custom bathrooms, custom stairs.",
        "card_variants": {
            "kitchen": ("https://static.wixstatic.com/media/dc69ab_3ff41089664044d0b53d9e33a20258b8~mv2.png", "Custom white kitchen with island and stainless appliances"),
            "bathroom": ("https://static.wixstatic.com/media/dc69ab_602d411d7b4c4b8cb1a2966014cab539~mv2.png", "Custom bathroom with freestanding tub"),
        },
        "scope_html": f'{SVC["kitchen"]}, {SVC["bathrooms"]}, {SVC["stairs"]}',
        "hero_img": ("https://static.wixstatic.com/media/dc69ab_58a09638df8844398aef21b5015379da~mv2.png", "Street view of a completed custom home build in Fishtown"),
        "gallery": [
            ("https://static.wixstatic.com/media/dc69ab_e84e9c093ada4984a8384c1e2abda728~mv2.png", "Open living space with custom stairs in the Fishtown custom home"),
            ("https://static.wixstatic.com/media/dc69ab_3ff41089664044d0b53d9e33a20258b8~mv2.png", "Custom white kitchen with island and stainless appliances"),
            ("https://static.wixstatic.com/media/dc69ab_e74a63f2dd9840cda488bc6dbdd96786~mv2.png", "Kitchen with custom cabinetry and pendant lighting"),
            ("https://static.wixstatic.com/media/dc69ab_602d411d7b4c4b8cb1a2966014cab539~mv2.png", "Custom bathroom with freestanding tub"),
            ("https://static.wixstatic.com/media/dc69ab_4700d96463914c44a1912149f4924ad3~mv2.png", "Glass-enclosed tiled shower in a custom bathroom"),
            ("https://static.wixstatic.com/media/dc69ab_5dc3f24376c34e6e8dd8e05c64067ba0~mv2.png", "Facade detail of the Fishtown new construction"),
        ],
        "narrative": [
            "A large project constructed on one of the busiest corridors in Fishtown — the kind of block where the neighborhood watches a build go up in real time. We built this custom home from the ground up: structure, systems, and every finish inside.",
            "The interior program was custom throughout — a custom kitchen with a full island, custom bathrooms including a freestanding tub and glass-enclosed shower, and stairs our carpenters built on site rather than ordering from a catalog. Open living spaces put the stair work on display, so there was nowhere for sloppy carpentry to hide.",
            "Fishtown full builds run through Philadelphia L&I permitting with inspections at every phase, and this one passed them on schedule. It now stands as our calling card in the neighborhood where we're headquartered.",
        ],
        "todo": "owner to confirm/add real project details — starting condition of the lot, program (units/floors), one challenge solved during the build. Wix images still hot-linked — self-host before launch.",
        "similar": ["modern-custom-home-east-kensington", "luxury-townhome-kensington"],
    },
    {
        "slug": "modern-custom-home-east-kensington",
        "title": "Modern Custom Home",
        "area": "East Kensington",
        "area_slug": "east-kensington",
        "type": "Full Build",
        "categories": ["full-build", "kitchen", "bathroom"],
        "card_blurb": "Ground-up custom construction — black-and-white kitchen, spa master bath, wet bar.",
        "card_variants": {
            "bathroom": img("modern-custom-home-east-kensington", "master-bath-freestanding-tub", "Spa master bathroom with freestanding tub and glass shower"),
        },
        "scope_html": f'{SVC["kitchen"]}, {SVC["bathrooms"]}, {SVC["stairs"]}',
        "hero_img": img("modern-custom-home-east-kensington", "kitchen-waterfall-island-wide", "Black-and-white custom kitchen with waterfall quartz island in East Kensington"),
        "gallery": [
            img("modern-custom-home-east-kensington", "black-white-kitchen-island", "Matte black kitchen cabinets with waterfall quartz island and bar seating"),
            img("modern-custom-home-east-kensington", "wet-bar-wine-fridge", "Custom wet bar with quartz counter and dual-zone wine fridge"),
            img("modern-custom-home-east-kensington", "master-bath-freestanding-tub", "Spa master bathroom with freestanding tub and glass shower"),
            img("modern-custom-home-east-kensington", "master-bath-glass-shower", "Glass slider shower and black floor-mounted tub filler in the master bath"),
            img("modern-custom-home-east-kensington", "double-vanity-led-mirror", "Marble-top double vanity with LED mirror"),
            img("modern-custom-home-east-kensington", "shower-bench-black-fixtures", "Glass-enclosed shower with bench and matte black rain fixtures"),
            img("modern-custom-home-east-kensington", "soaking-tub-window", "Freestanding soaking tub under a bright window"),
            img("modern-custom-home-east-kensington", "powder-room-geometric-tile", "Powder room with matte black toilet and geometric starburst tile floor"),
        ],
        "narrative": [
            "A ground-up construction for a client, fully customized to their wants and needs — and a true stand-out property in the East Kensington area. This build started as their wish list and ended as their address.",
            "The finish palette runs dark and confident: a black-and-white custom kitchen with a waterfall quartz island and bar seating, a wet bar with a dual-zone wine fridge, and a spa-grade master bath — freestanding soaking tub, glass shower with bench, marble-top double vanity, matte black fixtures throughout. Even the powder room got a statement geometric tile floor.",
            "Building custom for a client is a different discipline from building on spec: every selection is a conversation, and the schedule has to hold anyway. This one did, from foundation to the roof deck.",
        ],
        "todo": "owner to confirm/add real project details — timeline, one client-driven customization story, one challenge solved",
        "similar": ["custom-home-build-fishtown", "spa-master-bathroom-east-kensington"],
    },
    {
        "slug": "luxury-townhome-kensington",
        "title": "Luxury Custom Townhome",
        "area": "Kensington",
        "area_slug": "east-kensington",
        "type": "Full Build",
        "categories": ["full-build", "kitchen", "bathroom"],
        "card_blurb": "A unique gem designed and built completely by our crew — down to the built-in speakers.",
        "card_variants": {
            "bathroom": img("luxury-townhome-kensington", "master-bath-marble-wall", "Master bath with marble feature wall and freestanding tub"),
        },
        "scope_html": f'{SVC["kitchen"]}, {SVC["bathrooms"]}, {SVC["stairs"]}',
        "hero_img": img("luxury-townhome-kensington", "luxury-kitchen-waterfall-island", "Luxury white kitchen with waterfall quartz island and brass globe chandelier"),
        "gallery": [
            img("luxury-townhome-kensington", "modern-stucco-facade", "Modern stucco townhome facade with round windows and wood-slat balcony"),
            img("luxury-townhome-kensington", "kitchen-floating-staircase", "Kitchen island with brass faucet beside the floating steel-and-wood staircase"),
            img("luxury-townhome-kensington", "kitchen-skylight-fireplace", "Open kitchen and stairwell under a skylight with double-sided fireplace"),
            img("luxury-townhome-kensington", "master-bath-marble-wall", "Master bath with marble feature wall, freestanding tub, and curbless shower"),
            img("luxury-townhome-kensington", "master-bath-double-vanity", "Floating double vanity with round LED mirrors in the master bath"),
            img("luxury-townhome-kensington", "marble-shower-brass-fixtures", "Marble shower wall with brass rain heads and marble bench"),
            img("luxury-townhome-kensington", "guest-bath-herringbone-tile", "Guest bath with herringbone tile tub surround, round window, and walnut vanity"),
            img("luxury-townhome-kensington", "walnut-floating-vanity", "Walnut floating vanity with LED mirror in the guest bath"),
        ],
        "narrative": [
            "A unique gem of a building in the heart of Philadelphia — designed and built completely by B2B2 Builders. The exterior alone breaks the rowhome mold: custom stucco, round porthole windows, a wood-slat balcony, and a real wood entry.",
            "Inside, the customization runs deeper than finishes. A floating steel-and-wood staircase climbs under a skylight, a white kitchen with waterfall quartz island carries brass hardware and a globe chandelier, and the master bath pairs a marble feature wall with a freestanding tub, curbless shower, and brass fittings. Built-in speakers and integrated appliances round out the spec.",
            "This townhome is what we point to when a client asks what 'fully custom' means from our crew: a building where the design, the structure, and every interior decision came from one shop.",
        ],
        "todo": "owner to confirm/add real project details — design intent, timeline, one challenge solved",
        "similar": ["modern-custom-home-east-kensington", "marble-brass-bathrooms-philadelphia"],
    },
    {
        "slug": "rowhome-rehab-kensington",
        "title": "Signature Rowhome Rehab",
        "area": "Kensington",
        "area_slug": "east-kensington",
        "type": "Property Rehab",
        "categories": ["property-rehab", "kitchen", "bathroom"],
        "card_blurb": "Full rehab with a stand-out exterior — custom kitchen, baths, and stairs inside.",
        "card_variants": {
            "kitchen": ("https://static.wixstatic.com/media/dc69ab_b15929ca459d491a98da67cbabf28491~mv2.jpg", "Custom kitchen with black cabinetry against exposed brick"),
            "bathroom": ("https://static.wixstatic.com/media/dc69ab_bcd4e5eaf94d496a97fc5d6df4ffb0d9~mv2.webp", "Double vanity with brass fixtures in a custom bathroom"),
        },
        "scope_html": f'{SVC["kitchen"]}, {SVC["bathrooms"]}, {SVC["stairs"]}',
        "hero_img": ("https://static.wixstatic.com/media/dc69ab_783e73794a7448b1adedcc422906629d~mv2.jpg", "Distinctive rehabbed rowhome facade with garage and wood balcony in Kensington"),
        "gallery": [
            ("https://static.wixstatic.com/media/dc69ab_82514fb7b6834ec19794f4c1b4a1d14a~mv2.jpg", "Front facade with custom garage door and balcony detail"),
            ("https://static.wixstatic.com/media/dc69ab_b15929ca459d491a98da67cbabf28491~mv2.jpg", "Custom kitchen with black cabinetry against exposed brick"),
            ("https://static.wixstatic.com/media/dc69ab_8acbed2e08d44ada9f5cbb456b37f989~mv2.jpg", "Custom floating stairs with wood treads"),
            ("https://static.wixstatic.com/media/dc69ab_bcd4e5eaf94d496a97fc5d6df4ffb0d9~mv2.webp", "Double vanity with brass fixtures in a custom bathroom"),
            ("https://static.wixstatic.com/media/dc69ab_d7c7d114ef894e8db7a70068f9338245~mv2.jpg", "Rear yard with brick patio after the rehab"),
            ("https://static.wixstatic.com/media/dc69ab_a711604113b64991b4ddc4a5cc0131ca~mv2.webp", "Living space with exposed brick and new wood flooring"),
        ],
        "narrative": [
            "A property rehab fully designed and built by B2B2 Builders in the Fishtown/Kensington area — with an exterior that stops people on the sidewalk: custom garage door, wood balcony, and a facade that looks nothing like the tired building we started with.",
            "Inside, the rehab kept the best of the original — exposed brick walls — and rebuilt everything around it: a custom black kitchen set against the brick, floating stairs with wood treads, and bathrooms with brass fixtures and double vanities. The mix of preserved texture and new construction is what gives the house its character.",
            "Rehabs like this are equal parts demolition judgment and rebuild discipline: deciding what stays, making what stays sound, and building the new work to a standard the old brick deserves.",
        ],
        "todo": "owner to confirm/add real project details — starting condition, what was preserved vs replaced, one challenge solved. Wix images still hot-linked — self-host before launch.",
        "similar": ["home-addition-rehab-port-richmond", "exposed-brick-gut-renovation-kensington"],
    },
    {
        "slug": "home-addition-rehab-port-richmond",
        "title": "Home Addition &amp; Rehab",
        "area": "Port Richmond",
        "area_slug": "port-richmond",
        "type": "Property Rehab",
        "categories": ["property-rehab", "kitchen"],
        "card_blurb": "Home rehab with an addition, facade changes, and full interior renovation.",
        "card_variants": {
            "kitchen": ("https://static.wixstatic.com/media/dc69ab_df8e128588c640d1a7a13feacc9f7233~mv2.png", "Custom white kitchen after the renovation"),
        },
        "scope_html": f'{SVC["kitchen"]}, <a href="/services/full-builds-remodeling/">addition &amp; facade changes</a>',
        "hero_img": ("https://static.wixstatic.com/media/dc69ab_af97b51b2a6f4624954588d75d2eba35~mv2.png", "Rehabbed home with addition and new facade in Port Richmond"),
        "gallery": [
            ("https://static.wixstatic.com/media/dc69ab_d46a13a2c38340cf93628a4c39b08a69~mv2.png", "Addition under construction on the Port Richmond rehab"),
            ("https://static.wixstatic.com/media/dc69ab_df8e128588c640d1a7a13feacc9f7233~mv2.png", "Custom white kitchen after the renovation"),
            ("https://static.wixstatic.com/media/dc69ab_6b5b0190f10f4a4b851874fd67a4af82~mv2.png", "Kitchen island with seating and stainless appliances"),
            ("https://static.wixstatic.com/media/dc69ab_1eb4126f801b48fd91c0fda6390775ce~mv2.png", "Living space with open stairs and new flooring"),
            ("https://static.wixstatic.com/media/dc69ab_6087660590c046faaa56e382fcab0984~mv2.png", "Rear deck and outdoor space after the rehab"),
            ("https://static.wixstatic.com/media/dc69ab_01701671954043e78be252c593ff8f50~mv2.png", "Rear elevation showing the new addition"),
        ],
        "narrative": [
            "This home rehab in Port Richmond was customized with an addition, facade changes, and a full interior renovation — the three biggest moves you can make on an existing rowhome, all on one project.",
            "The addition bought the house the space its layout always wanted, and the interior was rebuilt around it: a custom white kitchen with island seating, open stairs, new flooring throughout, and a rear deck connecting the house to its outdoor space.",
            "Additions on occupied blocks are sequencing work — structure opened, weathered in, and closed without leaving the house exposed. It's the kind of project where having the same crew do the framing, the concrete, and the finishes pays for itself.",
        ],
        "todo": "owner to confirm/add real project details — addition size/purpose, starting condition, one challenge solved. Wix images still hot-linked — self-host before launch.",
        "similar": ["rowhome-rehab-kensington", "new-construction-port-richmond"],
    },
    {
        "slug": "new-construction-port-richmond",
        "title": "Five New Construction Homes",
        "area": "Port Richmond",
        "area_slug": "port-richmond",
        "type": "Full Build ×5",
        "categories": ["full-build", "kitchen", "bathroom"],
        "card_blurb": "Five new homes, each with a unique custom kitchen and baths, designed and built by us.",
        "card_variants": {
            "kitchen": img("new-construction-port-richmond", "white-shaker-kitchen-island", "White shaker kitchen with quartz island and black window frames"),
            "bathroom": img("new-construction-port-richmond", "floating-double-vanity-bath", "Floating double vanity with marble floor and glass shower"),
        },
        "scope_html": f'{SVC["fullbuild"].capitalize()}, {SVC["kitchens"]} &amp; {SVC["bathrooms"]}, <a href="/services/concrete/">foundations</a>',
        "hero_img": img("new-construction-port-richmond", "open-concept-living-stairs", "Open-concept living area with kitchen island and black-railed staircase in Port Richmond"),
        "gallery": [
            img("new-construction-port-richmond", "white-shaker-kitchen-island", "White shaker kitchen with quartz island and black window frames"),
            img("new-construction-port-richmond", "gloss-white-kitchen-quartz-island", "Gloss white kitchen with quartz island and stainless appliances"),
            img("new-construction-port-richmond", "granite-waterfall-island-kitchen", "Kitchen with waterfall granite island and pendant lights"),
            img("new-construction-port-richmond", "chimney-hood-gas-range", "Stainless chimney hood over a gas range with white shaker cabinetry"),
            img("new-construction-port-richmond", "floating-double-vanity-bath", "Floating double vanity with marble floor and glass shower"),
            img("new-construction-port-richmond", "glass-walkin-shower-bench", "Glass walk-in shower with bench and floating vanity"),
            img("new-construction-port-richmond", "tub-shower-marble-tile", "Tub shower with marble-look tile and built-in shelving"),
            img("new-construction-port-richmond", "black-marble-accent-bath", "Bathroom with black marble accent wall and floating vanity"),
        ],
        "narrative": [
            "Fully designed and built by B2B2 Builders, these five homes stand tall among the surrounding blocks of Port Richmond. In a nod to the neighborhood's historic ports, the exteriors carry a unique panelized design — five siblings, not five clones.",
            "Every home got its own custom kitchen, its own bathroom finishes, and its own flooring selections — white shaker with granite waterfall islands in one, gloss white with quartz in another; marble-tiled tub showers, glass walk-in showers with benches, floating double vanities. A deliberate choice to serve five different future owners instead of copy-pasting one spec sheet.",
            "Multi-home projects are where a builder's systems show: five foundations, five framing packages, five inspection tracks, one crew keeping them all moving. It remains one of the projects we're proudest of.",
        ],
        "todo": "owner to confirm/add real project details — build timeline, sales outcome, one challenge solved across the five homes",
        "similar": ["home-addition-rehab-port-richmond", "custom-kitchen-port-richmond"],
    },
    {
        "slug": "property-rehab-queen-village",
        "title": "Property Rehab &amp; Addition",
        "area": "Queen Village",
        "area_slug": "queen-village",
        "type": "Property Rehab",
        "categories": ["property-rehab", "kitchen"],
        "card_blurb": "Client rehab with a second-floor addition and a fully renovated custom interior.",
        "card_variants": {
            "kitchen": ("https://static.wixstatic.com/media/dc69ab_d23f00c228b440e990dcc8fc045d2fe9~mv2.jpg", "Green custom kitchen against original brick"),
        },
        "scope_html": f'{SVC["kitchen"]}, <a href="/services/full-builds-remodeling/">second-floor addition</a>',
        "hero_img": ("https://static.wixstatic.com/media/dc69ab_584fb1338625441989e9ff04275078f2~mv2.jpg", "Double-height living space with interior balcony in Queen Village"),
        "gallery": [
            ("https://static.wixstatic.com/media/dc69ab_d23f00c228b440e990dcc8fc045d2fe9~mv2.jpg", "Green custom kitchen against original brick in the Queen Village rehab"),
            ("https://static.wixstatic.com/media/dc69ab_3f77e04ff7ac411389ee560b4131945b~mv2.jpg", "Living area with exposed structure and garden views"),
            ("https://static.wixstatic.com/media/dc69ab_218158792e044569acd4170c03cd017df000.jpg", "Green tiled bathroom after the renovation"),
            ("https://static.wixstatic.com/media/dc69ab_612b24a376a44e90ba3bfb42be6682ba~mv2.jpg", "Sunroom opening to the rear garden"),
            ("https://static.wixstatic.com/media/dc69ab_871cc8c7ed1b4668b4a1641c661db400~mv2.jpg", "Open living space with new flooring and garden light"),
            ("https://static.wixstatic.com/media/dc69ab_61c6bcd72bfa44d39ad90c800ca5bd0d~mv2.jpg", "Mosaic wall detail preserved in the renovation"),
        ],
        "narrative": [
            "A beautiful client rehab two blocks off the Delaware in Queen Village, with a second-floor extension constructed above the original footprint. The interior was fully renovated to the client's taste and choice — and their taste was worth building.",
            "The house is anything but standard: a double-height living space with an interior balcony, a green custom kitchen set against original brick, a green-tiled bath, and a sunroom opening to the rear garden. Even a mosaic wall was kept and worked around rather than demolished — in a neighborhood this old, character is the asset.",
            "Additions in Queen Village mean building new structure onto very old structure, and making the seam invisible. That seam — where 200-year-old bones meet new framing — is where this project earned its keep.",
        ],
        "todo": "owner to confirm/add real project details — what the extension added, starting condition, one challenge solved. Wix images still hot-linked — self-host before launch.",
        "similar": ["rowhome-rehab-kensington", "luxury-townhome-kensington"],
    },
    # ================= NEW PROJECTS =================
    {
        "slug": "exposed-brick-gut-renovation-kensington",
        "title": "Exposed-Brick Gut Renovation",
        "area": "Kensington",
        "area_slug": "east-kensington",
        "type": "Gut Renovation",
        "categories": ["property-rehab", "kitchen", "bathroom"],
        "card_blurb": "Full gut renovation — exposed brick, floating reclaimed-wood stairs, navy-and-brass kitchen.",
        "card_variants": {
            "bathroom": img("exposed-brick-gut-renovation-kensington", "walnut-vanity-backlit-mirror", "Walnut double vanity with quartz top and backlit mirror"),
        },
        "scope_html": f'{SVC["kitchen"]}, {SVC["bathrooms"]}, {SVC["stairs"]}, facade restoration',
        "hero_img": img("exposed-brick-gut-renovation-kensington", "navy-island-kitchen-exposed-beams", "Kitchen with navy island, whitewashed exposed joists, and brass hardware in Kensington"),
        "gallery": [
            img("exposed-brick-gut-renovation-kensington", "renovated-rowhome-facade", "Renovated rowhome facade with white-painted brick, black windows, and restored cornice"),
            img("exposed-brick-gut-renovation-kensington", "floating-reclaimed-wood-stairs", "Floating steel-and-reclaimed-wood staircase against exposed brick"),
            img("exposed-brick-gut-renovation-kensington", "exposed-brick-living-room", "Living room with full exposed brick wall, spiral duct, and whitewashed joists"),
            img("exposed-brick-gut-renovation-kensington", "navy-kitchen-island-pendants", "Navy kitchen island with quartz top, globe pendants, and reclaimed wood shelving"),
            img("exposed-brick-gut-renovation-kensington", "entry-exposed-brick-joists", "Entry door against exposed brick under a whitewashed joist ceiling"),
            img("exposed-brick-gut-renovation-kensington", "walnut-vanity-backlit-mirror", "Walnut double vanity with quartz top and backlit mirror"),
            img("exposed-brick-gut-renovation-kensington", "glass-shower-hex-tile", "Glass shower with white subway tile and charcoal hexagon floor"),
            img("exposed-brick-gut-renovation-kensington", "open-riser-stairs-brick", "Open-riser reclaimed wood stair treads along the exposed brick wall"),
            img("exposed-brick-gut-renovation-kensington", "subway-tile-tub-shower", "Tub shower with white subway tile and matte black fixtures"),
            img("exposed-brick-gut-renovation-kensington", "sunroom-balcony-door", "Sunlit corner room with balcony glass door and tray ceiling"),
            img("exposed-brick-gut-renovation-kensington", "facade-night-view", "Night view of the finished white-painted brick facade with new sconce"),
            img("exposed-brick-gut-renovation-kensington", "brick-accent-niche", "Framed exposed-brick accent niche in a white hallway wall"),
        ],
        "narrative": [
            "A full gut renovation of a two-story brick rowhouse in Kensington — taken down to the shell and rebuilt into one of the most characterful houses on the block. The facade got the respect treatment: repointed and painted brick, a restored cornice, black windows, and a new entry with a proper transom.",
            "Inside, we let the building's bones do the talking. Exposed brick walls run the full depth of the house under whitewashed original joists, and a floating steel-and-reclaimed-wood staircase climbs past them to a skylight. The kitchen pairs a navy island and quartz counters with brass hardware and reclaimed wood shelving; the baths run white subway and hexagon tile with walnut vanities and backlit mirrors.",
            "Gut renovations are where judgment matters most: what you save, what you replace, and how new systems thread through a hundred-year-old structure. This one kept the century of character and replaced everything that needed to work like new.",
        ],
        "todo": "owner to confirm/add real project details — timeline, scope highlights, one challenge solved",
        "similar": ["rowhome-rehab-kensington", "navy-kitchen-kensington"],
    },
    {
        "slug": "new-construction-townhome-philadelphia",
        "title": "New Construction Townhome",
        "area": "Philadelphia",
        "area_slug": "fishtown",
        "type": "Full Build",
        "categories": ["full-build", "kitchen"],
        "card_blurb": "Three-story infill new build — modern panel-and-brick facade, quartz waterfall kitchen.",
        "card_variants": {
            "kitchen": img("new-construction-townhome-philadelphia", "kitchen-quartz-waterfall-island", "Kitchen with quartz waterfall island and black faucet"),
        },
        "scope_html": f'{SVC["fullbuild"].capitalize()}, {SVC["kitchen"].lower()}, {SVC["concrete"]}',
        "hero_img": img("new-construction-townhome-philadelphia", "three-story-townhome-facade", "Three-story new construction townhome facade with gray panels and black brick"),
        "gallery": [
            img("new-construction-townhome-philadelphia", "black-brick-entry-stoop", "Street-level entry with black brick, concrete stoop, and metal railings"),
            img("new-construction-townhome-philadelphia", "living-area-oak-floors", "Main living area with dark-stained stairs and whitewashed oak floors"),
            img("new-construction-townhome-philadelphia", "kitchen-quartz-waterfall-island", "Kitchen with quartz waterfall island and black faucet"),
            img("new-construction-townhome-philadelphia", "kitchen-island-patio-sliders", "Kitchen island with pendants and sliding door to the concrete patio"),
            img("new-construction-townhome-philadelphia", "waterfall-island-black-faucet", "Close-up of the quartz waterfall island with undermount sink"),
        ],
        "narrative": [
            "A three-story infill townhome built from the ground up on a Philadelphia corner lot — modern gray panel bays over black brick at the street, with a concrete stoop and metal railings that will still look right in twenty years.",
            "Inside, whitewashed oak floors run to a kitchen with a quartz waterfall island, black fixtures, and sliding doors to a private concrete patio. The layout keeps the living level open front to back, with the stair tucked to one side as a dark-stained counterpoint.",
            "Infill construction means building tight to neighbors, tight to the lot lines, and tight to the inspection schedule. This one went from foundation to finishes with our own crew on every phase.",
        ],
        "todo": "owner to confirm/add real project details — exact neighborhood, timeline, program",
        "similar": ["custom-home-build-fishtown", "quartz-island-kitchen-philadelphia"],
    },
    {
        "slug": "multifamily-new-construction-port-richmond",
        "title": "Multifamily New Construction",
        "area": "Port Richmond",
        "area_slug": "port-richmond",
        "type": "Full Build",
        "categories": ["full-build"],
        "card_blurb": "Ground-up multifamily development — black corrugated metal, corner garage townhomes.",
        "scope_html": f'{SVC["fullbuild"].capitalize()}, {SVC["framing"]}, {SVC["concrete"]}, {SVC["gc"]}',
        "hero_img": img("multifamily-new-construction-port-richmond", "corner-townhome-garage-complete", "Completed corner townhome with garage and new sidewalk in Port Richmond"),
        "gallery": [
            img("multifamily-new-construction-port-richmond", "black-corrugated-corner-building", "Black corrugated metal multifamily building at the street corner"),
            img("multifamily-new-construction-port-richmond", "corrugated-facade-windows", "Close-up of the black and white corrugated facade with new windows"),
            img("multifamily-new-construction-port-richmond", "finished-townhomes-garages", "Finished black and white townhomes with garages"),
            img("multifamily-new-construction-port-richmond", "pickwick-corner-elevation", "Corner elevation at the window-install stage"),
            img("multifamily-new-construction-port-richmond", "edgemont-side-elevation", "Side elevation with black siding during construction"),
            img("multifamily-new-construction-port-richmond", "multifamily-boom-lift", "Boom lift working the corrugated facade mid-construction"),
            img("multifamily-new-construction-port-richmond", "skyline-view-bathroom", "Freestanding tub with black marble tile and a Philadelphia skyline view"),
            img("multifamily-new-construction-port-richmond", "black-siding-dusk", "Black corrugated siding at dusk"),
        ],
        "narrative": [
            "A ground-up multifamily development on a Port Richmond corner — black and white corrugated metal over a modern frame, with garage-fronted townhomes completing the row. The material palette is industrial on purpose: this is a neighborhood built on work, and the building looks like it belongs.",
            "We carried the project from structure through skin: framing, concrete, window installation, and the corrugated rainscreen. Inside, the units run to a high spec — one master bath pairs a freestanding tub and black marble tile with a picture-window view of the Philadelphia skyline.",
            "Multifamily corners are logistics projects as much as construction projects: lifts on the sidewalk, deliveries on a live street, inspections stacked across units. Our crew ran it like the row deserved.",
        ],
        "todo": "owner to confirm/add real project details — unit count, timeline, delivery date",
        "similar": ["new-construction-port-richmond", "framing-structural-philadelphia"],
    },
    {
        "slug": "designer-rowhome-renovation-philadelphia",
        "title": "Designer Rowhome Renovation",
        "area": "Philadelphia",
        "area_slug": "port-richmond",
        "type": "Property Rehab",
        "categories": ["property-rehab", "kitchen", "bathroom"],
        "card_blurb": "Full renovation with a green herringbone master bath, teal-hood kitchen, and custom art-deco entry.",
        "card_variants": {
            "kitchen": img("designer-rowhome-renovation-philadelphia", "teal-hood-kitchen-range", "Pro-style range with teal vent hood, subway tile, and wood shelves"),
        },
        "scope_html": f'{SVC["kitchen"]}, {SVC["bathrooms"]}, facade &amp; porch restoration',
        "hero_img": img("designer-rowhome-renovation-philadelphia", "green-herringbone-master-bath", "Master bath with green herringbone tile shower, freestanding tub, and brass fixtures"),
        "gallery": [
            img("designer-rowhome-renovation-philadelphia", "herringbone-shower-freestanding-tub", "Green herringbone shower wall beside the freestanding tub"),
            img("designer-rowhome-renovation-philadelphia", "walnut-double-vanity-brass", "Walnut double vanity with marble top and brass faucets"),
            img("designer-rowhome-renovation-philadelphia", "tub-brass-filler-green-tile", "Freestanding white tub with brass filler against glossy green tile"),
            img("designer-rowhome-renovation-philadelphia", "navy-vanity-geometric-floor", "Guest bath with navy vanity and geometric black-and-white floor tile"),
            img("designer-rowhome-renovation-philadelphia", "brick-tile-walkin-shower", "Brick-look tiled walk-in shower with black fixtures and marble pan"),
            img("designer-rowhome-renovation-philadelphia", "teal-hood-kitchen-range", "Pro-style range with teal vent hood, subway tile, and wood shelves"),
            img("designer-rowhome-renovation-philadelphia", "repainted-rowhouse-facade", "Repainted black and white rowhouse facade with ornate pediment"),
            img("designer-rowhome-renovation-philadelphia", "yellow-art-deco-door", "Custom yellow art-deco security door and mailbox panel"),
            img("designer-rowhome-renovation-philadelphia", "porch-ceiling-fan", "Restored porch with ceiling fan on the renovated rowhouse"),
        ],
        "narrative": [
            "A designer-grade renovation of a classic two-story Philadelphia rowhouse — the kind of project where every room got a point of view. The master bath is the showpiece: glossy green herringbone tile, a freestanding tub with a brass floor filler, and a walnut double vanity under marble.",
            "The rest of the house keeps pace. The guest bath pairs a navy vanity with geometric black-and-white floor tile and a brick-look walk-in shower; the kitchen runs a pro-style range under a teal vent hood with open wood shelving. Outside, the facade was repainted black and white under its ornate original pediment — and the entry got a custom yellow art-deco security door you won't find on any other block.",
            "Renovations like this succeed on coordination: tile setters, painters, and metal fabricators all working to one design language. That's the general contracting discipline behind the photos.",
        ],
        "todo": "owner to confirm/add real project details — neighborhood, timeline, design credits",
        "similar": ["exposed-brick-gut-renovation-kensington", "designer-bathrooms-philadelphia"],
    },
    {
        "slug": "concrete-walkway-bluestone-patio-philadelphia",
        "title": "Concrete Walkway &amp; Bluestone Patio",
        "area": "Philadelphia",
        "area_slug": "montgomery-county",
        "type": "Concrete &amp; Hardscape",
        "categories": ["concrete"],
        "card_blurb": "Poured concrete walkway, bluestone flagstone patio, and new French doors — with video.",
        "scope_html": f'{SVC["concrete"].capitalize()}, hardscape, exterior door installation',
        "hero_img": img("concrete-walkway-bluestone-patio-philadelphia", "concrete-walkway-pour", "Freshly poured concrete walkway beside a bluestone flagstone patio"),
        "gallery": [
            vid("concrete-walkway-bluestone-patio-philadelphia", "bluestone-patio-tour-1", "Video tour of the newly laid bluestone flagstone patio"),
            img("concrete-walkway-bluestone-patio-philadelphia", "walkway-flagstone-garden", "New concrete walkway meeting the flagstone patio and flower garden"),
            img("concrete-walkway-bluestone-patio-philadelphia", "french-doors-stone-facade", "New white French doors installed in the stone facade"),
            img("concrete-walkway-bluestone-patio-philadelphia", "french-doors-bluestone-patio", "French patio doors opening onto the bluestone patio"),
            img("concrete-walkway-bluestone-patio-philadelphia", "french-doors-interior", "Interior view of the newly installed French doors"),
            vid("concrete-walkway-bluestone-patio-philadelphia", "bluestone-patio-tour-2", "Video of the finished flagstone patio around the tree and pergola posts"),
        ],
        "narrative": [
            "An outdoor living package: a poured concrete walkway ramping from the sidewalk, a bluestone flagstone patio set around the yard's existing tree, and new French doors cut into the stone facade to connect the house to all of it.",
            "Concrete and hardscape are two different trades that have to meet perfectly — the walkway's pour, pitch, and finish on one side, the flagstone's pattern and joints on the other. The videos in the gallery show the result the way photos can't: walk the patio yourself.",
            "Exterior work like this is weather-window work. We sequenced demolition, base prep, pour, and stone set so the yard was never torn up longer than it had to be.",
        ],
        "todo": "owner to confirm/add real project details — location, square footage, timeline",
        "similar": ["structural-concrete-philadelphia", "property-rehab-queen-village"],
    },
    {
        "slug": "rowhome-renovation-video-tour-philadelphia",
        "title": "Rowhome Renovation — Video Tour",
        "area": "Philadelphia",
        "area_slug": "fishtown",
        "type": "Property Rehab",
        "categories": ["property-rehab", "kitchen"],
        "card_blurb": "Finished full renovation — walk the open-concept living level and finished basement on video.",
        "scope_html": f'{SVC["kitchen"]}, basement finishing, flooring throughout',
        "hero_img": img("rowhome-renovation-video-tour-philadelphia", "open-concept-kitchen", "Open-concept kitchen with white shaker cabinets, island, and dark hardwood floors"),
        "gallery": [
            vid("rowhome-renovation-video-tour-philadelphia", "rowhome-walkthrough-tour", "Video walkthrough of the finished rowhome living area and kitchen"),
            img("rowhome-renovation-video-tour-philadelphia", "finished-basement-stairs", "Finished basement staircase with brown treads and white risers"),
            vid("rowhome-renovation-video-tour-philadelphia", "bedroom-hardwood-tour", "Video of a sunlit bedroom with new hardwood floors"),
        ],
        "narrative": [
            "A complete rowhome renovation, delivered move-in ready — and best seen in motion. The videos in the gallery walk the open-concept living level, the white shaker kitchen with island, and a sunlit bedroom with new hardwood floors.",
            "The basement went from storage to living space: a finished staircase with brown treads and white risers, new flooring, and clean drywall throughout. It's the square footage most rowhomes waste, put back to work.",
            "We publish walkthrough video because it's the honest format — no wide-angle tricks, just the house as you'd tour it. If you want to see a B2B2 renovation at eye level, press play.",
        ],
        "todo": "owner to confirm/add real project details — neighborhood, scope list, timeline",
        "similar": ["designer-rowhome-renovation-philadelphia", "exposed-brick-gut-renovation-kensington"],
    },
    # ================= KITCHEN SHOWCASES =================
    {
        "slug": "custom-kitchen-port-richmond",
        "title": "Custom Kitchens",
        "area": "Port Richmond",
        "area_slug": "port-richmond",
        "type": "Custom Kitchen",
        "categories": ["kitchen"],
        "card_blurb": "Five kitchens, five looks — waterfall granite, gloss white, shaker and quartz.",
        "scope_html": f'{SVC["kitchen"]} design &amp; build, part of {SVC["fullbuild"]}',
        "hero_img": img("new-construction-port-richmond", "white-shaker-kitchen-island", "White shaker custom kitchen with quartz island in Port Richmond"),
        "gallery": [
            img("new-construction-port-richmond", "gloss-white-kitchen-quartz-island", "Gloss white kitchen with quartz island and stainless fridge"),
            img("new-construction-port-richmond", "white-kitchen-pendant-island", "White kitchen with island pendant light and rear entry"),
            img("new-construction-port-richmond", "granite-waterfall-island-kitchen", "Waterfall granite island with pendant lights"),
            img("new-construction-port-richmond", "chimney-hood-gas-range", "Stainless chimney hood over a black gas range"),
            img("new-construction-port-richmond", "kitchen-wide-hardwood", "Wide kitchen view with island, stair railing, and hardwood floors"),
            img("new-construction-port-richmond", "open-concept-living-stairs", "Open-concept living area flowing into the kitchen"),
        ],
        "narrative": [
            "These kitchens come from our five-home new construction project in Port Richmond — and no two are the same. One runs white shaker with a granite waterfall island; another goes gloss white and quartz with a full stainless package.",
            "Every kitchen we build gets the same fundamentals: real plywood boxes, counters templated after cabinets are set, appliance panels aligned to the millimeter, and lighting planned with the layout instead of after it.",
            "Planning a kitchen in Port Richmond or the River Wards? Start with our <a href=\"/services/kitchen-remodeling/\">kitchen remodeling service</a> — or see the whole five-home project this work came from.",
        ],
        "parent": "new-construction-port-richmond",
        "similar": ["new-construction-port-richmond", "navy-kitchen-kensington"],
    },
    {
        "slug": "navy-kitchen-kensington",
        "title": "Navy &amp; Brass Custom Kitchen",
        "area": "Kensington",
        "area_slug": "east-kensington",
        "type": "Custom Kitchen",
        "categories": ["kitchen"],
        "card_blurb": "Navy island, quartz counters, brass hardware, and reclaimed wood under whitewashed joists.",
        "scope_html": f'{SVC["kitchen"]} design &amp; build, part of a gut renovation',
        "hero_img": img("exposed-brick-gut-renovation-kensington", "navy-island-kitchen-exposed-beams", "Navy island kitchen under whitewashed exposed joists in Kensington"),
        "gallery": [
            img("exposed-brick-gut-renovation-kensington", "navy-kitchen-island-pendants", "Navy kitchen island with globe pendants and coil faucet"),
            img("exposed-brick-gut-renovation-kensington", "navy-cabinet-reclaimed-shelves", "Navy cabinetry with reclaimed wood shelving by the deck door"),
            img("exposed-brick-gut-renovation-kensington", "white-pantry-brass-pulls", "White pantry cabinets with brass pulls and stainless fridge"),
            img("exposed-brick-gut-renovation-kensington", "island-pendants-deck-door", "Kitchen island under exposed beam ceiling with patio door to the deck"),
        ],
        "narrative": [
            "The kitchen from our exposed-brick gut renovation in Kensington: a navy island under globe pendants, quartz counters, brass pulls, and reclaimed wood shelving — all beneath the house's original whitewashed joists.",
            "The palette works because the contrast is disciplined — navy and white cabinetry, warm brass, and one material (reclaimed wood) repeated from shelves to stair treads. That's design intent carried through by one crew.",
            "Want a kitchen with this much character? See our <a href=\"/services/kitchen-remodeling/\">kitchen remodeling service</a> or the full gut renovation this kitchen lives in.",
        ],
        "parent": "exposed-brick-gut-renovation-kensington",
        "similar": ["exposed-brick-gut-renovation-kensington", "custom-kitchen-port-richmond"],
    },
    {
        "slug": "black-white-kitchen-east-kensington",
        "title": "Black &amp; White Designer Kitchen",
        "area": "East Kensington",
        "area_slug": "east-kensington",
        "type": "Custom Kitchen",
        "categories": ["kitchen"],
        "card_blurb": "Matte black cabinets, waterfall quartz island, built-in bench, and a wet bar to match.",
        "scope_html": f'{SVC["kitchen"]} design &amp; build, part of {SVC["fullbuild"]}',
        "hero_img": img("modern-custom-home-east-kensington", "kitchen-waterfall-island-wide", "Black and white kitchen with waterfall quartz island and built-in bench"),
        "gallery": [
            img("modern-custom-home-east-kensington", "black-white-kitchen-island", "Matte black kitchen island with bar stools"),
            img("modern-custom-home-east-kensington", "wet-bar-wine-fridge", "Matching wet bar with black sink and dual-zone wine fridge"),
        ],
        "narrative": [
            "The kitchen from our modern custom home in East Kensington: matte black cabinetry against white walls, a waterfall quartz island with seating, a built-in dining bench, and sliding doors to the patio.",
            "The same palette carries to a wet bar nook — quartz counter, black undermount sink, and a stainless dual-zone wine fridge — so the entertaining space reads as one design, not an afterthought.",
            "Thinking about a statement kitchen? Start with our <a href=\"/services/kitchen-remodeling/\">kitchen remodeling service</a> or tour the full custom home this kitchen anchors.",
        ],
        "parent": "modern-custom-home-east-kensington",
        "similar": ["modern-custom-home-east-kensington", "luxury-kitchen-philadelphia"],
    },
    {
        "slug": "luxury-kitchen-philadelphia",
        "title": "Luxury Kitchen with Floating Staircase",
        "area": "Kensington",
        "area_slug": "east-kensington",
        "type": "Custom Kitchen",
        "categories": ["kitchen"],
        "card_blurb": "Waterfall quartz island, brass globe chandelier, and a skylit floating staircase.",
        "scope_html": f'{SVC["kitchen"]} design &amp; build, part of {SVC["fullbuild"]}',
        "hero_img": img("luxury-townhome-kensington", "luxury-kitchen-waterfall-island", "Luxury white kitchen with waterfall quartz island and brass chandelier"),
        "gallery": [
            img("luxury-townhome-kensington", "kitchen-floating-staircase", "Kitchen island with brass faucet beside the floating staircase"),
            img("luxury-townhome-kensington", "kitchen-skylight-fireplace", "Kitchen and open stairwell under a skylight with double-sided fireplace"),
        ],
        "narrative": [
            "The kitchen from our luxury custom townhome in Kensington — a white kitchen with a waterfall quartz island, brass fixtures, driftwood accents, and a globe chandelier, set beside a floating steel-and-wood staircase that climbs to a skylight.",
            "A kitchen this open has no back side: every elevation is on display, including the stair beside it. That's why the same crew built both — so the reveal lines, materials, and sight lines agree.",
            "See our <a href=\"/services/kitchen-remodeling/\">kitchen remodeling service</a>, or tour the full townhome this kitchen belongs to.",
        ],
        "parent": "luxury-townhome-kensington",
        "similar": ["luxury-townhome-kensington", "black-white-kitchen-east-kensington"],
    },
    {
        "slug": "quartz-island-kitchen-philadelphia",
        "title": "Quartz Waterfall Island Kitchen",
        "area": "Philadelphia",
        "area_slug": "fishtown",
        "type": "Custom Kitchen",
        "categories": ["kitchen"],
        "card_blurb": "Quartz waterfall island, black faucet, and patio sliders in a new-build townhome.",
        "scope_html": f'{SVC["kitchen"]} design &amp; build, part of {SVC["fullbuild"]}',
        "hero_img": img("new-construction-townhome-philadelphia", "kitchen-quartz-waterfall-island", "Kitchen with quartz waterfall island and black faucet"),
        "gallery": [
            img("new-construction-townhome-philadelphia", "kitchen-island-patio-sliders", "Kitchen island with pendants and sliding patio door"),
            img("new-construction-townhome-philadelphia", "waterfall-island-black-faucet", "Quartz waterfall island close-up with undermount sink"),
        ],
        "narrative": [
            "The kitchen from our new construction townhome: a quartz waterfall island with a black faucet and undermount sink, pendant lighting, and sliding doors that open the cooking space to a private concrete patio.",
            "New-build kitchens let us plan everything at once — plumbing runs, island electrical, venting, and lighting all placed for the layout instead of retrofitted around it.",
            "Planning a kitchen for a new build or a renovation? Our <a href=\"/services/kitchen-remodeling/\">kitchen remodeling service</a> covers both.",
        ],
        "parent": "new-construction-townhome-philadelphia",
        "similar": ["new-construction-townhome-philadelphia", "custom-kitchen-port-richmond"],
    },
    # ================= BATHROOM SHOWCASES =================
    {
        "slug": "spa-master-bathroom-east-kensington",
        "title": "Spa Master Bathroom",
        "area": "East Kensington",
        "area_slug": "east-kensington",
        "type": "Custom Bathroom",
        "categories": ["bathroom"],
        "card_blurb": "Freestanding tub, glass shower with bench, double vanity, matte black fixtures.",
        "scope_html": f'{SVC["bathrooms"].capitalize()} design &amp; build, part of {SVC["fullbuild"]}',
        "hero_img": img("modern-custom-home-east-kensington", "master-bath-freestanding-tub", "Spa master bathroom with freestanding tub, glass shower, and double vanity"),
        "gallery": [
            img("modern-custom-home-east-kensington", "master-bath-glass-shower", "Glass slider shower with black floor-mounted tub filler"),
            img("modern-custom-home-east-kensington", "double-vanity-led-mirror", "Marble-top double vanity with LED mirror"),
            img("modern-custom-home-east-kensington", "shower-bench-black-fixtures", "Textured white tile shower with bench and matte black rain fixtures"),
            img("modern-custom-home-east-kensington", "soaking-tub-window", "Freestanding soaking tub under the window with black filler"),
            img("modern-custom-home-east-kensington", "powder-room-geometric-tile", "Powder room with matte black toilet and starburst tile floor"),
            img("modern-custom-home-east-kensington", "kids-bathroom-orange-vanity", "Colorful kids bathroom with orange vanity and vessel sink"),
        ],
        "narrative": [
            "The bathrooms from our modern custom home in East Kensington, led by a spa-grade master: freestanding soaking tub under the window, a glass shower with bench and matte black rain fixtures, and a marble-top double vanity with an LED mirror.",
            "The supporting cast has personality — a powder room with a matte black toilet on a geometric starburst floor, and a kids bath in orange with a vessel sink. Custom means every bathroom gets designed, not just the big one.",
            "Ready for a bathroom that feels like a retreat? Start with our <a href=\"/services/bathroom-remodeling/\">bathroom remodeling service</a>.",
        ],
        "parent": "modern-custom-home-east-kensington",
        "similar": ["modern-custom-home-east-kensington", "designer-bathrooms-philadelphia"],
    },
    {
        "slug": "custom-bathrooms-port-richmond",
        "title": "Custom Bathrooms",
        "area": "Port Richmond",
        "area_slug": "port-richmond",
        "type": "Custom Bathroom",
        "categories": ["bathroom"],
        "card_blurb": "Marble tile, glass walk-in showers, floating vanities — across five new homes.",
        "scope_html": f'{SVC["bathrooms"].capitalize()} design &amp; build, part of {SVC["fullbuild"]}',
        "hero_img": img("new-construction-port-richmond", "floating-double-vanity-bath", "Floating double vanity bathroom with marble floor in Port Richmond"),
        "gallery": [
            img("new-construction-port-richmond", "glass-walkin-shower-bench", "Glass walk-in shower with bench"),
            img("new-construction-port-richmond", "tub-shower-marble-tile", "Tub shower with marble-look tile and hex accent strip"),
            img("new-construction-port-richmond", "black-marble-accent-bath", "Bathroom with black marble accent wall and floating vanity"),
            img("new-construction-port-richmond", "shower-mosaic-band-detail", "Shower detail with gray marble tile and mosaic accent band"),
        ],
        "narrative": [
            "The bathrooms from our five-home Port Richmond project: glass walk-in showers with benches, floating double vanities over marble floors, tub showers in marble-look tile with hex accents, and one statement bath with a black marble feature wall.",
            "Five homes meant five bathroom specs — tiled, waterproofed, and finished by the same crew so the quality is identical even where the designs aren't.",
            "Planning a bathroom? Our <a href=\"/services/bathroom-remodeling/\">bathroom remodeling service</a> handles design through grout lines.",
        ],
        "parent": "new-construction-port-richmond",
        "similar": ["new-construction-port-richmond", "custom-bathrooms-kensington"],
    },
    {
        "slug": "custom-bathrooms-kensington",
        "title": "Custom Bathrooms",
        "area": "Kensington",
        "area_slug": "east-kensington",
        "type": "Custom Bathroom",
        "categories": ["bathroom"],
        "card_blurb": "Walnut vanities, backlit mirrors, subway and hex tile from a full gut renovation.",
        "scope_html": f'{SVC["bathrooms"].capitalize()} design &amp; build, part of a gut renovation',
        "hero_img": img("exposed-brick-gut-renovation-kensington", "walnut-vanity-backlit-mirror", "Walnut double vanity with backlit mirror in Kensington"),
        "gallery": [
            img("exposed-brick-gut-renovation-kensington", "glass-shower-hex-tile", "Glass shower with subway tile and charcoal hexagon floor"),
            img("exposed-brick-gut-renovation-kensington", "subway-tile-tub-shower", "Tub shower with white subway tile and matte black fixtures"),
            img("exposed-brick-gut-renovation-kensington", "white-vanity-hex-floor", "White vanity with waterfall faucet over black hexagon tile"),
            img("exposed-brick-gut-renovation-kensington", "subway-shower-glass", "Glass shower with white subway tile"),
        ],
        "narrative": [
            "The bathrooms from our exposed-brick gut renovation in Kensington: a walnut double vanity with a quartz top and backlit LED mirror, glass showers in white subway tile, and charcoal hexagon floors that ground the palette.",
            "Every bath in the house was taken to the studs — new plumbing, new waterproofing, new tile — so the finishes are backed by systems that work like the house is new.",
            "See the <a href=\"/services/bathroom-remodeling/\">bathroom remodeling service</a> or walk the full gut renovation these baths belong to.",
        ],
        "parent": "exposed-brick-gut-renovation-kensington",
        "similar": ["exposed-brick-gut-renovation-kensington", "custom-bathrooms-port-richmond"],
    },
    {
        "slug": "marble-brass-bathrooms-philadelphia",
        "title": "Marble &amp; Brass Luxury Bathrooms",
        "area": "Kensington",
        "area_slug": "east-kensington",
        "type": "Custom Bathroom",
        "categories": ["bathroom"],
        "card_blurb": "Marble feature walls, brass rain heads, walnut vanities, round LED mirrors.",
        "scope_html": f'{SVC["bathrooms"].capitalize()} design &amp; build, part of {SVC["fullbuild"]}',
        "hero_img": img("luxury-townhome-kensington", "master-bath-marble-wall", "Luxury master bath with marble feature wall and freestanding tub"),
        "gallery": [
            img("luxury-townhome-kensington", "master-bath-double-vanity", "Floating double vanity with round LED mirrors"),
            img("luxury-townhome-kensington", "marble-shower-brass-fixtures", "Marble shower with brass rain heads and bench"),
            img("luxury-townhome-kensington", "white-master-bath-brass", "Bright master bath with brass tub filler and double vanity"),
            img("luxury-townhome-kensington", "guest-bath-herringbone-tile", "Guest bath with herringbone tile and round window"),
            img("luxury-townhome-kensington", "walnut-floating-vanity", "Walnut floating vanity with LED mirror"),
        ],
        "narrative": [
            "The bathrooms from our luxury custom townhome: a master with a full marble feature wall, curbless shower with double brass rain heads and a marble bench, freestanding tub with brass floor filler, and a floating double vanity under round LED mirrors.",
            "The guest bath holds its own — herringbone tile around the tub, a walnut floating vanity, and the townhome's signature round porthole window.",
            "For bathwork at this level, start with our <a href=\"/services/bathroom-remodeling/\">bathroom remodeling service</a>.",
        ],
        "parent": "luxury-townhome-kensington",
        "similar": ["luxury-townhome-kensington", "spa-master-bathroom-east-kensington"],
    },
    {
        "slug": "designer-bathrooms-philadelphia",
        "title": "Designer Bathrooms",
        "area": "Philadelphia",
        "area_slug": "port-richmond",
        "type": "Custom Bathroom",
        "categories": ["bathroom"],
        "card_blurb": "Green herringbone tile, brass fixtures, navy vanities, and brick-look showers.",
        "scope_html": f'{SVC["bathrooms"].capitalize()} design &amp; build, part of a full renovation',
        "hero_img": img("designer-rowhome-renovation-philadelphia", "green-herringbone-master-bath", "Designer master bath with green herringbone tile and freestanding tub"),
        "gallery": [
            img("designer-rowhome-renovation-philadelphia", "herringbone-shower-freestanding-tub", "Green herringbone shower beside the freestanding tub"),
            img("designer-rowhome-renovation-philadelphia", "walnut-double-vanity-brass", "Walnut double vanity with marble top and brass faucets"),
            img("designer-rowhome-renovation-philadelphia", "tub-brass-filler-green-tile", "White tub with brass filler against green tile"),
            img("designer-rowhome-renovation-philadelphia", "navy-vanity-geometric-floor", "Navy vanity with geometric black-and-white floor tile"),
            img("designer-rowhome-renovation-philadelphia", "brick-tile-walkin-shower", "Brick-look walk-in shower with black fixtures"),
        ],
        "narrative": [
            "The bathrooms from our designer rowhome renovation — led by a master in glossy green herringbone tile with a freestanding tub, brass floor filler, and walnut double vanity under marble.",
            "The guest bath answers with a navy vanity on geometric black-and-white tile and a brick-look walk-in shower with matte black fixtures. Two rooms, two personalities, one standard of tile work.",
            "Want a bathroom with a point of view? Start at our <a href=\"/services/bathroom-remodeling/\">bathroom remodeling service</a>.",
        ],
        "parent": "designer-rowhome-renovation-philadelphia",
        "similar": ["designer-rowhome-renovation-philadelphia", "custom-bathrooms-kensington"],
    },
    # ================= CONCRETE & FRAMING SHOWCASES =================
    {
        "slug": "structural-concrete-philadelphia",
        "title": "Structural Concrete &amp; Foundations",
        "area": "Philadelphia",
        "area_slug": "fishtown",
        "type": "Concrete",
        "categories": ["concrete"],
        "card_blurb": "Poured walls, stair formwork, light-well courtyards, and insulated basement slabs.",
        "scope_html": f'{SVC["concrete"].capitalize()} — foundations, walls, flatwork; {SVC["framing"]} coordination',
        "hero_img": img("structural-concrete-philadelphia", "concrete-lightwell-spiral-stair", "Concrete light-well courtyard with black steel spiral stair"),
        "gallery": [
            img("structural-concrete-philadelphia", "concrete-stair-formwork-rebar", "Rebar-reinforced concrete stair formwork against a board-formed wall"),
            img("structural-concrete-philadelphia", "concrete-courtyard-walls", "Poured concrete courtyard walls with steel catwalk above"),
            img("structural-concrete-philadelphia", "basement-concrete-walls-steel-beam", "Basement with poured concrete walls and steel beam"),
            img("structural-concrete-philadelphia", "basement-slab-insulation", "Rigid foam insulation over a basement slab between concrete walls"),
            img("structural-concrete-philadelphia", "poured-party-walls-steel", "Poured concrete party walls with steel beams and framing above"),
        ],
        "narrative": [
            "Concrete is where our builds start — and on some projects, it's the architecture. This portfolio runs from board-formed courtyard walls and a light-well with a steel spiral stair to rebar-cage stair formwork, insulated basement slabs, and poured party walls carrying steel and framing above.",
            "Structural concrete rewards preparation: the formwork, the rebar schedule, and the pour sequence decide everything you see after the forms strip. We self-perform this work so the framing that follows lands on dimensions we controlled.",
            "Need foundations, walls, or flatwork? See our <a href=\"/services/concrete/\">concrete service</a> for the full scope we pour.",
        ],
        "similar": ["concrete-walkway-bluestone-patio-philadelphia", "framing-structural-philadelphia"],
    },
    {
        "slug": "framing-structural-philadelphia",
        "title": "Framing &amp; Structural Work",
        "area": "Philadelphia",
        "area_slug": "fishtown",
        "type": "Framing",
        "categories": ["framing"],
        "card_blurb": "Rowhome additions, interior framing, roof decks — our crew, our lumber, our schedule.",
        "scope_html": f'{SVC["framing"].capitalize()} — additions, full structures, roof decks',
        "hero_img": img("framing-structural-philadelphia", "roof-deck-skyline", "Crew member on a framed roof deck with the Philadelphia skyline behind"),
        "gallery": [
            img("framing-structural-philadelphia", "rowhome-addition-framing", "Framed addition rising between brick rowhomes"),
            img("framing-structural-philadelphia", "stud-wall-framing-crew", "Crew framing wood stud walls on an addition"),
            img("framing-structural-philadelphia", "interior-framing-blocking", "Interior stud and OSB framing with blocking"),
            img("framing-structural-philadelphia", "framing-layout-crew", "Crew laying out lumber in a framed room"),
            img("framing-structural-philadelphia", "top-plate-framing-sky", "Framed wall and joists against the sky"),
            img("framing-structural-philadelphia", "stud-framed-rooms", "Stud-framed rooms and doorway openings on the second floor"),
            img("framing-structural-philadelphia", "roof-deck-parapet-framing", "Roof deck sheathing and parapet framing over city rooftops"),
        ],
        "narrative": [
            "Framing is the trade we never sub out. This portfolio shows why: rowhome additions rising between existing brick, interior stud work with blocking where the finishes will need it, and roof decks framed with the Philadelphia skyline for a backdrop.",
            "Good framing is invisible in the finished photos — it's why the doors swing true, the tile lines stay straight, and the floors don't bounce. Our carpenters frame to the finish schedule, not just to the inspection.",
            "Have a structure, addition, or roof deck in mind? Our <a href=\"/services/framing/\">framing service</a> covers it.",
        ],
        "similar": ["structural-concrete-philadelphia", "multifamily-new-construction-port-richmond"],
    },
]

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
    hero_src, hero_alt = p["hero_img"]
    tag = f'{esc_plain(p["type"])} · {p["area"]}'
    types = " ".join(p["categories"])
    # Per-category thumbnails: the filter JS swaps the card image so a
    # "Custom Kitchens" filter shows a kitchen, not the project's facade.
    variant_attrs = f' data-img-default="{hero_src}" data-alt-default="{hero_alt}"'
    for cat, (v_src, v_alt) in p.get("card_variants", {}).items():
        variant_attrs += f' data-img-{cat}="{v_src}" data-alt-{cat}="{v_alt}"'
    return f'''          <li class="hub-card" data-project-type="{types}" data-reveal>
            <img src="{hero_src}" alt="{hero_alt}" width="480" height="300" loading="lazy"{variant_attrs}>
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
    cards_html = "\n".join(hub_card(p) for p in PROJECTS)
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
