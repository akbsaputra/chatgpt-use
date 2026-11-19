"""Screenshot sections of dist/index.html for visual checks.

Usage: python scripts/shot.py WIDTH HEIGHT TAG TARGET [TARGET ...]
  TARGET is one of:
    top                      the opening sheet
    section:step             a scroll step, e.g. drift:3 or young:1
    a CSS selector           e.g. '[data-fig="topics"]' or '#closing'
Examples:
  python scripts/shot.py 1440 900 d top drift:0 drift:3 '[data-fig="iwa"]'
  python scripts/shot.py 390 844 m hundred:2 '[data-fig="percap"]'
Needs: pip install playwright, plus a Chrome or Chromium. Set CHROME=/path/to/chrome
to use an installed browser, or run `playwright install chromium` once.
Output goes to shots/.
"""
import sys, os, re, asyncio, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent

async def main(w, h, tag, targets):
    (ROOT / "shots").mkdir(exist_ok=True)
    async with async_playwright() as p:
        kw = {"executable_path": os.environ["CHROME"]} if os.environ.get("CHROME") else {}
        b = await p.chromium.launch(args=["--no-sandbox"], **kw)
        pg = await b.new_page(viewport={"width": w, "height": h})
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "dist/index.html").as_uri())
        await pg.wait_for_timeout(4800)  # opening animation
        for t in targets:
            if t == "top":
                await pg.evaluate("window.scrollTo(0,0)")
            elif re.fullmatch(r"[\w-]+:\d+", t):
                sec, step = t.split(":")
                await pg.evaluate(f"(()=>{{const e=document.querySelectorAll('#{sec} .step')[{step}];const r=e.getBoundingClientRect();window.scrollTo(0,window.scrollY+r.top+r.height/2-innerHeight/2);}})()")
            else:
                await pg.evaluate(f"(()=>{{const e=document.querySelector('{t}');const r=e.getBoundingClientRect();window.scrollTo(0,window.scrollY+r.top-20);}})()")
            await pg.wait_for_timeout(1900)
            name = re.sub(r"[^\w-]+", "_", t).strip("_")
            await pg.screenshot(path=str(ROOT / f"shots/{tag}_{name}.png"))
        print("page errors:", errs[:6])
        await b.close()

if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4:]))
