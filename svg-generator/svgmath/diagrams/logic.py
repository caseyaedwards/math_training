"""Logic diagrams: truth tables, logic gate circuits, and set operations on Venn diagrams."""

from __future__ import annotations

from itertools import product

from .. import theme
from ..annotate import brace
from ..registry import diagram
from ..svg import Element, fmt
from ..walkthrough import Walkthrough

TRUE_C = theme.GREEN
FALSE_C = theme.RED


def _stage(scene, stage):
    """Returns a step function that draws the scene at the given stage."""
    def draw(c, ctx):
        scene(c, stage)
    return draw


# ---------------------------------------------------------------------------
# Truth tables
# ---------------------------------------------------------------------------


def _tf(v: bool) -> str:
    return "T" if v else "F"


def truth_table(c, x, y, headers, rows, colw=70, rowh=34, result_cols=(), row_fill=None, size=16):
    """Draws a truth table at top-left (x, y). rows hold booleans. Returns (width, height)."""
    row_fill = row_fill or {}
    n = len(headers)
    w = n * colw
    for k, h in enumerate(headers):
        fill = theme.HIGHLIGHT if k in result_cols else theme.PANEL
        c.rect(x + k * colw, y, colw, rowh, color=theme.MUTED, fill=fill, width=1)
        c.math(x + k * colw + colw / 2, y + rowh / 2, h, size=size)
    for r, row in enumerate(rows):
        top = y + (r + 1) * rowh
        for k, v in enumerate(row):
            fill = row_fill.get(r, "none")
            c.rect(x + k * colw, top, colw, rowh, color=theme.MUTED, fill=fill, width=1)
            c.text(x + k * colw + colw / 2, top + rowh / 2, _tf(v), size=size, weight="bold",
                   color=TRUE_C if v else FALSE_C)
    # heavier line to separate the inputs from the result
    if result_cols:
        k = min(result_cols)
        c.line(x + k * colw, y, x + k * colw, y + (len(rows) + 1) * rowh, color=theme.INK, width=2)
    c.rect(x, y, w, (len(rows) + 1) * rowh, color=theme.INK, width=1.5)
    return w, (len(rows) + 1) * rowh


