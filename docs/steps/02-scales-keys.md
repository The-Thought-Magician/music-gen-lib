# Step 2: Music Theory Module - Scales and Keys

## Overview

This step implements the music theory foundation for scale generation, key signatures, and modal relationships. The scales and keys module is essential for all subsequent composition features (melody generation, chord progressions, etc.).

**Prerequisites**: Step 1 (Project Setup and Core Data Structures) must be completed first.

## Project Context

You are working on a Python library called `musicgen` that generates orchestral instrumental music using traditional music theory principles. The project is located at:

```
/home/chiranjeet/projects-cc/projects/music-gen-lib
```

### Expected Project Structure (after Step 1)

```
music-gen-lib/
├── pyproject.toml
├── src/
│   └── musicgen/
│       ├── __init__.py
│       └── core/
│           ├── __init__.py
│           ├── note.py          # Note, Rest, duration/dynamic constants
│           └── chord.py         # Chord class
└── tests/
    ├── test_note.py
    └── test_chord.py
```

### Dependencies from Step 1

Your implementation will depend on the following classes from Step 1:

#### From `src/musicgen/core/note.py`:

```python
class Note:
    """Represents a musical note with pitch, duration, and velocity."""

    def __init__(self, name: str, octave: int, duration: float = 1.0, velocity: int = 100):
        ...

    @property
    def name(self) -> str:
        """Note name (C, C#, D, D#, etc.)."""

    @property
    def octave(self) -> int:
        """Octave number (0-9)."""

    @property
    def midi_number(self) -> int:
        """MIDI note number (0-127)."""

    @property
    def frequency(self) -> float:
        """Frequency in Hz."""

    def __repr__(self) -> str:
        return f"Note('{self.name}{self.octave}')"
```

#### From `src/musicgen/core/chord.py`:

```python
class Chord:
    """Represents a musical chord as a collection of notes."""

    def __init__(self, root: str, quality: str = "major", inversion: int = 0,
                 root_octave: int = 4):
        ...

    @property
    def notes(self) -> List[Note]:
        """List of Note objects in the chord."""

    @property
    def root_name(self) -> str:
        """Root note name."""

    @property
    def quality(self) -> str:
        """Chord quality (major, minor, diminished, augmented, etc.)."""
```

## Implementation Tasks

### Task 1: Create the theory module structure

Create the theory package directory and `__init__.py` file:

**File**: `src/musicgen/theory/__init__.py`

```python
"""
Music theory module for musicgen.

Provides scale generation, key signatures, and modal relationships.
"""

from musicgen.theory.scales import Scale, ScaleType, INTERVALS
from musicgen.theory.keys import Key, KeySignature

__all__ = [
    "Scale",
    "ScaleType",
    "INTERVALS",
    "Key",
    "KeySignature",
]
```

### Task 2: Implement scale patterns and constants

**File**: `src/musicgen/theory/scales.py`

Create a module that defines scale patterns and implements the `Scale` class.

#### 2.1 Define Scale Type Enum and Interval Patterns

```python
from enum import Enum
from typing import List, Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from musicgen.core.note import Note
    from musicgen.core.chord import Chord


class ScaleType(Enum):
    """Enumeration of supported scale types."""
    MAJOR = "major"
    NATURAL_MINOR = "natural_minor"
    HARMONIC_MINOR = "harmonic_minor"
    MELODIC_MINOR = "melodic_minor"
    CHROMATIC = "chromatic"

    # Church modes
    IONIAN = "ionian"
    DORIAN = "dorian"
    PHRYGIAN = "phrygian"
    LYDIAN = "lydian"
    MIXOLYDIAN = "mixolydian"
    AEOLIAN = "aeolian"
    LOCRIAN = "locrian"

    # Pentatonic scales
    MAJOR_PENTATONIC = "major_pentatonic"
    MINOR_PENTATONIC = "minor_pentatonic"

    # Symmetric scales
    WHOLE_TONE = "whole_tone"
    OCTATONIC = "octatonic"
    BLUES = "blues"


# Note names for reference
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_NAMES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


# Interval patterns (in semitones from root)
# W = whole step (2), H = half step (1)
INTERVALS = {
    # Major and minor scales
    ScaleType.MAJOR: [0, 2, 4, 5, 7, 9, 11],           # W-W-H-W-W-W-H
    ScaleType.NATURAL_MINOR: [0, 2, 3, 5, 7, 8, 10],   # W-H-W-W-H-W-W
    ScaleType.HARMONIC_MINOR: [0, 2, 3, 5, 7, 8, 11],  # W-H-W-W-H-W+H-H
    ScaleType.MELODIC_MINOR_ASC: [0, 2, 3, 5, 7, 9, 11],  # W-H-W-W-W-W-H
    ScaleType.MELODIC_MINOR_DESC: [0, 2, 3, 5, 7, 8, 10],  # Same as natural minor

    # Church modes (all from C reference)
    ScaleType.IONIAN: [0, 2, 4, 5, 7, 9, 11],          # Same as major
    ScaleType.DORIAN: [0, 2, 3, 5, 7, 9, 10],          # W-H-W-W-W-H-W
    ScaleType.PHRYGIAN: [0, 1, 3, 5, 7, 8, 10],       # H-W-W-W-H-W-W
    ScaleType.LYDIAN: [0, 2, 4, 6, 7, 9, 11],         # W-W-W-H-W-W-H
    ScaleType.MIXOLYDIAN: [0, 2, 4, 5, 7, 9, 10],     # W-W-H-W-W-H-W
    ScaleType.AEOLIAN: [0, 2, 3, 5, 7, 8, 10],        # Same as natural minor
    ScaleType.LOCRIAN: [0, 1, 3, 5, 6, 8, 10],        # H-W-W-H-W-W-W

    # Pentatonic scales
    ScaleType.MAJOR_PENTATONIC: [0, 2, 4, 7, 9],       # 1-2-3-5-6
    ScaleType.MINOR_PENTATONIC: [0, 3, 5, 7, 10],     # 1-b3-4-5-b7

    # Symmetric scales
    ScaleType.WHOLE_TONE: [0, 2, 4, 6, 8, 10],        # All whole steps
    ScaleType.OCTATONIC: [0, 1, 3, 4, 6, 7, 9, 10],   # W-H-W-H-W-H-W-H
    ScaleType.BLUES: [0, 3, 5, 6, 7, 10],             # 1-b3-4-b5-5-b7

    # Chromatic
    ScaleType.CHROMATIC: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
}
```

