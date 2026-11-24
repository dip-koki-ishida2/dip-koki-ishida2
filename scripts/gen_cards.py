#!/usr/bin/env python3
"""Static cards (numbers from public LT decks). Run manually when content changes."""
import os

FONT = "'Segoe UI',Ubuntu,'Hiragino Sans','Noto Sans JP',sans-serif"
DEFS = """<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#0b2a2f"/></linearGradient>
<linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="#2dd4bf"/><stop offset="1" stop-color="#38bdf8"/></linearGradient>
<marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#2dd4bf"/></marker></defs>"""
STYLE = f"""<style>
.h{{font:700 15px {FONT};fill:#e6edf3;letter-spacing:2px}}
.f{{font:500 11px {FONT};fill:#8b949e}}
.v{{font:700 36px {FONT};fill:#2dd4bf;text-anchor:middle}}
.u{{font:600 13px {FONT};fill:#e6edf3;text-anchor:middle}}
.s{{font:500 11.5px {FONT};fill:#8b949e;text-anchor:middle}}
.who{{font:700 17px {FONT};fill:#e6edf3;text-anchor:middle}}
.role{{font:700 12px {FONT};fill:#2dd4bf;text-anchor:middle;letter-spacing:1px}}
.d{{font:500 12px {FONT};fill:#c9d1d9;text-anchor:middle}}
.box{{fill:#0d1117;stroke:#2dd4bf;stroke-opacity:.45}}
.hum{{fill:#0d1117;stroke:#fbbf24;stroke-opacity:.7}}
.sep{{stroke:#2dd4bf;stroke-opacity:.18}}
.ar{{stroke:#2dd4bf;stroke-width:1.6;fill:none;marker-end:url(#a)}}
.tag{{font:600 11px {FONT};fill:#5eead4}}
</style>"""


def frame(w, h, title, note, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'{DEFS}{STYLE}<rect width="{w}" height="{h}" rx="14" fill="url(#g)" stroke="#2dd4bf" stroke-opacity=".35"/>'
            f'<text x="28" y="38" class="h">{title}</text><text x="{w-28}" y="38" class="f" text-anchor="end">{note}</text>'
            f'{body}</svg>')


def highlights():
    W, H = 820, 190
    items = [
        ("1,434", "PRs merged", "2026.05 – 10 / 約半年"),
        ("~50", "PRs / week", "7月以降 週40〜77件で安定"),
        ("12", "PRs / workday", "中央値"),
        ("92", "CI checks", "レビュー指摘を自動チェック化"),
    ]
    col = W / len(items)
    body = []
    for i, (v, u, s) in enumerate(items):
        cx = col * i + col / 2
        body.append(f'<text x="{cx:.0f}" y="98" class="v">{v}</text><text x="{cx:.0f}" y="124" class="u">{u}</text>'
                    f'<text x="{cx:.0f}" y="150" class="s">{s}</text>')
        if i:
            body.append(f'<line x1="{col*i:.0f}" y1="66" x2="{col*i:.0f}" y2="160" class="sep"/>')
    return frame(W, H, "🚀 AI-DRIVEN OUTPUT", "量は AI で、質は CI で", "".join(body))


def pipeline():
    W, H = 820, 250
    steps = [
        ("Claude", "PLAN", "Issue を切り", "次にやることを決める", "box"),
        ("Codex", "IMPLEMENT", "Issue から", "PR まで作る", "box"),
        ("Copilot + Codex", "REVIEW", "別の AI が", "もう一度見て直す", "box"),
        ("Human", "DECIDE", "マージするか", "最後の判断だけ", "hum"),
    ]
    bw, gap, x0, y0, bh = 170, 30, 28, 62, 120
    body = []
    for i, (who, role, d1, d2, cls) in enumerate(steps):
        x = x0 + i * (bw + gap)
        cx = x + bw / 2
        rs = ' style="fill:#fbbf24"' if cls == "hum" else ""
        body.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="10" class="{cls}"/>'
                    f'<text x="{cx}" y="{y0+28}" class="role"{rs}>{role}</text>'
                    f'<text x="{cx}" y="{y0+56}" class="who">{who}</text>'
                    f'<text x="{cx}" y="{y0+84}" class="d">{d1}</text><text x="{cx}" y="{y0+102}" class="d">{d2}</text>')
        if i < len(steps) - 1:
            body.append(f'<line x1="{x+bw+4}" y1="{y0+bh/2}" x2="{x+bw+gap-4}" y2="{y0+bh/2}" class="ar"/>')
    body.append(f'<text x="{W/2}" y="222" class="tag" text-anchor="middle">'
                'AI ごとに役割を分けて、止めずに動かし続ける ── 人が触るのは「入口」と「最後の判断」だけ</text>')
    return frame(W, H, "🤖 MY AI PIPELINE", "multi-agent workflow", "".join(body))


def loop():
    W, H = 820, 230
    steps = [
        ("☀️ 昼 / Human", ["受入条件と設計判断を", "曖昧さゼロまで issue に書く"]),
        ("🏷️ Label", ["ready-for-loop を貼る", "ループが拾う対象を決める"]),
        ("🌙 夜 / AI", ["寝る前に skill を 1 発", "無人で 1 件ずつ PR まで"]),
        ("🌅 朝 / Review", ["AI レビューで 3 分類", "詰まりは理由付きで返る"]),
    ]
    bw, gap, x0, y0, bh = 170, 30, 28, 62, 104
    body = []
    for i, (t, ds) in enumerate(steps):
        x = x0 + i * (bw + gap)
        cx = x + bw / 2
        body.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="10" class="box"/>'
                    f'<text x="{cx}" y="{y0+32}" class="u" style="font-size:14px">{t}</text>'
                    f'<text x="{cx}" y="{y0+62}" class="d" style="font-size:11px">{ds[0]}</text>'
                    f'<text x="{cx}" y="{y0+80}" class="d" style="font-size:11px">{ds[1]}</text>')
        if i < len(steps) - 1:
            body.append(f'<line x1="{x+bw+4}" y1="{y0+bh/2}" x2="{x+bw+gap-4}" y2="{y0+bh/2}" class="ar"/>')
    body.append(f'<text x="{W/2}" y="204" class="tag" text-anchor="middle">昼は人間の時間、夜は AI の時間。── 朝には、レビュー待ちの PR が並んでいる</text>')
    return frame(W, H, "🌙 LOOP ENGINEERING", "実装を夜中に片付ける仕組み", "".join(body))


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    for name, fn in [("highlights", highlights), ("pipeline", pipeline), ("loop", loop)]:
        with open(f"assets/{name}.svg", "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", name)
