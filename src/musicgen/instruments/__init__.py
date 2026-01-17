"""
Extended instrument definitions for music-gen-lib V4.

This module provides instrument definitions for guitars, basses, drums,
world instruments, and electronic instruments beyond the orchestral
instruments from V3.
"""

from musicgen.instruments.drum_articulations import (
    CYMBAL_ARTICULATIONS,
    GM_DRUM_KEYS,
    HIHAT_ARTICULATIONS,
    KICK_ARTICULATIONS,
    SNARE_ARTICULATIONS,
    STICK_TYPES,
    TOM_ARTICULATIONS,
    apply_velocity,
    get_cymbal_articulation,
    get_drum_key,
    get_hihat_articulation,
    get_kick_articulation,
    get_snare_articulation,
    get_tom_articulation,
)
from musicgen.instruments.drums import (
    DRUM_PATTERNS,
    DrumFillGenerator,
    DrumPattern,
    apply_groove,
    get_pattern,
    get_patterns_by_genre,
)
from musicgen.instruments.fretboard import (
    DROP_D_GUITAR,
    OPEN_D_GUITAR,
    STANDARD_BASS_4,
    STANDARD_BASS_5,
    STANDARD_GUITAR,
    Fretboard,
    FretboardPosition,
    GuitarStringAssigner,
    midi_to_note,
    note_to_midi,
)
from musicgen.instruments.guitars import (
    BASS_TUNING_4_STRING,
    BASS_TUNING_5_STRING,
    BASS_TUNING_6_STRING,
    DADGAD_TUNING,
    DROP_D_TUNING,
    GUITAR_CHORDS_JAZZ,
    GUITAR_CHORDS_OPEN,
    GUITAR_CHORDS_POWER,
    GUITAR_PATTERNS,
    OPEN_D_TUNING,
    STANDARD_TUNING,
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
    # Guitar Tunings
    "STANDARD_TUNING",
    "DROP_D_TUNING",
    "OPEN_D_TUNING",
    "DADGAD_TUNING",
    "BASS_TUNING_4_STRING",
    "BASS_TUNING_5_STRING",
    "BASS_TUNING_6_STRING",
    # Guitar Chords
    "GUITAR_CHORDS_OPEN",
    "GUITAR_CHORDS_BARRE",
    "GUITAR_CHORDS_POWER",
    "GUITAR_CHORDS_JAZZ",
    "GUITAR_PATTERNS",
    # MIDI
    "GMProgram",
    "GMKey",
    "GM_PROGRAM_NAMES",
    "GM_DRUM_NAMES",
    "PROGRAM_TO_NUMBER",
    "DRUM_TO_NUMBER",
    # Fretboard
    "Fretboard",
    "FretboardPosition",
    "GuitarStringAssigner",
    "note_to_midi",
    "midi_to_note",
    "STANDARD_GUITAR",
    "DROP_D_GUITAR",
    "OPEN_D_GUITAR",
    "STANDARD_BASS_4",
    "STANDARD_BASS_5",
    # Drums
    "DrumPattern",
    "DRUM_PATTERNS",
    "DrumFillGenerator",
    "get_pattern",
    "get_patterns_by_genre",
    "apply_groove",
    # Drum Articulations
    "STICK_TYPES",
    "HIHAT_ARTICULATIONS",
    "SNARE_ARTICULATIONS",
    "CYMBAL_ARTICULATIONS",
    "KICK_ARTICULATIONS",
    "TOM_ARTICULATIONS",
    "GM_DRUM_KEYS",
    "get_hihat_articulation",
    "get_snare_articulation",
    "get_cymbal_articulation",
    "get_kick_articulation",
    "get_tom_articulation",
    "get_drum_key",
    "apply_velocity",
    # World
    "WorldInstrumentDefinition",
]
