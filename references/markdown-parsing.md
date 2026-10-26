# Supported Markdown

Use one H1 for the name, a plain role line, optional target role, header contacts and H2 sections. The skill normalizes unfamiliar input into a working copy without changing facts. The CLI itself expects this structure and does not infer a name from arbitrary Markdown or PDF.

```markdown
# Example Candidate

Backend Engineer
Target role: Platform Engineer
hello@example.com
Phone: +1 (000) 000-0000
[Portfolio](https://example.com/portfolio)

## Summary
A factual summary supplied by the resume owner.

## Skills
- Python, SQL

## Work Experience
### Example Studio | Engineer
*2023.04 - 2025.08*

Company-level description or achievements.

**Project Title** *(Web / Design)*
- Achievement supplied by the owner.

## Projects
### Independent Project
A project paragraph.
- A result supplied by the owner.

## Education
- **Example College** | Computing | Bachelor | 2021

## Certificates
- Example Course Completion (fictional)

## Research Addendum
This unfamiliar section remains in the output.
```

All entities above are fictional. The [original Chinese](../examples/resume.zh-CN.md) and [English](../examples/resume.en.md) examples remain supported; [career profiles](../examples/profiles) exercise more structures.

## Rich layouts and generic preservation

| Canonical section | Recognized headings |
| --- | --- |
| Profile | 个人简介, 简介, Profile, Summary, Professional Summary |
| Employment | 工作经历, 工作经验, Experience, Employment, Work Experience, Professional Experience |
| Early work | 早期项目, 早期项目与专利, 专利, Early Projects, Patents, Early Projects & Patents |
| Education | 教育背景, 教育, Education, 学历 |
| Gaming | 游戏经历, Gaming, Gaming Experience |

Recognized headings use translated interface labels according to --lang. Other headings retain their original text. Projects, skills, awards, certificates, publications and any unknown H2 are supported through generic content blocks. Section order and repeated sections are retained. Empty sections are omitted.

Canonical employment uses H3 company | role, an italic date, optional description, bold project headings and bullets. Canonical education uses school | detail rows. Rich layouts are used only when their parsed text retains the source facts; unfamiliar structures fall back to paragraphs/headings/lists instead of silently dropping content. --lang changes interface labels only, never the source body's language.

Generic blocks support paragraphs, subheadings, bold/italic text, unordered and numbered list items, and HTTP(S) Markdown links. Numbered items render as bullets. Blank lines separate paragraphs. Nested lists are flattened; tables and complex Markdown are displayed as escaped text, not interpreted as rich layout. The skill should convert those structures in its working copy when needed for a readable resume. Embedded HTML is escaped, never executed.

## Header contacts

Use plain email, Chinese mobile numbers, or an explicit Phone: / 电话: / 手机: line for other number formats. HTTP(S) header links include the first portfolio link, a GitHub link and additional general links. Put actual project URLs inside their sections; they must not be promoted into header contacts. Non-HTTP(S) Markdown links are not rendered as active links. This is not a comprehensive international phone parser.

Photos are optional to the CLI. The skill asks the user to upload one or choose a text-only header. Output source.md preserves the normalized input, and is not automatically anonymized.
