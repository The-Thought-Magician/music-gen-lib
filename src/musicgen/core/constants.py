"""Constants for music notation and timing.

This module imports duration constants from core.note to maintain a single
source of truth for note durations.
"""

from dataclasses import dataclass

# Import duration constants from note module (source of truth)
from musicgen.core.note import (
    EIGHTH,
    HALF,
    QUARTER,
    SIXTEENTH,
    THIRTY_SECOND,
    WHOLE,
    DOTTED_EIGHTH,
    DOTTED_HALF,
    DOTTED_QUARTER,
    DOTTED_WHOLE,
)

# Additional duration values (if note.py doesn't have these)

# Triplet durations
TRIPLET_WHOLE = WHOLE * 2/3
TRIPLET_HALF = HALF * 2/3
TRIPLET_QUARTER = QUARTER * 2/3
TRIPLET_EIGHTH = EIGHTH * 2/3

# Dynamic markings (velocity values 0-127)
PP = 20   # pianissimo
P = 40    # piano
MP = 60   # mezzo-piano
MF = 80   # mezzo-forte
F = 100   # forte
FF = 120  # fortissimo

# MIDI note numbers for middle C and octave
MIDDLE_C_MIDI = 60
STANDARD_OCTAVE = 4

# Frequency of A4 (standard tuning)
A4_FREQUENCY = 440.0

# Tempo markings
TEMPO_MARKINGS = {
    "grave": 40,
    "largo": 50,
    "lento": 60,
    "adagio": 70,
    "andante": 80,
    "moderato": 100,
    "allegretto": 110,
    "allegro": 120,
    "vivace": 140,
    "presto": 160,
    "prestissimo": 200,
}


@dataclass(frozen=True)
class Interval:
    """Represents a musical interval."""
    name: str
    semitones: int
    diatonic_steps: int


# Standard intervals
INTERVALS = {
    "unison": Interval("unison", 0, 0),
    "minor_second": Interval("m2", 1, 1),
    "major_second": Interval("M2", 2, 1),
    "minor_third": Interval("m3", 3, 2),
    "major_third": Interval("M3", 4, 2),
    "perfect_fourth": Interval("P4", 5, 3),
    "augmented_fourth": Interval("A4", 6, 3),
    "diminished_fifth": Interval("d5", 6, 4),
    "perfect_fifth": Interval("P5", 7, 4),
    "minor_sixth": Interval("m6", 8, 5),
    "major_sixth": Interval("M6", 9, 5),
    "minor_seventh": Interval("m7", 10, 6),
    "major_seventh": Interval("M7", 11, 6),
    "octave": Interval("P8", 12, 7),
}


def duration_to_ticks(duration: float, ticks_per_quarter: int = 480) -> int:
    """Convert duration value to MIDI ticks.

    Args:
        duration: Duration in quarter note units
        ticks_per_quarter: Number of ticks per quarter note (default 480)

    Returns:
        Number of MIDI ticks
    """
    return int(duration * ticks_per_quarter)


def ticks_to_duration(ticks: int, ticks_per_quarter: int = 480) -> float:
    """Convert MIDI ticks to duration value.

    Args:
        ticks: Number of MIDI ticks
        ticks_per_quarter: Number of ticks per quarter note (default 480)

    Returns:
        Duration in quarter note units
    """
    return ticks / ticks_per_quarter


def velocity_to_dynamic(velocity: int) -> str:
    """Convert velocity value to dynamic marking.

    Args:
        velocity: MIDI velocity (0-127)

    Returns:
        Dynamic marking name
    """
    if velocity <= 30:
        return "pp"
    elif velocity <= 50:
        return "p"
    elif velocity <= 70:
        return "mp"
    elif velocity <= 90:
        return "mf"
    elif velocity <= 110:
        return "f"
    else:
        return "ff"


def dynamic_to_velocity(dynamic: str) -> int:
    """Convert dynamic marking to velocity value.

    Args:
        dynamic: Dynamic marking name

    Returns:
        MIDI velocity (0-127)
    """
    dynamic_map = {
        "pp": PP,
        "p": P,
        "mp": MP,
        "mf": MF,
        "f": F,
        "ff": FF,
    }
    return dynamic_map.get(dynamic.lower(), MF)
