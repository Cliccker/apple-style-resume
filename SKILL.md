---
name: apple-style-resume
description: Generate an Apple-inspired static HTML and A4 PDF resume from structured Markdown and a JPG or PNG portrait. Use for Apple-style resume requests, including 苹果风格简历, with Chinese or English interface labels.
---

# Apple Style Resume

Create a restrained, card-based resume using the included templates and scripts. Read [DESIGN.md](DESIGN.md) before changing visual components. Preserve the user's facts and wording; do not invent experience, achievements or credentials.

## Inputs and language

- A structured Markdown resume and a JPG/PNG portrait. If either is missing, request the missing input before running the generator.
- An output directory chosen for the user's deliverables.
- Use `--lang zh-CN` for Chinese labels (default) or `--lang en` for English. This controls headings and HTML language, not translation of the resume body. Translate content only when requested.
- Read [references/markdown-parsing.md](references/markdown-parsing.md) when preparing or adapting Markdown. For unfamiliar source structures, reorganize a working copy without dropping or inventing facts.

## Typography

Keep **Inter** for Latin text and **Noto Sans SC** for Simplified Chinese at the front of the font stack. Recommend local installation from the sources linked in the README for consistent offline output. System fonts are fallbacks; they can change wrapping and pagination. If the user prefers online fonts, pass `--web-fonts` to load both families from Google Fonts. Do not silently replace the original fonts with a different design.

## Generate

Locate this installed skill directory and run its script using an absolute path or from that directory; do not assume the current working directory is the skill directory. The generator uses only the Python standard library.

```bash
python scripts/md_to_resume.py resume.md portrait.png output --lang zh-CN
python scripts/md_to_resume.py resume.md portrait.png output --lang en --web-fonts
```

The original three-positional-argument form remains supported. The generator creates:

- `index.html`: responsive web resume.
- `resume_a4.html`: print layout with A4 dimensions and 16mm/18mm margins.
- `photo.jpg`, `photo.jpeg` or `photo.png`: portrait copy, preserving the input extension.

Empty sections are omitted. Subsequent employers begin on a new PDF page. Let long content flow; do not force every resume onto one or two pages. Do not truncate user content to achieve a page count.

## Export PDF

PDF export needs the optional Playwright dependency and Chromium:

```bash
python -m pip install -r requirements-pdf.txt
python -m playwright install chromium
python scripts/export_pdf.py output/resume_a4.html --output output/resume.pdf
```

On Linux, install Chromium's OS dependencies using Playwright's documented setup if needed. Alternatively, open the A4 HTML in a browser and print to PDF using A4, CSS margins, background graphics on, and browser headers/footers off.

Wait for fonts and images to load before printing. Inspect every PDF page and the web layout at desktop and mobile widths. Check missing glyphs, line wrapping, overflow and broken images. If fonts are unavailable, explain the fallback and its possible pagination differences.

## Delivery and privacy

Return local links to the HTML and PDF. Upload or deploy a user's resume only when requested. This repository's examples are entirely fictional, but actual generated resumes contain the user's supplied information and are not automatically anonymized. For public demonstrations, build a separate fictional example from scratch and inspect HTML, PDF, image metadata and links before sharing; blurring a real resume is insufficient.
