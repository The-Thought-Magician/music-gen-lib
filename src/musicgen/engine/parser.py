"""YAML composition specification parser and models.

This module defines the schema for YAML-based music generation specifications.
The YAML file serves as the interface between AI (configuration) and the rule-based
music generation engine (execution).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from types import NoneType, UnionType
from typing import Any, ForwardRef, Union, get_args, get_origin, get_type_hints

import yaml

from musicgen.core.note import Note
from musicgen.io.midi_writer import Part, Score


# =============================================================================
# Models
# =============================================================================


@dataclass
class KeySpec:
    """Musical key specification."""
    root: str
    mode: str = "major"  # major, minor, dorian, phrygian, lydian, mixolydian, locrian
    octave: int = 4


@dataclass
class TempoSpec:
    """Tempo and timing specification."""
    bpm: float
    fluctuations: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class TimeSignatureSpec:
    """Time signature specification."""
    numerator: int
    denominator: int


@dataclass
class StyleSpec:
    """Style and mood specification."""
    complexity: str = "medium"  # low, medium, high
    mood: str = "neutral"  # For genre-specific moods
    ornamentation: str = "medium"  # none, light, medium, heavy


@dataclass
class SectionSpec:
    """A section of the composition (e.g., alap, gat, verse, chorus)."""
    name: str
    duration_bars: float = 16.0
    tempo_multiplier: float = 1.0
    tala: str | None = None
    laya: str | None = None  # vilambit, drut for Indian classical


@dataclass
class DroneNoteSpec:
    """Specification for a drone note (e.g., tanpura)."""
    note: str  # Note name like "C3"
    detune_cents: int = 0  # Detuning in cents
    velocity: int = 64
    start_offset: float = 0.0  # Start time offset for creating overlap


@dataclass
class InstrumentSpec:
    """Instrument specification."""
    name: str
    family: str  # strings, percussion, drone, winds, brass, keyboards, electronic
    role: str  # melody, harmony, bass, rhythm, drone
    channel: int
    midi_program: int | None = None
    drone_notes: list[DroneNoteSpec] | None = None
    stroke_mapping: dict[str, int] | None = None  # For tabla: {"ge": 36, "ke": 40}


@dataclass
class NoteDensitySpec:
    """Note generation parameters."""
    notes_per_minute: tuple[int, int] = (60, 100)
    avg_duration_beats: tuple[float, float] = (0.5, 1.5)
    duration_range: tuple[float, float] = (0.25, 2.0)


@dataclass
class PhraseSpec:
    """Melodic phrase structure."""
    length_bars: tuple[int, int] = (4, 8)
    development: str = "mixed"  # ascending, descending, arc, mixed
    repetition: bool = True


@dataclass
class RegisterSpec:
    """Register (octave range) specification."""
    lowest_octave: int = 3
    highest_octave: int = 6
    emphasis: str = "middle"  # low, middle, high


@dataclass
class OrnamentationSpec:
    """Ornamentation preferences."""
    meend: str = "none"  # none, rare, occasional, frequent
    gamaka: str = "none"  # none, light, medium, heavy
    krintan: str = "none"  # none, rare, occasional, frequent


@dataclass
class MelodyRulesSpec:
    """Rules for melody generation."""
    source: str  # raga, scale, chord_progression, motif
    raga: str | None = None
    scale: str | None = None
    key: KeySpec | None = None
    chord_progression: list[str] | None = None
    density: NoteDensitySpec = field(default_factory=NoteDensitySpec)
    phrases: PhraseSpec = field(default_factory=PhraseSpec)
    register: RegisterSpec = field(default_factory=RegisterSpec)
    ornamentation: OrnamentationSpec = field(default_factory=OrnamentationSpec)


@dataclass
class RhythmRulesSpec:
    """Rules for rhythm generation."""
    source: str  # tala, groove, pattern
    tala: str | None = None
    cycle_beats: int = 16
    division: list[int] | None = None
    accent_pattern: list[int] | None = None
    bols: list[str] | None = None  # For tabla


@dataclass
class CompositionSpec:
    """Top-level composition specification."""
    # Required parameters (must come first in dataclass)
    title: str
    key: KeySpec
    tempo: TempoSpec
    time_signature: TimeSignatureSpec

    # Optional parameters with defaults
    composer: str = ""
    duration_seconds: float = 240
    genre: str = "classical"  # indian_classical, jazz, rock, electronic, classical
    style: StyleSpec = field(default_factory=StyleSpec)
    sections: list[SectionSpec] = field(default_factory=list)
    instruments: list[InstrumentSpec] = field(default_factory=list)
    melody_rules: MelodyRulesSpec | None = None
    rhythm_rules: RhythmRulesSpec | None = None


# =============================================================================
# Parser
# =============================================================================


def _parse_dict(cls: type, data: dict[str, Any]) -> Any:
    """Recursively parse a dict into a dataclass.

    Args:
        cls: Target dataclass type
        data: Dictionary to parse

    Returns:
        Instance of the dataclass
    """
    if not isinstance(data, dict):
        return data

    # Get type hints for this class (evaluates string annotations)
    try:
        hints = get_type_hints(cls)
    except Exception:
        # Fallback to raw annotations if get_type_hints fails
        if hasattr(cls, "__annotations__"):
            hints = cls.__annotations__
        else:
            return cls(**data)

    parsed = {}
    for key, value in data.items():
        if key not in hints:
            parsed[key] = value
            continue

        type_hint = hints[key]

        # Get origin and args for proper type inspection
        origin = get_origin(type_hint)
        args = get_args(type_hint)

        # Handle Optional types (Union with None) - supports both Union and X | None
        if origin is Union or origin is UnionType:
            # Check if any arg is None (makes it Optional)
            is_optional = any(arg is type(None) for arg in args)
            if is_optional:
                if value is None:
                    parsed[key] = None
                    continue
                # Get the non-None type
                non_none_type = args[0] if args[1] is type(None) else args[1]
                # If the non-None type is a list, handle it
                non_none_origin = get_origin(non_none_type)
                non_none_args = get_args(non_none_type)
                if non_none_origin is list:
                    # Parse list items
                    inner_type = non_none_args[0] if non_none_args else Any
                    parsed[key] = [_parse_dict(inner_type, item) if isinstance(item, dict) else item for item in value]
                elif isinstance(value, dict) and hasattr(non_none_type, "__dataclass_fields__"):
                    parsed[key] = _parse_dict(non_none_type, value)
                else:
                    parsed[key] = value
                continue

        # Handle list types
        if origin is list:
            if value is None:
                parsed[key] = None
            else:
                # Get the inner type
                inner_type = args[0] if args else Any
                parsed[key] = [_parse_dict(inner_type, item) if isinstance(item, dict) else item for item in value]
            continue

        # Handle dataclass types
        if isinstance(value, dict):
            # Check if the type hint is a dataclass
            if hasattr(type_hint, "__dataclass_fields__"):
                parsed[key] = _parse_dict(type_hint, value)
            else:
                parsed[key] = value
        else:
            parsed[key] = value

    return cls(**parsed)


def load_yaml(yaml_path: str | Path) -> CompositionSpec:
    """Load a YAML composition specification from a file.

    Args:
        yaml_path: Path to YAML file

    Returns:
        Parsed CompositionSpec

    Raises:
        FileNotFoundError: If file doesn't exist
        yaml.YAMLError: If YAML is invalid
        ValidationError: If spec is invalid
    """
    path = Path(yaml_path)

    if not path.exists():
        raise FileNotFoundError(f"YAML specification not found: {path}")

    with open(path) as f:
        data = yaml.safe_load(f)

    if not data:
        raise ValueError(f"Empty YAML specification: {path}")

    return _parse_dict(CompositionSpec, data)


def save_yaml(spec: CompositionSpec, yaml_path: str | Path) -> None:
    """Save a composition specification to YAML file.

    Args:
        spec: CompositionSpec to save
        yaml_path: Output path
    """
    path = Path(yaml_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = spec.model_dump(mode="dict", exclude_unset=True)

    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=False)


# =============================================================================
# Validation
# =============================================================================


class ValidationError(Exception):
    """Raised when the composition specification is invalid."""
    pass


def validate_spec(spec: CompositionSpec) -> list[str]:
    """Validate a composition specification.

    Returns:
        List of validation errors (empty if valid)

    Raises:
        ValidationError: If validation fails critically
    """
    errors = []

    # Validate tempo
    if spec.tempo.bpm < 20 or spec.tempo.bpm > 300:
        errors.append(f"Invalid tempo: {spec.tempo.bpm} BPM (must be 20-300)")

    # Validate time signature
    if spec.time_signature.denominator not in (1, 2, 4, 8, 16):
        errors.append(f"Invalid time signature denominator: {spec.time_signature.denominator}")

    # Validate sections
    total_duration = 0
    for section in spec.sections:
        total_duration += section.duration_bars

    if spec.duration_seconds > 0 and total_duration == 0:
        errors.append("No sections defined or total duration is zero")

    # Validate instruments
    instrument_roles = set()
    for inst in spec.instruments:
        instrument_roles.add(inst.role)

    # Require at least melody
    if "melody" not in instrument_roles:
        errors.append("No melody instrument defined")

    # For Indian classical, require specific instrument types
    if spec.genre == "indian_classical":
        # Need at least: melody (sitar/sarod/bansuri/santoor), rhythm (tabla), drone (tanpura)
        has_melody = any(inst.role == "melody" for inst in spec.instruments)
        has_rhythm = any(inst.role == "rhythm" for inst in spec.instruments)
        has_drone = any(inst.role == "drone" for inst in spec.instruments)

        if not has_melody:
            errors.append("Indian classical requires a melody instrument (sitar, sarod, bansuri, santoor, etc.)")
        if not has_rhythm:
            errors.append("Indian classical requires a rhythm instrument (tabla, pakhawaj, etc.)")
        if not has_drone:
            errors.append("Indian classical requires a drone instrument (tanpura)")

    return errors
