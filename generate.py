"""Generate the InvariantPlatform organization profile: README + SVG artwork.

    python3 generate.py          # writes profile/README.md and profile/assets/*.svg

Standard library only. Every claim and number here is one the public site
(invariant-platform.io) already makes; STATS and REGISTER are copied from its
site.config.ts and must move with it. Nothing names a machine or an address.

The SVGs are shown by GitHub through <img>, so each one is self-contained:
its own styles, no web fonts (system fallbacks), no script. Animations are
CSS, play once on load, and stop for readers who prefer reduced motion.
"""

from __future__ import annotations

import html
from pathlib import Path

OUT = Path(__file__).resolve().parent / "profile"

SITE = "https://invariant-platform.io"
# From invariant-platform-site/site.config.ts (ADR-173: a number the platform
# does not keep is a false claim). Update both together.
STATS = [("210", "decisions", "numbered, never deleted"), ("18", "invariants", "re-asserted nightly"),
         ("7", "rebuilds", "from a declaration"), ("2", "restore drills", "passed, not assumed"),
         ("2", "failure domains", "and what survives each")]
REGISTER = [("Topology and capacity", 20), ("Provisioning, roll and rebuild", 26), ("Networking and DNS", 21),
            ("Security and admission", 23), ("Secrets and identity", 8), ("Supply chain and releases", 17),
            ("GitOps and config delivery", 9), ("Storage, backup and disaster recovery", 17),
            ("Observability and alerting", 26), ("Workloads and migrations", 10), ("Engineering practice", 26),
            ("Site and funnel", 5)]
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
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
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
    w, h = 1280, 460
    style = """
    .line { animation: in .35s ease-out backwards; }
    @keyframes in { from { opacity: 0; transform: translateX(-6px); } }
    .cursor { animation: blink 1.1s steps(1) infinite; }
    @keyframes blink { 50% { opacity: 0; } }
    .pulse { animation: pulse 2.4s ease-in-out infinite; transform-origin: center; transform-box: fill-box; }
    @keyframes pulse { 50% { opacity: .35; } }
    """
    # the posture signal: a trace that runs flat, spikes at each check, and
    # carries on; the instrument's own heartbeat behind the headline
    pts, x = [], 40.0
    beat = [0, -4, 6, -26, 30, -10, 0]
    while x < 680:
        pts.append((x, 432))
        if int(x) % 160 == 40:
            for k, dy in enumerate(beat):
                pts.append((x + 6 + k * 5, 432 + dy))
            x += 40
        x += 20
    sig = "M " + " L ".join(f"{a:.0f} {b:.0f}" for a, b in pts)
    ticks = "".join(f"M {xx} 452 L {xx} {448 if xx % 80 else 444} " for xx in range(40, 690, 10))
    b = [f'<path d="{ticks}" stroke="#8b939e" stroke-opacity=".35"/>',
         trace(sig, 0, pulse=True, marker=False),
         logo(64, 56, 1.0),
         f'<text x="128" y="96" class="mono" font-size="40" font-weight="600" letter-spacing="-1">invariant</text>',
         f'<text x="352" y="96" class="label" font-size="15">PLATFORM</text>',
         f'<text x="64" y="186" font-size="44" font-weight="700" letter-spacing="-1">A control you cannot</text>',
         f'<text x="64" y="240" font-size="44" font-weight="700" letter-spacing="-1"><tspan fill="{AMBER}" filter="url(#glow)">verify</tspan> is not a control.</text>']
    lede = ("A small, security-first Kubernetes platform that re-asserts its own posture every night, "
            "from outside itself, and whose only repair is a rebuild from a declaration.")
    for i, ln in enumerate(wrap(lede, 62)):
        b.append(f'<text x="64" y="{292 + i * 26}" font-size="18" fill="#a3acb8">{esc(ln)}</text>')
    # chips
    cx = 64
    for label, hue in (("rebuilt, never repaired", 1), ("signed end to end", 2), ("checked nightly", 4)):
        wd = len(label) * 8.2 + 30
        b.append(f'<rect x="{cx}" y="366" width="{wd}" height="30" rx="2" fill="{HUES[hue]}" fill-opacity=".08" stroke="{HUES[hue]}" stroke-opacity=".55"/>'
                 f'<rect x="{cx + 11}" y="377" width="8" height="8" fill="{HUES[hue]}" filter="url(#glow)" class="pulse"/>'
                 f'<text x="{cx + 26}" y="386" class="mono" font-size="13" fill="{HUES[hue]}">{esc(label)}</text>')
        cx += wd + 12
    # terminal
    tx, ty, tw, th = 712, 48, 520, 372
    b.append(card(tx, ty, tw, th, 0, tag="CH-01 · POSTURE · NIGHTLY"))
    b.append(f'<rect x="{tx + 3}" y="{ty + 1}" width="{tw - 4}" height="38" fill="#121820"/>'
             f'<path d="M {tx + 3} {ty + 39} L {tx + tw - 1} {ty + 39}" stroke="{AMBER}" stroke-opacity=".3"/>')
    for i, c in enumerate((ROSE, AMBER_L, EMERALD)):
        b.append(f'<rect x="{tx + 20 + i * 18}" y="{ty + 15}" width="9" height="9" fill="{c}" filter="url(#glow)"/>')
    b.append(f'<text x="{tx + 90}" y="{ty + 25}" class="mono" font-size="12.5" fill="#7c8794">from the host tier · read-only identity</text>')
    b.append(f'<text x="{tx + 24}" y="{ty + 72}" class="mono" font-size="14"><tspan fill="{EMERALD}">$</tspan> posture-check</text>')
    for i, (st, line) in enumerate(POSTURE):
        y = ty + 100 + i * 24
        ok = st == "ok"
        col = EMERALD if ok else ROSE
        tag = " ok " if ok else "FAIL"
        b.append(f'<g class="line" style="animation-delay:{0.35 + i * 0.22:.2f}s">'
                 f'<rect x="{tx + 22}" y="{y - 14}" width="42" height="19" rx="1" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".5"/>'
                 f'<text x="{tx + 43}" y="{y}" class="mono" font-size="12" font-weight="700" fill="{col}" text-anchor="middle">{tag}</text>'
                 f'<text x="{tx + 76}" y="{y}" class="mono" font-size="13" fill="{"#dbe2ea" if ok else "#fda4af"}">{esc(line)}</text></g>')
    y = ty + 100 + len(POSTURE) * 24 + 10
    d = 0.35 + len(POSTURE) * 0.22
    b.append(f'<g class="line" style="animation-delay:{d:.2f}s"><text x="{tx + 24}" y="{y}" class="mono" font-size="13.5" fill="{AMBER_L}">'
             f'9 of 10 shown hold · 1 finding, paged</text></g>')
    b.append(f'<rect x="{tx + 24}" y="{y + 12}" width="9" height="16" fill="{AMBER}" class="cursor"/>')
    return doc(w, h, "Invariant Platform: a control you cannot verify is not a control", "".join(b), style)


