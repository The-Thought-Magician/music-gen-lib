"""AI-generated composition models.

These models validate AI output and provide type-safe structures.
"""

from musicgen.ai_models.composition import (
    AIComposition,
    KeySignature,
    TimeSignature,
)
from musicgen.ai_models.notes import (
    AINote,
    AINoteEvent,
    AIRest,
    ArticulationType,
)
from musicgen.ai_models.parts import (
    AIPart,
    InstrumentRole,
)

__all__ = [
    # Notes
    "AINote",
    "AIRest",
    "AINoteEvent",
    "ArticulationType",
    # Parts
    "AIPart",
    "InstrumentRole",
    # Composition
    "AIComposition",
    "TimeSignature",
    "KeySignature",
]
