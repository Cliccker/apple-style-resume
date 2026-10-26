import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prepare_pdf', ROOT / 'scripts/prepare_pdf.py')
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)

try:
    import pypdfium2
    from PIL import Image
    PDF_INPUT_AVAILABLE = True
except ImportError:
    PDF_INPUT_AVAILABLE = False


@unittest.skipUnless(PDF_INPUT_AVAILABLE, 'Install requirements-input.txt for PDF input tests')
class PDFInputTests(unittest.TestCase):
    def test_single_and_columns_keep_key_fields_and_render_every_page(self):
        for name in ('text-single', 'text-columns'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                dest = Path(directory)
                manifest = prepare.prepare_pdf(ROOT / f'examples/pdf-input/{name}.pdf', dest)
                self.assertEqual(len(manifest['pages']), 1)
                page = manifest['pages'][0]
                text = (dest / page['text']).read_text(encoding='utf-8')
                for fact in ('Alex Example', '2022 - 2026', '120', '9 to 3', '7 recovery scenarios'):
                    self.assertIn(fact, text)
                self.assertEqual(page['text_status'], 'has_text')
                self.assertTrue(page['requires_visual_review'])
                with Image.open(dest / page['preview']) as image:
                    self.assertGreater(image.width, 800)
                self.assertEqual(json.loads((dest / 'manifest.json').read_text(encoding='utf-8')), manifest)

    def test_scan_has_preview_but_no_text_and_needs_visual_recognition(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory)
            manifest = prepare.prepare_pdf(ROOT / 'examples/pdf-input/scan.pdf', dest)
            page = manifest['pages'][0]
            self.assertEqual(page['text_status'], 'no_text')
            self.assertEqual(page['text_characters'], 0)
            self.assertTrue(page['requires_visual_review'])
            self.assertTrue((dest / page['preview']).is_file())

    def test_mixed_text_does_not_hide_image_only_achievement(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory)
            manifest = prepare.prepare_pdf(ROOT / 'examples/pdf-input/mixed.pdf', dest)
            self.assertEqual(len(manifest['pages']), 2)
            page = manifest['pages'][1]
            text = (dest / page['text']).read_text(encoding='utf-8')
            self.assertIn('Reviewed 5 synthetic retry cases.', text)
            self.assertNotIn('23 mock records', text)
            self.assertEqual(page['text_status'], 'has_text')
            self.assertTrue(page['requires_visual_review'])
            expected = (ROOT / 'examples/pdf-input/mixed.expected.md').read_text(encoding='utf-8')
            self.assertIn('Recovered 23 mock records after retry.', expected)


if __name__ == '__main__':
    unittest.main()
