"""Complex numbers as points: the complex plane, multiplication, and roots of unity."""

from __future__ import annotations

import cmath
import math

from .. import theme
from ..annotate import angle_mark, right_angle
from ..plane import Plane
from ..registry import diagram
from ..svg import text_width
from ..walkthrough import Walkthrough
from ._trigkit import deg_text, num

CAT = "Complex Numbers"
RE = theme.BLUE
IM = theme.RED
MOD = theme.GREEN
ARG = theme.ORANGE
CONJ = theme.PURPLE


def cstr(z: complex, digits: int = 3) -> str:
    """Formats a complex number as a + bi with a real minus sign."""
    a, b = z.real, z.imag
    if abs(b) < 1e-12:
        return num(a, digits).replace("-", "−")
    bs = num(abs(b), digits)
    bs = "" if bs == "1" else bs
    if abs(a) < 1e-12:
        return ("−" if b < 0 else "") + bs + "i"
    return f"{num(a, digits)} {'−' if b < 0 else '+'} {bs}i".replace("-", "−")


def complex_plane(c, box, x, y, step=1):
    """A Plane with Re and Im axes and tick labels like 2i on the imaginary axis."""
    p = Plane(c, box=box, x=x, y=y, equal=True)
    p.grid(step=step)
    p.axes(xlabel="Re", ylabel="", step=step, ystep=step,
           yfmt=lambda v: (("−" if v < 0 else "") + ("" if abs(v) == 1 else f"{abs(v):g}") + "i"))
    X, Y = p.px(0, y[1])
    c.text(X + 10, Y + 4, "Im", size=16, math=True, anchor="start", halo=True)
    return p


def panel_line(c, x, y, s, color=theme.INK, size=17, boxed=False):
    c.math(x, y, s, anchor="start", color=color, size=size)
    if boxed:
        w = text_width(s, size, "serif")
        c.rect(x - 8, y - size, w + 26, 2 * size, color=color, width=1.5, rx=6)