#### 2.2 Implement the Scale Class

```python
class Scale:
    """
    Represents a musical scale with a root note and scale type.

    The Scale class provides methods for:
    - Generating scale notes
    - Accessing scale degrees
    - Creating diatonic chords
    - Getting parallel and relative scales
    """

    def __init__(self, root: str, scale_type: str | ScaleType, octave: int = 4):
        """
        Initialize a Scale.

        Args:
            root: Root note name (e.g., "C", "F#", "Bb")
            scale_type: Type of scale (e.g., "major", "dorian", "harmonic_minor")
            octave: Starting octave for the scale (default: 4)

        Raises:
            ValueError: If root note or scale type is invalid
        """
        # Convert string to ScaleType if needed
        if isinstance(scale_type, str):
            try:
                self._scale_type = ScaleType(scale_type.lower())
            except ValueError:
                # Try alternative names
                scale_type = self._normalize_scale_type(scale_type)
                self._scale_type = ScaleType(scale_type)
        else:
            self._scale_type = scale_type

        # Normalize root note (handle flats/sharps)
        self._root = self._normalize_root(root)
        self._octave = octave

        # Get interval pattern
        self._intervals = self._get_intervals()

        # Generate notes
        self._notes = self._generate_notes()

    def _normalize_scale_type(self, scale_type: str) -> str:
        """Normalize various scale type names to valid enum values."""
        mapping = {
            "minor": "natural_minor",
            "harmonic": "harmonic_minor",
            "melodic": "melodic_minor",
            "pentatonic": "major_pentatonic",
            "pentatonic_major": "major_pentatonic",
            "pentatonic_minor": "minor_pentatonic",
            "diminished": "octatonic",
        }
        return mapping.get(scale_type.lower(), scale_type.lower())

    def _normalize_root(self, root: str) -> str:
        """
        Normalize root note name, converting flats to sharps.

        Examples:
            "Db" -> "C#"
            "Gb" -> "F#"
            "Ab" -> "G#"
        """
        root = root.capitalize()
        if root in NOTE_NAMES:
            return root
        if root in NOTE_NAMES_FLAT:
            idx = NOTE_NAMES_FLAT.index(root)
            return NOTE_NAMES[idx]
        raise ValueError(f"Invalid root note: {root}")

    def _get_intervals(self) -> List[int]:
        """Get the interval pattern for this scale type."""
        # Handle melodic minor special case
        if self._scale_type == ScaleType.MELODIC_MINOR:
            return INTERVALS[ScaleType.MELODIC_MINOR_ASC]

        if self._scale_type in INTERVALS:
            return INTERVALS[self._scale_type]

        raise ValueError(f"Unknown scale type: {self._scale_type}")

    def _generate_notes(self) -> List[str]:
        """
        Generate the note names in this scale.

        Returns:
            List of note names (e.g., ["C", "D", "E", "F", "G", "A", "B"])
        """
        root_idx = NOTE_NAMES.index(self._root)
        notes = []

        for interval in self._intervals:
            note_idx = (root_idx + interval) % 12
            notes.append(NOTE_NAMES[note_idx])

        return notes

    @property
    def root(self) -> str:
        """Root note name."""
        return self._root

    @property
    def scale_type(self) -> ScaleType:
        """Scale type."""
        return self._scale_type

    @property
    def notes(self) -> List[str]:
        """List of note names in the scale."""
        return self._notes.copy()

    @property
    def intervals(self) -> List[int]:
        """Interval pattern in semitones."""
        return self._intervals.copy()

    def get_degree(self, degree: int, octave: Optional[int] = None) -> "Note":
        """
        Get a scale degree as a Note object.

        Args:
            degree: Scale degree (1-indexed, can be > 7)
            octave: Octave for the note (default: use scale's octave)

        Returns:
            Note object for the scale degree

        Examples:
            >>> scale = Scale("C", "major")
            >>> scale.get_degree(1)
            Note('C4')
            >>> scale.get_degree(5)
            Note('G4')
            >>> scale.get_degree(8)  # Next octave
            Note('C5')
        """
        if octave is None:
            octave = self._octave

        # Adjust for 1-indexed degrees
        degree_zero_indexed = degree - 1

        # Calculate which octave the degree is in
        num_notes = len(self._notes)
        octave_offset = degree_zero_indexed // num_notes
        note_index = degree_zero_indexed % num_notes

        note_name = self._notes[note_index]
        actual_octave = octave + octave_offset

        from musicgen.core.note import Note
        return Note(note_name, actual_octave)

    def get_note_index(self, note_name: str) -> Optional[int]:
        """
        Get the scale degree index for a given note name.

        Args:
            note_name: Note name to find in the scale

        Returns:
            Scale degree (1-indexed) or None if note not in scale
        """
        note_name = self._normalize_root(note_name)
        if note_name in self._notes:
            return self._notes.index(note_name) + 1
        return None

    def contains(self, note: str | "Note") -> bool:
        """
        Check if a note is in the scale.

        Args:
            note: Note name or Note object

        Returns:
            True if the note is in the scale
        """
        if isinstance(note, str):
            note_name = self._normalize_root(note)
        else:
            note_name = note.name

        return note_name in self._notes

    def transpose(self, interval: int) -> "Scale":
        """
        Transpose the scale by a given interval in semitones.

        Args:
            interval: Number of semitones to transpose (positive or negative)

        Returns:
            New Scale object transposed by the interval
        """
        root_idx = NOTE_NAMES.index(self._root)
        new_idx = (root_idx + interval) % 12
        new_root = NOTE_NAMES[new_idx]
        return Scale(new_root, self._scale_type, self._octave)

    def parallel(self, new_scale_type: str | ScaleType) -> "Scale":
        """
        Get the parallel scale (same root, different scale type).

        Args:
            new_scale_type: The scale type for the parallel scale

        Returns:
            New Scale object with the same root but different type

        Examples:
            >>> c_major = Scale("C", "major")
            >>> c_minor = c_major.parallel("natural_minor")
            >>> c_minor.root
            'C'
            >>> c_minor.scale_type
            ScaleType.NATURAL_MINOR
        """
        return Scale(self._root, new_scale_type, self._octave)

    def relative(self) -> "Scale":
        """
        Get the relative scale.

        For major scales, returns the relative natural minor.
        For natural minor scales, returns the relative major.

        Returns:
            New Scale object that is the relative scale

        Examples:
            >>> c_major = Scale("C", "major")
            >>> a_minor = c_major.relative()
            >>> a_minor.root
            'A'
            >>> a_minor.scale_type
            ScaleType.NATURAL_MINOR
        """
        if self._scale_type == ScaleType.MAJOR:
            # Relative minor is a minor third below
            return self.transpose(-3).parallel("natural_minor")
        elif self._scale_type == ScaleType.NATURAL_MINOR:
            # Relative major is a minor third above
            return self.transpose(3).parallel("major")
        else:
            raise ValueError(
                f"Relative scale only defined for major and natural minor scales, "
                f"not {self._scale_type}"
            )

    def diatonic_chords(self, octave: int = 4) -> List["Chord"]:
        """
        Generate all diatonic triads in this scale.

        Args:
            octave: Octave for the root of each chord

        Returns:
            List of Chord objects, one for each scale degree

        Examples:
            >>> c_major = Scale("C", "major")
            >>> chords = c_major.diatonic_chords()
            >>> [(i+1, c.quality) for i, c in enumerate(chords)]
            [(1, 'major'), (2, 'minor'), (3, 'minor'), (4, 'major'),
             (5, 'major'), (6, 'minor'), (7, 'diminished')]
        """
        from musicgen.core.chord import Chord

        chords = []
        num_notes = len(self._notes)

        # Determine chord qualities based on scale type
        qualities = self._diatonic_qualities()

        for i, note_name in enumerate(self._notes):
            root_note = self.get_degree(i + 1, octave=octave)
            quality = qualities[i]
            chords.append(Chord(root_note.name, quality, root_octave=octave))

        return chords

    def _diatonic_qualities(self) -> List[str]:
        """
        Get the chord qualities for diatonic chords in this scale.

        Returns:
            List of chord quality strings
        """
        # Major scale qualities: major, minor, minor, major, major, minor, diminished
        major_qualities = ["major", "minor", "minor", "major", "major", "minor", "diminished"]

        # Natural minor qualities: minor, diminished, major, minor, minor, major, major
        minor_qualities = ["minor", "diminished", "major", "minor", "minor", "major", "major"]

        # Harmonic minor qualities: minor, diminished, augmented, minor, major, major, diminished
        harmonic_minor_qualities = ["minor", "diminished", "augmented", "minor",
                                   "major", "major", "diminished"]

        if self._scale_type == ScaleType.MAJOR:
            return major_qualities
        elif self._scale_type == ScaleType.IONIAN:
            return major_qualities
        elif self._scale_type == ScaleType.NATURAL_MINOR:
            return minor_qualities
        elif self._scale_type == ScaleType.AEOLIAN:
            return minor_qualities
        elif self._scale_type == ScaleType.HARMONIC_MINOR:
            return harmonic_minor_qualities
        elif self._scale_type == ScaleType.DORIAN:
            # Dorian: minor, minor, major, major, minor, diminished, major
            return ["minor", "minor", "major", "major", "minor", "diminished", "major"]
        elif self._scale_type == ScaleType.PHRYGIAN:
            # Phrygian: minor, major, diminished, minor, minor, major, major
            return ["minor", "major", "diminished", "minor", "minor", "major", "major"]
        elif self._scale_type == ScaleType.LYDIAN:
            # Lydian: major, major, minor, diminished, major, minor, minor
            return ["major", "major", "minor", "diminished", "major", "minor", "minor"]
        elif self._scale_type == ScaleType.MIXOLYDIAN:
            # Mixolydian: major, minor, diminished, major, minor, minor, major
            return ["major", "minor", "diminished", "major", "minor", "minor", "major"]
        elif self._scale_type == ScaleType.LOCRIAN:
            # Locrian: diminished, minor, minor, major, diminished, major, major
            return ["diminished", "minor", "minor", "major", "diminished", "major", "major"]
        else:
            # Default to major qualities for pentatonic and other scales
            # Adjust list length based on number of notes
            num_notes = len(self._notes)
            return major_qualities[:num_notes]

    def __repr__(self) -> str:
        return f"Scale('{self._root}', '{self._scale_type.value}')"

    def __str__(self) -> str:
        return f"{self._root} {self._scale_type.value}: {' '.join(self._notes)}"


# Helper functions
def scale_from_intervals(root: str, intervals: List[int], octave: int = 4) -> Scale:
    """
    Create a Scale from a custom interval pattern.

    Args:
        root: Root note name
        intervals: List of semitone intervals from root
        octave: Starting octave

    Returns:
        Scale object with the custom interval pattern
    """
    scale = Scale(root, ScaleType.MAJOR, octave)  # Temporary
    scale._intervals = intervals
    scale._notes = scale._generate_notes()
    return scale
```

