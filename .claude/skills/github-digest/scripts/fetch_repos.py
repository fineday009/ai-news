#!/usr/bin/env python3
"""Fetch candidate GitHub repos for the daily/weekly digest.

Usage: python3 fetch_repos.py [daily|weekly|monthly|yearly]

Note: GitHub Trending has no yearly view, so "yearly" relies on the
Search API only (top repos created in the past year).

Sources:
  1. GitHub Trending page (scraped HTML, no API key needed)
  2. GitHub Search API: recently created repos with high star counts
     (set GITHUB_TOKEN env var to raise rate limits; optional)

Prints JSON to stdout:
  {"period": "...", "trending": [...], "new_hot": [...]}
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

UA = {"User-Agent": "Mozilla/5.0 (compatible; github-digest-skill)"}


def http_get(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def strip_tags(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def fetch_trending(since):
    html = http_get(f"https://github.com/trending?since={since}")
    repos = []
    for block in html.split("<article")[1:]:
        m = re.search(r'<h2[^>]*>\s*<a[^>]*href="/([^"/]+/[^"/]+)"', block, re.S)
        if not m:
            continue
        name = m.group(1)
        desc_m = re.search(
            r'<p[^>]*class="[^"]*col-9[^"]*"[^>]*>(.*?)</p>', block, re.S
        )
        lang_m = re.search(r'itemprop="programmingLanguage">([^<]+)<', block)
        stars_m = re.search(
            r'href="/%s/stargazers"[^>]*>(.*?)</a>' % re.escape(name), block, re.S
        )
        gained_m = re.search(
            r"([\d,]+)\s+stars\s+(?:today|this\s+(?:week|month))", block
        )
        repos.append(
            {
                "repo": name,
                "url": f"https://github.com/{name}",
                "description": strip_tags(desc_m.group(1)) if desc_m else "",
                "language": lang_m.group(1).strip() if lang_m else None,
                "stars": strip_tags(stars_m.group(1)) if stars_m else None,
                "stars_gained_this_period": gained_m.group(1) if gained_m else None,
            }
        )
    return repos


def fetch_new_hot(days, min_stars):
    since = (date.today() - timedelta(days=days)).isoformat()
    q = urllib.parse.quote(f"created:>{since} stars:>{min_stars}")
    url = (
        "https://api.github.com/search/repositories"
        f"?q={q}&sort=stars&order=desc&per_page=30"
    )
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.loads(http_get(url, headers))
    return [
        {
            "repo": it["full_name"],
            "url": it["html_url"],
            "description": it.get("description") or "",
            "language": it.get("language"),
            "stars": it["stargazers_count"],
            "created_at": it["created_at"][:10],
            "topics": it.get("topics", [])[:8],
        }
        for it in data.get("items", [])
    ]


# period -> (search window in days, min stars). Trending covers the rest.
SEARCH_PARAMS = {
    "daily": (14, 300),
    "weekly": (30, 500),
    "monthly": (90, 1000),
    "yearly": (365, 3000),
}


def main():
    period = sys.argv[1] if len(sys.argv) > 1 else "daily"
    if period not in SEARCH_PARAMS:
        sys.exit("usage: fetch_repos.py [daily|weekly|monthly|yearly]")

    # GitHub Trending has no yearly view
    trending = [] if period == "yearly" else fetch_trending(period)
    days, min_stars = SEARCH_PARAMS[period]
    new_hot = fetch_new_hot(days=days, min_stars=min_stars)

    seen = {r["repo"].lower() for r in trending}
    new_hot = [r for r in new_hot if r["repo"].lower() not in seen]

    json.dump(
        {"period": period, "date": date.today().isoformat(),
         "trending": trending, "new_hot": new_hot},
        sys.stdout, ensure_ascii=False, indent=1,
    )


if __name__ == "__main__":
    main()
