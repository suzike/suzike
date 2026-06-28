import datetime as dt
import html
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

LANG_ICONS = {
    "Python": "🐍",
    "JavaScript": "🟨",
    "TypeScript": "🔷",
    "MATLAB": "📐",
    "Jupyter Notebook": "📓",
    "HTML": "🌐",
    "CSS": "🎨",
    "Shell": "🐚",
    "PowerShell": "⚡",
    "Docs": "📚",
}

TRACK_RULES = [
    ("Profile / Ops", "🪪", ("profile", "readme", OWNER.lower())),
    ("MBD / Simulink", "📐", ("matlab", "simulink", "mbd", "model")),
    ("Thermal Agent", "🌡️", ("thermal", "comfort", "vehicle", "air", "agent", "热舒适", "热管理", "空调")),
    ("AI Training Platform", "🧠", ("train", "platform", "算法", "训练", "部署")),
    ("Diagram Workflow", "🧩", ("draw", "diagram", "draw.io", "图形")),
    ("Signal Dashboard", "📡", ("wechat", "radar", "signal", "情报", "聊天", "看板")),
    ("Knowledge Base", "📚", ("embed", "summary", "knowledge", "resource", "知识", "资源")),
]


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


def badge(label, value, color="0F172A", label_color="0F172A"):
    label_q = urllib.parse.quote(str(label).replace("-", "--"))
    value_q = urllib.parse.quote(str(value).replace("-", "--"))
    return (
        f'<img src="https://img.shields.io/badge/{label_q}-{value_q}-{color}'
        f'?style=flat-square&labelColor={label_color}" alt="{label}: {value}" />'
    )


def parse_github_date(value):
    if not value:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def fmt_date(value):
    if not value:
        return "-"
    return value[:10]


def repo_link(repo):
    return f'<a href="{repo["html_url"]}">{html.escape(repo["name"])}</a>'


def repo_track(repo):
    text = f'{repo.get("name", "")} {repo.get("description") or ""}'.lower()
    for label, icon, keywords in TRACK_RULES:
        if any(keyword.lower() in text for keyword in keywords):
            return label, icon
    return "Engineering Lab", "🧪"


def active_count(repos, days, now):
    count = 0
    for repo in repos:
        pushed = parse_github_date(repo.get("pushed_at") or repo.get("updated_at"))
        if pushed and (now - pushed).days <= days:
            count += 1
    return count


def repo_signal_score(repo, now):
    stars = repo.get("stargazers_count", 0)
    watchers = repo.get("watchers_count", 0)
    forks = repo.get("forks_count", 0)
    pushed = parse_github_date(repo.get("pushed_at") or repo.get("updated_at"))
    created = parse_github_date(repo.get("created_at"))

    days_since_push = (now - pushed).days if pushed else 9999
    if days_since_push <= 14:
        freshness = 24
    elif days_since_push <= 30:
        freshness = 18
    elif days_since_push <= 90:
        freshness = 12
    elif days_since_push <= 365:
        freshness = 8
    else:
        freshness = 3

    adoption = min(28, stars * 4 + watchers * 2 + forks * 5)
    originality = 18 if not repo.get("fork") else 6
    description = 8 if (repo.get("description") or "").strip() else 0
    language = 6 if repo.get("language") else 3
    newness = 8 if created and (now - created).days <= 120 else 0

    return min(100, adoption + freshness + originality + description + language + newness)


def score_color(score):
    if score >= 80:
        return "0F766E"
    if score >= 65:
        return "0369A1"
    if score >= 50:
        return "B45309"
    return "475569"


def score_bar(score):
    filled = max(1, min(8, round(score / 12.5)))
    return "▰" * filled + "▱" * (8 - filled)


