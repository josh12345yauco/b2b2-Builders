#!/usr/bin/env python3
"""Authoring tool, not a runtime build step.

Stamps the canonical shared header/footer (partials/header.html,
partials/footer.html) into every page between marker comments, so the
chrome stays byte-identical sitewide. Output is committed static HTML.

Usage: python3 tools/inject_partials.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADER = (ROOT / "partials/header.html").read_text()
FOOTER = (ROOT / "partials/footer.html").read_text()
HEAD_COMMON = (ROOT / "partials/head-common.html").read_text()

MARKERS = [
    ("<!-- HEAD-COMMON-START -->", "<!-- HEAD-COMMON-END -->", HEAD_COMMON),
    ("<!-- SITE-HEADER-START -->", "<!-- SITE-HEADER-END -->", HEADER),
    ("<!-- SITE-FOOTER-START -->", "<!-- SITE-FOOTER-END -->", FOOTER),
]

changed = 0
for path in sorted(ROOT.rglob("index.html")):
    if "partials" in path.parts or "tools" in path.parts:
        continue
    html = original = path.read_text()
    for start, end, content in MARKERS:
        if start not in html or end not in html:
            print(f"WARN missing markers in {path.relative_to(ROOT)}")
            continue
        pattern = re.escape(start) + r".*?" + re.escape(end)
        html = re.sub(pattern, start + "\n" + content + end, html, flags=re.S)
    if html != original:
        path.write_text(html)
        changed += 1
print(f"stamped {changed} pages")
