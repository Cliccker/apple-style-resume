#!/usr/bin/env python3
"""Check that actual preview PDFs retain HTML text and contain no blank pages."""

from html.parser import HTMLParser
import json
from pathlib import Path
import unicodedata

import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]


def normalize(text):
    return ''.join(c for c in unicodedata.normalize('NFKC', text) if c.isalnum()).casefold()


class BodyText(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.in_body = False
        self.nodes = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True

    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False

    def handle_data(self, data):
        if self.in_body and normalize(data):
            self.nodes.append(data.strip())


def main():
    results = []
    apple_samples = [ROOT / 'examples/preview' / folder / 'resume.pdf' for folder in (
        'zh-CN', 'en', 'styles/apple/zh-CN', 'styles/apple/en')]
    for source in sorted((ROOT / 'examples/preview/styles').glob('*/*/resume.pdf')) + sorted(
            (ROOT / 'examples/preview/careers').glob('*/resume.pdf')) + apple_samples[:2]:
        extracted, page_lengths, outside = [], [], 0
        with pdfium.PdfDocument(source) as document:
            for index in range(len(document)):
                page = document[index]
                textpage = page.get_textpage()
                try:
                    text = textpage.get_text_bounded()
                    extracted.append(text)
                    page_lengths.append(len(normalize(text)))
                    width, height = page.get_size()
                    for char_index in range(textpage.count_chars()):
                        left, bottom, right, top = textpage.get_charbox(char_index)
                        if left < -1 or bottom < -1 or right > width + 1 or top > height + 1:
                            outside += 1
                finally:
                    textpage.close()
                    page.close()
        combined = normalize(' '.join(extracted))
        nodes = BodyText(source.with_name('resume_a4.html').read_text(encoding='utf-8')).nodes
        missing = [text for text in nodes if normalize(text) not in combined]
        results.append({'file': source.relative_to(ROOT).as_posix(), 'page_text_lengths': page_lengths,
                        'expected_pages': 1 if source in apple_samples else None,
                        'missing_html_text': missing, 'glyphs_outside_page': outside})
    report_dir = ROOT / 'output/validation'
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / 'pdf-checks.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    failures = [r for r in results if r['missing_html_text'] or r['glyphs_outside_page'] or not all(r['page_text_lengths'])
                or (r['expected_pages'] is not None and len(r['page_text_lengths']) != r['expected_pages'])]
    if failures:
        raise SystemExit(json.dumps(failures, ensure_ascii=False, indent=2))
    print(f'Checked {len(results)} PDFs: all HTML text retained, expected page counts, no blank pages or glyphs outside page bounds.')


if __name__ == '__main__':
    main()
