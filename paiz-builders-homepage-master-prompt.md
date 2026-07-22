# MASTER PROMPT — Paiz Builders Homepage (v1, design review build)

You are a senior front-end designer/developer at a boutique studio. Build a **single, complete, production-quality homepage** for **Paiz Builders**, a Philadelphia general contractor. This is a design-review build: everything must render locally with no build step, but the code quality, semantics, and SEO must be production-grade so it can graduate to the live site with minimal changes.

The bar: on par with or better than premium Webflow templates like Woodworked (woodworked-template.webflow.io) and Remodix (remodix.webflow.io) — generous whitespace, disciplined type system, editorial section layouts, calm confidence. It must NOT look like a contractor template or an AI-generated page.

---

## 1. Deliverable & tech constraints

- Three files: `index.html`, `styles.css`, `script.js`. No frameworks, no build step, no Tailwind. Vanilla HTML/CSS/JS.
- Semantic HTML5 throughout: `header`, `nav`, `main`, `section`, `article`, `footer`, proper landmark roles. Exactly **one `<h1>`**. Logical H2→H3 hierarchy, no skipped levels.
- Fully responsive: 1440px desktop → 768px tablet → 375px mobile. Mobile gets a **sticky bottom click-to-call bar** (phone icon + "Call 215-888-4384", `tel:` link).
- Accessibility floor: visible keyboard focus states, WCAG AA contrast, `prefers-reduced-motion` respected (all animation disabled under it), all interactive elements reachable by keyboard.
- Images: use **solid-color placeholder `<div>`s or `https://picsum.photos` seeds**, each with a descriptive HTML comment like `<!-- TODO: real photo — finished kitchen, 1502 Hancock St, Fishtown -->` and a written `alt` as if the real photo were in place. Real photos get swapped in later.
- Performance: no text rendered on top of the hero's LCP image; system font fallbacks declared; lazy-load all below-fold images (`loading="lazy"`); no layout shift (explicit aspect-ratios on media containers).

## 2. Brand & design system

### Identity
- Business name: **Paiz Builders** (logo mark: stylized blue "P" — use a text logo "PAIZ **BUILDERS**" styled in the display font for now, with a TODO comment for the SVG logo).
- Voice: confident, plainspoken, craftsman-direct. Short sentences. No marketing fluff, no "we strive to."

### Color tokens (CSS custom properties)
```
--ink:        #16181D   (charcoal — primary text, dark sections)
--paper:      #FAFAF8   (warm near-white — page background)
--surface:    #FFFFFF   (cards)
--line:       #E6E7EA   (hairline borders)
--blue:       #1B66E0   (primary — buttons, links, headline accent word, icons)
--blue-deep:  #0E3E92   (hover, dark-section accents)
--orange:     #F26419   (construction orange — accent ONLY, see rules)
--muted:      #5C6470   (secondary text)
```

**Color discipline (hard rules):**
- Roughly 90% neutral / 8% blue / 2% orange across the page.
- Blue is the workhorse: primary buttons, links, one accent word per major headline, icon strokes.
- Orange appears ONLY as: (1) the bracketed eyebrow section labels, (2) short underline accent bars in alternating sections, (3) hover state on card arrow chips, (4) the "Takes about 60 seconds" chip on the Project Builder, and (5) **the single orange button in the final dark CTA band** — the loudest moment on the page. Orange is never a background fill and never body text.

### Typography
- **Display:** Clash Display (weights 500/600/700) via Fontshare: `https://api.fontshare.com/v2/css?f[]=clash-display@500,600,700&display=swap`
- **Body:** Satoshi (weights 400/500/700) via Fontshare: `https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap`
- Fallback stacks: display → `"Clash Display", "Arial Narrow", sans-serif`; body → `"Satoshi", -apple-system, "Segoe UI", sans-serif`.
- Type scale (desktop): H1 clamp(3.5rem→6rem), section H2 clamp(2.5rem→4rem), tight leading (1.05–1.1) on display sizes, body 1.0625rem/1.7. Big and bold is the personality of this site — headlines should feel oversized and confident, like Woodworked.
- **Two-tone headline device:** every major headline has exactly one word or phrase in `--blue` (e.g., "We **Build** It."). Carry this through the whole page.
- **Eyebrow label system:** every section opens with a small bracketed uppercase label in `--orange`, letterspaced: `[ OUR SERVICES ]`, `[ RECENT PROJECTS ]`, etc. Consistent size/spacing everywhere.