@diagram("complex-plane", "The Complex Plane", CAT)
def complex_plane_diagram() -> Walkthrough:
    z = complex(3, 4)
    r = abs(z)
    th = math.degrees(cmath.phase(z))
    wt = Walkthrough(
        "complex-plane", "The Complex Plane", CAT,
        concept="z = a + bi \\to (a, b), |z| = sqrt(a^2 + b^2)",
        summary="A complex number a + bi is a point: a steps along the real axis and b steps along the "
                "imaginary axis. Its distance from 0 is the modulus, its direction is the argument, and its "
                "mirror image across the real axis is the conjugate.",
        width=720, height=480, level="201",
    )
    PX = 402

    @wt.setup
    def _(c):
        p = complex_plane(c, box=(20, 26, 360, 440), x=(-1.4, 5.8), y=(-4.9, 4.9))
        c.line(PX - 14, 30, PX - 14, 450, color=theme.GRID, width=1)
        return p

    def row(i):
        return 60 + i * 50

    @wt.step("Two axes for two parts",
             "The horizontal axis holds real numbers. The vertical axis holds multiples of i, where "
             "i² = −1. A complex number a + bi is the point (a, b), no imagination required.",
             math="a + bi \\to (a, b)")
    def _(c, p):
        for w, col in ((1, RE), (1j, IM), (-1, RE), (-1j, IM)):
            X, Y = p.px(w.real, w.imag)
            c.dot(X, Y, r=5, color=col)
        if c.is_new:
            X, Y = p.px(4.2, 0)
            c.text(X, Y - 14, "real axis", size=14, color=RE, halo=True)
            X, Y = p.px(0, 3.3)
            c.text(X + 12, Y, "imaginary axis", size=14, color=IM, anchor="start", halo=True)
        panel_line(c, PX, row(0), "a + bi \\to (a, b)")

    @wt.step("Plot 3 + 4i",
             "Walk 3 along the real axis, then 4 up the imaginary axis. The point where you stop is "
             "3 + 4i.",
             math="z = 3 + 4i \\to (3, 4)")
    def _(c, p):
        o, A, Z = p.px(0, 0), p.px(z.real, 0), p.px(z.real, z.imag)
        c.arrow(*o, A[0] - 2, A[1], color=RE, width=3.5)
        c.arrow(*A, Z[0], Z[1] + 4, color=IM, width=3.5)
        c.text((o[0] + A[0]) / 2 + 12, o[1] + 36, "3 real", size=14, color=RE, halo=True)
        c.text(A[0] + 8, (A[1] + Z[1]) / 2 + 20, "4 imaginary", size=14, color=IM, anchor="start", halo=True)
        c.dot(*Z, r=6, color=theme.INK)
        c.text(Z[0] + 10, Z[1] - 14, "z = 3 + 4i", size=16, math=True, anchor="start", halo=True)
        panel_line(c, PX, row(1), "z = 3 + 4i: Re z = 3, Im z = 4")

    @wt.step("Measure the modulus",
             f"The distance from 0 to z is the modulus |z|. The real and imaginary parts are the legs "
             f"of a right triangle, so |z| = {num(r)}.",
             math=f"|z| = sqrt(3^2 + 4^2) = sqrt(25) = {num(r)}")
    def _(c, p):
        o, Z = p.px(0, 0), p.px(z.real, z.imag)
        c.line(*o, *Z, color=MOD, width=4)
        right_angle(c, p.px(z.real, 0), o, Z, s=10)
        X, Y = p.px(2.2, 1.35)
        c.text(X, Y, f"|z| = {num(r)}", size=16, color=MOD, math=True, halo=True)
        panel_line(c, PX, row(2), f"|z| = sqrt(9 + 16) = {num(r)}", color=MOD)

    @wt.step("Measure the argument",
             f"The angle from the positive real axis to z is the argument. Here tan(arg z) = 4/3, so "
             f"arg z ≈ {num(th, 2)}°, or {num(math.radians(th), 3)} radians.",
             math=f"arg z = arctan(4/3) \\approx {num(th, 2)}°")
    def _(c, p):
        o, Z = p.px(0, 0), p.px(z.real, z.imag)
        angle_mark(c, o, p.px(1, 0), Z, r=34, label=deg_text(th, 2), color=ARG, label_r=64, size=14)
        panel_line(c, PX, row(3), f"arg z \\approx {num(th, 2)}° \\approx {num(math.radians(th), 3)} rad",
                   color=ARG)

    @wt.step("Reflect to get the conjugate",
             "Flip the sign of the imaginary part: the conjugate of 3 + 4i is 3 − 4i, the mirror image "
             "across the real axis. Same modulus, opposite angle. A number times its conjugate is "
             "|z|², a plain real number.",
             math="(3 + 4i)(3 - 4i) = 9 + 16 = 25 = |z|^2")
    def _(c, p):
        o, Z, W = p.px(0, 0), p.px(z.real, z.imag), p.px(z.real, -z.imag)
        c.line(*Z, *W, color=CONJ, width=1.5, dash="5 5")
        c.line(*o, *W, color=CONJ, width=3)
        c.dot(*W, r=6, color=CONJ)
        c.text(W[0] + 10, W[1] + 14, "z̄ = 3 − 4i", size=17, color=CONJ, anchor="start", halo=True)
        angle_mark(c, o, p.px(1, 0), W, r=34, color=CONJ)
        X, Y = p.px(2.2, -1.35)
        c.text(X, Y, f"|z̄| = {num(r)}", size=16, color=CONJ, halo=True)
        c.text(PX, row(4), f"z̄ = 3 − 4i,  arg z̄ ≈ −{num(th, 2)}°", size=16, color=CONJ, anchor="start")
        panel_line(c, PX, row(5) + 10, "(3 + 4i)(3 - 4i) = 25 = |z|^2", color=theme.INK, boxed=True)

    return wt


