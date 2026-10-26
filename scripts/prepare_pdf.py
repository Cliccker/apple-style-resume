#!/usr/bin/env python3
"""Extract page text and previews for agent-assisted PDF-to-Markdown preparation.

This is deliberately not OCR or a semantic resume parser. Every page must be
reviewed, including pages with text (their images can contain additional text).
"""

import argparse
import json
from pathlib import Path


def prepare_pdf(source: Path, output: Path) -> dict:
    import pypdfium2 as pdfium

    with pdfium.PdfDocument(source) as document:
        output.mkdir(parents=True, exist_ok=True)
        pages = []
        for index in range(len(document)):
            page = document[index]
            try:
                textpage = page.get_textpage()
                try:
                    text = textpage.get_text_bounded()
                finally:
                    textpage.close()
                stem = f'page-{index + 1:03}'
                (output / f'{stem}.txt').write_text(text, encoding='utf-8')
                bitmap = page.render(scale=1.5)
                try:
                    bitmap.to_pil().save(output / f'{stem}.png')
                finally:
                    bitmap.close()
                pages.append({'page': index + 1, 'text': f'{stem}.txt', 'preview': f'{stem}.png',
                              'text_characters': len(text.strip()),
                              'text_status': 'has_text' if text.strip() else 'no_text',
                              'requires_visual_review': True})
            finally:
                page.close()
    manifest = {'source': source.name, 'pages': pages,
                'next_step': 'Review EVERY preview; use visual/OCR recognition for image text. '
                             'Resolve columns and uncertainties, then write source.md. '
                             'Extracted text is not a verified transcription.'}
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if not args.input.is_file() or args.input.suffix.lower() != '.pdf':
        parser.error('Input must be an existing PDF.')
    try:
        result = prepare_pdf(args.input, args.output)
    except ImportError:
        parser.exit(1, 'Install input dependencies: python -m pip install -r requirements-input.txt\n')
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f'PDF preparation failed: {error}\n')
    print(f'Prepared {len(result["pages"])} pages. Review every preview before writing Markdown.')


if __name__ == '__main__':
    main()
