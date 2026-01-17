"""V3 AI-generated composition models.

These models provide complete support for SFZ-based orchestral rendering
with articulations, keyswitches, and full validation.
"""

# ============================================================================
# Articulation Models
# ============================================================================
from musicgen.ai_models.v3.articulation import (
    DEFAULT_DURATION_MULTIPLIERS,
    DEFAULT_VELOCITY_MULTIPLIERS,
    ArticulationDefinition,
    ArticulationType,
    KeyswitchEvent,
)

# ============================================================================
# Composition Models
# ============================================================================
from musicgen.ai_models.v3.composition import (
    Composition,
    CompositionRequest,
    CompositionResponse,
    DynamicChange,
    DynamicMarking,
    MusicalForm,
    SectionMarker,
    StylePeriod,
    TempoChange,
    TempoMarking,
    TimeSignature,
    TimeSignatureChange,
    get_dynamic_velocity,
    get_tempo_bpm_range,
)

# ============================================================================
# Note and Event Models
# ============================================================================
from musicgen.ai_models.v3.notes import (
    CC,
    CCEvent,
    Note,
    PitchBendEvent,
    ProgramChangeEvent,
)

# ============================================================================
# Part Models
# ============================================================================
from musicgen.ai_models.v3.parts import (
    InstrumentPart,
)

__all__ = [
    # Articulation
    "ArticulationType",
    "KeyswitchEvent",
    "ArticulationDefinition",
    "DEFAULT_DURATION_MULTIPLIERS",
    "DEFAULT_VELOCITY_MULTIPLIERS",
    # Notes and Events
    "Note",
    "CCEvent",
    "CC",
    "PitchBendEvent",
    "ProgramChangeEvent",
    # Parts
    "InstrumentPart",
    # Composition
    "Composition",
    "CompositionRequest",
    "CompositionResponse",
    "StylePeriod",
    "MusicalForm",
    "TempoMarking",
    "DynamicMarking",
    "TimeSignature",
    "SectionMarker",
    "TempoChange",
    "TimeSignatureChange",
    "DynamicChange",
    # Helper functions
    "get_tempo_bpm_range",
    "get_dynamic_velocity",
]
