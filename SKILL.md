---
name: brand-style-resume
description: Create company-design-inspired resumes as responsive HTML and A4 PDF from Markdown or PDF, including scanned resumes with agent-assisted visual recognition. Use for Apple, Material, Fluent, Carbon, Ant, TDesign, Arco, Semi, HarmonyOS, Baidu DLS, Spectrum or Lightning resume styling, including 大厂风格简历 and 公司风格简历.
---

# Brand Style Resume

Create a resume using a selected company's design language. Read [DESIGN.md](DESIGN.md), then only the selected style's linked DESIGN.md. Preserve facts, wording, language and section order. These are independent visual adaptations, not official templates or evidence of hiring preference.

## Choose inputs and style

- Accept Markdown, a text PDF or a scanned/mixed PDF, plus an output directory.
- If style is missing, show the 12 choices from `python scripts/md_to_resume.py --list-styles` and ask the user to choose. Clarify company-only requests when multiple systems apply, such as ByteDance Arco versus Douyin Semi.
- If no photo was supplied, ask whether to upload a JPG/PNG or continue without a photo. Wait for the choice; do not invent an avatar. A prior choice to omit photos remains valid.
- Use `--lang zh-CN` (default) or `--lang en` for interface labels. This does not translate the body. Translate only when asked.
- Locate this installed skill's directory and use absolute script paths, or run from that directory. Do not assume the caller's working directory contains the scripts.

## Prepare Markdown

Read [references/markdown-parsing.md](references/markdown-parsing.md). Keep the original untouched and normalize a working copy into a single H1 name, header contacts and H2 sections. Generic sections support paragraphs, H3 headings, bold/italic text, safe HTTP(S) links and lists. Preserve skills, projects, certificates, awards, publications and unfamiliar sections; do not discard them to fit the legacy schema. Ask about factual uncertainties instead of filling gaps.

## Prepare PDF

Read [references/pdf-input.md](references/pdf-input.md) and run:

```bash
python -m pip install -r requirements-input.txt
python scripts/prepare_pdf.py input.pdf --output work/pdf-input
```

Read `manifest.json` and inspect EVERY page preview alongside its text. Recover column order and image-only content even on pages with extracted text. Use the current agent's available visual/OCR capabilities for scans and mixed pages. Write a verified working `source.md`; do not feed raw extraction directly into the renderer. Ask about unresolved names, dates, numbers or other facts before final generation. If visual/OCR capabilities are unavailable, explain which pages cannot be read and request a readable source; the preparation script is not OCR.

## Generate and export

```bash
python scripts/md_to_resume.py source.md output --style ibm-carbon --lang en
python scripts/md_to_resume.py source.md output --style ant-design --photo portrait.png
# Legacy form remains available; default style is Apple.
python scripts/md_to_resume.py source.md portrait.png output --lang zh-CN
```

HTML generation uses the Python standard library. Outputs: `index.html`, `resume_a4.html`, `source.md`, and a photo copy when supplied. CSS is embedded, so HTML does not depend on the installed skill folder.

Local fonts and documented system fallbacks are the default. For optional open web fonts, pass `--web-fonts` and wait for fonts before exporting. Apple retains Inter / Noto Sans SC; other styles have their documented stacks. Proprietary fonts are neither downloaded nor bundled. Disclose missing brand fonts and possible line-wrap differences.

```bash
python -m pip install -r requirements-pdf.txt
python -m playwright install chromium
python scripts/export_pdf.py output/resume_a4.html --output output/resume.pdf
```

Alternatively print the A4 HTML with CSS margins, background graphics on and browser headers/footers off. Allow long content to flow without truncation or over-shrinking. Apple retains employer page breaks; other styles flow naturally.

## Verify and deliver

Inspect desktop and mobile web layouts and every rendered PDF page. Compare text against the prepared Markdown, including additional sections, links, dates and numbers. Fix clipping, missing glyphs, overflow, broken photos, orphan headings and unexpected blank pages.

Return local links to the HTML and PDF, plus verified Markdown for PDF inputs. Upload or deploy only when requested. Public examples must be separately authored fictional content, following [references/sample-sources.md](references/sample-sources.md); blurring a real resume is insufficient.
