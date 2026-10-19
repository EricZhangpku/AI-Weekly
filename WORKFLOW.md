# 每周更新规程

## 触发与范围

沿用 Codex 当前对话的 heartbeat `ai-ai-ai`，每周一 10:00（Asia/Shanghai）开始收集前一周一至周日的信息，完成后通知阅读。任务执行依赖本地 Codex 可运行、电脑处于唤醒状态且网络可用；10:00 是开始时间，不是保证完成时间。

## 内容要求

- 美国：OpenAI、Anthropic、Google DeepMind、Meta、xAI、Nvidia 等；中国：DeepSeek、阿里/Qwen、月之暗面/Kimi、智谱、字节、腾讯等；欧洲：Mistral、相关头部实验室与科学 AI 项目。按新闻重要性选取，不为凑齐名单填充无关消息。
- 记录新的模型、架构、训练/推理算法与实际能力变化。比较基准时保留任务、测量口径、价格条件和厂商归因。
- 重要观点尽量找领导者本人原帖或演讲全文。转发、认同、记者概括与本人原话应区分；没有足够证据时不使用“划时代”“已实现 AGI”等结论。
- 默认用 Edge 浏览；X 可以直接读取现有登录态，失败时不反复尝试，不处理账号密码。
- 每条事实附直接链接和事件日期；网页检索结果只是线索，应打开来源阅读。独立测评和公司自述明确标注。
- `content/evidence/YYYY-MM-DD.md` 保存检索日期、来源链接、关键证据、必要的引用摘录、未决信息与修订原因。仅收录需要的证据，不保存登录信息。
- 成稿经过 humanizer-zh 润色。正文简洁，避免把检索流水账或内部自检清单放进读者页面。

## 文件与构建

首期范例：`content/issues/2026-10-18.md` 与 `.json`。JSON 字段：

| 字段 | 含义 |
| --- | --- |
| slug | 周日日期 YYYY-MM-DD，与两个文件名一致 |
| start / end / published | 周一、周日、实际发布日期 |
| title / subtitle / summary | 编辑标题、副标题、简短摘要 |
| tags | 2–4 个主题，用于首页筛选 |
| highlights | 三个地区速览，各含 region、label、title、text、anchor |
| source_page | 可选，原始 Page 链接 |

Markdown 支持 `#`、`##`、`###` 标题，普通段落、`-` 列表、粗体、行内代码、引用、表格、HTTP(S) 链接。标题依出现次序获得 `section-1`、`section-2` 等锚点；highlights 的 anchor 应指向对应地区标题。不要嵌入原始 HTML。保持厂商、技术、观点、来源四类内容清晰。

```sh
cd /Users/ericzhang/Documents/Codex/AI-Weekly
python3 scripts/build.py
python3 scripts/check.py
python3 scripts/manage.py start
```

检查新期 `http://127.0.0.1:8765/issues/YYYY-MM-DD.html` 和首页。校验失败时修正文案或元数据再构建，不发布半成品；重复运行同一期不会增加重复卡片。不要删除已有期刊。

## GitHub 同步

远程仓库：`https://github.com/EricZhangpku/AI-Weekly`，分支 `main`。用户已授权每周完成后提交并推送。

1. 开始前检查 `git status` 和 `origin`。工作区干净时执行 `git pull --ff-only origin main`，再编写新一期；如有用户未提交的修改，保留它们，不覆盖或混入本次提交。
2. 构建会自动更新 README 计时板块、`site/assets/weekly-stats.svg` 和网站总期数，无需手填数字。统计来自通过校验且有配套正文的 JSON 文件，创刊日期取最早发布日期。
3. 内容和构建完成后检查差异，仅暂存本任务产生的文章、证据、生成网页及 README 等相关变更。不要提交 `.runtime/`、登录信息或无关修改。
4. 用 `git commit` 提交，消息注明周报日期，然后执行 `git push origin main`。没有变更时无需重复提交；如有上次未推送的本任务提交，仍需推送。
5. 确认远程 `main` 的提交与本地 HEAD 一致。推送被拒绝时先获取远程更新，保留双方内容；无法安全合并、认证失败或网络失败时保留本地成果并说明原因，禁止强制推送。

## 通知

在当前对话用一句话概括本期焦点，附首页和新一期网址、静态 HTML 文件链接，提醒阅读。同时说明 GitHub 同步结果，并提醒其他电脑拉取仓库后阅读。网站只在本机运行，不把 localhost 当作公网网址。