@diagram("truth-tables", "Truth Tables", "Logic and Proof")
def build_truth_tables() -> Walkthrough:
    wt = Walkthrough(
        "truth-tables", "Truth Tables", "Logic and Proof",
        concept="p \\to q is false only when p is true and q is false",
        summary="A truth table lists every combination of true and false inputs and the value of a statement "
                "for each. The conditional p → q is false in just one row.",
        width=700, height=360, level="201",
    )
    TF = [True, False]
    pairs = list(product(TF, TF))
    imp = lambda p, q: (not p) or q
    n_and = sum(1 for p, q in pairs if p and q)
    n_or = sum(1 for p, q in pairs if p or q)

    def tables(c, stage):
        y = 70
        if stage >= 1:
            x = 30
            truth_table(c, x, y, ["p", "\\neg p"], [[p, not p] for p in TF], result_cols=(1,))
            c.text(x + 70, y - 24, "NOT", size=17, weight="bold")
            c.text(x + 70, y + 3 * 34 + 24, "flips the value", size=14, color=theme.SOFT_INK)
        if stage >= 2:
            x = 215
            fills = {i: theme.fill(TRUE_C, "26") for i, (p, q) in enumerate(pairs) if p and q}
            truth_table(c, x, y, ["p", "q", "p \\land q"], [[p, q, p and q] for p, q in pairs],
                        result_cols=(2,), row_fill=fills)
            c.text(x + 105, y - 24, "AND", size=17, weight="bold")
            c.text(x + 105, y + 5 * 34 + 24, "true only when both are true", size=14, color=theme.SOFT_INK)
        if stage >= 3:
            x = 470
            fills = {i: theme.fill(FALSE_C, "26") for i, (p, q) in enumerate(pairs) if not (p or q)}
            truth_table(c, x, y, ["p", "q", "p \\lor q"], [[p, q, p or q] for p, q in pairs],
                        result_cols=(2,), row_fill=fills)
            c.text(x + 105, y - 24, "OR", size=17, weight="bold")
            c.text(x + 105, y + 5 * 34 + 24, "true when at least one is true", size=14, color=theme.SOFT_INK)
        for k, (x, name) in enumerate(((215, "AND"), (470, "OR"))):
            if stage < k + 2:
                c.rect(x, y, 210, 170, color=theme.GRID, width=1.5, dash="6 5", rx=6)
                c.text(x + 105, y - 24, name, size=17, weight="bold", color=theme.MUTED)
                c.text(x + 105, y + 85, "next", size=14, color=theme.MUTED)
        c.text(30, 335, "T", size=15, weight="bold", color=TRUE_C, anchor="start")
        c.text(44, 335, "= true", size=14, color=theme.SOFT_INK, anchor="start")
        c.text(110, 335, "F", size=15, weight="bold", color=FALSE_C, anchor="start")
        c.text(124, 335, "= false", size=14, color=theme.SOFT_INK, anchor="start")

    notes = [
        ("rain, umbrella: promise kept", TRUE_C),
        ("rain, no umbrella: promise broken", FALSE_C),
        ("no rain, umbrella anyway: not broken", TRUE_C),
        ("no rain, no umbrella: not broken", TRUE_C),
    ]

    def conditional(c, stage):
        c.label_box(350, 30, "promise:  if it rains (p), then I carry an umbrella (q)", size=15,
                    border=theme.MUTED, color=theme.INK)
        x, y, rh = 30, 70, 40
        fills = {i: theme.fill(FALSE_C, "26") for i, (p, q) in enumerate(pairs) if not imp(p, q)}
        truth_table(c, x, y, ["p", "q", "p \\to q"], [[p, q, imp(p, q)] for p, q in pairs],
                    rowh=rh, result_cols=(2,), row_fill=fills)
        shown = 2 if stage == 4 else 4
        for i in range(shown):
            s, col = notes[i]
            cy = y + (i + 1) * rh + rh / 2
            c.line(250, cy, 268, cy, color=theme.MUTED, width=1.5)
            c.text(276, cy, s, size=15, color=col, anchor="start",
                   weight="bold" if (stage == 5 and i >= 2) else None)
        if stage == 4:
            c.text(30, 300, "p is the hypothesis (the if part), q is the conclusion (the then part).", size=15,
                   anchor="start")
            c.text(30, 326, "A promise like this can be broken in only one way: the shaded row.", size=14,
                   anchor="start", color=theme.SOFT_INK)
        if stage == 5:
            top = y + 3 * rh + 4
            bot = y + 5 * rh - 4
            brace(c, 568, top, 568, bot, color=theme.PURPLE, depth=12)
            c.text(590, (top + bot) / 2 - 10, "p false:", size=14, color=theme.PURPLE, anchor="start")
            c.text(590, (top + bot) / 2 + 10, "always true", size=14, color=theme.PURPLE, anchor="start",
                   weight="bold")
            c.text(30, 300, "A false p means the promise is never tested, so it is not broken.", size=15,
                   color=theme.PURPLE, anchor="start")

    def equivalence(c, stage):
        x, y, rh, cw = 125, 40, 40, 90
        rows = [[p, q, not p, (not p) or q, imp(p, q)] for p, q in pairs]
        assert all(r[3] == r[4] for r in rows)
        truth_table(c, x, y, ["p", "q", "\\neg p", "\\neg p \\lor q", "p \\to q"], rows, colw=cw, rowh=rh,
                    result_cols=(3, 4))
        c.rect(x + 3 * cw - 4, y - 4, 2 * cw + 8, 5 * rh + 8, color=theme.PURPLE, width=3, rx=8)
        c.text(x + 4 * cw, y + 5 * rh + 26, "the two columns match in every row", size=15,
               color=theme.PURPLE, weight="bold")
        c.text(350, 300, "\u00acp \u2228 q reads: it does not rain, or I carry an umbrella.", size=15,
               color=theme.INK)
        c.text(350, 326, "Either way, nobody gets a broken promise (or wet socks).", size=14,
               color=theme.SOFT_INK)

    def scene(c, stage):
        if stage <= 3:
            tables(c, stage)
        elif stage <= 5:
            conditional(c, stage)
        else:
            equivalence(c, stage)

    wt.step("NOT flips a statement",
            "A truth table lists every possible input. NOT has one input p, so it has two rows, and it turns "
            "true into false and false into true.", math="\\neg T = F,  \\neg F = T", fresh=True)(_stage(scene, 1))
    wt.step("AND needs both",
            "With two inputs p and q there are four rows. The statement p ∧ q is true in "
            f"{'one row' if n_and == 1 else str(n_and) + ' rows'}: the row where both inputs are true.",
            math="p \\land q = T  only for  p = T, q = T", fresh=True)(_stage(scene, 2))
    wt.step("OR needs at least one",
            f"The statement p ∨ q is true in {n_or} of the four rows. It is false only when both inputs "
            "are false.", math="p \\lor q = F  only for  p = F, q = F", fresh=True)(_stage(scene, 3))
    wt.step("Read the conditional as a promise",
            "The statement p → q says: if p happens, then q happens. When it rains, the promise is kept with "
            "an umbrella and broken without one.", math="T \\to T = T,  T \\to F = F", fresh=True)(_stage(scene, 4))
    wt.step("Explain the surprising rows",
            "When it does not rain, nothing I do breaks the promise, so p → q is true in both rows where p is "
            "false. The conditional is false only in the row T, F.",
            math="F \\to T = T,  F \\to F = T", fresh=True)(_stage(scene, 5))
    wt.step("Rewrite the conditional",
            "Add a column for ¬p ∨ q. It matches p → q in every row, so the two statements say the same thing.",
            math="p \\to q \\equiv \\neg p \\lor q", fresh=True)(_stage(scene, 6))
    return wt


