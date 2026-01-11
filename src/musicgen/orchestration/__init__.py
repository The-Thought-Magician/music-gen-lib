"""Orchestration module.

This module provides classes for instruments and ensembles.
"""

from musicgen.orchestration.instruments import (
    Instrument,
    InstrumentFamily,
    Voice,
)
from musicgen.orchestration.ensembles import (
    Texture,
    TextureType,
    Ensemble,
)

__all__ = [
    "Instrument",
    "InstrumentFamily",
    "Voice",
    "Texture",
    "TextureType",
    "Ensemble",
]
