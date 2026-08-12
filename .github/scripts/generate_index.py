#!/usr/bin/env python3
"""Generates index.html from catalog.json for GitHub Pages deployment."""

import json
import os
import sys

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
CATALOG_PATH = os.path.join(REPO_ROOT, "catalog.json")
OUTPUT_PATH = os.path.join(REPO_ROOT, "index.html")


def badge(trust_level: str) -> str:
    if trust_level == "verified":
        return '<span class="badge verified">verified</span>'
    return '<span class="badge community">community</span>'


def tag_chips(tags: list) -> str:
    return " ".join(f'<span class="tag">{t}</span>' for t in tags)


def plugin_card(p: dict) -> str:
    source = p.get("source", {})
    repo = source.get("repo", "")
    ref = source.get("ref", "")
    release_url = (
        f"https://github.com/{repo}/releases/tag/{ref}" if repo and ref else p["homepage"]
    )

    return f"""
    <article class="card">
      <div class="card-header">
        <h2><a href="{p['homepage']}">{p['name']}</a></h2>
        {badge(p['trust_level'])}
        <span class="version">v{p['latest_version']}</span>
      </div>
      <p class="description">{p['description']}</p>
      <div class="meta">
        <span class="author">by <a href="https://github.com/{p['author']}">{p['author']}</a></span>
        {tag_chips(p.get('tags', []))}
      </div>
      <div class="card-footer">
        <a class="btn" href="plugins/{p['slug']}.html">Details</a>
        <a class="btn secondary" href="{release_url}">Release {ref}</a>
      </div>
    </article>"""


def generate(catalog: dict) -> str:
    plugins = catalog.get("plugins", [])
    updated_at = catalog.get("updated_at", "")
    cards = "\n".join(plugin_card(p) for p in plugins)
    count = len(plugins)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>deckwatch marketplace</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #0d1117;
      color: #e6edf3;
      line-height: 1.6;
      padding: 2rem 1rem;
    }}
    a {{ color: #58a6ff; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    header {{
      max-width: 900px;
      margin: 0 auto 3rem;
      border-bottom: 1px solid #21262d;
      padding-bottom: 1.5rem;
    }}
    header h1 {{ font-size: 2rem; font-weight: 700; margin-bottom: .5rem; }}
    header p {{ color: #8b949e; }}
    header .links {{ margin-top: .75rem; font-size: .9rem; }}
    header .links a {{ margin-right: 1.25rem; }}
    .catalog-meta {{
      max-width: 900px;
      margin: 0 auto 1.5rem;
      font-size: .85rem;
      color: #8b949e;
    }}
    .grid {{
      max-width: 900px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
      gap: 1.25rem;
    }}
    .card {{
      background: #161b22;
      border: 1px solid #21262d;
      border-radius: 8px;
      padding: 1.25rem 1.5rem;
    }}
    .card-header {{
      display: flex;
      align-items: center;
      gap: .6rem;
      margin-bottom: .6rem;
      flex-wrap: wrap;
    }}
    .card-header h2 {{ font-size: 1.1rem; font-weight: 600; }}
    .card-header h2 a {{ color: #e6edf3; }}
    .version {{ font-size: .8rem; color: #8b949e; }}
    .badge {{
      font-size: .72rem;
      font-weight: 600;
      padding: .15rem .5rem;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}
    .badge.verified {{ background: #1f4a2e; color: #3fb950; border: 1px solid #3fb950; }}
    .badge.community {{ background: #2d2200; color: #d29922; border: 1px solid #d29922; }}
    .description {{ color: #c9d1d9; font-size: .92rem; margin-bottom: .75rem; }}
    .meta {{ display: flex; align-items: center; gap: .5rem; flex-wrap: wrap; font-size: .82rem; margin-bottom: 1rem; }}
    .author {{ color: #8b949e; }}
    .tag {{
      background: #21262d;
      border: 1px solid #30363d;
      border-radius: 999px;
      padding: .1rem .55rem;
      font-size: .75rem;
      color: #8b949e;
    }}
    .card-footer {{ display: flex; gap: .6rem; }}
    .btn {{
      display: inline-block;
      padding: .35rem .85rem;
      border-radius: 6px;
      font-size: .85rem;
      font-weight: 500;
      background: #238636;
      color: #fff;
      border: 1px solid #2ea043;
    }}
    .btn:hover {{ background: #2ea043; text-decoration: none; }}
    .btn.secondary {{ background: #21262d; color: #c9d1d9; border-color: #30363d; }}
    .btn.secondary:hover {{ background: #30363d; }}
    footer {{
      max-width: 900px;
      margin: 3rem auto 0;
      padding-top: 1.5rem;
      border-top: 1px solid #21262d;
      font-size: .82rem;
      color: #8b949e;
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: .5rem;
    }}
  </style>
</head>
<body>
  <header>
    <h1>deckwatch marketplace</h1>
    <p>Official plugin catalog for the <a href="https://github.com/alexconrey/deckwatch">deckwatch</a> Kubernetes operator.</p>
    <div class="links">
      <a href="catalog.json">catalog.json</a>
      <a href="https://github.com/alexconrey/deckwatch-marketplace/blob/main/CONTRIBUTING.md">Submit a plugin</a>
      <a href="https://github.com/alexconrey/deckwatch-marketplace">GitHub</a>
    </div>
  </header>

  <div class="catalog-meta">
    {count} plugin(s) &nbsp;&middot;&nbsp; updated {updated_at}
  </div>

  <div class="grid">
{cards}
  </div>

  <footer>
    <span>Fetched by deckwatch from <code>https://market.deckwatch.io/catalog.json</code></span>
    <span>Updated {updated_at}</span>
  </footer>
</body>
</html>
"""


def main() -> int:
    try:
        with open(CATALOG_PATH, encoding="utf-8") as f:
            catalog = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Failed to read catalog.json: {exc}", file=sys.stderr)
        return 1

    html = generate(catalog)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated index.html ({len(catalog.get('plugins', []))} plugin(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