def stats() -> str:
    w, h = 1280, 170
    b = []
    cw, gap = 226, 22
    for i, (n, label, sub) in enumerate(STATS):
        x = 32 + i * (cw + gap)
        hue = [0, 4, 1, 2, 3][i]
        b.append(card(x, 30, cw, 112, hue))
        b.append(f'<text x="{x + 22}" y="{26 + 54}" class="mono" font-size="40" font-weight="700" fill="{HUES[hue]}" filter="url(#glow)">{n}</text>')
        b.append(f'<text x="{x + 24 + len(n) * 25 + 10}" y="{26 + 52}" class="mono" font-size="13" font-weight="600" letter-spacing=".08em">{esc(label.upper())}</text>')
        b.append(f'<text x="{x + 22}" y="{26 + 88}" font-size="13.5" fill="#a3acb8">{esc(sub)}</text>')
    return doc(w, h, "210 decisions, 18 invariants, 7 rebuilds, 2 restore drills, 2 failure domains", "".join(b))


ICONS = {
    # simple line icons on a 28-unit grid
    "arch": '<rect x="2" y="2" width="10" height="10" rx="2"/><rect x="16" y="2" width="10" height="10" rx="2"/><rect x="9" y="16" width="10" height="10" rx="2"/><path d="M7 12 L14 16 M21 12 L14 16"/>',
    "shield": '<path d="M14 2 L25 6 V14 C25 20 20 25 14 27 C8 25 3 20 3 14 V6 Z"/><path d="M9 14 L13 18 L20 10"/>',
    "rebuild": '<path d="M24 14 A10 10 0 1 1 20 6"/><path d="M20 1 V7 H26"/>',
    "pulse": '<path d="M2 15 H8 L11 7 L16 23 L19 15 H26"/>',
    "chain": '<rect x="2" y="9" width="12" height="10" rx="5"/><rect x="14" y="9" width="12" height="10" rx="5"/><path d="M10 14 H18"/>',
}
PILLARS = [
    ("Architecture", "arch", 1, "Every component is modelled before it exists. A component the model does not describe fails the build."),
    ("Security posture", "shield", 3, "Eighteen invariants, re-asserted nightly from outside the cluster. A failure pages; silence is a written-down gap."),
    ("Resiliency", "rebuild", 4, "No repair path. Anything broken is destroyed and rebuilt from a declaration, and every rebuild is measured."),
    ("Observability", "pulse", 2, "Metrics, logs and alert rules live beside the cluster. A monitor inside the thing cannot report it gone."),
    ("Supply chain", "chain", 0, "Nothing reaches the cluster except a signed artifact from one named workflow. A push deploys nothing."),
]


