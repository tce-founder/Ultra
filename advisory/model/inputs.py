#!/usr/bin/env python3
"""
Graded inputs — value, unit, population, source and grade bound together.

WHY THIS TYPE EXISTS. A number in this domain is not usable without knowing who
it was measured on. `90` is not a fuelling target; "90 g of carbohydrate per hour,
from laboratory studies of trained cyclists and runners at intensities and
durations below an ultra, REPORTED" is. The moment the number is separated from
that context it becomes quotable by anything downstream, and nothing downstream
can recover what was dropped.

So the number and its caveat are one object, and arithmetic on graded values
propagates the weakest grade. A derived figure cannot be more certain than its
least certain input, and the commonest way that rule gets broken is not by anyone
deciding to break it — it is by the caveat living in a comment.

GRADES, in the sense used in the repository README:

  VERIFIED    traced to a primary source that was actually opened
  REPORTED    stated somewhere credible; the primary was not opened
  UNVERIFIED  assumed, modelled, or taken from the athlete's own estimate

Note that VERIFIED is about the CHECKING, and is a different axis from the corpus
schema's `authority` field, which is about the KIND of claim. A coaching
convention can be VERIFIED (we opened the book and it does say that) and still be
`experienced` rather than `established`.
"""

from dataclasses import dataclass, field
from typing import Optional

GRADES = ("VERIFIED", "REPORTED", "UNVERIFIED")
# Ordered weakest-last so `max` over indices picks the weakest.
_RANK = {g: i for i, g in enumerate(GRADES)}


@dataclass(frozen=True)
class Input:
    """A number with everything needed to refuse it."""

    value: float
    unit: str
    source: str
    grade: str = "UNVERIFIED"
    population: str = ""
    note: str = ""

    def __post_init__(self):
        if self.grade not in GRADES:
            raise ValueError(f"grade must be one of {GRADES}, got {self.grade!r}")
        if not self.unit:
            raise ValueError("unit is required — an unlabelled number is the failure this type exists to prevent")
        if not self.source:
            raise ValueError("source is required")

    def __str__(self):
        pop = f" [{self.population}]" if self.population else ""
        return f"{self.value:g} {self.unit} ({self.grade}, {self.source}){pop}"


@dataclass(frozen=True)
class Derived:
    """A computed figure that carries the weakest grade among its inputs.

    `inputs` is kept so a derived number can always be walked back to what it was
    built from. That is the whole point: when one of them turns out to be wrong,
    the question "what depends on this" has an answer.
    """

    value: float
    unit: str
    grade: str
    inputs: tuple = field(default_factory=tuple)
    note: str = ""

    def __str__(self):
        return f"{self.value:g} {self.unit} ({self.grade}, derived from {len(self.inputs)} inputs)"

    def explain(self, indent=0):
        pad = " " * indent
        lines = [f"{pad}{self}"]
        if self.note:
            lines.append(f"{pad}  note: {self.note}")
        for i in self.inputs:
            if isinstance(i, Derived):
                lines.extend(i.explain(indent + 4).split("\n"))
            else:
                lines.append(f"{pad}    <- {i}")
        return "\n".join(lines)


def weakest(*items) -> str:
    """The weakest grade among any mix of Input and Derived."""
    grades = [i.grade for i in items if isinstance(i, (Input, Derived))]
    if not grades:
        return "UNVERIFIED"
    return max(grades, key=lambda g: _RANK[g])


def derive(value, unit, *inputs, note="") -> Derived:
    """Build a Derived that inherits the weakest input grade. Use this, not the
    constructor — passing the grade by hand is how a VERIFIED label ends up on
    something built out of an assumption."""
    return Derived(value=value, unit=unit, grade=weakest(*inputs),
                   inputs=tuple(inputs), note=note)
