#!/usr/bin/env python3
"""Generate local web and A4 HTML resumes from structured Markdown."""

import re
import argparse
import json
from html import escape, unescape
from urllib.parse import urlsplit
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLES = json.loads((ROOT / 'assets/styles.json').read_text(encoding='utf-8'))


def section_key(title: str) -> str:
    title = title.lower().strip()
    for key, names in (
        ('profile', ('个人简介', '简介', 'profile', 'summary', 'professional summary')),
        ('gaming', ('游戏经历', 'gaming', 'gaming experience')),
        ('early', ('早期项目', '早期项目与专利', '专利', 'early projects', 'patents', 'early projects & patents')),
        ('experience', ('工作经历', '工作经验', 'experience', 'employment', 'work experience', 'professional experience')),
        ('education', ('教育背景', '教育', 'education', '学历')),
    ):
        if title in names:
            return key
    return 'generic'


def clean_markdown(text: str) -> str:
    """Remove markdown formatting from text."""
    text = re.sub(r"\*\*", "", text)  # bold
    text = re.sub(r"\*", "", text)    # italic
    text = re.sub(r"[【\[】\]]", "", text)  # brackets
    text = text.strip()
    return text


def parse_markdown_resume(md_text: str) -> dict:
    """Parse markdown resume into structured data."""
    data = {
        "name": "",
        "role": "",
        "intent_role": "",
        "email": "",
        "phone": "",
        "blog": "",
        "blog_url": "",
        "github": "",
        "github_url": "",
        "profile": "",
        "experiences": [],
        "early_works": [],
        "education": [],
        "gaming": [],
        "sections": [],
        "extra_contacts": [],
    }

    lines = md_text.split("\n")
    i = 0

    # Parse name (first h1)
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("# ") and not line.startswith("## "):
            data["name"] = line[2:].strip()
            i += 1
            break
        i += 1

    # Read the role and optional target role from the header only.
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("---") or line.startswith("## "):
            break
        clean = clean_markdown(line)
        if re.search(r"意向|求职|^target(?: role)?\s*:", clean, re.I):
            data["intent_role"] = clean
        elif (clean and not data["role"] and not line.startswith("[")
              and not re.search(r"@|https?://|github\.com|\d{11}|^(?:phone|电话|手机)\s*[:：]", line, re.I)):
            data["role"] = clean
        i += 1

    # Contacts belong to the header; project links must not become contacts.
    header_end = next((n for n, line in enumerate(lines) if line.startswith('## ')), len(lines))
    for line in lines[:header_end]:
        stripped = line.strip()
        email_match = re.search(r"[\w.-]+@[\w.-]+\.\w+", stripped)
        if email_match and not data["email"]:
            data["email"] = email_match.group(0)
        phone_match = re.search(r"(?<!\d)1[3-9]\d{9}(?!\d)", stripped)
        explicit_phone = re.search(r"(?:phone|电话|手机)\s*[:：]\s*(\+?[\d ()-]{7,})", stripped, re.I)
        if explicit_phone:
            data["phone"] = explicit_phone.group(1).strip()
        if phone_match and not data["phone"]:
            data["phone"] = phone_match.group(0)
        link_matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", stripped)
        for text, url in link_matches:
            if "github" in url.lower() or "github" in text.lower():
                data["github"] = text
                data["github_url"] = url
            elif not data["blog"]:
                data["blog"] = text
                data["blog_url"] = url
            else:
                data['extra_contacts'].append((text, url))

    # Find sections
    current_section = None
    for line in lines[i:]:
        if line.startswith("## "):
            title = line[3:].strip()
            current_section = {'key': section_key(title), 'title': title, 'lines': []}
            data['sections'].append(current_section)
        elif current_section is not None:
            current_section['lines'].append(line)

    sections = {}
    for section in data['sections']:
        sections.setdefault(section['key'], []).extend(section['lines'])

    # Parse profile - filter out --- separators
    if "profile" in sections:
        profile_lines = []
        for pl in sections["profile"]:
            if pl.strip().startswith("---"):
                continue
            profile_lines.append(pl)
        profile_text = " ".join(profile_lines).strip()
        profile_text = re.sub(r"\s+", " ", profile_text)
        data["profile"] = profile_text

    # Parse experience
    if "experience" in sections:
        data["experiences"] = parse_experience(sections["experience"])

    # Parse early work
    if "early" in sections:
        data["early_works"] = parse_early_work(sections["early"])

    # Parse education
    if "education" in sections:
        data["education"] = parse_education(sections["education"])

    # Parse gaming
    if "gaming" in sections:
        data["gaming"] = parse_gaming(sections["gaming"])

    return data