### Task 3: Implement the Key and KeySignature classes

**File**: `src/musicgen/theory/keys.py`

```python
from enum import Enum
from typing import List, Optional, Tuple
from dataclasses import dataclass

from musicgen.theory.scales import Scale, ScaleType, NOTE_NAMES


class Accidentals(Enum):
    """Number of accidentals in key signature."""
    ZERO = 0
    ONE_SHARP = 1
    TWO_SHARPS = 2
    THREE_SHARPS = 3
    FOUR_SHARPS = 4
    FIVE_SHARPS = 5
    SIX_SHARPS = 6
    SEVEN_SHARPS = 7
    ONE_FLAT = -1
    TWO_FLATS = -2
    THREE_FLATS = -3
    FOUR_FLATS = -4
    FIVE_FLATS = -5
    SIX_FLATS = -6
    SEVEN_FLATS = -7


# Order of sharps: F, C, G, D, A, E, B
SHARP_ORDER = ["F", "C", "G", "D", "A", "E", "B"]

# Order of flats: B, E, A, D, G, C, F
FLAT_ORDER = ["B", "E", "A", "D", "G", "C", "F"]

# Major keys by number of sharps/flats
MAJOR_KEYS = {
    0: "C",
    1: "G",
    2: "D",
    3: "A",
    4: "E",
    5: "B",
    6: "F#",
    7: "C#",
    -1: "F",
    -2: "Bb",
    -3: "Eb",
    -4: "Ab",
    -5: "Db",
    -6: "Gb",
    -7: "Cb",
}

# Minor keys by number of sharps/flats
MINOR_KEYS = {
    0: "A",
    1: "E",
    2: "B",
    3: "F#",
    4: "C#",
    5: "G#",
    6: "D#",
    7: "A#",
    -1: "D",
    -2: "G",
    -3: "C",
    -4: "F",
    -5: "Bb",
    -6: "Eb",
    -7: "Ab",
}


@dataclass
class KeySignature:
    """
    Represents a key signature with accidentals.

    Attributes:
        accidentals: Number of accidentals (positive for sharps, negative for flats)
    """

    accidentals: int

    def __post_init__(self):
        """Validate accidental count."""
        if self.accidentals < -7 or self.accidentals > 7:
            raise ValueError("Number of accidentals must be between -7 and 7")

    @property
    def sharps(self) -> List[str]:
        """List of notes that are sharp in this key signature."""
        if self.accidentals <= 0:
            return []
        return SHARP_ORDER[:self.accidentals]

    @property
    def flats(self) -> List[str]:
        """List of notes that are flat in this key signature."""
        if self.accidentals >= 0:
            return []
        return FLAT_ORDER[:abs(self.accidentals)]

    @property
    def is_sharp(self) -> bool:
        """True if this key uses sharps."""
        return self.accidentals > 0

    @property
    def is_flat(self) -> bool:
        """True if this key uses flats."""
        return self.accidentals < 0

    def has_sharp(self, note: str) -> bool:
        """Check if a note is sharp in this key signature."""
        return note in self.sharps

    def has_flat(self, note: str) -> bool:
        """Check if a note is flat in this key signature."""
        return note in self.flats

    @classmethod
    def from_sharps(cls, num_sharps: int) -> "KeySignature":
        """Create a key signature from a number of sharps."""
        return cls(num_sharps)

    @classmethod
    def from_flats(cls, num_flats: int) -> "KeySignature":
        """Create a key signature from a number of flats."""
        return cls(-num_flats)

    def __repr__(self) -> str:
        if self.accidentals == 0:
            return "KeySignature(accidentals=0)"
        elif self.accidentals > 0:
            return f"KeySignature(sharps={self.accidentals})"
        else:
            return f"KeySignature(flats={abs(self.accidentals)})"


class Key:
    """
    Represents a musical key with tonic and mode.

    The Key class provides methods for:
    - Getting the key signature
    - Accessing the scale for the key
    - Getting parallel and relative keys
    - Determining chord qualities
    """

    def __init__(self, tonic: str, mode: str = "major"):
        """
        Initialize a Key.

        Args:
            tonic: Tonic note name (e.g., "C", "F#", "Bb")
            mode: Mode of the key ("major" or "minor")

        Raises:
            ValueError: If tonic or mode is invalid
        """
        # Normalize inputs
        self._tonic = self._normalize_tonic(tonic)
        self._mode = self._normalize_mode(mode)

        # Create the scale for this key
        scale_type = ScaleType.MAJOR if self._mode == "major" else ScaleType.NATURAL_MINOR
        self._scale = Scale(self._tonic, scale_type)

        # Determine key signature
        self._signature = self._determine_signature()

    def _normalize_tonic(self, tonic: str) -> str:
        """Normalize tonic note name."""
        tonic = tonic.capitalize()
        if tonic in NOTE_NAMES:
            return tonic
        # Handle flats using enharmonic equivalence
        flat_to_sharp = {
            "Db": "C#", "Eb": "D#", "Gb": "F#",
            "Ab": "G#", "Bb": "A#", "Cb": "B", "Fb": "E"
        }
        if tonic in flat_to_sharp:
            return flat_to_sharp[tonic]
        raise ValueError(f"Invalid tonic note: {tonic}")

    def _normalize_mode(self, mode: str) -> str:
        """Normalize mode name."""
        mode = mode.lower()
        if mode in ["major", "maj", "M"]:
            return "major"
        elif mode in ["minor", "min", "m", "natural_minor", "aeolian"]:
            return "minor"
        else:
            raise ValueError(f"Invalid mode: {mode}. Use 'major' or 'minor'.")

    def _determine_signature(self) -> KeySignature:
        """Determine the key signature from tonic and mode."""
        # Look up tonic in major/minor key tables
        if self._mode == "major":
            for accidentals, key in MAJOR_KEYS.items():
                if key == self._tonic:
                    return KeySignature(accidentals)
        else:
            for accidentals, key in MINOR_KEYS.items():
                if key == self._tonic:
                    return KeySignature(accidentals)

        # If not found, calculate using circle of fifths
        return self._calculate_signature()

    def _calculate_signature(self) -> KeySignature:
        """Calculate key signature using circle of fifths."""
        # C major / A minor = 0 accidentals
        # Each perfect fifth up adds a sharp
        # Each perfect fourth up adds a flat

        # For simplicity, just find the closest match
        if self._mode == "major":
            key_table = MAJOR_KEYS
        else:
            key_table = MINOR_KEYS

        # Check enharmonic equivalents for edge cases
        enharmonics = {
            "Db": "C#", "Eb": "D#", "Gb": "F#",
            "Ab": "G#", "Bb": "A#"
        }

        for accidentals, key in key_table.items():
            if key == self._tonic:
                return KeySignature(accidentals)

        # Default to 0 if not found
        return KeySignature(0)

    @property
    def tonic(self) -> str:
        """Tonic note name."""
        return self._tonic

    @property
    def mode(self) -> str:
        """Mode of the key ('major' or 'minor')."""
        return self._mode

    @property
    def signature(self) -> KeySignature:
        """Key signature."""
        return self._signature

    @property
    def scale(self) -> Scale:
        """Scale for this key."""
        return self._scale

    def parallel(self) -> "Key":
        """
        Get the parallel key (same tonic, opposite mode).

        Examples:
            >>> c_major = Key("C", "major")
            >>> c_minor = c_major.parallel()
            >>> c_minor.tonic
            'C'
            >>> c_minor.mode
            'minor'
        """
        new_mode = "minor" if self._mode == "major" else "major"
        return Key(self._tonic, new_mode)

    def relative(self) -> "Key":
        """
        Get the relative key.

        For major keys, returns the relative minor.
        For minor keys, returns the relative major.

        Examples:
            >>> c_major = Key("C", "major")
            >>> a_minor = c_major.relative()
            >>> a_minor.tonic
            'A'
            >>> a_minor.mode
            'minor'
        """
        if self._mode == "major":
            # Relative minor is a minor third below
            new_tonic = self._transpose_tonic(-3)
            return Key(new_tonic, "minor")
        else:
            # Relative major is a minor third above
            new_tonic = self._transpose_tonic(3)
            return Key(new_tonic, "major")

    def _transpose_tonic(self, semitones: int) -> str:
        """Transpose tonic by semitones and return note name."""
        idx = NOTE_NAMES.index(self._tonic)
        new_idx = (idx + semitones) % 12
        return NOTE_NAMES[new_idx]

    def transpose(self, semitones: int) -> "Key":
        """
        Transpose the key by semitones.

        Args:
            semitones: Number of semitones to transpose

        Returns:
            New Key object transposed by the given interval
        """
        new_tonic = self._transpose_tonic(semitones)
        return Key(new_tonic, self._mode)

    def get_chord_quality(self, scale_degree: int) -> str:
        """
        Get the chord quality for a diatonic chord degree.

        Args:
            scale_degree: Scale degree (1-7)

        Returns:
            Chord quality string ('major', 'minor', 'diminished', 'augmented')

        Examples:
            >>> c_major = Key("C", "major")
            >>> c_major.get_chord_quality(1)
            'major'
            >>> c_major.get_chord_quality(2)
            'minor'
            >>> c_major.get_chord_quality(7)
            'diminished'
        """
        if not 1 <= scale_degree <= 7:
            raise ValueError("Scale degree must be between 1 and 7")

        chords = self._scale.diatonic_chords()
        return chords[scale_degree - 1].quality

    def diatonic_chords(self, octave: int = 4) -> List:
        """
        Get all diatonic triads in this key.

        Args:
            octave: Octave for chord roots

        Returns:
            List of Chord objects for each scale degree
        """
        return self._scale.diatonic_chords(octave=octave)

    def __repr__(self) -> str:
        return f"Key('{self._tonic}', '{self._mode}')"

    def __str__(self) -> str:
        mode_str = self._mode.capitalize()
        return f"{self._tonic} {mode_str}"


# Helper functions
def key_from_signature(signature: KeySignature, mode: str = "major") -> Key:
    """
    Create a Key from a key signature.

    Args:
        signature: KeySignature object
        mode: 'major' or 'minor'

    Returns:
        Key object corresponding to the signature
    """
    if mode == "major":
        tonic = MAJOR_KEYS.get(signature.accidentals, "C")
    else:
        tonic = MINOR_KEYS.get(signature.accidentals, "A")

    return Key(tonic, mode)


def get_key_signature(tonic: str, mode: str = "major") -> KeySignature:
    """
    Get the key signature for a given tonic and mode.

    Args:
        tonic: Tonic note name
        mode: 'major' or 'minor'

    Returns:
        KeySignature object
    """
    key = Key(tonic, mode)
    return key.signature
```

