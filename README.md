# Brand Style Resume

把 Markdown 或 PDF 简历转换为国内外公司设计语言启发的响应式网页与 A4 PDF。首批包含 12 套风格，支持中文、英文、额外章节和可选照片。它们是独立的设计改编，不是公司官方简历模板，也不承诺提高录用概率。

**简体中文** · [English](README.en.md)

## 风格画廊

[打开本地画廊](examples/preview/index.html)。GitHub 会显示 HTML 源码，请下载仓库后用浏览器打开。所有风格使用同一份虚构简历便于比较；头像为原创几何占位图，人物、组织、学校、时间和成果均为虚构。

![前六套风格的中英文桌面比较](docs/images/gallery/desktop-1.png)
![后六套风格的中英文桌面比较](docs/images/gallery/desktop-2.png)

| 风格 / 规范 | 中文网页 / PDF | English web / PDF |
| --- | --- | --- |
| [Apple](references/styles/apple/DESIGN.md) `apple` | [HTML](examples/preview/styles/apple/zh-CN/index.html) · [PDF](examples/preview/styles/apple/zh-CN/resume.pdf) | [HTML](examples/preview/styles/apple/en/index.html) · [PDF](examples/preview/styles/apple/en/resume.pdf) |
| [Google / Material 3](references/styles/google-material/DESIGN.md) `google-material` | [HTML](examples/preview/styles/google-material/zh-CN/index.html) · [PDF](examples/preview/styles/google-material/zh-CN/resume.pdf) | [HTML](examples/preview/styles/google-material/en/index.html) · [PDF](examples/preview/styles/google-material/en/resume.pdf) |
| [Microsoft / Fluent 2](references/styles/microsoft-fluent/DESIGN.md) `microsoft-fluent` | [HTML](examples/preview/styles/microsoft-fluent/zh-CN/index.html) · [PDF](examples/preview/styles/microsoft-fluent/zh-CN/resume.pdf) | [HTML](examples/preview/styles/microsoft-fluent/en/index.html) · [PDF](examples/preview/styles/microsoft-fluent/en/resume.pdf) |
| [IBM / Carbon](references/styles/ibm-carbon/DESIGN.md) `ibm-carbon` | [HTML](examples/preview/styles/ibm-carbon/zh-CN/index.html) · [PDF](examples/preview/styles/ibm-carbon/zh-CN/resume.pdf) | [HTML](examples/preview/styles/ibm-carbon/en/index.html) · [PDF](examples/preview/styles/ibm-carbon/en/resume.pdf) |
| [Ant Group / Ant Design](references/styles/ant-design/DESIGN.md) `ant-design` | [HTML](examples/preview/styles/ant-design/zh-CN/index.html) · [PDF](examples/preview/styles/ant-design/zh-CN/resume.pdf) | [HTML](examples/preview/styles/ant-design/en/index.html) · [PDF](examples/preview/styles/ant-design/en/resume.pdf) |
| [Tencent / TDesign](references/styles/tencent-tdesign/DESIGN.md) `tencent-tdesign` | [HTML](examples/preview/styles/tencent-tdesign/zh-CN/index.html) · [PDF](examples/preview/styles/tencent-tdesign/zh-CN/resume.pdf) | [HTML](examples/preview/styles/tencent-tdesign/en/index.html) · [PDF](examples/preview/styles/tencent-tdesign/en/resume.pdf) |
| [ByteDance / Arco](references/styles/bytedance-arco/DESIGN.md) `bytedance-arco` | [HTML](examples/preview/styles/bytedance-arco/zh-CN/index.html) · [PDF](examples/preview/styles/bytedance-arco/zh-CN/resume.pdf) | [HTML](examples/preview/styles/bytedance-arco/en/index.html) · [PDF](examples/preview/styles/bytedance-arco/en/resume.pdf) |
| [Douyin / Semi](references/styles/douyin-semi/DESIGN.md) `douyin-semi` | [HTML](examples/preview/styles/douyin-semi/zh-CN/index.html) · [PDF](examples/preview/styles/douyin-semi/zh-CN/resume.pdf) | [HTML](examples/preview/styles/douyin-semi/en/index.html) · [PDF](examples/preview/styles/douyin-semi/en/resume.pdf) |
| [Huawei / HarmonyOS](references/styles/huawei-harmonyos/DESIGN.md) `huawei-harmonyos` | [HTML](examples/preview/styles/huawei-harmonyos/zh-CN/index.html) · [PDF](examples/preview/styles/huawei-harmonyos/zh-CN/resume.pdf) | [HTML](examples/preview/styles/huawei-harmonyos/en/index.html) · [PDF](examples/preview/styles/huawei-harmonyos/en/resume.pdf) |
| [Baidu / Light DLS](references/styles/baidu-dls/DESIGN.md) `baidu-dls` | [HTML](examples/preview/styles/baidu-dls/zh-CN/index.html) · [PDF](examples/preview/styles/baidu-dls/zh-CN/resume.pdf) | [HTML](examples/preview/styles/baidu-dls/en/index.html) · [PDF](examples/preview/styles/baidu-dls/en/resume.pdf) |
| [Adobe / Spectrum](references/styles/adobe-spectrum/DESIGN.md) `adobe-spectrum` | [HTML](examples/preview/styles/adobe-spectrum/zh-CN/index.html) · [PDF](examples/preview/styles/adobe-spectrum/zh-CN/resume.pdf) | [HTML](examples/preview/styles/adobe-spectrum/en/index.html) · [PDF](examples/preview/styles/adobe-spectrum/en/resume.pdf) |
| [Salesforce / Lightning](references/styles/salesforce-lightning/DESIGN.md) `salesforce-lightning` | [HTML](examples/preview/styles/salesforce-lightning/zh-CN/index.html) · [PDF](examples/preview/styles/salesforce-lightning/zh-CN/resume.pdf) | [HTML](examples/preview/styles/salesforce-lightning/en/index.html) · [PDF](examples/preview/styles/salesforce-lightning/en/resume.pdf) |