# ---------------------------------------------------------------------------
# Logic gates
# ---------------------------------------------------------------------------


def _signal_color(v: int) -> str:
    return TRUE_C if v else FALSE_C


def _and_gate(c, x, cy, color, fill):
    d = (f"M{fmt(x)},{fmt(cy - 30)} L{fmt(x + 30)},{fmt(cy - 30)} "
         f"A30,30 0 0 1 {fmt(x + 30)},{fmt(cy + 30)} L{fmt(x)},{fmt(cy + 30)} Z")
    c.path(d, color=color, fill=fill, width=2.4)
    c.text(x + 26, cy, "AND", size=13, weight="bold", color=color)


def _or_gate(c, x, cy, color, fill):
    d = (f"M{fmt(x)},{fmt(cy - 30)} Q{fmt(x + 15)},{fmt(cy)} {fmt(x)},{fmt(cy + 30)} "
         f"Q{fmt(x + 45)},{fmt(cy + 30)} {fmt(x + 70)},{fmt(cy)} Q{fmt(x + 45)},{fmt(cy - 30)} {fmt(x)},{fmt(cy - 30)} Z")
    c.path(d, color=color, fill=fill, width=2.4)
    c.text(x + 32, cy, "OR", size=13, weight="bold", color=color)


def _not_gate(c, x, cy, color, fill):
    c.polygon([(x, cy - 20), (x, cy + 20), (x + 36, cy)], color=color, fill=fill, width=2.4)
    c.circle(x + 41, cy, 5, color=color, fill=theme.PAPER, width=2.4)
    c.text(x + 18, cy + 36, "NOT", size=13, weight="bold", color=color)


