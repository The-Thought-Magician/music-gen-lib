"""Composition module.

This module provides classes for melody generation and musical forms.
"""

from musicgen.composition.melody import (
    MelodicContour,
    Motif,
    Phrase,
    Melody,
    MelodyGenerator,
)
from musicgen.composition.forms import (
    FormType,
    Section,
    Form,
)

__all__ = [
    "MelodicContour",
    "Motif",
    "Phrase",
    "Melody",
    "MelodyGenerator",
    "FormType",
    "Section",
    "Form",
]
