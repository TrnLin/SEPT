#!/usr/bin/env python3
"""Copy tokens.css into the <style id="tokens"> block of every mockup page.

Run after editing tokens.css. Each page keeps its own copy so it still works as a single file:
file previews (like the T3 Code viewer) show one HTML file and can't load ../shared/tokens.css.
"""
import pathlib
import re
import sys

here = pathlib.Path(__file__).resolve().parent
tokens = (here / "tokens.css").read_text().strip()
if "</style" in tokens:
    sys.exit("tokens.css must not contain '</style'")
pages = sorted(here.parent.glob("*/index.html"))

for page in pages:
    text = page.read_text()
    # [^<]* can't run past the block's own </style>, so the page's other stylesheets are never touched.
    text, count = re.subn(
        r'<style id="tokens">[^<]*</style>',
        lambda m: f'<style id="tokens">\n{tokens}\n</style>',
        text,
    )
    if count != 1:
        sys.exit(f'{page}: <style id="tokens"> block not found')
    page.write_text(text)
    print(f"Synced tokens into {page.relative_to(here.parent)}")
