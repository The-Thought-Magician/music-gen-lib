"""
Guitar and bass instrument definitions for music-gen-lib V4.

This module provides guitar-specific models including chords, patterns,
and techniques for realistic guitar MIDI generation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    pass


# =============================================================================
# Guitar Tunings
# =============================================================================

# Standard tuning (low to high): E2 A2 D3 G3 B3 E4
STANDARD_TUNING: list[str] = ["E2", "A2", "D3", "G3", "B3", "E4"]

# Drop D tuning
DROP_D_TUNING: list[str] = ["D2", "A2", "D3", "G3", "B3", "E4"]

# Open D tuning
OPEN_D_TUNING: list[str] = ["D2", "A2", "D3", "F#3", "A3", "D4"]

# Open G tuning
OPEN_G_TUNING: list[str] = ["D2", "G2", "D3", "G3", "B3", "D4"]

# DADGAD tuning
DADGAD_TUNING: list[str] = ["D2", "A2", "D3", "G3", "A3", "D4"]


# =============================================================================
# Guitar Techniques
# =============================================================================


@dataclass
class GuitarTechnique:
    """
    Guitar-specific playing technique.

    Attributes:
        name: Name of the technique
        pluck_type: How the string is plucked (finger, pick, thumb, slap)
        articulation: Type of articulation
        fret: Fret position (if applicable)
        string_num: String number (1-6, 1=highest)
        midi_cc: MIDI CC for continuous control
        keyswitch: MIDI keyswitch for articulation switching
    """

    name: str
    pluck_type: Literal["finger", "pick", "thumb", "slap"] = "pick"
    articulation: Literal[
        "normal", "hammer_on", "pull_off", "slide", "bend", "vibrato", "trill"
    ] = "normal"
    fret: int | None = None
    string_num: int | None = None  # 1-6, 1=highest
    midi_cc: int | None = None
    keyswitch: int | None = None
    parameters: dict[str, float] = field(default_factory=dict)


# =============================================================================
# Guitar Chords
# =============================================================================


@dataclass
class GuitarChord:
    """
    Guitar chord with fingering information.

    Attributes:
        name: Chord name (e.g., "C", "Am", "F#m7b5")
        voicing: Type of voicing (open, barre, jazz, power)
        fingering: List of (fret, string) tuples. 0=open, None=muted
            Example: [(0, None), (1, 2), (0, None), (2, 3), (3, 3), (None, None)]
            Strings: E(6) A(5) D(4) G(3) B(2) E(1)
        fret_range: (min_fret, max_fret) used
        difficulty: Easy/medium/hard to play
        notes: List of note names in the chord
    """

    name: str
    voicing: Literal["open", "barre", "jazz", "power", "slash"] = "open"
    fingering: list[tuple[int | None, int | None]] = field(default_factory=list)
    fret_range: tuple[int, int] = (0, 0)
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    notes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Calculate fret range from fingering."""
        frets = [f for f, _ in self.fingering if f is not None and f > 0]
        if frets:
            self.fret_range = (min(frets), max(frets))


# =============================================================================
# Guitar Chord Library
# =============================================================================

