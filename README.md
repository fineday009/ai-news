# ai-news

**English** | [中文](README.zh-CN.md)

Curated digests of GitHub's most valuable open-source projects — AI-focused but not AI-only — bilingual (English/Chinese), auto-generated daily by a Claude Code skill.

## Reports

All four views are regenerated with fresh data every day at 11:00 (Asia/Shanghai):

| View | Path | Behavior |
|---|---|---|
| 📅 Daily | [`reports/daily/`](reports/daily/) | New file every day |
| 📆 Weekly | [`reports/weekly/`](reports/weekly/) | Current-week snapshot, refreshed daily |
| 🗓️ Monthly | [`reports/monthly/`](reports/monthly/) | Current-month snapshot, refreshed daily |
| 🏆 Yearly | [`reports/yearly/`](reports/yearly/) | Current-year snapshot, refreshed daily |

Each report features 10 hand-picked projects with star momentum, a one-line intro, and why it matters.

The daily report also includes a **🎙️ What Builders Are Saying** section: curated takes from top AI builders' tweets, podcast takeaways, and blog picks.

## The Skill

`.claude/skills/github-digest/` — fetches ~50 candidates from GitHub Trending + the Search API, then curates by "AI-first but not AI-only, substance over hype, momentum and novelty".

Manual use in Claude Code: `/github-digest` (optionally `weekly` / `monthly` / `yearly` / `all`).

## Credits

The "What Builders Are Saying" section consumes the public central feed (builder tweets / podcast transcripts / blogs) and curation rules of **[follow-builders](https://github.com/zarazhangrui/follow-builders)** by [@zarazhangrui](https://github.com/zarazhangrui) (MIT License). The curated source list is maintained upstream by the original author.
