"""AI-generated composition models.

These models validate AI output and provide type-safe structures.
"""

from musicgen.ai_models.composition import (
    AIComposition,
    AIMeasure,
    KeySignature,
    StructureType,
    TempoEvent,
    TimeSignature,
    TimeSignatureEvent,
)
from musicgen.ai_models.notes import (
    AINote,
    AINoteEvent,
    AIRest,
    ArticulationType,
    CC,
    ControlChangeEvent,
)
from musicgen.ai_models.parts import (
    AIPart,
    InstrumentRole,
)
from musicgen.ai_models.sections import AISection

__all__ = [
    # Notes
    "AINote",
    "AIRest",
    "AINoteEvent",
    "ArticulationType",
    "ControlChangeEvent",
    "CC",
    # Parts
    "AIPart",
    "InstrumentRole",
    # Composition
    "AIComposition",
    "AIMeasure",
    "AISection",
    "TimeSignature",
    "TimeSignatureEvent",
    "TempoEvent",
    "KeySignature",
    "StructureType",
]
