#!/usr/bin/env python3
"""Embed the vehicle models from assets/models/ into index.html.

Run after re-exporting a vehicle from Blender. Embedding keeps index.html a single
file that opens straight from disk (browsers block loading a .glb over file://).
"""
import base64
import pathlib
import re
import sys

here = pathlib.Path(__file__).resolve().parent
models = here.parents[1] / "models"
html = here / "index.html"
blocks = {"car-glb": "rentxe-car.glb", "bike-glb": "rentxe-bike.glb"}

text = html.read_text()
for block_id, filename in blocks.items():
    glb = models / filename
    data = base64.b64encode(glb.read_bytes()).decode()
    text, count = re.subn(
        rf'(<script id="{block_id}" type="application/octet-stream">)[^<]*(</script>)',
        lambda m: m.group(1) + data + m.group(2),
        text,
    )
    if count != 1:
        sys.exit(f'index.html: <script id="{block_id}"> block not found')
    print(f"Embedded {filename} ({glb.stat().st_size // 1024} KB)")
html.write_text(text)
