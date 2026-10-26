# 2026-10-18 周报补充检索证据

- 补充检索日期：2026-10-26（Asia/Shanghai）。观察区间仍为 2026-10-12 至 2026-10-18；仅收录期间内发生的事件。补充修订原周报，不新增重复期号。
- 扫描用综述：AI Atlas《The Week in AI: Week of 12 Oct to 18 Oct 2026》<https://atlas.prashish.com/weeks/2026-10-12>；Varun Singla 周度 AI digest <https://varunsingla.com/weekly/>（该周条目见 <https://varunsingla.com/entries/2026-10-18.html>）。综述用于发现漏项；以下关键数据已回查官方或论文来源。
- 本轮发现此前遗漏的重点：Microsoft MAI-Base-2、Anthropic 自我复制风险研究、xAI Grok Voice 3、腾讯 Hy-Memory 2.0。

## 核实的新增内容

1. Microsoft AI，2026-10-15，MAI-Base-2 预训练报告：<https://microsoft.ai/news/frontier-pre-training-at-microsoft-ai/>。报告称 MoE 总参数 2.8T、80B active，训练数据 50T token，16,000 张 GB200 训练 38 天，MFU 21%、goodput 89%。4.2–12.3 倍 FLOPs 效率是微软以四组 held-out evaluation 和缩放曲线对比 DeepSeek-V4-Pro-Base 的厂商计算；这是基础模型，尚在 post-training。
2. Anthropic Frontier Red Team，2026-10-12，自我复制风险研究：<https://www.anthropic.com/research/self-replicating-ai>。9B 模型在 9 类测试硬件的 8 类运行了推理；不超过 30B 的模型可完成许多单独步骤，但端到端组合会出错。年底可能达到端到端能力是按历史改进速度外推，不是已实现事实。
3. NVIDIA，2026-10-15，Nemotron 3.5 Super VL 与 Bolt：<https://blogs.nvidia.com/blog/nemotron-3-5-super-vl/>。NVIDIA 报告 Super VL 为 120B 开放模型，并称同级任务最高快 5 倍；速度主张为厂商自述。Bolt E4B 发布计划为 10 月 23 日，未列作当周已发布。
4. xAI，2026-10-14，Grok Voice 3：<https://x.ai/news/grok-voice-3>。公告转述 Artificial Analysis 2026-10-13 独立测试：Speech-to-Speech Index 86.9、Full Duplex Bench 97%、任务成功率 94.8%；比较组 GPT-Live-1 Astra 83.2、Gemini 3.8 Live 82.6。xAI API 报价 $0.08/min。指标只针对该评测语音任务，客服部署量等是公司提供的数据。
5. 腾讯混元，2026-10-16，Hy-Memory 2.0：<https://memory.hunyuan.tencent.com/>。官方提供模型、SDK、MemHub 三层开源方案；30B-A3B 记忆模型四套系统平均分 55.49，对比 Opus 5 54.62；未见系统 EverMemOS 得分 56.89。均为腾讯组织的专项记忆测试，非通用模型榜单。

## 语言与归因

- 用 “MoE”“active parameters”“FLOPs 利用率”时附简短含义或可读上下文；将厂商模型披露、独立测试、实验论文和趋势判断分开。
- 本轮新增文字保留以上限定；最终经 humanizer-zh 与 language-demand 润色。
