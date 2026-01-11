"""Core music data structures.

This module provides the fundamental classes for representing musical
elements: Note, Rest, and Chord, along with duration and dynamic constants.
"""

from musicgen.core.note import (
    Note,
    Rest,
    WHOLE,
    HALF,
    QUARTER,
    EIGHTH,
    SIXTEENTH,
    DOTTED_HALF,
    DOTTED_QUARTER,
    DOTTED_EIGHTH,
    TRIPLET_HALF,
    TRIPLET_QUARTER,
    TRIPLET_EIGHTH,
    PP,
    P,
    MP,
    MF,
    F,
    FF,
)
from musicgen.core.chord import (
    Chord,
    MAJOR,
    MINOR,
    DIMINISHED,
    AUGMENTED,
    MAJOR_SEVENTH,
    MINOR_SEVENTH,
    DOMINANT_SEVENTH,
    DIMINISHED_SEVENTH,
    HALF_DIMINISHED,
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
