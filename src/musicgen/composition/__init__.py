"""Composition module.

This module provides classes for melody generation and musical forms.
"""

from musicgen.composition.forms import (
    Form,
    FormType,
    Section,
)
from musicgen.composition.melody import (
    MelodicContour,
    Melody,
    MelodyGenerator,
    Motif,
    Phrase,
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
