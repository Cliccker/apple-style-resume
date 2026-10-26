# Ant Group / Ant Design: resume design

Collected / checked: **2026-10-26**. Independent interpretation; not an official resume template or hiring recommendation.

## Official evidence

- Primary source: https://ant.design/docs/spec/font/

Ant prefers system fonts, a 14px base size, a deliberate type scale and tabular figures for aligned numbers.

These statements summarize the cited design system. They do not imply that the company prescribes the tokens or document layout below. Dynamic official sites may require JavaScript; use the linked official repository or resources to recheck details.

## Resume adaptation

Compact section headings, 8px spacing rhythm, a thin experience timeline and aligned metadata; no dashboard controls in the resume.

All following values are **project-selected resume tokens**, including adjustments for paper, CJK reading and accessible text. They are not a reproduction of the complete upstream token set.

| Role | Value |
| --- | --- |
| Page / card / inset | `#F5F5F5` / `#FFFFFF` / `#FAFAFA` |
| Heading / body / metadata | `#141414` / `#434343` / `#595959` |
| Accent / accent surface | `#1677FF` / `#E6F4FF` |
| Card / inset radius | `6px` / `4px` |
| Desktop card padding / gap | `24px` / `16px` |
| Mobile gutter / maximum content width | `16px` / `960px` |
| Web name / body / metadata | `28–48px` / `13–14px` / `12–13px` |
| Print name / body / metadata | `28px` / `11.5–12px` / `11–12px` |
| A4 page / margins | `210 × 297mm` / `16mm vertical, 18mm horizontal` |

Font stack: `system-ui, "Noto Sans SC", "Segoe UI", "Microsoft YaHei", sans-serif`. Local fonts are preferred. `--web-fonts` loads Noto Sans SC only; it does not download or substitute proprietary brand fonts. Missing local brand fonts fall back as listed and can change pagination. Font binaries are not distributed.

## Hierarchy and components

Name → role/contact → section label → company/project title → narrative and achievements → dates. Use weight and alignment before decoration. Preserve input section order and facts. No logos, fake controls or decorative text images. The style sheet implements the particular header, section and project treatment described above, beyond a palette change.

## Responsive and print behavior

Below 600px, wrap identity/contact rows and dates, collapse label/content grids and retain 16px outer gutters. A photo is optional; never reserve an empty avatar box. Disable movement for reduced-motion preferences and print. PDF uses solid surfaces, selectable text and a single reading column. Keep headings with following text, allow long sections to flow and avoid fixed-height clipping. Employers flow naturally without forced page breaks.

Implementation: [style sheet](../../../assets/styles/ant-design.css). Shared constraints: [root design](../../../DESIGN.md).

## Provenance and reuse

Official guidance was summarized rather than copied. No official images, logos, font files or components are redistributed. Third-party DESIGN.md catalogs are discovery aids only; no third-party DESIGN.md text is incorporated. Exact source versions are not bundled: recheck upstream guidance when updating this adaptation.
