"""Orchestration module.

This module provides classes for instruments, ensembles, and orchestration strategies.
"""

# V1/V2 orchestration (existing)
# V3 instrument definitions (new)
from musicgen.orchestration.definitions import (
    Articulation,
    Clef,
    DynamicMarking,
    DynamicRange,
    EnsembleDefinition,
    InstrumentDefinition,
    InstrumentFamily,
    get_ensemble,
    get_instrument,
    get_instrument_library,
    list_ensembles,
    list_instruments_by_family,
    load_instrument_definitions,
)
from musicgen.orchestration.ensembles import (
    Ensemble,
    Texture,
    TextureType,
)
from musicgen.orchestration.instruments import (
    Instrument,
    Voice,
)
from musicgen.orchestration.instruments import (
    InstrumentFamily as InstrumentFamilyV2,
)
from musicgen.orchestration.strategies import (
    OrchestrationBuilder,
    OrchestrationStrategies,
    TextureDensity,
    TexturePlan,
    get_preset,
)

# Re-export V2 InstrumentFamily with alias to maintain compatibility
InstrumentFamilyV1 = InstrumentFamilyV2

__all__ = [
    # V1/V2 exports
    "Instrument",
    "InstrumentFamilyV1",
    "Voice",
    "Texture",
    "TextureType",
    "Ensemble",
    "OrchestrationStrategies",
    "OrchestrationBuilder",
    "TexturePlan",
    "TextureDensity",
    "get_preset",
    # V3 exports
    "InstrumentDefinition",
    "EnsembleDefinition",
    "DynamicRange",
    "Articulation",
    "InstrumentFamily",
    "Clef",
    "DynamicMarking",
    "load_instrument_definitions",
    "get_instrument_library",
    "get_instrument",
    "get_ensemble",
    "list_ensembles",
    "list_instruments_by_family",
]
