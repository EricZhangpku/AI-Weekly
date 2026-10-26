# 2026-10-25 周报补充检索证据

- 补充检索日期：2026-10-26（Asia/Shanghai）。观察区间：2026-10-19 至 2026-10-25。更新已存在的周报，不新增重复期号。
- 扫描用综述：AI Atlas《The Week in AI: Week of 19 to 25 October 2026》<https://atlas.prashish.com/weeks/2026-10-19>；Varun Singla 周度 AI digest <https://varunsingla.com/weekly/>，并回读 10 月 19–21 日条目 <https://varunsingla.com/entries/2026-10-19.html>、<https://varunsingla.com/entries/2026-10-20.html>、<https://varunsingla.com/entries/2026-10-21.html>。这些材料帮助发现本期遗漏模型；关键事实和分数回到官方或评测来源确认。
- 本轮补入此前漏掉的关键动态：Kimi K3.1 Pro、MiniMax M3.1 Flash、Mistral Voxtral 3、Claude Duet、NVIDIA Nemotron 3.5 Super VL/Bolt；并说明欧洲本土厂商与 NVIDIA 在柏林发布的区别。

## 长程强化学习系统

Qwen 团队 arXiv:2609.33848 v2 于 2026-10-20 修订：<https://arxiv.org/abs/2609.33848>。QwenGyre 为长程在线强化学习系统，在 Qwen 3.8 2.4T、700K token rollout 设置下，NL2RepoBench 52.5%→58.5%（48 steps）；相对 Colocate/Async 最高 1.85×/1.78× speedup。该论文首次提交于 9 月 27 日，故周报只把 10 月 20 日修订视为本期系统研究更新，不称新发布。

## 重点模型：Kimi K3.1 Pro

1. Moonshot/Kimi 官方技术博客，发布日期 2026-10-23：<https://www.kimi.ai/blog/kimi-k3-1-pro>。官方称 2.8T 总参数、104B 激活参数、1M token 上下文；模型由 K3 继续进行大规模后训练，优化 RL、长上下文推理、沙盒和 rollout 调度。API/产品当周开放；完整权重承诺于 11 月 4 日发布，因此 10 月 25 日时并未开放权重。
2. 官方 Terminal-Bench 4.0 报告分数 65.7%（Claude Code harness、max effort、temperature 1.0、top-p 0.95）；同页列 Claude Opus 5.5 66.4、GPT-6 Astra 58.2。官方脚注说明竞品结果来自其各自官方报告/榜单最高值，harness 和设置不完全统一，故只能视为参考而非严格同条件比赛。
3. 同一官方博客的 Kimi Code Bench 3.0 Long-horizon 为 61.2，K3 为 55.95；属 Kimi 内部评测。
4. BenchCAD 是多视角图像到 CAD 代码生成任务。官方 1,000 例子集、Voxel IoU：带工具 Kimi 92.7、Opus 96.2、GPT-6 Astra 95.9；不带工具 Kimi 72.8、Opus 73.0、DeepSeek V4.1 Flash 1017 为 41.2。测试使用工具时采用 Claude Code harness，不用工具时采用官方单轮提示和评分流程；工具条件不同的结果不混比。
5. Official OfficeQA Pro v2 得分 64.4，任务是在真实财务文档中做检索、跨文档校验和多步数值推理。Kimi 内部 Hallu Bench Hard 声称 claim-level hallucination rate 从 K3 的 23.4% 降至 K3.1 Pro 的 8.3%；公司明确注明这是刻意构造的事实性压力测试，不代表日常使用错误率。
6. Artificial Analysis 独立比较页：<https://artificialanalysis.ai/models/comparisons/kimi-k3-1-pro-vs-gpt-6-1-sol>。Intelligence Index v4.3.2 汇总 10 项任务，Kimi 55，GPT-6.1 Sol Max 52；Terminal-Bench 4.0 页面值 Kimi 67%、GPT-6.1 Sol Max 56%。AA 显示 Kimi Intelligence Index 每任务估算成本 $2.11。该页发布时仍标注 open-source weights 为 No；与 Kimi 11 月 4 日权重发布时间承诺相符。
7. 使用 Kimi 官方 BenchCAD 图表，已复制到 `site/assets/kimi-k3-1-benchcad-results.webp`（32 KB）。原图：<https://statics.kimi.ai/kimi-blogs/kimi-k3-1/20261023/benchcad-results-v2.webp>。图像仅展示厂商自己的 1,000 例子集结果，网站图注说明工具条件，正文同时给出来源和限制。

## 其他重要更新

1. MiniMax，2026-10-19，M3.1 Flash：<https://www.minimax.io/blog/minimax-m31f>。厂商指标：DeepSWE v1.1 73.7%、OSWorld V2 61.7、BankerToolBench 76.2、CyberGym 82%、Agents' Last Exam 29.6；价格输入/输出/缓存分别 $0.15/$0.60/$0.015 每百万 token；公司说中位生成速度超过 170 token/s、代理任务成本比前代低 70%，后两项不是独立测量。AI Atlas 周度快照记 Artificial Analysis Index 42（前代 M3 为 29）：<https://atlas.prashish.com/weeks/2026-10-19>；Artificial Analysis 当前模型页显示 43，评测任务成本约 $0.22：<https://artificialanalysis.ai/models/minimax-m3-1-flash>。正文记录两种读数，未推断其差异原因。该综述没有说明 93% hallucination rate 的定义，因此正文不使用这个难以解释和横比的指标。发布说明说权重稍后发布，故本期称 API 可用而未称权重开源。
2. Mistral，2026-10-20，Voxtral 3：<https://mistral.ai/news/voxtral-3/>。官方规格称转写覆盖 50+ 语言，合成支持 35+ 语言和 50+ 方言；SDK 组合听、推理、工具调用与说话，提供欧盟托管 API 或自行部署。能力和部署描述归因厂商。
3. Anthropic，2026-10-21，Claude Duet：<https://claude.com/resources/articles/claude-duet>。产品研究预览，可接入应用并在独立 VM 环境中工作；支付、发送、删除等操作前设有人类确认。由 Opus 5.5 提供模型能力，不是基础模型发布。
4. NVIDIA，2026-10-15，Nemotron 3.5 Super VL 与 Bolt：<https://blogs.nvidia.com/blog/nemotron-3-5-super-vl/>。官方称 Super VL 为 120B，总参数/激活参数口径可在对应模型报告确认；Bolt 74B-A9B 面向 24GB，Bolt E4B 面向 4GB 本地语音代理。5×性能为 NVIDIA 厂商说法。
5. AI Atlas 将 MiniMax 代理指标、Kimi 的独立与厂商评测并列整理：<https://atlas.prashish.com/weeks/2026-10-19>。正文用其作发现线索，并已核实所列官方来源和 AA 页面。

## 写作与图片取舍

- 重点是把综合指数、单任务分数、任务成本、上下文、权重开放状态和 harness 分开表述，避免把不同口径拼成“全面领先”。
- 使用一张 Kimi 官方基准图，是因为它直观展示同一基准中带/不带工具的分数变化；不采用其他无助于理解的装饰图片。
- 正文经 language-demand 与 humanizer-zh 润色；没有改变原始数据或来源归属。
