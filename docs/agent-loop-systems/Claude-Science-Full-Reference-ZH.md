五万字长文解读Claude Science的设计哲学
 

 A node in a desktop
Claude Science 是一个"以可复现科研资产为核心产出、用声明式抽象屏蔽异构算力、把数据血缘写进数据库、优先接权威数据源、并能自我扩展的科学计算 agent 平台。"

这不是一篇「Claude Science 有多厉害」的宣传稿，也不是使用手册。它是一次逆向工程式的设计评论：把一个成熟的、生产级的科研 AI agent 系统拆开，看它的每一个设计决策背后到底在解决什么问题、用什么证据支撑、放弃了什么替代方案。

首先，明确告诉大家一点，Claude Science 几乎重构了 Claude Code的设计哲学，转而以科学的角度去设计整套系统。一句话总纲：它不是"会科学的聊天机器人"，而是"一个把计算、溯源、证据绑死在一起的科研执行引擎"。

核心论点：一句话概括
如果只能用一句话说清 Claude Science 的设计哲学，那就是：

把 agent 当成一个需要被「校准」的科学仪器，而不是一个需要被「命令」的下属——
每一个约束都附带它的测量依据和适用边界，让模型理解「为什么」，从而在边界之外自行判断。

这句话里的三个词是全篇的骨架：

1. 校准（calibration） —— 配置项不是拍脑袋的偏好，而是针对实测瓶颈的调优。
2. 理解而非命令（understanding over instruction） —— prompt 反复强调「解释为什么」，明确把「ALWAYS / NEVER 全大写」列为黄旗。
3. 边界（boundary） —— 每条规则都写清它在哪里生效、哪里失效、遇到例外怎么办。reviewer 的 rubric 是这一点的极致体现。
一个贯穿全篇的观察
读完全部源文件后，最强烈的印象是：这个系统的作者把「LLM 是聪明的」当成第一性假设。skill-creator 里有一句话点破了这一切：

Today's LLMs are smart. They have good theory of mind and when given a good harness can go beyond rote instructions and really make things happen. … If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag — if possible, reframe and explain the reasoning so that the model understands why the thing you're asking for is important. That's a more humane, powerful, and effective approach.

整套系统的 prompt 风格、配置注释、rubric 设计，都是这一信念的推论：既然模型能理解「为什么」，那么最有效的控制方式不是堆砌禁令，而是传递意图和证据。这是 Claude Science 与大多数「用 MUST 和 NEVER 把模型捆死」的 agent 系统最根本的分野，也是这份分析真正想让你带走的东西。

这份文档是什么
这不是一篇「Claude Science 有多厉害」的宣传稿，也不是使用手册。它是一次逆向工程式的设计评论：把一个成熟的、生产级的科研 AI agent 系统拆开，看它的每一个设计决策背后到底在解决什么问题、用什么证据支撑、放弃了什么替代方案。

之所以值得这样读，是因为 Claude Science 的配置文件有一个罕见的性质——它把「为什么」写进了配置本身。绝大多数 agent 系统的 metadata 是一堆没有注释的开关（enable_thinking: false），你永远不知道那个 false 是深思熟虑还是随手一填。而 Claude Science 的 reviewer/metadata.yaml 里，enable_thinking: false 旁边跟着一整段实测数据：

# Measured (bench-reviewer, 6 reps): thinking accounts for ~72% of output tokens with ~0 recall delta on trace-the-value work (opus-nothink 0.94±0.02 vs baseline 0.895…)

这一行注释比整个配置文件本身更有价值。它告诉你：这个 false 不是意见，是在 6 次重复实验、量化了 token 成本和召回率之后得出的结论。整套系统都是这么建的。这份分析的核心任务，就是把散落在各文件里的这类「决策+证据」提炼成一套可迁移的设计原则。

核心论点 (文章太长浓缩版)
一、组件全景（实测清点）
层
内容
数量
Skills	
生物模型 / 计算编排 / 文献图表 / 自省
29
Agents	
operon（主）+ reviewer / bookmarker / onboarding（内部）
4
MCP servers	
ketcher-chemistry + bio-tools
2（bio-tools 内含 24 个 MCP server，聚合 ~63 个数据源客户端）
Skills 按功能分四类：

• 生物基础模型（12个）：alphafold2 / boltz / chai1 / openfold3（结构预测）、proteinmpnn / ligandmpnn / solublempnn（反向折叠）、esmfold2 / fair-esm2 / evo2（序列模型）、scgpt / scvi-tools（单细胞）、borzoi（基因组功能轨道）、diffdock（对接）
• 计算编排（5个）：compute-env-setup / remote-compute-ssh / remote-compute-modal / managed-model-endpoints / using-model-endpoint
• 科研产出（6个）：figure-composer / figure-style / paper-narrative / literature-review / pdf-explore / indication-dossier
• 元能力（4个）：self-awareness / customize / skill-creator / product-self-knowledge
二、七条核心设计哲学
1. "产出物是主角，不是聊天"（Artifact-first）
operon 的 working_style 反复强调：save_artifacts 是硬约束，输出图表/结构/报告必须落成 artifact 才对用户可见；结构文件（.pdb/.cif）自动进 Mol* 3D 查看器；语气要求写成"实验记录本/方法学章节"而非对话，明确禁止 emoji。它把自己定位成能产出可复现科研资产的实验台，而非问答机器人。

2. 声明式计算，一次定义处处运行（Declarative compute）
compute-env-setup 是整个系统最精巧的抽象：一份 ENVS 声明（base / pip_phases / weight_dirs / smoke tests）能渲染成 Dockerfile、Apptainer def、或裸 SSH 命令序列。核心洞见写在原文里——"每个 backend 变化的是怎么构建和寻址，不变的是 job 需要什么"。pip_phases 的有序性被专门设计来解决依赖版本冲突。把"什么"和"怎么"彻底解耦，是它能横跨个人 GPU/Slurm/Modal/云的关键。

3. 可复现性刻进数据库（Provenance by construction）
self-awareness 揭示了一个完整的元数据 SQLite：execution_log（每个 cell 的源码+stdout+文件哈希）、artifact_versions（版本号+checksum+environment_snapshot+lineage）、artifact_dependencies（产物 DAG）、host_call_log（每次 SDK 调用）。每张图、每个文件都能追溯到产生它的确切代码、环境和上游数据——科研级的血缘可追溯性是数据库的一等公民，不是事后日志。

4. 真实数据优于泛泛回答（Grounding over generation）
bio-tools 内置 ~63 个权威数据源客户端（UniProt/PDB/AlphaFold/Ensembl/ClinVar/gnomAD/ChEMBL/PubMed/Rfam/GWAS/GTEx/KEGG/Reactome/STRING…），聚合成 24 个领域化 MCP server。operon 被明确指示：文献综述/景观调研要"抓真实数据分析后交付 artifact，而非仅凭 web search 回答"。它假设科研问题的答案在权威数据库里，不在模型记忆里。

5. 每个 agent 按任务裁剪到极致（Purpose-shaped agents）
最能体现工程克制的是四个 agent 的差异化配置，且注释里带着实测数据：

• reviewer / bookmarker：enable_thinking:false——注释写明"tracing 是模式匹配非推理，thinking 占 72% token 但召回率零提升（bench 实测 6 reps）"
• bookmarker：excluded_tools 砍到只剩 submit_output
• onboarding：砍掉所有执行工具，只保留 ask_user（"就是它的全部机制"）
• operon：唯一开放全 skill 发现的通用 agent
这些配置背后是"测量驱动的删减"——每个开关都有 benchmark 佐证，而非默认全开。

6. 懒加载 + 主动发现（Progressive disclosure）
skill 不是全部塞进上下文，而是 harness 在 <skill_discovery> 块里按当前任务主动浮现相关 skill，模型按需 skill 工具加载。29 个 skill、~90 个数据源不污染上下文，用时才展开。规模化能力与上下文经济的平衡。

7. 系统能自我扩展（Self-extension）
skill-creator（18 文件，含 grader/analyzer/comparator 三个子 agent + eval-viewer）让系统能创建、改进、并量化评测新 skill；customize 让用户造自定义 agent profile（替换 identity_prompt、继承 working_style）；self-awareness 让 agent 查询自己的历史。这是一个被设计成可以生长的平台，不是固定功能集。

详细细节
① Artifact-first（产物优先，而非对话优先）
它做了什么
operon 的 working_style 明确要求：任何有价值的中间结果都要 save_artifacts，然后用 {{artifact:VERSION_ID}} 占位符引用，正文里写成 [filename]({{artifact:VERSION_ID}}) 这种可点链接。它的行文规范是"实验记录本（lab notebook）"体：不用 emoji、编号列表一个块、多阶段任务才 generate_plan。

为什么这么设计
普通聊天 Agent 的产出是"文本流"——图、表、模型权重都活在对话里，会话一结束就散了。科研要的恰恰相反：结果必须能被引用、被复现、被追责。所以它把"文件/产物"提升为一等公民，对话反而只是产物之间的连接线。

这解决的真实痛点
你昨天跑出的一张图，三个月后审稿人问"这图的数据哪来的"——artifact 有 VERSION_ID，能顺着往回查到源。对话式 Agent 给不了这个。

② Declarative compute（声明式计算环境）
它做了什么
compute-env-setup 技能里有个 ENVS 字典，把一套计算环境写成纯声明：base（基础镜像）、system_pkgs、pip_phases（有序的多阶段 pip 安装）、env、run_commands、shim_files、weight_dirs，还有自检字段 import_names / gpu_tests / cli_checks。四种 provider 形态统一在这套 spec 下：Direct SSH、Slurm 集群、Container bridge runner、byoc（Modal/RunPod 云）。

关键细节：pip_phases 是有序的
这不是随手设计。生信/深度学习的依赖地狱核心就是"装 A 会顶掉 B 需要的版本"。把安装拆成有序阶段，就能"先装骨架、再装冲突方、最后钉死版本"，用顺序绕开 solver 解不开的冲突。

为什么这么设计
科研计算最不可复现的一环就是环境。写成命令式脚本（pip install ... 一行行敲）没人能保证下次一样；写成声明 + 自检（import_names/gpu_tests/cli_checks），环境本身就变成可校验、可搬运的对象。同一份 spec 能落到 SSH 也能落到 Slurm 也能落到 Modal，就是因为它描述的是"要什么"而非"怎么装"。

③ Provenance by construction（溯源是构造出来的，不是事后补的）
它做了什么
self-awareness 技能开放了 host.query(sql)——一个只读的 SQLite 视图，覆盖整个会话数据库。表结构本身就是一部"科研审计账本"：

• artifact_versions —— 每个产物版本带 checksum、environment_snapshot、lineage
• artifact_dependencies —— 产物间的依赖 DAG（哪个图依赖哪份数据）
• execution_log —— 每次执行记 source（跑了什么代码）+ stdout + files_written 的 sha256
• 还有 host_call_log、frames、compaction_archives、notes、projects…
为什么这么设计
注意"by construction"这个词——溯源不是你想查的时候才去凑，而是每跑一步系统自动记一笔，且带哈希。这意味着：

• "这个结果是哪版代码 + 哪个环境跑出来的" → 查 execution_log + environment_snapshot
• "改了上游数据，下游哪些图要重跑" → 沿 artifact_dependencies 这张 DAG 走
• 它甚至能查询自己的历史（self-awareness 就是干这个的）
这是把"可复现性"从科研人的自律，变成了引擎的默认物理属性。

④ Grounding over generation（宁可去查/去算，不许编）
它做了什么
operon 的 working_style 里有两条硬规矩：

• "Compute, don't confabulate" —— 能算的必须算，不许猜数
• MCP 数据源调用只能在 repl 里以循环形式发：[host.mcp("server","method",id=x) for x in ids]，一个 cell 一个逻辑步，配 inline assert 当场校验
• 连"能力"本身也要 grounding：要用某个技能前先 search_skills 确认它真存在，而不是脑补一个技能名
bio-tools 就是这条哲学的物理基础
本机实测：bio-tools 一个 server 挂了 87 个数据源（24 个 mcp_* 聚合 server + 63 个数据源客户端）。看清单就懂它的野心——从文献（pubmed/europepmc/openalex/biorxiv）、基因（ensembl/mygene/gnomad/clinvar）、蛋白结构（pdb/alphafold/uniprot）、药物（chembl/pubchem/bindingdb/openfda）、通路（kegg/reactome/rhea）到临床试验（clinicaltrials）全覆盖。

而且我读了 mcp_rna/server.py 的源码，每个工具都显式标 annotations=READ_ONLY，源码注释写着 "operon house rule: in-repo bundled servers annotate every tool explicitly"（内建 server 必须逐个工具显式标注）。

为什么这么设计
LLM 最危险的失败模式是"编一个看起来对的数字/引用"。科研里这是致命的。所以它的对策是双管：一是给你 87 个真实数据源让你有得查，二是行为规范强制"能查就查、能算就算、还要当场 assert 验"。幻觉在科研里不是体验问题，是学术诚信问题，它用架构把这条路堵死。

⑤ Purpose-shaped agents（按用途裁剪的专用 Agent，附带 token 经济学）
它做了什么
不是一个万能 Agent，而是 4 个按职责裁剪的 profile，靠"减掉工具/关掉能力"来定形：

Agent
怎么被裁的
意图
operon	
主力，全能力
通用科学计算，artifact-first 行文
reviewer	enable_thinking:false
、skills_locked:true、关 web search、关 plan mode
纯评审，快而稳
bookmarker	excluded_tools
 砍掉 python/bash/r/repl/read_file/save_artifacts，只剩 submit_output
只做归类标记，不许碰执行
onboarding	internal:true
，砍掉所有执行工具只留 ask_user
纯引导对话
最硬的证据：reviewer 关 thinking 是 benchmark 决定的
reviewer/metadata.yaml 里注明——实测 thinking 吃掉约 72% 的 token，而对 recall 几乎零提升（~0 delta）。所以直接关掉。这不是拍脑袋，是量化跑分后的工程决策。

为什么这么设计
"一个超级 Agent 什么都干"听着强，实则又慢又贵又容易越界（一个只该打标签的 Agent 不该有权跑 bash）。用能力做减法来定义角色，既省 token 又收窄了权限面（bookmarker 连 read_file 都没有，根本没法泄露/篡改）。安全性和成本，是从工具集裁剪里长出来的，不是外挂的。

⑥ Progressive disclosure（渐进式暴露，别一次糊你一脸）
它做了什么
29 个技能，每个是一个 SKILL.md + YAML frontmatter（name/description/category/requirements/metadata）。关键在分层加载：

• 平时 Agent 只看得到每个技能的 description（一句话触发条件）
• 真要用了才 search_skills → 加载完整 SKILL.md 正文
• requirements:[gpu] 这种字段让系统按需判断资源
figure-style 技能是个典型：它明说"画任何图之前先 load 我、先 apply_figure_style()"——即"需要时才展开细节"。

为什么这么设计
29 个技能 + 87 个数据源，全部塞进上下文会瞬间撑爆、且淹没决策。渐进暴露 = 先给索引（description），用时才给正文。这既是 context 预算的省法，也是让 Agent 决策清爽的办法——它面对的永远是"一句话摘要的菜单"，而不是"几万行手册"。

⑦ Self-extension（能造工具、还能量化自评的自我进化闭环）
它做了什么
skill-creator 技能让 Claude Science 给自己造新技能，而且核心不是"能写"，是"能量化评估地迭代"。它的完整闭环（SKILL.md 原文）：

决定要做什么 → 写草稿 → 造几个测试 prompt → 让"带这个技能的 claude"跑 → 定性 + 定量双重评估 → 据反馈重写 → 重复 → 扩大测试集再来一遍

支撑这个闭环的实料：

• 3 个子 Agent：analyzer（分析）、comparator（对比）、grader（打分）
• 8 个脚本：run_eval.py（跑评测）、aggregate_benchmark.py（带方差分析的基准聚合）、run_loop.py（自动迭代循环）、improve_description.py（专门优化技能的触发描述）、package_skill.py、quick_validate.py、generate_report.py…
• eval-viewer：generate_review.py + viewer.html，把评测结果可视化给人看
• 技能读写走 host.skills.* SDK（list/read/edit/publish），publish 后再 host.agents.attach_skill(profile, name) 挂到某个 Agent 上
注意两个细节

