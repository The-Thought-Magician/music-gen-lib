"""
Extended instrument definitions for music-gen-lib V4.

This module provides instrument definitions for guitars, basses, drums,
world instruments, and electronic instruments beyond the orchestral
instruments from V3.
"""

from musicgen.instruments.guitars import (
    GuitarChord,
    GuitarPattern,
    GuitarTechnique,
    guitar_chord_library,
    standard_tuning,
)
from musicgen.instruments.midi_map import (
    DRUM_TO_NUMBER,
    GM_DRUM_NAMES,
    GM_PROGRAM_NAMES,
    PROGRAM_TO_NUMBER,
    GMKey,
    GMProgram,
)
from musicgen.instruments.world import WorldInstrumentDefinition

__all__ = [
    # Guitar
    "GuitarChord",
    "GuitarPattern",
    "GuitarTechnique",
    "guitar_chord_library",
    "standard_tuning",
    # MIDI
    "GMProgram",
    "GMKey",
    "GM_PROGRAM_NAMES",
    "GM_DRUM_NAMES",
    "PROGRAM_TO_NUMBER",
    "DRUM_TO_NUMBER",
    # World
    "WorldInstrumentDefinition",
]
