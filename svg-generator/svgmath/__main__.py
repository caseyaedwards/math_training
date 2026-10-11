"""Command-line interface.

    python3 -m svgmath list                       # every diagram type
    python3 -m svgmath render SLUG --out DIR      # SVGs for one diagram
    python3 -m svgmath showcase [--out DIR]       # rebuild the showcase site
"""

from __future__ import annotations

import argparse
import os
import sys

from . import showcase
from .registry import all_diagrams, get

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SHOWCASE = os.path.join(os.path.dirname(HERE), "showcase")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="svgmath", description="Step-by-step SVG diagrams for math.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="list every diagram type")

    r = sub.add_parser("render", help="render one diagram type")
    r.add_argument("slug")
    r.add_argument("--out", default=".", help="output folder (default: current folder)")

    s = sub.add_parser("showcase", help="build the HTML showcase")
    s.add_argument("--out", default=DEFAULT_SHOWCASE)
    s.add_argument("--only", nargs="*", help="rebuild only these slugs")

    args = ap.parse_args(argv)

    if args.cmd == "list":
        cat = None
        for d in all_diagrams():
            if d.category != cat:
                cat = d.category
                print(f"\n{cat}")
            print(f"  {d.slug:32s} {d.title}")
        return 0

    if args.cmd == "render":
        d = get(args.slug)
        os.makedirs(args.out, exist_ok=True)
        showcase.render_diagram(d, args.out)
        print(os.path.join(args.out, d.slug))
        return 0

    if args.cmd == "showcase":
        pages = showcase.build(args.out, only=args.only)
        print(f"wrote {len(pages)} diagrams to {args.out}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
