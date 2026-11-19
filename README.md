# How Indonesia Uses ChatGPT Differently

A data story of how Indonesians work more (and chat less) with ChatGPT. One self-contained HTML page with ten D3 charts.

Read it at https://akbsaputra.github.io/chatgpt-use/.

## Run it

Open `dist/index.html` in a browser. Nothing else is needed.

## Change it

Use `python3` instead of `python` if that is what your system calls it.

```bash
pip install -r requirements.txt
# edit src/template.html (prose, styles, chart code), then:
python scripts/assemble.py         # rebuilds dist/index.html
# only if the data logic changes:
python scripts/build_data.py       # rebuilds data/story_data.json
```

`docs/project-notes.md` describes the structure, design system, data rules, and decisions made so far. `docs/findings.md` lists the numbers behind each section.

## Credits

Data: OpenAI Signals v3.0, licensed CC BY 4.0. Charts: D3 v7 (ISC license). The page uses the reader's system font. Its layout borrows from the ChatGPT app, and it is not affiliated with OpenAI.