### Task 4: Update package exports

**File**: `src/musicgen/__init__.py`

Add the theory module to the main package exports:

```python
"""
Music Generation Library - Rule-based orchestral music composition.

This library generates orchestral music using traditional music theory principles.
"""

__version__ = "0.1.0"

# Core imports
from musicgen.core import Note, Rest, Chord
from musicgen.core.constants import WHOLE, HALF, QUARTER, EIGHTH, SIXTEENTH
from musicgen.core.constants import PP, P, MP, MF, F, FF

# Theory imports
from musicgen.theory import Scale, ScaleType, Key, KeySignature

__all__ = [
    # Core
    "Note",
    "Rest",
    "Chord",
    "WHOLE",
    "HALF",
    "QUARTER",
    "EIGHTH",
    "SIXTEENTH",
    "PP",
    "P",
    "MP",
    "MF",
    "F",
    "FF",
    # Theory
    "Scale",
    "ScaleType",
    "Key",
    "KeySignature",
]
```

## Test Requirements

Create comprehensive tests for the scales and keys module.

### Test File: `tests/test_scales.py`

```python
import pytest
from musicgen.theory.scales import Scale, ScaleType, INTERVALS, NOTE_NAMES


class TestScaleType:
    """Test ScaleType enum."""

    def test_scale_type_values(self):
        """Test that all expected scale types are defined."""
        assert ScaleType.MAJOR.value == "major"
        assert ScaleType.NATURAL_MINOR.value == "natural_minor"
        assert ScaleType.DORIAN.value == "dorian"
        assert ScaleType.MAJOR_PENTATONIC.value == "major_pentatonic"


class TestIntervals:
    """Test interval definitions."""

    def test_major_intervals(self):
        """Test major scale intervals."""
        assert INTERVALS[ScaleType.MAJOR] == [0, 2, 4, 5, 7, 9, 11]

    def test_minor_intervals(self):
        """Test minor scale intervals."""
        assert INTERVALS[ScaleType.NATURAL_MINOR] == [0, 2, 3, 5, 7, 8, 10]

    def test_harmonic_minor_intervals(self):
        """Test harmonic minor has raised seventh."""
        assert INTERVALS[ScaleType.HARMONIC_MINOR] == [0, 2, 3, 5, 7, 8, 11]

    def test_dorian_intervals(self):
        """Test Dorian mode intervals."""
        assert INTERVALS[ScaleType.DORIAN] == [0, 2, 3, 5, 7, 9, 10]

    def test_pentatonic_intervals(self):
        """Test pentatonic scale intervals."""
        assert len(INTERVALS[ScaleType.MAJOR_PENTATONIC]) == 5
        assert INTERVALS[ScaleType.MAJOR_PENTATONIC] == [0, 2, 4, 7, 9]


class TestScale:
    """Test Scale class."""

    def test_c_major_scale(self):
        """Test C major scale."""
        scale = Scale("C", "major")
        assert scale.root == "C"
        assert scale.scale_type == ScaleType.MAJOR
        assert scale.notes == ["C", "D", "E", "F", "G", "A", "B"]

    def test_a_minor_scale(self):
        """Test A natural minor scale."""
        scale = Scale("A", "natural_minor")
        assert scale.root == "A"
        assert scale.notes == ["A", "B", "C", "D", "E", "F", "G"]

    def test_d_dorian_scale(self):
        """Test D Dorian mode."""
        scale = Scale("D", "dorian")
        assert scale.notes == ["D", "E", "F", "G", "A", "B", "C"]

    def test_g_harmonic_minor(self):
        """Test G harmonic minor has raised seventh."""
        scale = Scale("G", "harmonic_minor")
        assert "F#" in scale.notes

    def test_f_lydian_scale(self):
        """Test F Lydian mode."""
        scale = Scale("F", "lydian")
        assert scale.notes == ["F", "G", "A", "Bb", "C", "D", "E"]

    def test_scale_with_flat_note(self):
        """Test scale creation with flat root."""
        scale = Scale("Bb", "major")
        assert scale.root == "A#"  # Flats converted to sharps

    def test_major_pentatonic(self):
        """Test C major pentatonic."""
        scale = Scale("C", "major_pentatonic")
        assert scale.notes == ["C", "D", "E", "G", "A"]

    def test_minor_pentatonic(self):
        """Test A minor pentatonic."""
        scale = Scale("A", "minor_pentatonic")
        assert scale.notes == ["A", "C", "D", "E", "G"]

    def test_whole_tone_scale(self):
        """Test C whole tone scale."""
        scale = Scale("C", "whole_tone")
        assert len(scale.notes) == 6
        assert scale.notes == ["C", "D", "E", "F#", "G#", "A#"]

    def test_blues_scale(self):
        """Test C blues scale."""
        scale = Scale("C", "blues")
        assert "F#" in scale.notes  # Blue note (flat 5)


class TestScaleDegree:
    """Test scale degree access."""

    def test_get_degree_1(self):
        """Test getting first scale degree."""
        scale = Scale("C", "major")
        note = scale.get_degree(1)
        assert note.name == "C"
        assert note.octave == 4

    def test_get_degree_5(self):
        """Test getting fifth scale degree."""
        scale = Scale("C", "major")
        note = scale.get_degree(5)
        assert note.name == "G"

    def test_get_degree_above_7(self):
        """Test getting scale degree above 7."""
        scale = Scale("C", "major")
        note = scale.get_degree(8)
        assert note.name == "C"
        assert note.octave == 5

    def test_get_degree_custom_octave(self):
        """Test getting scale degree with custom octave."""
        scale = Scale("C", "major", octave=3)
        note = scale.get_degree(1)
        assert note.octave == 3


class TestScaleContains:
    """Test scale membership tests."""

    def test_contains_note_in_scale(self):
        """Test checking if note is in scale."""
        scale = Scale("C", "major")
        assert scale.contains("C")
        assert scale.contains("E")
        assert scale.contains("G")

    def test_contains_note_not_in_scale(self):
        """Test checking if note is not in scale."""
        scale = Scale("C", "major")
        assert not scale.contains("C#")
        assert not scale.contains("F#")

    def test_get_note_index(self):
        """Test getting scale degree index."""
        scale = Scale("C", "major")
        assert scale.get_note_index("C") == 1
        assert scale.get_note_index("D") == 2
        assert scale.get_note_index("G") == 5


class TestScaleTransposition:
    """Test scale transposition."""

    def test_transpose_up(self):
        """Test transposing scale up."""
        c_major = Scale("C", "major")
        d_major = c_major.transpose(2)
        assert d_major.root == "D"
        assert d_major.scale_type == ScaleType.MAJOR

    def test_transpose_down(self):
        """Test transposing scale down."""
        c_major = Scale("C", "major")
        g_major = c_major.transpose(-5)
        assert g_major.root == "G"

    def test_transpose_preserves_type(self):
        """Test transposition preserves scale type."""
        d_dorian = Scale("D", "dorian")
        e_dorian = d_dorian.transpose(2)
        assert e_dorian.scale_type == ScaleType.DORIAN


class TestParallelScale:
    """Test parallel scale relationship."""

    def test_parallel_major_to_minor(self):
        """Test getting parallel minor from major."""
        c_major = Scale("C", "major")
        c_minor = c_major.parallel("natural_minor")
        assert c_minor.root == "C"
        assert c_minor.scale_type == ScaleType.NATURAL_MINOR

    def test_parallel_minor_to_major(self):
        """Test getting parallel major from minor."""
        a_minor = Scale("A", "natural_minor")
        a_major = a_minor.parallel("major")
        assert a_major.root == "A"
        assert a_major.scale_type == ScaleType.MAJOR


class TestRelativeScale:
    """Test relative scale relationship."""

    def test_relative_minor_from_major(self):
        """Test getting relative minor from major."""
        c_major = Scale("C", "major")
        a_minor = c_major.relative()
        assert a_minor.root == "A"
        assert a_minor.scale_type == ScaleType.NATURAL_MINOR

    def test_relative_major_from_minor(self):
        """Test getting relative major from minor."""
        a_minor = Scale("A", "natural_minor")
        c_major = a_minor.relative()
        assert c_major.root == "C"
        assert c_major.scale_type == ScaleType.MAJOR

    def test_relative_not_defined_for_dorian(self):
        """Test relative scale not defined for modes."""
        d_dorian = Scale("D", "dorian")
        with pytest.raises(ValueError):
            d_dorian.relative()


class TestDiatonicChords:
    """Test diatonic chord generation."""

    def test_major_diatonic_chords(self):
        """Test diatonic chords in major key."""
        scale = Scale("C", "major")
        chords = scale.diatonic_chords()

        assert len(chords) == 7
        assert chords[0].quality == "major"  # I
        assert chords[1].quality == "minor"  # ii
        assert chords[2].quality == "minor"  # iii
        assert chords[3].quality == "major"  # IV
        assert chords[4].quality == "major"  # V
        assert chords[5].quality == "minor"  # vi
        assert chords[6].quality == "diminished"  # vii

    def test_minor_diatonic_chords(self):
        """Test diatonic chords in minor key."""
        scale = Scale("A", "natural_minor")
        chords = scale.diatonic_chords()

        assert chords[0].quality == "minor"  # i
        assert chords[1].quality == "diminished"  # ii
        assert chords[2].quality == "major"  # III
        assert chords[3].quality == "minor"  # iv
        assert chords[4].quality == "minor"  # v
        assert chords[5].quality == "major"  # VI
        assert chords[6].quality == "major"  # VII

    def test_harmonic_minor_diatonic_chords(self):
        """Test diatonic chords in harmonic minor."""
        scale = Scale("A", "harmonic_minor")
        chords = scale.diatonic_chords()

        assert chords[0].quality == "minor"  # i
        assert chords[1].quality == "diminished"  # ii
        assert chords[2].quality == "augmented"  # III+
        assert chords[4].quality == "major"  # V (dominant)

    def test_dorian_diatonic_chords(self):
        """Test diatonic chords in Dorian mode."""
        scale = Scale("D", "dorian")
        chords = scale.diatonic_chords()

        # Dorian: i, ii, III, IV, v, vi, VII
        assert chords[0].quality == "minor"
        assert chords[1].quality == "minor"
        assert chords[2].quality == "major"


class TestScaleStringRepresentation:
    """Test scale string representations."""

    def test_repr(self):
        """Test scale repr."""
        scale = Scale("C", "major")
        assert repr(scale) == "Scale('C', 'major')"

    def test_str(self):
        """Test scale string output."""
        scale = Scale("C", "major")
        str_output = str(scale)
        assert "C" in str_output
        assert "major" in str_output


class TestInvalidInputs:
    """Test error handling for invalid inputs."""

    def test_invalid_root(self):
        """Test error on invalid root note."""
        with pytest.raises(ValueError):
            Scale("H", "major")

    def test_invalid_scale_type(self):
        """Test error on invalid scale type."""
        with pytest.raises(ValueError):
            Scale("C", "nonexistent")
```

