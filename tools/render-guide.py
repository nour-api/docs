#!/usr/bin/env python3
"""Render the canonical guide and optionally synchronize the second static site."""
import argparse
import html
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--mirror', type=Path, help='Local nour-api.github.io checkout')
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
source = json.loads((root / 'guide/source.json').read_text())
escape = html.escape
navigation = ''.join(f'<li><a href="#{escape(s["id"])}">{escape(s["title"])}</a></li>' for s in source['sections'])
sections = []
for section in source['sections']:
    parts = [f'<section id="{escape(section["id"])}"><h2>{escape(section["title"])}</h2>']
    parts += [f'<p>{escape(p)}</p>' for p in section.get('paragraphs', [])]
    if 'code' in section:
        parts.append(f'<pre><code>{escape(section["code"])}</code></pre>')
    if 'example' in section:
        example = (root / section['example']).read_text()
        parts.append(f'<pre><code>{escape(example)}</code></pre>')
    parts.append('</section>')
    sections.append(''.join(parts))
page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nour-API engineering guide</title>
<style>body{font:18px/1.65 system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 1.2rem;color:#172033;background:#fafbfd}a{color:#125a9d}pre{overflow:auto;background:#142034;color:#eaf2ff;padding:1rem;border-radius:8px;font-size:14px}section{margin:3rem 0}nav ul{columns:2}h1,h2{line-height:1.25}p{overflow-wrap:anywhere}@media(max-width:600px){nav ul{columns:1}}</style>
</head><body><main><h1>Nour-API engineering guide</h1><p>Nour-API 2.2 reference: framework and application 2.2.0, installer 2.1.0.</p><nav aria-label="Contents"><ul>'''+navigation+'</ul></nav>'+''.join(sections)+'</main></body></html>\n'
targets = [root / 'guide/index.html']
if args.mirror:
    if not (args.mirror / '.git').is_dir():
        raise SystemExit('Mirror must be an existing local Git checkout.')
    targets.append(args.mirror / 'guide/index.html')
for target in targets:
    if args.check:
        if not target.is_file() or target.read_text() != page:
            raise SystemExit(f'Guide is out of date: {target}')
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page)
print('PASS: guide matches canonical source' if args.check else 'Rendered guide locally')