### Layout & spacing
- Max content width 1240px, generous gutters.
- Sections separated by large vertical space (desktop: 120–160px). Sections must breathe — whitespace is the premium signal.
- Border radius: 16px cards, 10px buttons. Soft shadows only on floating elements (subtle, never heavy).
- Alternate section backgrounds sparingly: `--paper` default, `--surface` white cards, ONE dark `--ink` band (final CTA) plus the reviews band may use a very subtle tint.

### Motion (restrained)
- One orchestrated hero load-in: headline lines rise/fade staggered, then the 2×2 cards fade up staggered. ~700ms total.
- Scroll-triggered reveals (IntersectionObserver): sections fade/translate up 16px once. No parallax, no scroll-jacking.
- Hover micro-interactions: card lift 4px + arrow chip turns orange; buttons darken.
- The neighborhood marquee scrolls continuously (CSS animation), pauses on hover, static under reduced-motion.

---

## 3. Page structure & copy (build in this exact order)

### Nav (sticky, white, hairline bottom border on scroll)
Logo left. Links: Services, Our Work, Process, About, Service Areas, FAQ (anchor links for now — this is a one-page build). Right: phone number `215-888-4384` (tel: link, medium weight) + primary button "Get a Free Estimate" (scrolls to Project Builder). Mobile: hamburger → full-screen overlay menu in the same type system.

### Section 1 — HERO (split layout, text left / 2×2 service cards right)
Recreate this exact structure:
- **Left column:**
  - Eyebrow: `[ PHILADELPHIA GENERAL CONTRACTOR ]` (orange)
  - **H1:** `You Dream It; We Build It.` — "Build" in blue. Include visually-hidden or small-styled lead-in so the full H1 semantically reads: "Philadelphia General Contractor — You Dream It; We Build It." (style the location part as the small eyebrow line inside the h1; the big visual words remain the brand line)
  - Short blue underline accent bar
  - Subline: `Full builds, kitchen & bath remodels, framing, and concrete — serving Philadelphia, Fishtown, Northern Liberties, and nearby Montgomery County.`
  - Buttons: primary `Get a Free Estimate` (→ Project Builder), secondary outline `View Our Work` (→ projects section)
- **Right column:** 2×2 grid of tall image cards, each a real link with photo, small white icon chip, title, one-liner, and a circular arrow chip (blue → orange on hover):
  1. **Kitchen & Bathrooms** — "Beautiful. Functional. Built for life."
  2. **Framing** — "Strong starts. Solid results."
  3. **Concrete** — "Durable. Precise. Built to perform."
  4. **Full Build & Remodeling** — "From concept to completion."
- **Full-width trust bar below** (white card, 3 cells):
  - 🛡 "Built on Trust. Backed by Experience." / "Licensed & Insured · Quality Guaranteed"
  - 👥 "Local. Reliable. Results That Last." / "Proudly serving Philadelphia"
  - 📞 "Ready to get started?" / "Call us today **215-888-4384**" (number in blue, tel: link)

### Section 2 — Neighborhood marquee
Thin full-width strip, continuously scrolling display-font text separated by small orange diamonds:
`Fishtown ◆ Northern Liberties ◆ Center City ◆ Queen Village ◆ Port Richmond ◆ East Kensington ◆ Graduate Hospital ◆ Rittenhouse ◆ Ambler ◆ Blue Bell ◆ Montgomery County` (loop seamlessly, aria-hidden duplicate for the loop).

### Section 3 — Services
Eyebrow `[ WHAT WE BUILD ]`. H2: `Built for How You **Live**.` "View all services →" link top-right.
Woodworked-style row of **5 tall portrait cards** (image fills card, name + one-liner at bottom over gradient scrim, arrow chip):
1. Kitchen & Bathroom Remodeling — "The rooms that sell homes — and make them home."
2. Full Builds & Remodeling — "Ground-up construction and whole-home renovations."
3. Framing — "The bones of the build, done right the first time."
4. Concrete — "Foundations, sidewalks, pads, and driveways."
5. General Contracting — "Permits, management, and every trade in between."
Each card is an `<a>` (href="#" with TODO comment for future service page URLs). Horizontal scroll-snap on mobile.