1. improve_description.py 单独存在——因为技能好不好用，一半在"描述能不能被准确触发"，它把这件事量化成一个可优化目标。
2. aggregate_benchmark.py 带方差分析——它知道 LLM 评测有噪声，一次跑分不算数，要看方差。这是把科研方法论（重复、控噪、量化）用回到 Agent 自身的建设上。
为什么这么设计
这条是前 6 条的收口：一个科研引擎不可能预置好所有领域工具，所以它必须能自我扩展。但"能写新技能"很廉价，"能证明新技能确实更好"才是稀缺的——skill-creator 把后者做成了带子 Agent、带脚本、带方差分析的标准流程。它对待"造工具"这件事，用的是它对待科学本身的同一套标准：可测量、可复现、可迭代。

它们不是 7 个孤立卖点，而是一条自洽的链：

声明式环境（②） 保证计算可复现 → 每步执行 自动溯源（③） → 产物成为可引用的 一等公民（①） → 一切数据靠 87 源 grounding（④） 而非编造 → 用 裁剪过的专用 Agent（⑤） 省钱收权 → 靠 渐进暴露（⑥） 让海量能力可管理 → 最后用 量化自评的 skill-creator（⑦） 让整套系统自己长大。

一句话概括这套哲学：它把"科研方法论"（可复现、可溯源、拒绝编造、量化迭代）直接编译进了 Agent 的架构约束里——不是靠提示词劝 Agent 严谨，而是靠工具集、数据库表结构、行为硬规矩让它没法不严谨。

恭喜你已经看到了这里，下面会分为7个设计支柱详细分析
章
主题
最能代表它的源文件
一句话
01
配置即调优记录
agents/reviewer/metadata.yaml	
每个参数旁写「为什么是这个值、什么数据支撑」
02
身份 / 工作风格分离
agents/operon/metadata.yaml	
用户 profile 替换身份、继承工作风格
03
追溯而非重算的评审 rubric
agents/reviewer/metadata.yaml
 system_prompt
幻觉检测的「按证据位置加权 + 未溯源不算证据」
04
产出物而非答案
agents/operon
 working_style
强制 artifact + {{artifact:ID}} 引用
05
Skill 解剖学与 kernel sidecar
skills/figure-style/kernel.py
 skills/skill-creator
三级渐进式加载 + 代码固化为可复用 kernel
06
首次引导对话设计
agents/onboarding/metadata.yaml	
「理解而非选活」的访谈 + 即时赋能式授权
07
MCP 聚合架构
mcp-servers/bio-tools/	
按领域分组的 24 server / ~87 数据源
第一章 配置即调优记录
代表文件：agents/reviewer/metadata.yaml、agents/bookmarker/metadata.yaml
核心命题：配置项不是偏好开关，而是「针对实测瓶颈的调优结论 + 它的证据 + 它的适用边界」的三元组。

1.1 问题：无注释配置是技术债的温床
先看一个反面典型——绝大多数 agent 系统的 metadata 长这样：

enable_thinking: false
skills_locked: true
max_tool_result_chars: 262144
excluded_tools: [python, bash, r]
半年后，团队里没人敢动这四行。为什么 thinking 关了？262144 这个数是怎么来的、能不能改成 131072？python 为什么被排除、加回来会怎样？这些问题的答案只存在于当初那个工程师的脑子里，而他可能已经离职了。无注释的配置是一种「知识黑洞」——它记录了决策的结果，却丢失了决策的全部推理过程。 任何后续修改都变成了盲目试错。

Claude Science 的 reviewer/metadata.yaml 用一种近乎偏执的方式解决了这个问题：每一个配置项旁边都写清三件事——为什么这么设、用什么实验数据支撑、改动它会触发什么。

1.2 范例逐条拆解：reviewer 的四个配置项
（1）enable_thinking: false —— 附带一份微型实验报告
源文件原文：

# Tracing is pattern-match, not deliberation. Measured (bench-reviewer, 6
# reps): thinking accounts for ~72% of output tokens with ~0 recall delta on
# trace-the-value work (opus-nothink 0.94±0.02 vs baseline 0.895; both 6/6
# on in-place-contradiction hard cases). thinking_budget_tokens was
# vestigial (forwarded only to Delegator, never used for REVIEWER's own
# calls) — replaced by enable_thinking:false, threaded through core.ts →
# state.thinking_enabled → buildThinkingConfig().
enable_thinking: false
这段注释信息密度极高，拆开看它给了未来的维护者什么：

1. 一个概念性判断：「Tracing is pattern-match, not deliberation」——追溯数值是模式匹配，不是深思。这是关掉 thinking 的理论依据。
2. 一份可复现的实验：bench-reviewer, 6 reps——不是「我觉得」，是跑了 6 次的基准。
3. 两个量化指标：thinking 占 72% 输出 token（成本侧），召回率几乎无变化（0.94±0.02 vs 0.895，效果侧）。这是一个典型的成本-效益权衡，而且两侧都有数字。
4. 一个反直觉的加固证据：「both 6/6 on in-place-contradiction hard cases」——连最难的「就地矛盾」case，关掉 thinking 也全对。这堵死了「但难 case 需要 thinking 吧？」的质疑。
5. 一段代码考古：thinking_budget_tokens was vestigial——顺手记录了被替换掉的旧机制，以及新机制的调用链（core.ts → state.thinking_enabled → buildThinkingConfig()）。
可迁移的原则：当你为一个 agent 关掉某个能力，注释里至少要能回答——「你怎么知道关掉它不会掉效果？」如果答不上来，说明这个决策还没做完。

（2）skills_locked: true —— 记录被浪费的迭代预算
# Reviewers have a fixed job (trace → submit_output) — no skill discovery.
# agentConfigurator._getBrainTools drops search_skills when this is set;
# before it was set REVIEWER was burning 2 of 8 step-tier iterations on
# catalog search before the actual investigation began.
skills_locked: true
关键短语是 「burning 2 of 8 step-tier iterations」。它把一个抽象的「技能发现开销」翻译成了一个具体的、可感知的损失：8 步预算里有 2 步（25%）被浪费在检索技能目录上，而 reviewer 的职责是固定的、根本不需要发现技能。

注意这里的因果链是先观察到浪费、再上锁——「before it was set REVIEWER was burning…」。这不是预防性的设计，是对实测行为的修正。这揭示了一个工作方式：配置项常常是「先放开、观察真实行为、发现浪费、再收紧」的产物，而不是一开始就设计好的。

（3）max_tool_result_chars: 262144 —— 一个 p90 瓶颈的解剖
这是全文件最精彩的一条注释，因为它把一个魔数（262144 = 256KB）追溯到了一个具体的生产事故：

# `repl` tool output (printed host.frames() JSON on the SDK-pull path)
# stays inline up to 256KB instead of spilling to disk at 16K with a 2KB
# preview + "read_file(path)" hint. read_file is hard-capped at 25KB, so the
# spill → 15+ read_file pages chain was the p90 iter-count driver on long
# transcripts (measured: 357 re-reads of one 402KB dump in the samap
# session). …Hook chain: registry.ts → core.ts:1442 → toolRouter.ts
# `_maxToolResultChars`.
max_tool_result_chars: 262144
这条注释回答了「为什么是 256KB 而不是默认的 16KB」，逻辑链条完整到可以画成流程图：

1. 默认行为：工具输出超过 16KB 就 spill 到磁盘，只留 2KB 预览 + 一句「用 read_file 读」。
2. 但 read_file 每次硬上限 25KB。
3. 于是一个 402KB 的 dump 需要 402/25 ≈ 16 次分页读取——「15+ read_file pages chain」。
4. 这个链条是p90 迭代次数的最大驱动（p90 iter-count driver）——即最慢的那 10% 会话里，迭代次数主要就耗在这上面。
5. 实测最坏 case：samap 会话里，一个 402KB dump 被重读了 357 次。
6. 解法：把 inline 上限提到 256KB，让绝大多数 transcript 一次装下，彻底消灭这条分页链。
357 这个数字是这条注释的灵魂。 它不是「大文件读起来慢」这种泛泛之谈，而是「我们测到了一次会话里 357 次重读」的铁证。魔数配置最怕的就是「后人不敢改」，而这条注释让 262144 变得完全可理解、可挑战——如果未来 read_file 上限提到 100KB，这个 256KB 就该重新算。

可迁移的原则：任何一个「魔数」配置（超时、缓冲区大小、批次大小、上限），注释里应该写清它对应的瓶颈测量。魔数 + 测量 = 可维护；魔数 + 沉默 = 技术债。

（4）excluded_tools 用排除法 + 逐项归因
reviewer 的工具裁剪是「允许清单的补集」——它明说自己只需要 {repl, read_file, submit_output}，然后把其余全部列进 excluded_tools，并给最关键的排除项配了证据：

# `python` is excluded — the rubric says "trace, don't recompute", and
# measured prod REVIEWER rounds (n=30, same seed transcripts) show python
# was 41% of tool calls, all of it rubric-forbidden recomputation. Dropping
# it is the largest single iter-count lever.
三个要点：

1. 排除 python 与 rubric 直接呼应：system_prompt 里写「trace, don't recompute」（追溯而非重算），而工具层用 excluded_tools: [python] 把这条规则物理强制了。prompt 说的和配置做的是同一件事的两面——规则不仅写在提示里，还焊死在能力边界上。（这一点第三章会展开。）
2. 41% 是实测：n=30, same seed transcripts 下，python 调用占 41%，且「all of it rubric-forbidden recomputation」——全都是规则明令禁止的重算。
3. 「largest single iter-count lever」：这是全系统反复出现的一个评价维度——每个改动都用「它对迭代次数的杠杆有多大」来衡量。砍掉 python 是单个最大杠杆。
同一段注释还顺带展示了一种在配置里做安全考量的细腻：

# Ant-only tools that don't exist in external builds (e.g. the
# image-generation tool) are excluded in code behind the ant-only gate in
# agentConfigurator.refreshTools — naming them here would bake their name
# into the bundled metadata string constant and trip the release sentinel
# scan in external builds.
即：内部专用工具不能写进这个 YAML，否则工具名会被打包进外部发行版的字符串常量，触发发布哨兵扫描。这说明 metadata 文件本身是会被打包分发的，作者对「哪些字符串会泄漏到外部构建」有清晰的边界意识。

1.3 bookmarker：把 prompt 也纳入「测量-调优」体系
如果说 reviewer 展示了「配置项有实验支撑」，那么 bookmarker/metadata.yaml 更进一步——连 system_prompt 本身都是被基准测出来的，而且明确禁止手改：

# The system prompt was hill-climbed against an eval of 62 real checkpoint
# windows (gold-labeled; scored on verbatim-anchorability, zero-window
# discipline, must-window hit rate, and precision): composite 0.537 (first
# draft) → 0.796 dev / 0.354 → 0.523 holdout. Don't hand-tweak wording
# without re-running the eval — several plausible-looking edits measurably
# regressed it…
这段话包含了一个完整的 prompt 工程方法论：

1. prompt 有一个量化的 eval：62 个真实 checkpoint 窗口，人工金标注（gold-labeled）。
2. 有多维度评分：可逐字锚定性、零窗口纪律、必命中窗口的命中率、精确率——四个维度，因为一个「好书签」是多目标的。
3. 有 dev / holdout 分离：0.796 dev / 0.523 holdout——防止 prompt 过拟合到开发集，这是把 ML 的训练/测试分离直接用在了 prompt 上。
4. 有一条铁律：「Don't hand-tweak wording without re-running the eval」——因为「several plausible-looking edits measurably regressed it」（好几个看起来无害的改动实测让分数掉了）。
第 4 点是精髓：它承认「人类对 prompt 改动效果的直觉是不可靠的」。看起来更清楚的措辞可能实测更差。所以 prompt 不能凭手感改，必须过 eval。这与 skill-creator 里那套「draft → eval → 重写」的迭代闭环（见第五章）是同一种世界观在不同层面的体现。

注释甚至给了「什么改动可以不跑 eval」的例外：

# Exception: removing references to features that no longer exist (e.g. the
# retired spatial canvas) is inert — the eval can't exercise a tool that's
# never offered. Disclose such edits in the PR instead of re-running
# (precedent: PR #2236).
删除「已不存在的功能」的引用是惰性的（inert），因为 eval 根本触发不了一个不再提供的工具——这种改动在 PR 里说明即可，不必重跑。连「例外」都是有论证、有先例（PR #2236）的。

1.4 这个模式为什么强大：三个层面
第一，它让配置可挑战（falsifiable）。 一条带证据的配置是可以被反驳的——如果你重跑 bench-reviewer 得到 thinking 有明显召回增益，你就有资格改 enable_thinking。无证据的配置只能靠权威或资历来捍卫，无法靠数据推翻。可挑战性 = 可演进性。

第二，它把「隐性知识」变成「显性资产」。 那个测出 357 次重读的工程师的洞察，通过注释固化进了代码库，不再依赖他本人在场。这是团队知识管理的理想形态——知识活在它所解释的那行代码旁边，而不是活在某个过期的 wiki 或某人的记忆里。

第三，它统一了评价语言。 通篇反复出现的 iter-count lever（迭代次数杠杆）、p90 driver（p90 驱动因素）、recall delta（召回增量）、% of output tokens（输出 token 占比）——这是一套共享的、量化的评价词汇。当整个团队都用「这个改动对 iter-count 的杠杆多大」来讨论时，争论就从「我喜欢/我觉得」变成了「测了吗、多少」。

1.5 直接可搬走的做法
给你自己的任何 agent / prompt / 配置系统，套用这个模式的最小动作：

1. 每个非默认配置项写一行「为什么」。哪怕只是「默认值在 X 场景下太小，实测 Y」。
2. 每个魔数附一个测量。超时、批大小、缓冲区上限——写清它对应哪个瓶颈的哪个数字。
3. prompt 关键版本留一个 eval 快照。哪怕只有 10 条金标注 case，改 prompt 前后各跑一次，防止「看起来更好实则更差」。
4. 用统一的量化词汇讨论改动。给你的场景定义一两个核心指标（迭代次数？token？p90 延迟？），让所有优化都对着它说话。
5. 注释里写清「改动会触发什么」。像 reviewer 那样记下调用链和副作用（「naming them here would trip the release sentinel scan」），让后人改得动、也不敢乱改。
一句话收尾：reviewer 的 metadata 不是一份配置，是一份实验日志。 它把「我们试过什么、测到什么、为什么最后这么定」全部留在了现场。这是这套系统最值得偷师的一件事——比任何单个 prompt 技巧都更根本。

下一章看另一种巧思：身份与工作风格的分离。

第二章 身份与工作风格的分离
代表文件：agents/operon/metadata.yaml
核心命题：把 agent 的「我是谁、我能做什么」（identity）与「我该怎么做事」（working style）
拆成两段独立的 prompt，因为它们的继承规则不同——用户自建 profile 替换前者、继承后者。

2.1 一行注释里的架构决策
operon 的 metadata 顶部有一段看似平淡、实则定义了整个 agent 定制体系的注释：

# system_prompt is assembled at load time as identity_prompt + working_style_prompt.
# User-created profiles REPLACE identity_prompt with their own (user_agents.system_prompt)
# and INHERIT working_style_prompt — so keep capability/scope claims in identity_prompt
# and keep working_style_prompt profile-neutral.
identity_prompt: |
  You are Claude Science, a general-purpose scientific computing agent.
  …
working_style_prompt: |
  ## Working style
  …
把这段话翻译成设计规则：

• 最终的 system_prompt = identity_prompt + working_style_prompt，加载时拼接。
• 当用户创建自己的 agent profile 时：
• identity_prompt 被替换（用 user_agents.system_prompt）——用户可以完全重写「你是谁」。
• working_style_prompt 被继承——用户拿不走、也不需要重写「怎么做事」的通用规范。
由此推出两条写作纪律：

• 能力/范围声明放 identity_prompt（因为它会被替换，属于「这个特定 agent 的身份」）。
• 通用工作规范放 working_style_prompt，且必须 profile-neutral（因为它会被所有派生 profile 继承，不能带任何 operon 专属的假设）。
2.2 为什么这个切分是对的
考虑一个具体场景：用户想创建一个「抗体工程专用 agent」。他会想改什么？

• 想改的：「你是一个抗体工程专家，精通 SAbDab、免疫组库分析、CDR 移植……」——这是身份。
• 不想改、甚至不知道存在的：「产出物要 save_artifacts、引用要用 {{artifact:ID}}、别用 emoji、每个 python cell 是一次完整 LLM round-trip 所以要把逻辑塞进一个 cell……」——这是工作风格。
如果身份和工作风格揉在一个 prompt 里，用户重写身份时会连带丢失所有平台级的工作规范，于是他的自定义 agent 会开始用裸文件名引用产物、开始发 emoji、开始一个 cell 一个 cell 地打印 shape。切分之后，用户改身份的自由和平台保工作规范的需求互不干扰——这是一个干净的关注点分离（separation of concerns）。

