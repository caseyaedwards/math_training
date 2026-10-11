"""Graph theory: the bridges of Königsberg, vertex degrees, and Euler paths."""

from __future__ import annotations

import math
from collections import Counter, defaultdict

from .. import theme
from ..registry import diagram
from ..svg import fmt
from ..walkthrough import Walkthrough

BRIDGE, ODD, EVEN, PATH = theme.ORANGE, theme.RED, theme.GREEN, theme.BLUE


def degrees(edges) -> Counter:
    d = Counter()
    for a, b in edges:
        d[a] += 1
        d[b] += 1
    return d


def euler_path(edges, start):
    """Hierholzer's algorithm. Returns the edge indices in walking order."""
    adj = defaultdict(list)
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, i))
        adj[b].append((a, i))
    used = set()
    stack = [(start, None)]
    out = []
    while stack:
        v, e = stack[-1]
        while adj[v] and adj[v][-1][1] in used:
            adj[v].pop()
        if adj[v]:
            w, i = adj[v].pop()
            used.add(i)
            stack.append((w, i))
        else:
            stack.pop()
            if e is not None:
                out.append(e)
    out.reverse()
    assert len(out) == len(edges)
    return out


def draw_edges(c, pos, edges, color=BRIDGE, width=3, labels=None):
    """Draws edges, bending repeated pairs apart. Returns each edge's midpoint and bend control point."""
    seen = Counter()
    total = Counter(tuple(sorted(e)) for e in edges)
    mids = []
    for i, (a, b) in enumerate(edges):
        key = tuple(sorted((a, b)))
        k = seen[key]
        seen[key] += 1
        n = total[key]
        bend = 0 if n == 1 else (k - (n - 1) / 2) * 0.55
        (x1, y1), (x2, y2) = pos[key[0]], pos[key[1]]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        cx, cy = mx - dy * bend, my + dx * bend
        col = color(i) if callable(color) else color
        c.path(f"M{fmt(x1)},{fmt(y1)} Q{fmt(cx)},{fmt(cy)} {fmt(x2)},{fmt(y2)}", color=col, width=width)
        mids.append((0.25 * x1 + 0.5 * cx + 0.25 * x2, 0.25 * y1 + 0.5 * cy + 0.25 * y2))
    return mids


def draw_vertices(c, pos, ring=None, r=18):
    for v, (x, y) in pos.items():
        col = (ring or {}).get(v, theme.INK)
        c.circle(x, y, r, color=col, fill=theme.PAPER, width=2.5)
        c.text(x, y, v, size=16, weight="bold", color=col)


