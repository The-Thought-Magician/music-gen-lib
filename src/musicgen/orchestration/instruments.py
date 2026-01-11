"""Instrument definitions and classes.

This module provides classes for representing musical instruments
with their ranges and characteristics.
"""

from __future__ import annotations
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum

from musicgen.core.note import Note


class InstrumentFamily(Enum):
    """Categories of musical instruments."""

    STRINGS = "strings"
    WOODWINDS = "woodwinds"
    BRASS = "brass"
    PERCUSSION = "percussion"
    KEYBOARDS = "keyboards"
    ELECTRONIC = "electronic"


@dataclass
class Instrument:
    """Represents a musical instrument.

    Attributes:
        name: The instrument name
        family: The instrument family
        range: String representing pitch range (e.g., "G3-A7")
        transposition: Semitones to transpose from written to sounding
        midi_program: MIDI program number (0-127)
        clef: Preferred clef
    """

    name: str
    family: InstrumentFamily = InstrumentFamily.STRINGS
    range: str = "C4-C6"
    transposition: int = 0
    midi_program: int = 0
    clef: str = "treble"

    # Common instrument presets
    _PRESETS: Dict[str, Dict] = field(default_factory=dict, repr=False)

    def __post_init__(self):
        """Initialize instrument and set up presets."""
        # Define common instruments
        if not self._PRESETS:
            self._PRESETS = {
                # Strings
                "violin": {
                    "family": InstrumentFamily.STRINGS,
                    "range": "G3-A7",
                    "transposition": 0,
                    "midi_program": 40,
                    "clef": "treble"
                },
                "viola": {
                    "family": InstrumentFamily.STRINGS,
                    "range": "C3-E6",
                    "transposition": 0,
                    "midi_program": 41,
                    "clef": "alto"
                },
                "cello": {
                    "family": InstrumentFamily.STRINGS,
                    "range": "C2-C6",
                    "transposition": 0,
                    "midi_program": 42,
                    "clef": "bass"
                },
                "double_bass": {
                    "family": InstrumentFamily.STRINGS,
                    "range": "E1-C5",
                    "transposition": -12,  # Sounds octave lower
                    "midi_program": 43,
                    "clef": "bass"
                },
                # Woodwinds
                "flute": {
                    "family": InstrumentFamily.WOODWINDS,
                    "range": "C4-D7",
                    "transposition": 0,
                    "midi_program": 73,
                    "clef": "treble"
                },
                "piccolo": {
                    "family": InstrumentFamily.WOODWINDS,
                    "range": "C5-C8",
                    "transposition": 12,  # Sounds octave higher
                    "midi_program": 72,
                    "clef": "treble"
                },
                "oboe": {
                    "family": InstrumentFamily.WOODWINDS,
                    "range": "Bb3-A6",
                    "transposition": 0,
                    "midi_program": 68,
                    "clef": "treble"
                },
                "clarinet": {
                    "family": InstrumentFamily.WOODWINDS,
                    "range": "E3-Bb7",
                    "transposition": -2,  # Bb clarinet
                    "midi_program": 71,
                    "clef": "treble"
                },
                "bassoon": {
                    "family": InstrumentFamily.WOODWINDS,
                    "range": "Bb1-Eb5",
                    "transposition": 0,
                    "midi_program": 70,
                    "clef": "bass"
                },
                # Brass
                "trumpet": {
                    "family": InstrumentFamily.BRASS,
                    "range": "F#3-D6",
                    "transposition": -2,  # Bb trumpet
                    "midi_program": 56,
                    "clef": "treble"
                },
                "french_horn": {
                    "family": InstrumentFamily.BRASS,
                    "range": "B1-F5",
                    "transposition": -7,  # F horn
                    "midi_program": 60,
                    "clef": "treble"
                },
                "trombone": {
                    "family": InstrumentFamily.BRASS,
                    "range": "E2-F5",
                    "transposition": 0,
                    "midi_program": 57,
                    "clef": "bass"
                },
                "tuba": {
                    "family": InstrumentFamily.BRASS,
                    "range": "D1-F4",
                    "transposition": 0,
                    "midi_program": 58,
                    "clef": "bass"
                },
                # Keyboards
                "piano": {
                    "family": InstrumentFamily.KEYBOARDS,
                    "range": "A0-C8",
                    "transposition": 0,
                    "midi_program": 0,
                    "clef": "grand_staff"
                },
                "harpsichord": {
                    "family": InstrumentFamily.KEYBOARDS,
                    "range": "F1-C8",
                    "transposition": 0,
                    "midi_program": 6,
                    "clef": "grand_staff"
                },
            }

    def in_range(self, note: Note) -> bool:
        """Check if a note is within this instrument's range.

        Args:
            note: The note to check

        Returns:
            True if the note is in range
        """
        try:
            # Parse range
            low_str, high_str = self.range.split("-")
            low_note = Note.from_pitch_string(low_str + "0")
            high_note = Note.from_pitch_string(high_str + "9")

            return low_note.midi_number <= note.midi_number <= high_note.midi_number
        except (ValueError, IndexError):
            return True  # Assume in range if parsing fails

    def written_to_concert(self, written_note: Note) -> Note:
        """Convert a written note to its sounding pitch.

        Args:
            written_note: The written note

        Returns:
            The sounding note
        """
        return written_note.transpose(self.transposition)

    def concert_to_written(self, concert_note: Note) -> Note:
        """Convert a sounding note to its written pitch.

        Args:
            concert_note: The sounding note

        Returns:
            The written note
        """
        return concert_note.transpose(-self.transposition)

    @classmethod
    def preset(cls, name: str) -> "Instrument":
        """Create an instrument from a preset name.

        Args:
            name: Preset name

        Returns:
            A new Instrument with preset configuration
        """
        # Create a dummy instance to access presets
        dummy = cls(name=name)
        presets = dummy._PRESETS

        if name.lower() not in presets:
            return cls(name=name)

        config = presets[name.lower()]
        return cls(
            name=name,
            family=config["family"],
            range=config["range"],
            transposition=config["transposition"],
            midi_program=config["midi_program"],
            clef=config["clef"]
        )

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Instrument({self.name}, {self.family.value})"

    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, Instrument):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        """Make Instrument hashable."""
        return hash(self.name)


@dataclass
class Voice:
    """An individual voice or part within a composition.

    Attributes:
        name: Voice name (e.g., "violin I", "soprano")
        instrument: The instrument for this voice
        notes: List of notes in this voice
    """

    name: str
    instrument: Instrument
    notes: List[Note] = field(default_factory=list)

    @property
    def length(self) -> int:
        """Return number of notes."""
        return len(self.notes)

    @property
    def range(self) -> int:
        """Return pitch range in semitones."""
        if not self.notes:
            return 0
        midi_nums = [n.midi_number for n in self.notes]
        return max(midi_nums) - min(midi_nums)

    def add_note(self, note: Note) -> None:
        """Add a note to this voice.

        Args:
            note: Note to add
        """
        self.notes.append(note)

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Voice({self.name}, {len(self.notes)} notes)"