@diagram("logic-gates", "Logic Gates", "Logic and Proof")
def build_logic_gates() -> Walkthrough:
    wt = Walkthrough(
        "logic-gates", "Logic Gates", "Logic and Proof",
        concept="Y = (A \\land B) \\lor \\neg C",
        summary="A logic circuit computes a truth value from its inputs. Signals flow left to right, and each "
                "gate applies AND, OR, or NOT to the values that reach it.",
        width=700, height=372, level="201",
    )
    A, B, C = 1, 0, 0
    AB = A & B
    NC = 1 - C
    Y = AB | NC

    # geometry
    AND_X, AND_Y = 190, 110
    OR_X, OR_Y = 320, 200
    NOT_X, NOT_Y = 170, 290
    OR_IN = OR_X + 5.6  # where the curved back of the OR gate meets y = OR_Y +- 15
    wires = {
        "A": [(60, AND_Y - 15), (AND_X, AND_Y - 15)],
        "B": [(60, AND_Y + 15), (AND_X, AND_Y + 15)],
        "C": [(60, NOT_Y), (NOT_X, NOT_Y)],
        "AB": [(AND_X + 60, AND_Y), (285, AND_Y), (285, OR_Y - 15), (OR_IN, OR_Y - 15)],
        "NC": [(NOT_X + 46, NOT_Y), (300, NOT_Y), (300, OR_Y + 15), (OR_IN, OR_Y + 15)],
        "Y": [(OR_X + 70, OR_Y), (450, OR_Y)],
    }

    def wire(c, key, v=None):
        col = theme.MUTED if v is None else _signal_color(v)
        c.polyline(wires[key], color=col, width=4 if v is not None else 2.5)

    def chip(c, x, y, v):
        col = _signal_color(v)
        c.label_box(x, y, str(v), size=15, color=col, border=col)

    def scene(c, stage):
        for k in wires:
            wire(c, k)
        for name, (x, y) in (("A", wires["A"][0]), ("B", wires["B"][0]), ("C", wires["C"][0])):
            c.text(x - 14, y, name, size=18, math=True, anchor="end")
        c.text(462, OR_Y, "Y", size=18, math=True, anchor="start")
        gate_col = theme.INK
        _and_gate(c, AND_X, AND_Y, gate_col, theme.PANEL)
        _or_gate(c, OR_X, OR_Y, gate_col, theme.PANEL)
        _not_gate(c, NOT_X, NOT_Y, gate_col, theme.PANEL)
        c.text(AND_X + 30, AND_Y + 46, "1 only if both are 1", size=12, color=theme.SOFT_INK)
        c.text(OR_X + 36, OR_Y + 46, "1 if any input is 1", size=12, color=theme.SOFT_INK)
        c.text(NOT_X + 18, NOT_Y + 54, "flips 0 and 1", size=12, color=theme.SOFT_INK)
        if stage >= 2:
            for k, v in (("A", A), ("B", B), ("C", C)):
                wire(c, k, v)
                x, y = wires[k][0]
                chip(c, 115, y, v)
            _and_gate(c, AND_X, AND_Y, gate_col, theme.PANEL)
            _not_gate(c, NOT_X, NOT_Y, gate_col, theme.PANEL)
        if stage >= 3:
            wire(c, "AB", AB)
            _and_gate(c, AND_X, AND_Y, gate_col, theme.PANEL)
            chip(c, 268, AND_Y, AB)
            c.text(AND_X + 30, AND_Y - 48, f"{A} AND {B} = {AB}", size=15, color=_signal_color(AB),
                   weight="bold" if stage == 3 else None)
        if stage >= 4:
            wire(c, "NC", NC)
            _not_gate(c, NOT_X, NOT_Y, gate_col, theme.PANEL)
            chip(c, 258, NOT_Y, NC)
            c.text(NOT_X + 20, NOT_Y - 36, f"NOT {C} = {NC}", size=15, color=_signal_color(NC),
                   weight="bold" if stage == 4 else None)
        if stage >= 5:
            wire(c, "Y", Y)
            _or_gate(c, OR_X, OR_Y, gate_col, theme.PANEL)
            chip(c, 425, OR_Y, Y)
            c.text(OR_X + 40, OR_Y - 50, f"{AB} OR {NC} = {Y}", size=15, color=_signal_color(Y),
                   weight="bold" if stage == 5 else None)
        if stage >= 6:
            x0, y0, cw, rh = 520, 52, 38, 26
            c.text(x0 + 2 * cw, y0 - 22, "every input row", size=14, color=theme.SOFT_INK)
            heads = ["A", "B", "C", "Y"]
            for k, h in enumerate(heads):
                c.rect(x0 + k * cw, y0, cw, rh, color=theme.MUTED, fill=theme.PANEL if k < 3 else theme.HIGHLIGHT,
                       width=1)
                c.math(x0 + k * cw + cw / 2, y0 + rh / 2, h, size=16)
            for r, (a, b, cc) in enumerate(product((0, 1), repeat=3)):
                y = (a & b) | (1 - cc)
                top = y0 + (r + 1) * rh
                hit = (a, b, cc) == (A, B, C)
                for k, v in enumerate((a, b, cc, y)):
                    c.rect(x0 + k * cw, top, cw, rh, color=theme.MUTED, width=1,
                           fill=theme.HIGHLIGHT if hit else "none")
                    c.text(x0 + k * cw + cw / 2, top + rh / 2, str(v), size=14, weight="bold",
                           color=_signal_color(v))
            hit_r = list(product((0, 1), repeat=3)).index((A, B, C))
            c.rect(x0 - 3, y0 + (hit_r + 1) * rh - 2, 4 * cw + 6, rh + 4, color=theme.ORANGE, width=2.5, rx=4)
            c.line(x0 + 3 * cw, y0, x0 + 3 * cw, y0 + 9 * rh, color=theme.INK, width=2)
            c.rect(x0, y0, 4 * cw, 9 * rh, color=theme.INK, width=1.5)

    wt.step("Read the circuit",
            "Signals enter on the left and flow right. A and B feed an AND gate, C feeds a NOT gate, and both "
            "results feed an OR gate that produces Y.", math="Y = (A \\land B) \\lor \\neg C",
            fresh=True)(_stage(scene, 1))
    wt.step("Set the inputs",
            "Pick one input row: A = 1, B = 0, C = 0. Green wires carry 1 (true) and red wires carry 0 (false).",
            math=f"A = {A},  B = {B},  C = {C}", fresh=True)(_stage(scene, 2))
    wt.step("Evaluate the AND gate",
            "AND outputs 1 only when both inputs are 1. Here B is 0, so the AND output is 0.",
            math=f"A \\land B = {A} \\land {B} = {AB}", fresh=True)(_stage(scene, 3))
    wt.step("Evaluate the NOT gate",
            "NOT flips its input. C is 0, so the NOT output is 1.",
            math=f"\\neg C = \\neg {C} = {NC}", fresh=True)(_stage(scene, 4))
    wt.step("Evaluate the OR gate",
            "OR outputs 1 when at least one input is 1. The NOT branch carries a 1, so Y is 1 even though the "
            "AND branch is 0.", math=f"Y = {AB} \\lor {NC} = {Y}", fresh=True)(_stage(scene, 5))
    wt.step("See every input row",
            "Repeat the same flow for all eight input rows to get the truth table of the circuit. The row "
            "traced above is outlined.", math="2^3 = 8 rows", fresh=True)(_stage(scene, 6))
    return wt