完整桌面、移动端及每一页 PDF 截图保存在对应预览目录。[公共设计规则](DESIGN.md)链接到各风格的官方来源、采集日期、设计原则、排版 token 及项目改编说明。网上现成 DESIGN.md 的检索结果也在其中说明，未直接复制第三方规范。

## 安装与迁移

需要 Node.js 22.20+ 和 npm；通过 [Vercel Skills CLI](https://github.com/vercel-labs/skills) 安装，仓库地址保持不变：

```bash
npx skills add Cliccker/apple-style-resume --skill brand-style-resume -a codex -y
# 用户范围安装
npx skills add Cliccker/apple-style-resume --skill brand-style-resume -a codex -g -y
# 查看可发现的技能
npx skills add Cliccker/apple-style-resume --list
```

skill 已从 `apple-style-resume` 改名为 `brand-style-resume`。原 CLI 仍兼容；旧的 `$apple-style-resume` 调用应改为 `$brand-style-resume`。若曾手工安装，备份后替换旧文件夹，不同时保留两份技能。

手工安装可以将整个仓库克隆到目标项目的 `.agents/skills/brand-style-resume`。文件夹需直接包含 `SKILL.md`、`assets`、`scripts`、`references` 和 `DESIGN.md`。不要只复制 SKILL.md。安装不会自动配置 Python、字体或 PDF 依赖。

## 在 skill 中使用

```text
$brand-style-resume 请将 resume.pdf 编排为腾讯 TDesign 风格，输出到 output/resume，保留原文并导出 PDF。暂不使用照片。
```

```text
$brand-style-resume Use resume.md and portrait.png to create an English IBM Carbon-inspired resume in output/resume, including a PDF.
```

未指定风格时，skill 展示列表并询问。未提供照片时，会询问上传照片还是无照片继续；不自动生成头像。只在用户要求时翻译、上传或部署。

## 命令行生成

Python 3.10+；HTML 生成仅使用标准库。直接运行 CLI 不询问问题，默认 Apple、中文标签、无照片。

```bash
python scripts/md_to_resume.py --list-styles
python scripts/md_to_resume.py resume.md output/resume --style ant-design
python scripts/md_to_resume.py resume.md output/resume --style ibm-carbon --lang en --photo portrait.png
# 原有三个位置参数保持兼容
python scripts/md_to_resume.py resume.md portrait.png output/resume
```

输出：`index.html`、`resume_a4.html`、`source.md`；提供照片时另复制为 `photo.jpg`、`photo.jpeg` 或 `photo.png`。CSS 内嵌，交付文件不依赖 skill 的安装目录。`--lang` 只改变界面标签，不翻译正文。

```bash
python -m pip install -r requirements-pdf.txt
python -m playwright install chromium
python scripts/export_pdf.py output/resume/resume_a4.html --output output/resume/resume.pdf
```

Linux 缺少 Chromium 系统依赖时使用 Playwright 的 `install --with-deps chromium`。也可浏览器打印 A4 HTML：使用 CSS 边距、开启背景图形、关闭浏览器页眉页脚。长内容自然分页，不删文字、不强制一两页；Apple 保留后续雇主另页，其余风格连续排版。

## PDF 输入：提取、视觉核对、Markdown

```bash
python -m pip install -r requirements-input.txt
python scripts/prepare_pdf.py resume.pdf --output output/pdf-input
```

该脚本生成逐页 `.txt`、`.png` 和 `manifest.json`，不会执行 OCR 或猜测简历结构。skill 会对照每页预览整理成可编辑 Markdown，再交给生成器。双栏需要恢复语义顺序；扫描页和混合页需要当前 agent 的视觉/OCR 能力。页面能提取文字，也必须核对图片中的额外内容。

无法确认的姓名、日期、数字等信息会向用户追问。缺少视觉/OCR 能力时会明确说明并请求可读源文件。纯 CLI 不能独立完成扫描件识别。详见 [PDF 工作流](references/pdf-input.md)；[四类虚构输入样本](examples/pdf-input)附正确 Markdown，可用于练习和测试。

## Markdown、字体和样本

输入格式见 [解析说明](references/markdown-parsing.md)。支持简介、经历、教育、技能、独立项目、证书、奖项、出版物及自定义章节；重复章节保留顺序。任意 HTML、复杂表格和嵌套 Markdown 应由 skill 在工作副本中转为可读结构，不执行源 HTML。

字体默认本地加载，缺少时按每套规范回退，可能改变换行和分页。Apple 保留 [Inter](https://rsms.me/inter/) / [Noto Sans SC](https://fonts.google.com/specimen/Noto+Sans+SC) 字体栈；Carbon 使用 IBM Plex Sans，Material 使用 Roboto，其他详见各自 DESIGN.md。可选 `--web-fonts` 加载该风格的开源在线字体；导出前应等待字体与照片就绪。不捆绑专有字体或公司标志。

新增 [12 份职业 Markdown](examples/profiles)，对应 6 位虚构人物的中英文版本。另有 [职业预览](examples/preview/careers)：应届生、前端、后端、产品、设计、数据；包含无经历、多雇主、长文本、长链接和未知章节。[6 个公开来源与样本溯源](references/sample-sources.md)仅作为结构参考，未复制真实履历和个人信息。实际用户输入及输出不会自动脱敏。

## 重建示例

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python scripts/build_pdf_fixtures.py
python scripts/build_previews.py
```
