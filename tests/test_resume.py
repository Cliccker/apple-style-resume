"""Behavior checks using only fictional examples and the standard library."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("resume", ROOT / "scripts/md_to_resume.py")
resume = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(resume)


class ResumeTests(unittest.TestCase):
    def example(self, lang):
        return resume.parse_markdown_resume((ROOT / f"examples/resume.{lang}.md").read_text(encoding="utf-8"))

    def test_chinese_and_english_content_is_retained(self):
        for lang, role in (("zh-CN", "产品工程师"), ("en", "Product Engineer")):
            with self.subTest(lang=lang):
                data = self.example(lang)
                self.assertEqual(data["role"], role)
                self.assertEqual(len(data["experiences"]), 2)
                self.assertEqual(len(data["gaming"]), 1)
                self.assertTrue(data["experiences"][1]["description"])
                self.assertEqual(len(data["experiences"][0]["projects"]), 2)
                self.assertTrue(all(not item["detail"].startswith((":", "：")) for item in data["early_works"]))
                for render in (resume.render_web_template, resume.render_pdf_template):
                    html = render(data, lang)
                    self.assertIn(f'lang="{lang}"', html)
                    self.assertIn(data["name"], html)
                    self.assertIn(resume.LABELS[lang]["GAMING_TITLE"], html)
                    self.assertNotIn("{{", html)

    def test_empty_sections_are_absent(self):
        data = resume.parse_markdown_resume("# Example Candidate\n\nEngineer\n\n## Summary\nExample text.")
        for render in (resume.render_web_template, resume.render_pdf_template):
            html = render(data, "en")
            self.assertIn('>Profile<', html)
            for title in (">Experience<", ">Education<", ">Gaming Experience<", ">Early Projects &amp; Patents<"):
                self.assertNotIn(title, html)

    def test_language_only_changes_interface(self):
        data = self.example("zh-CN")
        html = resume.render_web_template(data, "en")
        self.assertIn(data["profile"], html)
        self.assertIn(">Profile<", html)
        self.assertNotIn(">个人简介<", html)

    def test_text_and_contact_urls_are_escaped(self):
        data = self.example("en")
        data["profile"] = '<script>alert("example")</script> & text'
        data["blog_url"] = 'javascript:alert("example")'
        for render in (resume.render_web_template, resume.render_pdf_template):
            html = render(data, "en")
            self.assertIn("&lt;script&gt;", html)
            self.assertNotIn("<script>", html)
            self.assertNotIn("javascript:", html)

    def test_online_fonts_are_opt_in_and_original_stack_is_kept(self):
        data = self.example("en")
        for render in (resume.render_web_template, resume.render_pdf_template):
            self.assertNotIn("fonts.googleapis.com", render(data))
            html = render(data, web_fonts=True)
            self.assertIn("fonts.googleapis.com", html)
            self.assertIn('"Inter", "Noto Sans SC"', html)

    def test_legacy_cli_png_and_unicode_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "示例 output"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/md_to_resume.py"),
                                     str(ROOT / "examples/resume.zh-CN.md"), str(ROOT / "examples/avatar.png"), str(dest)],
                                    capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((dest / "photo.png").read_bytes(), (ROOT / "examples/avatar.png").read_bytes())
            self.assertIn('lang="zh-CN"', (dest / "index.html").read_text(encoding="utf-8"))
            self.assertIn('src="photo.png"', (dest / "resume_a4.html").read_text(encoding="utf-8"))

    def test_jpeg_extensions_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            for extension in (".jpg", ".jpeg"):
                source = Path(directory) / ("avatar" + extension)
                source.write_bytes((ROOT / "examples/avatar.jpg").read_bytes())
                dest = Path(directory) / extension[1:]
                subprocess.run([sys.executable, str(ROOT / "scripts/md_to_resume.py"),
                                str(ROOT / "examples/resume.en.md"), str(source), str(dest), "--lang", "en"],
                               check=True, capture_output=True)
                self.assertEqual((dest / ("photo" + extension)).read_bytes(), source.read_bytes())
                self.assertIn(f'src="photo{extension}"', (dest / "index.html").read_text(encoding="utf-8"))

    def test_missing_file_and_invalid_language_fail_cleanly(self):
        for args in (("missing.md", "missing.png", "output"),
                     ("missing.md", "missing.png", "output", "--lang", "invalid")):
            result = subprocess.run([sys.executable, str(ROOT / "scripts/md_to_resume.py"), *args], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b"error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
