"""
Drum articulation system for music-gen-lib V4.

This module provides drum-specific articulations and playing techniques
for realistic drum rendering.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    pass


# =============================================================================
# Drum Stick Types
# =============================================================================


@dataclass
class StickType:
    """Drum stick type characteristics."""

    name: str
    material: str
    tip: Literal["round", "acorn", "barrel", "diamond", "triangle", "none", "bundle"]
    length: str
    diameter: str
    velocity_modifier: float = 1.0
    attack_character: Literal["sharp", "muted", "warm"] = "sharp"


STICK_TYPES: dict[str, StickType] = {
    "5a": StickType(
        name="5A",
        material="hickory",
        tip="acorn",
        length="16",
        diameter="0.565",
    ),
    "5b": StickType(
        name="5B",
        material="hickory",
        tip="acorn",
        length="16-1/2",
        diameter="0.595",
        velocity_modifier=1.05,
    ),
    "7a": StickType(
        name="7A",
        material="hickory",
        tip="acorn",
        length="15-1/2",
        diameter="0.535",
        velocity_modifier=0.9,
    ),
    "rock": StickType(
        name="Rock",
        material="hickory",
        tip="round",
        length="16-3/4",
        diameter="0.630",
        velocity_modifier=1.1,
    ),
    "brushes": StickType(
        name="Brushes",
        material="wire",
        tip="none",
        length="variable",
        diameter="n/a",
        velocity_modifier=0.6,
        attack_character="muted",
    ),
    "mallets": StickType(
        name="Mallets",
        material="rubber",
        tip="round",
        length="variable",
        diameter="variable",
        velocity_modifier=0.85,
        attack_character="warm",
    ),
    "rods": StickType(
        name="Rods",
        material="birch",
        tip="bundle",
        length="16",
        diameter="bundle",
        velocity_modifier=0.75,
        attack_character="warm",
    ),
    "hands": StickType(
        name="Hands",
        material="none",
        tip="none",
        length="n/a",
        diameter="n/a",
        velocity_modifier=0.7,
        attack_character="muted",
    ),
}


# =============================================================================
# Hi-Hat Articulations
# =============================================================================


@dataclass
class HiHatArticulation:
    """Hi-hat playing technique."""

    name: str
    midi_note_base: int
    open_duration: float  # How long hat stays open
    velocity_mod: float
    duration_mod: float


HIHAT_ARTICULATIONS: dict[str, HiHatArticulation] = {
    "closed": HiHatArticulation(
        name="Closed",
        midi_note_base=42,
        open_duration=0.0,
        velocity_mod=1.0,
        duration_mod=0.05,
    ),
    "half_open": HiHatArticulation(
        name="Half Open",
        midi_note_base=42,
        open_duration=0.1,
        velocity_mod=0.95,
        duration_mod=0.15,
    ),
    "open": HiHatArticulation(
        name="Open",
        midi_note_base=46,
        open_duration=0.3,
        velocity_mod=1.0,
        duration_mod=0.4,
    ),
    "loose": HiHatArticulation(
        name="Loose",
        midi_note_base=46,
        open_duration=0.2,
        velocity_mod=0.9,
        duration_mod=0.25,
    ),
    "foot_chick": HiHatArticulation(
        name="Foot Chick",
        midi_note_base=44,
        open_duration=0.0,
        velocity_mod=0.7,
        duration_mod=0.02,
    ),
    "splash": HiHatArticulation(
        name="Splash",
        midi_note_base=46,
        open_duration=0.15,
        velocity_mod=1.1,
        duration_mod=0.2,
    ),
}


# =============================================================================
# Snare Articulations
# =============================================================================


@dataclass
class SnareArticulation:
    """Snare drum playing technique."""

    name: str
    hit_zone: Literal["center", "edge", "rim", "cross_stick"]
    stick_type: str
    velocity_mod: float
    duration_mod: float
    tone_mod: float  # Brightness adjustment (0-1)
    snare_wires: bool = True
    midi_note_override: int | None = None


SNARE_ARTICULATIONS: dict[str, SnareArticulation] = {
    "center": SnareArticulation(
        name="Center Hit",
        hit_zone="center",
        stick_type="5a",
        velocity_mod=1.0,
        duration_mod=0.15,
        tone_mod=0.5,
    ),
    "rimshot": SnareArticulation(
        name="Rimshot",
        hit_zone="rim",
        stick_type="5a",
        velocity_mod=1.3,
        duration_mod=0.12,
        tone_mod=0.9,
        midi_note_override=37,
    ),
    "cross_stick": SnareArticulation(
        name="Cross Stick",
        hit_zone="cross_stick",
        stick_type="5a",
        velocity_mod=0.8,
        duration_mod=0.08,
        tone_mod=0.3,
        midi_note_override=37,
    ),
    "ghost": SnareArticulation(
        name="Ghost Note",
        hit_zone="center",
        stick_type="5a",
        velocity_mod=0.4,
        duration_mod=0.08,
        tone_mod=0.4,
    ),
    "brush_sweep": SnareArticulation(
        name="Brush Sweep",
        hit_zone="center",
        stick_type="brushes",
        velocity_mod=0.6,
        duration_mod=0.2,
        tone_mod=0.6,
    ),
}


# =============================================================================
# Cymbal Articulations
# =============================================================================


@dataclass
class CymbalArticulation:
    """Cymbal playing technique."""

    name: str
    cymbal_type: Literal["crash", "ride", "splash", "china", "effect"]
    hit_zone: Literal["bell", "bow", "edge"]
    velocity_mod: float
    duration_mod: float
    choke: bool = False
    midi_note_override: int | None = None


CYMBAL_ARTICULATIONS: dict[str, CymbalArticulation] = {
    "crash_normal": CymbalArticulation(
        name="Crash",
        cymbal_type="crash",
        hit_zone="bow",
        velocity_mod=1.0,
        duration_mod=2.0,
    ),
    "crash_accent": CymbalArticulation(
        name="Crash Accent",
        cymbal_type="crash",
        hit_zone="bow",
        velocity_mod=1.3,
        duration_mod=2.5,
    ),
    "crash_choke": CymbalArticulation(
        name="Crash Choke",
        cymbal_type="crash",
        hit_zone="bow",
        velocity_mod=1.2,
        duration_mod=0.3,
        choke=True,
    ),
    "ride_bow": CymbalArticulation(
        name="Ride Bow",
        cymbal_type="ride",
        hit_zone="bow",
        velocity_mod=0.9,
        duration_mod=1.0,
    ),
    "ride_bell": CymbalArticulation(
        name="Ride Bell",
        cymbal_type="ride",
        hit_zone="bell",
        velocity_mod=1.1,
        duration_mod=1.5,
        midi_note_override=53,
    ),
    "china": CymbalArticulation(
        name="China",
        cymbal_type="china",
        hit_zone="bow",
        velocity_mod=1.2,
        duration_mod=2.5,
    ),
    "splash": CymbalArticulation(
        name="Splash",
        cymbal_type="splash",
        hit_zone="bow",
        velocity_mod=1.0,
        duration_mod=0.3,
    ),
}


# =============================================================================
# Kick Drum Articulations
# =============================================================================


@dataclass
class KickArticulation:
    """Kick drum playing technique."""

    name: str
    beater_type: Literal["felt", "plastic", "wood", "fuzzy"]
    velocity_mod: float
    duration_mod: float
    pitch_mod: float = 0.0  # For electronic kicks


KICK_ARTICULATIONS: dict[str, KickArticulation] = {
    "normal": KickArticulation(
        name="Normal Kick",
        beater_type="felt",
        velocity_mod=1.0,
        duration_mod=0.3,
    ),
    "soft": KickArticulation(
        name="Soft Kick",
        beater_type="felt",
        velocity_mod=0.7,
        duration_mod=0.25,
    ),
    "hard": KickArticulation(
        name="Hard Kick",
        beater_type="plastic",
        velocity_mod=1.2,
        duration_mod=0.35,
    ),
    "dead": KickArticulation(
        name="Dead/Stroke Kick",
        beater_type="felt",
        velocity_mod=0.9,
        duration_mod=0.1,
    ),
}


# =============================================================================
# Tom Articulations
# =============================================================================


@dataclass
class TomArticulation:
    """Tom drum playing technique."""

    name: str
    tom_size: Literal["floor", "low", "mid", "high"]
    hit_zone: Literal["center", "rim"]
    velocity_mod: float
    duration_mod: float


TOM_ARTICULATIONS: dict[str, TomArticulation] = {
    "floor_center": TomArticulation(
        name="Floor Tom",
        tom_size="floor",
        hit_zone="center",
        velocity_mod=1.0,
        duration_mod=0.5,
    ),
    "floor_rim": TomArticulation(
        name="Floor Tom Rim",
        tom_size="floor",
        hit_zone="rim",
        velocity_mod=0.9,
        duration_mod=0.4,
    ),
    "low_center": TomArticulation(
        name="Low Tom",
        tom_size="low",
        hit_zone="center",
        velocity_mod=1.0,
        duration_mod=0.4,
    ),
    "mid_center": TomArticulation(
        name="Mid Tom",
        tom_size="mid",
        hit_zone="center",
        velocity_mod=1.0,
        duration_mod=0.3,
    ),
    "high_center": TomArticulation(
        name="High Tom",
        tom_size="high",
        hit_zone="center",
        velocity_mod=1.0,
        duration_mod=0.25,
    ),
}


# =============================================================================
# GM Drum Key Map
# =============================================================================

GM_DRUM_KEYS: dict[str, int] = {
    # Kick
    "kick": 36,
    "acoustic_bass_drum": 35,
    "bass_drum_1": 36,
    # Snare
    "snare": 38,
    "acoustic_snare": 38,
    "electric_snare": 40,
    "side_stick": 37,
    "hand_clap": 39,
    # Hi-hat
    "hihat_closed": 42,
    "hihat_open": 46,
    "hihat_pedal": 44,
    # Toms
    "tom_floor_low": 41,
    "tom_floor_high": 43,
    "tom_low": 45,
    "tom_hi_mid": 47,
    "tom_hi": 48,
    # Cymbals
    "crash_1": 49,
    "crash_2": 57,
    "ride_1": 51,
    "ride_2": 59,
    "ride_bell": 53,
    "splash": 55,
    "china": 52,
    # Percussion
    "cowbell": 56,
    "tambourine": 54,
    "vibraslap": 58,
    # Latin
    "bongo_hi": 60,
    "bongo_lo": 61,
    "conga_hi_muted": 62,
    "conga_hi_open": 63,
    "conga_lo": 64,
    "timbale_hi": 65,
    "timbale_lo": 66,
    "agogo_hi": 67,
    "agogo_lo": 68,
}


# =============================================================================
# Articulation Getters
# =============================================================================


def get_hihat_articulation(name: str) -> HiHatArticulation | None:
    """Get hi-hat articulation by name."""
    return HIHAT_ARTICULATIONS.get(name)


def get_snare_articulation(name: str) -> SnareArticulation | None:
    """Get snare articulation by name."""
    return SNARE_ARTICULATIONS.get(name)


def get_cymbal_articulation(name: str) -> CymbalArticulation | None:
    """Get cymbal articulation by name."""
    return CYMBAL_ARTICULATIONS.get(name)


def get_kick_articulation(name: str) -> KickArticulation | None:
    """Get kick articulation by name."""
    return KICK_ARTICULATIONS.get(name)


def get_tom_articulation(name: str) -> TomArticulation | None:
    """Get tom articulation by name."""
    return TOM_ARTICULATIONS.get(name)


def get_drum_key(piece: str) -> int:
    """Get GM MIDI key for a drum piece."""
    return GM_DRUM_KEYS.get(piece, 36)  # Default to kick


def apply_velocity(
    velocity: int,
    articulation: SnareArticulation
    | KickArticulation
    | HiHatArticulation
    | CymbalArticulation
    | TomArticulation,
) -> int:
    """Apply velocity modifier from articulation."""
    modified = int(velocity * articulation.velocity_mod)
    return max(0, min(127, modified))


__all__ = [
    "StickType",
    "STICK_TYPES",
    "HiHatArticulation",
    "HIHAT_ARTICULATIONS",
    "SnareArticulation",
    "SNARE_ARTICULATIONS",
    "CymbalArticulation",
    "CYMBAL_ARTICULATIONS",
    "KickArticulation",
    "KICK_ARTICULATIONS",
    "TomArticulation",
    "TOM_ARTICULATIONS",
    "GM_DRUM_KEYS",
    "get_hihat_articulation",
    "get_snare_articulation",
    "get_cymbal_articulation",
    "get_kick_articulation",
    "get_tom_articulation",
    "get_drum_key",
    "apply_velocity",
]