# Open chords (first position)
GUITAR_CHORDS_OPEN: dict[str, GuitarChord] = {
    "C": GuitarChord(
        name="C",
        voicing="open",
        fingering=[(0, None), (3, 5), (2, 4), (0, None), (1, 2), (0, None)],
        fret_range=(0, 3),
        difficulty="easy",
        notes=["C3", "C4", "E4", "G4", "C5"],
    ),
    "C7": GuitarChord(
        name="C7",
        voicing="open",
        fingering=[(0, None), (3, 5), (2, 4), (3, 3), (1, 2), (0, None)],
        fret_range=(0, 3),
        difficulty="easy",
        notes=["C3", "Bb3", "E4", "G4", "C5"],
    ),
    "Cmaj7": GuitarChord(
        name="Cmaj7",
        voicing="open",
        fingering=[(0, None), (3, 5), (2, 4), (0, None), (0, None), (0, None)],
        fret_range=(0, 3),
        difficulty="easy",
        notes=["C3", "B3", "E4", "G4"],
    ),
    "D": GuitarChord(
        name="D",
        voicing="open",
        fingering=[(None, None), (None, None), (0, None), (2, 3), (3, 2), (2, 1)],
        fret_range=(0, 3),
        difficulty="easy",
        notes=["D3", "D4", "F#4", "A4"],
    ),
    "Dm": GuitarChord(
        name="Dm",
        voicing="open",
        fingering=[(None, None), (None, None), (0, None), (2, 3), (3, 2), (1, 1)],
        fret_range=(0, 3),
        difficulty="easy",
        notes=["D3", "D4", "F4", "A4"],
    ),
    "D7": GuitarChord(
        name="D7",
        voicing="open",
        fingering=[(None, None), (None, None), (0, None), (2, 3), (1, 2), (2, 1)],
        fret_range=(0, 3),
        difficulty="easy",
        notes=["D3", "C#4", "F4", "A4"],
    ),
    "E": GuitarChord(
        name="E",
        voicing="open",
        fingering=[(0, None), (2, 5), (2, 4), (1, 3), (0, None), (0, None)],
        fret_range=(0, 2),
        difficulty="easy",
        notes=["E2", "E3", "B3", "E4", "G#4"],
    ),
    "Em": GuitarChord(
        name="Em",
        voicing="open",
        fingering=[(0, None), (2, 5), (2, 4), (0, None), (0, None), (0, None)],
        fret_range=(0, 2),
        difficulty="easy",
        notes=["E2", "E3", "B3", "E4", "G4"],
    ),
    "E7": GuitarChord(
        name="E7",
        voicing="open",
        fingering=[(0, None), (2, 5), (0, None), (1, 3), (0, None), (0, None)],
        fret_range=(0, 2),
        difficulty="easy",
        notes=["E2", "D3", "B3", "E4", "G#4"],
    ),
    "F": GuitarChord(
        name="F",
        voicing="barre",
        fingering=[(1, 6), (1, 5), (2, 4), (3, 3), (3, 2), (1, 1)],
        fret_range=(1, 3),
        difficulty="medium",
        notes=["F2", "F3", "A3", "C4", "F4"],
    ),
    "Fmaj7": GuitarChord(
        name="Fmaj7",
        voicing="open",
        fingering=[(None, None), (None, None), (3, 4), (2, 3), (0, None), (0, None)],
        fret_range=(0, 3),
        difficulty="easy",
        notes=["F3", "A3", "C4", "E4"],
    ),
    "G": GuitarChord(
        name="G",
        voicing="open",
        fingering=[(3, 6), (2, 5), (0, None), (0, None), (0, None), (3, 1)],
        fret_range=(0, 3),
        difficulty="easy",
        notes=["G2", "G3", "B3", "D4", "G4"],
    ),
    "G7": GuitarChord(
        name="G7",
        voicing="open",
        fingering=[(3, 6), (2, 5), (0, None), (0, None), (0, None), (1, 1)],
        fret_range=(0, 3),
        difficulty="easy",
        notes=["G2", "G3", "B3", "D4", "F4"],
    ),
    "A": GuitarChord(
        name="A",
        voicing="open",
        fingering=[(None, None), (0, None), (2, 4), (2, 3), (2, 2), (0, None)],
        fret_range=(0, 2),
        difficulty="easy",
        notes=["A2", "E3", "A3", "C#4", "E4"],
    ),
    "Am": GuitarChord(
        name="Am",
        voicing="open",
        fingering=[(None, None), (0, None), (2, 4), (2, 3), (1, 2), (0, None)],
        fret_range=(0, 2),
        difficulty="easy",
        notes=["A2", "E3", "A3", "C4", "E4"],
    ),
    "A7": GuitarChord(
        name="A7",
        voicing="open",
        fingering=[(None, None), (0, None), (2, 4), (0, None), (2, 2), (0, None)],
        fret_range=(0, 2),
        difficulty="easy",
        notes=["A2", "E3", "G3", "C#4"],
    ),
    "Am7": GuitarChord(
        name="Am7",
        voicing="open",
        fingering=[(None, None), (0, None), (2, 4), (0, None), (1, 2), (0, None)],
        fret_range=(0, 2),
        difficulty="easy",
        notes=["A2", "E3", "G3", "C4", "E4"],
    ),
    "B7": GuitarChord(
        name="B7",
        voicing="open",
        fingering=[(None, None), (2, 5), (1, 4), (2, 3), (0, None), (2, 1)],
        fret_range=(0, 2),
        difficulty="medium",
        notes=["B2", "A#3", "D#4", "F#4", "A#4"],
    ),
}