@diagram("complex-multiplication", "Complex Multiplication Rotates and Scales", CAT)
def complex_multiplication() -> Walkthrough:
    z = complex(2, 1)
    w, v = complex(1, 1), complex(1, 2)
    prod = w * v
    aw, av = math.degrees(cmath.phase(w)), math.degrees(cmath.phase(v))
    ap = math.degrees(cmath.phase(prod))
    assert abs(ap - (aw + av)) < 1e-9
    wt = Walkthrough(
        "complex-multiplication", "Complex Multiplication Rotates and Scales", CAT,
        concept="|wv| = |w||v|, arg(wv) = arg w + arg v",
        summary="Multiplying by a complex number turns and stretches. Multiplying by i is a quarter turn. "
                "In general the angles add and the lengths multiply.",
        width=720, height=440, level="201",
    )
    PX = 482
    Z_COL, IZ_COL, I2_COL = theme.BLUE, theme.ORANGE, theme.RED
    W_COL, V_COL, P_COL = theme.BLUE, theme.ORANGE, theme.GREEN

    @wt.setup
    def _(c):
        p = complex_plane(c, box=(12, 26, 420, 400), x=(-2.8, 2.8), y=(-2.4, 3.6))
        c.line(PX - 14, 30, PX - 14, 410, color=theme.GRID, width=1)
        return p

    def row(i):
        return 56 + i * 44

    def vec(c, p, u, color, label, off=(10, -12), anchor="start", width=3.5):
        X, Y = p.px(u.real, u.imag)
        c.arrow(*p.px(0, 0), X, Y, color=color, width=width)
        c.text(X + off[0], Y + off[1], label, size=15, color=color, math=True, anchor=anchor, halo=True)

    @wt.step("Multiply by i: a quarter turn",
             "Take z = 2 + i. Then i·z = 2i + i² = −1 + 2i. The arrow keeps its length and turns 90° "
             "counterclockwise.",
             math="i(2 + i) = 2i + i^2 = -1 + 2i")
    def _(c, p):
        vec(c, p, z, Z_COL, "z = 2 + i")
        vec(c, p, 1j * z, IZ_COL, "iz = −1 + 2i", off=(-10, -12), anchor="end")
        right_angle(c, p.px(0, 0), p.px(z.real, z.imag), p.px(-z.imag, z.real), s=14, color=IZ_COL)
        a0 = math.degrees(cmath.phase(z))
        c.arc(*p.px(0, 0), 0.62 * abs(z) * p.sx, a0 + 14, a0 + 84, color=IZ_COL, width=2, arrow=True)
        c.text(*p.px(0.45, 1.72), "90°", size=13, color=IZ_COL, halo=True)
        panel_line(c, PX, row(0), "z = 2 + i", color=Z_COL)
        panel_line(c, PX, row(1), "iz = -1 + 2i", color=IZ_COL)
        panel_line(c, PX, row(2), f"|z| = |iz| = √5 \\approx {num(abs(z))}", size=16)

    @wt.step("Multiply by i again",
             "Two quarter turns make a half turn, which points the arrow the other way. That is why "
             "i² = −1: multiplying by −1 is a 180° turn.",
             math="i^2 z = i(-1 + 2i) = -2 - i = -z")
    def _(c, p):
        u = -z
        vec(c, p, u, I2_COL, "i²z = −2 − i", off=(8, 18), anchor="start")
        a0 = math.degrees(cmath.phase(1j * z))
        c.arc(*p.px(0, 0), 0.45 * abs(z) * p.sx, a0 + 12, a0 + 86, color=I2_COL, width=2, arrow=True)
        c.text(*p.px(-1.3, 0.34), "90°", size=13, color=I2_COL, halo=True)
        panel_line(c, PX, row(3), "i^2 z = -2 - i = -z", color=I2_COL)
        panel_line(c, PX, row(4), "i^2 = -1 (half turn)", color=I2_COL, size=16)

    @wt.step("Write two numbers as length and angle",
             f"Now multiply w = 1 + i by v = 1 + 2i. Measure each one: w has length √2 and angle 45°, "
             f"v has length √5 and angle {num(av, 2)}°.",
             math=f"|w| = √2, arg w = 45°; |v| = √5, arg v \\approx {num(av, 2)}°", fresh=True)
    def _(c, p):
        vec(c, p, w, W_COL, "w", off=(4, 16))
        vec(c, p, v, V_COL, "v = 1 + 2i", off=(10, -8))
        o = p.px(0, 0)
        c.arc(*o, 46, 0, aw, color=W_COL, width=2.5)
        c.arc(*o, 70, 0, av, color=V_COL, width=2.5)
        c.text(o[0] + 58 * math.cos(math.radians(20)), o[1] - 58 * math.sin(math.radians(20)), "45°", size=13,
               color=W_COL, halo=True)
        c.text(o[0] + 82 * math.cos(math.radians(77)), o[1] - 82 * math.sin(math.radians(77)), deg_text(av, 1),
               size=13, color=V_COL, halo=True)
        panel_line(c, PX, row(0), "w = 1 + i", color=W_COL)
        panel_line(c, PX, row(1), f"|w| = √2 \\approx {num(abs(w))}, arg w = 45°", color=W_COL, size=16)
        panel_line(c, PX, row(2), "v = 1 + 2i", color=V_COL)
        panel_line(c, PX, row(3), f"|v| = √5 \\approx {num(abs(v))}, arg v \\approx {num(av, 1)}°", color=V_COL,
                   size=16)

    @wt.step("The angles add",
             f"The product points at 45° + {num(av, 2)}° = {num(ap, 2)}°. Lay the angle of v on top of the "
             "angle of w and you land on the angle of wv.",
             math=f"arg(wv) = 45° + {num(av, 2)}° = {num(ap, 2)}°")
    def _(c, p):
        o = p.px(0, 0)
        R = 110
        c.arc(*o, R, 0, aw, color=W_COL, width=5)
        c.arc(*o, R, aw, ap, color=V_COL, width=5)
        X, Y = p.px(prod.real * 1.12, prod.imag * 1.12)
        c.line(*o, *p.px(prod.real, prod.imag), color=P_COL, width=1.5, dash="6 4")
        x2 = o[0] + (R + 18) * math.cos(math.radians(ap))
        y2 = o[1] - (R + 18) * math.sin(math.radians(ap))
        c.text(x2 - 6, y2 + 4, deg_text(ap, 2), size=14, color=P_COL, anchor="end", halo=True)
        panel_line(c, PX, row(4), f"arg(wv) = {num(ap, 2)}°", color=P_COL)

    @wt.step("The lengths multiply",
             f"The product has length √2 · √5 = √10 ≈ {num(abs(prod))}. Multiplying it out the long way "
             "agrees: (1 + i)(1 + 2i) = −1 + 3i.",
             math="(1 + i)(1 + 2i) = 1 + 2i + i + 2i^2 = -1 + 3i")
    def _(c, p):
        vec(c, p, prod, P_COL, "wv = −1 + 3i", off=(-10, -12), anchor="end", width=4)
        panel_line(c, PX, row(5), f"|wv| = √2 · √5 = √10", color=P_COL)
        panel_line(c, PX, row(6), f"wv = -1 + 3i", color=P_COL, boxed=True)

    return wt