### Section 4 — Recent Projects (Remodix alternating showcase)
Eyebrow `[ RECENT PROJECTS ]`. H2: `Real Streets. Real **Results**.`
Three featured projects, alternating text/image sides, each with labeled metadata fields (small caps labels, like structured data made visible):
1. **1502 Hancock Street** — Neighborhood: Fishtown · Project type: Full Build · Scope: Custom kitchen, custom bathrooms, custom stairs
2. **1855 E Huntingdon Street** — Neighborhood: East Kensington · Project type: Full Build · Scope: Custom kitchen, custom bathrooms, custom stairs
3. **766 S Front Street** — Neighborhood: Queen Village · Project type: Property Rehab · Scope: Custom kitchen
Each has a short 2-sentence description written in first person plural, plain and specific (e.g., "A full gut renovation three blocks from Frankford Ave. We took this rowhome down to the studs and rebuilt it — new framing, new kitchen, two custom baths."). Photo collage of 2–3 images per project. "View project →" links (TODO hrefs). Button below: `View All Projects`.

### Section 5 — Reviews
Eyebrow `[ WHAT CLIENTS SAY ]`. H2: `Word **Travels** on Every Block.`
Row of 3–4 review cards (star row, quote, name + neighborhood). Use clearly-marked placeholder reviews with `<!-- TODO: replace with real Google reviews before launch -->`. Placeholder pattern: "Placeholder — real client review goes here. Two to three sentences about communication, timeline, and finish quality." — Name, Neighborhood. Link under the row: "Read our reviews on Google →" (TODO href). **Do not add review schema in this build.**

### Section 6 — Project Builder ⭐ (the signature element)
Eyebrow `[ START YOUR PROJECT ]`. H2: `Price Your Project in **60 Seconds**.` Orange chip: "Takes about 60 seconds — no obligation."
A polished multi-step card (white, soft shadow, progress bar in blue):
- **Step 1 — Project type:** icon-button grid: Kitchen · Bathroom · Full Build / Remodel · Concrete · Framing · Something else
- **Step 2 — The property:** Rowhome · Twin · Detached · Multi-unit / Investment · Commercial; plus timeline chips: ASAP · 1–3 months · 3–6 months · Just planning
- **Step 3 — Location:** neighborhood/ZIP text input
- **Step 4 — Contact:** Name, Phone, Email → button `Get My Free Estimate`
Behavior: front-end only. Steps animate (slide/fade), Back/Next controls, keyboard accessible, progress bar updates. On submit: show a success state ("Got it — we'll reach out within one business day. Or call us now: 215-888-4384") and `console.log` the payload as JSON. Include a clearly commented stub: `// TODO: POST payload to GHL webhook`. Fire a `dataLayer.push` event on every step advance and on submit (guard for undefined dataLayer). Next to the card, quiet escape hatch: "Prefer to talk it through? **Call 215-888-4384**."

### Section 7 — Process
Eyebrow `[ HOW IT WORKS ]`. H2: `From First Call to Final **Walkthrough**.`
Four numbered cards (numbers in display font — this content is a true sequence, so numbering is earned):
1. **Free Estimate** — "Call or send your project. We come out, look at everything, and give you a real number."
2. **Design & Proposal** — "Scope, materials, timeline, and price — agreed on paper before we start."
3. **The Build** — "Owner on site. Clean job site. You always know what's happening and when."
4. **Walkthrough & Warranty** — "We walk every inch together. It's done when you say it's done."

### Section 8 — Why Paiz / About (merged, Woodworked "values" layout)
Eyebrow `[ WHY PAIZ ]`. H2: `Family Owned. **Owner** on Every Project.`
Left: large crew/owner photo placeholder. Right: one short paragraph (adapted, people-first): `Paiz Builders is a family-owned Philadelphia contractor with 20+ years in the trades. In an industry full of unreturned calls and blown timelines, we run on the opposite: the owner is on every project, the site stays clean, and you always know what's happening next. We build like the block is watching — because it is.`
Below it a 2×2 icon grid: **Owner-Operated** · **20+ Years Experience** · **Licensed & Insured** · **Communication First** (one line each). Stats row baked into this section (Remodix-style large numerals): `100+ Projects Completed · 20+ Years Experience · 5.0★ Client Rating`. Link: "More about us →".

### Section 9 — Service Areas
Eyebrow `[ WHERE WE WORK ]`. H2: `Philadelphia Is **Home** Base.`
Short intro: `Headquartered at 3146 Frankford Ave, we build across the city and into nearby Montgomery County.` Then a clean linked grid (chips or two-column list) of areas: Fishtown, Northern Liberties, East Kensington, Port Richmond, Center City, Queen Village, Graduate Hospital, Rittenhouse Square, Fairmount, South Philadelphia, Chestnut Hill, Ambler, Blue Bell, Conshohocken. Each is an `<a>` with TODO href for future area pages.

