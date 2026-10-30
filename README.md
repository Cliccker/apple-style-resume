# Brand Style Resume

将 Markdown 或 PDF 简历转换为响应式网页与 A4 PDF，提供 12 套基于公开设计语言的公司风格方案。

**简体中文** · [English](README.en.md)

---

项目将简历的「内容」与「呈现」分离：正文只需维护一份源文件，更换风格无需改动内容。生成的网页与 PDF 均内嵌 CSS，可脱离本项目独立分发与归档。

所有风格均为基于公开设计语言的独立改编，不是任何公司的官方模板，也不构成录用承诺。

## 功能特性

- 12 套设计风格，覆盖国内外主流设计体系，同一份内容可横向比较效果
- 同时输出响应式网页与 A4 打印版，正文内容完全一致
- 支持中文 / 英文界面标签，正文语言保持不变
- 支持简介、工作经历、教育背景、技能、独立项目、证书、奖项、出版物及自定义章节
- 照片可选；未提供时使用纯文字页眉，不生成占位头像
- 输入支持 Markdown、文本型 PDF 与扫描件（扫描件需 agent 视觉能力）
- HTML 生成仅依赖 Python 标准库，无需构建工具

## 效果预览

12 套风格使用同一份虚构简历，便于横向比较。人物、组织、学校、时间与成果均为虚构，头像为原创几何占位图。

![前六套风格的中英文桌面预览](docs/images/gallery/desktop-1.png)
![后六套风格的中英文桌面预览](docs/images/gallery/desktop-2.png)

完整效果可在[本地画廊](examples/preview/index.html)中浏览。GitHub 仅显示 HTML 源码，需下载仓库后用浏览器打开。各风格的桌面端、移动端与逐页 PDF 截图保存在对应的预览目录中。

## 安装

