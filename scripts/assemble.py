"""Assemble dist/index.html: one self-contained page.

Inlines d3 and data/story_data.json into src/template.html. The page uses the
reader's system font, so there are no font files to embed.
Usage: python scripts/assemble.py
"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
d3 = (ROOT / "vendor/d3.min.js").read_text(encoding="utf-8")
data = (ROOT / "data/story_data.json").read_text(encoding="utf-8")
assert "</script" not in d3.lower() and "</script" not in data.lower()
html = (ROOT / "src/template.html").read_text(encoding="utf-8")
for token in ("/*__D3__*/", "/*__DATA__*/"):
    assert token in html, f"missing placeholder {token}"
html = html.replace("/*__D3__*/", d3).replace("/*__DATA__*/", data)
(ROOT / "dist").mkdir(exist_ok=True)
# write bytes so the output is UTF-8 with LF endings on every OS (Windows text mode would add CRLF)
(ROOT / "dist/index.html").write_bytes(html.encode("utf-8"))
print(f"wrote dist/index.html ({len(html):,} bytes)")
