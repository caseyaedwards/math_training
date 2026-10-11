"""Solid geometry: volume by stacking layers, nets and surface area."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import brace
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._geo import Oblique, centroid, num, rich, solid_face, word

BASE, HEIGHT, VOL = theme.BLUE, theme.ORANGE, theme.GREEN


def _grid_face(c, P, corner, u, v, n, m, color, width=1):
    """Draws the inner grid lines of a face spanned by n steps along u and m steps along v (world)."""
    ox, oy, oz = corner
    for i in range(1, n):
        a = (ox + u[0] * i, oy + u[1] * i, oz + u[2] * i)
        b = (a[0] + v[0] * m, a[1] + v[1] * m, a[2] + v[2] * m)
        c.line(*P(*a), *P(*b), color=color, width=width, stroke_opacity=0.7)
    for j in range(1, m):
        a = (ox + v[0] * j, oy + v[1] * j, oz + v[2] * j)
        b = (a[0] + u[0] * n, a[1] + u[1] * n, a[2] + u[2] * n)
        c.line(*P(*a), *P(*b), color=color, width=width, stroke_opacity=0.7)


def _box(c, P, W, D, H, color, grid=True, layer_color=None):
    """Draws a W x H x D box of unit cubes: front, right, and top faces."""
    front = [P(0, 0, 0), P(W, 0, 0), P(W, H, 0), P(0, H, 0)]
    right = [P(W, 0, 0), P(W, 0, D), P(W, H, D), P(W, H, 0)]
    top = [P(0, H, 0), P(W, H, 0), P(W, H, D), P(0, H, D)]
    solid_face(c, front, color, "40")
    solid_face(c, right, color, "60")
    solid_face(c, top, color, "28")
    if grid:
        _grid_face(c, P, (0, 0, 0), (1, 0, 0), (0, 1, 0), W, H, color)
        _grid_face(c, P, (W, 0, 0), (0, 0, 1), (0, 1, 0), D, H, color)
        _grid_face(c, P, (0, H, 0), (1, 0, 0), (0, 0, 1), W, D, color)
    if layer_color:
        for y in range(1, H):
            c.polyline([P(0, y, 0), P(W, y, 0), P(W, y, D)], color=layer_color, width=2)


@diagram("volume-prism-cylinder", "Volume of a Prism and a Cylinder", "Geometry")
def volume() -> Walkthrough:
    W, D, H = 4, 3, 5
    B = W * D
    r = 2
    Bc = math.pi * r * r
    wt = Walkthrough(
        "volume-prism-cylinder", "Volume of a Prism and a Cylinder", "Geometry",
        concept="V = B \\cdot h",
        summary="A prism or a cylinder is a stack of identical layers. Volume is the area of one layer, the "
                "base B, times the number of layers, the height h.",
        width=720, height=370, level="201",
    )
    P = Oblique(70, 335, 40, k=0.6, angle=40)
    CX, CY, S = 520.0, 315.0, 40.0  # cylinder: center of the bottom circle, pixels per unit
    RX, RY = r * S, r * S * 0.38  # the base circle seen at a slant is an ellipse

    def ring(y):
        return CX, CY - y * S

    def front_arc(y, n=60):
        cx, cy = ring(y)
        return [(cx + RX * math.cos(t), cy + RY * math.sin(t)) for t in (math.pi * i / n for i in range(n + 1))]

    def cylinder(c, h, layers=True):
        cx, ty = ring(h)
        body = front_arc(0) + [(CX - RX, ty), (CX + RX, ty)]
        solid_face(c, body, VOL, "40")
        c.ellipse(CX, CY, RX, RY, color=VOL, width=1.4, dash="5 4")
        c.polyline(front_arc(0), color=VOL, width=1.8)
        if layers:
            for y in range(1, h):
                c.polyline(front_arc(y), color=HEIGHT, width=2)
        c.ellipse(cx, ty, RX, RY, color="none", fill=theme.PAPER)
        c.ellipse(cx, ty, RX, RY, color=VOL, fill=theme.fill(VOL, "28"), width=1.8)

    def ghost(c):
        """Dashed outline of the finished prism, so early steps show where they are headed."""
        for a_, b_ in (((0, 0, 0), (0, H, 0)), ((W, 0, 0), (W, H, 0)), ((W, 0, D), (W, H, D)),
                       ((0, H, 0), (W, H, 0)), ((W, H, 0), (W, H, D)), ((W, H, D), (0, H, D)),
                       ((0, H, D), (0, H, 0))):
            c.line(*P(*a_), *P(*b_), color=theme.MUTED, width=1.4, dash="5 4")
        c.text(*P(W / 2, H * 0.6, 0), "the prism", size=13, color=theme.MUTED)

    def base_label(c, x, y, parts):
        rich(c, x, y, parts, size=17)

    @wt.setup
    def _(c):
        return None

    @wt.step("Find the base area", f"The prism sits on a {W} by {D} rectangle. That floor holds {B} unit "
             "squares, so the base area is B = 12.", math=f"B = {W} \\times {D} = {B}")
    def _(c):
        floor = [P(0, 0, 0), P(W, 0, 0), P(W, 0, D), P(0, 0, D)]
        c.polygon(floor, color=BASE, fill=theme.fill(BASE, "40"), width=2.5)
        _grid_face(c, P, (0, 0, 0), (1, 0, 0), (0, 0, 1), W, D, BASE)
        for x in range(W):
            for z in range(D):
                X, Y = P(x + 0.5, 0, z + 0.5)
                c.text(X, Y, str(z * W + x + 1), size=10, color=BASE)
        X, Y = P(W / 2, 0, 0)
        c.text(X, Y + 18, f"{W}", size=15, math=True, color=BASE)
        X, Y = P(W, 0, D / 2)
        c.text(X + 14, Y + 6, f"{D}", size=15, math=True, color=BASE)
        if c.is_new:
            ghost(c)
            base_label(c, P(W, 0, D)[0] + 100, P(W, 0, D)[1] + 10, [(f"B = {W} × {D} = {B}", BASE)])

    @wt.step("Build one layer", f"Put a cube on every square of the floor. One layer, one unit tall, holds "
             f"{B} cubes.", math=f"1 layer = {B} cubes")
    def _(c):
        if c.is_new:
            ghost(c)
            _box(c, P, W, D, 1, BASE)
            base_label(c, P(W, 1, D)[0] + 80, P(W, 1, D)[1] - 10, [(f"1 layer = {B} cubes", BASE)])

    @wt.step("Stack the layers", f"Stack {word(H)} identical layers to reach height h = {H}. Count layers, not "
             f"cubes: {B} cubes per layer times {H} layers.",
             math=f"V = B \\cdot h = {B} \\times {H} = {B * H}")
    def _(c):
        _box(c, P, W, D, H, BASE, layer_color=HEIGHT)
        a, b = P(0, 0, 0), P(0, H, 0)
        brace(c, *a, *b, f"h = {H}", color=HEIGHT, size=16)
        top = P(W / 2, H, D)
        rich(c, top[0], top[1] - 26, [(f"{B}", BASE), (" × ", theme.INK), (f"{H}", HEIGHT),
                                       (f" = {B * H}", VOL)], size=18)

    @wt.step("Find the base of a cylinder", f"A cylinder has a circle for a base. With radius r = {r}, "
             f"the base area is πr² = 4π, about {Bc:.2f}: almost the same as the prism floor.",
             math=f"B = \\pi r^2 = \\pi \\cdot {r}^2 \\approx {Bc:.2f}")
    def _(c):
        if not c.is_new:
            return
        c.ellipse(CX, CY, RX, RY, color=BASE, fill=theme.fill(BASE, "40"), width=2.5)
        c.line(CX, CY, CX + RX, CY, color=theme.INK, width=2)
        c.dot(CX, CY, r=3.5)
        c.text(CX + RX / 2, CY - 10, f"r = {r}", size=15, math=True, halo=True)
        rich(c, CX, CY - RY - 26, [(f"B = 4π ≈ {Bc:.2f}", BASE)], size=17)

    @wt.step("Stack circular layers", f"Stack {word(H)} disks, each with area {Bc:.2f}. The same rule works: "
             "base area times height. Prism or cylinder, the shape of the slice does not matter.",
             math=f"V = \\pi r^2 h = \\pi \\cdot {r}^2 \\cdot {H} = 20\\pi \\approx {Bc * H:.2f}")
    def _(c):
        cylinder(c, H)
        cx, ty = ring(H)
        c.line(cx, ty, cx + RX, ty, color=theme.INK, width=2)
        c.dot(cx, ty, r=3)
        c.text(cx + RX / 2, ty - 10, f"r = {r}", size=14, math=True, halo=True)
        brace(c, CX - RX - 10, CY, CX - RX - 10, ty, f"h = {H}", color=HEIGHT, size=16)
        rich(c, cx, ty - RY - 24, [(f"{Bc:.2f}", BASE), (" × ", theme.INK), (f"{H}", HEIGHT),
                                   (f" ≈ {Bc * H:.2f}", VOL)], size=18)

    return wt


# ---------------------------------------------------------------------------
# Nets and surface area
# ---------------------------------------------------------------------------


@diagram("nets-surface-area", "Nets and Surface Area", "Geometry")
def nets() -> Walkthrough:
    s = 3  # cube edge
    FB, TB, LR = theme.BLUE, theme.ORANGE, theme.GREEN  # front/back, top/bottom, left/right
    a, b, L = 3, 4, 6  # prism: right triangle legs a (vertical) and b (horizontal), length L
    hyp = math.hypot(a, b)
    rects = [(a, theme.BLUE), (b, theme.ORANGE), (hyp, theme.GREEN)]
    TRI = theme.PURPLE
    tri_area = a * b / 2
    prism_sa = sum(w * L for w, _ in rects) + 2 * tri_area
    wt = Walkthrough(
        "nets-surface-area", "Nets and Surface Area", "Geometry",
        concept="surface area = sum of the areas of all faces",
        summary="Unfold a solid into a flat net and the surface area is just the area of the net. A cube "
                "gives six equal squares; a triangular prism gives three rectangles and two triangles.",
        width=720, height=365, level="201",
    )
    P = Oblique(60, 280, 40)
    u = 26.0  # net unit in px

    def cube(c):
        front = [P(0, 0, 0), P(s, 0, 0), P(s, s, 0), P(0, s, 0)]
        right = [P(s, 0, 0), P(s, 0, s), P(s, s, s), P(s, s, 0)]
        top = [P(0, s, 0), P(s, s, 0), P(s, s, s), P(0, s, s)]
        for pts, col, nm in ((front, FB, "front"), (right, LR, "right"), (top, TB, "top")):
            solid_face(c, pts, col, "50")
            g = centroid(pts)
            c.text(g[0], g[1], nm, size=13, color=theme.INK, halo=True)
        c.text(*_off(P(s / 2, 0, 0), 0, 16), f"{s}", size=15, math=True)
        c.text(*_off(P(0, s / 2, 0), -12, 0), f"{s}", size=15, math=True)
        c.text(*_off(P(s, 0, s / 2), 12, 8), f"{s}", size=15, math=True)

    nx0, ny0 = 330.0, 60.0  # net top-left
    # cross net: top above front, bottom below; row: left, front, right, back
    faces = [("top", 1, 0, TB), ("left", 0, 1, LR), ("front", 1, 1, FB), ("right", 2, 1, LR),
             ("back", 3, 1, FB), ("bottom", 1, 2, TB)]

    def cube_net(c, areas=False):
        k = s * u
        for nm, i, j, col in faces:
            x, y = nx0 + i * k, ny0 + j * k
            c.rect(x, y, k, k, color=col, fill=theme.fill(col, "40"), width=2)
            for t in range(1, s):
                c.line(x + t * u, y, x + t * u, y + k, color=col, width=1, stroke_opacity=0.5)
                c.line(x, y + t * u, x + k, y + t * u, color=col, width=1, stroke_opacity=0.5)
            if areas:
                c.text(x + k / 2, y + k / 2 - 9, nm, size=12, color=theme.INK, halo=True)
                c.text(x + k / 2, y + k / 2 + 10, f"{s * s}", size=17, math=True, weight="bold", halo=True)
            else:
                c.text(x + k / 2, y + k / 2, nm, size=13, color=theme.INK, halo=True)

    def tri_prism(c):
        R = Oblique(50, 320, 36)
        # right angle at the origin: leg b along x, leg a up the y-axis, length L in depth
        hyp_face = [R(b, 0, 0), R(0, a, 0), R(0, a, L), R(b, 0, L)]
        front = [R(0, 0, 0), R(b, 0, 0), R(0, a, 0)]
        solid_face(c, hyp_face, theme.GREEN, "50")
        solid_face(c, front, TRI, "55")
        for p0, p1 in (((0, 0, 0), (0, 0, L)), ((0, 0, L), (b, 0, L)), ((0, 0, L), (0, a, L))):
            c.line(*R(*p0), *R(*p1), color=theme.SOFT_INK, width=1.4, dash="5 4")
        c.text(*_off(R(b / 2, 0, 0), 0, 16), f"{b}", size=15, math=True, color=theme.ORANGE)
        c.text(*_off(R(0, a / 2, 0), -12, 0), f"{a}", size=15, math=True, color=theme.BLUE)
        c.text(*_off(R(b * 0.78, a * 0.22, 0), 12, -8), f"{num(hyp)}", size=15, math=True, color=theme.GREEN,
               halo=True)
        c.text(*_off(R(b, 0, L / 2), 14, 8), f"{L}", size=15, math=True, color=theme.INK)
        g = centroid(hyp_face)
        c.text(g[0] + 24, g[1] - 34, f"{num(hyp)} × {L} face", size=12, color=theme.INK, halo=True)
        c.text(*_off(R(0, a, L), 0, -14), "hidden edges dashed", size=11, color=theme.SOFT_INK)

    px0, py0 = 360.0, 30.0  # prism net top-left (triangle tip row)
    v = 22.0

    def prism_net(c, areas=False):
        x = px0
        top = py0 + a * v
        for w, col in rects:
            c.rect(x, top, w * v, L * v, color=col, fill=theme.fill(col, "40"), width=2)
            c.text(x + w * v / 2, top - 10 if col != theme.ORANGE else top + 14, num(w), size=13, math=True,
                   color=col, halo=True)
            if areas:
                c.text(x + w * v / 2, top + L * v / 2, f"{num(w)}×{L}", size=12, color=theme.INK, halo=True)
                c.text(x + w * v / 2, top + L * v / 2 + 18, num(w * L), size=16, weight="bold", math=True,
                       halo=True)
            x += w * v
        x3 = px0 + a * v
        bot = top + L * v
        for tri in ([(x3, top), (x3 + b * v, top), (x3, top - a * v)],
                    [(x3, bot), (x3 + b * v, bot), (x3, bot + a * v)]):
            c.polygon(tri, color=TRI, fill=theme.fill(TRI, "50"), width=2)
            if areas:
                g = centroid(tri)
                c.text(g[0] - 2, g[1] + (4 if tri[2][1] < top + 1 else -4), num(tri_area), size=14, math=True,
                       weight="bold", halo=True)
        c.text(px0 - 8, top + L * v / 2, f"{L}", size=14, math=True, anchor="end")

    @wt.step("Look at a cube", f"A cube with edge {s} has six square faces. Opposite faces share a color: "
             "front and back, top and bottom, left and right.", math=f"edge = {s}, 6 faces")
    def _(c):
        cube(c)

    @wt.step("Unfold it into a net", "Cut along some edges and fold the cube flat. The six faces lie in a "
             "cross shape called a net. Fold it back up and you get the cube again.",
             math="net = 6 squares")
    def _(c):
        cube_net(c)
        c.curved_arrow(250, 150, nx0 - 10, 150, bend=-0.25, color=theme.MUTED, width=1.5)

    @wt.step("Add the face areas", f"Each face is {s} × {s} = {s * s} unit squares. Six faces give the "
             "surface area: the paint needed to cover the cube.",
             math=f"SA = 6 \\times {s}^2 = 6 \\times {s * s} = {6 * s * s}", fresh=True)
    def _(c):
        cube(c)
        cube_net(c, areas=True)
        c.text(nx0 + 3.5 * s * u, ny0 + 2.5 * s * u, f"6 × {s * s} = {6 * s * s}", size=20, math=True,
               weight="bold")

    @wt.step("Look at a triangular prism", f"This prism has two right triangles with legs {a} and {b} "
             f"for its ends, and it is {L} long. Its sides are three rectangles.",
             math=f"legs {a}, {b}, hypotenuse {num(hyp)}, length {L}", fresh=True)
    def _(c):
        tri_prism(c)

    @wt.step("Unfold the prism", f"Lay the three rectangles side by side, {a}, {b}, and {num(hyp)} wide "
             f"and {L} tall. The two triangles hang off the {b}-wide rectangle.",
             math="net = 3 rectangles + 2 triangles", fresh=True)
    def _(c):
        tri_prism(c)
        prism_net(c)

    @wt.step("Add the face areas", f"Rectangles: {a * L} + {b * L} + {num(hyp * L)}. Triangles: "
             f"{num(tri_area)} each. The total is the surface area.",
             math=f"SA = {a * L} + {b * L} + {num(hyp * L)} + 2 \\times {num(tri_area)} = {num(prism_sa)}",
             fresh=True)
    def _(c):
        tri_prism(c)
        prism_net(c, areas=True)
        c.text(620, 330, f"total = {num(prism_sa)}", size=20, math=True, weight="bold")

    return wt


def _off(p, dx, dy):
    return (p[0] + dx, p[1] + dy)
