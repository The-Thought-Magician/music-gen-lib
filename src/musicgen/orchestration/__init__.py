"""Orchestration module.

This module provides classes for instruments, ensembles, and orchestration strategies.
"""

from musicgen.orchestration.ensembles import (
    Ensemble,
    Texture,
    TextureType,
)
from musicgen.orchestration.instruments import (
    Instrument,
    InstrumentFamily,
    Voice,
)
from musicgen.orchestration.strategies import (
    OrchestrationBuilder,
    OrchestrationStrategies,
    TextureDensity,
    TexturePlan,
    get_preset,
)

__all__ = [
    "Instrument",
    "InstrumentFamily",
    "Voice",
    "Texture",
    "TextureType",
    "Ensemble",
    "OrchestrationStrategies",
    "OrchestrationBuilder",
    "TexturePlan",
    "TextureDensity",
    "get_preset",
]