def parse_experience(lines: list) -> list:
    """Parse work experience section."""
    experiences = []
    current_exp = None
    current_project = None

    for line in lines:
        stripped = line.rstrip()
        if not stripped:
            continue

        # Company heading: ### Company | Role
        if stripped.startswith("### "):
            if current_exp:
                if current_project:
                    current_exp["projects"].append(current_project)
                    current_project = None
                experiences.append(current_exp)

            text = stripped[4:]
            # Split company and role by |
            parts = text.split("|")
            company = clean_markdown(parts[0]).strip()
            role = clean_markdown(parts[1]).strip() if len(parts) > 1 else ""

            current_exp = {
                "company": company,
                "role": role,
                "date": "",  # Will be filled from next line
                "description": "",
                "projects": [],
            }
            current_project = None

        # Date line (italic, right after company heading)
        elif (stripped.startswith("*") and not stripped.startswith("**")
              and stripped.endswith("*") and current_exp and not current_exp["date"]):
            date_match = re.search(r"\*(.+?)\*", stripped)
            if date_match:
                current_exp["date"] = date_match.group(1)

        # Project heading: **【Project Name】** *(meta)* or **Project Name** *(meta)*
        elif stripped.startswith("**") and any(m in stripped for m in ["**", "【"]):
            if current_exp and current_project:
                current_exp["projects"].append(current_project)

            # Extract all content between ** markers
            title_parts = re.findall(r"\*\*(.+?)\*\*", stripped)
            meta_match = re.search(r"\*(\(.+?\))\*", stripped)

            title = clean_markdown(title_parts[0]) if title_parts else clean_markdown(stripped)
            meta = clean_markdown(meta_match.group(1)) if meta_match else ""

            current_project = {
                "title": title,
                "meta": meta,
                "bullets": [],
            }

        # Bullet points
        elif re.match(r"^[\-*]\s", stripped):
            bullet = re.sub(r"^[\-*]\s*", "", stripped)
            # Clean leading **bold_key：** pattern
            bullet = clean_markdown(bullet)
            bullet = bullet.strip()
            if bullet and current_project:
                current_project["bullets"].append(bullet)
            elif bullet and current_exp and not current_project:
                # Bullet without a project: treat as company-level description
                if current_exp["description"]:
                    current_exp["description"] += " " + bullet
                else:
                    current_exp["description"] = bullet

        # Regular description text (not a heading, not a bullet)
        elif current_exp and not stripped.startswith("#"):
            clean = clean_markdown(stripped)
            if clean and not clean.startswith("---"):
                if current_project:
                    current_project.setdefault('paragraphs', []).append(clean)
                elif current_exp["description"]:
                    current_exp["description"] += " " + clean
                else:
                    current_exp["description"] = clean

    # Close final items
    if current_exp:
        if current_project:
            current_exp["projects"].append(current_project)
        experiences.append(current_exp)

    return experiences


def parse_early_work(lines: list) -> list:
    """Parse early work / patents section."""
    works = []
    for line in lines:
        stripped = line.strip()
        if not stripped or not re.match(r"^[\-*]\s", stripped):
            continue
        text = re.sub(r"^[\-*]\s*", "", stripped)
        # Extract bold title
        title_match = re.search(r"\*\*(.+?)\*\*", text)
        title = clean_markdown(title_match.group(1)) if title_match else ""
        # Clean detail
        detail = clean_markdown(text)
        # Remove title from detail if it was extracted
        if title and title in detail:
            detail = detail.replace(title, "", 1).strip()
        detail = re.sub(r"^[（(].*?[)）]", "", detail).strip()
        detail = detail.lstrip(":：").strip()

        # Extract year
        year_match = re.search(r"[（(](\d{4}[^）)]*)[）)]", text)
        year = year_match.group(1) if year_match else ""

        if title:
            full_title = f"{title}（{year}）" if year else title
            works.append({"title": full_title, "detail": detail})
    return works


