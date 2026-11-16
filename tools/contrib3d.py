"""The last year of contributions as an isometric 3D bar chart: assets/contrib3d.svg.

    python3 tools/contrib3d.py                 # asks GitHub (GITHUB_TOKEN, or the gh CLI)
    python3 tools/contrib3d.py calendar.json   # from a saved GraphQL response

Run daily by .github/workflows/contrib3d.yml. Each day is a tower whose height is the square root
of its count (so one huge day doesn't flatten the rest); towers rise week by week when the image
loads, then a slow light travels across the year.
"""

from __future__ import annotations

import datetime as dt
import json
import math
import os
import pathlib
import subprocess
import sys
import urllib.request

from svgkit import DIM, EASE_OUT, FAINT, GLOW, HOT, PAPER, RULE, document, magma, shade, text, width

USER = os.environ.get("PROFILE_USER", "MarcussRico")
ROOT = pathlib.Path(__file__).resolve().parents[1]
QUERY = "query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"


def fetch() -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
            headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "contrib3d"},
        )
        return json.load(urllib.request.urlopen(req))
    out = subprocess.run(["gh", "api", "graphql", "-f", f"query={QUERY}", "-f", f"login={USER}"], check=True, capture_output=True, text=True)
    return json.loads(out.stdout)


def streaks(counts: list[int]) -> tuple[int, int]:
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current = 0
    for c in reversed(counts):
        if not c:
            break
        current += 1
    return longest, current


def build(raw: dict) -> str:
    cal = raw["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [w["contributionDays"] for w in cal["weeks"]]
    days = [d for w in weeks for d in w]
    counts = [d["contributionCount"] for d in days]
    peak = max(counts) or 1
    busiest = max(days, key=lambda d: d["contributionCount"])
    longest, _current = streaks(counts)

    W, H = 1000, 430
    wv = (14.4, -3.3)  # one week along the year
    dv = (5.4, 6.2)  # one day down the week
    ox, oy = 92, 322  # where week 0, Sunday sits
    max_h = 118

    def at(w, d):
        return ox + w * wv[0] + d * dv[0], oy + w * wv[1] + d * dv[1]

    def poly(pts, fill, extra=""):
        return f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}Z" fill="{fill}"{extra}/>'

    towers = []
    for wi, week in enumerate(weeks):
        for day in week:
            di = dt.date.fromisoformat(day["date"]).isoweekday() % 7  # Sunday = 0, as GitHub draws it
            c = day["contributionCount"]
            p0 = at(wi, di)
            p1 = (p0[0] + wv[0] * 0.86, p0[1] + wv[1] * 0.86)
            p3 = (p0[0] + dv[0] * 0.86, p0[1] + dv[1] * 0.86)
            p2 = (p1[0] + dv[0] * 0.86, p1[1] + dv[1] * 0.86)
            t = math.sqrt(c / peak)
            h = 2.0 + max_h * t if c else 1.4
            up = lambda p: (p[0], p[1] - h)  # noqa: E731
            if c:
                top = magma(0.42 + 0.56 * t)
                left, front = shade(top, 0.55), shade(top, 0.74)
            else:
                top, left, front = "#2A2036", "#1C1526", "#221A2E"
            faces = poly([p0, p3, up(p3), up(p0)], left) + poly([p3, p2, up(p2), up(p3)], front) + poly([up(p0), up(p1), up(p2), up(p3)], top)
            glow = ""
            if c:
                glow = poly([up(p0), up(p1), up(p2), up(p3)], GLOW, f' class="wave" style="animation-delay:{2.4 + wi * 0.09:.2f}s"')
            depth = p0[1] + p3[1]  # paint far (higher on screen) first
            ox_, oy_ = (p0[0] + p2[0]) / 2, max(p2[1], p3[1])
            towers.append((depth, wi, f'<g class="tower" style="transform-origin:{ox_:.1f}px {oy_:.1f}px;animation-delay:{120 + wi * 30 + di * 9}ms">{faces}{glow}</g>'))
    towers.sort(key=lambda t: (t[0], t[1]))

    body = []
    body.append(text("Contributions, last 12 months", 40, 62, 27, "serif", PAPER, cls="fade"))
    body.append(text(f"{cal['totalContributions']:,} contributions · {sum(1 for c in counts if c)} active days · updated {days[-1]['date']}", 40, 88, 12, "mono", DIM, cls="fade"))
    body.extend(t[2] for t in towers)

    # month names along the near edge of the year
    seen = set()
    for wi, week in enumerate(weeks):
        first = dt.date.fromisoformat(week[0]["date"])
        if first.day <= 7 and first.month not in seen and 0 < wi < len(weeks) - 1:
            seen.add(first.month)
            x, y = at(wi, 7)  # the near edge, where no tower can hide it
            body.append(text(first.strftime("%b"), x + 2, y + 16, 10, "mono", FAINT, cls="fade"))
    for di, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        x, y = at(0, di)
        body.append(text(name, x - 10, y + 6, 10, "mono", FAINT, anchor="end", cls="fade"))

    # readouts, along the bottom right
    stats = [
        (f"{peak}", f"on {dt.date.fromisoformat(busiest['date']).strftime('%-d %b')}, the busiest day"),
        (f"{longest} days", "longest streak"),
    ]
    sx = W - 40
    for num, label in reversed(stats):
        body.append(text(label, sx, H - 25, 12, "mono", DIM, anchor="end", cls="fade"))
        sx -= width(label + "  ", 12)
        body.append(text(num, sx, H - 25, 13, "mono-medium", GLOW, anchor="end", cls="fade"))
        sx -= width(num + "      ", 13, "mono-medium")
    # legend
    lx, ly = 40, H - 34
    body.append(text("less", lx, ly + 9, 10, "mono", FAINT))
    for i, tt in enumerate([0, 0.25, 0.5, 0.75, 1.0]):
        fill = "#2A2036" if tt == 0 else magma(0.42 + 0.56 * tt)
        body.append(f'<rect x="{lx + 34 + i * 16}" y="{ly}" width="11" height="11" rx="2" fill="{fill}"/>')
    body.append(text("more", lx + 34 + 5 * 16 + 4, ly + 9, 10, "mono", FAINT))
    body.append(text("height = √count", lx + 34 + 5 * 16 + 48, ly + 9, 10, "mono", FAINT))

    cycle = 2.4 + len(weeks) * 0.09 + 3.0
    css = f"""
.tower {{ transform-box: view-box; animation: rise 1000ms {EASE_OUT} backwards; }}
@keyframes rise {{ from {{ transform: scaleY(0.04); opacity: 0; }} }}
.fade {{ animation: fade 800ms {EASE_OUT} backwards; animation-delay: 200ms; }}
@keyframes fade {{ from {{ opacity: 0; }} }}
.wave {{ opacity: 0; animation: wave {cycle:.1f}s linear infinite; }}
@keyframes wave {{ 0% {{ opacity: 0; }} 2% {{ opacity: 0.55; }} 9% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
"""
    desc = f"Isometric 3D bar chart of {USER}'s GitHub contributions over the last year: {cal['totalContributions']} contributions on {sum(1 for c in counts if c)} days, busiest day {peak}."
    return document(W, H, "\n".join(body), css, "Contributions in 3D", desc)


def main():
    raw = json.loads(pathlib.Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else fetch()
    svg = build(raw)
    out = ROOT / "assets" / "contrib3d.svg"
    out.parent.mkdir(exist_ok=True)
    out.write_text(svg)
    print(f"contrib3d.svg  {len(svg) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
