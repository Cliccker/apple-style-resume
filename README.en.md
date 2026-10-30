# Brand Style Resume

Convert a Markdown or PDF resume into a responsive web page and an A4 PDF, with twelve company-inspired design systems.

[简体中文](README.md) · **English**

---

The project separates a resume's content from its presentation: maintain one source file, and switch styles without touching the text. Both generated deliverables embed their CSS, so they can be distributed or archived independently of this repository.

Every style is an independent adaptation of a public design system. None is an official company template, and none implies a hiring outcome.

## Features

- Twelve design systems covering major Chinese and international companies, comparable against identical content
- Responsive web output and an A4 print version with identical body content
- Chinese and English interface labels, with the body language left untouched
- Support for summary, employment, education, skills, independent projects, certificates, awards, publications and custom sections
- Optional photo; without one, the header is text-only and no placeholder is generated
- Input as Markdown, text-based PDF or scanned PDF (scans require an agent with visual capability)
- HTML generation uses only the Python standard library, with no build step

## Preview

All twelve styles render the same fictional resume for comparison. People, organizations, schools, dates and achievements are invented; the avatar is an original geometric placeholder.

![First six styles, Chinese and English desktop](docs/images/gallery/desktop-1.png)
![Remaining six styles, Chinese and English desktop](docs/images/gallery/desktop-2.png)

Browse the full set in the [local gallery](examples/preview/index.html). GitHub renders HTML as source, so download the repository and open the file in a browser. Desktop, mobile and per-page PDF screenshots are stored alongside each preview.

## Installation

