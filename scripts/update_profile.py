import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path


OWNER = os.environ.get("GITHUB_OWNER") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "suzike"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
START = "<!-- PROFILE-AUTO:START -->"
END = "<!-- PROFILE-AUTO:END -->"

LANG_COLORS = {
    "Python": "3776AB",
    "JavaScript": "F7DF1E",
    "TypeScript": "3178C6",
    "MATLAB": "E16737",
    "Jupyter Notebook": "DA5B0B",
    "HTML": "E34F26",
    "CSS": "1572B6",
    "Shell": "4EAA25",
    "PowerShell": "5391FE",
}


def request_json(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "suzike-profile-updater",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def get_all_repos():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{OWNER}/repos?per_page=100&page={page}&sort=created&direction=desc"
        batch = request_json(url)
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos


def badge(label, value, color="0F172A", label_color="E0F2FE"):
    label_q = urllib.parse.quote(str(label).replace("-", "--"))
    value_q = urllib.parse.quote(str(value).replace("-", "--"))
    return (
        f'<img src="https://img.shields.io/badge/{label_q}-{value_q}-{color}'
        f'?style=flat-square&labelColor={label_color}" alt="{label}: {value}" />'
    )


def fmt_date(value):
    if not value:
        return "-"
    return value[:10]


def repo_link(repo):
    return f'<a href="{repo["html_url"]}">{repo["name"]}</a>'


def generated_section(repos):
    public_repos = [r for r in repos if not r.get("archived")]
    total_stars = sum(r.get("stargazers_count", 0) for r in public_repos)
    total_forks = sum(r.get("forks_count", 0) for r in public_repos)
    total_watchers = sum(r.get("watchers_count", 0) for r in public_repos)
    original_count = sum(1 for r in public_repos if not r.get("fork"))
    fork_count = sum(1 for r in public_repos if r.get("fork"))

    lang_counter = Counter(r.get("language") or "Docs" for r in public_repos)
    lang_badges = []
    for lang, count in lang_counter.most_common():
        color = LANG_COLORS.get(lang, "0369A1")
        label_color = "E0F2FE" if color != "F7DF1E" else "0F172A"
        lang_badges.append(badge(lang, count, color, label_color))

    metric_badges = [
        badge("Public Repos", len(public_repos), "0369A1"),
        badge("Original", original_count, "075985"),
        badge("Forks", fork_count, "475569"),
        badge("Stars", total_stars, "0F172A"),
        badge("Watchers", total_watchers, "1E3A8A"),
        badge("Forked By Others", total_forks, "334155"),
    ]

    rows = []
    for repo in sorted(public_repos, key=lambda r: r.get("created_at") or "", reverse=True):
        language = repo.get("language") or "Docs"
        stars = repo.get("stargazers_count", 0)
        watchers = repo.get("watchers_count", 0)
        forks = repo.get("forks_count", 0)
        created = fmt_date(repo.get("created_at"))
        pushed = fmt_date(repo.get("pushed_at") or repo.get("updated_at"))
        kind = "Fork" if repo.get("fork") else "Original"
        desc = (repo.get("description") or "").strip() or "-"
        rows.append(
            "<tr>"
            f"<td><code>{created}</code></td>"
            f"<td>{repo_link(repo)}<br /><sub>{desc}</sub></td>"
            f"<td><code>{language}</code><br /><sub>{kind}</sub></td>"
            f"<td><code>Stars {stars}</code><br /><code>Watchers {watchers}</code><br /><code>Forks {forks}</code></td>"
            f"<td><code>{pushed}</code></td>"
            "</tr>"
        )

    generated_at = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return "\n".join(
        [
            '<div align="center">',
            "  " + "\n  ".join(metric_badges),
            "</div>",
            "",
            "<br />",
            "",
            "<div align=\"center\">",
            "  " + "\n  ".join(lang_badges),
            "</div>",
            "",
            "<br />",
            "",
            "<table>",
            "  <tr>",
            "    <th>发布时间</th>",
            "    <th>仓库</th>",
            "    <th>主语言</th>",
            "    <th>动态信号</th>",
            "    <th>最近更新</th>",
            "  </tr>",
            "\n".join(rows),
            "</table>",
            "",
            f"<sub>自动更新: {generated_at} · 数据来自 GitHub REST API · workflow 每 6 小时运行一次，也支持手动触发。</sub>",
        ]
    )


def replace_section(readme, section):
    if START not in readme or END not in readme:
        raise RuntimeError("README markers not found")
    before, rest = readme.split(START, 1)
    _, after = rest.split(END, 1)
    return before + START + "\n" + section + "\n" + END + after


def main():
    repos = get_all_repos()
    current = README.read_text(encoding="utf-8")
    updated = replace_section(current, generated_section(repos))
    if current != updated:
        README.write_text(updated, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"profile update failed: {exc}", file=sys.stderr)
        raise