def generated_section(repos):
    public_repos = [r for r in repos if not r.get("archived")]
    total_stars = sum(r.get("stargazers_count", 0) for r in public_repos)
    total_forks = sum(r.get("forks_count", 0) for r in public_repos)
    original_count = sum(1 for r in public_repos if not r.get("fork"))
    fork_count = sum(1 for r in public_repos if r.get("fork"))
    now = dt.datetime.now(dt.UTC)
    active_30 = active_count(public_repos, 30, now)
    active_90 = active_count(public_repos, 90, now)
    active_365 = active_count(public_repos, 365, now)
    track_counter = Counter(repo_track(repo)[0] for repo in public_repos)
    top_track = track_counter.most_common(1)[0][0] if track_counter else "Engineering Lab"
    score_values = [repo_signal_score(repo, now) for repo in public_repos]
    average_score = round(sum(score_values) / len(score_values)) if score_values else 0

    lang_counter = Counter(r.get("language") or "Docs" for r in public_repos)
    lang_items = []
    for lang, count in lang_counter.most_common():
        lang_items.append(f"{LANG_ICONS.get(lang, '🧰')} {html.escape(lang)} <b>{count}</b>")

    signal_summary = " · ".join(
        [
            f"Repos <b>{len(public_repos)}</b>",
            f"Original <b>{original_count}</b>",
            f"Fork <b>{fork_count}</b>",
            f"Active 90d <b>{active_90}</b>",
            f"Stars <b>{total_stars}</b>",
            f"Forks <b>{total_forks}</b>",
        ]
    )

    rows = []
    ranked_repos = sorted(
        public_repos,
        key=lambda r: (repo_signal_score(r, now), r.get("pushed_at") or r.get("updated_at") or ""),
        reverse=True,
    )
    for repo in ranked_repos:
        language = repo.get("language") or "Docs"
        stars = repo.get("stargazers_count", 0)
        watchers = repo.get("watchers_count", 0)
        forks = repo.get("forks_count", 0)
        created = fmt_date(repo.get("created_at"))
        pushed = fmt_date(repo.get("pushed_at") or repo.get("updated_at"))
        kind = "Fork" if repo.get("fork") else "Original"
        desc = (repo.get("description") or "").strip() or "-"
        desc = html.escape(desc)
        language = html.escape(language)
        kind = html.escape(kind)
        track, track_icon = repo_track(repo)
        score = repo_signal_score(repo, now)
        rows.append(
            "<tr>"
            f"<td align=\"center\">{badge('Signal', score, score_color(score))}<br /><sub>{score_bar(score)}</sub></td>"
            f"<td>{repo_link(repo)}<br /><sub>{desc}</sub></td>"
            f"<td>{track_icon} {html.escape(track)}<br /><sub>{language} · {kind}</sub></td>"
            f"<td>⭐ {stars} · 👁️ {watchers} · 🍴 {forks}<br /><sub>created {created}</sub></td>"
            f"<td>{pushed}</td>"
            "</tr>"
        )

    generated_at = now.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return "\n".join(
        [
            "<table>",
            "  <tr>",
            "    <td colspan=\"4\"><b>📡 Signal Console</b><br />"
            f"<sub>Signal Model v2 · {signal_summary}</sub></td>",
            "  </tr>",
            "  <tr>",
            "    <td width=\"25%\"><b>🧭 Portfolio</b><br />"
            f"<code>{original_count} original</code> / <code>{fork_count} fork</code><br />"
            "<sub>Profile is original-first, forks are reference assets.</sub></td>",
            "    <td width=\"25%\"><b>⚡ Momentum</b><br />"
            f"<code>{active_30}</code> in 30d · <code>{active_90}</code> in 90d<br />"
            f"<sub>{active_365} repos touched within 365 days.</sub></td>",
            "    <td width=\"25%\"><b>🧪 Engineering</b><br />"
            f"<code>{html.escape(top_track)}</code><br />"
            "<sub>Dominant public engineering track.</sub></td>",
            "    <td width=\"25%\"><b>🌐 Reach</b><br />"
            f"<code>{average_score}</code> avg signal<br />"
            "<sub>Stars, watchers, forks and freshness.</sub></td>",
            "  </tr>",
            "  <tr>",
            "    <td colspan=\"4\"><b>Language Mix</b><br />"
            f"<sub>{' · '.join(lang_items)}</sub></td>",
            "  </tr>",
            "</table>",
            "",
            "<table>",
            "  <tr>",
            "    <th>Signal</th>",
            "    <th>Repository</th>",
            "    <th>Track</th>",
            "    <th>Signals</th>",
            "    <th>更新</th>",
            "  </tr>",
            "\n".join(rows),
            "</table>",
            "",
            "<sub>模型说明: Signal = 活跃度 + 原创性 + 采用度 + 工程描述完整度；"
            "仅使用 GitHub REST API 公开元数据，不代表项目商业价值或代码质量终判。</sub>",
            "",
            f"<sub>生成时间: {generated_at} · 数据来自 GitHub REST API · 授权 workflow scope 后可启用 6 小时定时刷新。</sub>",
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
