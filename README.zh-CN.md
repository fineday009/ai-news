# ai-news

[English](README.md) | **中文**

GitHub 最有价值开源项目精选（以 AI 为主、不限于 AI），中英双语，由 Claude Code skill 每日自动生成。

## 报告

每天 11:00（Asia/Shanghai）用最新数据全量更新四个视图：

| 视图 | 路径 | 更新方式 |
|---|---|---|
| 📅 日榜 | [`reports/daily/`](reports/daily/) | 每天新增一份 |
| 📆 周榜 | [`reports/weekly/`](reports/weekly/) | 当周快照，每天刷新 |
| 🗓️ 月榜 | [`reports/monthly/`](reports/monthly/) | 当月快照，每天刷新 |
| 🏆 年榜 | [`reports/yearly/`](reports/yearly/) | 当年快照，每天刷新 |

每份报告精选 10 个项目，附 star 动量、一句话简介和推荐理由。

日报额外包含「**🎙️ Builders 动态**」一节：AI builders 的推文观点、播客要点与博客精选。

## Skill

`.claude/skills/github-digest/` — 抓取 GitHub Trending + Search API 候选（约 50 个），按"AI 优先、实质优先、看动量和新意"的标准精选。

手动使用：在 Claude Code 中运行 `/github-digest`（可加 `weekly` / `monthly` / `yearly` / `all`）。

## 鸣谢

「Builders 动态」的内容数据（builders 推文 / 播客转录 / 博客 feed）与策展规则来自开源项目 **[follow-builders](https://github.com/zarazhangrui/follow-builders)**（作者 [@zarazhangrui](https://github.com/zarazhangrui)，MIT License）——本仓库直接消费其公开中央 feed，源列表由原作者持续维护更新。