def parse_education(lines: list) -> list:
    """Parse education section."""
    education = []
    for line in lines:
        stripped = line.strip()
        if not stripped or not re.match(r"^[\-*]\s", stripped):
            continue
        text = re.sub(r"^[\-*]\s*", "", stripped)
        parts = [clean_markdown(p).strip() for p in text.split("|")]
        if len(parts) >= 2:
            school = parts[0]
            detail_parts = parts[1:]
            detail = " · ".join(filter(None, detail_parts))
            education.append({"school": school, "detail": detail})
    return education


def parse_gaming(lines: list) -> list:
    """Parse gaming section. Returns list of platform groups."""
    platforms = []
    current_platform = None

    for line in lines:
        stripped = line.rstrip()
        if not stripped:
            continue

        # Platform heading: **Platform Name**
        if stripped.startswith("**") and stripped.endswith("**"):
            if current_platform:
                platforms.append(current_platform)
            platform_name = clean_markdown(stripped)
            current_platform = {
                "name": platform_name,
                "games": [],
            }

        # Game entry: - Game Name — Xh
        elif re.match(r"^[\-*]\s", stripped) and current_platform:
            text = re.sub(r"^[\-*]\s*", "", stripped)
            text = clean_markdown(text)
            # Split by em-dash or en-dash
            parts = re.split(r"[\—\–\-]\s*", text, maxsplit=1)
            if len(parts) >= 2:
                game_name = parts[0].strip()
                hours = parts[1].strip()
                current_platform["games"].append({
                    "name": game_name,
                    "hours": hours,
                })
            else:
                current_platform["games"].append({
                    "name": text.strip(),
                    "hours": "",
                })

    if current_platform:
        platforms.append(current_platform)

    return platforms


LABELS = {
    "zh-CN": {
        "PROFILE_TITLE": "个人简介", "EXPERIENCE_TITLE": "工作经历",
        "EARLY_SECTION_TITLE": "早期项目与专利", "EDUCATION_TITLE": "教育背景",
        "GAMING_TITLE": "游戏经历", "FOOTER_TEXT": "用心设计",
    },
    "en": {
        "PROFILE_TITLE": "Profile", "EXPERIENCE_TITLE": "Experience",
        "EARLY_SECTION_TITLE": "Early Projects & Patents", "EDUCATION_TITLE": "Education",
        "GAMING_TITLE": "Gaming Experience", "FOOTER_TEXT": "Designed with care",
    },
}


def inline_markdown(text: str) -> str:
    """Render a small, escaped inline subset; never accept source HTML."""
    parts = []
    position = 0
    for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', text):
        parts.append(escape(text[position:match.start()], quote=True))
        label, url = match.groups()
        label = escape(label, quote=True)
        if urlsplit(url).scheme.lower() in ('http', 'https'):
            parts.append(f'<a href="{escape(url, quote=True)}" rel="noopener noreferrer">{label}</a>')
        else:
            parts.append(label)
        position = match.end()
    parts.append(escape(text[position:], quote=True))
    result = ''.join(parts)
    result = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', result)
    result = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', result)
    return result


def render_blocks(lines: list) -> str:
    """Preserve paragraphs, headings and list items in arbitrary resume sections."""
    blocks, paragraph = [], []
    in_list = False

    def flush():
        if paragraph:
            blocks.append('<p>' + inline_markdown(' '.join(paragraph)) + '</p>')
            paragraph.clear()

    for line in [*lines, '']:
        text = line.strip()
        bullet = re.match(r'^(?:[-*+]\s+|\d+[.)]\s+)(.*)', text)
        if not bullet and in_list:
            blocks.append('</ul>')
            in_list = False
        if not text or re.fullmatch(r'[-*_]{3,}', text):
            flush()
        elif bullet:
            flush()
            if not in_list:
                blocks.append('<ul>')
                in_list = True
            blocks.append('<li>' + inline_markdown(bullet.group(1)) + '</li>')
        elif text.startswith('#') or (text.startswith('**') and text.endswith('**')):
            flush()
            blocks.append('<h3>' + inline_markdown(re.sub(r'^#{1,6}\s*', '', text)) + '</h3>')
        else:
            paragraph.append(text)
    return ''.join(blocks)