def pillars() -> str:
    w, h = 1280, 330
    b = [f'<text x="32" y="44" class="label">FIVE PROPERTIES · EACH ONE CHECKED, NOT CLAIMED</text>']
    cw, gap = 226, 22
    for i, (title, icon, hue, body) in enumerate(PILLARS):
        x, y = 32 + i * (cw + gap), 70
        c = HUES[hue]
        b.append(card(x, y, cw, 222, hue, tag=f"P-{i + 1:02d}"))
        b.append(f'<rect x="{x + 18}" y="{y + 22}" width="48" height="48" rx="2" fill="{c}" fill-opacity=".08" stroke="{c}" stroke-opacity=".5"/>')
        b.append(f'<g transform="translate({x + 28} {y + 32})" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)">{ICONS[icon]}</g>')
        b.append(f'<text x="{x + 22}" y="{y + 102}" class="mono" font-size="16.5" font-weight="700">{esc(title)}</text>')
        for j, ln in enumerate(wrap(body, 27)):
            b.append(f'<text x="{x + 22}" y="{y + 130 + j * 20}" font-size="13.5" fill="#a3acb8">{esc(ln)}</text>')
    return doc(w, h, "Five properties: architecture, security posture, resiliency, observability, supply chain", "".join(b))


def flow() -> str:
    w, h = 1280, 360
    steps = [
        ("A reviewed change", "signed commit, pinned versions; tests are a gate", 5),
        ("One named workflow", "builds once, signs keyless; SBOM + provenance", 2),
        ("A private registry", "immutable tags; nothing is ever called latest", 0),
        ("The cluster verifies", "signature against one pinned identity, then applies and prunes", 4),
    ]
    b = [f'<text x="32" y="44" class="label">HOW A CHANGE REACHES THE CLUSTER · ONE DIRECTION</text>']
    cw, gap, y = 262, 64, 92
    for i, (t, sub, hue) in enumerate(steps):
        x = 32 + i * (cw + gap)
        b.append(card(x, y, cw, 128, hue, tag=f"STAGE {i + 1}"))
        b.append(f'<text x="{x + 22}" y="{y + 46}" class="mono" font-size="17" font-weight="700">{esc(t)}</text>')
        for j, ln in enumerate(wrap(sub, 31)):
            b.append(f'<text x="{x + 22}" y="{y + 74 + j * 19}" font-size="13.5" fill="#a3acb8">{esc(ln)}</text>')
        if i:
            x0, x1 = x - gap + 4, x - 8
            b.append(trace(f"M {x0} {y + 64} L {x1} {y + 64}", 0))
    # the path that does not exist
    py = 290
    b.append(trace(f"M 163 {y + 136} L 163 {py} L 1100 {py} L 1100 {y + 140}", 3, pulse=False, dashed=True))
    b.append(f'<rect x="630" y="{py - 10}" width="20" height="20" rx="2" fill="#0b0d10" stroke="{ROSE}" stroke-width="1.6" filter="url(#glow)"/>'
             f'<path d="M 636 {py - 4} L 644 {py + 4} M 644 {py - 4} L 636 {py + 4}" stroke="{ROSE}" stroke-width="2.2" stroke-linecap="square"/>')
    b.append(f'<rect x="676" y="{py - 13}" width="476" height="26" rx="2" fill="#0b0d10"/>')
    b.append(f'<text x="684" y="{py + 5}" class="mono" font-size="14" font-weight="600" fill="#fda4af">git push → cluster: no such path. A push deploys nothing.</text>')
    return doc(w, h, "How a change reaches the cluster: reviewed change, named workflow, private registry, verifying cluster", "".join(b))


