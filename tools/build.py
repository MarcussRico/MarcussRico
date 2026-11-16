"""Builds the profile figures in assets/ from the data in tools/data/.

    python3 tools/build.py            # every figure
    python3 tools/build.py hero muon  # some

The contribution graph has its own script (tools/contrib3d.py), run daily by a workflow.
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

from svgkit import BG, DIM, EASE_IN_OUT, EASE_OUT, FAINT, GLOW, HOT, PAPER, RULE, document, magma, text, warn_missing, width

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "tools" / "data"
OUT = ROOT / "assets"


def load(name):
    return json.loads((DATA / name).read_text())


# ═════════════════════════ hero ═════════════════════════


def hero(phone: bool = False) -> str:
    """The header. The wide layout puts the matrix beside the name; the phone layout stacks them,
    with bigger type, for screens too narrow to read the wide one (served through <picture>)."""
    att = load("attention.json")
    toks = [t.strip() or "·" for t in att["tokens"]]
    w = att["weights"]
    n = len(toks)
    if phone:
        W, H = 600, 1090
        cell, gap, ls = 24.0, 2.4, 15  # matrix cell, gap, label size
        lx = 44
        mx, my = W - 44 - n * cell, 560
        head = dict(label=(lx, 66, 19), name=(lx - 4, 152, 74), lines_y=214, line_size=27, line_gap=37, readout_y=448, readout_size=17, readout_gap=31)
        lines = [
            ("I build neural networks", PAPER),
            ("from the chain rule up:", PAPER),
            ("autograd, GPT-2 and optimisers", DIM),
            ("written from scratch, and research", DIM),
            ("on when attention can be trusted.", DIM),
        ]
        caption = ("real GPT-2 attention · layer 11, head 0", W / 2, H - 30, "middle")
    else:
        W, H = 1000, 400
        cell, gap, ls = 13.2, 1.6, 10
        lx = 56
        mx, my = 676, 58
        head = dict(label=(lx, 76, 13), name=(lx - 4, 152, 68), lines_y=200, line_size=21, line_gap=30, readout_y=316, readout_size=13, readout_gap=24)
        lines = [
            ("I build neural networks from the chain rule up:", PAPER),
            ("autograd, GPT-2 and optimisers written from scratch,", DIM),
            ("and research on when attention can be trusted.", DIM),
        ]
        caption = ("real GPT-2 attention · layer 11, head 0 · my implementation", W - 32, H - 22, "end")
    body, css = [], []

    # the words
    x0, y0, s0 = head["label"]
    body.append(text("github.com/MarcussRico", x0, y0, s0, "mono", DIM, cls="fade d0"))
    body.append(text("Chennai, India", x0 + width("github.com/MarcussRico   ", s0), y0, s0, "mono", FAINT, cls="fade d0"))
    nx, ny, ns = head["name"]
    body.append(text("Sai Charan A", nx, ny, ns, "italic", PAPER, cls="rise d1"))
    for i, (s, c) in enumerate(lines):
        body.append(text(s, lx, head["lines_y"] + i * head["line_gap"], head["line_size"], "serif", c, cls=f"rise d{min(2 + i, 6)}"))
    readouts = [
        ("28 / 28", "autograd gradients match PyTorch's"),
        ("124,439,808", "parameters; logits equal OpenAI's GPT-2" if not phone else "params; logits = OpenAI's GPT-2"),
        ("0.398 → 0.955", "attention faithfulness, set by benchmark design" if not phone else "attention faithfulness"),
    ]
    rs = head["readout_size"]
    for i, (num, label) in enumerate(readouts):
        y = head["readout_y"] + i * head["readout_gap"]
        sq = rs * 0.46
        body.append(f'<rect x="{lx}" y="{y - rs * 0.62:.1f}" width="{sq:.1f}" height="{sq:.1f}" rx="1" fill="{HOT}" class="fade d{5 + i}"/>')
        body.append(text(num, lx + rs * 1.25, y, rs, "mono-medium", GLOW, cls=f"fade d{5 + i}"))
        body.append(text(label, lx + rs * 1.25 + width(num + "  ", rs, "mono-medium"), y, rs, "mono", DIM, cls=f"fade d{5 + i}"))

    # the matrix: queries down the side, keys along the bottom; the upper triangle is masked
    cells, mask_dots = [], []
    for i in range(n):
        for j in range(n):
            x, y = mx + j * cell, my + i * cell
            if j > i:
                mask_dots.append(f'<circle cx="{x + cell / 2 - gap / 2:.1f}" cy="{y + cell / 2 - gap / 2:.1f}" r="{cell * 0.07:.1f}" fill="{RULE}"/>')
                continue
            colour = magma(0.08 + 0.92 * math.sqrt(w[i][j]))
            delay = 380 + i * 46 + j * 7
            cells.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell - gap:.1f}" height="{cell - gap:.1f}" rx="{cell * 0.15:.1f}" fill="{colour}" class="cell" style="animation-delay:{delay}ms"/>')
    body.append(f'<g>{"".join(mask_dots)}</g>')
    body.append(f'<g>{"".join(cells)}</g>')

    pad = ls * 0.8
    for i, t in enumerate(toks):
        body.append(text(t, mx - pad, my + i * cell + cell * 0.5 + ls * 0.36, ls, "mono", DIM, anchor="end", cls="fade d3"))
    key_y = my + n * cell + pad

    def key_label(j, kind, colour):
        x = mx + j * cell + cell * 0.5 + ls * 0.2
        return f'<g transform="rotate(-58 {x:.1f} {key_y:.1f})">{text(toks[j], x, key_y, ls, kind, colour, anchor="end")}</g>'

    for j in range(n):
        body.append(f'<g class="fade d3">{key_label(j, "mono", DIM)}</g>')
    body.append(text("query", mx - pad, my - ls * 1.2, ls, "mono", FAINT, anchor="end", cls="fade d3"))
    body.append(text("key →", mx + n * cell - gap, my - ls * 1.2, ls, "mono", FAINT, anchor="end", cls="fade d3"))

    # the loop: one query at a time, its row outlined and its strongest key ringed
    slot = 1.7
    cycle = (n - 1) * slot
    for i in range(1, n):
        row = w[i][: i + 1]
        best = max(range(1, i + 1), key=lambda j: row[j])  # skip the first-token sink
        y = my + i * cell
        bx = mx + best * cell
        delay = 3.2 + (i - 1) * slot
        qw = width(toks[i], ls, "mono-medium")
        body.append(
            f'<g class="scan" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{mx - 1.5:.1f}" y="{y - 1.5:.1f}" width="{(i + 1) * cell + 1.4:.1f}" height="{cell + 1.4:.1f}" rx="{cell * 0.2:.1f}" fill="none" stroke="{PAPER}" stroke-opacity="0.55" stroke-width="{cell / 13:.1f}"/>'
            f'<rect x="{bx - cell * 0.17:.1f}" y="{y - cell * 0.17:.1f}" width="{cell * 1.21:.1f}" height="{cell * 1.21:.1f}" rx="{cell * 0.27:.1f}" fill="none" stroke="{GLOW}" stroke-width="{cell / 8:.1f}"/>'
            f'<rect x="{mx - pad - qw - ls * 0.4:.1f}" y="{y:.1f}" width="{qw + ls * 0.8:.1f}" height="{cell - gap:.1f}" rx="2" fill="{BG}"/>'
            f'{text(toks[i], mx - pad, y + cell * 0.5 + ls * 0.36, ls, "mono-medium", GLOW, anchor="end")}{key_label(best, "mono-medium", GLOW)}</g>'
        )
    cs, cx, cy, ca = caption
    body.append(text(cs, cx, cy, ls, "mono", FAINT, anchor=ca, cls="fade d8"))

    css.append(f"""