# ---------------------------------------------------------------------------
# Set operations
# ---------------------------------------------------------------------------

U = set(range(1, 11))
SET_A = {1, 2, 3, 4, 5}
SET_B = {4, 5, 6, 7}
CA = (150, 145)
CB = (250, 145)
R = 95
UW, UH = 400, 280
POS = {
    1: (100, 110), 2: (88, 165), 3: (128, 210),
    4: (200, 118), 5: (200, 172),
    6: (292, 112), 7: (300, 178),
    8: (28, 150), 9: (200, 262), 10: (372, 150),
}
A_COL = theme.BLUE
B_COL = theme.ORANGE
RES_COL = theme.GREEN


def _circle_d(cx, cy, r):
    return (f"M{fmt(cx - r)},{fmt(cy)} a{fmt(r)},{fmt(r)} 0 1 0 {fmt(2 * r)},0 "
            f"a{fmt(r)},{fmt(r)} 0 1 0 {fmt(-2 * r)},0 Z")


def _rect_d():
    return f"M0,0 H{UW} V{UH} H0 Z"


def _clip(c, d, evenodd=False):
    cid = c.unique_id("venn-clip")
    cp = c.defs.add(Element("clipPath", id=cid))
    cp.add(Element("path", d=d, clip_rule="evenodd" if evenodd else None))
    return f"url(#{cid})"


def _hatch(c, color, angle):
    pid = c.unique_id("hatch")
    pat = c.defs.add(Element("pattern", id=pid, patternUnits="userSpaceOnUse", width=9, height=9,
                             patternTransform=f"rotate({angle})"))
    pat.add(Element("line", x1=0, y1=0, x2=0, y2=9, stroke=color, stroke_width=3))
    return f"url(#{pid})"


