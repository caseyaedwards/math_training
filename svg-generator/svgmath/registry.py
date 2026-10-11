"""Registry of diagram types.

Each module in `svgmath.diagrams` registers one or more walkthrough
builders with the `diagram` decorator. A builder takes no arguments and
returns a `Walkthrough` with a worked example.

    @diagram("number-line-addition", "Adding on a Number Line", "Arithmetic")
    def build() -> Walkthrough: ...
"""

from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from typing import Callable, Dict, List

from .walkthrough import Walkthrough

# Display order for categories in the showcase. Unknown categories sort last.
CATEGORIES = [
    "Arithmetic",
    "Fractions and Ratios",
    "Number Theory",
    "Algebra",
    "Functions",
    "Geometry",
    "Trigonometry",
    "Calculus",
    "Linear Algebra",
    "Probability",
    "Statistics",
    "Discrete Math",
    "Logic and Proof",
    "Complex Numbers",
    "Sequences and Series",
    "Differential Equations",
    "Concept Maps",
]


@dataclass
class DiagramType:
    slug: str
    title: str
    category: str
    build: Callable[[], Walkthrough]
    module: str


_REGISTRY: Dict[str, DiagramType] = {}


def diagram(slug: str, title: str, category: str):
    """Registers a walkthrough builder under a unique slug."""
    def deco(fn: Callable[[], Walkthrough]):
        if slug in _REGISTRY:
            raise ValueError(f"duplicate diagram slug {slug!r} in {fn.__module__}")
        _REGISTRY[slug] = DiagramType(slug, title, category, fn, fn.__module__)
        return fn
    return deco


def load_all() -> None:
    """Imports every module in svgmath.diagrams so they can register."""
    from . import diagrams

    for mod in pkgutil.iter_modules(diagrams.__path__):
        if not mod.name.startswith("_"):
            importlib.import_module(f"{diagrams.__name__}.{mod.name}")


def all_diagrams() -> List[DiagramType]:
    load_all()

    def key(d: DiagramType):
        cat = CATEGORIES.index(d.category) if d.category in CATEGORIES else len(CATEGORIES)
        return (cat, d.category, d.module, d.slug)

    return sorted(_REGISTRY.values(), key=key)


def get(slug: str) -> DiagramType:
    load_all()
    if slug not in _REGISTRY:
        raise KeyError(f"unknown diagram {slug!r}; run `python3 -m svgmath list`")
    return _REGISTRY[slug]