Requires Node.js 22.20+ and npm. Install through the [Vercel Skills CLI](https://github.com/vercel-labs/skills); the repository URL is unchanged:

```bash
npx skills add Cliccker/apple-style-resume --skill brand-style-resume -a codex -y
```

Add `-g` to install at user scope for all projects, or use `--list` to see what is discoverable:

```bash
npx skills add Cliccker/apple-style-resume --skill brand-style-resume -a codex -g -y
npx skills add Cliccker/apple-style-resume --list
```

For a manual install, clone the entire repository into `.agents/skills/brand-style-resume` in your project. That directory must contain `SKILL.md`, `assets`, `scripts`, `references` and `DESIGN.md` directly; copying `SKILL.md` alone will not run. Installation does not configure Python, fonts or PDF dependencies — see below.

<details>
<summary>Migrating from <code>apple-style-resume</code></summary>

The skill is now named `brand-style-resume`; the repository URL is unchanged. Existing CLI commands remain compatible. Replace any `$apple-style-resume` invocation with `$brand-style-resume`.

If you installed manually before, back up and replace the old directory rather than keeping both copies.

</details>

## Usage

### With the skill

Once installed, describe the task in natural language rather than recalling flags:

```text
$brand-style-resume Use resume.md and portrait.png to create an English IBM Carbon-inspired resume in output/resume, including a PDF.
```

```text
$brand-style-resume 将 resume.pdf 编排为腾讯 TDesign 风格，输出到 output/resume，保留原文并导出 PDF，暂不使用照片。
```

The skill handles the following: it lists all twelve styles when none is specified; it asks whether to upload a photo or continue without one; and it reviews desktop, mobile and every PDF page after rendering. It does not translate body text, and it does not upload or deploy unless asked.

### With the CLI

The CLI runs independently. HTML generation requires only Python 3.10+, prompts for nothing, and defaults to Apple, Chinese labels and no photo.

```bash
python scripts/md_to_resume.py --list-styles
python scripts/md_to_resume.py resume.md output/resume --style ant-design
python scripts/md_to_resume.py resume.md output/resume --style ibm-carbon --lang en --photo portrait.png
```

The original three-positional-argument form remains supported:

```bash
python scripts/md_to_resume.py resume.md portrait.png output/resume
```

Outputs are `index.html` (responsive web), `resume_a4.html` (A4 print) and `source.md` (the source used for rendering). A supplied photo is copied in as `photo.jpg`, `photo.jpeg` or `photo.png`.

Exporting the PDF:

```bash
python -m pip install -r requirements-pdf.txt
python -m playwright install chromium
python scripts/export_pdf.py output/resume/resume_a4.html --output output/resume/resume.pdf
```

On Linux, use Playwright's `install --with-deps chromium` when the browser's system dependencies are missing. Alternatively, print `resume_a4.html` from a browser: select A4, keep CSS margins, enable background graphics and disable headers and footers.

## Design systems

Chinese design systems:

| Style | CLI ID | Chinese | English |
| --- | --- | --- | --- |
| [Ant Design](references/styles/ant-design/DESIGN.md) | `ant-design` | [web](examples/preview/styles/ant-design/zh-CN/index.html) · [PDF](examples/preview/styles/ant-design/zh-CN/resume.pdf) | [web](examples/preview/styles/ant-design/en/index.html) · [PDF](examples/preview/styles/ant-design/en/resume.pdf) |
| [Tencent TDesign](references/styles/tencent-tdesign/DESIGN.md) | `tencent-tdesign` | [web](examples/preview/styles/tencent-tdesign/zh-CN/index.html) · [PDF](examples/preview/styles/tencent-tdesign/zh-CN/resume.pdf) | [web](examples/preview/styles/tencent-tdesign/en/index.html) · [PDF](examples/preview/styles/tencent-tdesign/en/resume.pdf) |
| [ByteDance Arco](references/styles/bytedance-arco/DESIGN.md) | `bytedance-arco` | [web](examples/preview/styles/bytedance-arco/zh-CN/index.html) · [PDF](examples/preview/styles/bytedance-arco/zh-CN/resume.pdf) | [web](examples/preview/styles/bytedance-arco/en/index.html) · [PDF](examples/preview/styles/bytedance-arco/en/resume.pdf) |
| [Douyin Semi](references/styles/douyin-semi/DESIGN.md) | `douyin-semi` | [web](examples/preview/styles/douyin-semi/zh-CN/index.html) · [PDF](examples/preview/styles/douyin-semi/zh-CN/resume.pdf) | [web](examples/preview/styles/douyin-semi/en/index.html) · [PDF](examples/preview/styles/douyin-semi/en/resume.pdf) |
| [Huawei HarmonyOS](references/styles/huawei-harmonyos/DESIGN.md) | `huawei-harmonyos` | [web](examples/preview/styles/huawei-harmonyos/zh-CN/index.html) · [PDF](examples/preview/styles/huawei-harmonyos/zh-CN/resume.pdf) | [web](examples/preview/styles/huawei-harmonyos/en/index.html) · [PDF](examples/preview/styles/huawei-harmonyos/en/resume.pdf) |
| [Baidu Light DLS](references/styles/baidu-dls/DESIGN.md) | `baidu-dls` | [web](examples/preview/styles/baidu-dls/zh-CN/index.html) · [PDF](examples/preview/styles/baidu-dls/zh-CN/resume.pdf) | [web](examples/preview/styles/baidu-dls/en/index.html) · [PDF](examples/preview/styles/baidu-dls/en/resume.pdf) |

International design systems:

| Style | CLI ID | Chinese | English |
| --- | --- | --- | --- |
| [Apple](references/styles/apple/DESIGN.md) | `apple` | [web](examples/preview/styles/apple/zh-CN/index.html) · [PDF](examples/preview/styles/apple/zh-CN/resume.pdf) | [web](examples/preview/styles/apple/en/index.html) · [PDF](examples/preview/styles/apple/en/resume.pdf) |
| [Google / Material 3](references/styles/google-material/DESIGN.md) | `google-material` | [web](examples/preview/styles/google-material/zh-CN/index.html) · [PDF](examples/preview/styles/google-material/zh-CN/resume.pdf) | [web](examples/preview/styles/google-material/en/index.html) · [PDF](examples/preview/styles/google-material/en/resume.pdf) |
| [Microsoft / Fluent 2](references/styles/microsoft-fluent/DESIGN.md) | `microsoft-fluent` | [web](examples/preview/styles/microsoft-fluent/zh-CN/index.html) · [PDF](examples/preview/styles/microsoft-fluent/zh-CN/resume.pdf) | [web](examples/preview/styles/microsoft-fluent/en/index.html) · [PDF](examples/preview/styles/microsoft-fluent/en/resume.pdf) |
| [IBM / Carbon](references/styles/ibm-carbon/DESIGN.md) | `ibm-carbon` | [web](examples/preview/styles/ibm-carbon/zh-CN/index.html) · [PDF](examples/preview/styles/ibm-carbon/zh-CN/resume.pdf) | [web](examples/preview/styles/ibm-carbon/en/index.html) · [PDF](examples/preview/styles/ibm-carbon/en/resume.pdf) |
| [Adobe / Spectrum](references/styles/adobe-spectrum/DESIGN.md) | `adobe-spectrum` | [web](examples/preview/styles/adobe-spectrum/zh-CN/index.html) · [PDF](examples/preview/styles/adobe-spectrum/zh-CN/resume.pdf) | [web](examples/preview/styles/adobe-spectrum/en/index.html) · [PDF](examples/preview/styles/adobe-spectrum/en/resume.pdf) |
| [Salesforce / Lightning](references/styles/salesforce-lightning/DESIGN.md) | `salesforce-lightning` | [web](examples/preview/styles/salesforce-lightning/zh-CN/index.html) · [PDF](examples/preview/styles/salesforce-lightning/zh-CN/resume.pdf) | [web](examples/preview/styles/salesforce-lightning/en/index.html) · [PDF](examples/preview/styles/salesforce-lightning/en/resume.pdf) |

`CLI ID` is the value passed to `--style`. Styles share content rendering but not layout: label grids, header treatments, project containers and type hierarchy are implemented per style. All are light-theme, with no company logos and no dark variant.

## FAQ

**Does it translate the resume?**
No. `--lang` switches interface labels only, such as "Work Experience" versus "工作经历". The body always matches the source file. Ask for translation as a separate step.

**Is a photo required?**
No. Without one the header is text-only, and no placeholder avatar is generated.

**Can the CLI be used without the skill?**
Yes. `scripts/md_to_resume.py` is a standalone CLI with no agent dependency. The skill covers the parts that need visual judgment: style selection, PDF review and layout checks.

**Can output be forced to a specific page count?**
Not by deleting content. Every style flows the resume naturally and starts a new page when the current one fills; type size and margins are set for print legibility, and long resumes are not shrunk to fit.

**Does it require network access?**
No, fonts load locally by default. Adding `--web-fonts` loads that style's open web fonts, so wait for fonts and photos before exporting.

**How are scanned PDFs handled?**
They require an agent with visual capability. `prepare_pdf.py` splits pages, captures previews and writes a manifest; it is not OCR and does not infer document structure.

**Does a missing font affect layout?**
Yes. It falls back along each style's documented stack, which can change line wrapping and pagination.

## Input format

Input needs one H1 for the name, a role line, an optional target role, contact details, then H2 sections. Summary, employment, education, skills, independent projects, certificates, awards and publications are supported. Unrecognized headings are preserved as written rather than dropped for not matching a template.

```markdown
# Example Candidate

Backend Engineer
Target role: Platform Engineer

hello@example.com
[Portfolio](https://example.com/portfolio)

## Summary

A factual summary supplied by the resume owner.

## Work Experience

### Example Studio | Engineer
*2023.04 - 2025.08*

**Project Title** *(Web / Design)*
- One verifiable outcome.
```

Repeated sections keep their order and empty ones are hidden. Nested lists flatten; complex tables and HTML are escaped and displayed as text rather than executed. Full rules are in the [Markdown guide](references/markdown-parsing.md).

## PDF input

```bash
python -m pip install -r requirements-input.txt
python scripts/prepare_pdf.py resume.pdf --output output/pdf-input
```

The script splits the PDF into per-page `.txt`, `.png` and a `manifest.json`. The following step requires visual review: read each page preview alongside its text, write editable Markdown, then pass it to the renderer. Two-column layouts need their reading order restored, and scanned or mixed pages need closer inspection, since an extractable text layer does not mean the image content was captured.

Uncertain names, dates, numbers or other facts are raised as questions rather than filled in. If visual/OCR capability is unavailable, the affected pages are reported and a readable source is requested; the CLI alone cannot recognize scanned text.

See the [PDF workflow](references/pdf-input.md). [Four fictional PDF inputs](examples/pdf-input) ship with their expected Markdown for practice and testing.

## Fonts and design rules

Fonts load locally by default. Apple keeps its Inter and Noto Sans SC stack, Carbon uses IBM Plex Sans, Material uses Roboto, and each style's `DESIGN.md` documents the rest. No proprietary font binaries or company marks are bundled.

Shared rules — web width, A4 margins, minimum print size, pagination policy — are collected in [DESIGN.md](DESIGN.md), which also records each adaptation's official sources, retrieval date, design tokens and adaptation notes. Community DESIGN.md documents found during research are documented there as well; none of their content was copied.

## Examples and rebuilding

- [examples/profiles](examples/profiles): twelve Markdown profiles covering six fictional candidates in both languages
- [examples/preview/careers](examples/preview/careers): graduate, frontend, backend, product, design and data roles, including no employment history, multiple employers, long content, long links and custom sections
- [references/sample-sources.md](references/sample-sources.md): six public sources used for structure only, with no real resume data or personal information copied

After changing a style, regenerate every preview:

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python scripts/build_pdf_fixtures.py
python scripts/build_previews.py
```

Real input and output are not automatically anonymized. Public examples must be separately authored fictional content; blurring a real resume is not sufficient.

## Project structure

```text
assets/       style CSS and the style index
scripts/      generation, PDF export and preview build scripts
references/   per-style DESIGN.md, input format and source notes
examples/     fictional resumes, career samples and generated previews
docs/         preview images used by this README
tests/        tests
```

## License

[MIT](LICENSE).

Each style is an independent adaptation of a public design system. This project is not affiliated with or endorsed by Apple, Google, Microsoft, IBM, Ant Group, Tencent, ByteDance, Douyin, Huawei, Baidu, Adobe or Salesforce.

## Community

Join [LINUX DO](https://linux.do/), "a new ideal community."
