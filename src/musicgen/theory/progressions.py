"""Chord progression classes for music theory.

This module provides classes for representing and generating
chord progressions.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from musicgen.core.chord import DIMINISHED, MAJOR, MINOR, Chord
from musicgen.theory.keys import Key

# Roman numeral to scale degree mapping (1-based)
ROMAN_TO_DEGREE = {
    "i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5,
    "vi": 6, "vii": 7,
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
    "VI": 6, "VII": 7,
}


@dataclass
class Progression:
    """Represents a chord progression.

    Attributes:
        chords: List of Chord objects in the progression
        key: The key of the progression
    """

    chords: list[Chord] = field(default_factory=list)
    key: Key | None = None

    def __post_init__(self):
        """Initialize progression."""
        if self.key is None and self.chords:
            # Default to major/minor based on first chord
            tonic = self.chords[0].root_name
            self.key = Key(tonic, "major")

    @property
    def length(self) -> int:
        """Return the number of chords in the progression."""
        return len(self.chords)

    def add_chord(self, chord: Chord) -> None:
        """Add a chord to the progression.

        Args:
            chord: Chord to add
        """
        self.chords.append(chord)

    def get_chord(self, index: int) -> Chord | None:
        """Get a chord by index.

        Args:
            index: Index (0-based)

        Returns:
            Chord at index or None
        """
        if 0 <= index < len(self.chords):
            return self.chords[index]
        return None

    def transpose(self, semitones: int) -> Progression:
        """Return a new progression transposed by semitones.

        Args:
            semitones: Number of semitones to transpose

        Returns:
            A new Progression
        """
        new_chords = [c.transpose(semitones) for c in self.chords]
        new_key = None

        if self.key:
            # Transpose the key tonic
            from musicgen.core.note import Note
            tonic_note = Note(self.key.tonic, 4)
            transposed = tonic_note.transpose(semitones)
            new_key = Key(transposed.name + transposed.accidental, self.key.key_type)

        return Progression(chords=new_chords, key=new_key)

    @classmethod
    def from_roman(cls, roman_numerals: str, key: str | Key,
                   quality: str | None = None) -> Progression:
        """Create a progression from Roman numerals.

        Args:
            roman_numerals: String like "I-IV-V-I" or "I-IV-V7-I"
            key: The key (tonic name or Key object)
            quality: Optional quality hint for key

        Returns:
            A new Progression
        """
        # Parse key
        if isinstance(key, str):
            key_obj = Key(key, quality if quality else "major")
        else:
            key_obj = key

        # Get diatonic chords
        diatonic = key_obj.diatonic_chords()

        # Parse Roman numerals
        symbols = roman_numerals.replace(" ", "").split("-")
        chords = []

        for symbol in symbols:
            # Extract the base numeral
            base = ""
            for char in symbol:
                if char in "IVXivx":
                    base += char
                else:
                    break

            # Check for seventh
            is_seventh = "7" in symbol

            # Get the degree
            degree = ROMAN_TO_DEGREE.get(base, 1)

            # Get the chord from diatonic
            if 1 <= degree <= len(diatonic):
                chord = diatonic[degree - 1]

                # Handle seventh chords
                if is_seventh:
                    from musicgen.core.chord import (
                        DIMINISHED_SEVENTH,
                        DOMINANT_SEVENTH,
                        MAJOR_SEVENTH,
                        MINOR_SEVENTH,
                    )
                    if chord.quality == MAJOR:
                        if degree == 5:  # V chord = dominant
                            new_quality = DOMINANT_SEVENTH
                        else:
                            new_quality = MAJOR_SEVENTH
                    elif chord.quality == MINOR:
                        new_quality = MINOR_SEVENTH
                    elif chord.quality == DIMINISHED:
                        new_quality = DIMINISHED_SEVENTH
                    else:
                        new_quality = chord.quality

                    chord = Chord(
                        _root_name=chord.root_name,
                        _quality=new_quality,
                        _root_octave=chord.root_octave,
                        _inversion=chord.inversion,
                        duration=chord.duration
                    )

                chords.append(chord)

        return cls(chords=chords, key=key_obj)

    @classmethod
    def circle_of_fifths(cls, root: str, length: int = 4,
                         quality: str | None = None) -> Progression:
        """Generate a circle-of-fifths progression.

        Args:
            root: Root chord name
            length: Number of chords
            quality: Quality of chords

        Returns:
            A new Progression
        """
        if quality is None:
            quality = MAJOR

        chords = []
        current = root

        for _ in range(length):
            chords.append(Chord(_root_name=current, _quality=quality))

            # Move up a perfect fifth (7 semitones)
            from musicgen.core.note import Note
            note = Note.from_pitch_string(current + "4")
            next_note = note.transpose(7)
            current = next_note.name + next_note.accidental

        return cls(chords=chords, key=Key(root, "major" if quality == MAJOR else "minor"))

    @classmethod
    def functional(cls, key: str | Key, length: int = 8,
                   cadence: str = "authentic", allow_secondary: bool = False) -> Progression:
        """Generate a functionally coherent progression.

        Args:
            key: The key
            length: Number of chords
            cadence: Type of cadence ("authentic", "half", "deceptive", "plagal")
            allow_secondary: Whether to allow secondary dominants

        Returns:
            A new Progression
        """
        if isinstance(key, str):
            key_obj = Key(key, "major")
        else:
            key_obj = key

        diatonic = key_obj.diatonic_chords()

        # Common progression patterns
        if key_obj.key_type == "major":
            patterns = [
                [1, 4, 5, 1],      # I-IV-V-I
                [1, 6, 4, 5],      # I-vi-IV-V
                [1, 5, 6, 4],      # I-V-vi-IV (pop)
                [1, 4, 1, 5],      # I-IV-I-V
                [2, 5, 1],         # ii-V-I
            ]
        else:
            patterns = [
                [1, 4, 5, 1],      # i-iv-V-i
                [1, 6, 7, 1],      # i-VI-VII-i
                [1, 7, 1, 6],      # i-VII-i-VI
            ]

        # Build progression
        chords = []
        remaining = length

        while remaining > 0:
            pattern = random.choice(patterns)
            for degree in pattern:
                if remaining <= 0:
                    break
                if 1 <= degree <= len(diatonic):
                    chords.append(diatonic[degree - 1])
                    remaining -= 1

        return cls(chords=chords[:length], key=key_obj)

    def __repr__(self) -> str:
        """Return string representation."""
        if not self.chords:
            return "Progression([])"
        symbols = [f"{c.root_name}" for c in self.chords]
        return f"Progression({'-'.join(symbols)})"

    def __iter__(self):
        """Allow iteration over chords."""
        return iter(self.chords)

    def __len__(self) -> int:
        """Return length."""
        return len(self.chords)

    def __getitem__(self, index: int) -> Chord:
        """Get chord by index."""
        return self.chords[index]
