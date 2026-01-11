# Step 1: Project Setup and Core Data Structures

## Overview

This is the first implementation step for the Music Generation Library. This step establishes the project foundation by creating the directory structure, configuring the build system, and implementing the fundamental music data structures that all other modules will depend on.

## Context

You are building a Python library for generating orchestral instrumental music using traditional music theory principles (rule-based composition, NOT AI). The library will produce sheet music (MusicXML/LilyPond) and audio files (WAV/FLAC) from programmatic input based on mood/theme parameters.

This is Step 1 of 13 steps. The core data structures you implement here (Note, Chord, Rest) are the building blocks for the entire system.

## Project Structure to Create

```
music-gen-lib/
├── src/
│   └── musicgen/
│       ├── __init__.py           # Package initialization, exports main classes
│       ├── core/
│       │   ├── __init__.py       # Export Note, Rest, Chord, constants
│       │   ├── note.py           # Note, Rest classes, duration/dynamic constants
│       │   └── chord.py          # Chord class
│       ├── theory/               # (empty for now, create __init__.py)
│       │   └── __init__.py
│       ├── composition/          # (empty for now, create __init__.py)
│       │   └── __init__.py
│       ├── orchestration/        # (empty for now, create __init__.py)
│       │   └── __init__.py
│       ├── io/                   # (empty for now, create __init__.py)
│       │   └── __init__.py
│       └── config/               # (empty for now, create __init__.py)
│           └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_note.py
│   └── test_chord.py
├── examples/                     # (empty directory for now)
├── docs/                         # (already exists)
├── pyproject.toml
├── README.md                     # Basic placeholder
└── .gitignore
```

## Implementation Tasks

### Task 1: Create pyproject.toml

Create `pyproject.toml` in the project root with the following configuration:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "musicgen"
version = "0.1.0"
description = "A rule-based orchestral music generation library"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["music", "composition", "midi", "music-theory", "orchestration"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Multimedia :: Sound/Audio :: MIDI",
    "Topic :: Artistic Software",
]

