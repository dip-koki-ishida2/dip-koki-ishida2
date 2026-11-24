#!/usr/bin/env python3
"""Generate an anonymous activity stats card (counts only, no repo/org names)."""
import datetime as dt
import json
import os
import sys
import urllib.request

LOGIN = os.environ.get("GH_LOGIN", "dip-koki-ishida2")
TOKEN = os.environ["GITHUB_TOKEN"]
OUT = sys.argv[1] if len(sys.argv) > 1 else "assets/stats.svg"

QUERY = """
query($login:String!,$from:DateTime!,$to:DateTime!){
  user(login:$login){
    createdAt
    contributionsCollection(from:$from,to:$to){
      contributionCalendar{ weeks{ contributionDays{ date contributionCount } } }
    }
  }
}"""


def gql(variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        body = json.load(r)
    if "errors" in body:
        raise SystemExit(body["errors"])
    return body["data"]["user"]


def fetch_days():
    now = dt.datetime.now(dt.timezone.utc)
    created = dt.datetime.fromisoformat(gql({"login": LOGIN, "from": now.isoformat(), "to": now.isoformat()})["createdAt"].replace("Z", "+00:00"))
    days = {}
    start = created
    while start < now:
        end = min(start + dt.timedelta(days=365), now)
        u = gql({"login": LOGIN, "from": start.isoformat(), "to": end.isoformat()})
        for w in u["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
        start = end
    return created, dict(sorted(days.items()))


def streaks(days):
    vals = list(days.values())
    longest = cur = 0
    for v in vals:
        cur = cur + 1 if v > 0 else 0
        longest = max(longest, cur)
    current = 0
    rev = vals[::-1]
    if rev and rev[0] == 0:  # today not yet contributed: don't break streak
        rev = rev[1:]
    for v in rev:
        if v == 0:
            break
        current += 1
    return current, longest


def main():
    created, days = fetch_days()
    total = sum(days.values())
    active = sum(1 for v in days.values() if v > 0)
    current, longest = streaks(days)
    best = max(days.values()) if days else 0
    last30 = list(days.values())[-30:]
    since = created.strftime("%Y.%m")

    stats = [
        ("Total Contributions", f"{total:,}", f"since {since}"),
        ("Current Streak", f"{current}", "days"),
        ("Longest Streak", f"{longest}", "days"),
        ("Active Days", f"{active}", "days"),
        ("Best Day", f"{best}", "contributions"),
    ]

    W, H = 820, 210
    col = W / len(stats)
    parts = []
    for i, (label, value, unit) in enumerate(stats):
        cx = col * i + col / 2
        parts.append(
            f'<g>'
            f'<text x="{cx:.0f}" y="92" class="v">{value}</text>'
            f'<text x="{cx:.0f}" y="118" class="u">{unit}</text>'
            f'<text x="{cx:.0f}" y="146" class="l">{label}</text></g>'
        )
        if i:
            parts.append(f'<line x1="{col*i:.0f}" y1="64" x2="{col*i:.0f}" y2="150" class="sep"/>')

    # 30-day sparkline bars
    mx = max(last30) or 1
    bw = (W - 80) / max(len(last30), 1)
    bars = []
    for i, v in enumerate(last30):
        h = 4 + 22 * v / mx
        bars.append(f'<rect x="{40 + i*bw:.1f}" y="{196 - h:.1f}" width="{bw-3:.1f}" height="{h:.1f}" rx="2" class="b" style="opacity:{0.25 + 0.75*v/mx:.2f}"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#0b2a2f"/></linearGradient>
<linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="#2dd4bf"/><stop offset="1" stop-color="#38bdf8"/></linearGradient></defs>
<style>
.v{{font:700 34px 'Segoe UI',Ubuntu,sans-serif;fill:url(#t);text-anchor:middle}}
.u{{font:500 12px 'Segoe UI',Ubuntu,sans-serif;fill:#5eead4;text-anchor:middle;opacity:.8}}
.l{{font:600 13px 'Segoe UI',Ubuntu,sans-serif;fill:#c9d1d9;text-anchor:middle}}
.h{{font:700 15px 'Segoe UI',Ubuntu,sans-serif;fill:#e6edf3;letter-spacing:2px}}
.f{{font:500 11px 'Segoe UI',Ubuntu,sans-serif;fill:#8b949e}}
.sep{{stroke:#2dd4bf;stroke-opacity:.18}}
.b{{fill:#2dd4bf}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="url(#g)" stroke="#2dd4bf" stroke-opacity=".35"/>
<text x="28" y="38" class="h">⚡ ACTIVITY</text>
<text x="{W-28}" y="38" class="f" text-anchor="end">last 30 days ▸ updated {dt.date.today():%Y-%m-%d}</text>
{''.join(parts)}
{''.join(bars)}
</svg>'''
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT}: total={total} current={current} longest={longest}")


if __name__ == "__main__":
    main()
