# Brand Style Resume design

Read this document and the selected style's DESIGN.md before changing visual components. These are independent resume adaptations of company design systems, not official templates or evidence of hiring preference.

## Shared rules

- Preserve facts, section order and source language. Hide empty sections, retain unfamiliar headings and never shorten content to meet a page count.
- Use semantic text and safe links; keep PDF text selectable. Web width is at most 960px; narrow layouts use 16px gutters. A4 margins are 16mm vertical and 18mm horizontal.
- Name, role/contact, section, project and achievement levels must remain distinct. Minimum print body is 11.5px. Avoid fixed heights, broad break-inside rules and shrinking long resumes.
- Use local fonts by default with documented fallbacks. Online open fonts require --web-fonts. Do not bundle proprietary fonts, company marks or screenshots.
- Photos are optional after asking the user. Without one, the header is text-only. Reduced-motion and print disable motion.
- Apple retains the existing Inter / Noto Sans SC stack, palette and employer page breaks. Other styles use natural employer flow. Document adaptations separately from official evidence.

## Style index

| CLI ID | Design reference | Implementation |
| --- | --- | --- |
| `apple` | [Apple](references/styles/apple/DESIGN.md) | [CSS](assets/styles/apple.css) |
| `google-material` | [Google / Material 3](references/styles/google-material/DESIGN.md) | [CSS](assets/styles/google-material.css) |
| `microsoft-fluent` | [Microsoft / Fluent 2](references/styles/microsoft-fluent/DESIGN.md) | [CSS](assets/styles/microsoft-fluent.css) |
| `ibm-carbon` | [IBM / Carbon](references/styles/ibm-carbon/DESIGN.md) | [CSS](assets/styles/ibm-carbon.css) |
| `ant-design` | [Ant Group / Ant Design](references/styles/ant-design/DESIGN.md) | [CSS](assets/styles/ant-design.css) |
| `tencent-tdesign` | [Tencent / TDesign](references/styles/tencent-tdesign/DESIGN.md) | [CSS](assets/styles/tencent-tdesign.css) |
| `bytedance-arco` | [ByteDance / Arco](references/styles/bytedance-arco/DESIGN.md) | [CSS](assets/styles/bytedance-arco.css) |
| `douyin-semi` | [Douyin / Semi](references/styles/douyin-semi/DESIGN.md) | [CSS](assets/styles/douyin-semi.css) |
| `huawei-harmonyos` | [Huawei / HarmonyOS](references/styles/huawei-harmonyos/DESIGN.md) | [CSS](assets/styles/huawei-harmonyos.css) |
| `baidu-dls` | [Baidu / Light DLS](references/styles/baidu-dls/DESIGN.md) | [CSS](assets/styles/baidu-dls.css) |
| `adobe-spectrum` | [Adobe / Spectrum](references/styles/adobe-spectrum/DESIGN.md) | [CSS](assets/styles/adobe-spectrum.css) |
| `salesforce-lightning` | [Salesforce / Lightning](references/styles/salesforce-lightning/DESIGN.md) | [CSS](assets/styles/salesforce-lightning.css) |

The machine-readable style index is [assets/styles.json](assets/styles.json). Styles share content rendering, not identical visual composition. Desktop label grids, header treatments, project containers and typographic hierarchy are specified per style. Light themes only; no company logos or dark-mode variants are included.

## Existing DESIGN.md discovery

Checked 2026-10-26: [DesignMD Apple](https://www.designmd.co/d/apple), [Apple HIG catalog](https://designmd.app/library/apple-hig), [Fluent acrylic catalog](https://designmd.app/library/acrylic-fluent). These are community interpretations, not official company specifications. No content was copied: generic acrylic guidance is not appropriate for a resume, and a community document's availability alone does not establish redistribution rights. Official sources remain the basis of each adaptation.
