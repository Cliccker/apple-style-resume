# PDF input preparation

The skill accepts PDF through agent-assisted normalization. The renderer accepts only `.md`; a Python CLI does not understand arbitrary layouts or perform OCR unaided.

`scripts/prepare_pdf.py INPUT.pdf --output WORKDIR` uses optional pypdfium2 and Pillow to create `manifest.json`, `page-NNN.txt` (possibly empty), and `page-NNN.png` (1.5x preview). The original file is never changed. Use a dedicated work directory. Unreadable, encrypted or malformed PDFs exit with a diagnostic; ask for an accessible copy instead of skipping pages.

## Review and normalize

1. Inspect every preview, including pages marked `has_text`. Images can contain additional dates, achievements or sidebars even when extraction succeeds.
2. Recover meaningful column order. Keep a company's role, date, projects and achievements together; keep sidebar skills separate. Do not concatenate alternating lines from unrelated columns.
3. Read image-only text using the agent's visual recognition or an available OCR tool. Without either capability, explain the unreadable pages and request a readable source.
4. Write `source.md` following [markdown-parsing.md](markdown-parsing.md). Preserve facts, names, qualifiers, units, dates, links and project ownership. Remove repeated page furniture only when it is clearly not meaningful resume content.
5. Compare with every source page. Ask about unresolved ambiguity; do not require approval of an unambiguous transcription. Never estimate unreadable numbers.

Do not infer hyperlink destinations from printed labels. Keep visible text when a destination cannot be verified. Photos follow the skill's upload/omit question; do not automatically crop a portrait from the PDF.

## Validation fixtures

See [examples/pdf-input](../examples/pdf-input) for four fictional PDFs and corresponding expected Markdown. `scan.pdf` intentionally has no text layer. `mixed.pdf` contains a page with both selectable text and an image-only result. The double-column fixture separates skills/education from work/projects. Compare semantics, not extraction-stream order.

Actual resumes are not anonymized or uploaded by this workflow. Work directories and prepared Markdown contain the user's supplied information.
