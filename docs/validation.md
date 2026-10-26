# Validation record

Date: 2026-10-26. All candidate data and PDF fixtures are fictional.

## Automated checks

- `python -m unittest discover -s tests -v`: **17 tests passed**, including the original eight. Optional PDF input tests ran, not skipped.
- The new profile matrix exercises 12 profiles × 12 styles × two HTML layouts (288 renders), checking equal visible content across styles, optional photos, additional/repeated sections, escaping and CLI compatibility.
- Skill creator `quick_validate.py`: **Skill is valid** for `brand-style-resume`.
- `scripts/build_previews.py`: built 24 bilingual style previews plus six career previews. Every preview has actual HTML, PDF, desktop/mobile screenshots and rendered PDF pages. At 1280×1000 and 390×844 viewport sizes, all 60 web checks reported no horizontal overflow or broken images. See [geometry results](preview-checks.json).
- `scripts/verify_previews.py`: **30 PDFs / 39 pages** retain every meaningful HTML text node after whitespace/punctuation normalization; no blank pages or glyph bounding boxes outside page bounds. See [PDF results](pdf-checks.json). Text checks complement rather than replace visual review.
- Local documentation links and the 12 design/CSS references resolve. Generated HTML embeds its CSS and does not refer to the developer's filesystem. `git diff --check` passed.

## Visual review

Reviewed the desktop and mobile contact sheets for all 24 style/language pairs and rendered-page contact sheets for all 39 output pages. Inspected full-size Chinese print output and the four PDF input scenarios. No clipping, overlapping text, broken images, visibly missing glyphs or stranded section headings were observed. The backend career sample spans three pages with continuous long content. Apple intentionally retains its employer page breaks.

The styles differ in header composition, section treatment, typography, project grouping, shape and spacing, including desktop label/content grids that collapse on mobile. Print uses solid surfaces and a single reading column.

Some English baseline examples naturally have a short final section on their second page. No content was removed or font size reduced to force a page count. Local font availability can change these breaks.

## PDF recognition exercise

Used the new skill's preparation workflow to render and inspect every source page. Independently transcribed the visible fixture content into working Markdown under the ignored `output/pdf-review/` directory, then compared it with the stored expected Markdown and rendered it using Fluent:

| Input | Observed and recovered |
| --- | --- |
| `text-single.pdf` | Alex Example; Backend Engineer; Example Lab; 2022–2026; 120 requests; failures 9 to 3; 7 recovery scenarios |
| `text-columns.pdf` | Same facts, with sidebar skills/education kept separate from employment/projects and the date associated with its employer |
| `scan.pdf` | No text layer; all fields recovered through actual visual recognition of the page preview |
| `mixed.pdf` | Both pages reviewed; selectable “Reviewed 5 synthetic retry cases.” plus image-only “Recovered 23 mock records after retry.” retained |

All four normalized inputs matched their expected Markdown. The mixed-page text extraction intentionally lacks the 23-record achievement, demonstrating why a nonempty text layer cannot replace page inspection. This is an agent-assisted visual-recognition check, not a claim that the preparation CLI includes OCR or that arbitrary scans are always recoverable.

## Environment and limits

- Windows, Python 3.11; Playwright 1.58.0 with local Chromium; pypdfium2 5.12.1; Pillow 12.3.0. PDF fixtures were authored with ReportLab 4.4.9 from the bundled runtime.
- Previews were built offline without `--web-fonts`. Noto Sans SC is locally installed. Proprietary brand fonts were not installed or downloaded for this task; missing Inter, Roboto, IBM Plex Sans, Source Sans 3 or HarmonyOS Sans use their declared local/system fallbacks. These previews therefore demonstrate fallback rendering as well as the selected style rules, not guaranteed identical branded typography on every machine.
- Official design sources and six resume source studies are recorded in the design references and [sample provenance](../references/sample-sources.md). No third-party DESIGN.md text or real candidate data was copied. Some dynamic design sites require JavaScript; the references state which principles were adapted rather than presenting invented values as official tokens.
- The Markdown CLI remains a structured renderer, not a universal Markdown parser. PDF normalization and OCR are handled by the skill; unreadable or uncertain facts require user clarification. Fonts and image readiness are required before printing.

## Reproduce

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python -m unittest discover -s tests -v
python scripts/build_pdf_fixtures.py
python scripts/build_previews.py
python scripts/verify_previews.py
```

The style gallery opens locally from [examples/preview/index.html](../examples/preview/index.html). Generated work under `output/` is deliberately excluded from version control.
