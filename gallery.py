#!/usr/bin/env python3
"""Generate a self-contained slideshow HTML for a session directory."""
from __future__ import annotations

import argparse
import html
import json
import os


def build(sessions_dir: str, output: str, interval: int = 8000) -> int:
    slides = []
    if os.path.isdir(sessions_dir):
        for name in sorted(os.listdir(sessions_dir)):
            manifest = os.path.join(sessions_dir, name, "session.json")
            if not os.path.exists(manifest):
                continue
            with open(manifest, encoding="utf-8") as fh:
                m = json.load(fh)
            img = os.path.relpath(m["image"]["path"], output).replace(os.sep, "/")
            slides.append({
                "image": img,
                "excerpt": m.get("excerpt", ""),
                "text": m.get("text", ""),
                "style": m.get("style", ""),
            })
    cards = "\n".join(
        f'<div class="slide"><img src="{html.escape(s["image"])}" alt="">'
        f'<div class="cap"><h1>{html.escape(s["excerpt"])}</h1>'
        f'<p>{html.escape(s["text"][:300])}</p>'
        f'<small>{html.escape(s["style"])}</small></div></div>'
        for s in slides
    ) or '<div class="slide"><div class="cap"><h1>No sessions yet</h1></div></div>'
    doc = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Poetry Wall</title><style>
html,body{{margin:0;background:#0d0c10;color:#eee;font-family:Georgia,serif;height:100%}}
.slide{{position:absolute;inset:0;display:none;align-items:center;justify-content:center;opacity:0;transition:opacity 1s}}
.slide.active{{display:flex;opacity:1}}
img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55}}
.cap{{position:relative;max-width:760px;padding:40px;text-shadow:0 2px 12px #000}}
h1{{font-size:3rem;margin:0 0 20px}}p{{font-size:1.4rem}}small{{opacity:.6}}
</style></head><body>{cards}
<script>
const s=[...document.querySelectorAll('.slide')];let i=0;
setInterval(()=>{{s[i].classList.remove('active');i=(i+1)%s.length;s[i].classList.add('active')}},{interval});
if(s[0])s[0].classList.add('active');
</script></body></html>"""
    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    with open(output, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return len(slides)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions", default="sessions")
    ap.add_argument("--output", default="gallery.html")
    ap.add_argument("--interval", type=int, default=8000)
    a = ap.parse_args()
    print(f"slides: {build(a.sessions, a.output, a.interval)} -> {a.output}")
