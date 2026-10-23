#!/usr/bin/env python3
"""Generate local web and A4 HTML resumes from structured Markdown."""

import re
import argparse
from html import escape
from urllib.parse import urlsplit
import shutil
from pathlib import Path


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

    # Parse contact info from all lines
    for line in lines:
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

    # Find sections
    sections = {}
    current_section = None
    current_content = []

    for line in lines[i:]:
        if line.startswith("## "):
            if current_section:
                sections[current_section] = current_content
            title = line[3:].strip().lower()
            if any(k in title for k in ["简介", "profile", "summary"]):
                current_section = "profile"
            elif any(k in title for k in ["游戏", "gaming"]):
                current_section = "gaming"
            elif any(k in title for k in ["经历", "experience", "工作", "work"]):
                current_section = "experience"
            elif any(k in title for k in ["早期", "项目", "patent", "projects", "专利"]):
                current_section = "early"
            elif any(k in title for k in ["教育", "education", "学历"]):
                current_section = "education"
            else:
                current_section = title
            current_content = []
        elif current_section is not None:
            current_content.append(line)

    if current_section:
        sections[current_section] = current_content

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
        elif stripped.startswith("*") and stripped.endswith("*") and current_exp and not current_exp["date"]:
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
        elif current_exp and not current_project and not stripped.startswith("#"):
            clean = clean_markdown(stripped)
            if clean and not clean.startswith("---"):
                if current_exp["description"]:
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


def _render(data: dict, lang: str, photo: str, pdf: bool, web_fonts: bool) -> str:
    """Fill the two existing layouts, escaping all user-supplied text."""
    filename = "resume_pdf_template.html" if pdf else "resume_template.html"
    template = (Path(__file__).resolve().parent.parent / "assets" / filename).read_text(encoding="utf-8")
    h = lambda value: escape(str(value), quote=True)
    values = {key: h(value) for key, value in LABELS[lang].items()}
    values.update({"LANG": lang, "NAME": h(data["name"]), "ROLE": h(data["role"]),
                   "PHOTO": h(photo), "PROFILE": h(data["profile"])})
    values["FONT_LINK"] = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
                           'family=Inter:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@400;500;600;700&amp;display=swap">'
                           if web_fonts else "")
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
    values["CONTACT_INFO"] = '<span class="divider-dot">&#183;</span>'.join(contacts)
    values["CONTACT_LINE"] = '<span class="divider">|</span>'.join(contacts)

    experiences = []
    for index, exp in enumerate(data["experiences"]):
        outer = "exp-block" + (" page-break" if index else "") if pdf else "exp-item"
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
                         f'<div class="project-body"><ul>{bullets}</ul></div></div>')
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

    for section, content in (("PROFILE", data["profile"]), ("EXPERIENCE", data["experiences"]),
                             ("EARLY", data["early_works"]), ("EDUCATION", data["education"]),
                             ("GAMING", data.get("gaming"))):
        if not content:
            template = re.sub(r'<!-- START:' + section + r' -->.*?<!-- END:' + section + r' -->',
                              "", template, flags=re.S)
    return re.sub(r'\{\{([A-Z_]+)\}\}', lambda match: values[match.group(1)], template)


def render_web_template(data: dict, lang: str = "zh-CN", photo: str = "photo.jpg", web_fonts: bool = False) -> str:
    return _render(data, lang, photo, pdf=False, web_fonts=web_fonts)


def render_pdf_template(data: dict, lang: str = "zh-CN", photo: str = "photo.jpg", web_fonts: bool = False) -> str:
    return _render(data, lang, photo, pdf=True, web_fonts=web_fonts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Structured Markdown resume")
    parser.add_argument("photo", type=Path, help="JPG or PNG portrait")
    parser.add_argument("output", type=Path, help="Destination directory")
    parser.add_argument("--lang", choices=LABELS, default="zh-CN", help="Interface language; body text is not translated")
    parser.add_argument("--web-fonts", action="store_true", help="Load Inter and Noto Sans SC from Google Fonts (requires network)")
    args = parser.parse_args()
    if not args.input.is_file() or not args.photo.is_file():
        parser.error("Input Markdown and photo must be existing files.")
    if args.photo.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        parser.error("Photo must be JPG, JPEG or PNG.")
    data = parse_markdown_resume(args.input.read_text(encoding="utf-8-sig"))
    if not data["name"]:
        parser.error("Resume must contain a '# Name' heading.")
    args.output.mkdir(parents=True, exist_ok=True)
    photo_name = "photo" + args.photo.suffix.lower()
    photo_dest = args.output / photo_name
    if args.photo.resolve() != photo_dest.resolve():
        shutil.copyfile(args.photo, photo_dest)
    for filename, render in (("index.html", render_web_template), ("resume_a4.html", render_pdf_template)):
        (args.output / filename).write_text(render(data, args.lang, photo_name, args.web_fonts), encoding="utf-8")
        print(f"Created {filename}")
    print("For PDF export, run scripts/export_pdf.py on resume_a4.html.")


if __name__ == "__main__":
    main()