### Test File: `tests/test_keys.py`

```python
import pytest
from musicgen.theory.keys import (
    Key, KeySignature, Accidentals,
    SHARP_ORDER, FLAT_ORDER, MAJOR_KEYS, MINOR_KEYS,
    key_from_signature, get_key_signature
)


class TestKeySignature:
    """Test KeySignature class."""

    def test_c_major_signature(self):
        """Test C major has no accidentals."""
        signature = KeySignature(0)
        assert signature.accidentals == 0
        assert signature.sharps == []
        assert signature.flats == []
        assert not signature.is_sharp
        assert not signature.is_flat

    def test_one_sharp(self):
        """Test one sharp (G major)."""
        signature = KeySignature(1)
        assert signature.sharps == ["F"]
        assert signature.has_sharp("F")
        assert not signature.has_sharp("C")

    def test_two_sharps(self):
        """Test two sharps (D major)."""
        signature = KeySignature(2)
        assert signature.sharps == ["F", "C"]

    def test_all_sharps(self):
        """Test all seven sharps (C# major)."""
        signature = KeySignature(7)
        assert len(signature.sharps) == 7
        assert signature.has_sharp("B")

    def test_one_flat(self):
        """Test one flat (F major)."""
        signature = KeySignature(-1)
        assert signature.flats == ["B"]
        assert signature.has_flat("B")

    def test_all_flats(self):
        """Test all seven flats (Cb major)."""
        signature = KeySignature(-7)
        assert len(signature.flats) == 7
        assert signature.has_flat("F")

    def test_invalid_accidentals(self):
        """Test error on invalid accidental count."""
        with pytest.raises(ValueError):
            KeySignature(8)
        with pytest.raises(ValueError):
            KeySignature(-8)

    def test_from_sharps(self):
        """Test creating signature from sharps."""
        signature = KeySignature.from_sharps(3)
        assert signature.accidentals == 3
        assert signature.is_sharp

    def test_from_flats(self):
        """Test creating signature from flats."""
        signature = KeySignature.from_flats(3)
        assert signature.accidentals == -3
        assert signature.is_flat


class TestKeyTables:
    """Test major/minor key lookup tables."""

    def test_sharp_order(self):
        """Test order of sharps."""
        assert SHARP_ORDER == ["F", "C", "G", "D", "A", "E", "B"]

    def test_flat_order(self):
        """Test order of flats."""
        assert FLAT_ORDER == ["B", "E", "A", "D", "G", "C", "F"]

    def test_major_keys(self):
        """Test major key table."""
        assert MAJOR_KEYS[0] == "C"
        assert MAJOR_KEYS[1] == "G"
        assert MAJOR_KEYS[-1] == "F"

    def test_minor_keys(self):
        """Test minor key table."""
        assert MINOR_KEYS[0] == "A"
        assert MINOR_KEYS[1] == "E"
        assert MINOR_KEYS[-1] == "D"


class TestKey:
    """Test Key class."""

    def test_c_major_key(self):
        """Test C major key."""
        key = Key("C", "major")
        assert key.tonic == "C"
        assert key.mode == "major"
        assert key.signature.accidentals == 0

    def test_a_minor_key(self):
        """Test A minor key."""
        key = Key("A", "minor")
        assert key.tonic == "A"
        assert key.mode == "minor"
        assert key.signature.accidentals == 0

    def test_g_major_key(self):
        """Test G major key (one sharp)."""
        key = Key("G", "major")
        assert key.tonic == "G"
        assert key.signature.accidentals == 1

    def test_f_major_key(self):
        """Test F major key (one flat)."""
        key = Key("F", "major")
        assert key.tonic == "F"
        assert key.signature.accidentals == -1

    def test_e_minor_key(self):
        """Test E minor key (one sharp)."""
        key = Key("E", "minor")
        assert key.tonic == "E"
        assert key.signature.accidentals == 1

    def test_d_minor_key(self):
        """Test D minor key (one flat)."""
        key = Key("D", "minor")
        assert key.tonic == "D"
        assert key.signature.accidentals == -1

    def test_key_has_scale(self):
        """Test key has associated scale."""
        key = Key("C", "major")
        scale = key.scale
        assert scale.notes == ["C", "D", "E", "F", "G", "A", "B"]

    def test_mode_normalization(self):
        """Test various mode names are normalized."""
        key1 = Key("C", "maj")
        key2 = Key("C", "M")
        key3 = Key("C", "major")
        assert key1.mode == "major"
        assert key2.mode == "major"
        assert key3.mode == "major"

    def test_flat_tonic_normalization(self):
        """Test flat tonics are converted to sharps."""
        key = Key("Bb", "major")
        # Bb major is enharmonic to A# major (uses flats in notation)
        # Internally we may use sharps, but the key signature should be correct
        assert key.signature.accidentals == -2  # Bb major has 2 flats


class TestKeyParallel:
    """Test parallel key relationship."""

    def test_parallel_major_to_minor(self):
        """Test getting parallel minor from major."""
        c_major = Key("C", "major")
        c_minor = c_major.parallel()
        assert c_minor.tonic == "C"
        assert c_minor.mode == "minor"

    def test_parallel_minor_to_major(self):
        """Test getting parallel major from minor."""
        a_minor = Key("A", "minor")
        a_major = a_minor.parallel()
        assert a_major.tonic == "A"
        assert a_major.mode == "major"

    def test_parallel_preserves_tonic(self):
        """Test parallel key has same tonic."""
        d_major = Key("D", "major")
        d_minor = d_major.parallel()
        assert d_major.tonic == d_minor.tonic


class TestKeyRelative:
    """Test relative key relationship."""

    def test_relative_minor_from_major(self):
        """Test getting relative minor from major."""
        c_major = Key("C", "major")
        a_minor = c_major.relative()
        assert a_minor.tonic == "A"
        assert a_minor.mode == "minor"

    def test_relative_major_from_minor(self):
        """Test getting relative major from minor."""
        a_minor = Key("A", "minor")
        c_major = a_minor.relative()
        assert c_major.tonic == "C"
        assert c_major.mode == "major"

    def test_relative_g_major(self):
        """Test G major relative is E minor."""
        g_major = Key("G", "major")
        e_minor = g_major.relative()
        assert e_minor.tonic == "E"
        assert e_minor.mode == "minor"

    def test_relative_d_major(self):
        """Test D major relative is B minor."""
        d_major = Key("D", "major")
        b_minor = d_major.relative()
        assert b_minor.tonic == "B"
        assert b_minor.mode == "minor"


class TestKeyTransposition:
    """Test key transposition."""

    def test_transpose_up_fifth(self):
        """Test transposing up a perfect fifth."""
        c_major = Key("C", "major")
        g_major = c_major.transpose(7)
        assert g_major.tonic == "G"
        assert g_major.mode == "major"

    def test_transpose_down_fifth(self):
        """Test transposing down a perfect fifth."""
        c_major = Key("C", "major")
        f_major = c_major.transpose(-7)
        assert f_major.tonic == "F"
        assert f_major.mode == "major"

    def test_transpose_preserves_mode(self):
        """Test transposition preserves mode."""
        a_minor = Key("A", "minor")
        e_minor = a_minor.transpose(7)
        assert e_minor.tonic == "E"
        assert e_minor.mode == "minor"


class TestKeyChordQualities:
    """Test getting chord qualities from key."""

    def test_major_chord_qualities(self):
        """Test chord qualities in major key."""
        key = Key("C", "major")
        assert key.get_chord_quality(1) == "major"
        assert key.get_chord_quality(2) == "minor"
        assert key.get_chord_quality(3) == "minor"
        assert key.get_chord_quality(4) == "major"
        assert key.get_chord_quality(5) == "major"
        assert key.get_chord_quality(6) == "minor"
        assert key.get_chord_quality(7) == "diminished"

    def test_minor_chord_qualities(self):
        """Test chord qualities in minor key."""
        key = Key("A", "minor")
        assert key.get_chord_quality(1) == "minor"
        assert key.get_chord_quality(2) == "diminished"
        assert key.get_chord_quality(3) == "major"

    def test_invalid_scale_degree(self):
        """Test error on invalid scale degree."""
        key = Key("C", "major")
        with pytest.raises(ValueError):
            key.get_chord_quality(0)
        with pytest.raises(ValueError):
            key.get_chord_quality(8)


class TestKeyDiatonicChords:
    """Test diatonic chord generation from keys."""

    def test_diatonic_chords(self):
        """Test getting all diatonic chords."""
        key = Key("C", "major")
        chords = key.diatonic_chords()
        assert len(chords) == 7
        assert chords[0].root_name == "C"
        assert chords[3].root_name == "F"


class TestKeyStringRepresentation:
    """Test key string representations."""

    def test_repr(self):
        """Test key repr."""
        key = Key("C", "major")
        assert repr(key) == "Key('C', 'major')"

    def test_str(self):
        """Test key string output."""
        key = Key("C", "major")
        assert str(key) == "C Major"


class TestHelperFunctions:
    """Test helper functions."""

    def test_key_from_signature_major(self):
        """Test creating key from signature (major)."""
        signature = KeySignature(3)  # A major
        key = key_from_signature(signature, "major")
        assert key.tonic == "A"
        assert key.mode == "major"

    def test_key_from_signature_minor(self):
        """Test creating key from signature (minor)."""
        signature = KeySignature(1)  # E minor
        key = key_from_signature(signature, "minor")
        assert key.tonic == "E"
        assert key.mode == "minor"

    def test_get_key_signature(self):
        """Test getting key signature."""
        signature = get_key_signature("D", "major")
        assert signature.accidentals == 2
        assert signature.is_sharp


class TestInvalidInputs:
    """Test error handling for invalid inputs."""

    def test_invalid_tonic(self):
        """Test error on invalid tonic."""
        with pytest.raises(ValueError):
            Key("H", "major")

    def test_invalid_mode(self):
        """Test error on invalid mode."""
        with pytest.raises(ValueError):
            Key("C", "dorian")
```