def _render(data: dict, lang: str, photo: str, pdf: bool, web_fonts: bool, style: str) -> str:
    """Fill the two existing layouts, escaping all user-supplied text."""
    filename = "resume_pdf_template.html" if pdf else "resume_template.html"
    template = (ROOT / "assets" / filename).read_text(encoding="utf-8")
    if style not in STYLES:
        raise ValueError(f'Unknown style: {style}')
    theme = STYLES[style]
    h = lambda value: escape(str(value), quote=True)
    values = {key: h(value) for key, value in LABELS[lang].items()}
    values.update({"LANG": lang, "NAME": h(data["name"]), "ROLE": h(data["role"]),
                   "PHOTO": h(photo or ''), "PROFILE": h(data["profile"]), 'STYLE': style})
    values['STYLE_CSS'] = ((ROOT / 'assets/styles/common.css').read_text(encoding='utf-8') + '\n' +
                           (ROOT / 'assets/styles' / f'{style}.css').read_text(encoding='utf-8'))
    values['FONT_LINK'] = (f'<link rel="stylesheet" href="{h(theme["web_fonts"])}">' if web_fonts else '')
    values['AVATAR'] = f'<img src="{h(photo)}" alt="{h(data["name"])}" class="avatar">' if photo else ''
    values["INTENT_ROLE_BADGE"] = (
        f'<span class="role-badge">{h(data["intent_role"])}</span>' if data["intent_role"] else ""
    )
    values["ROLE_LINE"] = f'<strong>{h(data["role"])}</strong>'
    if data["intent_role"]:
        values["ROLE_LINE"] += " · " + h(data["intent_role"])

    contacts = [h(data[key]) for key in ("email", "phone") if data[key]]
    for key in ("blog", "github"):
        label, url = data[key], data[key + "_url"]
        if label and url and urlsplit(url).scheme.lower() in ("https", "http"):
            contacts.append(f'<a href="{h(url)}" target="_blank" rel="noopener noreferrer">{h(label)}</a>')
    for label, url in data.get('extra_contacts', []):
        if urlsplit(url).scheme.lower() in ('https', 'http'):
            contacts.append(f'<a href="{h(url)}" rel="noopener noreferrer">{h(label)}</a>')
    values["CONTACT_INFO"] = '<span class="divider-dot">&#183;</span>'.join(contacts)
    values["CONTACT_LINE"] = '<span class="divider">|</span>'.join(contacts)

    experiences = []
    for exp in data["experiences"]:
        outer = "exp-block" if pdf else "exp-item"
        role_class = "exp-role-tag" if pdf else "exp-role-inline"
        role_text = (" · " if pdf and exp["role"] else "") + exp["role"]
        body = (f'<div class="{outer}"><div class="exp-header"><div class="exp-company-role">'
                f'<span class="exp-company">{h(exp["company"])}</span>'
                f'<span class="{role_class}">{h(role_text)}</span></div>'
                f'<span class="exp-date">{h(exp["date"])}</span></div>')
        if exp["description"]:
            cls = "exp-overview" if pdf else "exp-desc"
            body += f'<p class="{cls}">{h(exp["description"])}</p>'
        if exp["projects"]:
            body += '<div class="project-list">'
            for project in exp["projects"]:
                cls = "project" if pdf else "project-item"
                bullets = "".join(f'<li>{h(item)}</li>' for item in project["bullets"])
                body += (f'<div class="{cls}"><div class="project-title">{h(project["title"])}'
                         f' <span class="project-meta">{h(project["meta"])}</span></div>'
                         f'<div class="project-body"><ul>{bullets}</ul>' +
                         ''.join(f'<p>{h(p)}</p>' for p in project.get('paragraphs', [])) + '</div></div>')
            body += '</div>'
        experiences.append(body + '</div>')
    values["EXPERIENCE_SECTIONS"] = "\n".join(experiences)
    values["EARLY_WORK_ITEMS"] = "".join(
        f'<div class="early-item"><div class="early-content"><div class="early-title">{h(item["title"])}</div>'
        f'<div class="early-detail">{h(item["detail"])}</div></div></div>' for item in data["early_works"]
    )
    detail_class = "edu-detail" if pdf else "edu-major"
    values["EDUCATION_ITEMS"] = "".join(
        f'<div class="edu-item"><div class="edu-content"><div class="edu-school">{h(item["school"])}</div>'
        f'<div class="{detail_class}">{h(item["detail"])}</div></div></div>' for item in data["education"]
    )
    gaming = []
    for platform in data.get("gaming", []):
        if pdf:
            games = ", ".join(h(game["name"]) + (f' ({h(game["hours"])})' if game["hours"] else "")
                              for game in platform["games"])
            gaming.append(f'<div class="gaming-item"><div class="gaming-platform">{h(platform["name"])}</div>'
                          f'<div class="gaming-games">{games}</div></div>')
        else:
            games = "".join(f'<div class="gaming-game">{h(game["name"])}' +
                            (f'<span class="gaming-hours">{h(game["hours"])}</span>' if game["hours"] else "") + '</div>'
                            for game in platform["games"])
            gaming.append(f'<div class="gaming-platform"><div class="gaming-platform-name">{h(platform["name"])}</div>'
                          f'<div class="gaming-games">{games}</div></div>')
    values["GAMING_ITEMS"] = "".join(gaming)

    # Raw sections preserve order, repeated headings, and unfamiliar structures.
    # Use the established rich layouts only for their supported canonical shape.
    if 'sections' in data:
        rendered_sections = []
        counts = {key: sum(s['key'] == key for s in data['sections'])
                  for key in ('profile', 'experience', 'early', 'education', 'gaming')}
        titles = {'profile': 'PROFILE_TITLE', 'experience': 'EXPERIENCE_TITLE',
                  'early': 'EARLY_SECTION_TITLE', 'education': 'EDUCATION_TITLE', 'gaming': 'GAMING_TITLE'}
        for section in data['sections']:
            key = section['key']
            lines = [line for line in section['lines'] if line.strip() and line.strip() != '---']
            if not lines:
                continue
            generic_content = '<div class="generic-block">' + render_blocks(section['lines']) + '</div>'
            content = generic_content
            single = counts.get(key) == 1
            if key == 'profile' and single and not any(re.match(r'^\s*(?:#|[-*+]\s)', line) for line in lines):
                content = f'<p class="profile-text">{inline_markdown(data["profile"])}</p>'
            elif (key == 'experience' and single and lines[0].startswith('### ')
                  and not any('](' in line or (line.startswith('#') and not line.startswith('### ')) for line in lines)):
                content = '<div class="experience-list">' + values['EXPERIENCE_SECTIONS'] + '</div>'
            elif key == 'early' and single and all(re.match(r'^[-*]\s+\*\*.+?\*\*', line) for line in lines):
                content = '<div class="early-list early-grid">' + values['EARLY_WORK_ITEMS'] + '</div>'
            elif key == 'education' and single and all(re.match(r'^[-*]\s+.+\|', line) for line in lines):
                content = '<div class="edu-list edu-grid">' + values['EDUCATION_ITEMS'] + '</div>'
            elif key == 'gaming' and single and lines[0].startswith('**') and all(
                    re.match(r'^(?:\*\*.+\*\*|[-*]\s+.+)$', line) for line in lines):
                content = '<div class="gaming-list gaming-grid">' + values['GAMING_ITEMS'] + '</div>'
            if key != 'profile' and content != generic_content:
                # A noncanonical entry must not lose facts just to fit a rich layout.
                normalize = lambda text: re.sub(r'[\W_]+', '', text).casefold()
                source_text = normalize(' '.join(lines))
                rendered_text = normalize(unescape(re.sub(r'<[^>]*>', '', content)))
                if source_text != rendered_text or any('](' in line for line in lines):
                    content = generic_content
            title = values[titles[key]] if key in titles else h(section['title'])
            heading = 'section-title' if pdf else 'card-section-title'
            rendered_sections.append(f'<section class="resume-section card" data-section="{key}">'
                                     f'<h2 class="{heading}">{title}</h2>{content}</section>')
        # Replace the fixed section region, leaving header and footer untouched.
        values['SECTIONS'] = '\n'.join(rendered_sections)
        template = re.sub(r'<!-- START:PROFILE -->.*<!-- END:GAMING -->',
                          '{{SECTIONS}}', template, flags=re.S)

    for section, content in (("PROFILE", data["profile"]), ("EXPERIENCE", data["experiences"]),
                             ("EARLY", data["early_works"]), ("EDUCATION", data["education"]),
                             ("GAMING", data.get("gaming"))):
        if not content:
            template = re.sub(r'<!-- START:' + section + r' -->.*?<!-- END:' + section + r' -->',
                              "", template, flags=re.S)
    return re.sub(r'\{\{([A-Z_]+)\}\}', lambda match: values[match.group(1)], template)