def _venn(c, ox, oy, s, region=None, members=None, hatch=False):
    """Draws the Venn diagram at (ox, oy) scaled by s.

    region: 'union', 'inter', 'diff', 'compA', 'compUnion' shades that region in the result color.
    members: the set of elements to show in bold; others fade. None shows all in ink.
    hatch=True shades A' and B' with stripes instead.
    """
    with c.group(transform=f"translate({fmt(ox)},{fmt(oy)}) scale({s})"):
        c.rect(0, 0, UW, UH, color=theme.INK, fill=theme.PAPER, width=2)
        circA, circB = _circle_d(*CA, R), _circle_d(*CB, R)
        outA = _clip(c, _rect_d() + " " + circA, evenodd=True)
        outB = _clip(c, _rect_d() + " " + circB, evenodd=True)
        inA = _clip(c, circA)
        if region:
            with c.group(opacity=0.35):
                if region == "union":
                    c.path(circA, color="none", fill=RES_COL)
                    c.path(circB, color="none", fill=RES_COL)
                elif region == "inter":
                    with c.group(clip_path=inA):
                        c.path(circB, color="none", fill=RES_COL)
                elif region == "diff":
                    with c.group(clip_path=outB):
                        c.path(circA, color="none", fill=RES_COL)
                elif region == "compA":
                    with c.group(clip_path=outA):
                        c.rect(0, 0, UW, UH, color="none", fill=RES_COL)
                elif region == "compUnion":
                    with c.group(clip_path=outA):
                        with c.group(clip_path=outB):
                            c.rect(0, 0, UW, UH, color="none", fill=RES_COL)
        if hatch:
            with c.group(clip_path=outA, opacity=0.55):
                c.rect(0, 0, UW, UH, color="none", fill=_hatch(c, A_COL, 45))
            with c.group(clip_path=outB, opacity=0.55):
                c.rect(0, 0, UW, UH, color="none", fill=_hatch(c, B_COL, -45))
        c.path(circA, color=A_COL, width=3)
        c.path(circB, color=B_COL, width=3)
        c.text(56, 34, "A", size=22, math=True, color=A_COL, weight="bold")
        c.text(344, 34, "B", size=22, math=True, color=B_COL, weight="bold")
        c.text(UW - 12, UH - 16, "U", size=18, math=True, color=theme.SOFT_INK, anchor="end")
        for v, (x, y) in POS.items():
            if members is None:
                c.text(x, y, str(v), size=18, color=theme.INK, halo=True)
            elif v in members:
                c.text(x, y, str(v), size=19, color=theme.INK, weight="bold", halo=True)
            else:
                c.text(x, y, str(v), size=17, color=theme.MUTED, halo=True)


def _setstr(s) -> str:
    return "{" + ", ".join(str(v) for v in sorted(s)) + "}" if s else "\\emptyset"