## Validation

After implementation, run the following tests to verify the implementation:

```bash
# Run all tests
pytest tests/test_scales.py tests/test_keys.py -v

# Run with coverage
pytest tests/test_scales.py tests/test_keys.py --cov=src/musicgen/theory --cov-report=html

# Test import from package root
python -c "from musicgen import Scale, Key; print('Import successful')"
```

## Expected Deliverables

After completing this step, the following files should exist:

1. `src/musicgen/theory/__init__.py` - Theory module exports
2. `src/musicgen/theory/scales.py` - Scale implementation
3. `src/musicgen/theory/keys.py` - Key/KeySignature implementation
4. `tests/test_scales.py` - Scale tests
5. `tests/test_keys.py` - Key tests

## Implementation Notes

1. **Import Order**: Place imports at the top of files in this order: standard library, third-party, local imports
2. **Type Hints**: Use proper type hints throughout, using `List[str]` instead of `list[str]` for Python 3.8+ compatibility
3. **Docstrings**: Use Google-style docstrings for all classes and methods
4. **Flat/Sharp Handling**: Internally prefer sharps over flats for consistency
5. **Error Messages**: Provide clear, helpful error messages for invalid inputs
6. **Testing**: Ensure all edge cases are tested (invalid inputs, boundary conditions, etc.)

## Common Patterns

Use these patterns throughout the implementation:

### Note Name Normalization
```python
def _normalize_note(self, note: str) -> str:
    """Convert flats to sharps and capitalize."""
    note = note.capitalize()
    if note in NOTE_NAMES:
        return note
    if note in NOTE_NAMES_FLAT:
        idx = NOTE_NAMES_FLAT.index(note)
        return NOTE_NAMES[idx]
    raise ValueError(f"Invalid note: {note}")
```

### Scale Type Normalization
```python
def _normalize_scale_type(self, scale_type: str) -> ScaleType:
    """Accept various names for scale types."""
    scale_type = scale_type.lower()
    mapping = {"minor": "natural_minor", ...}
    return ScaleType(mapping.get(scale_type, scale_type))
```

## Success Criteria

This step is complete when:

1. All scale types generate correct note sequences
2. Scale degree access works for all degrees including > 7
3. Diatonic chord generation produces correct chord qualities
4. Parallel and relative scale/key relationships work correctly
5. Key signatures are correctly determined for all major/minor keys
6. All tests pass with > 90% code coverage
7. Code follows PEP 8 style guidelines
8. All classes and methods have complete docstrings
