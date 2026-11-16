"""Shared pieces for the profile figures: palette, type set as outlines, and SVG scaffolding.

GitHub shows README images through its image proxy, where an SVG cannot load web fonts or run
scripts, but can run CSS animations. So every word here is converted to vector outlines with
fontTools, and every animation is a CSS keyframe whose *resting* state is the finished figure:
with reduced motion (or a renderer that ignores animation) the reader still sees the full figure.
"""

from __future__ import annotations

import pathlib
from functools import lru_cache
from xml.sax.saxutils import escape

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONTS = pathlib.Path(__file__).resolve().parent / "fonts"

# ───────── palette: matplotlib's magma, on aubergine ink ─────────

BG = "#120C1A"
PANEL = "#1A1325"
RULE = "#2C2238"
PAPER = "#F3EADF"
DIM = "#A496B4"
FAINT = "#6E6180"

MAGMA = [  # matplotlib magma at 0, 1/8, ..., 1
    (0.000, (0, 0, 4)),
    (0.125, (28, 16, 68)),
    (0.250, (79, 18, 123)),
    (0.375, (129, 37, 129)),
    (0.500, (181, 54, 122)),
    (0.625, (229, 80, 100)),
    (0.750, (251, 135, 97)),
    (0.875, (254, 194, 135)),
    (1.000, (252, 253, 191)),
]
HOT = "#FB8761"  # magma 0.75: the one accent
GLOW = "#FEC287"  # magma 0.875
ROSE = "#E55064"  # magma 0.625


def magma(t: float) -> str:
    t = min(1.0, max(0.0, t))
    for (t0, c0), (t1, c1) in zip(MAGMA, MAGMA[1:]):
        if t <= t1:
            u = (t - t0) / (t1 - t0)
            r, g, b = (round(a + (b_ - a) * u) for a, b_ in zip(c0, c1))
            return f"#{r:02X}{g:02X}{b:02X}"
    return "#FCFDBF"