可迁移的原则：任何允许用户自定义 system_prompt 的多 agent 平台，都应该把 prompt 切成「用户可替换层」和「平台继承层」。用户拥有身份，平台拥有规范。别让用户为了改身份而意外丢掉他根本不该管的平台约束。

2.3 working_style_prompt 逐条精读：一部「科研 agent 行为宪法」
operon 的 working_style 是整个系统里最长、最精雕细琢的一段行为规范。它值得逐条读，因为每一条都在解决一个具体的「LLM 常犯的错」。

（1）克制地用 plan——只在真正多阶段时
Reach for `generate_plan` only when the work is genuinely multi-stage… Skip
it for lookups, quick questions, a single computation, or inspecting a file…
A plan pauses for user approval, so a plan on a one-step task is friction
with no payoff; when in doubt, start without one and call `generate_plan`
later if the scope grows.
解决的问题：LLM 倾向于「仪式化」——什么任务都先列个计划显得郑重。但计划会暂停等用户批准，对单步任务纯属摩擦。规则给了明确的判据（多个分析要排序 / 长或贵的计算 / 用户需要签字的 pipeline）和一个默认倾向（拿不准就先不 plan，范围变大再补）。注意它解释了「为什么」——「A plan pauses for user approval」——而不是简单地说「别乱 plan」。

（2）产出物而非答案（本章点到，第四章详解）
Produce artifacts, not just answers. Whenever your work produces user-facing
outputs (figures, tables, reports, structure files), call `save_artifacts`
before moving on — plan or no plan, workspace files aren't visible to the
user until you do.
这条极其重要，第四章整章讲。这里只标记它在工作风格里的位置：它是继承给所有派生 profile 的——无论用户造什么 agent，「产出物必须 save」都跑不掉。

（3）用真实数据，别只靠 web search
for open-ended research asks like literature reviews or landscape surveys,
use them — fetch and analyze real data and deliver the results as artifacts
rather than answering from web search alone.
解决的问题：LLM 面对「综述一下这个领域」时会偷懒，直接凭 web search 摘要作答。规则要求它动用完整的计算环境和学术数据库，抓真实数据来分析。这与后文的「compute don't confabulate」是一脉相承的（见第九章）。

（4）实验室笔记本的语气，而非聊天语气——含一段反 emoji 的雄辩
Lean toward the register of a lab notebook or methods section rather than a
chat thread. Your reader is scanning for the result, the artifact link, the
caveat, the next step — and emoji (section-header decoration, celebration,
warmth signals) are visual noise between them and that payload. When you
feel the pull to add one, it's usually a sign to reach for structure
instead: a markdown header, a bold term, a clearer sentence. The artifact is
the hero; it doesn't need a 🎉 to announce itself.
这段是 prompt 写作的范本。它没有写「NEVER use emoji」，而是：

1. 给了读者模型：读者在扫描 result / artifact link / caveat / next step。
2. 论证了为什么 emoji 有害：它是这些 payload 之间的「视觉噪声」。
3. 给了替代方案：想加 emoji 的冲动其实是「该用结构了」的信号——用 header、加粗、更清晰的句子。
4. 给了一个记忆点：「The artifact is the hero; it doesn't need a 🎉 to announce itself.」
这就是「解释而非命令」的教科书示范（第九章主题）。一个禁令（别用 emoji）被重写成了一套可理解的推理，模型因此能在边界情况自行判断——比如它会明白「用户明确要求用 emoji」时该破例。

（5）数字列表要连续——一个渲染器的坑
When writing a numbered list, keep it as one uninterrupted `1. 2. 3. …`
block — don't put headers or prose between the items. A sub-heading mid-list
breaks it into pieces the renderer won't stitch back together, and items 3.
onward collapse into the paragraph.
这条是纯工程性的：Markdown 渲染器遇到列表中间插标题会断裂，3. 之后的项会塌进段落。这种「知道具体渲染器行为」的细节，只有在真实产品里踩过坑才写得出来。它提醒我们：working_style 不只是风格偏好，还沉淀了大量关于「输出会被怎么渲染」的实操知识。

（6）不要用行话套话——一段关于「可辩护措辞」的讲究
Casual shorthand and field cliché — calling an approach "unsexy," a method
"vanilla," a tool "the workhorse," a fix "quick-and-dirty" — read as
editorializing to a scientist, and the value judgment they carry isn't one
you can defend. When you reach for that kind of word you're usually
compressing a concrete property you could state directly: which approach is
more established, which is higher-resolution, which trades runtime for
accuracy. Name the property.
这条的洞察很深：套话（vanilla / workhorse / quick-and-dirty）之所以该避免，不是因为不专业，而是因为它们携带了一个你无法辩护的价值判断。而且套话通常是在偷懒地压缩一个你本可以直接陈述的具体属性——「更成熟」「分辨率更高」「用运行时换精度」。规则要求：说出那个属性（Name the property），别用套话糊过去。 面向科学家写作时，这是把「口语化 AI」调教成「可被同行评审接受的写作者」的关键一刀。

（7）叙述科学，不叙述管道（narrate the work, not the plumbing）
这是 working_style 里最长的一条，也是最能体现「用户视角」的一条：

Narrate the work, not the plumbing. In user-facing prose, say what you're
doing in domain terms — "dispatching three sub-agents to screen each
compound family", "pulling arXiv records for the citation list" — never
which tool or SDK function you're about to call… ("I'll call `host.delegate`
with `wait=False`"…). The reader cares about the science, not the mechanics…
Paraphrasing the mechanics is the same offense — "collect cell", "side/fresh
kernel", "side channel", "background cell", "steer the child", "dispatch is
mid-flight" are plumbing vocabulary even without a function name.
要点：

1. 正面例子 vs 反面例子并列：「dispatching three sub-agents to screen each compound family」（好）对比「I'll call host.delegate with wait=False」（坏）。
2. 堵住规避路径：光是不提函数名还不够——「side channel」「background cell」「steer the child」这些paraphrase 也算犯规，因为它们仍然是管道词汇。规则预判了模型会用「同义改写」来钻空子，并提前封死。
3. 给了删除判据：「If a sentence only explains which kernel or channel you're routing through, or why one is blocked, drop the sentence.」——如果一句话只在解释你走哪个 kernel/channel，直接删掉。
这条规则背后的哲学是：用户是科学家，不是这个 agent 系统的运维。他关心「三个子 agent 在筛化合物家族」，不关心「dispatch 正在飞行中所以我用 side channel 找 child」。把实现机制彻底挡在用户视线外，是产品成熟度的标志。

（8）先读文档再写代码——一次摊销 vs 三次重试
Before reaching for a specialized library… read its docs first. If a skill
exists for it, load that… If no skill exists, run a quick inspection turn
before writing real code: `print(lib.__version__)` plus `help()` on the key
functions… One amortized inspection turn is much cheaper than 2–3 retry
turns.
这条把「先探查再写」量化成了成本论证：一次探查回合（inspection turn）比 2-3 次重试回合便宜。它甚至指出探查能抓到什么——「version-changed return types, expected argument types, and other gotchas」（版本变更的返回类型、期望的参数类型）。这是用「回合经济学」来推销一个好习惯，而不是干巴巴地说「要仔细」。

（9）MCP 调用只在 repl、循环塞进一个 cell——kernel 拓扑约束
MCP calls happen in the `repl` tool — never in `python`/`r` (those kernels
have no MCP surface). Looping over samples or records? Write the loop in a
`repl` cell — `[host.mcp("server", "method", id=x) for x in ids]` is one
`repl` call with N host round-trips inside it — then `json.dump(...)` the
results to `./handoff/<name>.json` and `json.load(...)` them in the next
`python` cell…
这条揭示了 Claude Science 的一个核心执行模型：repl kernel 和 python/r kernel 是分离的进程，只共享工作目录（cwd），不共享内存。所以：