### Section 10 — FAQ
Eyebrow `[ QUESTIONS ]`. H2: `Straight **Answers**.`
Accessible accordion (`<details>/<summary>` styled, or button+region with aria-expanded). Six items:
1. **Are you licensed and insured in Philadelphia?** — "Yes. Paiz Builders is fully licensed and insured for residential and commercial work in Philadelphia and Pennsylvania. <!-- TODO: insert license number -->"
2. **Do you handle permits?** — "Yes. We handle permitting, inspections, and scheduling with L&I as part of the job."
3. **How much does a kitchen remodel cost in Philadelphia?** — "Most of our kitchen remodels land between $X and $X depending on size, layout changes, and finishes. A full gut with custom cabinetry runs higher. Every estimate is free and itemized. <!-- TODO: confirm real ranges with client — do not launch with X placeholders -->"
4. **How long does a full renovation take?** — realistic timeline answer with a TODO to confirm typical ranges.
5. **What areas do you serve?** — city + Montgomery County answer, naming key neighborhoods.
6. **Do you do small projects, or only full builds?** — "Both..." honest answer.

### Section 11 — Final CTA (dark full-bleed band)
`--ink` background with a dark-treated project photo. Small floating service tag chips at top (Kitchens · Bathrooms · Full Builds · Concrete · Framing — anchor links). Huge display headline: `Ready to Build in **Philadelphia**?` (accent word in a lighter blue that passes contrast on dark). Subline: `Free estimates. Straight answers. A builder who picks up the phone.` **The orange button:** `Get a Free Estimate` + secondary ghost button `Call 215-888-4384`.

### Footer
Four columns on `--ink` (or very dark) background:
1. Logo + one-liner + social links (Instagram: https://www.instagram.com/paiz_construction/ — TODO confirm new handle; Facebook TODO).
2. **Services** links (the five services).
3. **Service Areas** links (top 6–8 neighborhoods).
4. **Contact / NAP block** (must be crawlable text, exact format): `Paiz Builders · 3146 Frankford Ave, Philadelphia, PA 19134 · 215-888-4384 · PaizGC@gmail.com` <!-- TODO: confirm ZIP and email on GBP match exactly -->
Bottom bar: `© 2026 Paiz Builders. All rights reserved.` + "Site by Legacy LinQ Digital" link.

---

## 4. SEO requirements (non-negotiable)

- `<title>`: `Paiz Builders | General Contractor in Philadelphia — Kitchens, Baths & Full Builds`
- Meta description (~155 chars): `Family-owned Philadelphia general contractor. Kitchen & bath remodels, full builds, framing & concrete in Fishtown, Northern Liberties & beyond. Free estimates.`
- Canonical tag (placeholder domain, TODO comment), `og:` and `twitter:` meta set, `lang="en"`, favicon placeholder.
- **JSON-LD, exactly two blocks:**
  1. `GeneralContractor` (LocalBusiness subtype): name Paiz Builders, telephone +1-215-888-4384, address 3146 Frankford Ave, Philadelphia PA 19134 (TODO confirm ZIP), areaServed listing the neighborhoods + Montgomery County, url placeholder, sameAs Instagram.
  2. `FAQPage` mirroring the six FAQ items word-for-word.
  No other schema. No review/rating schema in this build.
- Every placeholder image gets a real descriptive `alt` (e.g., `alt="Custom kitchen remodel in a Fishtown rowhome by Paiz Builders"`).
- All internal links are real `<a href>` elements (anchors for now), never JS-only navigation.
- First 100 words of rendered body copy naturally include: general contractor, Philadelphia, kitchen, bathroom, remodeling.

---

## 5. Build process & acceptance criteria

Before writing code, briefly restate your design plan (tokens, type scale, signature element = the Project Builder) and confirm it matches this spec — then build. Do not substitute fonts, colors, section order, or copy. Where copy is specified above, use it verbatim; where it isn't, write in the same plainspoken voice.

Done means:
- [ ] Renders correctly at 1440 / 768 / 375 with no horizontal scroll
- [ ] One H1; heading tree validates; landmarks present
- [ ] Project Builder: all 4 steps work, keyboard accessible, success state + console payload + dataLayer events
- [ ] Sticky mobile call bar works (`tel:` link)
- [ ] Marquee loops seamlessly; all motion off under `prefers-reduced-motion`
- [ ] Both JSON-LD blocks validate (no syntax errors)
- [ ] Orange appears only in its five sanctioned jobs; page reads ~90% neutral
- [ ] Zero lorem ipsum anywhere; every TODO is an HTML comment, not visible text
- [ ] Lighthouse-minded: lazy-loaded below-fold images, aspect-ratios set, fonts with `display=swap`
