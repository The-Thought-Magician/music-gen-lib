"""Scale classes for music theory.

This module provides classes for representing musical scales with
various modes and types.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from musicgen.core.note import Note


class ScaleType(Enum):
    """Enumeration of available scale types."""

    MAJOR = "major"
    NATURAL_MINOR = "natural_minor"
    HARMONIC_MINOR = "harmonic_minor"
    MELODIC_MINOR = "melodic_minor"
    DORIAN = "dorian"
    PHRYGIAN = "phrygian"
    LYDIAN = "lydian"
    MIXOLYDIAN = "mixolydian"
    LOCRIAN = "locrian"
    MAJOR_PENTATONIC = "major_pentatonic"
    MINOR_PENTATONIC = "minor_pentatonic"
    BLUES = "blues"
    CHROMATIC = "chromatic"


# Scale interval patterns (semitones from tonic)
SCALE_INTERVALS = {
    ScaleType.MAJOR: [0, 2, 4, 5, 7, 9, 11],
    ScaleType.NATURAL_MINOR: [0, 2, 3, 5, 7, 8, 10],
    ScaleType.HARMONIC_MINOR: [0, 2, 3, 5, 7, 8, 11],
    ScaleType.MELODIC_MINOR: [0, 2, 3, 5, 7, 9, 11],
    ScaleType.DORIAN: [0, 2, 3, 5, 7, 9, 10],
    ScaleType.PHRYGIAN: [0, 1, 3, 5, 7, 8, 10],
    ScaleType.LYDIAN: [0, 2, 4, 6, 7, 9, 11],
    ScaleType.MIXOLYDIAN: [0, 2, 4, 5, 7, 9, 10],
    ScaleType.LOCRIAN: [0, 1, 3, 5, 6, 8, 10],
    ScaleType.MAJOR_PENTATONIC: [0, 2, 4, 7, 9],
    ScaleType.MINOR_PENTATONIC: [0, 3, 5, 7, 10],
    ScaleType.BLUES: [0, 3, 5, 6, 7, 10],
    ScaleType.CHROMATIC: list(range(12)),
}

# Scale names for string input
SCALE_NAMES = {
    "major": ScaleType.MAJOR,
    "minor": ScaleType.NATURAL_MINOR,
    "natural_minor": ScaleType.NATURAL_MINOR,
    "harmonic_minor": ScaleType.HARMONIC_MINOR,
    "melodic_minor": ScaleType.MELODIC_MINOR,
    "dorian": ScaleType.DORIAN,
    "phrygian": ScaleType.PHRYGIAN,
    "lydian": ScaleType.LYDIAN,
    "mixolydian": ScaleType.MIXOLYDIAN,
    "locrian": ScaleType.LOCRIAN,
    "major_pentatonic": ScaleType.MAJOR_PENTATONIC,
    "minor_pentatonic": ScaleType.MINOR_PENTATONIC,
    "blues": ScaleType.BLUES,
    "chromatic": ScaleType.CHROMATIC,
}


@dataclass
class Scale:
    """Represents a musical scale.

    Attributes:
        tonic: The tonic note name (e.g., "C", "A#")
        scale_type: The type of scale
        octave: The starting octave for the scale
    """

    tonic: str
    scale_type: str = "major"
    octave: int = 4

    def __post_init__(self):
        """Initialize scale after dataclass creation."""
        self.tonic = self.tonic.strip().upper()

        # Parse scale type
        if isinstance(self.scale_type, ScaleType):
            self._type_enum = self.scale_type
        else:
            type_str = self.scale_type.lower().replace("-", "_")
            if type_str not in SCALE_NAMES:
                raise ValueError(f"Invalid scale type: {self.scale_type}")
            self._type_enum = SCALE_NAMES[type_str]

    @property
    def intervals(self) -> list[int]:
        """Return the interval pattern for this scale."""
        return SCALE_INTERVALS[self._type_enum]

    @property
    def notes(self) -> list[str]:
        """Return the note names in this scale."""
        tonic_note = Note(self.tonic, self.octave)
        tonic_midi = tonic_note.midi_number
        note_names = []

        for interval in self.intervals:
            midi_num = tonic_midi + interval
            note = Note.from_midi(midi_num)
            note_names.append(note.name + note.accidental)

        return note_names

    def get_degree(self, degree: int) -> Note:
        """Get the note at a specific scale degree.

        Args:
            degree: Scale degree (1-based, wraps around)

        Returns:
            A Note object at that scale degree
        """
        if degree < 1:
            degree = 1

        # Calculate which octave
        octave_offset = (degree - 1) // len(self.intervals)
        interval_index = (degree - 1) % len(self.intervals)

        interval = self.intervals[interval_index]
        midi_num = Note(self.tonic, self.octave).midi_number + interval + (octave_offset * 12)

        return Note.from_midi(midi_num)

    def contains(self, note: str) -> bool:
        """Check if a note is in this scale.

        Args:
            note: Note name to check (e.g., "C", "D#")

        Returns:
            True if the note is in the scale
        """
        note = note.strip().upper()
        return note in self.notes

    def get_note_index(self, note: str) -> int | None:
        """Get the scale degree of a note.

        Args:
            note: Note name to find

        Returns:
            Scale degree (1-based) or None if not in scale
        """
        note = note.strip().upper()
        try:
            return self.notes.index(note) + 1
        except ValueError:
            return None

    def transpose(self, semitones: int) -> Scale:
        """Return a new Scale transposed by the given semitones.

        Args:
            semitones: Number of semitones to transpose

        Returns:
            A new Scale instance
        """
        tonic_note = Note(self.tonic, self.octave)
        transposed = tonic_note.transpose(semitones)

        return Scale(
            tonic=transposed.name + transposed.accidental,
            scale_type=self.scale_type,
            octave=transposed.octave
        )

    def diatonic_chords(self) -> list:
        """Generate diatonic chords for each scale degree.

        Returns:
            List of Chord objects
        """
        from musicgen.core.chord import DIMINISHED, MAJOR, MINOR, AUGMENTED, Chord

        # Determine chord qualities based on scale type
        if self._type_enum == ScaleType.MAJOR:
            qualities = [MAJOR, MINOR, MINOR, MAJOR, MAJOR, MINOR, DIMINISHED]
        elif self._type_enum == ScaleType.NATURAL_MINOR:
            qualities = [MINOR, DIMINISHED, MAJOR, MINOR, MINOR, MAJOR, MAJOR]
        elif self._type_enum == ScaleType.HARMONIC_MINOR:
            qualities = [MINOR, DIMINISHED, AUGMENTED, MINOR, MAJOR, MAJOR, DIMINISHED]
        else:
            # Default to major pattern
            qualities = [MAJOR, MINOR, MINOR, MAJOR, MAJOR, MINOR, DIMINISHED]

        chords = []
        # Get notes for first 7 scale degrees
        for i in range(min(7, len(self.intervals))):
            note = self.get_degree(i + 1)
            # Use just the note name (without accidental) as root
            # The accidental is handled in the note generation
            root_name = note.name
            chords.append(Chord(_root_name=root_name, _quality=qualities[i]))

        return chords

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Scale({self.tonic}, {self.scale_type})"

    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, Scale):
            return False
        return self.tonic == other.tonic and self._type_enum == other._type_enum
