# AI Weekly

本地网站：`/Users/ericzhang/Documents/Codex/AI-Weekly`。只在本地运行，默认使用 Edge 浏览。

## 每周编辑流程

1. 阅读 `WORKFLOW.md`。按 Asia/Shanghai 时间确定前一完整周（周一至周日）。
2. 使用互联网检索。优先官方公告、论文、模型卡、作者与负责人原帖；中美欧厂商、模型/架构/算法、能力演进和重要观点都要覆盖。浏览器操作默认 Edge；X 登录失效时快速跳过并记录。
3. 保留来源证据与事件日期，区分厂商自述、独立测评和编辑判断。避免跨周归类或把观点写成既成事实。
4. 写作和润色前阅读并应用 `/Users/ericzhang/.codex/skills/language-demand/SKILL.md`，使正文、标题、摘要、网站文案和 README 自然直接、术语准确，减少空话、重复和防御式表达。成稿再按 `/Users/ericzhang/.codex/skills/humanizer-zh/SKILL.md` 润色，保留事实、归因、链接与必要限定。
5. 在 `content/issues/` 新增周日日期命名的 `.md` 与 `.json`，参照首期结构。先完成内容再构建；同周期已有文件则更新该期，避免重复。
6. 运行 `python3 scripts/build.py`、`python3 scripts/check.py`。它们更新首页、归档和每期独立页面；保留旧期，不直接编辑生成的 HTML。
7. 按 `WORKFLOW.md` 的 GitHub 同步流程提交并推送本期内容、生成页面和自动统计；保留用户修改，不强制推送。
8. 运行 `python3 scripts/manage.py start`。确认首页和新期页面可访问，提醒用户阅读并提供本地网址及文件链接。

## 页面设计

克制的科技感：深墨底、细网格、低饱和青绿。保留明暗切换、目录、阅读进度、搜索/筛选、Markdown 下载与打印。无需 npm、CDN 或网络字体，页面可离线打开。
