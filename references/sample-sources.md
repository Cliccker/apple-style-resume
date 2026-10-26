# Sample research and provenance

Reviewed 2026-10-26. The files below informed **structural scenarios only**. No candidate biography, accomplishment, code, photo or font was copied into this repository. Public availability and a template's license do not grant permission to republish its candidate data. In particular, sb2nov explicitly separates the MIT format from the owner's data.

| Primary source and specific file | Format / observation | Original fixture informed |
| --- | --- | --- |
| [tengjuilin: source/resume.md](https://github.com/tengjuilin/markdown-resume/blob/main/source/resume.md) | Markdown with embedded HTML, education first, separate content/style workflow. Raw HTML needs normalization, not execution. | Graduate profile; normalization guidance |
| [sb2nov: sourabh_bajaj_resume.tex](https://github.com/sb2nov/resume/blob/master/sourabh_bajaj_resume.tex), [PDF](https://github.com/sb2nov/resume/blob/master/sourabh_bajaj_resume.pdf) | Single-column education, experience and projects with aligned dates; explicit machine-readable text. | Backend multi-employer profile; text-single fixture |
| [forfrt: resume.tex](https://github.com/forfrt/cn_resume/blob/main/resume.tex), [Chinese PDF](https://github.com/forfrt/cn_resume/blob/main/%E4%B8%AD%E6%96%87%E7%AE%80%E5%8E%86%E6%A8%A1%E6%9D%BF.pdf) | Chinese section rules, dated entries and categorized information. We do not copy its bundled Adobe fonts. | Chinese profiles and categorized skills |
| [dphang: resume.tex](https://github.com/dphang/resume/blob/master/resume.tex), [PDF](https://github.com/dphang/resume/blob/master/resume-example.pdf) | Compact experience, categorized skills, education and aligned entry headers. | Frontend profile; dense-content checks |
| [skjjks: example.tex](https://github.com/skjjks/resume-latex/blob/main/example.tex), [PDF](https://github.com/skjjks/resume-latex/blob/main/example.pdf) | Mixed Chinese/English text, company/role/date rows, optional portrait and skill categories. | Designer profile; two-column reading-order fixture |
| [markdownresume: templates/product-manager.md](https://github.com/markdownresume/markdown-resume-templates/blob/main/templates/product-manager.md) | Separate competencies, professional experience and quantified project outcomes. | Product profile; standalone skills and certificate sections |

The Markdown, TeX sources and repository descriptions were read directly. Linked PDF artifacts establish the source formats; raw PDF delivery returned an unsupported content type in the web reader, so observations about those layouts were checked against their authoring sources rather than claiming a rendered-PDF inspection. Source links track upstream branches, not frozen snapshots. No external sample files are redistributed.

## Our sample set

[examples/profiles](../examples/profiles) contains six newly invented candidates, each in Chinese and English: graduate, frontend, backend, product, designer and data. Backend intentionally contains a long exercise log; frontend has a long URL; data has an unfamiliar section and a publication. All figures describe fictional demonstrations. Contact links use example.com.

The original bilingual product-engineer examples remain the identical-content comparison baseline across all 12 styles. Career previews cycle through the six new profiles using the first six styles in the style index. [scripts/build_previews.py](../scripts/build_previews.py) rebuilds the actual HTML, PDFs and screenshots.

## PDF input fixtures

The four input PDFs in [examples/pdf-input](../examples/pdf-input) are authored from scratch, not modified real resumes. Their expected Markdown is stored next to them. The single-column and two-column versions contain the same facts. The scan has no text layer. The mixed version contains one text page and one page with both machine text and an image-only achievement. Every page must be reviewed even when text extraction succeeds.

[scripts/build_pdf_fixtures.py](../scripts/build_pdf_fixtures.py) rebuilds these documents. The extra scan/mixed variants are deliberate parsing exercises, not design inspiration copied from any source. Output examples contain neither actual candidate contact data nor copied employer histories.
