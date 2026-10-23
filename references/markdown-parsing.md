# Supported Markdown

The parser accepts this deliberately small structure, not arbitrary Markdown or HTML:

```markdown
# Example Candidate

Product Engineer
Target role: Product Experience Engineer

hello@example.com
[Portfolio](https://example.com/portfolio)

---

## Summary
A factual summary provided by the resume owner.

## Work Experience
### Example Studio | Product Engineer
*2023.04 - 2025.08*

Company-level description or bullet points.

**Project Title** *(Web / Design)*
- Achievement supplied by the owner.

## Early Projects
- **Project Title** (2021): Description.

## Education
- **Example College** | Computing | Bachelor | 2021

## Gaming Experience
**Example Platform**
- Example Game — 40 hours
```

All entities above are fictional. See the complete [Chinese](../examples/resume.zh-CN.md) and [English](../examples/resume.en.md) examples.

| Section | Recognized headings |
| --- | --- |
| Profile | `个人简介`, `Profile`, `Summary` |
| Employment | `工作经历`, `Experience`, `Work Experience` |
| Early projects | `早期项目`, `项目`, `专利`, `Projects`, `Patents` |
| Education | `教育背景`, `Education` |
| Gaming | `游戏经历`, `Gaming`, `Gaming Experience` |

Use a single H1 for the name, a plain role line and an optional `意向岗位：…` or `Target role: …` line. Use H2 for sections, H3 for employers and bold standalone project titles. Put the employer's italic date range before its projects. Company-level bullets work without a project heading. Keep each section present only once. Omit sections with no information.

Contacts are plain email addresses and Markdown links using `https://` or `http://`. Only the first general portfolio link and the GitHub link are retained. Chinese mobile numbers are recognized; other phone formats can use a dedicated `Phone: …` line. No phone number is included in the public examples. This is not a comprehensive international phone parser.

Basic bold/italic markers are stripped. Lists become achievements. The renderer escapes text and attribute values; embedded HTML, arbitrary inline Markdown and Markdown tables are not supported. Do not expect rich-text formatting in the body. `--lang` changes the template labels only, so source content should already be in the intended language.
