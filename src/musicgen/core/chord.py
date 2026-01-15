"""Core chord classes for music representation.

This module provides classes for representing musical chords with
various qualities and inversions.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from musicgen.core.note import QUARTER, Note

# Chord quality types
MAJOR = "major"
MINOR = "minor"
DIMINISHED = "diminished"
AUGMENTED = "augmented"
MAJOR_SEVENTH = "major_7th"
MINOR_SEVENTH = "minor_7th"
DOMINANT_SEVENTH = "dominant_7th"
DIMINISHED_SEVENTH = "diminished_7th"
HALF_DIMINISHED = "half_diminished"

# Interval patterns for each quality (semitones from root)
CHORD_INTERVALS = {
    MAJOR: [0, 4, 7],
    MINOR: [0, 3, 7],
    DIMINISHED: [0, 3, 6],
    AUGMENTED: [0, 4, 8],
    MAJOR_SEVENTH: [0, 4, 7, 11],
    MINOR_SEVENTH: [0, 3, 7, 10],
    DOMINANT_SEVENTH: [0, 4, 7, 10],
    DIMINISHED_SEVENTH: [0, 3, 6, 9],
    HALF_DIMINISHED: [0, 3, 6, 10],
}

# Quality to interval count
CHORD_SIZE = {
    MAJOR: 3, MINOR: 3, DIMINISHED: 3, AUGMENTED: 3,
    MAJOR_SEVENTH: 4, MINOR_SEVENTH: 4, DOMINANT_SEVENTH: 4,
    DIMINISHED_SEVENTH: 4, HALF_DIMINISHED: 4,
}

# Valid chord qualities
VALID_QUALITIES = set(CHORD_INTERVALS.keys())


@dataclass
class Chord:
    """Represents a musical chord as a collection of Notes.

    Attributes:
        _root_name: The root note name (C, D, E, etc.)
        _quality: The chord quality
        _root_octave: Octave of the root note
        _inversion: Inversion number (0=root, 1=first, 2=second)
        duration: Duration in quarter notes
        _notes: List of Note objects in the chord
    """

    _root_name: str
    _quality: str = MAJOR
    _root_octave: int = 4
    _inversion: int = 0
    duration: float = QUARTER
    _notes: list[Note] = field(default_factory=list, repr=False)

    def __post_init__(self):
        """Validate and initialize chord."""
        # Clean up root name
        self._root_name = self._root_name.strip().upper()

        # Validate root
        if self._root_name not in ["C", "D", "E", "F", "G", "A", "B"]:
            # Try to parse as a full pitch
            try:
                note = Note.from_pitch_string(self._root_name)
                self._root_name = note.name
                self._root_octave = note.octave
            except ValueError:
                raise ValueError(f"Invalid root note: {self._root_name}")

        # Validate quality
        if self._quality not in VALID_QUALITIES:
            raise ValueError(f"Invalid quality: {self._quality}. Must be one of {VALID_QUALITIES}")

        # Validate inversion
        max_inversion = CHORD_SIZE[self._quality] - 1
        if not 0 <= self._inversion <= max_inversion:
            raise ValueError(f"Invalid inversion: {self._inversion}. Must be 0-{max_inversion}")

        # Generate notes if not provided
        if not self._notes:
            self._notes = self._generate_notes()

    def _generate_notes(self) -> list[Note]:
        """Generate the notes for this chord based on root, quality, and inversion."""
        intervals = CHORD_INTERVALS[self._quality]
        notes = []

        for i, interval in enumerate(intervals):
            # Calculate the note name based on root + interval
            root_midi = Note(self._root_name, self._root_octave).midi_number
            note_midi = root_midi + interval

            # Create the note
            note = Note.from_midi(note_midi, duration=self.duration)

            # For inversions, move notes down by octaves as needed
            if i < self._inversion:
                note.octave -= 1

            notes.append(note)

        # Sort notes by pitch for proper voicing
        notes.sort(key=lambda n: n.midi_number)

        # Handle inversion by moving the lowest notes up
        if self._inversion > 0:
            for i in range(self._inversion):
                notes[i].octave += 1

            # Re-sort after inversion
            notes.sort(key=lambda n: n.midi_number)

        return notes

    @property
    def root_name(self) -> str:
        """Return the root note name (without octave)."""
        return self._root_name

    @property
    def notes(self) -> list[Note]:
        """Return list of Note objects in the chord (sorted by pitch)."""
        return self._notes.copy()

    @property
    def inversion(self) -> int:
        """Return the current inversion number."""
        return self._inversion

    @inversion.setter
    def inversion(self, value: int) -> None:
        """Set the inversion and reorder notes accordingly."""
        max_inversion = CHORD_SIZE[self._quality] - 1
        if not 0 <= value <= max_inversion:
            raise ValueError(f"Invalid inversion: {value}. Must be 0-{max_inversion}")

        self._inversion = value
        self._notes = self._generate_notes()

    @property
    def quality(self) -> str:
        """Return the chord quality."""
        return self._quality

    @property
    def root_octave(self) -> int:
        """Return the root octave."""
        return self._root_octave

    def invert(self, inversion: int) -> Chord:
        """Return a new Chord with the specified inversion.

        Args:
            inversion: Inversion number (0=root position, 1=first, etc.)

        Returns:
            A new Chord instance
        """
        return Chord(
            _root_name=self._root_name,
            _quality=self._quality,
            _root_octave=self._root_octave,
            _inversion=inversion,
            duration=self.duration
        )

    def transpose(self, semitones: int) -> Chord:
        """Return a new Chord transposed by the given semitones.

        Args:
            semitones: Number of semitones to transpose

        Returns:
            A new Chord instance
        """
        # Transpose the root note
        root_note = Note(self._root_name, self._root_octave)
        transposed_root = root_note.transpose(semitones)

        return Chord(
            _root_name=transposed_root.name,
            _quality=self._quality,
            _root_octave=transposed_root.octave,
            _inversion=self._inversion,
            duration=self.duration
        )

    def get_inversion(self, bass_note: str) -> int:
        """Return the inversion that puts the specified note on bottom.

        Args:
            bass_note: Note name to use as bass

        Returns:
            Inversion number (0-2 for triads)
        """
        bass_note = bass_note.strip().upper()

        # Find which note in the chord matches
        for i, note in enumerate(self._generate_notes()):
            if note.name == bass_note:
                return i

        return 0

    def contains(self, note: Note) -> bool:
        """Check if the chord contains the given note (any octave).

        Args:
            note: Note to check

        Returns:
            True if note is in chord
        """
        for chord_note in self._notes:
            if chord_note.name == note.name and chord_note.accidental == note.accidental:
                return True
        return False

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Chord({self._root_name}, {self._quality}, {self._inversion})"

    def __eq__(self, other) -> bool:
        """Check equality based on root and quality."""
        if not isinstance(other, Chord):
            return False
        return (self._root_name == other._root_name and
                self._quality == other._quality and
                self._inversion == other._inversion)

    def __hash__(self) -> int:
        """Make Chord hashable."""
        return hash((self._root_name, self._quality, self._inversion))

    @classmethod
    def from_notes(cls, notes: list[Note], quality: str | None = None) -> Chord:
        """Create a Chord from a list of Notes.

        Determines root and quality from the notes if not specified.

        Args:
            notes: List of Note objects
            quality: Optional quality hint

        Returns:
            A new Chord instance
        """
        if len(notes) < 3:
            raise ValueError("Need at least 3 notes to form a chord")

        # Sort notes by pitch
        sorted_notes = sorted(notes, key=lambda n: n.midi_number)
        root = sorted_notes[0]

        # Calculate intervals from root
        intervals = [(n.midi_number - root.midi_number) % 12 for n in sorted_notes]

        # Try to determine quality
        if quality is None:
            interval_set = set(intervals)

            if interval_set == {0, 4, 7}:
                quality = MAJOR
            elif interval_set == {0, 3, 7}:
                quality = MINOR
            elif interval_set == {0, 3, 6}:
                quality = DIMINISHED
            elif interval_set == {0, 4, 8}:
                quality = AUGMENTED
            elif interval_set == {0, 4, 7, 11}:
                quality = MAJOR_SEVENTH
            elif interval_set == {0, 3, 7, 10}:
                quality = MINOR_SEVENTH
            else:
                quality = MAJOR  # Default

        return cls(
            _root_name=root.name,
            _quality=quality,
            _root_octave=root.octave,
            duration=notes[0].duration
        )
