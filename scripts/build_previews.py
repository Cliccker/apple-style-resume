#!/usr/bin/env python3
"""Build the fictional style gallery, career previews and visual-check artifacts."""

import json
from html import escape
from pathlib import Path
import shutil

from PIL import Image, ImageDraw
import pypdfium2 as pdfium
from playwright.sync_api import sync_playwright

from md_to_resume import ROOT, STYLES, parse_markdown_resume, render_web_template, render_pdf_template


def render_pdf_pages(source: Path, destination: Path) -> list:
    for previous in destination.glob('pdf-page-*.png'):
        previous.unlink()
    paths = []
    with pdfium.PdfDocument(source) as document:
        for index in range(len(document)):
            page = document[index]
            try:
                bitmap = page.render(scale=1.1)
                path = destination / f'pdf-page-{index + 1}.png'
                bitmap.to_pil().save(path)
                bitmap.close()
                paths.append(path)
            finally:
                page.close()
    return paths


def contact_sheet(entries: list, destination: Path, columns=4, width=280, height=420):
    rows = (len(entries) + columns - 1) // columns
    sheet = Image.new('RGB', (columns * width, rows * (height + 30)), '#dedede')
    draw = ImageDraw.Draw(sheet)
    for index, (label, path) in enumerate(entries):
        with Image.open(path) as image:
            image = image.convert('RGB')
            image.thumbnail((width - 12, height - 8))
            x = (index % columns) * width
            y = (index // columns) * (height + 30)
            draw.text((x + 6, y + 4), label, fill='black')
            sheet.paste(image, (x + 6, y + 26))
    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination)


def build_one(page, source, dest, style, lang, photo=None):
    dest.mkdir(parents=True, exist_ok=True)
    data = parse_markdown_resume(source.read_text(encoding='utf-8'))
    photo_name = None
    if photo:
        photo_name = 'photo' + photo.suffix
        shutil.copyfile(photo, dest / photo_name)
    shutil.copyfile(source, dest / 'source.md')
    for name, renderer in (('index.html', render_web_template), ('resume_a4.html', render_pdf_template)):
        (dest / name).write_text(renderer(data, lang, photo_name, style=style), encoding='utf-8')
    checks = []
    for mode, width, height in (('desktop', 1280, 1000), ('mobile', 390, 844)):
        page.set_viewport_size({'width': width, 'height': height})
        page.emulate_media(media='screen', reduced_motion='reduce')
        page.goto((dest / 'index.html').as_uri(), wait_until='load')
        page.evaluate('document.fonts.ready')
        page.screenshot(path=str(dest / f'{mode}.png'), full_page=True)
        overflowing = page.evaluate('''() => [...document.body.querySelectorAll('*')].filter(el => {
            const r = el.getBoundingClientRect();
            return r.width > 0 && (r.right > innerWidth + 1 || r.left < -1);
        }).map(el => el.className || el.tagName)''')
        broken_images = page.evaluate('''() => [...document.images].filter(i => !i.complete || !i.naturalWidth).length''')
        checks.append({'view': mode, 'overflow': overflowing, 'broken_images': broken_images})
    page.goto((dest / 'resume_a4.html').as_uri(), wait_until='load')
    page.evaluate('document.fonts.ready')
    page.evaluate('Promise.all([...document.images].map(img => img.decode()))')
    page.pdf(path=str(dest / 'resume.pdf'), format='A4', prefer_css_page_size=True,
             print_background=True, display_header_footer=False)
    pages = render_pdf_pages(dest / 'resume.pdf', dest)
    return checks, pages


def main():
    results, sheets = [], {'desktop': [], 'mobile': [], 'pdf': []}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        for style in STYLES:
            for lang in ('zh-CN', 'en'):
                dest = ROOT / 'examples/preview/styles' / style / lang
                checks, pages = build_one(page, ROOT / f'examples/resume.{lang}.md', dest, style, lang,
                                          ROOT / 'examples/avatar.png')
                results.append({'style': style, 'lang': lang, 'checks': checks, 'pages': len(pages)})
                for mode in ('desktop', 'mobile'):
                    sheets[mode].append((f'{style} / {lang}', dest / f'{mode}.png'))
                sheets['pdf'].extend((f'{style}/{lang} p{i + 1}', path) for i, path in enumerate(pages))
                print(f'Built {style}/{lang}: {len(pages)} PDF pages', flush=True)
        for ident, style in zip(('graduate', 'frontend', 'backend', 'product', 'designer', 'data'), STYLES):
            dest = ROOT / 'examples/preview/careers' / ident
            checks, pages = build_one(page, ROOT / f'examples/profiles/{ident}.en.md', dest, style, 'en')
            results.append({'career': ident, 'style': style, 'checks': checks, 'pages': len(pages)})
            sheets['pdf'].extend((f'{ident} p{i + 1}', path) for i, path in enumerate(pages))
            print(f'Built career {ident}: {len(pages)} PDF pages', flush=True)
        browser.close()
    for mode, entries in sheets.items():
        for previous in (ROOT / 'docs/images/gallery').glob(f'{mode}-*.png'):
            previous.unlink()
        # Split sheets to keep every thumbnail large enough to inspect.
        for part, offset in enumerate(range(0, len(entries), 12), 1):
            contact_sheet(entries[offset:offset + 12], ROOT / f'docs/images/gallery/{mode}-{part}.png')
    report_dir = ROOT / 'output/validation'
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / 'preview-checks.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    cards = []
    for style, theme in STYLES.items():
        cards.append(f'<article><h2>{escape(theme["name"])}</h2>'
                     f'<a href="styles/{style}/zh-CN/index.html"><img src="styles/{style}/zh-CN/desktop.png" '
                     f'alt="{escape(theme["name"])} fictional resume preview"></a><p>' +
                     ' · '.join(f'<a href="styles/{style}/{lang}/{filename}">{label}</a>' for lang, filename, label in (
                         ('zh-CN', 'index.html', '中文 HTML'), ('zh-CN', 'resume.pdf', '中文 PDF'),
                         ('en', 'index.html', 'English HTML'), ('en', 'resume.pdf', 'English PDF'))) + '</p></article>')
    gallery = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Brand Style Resume Gallery</title><style>
*{box-sizing:border-box}body{margin:0;background:#FAFAFA;color:#1D1D1F;font:15px/1.7 "Inter","Noto Sans SC",system-ui,sans-serif}
main{max-width:960px;margin:auto;padding:40px 20px}h1{font-size:32px;line-height:1.25}h2{font-size:18px;margin:0 0 14px}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}article{min-width:0;background:white;border:1px solid #e6e6e8;border-radius:24px;padding:24px}
img{width:100%;height:300px;object-fit:cover;object-position:top;border-radius:12px}a{color:#0071E3}a:focus-visible{outline:2px solid #0071E3;outline-offset:3px}
@media(max-width:600px){.grid{grid-template-columns:1fr}main{padding:24px 16px}}
</style><main><h1>Brand Style Resume</h1><p>12 套设计语言，同一份虚构简历。Independent adaptations; all candidate data is fictional.</p>
<p>字体使用本地字体及系统回退；不含公司标志或专有字体。Local/system fonts, no company marks.</p><div class="grid">'''
    (ROOT / 'examples/preview/index.html').write_text(gallery + ''.join(cards) + '</div></main></html>', encoding='utf-8')
    errors = [r for r in results if any(c['overflow'] or c['broken_images'] for c in r['checks'])]
    if errors:
        raise SystemExit(f'Visual geometry failures: {errors}')
    print('All preview geometry checks passed. Inspect the contact sheets and individual PDF pages.')


if __name__ == '__main__':
    main()
