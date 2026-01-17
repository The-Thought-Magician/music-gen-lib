"""V3 Composition models.

These models represent a complete musical composition with all metadata,
structural elements, and instrument parts needed for SFZ rendering.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

# Type aliases for common values
StylePeriod = Literal[
    "baroque",
    "classical",
    "romantic",
    "modern",
    "film_score",
    "contemporary",
]

MusicalForm = Literal[
    "binary",  # AB
    "ternary",  # ABA
    "rondo",  # ABACA...
    "sonata",  # Exposition-Development-Recapitulation
    "theme_and_variations",
    "minuet",  # Minuet-Trio-Minuet
    "scherzo",
    "through_composed",
    "strophic",
]

TempoMarking = Literal[
    "larghissimo",
    "grave",
    "largo",
    "lento",
    "adagio",
    "larghetto",
    "adagietto",
    "andante",
    "andantino",
    "moderato",
    "allegretto",
    "allegro",
    "vivace",
    "presto",
    "prestissimo",
    # Tempo change indications
    "ritardando",
    "rallentando",
    "accelerando",
    "a_tempo",
]

DynamicMarking = Literal[
    "ppp",
    "pp",
    "p",
    "mp",
    "mf",
    "f",
    "ff",
    "fff",
]

# Helper functions for tempo and dynamic mappings
def get_tempo_bpm_range(tempo: TempoMarking) -> tuple[int, int]:
    """Get typical BPM range for a tempo marking."""
    ranges = {
        "larghissimo": (20, 40),
        "grave": (30, 45),
        "largo": (40, 60),
        "lento": (45, 60),
        "adagio": (50, 70),
        "larghetto": (60, 70),
        "adagietto": (65, 80),
        "andante": (70, 85),
        "andantino": (80, 95),
        "moderato": (85, 100),
        "allegretto": (100, 115),
        "allegro": (115, 140),
        "vivace": (135, 160),
        "presto": (150, 180),
        "prestissimo": (170, 220),
        # Tempo change indications (return current tempo range)
        "ritardando": (60, 120),
        "rallentando": (60, 120),
        "accelerando": (60, 120),
        "a_tempo": (60, 120),
    }
    return ranges.get(tempo, (60, 120))


def get_dynamic_velocity(dynamic: DynamicMarking) -> int:
    """Get approximate MIDI velocity for a dynamic marking."""
    velocities = {
        "ppp": 16, "pp": 32, "p": 48, "mp": 64,
        "mf": 80, "f": 96, "ff": 112, "fff": 127
    }
    return velocities.get(dynamic, 80)


class TimeSignature(BaseModel):
    """A time signature."""

    numerator: int = Field(
        ge=1,
        description="Top number (beats per measure)"
    )
    denominator: int = Field(
        ge=1,
        description="Bottom number (note value for one beat)"
    )


class SectionMarker(BaseModel):
    """A marker for musical sections (A, B, bridge, etc.)."""

    label: str = Field(description="Section label (e.g., 'A', 'B', 'Coda')")
    time: float = Field(
        ge=0,
        description="Time in seconds"
    )
    rehearsal_letter: str | None = Field(
        default=None,
        description="Rehearsal letter (A, B, C, etc.)"
    )


class TempoChange(BaseModel):
    """A tempo change event."""

    tempo_bpm: float = Field(
        gt=0,
        description="Tempo in beats per minute"
    )
    time: float = Field(
        ge=0,
        description="Time in seconds"
    )
    tempo_marking: TempoMarking | None = None

    @field_validator("tempo_marking", mode="before")
    @classmethod
    def normalize_tempo_marking(cls, v: str | None) -> str | None:
        """Normalize tempo marking to lowercase before validation."""
        if v is None:
            return None
        return v.lower()


class TimeSignatureChange(BaseModel):
    """A time signature change event."""

    time_signature: TimeSignature
    time: float = Field(
        ge=0,
        description="Time in seconds"
    )


class DynamicChange(BaseModel):
    """A dynamic marking change."""

    dynamic: DynamicMarking = Field(description="Dynamic marking (ppp through fff)")
    time: float = Field(
        ge=0,
        description="Time in seconds"
    )
    ramp_duration: float | None = Field(
        default=None,
        description="Duration for crescendo/diminuendo in seconds"
    )


class Composition(BaseModel):
    """A complete musical composition.

    Contains all metadata, structural events, and instrument parts
    needed for rendering to audio via SFZ libraries.
    """

    # Metadata
    title: str = Field(description="Title of the composition")
    composer: str | None = Field(
        default="AI Composer",
        description="Composer name"
    )
    description: str | None = Field(
        default=None,
        description="Description of the piece"
    )

    # Style and Form
    style_period: StylePeriod | None = None
    musical_form: MusicalForm | None = None
    key_signature: str = Field(
        description="Key signature (e.g., 'C major', 'A minor')"
    )

    # Tempo and Meter
    initial_tempo_bpm: float = Field(
        gt=0,
        description="Initial tempo in BPM"
    )
    tempo_marking: TempoMarking | None = None
    time_signature: TimeSignature = Field(
        default_factory=lambda: TimeSignature(numerator=4, denominator=4)
    )

    # Structural Events
    tempo_changes: list[TempoChange] = Field(
        default_factory=list,
        description="Tempo change events"
    )
    time_signature_changes: list[TimeSignatureChange] = Field(
        default_factory=list,
        description="Time signature change events"
    )
    section_markers: list[SectionMarker] = Field(
        default_factory=list,
        description="Section markers (A, B, bridge, etc.)"
    )
    dynamic_changes: list[DynamicChange] = Field(
        default_factory=list,
        description="Dynamic change events"
    )

    # Instrumentation
    parts: list["InstrumentPart"] = Field(
        default_factory=list,
        description="Instrument parts"
    )

    # Performance notes
    performance_notes: str | None = Field(
        default=None,
        description="Notes for performers/conductors"
    )

    @field_validator("tempo_marking", mode="before")
    @classmethod
    def normalize_tempo_marking(cls, v: str | None) -> str | None:
        """Normalize tempo marking to lowercase before validation."""
        if v is None:
            return None
        return v.lower()

    @field_validator("musical_form", mode="before")
    @classmethod
    def normalize_musical_form(cls, v: str | None) -> str | None:
        """Normalize musical form (replace hyphens with underscores) before validation."""
        if v is None:
            return None
        # Common AI mistake: "through-composed" -> "through_composed"
        return v.replace("-", "_")

    @property
    def duration(self) -> float:
        """Get total duration of the composition in seconds."""
        if not self.parts:
            return 0.0
        from musicgen.ai_models.v3.parts import InstrumentPart
        return max(
            (p.get_duration() for p in self.parts if isinstance(p, InstrumentPart)),
            default=0.0
        )

    @property
    def instrument_count(self) -> int:
        """Get number of instruments."""
        return len(self.parts)

    def get_parts_by_family(self, family: str) -> list["InstrumentPart"]:
        """Get all parts of a specific instrument family."""
        from musicgen.ai_models.v3.parts import InstrumentPart
        return [
            p for p in self.parts
            if isinstance(p, InstrumentPart) and p.instrument_family == family
        ]

    def get_solo_parts(self) -> list["InstrumentPart"]:
        """Get all solo parts."""
        from musicgen.ai_models.v3.parts import InstrumentPart
        return [
            p for p in self.parts
            if isinstance(p, InstrumentPart) and p.solo
        ]


# Import InstrumentPart for type hints and update forward references
# ruff: noqa: E402
from musicgen.ai_models.v3.parts import InstrumentPart

Composition.model_rebuild()


class CompositionRequest(BaseModel):
    """Request for AI composition generation."""

    # User input
    prompt: str = Field(description="Natural language description of desired music")

    # Constraints
    duration_seconds: float | None = Field(
        default=None,
        ge=10,
        le=600,
        description="Target duration in seconds"
    )
    key_signature: str | None = Field(
        default=None,
        description="Key signature (e.g., 'C major', 'A minor')"
    )

    # Style guidance
    style_period: StylePeriod | None = None
    musical_form: MusicalForm | None = None
    mood: str | None = None

    # Orchestration
    ensemble: str | None = Field(
        default=None,
        description="Ensemble preset (e.g., 'string_quartet', 'full_orchestra')"
    )
    instruments: list[str] | None = Field(
        default=None,
        description="Specific instruments to include"
    )

    # Output options
    output_format: Literal["midi", "wav", "mp3", "all"] = "midi"
    include_stems: bool = Field(
        default=False,
        description="Export individual instrument stems"
    )


class CompositionResponse(BaseModel):
    """Response from AI composition generation."""

    composition: Composition
    metadata: dict = Field(
        default_factory=dict,
        description="Additional metadata about the generation"
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings generated during composition"
    )
    validation_errors: list[str] = Field(
        default_factory=list,
        description="Validation errors (non-critical)"
    )