.cell {{ transform-box: fill-box; transform-origin: center; animation: cellin 520ms {EASE_OUT} backwards; }}
@keyframes cellin {{ from {{ opacity: 0; transform: scale(0.85); }} }}
.fade {{ animation: fade 700ms {EASE_OUT} backwards; }}
@keyframes fade {{ from {{ opacity: 0; }} }}
.rise {{ animation: rise 900ms {EASE_OUT} backwards; }}
@keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); }} }}
{"".join(f".d{i} {{ animation-delay: {80 + i * 90}ms; }}" for i in range(10))}
.scan {{ opacity: 0; animation: scan {cycle:.2f}s linear infinite; }}
@keyframes scan {{ 0% {{ opacity: 0; }} {100 * 0.18 / cycle:.3f}% {{ opacity: 1; }} {100 * (slot - 0.22) / cycle:.3f}% {{ opacity: 1; }} {100 * slot / cycle:.3f}% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
""")
    return document(W, H, "\n".join(body), "\n".join(css), "Sai Charan A", "Sai Charan A builds neural networks from the chain rule up. Beside the name, a heatmap of real GPT-2 attention weights for the sentence 'Sai builds neural networks from the chain rule up, one gradient at a time.'")


def hero_phone() -> str:
    return hero(phone=True)


# ═════════════════════════ muon / newton-schulz ═════════════════════════


def muon() -> str:
    W, H = 1000, 340
    ns = load("newton_schulz.json")["steps"]
    n = len(ns[0])
    px, py, pw, ph = 452, 54, 512, 220  # plot box
    lo, hi = -4.0, math.log10(2.0)  # log10 axis from 1e-4 to 2

    def ypos(v):
        return py + ph - (math.log10(max(v, 1e-4)) - lo) / (hi - lo) * ph

    body, css = [], []
    body.append(text("muon-newtonschulz", 40, 64, 13, "mono-medium", HOT))
    body.append(text("Orthogonalising an", 40, 104, 29, "serif", PAPER))
    body.append(text("update without an SVD", 40, 138, 29, "italic", PAPER))
    for i, s in enumerate([
        "Muon swaps a gradient G = USV^{T} for UV^{T},",
        "so every direction takes the same step.",
        "Five quintic Newton–Schulz iterations get",
        "there with nothing but matrix multiplies.",
    ]):
        body.append(text(s, 40, 176 + i * 22, 15, "serif", DIM))
    body.append(text("X ← aX + bX(X^{T}X) + cX(X^{T}X)^{2}", 40, 284, 17, "italic", PAPER))
    body.append(text("(a, b, c) = (3.4445, −4.7750, 2.0315)", 40, 308, 11.5, "mono", FAINT))

    # axis, gridlines and the band Muon aims for
    for e in range(-4, 1):
        y = ypos(10**e)
        body.append(f'<line x1="{px}" x2="{px + pw}" y1="{y:.1f}" y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        body.append(text(f"1e{e}" if e else "1", px - 8, y + 4, 10, "mono", FAINT, anchor="end"))
    yb0, yb1 = ypos(0.7), ypos(1.2)
    body.append(f'<rect x="{px}" y="{yb1:.1f}" width="{pw}" height="{yb0 - yb1:.1f}" fill="{HOT}" opacity="0.13"/>')
    body.append(text("target band", px + pw - 6, yb1 - 6, 10, "mono", HOT, anchor="end"))

    # 48 bars, one per singular value, each with its own keyframes through the 6 states
    bw = pw / n
    base = py + ph
    hold, step_t = 1.1, 0.9  # seconds each state is held / takes to move
    cycle = 6 * (hold + step_t) + 1.6
    marks = []
    t = 0.0
    for k in range(6):
        marks.append((t, k))
        t += step_t + hold
    for i in range(n):
        heights = [base - ypos(ns[k][i]) for k in range(6)]
        final = heights[-1]
        frames = []
        for k in range(6):
            start = (k * (step_t + hold)) / cycle * 100
            end = (k * (step_t + hold) + step_t) / cycle * 100 if k else 0
            sc = heights[k] / final
            frames.append(f"{end:.2f}% {{ transform: scaleY({sc:.4f}); }}")
            if k < 5:
                frames.append(f"{((k * (step_t + hold) + step_t + hold) / cycle * 100):.2f}% {{ transform: scaleY({sc:.4f}); }}")
        frames.append(f"{(6 * (step_t + hold)) / cycle * 100:.2f}% {{ transform: scaleY(1); }}")
        frames.append("100% { transform: scaleY(1); }")
        css.append(f"@keyframes sv{i} {{ {' '.join(frames)} }}")
        x = px + i * bw + bw * 0.18
        colour = magma(0.35 + 0.6 * (i / (n - 1)) ** 0.8)
        body.append(f'<rect x="{x:.1f}" y="{base - final:.1f}" width="{bw * 0.64:.1f}" height="{final:.1f}" rx="1.2" fill="{colour}" style="animation: sv{i} {cycle:.2f}s {EASE_IN_OUT} infinite"/>')
    css.append(f"rect[style*='animation: sv'] {{ transform-box: fill-box; transform-origin: bottom; }}")

    # step counter and readout, one label per state
    def label(k):
        s = ns[k]
        inside = sum(0.7 <= v <= 1.2 for v in s)
        return f"step {k}", f"{inside:2d} of {n} in band · smallest {min(s):.4f}"

    for k in range(6):
        a, b = label(k)
        start = (k * (step_t + hold) + (step_t if k else 0)) / cycle * 100
        end = ((k + 1) * (step_t + hold) + step_t) / cycle * 100 if k < 5 else 100
        if k == 5:
            css.append(f"@keyframes st{k} {{ 0%, {start - 0.01:.2f}% {{ opacity: 0; }} {start:.2f}%, 100% {{ opacity: 1; }} }}")
        else:
            css.append(f"@keyframes st{k} {{ 0%, {max(0, start - 0.01):.2f}% {{ opacity: {1 if k == 0 else 0}; }} {start:.2f}%, {end - 0.01:.2f}% {{ opacity: 1; }} {end:.2f}%, 100% {{ opacity: 0; }} }}")
        style = f"animation: st{k} {cycle:.2f}s linear infinite" + ("; opacity: 0" if k < 5 else "")
        body.append(f'<g style="{style}">{text(a, px, py + ph + 34, 13, "mono-medium", GLOW)}{text(b, px + 70, py + ph + 34, 13, "mono", DIM)}</g>')
    body.append(text("singular values of one update, sorted", px + pw, py - 14, 10, "mono", FAINT, anchor="end"))
    return document(W, H, "\n".join(body), "\n".join(css), "Muon: Newton-Schulz orthogonalisation", "Bar chart of 48 singular values of a gradient-like matrix on a log scale, animated through five quintic Newton-Schulz iterations: from 0 of 48 inside the target band to 36 of 48, with the smallest value growing from 0.0005 to 0.24.")


# ═════════════════════════ PUM2 research ═════════════════════════


def pum2() -> str:
    W, H = 1000, 380
    d = load("pum2.json")
    ds = d["designs"]
    body, css = [], []
    body.append(text("PUM2-attention-vs-IG · research", 40, 64, 13, "mono-medium", HOT))
    body.append(text("Benchmark design decides", 40, 104, 29, "serif", PAPER))
    body.append(text("whether attention is faithful", 40, 138, 29, "italic", PAPER))
    for i, s in enumerate([
        "One CNN–BiLSTM–attention model, one set of ENCODE",
        "PUM2 peaks. Change only how the benchmark is built,",
        "and how often attention lands on PUM2's motif",
        "UGUANAUA swings from 0.398 to 0.955.",
    ]):
        body.append(text(s, 40, 178 + i * 22, 15, "serif", DIM))
    body.append(text("The design that scores best on AUC is the one where", 40, 284, 13, "serif", PAPER))
    body.append(text("attention is least faithful: shortcuts, not the motif.", 40, 303, 13, "serif", PAPER))
    body.append(text("attention ≈ integrated gradients (D): 0.955 vs 0.951, p = 0.43", 40, 336, 11, "mono", FAINT))
    body.append(text("motif shuffle moves predictions ~200× more than a random 8-mer", 40, 352, 11, "mono", FAINT))

    # the 2 x 2
    gx, gy, cw, ch, g = 520, 92, 210, 112, 14
    cols = ["peak-centred", "random-padded"]
    rows = ["chromosome", "region-matched"]
    body.append(text("positives →", gx, gy - 34, 10, "mono", FAINT))
    for c, name in enumerate(cols):
        body.append(text(name, gx + c * (cw + g) + cw / 2, gy - 12, 12, "mono", DIM, anchor="middle"))
    body.append(text("negatives ↓", gx - 40, gy - 34, 10, "mono", FAINT, anchor="end"))
    for r, name in enumerate(rows):
        body.append(f'<g transform="rotate(-90 {gx - 32} {gy + r * (ch + g) + ch / 2})">{text(name, gx - 32, gy + r * (ch + g) + ch / 2 + 4, 12, "mono", DIM, anchor="middle")}</g>')
    order = {("peak-centred", "chromosome"): "A", ("peak-centred", "region-matched"): "B", ("random-padded", "chromosome"): "C", ("random-padded", "region-matched"): "D"}
    for r, neg in enumerate(rows):
        for c, pos in enumerate(cols):
            key = order[(pos, neg)]
            v = ds[key]
            x, y = gx + c * (cw + g), gy + r * (ch + g)
            k = r * 2 + c
            fillc = magma(0.18 + 0.7 * v["hit"])
            body.append(f'<g class="cellin" style="animation-delay:{300 + k * 70}ms">')
            body.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="{fillc}" fill-opacity="0.16" stroke="{fillc}" stroke-opacity="0.55"/>')
            body.append(text(key, x + 16, y + 28, 13, "mono-medium", DIM))
            body.append(text(f"{v['hit']:.3f}", x + 16, y + 68, 34, "serif", PAPER))
            body.append(text(f"± {v['sd']:.3f}", x + 16 + width(f"{v['hit']:.3f} ", 34, "serif"), y + 68, 12, "mono", DIM))
            body.append(text(f"AUC {v['auc']:.3f}", x + cw - 16, y + 28, 12, "mono", FAINT, anchor="end"))
            # meter: hit rate on 0..1, with the random-position null marked
            mx0, my0, mw = x + 16, y + ch - 22, cw - 32
            body.append(f'<rect x="{mx0}" y="{my0}" width="{mw}" height="6" rx="3" fill="{RULE}"/>')
            body.append(f'<rect x="{mx0}" y="{my0}" width="{mw * v["hit"]:.1f}" height="6" rx="3" fill="{fillc}" class="meter" style="animation-delay:{650 + k * 90}ms"/>')
            nx = mx0 + mw * d["null_hit_rate"]
            body.append(f'<line x1="{nx:.1f}" x2="{nx:.1f}" y1="{my0 - 4}" y2="{my0 + 10}" stroke="{PAPER}" stroke-opacity="0.6"/>')
            body.append("</g>")
    body.append(text("motif hit rate · five seeds · tick = random-position null (0.12)", gx + 2 * cw + g, gy + 2 * ch + g + 26, 10, "mono", FAINT, anchor="end"))
    css.append(f"""
.cellin {{ animation: fadeup 700ms {EASE_OUT} backwards; }}
@keyframes fadeup {{ from {{ opacity: 0; transform: translateY(10px); }} }}
.meter {{ transform-box: fill-box; transform-origin: left; animation: grow 1100ms {EASE_OUT} backwards; }}
@keyframes grow {{ from {{ transform: scaleX(0.02); }} }}
""")
    return document(W, H, "\n".join(body), "\n".join(css), "Benchmark design decides whether attention is faithful", "A 2 by 2 grid of benchmark designs for PUM2 binding-site models. Attention motif hit rate: A 0.398, B 0.799, C 0.921, D 0.955, while AUC runs the other way, from 0.803 in A to 0.695 in D.")


# ═════════════════════════ shared: a loss chart that draws itself ═════════════════════════


def loss_chart(series, x0, y0, w, h, steps, lo, hi, delay_ms=600, dur_ms=2200):
    """Lines that draw on, left to right, labelled at their right ends. series: [(values, colour, label, dashed)]."""
    out = []
    for v in (lo, (lo + hi) / 2, hi):
        y = y0 + h - (v - lo) / (hi - lo) * h
        out.append(f'<line x1="{x0}" x2="{x0 + w}" y1="{y:.1f}" y2="{y:.1f}" stroke="{RULE}"/>')
        out.append(text(f"{v:.1f}", x0 - 6, y + 3.5, 10, "mono", FAINT, anchor="end"))
    smax = steps[-1]
    for frac in (0, 0.5, 1):
        s = round(smax * frac)
        out.append(text(f"{s:,}", x0 + w * frac, y0 + h + 16, 10, "mono", FAINT, anchor="middle"))
    ends, lines = [], []
    global _CLIPS
    _CLIPS += 1
    cid = f"reveal{_CLIPS}"
    out.append(f'<clipPath id="{cid}"><rect x="{x0 - 6}" y="{y0 - 12}" width="{w + 12}" height="{h + 24}" class="wipe" style="animation-delay:{delay_ms}ms;animation-duration:{dur_ms}ms"/></clipPath>')
    for k, (vals, colour, label, dashed) in enumerate(series):
        pts = [(x0 + s / smax * w, y0 + h - (min(max(v, lo), hi) - lo) / (hi - lo) * h) for s, v in zip(steps, vals)]
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        length = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
        lines.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
        ex, ey = pts[-1]
        out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.2" fill="{colour}" class="fade" style="animation-delay:{delay_ms + dur_ms}ms"/>')
        ends.append([ey, ex, f"{label} {vals[-1]:.2f}", colour])
    out.append(f'<g clip-path="url(#{cid})">{"".join(lines)}</g>')
    # end labels to the right of the chart, top to bottom, at least 14px apart
    ends.sort()
    for i in range(1, len(ends)):
        ends[i][0] = max(ends[i][0], ends[i - 1][0] + 14)
    for ey, ex, s, colour in ends:
        out.append(text(s, ex + 10, ey + 4, 11, "mono-medium", colour, cls="fade", style=f"animation-delay:{delay_ms + dur_ms}ms"))
    return "\n".join(out)


_CLIPS = 0

CHART_CSS = f"""
.wipe {{ transform-box: fill-box; transform-origin: left; animation: wipe 2200ms {EASE_IN_OUT} backwards; }}
@keyframes wipe {{ from {{ transform: scaleX(0.001); }} }}
.fade {{ animation: fade 700ms {EASE_OUT} backwards; }}
@keyframes fade {{ from {{ opacity: 0; }} }}
"""


# ═════════════════════════ autograd ═════════════════════════


def autograd() -> str:
    W, H = 1000, 400
    run = load("autograd_run.json")
    body, css = [], [CHART_CSS]
    body.append(text("autograd-from-scratch", 40, 64, 13, "mono-medium", HOT))
    body.append(text("Reverse-mode autograd", 40, 104, 29, "serif", PAPER))
    body.append(text("in ~200 lines of NumPy", 40, 138, 29, "italic", PAPER))
    for i, s in enumerate([
        "Every operation records how to send its gradient",
        "back. One reverse sweep in topological order fills",
        "every .grad, and broadcasting is undone on the way.",
        "28 tests check its gradients against PyTorch's.",
    ]):
        body.append(text(s, 40, 178 + i * 22, 15, "serif", DIM))
    v0, v1 = run["val"][0], run["val"][-1]
    body.append(text(f"It trains a {run['params'] / 1e3:.0f}K-parameter GPT on Shakespeare,", 40, 286, 13, "serif", PAPER))
    body.append(text(f"no PyTorch: validation loss {v0:.2f} → {v1:.2f}.", 40, 305, 13, "serif", PAPER))

    # the graph: L = loss(tanh(x @ W + b))
    nodes = {
        "x": (478, 196, "x", "tensor"),
        "W": (478, 118, "W", "tensor"),
        "mm": (590, 157, "@", "op"),
        "b": (690, 88, "b", "tensor"),
        "add": (690, 157, "+", "op"),
        "tanh": (800, 157, "tanh", "op"),
        "L": (910, 157, "L", "tensor"),
    }
    edges = [("x", "mm", 0), ("W", "mm", 0), ("mm", "add", 1), ("b", "add", 1), ("add", "tanh", 2), ("tanh", "L", 3)]
    hop, gap_t = 0.5, 0.42  # seconds per hop forward/back; pause between passes
    cycle = 8.0

    def edge_pts(a, b):
        ax, ay, *_ = nodes[a]
        bx, by, *_ = nodes[b]
        L = math.dist((ax, ay), (bx, by))
        ux, uy = (bx - ax) / L, (by - ay) / L
        return (ax + ux * 24, ay + uy * 24), (bx - ux * 24, by - uy * 24)

    for a, b, _ in edges:
        (sx, sy), (ex, ey) = edge_pts(a, b)
        body.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{FAINT}" stroke-width="1.3"/>')
    for key, (x, y, label, kind) in nodes.items():
        if kind == "op":
            body.append(f'<circle cx="{x}" cy="{y}" r="22" fill="#1E1629" stroke="{FAINT}"/>')
            body.append(text(label, x, y + 5, 14 if len(label) > 1 else 17, "mono-medium" if len(label) > 1 else "serif", PAPER, anchor="middle"))
        else:
            body.append(f'<rect x="{x - 21}" y="{y - 21}" width="42" height="42" rx="9" fill="#241A31" stroke="{magma(0.62)}"/>')
            body.append(text(label, x, y + 7, 21, "italic", PAPER, anchor="middle"))

    pulses = []

    def pulse(a, b, t0, colour, back=False):
        (sx, sy), (ex, ey) = edge_pts(a, b)
        if back:
            sx, sy, ex, ey = ex, ey, sx, sy
        i = len(pulses)
        s0, s1 = t0 / cycle * 100, (t0 + hop) / cycle * 100
        css.append(f"@keyframes p{i} {{ 0%, {s0:.2f}% {{ opacity: 0; transform: translate(0px, 0px); }} {s0 + 0.5:.2f}% {{ opacity: 1; }} {s1:.2f}% {{ opacity: 1; transform: translate({ex - sx:.1f}px, {ey - sy:.1f}px); }} {s1 + 1.2:.2f}%, 100% {{ opacity: 0; transform: translate({ex - sx:.1f}px, {ey - sy:.1f}px); }} }}")
        pulses.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{4.5 if back else 3.6}" fill="{colour}" style="opacity:0;animation: p{i} {cycle}s {EASE_IN_OUT} infinite"/>')

    for a, b, k in edges:
        pulse(a, b, 0.3 + k * hop, magma(0.55))
    back_start = 0.3 + 4 * hop + gap_t
    for a, b, k in edges:
        pulse(a, b, back_start + (3 - k) * hop, GLOW, back=True)
    body.extend(pulses)

    grads = {"b": ("∂L/∂b", 0, -34), "W": ("∂L/∂W", 0, -34), "x": ("∂L/∂x", 0, 44)}
    arrive = {"b": back_start + 2 * hop + hop, "W": back_start + 3 * hop + hop, "x": back_start + 3 * hop + hop}
    for key, (label, dx, dy) in grads.items():
        x, y, *_ = nodes[key]
        a = arrive[key] / cycle * 100
        css.append(f"@keyframes g{key} {{ 0%, {a:.2f}% {{ opacity: 0; transform: translateY(4px); }} {a + 3:.2f}%, 92% {{ opacity: 1; transform: translateY(0px); }} 98%, 100% {{ opacity: 0; }} }}")
        body.append(f'<g style="animation: g{key} {cycle}s {EASE_OUT} infinite">{text(label, x + dx, y + dy, 14, "italic", GLOW, anchor="middle")}</g>')
    body.append(text("forward: values", 478, 262, 10, "mono", magma(0.6)))
    body.append(text("backward: gradients", 478 + width("forward: values    ", 10), 262, 10, "mono", GLOW))

    # the training curve
    body.append(loss_chart([(run["train"], magma(0.55), "train", False), (run["val"], GLOW, "val", False)], 520, 292, 360, 70, run["steps"], 1.0, 4.5, delay_ms=500))
    body.append(text("char-level GPT, trained by this engine", 960, 287, 10, "mono", FAINT, anchor="end"))
    return document(W, H, "\n".join(body), "\n".join(css), "autograd-from-scratch", f"A computation graph for L = loss(tanh(x @ W + b)): values flow forward, gradients flow back and the labels dL/dW, dL/db and dL/dx appear. Below, the training curve of a {run['params']:,}-parameter character-level GPT trained with this engine and NumPy only: validation loss {v0:.2f} to {v1:.2f}.")


# ═════════════════════════ GPT-2 ═════════════════════════


def gpt2() -> str:
    W, H = 1000, 420
    run = load("gpt2_run.json")
    check = load("gpt2_check.json")
    body, css = [], [CHART_CSS]
    body.append(text("gpt2-from-scratch", 40, 64, 13, "mono-medium", HOT))
    body.append(text("GPT-2, written by hand", 40, 104, 29, "serif", PAPER))
    body.append(text("and checked against OpenAI", 40, 138, 29, "italic", PAPER))
    for i, s in enumerate([
        "Causal self-attention, the residual stream, weight",
        "tying and a KV cache, written out in PyTorch. Given",
        "OpenAI's 124M checkpoint it computes what the",
        "reference computes, to float precision.",
    ]):
        body.append(text(s, 40, 178 + i * 22, 15, "serif", DIM))
    checks = [
        f"logits match the reference · max |Δ| {check['max_abs_logit_diff']:.1e}",
        "20 greedy tokens identical to the reference",
        "KV-cached generation ≡ uncached",
        "124,439,808 parameters, as released",
    ]
    for i, s in enumerate(checks):
        y = 286 + i * 24
        delay = 700 + i * 220
        body.append(f'<path d="M40 {y - 5} l4 4 l8 -9" fill="none" stroke="{GLOW}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="tick" style="animation-delay:{delay}ms"/>')
        body.append(text(s, 60, y, 12, "mono", PAPER if i == 0 else DIM, cls="fade", style=f"animation-delay:{delay}ms"))

    # right: training curve and a sample
    cx0 = 520
    body.append(text(f"trained from scratch on Shakespeare · {run['params'] / 1e6:.1f}M params · Apple M5 GPU", 960, 64, 10, "mono", FAINT, anchor="end"))
    body.append(loss_chart([(run["train"], magma(0.55), "train", False), (run["val"], GLOW, "val", False)], cx0 + 26, 84, 334, 118, run["steps"], 1.0, 4.5, delay_ms=400))
    lines = [l for l in run["sample"].split("\n") if l.strip()][:6]
    body.append(f'<rect x="{cx0}" y="238" width="440" height="148" rx="10" fill="#17101F" stroke="{RULE}"/>')
    body.append(text("sample, temperature 0.8", cx0 + 16, 258, 10, "mono", FAINT))
    t0 = 2.4
    for i, line in enumerate(lines):
        line = line[:52]
        y = 282 + i * 18
        body.append(text(line, cx0 + 16, y, 12, "mono", PAPER if i % 2 == 0 else DIM))
        wpx = width(line, 12) + 4
        dur = max(0.25, len(line) * 0.028)
        body.append(f'<rect x="{cx0 + 14}" y="{y - 12}" width="{wpx:.1f}" height="16" fill="#17101F" class="type" style="--w:{wpx:.1f}px;animation-delay:{t0:.2f}s;animation-duration:{dur:.2f}s;animation-timing-function:steps({max(1, len(line))})"/>')
        t0 += dur + 0.12
    css.append(f"""
.tick {{ animation: tick 500ms {EASE_OUT} backwards; }}
@keyframes tick {{ from {{ opacity: 0; transform: translateY(4px); }} }}
/* the cover rests invisible, so with motion off the sample is simply there */
.type {{ opacity: 0; animation-name: type; animation-fill-mode: backwards; }}
@keyframes type {{ from {{ opacity: 1; transform: translateX(0px); }} 99.9% {{ opacity: 1; transform: translateX(var(--w)); }} to {{ opacity: 0; transform: translateX(var(--w)); }} }}
""")
    return document(W, H, "\n".join(body), "\n".join(css), "gpt2-from-scratch", f"GPT-2 written by hand in PyTorch. With OpenAI's weights its logits match the reference to {check['max_abs_logit_diff']:.1e}, greedy output is identical, and the KV cache changes nothing. Trained from scratch on Shakespeare it reaches validation loss {run['val'][-1]:.2f}.")


FIGURES = {"hero": hero, "hero_phone": hero_phone, "muon": muon, "pum2": pum2, "autograd": autograd, "gpt2": gpt2}


def main(names):
    OUT.mkdir(exist_ok=True)
    for name in names or FIGURES:
        svg = FIGURES[name]()
        (OUT / f"{name}.svg").write_text(svg)
        print(f"{name}.svg  {len(svg) / 1024:.0f} KB")
    warn_missing()


if __name__ == "__main__":
    main(sys.argv[1:])
