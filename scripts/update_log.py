"""Rewrite the self-updating log in README.md between the log markers.

Reads my public repos (GitHub API), NeetCode submissions and Boot.dev stats.
Usage: GITHUB_TOKEN=... python scripts/update_log.py
"""
import datetime as dt
import json
import os
import re
import urllib.request

USER = "ASR222"
BOOTDEV = "unlawfulform24"
SKIP = {"ASR222", "bootdev-progress", "neetcode-submissions"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")


def get(url):
    headers = {"User-Agent": USER, "Accept": "application/vnd.github+json"}
    if "api.github.com" in url and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        body = json.load(r)
    return body["data"] if "api.boot.dev" in url else body


def day(iso):
    d = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return f"{d:%b} {d.day}"


def item(title, url, note):
    return f'<a href="{url}">{title}</a><br/><sub>{note}</sub>'


def recently_pushed(n=4):
    repos = get(f"https://api.github.com/users/{USER}/repos?sort=pushed&per_page=30")
    out = []
    for r in repos:
        if r["fork"] or r["name"] in SKIP:
            continue
        commits = get(f"https://api.github.com/repos/{r['full_name']}/commits?per_page=1&author={USER}")
        if not commits:
            continue
        c = commits[0]
        msg = c["commit"]["message"].splitlines()[0]
        msg = msg if len(msg) <= 44 else msg[:43].rstrip() + "…"
        out.append(item(r["name"], c["html_url"], f"{msg} · {day(c['commit']['author']['date'])}"))
        if len(out) == n:
            break
    return out


def practising(n=3):
    out = []
    p = get(f"https://api.boot.dev/v1/users/public/{BOOTDEV}")
    s = get(f"https://api.boot.dev/v1/users/public/{BOOTDEV}/stats")
    out.append(item(f"Boot.dev: level {p['level']}, {s['lessonsCompleted']} lessons",
                    "https://github.com/ASR222/bootdev-progress", f"{p['xp']:,} XP"))
    seen = set()
    for c in get(f"https://api.github.com/repos/{USER}/neetcode-submissions/commits?per_page=40"):
        m = re.match(r"Add: (.+?) - submission", c["commit"]["message"])
        if not m or m.group(1) in seen:
            continue
        seen.add(m.group(1))
        name = m.group(1).replace("-", " ").capitalize()
        name = re.sub(r"\b(sql|api|bfs|dfs|lru)\b", lambda w: w.group(1).upper(), name, flags=re.I)
        out.append(item(f"NeetCode: {name}", c["html_url"], day(c["commit"]["author"]["date"])))
        if len(seen) == n:
            break
    return out


LIVE = [
    item("CortexAI", "https://cortex-gateway-720170616128.asia-south1.run.app/", "Multi-agent assistant · Cloud Run"),
    item("HazeBusters", "https://main.dxwuap9t49si3.amplifyapp.com", "Air quality where no monitor is · AWS"),
]


def column(title, items):
    return f'<td valign="top" width="33%">\n\n<b>{title}</b>\n\n' + "\n\n".join(items) + "\n\n</td>"


def main():
    table = (
        "<table><tr>\n"
        + column("Recently pushed", recently_pushed()) + "\n"
        + column("Practising", practising()) + "\n"
        + column("Live now", LIVE) + "\n"
        + "</tr></table>"
    )
    with open(README, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"(<!-- log:start -->).*?(<!-- log:end -->)", lambda m: f"{m.group(1)}\n{table}\n{m.group(2)}",
                  text, flags=re.S)
    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(table)


if __name__ == "__main__":
    main()