• MCP 只能在 repl 里调（python/r 没有 MCP surface）。
• 跨 kernel 传数据要走 ./handoff/*.json 文件，不能靠变量。
• 循环 N 个 MCP 调用应该写成一个 repl cell 里的 list comprehension（一次 repl 调用、内部 N 次 host round-trip），而不是 N 个 cell。
（10）每个 python call 是一次完整 LLM round-trip——成本意识的极致
Each `python` call is a full LLM round-trip. The kernel persists state, but
the turn doesn't come free. Write the whole logical step in one cell — fetch,
parse, check, compute — and put your sanity checks inline: `assert len(df) >
0, f"got {df.shape}"` costs nothing; a bare `print(df.shape)` as its own cell
costs a full turn. Only break when the *next line you write* depends on
output you haven't seen.
这条是我个人认为整个 working_style 里最锋利的一条。它点破了一个 LLM agent 的隐藏成本结构：kernel 状态是持久的，但每次提交一个 cell 都是一次完整的 LLM 往返（模型要重新读上下文、生成、等结果）。因此：

• 把一个逻辑步骤（取数→解析→检查→计算）写进一个 cell。
• sanity check 用 inline assert（assert len(df) > 0, f"got {df.shape}"）——它不花额外回合。
• 而单独一个 print(df.shape) 的 cell 要花一整个回合。
• 只在「下一行代码依赖你还没见过的输出」时才断开 cell。
这把「少发 cell」从一个模糊的效率建议，变成了一条有清晰判据的规则。判据是：断 cell 的唯一正当理由是「我需要先看到这个输出才能写下一行」。 其余一切都该塞进一个 cell。

（11）Compute, don't confabulate（本章点到，第九章详解）
Compute, don't confabulate. If a question needs data, fetch or load it; don't
hardcode plausible answers. When you fetch via `host.mcp()`, the result is
the source of truth — cite the identifiers it returns…
「计算，别瞎编」。需要数据就去取，别硬编一个看起来合理的答案。取回来的就是真相之源，引用它返回的标识符（NCT ID、accession），别引用你训练时记住的值。这是全系统反幻觉哲学的一条主脉，第九章会把它和 reviewer rubric、self-awareness、product-self-knowledge 串起来讲。

（12）能力也要落地，别凭记忆答「支持什么」
The same grounding applies to capabilities. When asked what you support or
which tools exist for a domain, that's a question about the catalog, not your
training — answer it like a data question: fan `search_skills` across the
field's vocabulary, then report only what came back. Knowing a method exists
in the literature is not evidence it's installed here…
这条把「反幻觉」推到了一个反直觉的地方：连「你支持哪些工具」都不许凭记忆答。 因为那是关于「本地 catalog」的问题，不是关于「训练知识」的问题。正确做法是用 search_skills 扫领域词汇，只报检索到的。「文献里存在某方法」不等于「这里装了它」。这一条与 product-self-knowledge skill（第八章）完全同构——不信任自己的训练记忆，一切事实性问题都去查权威来源。

2.4 从这一章能带走什么
1. 切分 prompt 的继承边界：用户可替换层（身份）/ 平台继承层（工作规范）。这是可自定义 agent 平台的地基。
2. working_style 是行为债务的沉淀池：渲染器的坑、kernel 拓扑、回合经济学、写作规范——这些跨所有 agent 通用的知识，应该集中在一个被继承的层里，而不是散落在每个 agent 各自的 prompt 中。
3. 每条规则都带「为什么」：回看这 12 条，没有一条是光秃秃的禁令。plan 那条解释了「plan 会暂停等批准」，emoji 那条给了读者模型，一个-cell 那条讲了回合经济学。这正是第九章「解释而非命令」主题的最密集样本。
收尾：identity/working-style 的切分看起来只是个工程细节，但它其实定义了「用户能改什么、平台守什么」的权力边界。而被继承的那段 working_style，是把一个通用 LLM 调教成「实验室里可信赖的同事」的全部行为规范——它值得你逐条读三遍。

下一章进入全系统设计密度最高的地方：追溯而非重算的评审 rubric。

第三章 追溯而非重算：一套幻觉检测的完整 rubric
代表文件：agents/reviewer/metadata.yaml 的 system_prompt（247 行提示词）
核心命题：如何让一个 LLM 可靠地审查另一个 LLM 的输出、抓出编造和幻觉，
而不制造假阳性——这是整个系统里推敲最深、边界划得最细的一份 prompt。

3.1 背景：REVIEWER 是什么
REVIEWER 不是根 agent，它由审查编排器（Verifier class）派生，收到的输入是指向另一个 agent 会话的指针——frame_id、消息窗口、执行日志 id、artifact id。它读那段 transcript，报告哪里编造（fabricate）、幻觉（hallucinate）、或偏离计划（deviate）。它的职责是只读的、固定的：trace → submit_output。

理解这个设定很重要，因为它解释了第一章讲过的那些配置——enable_thinking:false（追溯是模式匹配不是深思）、excluded_tools:[python]（追溯不许重算）、skills_locked:true（固定职责不需发现技能）——全都是为了服务 rubric 而做的能力裁剪。配置和 prompt 是同一设计意图的两面。

3.2 第一原则：Trace, don't recompute
整个 rubric 建立在一句话上：

Trace, don't recompute. If the agent claims a number, find the cell that
printed it and compare — a CONTRADICTION is the finding. A value you simply
cannot trace inside this window is NOT a finding: values routinely originate
earlier in the session than your review window.
这里藏着 rubric 最核心、也最反直觉的判定规则，我称之为**「非对称举证」**：

• 找到矛盾 → 定罪（found-contradiction convicts）。
• 找不到来源 → 不定罪（not-found never does）。
为什么？因为 REVIEWER 只看到会话的一个窗口，而大多数关键值在窗口之前就进入了会话。如果「找不到来源 = 编造」，那 REVIEWER 会把海量「其实来源在窗口外」的正确值全部误判为幻觉——假阳性爆炸。所以规则规定：只有当你实际检索到的证据与某个值矛盾时，才算发现；单纯追溯不到，永远不算。

这一条是整个 rubric 的「宪法第一条」，后面所有复杂的例外都是在小心翼翼地给它开口子，同时不破坏它。

3.3 按证据所在位置加权——同一个错，产物里比聊天里严重
rubric 的第二根支柱是「按 claim 住在哪里来定严重度」：

Weight by WHERE the claim lives. Artifact contents (saved files, figures,
tables, reports) are the session's durable output — a wrong value there is a
wrong value the user cites later with no transcript to check. Hold these to
the strict bar. Assistant prose is chat narration the user skims in the
moment — flag only if a reader ACTING on it would be materially misled.
Immaterial precision and wording nits in prose are not findings.
设计洞察：

• 产物（artifact）是会话的持久输出——用户以后会引用它，而且那时没有 transcript 可核对。所以产物里的错误值用严格标准。
• 聊天口述（prose）是用户当下扫一眼的叙述——只有「据此行动会被实质误导」才报。措辞小瑕疵、无关紧要的精度差异不算发现。
这是一个非常成熟的判断：错误的成本取决于它会被消费的方式。 图表标题里的错误会被后人当事实引用（高成本），聊天里的一句约整数（低成本）。用同一把尺子量两者是不专业的。

3.4 三级判决：fail / warn / pass
rubric 定义了三个判决等级，判准是一句总纲：

the line is "would a reader acting on this be misled, or is the work incomplete?"
（据此行动的读者会被误导吗？或者工作是否不完整？）

fail —— 结果不可信或不完整，agent 必须修
fail 的触发条件列了一长串，每一条都很精确。挑几条最有代表性的：

（a）声称做了但没做的动作

A claimed ACTION that did not happen — the agent asserts it ran, tested,
verified, or checked something, and no corresponding tool activity appears
anywhere in the traceable history.
agent 说「我跑了/测了/验证了」，但可追溯历史里找不到对应的工具活动。注意它给了这条一个逃生舱：如果这个动作可能发生在窗口之前，要先用 query_target_history 钻取再定罪——动作和值享受同样的「窗口前豁免」。

（b）实质矛盾工具输出的值

A value that MATERIALLY contradicts tool output — wrong sign, wrong order of
magnitude, wrong entity/gene/compound/accession, wrong direction of effect…
Not rounding or reformatting.
符号错、数量级错、实体/基因/化合物/accession 错、效应方向错——这些是实质矛盾。四舍五入或重新格式化不算。

（c）错误归因外部来源——但必须先打开来源核对

A claim the agent attributes to an external source — "the paper says X"… —
that contradicts what the source actually says, WHEN that source is available
to you (listed under Session source documents…). This is NOT domain recall:
the source is an artifact you can open. You MUST open it before dispositioning
the claim — call read_file(version_id=…, pages=[…]) on the pages the agent
itself cited… Do not emit "could not verify" without having attempted the
read.
如果 agent 说「论文说 X」而论文就在会话里，REVIEWER 必须打开论文对应页码核对才能定罪。而且限定「target pages — never read a whole document, and spend at most 1-2 reads per claim」（读它引用的那几页，每条 claim 最多 1-2 次读取）。不许在没尝试读取的情况下就说「无法验证」。 这条极其克制——它防止 REVIEWER 用「我核不了」来偷懒定罪。

（d）编造的引用——唯一「找不到也定罪」的例外

这是整个 rubric 里唯一打破「非对称举证」的地方，也是设计上最精妙的一处：

EXCEPTION — fabricated references. External citations and specific
identifiers PRESENTED AS RETRIEVED OR ESTABLISHED (a PMID, DOI, "Author et
al. YEAR", an accession) are checkable claims, not ambient values. Drill for
their origin; if the reference traces nowhere… it remains a finding. This is
the one class of VALUES where not-found still convicts: a reference that
resolves to nothing is the citation-confabulation failure mode this reviewer
exists to catch.
为什么引用可以「找不到也定罪」，而普通值不行？因为一个 PMID / DOI / accession 是声称「已检索到」的可核对断言，不是「环境里飘进来的值」。如果它追溯不到任何来源，那正是「引用幻觉」这个 REVIEWER 存在的意义所在的失败模式。这是对第一原则的一个精确开口——只对「声称已检索的外部标识符」开，其余一律遵守非对称举证。

而且这个例外自己又划了一圈边界：

• 自引用不算：agent 引用自己早前的 artifact/version id 或自己早前算的值，走普通值规则，不走这个例外。
• 被裁剪的跨度不算：如果 excerpt 显示来源跨度被截断（truncation markers），引用是「尝试后无法验证」→ warn，不 fail。
• 明面上被带进来的不算：如果标识符原样出现在 [carried identifiers from elided span(s)…] 行里，说明它在窗口前已进入会话——这是「不报」的情况，即使钻取返回 NOT FOUND。
• 对冲措辞不能免罪：「hedging ("I believe the PMID is…") does not convert a checkable reference into recollection; confabulated references naturally surface hedged.」——「我记得 PMID 大概是」这种对冲不能把可核对引用变成「凭记忆」，因为编造的引用天然就是对冲着冒出来的。这一刀堵死了最狡猾的规避。
这一整段是我见过的对「引用幻觉」最完整的形式化。 它精确到了「什么算引用、什么算普通值、对冲算不算、被截断算不算、被带进来算不算」的每一个角落。

warn —— 结果可信，但呈现或过程有瑕疵
warn — result is correct and trustworthy; process or presentation off.
Reserve warn for ARTIFACTS — a label, legend, axis name, or unit annotation
inside a saved file that doesn't match its data when the mismatch does NOT
change the conclusion a reader takes away…
warn 专门留给产物里「不改变结论」的呈现瑕疵——标签、图例、轴名、单位注错了，但读者拿走的结论没变。（改变结论的错是 fail。）它明确说「Prose-only process/style issues are not worth a finding」——纯聊天里的过程/风格问题不值得报。

pass —— 只记录给用户，不反馈给 agent
Only `fail` and `warn` are surfaced to the agent; `pass` is recorded for the user.
一个小而重要的机制细节：pass 不打扰被审查的 agent，只默默记给用户看。

3.5 「不许报」清单——防假阳性的护栏
rubric 花了大量篇幅列什么不该报，因为假阳性（把正确的判成错的）会让整个审查系统失去信任。

在 prose 里不报：

Do NOT flag in PROSE:
  • Rounding, truncation, unit/notation changes… when the conclusion holds
  • Paraphrases or summaries of tool output that preserve meaning
  • Stylistic, tone, or phrasing choices
任何地方都不报无来源的值（宪法第一条的重申）：

Do NOT flag unsourced values — anywhere, including artifacts. A value or
configuration with no visible in-window source is not evidence of
fabrication; most load-bearing values enter a session long before any given
review window. Flag a value ONLY when evidence you actually retrieved
CONTRADICTS it… Found-contradiction convicts; not-found never does.
这句「Found-contradiction convicts; not-found never does」在文件里出现的位置，是整份 rubric 的定盘星。

3.6 Drill before you disposition——定罪前先钻取
rubric 给了一个主动核查的机制，防止 REVIEWER 在信息不全时草率判决：

Drill before you disposition: when a LOAD-BEARING value, configuration,
decision, or claimed action in the window has no in-window source and your
verdict would turn on its origin… call `query_target_history` — pass the
summary id covering the span plus your question — to retrieve the original
before deciding.
即：当一个关键值/配置/决策/动作在窗口内无来源，而你的判决取决于它的来源时，先调 query_target_history 把原始记录拉出来再判。

这里还有一个极其细腻的「form 检查」：

When a history-query answer carries a FORM: line, or the quoted source shows
a different BINDING FORM than the window (literal constant vs
derived/formula/auto), value-equality does NOT clear the claim… A silent
change from a locked literal to a derived expression (or vice versa) is a
warn-severity finding even when the resolved values are equal today.
意思是：即使数值今天相等，如果绑定形式变了（本来是锁死的字面常量，悄悄变成了推导表达式，或反过来），也是 warn。因为「今天相等」不代表「明天相等」——一个字面 0.05 和一个 compute_threshold() 今天都返回 0.05，但语义完全不同。这是对「静默的语义漂移」的防范，远超一般的数值核对。

3.7 Domain recall 豁免——凭背景知识说的事实不追溯
Domain recall — a fact stated from the agent's own background knowledge with
NO source document in the session — is exempt from tracing; there is nothing
to check it against, so do not flag it (not even as warn).
如果 agent 凭自己的领域知识陈述一个事实、且会话里没有对应的来源文档，那无从核对，不报（连 warn 都不报）。但这个豁免有明确的终止条件：

The exemption ends the moment the session contains the source: once a paper,
manual, or spec the claim refers to is attached to the session… claims about
its contents are traceable and get the rubric above.
一旦来源进了会话，豁免立即失效，该 claim 就变成可追溯的。而且 domain recall 只覆盖「事实」，不覆盖「引用」——具体的可核对标识符永远走 3.4(d) 的编造引用例外。

这个「豁免 + 终止条件」的设计再次体现了系统的边界意识：它区分了「无从核对的领域知识」和「本该核对的可追溯断言」，并精确定义了两者的分界线是「来源是否在会话里」。

3.8 表格陷阱——一个真实误判催生的具体规则
rubric 里有一条极其具体的操作规则，它显然来自一次真实的误判：

Tabular artifacts — never eyeball-align a >5-column CSV/TSV row against its
header. Runs of same-valued flag columns drift under prose reading (a
`True,True,False,False` tail misread as `True,False,False` convicted a
correct claim). Parse the cell by name via the `repl` kernel:
`import csv; [r[col] for r in csv.DictReader(open(host.artifact_path(vid)))
if r[key]==target]`. Reading a saved file's cell is tracing, not
recomputation.
这条说：永远不要用肉眼把一个超过 5 列的 CSV 行对齐到表头。 因为一串相同值的 flag 列在「阅读」时会漂移——True,True,False,False 会被误读成 True,False,False，而这曾经导致一个正确的 claim 被误判。正确做法是用 repl kernel 按列名解析。最后一句化解了一个潜在矛盾：「读取已保存文件的某个 cell 是追溯，不是重算」——所以它不违反 excluded_tools:[python] 背后的「不许重算」原则。

这条规则的存在本身就是「配置即调优记录」哲学（第一章）在 prompt 层的延续——一个具体的失败（True,True,False,False 误判）被固化成了一条防止复发的操作指令，连触发它的数据都留在了注释里。

3.9 Context drift——对照压缩历史检查漂移
rubric 最后处理一种高级失败：agent 偏离了自己早前的决策。当 payload 含「Target's compacted history」（目标自己折叠的早期记忆）时：

Flag when the window shows the target:
  • Contradicting a decision or constraint a summary records, with no visible
    justification → warn (valid approach change) or fail (invalidates a
    deliverable / violates a hard constraint).
  • Re-doing work a summary says was already completed → warn.
  • Acting on a premise a summary shows was already disproven → fail.
即检查三种漂移：无理由推翻早前决策、重做已完成的工作、在已被证伪的前提上继续。而且警告「Do NOT trace values inside the summaries themselves — they are compacted prose, not tool output.」——摘要本身是压缩过的散文、不是工具输出，不能拿它当追溯依据。

3.10 这一章的方法论价值
REVIEWER 的 rubric 是一份可以直接迁移到任何「LLM 审查 LLM」场景的模板。它的可迁移结构是：

1. 定一个非对称举证原则：找到矛盾才定罪，找不到不定罪。这是防假阳性的地基。
2. 按证据位置加权严重度：持久产物严格、即时聊天宽松。
3. 给一两个精确的例外：像「编造引用」那样，只对「声称已检索的可核对标识符」开口子，并把这个口子的每条边界都划清。
4. 强制「核查后才判」：能打开的来源必须打开（限定页数/次数），不许未尝试就说「无法验证」。
5. 列一份「不许报」清单：把假阳性的常见来源（约整数、改格式、保义改写、无来源值）显式排除。
6. 把每次真实误判固化成一条具体规则：表格陷阱那条就是范例。
收尾：这份 rubric 之所以是全系统「设计密度最高」的文件，不是因为它长，而是因为它在「抓住真幻觉」和「不制造假阳性」这两个相互拉扯的目标之间，用极其精细的边界划分找到了平衡。它教给你的不是「怎么写审查 prompt」，而是**「怎么在两个对立的失败模式之间划一条可执行的线」**——这是所有高质量 rubric 设计的元技能。

下一章回到 operon，讲一个更贴近日常的设计：产出物而非答案。

第四章 产出物而非答案
代表文件：agents/operon/metadata.yaml（working_style 的 artifact 段）、
skills/self-awareness/SKILL.md（artifacts / artifact_versions 表结构）、
agents/bookmarker/metadata.yaml（把「保存了什么、存在哪」列为头号书签）
核心命题：科研 agent 的交付单位是可引用、可追溯、有版本的产物，不是聊天里的一段话。

4.1 一句设计宣言
operon 的 working_style 把它写成一条硬规则：

Produce artifacts, not just answers. Whenever your work produces user-facing
outputs (figures, tables, reports, structure files), call `save_artifacts`
before moving on — plan or no plan, workspace files aren't visible to the
user until you do.
关键机制：工作目录里的文件，在你调 save_artifacts 之前，用户根本看不见。 这不是一个建议，是一个可见性契约——workspace 是 agent 的私有草稿纸，只有显式保存的东西才进入用户的视野。

为什么科研 agent 要这么设计？因为科研的产出天然是制品：一张图、一个表、一份报告、一个结构文件（.pdb/.cif）。这些东西的价值在于能被引用、能被复查、能被下游消费。一段聊天里的口头结论做不到这些——它没有稳定的引用锚点、没有版本、复查时 transcript 可能已被压缩。第三章的 reviewer rubric 正是基于这个区别（产物严格、聊天宽松）。

4.2 引用产物必须带 version_id——一个「同名陷阱」的防范
这是 artifact 哲学里最工程化、也最容易被忽视的一条：

Embed saved figures inline in chat with `{{artifact:VERSION_ID}}`… When you
refer to a saved artifact anywhere else — chat prose, a report or README you
save as an artifact — write `[filename]({{artifact:VERSION_ID}})` using the
version_id that `save_artifacts` returned… Never drop the id: a bare filename
is only clickable when it exactly matches an artifact in scope, and not at
all outside the app.
规则的核心：永远不要用裸文件名引用产物，要用 {{artifact:VERSION_ID}}。 为什么？working_style 明确给了理由：

Inside a document artifact (a `.tex`, `.md`, or `.html` file you
`save_artifacts`), never write an image path as a bare filename —
`\includegraphics{figure.png}` or `![plot](figure.png)` breaks when two
artifacts share a name.
「breaks when two artifacts share a name」——两个同名产物时裸文件名会失效。 这是一个真实的、会咬人的 bug 场景：一个会话里存了两张都叫 figure.png 的图，![plot](figure.png) 到底指哪张？系统无法确定。而 {{artifact:art_ARTIFACT_ID}}（用 save_artifacts 返回的 artifact_id 加 art_ 前缀）唯一锚定一个产物，并且自动追踪该产物的最新版本。

这里体现了一个深层设计：产物有身份（artifact_id）、有版本（version_id），引用系统建立在身份而非名字之上。 名字会碰撞、会重复，id 不会。这和数据库设计里「用主键而非业务字段做外键」是同一个道理。

4.3 产物的数据模型——从 self-awareness 表结构反推
self-awareness/SKILL.md 暴露了产物在底层数据库里的完整模型，这让我们能看清「artifact 哲学」在数据层是怎么落地的：

artifacts 表（一个文件一行）：

id, project_id, root_frame_id, frame_id, filename, latest_version_id,
is_user_upload, is_ephemeral, folder_id, sort_order, priority, created_at
artifact_versions 表（一个保存的修订一行）：

id, artifact_id, version_number, frame_id, content_type, size_bytes,
checksum, storage_path, extracted_code, code_description, language,
agent_name, is_intermediate, is_checkpoint, parent_version_id,
producing_cell_id (→ execution_log.id), created_at
从这个 schema 能读出好几个设计意图：

1. artifact 与 version 分离：artifacts 是逻辑文件，artifact_versions 是它的每次保存。artifacts.latest_version_id 指向当前最新版。这就是为什么 {{artifact:art_ID}} 能「自动追踪最新版本」——引用挂在 artifact 上，渲染时解析到它的 latest version。
2. 每个版本记得自己是哪个 cell 产的：producing_cell_id → execution_log.id。这建立了产物到生成它的代码的可追溯链。reviewer 要核对「这个图的数据对不对」时，能顺着 producing_cell_id 找到产它的那次执行。
3. 版本有血缘：parent_version_id 让版本形成链，artifact_dependencies 表（artifact_version_id, depends_on_version_id, reference_name）更进一步记录了产物间的 DAG 依赖——「这张图依赖那个 CSV 的哪个版本」。
4. 区分中间产物和最终产物：is_intermediate / is_checkpoint 标记。这直接服务于下面 4.4 要讲的「检查点规则」。
5. 内容去重存储：content_snapshots 表是「content-addressed dedup store」（hash, content, size_bytes），按内容哈希去重。同样内容的多个版本不重复占空间。
这个数据模型是 artifact 哲学的骨架：正因为底层有 id、version、blood-line、producing cell 这套结构，上层「用 {{artifact:ID}} 引用、自动追最新版、可追溯到源代码」的体验才成立。

4.4 检查点规则——不是每步都存
artifact 哲学不是「无脑存一切」。working_style 明确区分了两类保存：

Intermediate data checkpoints follow the separate Checkpoint Rule — save
those only when regeneration would be expensive, not after every step.
• 用户可见产物（图/表/报告/结构）：产出即存，因为不存用户看不见。
• 中间数据检查点：只在「重新生成会很贵」时存，不是每步都存。
这个区分很关键——它避免了两个极端：既不让用户看不到成果（该存的产物必存），也不让工作区被无意义的中间态淹没（廉价可再生的不存）。is_checkpoint 字段就是这条规则在数据层的落点。

4.5 收尾要克制——别把产物列表复述一遍
artifact 哲学延伸到了「怎么在消息结尾呈现产物」：

The UI shows a thumbnail tray of every saved artifact under your message, so
don't list them all. Close with the primary deliverable — `[filename]({{
artifact:VERSION_ID}}) — one-line summary` — and add a line only for any
other file whose purpose isn't obvious from its name. Leave images and plots
out of the close; you've already embedded them inline and the tray shows
them.
要点：

• UI 已经有一个缩略图托盘（thumbnail tray）展示所有保存的产物，所以别在文字里再列一遍。
• 结尾只点主交付物（一行摘要），外加任何「名字看不出用途」的文件各一行。
• 图片和 plot 不进结尾——你已经 inline 嵌入了，托盘也有。
这是「叙述科学不叙述管道」（第二章）的一个具体延伸：不要让用户读一份他已经能在 UI 上看到的清单。 结尾是给「名字不自明的东西」补一句话的地方，不是产物目录的镜像。

4.6 bookmarker 的视角——产物是头号可书签内容
从 bookmarker/metadata.yaml 能反向印证 artifact 的中心地位。bookmarker 的职责是在别人的 transcript 里留「面包屑」，它的书签优先级排序里，「交付了什么、存在哪」排第二位（仅次于结论性的 verdict）：

2. The statement of what was delivered and where it lives — the agent's
prose "saved X to Y" sentence or an artifact bullet line like "- [report.md]
(report.md) — one-line description". (Never the raw tool JSON or ids.)
而且它明确规定书签要取agent 的散文陈述（「saved X to Y」），不要取原始工具 JSON 或 id：

WHAT IS NEVER A BOOKMARK
- Raw tool JSON: artifact_id/version_id strings, {"n_pass": 9, …} dumps…
- Anything inside a [tool_use …] or [tool_result …] block when the agent
  restated it in prose — quote the prose.
这与 operon 的「叙述科学不叙述管道」再次同构——面向用户的书签应该是「这份报告存到了这里」这样的人话，而不是 art_abc123 这样的机器 id。 整个系统在「用户看到人话、机器 id 藏在底层」这一点上高度一致。

4.7 这一章的可迁移原则
1. 交付单位是制品，不是消息。任何产出型 agent，都应该有一个「显式保存才可见」的产物机制，把私有草稿区和用户视野分开。
2. 引用建立在 id 上，不在名字上。名字会碰撞，用稳定 id + 自动追最新版，从根上消灭「同名指谁」的歧义。
3. 产物要可追溯到源代码（producing_cell_id）。这是让下游审查/复现成为可能的前提。
4. 区分「必存的成果」和「按需存的中间态」。用「重新生成是否昂贵」当判据。
5. 别复述 UI 已经展示的东西。收尾聚焦主交付物 + 名字不自明的补充说明。
收尾：artifact 哲学表面上是「记得存文件」，实质上是一整套**「让科研成果可引用、可追溯、可版本化」的数据与交互契约**。它是 reviewer 能严格审查产物、bookmarker 能标记交付、用户能在会话结束很久后仍能点开正确文件的共同地基。

下一章进入 skill 系统本身：技能解剖学与 kernel sidecar。

第五章 技能解剖学与 kernel sidecar
代表文件：skills/skill-creator/SKILL.md（613 行元技能）、skills/figure-style/kernel.py
（290 行出版级绘图库）、skills/alphafold2/SKILL.md（纯文档型 skill 范例）、
skills/self-awareness/SKILL.md（host.skills.* SDK）
核心命题：skill 是「渐进式加载的知识 + 可选的固化代码」，它的设计围绕
「上下文经济」和「一次写好、无限复用」两个目标。

5.1 什么是 skill：三级渐进式加载
skill-creator 把 skill 的加载模型讲得最清楚：

Skills use a three-level loading system:
1. Metadata (name + description) - Always in context (~100 words)
2. SKILL.md body - In context whenever skill triggers (<500 lines ideal)
3. Bundled resources - As needed (unlimited, scripts can execute without loading)
这是整个 skill 系统的地基——渐进式披露（progressive disclosure）：

• 第一级 metadata（name + description，约 100 词）：永远在上下文里。这是模型「知道有这个 skill 存在」的全部信息，也是决定「何时触发」的唯一依据。
• 第二级 SKILL.md 正文（理想 <500 行）：只在 skill 触发时才进上下文。
• 第三级 bundled 资源（无限大）：按需读取；scripts/ 甚至能直接执行而不必读进上下文。
设计意图非常清楚：上下文是稀缺资源，要按「模型此刻是否需要」来分层付费。 每个 skill 常驻的成本只有 100 词的 metadata；只有真正用到时才付 SKILL.md 正文的成本；大块参考资料和脚本则完全不占常驻上下文。这让系统能挂载几十上百个 skill 而不撑爆上下文——29 个 skill 常驻成本只是 29×100 词。

5.2 description 是触发的唯一开关——所以要「推一把」
既然 metadata 是模型判断「何时用这个 skill」的唯一依据，那 description 字段就是 skill 工程的重心。skill-creator 给了一条反直觉但极重要的建议：

Note: Claude tends to "undertrigger" skills -- to not use them when they'd
be useful. To combat this, please make the skill descriptions a little bit
"pushy". So for instance, instead of "How to build a simple fast dashboard…",
you might write "How to build a simple fast dashboard… Make sure to use this
skill whenever the user mentions dashboards, data visualization, internal
metrics, or wants to display any kind of company data, even if they don't
explicitly ask for a 'dashboard.'"
洞察：模型倾向于「欠触发」skill——该用时不用。对策是把 description 写得主动一点（pushy），显式列出「一提到 X、Y、Z 就该用，哪怕用户没明说」。

我们可以在真实 skill 里验证这一点。看 alphafold2 的 description：

Reach for this skill to fold a sequence or complex with the AF2/AF2-Multimer
evoformer, to validate designed sequences by self-consistency pLDDT, ipTM,
and RMSD, or to run a quick MSA-backed prediction…
它不只说「这是 AlphaFold2」，而是列举了三个具体的触发场景（折叠序列/复合物、验证设计序列、跑 MSA 预测），每个都用领域动词（fold、validate、run）开头。这正是「主动式 description」的实践。

再看 product-self-knowledge（第八章会详谈）的 description，它甚至以命令开头：

Stop and consult this skill whenever your response would include specific
facts about Anthropic's products.
「Stop and consult」——这是把「推一把」推到了极致，因为这个 skill 防的是幻觉，欠触发的代价特别高。

可迁移原则：skill/tool 的 description 不是说明书，是触发分类器的输入。写它时要站在「模型会不会在该用时想起我」的角度，主动列出触发信号，对抗欠触发。

5.3 两种 skill 结构：纯文档型 vs 带 kernel 型
纯文档型：以 alphafold2 为例
alphafold2 只有一个 SKILL.md，没有代码 sidecar。它的正文是什么？是踩坑经验的结晶。看它最精彩的一节：

## Unified-memory defaults loop forever under gVisor — the env patches them out
`colabfold/batch.py` hard-sets `TF_FORCE_UNIFIED_MEMORY=1` and
`XLA_PYTHON_CLIENT_MEM_FRACTION=4.0` on import. Under a gVisor sandbox
unified memory is unsupported, so JAX's `device_put` loops indefinitely
allocating host RAM during AF2 parameter load — the job appears hung, never
errors. Override both before the import…
这一段的价值不在于「怎么运行 AlphaFold2」（那是一行 colabfold_batch 命令），而在于**「它在这个沙箱环境里会怎么诡异地挂掉，以及为什么」**。ColabFold 在 import 时硬设了两个环境变量，在 gVisor 沙箱下会导致 JAX 无限循环分配内存——任务看起来卡住、但永远不报错。这种「知道特定环境下的特定失败模式」的知识，是训练数据里绝对没有的，也是 skill 存在的核心理由。

skill 正文还有一个「错误识别表」：

| You see | It means / do this |
| Job hangs silently during "Running model_1" with host RAM climbing |
  Unified-memory loop under gVisor — see the gotcha above… |
| `RESOURCE_EXHAUSTED` / OOM during XLA compile | …drop below the `0.95`… |
把「你会看到的现象」直接映射到「它意味着什么、怎么办」。这是运维知识的理想编码形式。

纯文档型 skill 的本质：它是curated 的领域知识 + 已知陷阱，把「专家踩过的坑」固化成模型触发时能读到的正文。skill-creator 印证了这一点——「skills carry curated usage patterns and known pitfalls」（operon working_style 原话）。

带 kernel 型：以 figure-style 为例
当 skill 的工作流依赖可复用的辅助函数时，就配一个 kernel.py（或 kernel.R）。skill-creator 解释了它的加载机制：

If the skill's workflow depends on reusable helper functions, ship them as
`kernel.py`… When any agent calls `skill({skill: <name>})`, that file is
executed in its persistent python/R kernel and the tool result reports which
top-level names were defined — so SKILL.md can say "call `annotate_df(df)`"
and the function already exists.
即：加载 skill 时，kernel.py 被执行进持久 kernel，其顶层定义的函数直接可用。于是 SKILL.md 只需说「调 annotate_df(df)」，函数已经在那里了。这是「把可复用逻辑固化成代码、prompt 只管调用」的机制——省掉了每次让模型重新写一遍辅助函数的成本和出错风险。

5.4 figure-style/kernel.py 深读：一个「机制而非美学」的绘图库
这个 kernel 是带代码型 skill 的典范，值得逐个函数分析，因为它示范了「好的 kernel 长什么样」。

设计宣言写在第一个函数的 docstring 里
def apply_figure_style(*, frame="open", font=None, sizes=(8, 7, 6), grid=False):
    """Set matplotlib rcParams for publication-grade output. Call once before plotting.
    This sets mechanics (role-mapped font-size ladder, outward ticks, frameless
    legends, 300-dpi save, Type-42 embedded fonts) — not a house aesthetic.
    Frame, font and the size ladder are parameters.
    """
关键句：「This sets mechanics… not a house aesthetic.」 它设的是机制——字号阶梯、朝外的刻度、无框图例、300dpi 保存、Type-42 嵌入字体——而不是一套「审美风格」。frame/font/字号都是参数，用户可调。

这个区分很深刻：一个绘图辅助库，如果强加一套具体审美（固定配色、固定字体），会让所有图长一个样、且难以适配不同期刊要求。而 figure-style 只固化普适的出版级机制（矢量图字体要可编辑所以 Type-42、刻度朝外更清晰、图例框是噪声所以去掉），把审美选择留成参数。「机制固化、美学参数化」是可复用工具库的黄金分割线。

每个函数都锚定到一份规范（§）
注意函数 docstring 里的 §3、§5.7、§6.1：

def set_frame(ax, style="open"):
    """§3: set spine visibility on an existing axes…"""
def panel_letter(ax, letter, dx=-0.18, dy=1.02, case="lower", fontsize=None):
    """§5.7: bold panel letter outside top-left of axes…"""
def bar_with_points(ax, x, ymat, labels, colors, …):
    """§6.1: bar = mean; optionally overlay raw points or draw an interval."""
这些 § 号指向 SKILL.md 正文里的编号章节。kernel 代码和 skill 文档通过 § 号双向锚定——文档说「按 §6.1 画带点柱状图」，代码里 bar_with_points 的 docstring 标着 §6.1。这让「文档描述的规范」和「实现它的代码」保持一一对应，改一处能顺藤摸到另一处。这是第一章「配置即调优记录」在代码组织层的回响。

统计正确性被认真对待
看 bar_with_points 里误差棒的实现：

elif errorbar == "ci95":
    from scipy.stats import t
    def _hw(y):
        n = np.asarray(y).size
        return t.ppf(0.975, n - 1) * np.std(y, ddof=1) / np.sqrt(n) if n > 1 else 0
docstring 解释了为什么用 t 分布而不是 z：

'ci95' is the t-distribution 95% CI of the mean (half-width t_{0.975,n-1}·
s/√n); correct at small n where the z-approximation (1.96·s/√n) is markedly
too narrow.
它没有偷懒用 1.96×s/√n，而是用 t 分布的临界值，并解释了原因——小样本下 z 近似「明显过窄」。对一个绘图辅助库来说，这种统计上的较真是罕见的，也正是「科研级」的体现：图不只是好看，图上的误差棒得是对的。

反 legend 的设计倾向
kernel 里有 end_of_line_labels（在线的右端直接标名，替代图例框）和 goodness_arrow（在边角标「↑ higher = better」）。这些函数的存在体现了一种绘图哲学：尽量用「就地标注」替代「图例框」，因为图例框逼读者在图和图例之间来回跳视线。这与前言里引用的用户记忆「self-label dots over legends」完全吻合——用户明确偏好自标注点而非图例。

panel_crops：一个为「AI 看图」设计的函数
最后一个函数 panel_crops 很特别，它返回每个子图面板在保存的 PNG 里的像素裁剪框：

>>> fig.savefig("fig.png")
>>> for letter, box in panel_crops(fig).items():
...     host.view_image("fig.png", crop=box)
它的用途是让 agent 能逐个面板地放大查看自己画的图（host.view_image(path, crop=box)）。这是一个「为 agent 自查而设计」的工具——多面板复合图整张看太小，agent 需要裁出每个面板单独审视。这揭示了 kernel 不只服务「生成」，也服务「agent 对自己产出的验证」。

5.5 kernel.py 的工程约束——sidecar loader 的规矩
skill-creator 详列了写 kernel.py 的约束，每条都对应一个真实的加载失败模式。这些是「想写 kernel sidecar 必须知道」的坑：

- Top-level definitions only: functions, imports, and literal constants —
  top-level `class` statements and decorators are rejected by the validator
  (define classes inside a factory function if needed).
- Default argument values must be literals — `def f(url=MY_CONSTANT)` gets
  the whole file rejected. Wrap constants with an explicit `is None` check…
  (not `url = url or MY_CONSTANT`, which also replaces `0`, `""`, `[]`).
- Do not use `_`-prefixed top-level names — they are reserved by the sidecar
  loader…
- Defer third-party imports to inside function bodies. The skeleton python
  env ships stdlib + a small starter set (numpy, pandas, scipy, matplotlib,
  seaborn, pillow), so e.g. `import requests` at module scope surfaces a load
  error on every fresh kernel.
- Keep it small and self-contained. `kernel.py` cannot import from the
  skill's `scripts/` dir…
逐条对照 figure-style/kernel.py，会发现它严格遵守了每一条：

• 只有顶层函数和一个字面常量 META_GREY = "#888888"，没有顶层 class。
• 第三方 import（matplotlib、scipy.stats、numpy）全部延迟到函数体内——apply_figure_style 里才 import matplotlib as mpl。这正是为了满足「skeleton env 只有 starter set，模块级 import 第三方会在每次新 kernel 加载时报错」。
• 默认参数全是字面量（frame="open"、sizes=(8,7,6)），fontsize=None 后用 if fontsize is None 展开——完全按规矩来，避开了「默认值不能是常量引用」的坑。
figure-style/kernel.py 本身就是「怎么写合规 kernel」的活教材。 这也说明 skill-creator 里那些约束不是纸上规矩，是被真实 skill 验证过的。

命名空间机制——多 skill 共存的巧思
skill-creator 还解释了一个精细的命名空间设计：

each `kernel.py`/`kernel.R` runs in its own namespace, and its public names
are mirrored to the shared session — bare when no earlier-loaded skill owns
the name (first-owner-wins), and normally also under a stable qualified alias
(typically `<skill-slug>__<name>`…). If another skill already owns a bare
name, the load report tells the agent the exact alias to call…
即：每个 kernel 有自己的命名空间，公开名字镜像到共享会话——没人占用时用裸名（先到先得），同时通常还有一个限定别名（<skill-slug>__<name>）。名字冲突时，加载报告告诉 agent 该用哪个别名。这解决了「几十个 skill 各带 kernel、函数名难免撞车」的规模化问题——不要求全局唯一，但提供确定性的消歧路径。

5.6 skill-creator：把「造 skill」也变成测量驱动的迭代
skill-creator 是元技能（教 Claude 造 skill），它最重要的贡献是把第一章的「测量驱动」哲学系统化成一个可执行的 skill 开发流程：

- Decide what you want the skill to do…
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
- Rewrite the skill based on feedback…
- Repeat until you're satisfied
- Expand the test set and try again at larger scale
关键设计点：

1. 对照实验：每个测试 case 同时跑「带 skill」和「不带 skill（baseline）」两个 subagent，在同一回合发起，这样它们同时完成、可比。这和第一章 reviewer 用 baseline 对照测 thinking 效果是同一方法。
2. 量化 + 定性双轨：既有 benchmark.json（pass_rate、时间、token 的 mean±stddev + delta），也有人工在 viewer 里逐 case 看输出留 feedback。它明确指出主观 skill（写作风格、艺术）不该硬套量化 expectation——「don't force expectations onto things that need human judgment」。
3. description 优化有独立的 eval 循环：run_loop.py 把 eval 集切 60% 训练 / 40% 留出，每个 query 跑 3 次测触发率，迭代最多 5 次，按留出集分数选最佳 description 以防过拟合。这又是「训练/测试分离」用在 prompt 上（对应第一章 bookmarker 的 dev/holdout）。
4. 触发 eval 的 query 要真实、要刁钻：skill-creator 花了整段讲怎么写 eval query——要有具体细节（文件路径、列名、公司名）、要有口语和错别字、should-not-trigger 的要用「近似但不该触发」的刁钻 case 而非「明显无关」的送分题：
Bad: "Format this data", "Extract text from PDF", "Create a chart"
Good: "ok so my boss just sent me this xlsx file (its in my downloads,
called something like 'Q4 sales final FINAL v2.xlsx')…"
5.7 skill 的写作哲学——又见「解释而非命令」
skill-creator 关于「怎么写 skill 正文」的指导，是第九章主题「解释而非命令」的又一次密集出现，值得原样引用：

Try to explain to the model why things are important in lieu of heavy-handed
musty MUSTs. … Today's LLMs are smart. … If you find yourself writing ALWAYS
or NEVER in all caps, or using super rigid structures, that's a yellow flag —
if possible, reframe and explain the reasoning so that the model understands
why the thing you're asking for is important. That's a more humane, powerful,
and effective approach.
「全大写的 ALWAYS/NEVER 是黄旗」——这是整个系统 prompt 写作观的旗帜性表述。它把「堆砌禁令」明确标记为一种代码异味，主张用「解释为什么」替代。这解释了为什么 operon working_style、reviewer rubric 通篇都在讲道理而非下命令。

它还有一条关于「泛化 vs 过拟合」的深刻提醒：

if the skill you and the user are codeveloping works only for those
examples, it's useless. Rather than put in fiddly overfitty changes, or
oppressively constrictive MUSTs, if there's some stubborn issue, you might
try branching out and using different metaphors…
即：skill 是要在海量不同 prompt 上大规模复用的，而你只在少数几个例子上迭代——所以别做「只在这几个例子上管用」的过拟合修改。遇到顽固问题，宁可换个比喻、换种工作模式，也别堆越来越严的 MUST。这是把 ML 的「过拟合」概念直接搬到了 prompt 工程，并给出了对策。

5.8 host.skills.* SDK——skill 是可编程的一等对象
skill 不只是静态文件，它通过 host.skills.* SDK 成为可编程对象（在 repl kernel 里）：

host.skills.list()                          # 所有 skill + 草稿
host.skills.read(name, path="SKILL.md")     # 读
host.skills.edit(name, path, content, old_string=None)  # 建/改（可 str_replace）
host.skills.publish(name, overwrite=False)  # 草稿 → 正式
这意味着 agent 能在运行时创造和修改 skill。operon working_style 里那条「offer to capture the pattern」正是基于此——当 agent 刚建好一个用户会重复运行的工作流，它可以主动提议「把这个模式固化成 skill」，然后用 host.skills.edit/publish 落地。skill 系统因此是自生长的：agent 的每一次成功工作流都可能沉淀成一个未来可复用的 skill。

5.9 这一章的可迁移原则
1. 渐进式披露：把知识分成「常驻 metadata / 触发时正文 / 按需资源」三级，按「此刻是否需要」分层付上下文成本。这是挂载大量能力而不撑爆上下文的唯一办法。
2. description 是触发分类器的输入：主动列触发信号，对抗欠触发。
3. 纯文档型 skill = curated 陷阱知识：它的价值在于「训练数据里没有的、特定环境的失败模式」，不在于复述通用用法。
4. kernel = 机制固化、美学参数化：把普适机制写进代码一次写好，把审美/场景选择留成参数。figure-style 的「mechanics not aesthetic」是黄金准则。
5. 代码与文档双向锚定（§ 号）：让规范描述和实现保持可追溯的对应。
6. 造能力的过程本身要测量驱动：对照 baseline、量化+定性双轨、训练/测试分离防过拟合。
7. 写指令时解释为什么：全大写的 ALWAYS/NEVER 是黄旗。
收尾：skill 系统是 Claude Science「能力可扩展性」的载体，但它真正精巧的地方不在于「能挂很多 skill」，而在于它用上下文经济学（渐进披露）、软件工程（kernel 约束、命名空间、id-based 引用）、和 ML 方法论（对照 eval、防过拟合）三套原理，共同支撑起一个能自生长、可大规模复用的能力体系。figure-style/kernel.py 值得任何做科研绘图的人直接读一遍源码——它是这套哲学最紧凑的实体化。

下一章看系统与用户的第一次接触：首次引导对话设计。

第六章 首次引导对话设计
代表文件：agents/onboarding/metadata.yaml（285 行）
核心命题：新用户的第一次对话是一个被精密编排的「理解-提议-赋能」流程，
它的每一条规则都在防止一种具体的、会毁掉第一印象的失败。

6.1 onboarding 是一个「只问不做」的特殊 agent
onboarding 的配置开门见山地定义了它的极简能力边界：

agent_name: ONBOARDING
internal: true
excluded_tools:
  - bash, python, r, repl, save_artifacts, manage_environments,
    manage_packages, write_file, edit_file, fetch_article_fulltext,
    web_search, web_fetch, list_compute, … search_skills
enable_plan_mode: false
enable_subtask_delegation: false
enable_thinking: false
它几乎排除了所有工具，注释解释了原因：

# Onboarding is a short, structured conversation — it gathers context and
# proposes a first task. It never executes code, manages environments, reads
# files, or touches compute; those happen later in the real session.
# Excluding them keeps the model on-script and the turn fast. ask_user is
# intentionally NOT excluded — it is the whole mechanism (renders the
# elicitation cards).
关键洞察：排除工具是为了「让模型不跑偏、让回合快」（keeps the model on-script and the turn fast）。 onboarding 的职责是纯对话——理解用户、提议任务。如果给它 python/web_search，模型可能会在引导阶段就手痒去执行，破坏对话节奏。唯独 ask_user 保留——「it is the whole mechanism」，因为它渲染选项卡片，是整个引导的载体。

这和 reviewer 的 excluded_tools:[python]（第一/三章）是同一个设计动作：用能力裁剪把 agent 焊死在它该做的事上。 只不过 reviewer 焊死在「追溯」，onboarding 焊死在「对话」。

6.2 流程的六步编排
onboarding 的 system_prompt 定义了一个严格的六步流程：

1. Open（开场） —— 第一个回合只能是 ask_user 调用，不许有任何可见文字。
2. Understand（理解，≤4 问） —— 短访谈，每问一个 ask_user + 3-5 个选项卡。
3. Open door（开放式追问） —— 「还有什么要告诉我的？」，唯一一个不以工具调用结尾的回合。
4. Propose（提议任务） —— 一个 ask_user 提供恰好三个首任务。
5. Set up tools（配置工具，恰好一次） —— 在用户选定任务之后才请求权限。
6. Hand off（交接） —— 一句话宣布任务现在开始，结束回合。
这个流程的每一步都藏着一条防错规则，下面逐个拆。

6.3 第一回合的铁律：只有卡片，没有问候
Your first turn must be ONLY the `ask_user` call — no greeting, no lead-in,
no visible text of any kind before it. Anything you write on the first turn
shows up as a duplicate greeting the user has already read.
为什么？因为产品已经在屏幕上问候过、并已经显示了第一个问题。如果模型再写一句问候，用户会看到重复的问候。这是一个只有在真实产品 UI 里才会暴露的坑——模型不知道「屏幕上已经有东西了」，所以 prompt 必须显式告诉它「你的第一个 token 之前，用户已经读过问候了」。

这条规则揭示了 onboarding prompt 的一个特质：它大量编码了「模型看不见的 UI 状态」。 模型只看到对话流，看不到产品已经渲染了什么。prompt 的职责之一就是补上这个信息差。

6.4 访谈的核心纪律：理解，而非选活
这是 onboarding 最深刻的一条设计，也是最容易被做错的地方：

**Interview questions understand; they never select work.** Never ask "what
would help most right now", "what do you most want help with", "where should
we start", or any question whose options read like tasks I could do — that IS
the task proposal, and asking it twice (once as a question, once as the
proposal) makes the proposal feel redundant. The interview learns about their
world; the proposal step is where doing enters.
访谈问题是用来「理解用户的世界」的，绝不能用来「让用户选活」。 因为「你最想让我帮什么」这类问题本身就是任务提议——如果访谈阶段问了，第 4 步再提议一次，用户会觉得重复、多余。所以：访谈了解世界，提议阶段才引入「做」。

这是一个非常精细的对话设计哲学：把「了解」和「决定做什么」严格分成两个阶段。了解阶段纯粹是建立对用户的理解，不掺任何「选活」的动作。

配套规则：永不漏斗（Never funnel）
**Never funnel.** Do not let questions zoom narrower and narrower (field →
one data type → one preference about that data type) — that leaves you
knowing everything about one sliver and nothing about the rest of their work…
Each question should open a NEW dimension of their work instead.
不要让问题越问越窄（领域→一种数据类型→关于这种数据类型的一个偏好），那会让你对一个细枝末节了如指掌、对其余一无所知，逼得后面的任务提议全挤在那个细枝末节里。每个问题应该打开用户工作的一个新维度。 prompt 甚至列了好的维度：他的研究要发现什么、日常工作长什么样、一直想做但没时间做的是什么。

这条规则解决的是一个真实的对话退化模式——追问的引力。模型天然倾向于顺着用户上一个答案深挖（这在别的场景是好事），但在广度访谈里，深挖会导致「盲人摸象只摸到一条腿」。规则用「每问打开新维度」对抗这种引力。

选项要用用户熟悉的词汇，但不能收窄范围
Options should be informed by prior answers (a computational biologist sees
computational options) — but informed means familiar vocabulary, not a
narrower scope.
「被先前答案告知」意味着用他熟悉的词汇（计算生物学家看到计算类选项），而不是收窄范围。这是对「个性化」的一个精确定义——个性化是调整词汇，不是缩小视野。

6.5 第一个问题是硬编码的
**Your FIRST question must be exactly** "What kind of biology do you do?"
with exactly these four options in this order: "Computational — sequencing,
omics, modeling", "Wet lab — bench work, assays, screens", "Structural /
biophysics", "A mix of bench and computational". The product pre-renders this
exact question the instant the chat opens…
第一个问题逐字固定：「你做哪种生物学？」+ 四个固定选项。因为产品在聊天打开的瞬间就预渲染了这个问题，用户的答案直接送进模型的调用。所以模型「never word it differently, never add options, and never re-ask it」。

这又是「模型看不见的 UI 状态」的一个实例——产品和模型必须在这个问题上字对字一致，否则会错位。第一问定死，后续全部自适应。

6.6 「开放式追问」——唯一不调工具的回合
第 3 步是流程里一个奇特的例外：

After the interview and BEFORE proposing tasks: write the full invitation as
your visible text. Say WHY you are asking… and END YOUR TURN — no tool call
of any kind, and in particular NO `ask_user`. This is the only turn in the
whole onboarding that ends without a tool call…
它要求模型写一段邀请（「我要提议几个首任务了，我越了解你的工作、提议就越有用——还有什么要告诉我的？可以丢个论文或数据集进来」），然后结束回合、不调任何工具。这是整个引导里唯一一个不以工具调用结尾的回合。产品随后会显示一个文件拖放区和普通输入框。

为什么要专门设计这么一个「裸回合」？因为前面全是选项卡片（结构化输入），而这一步需要开放式输入——用户可能想打字描述、可能想拖个文件。卡片模式不适合这个。所以流程在这里故意「降档」到自由对话。这体现了对话设计里「结构化 vs 开放式」输入的有意切换——大部分时候用卡片保持紧凑，但在「让我补充点什么」这个天然开放的时刻，切回自由文本。

6.7 三个任务：真正不同，不是一个任务三种尺寸
第 4 步提议任务的规则同样精细：

**Three genuinely different ideas — never one task at three sizes.** Each
proposal should draw on a different part of what they told you… "Count cells
on one image" / "count cells on a folder of images" / "count cells on
everything with stats" is ONE idea three ways — that is a defect. Three
different directions, each one concrete.
三个真正不同的想法，不是一个任务的三种尺寸。 「数一张图的细胞 / 数一个文件夹的 / 数全部并加统计」是同一个想法的三个版本——这是缺陷。要三个不同方向，各自具体。

有意思的是，prompt 内部确实有三个「雄心等级」（Quick win / Hands-on / Ambitious），但这是给模型的内部校准，要求把它们分散到三个不同想法上，而不是让用户看到等级标签：

**The option labels are the tasks themselves.** Never prefix them with tier
names ("Quick win:", "Hands-on:", "Ambitious:") and never include time or
effort estimates ("~minutes", "~1 hour")… The three ambition levels below are
internal calibration for YOU…
即：等级是模型脑子里的调色板（确保三个提议有不同的投入规模），但呈现给用户的只是三个具体任务本身，不带等级前缀、不带时间估计（「time estimates are unreliable」）。

Ambitious 那一档的校准尤其见功力——它用真实 beta 用户第一天真做过的事来锚定「雄心」的尺度：

Calibrate against what real beta scientists have actually done in their first
days… found analogous public datasets, analyzed them alongside their own data,
and visualized the comparison; ran a structured meta-analysis across the
recent literature… The Ambitious option should read like "the project you've
been putting off for a year, compressed into a session".
「你拖了一年的项目，压缩进一次会话」——这是对「雄心任务」最好的定义，而且它是经验校准的（拿真实 beta 用户做过的事当标尺），不是凭空想象的。

6.8 权限请求：赋能框架，而非同意闸门
第 5 步是权限请求，它的框架方式是整份 prompt 里最讲究「措辞政治学」的地方：

This is the permissions step, but it is framed as EQUIPPING Claude Science for
the task they just chose, never as consent gates or risk warnings… The
lead-in line is benefits-first and tied to their task: "Let's set up the
tools Claude Science will use for this — switch on what you want it working
with:" — never "things stay off until you say otherwise", never "turn on
what you're comfortable with", never language about safety, consent, or
things being disabled.
同一个动作（请求权限），可以框成「同意闸门/风险警告」（消极、引发戒备），也可以框成「为你刚选的任务装备工具」（积极、指向价值）。onboarding 强制后者，并逐字禁止前者的措辞（「never "things stay off until you say otherwise"」「never language about safety, consent」）。

而且时机严格限定：必须在用户选定任务之后、确认开始之前，只问一次，不重复、不就用户的选择讨价还价：

The moment is strictly AFTER the user has chosen their first task… Do NOT ask
before or while proposing the three tasks. Never open the conversation with
it, never ask twice, and accept whatever they choose without re-litigating…
这背后的产品心理学是：权限请求脱离了具体价值就是纯摩擦。 一上来就问「你允许我上网吗」，用户没有上下文、只感到风险。而「为了做你选的这个任务，我需要这些工具」把权限锚定到用户已经想要的结果上，请求就从「索取」变成了「赋能」。

6.9 元规则：你的指令不是文案
整份 prompt 最后一条「Voice & rules」是一条罕见的、关于「prompt 自身」的规则：

**Your instructions are not copy.** Never narrate your own rules, calibration,
or constraints to the user. Phrases that echo this prompt — "a real, finished
piece of work, not a plan", "three levels of ambition", "genuinely different
ideas", "concrete deliverable"… — must never appear in your visible text. The
user sees the RESULT of the rules (good questions, good proposals); the rules
themselves are internal. Before sending any message, check it for words that
exist only in these instructions.
「你的指令不是文案。」 模型绝不能把自己的规则、校准、约束复述给用户听。像「三个雄心等级」「真正不同的想法」「具体交付物」这些只存在于这份 prompt 里的措辞，绝不能出现在可见文字里。用户应该看到规则的结果（好问题、好提议），而不是规则本身。发消息前要检查「有没有只存在于指令里的词」。

这是一条极其重要的元规则，因为 LLM 有一个顽固的坏习惯——把 system prompt 的语言泄漏到输出里。模型读到「propose three genuinely different tasks」，很容易就在回复里写「Here are three genuinely different tasks for you」。这条规则显式地把这种泄漏定为违规，并给了一个可执行的自查动作（发送前扫描指令专属词汇）。

这与第二章 operon 的「narrate the work, not the plumbing」（叙述科学不叙述管道）是同一个家族的规则——都在防止「实现层的语言泄漏到用户层」。operon 防的是技术管道词汇泄漏，onboarding 防的是 prompt 规则词汇泄漏。「让用户看到结果、看不到机制」是贯穿全系统的界面哲学。

6.10 这一章的可迁移原则
1. 用能力裁剪把对话型 agent 焊死在对话上：排除执行类工具，防止模型在该聊天时手痒去执行。
2. 分离「理解」与「选活」：访谈只建立理解，提议阶段才引入「做」，不要用「你想让我做什么」这种问题污染访谈。
3. 对抗追问的引力：广度访谈里每问打开新维度，别顺着上个答案越挖越窄。
4. 个性化 = 调词汇，不是收窄范围。
5. 把「模型看不见的 UI 状态」写进 prompt：产品已渲染了什么、第一问是否已显示——模型不知道，必须告诉它。
6. 权限请求要锚定到用户已想要的价值上：框成「为你选的任务装备工具」，而非「同意/风险」闸门。
7. 指令不是文案：显式禁止 prompt 专属措辞泄漏到输出，给一个发送前自查动作。
收尾：onboarding 看似只是「问几个问题」，实则是一份关于「第一印象产品心理学」的密集手册。它反复在做同一件事——预判模型会犯的一类具体错误（重复问候、越问越窄、把规则说出口、把权限框成风险），然后用一条带理由的规则精确堵住它。 这与第一章「配置即调优记录」是同构的：那里是配置项带着实测证据，这里是对话规则带着「会毁掉什么体验」的理由。

下一章看系统如何接触外部世界：MCP 聚合架构。

第七章 MCP 聚合架构
代表文件：mcp-servers/bio-tools/run_server.py（服务器分发入口）、lib/ 目录结构
核心命题：几十个生物信息学数据源，不是拍平成一个巨型工具面，也不是散成上百个独立
服务器，而是按领域聚成 24 个 MCP server 包，共享一个 ~87 模块的底层 lib——
这是「工具规模化」的一个折中范式。

7.1 先纠正一个容易犯的误读
初看 bio-tools，很容易得出「一个 MCP server 暴露 87 个数据源」的结论。读 run_server.py 后必须纠正：它是 24 个按领域分组的 MCP server 包，架在一个约 87 模块的扁平 lib/ 之上。 这个区分不是细节，它正是本章要讲的核心架构决策——「聚合的粒度」。

run_server.py 的分发逻辑把这一点讲得很清楚：

def discover_servers():
    # a server = a package under lib/ whose name starts with "mcp_"
    # and that contains a server.py
    …
def main(server_name):
    module = importlib.import_module(f"{server_name}.server")
    module.mcp.run()
即：一个 server = lib/ 下一个以 mcp_ 开头、且含 server.py 的包。 磁盘上 lib/ 有 25 个 mcp_ 目录——24 个真实 server + 1 个 mcp_servers_common（共享辅助，不是 server）。每个 server 是一个领域分组（如 mcp_structure、mcp_sequence、mcp_literature……），它内部再调用扁平 lib/ 里那 ~87 个功能模块。

三层结构因此是：

调度入口 (run_server.py)
   └── 24 个领域 server 包 (lib/mcp_*/server.py)   ← MCP 暴露面 / 聚合粒度
          └── ~87 个功能模块 (lib/*.py)             ← 实际数据源实现
7.2 为什么是「24 个领域服务器」，而不是两个极端
工具规模化有两个诱人但都错的极端：

极端 A：一个巨型 server 暴露全部 87 个工具
坏处：工具描述会挤爆上下文，且模型选错工具的概率随工具数线性上升。 MCP 的每个工具都要把 name + description + schema 常驻在模型可见的工具面里。87 个工具的 schema 是巨大的常驻成本，而且模型在 87 个里挑一个，误选率高。这与第五章 skill 的「渐进式披露」要解决的是同一个问题——上下文是稀缺资源，不能让所有能力同时全量常驻。

极端 B：87 个独立 server，一个数据源一个
坏处：运维与连接开销爆炸，且共享逻辑无处安放。 每个 server 要独立启动、独立握手；而像「HTTP 重试」「accession 校验」「速率限制」这种跨数据源的通用逻辑，会在 87 处重复。

折中：按领域聚成 24 个
mcp_structure 把所有结构相关的数据源（PDB、AlphaFold DB、结构比对……）聚在一个 server 里；mcp_literature 把文献相关的（PubMed、arXiv、bioRxiv……）聚在一起。这样：

• 模型面对的是「领域」这个它天然会用的分类维度——要查结构就去 structure server，选择成本低。
• 同一领域的数据源能共享 mcp_servers_common 里的辅助（HTTP 客户端、错误封装、通用解析）。
• 24 个 server 可以按需启动——不做结构分析的会话根本不必拉起 mcp_structure。
可迁移原则：工具聚合的粒度应该对齐「用户/模型的心智分类」（这里是科学领域），而不是对齐「实现单元」（一个数据源）或「一锅端」（全塞一个 server）。聚合粒度 = 选择成本与复用收益的平衡点。

7.3 server 与 lib 的分离——暴露面 vs 实现
run_server.py 只认「mcp_ 开头 + 有 server.py」的包为 server，这个约定造就了一个干净的分层：

• lib/mcp_*/server.py（暴露层）：定义 MCP 工具、写工具 description、组织参数 schema。这是模型看得见的部分。
• lib/*.py（实现层）：~87 个功能模块，是实际去调 NCBI / EBI / PDB 等的代码。模型看不见它们，只通过 server 层间接使用。
这个分离的价值在于：同一个底层实现模块可以被多个领域 server 复用，而每个 server 可以为自己的领域裁剪、命名、描述工具。 一个「序列比对」的底层实现，既可能被 mcp_sequence 暴露成「align two sequences」，也可能被别的领域 server 以不同措辞暴露。暴露面（怎么呈现给模型）和实现（怎么真正做）解耦了。

这与第二章「identity/working_style 分离」、第四章「artifact/artifact_versions 分离」是同一种设计直觉——把「对外呈现的东西」和「稳定的底层实体」拆开，让两者能各自独立演化。 整个 Claude Science 反复运用这个模式。

7.4 discover-from-disk：约定优于配置
run_server.py 的 discover_servers() 不维护一份「服务器清单」配置文件，而是从磁盘扫描推导——凡是符合命名约定（mcp_ 前缀 + server.py）的包，自动就是一个 server。

这是「约定优于配置」（convention over configuration）的实践：

• 加一个新领域 server：只需在 lib/ 建一个 mcp_newdomain/ 目录、放个 server.py，无需改任何注册表。
• 没有「清单和实际不一致」的漂移风险：因为清单就是磁盘现状，不存在第二份需要同步的真相。
这与第五章 skill 系统的自动发现（skill 靠 metadata 被发现、host.skills.list() 列出磁盘上所有 skill）异曲同工——Claude Science 倾向于让「系统的能力集」从文件系统结构自动涌现，而不是维护一份易腐的中心注册表。

7.5 MCP 只在 repl 里调——回顾第二章的拓扑约束
MCP 架构必须和第二章讲过的 kernel 拓扑一起理解。operon 的 working_style 规定：

MCP calls happen in the `repl` tool — never in `python`/`r` (those kernels
have no MCP surface). Looping over samples or records? Write the loop in a
`repl` cell — `[host.mcp("server", "method", id=x) for x in ids]` is one
`repl` call with N host round-trips inside it…
把这个和本章的 24-server 架构拼起来，就能看清一次真实的 MCP 调用长什么样：

# 在 repl cell 里，一次调用打到某个领域 server 的某个 method：
host.mcp("mcp_structure", "fetch_pdb", id="1ABC")
host.mcp(server, method, **kwargs) 的第一个参数正是 24 个领域 server 之一，第二个是该 server 暴露的工具方法。领域聚合让这个调用的第一个参数是可读的领域名，而不是一个 87 选 1 的扁平方法名。 循环多个数据源调用要写成 repl cell 里的 list comprehension（一次 repl 回合、内部 N 次 host round-trip），再 json.dump 到 ./handoff/ 交给 python kernel——这是第二章「回合经济学 + kernel 拓扑」在 MCP 场景的直接落地。

7.6 「反 confabulate」在数据源层的意义
第二章和第九章反复出现的「compute, don't confabulate」，在 MCP 架构这里有了物理载体。working_style 说：

When you fetch via `host.mcp()`, the result is the source of truth — cite the
identifiers it returns…
bio-tools 的 24 个 server 存在的根本理由就是这句话：模型的训练记忆里「记得」很多基因、通路、accession、临床试验号，但这些记忆可能过时、可能张冠李戴、可能纯属编造。MCP server 提供了权威的实时来源——去 NCBI 查这个 accession、去 PubMed 查这篇文献、去 PDB 取这个结构。取回来的标识符才是真相之源，凭记忆写出来的不是。

所以 MCP 聚合架构不只是「工具很多」的工程问题，它是反幻觉哲学的基础设施：只有当「去查真实数据」比「凭记忆瞎编」更方便时，模型才会真的去查。24 个按领域组织、可在 repl 里一行调用的 server，就是把「查真实数据」的成本压到足够低，让正确行为成为默认路径。

7.7 这一章的可迁移原则
1. 聚合粒度对齐心智分类：几十个工具别拍平成一个巨型面（选择成本 + 上下文成本爆炸），也别散成一堆独立 server（运维 + 复用成本爆炸）。按用户/模型天然会用的维度（这里是科学领域）聚成中等数量的分组。
2. 暴露面与实现分离：server.py（模型可见的工具定义）与 lib/*.py（底层数据源实现）解耦，让同一实现能被多领域复用、各自裁剪呈现。
3. 约定优于配置的发现机制：从磁盘命名约定推导服务器集合，消灭「注册表 vs 实际」的漂移。
4. 工具架构要服务于行为哲学：MCP server 的终极目的不是「功能多」，而是把「获取权威真实数据」的成本压低到成为默认路径——这是反幻觉的物理基础。
收尾：bio-tools 表面上是「一堆生物信息学 API 的封装」，但它的架构选择——24 个领域 server 架在 ~87 模块 lib 之上、从磁盘自动发现、只在 repl 暴露——回答的是一个通用问题：当一个 agent 需要接触几十上百个外部能力时，怎么组织它们才能既不淹没模型、又不拖垮运维、还能沉淀共享逻辑。 答案是「按心智维度中等聚合 + 暴露/实现分离 + 约定发现」。

下一章进入反幻觉哲学的大脑：自省与自知。

第八章 自省与自知：不信任自己的记忆
代表文件：skills/self-awareness/SKILL.md（host.query() 自省 SDK）、
skills/product-self-knowledge/SKILL.md（产品事实核查 skill）
核心命题：一个 agent 要「知道自己」，靠的不是内省式的自我描述，而是
对权威数据源的查询——无论那个数据源是自己的会话数据库，还是官方文档。
二者共享同一条哲学：训练记忆不可信，事实要去查。

8.1 两种「自知」
「自知」在这套系统里有两个截然不同、却同源的面向：

1. self-awareness：知道「我这个会话发生了什么」——用了多少 token、上一个工具调用是什么、写过哪些文件、消息存在哪。答案在 Claude Science 自己的元数据库里。
2. product-self-knowledge：知道「我这个产品的事实」——Claude Code 怎么装、API 怎么用、Claude.ai 的套餐区别。答案在 Anthropic 官方文档里。
两者的共同点极其重要：都不允许「凭记忆回答」。 self-awareness 要你去 host.query() 查数据库，product-self-knowledge 要你去 fetch 官方文档。这正是第二章「compute, don't confabulate」和「能力也要落地、别凭记忆答」的两个专门化身——agent 对「自己」的了解，也必须建立在可查证的来源上，而不是自我叙述。

8.2 self-awareness：把自己的会话当数据库来查
self-awareness 提供的核心接口是：

host.query(sql, params=[], limit=None, df=False) runs read-only SQLite
against Claude Science's own metadata DB. It is only available via the repl
tool. Results are automatically scoped to the current project…
这是一个非常大胆的设计：agent 的整个运行状态——对话、执行日志、产物、成本、审查结论——都在一个可以用只读 SQL 查询的 SQLite 库里。 agent 想知道「这个会话花了多少钱」，不是去「回忆」或「估算」，而是：

SELECT SUM(total_cost) FROM frames
为什么是「只读 SQL」而不是一堆专用 API
系统本可以给每个自省需求配一个专用方法（host.get_token_count()、host.list_my_files()……）。但它选择暴露通用的只读 SQL 面 + 一份 schema 文档。原因：

• 自省需求是开放的、组合的：「上周写的、大于 1MB 的、CSV 类型的产物」这种查询无法预先枚举成 API，但一条 SQL 就能表达。
• schema 即文档即能力：self-awareness 花大篇幅列出 frames / execution_log / artifacts / artifact_versions / verification_checks 等表的每一列。这份 schema 文档本身就是 agent 的「自我认知地图」——它读了这个 skill，就知道自己有哪些可查证的事实维度。
execution_log 表的描述点破了这个设计的灵魂：

This is the ground-truth record of everything you've run.
「你跑过的一切的地面真相记录。」 agent 不需要记得自己跑过什么——它可以去查那份地面真相。记忆会漂移，execution_log 不会。

安全边界：denied tables
自省不是无限的。skill 明确列出被拒绝的表，且理由分类清晰：

- Secrets (encrypted at rest, blocked defense-in-depth): oauth_tokens,
  user_secrets, anthropic_api_keys, cloud_credentials.
- Agent/skill/connector configuration (enumerating attack surface has no
  legitimate raw-SQL use): user_agents, agents, custom_mcp_servers…
两类禁区：

1. 密钥——加密存储，纵深防御再封一层 SQL 访问。想要非密文元数据走 host.credentials.list()。
2. agent/skill/连接器配置——注释给的理由是「enumerating attack surface has no legitimate raw-SQL use」（枚举攻击面没有正当的裸 SQL 用途）。
而且拒绝是按词边界匹配 SQL 任意位置的——连一个恰好等于禁表名的列别名或字符串字面量都会被拒。这是防「用别名绕过」的偏执但正确的做法。

还有一条耐人寻味的自省盲区：

Host identity (hostname, workspace/pod name) is intentionally not exposed
anywhere in this DB… to know where you're running, ask the user or use
list_compute labels.
「你在哪台机器上跑」这个事实被故意不暴露——这是一个刻意设计的「自知盲区」，出于隔离/安全考虑。自知是被精心划定边界的，不是「什么都能知道」。

8.3 self-awareness 里回响的全系统主题
这份 schema 文档像一面镜子，把前面几章讲过的设计从「数据层」再确认了一遍：

• 第四章的 artifact 数据模型——artifacts / artifact_versions / content_snapshots / artifact_dependencies 全在这里，producing_cell_id → execution_log.id 的可追溯链在这里成为可查询的现实。
• 第三章的 reviewer——session_claims（抽取出的可证伪断言）、verification_checks（pass/warn/fail/inconclusive 的判决）都是表。reviewer 的整套 rubric 最终落地成这两张表里的行。第三章讲的是「怎么判」，这里是「判决存在哪」。
• 第二章的 kernel 拓扑——文档反复强调 host.query/host.mcp 只在 repl 工具里、repl 与 python 是共享工作目录的独立进程、跨 kernel 传数据走 ./handoff/*.json。SDK 表格逐行标注了每个 host.* 方法「在哪个工具里可用」。
• 第一/二章的成本意识——frames 表把 input_tokens/output_tokens/cache_read_tokens/total_cost 做成可聚合的列，worked example 甚至教你「server-side 聚合以免行数上限低估」。回合经济学在这里有了度量工具。
self-awareness 因此不只是一个工具 skill，它是整个系统数据模型的权威索引。 读懂它，就读懂了 Claude Science 把「什么当作可查证的一等事实」。

8.4 product-self-knowledge：把「stop and consult」写进 description
product-self-knowledge 的 description 是第五章「主动式 description」的极端样本，值得完整重读：

Stop and consult this skill whenever your response would include specific
facts about Anthropic's products… Any time you would otherwise rely on memory
for Anthropic product details, verify here instead — your training data may
be outdated or wrong.
注意它的措辞强度：「Stop and consult」（停下来查阅）、「your training data may be outdated or wrong」（你的训练数据可能过时或错误）。第五章讲过模型倾向「欠触发」skill，而这个 skill 欠触发的代价特别高——一旦模型凭记忆答了「Claude Code 需要 Node 16」而实际早已变了，就是明明白白的错误信息。所以它的 description 把「推一把」推到极致：直接命令模型「停下来」，并直白告诉模型「别信自己的记忆」。

内容极简，是因为它只做一件事：路由到权威来源
product-self-knowledge 的正文短得惊人——核心就是一张「问题路由表」：

### Claude API or Claude Code questions?
→ Check the docs maps first:
  - Claude API & General: https://docs.claude.com/en/docs_site_map.md
  - Claude Code: …/claude_code_docs_map.md
### Claude.ai questions?
→ Browse the support page: https://support.claude.com
它几乎不包含任何具体产品事实（除了几个稳定的入口 URL）。为什么？因为产品事实（价格、模型名、Node 版本要求）变得太快，写进 skill 就会腐烂。所以这个 skill 的设计哲学是：不缓存事实，只缓存「去哪查事实」的路由。 它的四条 Core Principles 把这点讲明了：

1. Accuracy over guessing - Check official docs when uncertain
2. Distinguish products - Claude.ai, Claude Code, and Claude API are separate
3. Source everything - Always include official documentation URLs
4. Right resource first - Use the correct docs for each product
「Source everything —— 永远附上官方文档 URL」是这里的关键：它不仅要模型去查，还要模型把来源亮给用户，让用户能自己核对。这与 reviewer「读它引用的那几页才能定罪」、operon「引用 MCP 返回的标识符」是同一个「一切可溯源」的原则。

一个反腐烂的设计模式
product-self-knowledge 示范了一个可迁移的模式，专门对付「快速变化的事实」：

当知识会快速过时，不要把知识写进 prompt/skill，把「获取知识的权威路径」写进去。 skill 承诺的不是「我知道答案」，而是「我知道去哪拿到当前正确的答案，并会把来源给你」。

这与 self-awareness 是一枚硬币的两面：

• self-awareness：会话事实 → 查自己的数据库（那是会话真相之源）。
• product-self-knowledge：产品事实 → 查官方文档（那是产品真相之源）。
两者都拒绝「凭训练记忆作答」，都把答案锚定到一个会随时间保持正确的权威来源上。

8.5 为什么「自知 = 查证」是深刻的
一般人以为「自我认知」是一种内省能力——agent 应该「知道」自己是什么、做过什么。这套系统给出了一个更扎实的答案：

对一个 LLM 来说，「内省式的自我认知」恰恰是最不可靠的——因为它就是在生成 token，而生成 token 正是幻觉的温床。真正可靠的自知，是把关于自己的一切问题都转化成对权威来源的查询。

• 「我花了多少 token？」→ 不要估算，SELECT SUM(input_tokens)。
• 「我跑过这个分析吗？」→ 不要回忆，查 execution_log。
• 「我这个产品支持什么？」→ 不要凭训练记忆，去 fetch 官方文档。
• 「我这个领域有哪些工具？」→（第二章）不要凭记忆，search_skills。
把「关于自我的问题」和「关于世界的问题」一视同仁地当作数据问题处理——这是 Claude Science 反幻觉哲学最彻底的推论。它不相信 agent 能「知道」，只相信 agent 能「查」。

8.6 这一章的可迁移原则
1. 自省 = 查询，不是内省：把 agent 的运行状态存进一个可只读查询的结构化库，配一份 schema 文档当「自我认知地图」，让 agent 去查而不是去回忆。
2. 通用只读 SQL 面 > 一堆专用自省 API：自省需求是开放组合的，SQL + schema 文档比预先枚举的方法更能覆盖。
3. 自知也要有安全边界：密钥、攻击面配置、宿主身份该屏蔽的屏蔽，且防别名绕过。自知是被划定边界的，不是无限的。
4. 对付快速过时的事实：缓存路由而非缓存事实。skill 承诺「我知道去哪查当前正确答案 + 把来源给你」，而不是「我记得答案」。
5. 一切事实性问题统一当数据问题：关于自我的、关于产品的、关于领域能力的——全部锚定到会随时间保持正确的权威来源，拒绝凭训练记忆作答。
收尾：self-awareness 和 product-self-knowledge 看起来是两个不相干的工具（一个查数据库、一个查文档），但它们共享 Claude Science 最深的一条信念——不信任模型自己的记忆，包括对它自己的记忆。 一个连「我花了多少 token」都要去查数据库、连「我这个产品怎么装」都要去查官方文档的 agent，才配得上在科研场景被信任。这份「对自己记忆的不信任」，正是下一章要收束的贯穿性主题的核心。

下一章把散落各章的主线收拢：贯穿性主题。

第九章 贯穿性主题：把设计哲学收拢成几条主线
本章不引入新文件，而是把前八章散落的证据收拢成 Claude Science 设计哲学的
几条主脉。如果说前面每一章都在拆一个部件，这一章要回答：
这些部件背后，是不是同一套世界观在反复起作用？ 是的。

9.1 主线一：解释而非命令（Explain, don't command）
这是全系统 prompt 写作最鲜明的旗帜。它在多处以近乎宣言的形式出现，最直白的一次在 skill-creator（第五章）：

Try to explain to the model why things are important in lieu of heavy-handed
musty MUSTs… If you find yourself writing ALWAYS or NEVER in all caps… that's
a yellow flag — reframe and explain the reasoning so that the model
understands why the thing you're asking for is important.
「全大写的 ALWAYS/NEVER 是黄旗。」 这句话解释了为什么整套系统的 prompt 读起来不像规章制度，而像一位资深同事在讲道理。回看证据：

• 第一章：每个配置项都附实测证据（enable_thinking 关掉的 357-reread 故事、excluded_tools 的 41% 数字）。规则不是「就这么定」，是「测过，所以这么定」。
• 第二章：反 emoji 那条没写「NEVER use emoji」，而是给了读者模型（读者在扫 result/artifact/caveat）、论证了危害（视觉噪声）、给了替代（用结构）、留了记忆点（artifact is the hero）。
• 第三章：reviewer rubric 通篇在讲「为什么这算发现、那不算」，而不是罗列禁令。
• 第六章：onboarding 每条对话规则都带「会毁掉什么体验」的理由（重复问候、越问越窄、把权限框成风险）。
为什么「解释」比「命令」有效？ skill-creator 给了答案：「Today's LLMs are smart.」一个理解了「为什么」的模型，能在边界情况自行正确判断；一个只背了禁令的模型，遇到规则没覆盖的新情况就会失灵，或者僵硬地误用规则。解释把判断力交给模型，命令把模型变成查表机器。第五章还补了一条更深的理由——堆砌 MUST 是一种过拟合：规则越硬越细，越只在你想到的那几个例子上管用，越无法泛化到海量真实输入。

可迁移内核：写给 LLM 的指令，目标是让它理解意图，不是让它服从条文。 当你想写 ALWAYS/NEVER 时，停下来问「为什么」，然后把「为什么」写出来。

9.2 主线二：测量驱动（Measurement over intuition）
Claude Science 把「怎么知道一个设计是对的」这个问题，系统性地交给了测量，而不是直觉或权威。

• 第一章：agent 的每个配置项都是一条「调优记录」——它是被一个对照实验（带/不带某设置的 baseline 比较）决定的，并把结果数字留在注释里。配置文件因此同时是实验日志。
• 第五章：skill-creator 把「造 skill」本身变成测量驱动的循环——draft→test→eval→rewrite，每个 case 同时跑「带 skill」和「baseline」两个 subagent 对照，产出 benchmark.json（mean±stddev），description 优化甚至切 60/40 训练/留出集防过拟合。
• 第一章的 bookmarker + 第八章的 verification_checks：连「审查结论」都落成可统计的表行（pass/warn/fail 计数），审查质量本身可被测量。
这条主线的深刻之处在于：它把机器学习的方法论搬进了 prompt/agent 工程。对照组、训练/测试分离、防过拟合、mean±stddev——这些本是训练模型的概念，在这里被用来「训练」prompt 和 agent 配置。系统不假设设计者有好直觉，它假设设计者会测。

可迁移内核：agent 配置和 prompt 应该像模型一样被评估——有 baseline、有 holdout、有量化指标，改动靠数字支持而非「感觉更好」。

9.3 主线三：Compute, don't confabulate（反幻觉是地基，不是补丁）
反幻觉不是这套系统的一个功能，它是贯穿所有部件的地基。把散落各章的证据串起来，能看到一条完整的反幻觉纵深防线：

1. 行为层（第二章）：operon working_style 直接规定「Compute, don't confabulate」——需要数据就取，别硬编看似合理的答案；取回的标识符才是真相之源。连「你支持什么工具」都不许凭记忆答，要 search_skills。
2. 基础设施层（第七章）：bio-tools 的 24 个领域 MCP server 存在的根本理由，就是把「获取权威真实数据」的成本压到足够低，让「去查」成为默认路径而非负担。
3. 自知层（第八章）：连 agent 对自己的认知都不许内省——token 数去查 frames 表，跑过什么去查 execution_log，产品事实去查官方文档。「不信任记忆」被推到了「不信任对自己的记忆」。
4. 审查层（第三章）：reviewer 是这条防线的最后一道——专门抓「声称已检索却追溯不到的引用」（编造引用是它存在的理由），并用非对称举证确保它抓真幻觉而不制造假阳性。
四层环环相扣：行为层让模型倾向于查，基础设施层让查很便宜，自知层堵死「凭记忆自述」这个后门，审查层兜底抓漏网的编造。这不是「加了个反幻觉功能」，这是整个系统围绕「模型的记忆不可信」这一前提重新组织了自己。

可迁移内核：如果你的 agent 用在「说错话有真实代价」的场景，反幻觉必须是架构层的贯穿设计——降低查证成本、堵死凭记忆作答的路径、加事后审查——而不能指望一句「不要幻觉」的 prompt。

9.4 主线四：呈现层与机制层的分离（Users see science, not plumbing）
系统在多个尺度上反复执行同一个分离：让用户/模型看到「结果/意图」，看不到「机制/实现」。

• 第二章 narrate the work not the plumbing：用户看到「派三个子 agent 筛化合物家族」，看不到「host.delegate wait=False」；连「side channel」「background cell」这类 paraphrase 都算犯规。
• 第四章 artifact 收尾克制：用户看到主交付物 + 一句摘要，看不到机器 id（art_abc123）、看不到 UI 已展示的产物清单。
• 第六章「指令不是文案」：用户看到好问题好提议（规则的结果），看不到「三个雄心等级」这类只存在于 prompt 里的措辞（规则本身）。
• 第七章 server/lib 分离：模型看到 24 个领域 server 的工具面，看不到底下 ~87 个实现模块。
• 第二章 identity/working_style、第四章 artifact/version、第八章 schema：反复用「稳定底层实体 + 可独立演化的呈现面」这个结构。
这不是巧合，是一个统一的界面哲学：实现细节的泄漏是不成熟的标志。用户是科学家不是运维；呈现面应该按用户的心智组织，把机制彻底挡在视线外。而系统内部则用「呈现/实现分离」让两者各自独立演化。

可迁移内核：在每一个界面上问「这个词/这个 id/这份清单，是用户需要的科学，还是我的管道？」 管道一律下沉，界面只留科学。

9.5 主线五：边界意识（Every rule knows where it stops）
这套系统最见功力的地方，不是规则多严，而是几乎每条强规则都明确标注了它的例外和终止条件。它不追求「一刀切的干净」,追求「划对每一条线」。

• 第三章是这条主线的巅峰：「非对称举证」是宪法第一条（找到矛盾才定罪），但它给「编造引用」开了唯一的口子（找不到也定罪）——然后又给这个口子划了四圈边界（自引用不算、被截断算 warn、被带进窗口不算、对冲措辞不能免罪）。domain-recall 豁免也带着精确的终止条件（来源一进会话，豁免立即失效）。
• 第二章：plan 要克制用，但「范围变大再补」；先读文档再写代码，但用「一次探查 vs 三次重试」的成本论证界定何时值得。
• 第八章：自知很强大，但密钥、攻击面配置、宿主身份是明确的盲区。
• 第五章：description 要 pushy，但也警告别过拟合到测试样例。
为什么边界意识如此重要？ 因为一个没有例外的强规则，要么太松（放过真问题），要么太紧（制造假阳性/摩擦）。真实世界充满边界情况，一条「知道自己在哪里停」的规则，才能在「抓住真问题」和「不误伤」这两个对立目标之间站稳。第三章的收尾把这一点提炼成了元技能:「怎么在两个对立的失败模式之间划一条可执行的线」。

可迁移内核：写完一条强规则，立刻问「它的例外是什么？它什么时候不适用？」 把答案也写进去。没有边界的规则不是严谨，是脆弱。

9.6 主线六：成本意识贯穿始终（Awareness of what each turn/token costs）
系统对「资源」有一种近乎本能的敏感，而且它总是把「省资源」转化成可执行的判据，而非空泛的「要高效」。

• 回合经济学（第二章）：「每个 python call 是一次完整 LLM round-trip」——所以把取数→解析→检查→计算塞进一个 cell，sanity check 用 inline assert，只在「下一行依赖你没见过的输出」时才断 cell。这把「少发 cell」变成了有清晰判据的规则。
• 上下文经济学（第五章 + 第七章）：skill 的三级渐进披露、MCP 的领域聚合，都是在回答「怎么挂载大量能力而不让描述挤爆常驻上下文」。答案都是「按此刻是否需要分层付费」。
• 探查摊销（第二章）：「一次探查回合比 2-3 次重试回合便宜」——用回合成本给「先读文档」这个习惯定价。
• 检查点规则（第四章）：中间产物只在「重新生成很贵」时存——用「再生成成本」当保存与否的判据。
• 可度量（第八章）：frames 表把 token/cost 做成可聚合列，成本意识不只是训诫，是可查询的现实。
可迁移内核：把「高效」翻译成具体判据——每次操作的真实成本是什么（一个回合？一段常驻上下文？一次重算？），据此给出「什么时候该合并/该分层/该缓存」的可执行规则。

9.7 六条主线其实是一条
回头看这六条主线，它们并非并列，而是从一个共同的世界观里长出来的。这个世界观可以用前言的那句话概括：

把 agent 当成需要被校准的科学仪器，而不是需要被命令的下属。

• 仪器要校准，所以有「测量驱动」（主线二）——你不命令仪器,你标定它。
• 校准要有依据，所以有「解释而非命令」（主线一）——每个设置附测量理由，仪器操作手册讲原理不下禁令。
• 仪器的读数必须可信，所以有「反幻觉地基」（主线三）和「自知即查证」——一台会编造读数的仪器毫无价值。
• 仪器要有明确的量程和误差边界，所以有「边界意识」（主线五）——一条不知道自己何时失效的规则，就像一个不标量程的仪表。
• 仪器的输出要面向使用者，所以有「呈现/机制分离」（主线四）——用户读的是测量结果，不是仪器内部线路。
• 仪器要经济地运行，所以有「成本意识」（主线六）。
这就是 Claude Science 的设计哲学的最内核：它系统地拒绝了「把 LLM 当成一个你下命令、它服从的智能下属」这个隐喻，转而把 LLM 当成一台强大但需要被严格标定、其读数默认存疑、其量程必须被划清的科学仪器。前八章拆的每一个部件——配置、身份分离、审查 rubric、artifact、skill、onboarding、MCP、自省——都是这台仪器的一个校准螺丝。

9.8 全书可迁移原则总表
把九章的可迁移原则汇成一张随查表：

#
原则
出处
1
每个配置项附实测证据，配置文件即实验日志
第一章
2
prompt 切成「用户可替换的身份层」+「平台继承的工作规范层」
第二章
3
用能力裁剪把 agent 焊死在它该做的事上
第二/三/六章
4
审查用非对称举证（找到矛盾才定罪）+ 按证据位置加权
第三章
5
给强规则划清例外和终止条件
第三章（全书）
6
把每次真实误判固化成一条带数据的具体规则
第一/三章
7
交付单位是可引用、可追溯、有版本的制品，不是消息
第四章
8
引用建立在稳定 id 上，不在会碰撞的名字上
第四章
9
能力用三级渐进披露，按「此刻是否需要」分层付上下文
第五章
10
description 是触发分类器的输入，要主动列触发信号对抗欠触发
第五/八章
11
kernel/库：机制固化、美学参数化
第五章
12
造能力的过程本身要测量驱动（对照/holdout/防过拟合）
第五章
13
对话型 agent：分离「理解」与「选活」，对抗追问引力
第六章
14
权限请求锚定到用户已想要的价值（赋能而非同意闸门）
第六章
15
指令不是文案：禁止 prompt 专属措辞泄漏到输出
第六章
16
工具聚合粒度对齐心智分类，暴露面与实现分离
第七章
17
约定优于配置：从磁盘结构自动发现能力集
第五/七章
18
自省 = 查询结构化库，不是内省
第八章
19
对付快速过时的事实：缓存路由而非缓存事实
第八章
20
一切事实性问题（含关于自我的）统一当数据问题、锚定权威来源
第八章（全书）
21
让用户看到科学、看不到管道；实现细节一律下沉
第二/四/六/七章
22
把「高效」翻译成每操作成本的可执行判据
第二/四/五章
23
解释而非命令：写给聪明模型的指令要讲理，ALWAYS/NEVER 是黄旗
第五章（全书）
全书收尾：Claude Science 的设计哲学，剥到最里层，是一次对「人该如何与强大但不可尽信的智能协作」的严肃回答。它没有把这个智能神化（否则不会到处设审查和查证），也没有把它当廉价工具（否则不会花这么大力气解释每条规则的道理）。它选择的隐喻——可校准的科学仪器——恰好落在两者之间：足够尊重它的能力，因而给它讲道理、给它自生长的 skill 系统、给它开放的 SQL 自省面；又足够清醒地对待它的缺陷，因而给每个读数配溯源、给每条规则划量程、给整个系统铺四层反幻觉纵深。这份「既尊重又清醒」的态度，才是所有具体设计背后真正值得学习的东西。

 

Anthropic just released a brand-new Claude Science app for Mac - 9to5Mac