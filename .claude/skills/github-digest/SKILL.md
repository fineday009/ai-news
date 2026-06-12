---
name: github-digest
description: 抓取并精选每日/每周/每月/每年 GitHub 最有价值的开源项目（以 AI 为主、不限于 AI），生成 10 个项目的中文榜单报告。Use when the user asks for a GitHub daily/weekly/monthly/yearly digest, trending repos, or invokes /github-digest. Pass "weekly"/"monthly"/"yearly" for those editions; defaults to daily.
---

# GitHub 每日/每周/每月/每年精选

生成一份 10 个项目的中文精选报告，保存到项目的 `reports/` 目录。

## 步骤

### 1. 确定周期

参数含 `weekly`（周）→ weekly，`monthly`（月）→ monthly，`yearly`（年）→ yearly，`all`（全部）→ 依次生成四个周期各一份报告，否则 daily。

### 2. 抓取候选数据

```bash
python3 "<本 skill 目录>/scripts/fetch_repos.py" <daily|weekly|monthly|yearly>
```

输出 JSON：`trending`（GitHub Trending 榜，含本期新增 star 数）+ `new_hot`（近期新建的高星项目，Search API）。合计约 50 个候选。注意：GitHub Trending 没有年榜，yearly 的 `trending` 为空，候选全部来自 Search API（过去一年新建的高星项目）；年榜如需补充"老项目今年爆发"类候选，可另读 `reports/monthly/` 已有的月报。若脚本失败（GitHub 改版或限流），用 WebFetch 抓 `https://github.com/trending?since=<period>` 作为后备。

### 3. 排重

仅 daily 模式排重：读取 `reports/daily/` 最近 7 份报告（如存在），已上榜项目不再入选，除非有重大新动态（如发布大版本）。weekly/monthly/yearly 是阶段总结，不排重，可与更短周期的榜单重复。

### 4. 精选 10 个

从候选中选出**恰好 10 个**，按价值排序。标准：

- **AI 优先但不唯一**：AI 项目约占 6–8 个，留 2–4 个名额给其他领域真正出色的项目（基础设施、开发工具、安全等）
- **实质 > 热度**：优先真正的工具/框架/模型/产品；降权 awesome 清单、教程合集、面试题库这类靠转发涨星的仓库
- **动量**：本期新增 star 数、新项目的涨星速度
- **新意**：解决了什么以前没解决好的问题；同类项目中是否有差异化

候选信息不足以判断时（描述为空或含糊），用 WebFetch 抓该仓库主页补充了解，最多查 3–5 个，不要逐一全查。

### 5. Builders 动态（仅 daily）

日报在 10 个项目之后追加一节「🎙️ Builders 动态 / What Builders Are Saying」。内容与 remix 规则均来自 [follow-builders](https://github.com/zarazhangrui/follow-builders)（作者 zarazhangrui，MIT 协议）的公共 feed，无需 API key：

```bash
BASE=https://raw.githubusercontent.com/zarazhangrui/follow-builders/main
curl -s $BASE/feed-x.json          # builders 推文
curl -s $BASE/feed-podcasts.json   # 播客（含全文 transcript）
curl -s $BASE/feed-blogs.json      # 博客
curl -s $BASE/prompts/digest-intro.md $BASE/prompts/summarize-tweets.md $BASE/prompts/summarize-podcast.md   # 官方 remix prompts
```

remix 时优先遵循上面拉到的官方 prompts（整体框架、推文/播客的总结口吻）；与本 skill 冲突的地方（双语格式、放进 Markdown 报告而非聊天投递）以本 skill 为准。

- **推文**（feed-x.json）：从 builders 近期推文中挑 5–8 条最有信息量的观点/发布，每条 1–2 句概括；身份用 `bio` 字段推断（没有就只写名字），**每条必须附原推 url**
- **播客**（feed-podcasts.json）：至多 1 期，含全文 transcript；如有则总结 3–5 个要点，附节目 url（用 JSON 里的 name/title/url，不要从 transcript 里猜）
- **博客**（feed-blogs.json）：挑 1–3 篇值得读的，一句话点评 + url
- 铁律：只用 feed 里的内容，**绝不编造**；没有 url 的内容不写；feed 拉取失败或为空则整节省略，不要报错
- 注意 feed-podcasts.json 可能很大（含 transcript），建议先用 python3/jq 提取字段再读
- 同样中英双语、中英之间隔空行；周/月/年榜不含此节
- **出处声明（必须）**：本节末尾固定加一行：
  `> 本节内容与策展规则来自开源项目 [follow-builders](https://github.com/zarazhangrui/follow-builders)（作者 [@zarazhangrui](https://github.com/zarazhangrui)，MIT License）。Content and curation rules from the open-source project follow-builders by @zarazhangrui (MIT License).`

### 6. 生成报告

按周期写入对应文件（目录不存在则创建）：

| 周期 | 路径 | 日期命令 |
|---|---|---|
| daily | `reports/daily/YYYY-MM-DD.md` | `date +%F` |
| weekly | `reports/weekly/YYYY-Www.md` | `date +%G-W%V` |
| monthly | `reports/monthly/YYYY-MM.md` | `date +%Y-%m` |
| yearly | `reports/yearly/YYYY.md` | `date +%Y` |

daily 每天产生新文件；weekly/monthly/yearly 是**当期快照**——同一周期内重复运行时用最新数据整体覆盖刷新该文件。

格式：

报告为**中英双语**：每段先中文、后英文。项目原始描述是英文的，英文部分保留原文（可微调）；原始描述是中文的，翻译成英文。点评（为什么值得关注）中英文内容对应。注意：中英文之间必须隔一个空行（blockquote 里用单独一行 `>`），否则 GitHub 渲染时两种语言会挤在同一行。

```markdown
# GitHub 每日精选 · YYYY-MM-DD
# GitHub Daily Digest · YYYY-MM-DD

> 一句话概括今日趋势（如：本地 Agent 工具持续爆发，xx 领域出现黑马）
>
> One-line English summary of today's trend.

## 1. owner/repo

⭐ 33.6k（今日 +2,430）· Swift · [链接](https://github.com/owner/repo)

**是什么**：一句话中文简介。

**What it is**: Original English description (or English translation if the source is Chinese).

**为什么值得关注**：2–3 句，讲清它解决的问题、差异化、适合谁用。

**Why it matters**: English version of the same commentary.

---
（共 10 个，按价值排序）

## 🎙️ Builders 动态 / What Builders Are Saying
（仅日报；内容与规则见第 5 节：推文精选 → 播客要点 → 博客推荐，每条附 url）
```

其他周期标题改为"每周/每月/年度精选"，star 增量标注"本周/本月"；yearly 没有增量数据，标注总 star 数和创建时间即可。

### 7. 汇报

最后在对话中给用户一份精简版（每个项目一行：名字 + 一句话 + star 增量），并附报告文件路径。
