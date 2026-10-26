import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('brand_resume', ROOT / 'scripts/md_to_resume.py')
resume = importlib.util.module_from_spec(spec)
spec.loader.exec_module(resume)


class BodyText(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.in_body = False
        self.parts = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True

    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False

    def handle_data(self, data):
        if self.in_body:
            self.parts.append(data)

    def text(self):
        return ' '.join(' '.join(self.parts).split())


class BrandTests(unittest.TestCase):
    def test_all_profiles_retain_identical_content_across_styles(self):
        profiles = sorted((ROOT / 'examples/profiles').glob('*.md'))
        self.assertEqual(len(profiles), 12)
        for profile in profiles:
            data = resume.parse_markdown_resume(profile.read_text(encoding='utf-8'))
            lang = 'zh-CN' if '.zh-CN.' in profile.name else 'en'
            for render in (resume.render_web_template, resume.render_pdf_template):
                baseline = BodyText(render(data, lang, photo=None)).text()
                for style in resume.STYLES:
                    with self.subTest(profile=profile.name, renderer=render.__name__, style=style):
                        html = render(data, lang, photo=None, style=style)
                        self.assertEqual(BodyText(html).text(), baseline)
                        self.assertNotIn('{{', html)
                        self.assertNotIn('<img ', html)
                        self.assertIn(f'data-style="{style}"', html)

    def test_unfamiliar_repeated_and_noncanonical_sections_keep_facts_and_order(self):
        data = resume.parse_markdown_resume('''# Example Person
Engineer
## Skills
- Python
## Publications
### Example Paper
Notes about 2024.
## Education
School without pipe separators, class of 2020.
## Work Experience
### Example Company | Engineer | Remote
2021 - 2025
**Project**
A paragraph before the achievement.
- Delivered 14 components.
## Volunteer Experience
Kept separate from employment.
## Skills
- SQL
## Certificates
- Example Qualification
## Awards
- Example Prize
''')
        for render in (resume.render_web_template, resume.render_pdf_template):
            text = BodyText(render(data, 'en', photo=None)).text()
            for fragment in ('Python', 'Notes about 2024.', 'class of 2020', 'Remote',
                             'A paragraph before the achievement.', '14 components',
                             'Volunteer Experience', 'SQL', 'Example Qualification', 'Example Prize'):
                self.assertIn(fragment, text)
            self.assertLess(text.index('Python'), text.index('Example Paper'))
            self.assertLess(text.index('Volunteer Experience'), text.index('SQL'))

    def test_generic_blocks_escape_html_and_reject_executable_links(self):
        data = resume.parse_markdown_resume('''# Example
Engineer
## Other
<img src=x onerror=alert(1)>
- **Safe** [unsafe](javascript:alert) [valid](https://example.com/a?x=1&y=2)
Literal {{NOT_A_PLACEHOLDER}} stays literal.
''')
        for render in (resume.render_web_template, resume.render_pdf_template):
            html = render(data, 'en', photo=None)
            self.assertIn('&lt;img', html)
            self.assertNotIn('href="javascript:', html)
            self.assertNotIn('<img ', html)
            self.assertIn('https://example.com/a?x=1&amp;y=2', html)
            self.assertIn('Literal {{NOT_A_PLACEHOLDER}} stays literal.', html)

    def test_new_cli_optional_photo_and_style_selection(self):
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder) / '中文 output'
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/md_to_resume.py'),
                                     str(ROOT / 'examples/profiles/graduate.en.md'), str(dest),
                                     '--style', 'ibm-carbon', '--lang', 'en'], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            html = (dest / 'index.html').read_text(encoding='utf-8')
            self.assertIn('data-style="ibm-carbon"', html)
            self.assertNotIn('<img ', html)
            self.assertTrue((dest / 'source.md').is_file())

    def test_invalid_style_and_duplicate_photo_are_errors(self):
        for args in (('--style', 'unknown'), ('--photo', 'photo.png')):
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/md_to_resume.py'),
                                     'input.md', 'legacy.png', 'output', *args], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b'error:', result.stderr)

    def test_brand_font_loading_is_explicit(self):
        data = resume.parse_markdown_resume('# Example\nEngineer')
        for style, metadata in resume.STYLES.items():
            self.assertTrue((ROOT / metadata['design']).is_file())
            html = resume.render_web_template(data, style=style)
            self.assertNotIn('fonts.googleapis.com', html)
            html = resume.render_web_template(data, style=style, web_fonts=True)
            self.assertIn('fonts.googleapis.com', html)
        self.assertIn('IBM+Plex+Sans', resume.render_web_template(data, style='ibm-carbon', web_fonts=True))
        self.assertNotIn('family=Inter', resume.render_web_template(data, style='ibm-carbon', web_fonts=True))


if __name__ == '__main__':
    unittest.main()