@diagram("euler-paths", "Euler Paths and the Königsberg Bridges", "Discrete Math")
def build() -> Walkthrough:
    # A north bank, B south bank, C the island, D the east land
    edges7 = [("A", "C"), ("A", "C"), ("B", "C"), ("B", "C"), ("A", "D"), ("B", "D"), ("C", "D")]
    edges8 = edges7 + [("B", "D")]
    deg7, deg8 = degrees(edges7), degrees(edges8)
    odd7 = sorted(v for v in deg7 if deg7[v] % 2)
    odd8 = sorted(v for v in deg8 if deg8[v] % 2)
    assert len(odd7) == 4 and len(odd8) == 2
    walk = euler_path(edges8, odd8[0])

    wt = Walkthrough(
        "euler-paths", "Euler Paths and the Königsberg Bridges", "Discrete Math",
        concept="Euler path exists  \\iff  0 or 2 vertices of odd degree (connected graph)",
        summary="Turn land into dots and bridges into lines. A walk that crosses every bridge once exists only "
                "when zero or two dots have an odd number of lines.",
        width=700, height=480, level="301",
    )
    GPOS = {"A": (545, 70), "B": (545, 340), "C": (450, 205), "D": (650, 205)}

    # map geometry
    MX0, MX1, MY0, MY1 = 20, 330, 40, 370
    NORTH = (110, 145)  # north channel y range
    SOUTH = (255, 290)
    WEST = (20, 60)  # merged river x range west of the island
    GAPX = (230, 262)  # channel between island and east land
    bridges = {
        ("A", "C", 0): (100, "v", NORTH), ("A", "C", 1): (180, "v", NORTH),
        ("B", "C", 0): (100, "v", SOUTH), ("B", "C", 1): (180, "v", SOUTH),
        ("A", "D", 0): (296, "v", NORTH), ("B", "D", 0): (283, "v", SOUTH),
        ("C", "D", 0): (200, "h", GAPX), ("B", "D", 1): (314, "v", SOUTH),
    }

    def draw_map(c, edges, new=None):
        c.rect(MX0, MY0, MX1 - MX0, MY1 - MY0, color=theme.MUTED, fill=theme.fill(theme.GREEN, "14"), width=1)
        with c.group(opacity=0.45):
            for x, y, w, h in [(MX0, NORTH[0], MX1 - MX0, NORTH[1] - NORTH[0]),
                               (MX0, SOUTH[0], MX1 - MX0, SOUTH[1] - SOUTH[0]),
                               (WEST[0], NORTH[0], WEST[1] - WEST[0], SOUTH[1] - NORTH[0]),
                               (GAPX[0], NORTH[0], GAPX[1] - GAPX[0], SOUTH[1] - NORTH[0])]:
                c.rect(x, y, w, h, color="none", fill=theme.SKY)
        c.text(175, 75, "A  north bank", size=14, weight="bold")
        c.text(175, 330, "B  south bank", size=14, weight="bold")
        c.text(145, 200, "C  island", size=14, weight="bold")
        c.text(296, 200, "D", size=14, weight="bold")
        c.text(296, 218, "east", size=11, color=theme.SOFT_INK)
        c.text(40, 200, "river", size=11, color=theme.BLUE, transform="rotate(-90 40 200)")
        seen = Counter()
        for a, b in edges:
            key = tuple(sorted((a, b)))
            k = seen[key]
            seen[key] += 1
            at, kind, (lo, hi) = bridges[(key[0], key[1], k)]
            col = theme.GREEN if new == (key[0], key[1], k) else BRIDGE
            if kind == "v":
                c.rect(at - 6, lo - 7, 12, hi - lo + 14, color=theme.INK, fill=col, width=1.2, rx=2)
            else:
                c.rect(lo - 7, at - 6, hi - lo + 14, 12, color=theme.INK, fill=col, width=1.2, rx=2)

    @wt.step("Seven bridges, one walk", "Königsberg had four pieces of land joined by seven bridges. The town "
             "puzzle: walk across every bridge exactly once. People tried for years. Nobody managed it.", math="4 land masses, 7 bridges")
    def _(c):
        draw_map(c, edges7)
        c.text(175, 388, "orange = bridge", size=13, color=BRIDGE, weight="bold")
        if c.is_new:
            c.text(520, 120, "Can you cross every bridge", size=16, weight="bold")
            c.text(520, 144, "exactly once?", size=16, weight="bold")
            for i, line in enumerate(["A to C: 2 bridges", "B to C: 2 bridges", "A to D: 1 bridge",
                                      "B to D: 1 bridge", "C to D: 1 bridge"]):
                c.text(440, 190 + i * 26, line, size=14, anchor="start", color=BRIDGE)
            c.text(520, 330, "total: 7 bridges", size=15, weight="bold", color=BRIDGE)

    @wt.step("Turn the map into a graph", "Euler kept only what matters. Each piece of land becomes a dot "
             "(a vertex) and each bridge becomes a line (an edge). Shape and distance do not matter.",
             math="land \\to vertex,  bridge \\to edge")
    def _(c):
        c.arrow(338, 205, 388, 205, color=theme.SOFT_INK, width=2)
        draw_edges(c, GPOS, edges7)
        draw_vertices(c, GPOS)
        c.text(545, 410, "4 vertices, 7 edges", size=13, color=theme.SOFT_INK)

    BADGE = {"A": (34, -26), "B": (34, 26), "C": (-40, 0), "D": (0, -38)}

    def badges(c, deg, color_of):
        for v, (x, y) in GPOS.items():
            dx, dy = BADGE[v]
            col = color_of(v)
            c.circle(x + dx, y + dy, 13, color=col, fill=theme.fill(col, "33"), width=1.6)
            c.text(x + dx, y + dy, str(deg[v]), size=14, weight="bold", color=col)

    @wt.step("Count the edges at each vertex", "The degree of a vertex is how many edges touch it. "
             f"C has {deg7['C']}, and A, B, and D have 3 each.",
             math=f"deg A = {deg7['A']}, deg B = {deg7['B']}, deg C = {deg7['C']}, deg D = {deg7['D']}")
    def _(c):
        badges(c, deg7, lambda v: theme.INK)
        c.text(692, 120, "badge = degree", size=12, color=theme.SOFT_INK, anchor="end")

    @wt.step("A pass-through uses edges in pairs", "Each time the walk passes through a vertex, it uses one edge "
             "in and one edge out. So a middle vertex needs an even degree. Only the start and the end may be odd.",
             math="pass through: in + out = 2 edges")
    def _(c):
        c.rect(20, 404, 390, 70, color=theme.MUTED, fill=theme.PAPER, width=1, rx=8)

        def star(x, y, spec, caption, col):
            c.dot(x, y, r=6, color=theme.INK)
            for ang, kind in spec:
                a = math.radians(ang)
                ex, ey = x + 40 * math.cos(a), y - 22 * math.sin(a)
                nx, ny = x + 8 * math.cos(a), y - 8 * math.sin(a) * 0.55
                if kind == "in":
                    c.arrow(ex, ey, nx, ny, color=col, width=2)
                else:
                    c.arrow(nx, ny, ex, ey, color=col, width=2)
            c.text(x + 60, y - 9, caption[0], size=12, color=col, anchor="start", weight="bold")
            c.text(x + 60, y + 9, caption[1], size=12, color=col, anchor="start")

        star(60, 439, [(150, "in"), (210, "in"), (30, "out"), (330, "out")], ("degree 4", "in, out, in, out"), EVEN)
        star(250, 439, [(150, "in"), (210, "in"), (0, "out")], ("degree 3", "last in: stuck"), ODD)

    @wt.step("Four odd vertices: impossible", f"All four vertices have odd degree. A walk has room for at most two "
             "odd vertices, its start and its end. So no walk crosses every bridge once. Euler 1, town 0.",
             math=f"odd vertices: {', '.join(odd7)}  ({len(odd7)} > 2)")
    def _(c):
        for v in odd7:
            x, y = GPOS[v]
            c.circle(x, y, 24, color=ODD, width=3)
        badges(c, deg7, lambda v: ODD)
        c.label_box(545, 445, f"{len(odd7)} odd vertices: no Euler path", color=ODD, border=ODD, size=14)

    new_bridge = ("B", "D", 1)

    @wt.step("Add one bridge and it works", f"An eighth bridge from B to D makes B and D even. Now only A and C "
             f"are odd, so a walk exists: start at {odd8[0]}, end at {odd8[1]}, and follow the numbers.",
             math=f"odd vertices: {', '.join(odd8)}  \\implies  Euler path from {odd8[0]} to {odd8[1]}", fresh=True)
    def _(c):
        draw_map(c, edges8, new=new_bridge)
        c.text(314, 312, "new", size=11, color=theme.GREEN, weight="bold", anchor="middle")
        c.arrow(338, 205, 388, 205, color=theme.SOFT_INK, width=2)
        order = {e: k + 1 for k, e in enumerate(walk)}
        mids = draw_edges(c, GPOS, edges8, color=lambda i: theme.GREEN if i == len(edges8) - 1 else PATH)
        for i, (mx, my) in enumerate(mids):
            c.circle(mx, my, 11, color=PATH, fill=theme.PAPER, width=1.6)
            c.text(mx, my, str(order[i]), size=12, weight="bold", color=PATH)
        draw_vertices(c, GPOS, ring={v: ODD for v in odd8})
        badges(c, deg8, lambda v: ODD if deg8[v] % 2 else EVEN)
        c.text(GPOS[odd8[0]][0] - 34, GPOS[odd8[0]][1] - 4, "start", size=12, color=ODD, anchor="end",
               weight="bold")
        c.text(GPOS[odd8[1]][0] - 40, GPOS[odd8[1]][1] + 26, "end", size=12, color=ODD, weight="bold")
        c.text(545, 410, f"walk: {' → '.join(path_vertices(edges8, walk, odd8[0]))}", size=13, color=PATH)

    return wt


def path_vertices(edges, walk, start):
    out = [start]
    for i in walk:
        a, b = edges[i]
        out.append(b if out[-1] == a else a)
    return out