def register() -> str:
    cell, gap, label_w, row_h = 17, 4, 384, 28
    w = 1280
    h = 86 + len(REGISTER) * row_h + 40
    b = [f'<text x="32" y="44" class="label">THE DECISION REGISTER · ONE SQUARE = ONE DECISION</text>',
         f'<text x="{w - 32}" y="44" class="label" text-anchor="end">THE SHAPE IS PUBLIC · THE DECISIONS ARE FOR MEMBERS</text>']
    y = 76
    for i, (name, n) in enumerate(REGISTER):
        b.append(f'<rect x="35" y="{y + 4}" width="10" height="10" fill="{HUES[i]}" filter="url(#glow)"/>')
        b.append(f'<text x="56" y="{y + 14}" class="mono" font-size="12.5" fill="{HUES[i]}">{i + 1:02d}</text>')
        b.append(f'<text x="86" y="{y + 14}" font-size="14">{esc(name)}</text>')
        b.append(f'<text x="{label_w}" y="{y + 14}" class="mono" font-size="13" fill="#7c8794" text-anchor="end">{n}</text>')
        for j in range(n):
            x = label_w + 20 + j * (cell + gap)
            b.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="1.5" fill="url(#cell{i})" filter="url(#glow)" class="line" style="animation-delay:{(i * 0.05 + j * 0.012):.3f}s"/>')
        y += row_h
    b.append(f'<text x="{w - 32}" y="{h - 22}" class="mono" font-size="14" fill="{AMBER_L}" text-anchor="end">twelve categories · every entry numbered · nothing deleted</text>')
    style = ".line { animation: in .3s ease-out backwards; } @keyframes in { from { opacity: 0; } }"
    return doc(w, h, "The decision register: every decision, in twelve categories", "".join(b), style)


def members() -> str:
    w, h = 1280, 230
    b = [card(32, 30, w - 64, 168, 0, tag="MEMBERSHIP · FREE"),
         logo(70, 62, 1.25),
         f'<text x="150" y="98" font-size="30" font-weight="700" letter-spacing="-.5">The whole story is free.</text>',
         f'<text x="150" y="134" font-size="30" font-weight="700" letter-spacing="-.5" fill="{AMBER}">It just isn\'t anonymous.</text>',
         f'<text x="150" y="168" font-size="15.5" fill="#a3acb8">Join the organization and leave an email: field notes, the full decision register, and how every check is enforced.</text>']
    bx = w - 300
    b.append(f'<rect x="{bx}" y="84" width="220" height="56" rx="2" fill="{AMBER}" filter="url(#glow)"/>'
             f'<text x="{bx + 110}" y="119" class="mono" font-size="17" font-weight="700" fill="#0b0d10" text-anchor="middle">JOIN  →</text>')
    return doc(w, h, "The whole story is free. It just isn't anonymous. Join.", "".join(b))


README = f"""<p align="center">
  <a href="{SITE}"><img src="assets/hero.svg" width="100%" alt="Invariant Platform: a control you cannot verify is not a control. A nightly posture check, nine invariants holding and one finding paged."></a>
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

<p align="center"><img src="assets/stats.svg" width="100%" alt="210 decisions, 18 invariants, 7 rebuilds, 2 restore drills, 2 failure domains"></p>

A property asserted in a document is not a property until something outside the system checks it, on a schedule, and pages when it stops being true. Invariant Platform is a small Kubernetes platform built on that rule: every claim on the site is one it checks, every night, from outside itself.

<p align="center"><img src="assets/pillars.svg" width="100%" alt="Five properties: architecture modelled first; eighteen invariants checked nightly; rebuilt never repaired; observability beside the cluster; only signed artifacts deploy"></p>

<p align="center"><img src="assets/flow.svg" width="100%" alt="A reviewed change, built and signed by one named workflow, held in a private registry, verified by the cluster before it applies. A git push alone deploys nothing."></p>

<p align="center"><img src="assets/register.svg" width="100%" alt="The decision register: every decision as one square, across twelve categories"></p>

<p align="center">
  <a href="{SITE}/join/"><img src="assets/members.svg" width="100%" alt="The whole story is free. It just isn't anonymous. Join the organization."></a>
</p>

<p align="center"><sub>Built and run by <a href="https://www.bradpenney.io">Brad Penney</a>. Membership is free: no cost, no seat count, no card, and leaving is one click.</sub></p>
"""


def main() -> None:
    assets = OUT / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for name, fn in (("hero", hero), ("stats", stats), ("pillars", pillars), ("flow", flow), ("register", register), ("members", members)):
        (assets / f"{name}.svg").write_text(fn())
    (OUT / "README.md").write_text(README)
    print(f"wrote {OUT / 'README.md'} and 6 SVGs")


if __name__ == "__main__":
    main()