dependencies = [
    "music21>=9.0",
    "mido>=1.2",
    "pretty-midi>=0.2",
    "numpy>=1.24",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "sphinx>=5.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/music-gen-lib"
Documentation = "https://music-gen-lib.readthedocs.io"
Repository = "https://github.com/yourusername/music-gen-lib"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-dir]
"" = "src"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.coverage.run]
source = ["src"]
omit = ["tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

### Task 2: Implement Note and Rest Classes

Create `src/musicgen/core/note.py` with the following:

#### Duration Constants

Define duration values as fractions of a whole note:

```python
# Duration constants (in quarter notes)
WHOLE = 4.0      # 1 whole note = 4 quarter notes
HALF = 2.0       # 1 half note = 2 quarter notes
QUARTER = 1.0    # 1 quarter note
EIGHTH = 0.5     # 1 eighth note
SIXTEENTH = 0.25 # 1 sixteenth note

# Dotted durations
DOTTED_HALF = 3.0
DOTTED_QUARTER = 1.5
DOTTED_EIGHTH = 0.75

# Triplet durations
TRIPLET_HALF = 2.0 / 3 * 2
TRIPLET_QUARTER = 1.0 / 3 * 2
TRIPLET_EIGHTH = 0.5 / 3 * 2
```

#### Dynamic Constants

```python
# Dynamic marking constants (velocity values 0-127)
PP = 30   # pianissimo
P = 50    # piano
MP = 70   # mezzo-piano
MF = 90   # mezzo-forte
F = 100   # forte
FF = 120  # fortissimo
```

#### Note Names and Accidentals

```python
NOTE_NAMES = ["C", "D", "E", "F", "G", "A", "B"]
ACCIDENTALS = ["", "#", "b", "x", "bb"]  # natural, sharp, flat, double sharp, double flat
```

#### Note Class

```python
class Note:
    """Represents a musical note with pitch, duration, and attributes.

    Attributes:
        name (str): The note name (C, D, E, F, G, A, B)
        octave (int): The octave number (0-9)
        duration (float): Duration in quarter notes
        velocity (int): MIDI velocity (0-127)
        accidental (str): Accidental ("", "#", "b", "x", "bb")
        tied (bool): Whether this note is tied to the next
        articulation (str): Articulation mark (".", ">", "-", "^")
    """

    def __init__(self, pitch: str, duration: float = QUARTER, velocity: int = MF,
                 accidental: str = "", tied: bool = False, articulation: str = ""):
        """Initialize a Note.

        Args:
            pitch: Pitch string (e.g., "C4", "A#5", "Bb3")
            duration: Duration in quarter notes (default: QUARTER)
            velocity: MIDI velocity 0-127 (default: MF = 90)
            accidental: Accidental override (default: auto-detected from pitch)
            tied: Whether tied to next note (default: False)
            articulation: Articulation mark (default: None)

        Raises:
            ValueError: If pitch string is invalid or velocity out of range
        """
        pass  # TODO: Implement

    @property
    def name(self) -> str:
        """Return the note name (C, D, E, etc.)."""
        pass

    @property
    def octave(self) -> int:
        """Return the octave number."""
        pass

    @property
    def midi_number(self) -> int:
        """Return the MIDI note number (0-127).

        C4 = 60, A4 = 69
        """
        pass

    @property
    def frequency(self) -> float:
        """Return the frequency in Hz using A4 = 440Hz standard."""
        pass

    @property
    def pitch_class(self) -> int:
        """Return the pitch class (0-11, where C=0, C#=1, etc.)."""
        pass

    def transpose(self, semitones: int) -> "Note":
        """Return a new Note transposed by the given semitones.

        Args:
            semitones: Number of semitones to transpose (positive = up, negative = down)

        Returns:
            A new Note instance
        """
        pass

    def to_pitch_string(self) -> str:
        """Return the note as a pitch string (e.g., 'C#4', 'Bb3')."""
        pass

    def __repr__(self) -> str:
        """Return string representation (e.g., 'Note(C4, 1.0)')."""
        pass

    def __eq__(self, other) -> bool:
        """Check equality based on pitch (name, octave, accidental)."""
        pass

    def __hash__(self) -> int:
        """Make Note hashable for use in sets/dicts."""
        pass

    @classmethod
    def from_midi(cls, midi_number: int, duration: float = QUARTER,
                  velocity: int = MF) -> "Note":
        """Create a Note from a MIDI note number.

        Args:
            midi_number: MIDI note number (0-127)
            duration: Duration in quarter notes
            velocity: MIDI velocity

        Returns:
            A new Note instance
        """
        pass
```

#### Rest Class

```python
class Rest:
    """Represents a musical rest (silence) with a duration.

    Attributes:
        duration (float): Duration in quarter notes
    """

    def __init__(self, duration: float = QUARTER):
        """Initialize a Rest.

        Args:
            duration: Duration in quarter notes (default: QUARTER)
        """
        pass  # TODO: Implement

    def __repr__(self) -> str:
        """Return string representation (e.g., 'Rest(1.0)')."""
        pass

    def __eq__(self, other) -> bool:
        """Check equality based on duration."""
        pass
```

### Task 3: Implement Chord Class

Create `src/musicgen/core/chord.py` with the following:

#### Chord Quality Constants

```python
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
    MAJOR: [0, 4, 7],                    # root, M3, P5
    MINOR: [0, 3, 7],                    # root, m3, P5
    DIMINISHED: [0, 3, 6],               # root, m3, d5
    AUGMENTED: [0, 4, 8],                # root, M3, A5
    MAJOR_SEVENTH: [0, 4, 7, 11],        # root, M3, P5, M7
    MINOR_SEVENTH: [0, 3, 7, 10],        # root, m3, P5, m7
    DOMINANT_SEVENTH: [0, 4, 7, 10],     # root, M3, P5, m7
    DIMINISHED_SEVENTH: [0, 3, 6, 9],    # root, m3, d5, d7
    HALF_DIMINISHED: [0, 3, 6, 10],      # root, m3, d5, m7
}
```

#### Chord Class

```python
class Chord:
    """Represents a musical chord as a collection of Notes.

    Attributes:
        root_name (str): The root note name (C, D, E, etc.)
        quality (str): The chord quality
        root_octave (int): Octave of the root note
        inversion (int): Inversion number (0=root, 1=first, 2=second)
        duration (float): Duration in quarter notes
        notes (list[Note]): List of Note objects in the chord
    """

    def __init__(self, root: str, quality: str = MAJOR, root_octave: int = 4,
                 inversion: int = 0, duration: float = QUARTER):
        """Initialize a Chord.

        Args:
            root: Root note name (e.g., "C", "A#", "Bb")
            quality: Chord quality (default: MAJOR)
            root_octave: Octave of the root (default: 4)
            inversion: Inversion number 0-2 (default: 0)
            duration: Duration in quarter notes (default: QUARTER)

        Raises:
            ValueError: If root or quality is invalid
        """
        pass  # TODO: Implement

    @property
    def root_name(self) -> str:
        """Return the root note name (without octave)."""
        pass

    @property
    def notes(self) -> list[Note]:
        """Return list of Note objects in the chord (sorted by pitch)."""
        pass

    @property
    def inversion(self) -> int:
        """Return the current inversion number."""
        pass

    @inversion.setter
    def inversion(self, value: int) -> None:
        """Set the inversion and reorder notes accordingly."""
        pass

    @property
    def quality(self) -> str:
        """Return the chord quality."""
        pass

    @property
    def duration(self) -> float:
        """Return the chord duration."""
        pass

    @duration.setter
    def duration(self, value: float) -> None:
        """Set the chord duration."""
        pass

    @property
    def root_octave(self) -> int:
        """Return the root octave."""
        pass

    def invert(self, inversion: int) -> "Chord":
        """Return a new Chord with the specified inversion.

        Args:
            inversion: Inversion number (0=root position, 1=first, etc.)

        Returns:
            A new Chord instance
        """
        pass

    def transpose(self, semitones: int) -> "Chord":
        """Return a new Chord transposed by the given semitones.

        Args:
            semitones: Number of semitones to transpose

        Returns:
            A new Chord instance
        """
        pass

    def get_inversion(self, bass_note: str) -> int:
        """Return the inversion that puts the specified note on bottom.

        Args:
            bass_note: Note name to use as bass

        Returns:
            Inversion number (0-2 for triads)
        """
        pass

    def contains(self, note: Note) -> bool:
        """Check if the chord contains the given note (any octave).

        Args:
            note: Note to check

        Returns:
            True if note is in chord
        """
        pass

    def __repr__(self) -> str:
        """Return string representation (e.g., 'Chord(C, major, 0)')."""
        pass

    def __eq__(self, other) -> bool:
        """Check equality based on root and quality."""
        pass

    def __hash__(self) -> int:
        """Make Chord hashable."""
        pass

    @classmethod
    def from_notes(cls, notes: list[Note], quality: str = None) -> "Chord":
        """Create a Chord from a list of Notes.

        Determines root and quality from the notes if not specified.

        Args:
            notes: List of Note objects
            quality: Optional quality hint

        Returns:
            A new Chord instance
        """
        pass
```

### Task 4: Package Initialization Files

#### `src/musicgen/__init__.py`

```python
"""Music Generation Library - Rule-based orchestral music composition.

This library generates orchestral music using traditional music theory
principles including scales, chords, progressions, voice leading, and
musical forms.
"""

__version__ = "0.1.0"

# Core exports
from musicgen.core.note import Note, Rest
from musicgen.core.note import (
    WHOLE, HALF, QUARTER, EIGHTH, SIXTEENTH,
    DOTTED_HALF, DOTTED_QUARTER, DOTTED_EIGHTH,
    TRIPLET_HALF, TRIPLET_QUARTER, TRIPLET_EIGHTH,
    PP, P, MP, MF, F, FF,
)
from musicgen.core.chord import Chord
from musicgen.core.chord import (
    MAJOR, MINOR, DIMINISHED, AUGMENTED,
    MAJOR_SEVENTH, MINOR_SEVENTH, DOMINANT_SEVENTH,
    DIMINISHED_SEVENTH, HALF_DIMINISHED,
)

__all__ = [
    # Version
    "__version__",
    # Core classes
    "Note", "Rest", "Chord",
    # Durations
    "WHOLE", "HALF", "QUARTER", "EIGHTH", "SIXTEENTH",
    "DOTTED_HALF", "DOTTED_QUARTER", "DOTTED_EIGHTH",
    "TRIPLET_HALF", "TRIPLET_QUARTER", "TRIPLET_EIGHTH",
    # Dynamics
    "PP", "P", "MP", "MF", "F", "FF",
    # Chord qualities
    "MAJOR", "MINOR", "DIMINISHED", "AUGMENTED",
    "MAJOR_SEVENTH", "MINOR_SEVENTH", "DOMINANT_SEVENTH",
    "DIMINISHED_SEVENTH", "HALF_DIMINISHED",
]
```

#### `src/musicgen/core/__init__.py`

```python
"""Core music data structures.

This module provides the fundamental classes for representing musical
elements: Note, Rest, and Chord, along with duration and dynamic constants.
"""

from musicgen.core.note import Note, Rest
from musicgen.core.note import (
    WHOLE, HALF, QUARTER, EIGHTH, SIXTEENTH,
    DOTTED_HALF, DOTTED_QUARTER, DOTTED_EIGHTH,
    TRIPLET_HALF, TRIPLET_QUARTER, TRIPLET_EIGHTH,
    PP, P, MP, MF, F, FF,
)
from musicgen.core.chord import Chord
from musicgen.core.chord import (
    MAJOR, MINOR, DIMINISHED, AUGMENTED,
    MAJOR_SEVENTH, MINOR_SEVENTH, DOMINANT_SEVENTH,
    DIMINISHED_SEVENTH, HALF_DIMINISHED,
)

__all__ = [
    "Note", "Rest", "Chord",
    "WHOLE", "HALF", "QUARTER", "EIGHTH", "SIXTEENTH",
    "DOTTED_HALF", "DOTTED_QUARTER", "DOTTED_EIGHTH",
    "TRIPLET_HALF", "TRIPLET_QUARTER", "TRIPLET_EIGHTH",
    "PP", "P", "MP", "MF", "F", "FF",
    "MAJOR", "MINOR", "DIMINISHED", "AUGMENTED",
    "MAJOR_SEVENTH", "MINOR_SEVENTH", "DOMINANT_SEVENTH",
    "DIMINISHED_SEVENTH", "HALF_DIMINISHED",
]
```

### Task 5: Other __init__.py Files

Create empty `__init__.py` files for the other modules:

```python
"""Music theory module."""
# src/musicgen/theory/__init__.py

"""Composition module."""
# src/musicgen/composition/__init__.py

"""Orchestration module."""
# src/musicgen/orchestration/__init__.py

"""Input/output module."""
# src/musicgen/io/__init__.py

"""Configuration module."""
# src/musicgen/config/__init__.py
```

## Test Requirements

### `tests/test_note.py`

```python
"""Tests for Note and Rest classes."""

import pytest
from musicgen import Note, Rest, QUARTER, HALF, EIGHTH, MF, F, C4


class TestNoteCreation:
    """Test Note class initialization and basic properties."""

    def test_create_simple_note(self):
        note = Note("C4", QUARTER, velocity=90)
        assert note.name == "C"
        assert note.octave == 4
        assert note.duration == QUARTER
        assert note.velocity == 90
        assert note.accidental == ""

    def test_create_sharp_note(self):
        note = Note("C#4")
        assert note.name == "C"
        assert note.octave == 4
        assert note.accidental == "#"

    def test_create_flat_note(self):
        note = Note("Bb3")
        assert note.name == "B"
        assert note.octave == 3
        assert note.accidental == "b"

    def test_invalid_pitch_raises_error(self):
        with pytest.raises(ValueError):
            Note("H4")  # Invalid note name
        with pytest.raises(ValueError):
            Note("C")   # Missing octave

    def test_invalid_velocity_raises_error(self):
        with pytest.raises(ValueError):
            Note("C4", velocity=-1)
        with pytest.raises(ValueError):
            Note("C4", velocity=128)


class TestNoteMIDI:
    """Test MIDI note number conversions."""

    def test_midi_number_c4(self):
        assert Note("C4").midi_number == 60

    def test_midi_number_a4(self):
        assert Note("A4").midi_number == 69

    def test_midi_number_extreme_low(self):
        assert Note("C0").midi_number == 12

    def test_midi_number_extreme_high(self):
        assert Note("G9").midi_number == 127

    def test_from_midi(self):
        note = Note.from_midi(60)
        assert note.name == "C"
        assert note.octave == 4

    def test_from_midi_with_accidentals(self):
        note = Note.from_midi(61)  # C#4 / Db4
        assert note.name in ["C", "D"]
        assert note.octave == 4


class TestNoteFrequency:
    """Test frequency calculations."""

    def test_frequency_a4(self):
        assert abs(Note("A4").frequency - 440.0) < 0.01

    def test_frequency_c4(self):
        assert abs(Note("C4").frequency - 261.63) < 0.01

    def test_frequency_g4(self):
        assert abs(Note("G4").frequency - 392.00) < 0.01


class TestNotePitchClass:
    """Test pitch class property."""

    def test_pitch_class_c(self):
        assert Note("C4").pitch_class == 0
        assert Note("C5").pitch_class == 0

    def test_pitch_class_d_sharp(self):
        assert Note("D#4").pitch_class == 3

    def test_pitch_class_b_flat(self):
        assert Note("Bb4").pitch_class == 10


class TestNoteTranspose:
    """Test note transposition."""

    def test_transpose_up(self):
        note = Note("C4")
        transposed = note.transpose(2)
        assert transposed.name == "D"
        assert transposed.octave == 4

    def test_transpose_down(self):
        note = Note("C4")
        transposed = note.transpose(-2)
        assert transposed.name == "A"
        assert transposed.octave == 3

    def test_transpose_cross_octave(self):
        note = Note("B4")
        transposed = note.transpose(1)
        assert transposed.name == "C"
        assert transposed.octave == 5

    def test_transpose_preserves_duration(self):
        note = Note("C4", duration=HALF)
        transposed = note.transpose(3)
        assert transposed.duration == HALF


class TestNoteStringRepresentation:
    """Test string representations."""

    def test_to_pitch_string(self):
        assert Note("C4").to_pitch_string() == "C4"
        assert Note("C#4").to_pitch_string() == "C#4"
        assert Note("Bb3").to_pitch_string() == "Bb3"

    def test_repr(self):
        note = Note("C4", QUARTER)
        assert repr(note) == "Note(C4, 1.0)"


class TestNoteEquality:
    """Test Note equality and hashing."""

    def test_same_notes_equal(self):
        note1 = Note("C4", QUARTER, velocity=90)
        note2 = Note("C4", QUARTER, velocity=90)
        assert note1 == note2

    def test_different_duration_not_equal(self):
        note1 = Note("C4", QUARTER)
        note2 = Note("C4", HALF)
        # Notes are equal if pitch matches, regardless of duration
        # (adjust based on your implementation choice)

    def test_enharmonic_equal(self):
        # C# and Db should be considered equal or not based on preference
        # Implementation choice - test both ways
        c_sharp = Note("C#4")
        d_flat = Note("Db4")
        # These may or may not be equal depending on implementation

    def test_note_is_hashable(self):
        note = Note("C4")
        note_set = {note, Note("D4"), Note("C4")}
        assert len(note_set) == 2  # C4 and D4


class TestNoteArticulation:
    """Test note articulation properties."""

    def test_staccato(self):
        note = Note("C4", articulation=".")
        assert note.articulation == "."

    def test_accent(self):
        note = Note("C4", articulation=">")
        assert note.articulation == ">"

    def test_tenuto(self):
        note = Note("C4", articulation="-")
        assert note.articulation == "-"


class TestNoteTie:
    """Test note tie property."""

    def test_tied_note(self):
        note = Note("C4", tied=True)
        assert note.tied is True


class TestRest:
    """Test Rest class."""

    def test_create_rest(self):
        rest = Rest(QUARTER)
        assert rest.duration == QUARTER

    def test_rest_repr(self):
        rest = Rest(QUARTER)
        assert repr(rest) == "Rest(1.0)"

    def test_rest_equality(self):
        rest1 = Rest(QUARTER)
        rest2 = Rest(QUARTER)
        assert rest1 == rest2

    def test_rest_inequality(self):
        rest1 = Rest(QUARTER)
        rest2 = Rest(HALF)
        assert rest1 != rest2


class TestDurationConstants:
    """Test duration constant values."""

    def test_whole_note(self):
        from musicgen import WHOLE
        assert WHOLE == 4.0

    def test_half_note(self):
        from musicgen import HALF
        assert HALF == 2.0

    def test_quarter_note(self):
        from musicgen import QUARTER
        assert QUARTER == 1.0

    def test_eighth_note(self):
        from musicgen import EIGHTH
        assert EIGHTH == 0.5

    def test_dotted_values(self):
        from musicgen import DOTTED_HALF, DOTTED_QUARTER
        assert DOTTED_HALF == 3.0
        assert DOTTED_QUARTER == 1.5


class TestDynamicConstants:
    """Test dynamic constant values."""

    def test_pp(self):
        from musicgen import PP
        assert PP == 30

    def test_mf(self):
        from musicgen import MF
        assert MF == 90

    def test_ff(self):
        from musicgen import FF
        assert FF == 120
```

### `tests/test_chord.py`

```python
"""Tests for Chord class."""

import pytest
from musicgen import Chord, Note, MAJOR, MINOR, DIMINISHED, AUGMENTED
from musicgen import QUARTER


class TestChordCreation:
    """Test Chord class initialization."""

    def test_create_major_triad(self):
        chord = Chord("C", MAJOR)
        assert chord.root_name == "C"
        assert chord.quality == MAJOR
        assert len(chord.notes) == 3
        assert [n.name for n in chord.notes] == ["C", "E", "G"]

    def test_create_minor_triad(self):
        chord = Chord("C", MINOR)
        assert chord.quality == MINOR
        assert [n.name for n in chord.notes] == ["C", "D#", "G"]

    def test_create_diminished_triad(self):
        chord = Chord("C", DIMINISHED)
        assert chord.quality == DIMINISHED
        # C, Eb, Gb
        assert [n.to_pitch_string() for n in chord.notes] == ["C4", "D#4", "F#4"]

    def test_create_augmented_triad(self):
        chord = Chord("C", AUGMENTED)
        assert chord.quality == AUGMENTED
        # C, E, G#
        assert [n.to_pitch_string() for n in chord.notes] == ["C4", "E4", "G#4"]

    def test_chord_with_octave(self):
        chord = Chord("C", MAJOR, root_octave=5)
        assert chord.root_octave == 5
        assert chord.notes[0].octave == 5

    def test_chord_duration(self):
        chord = Chord("C", MAJOR, duration=QUARTER)
        assert chord.duration == QUARTER

    def test_invalid_root_raises_error(self):
        with pytest.raises(ValueError):
            Chord("H", MAJOR)

    def test_invalid_quality_raises_error(self):
        with pytest.raises(ValueError):
            Chord("C", "invalid_quality")


class TestChordInversions:
    """Test chord inversion functionality."""

    def test_root_position(self):
        chord = Chord("C", MAJOR, inversion=0)
        assert chord.inversion == 0
        # Root on bottom
        assert chord.notes[0].name == "C"

    def test_first_inversion(self):
        chord = Chord("C", MAJOR, inversion=1)
        assert chord.inversion == 1
        # Third on bottom (E)
        assert chord.notes[0].name == "E"

    def test_second_inversion(self):
        chord = Chord("C", MAJOR, inversion=2)
        assert chord.inversion == 2
        # Fifth on bottom (G)
        assert chord.notes[0].name == "G"

    def test_invert_method(self):
        chord = Chord("C", MAJOR)
        inverted = chord.invert(1)
        assert inverted.inversion == 1
        assert inverted.root_name == "C"
        assert inverted.notes[0].name == "E"

    def test_get_inversion_by_bass(self):
        chord = Chord("C", MAJOR)
        assert chord.get_inversion("C") == 0
        assert chord.get_inversion("E") == 1
        assert chord.get_inversion("G") == 2


class TestChordSevenths:
    """Test seventh chord creation."""

    def test_major_seventh(self):
        from musicgen import MAJOR_SEVENTH
        chord = Chord("C", MAJOR_SEVENTH)
        assert len(chord.notes) == 4
        # C, E, G, B
        assert [n.name for n in chord.notes] == ["C", "E", "G", "B"]

    def test_dominant_seventh(self):
        from musicgen import DOMINANT_SEVENTH
        chord = Chord("C", DOMINANT_SEVENTH)
        assert len(chord.notes) == 4
        # C, E, G, Bb
        assert [n.to_pitch_string() for n in chord.notes] == ["C4", "E4", "G4", "A#4"]

    def test_minor_seventh(self):
        from musicgen import MINOR_SEVENTH
        chord = Chord("C", MINOR_SEVENTH)
        assert len(chord.notes) == 4
        # C, Eb, G, Bb
        assert [n.to_pitch_string() for n in chord.notes] == ["C4", "D#4", "G4", "A#4"]


class TestChordTranspose:
    """Test chord transposition."""

    def test_transpose_up(self):
        chord = Chord("C", MAJOR)
        transposed = chord.transpose(2)
        assert transposed.root_name == "D"
        assert [n.name for n in transposed.notes] == ["D", "F#", "A"]

    def test_transpose_down(self):
        chord = Chord("C", MAJOR)
        transposed = chord.transpose(-3)
        assert transposed.root_name == "A"

    def test_transpose_preserves_quality(self):
        chord = Chord("C", MINOR)
        transposed = chord.transpose(4)
        assert transposed.quality == MINOR

    def test_transpose_preserves_inversion(self):
        chord = Chord("C", MAJOR, inversion=1)
        transposed = chord.transpose(2)
        assert transposed.inversion == 1


class TestChordContains:
    """Test chord note membership."""

    def test_contains_root(self):
        chord = Chord("C", MAJOR)
        assert chord.contains(Note("C4"))

    def test_contains_third(self):
        chord = Chord("C", MAJOR)
        assert chord.contains(Note("E4"))

    def test_contains_fifth(self):
        chord = Chord("C", MAJOR)
        assert chord.contains(Note("G4"))

    def test_contains_different_octave(self):
        chord = Chord("C", MAJOR, root_octave=4)
        # Should find C in any octave
        assert chord.contains(Note("C3"))
        assert chord.contains(Note("C5"))

    def test_does_not_contain_non_chord_tone(self):
        chord = Chord("C", MAJOR)
        assert not chord.contains(Note("D4"))


class TestChordEquality:
    """Test Chord equality and hashing."""

    def test_same_chords_equal(self):
        chord1 = Chord("C", MAJOR)
        chord2 = Chord("C", MAJOR)
        assert chord1 == chord2

    def test_different_root_not_equal(self):
        chord1 = Chord("C", MAJOR)
        chord2 = Chord("D", MAJOR)
        assert chord1 != chord2

    def test_different_quality_not_equal(self):
        chord1 = Chord("C", MAJOR)
        chord2 = Chord("C", MINOR)
        assert chord1 != chord2

    def test_chord_is_hashable(self):
        chord = Chord("C", MAJOR)
        chord_set = {chord, Chord("D", MAJOR), Chord("C", MAJOR)}
        assert len(chord_set) == 2


class TestChordFromNotes:
    """Test creating chords from note collections."""

    def test_from_notes_major(self):
        notes = [Note("C4"), Note("E4"), Note("G4")]
        chord = Chord.from_notes(notes)
        assert chord.root_name == "C"
        assert chord.quality == MAJOR

    def test_from_notes_minor(self):
        notes = [Note("C4"), Note("D#4"), Note("G4")]
        chord = Chord.from_notes(notes)
        assert chord.root_name == "C"
        assert chord.quality == MINOR


class TestChordRepresentation:
    """Test Chord string representations."""

    def test_repr_root_position(self):
        chord = Chord("C", MAJOR)
        assert repr(chord) == "Chord(C, major, 0)"

    def test_repr_first_inversion(self):
        chord = Chord("C", MAJOR, inversion=1)
        assert repr(chord) == "Chord(C, major, 1)"
```

### `tests/__init__.py`

Empty file to mark as a test package.

## Additional Files

### README.md (Basic placeholder)

```markdown
# Music Generation Library

A Python library for rule-based orchestral music generation using traditional music theory principles.

## Installation

```bash
pip install musicgen
```

## Quick Start

```python
from musicgen import Note, Chord, QUARTER, MAJOR

# Create a note
note = Note("C4", QUARTER, velocity=90)

# Create a chord
chord = Chord("C", MAJOR, root_octave=4)
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/musicgen --cov-report=html
```

## License

MIT
```

### .gitignore

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.mid
*.midi
*.wav
*.flac
*.mp3
*.pdf
*.ly
resources/soundfonts/*.sf2
!resources/soundfonts/.gitkeep
```

## Validation Criteria

After implementation, verify the following:

### 1. Package Structure
```bash
# Verify package is importable
python -c "import musicgen; print(musicgen.__version__)"

# Verify core classes are accessible
python -c "from musicgen import Note, Chord, Rest, QUARTER, MAJOR"
```

### 2. Note Class Validation
```python
from musicgen import Note, QUARTER, MF

# Test note creation
note = Note("C4", QUARTER, velocity=90)
assert note.name == "C"
assert note.octave == 4
assert note.midi_number == 60
assert abs(note.frequency - 261.63) < 0.01

# Test transposition
transposed = note.transpose(2)
assert transposed.name == "D"
assert transposed.octave == 4

# Test from MIDI
midi_note = Note.from_midi(69)
assert midi_note.name == "A"
assert midi_note.octave == 4
```

### 3. Chord Class Validation
```python
from musicgen import Chord, MAJOR, Note

# Test chord creation
chord = Chord("C", MAJOR, root_octave=4)
assert [n.name for n in chord.notes] == ["C", "E", "G"]
assert chord.inversion == 0

# Test inversion
inverted = chord.invert(1)
assert inverted.inversion == 1
assert inverted.notes[0].name == "E"

# Test contains
assert chord.contains(Note("C4"))
assert chord.contains(Note("G3"))  # Different octave
assert not chord.contains(Note("D4"))
```

### 4. Test Suite Validation
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/musicgen --cov-report=term-missing

# All tests should pass
# Coverage should be > 80% for the implemented modules
```

## Implementation Notes

1. **Note Pitch Parsing**: When parsing pitch strings like "C#4" or "Bb3", handle:
   - Note name (C, D, E, F, G, A, B)
   - Optional accidental (#, b, x, bb)
   - Octave number (0-9)

2. **MIDI Number Calculation**: MIDI note 0 is C-1. MIDI note 60 is C4.
   ```
   midi_number = (octave + 1) * 12 + pitch_class
   ```

3. **Frequency Calculation**: Use A4 = 440 Hz as reference
   ```
   frequency = 440 * 2^((midi_number - 69) / 12)
   ```

4. **Chord Note Ordering**: Notes in a chord should be sorted from lowest to highest pitch, taking into account the inversion.

5. **Enharmonic Handling**: Decide how to handle enharmonic equivalents (C# vs Db). The simplest approach is to accept both as input but standardize on one representation internally.

6. **Error Handling**: Raise `ValueError` with descriptive messages for invalid inputs.

## Dependencies to Install

Run the following to set up the development environment:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in development mode
pip install -e ".[dev]"

# Verify installation
python -c "import musicgen; print(musicgen.__version__)"
```

## Success Criteria

Step 1 is complete when:

1. All files are created in the correct locations
2. `pytest` runs without errors
3. All tests in `test_note.py` and `test_chord.py` pass
4. Test coverage is > 80% for core modules
5. The package can be imported: `import musicgen`
6. All validation criteria tests pass

## Next Steps

After completing this step, proceed to Step 2: "Music Theory Module - Scales and Keys" which will build upon these core data structures to implement scale generation and key signature management.
