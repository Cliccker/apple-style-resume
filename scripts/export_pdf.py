#!/usr/bin/env python3
"""Export local A4 resume HTML to PDF with optional Playwright/Chromium dependencies."""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Generated resume_a4.html")
    parser.add_argument("--output", required=True, type=Path, help="Destination PDF")
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error("Input HTML does not exist.")
    try:
        from playwright.sync_api import Error, sync_playwright
    except ImportError:
        parser.exit(1, "Install PDF dependencies: python -m pip install -r requirements-pdf.txt\n")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.goto(args.input.resolve().as_uri(), wait_until="load")
            page.evaluate("document.fonts.ready")
            page.evaluate("Promise.all([...document.images].map(img => img.decode()))")
            page.pdf(path=str(args.output), format="A4", prefer_css_page_size=True,
                     print_background=True, display_header_footer=False)
            browser.close()
    except Error:
        parser.exit(1, "PDF export failed. Check the HTML/images and install Chromium: python -m playwright install chromium\n")
    print(f"Created {args.output.name}")


if __name__ == "__main__":
    main()