def render_web_template(data: dict, lang: str = "zh-CN", photo: str = "photo.jpg", web_fonts: bool = False,
                        style: str = 'apple') -> str:
    return _render(data, lang, photo, pdf=False, web_fonts=web_fonts, style=style)


def render_pdf_template(data: dict, lang: str = "zh-CN", photo: str = "photo.jpg", web_fonts: bool = False,
                        style: str = 'apple') -> str:
    return _render(data, lang, photo, pdf=True, web_fonts=web_fonts, style=style)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs='?', type=Path, help="Structured Markdown resume")
    parser.add_argument("paths", nargs='*', type=Path, help="OUTPUT or legacy PHOTO OUTPUT")
    parser.add_argument('--photo', type=Path, help='Optional JPG or PNG portrait')
    parser.add_argument('--style', choices=STYLES, default='apple')
    parser.add_argument('--list-styles', action='store_true')
    parser.add_argument("--lang", choices=LABELS, default="zh-CN", help="Interface language; body text is not translated")
    parser.add_argument("--web-fonts", action="store_true", help="Load the selected style's open web fonts (requires network)")
    args = parser.parse_args()
    if args.list_styles:
        for name, theme in STYLES.items():
            print(f'{name:24} {theme["name"]}')
        return
    if args.input is None or len(args.paths) not in (1, 2):
        parser.error('Use INPUT OUTPUT [--photo PHOTO] or INPUT PHOTO OUTPUT.')
    if len(args.paths) == 2:
        if args.photo:
            parser.error('Do not combine a positional photo with --photo.')
        args.photo = args.paths[0]
    args.output = args.paths[-1]
    if not args.input.is_file() or (args.photo and not args.photo.is_file()):
        parser.error("Input Markdown and photo must be existing files.")
    if args.input.suffix.lower() != '.md':
        parser.error('Prepare PDF input with scripts/prepare_pdf.py, then review/normalize its text as Markdown.')
    if args.photo and args.photo.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        parser.error("Photo must be JPG, JPEG or PNG.")
    data = parse_markdown_resume(args.input.read_text(encoding="utf-8-sig"))
    if not data["name"]:
        parser.error("Resume must contain a '# Name' heading.")
    args.output.mkdir(parents=True, exist_ok=True)
    photo_name = None
    if args.photo:
        photo_name = "photo" + args.photo.suffix.lower()
        photo_dest = args.output / photo_name
        if args.photo.resolve() != photo_dest.resolve():
            shutil.copyfile(args.photo, photo_dest)
    source_dest = args.output / 'source.md'
    if args.input.resolve() != source_dest.resolve():
        shutil.copyfile(args.input, source_dest)
    for filename, render in (("index.html", render_web_template), ("resume_a4.html", render_pdf_template)):
        (args.output / filename).write_text(render(data, args.lang, photo_name, args.web_fonts, style=args.style), encoding="utf-8")
        print(f"Created {filename}")
    print("For PDF export, run scripts/export_pdf.py on resume_a4.html.")


if __name__ == "__main__":
    main()
