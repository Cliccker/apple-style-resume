# Apple-inspired resume design

Preserve the existing quiet, card-based visual language in both templates.

| Token | Value |
| --- | --- |
| Page / card / inset | `#FAFAFA` / `#FFFFFF` / `#F5F5F7` |
| Primary / secondary / metadata text | `#1D1D1F` / `#86868B` / `#A1A1A6` |
| Link / badge background | `#0071E3` / `#E8F4FD` |
| Border | `rgba(0,0,0,0.06)` |
| Card / inset / avatar radius | `24px` / `12–18px` / `20–28px` |
| Desktop card padding / gap | `32px` / `20px` |
| Mobile card padding / page gutter | `22px` / `16px` |
| Web content width | `960px` maximum |
| A4 margins | `16mm` top/bottom, `18mm` left/right |

Typography is part of the visual identity. Preserve the original font stack: `"Inter", "Noto Sans SC", -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif`. Recommend installing **Inter** and **Noto Sans SC** locally for faithful, offline rendering. System fonts are fallbacks, and their metrics can change line wrapping and PDF pagination. The README also offers an optional Google Fonts stylesheet. Do not bundle font binaries in the distribution.

Keep generous whitespace, a clear name/section/body hierarchy, rounded rectangular avatars, subtle card shadows and restrained blue links. Preserve readability on narrow screens. Disable motion for reduced-motion preferences and printing. Hide sections with no content. PDFs flow across A4 pages; subsequent employers start on a new page, while long projects may continue naturally.

These tokens are project choices inspired by Apple's visual language, not values prescribed by Apple. Reference the official [Typography](https://developer.apple.com/design/human-interface-guidelines/typography), [Layout](https://developer.apple.com/design/human-interface-guidelines/layout), [Color](https://developer.apple.com/design/human-interface-guidelines/color) guidelines and the [Mac website](https://www.apple.com/mac/). This independent project is not affiliated with Apple and includes no Apple logos, screenshots or proprietary fonts.