@diagram("roots-of-unity", "Roots of Unity", CAT)
def roots_of_unity() -> Walkthrough:
    n = 6
    roots = [cmath.exp(2j * math.pi * k / n) for k in range(n)]
    wt = Walkthrough(
        "roots-of-unity", "Roots of Unity", CAT,
        concept="z^6 = 1 \\iff z = e^{2\\pi ik/6}, k = 0, 1, ..., 5",
        summary="Euler's formula e^(iθ) = cos θ + i sin θ puts a point on the unit circle at angle θ. The six "
                "solutions of z⁶ = 1 sit 60° apart and form a regular hexagon.",
        width=720, height=440, level="301",
    )
    PX = 496
    E_COL, Z_COL, HEX = theme.PURPLE, theme.BLUE, theme.GREEN
    th = 40.0

    @wt.setup
    def _(c):
        p = Plane(c, box=(14, 22, 420, 400), x=(-1.55, 1.55), y=(-1.38, 1.38), equal=True)
        p.axes(xlabel="Re", ylabel="", ticks=False)
        X, Y = p.px(0, 1.38)
        c.text(X + 10, Y + 4, "Im", size=16, math=True, anchor="start", halo=True)
        p.circle(0, 0, 1, color=theme.MUTED, width=2)
        c.line(PX - 14, 30, PX - 14, 410, color=theme.GRID, width=1)
        return p

    def row(i):
        return 58 + i * 46

    @wt.step("Euler's formula puts a point on the circle",
             f"The number e^(iθ) is cos θ + i sin θ: the point on the unit circle at angle θ. Here "
             f"θ = {num(th)}°. Its modulus is always 1.",
             math="e^{i\\theta} = cos \\theta + i sin \\theta")
    def _(c, p):
        if not c.is_new:
            return
        t = math.radians(th)
        o, F, P = p.px(0, 0), p.px(math.cos(t), 0), p.px(math.cos(t), math.sin(t))
        c.line(*o, *P, color=E_COL, width=3)
        c.line(*o, *F, color=RE, width=3.5)
        c.line(*F, *P, color=IM, width=3.5)
        angle_mark(c, o, p.px(1, 0), P, r=30, label="θ", color=ARG, label_r=46)
        c.dot(*P, r=6, color=E_COL)
        c.text(P[0] + 10, P[1] - 14, "e^{iθ}", size=17, color=E_COL, math=True, anchor="start", halo=True)
        c.text((o[0] + F[0]) / 2, o[1] + 16, "cos θ", size=14, color=RE, math=True, halo=True)
        c.text(F[0] + 6, (F[1] + P[1]) / 2, "sin θ", size=14, color=IM, math=True, anchor="start", halo=True)
        panel_line(c, PX, row(0), "e^{i\\theta} = cos \\theta + i sin \\theta", color=E_COL, size=16)
        panel_line(c, PX, row(1), f"\\theta = {num(th)}°: {cstr(cmath.exp(1j * t))}", size=15)

    @wt.step("Guess one root: a sixth of a turn",
             "Try z = e^(iπ/3), the point at 60°. Raising it to the 6th power multiplies the angle by 6, "
             "and 6 × 60° = 360° is a full turn back to 1.",
             math="z^6 = e^{i\\cdot 6\\pi/3} = e^{2\\pi i} = 1")
    def _(c, p):
        z = roots[1]
        o, Z = p.px(0, 0), p.px(z.real, z.imag)
        if c.is_new:
            angle_mark(c, o, p.px(1, 0), Z, r=30, label="60°", color=ARG, label_r=50, size=14)
        c.line(*o, *Z, color=Z_COL, width=3)
        panel_line(c, PX, row(0), "z = e^{i\\pi/3}", color=Z_COL)
        panel_line(c, PX, row(1), "z^6 = e^{2\\pi i} = 1", color=Z_COL)

    @wt.step("Powers walk around the circle",
             "Each multiplication by z turns another 60°. After six steps the walk is back at 1, so "
             "z, z², z³, z⁴, z⁵, and z⁶ = 1 all solve z⁶ = 1.",
             math="z^k = e^{ik\\pi/3}, k = 1, 2, ..., 6")
    def _(c, p):
        o = p.px(0, 0)
        for k in range(n):
            u = roots[(k + 1) % n]
            X, Y = p.px(u.real, u.imag)
            c.line(*o, X, Y, color=Z_COL, width=1.5)
            c.dot(X, Y, r=6, color=Z_COL)
            lab = "z" if k == 0 else ("z^6 = 1" if k == n - 1 else f"z^{k + 1}")
            a = cmath.phase(u) + math.radians(13)
            L = p.px(0.74 * math.cos(a), 0.74 * math.sin(a))
            c.text(L[0], L[1], lab, size=15, color=Z_COL, math=True, halo=True)
        panel_line(c, PX, row(2), "z^k: k turns of 60°", color=ARG, size=16)
        if c.is_new:
            for k in range(n):
                a0, a1 = 60 * k + 8, 60 * (k + 1) - 8
                c.arc(*o, 1.16 * p.sx, a0, a1, color=ARG, width=1.8, arrow=True)

    @wt.step("The six roots form a hexagon",
             "Connect the roots. They split the circle into six equal slices, a regular hexagon. Each "
             "root has exact coordinates built from 1/2 and √3/2.",
             math="1, 1/2 + (√3/2)i, -1/2 + (√3/2)i, -1, -1/2 - (√3/2)i, 1/2 - (√3/2)i")
    def _(c, p):
        pts = [p.px(u.real, u.imag) for u in roots]
        c.polygon(pts, color=HEX, fill=theme.fill(HEX, "1f"), width=3)
        names = ["1", "½ + (√3/2)i", "−½ + (√3/2)i", "−1", "−½ − (√3/2)i", "½ − (√3/2)i"]
        for u, s in zip(roots, names):
            X, Y = p.px(u.real, u.imag)
            if abs(u.imag) < 1e-9:
                dx, anc, dy = (12 if u.real > 0 else -12), ("start" if u.real > 0 else "end"), -14
            else:
                dx, anc = (8 if u.real > 0 else -8), ("start" if u.real > 0 else "end")
                dy = -16 if u.imag > 0 else 18
            c.text(X + dx, Y + dy, s, size=14, color=HEX, anchor=anc, halo=True)
        panel_line(c, PX, row(3), "6 roots, 60° apart", color=HEX, size=16)

    @wt.step("Opposite roots cancel",
             "Each root has a partner straight across the circle, its negative. The three pairs cancel, "
             "so the six roots add to 0. The hexagon balances on its center like a well-made pizza.",
             math="1 + z + z^2 + z^3 + z^4 + z^5 = 0")
    def _(c, p):
        for k in range(3):
            a, b = roots[k], roots[k + 3]
            c.line(*p.px(a.real, a.imag), *p.px(b.real, b.imag), color=theme.RED, width=1.8, dash="6 4")
        c.dot(*p.px(0, 0), r=7, color=theme.RED)
        X, Y = p.px(0, 0)
        c.label_box(X + 40, Y + 26, "sum = 0", color=theme.RED, border=theme.RED, size=14)
        panel_line(c, PX, row(4), "z^k + z^{k+3} = 0", color=theme.RED)
        panel_line(c, PX, row(5), "sum of roots = 0", color=theme.RED, boxed=True)

    return wt