def shade(hex_: str, k: float) -> str:
    """Darken (k < 1) or lighten (k > 1) a colour, for the faces of the 3D bars."""
    r, g, b = (int(hex_[i : i + 2], 16) for i in (1, 3, 5))
    if k <= 1:
        r, g, b = (round(c * k) for c in (r, g, b))
    else:
        r, g, b = (round(c + (255 - c) * (k - 1)) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


# ───────── type as outlines ─────────


class Face:
    def __init__(self, file: str, wght: int | None = None, fallback: "Face | None" = None):
        font = TTFont(FONTS / file)
        if wght is not None and "fvar" in font:
            font = instancer.instantiateVariableFont(font, {"wght": wght})
        self.key = f"{pathlib.Path(file).stem}-{wght or 0}".replace("[", "").replace("]", "")
        self.glyphs = font.getGlyphSet()
        self.cmap = font.getBestCmap()
        self.upm = font["head"].unitsPerEm
        self.hmtx = font["hmtx"]
        self.fallback = fallback
        self.missing: set[str] = set()

    def resolve(self, ch: str) -> tuple["Face", str]:
        """The face and glyph that draw `ch`: this font, else the fallback, else '?'."""
        name = self.cmap.get(ord(ch))
        if name is not None:
            return self, name
        if self.fallback is not None and ord(ch) in self.fallback.cmap:
            return self.fallback, self.fallback.cmap[ord(ch)]
        self.missing.add(ch)
        return self, self.cmap[ord("?")]

    def advance(self, ch: str) -> float:
        f, name = self.resolve(ch)
        return f.hmtx[name][0] / f.upm  # in ems

    def outline(self, name: str) -> str:
        """One glyph's outline in font units (y up), drawn once per figure and reused."""
        pen = SVGPathPen(self.glyphs, ntos=lambda v: str(round(v)))
        self.glyphs[name].draw(pen)
        return pen.getCommands()


USED: dict[str, str] = {}

SUP_SCALE, SUP_RAISE = 0.64, 0.36  # superscripts: size and lift, in ems of the surrounding text


def runs(s: str) -> list[tuple[str, bool]]:
    """Split 'USV^{T}' into [('USV', False), ('T', True)]."""
    out, i = [], 0
    while i < len(s):
        j = s.find("^{", i)
        if j < 0:
            out.append((s[i:], False))
            break
        if j > i:
            out.append((s[i:j], False))
        k = s.index("}", j)
        out.append((s[j + 2 : k], True))
        i = k + 1
    return out


@lru_cache(maxsize=None)
def face(kind: str) -> Face:
    math_face = _math()
    return {
        "serif": lambda: Face("STIXTwoText[wght].ttf", 450, math_face),
        "serif-medium": lambda: Face("STIXTwoText[wght].ttf", 560, math_face),
        "italic": lambda: Face("STIXTwoText-Italic[wght].ttf", 450, math_face),
        "italic-medium": lambda: Face("STIXTwoText-Italic[wght].ttf", 560, math_face),
        "mono": lambda: Face("IBMPlexMono-Regular.ttf", None, math_face),
        "mono-medium": lambda: Face("IBMPlexMono-Medium.ttf", None, math_face),
    }[kind]()


@lru_cache(maxsize=None)
def _math() -> Face:
    return Face("STIXTwoMath-Regular.ttf")


def width(s: str, size: float, kind: str = "mono", tracking: float = 0.0) -> float:
    f = face(kind)
    total, count = 0.0, 0
    for chunk, sup in runs(s):
        k = SUP_SCALE if sup else 1.0
        total += sum(f.advance(c) for c in chunk) * size * k
        count += len(chunk)
    return total + tracking * size * max(0, count - 1)


def text(s: str, x: float, y: float, size: float, kind: str = "mono", fill: str = PAPER, anchor: str = "start", tracking: float = 0.0, cls: str = "", style: str = "", opacity: float | None = None) -> str:
    """`s` set in `kind` as reused glyph outlines, baseline at y. `^{...}` makes a superscript."""
    f = face(kind)
    w = width(s, size, kind, tracking)
    cx = x - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
    groups = []
    for chunk, sup in runs(s):
        sz = size * (SUP_SCALE if sup else 1.0)
        by = y - (size * SUP_RAISE if sup else 0)
        parts, gx = [], 0.0  # gx in ems of sz
        for ch in chunk:
            g, name = f.resolve(ch)
            gid = f"{g.key}-{name}".replace(".", "_")
            if gid not in USED:
                USED[gid] = g.outline(name)
            if ch != " ":
                # every font here uses 1000 units per em, so one scale serves both faces
                parts.append(f'<use href="#{gid}" x="{gx * 1000:.0f}"/>')
            gx += g.hmtx[name][0] / g.upm + tracking
        s_ = sz / 1000
        groups.append(f'<g transform="translate({cx:.1f} {by:.1f}) scale({s_:.5f} {-s_:.5f})">{"".join(parts)}</g>')
        cx += gx * sz
    attrs = f' class="{cls}"' if cls else ""
    attrs += f' style="{style}"' if style else ""
    attrs += f' opacity="{opacity}"' if opacity is not None else ""
    return f'<g fill="{fill}"{attrs}>{"".join(groups)}</g>'


# ───────── scaffolding ─────────

EASE_OUT = "cubic-bezier(0.23, 1, 0.32, 1)"
EASE_IN_OUT = "cubic-bezier(0.77, 0, 0.175, 1)"


def glyph_defs() -> str:
    """Every glyph this figure used, once each; then forget them for the next figure."""
    out = "".join(f'<path id="{k}" d="{d}"/>' for k, d in USED.items())
    USED.clear()
    return out


def document(w: int, h: int, body: str, css: str, title: str, desc: str) -> str:
    """A self-contained figure: rounded panel, faint grid, grain, and its own animation rules."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
<title id="t">{escape(title)}</title>
<desc id="d">{escape(desc)}</desc>
<defs>
{glyph_defs()}
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{RULE}" stroke-width="0.6" opacity="0.55"/>
  </pattern>
  <radialGradient id="glow" cx="0.72" cy="0.38" r="0.62">
    <stop offset="0" stop-color="#3B1A4F" stop-opacity="0.85"/>
    <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
  </radialGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="4" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.05 0"/>
  </filter>
  <clipPath id="panel"><rect width="{w}" height="{h}" rx="16"/></clipPath>
</defs>
<style>
{css}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<g clip-path="url(#panel)">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="{h}" fill="url(#glow)"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
  <rect width="{w}" height="{h}" filter="url(#grain)"/>
{body}
</g>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="15.5" fill="none" stroke="{RULE}"/>
</svg>
"""


def warn_missing():
    for k in ("serif", "serif-medium", "italic", "italic-medium", "mono", "mono-medium"):
        f = face(k)
        if f.missing:
            print(f"  {k}: no glyph for {''.join(sorted(f.missing))!r}")
