"""Generate the InvariantPlatform organization profile: README + SVG artwork.

    python3 generate.py          # writes profile/README.md and profile/assets/*.svg

Standard library only. Every claim and number here is one the public site
(invariant-platform.io) already makes. REGISTER is read from the site
repository's content/register-shape.json (generated from the private index),
and the decision total is its sum, so the two sites cannot disagree. There is
no invariant count: only the live nightly run states one. Nothing names a
machine or an address.

The SVGs are shown by GitHub through <img>, so each one is self-contained:
its own styles, no web fonts (system fallbacks), no script. Animations are
CSS, play once on load, and stop for readers who prefer reduced motion.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "profile"

SITE = "https://invariant-platform.io"
# The register's shape, from the site repository (scripts/register-shape.mjs
# there writes it). A missing file is an error, never a stale fallback.
_SHAPE = Path(__file__).resolve().parent.parent / "invariant-platform-site" / "content" / "register-shape.json"
REGISTER = [(c["name"], c["n"]) for c in json.loads(_SHAPE.read_text())]
DECISION_COUNT = sum(n for _, n in REGISTER)
# Kept by the platform and stated on the site (site.config.ts, ADR-173).
STATS = [(str(DECISION_COUNT), "decisions", "numbered, never deleted"),
         ("7", "rebuilds", "from a declaration"), ("2", "restore drills", "passed, not assumed"),
         ("2", "failure domains", "and what survives each")]
# A real nightly run, finding included (content/home.ts postureRun).
POSTURE = [
    ("ok", "pod security: 19/19 namespaces enforced"),
    ("ok", "network policy: 19 namespaces default-deny"),
    ("ok", "admission: 2 policies, 2 enforcing Deny"),
    ("ok", "cluster-admin: 5 subjects, all expected"),
    ("ok", "flux: 5 kustomizations reconciling"),
    ("ok", "supply chain: signature verified, pinned identity"),
    ("ok", "credentials: 8 external secrets syncing"),
    ("ok", "origin lock: direct bypass refused (000)"),
    ("ok", "selinux: both hypervisors enforcing"),
    ("FAIL", "systemd degraded; unit not on the watch list"),
]

AMBER, AMBER_L, CYAN, VIOLET, ROSE, EMERALD, BLUE = "#f59e0b", "#fbbf24", "#22d3ee", "#a78bfa", "#fb7185", "#34d399", "#60a5fa"
HUES = [AMBER, CYAN, VIOLET, ROSE, EMERALD, BLUE, "#f472b6", "#facc15", "#2dd4bf", "#c084fc", "#fb923c", "#4ade80"]
SANS = "'Segoe UI', 'Inter', 'Helvetica Neue', system-ui, -apple-system, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', 'Cascadia Code', Menlo, Consolas, ui-monospace, monospace"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def wrap(text: str, chars: int) -> list[str]:
    out, line = [], ""
    for w in text.split():
        if line and len(line) + 1 + len(w) > chars:
            out.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    return out + ([line] if line else [])


def doc(w: int, h: int, title: str, body: str, style: str = "", defs: str = "") -> str:
    base = f"""
    text {{ font-family: {SANS}; fill: #e6e8eb; }}
    .mono {{ font-family: {MONO}; }}
    .label {{ font-family: {MONO}; font-size: 12px; letter-spacing: .2em; fill: #7c8794; }}
    .flow {{ fill: none; stroke-width: 3.2; stroke-linecap: round; stroke-dasharray: 14 1400; stroke-dashoffset: 14;
            animation: flow 2.6s cubic-bezier(.5, 0, .5, 1) infinite; }}
    @keyframes flow {{ 0% {{ stroke-dashoffset: 14; stroke-opacity: 0; }} 12% {{ stroke-opacity: 1; }}
            88% {{ stroke-opacity: 1; }} 100% {{ stroke-dashoffset: -420; stroke-opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .flow {{ display: none; }} }}
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">'
        f"<title>{esc(title)}</title><defs><style>{base}{style}</style>{common_defs(w, h)}{defs}</defs>"
        f'<rect width="{w}" height="{h}" rx="4" fill="#0b0d10"/>'
        f'<rect width="{w}" height="{h}" rx="4" fill="url(#bg)"/>'
        f'<rect width="{w}" height="{h}" rx="4" fill="url(#grid)"/>'
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="4" fill="none" stroke="#2a3138"/>'
        + "".join(f'<path d="M {cx} {cy + dy * 14} L {cx} {cy} L {cx + dx * 14} {cy}" fill="none" stroke="{AMBER}" stroke-opacity=".7" stroke-width="1.5"/>'
                  for cx, cy, dx, dy in ((8, 8, 1, 1), (w - 8, 8, -1, 1), (8, h - 8, 1, -1), (w - 8, h - 8, -1, -1)))
        + f"{body}</svg>"
    )


def common_defs(w: int, h: int) -> str:
    out = [
        '<radialGradient id="bg" cx="12%" cy="0%" r="95%"><stop offset="0" stop-color="#f59e0b" stop-opacity=".16"/>'
        '<stop offset=".45" stop-color="#22d3ee" stop-opacity=".05"/><stop offset="1" stop-color="#0b0d10" stop-opacity="0"/></radialGradient>',
        '<filter id="shadow" x="-20%" y="-20%" width="140%" height="170%"><feDropShadow dx="0" dy="12" stdDeviation="12" flood-color="#000" flood-opacity=".6"/></filter>',
        # userSpaceOnUse: a blur on a straight line has a zero-height box otherwise
        f'<filter id="glow" filterUnits="userSpaceOnUse" x="-20" y="-20" width="{w + 40}" height="{h + 40}"><feGaussianBlur stdDeviation="3.2" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        '<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".11"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
        '<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0 L0 0 0 24" fill="none" stroke="#8b939e" stroke-opacity=".07"/></pattern>',
    ]
    for i, c in enumerate(HUES):
        out.append(
            f'<linearGradient id="face{i}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c}" stop-opacity=".12"/>'
            f'<stop offset=".6" stop-color="{c}" stop-opacity=".02"/></linearGradient>'
            f'<linearGradient id="cell{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}"/>'
            f'<stop offset="1" stop-color="{c}" stop-opacity=".62"/></linearGradient>'
            f'<marker id="head{i}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>'
        )
    return "".join(out)


def card(x: float, y: float, w: float, h: float, hue: int, depth: float = 0, dashed: bool = False, tag: str = "") -> str:
    """An instrument module: square, hairline, corner brackets and a lit left rule."""
    c = HUES[hue]
    dash = ' stroke-dasharray="6 5"' if dashed else ""
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="#0c1015"/>'
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="url(#face{hue})" stroke="{c}" stroke-opacity=".3"{dash}/>'
           f'<rect x="{x}" y="{y + 10}" width="3" height="{h - 20}" fill="{c}" filter="url(#glow)"/>')
    b = 11
    for cx, cy, dx, dy in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        out += f'<path d="M {cx + dx * b} {cy} L {cx} {cy} L {cx} {cy + dy * b}" fill="none" stroke="{c}" stroke-width="1.8"/>'
    if tag:
        out += f'<text x="{x + 14}" y="{y - 8}" class="mono" font-size="11" letter-spacing=".18em" fill="{c}">{esc(tag)}</text>'
    return out


def trace(d: str, hue: int, pulse: bool = True, dashed: bool = False, marker: bool = True) -> str:
    """A signal trace: glow, bright core, and a travelling pulse on working paths."""
    c = HUES[hue]
    da = ' stroke-dasharray="6 6"' if dashed else ""
    mk = f' marker-end="url(#head{hue})"' if marker else ""
    out = (f'<path d="{d}" fill="none" stroke="{c}" stroke-opacity="{.25 if dashed else .55}" stroke-width="5" filter="url(#glow)"/>'
           f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.8"{da}{mk}/>')
    if pulse:
        out += f'<path d="{d}" class="flow" stroke="#fff7e0"/>'
    return out


def logo(x: float, y: float, scale: float = 1.0) -> str:
    return (f'<g transform="translate({x} {y}) scale({scale})">'
            f'<path d="M10 6 L40 34 L10 62" fill="none" stroke="{AMBER}" stroke-width="14" stroke-opacity=".35" filter="url(#glow)"/>'
            f'<path d="M10 6 L40 34 L10 62" fill="none" stroke="{AMBER}" stroke-width="10" stroke-linecap="square"/></g>')


# ---------------------------------------------------------------------------
def hero() -> str:
    """The one image: a banner, large type only, so it still reads at phone width.
    The register's shape sits on the right as an LED matrix, one square per decision."""
    w, h = 1280, 400
    style = """
    .cell { animation: in .3s ease-out backwards; }
    @keyframes in { from { opacity: 0; } }
    .pulse { animation: pulse 2.4s ease-in-out infinite; transform-origin: center; transform-box: fill-box; }
    @keyframes pulse { 50% { opacity: .35; } }
    """
    pts, x = [], 0.0
    beat = [0, -4, 6, -26, 30, -10, 0]
    while x < w:
        pts.append((x, 360))
        if int(x) % 200 == 100:
            for k, dy in enumerate(beat):
                pts.append((x + 6 + k * 5, 360 + dy))
            x += 40
        x += 20
    sig = "M " + " L ".join(f"{a:.0f} {b:.0f}" for a, b in pts)
    b = [trace(sig, 0, pulse=True, marker=False),
         logo(64, 52, 0.9),
         f'<text x="122" y="88" class="mono" font-size="36" font-weight="600" letter-spacing="-1">invariant</text>',
         f'<text x="326" y="88" class="label" font-size="15">PLATFORM</text>',
         f'<text x="64" y="186" font-size="52" font-weight="700" letter-spacing="-1.5">A security posture that</text>',
         f'<text x="64" y="250" font-size="52" font-weight="700" letter-spacing="-1.5"><tspan fill="{AMBER}" filter="url(#glow)">proves</tspan> itself.</text>']
    cx = 64
    for label, hue in (("rebuilt, never repaired", 1), ("signed end to end", 2), ("checked nightly", 4)):
        wd = len(label) * 9.6 + 34
        b.append(f'<rect x="{cx}" y="290" width="{wd}" height="34" rx="2" fill="{HUES[hue]}" fill-opacity=".08" stroke="{HUES[hue]}" stroke-opacity=".55"/>'
                 f'<rect x="{cx + 12}" y="303" width="9" height="9" fill="{HUES[hue]}" filter="url(#glow)" class="pulse"/>'
                 f'<text x="{cx + 29}" y="313" class="mono" font-size="15" fill="{HUES[hue]}">{esc(label)}</text>')
        cx += wd + 12
    cell, gap, x0, y0 = 13, 4, 770, 60
    for i, (_, n) in enumerate(REGISTER):
        for j in range(n):
            b.append(f'<rect x="{x0 + j * (cell + gap)}" y="{y0 + i * (cell + gap)}" width="{cell}" height="{cell}" rx="1" '
                     f'fill="url(#cell{i})" fill-opacity=".85" class="cell" style="animation-delay:{(i * 0.04 + j * 0.01):.2f}s"/>')
    b.append(f'<text x="{x0}" y="{y0 + len(REGISTER) * (cell + gap) + 22}" class="label">THE DECISION REGISTER · ONE SQUARE PER DECISION</text>')
    return doc(w, h, "Invariant Platform: a security posture that proves itself", "".join(b), style)


RAW = "https://raw.githubusercontent.com/InvariantPlatform/.github/main/profile/assets"


def pic(name: str, alt: str) -> str:
    """The animated SVG for browsers; the PNG for renderers that cannot show SVG (the GitHub
    mobile app shows only the alt text). Absolute URLs: relative ones resolve differently per client."""
    return (f'<picture><source srcset="{RAW}/{name}.svg" type="image/svg+xml">'
            f'<img src="{RAW}/{name}.png" width="100%" alt="{alt}"></picture>')


PILLARS = [
    ("Architecture", "architecture", "Every component is modelled before it exists. A component the model does not describe fails the build."),
    ("Security posture", "security-posture", "Every invariant, re-asserted nightly from outside the cluster. A failure pages; silence is a written-down gap."),
    ("Resiliency", "resiliency", "No repair path. Anything broken is destroyed and rebuilt from a declaration, and every rebuild is measured."),
    ("Observability", "observability", "Metrics, logs and alert rules live beside the cluster. A monitor inside the thing cannot report it gone."),
    ("Supply chain", "supply-chain", "Nothing reaches the cluster except a signed artifact from one named workflow. A push deploys nothing."),
]
FLOW = [
    ("A reviewed change", "signed commit, pinned versions; tests are a gate"),
    ("One named workflow", "builds once and signs keyless, with an SBOM and provenance"),
    ("A private registry", "immutable tags; nothing is ever called latest"),
    ("The cluster verifies", "the signature against one pinned identity, then applies and prunes"),
]
STATS_TABLE = ("| " + " | ".join(f"**{n}**" for n, _, _ in STATS) + " |\n|"
               + ":-:|" * len(STATS) + "\n| "
               + " | ".join(f"{label}<br><sub>{sub}</sub>" for _, label, sub in STATS) + " |")
POSTURE_BLOCK = "\n".join(("+ ok    " if st == "ok" else "- FAIL  ") + line for st, line in POSTURE)
PILLAR_ROWS = "\n".join(f"| **[{t}]({SITE}/{slug}/)** | {body} |" for t, slug, body in PILLARS)
FLOW_STEPS = "\n".join(f"{i}. **{t}**: {sub}." for i, (t, sub) in enumerate(FLOW, 1))
CATEGORIES = len(REGISTER)


README = f"""<p align="center">
  <a href="{SITE}">{pic('hero', 'Invariant Platform: a security posture that proves itself.')}</a>
</p>

<p align="center">
  <a href="{SITE}"><b>invariant-platform.io</b></a> &nbsp;·&nbsp;
  <a href="{SITE}/architecture/">Architecture</a> &nbsp;·&nbsp;
  <a href="{SITE}/security-posture/">Security posture</a> &nbsp;·&nbsp;
  <a href="{SITE}/resiliency/">Resiliency</a> &nbsp;·&nbsp;
  <a href="{SITE}/observability/">Observability</a> &nbsp;·&nbsp;
  <a href="{SITE}/supply-chain/">Supply chain</a> &nbsp;·&nbsp;
  <a href="{SITE}/join/"><b>Join</b></a>
</p>

Invariant Platform is a security-first Kubernetes platform that re-asserts its own security posture every night, from outside itself, and whose only repair is a rebuild from a declaration. Every property it claims is one it checks. The checks ask the cluster's own API and compare the answer with the declaration, not with a list of machines, so they ask the same questions of five nodes as of a thousand.

{STATS_TABLE}

## Every night, from outside the cluster

A real run, finding included. A failure pages; silence is a written-down gap.

```diff
$ posture-check
{POSTURE_BLOCK}
```

## Five properties, each one checked

| Property | How it is held |
|---|---|
{PILLAR_ROWS}

## How a change reaches the cluster

{FLOW_STEPS}

> [!IMPORTANT]
> There is no path from `git push` to the cluster. A push deploys nothing; only a signed artifact from the one named workflow does.

## The whole story is free. It just isn't anonymous.

Members get a field note from a real incident every Thursday, the decision register ({DECISION_COUNT} decisions in {CATEGORIES} categories, every one numbered, none deleted, released a few each week), the architecture views, and read access to the platform's source. Membership costs nothing: no seat count, no card, and leaving is one click. It opens soon.

**[Membership →]({SITE}/join/)**

<sub>Built and run by <a href="https://www.bradpenney.io">Brad Penney</a>.</sub>
"""


def main() -> None:
    assets = OUT / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for name, fn in (("hero", hero),):
        (assets / f"{name}.svg").write_text(fn())
    (OUT / "README.md").write_text(README)
    print(f"wrote {OUT / 'README.md'} and the banner SVG")


if __name__ == "__main__":
    main()
