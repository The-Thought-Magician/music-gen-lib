"""Key and key signature classes for music theory.

This module provides classes for representing musical keys and
their associated key signatures.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from musicgen.theory.scales import Scale


class KeyType(Enum):
    """Enumeration of key types."""

    MAJOR = "major"
    MINOR = "minor"


# Circle of fifths for sharps
SHARP_ORDER = ["F", "C", "G", "D", "A", "E", "B"]
# Circle of fifths for flats
FLAT_ORDER = ["B", "E", "A", "D", "G", "C", "F"]


@dataclass
class KeySignature:
    """Represents a key signature with its accidentals.

    Attributes:
        sharps: Number of sharps (negative for flats)
        flats: Number of flats (negative for sharps)
    """

    sharps: int = 0
    flats: int = 0

    def __post_init__(self):
        """Initialize key signature."""
        if self.sharps < 0:
            self.sharps = 0
        if self.flats < 0:
            self.flats = 0

    @property
    def accidentals(self) -> list[str]:
        """Return list of accidentals in this key signature."""
        if self.sharps > 0:
            return [f"{n}#" for n in SHARP_ORDER[:self.sharps]]
        elif self.flats > 0:
            return [f"{n}b" for n in FLAT_ORDER[:self.flats]]
        return []

    @classmethod
    def from_key(cls, tonic: str, key_type: str = "major") -> KeySignature:
        """Create a KeySignature from a tonic and key type.

        Args:
            tonic: The tonic note
            key_type: "major" or "minor"

        Returns:
            A KeySignature object
        """
        # Number of sharps/flats for major keys
        major_sharps = {
            "C": 0, "G": 1, "D": 2, "A": 3, "E": 4, "B": 5, "F#": 6, "C#": 7,
            "F": -1, "Bb": -2, "Eb": -3, "Ab": -4, "Db": -5, "Gb": -6, "Cb": -7,
        }

        # Clean up tonic
        tonic = tonic.strip().upper().replace("#", "").replace("b", "")

        if key_type.lower() == "minor":
            # Relative minor is 3 semitones below major
            # So for minor keys, use the major key 3 semitones up
            major_tonics = list(major_sharps.keys())
            try:
                idx = major_tonics.index(tonic)
                # Minor key has same signature as major 3 semitones up
                idx = (idx + 2) % len(major_tonics)
                tonic = major_tonics[idx]
            except ValueError:
                tonic = "C"

        sharps_flats = major_sharps.get(tonic, 0)

        if sharps_flats >= 0:
            return cls(sharps=sharps_flats, flats=0)
        else:
            return cls(sharps=0, flats=-sharps_flats)

    def __repr__(self) -> str:
        """Return string representation."""
        if self.sharps > 0:
            return f"KeySignature({self.sharps} sharps)"
        elif self.flats > 0:
            return f"KeySignature({self.flats} flats)"
        return "KeySignature(0)"


@dataclass
class Key:
    """Represents a musical key with tonic and scale type.

    Attributes:
        tonic: The tonic note name
        key_type: The key type ("major" or "minor")
    """

    tonic: str
    key_type: str = "major"

    def __post_init__(self):
        """Initialize key."""
        self.tonic = self.tonic.strip().upper()

        # Validate key type
        if self.key_type.lower() not in ["major", "minor"]:
            raise ValueError(f"Invalid key type: {self.key_type}. Must be 'major' or 'minor'")

    @property
    def signature(self) -> KeySignature:
        """Return the key signature for this key."""
        return KeySignature.from_key(self.tonic, self.key_type)

    @property
    def scale(self) -> Scale:
        """Return the scale for this key."""
        if self.key_type.lower() == "minor":
            scale_type = "natural_minor"
        else:
            scale_type = "major"

        return Scale(self.tonic, scale_type)

    def relative(self) -> Key:
        """Return the relative key.

        For major keys, returns the relative minor.
        For minor keys, returns the relative major.

        Returns:
            A new Key object
        """
        tonic_note = self.scale.get_degree(1)

        if self.key_type.lower() == "major":
            # Relative minor is 3 semitones down (degree 6)
            relative_tonic = self.scale.get_degree(6)
            new_type = "minor"
        else:
            # Relative major is 3 semitones up (degree 3)
            relative_tonic = self.scale.get_degree(3)
            new_type = "major"

        return Key(
            tonic=relative_tonic.name + relative_tonic.accidental,
            key_type=new_type
        )

    def parallel(self) -> Key:
        """Return the parallel key (same tonic, opposite type).

        Returns:
            A new Key object
        """
        new_type = "minor" if self.key_type.lower() == "major" else "major"
        return Key(tonic=self.tonic, key_type=new_type)

    def diatonic_chords(self) -> list:
        """Return the diatonic chords in this key.

        Returns:
            List of Chord objects
        """
        return self.scale.diatonic_chords()

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Key({self.tonic}, {self.key_type})"

    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, Key):
            return False
        return self.tonic == other.tonic and self.key_type.lower() == other.key_type.lower()