@diagram("roots-of-unity-polygons", "Roots of Unity for Every n", CAT)
def roots_polygons() -> Walkthrough:
    ns = [2, 3, 4, 5, 8]
    cols = [theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE, theme.RED]
    wt = Walkthrough(
        "roots-of-unity-polygons", "Roots of Unity for Every n", CAT,
        concept="z^n = 1 \\iff z = e^{2\\pi ik/n}: n points 360°/n apart",
        summary="The n solutions of zⁿ = 1 always sit on the unit circle, spaced 360°/n apart, starting at 1. "
                "They form a regular polygon with n corners.",
        width=720, height=330, level="301",
    )
    R = 54.0
    centers = [(76 + 142 * i, 150.0) for i in range(5)]
    exact = {
        2: ["1", "−1"],
        3: ["1", "−½ + (√3/2)i", "−½ − (√3/2)i"],
        4: ["1", "i", "−1", "−i"],
    }

    @wt.setup
    def _(c):
        for (x, y), n in zip(centers, ns):
            c.circle(x, y, R, color=theme.MUTED, width=1.4)
            c.line(x - R - 8, y, x + R + 8, y, color=theme.GRID, width=1)
            c.line(x, y - R - 8, x, y + R + 8, color=theme.GRID, width=1)
        return None

    def draw(c, i):
        n, col = ns[i], cols[i]
        x, y = centers[i]
        pts = [(x + R * math.cos(2 * math.pi * k / n), y - R * math.sin(2 * math.pi * k / n)) for k in range(n)]
        if n == 2:
            c.line(*pts[0], *pts[1], color=col, width=2.5)
        else:
            c.polygon(pts, color=col, fill=theme.fill(col, "22"), width=2.5)
        for P in pts:
            c.dot(*P, r=4.5, color=col)
        c.text(x, y - R - 30, f"z^{n} = 1", size=17, color=col, math=True)
        c.text(x, y + R + 28, f"{n} roots", size=14, color=col, weight="bold")
        c.text(x, y + R + 48, f"{num(360 / n, 1)}° apart", size=13, color=theme.SOFT_INK)
        if n in exact and c.is_new:
            for k, s in enumerate(exact[n]):
                a = 2 * math.pi * k / n
                lx, ly = x + (R + 14) * math.cos(a), y - (R + 12) * math.sin(a)
                anchor = "start" if math.cos(a) > 0.3 else ("end" if math.cos(a) < -0.3 else "middle")
                c.text(lx, ly, s, size=12, color=col, anchor=anchor, halo=True)

    @wt.step("Two square roots of 1",
             "z² = 1 has two answers, 1 and −1. They sit on opposite sides of the circle, 180° apart.",
             math="z^2 = 1: z = 1, -1")
    def _(c):
        draw(c, 0)

    @wt.step("Three cube roots of 1",
             "z³ = 1 has three answers, 120° apart. Only one of them is real; the other two are complex "
             "and form a triangle with it.",
             math="z^3 = 1: z = 1, -1/2 \\pm (√3/2)i")
    def _(c):
        draw(c, 1)

    @wt.step("Four fourth roots of 1",
             "z⁴ = 1 gives 1, i, −1, and −i, a square. Each one is the previous one turned a quarter turn, "
             "which is multiplication by i.",
             math="z^4 = 1: z = 1, i, -1, -i")
    def _(c):
        draw(c, 2)

    @wt.step("Five and eight",
             "z⁵ = 1 makes a pentagon and z⁸ = 1 an octagon. Any n works the same way, and the polygon "
             "always has a corner at 1.",
             math="z^n = 1: z_k = cos(2\\pi k/n) + i sin(2\\pi k/n), k = 0, ..., n - 1")
    def _(c):
        draw(c, 3)
        draw(c, 4)

    return wt
