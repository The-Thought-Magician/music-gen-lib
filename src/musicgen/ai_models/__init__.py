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
    CC,
    AINote,
    AINoteEvent,
    AIRest,
    ArticulationType,
    ControlChangeEvent,
)
from musicgen.ai_models.parts import (
    AIPart,
    InstrumentRole,
)

# Post-processing
from musicgen.ai_models.postprocess import (
    ValidationResult,
    auto_fix_composition,
    fix_polyphony,
    get_polyphony_report,
    is_harmony_role,
    validate_composition,
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
    # Post-processing
    "ValidationResult",
    "validate_composition",
    "fix_polyphony",
    "auto_fix_composition",
    "get_polyphony_report",
    "is_harmony_role",
]
