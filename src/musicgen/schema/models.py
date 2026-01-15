"""Schema models for AI-generated compositions.

These models define what the AI can generate.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class NoteFormat(str, Enum):
    """Note representation format."""
    JSON = "json"          # {"pitch": "C4", "duration": 1.0, ...}
    COMPACT = "compact"   # "C4:1.0:80" (pitch:dur:vel)
    DETAILED = "detailed" # Full JSON with all attributes


class DurationUnit(str, Enum):
    """Duration unit representation."""
    QUARTER = "quarter"    # Quarter note = 1.0
    SECOND = "second"      # Seconds
    TICK = "tick"          # MIDI ticks (480 per quarter)


class PitchRepresentation(str, Enum):
    """Pitch representation format."""
    NOTE_NAME = "note_name"     # "C4", "Ab3"
    MIDI_NUMBER = "midi_number" # 60, 69
    FREQUENCY = "frequency"     # 440.0, 880.0


@dataclass
class NoteSchema:
    """Schema for a single note."""
    pitch: PitchRepresentation
    duration: float
    duration_unit: DurationUnit
    velocity: int  # 0-127
    start_time: float | None = None  # For absolute timing
    tied: bool = False
    articulation: str | None = None  # staccato, legato, accent


@dataclass
class RestSchema:
    """Schema for a rest."""
    duration: float
    duration_unit: DurationUnit


@dataclass
class PartSchema:
    """Schema for an instrument part."""
    name: str
    midi_program: int  # 0-127
    midi_channel: int  # 0-15
    notes: list  # List[NoteSchema]
    role: str  # melody, harmony, bass, accompaniment


@dataclass
class CompositionSchema:
    """Complete schema for a composition."""
    title: str
    tempo: int  # BPM
    time_signature: str  # "4/4", "3/4", etc.
    key: str  # "C major", "A minor"
    parts: list  # List[PartSchema]

    # Optional metadata
    duration_seconds: float | None = None
    form: str | None = None
    mood: str | None = None


@dataclass
class SchemaConfig:
    """Configuration for schema generation."""
    note_format: NoteFormat = NoteFormat.DETAILED
    duration_unit: DurationUnit = DurationUnit.QUARTER
    pitch_representation: PitchRepresentation = PitchRepresentation.NOTE_NAME

    # What to include
    include_articulation: bool = True
    include_dynamics: bool = True
    include_form: bool = True
    include_key_changes: bool = True
    include_tempo_changes: bool = True
    include_time_signature_changes: bool = True

    # Constraints
    max_duration: int = 600  # seconds
    max_instruments: int = 16
    velocity_min: int = 60
    velocity_max: int = 100