# Barre chords
GUITAR_CHORDS_BARRE: dict[str, GuitarChord] = {
    "Bm": GuitarChord(
        name="Bm",
        voicing="barre",
        fingering=[(None, None), (2, 5), (4, 4), (4, 3), (3, 2), (2, 1)],
        fret_range=(2, 4),
        difficulty="medium",
        notes=["B2", "B3", "D4", "F#4"],
    ),
    "Cm": GuitarChord(
        name="Cm",
        voicing="barre",
        fingering=[(None, None), (3, 5), (5, 4), (5, 3), (4, 2), (3, 1)],
        fret_range=(3, 5),
        difficulty="medium",
        notes=["C3", "C4", "Eb4", "G4"],
    ),
    "F#m": GuitarChord(
        name="F#m",
        voicing="barre",
        fingering=[(2, 6), (2, 5), (4, 4), (4, 3), (3, 2), (2, 1)],
        fret_range=(2, 4),
        difficulty="medium",
        notes=["F#2", "F#3", "A3", "C#4"],
    ),
    "Bb": GuitarChord(
        name="Bb",
        voicing="barre",
        fingering=[(None, None), (1, 5), (3, 4), (3, 3), (3, 2), (1, 1)],
        fret_range=(1, 3),
        difficulty="medium",
        notes=["Bb2", "Bb3", "D4", "F4"],
    ),
}

# Power chords (5th chords)
GUITAR_CHORDS_POWER: dict[str, GuitarChord] = {
    "A5": GuitarChord(
        name="A5",
        voicing="power",
        fingering=[(None, None), (0, None), (2, 4), (2, 3), (2, 2), (0, None)],
        fret_range=(0, 2),
        difficulty="easy",
        notes=["A2", "E3", "A3"],
    ),
    "B5": GuitarChord(
        name="B5",
        voicing="power",
        fingering=[(None, None), (2, 5), (4, 4), (4, 3), (4, 2), (2, 1)],
        fret_range=(2, 4),
        difficulty="medium",
        notes=["B2", "F#3", "B3"],
    ),
    "C5": GuitarChord(
        name="C5",
        voicing="power",
        fingering=[(None, None), (3, 5), (5, 4), (5, 3), (5, 2), (3, 1)],
        fret_range=(3, 5),
        difficulty="medium",
        notes=["C3", "G3", "C4"],
    ),
    "D5": GuitarChord(
        name="D5",
        voicing="power",
        fingering=[(None, None), (None, None), (0, None), (2, 3), (3, 2), (2, 1)],
        fret_range=(0, 3),
        difficulty="easy",
        notes=["D3", "A3", "D4"],
    ),
    "E5": GuitarChord(
        name="E5",
        voicing="power",
        fingering=[(0, None), (2, 5), (2, 4), (2, 3), (0, None), (0, None)],
        fret_range=(0, 2),
        difficulty="easy",
        notes=["E2", "B2", "E3"],
    ),
    "G5": GuitarChord(
        name="G5",
        voicing="power",
        fingering=[(None, None), (0, None), (0, None), (0, None), (0, None), (3, 1)],
        fret_range=(0, 3),
        difficulty="easy",
        notes=["G2", "D3", "G3"],
    ),
}

# Jazz chords (extended voicings)
GUITAR_CHORDS_JAZZ: dict[str, GuitarChord] = {
    "Cmaj9": GuitarChord(
        name="Cmaj9",
        voicing="jazz",
        fingering=[(None, None), (3, 5), (2, 4), (4, 3), (3, 2), (0, None)],
        fret_range=(2, 4),
        difficulty="hard",
        notes=["C3", "B3", "D4", "E4", "G4"],
    ),
    "C9": GuitarChord(
        name="C9",
        voicing="jazz",
        fingering=[(None, None), (3, 5), (3, 4), (2, 3), (3, 2), (None, None)],
        fret_range=(2, 3),
        difficulty="hard",
        notes=["C3", "Bb3", "D4", "G4"],
    ),
    "C13": GuitarChord(
        name="C13",
        voicing="jazz",
        fingering=[(None, None), (3, 5), (2, 4), (2, 3), (5, 2), (4, 1)],
        fret_range=(2, 5),
        difficulty="hard",
        notes=["C3", "Bb3", "E4", "G4", "A4"],
    ),
    "Dm9": GuitarChord(
        name="Dm9",
        voicing="jazz",
        fingering=[(None, None), (None, None), (0, None), (2, 3), (3, 2), (2, 1)],
        fret_range=(0, 3),
        difficulty="medium",
        notes=["D3", "C4", "E4", "F4"],
    ),
    "E9": GuitarChord(
        name="E9",
        voicing="jazz",
        fingering=[(0, None), (2, 5), (1, 4), (1, 3), (0, None), (2, 1)],
        fret_range=(0, 2),
        difficulty="medium",
        notes=["E2", "D3", "F#3", "G#3"],
    ),
}