需要 Node.js 22.20+ 与 npm。通过 [Vercel Skills CLI](https://github.com/vercel-labs/skills) 安装，仓库地址保持不变：

```bash
npx skills add Cliccker/apple-style-resume --skill brand-style-resume -a codex -y
```

安装到用户目录（对所有项目生效）追加 `-g`，查看可发现的技能使用 `--list`：

```bash
npx skills add Cliccker/apple-style-resume --skill brand-style-resume -a codex -g -y
npx skills add Cliccker/apple-style-resume --list
```

手工安装时，将整个仓库克隆至目标项目的 `.agents/skills/brand-style-resume`。该目录需直接包含 `SKILL.md`、`assets`、`scripts`、`references` 与 `DESIGN.md`，仅复制 `SKILL.md` 无法运行。安装过程不会配置 Python、字体或 PDF 依赖，相关步骤见下文。

<details>
<summary>从旧版 <code>apple-style-resume</code> 迁移</summary>

Skill 已更名为 `brand-style-resume`，仓库地址未变。原有 CLI 命令仍然兼容；历史调用中的 `$apple-style-resume` 应替换为 `$brand-style-resume`。

若此前为手工安装，请先备份，再整体替换旧目录，避免同时保留两份技能。

</details>

## 使用

### 通过 Skill

安装后以自然语言描述需求即可，无需记忆参数：

```text
$brand-style-resume 将 resume.pdf 编排为腾讯 TDesign 风格，输出到 output/resume，保留原文并导出 PDF，暂不使用照片。
```

```text
$brand-style-resume Use resume.md and portrait.png to create an English IBM Carbon-inspired resume in output/resume, including a PDF.
```

Skill 会处理以下环节：未指定风格时列出 12 套方案并确认；未提供照片时询问上传或跳过；生成后核对桌面端、移动端与每一页 PDF 的排版。它不会自动翻译正文，也不会在未要求的情况下上传或部署。

### 通过命令行

CLI 可独立使用。生成 HTML 仅需 Python 3.10+，不询问任何问题，默认 Apple 风格、中文标签、无照片。

```bash
python scripts/md_to_resume.py --list-styles
python scripts/md_to_resume.py resume.md output/resume --style ant-design
python scripts/md_to_resume.py resume.md output/resume --style ibm-carbon --lang en --photo portrait.png
```

原有的三位置参数写法保持兼容：

```bash
python scripts/md_to_resume.py resume.md portrait.png output/resume
```

输出文件为 `index.html`（响应式网页）、`resume_a4.html`（A4 打印版）与 `source.md`（排版使用的源文件）。提供照片时会额外复制为 `photo.jpg`、`photo.jpeg` 或 `photo.png`。

导出 PDF：

```bash
python -m pip install -r requirements-pdf.txt
python -m playwright install chromium
python scripts/export_pdf.py output/resume/resume_a4.html --output output/resume/resume.pdf
```

Linux 上缺少 Chromium 系统依赖时，使用 Playwright 的 `install --with-deps chromium`。也可直接用浏览器打印 `resume_a4.html`：选择 A4、保留 CSS 边距、开启背景图形、关闭页眉页脚。

## 设计风格

国内公司的设计体系：

| 风格 | CLI 参数 | 中文 | English |
| --- | --- | --- | --- |
| [蚂蚁 Ant Design](references/styles/ant-design/DESIGN.md) | `ant-design` | [网页](examples/preview/styles/ant-design/zh-CN/index.html) · [PDF](examples/preview/styles/ant-design/zh-CN/resume.pdf) | [web](examples/preview/styles/ant-design/en/index.html) · [PDF](examples/preview/styles/ant-design/en/resume.pdf) |
| [腾讯 TDesign](references/styles/tencent-tdesign/DESIGN.md) | `tencent-tdesign` | [网页](examples/preview/styles/tencent-tdesign/zh-CN/index.html) · [PDF](examples/preview/styles/tencent-tdesign/zh-CN/resume.pdf) | [web](examples/preview/styles/tencent-tdesign/en/index.html) · [PDF](examples/preview/styles/tencent-tdesign/en/resume.pdf) |
| [字节 Arco](references/styles/bytedance-arco/DESIGN.md) | `bytedance-arco` | [网页](examples/preview/styles/bytedance-arco/zh-CN/index.html) · [PDF](examples/preview/styles/bytedance-arco/zh-CN/resume.pdf) | [web](examples/preview/styles/bytedance-arco/en/index.html) · [PDF](examples/preview/styles/bytedance-arco/en/resume.pdf) |
| [抖音 Semi](references/styles/douyin-semi/DESIGN.md) | `douyin-semi` | [网页](examples/preview/styles/douyin-semi/zh-CN/index.html) · [PDF](examples/preview/styles/douyin-semi/zh-CN/resume.pdf) | [web](examples/preview/styles/douyin-semi/en/index.html) · [PDF](examples/preview/styles/douyin-semi/en/resume.pdf) |
| [华为 HarmonyOS](references/styles/huawei-harmonyos/DESIGN.md) | `huawei-harmonyos` | [网页](examples/preview/styles/huawei-harmonyos/zh-CN/index.html) · [PDF](examples/preview/styles/huawei-harmonyos/zh-CN/resume.pdf) | [web](examples/preview/styles/huawei-harmonyos/en/index.html) · [PDF](examples/preview/styles/huawei-harmonyos/en/resume.pdf) |
| [百度 Light DLS](references/styles/baidu-dls/DESIGN.md) | `baidu-dls` | [网页](examples/preview/styles/baidu-dls/zh-CN/index.html) · [PDF](examples/preview/styles/baidu-dls/zh-CN/resume.pdf) | [web](examples/preview/styles/baidu-dls/en/index.html) · [PDF](examples/preview/styles/baidu-dls/en/resume.pdf) |

国际公司的设计体系：

| 风格 | CLI 参数 | 中文 | English |
| --- | --- | --- | --- |
| [Apple](references/styles/apple/DESIGN.md) | `apple` | [网页](examples/preview/styles/apple/zh-CN/index.html) · [PDF](examples/preview/styles/apple/zh-CN/resume.pdf) | [web](examples/preview/styles/apple/en/index.html) · [PDF](examples/preview/styles/apple/en/resume.pdf) |
| [Google / Material 3](references/styles/google-material/DESIGN.md) | `google-material` | [网页](examples/preview/styles/google-material/zh-CN/index.html) · [PDF](examples/preview/styles/google-material/zh-CN/resume.pdf) | [web](examples/preview/styles/google-material/en/index.html) · [PDF](examples/preview/styles/google-material/en/resume.pdf) |
| [Microsoft / Fluent 2](references/styles/microsoft-fluent/DESIGN.md) | `microsoft-fluent` | [网页](examples/preview/styles/microsoft-fluent/zh-CN/index.html) · [PDF](examples/preview/styles/microsoft-fluent/zh-CN/resume.pdf) | [web](examples/preview/styles/microsoft-fluent/en/index.html) · [PDF](examples/preview/styles/microsoft-fluent/en/resume.pdf) |
| [IBM / Carbon](references/styles/ibm-carbon/DESIGN.md) | `ibm-carbon` | [网页](examples/preview/styles/ibm-carbon/zh-CN/index.html) · [PDF](examples/preview/styles/ibm-carbon/zh-CN/resume.pdf) | [web](examples/preview/styles/ibm-carbon/en/index.html) · [PDF](examples/preview/styles/ibm-carbon/en/resume.pdf) |
| [Adobe / Spectrum](references/styles/adobe-spectrum/DESIGN.md) | `adobe-spectrum` | [网页](examples/preview/styles/adobe-spectrum/zh-CN/index.html) · [PDF](examples/preview/styles/adobe-spectrum/zh-CN/resume.pdf) | [web](examples/preview/styles/adobe-spectrum/en/index.html) · [PDF](examples/preview/styles/adobe-spectrum/en/resume.pdf) |
| [Salesforce / Lightning](references/styles/salesforce-lightning/DESIGN.md) | `salesforce-lightning` | [网页](examples/preview/styles/salesforce-lightning/zh-CN/index.html) · [PDF](examples/preview/styles/salesforce-lightning/zh-CN/resume.pdf) | [web](examples/preview/styles/salesforce-lightning/en/index.html) · [PDF](examples/preview/styles/salesforce-lightning/en/resume.pdf) |

`CLI 参数` 即 `--style` 的取值。各风格共用内容渲染逻辑，但版式分别设计：标签网格、页眉处理、项目容器与层级关系均按各自规范实现。全部为浅色主题，不含公司 logo，无深色模式变体。

## 常见问题

**会翻译简历正文吗？**
不会。`--lang` 仅切换界面标签（如「工作经历 / Work Experience」），正文语言始终与源文件一致。需要翻译请单独说明。

**必须提供照片吗？**
不必须。无照片时使用纯文字页眉，不会生成占位头像。

**可以只用命令行吗？**
可以。`scripts/md_to_resume.py` 是独立 CLI，不依赖 agent。Skill 主要承担风格选择、PDF 核对与排版检查等需要视觉判断的环节。

**能否压缩到指定页数？**
不会为满足页数删减内容。所有风格让经历自然排版，页面填满后分页；字号与边距按打印可读性设定，长简历不会被强行缩小。

**是否依赖网络？**
默认不依赖，字体从本地加载。添加 `--web-fonts` 会加载该风格的开源在线字体，导出前需等待字体与照片就绪。

**扫描版 PDF 如何处理？**
需要 agent 的视觉能力。`prepare_pdf.py` 只负责拆页、截图与生成清单，不做 OCR，也不推断文档结构。

**字体缺失会影响排版吗？**
会。缺失时按各风格规范的顺序回退到系统字体，换行与分页可能随之变化。

## 输入格式

输入需要一个 H1 作为姓名、一行职位、可选意向岗位、联系方式，以及若干 H2 章节。支持简介、工作经历、教育背景、技能、独立项目、证书、奖项与出版物；无法识别的章节按原文保留，不会因不符合模板而丢弃。

```markdown
# 示例候选人

产品工程师
意向岗位：产品体验工程师

hello@example.com
[作品集](https://example.com/portfolio)

## 个人简介

一段事实性的自我介绍。

## 工作经历

### 示例公司 | 产品工程师
*2023.04 - 2025.08*

**项目名称** *(Web / 设计系统)*
- 一条可核实的成果。
```

重复章节保持原有顺序，空章节自动隐藏。嵌套列表会拍平；复杂表格与 HTML 按纯文本转义显示，不会执行。完整规则见[解析说明](references/markdown-parsing.md)。

## PDF 输入

```bash
python -m pip install -r requirements-input.txt
python scripts/prepare_pdf.py resume.pdf --output output/pdf-input
```

脚本将 PDF 拆分为逐页 `.txt`、`.png` 与 `manifest.json`。后续步骤需要视觉核对：对照每页预览将内容整理为可编辑 Markdown，再交由生成器处理。双栏排版需还原阅读顺序；扫描页与图文混排页需重点检查，因为文字层可提取并不代表图中内容完整。

无法确认的姓名、日期、数字等信息会向用户追问，不做猜测填充。当前环境缺少视觉/OCR 能力时，会说明受影响的页面并请求可读源文件；纯 CLI 无法独立完成扫描件识别。

详见 [PDF 工作流](references/pdf-input.md)。[四份虚构输入样本](examples/pdf-input)附有正确的 Markdown，可用于练习与测试。

## 字体与设计规范

字体默认本地加载。Apple 保留 Inter 与 Noto Sans SC 字体栈，Carbon 使用 IBM Plex Sans，Material 使用 Roboto，其余见各自 `DESIGN.md`。本项目不捆绑专有字体或公司标志。

公共设计规则（网页宽度、A4 边距、最小字号、分页策略等）集中在 [DESIGN.md](DESIGN.md)，其中同时记录各风格的官方来源、采集日期、设计 token 与改编说明。调研中发现的第三方 DESIGN.md 也在该文档中说明，未复制其内容。

## 示例与重建

- [examples/profiles](examples/profiles)：12 份职业 Markdown，对应 6 位虚构人物的中英文版本
- [examples/preview/careers](examples/preview/careers)：应届生、前端、后端、产品、设计、数据六类岗位预览，覆盖无经历、多雇主、长文本、长链接与自定义章节
- [references/sample-sources.md](references/sample-sources.md)：6 个公开来源，仅作结构参考，未复制真实履历与个人信息

修改样式后可重新生成全部预览：

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python scripts/build_pdf_fixtures.py
python scripts/build_previews.py
```

真实用户的输入与输出不会自动脱敏。公开示例须另行编写虚构内容，对真实简历做打码处理并不充分。

## 项目结构

```text
assets/       样式 CSS 与风格索引
scripts/      生成、PDF 导出与预览构建脚本
references/   各风格 DESIGN.md、输入格式与来源说明
examples/     虚构简历、职业样本与生成的预览产物
docs/         README 引用的预览图
tests/        测试
```

## 许可证

[MIT](LICENSE)。

各风格为公开设计语言的独立改编，与 Apple、Google、Microsoft、IBM、蚂蚁集团、腾讯、字节跳动、抖音、华为、百度、Adobe、Salesforce 均无隶属或背书关系。

## 社区

欢迎加入 [LINUX DO](https://linux.do/)，一个「新的理想型社区」。
