#!/usr/bin/env python3
"""Rebuild four entirely fictional PDF inputs (development dependencies only)."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import pypdfium2 as pdfium
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'examples/pdf-input'
EXPECTED = '''# Alex Example

Backend Engineer

alex@example.com

## Skills
- Python, SQL, API design

## Education
- **Example College (fictional)** | Computing | Bachelor | 2021

## Work Experience
### Example Lab (fictional) | Backend Engineer
*2022 - 2026*

**Queue Simulator**
- Processed 120 synthetic requests.
- Reduced mock failures from 9 to 3.

## Projects
### Retry Notebook
- Documented 7 recovery scenarios.
'''


def lines(canvas, x, y, entries, size=11):
    canvas.setFont('Helvetica', size)
    for text in entries:
        canvas.drawString(x, y, text)
        y -= 20
    return y


def identity(canvas):
    canvas.setTitle('Fictional PDF input fixture')
    canvas.setAuthor('Brand Style Resume Contributors')
    canvas.setFont('Helvetica-Bold', 25)
    canvas.drawString(42, 785, 'Alex Example')
    lines(canvas, 42, 755, ['Backend Engineer', 'alex@example.com'])


def single(canvas):
    identity(canvas)
    lines(canvas, 42, 680, ['Skills', 'Python, SQL, API design', '', 'Education',
                          'Example College (fictional) | Computing | Bachelor | 2021', '',
                          'Work Experience', 'Example Lab (fictional) | Backend Engineer',
                          '2022 - 2026', 'Queue Simulator',
                          '- Processed 120 synthetic requests.', '- Reduced mock failures from 9 to 3.', '',
                          'Projects', 'Retry Notebook', '- Documented 7 recovery scenarios.'])


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    canvas = Canvas(str(DEST / 'text-single.pdf'), pagesize=A4)
    single(canvas)
    canvas.save()

    canvas = Canvas(str(DEST / 'text-columns.pdf'), pagesize=A4)
    identity(canvas)
    canvas.setStrokeColorRGB(.8, .8, .8)
    canvas.line(225, 690, 225, 430)
    lines(canvas, 42, 680, ['Skills', 'Python, SQL, API design', '', 'Education',
                          'Example College (fictional)', 'Computing | Bachelor | 2021'], size=10)
    lines(canvas, 245, 680, ['Work Experience', 'Example Lab (fictional)', 'Backend Engineer | 2022 - 2026',
                           'Queue Simulator', '- Processed 120 synthetic requests.',
                           '- Reduced mock failures from 9 to 3.', '', 'Projects',
                           'Retry Notebook', '- Documented 7 recovery scenarios.'], size=10)
    canvas.save()

    with pdfium.PdfDocument(DEST / 'text-single.pdf') as document:
        page = document[0]
        try:
            bitmap = page.render(scale=1.5)
            image = bitmap.to_pil().convert('L').copy()
            bitmap.close()
        finally:
            page.close()
    canvas = Canvas(str(DEST / 'scan.pdf'), pagesize=A4)
    canvas.drawImage(ImageReader(image), 0, 0, width=A4[0], height=A4[1])
    canvas.save()

    canvas = Canvas(str(DEST / 'mixed.pdf'), pagesize=A4)
    single(canvas)
    canvas.showPage()
    lines(canvas, 42, 780, ['Exercise Notes', 'Reviewed 5 synthetic retry cases.'])
    image = Image.new('RGB', (1100, 100), 'white')
    draw = ImageDraw.Draw(image)
    # A rendered text image is intentional: this fact has no PDF text layer.
    try:
        font = ImageFont.truetype('arial.ttf', 30)
    except OSError:
        font = ImageFont.load_default(size=30)
    draw.text((10, 25), 'Recovered 23 mock records after retry.', fill='black', font=font)
    canvas.drawImage(ImageReader(image), 42, 620, width=500, height=46)
    canvas.save()

    for name in ('text-single', 'text-columns', 'scan', 'mixed'):
        text = EXPECTED
        if name == 'mixed':
            text += '\n## Exercise Notes\n- Reviewed 5 synthetic retry cases.\n- Recovered 23 mock records after retry.\n'
        (DEST / f'{name}.expected.md').write_text(text, encoding='utf-8')
    print('Created four fictional PDF inputs and expected Markdown.')


if __name__ == '__main__':
    main()