@diagram("set-operations", "Set Operations", "Logic and Proof")
def build_set_operations() -> Walkthrough:
    wt = Walkthrough(
        "set-operations", "Set Operations with Venn Diagrams", "Logic and Proof",
        concept="(A \\cup B)' = A' \\cap B'",
        summary="Union, intersection, difference, and complement each shade a region of a Venn diagram. "
                "De Morgan's law says the outside of a union equals the overlap of the two outsides.",
        width=700, height=380, level="201",
    )
    union = SET_A | SET_B
    inter = SET_A & SET_B
    diff = SET_A - SET_B
    compA = U - SET_A
    compU = U - union
    assert compU == (U - SET_A) & (U - SET_B)
    S = 1.1
    OX, OY = 20, 34
    PX = OX + UW * S + 24

    def one(region, members, sym=None, words=None):
        def draw(c, ctx):
            _venn(c, OX, OY, S, region, members)
            y = 50
            c.math(PX, y, f"A = {_setstr(SET_A)}", size=17, color=A_COL, anchor="start")
            c.math(PX, y + 30, f"B = {_setstr(SET_B)}", size=17, color=B_COL, anchor="start")
            c.math(PX, y + 60, f"U = {{1, 2, \\ldots, 10}}", size=17, color=theme.SOFT_INK, anchor="start")
            if sym:
                c.line(PX, y + 86, 690, y + 86, color=theme.GRID, width=1.5)
                c.math(PX, y + 116, sym + " =", size=20, color=RES_COL, anchor="start")
                c.math(PX, y + 150, _setstr(members), size=20, color=RES_COL, anchor="start")
                c.paragraph(PX, y + 180, words, 690 - PX, size=14, color=theme.SOFT_INK)
                c.rect(PX, y + 250, 22, 16, color="none", fill=RES_COL, opacity=0.35)
                c.text(PX + 30, y + 258, "shaded = the answer", size=13, anchor="start", color=theme.SOFT_INK)
                c.text(PX + 2, y + 286, "bold numbers are in it", size=13, anchor="start", color=theme.SOFT_INK)
            else:
                c.paragraph(PX, y + 100, "Each number sits in the one region that matches the sets it "
                            "belongs to. 4 and 5 are in both, so they live in the overlap.",
                            690 - PX, size=14, color=theme.SOFT_INK)
        return draw

    def demorgan(c, ctx):
        s = 0.74
        w = UW * s
        lx, rx, y = 24, 700 - 24 - w, 54
        c.math(lx + w / 2, 30, "(A \\cup B)'", size=20, color=RES_COL)
        c.math(rx + w / 2, 30, "A' \\cap B'", size=20, color=theme.INK)
        _venn(c, lx, y, s, "compUnion", compU)
        _venn(c, rx, y, s, None, compU, hatch=True)
        c.text(350, y + UH * s / 2, "=", size=34, weight="bold")
        ly = y + UH * s + 26
        c.rect(rx, ly - 8, 22, 16, color=A_COL, fill=_hatch(c, A_COL, 45), width=1)
        c.text(rx + 30, ly, "A' (outside A)", size=14, anchor="start", color=A_COL)
        c.rect(rx + 150, ly - 8, 22, 16, color=B_COL, fill=_hatch(c, B_COL, -45), width=1)
        c.text(rx + 180, ly, "B' (outside B)", size=14, anchor="start", color=B_COL)
        c.text(rx + w / 2, ly + 26, "crosshatched where both stripes meet", size=14, color=theme.SOFT_INK)
        c.text(lx + w / 2, ly + 13, "outside the union", size=14, color=RES_COL)

    wt.step("Draw the universe and two sets",
            "The rectangle U holds the numbers 1 to 10. Circle A holds 1 to 5 and circle B holds 4 to 7. "
            "The overlap holds the numbers in both.",
            math=f"A = {_setstr(SET_A)},  B = {_setstr(SET_B)}", fresh=True)(one(None, None))
    wt.step("Union: in A or in B",
            "Shade everything inside either circle. The union collects every element of A and every element "
            "of B.", math=f"A \\cup B = {_setstr(union)}", fresh=True)(one("union", union, "A \\cup B", "Anything in A, in B, or in both. Union means \"or\"."))
    wt.step("Intersection: in A and in B",
            "Shade only the overlap. The intersection keeps the elements that belong to both sets.",
            math=f"A \\cap B = {_setstr(inter)}", fresh=True)(one("inter", inter, "A \\cap B", "Only what A and B share. Intersection means \"and\"."))
    wt.step("Difference: in A but not in B",
            "Start with A and remove the part inside B. The difference is the crescent of A outside the "
            "overlap.", math=f"A - B = {_setstr(diff)}", fresh=True)(one("diff", diff, "A - B", "A with every member of B thrown out."))
    wt.step("Complement: not in A",
            "Shade everything in U outside circle A. The complement depends on the universe: here it is "
            "every number from 1 to 10 that is not in A.",
            math=f"A' = {_setstr(compA)}", fresh=True)(one("compA", compA, "A'", "Everything in U that A leaves behind."))
    wt.step("Complement of the union",
            "Shade what lies outside both circles. Only the numbers in neither set remain.",
            math=f"(A \\cup B)' = {_setstr(compU)}", fresh=True)(one("compUnion", compU, "(A \\cup B)'", "The numbers neither set wants."))
    wt.step("De Morgan's law",
            "Stripe the outside of A one way and the outside of B the other way. The crosshatched region "
            "is the same region as the outside of the union.",
            math=f"(A \\cup B)' = A' \\cap B' = {_setstr(compU)}", fresh=True)(demorgan)
    return wt
