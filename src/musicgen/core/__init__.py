"""Core music data structures.

This module provides the fundamental classes for representing musical
elements: Note, Rest, and Chord, along with duration and dynamic constants.
"""

from musicgen.core.chord import (
    AUGMENTED,
    DIMINISHED,
    DIMINISHED_SEVENTH,
    DOMINANT_SEVENTH,
    HALF_DIMINISHED,
    MAJOR,
    MAJOR_SEVENTH,
    MINOR,
    MINOR_SEVENTH,
    Chord,
)
from musicgen.core.note import (
    DOTTED_EIGHTH,
    DOTTED_HALF,
    DOTTED_QUARTER,
    EIGHTH,
    FF,
    HALF,
    MF,
    MP,
    PP,
    QUARTER,
    SIXTEENTH,
    TRIPLET_EIGHTH,
    TRIPLET_HALF,
    TRIPLET_QUARTER,
    WHOLE,
    F,
    Note,
    P,
    Rest,
)

__all__ = [
    # Classes
    "Note",
    "Rest",
    "Chord",
    # Durations
    "WHOLE",
    "HALF",
    "QUARTER",
    "EIGHTH",
    "SIXTEENTH",
    "DOTTED_HALF",
    "DOTTED_QUARTER",
    "DOTTED_EIGHTH",
    "TRIPLET_HALF",
    "TRIPLET_QUARTER",
    "TRIPLET_EIGHTH",
    # Dynamics
    "PP",
    "P",
    "MP",
    "MF",
    "F",
    "FF",
    # Chord qualities
    "MAJOR",
    "MINOR",
    "DIMINISHED",
    "AUGMENTED",
    "MAJOR_SEVENTH",
    "MINOR_SEVENTH",
    "DOMINANT_SEVENTH",
    "DIMINISHED_SEVENTH",
    "HALF_DIMINISHED",
]
