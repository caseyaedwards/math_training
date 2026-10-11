"""Checks every registered diagram: it builds, renders, and follows the writing rules."""

from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET

from svgmath.registry import all_diagrams

# Words and phrases the writing guide rules out, with a hint for each
BANNED = {
    r"\bwill\b": "use present tense",
    r"\bshould\b": "use must, or rephrase",
    r"\bplease\b": "drop it",
    r"\be\.g\.": "use for example",
    r"\bi\.e\.": "use that is",
    r"\bin order to\b": "use to",
    r"\bmake sure\b": "use check, or rephrase",
    r"\b\w+n't\b": "avoid contractions",
    r"\blet's\b": "avoid contractions",
    r"\b(it|that|there|what)'s\b": "avoid contractions",
    r"\band/or\b": "rephrase",
}

SVG_NS = "{http://www.w3.org/2000/svg}"


def prose(wt):
    yield "summary", wt.summary
    for i, st in enumerate(wt.steps, 1):
        yield f"step {i} title", st.title
        yield f"step {i} text", st.text


class DiagramTests(unittest.TestCase):
    def test_registry_not_empty(self):
        self.assertGreater(len(all_diagrams()), 0)

    def test_each_diagram(self):
        for d in all_diagrams():
            with self.subTest(d.slug):
                wt = d.build()
                self.assertEqual(wt.slug, d.slug, "Walkthrough slug must match the @diagram slug")
                self.assertEqual(wt.category, d.category, "Walkthrough category must match the @diagram category")
                self.assertGreaterEqual(len(wt.steps), 2, "a walkthrough needs at least two steps")
                self.assertTrue(wt.concept, "set concept to a one-line statement of the idea")
                self.assertTrue(wt.summary, "set summary to one or two plain sentences")
                for i, st in enumerate(wt.steps, 1):
                    self.assertTrue(st.title and st.text, f"step {i} needs a title and text")
                    self.assertFalse(st.title.endswith("."), f"step {i} title must not end with a period")
                outputs = [wt.render_step(k) for k in range(len(wt.steps))]
                outputs += [wt.storyboard(), wt.animated(), wt.final()]
                for canvas in outputs:
                    svg = canvas.to_svg()
                    root = ET.fromstring(svg.split("\n", 1)[1])
                    ids = [el.get("id") for el in root.iter() if el.get("id")]
                    dupes = {i for i in ids if ids.count(i) > 1}
                    self.assertFalse(dupes, f"duplicate ids {sorted(dupes)[:5]}")
                    self.assertNotIn("nan", re.findall(r'="(nan|inf)"', svg))

    def test_writing_rules(self):
        problems = []
        for d in all_diagrams():
            wt = d.build()
            for where, text in prose(wt):
                for pat, hint in BANNED.items():
                    for m in re.finditer(pat, text or "", re.IGNORECASE):
                        problems.append(f"{d.slug} {where}: '{m.group(0)}' ({hint})")
        self.assertFalse(problems, "\n" + "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