# Combined library
guitar_chord_library: dict[str, GuitarChord] = {
    **GUITAR_CHORDS_OPEN,
    **GUITAR_CHORDS_BARRE,
    **GUITAR_CHORDS_POWER,
    **GUITAR_CHORDS_JAZZ,
}


# =============================================================================
# Guitar Patterns
# =============================================================================


@dataclass
class GuitarPattern:
    """
    Guitar strumming/picking pattern.

    Attributes:
        name: Pattern name
        pattern: List of "down", "up", or "mute" strokes
        rhythm: Mini-notation string for rhythm
        style: Playing style
    """

    name: str
    pattern: list[Literal["down", "up", "mute"]]
    rhythm: str
    style: Literal["strum", "pick", "fingerstyle", "slap", "hybrid"] = "strum"


# Common strumming patterns
GUITAR_PATTERNS: dict[str, GuitarPattern] = {
    "basic_down": GuitarPattern(
        name="basic_down",
        pattern=["down"],
        rhythm="4",
        style="strum",
    ),
    "basic_down_up": GuitarPattern(
        name="basic_down_up",
        pattern=["down", "up"],
        rhythm="4 4",
        style="strum",
    ),
    "folk_strum": GuitarPattern(
        name="folk_strum",
        pattern=["down", "down", "up", "up"],
        rhythm="4~ 4 8 8",
        style="strum",
    ),
    "rock_strum": GuitarPattern(
        name="rock_strum",
        pattern=["down", "down", "up", "down", "up"],
        rhythm="8 8 8 8 8",
        style="strum",
    ),
    "country_pattern": GuitarPattern(
        name="country_pattern",
        pattern=["down", "mute", "up", "down", "mute", "up"],
        rhythm="8 8 8 8 8 8",
        style="hybrid",
    ),
    "fingerstyle_arpeggio": GuitarPattern(
        name="fingerstyle_arpeggio",
        pattern=["down", "up", "up", "up"],
        rhythm="8 8 8 8",
        style="fingerstyle",
    ),
}


# =============================================================================
# Bass Guitar Definitions
# =============================================================================

BASS_TUNING_4_STRING: list[str] = ["E1", "A1", "D2", "G2"]
BASS_TUNING_5_STRING: list[str] = ["B0", "E1", "A1", "D2", "G2"]
BASS_TUNING_6_STRING: list[str] = ["B0", "E1", "A1", "D2", "G2", "C3"]


@dataclass
class BassTechnique:
    """
    Bass guitar playing technique.

    Attributes:
        name: Name of the technique
        pluck_type: finger, pick, slap, pop
        articulation: Normal, hammer-on, pull-off, slide, ghost note
    """

    name: str
    pluck_type: Literal["finger", "pick", "slap", "pop"] = "finger"
    articulation: Literal[
        "normal", "hammer_on", "pull_off", "slide", "ghost", "bend", "vibrato"
    ] = "normal"
    fret: int | None = None
    string_num: int | None = None


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Tunings
    "STANDARD_TUNING",
    "DROP_D_TUNING",
    "OPEN_D_TUNING",
    "OPEN_G_TUNING",
    "DADGAD_TUNING",
    # Classes
    "GuitarTechnique",
    "GuitarChord",
    "GuitarPattern",
    "BassTechnique",
    # Chords
    "guitar_chord_library",
    "GUITAR_CHORDS_OPEN",
    "GUITAR_CHORDS_BARRE",
    "GUITAR_CHORDS_POWER",
    "GUITAR_CHORDS_JAZZ",
    # Patterns
    "GUITAR_PATTERNS",
    # Bass
    "BASS_TUNING_4_STRING",
    "BASS_TUNING_5_STRING",
    "BASS_TUNING_6_STRING",
]

# Convenience exports
standard_tuning = STANDARD_TUNING
