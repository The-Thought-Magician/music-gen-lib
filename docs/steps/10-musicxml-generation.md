# Step 10: Sheet Music Generation (MusicXML)

## Overview

This is the tenth implementation step for the Music Generation Library. This step implements MusicXML export functionality, allowing compositions to be saved in a format that can be imported by notation software like MuseScore, Sibelius, and Finale.

MusicXML is the standard interchange format for musical notation. This implementation will use the `music21` library which provides robust MusicXML reading and writing capabilities.

## Context

You are building a Python library for generating orchestral instrumental music using traditional music theory principles (rule-based composition, NOT AI). The library will produce sheet music (MusicXML/LilyPond) and audio files (WAV/FLAC) from programmatic input based on mood/theme parameters.

This is Step 10 of 13 steps. At this point, you should have already implemented:
- Step 1: Core data structures (Note, Rest, Chord)
- Step 2: Scales and Keys
- Step 3: Chord Progressions
- Step 4: Voice Leading
- Step 5: Melody Generation
- Step 6: Orchestration (Instrument, Ensemble)
- Step 7: Musical Form Structures
- Step 8: MIDI File Generation
- Step 9: Audio Synthesis Pipeline

This step will implement `MusicXMLWriter` which exports compositions to MusicXML format using music21 as the backend library.

## Prerequisites

Before starting this step, ensure the following dependencies are installed:

```bash
# music21 should already be in pyproject.toml from Step 1
pip install music21>=9.0

# For testing MusicXML files
pip install lxml
```

## Project Structure

```
src/musicgen/
├── __init__.py
├── core/           (already implemented)
├── theory/         (already implemented)
├── composition/    (already implemented)
├── orchestration/  (already implemented)
├── io/
│   ├── __init__.py           (already exists)
│   ├── midi_writer.py        (already implemented in Step 8)
│   ├── audio_synthesizer.py  (already implemented in Step 9)
│   └── musicxml_writer.py    (NEW - to implement in this step)
└── config/         (may exist)
```

## Data Model Dependencies

This step depends on the following classes that should already be implemented:

### From `core/note.py`:
```python
class Note:
    """Represents a musical note with pitch, duration, and attributes."""
    @property
    def name(self) -> str: ...
    @property
    def octave(self) -> int: ...
    @property
    def midi_number(self) -> int: ...
    @property
    def duration(self) -> float: ...
    @property
    def velocity(self) -> int: ...
    @property
    def accidental(self) -> str: ...
    @property
    def tied(self) -> bool: ...
    @property
    def articulation(self) -> str: ...

class Rest:
    """Represents a musical rest."""
    @property
    def duration(self) -> float: ...
```

### From `core/chord.py`:
```python
class Chord:
    """Represents a musical chord."""
    @property
    def notes(self) -> list[Note]: ...
    @property
    def duration(self) -> float: ...
```

### From `orchestration/instruments.py`:
```python
class Instrument:
    """Represents a musical instrument."""
    @property
    def name(self) -> str: ...
    @property
    def midi_program(self) -> int: ...
    @property
    def transposition(self) -> int: ...
    @property
    def clef(self) -> str: ...

class Part:
    """A collection of notes/rests for a single instrument."""
    @property
    def instrument(self) -> Instrument: ...
    @property
    def notes(self) -> list[Note | Rest]: ...
    @property
    def name(self) -> str: ...

class Score:
    """A complete musical composition with multiple parts."""
    @property
    def parts(self) -> list[Part]: ...
    @property
    def title(self) -> str: ...
    @property
    def composer(self) -> str: ...
    @property
    def tempo(self) -> int: ...
    @property
    def time_signature(self) -> str: ...
    @property
    def key_signature(self) -> str: ...
```

## Implementation Tasks

### Task 1: Create the MusicXMLWriter Module

Create `src/musicgen/io/musicxml_writer.py` with the following structure:

```python
"""MusicXML file writer using music21.

This module provides functionality to export musicgen compositions to MusicXML
format, which can be imported by notation software like MuseScore, Sibelius,
and Finale.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import TYPE_CHECKING, Optional

import music21 as m21

from musicgen.core.note import Note, Rest
from musicgen.core.chord import Chord

if TYPE_CHECKING:
    from musicgen.orchestration.ensemble import Part, Score, Instrument


class MusicXMLWriter:
    """Writes musicgen compositions to MusicXML format.

    This class converts musicgen Score, Part, Note, and Rest objects to
    music21 objects and exports them to MusicXML files.

    Attributes:
        score: The musicgen Score to export
    """

    # Mapping of musicgen instrument names to music21 instruments
    INSTRUMENT_MAP = {
        # Strings
        "violin": m21.instrument.Violin,
        "viola": m21.instrument.Viola,
        "cello": m21.instrument.Violoncello,
        "double_bass": m21.instrument.Contrabass,
        "harp": m21.instrument.Harp,

        # Woodwinds
        "flute": m21.instrument.Flute,
        "piccolo": m21.instrument.Piccolo,
        "oboe": m21.instrument.Oboe,
        "clarinet": m21.instrument.Clarinet,
        "bassoon": m21.instrument.Bassoon,

        # Brass
        "trumpet": m21.instrument.Trumpet,
        "french_horn": m21.instrument.Horn,
        "trombone": m21.instrument.Trombone,
        "tuba": m21.instrument.Tuba,

        # Percussion
        "timpani": m21.instrument.Timpani,
        "xylophone": m21.instrument.Xylophone,
        "marimba": m21.instrument.Marimba,

        # Keyboards
        "piano": m21.instrument.Piano,
        "organ": m21.instrument.Organ,
    }

    # Mapping of clef names to music21 clefs
    CLEF_MAP = {
        "treble": m21.clef.TrebleClef,
        "bass": m21.clef.BassClef,
        "alto": m21.clef.AltoClef,
        "tenor": m21.clef.TenorClef,
        "treble_8vb": m21.clef.BassClef,  # For instruments sounding 8vb
    }

    def __init__(self, score: Score):
        """Initialize the writer with a musicgen Score.

        Args:
            score: The Score object to export

        Raises:
            ValueError: If score is None or invalid
        """
        pass

    def to_music21(self) -> m21.stream.Score:
        """Convert the musicgen Score to a music21 Score.

        Returns:
            A music21.stream.Score object

        Example:
            >>> writer = MusicXMLWriter(score)
            >>> m21_score = writer.to_music21()
            >>> m21_score.show()  # Opens in music notation viewer
        """
        pass

    def _add_metadata(self, m21_score: m21.stream.Score) -> None:
        """Add metadata to the music21 score.

        Args:
            m21_score: The music21 score to add metadata to
        """
        pass

    def _convert_part(self, part: Part) -> m21.stream.Part:
        """Convert a musicgen Part to a music21 Part.

        Args:
            part: The musicgen Part to convert

        Returns:
            A music21.stream.Part object
        """
        pass

    def _get_instrument(self, instrument: Instrument) -> m21.instrument.Instrument:
        """Get or create a music21 Instrument object.

        Args:
            instrument: The musicgen Instrument

        Returns:
            A music21.instrument.Instrument object
        """
        pass

    def _get_clef(self, instrument: Instrument) -> m21.clef.Clef:
        """Get the appropriate clef for an instrument.

        Args:
            instrument: The musicgen Instrument

        Returns:
            A music21.clef.Clef object
        """
        pass

    def _convert_note(self, note: Note) -> m21.note.Note | m21.note.Rest:
        """Convert a musicgen Note or Rest to a music21 Note.

        Args:
            note: The musicgen Note or Rest

        Returns:
            A music21.note.Note or music21.note.Rest
        """
        pass

    def _convert_duration(self, duration: float) -> m21.duration.Duration:
        """Convert a duration value to music21 Duration.

        Args:
            duration: Duration in quarter notes

        Returns:
            A music21.duration.Duration object

        Note:
            Handles dotted notes and complex rhythms. Converts fractional
            durations to music21's type representation (whole, half, quarter, etc.)
        """
        pass

    def _add_articulations(self, m21_note: m21.note.Note, note: Note) -> None:
        """Add articulations to a music21 note.

        Args:
            m21_note: The music21 note to add articulations to
            note: The musicgen Note with articulation information
        """
        pass

    def _add_dynamics(self, m21_note: m21.note.Note, note: Note) -> None:
        """Add dynamic markings to a music21 note.

        Args:
            m21_note: The music21 note to add dynamics to
            note: The musicgen Note with velocity information
        """
        pass

    def _convert_key_signature(self, key: str) -> m21.key.KeySignature:
        """Convert a key string to music21 KeySignature.

        Args:
            key: Key string (e.g., "C", "F#", "Bb")

        Returns:
            A music21.key.KeySignature object
        """
        pass

    def _convert_time_signature(self, ts: str) -> m21.meter.TimeSignature:
        """Convert a time signature string to music21 TimeSignature.

        Args:
            ts: Time signature string (e.g., "4/4", "3/4", "6/8")

        Returns:
            A m21.meter.TimeSignature object
        """
        pass

    def write(self, filepath: str | Path,
              compress: bool = False) -> Path:
        """Write the Score to a MusicXML file.

        Args:
            filepath: Output file path (.musicxml or .xml extension recommended)
            compress: If True, writes compressed .mxl file

        Returns:
            The path to the written file

        Raises:
            IOError: If file cannot be written
            ValueError: If score has no parts

        Example:
            >>> writer = MusicXMLWriter(score)
            >>> writer.write("output.musicxml")
            >>> writer.write("output.mxl", compress=True)
        """
        pass

    def write_musicxml(self, filepath: str | Path) -> Path:
        """Write uncompressed MusicXML file.

        Args:
            filepath: Output file path

        Returns:
            The path to the written file
        """
        pass

    def write_mxl(self, filepath: str | Path) -> Path:
        """Write compressed MusicXML file (.mxl).

        Args:
            filepath: Output file path (will use .mxl extension)

        Returns:
            The path to the written file
        """
        pass

    @staticmethod
    def validate_musicxml(filepath: str | Path) -> bool:
        """Validate that a MusicXML file is well-formed.

        Args:
            filepath: Path to the MusicXML file to validate

        Returns:
            True if valid, False otherwise

        Example:
            >>> if MusicXMLWriter.validate_musicxml("output.musicxml"):
            ...     print("Valid MusicXML file!")
        """
        pass

    @staticmethod
    def get_part_excerpt(score: Score, part_names: list[str],
                         output_path: str | Path) -> Path:
        """Extract specific parts and save to a new MusicXML file.

        Useful for creating individual part files for performers.

        Args:
            score: The full Score
            part_names: List of part names to extract
            output_path: Where to save the excerpt

        Returns:
            Path to the excerpt file

        Example:
            >>> # Extract just the violin part
            >>> MusicXMLWriter.get_part_excerpt(
            ...     full_score,
            ...     ["violin"],
            ...     "violin_part.musicxml"
            ... )
        """
        pass


class MusicXMLReader:
    """Reads MusicXML files and converts to musicgen objects.

    This is the inverse operation of MusicXMLWriter, useful for importing
    existing sheet music into the musicgen system.
    """

    @staticmethod
    def read(filepath: str | Path) -> m21.stream.Score:
        """Read a MusicXML file into a music21 Score.

        Args:
            filepath: Path to the MusicXML file

        Returns:
            A music21.stream.Score object

        Example:
            >>> m21_score = MusicXMLReader.read("input.musicxml")
        """
        pass

    @staticmethod
    def to_musicgen(m21_score: m21.stream.Score) -> Score:
        """Convert a music21 Score to a musicgen Score.

        Args:
            m21_score: The music21 Score to convert

        Returns:
            A musicgen Score object

        Example:
            >>> m21_score = MusicXMLReader.read("input.musicxml")
            >>> score = MusicXMLReader.to_musicgen(m21_score)
        """
        pass
```

### Task 2: Update io/__init__.py

Update `src/musicgen/io/__init__.py` to export the new MusicXMLWriter:

```python
"""Input/output module for music generation library.

This module provides functionality for exporting compositions to various
formats including MIDI, audio (WAV/FLAC), and sheet music (MusicXML).
"""

from musicgen.io.midi_writer import MIDIWriter
from musicgen.io.audio_synthesizer import AudioSynthesizer
from musicgen.io.musicxml_writer import MusicXMLWriter, MusicXMLReader

__all__ = [
    "MIDIWriter",
    "AudioSynthesizer",
    "MusicXMLWriter",
    "MusicXMLReader",
]
```

### Task 3: Implement Helper Functions

Create the following helper functions in `musicxml_writer.py`:

```python
def note_to_music21(note: Note) -> m21.note.Note:
    """Convert a musicgen Note directly to music21 without context.

    This is a convenience function for single note conversion.

    Args:
        note: The musicgen Note to convert

    Returns:
        A music21.note.Note object

    Example:
        >>> from musicgen import Note
        >>> n = Note("C4", duration=1.0)
        >>> m21_note = note_to_music21(n)
    """
    pass


def rest_to_music21(rest: Rest) -> m21.note.Rest:
    """Convert a musicgen Rest directly to music21 without context.

    Args:
        rest: The musicgen Rest to convert

    Returns:
        A music21.note.Rest object
    """
    pass


def chord_to_music21(chord: Chord) -> m21.chord.Chord:
    """Convert a musicgen Chord to a music21 Chord.

    Args:
        chord: The musicgen Chord to convert

    Returns:
        A music21.chord.Chord object

    Example:
        >>> from musicgen import Chord, MAJOR
        >>> c = Chord("C", MAJOR)
        >>> m21_chord = chord_to_music21(c)
    """
    pass
```

## Implementation Details

### Duration Conversion Logic

MusicXML (and music21) uses symbolic duration types rather than pure numeric values. Implement the following conversion:

```python
def _convert_duration(self, duration: float) -> m21.duration.Duration:
    """Convert quarter-note duration to music21 Duration.

    Mapping table:
    - 4.0  -> whole
    - 3.0  -> dotted half
    - 2.5  -> half dotted eighth (complex)
    - 2.0  -> half
    - 1.5  -> dotted quarter
    - 1.0  -> quarter
    - 0.75 -> dotted eighth
    - 0.5  -> eighth
    - 0.25 -> sixteenth
    - 0.125 -> thirty-second

    For non-standard durations, use Tuplet or create complex durations.
    """
    # Standard duration types
    duration_map = {
        4.0: ('whole', 1),
        2.0: ('half', 1),
        1.0: ('quarter', 1),
        0.5: ('eighth', 1),
        0.25: ('sixteenth', 1),
        0.125: ('32nd', 1),
    }

    # Check for exact matches first
    if duration in duration_map:
        type_, dots = duration_map[duration]
        d = m21.duration.Duration()
        d.type = type_
        if dots > 1:
            d.dots = dots - 1
        return d

    # Check for dotted values
    dotted_map = {
        3.0: ('half', 1),      # dotted half
        1.5: ('quarter', 1),   # dotted quarter
        0.75: ('eighth', 1),   # dotted eighth
    }

    if duration in dotted_map:
        type_, dots = dotted_map[duration]
        d = m21.duration.Duration()
        d.type = type_
        d.dots = dots
        return d

    # For complex durations, calculate from quarter length
    d = m21.duration.Duration()
    d.quarterLength = duration
    return d
```

### Dynamic to Velocity Mapping

Implement conversion from MIDI velocity to music21 dynamic markings:

```python
def _velocity_to_dynamic(velocity: int) -> str | None:
    """Convert MIDI velocity to dynamic marking.

    Mapping:
    - 0-20: niente (silence)
    - 21-40: pp (pianissimo)
    - 41-60: p (piano)
    - 61-80: mp (mezzo-piano)
    - 81-100: mf (mezzo-forte)
    - 101-115: f (forte)
    - 116-127: ff (fortissimo)

    Args:
        velocity: MIDI velocity value (0-127)

    Returns:
        Dynamic marking string or None
    """
    if velocity <= 20:
        return 'niente'
    elif velocity <= 40:
        return 'pp'
    elif velocity <= 60:
        return 'p'
    elif velocity <= 80:
        return 'mp'
    elif velocity <= 100:
        return 'mf'
    elif velocity <= 115:
        return 'f'
    else:
        return 'ff'
```

### Articulation Markings

Map musicgen articulation symbols to music21 articulation objects:

```python
ARTICULATION_MAP = {
    '.': m21.articulations.Staccato,      # Staccato
    '>': m21.articulations.Accent,        # Accent
    '-': m21.articulations.Tenuto,        # Tenuto
    '^': m21.articulations.Marcato,       # Marcato
}

def _add_articulations(self, m21_note: m21.note.Note, note: Note) -> None:
    """Add articulations based on note.articulation property."""
    if note.articulation and note.articulation in ARTICULATION_MAP:
        articulation_class = ARTICULATION_MAP[note.articulation]
        m21_note.articulations.append(articulation_class())
```

### Key Signature Conversion

```python
def _convert_key_signature(self, key: str) -> m21.key.KeySignature:
    """Convert key string to music21 KeySignature.

    Args:
        key: Key like "C", "F#", "Bb", "Am", "G#m"

    Returns:
        music21 KeySignature object

    The key sharps/flats calculation:
    - C: 0, G: 1, D: 2, A: 3, E: 4, B: 5, F#: 6, C#: 7
    - F: -1, Bb: -2, Eb: -3, Ab: -4, Db: -5, Gb: -6, Cb: -7
    """
    # Parse the key string
    is_minor = key.lower().endswith('m')
    root = key[:-1].lower() if is_minor else key.lower()

    # Circle of fifths sharps
    sharp_order = ['f', 'c', 'g', 'd', 'a', 'e', 'b']
    flat_order = ['b', 'e', 'a', 'd', 'g', 'c', 'f']

    # Major key sharps/flats
    major_sharps = {'c': 0, 'g': 1, 'd': 2, 'a': 3, 'e': 4, 'b': 5, 'f#': 6, 'c#': 7}
    major_flats = {'f': -1, 'bb': -2, 'eb': -3, 'ab': -4, 'db': -5, 'gb': -6, 'cb': -7}

    # Get sharps/flats for major
    if root in major_sharps:
        sharps = major_sharps[root]
    elif root in major_flats:
        sharps = major_flats[root]
    else:
        sharps = 0

    # Adjust for minor (relative minor is 3 semitones below major)
    if is_minor:
        sharps -= 3

    return m21.key.KeySignature(sharps)
```

## Test Requirements

### `tests/test_musicxml_writer.py`

```python
"""Tests for MusicXMLWriter module."""

import pytest
import xml.etree.ElementTree as ET
from pathlib import Path

import music21 as m21

from musicgen import Note, Rest, Chord, QUARTER, HALF, WHOLE, EIGHTH, MAJOR, MINOR, MF, F
from musicgen.io import MusicXMLWriter, MusicXMLReader
from musicgen.orchestration import Instrument, Part, Score


class TestMusicXMLWriterInit:
    """Test MusicXMLWriter initialization."""

    def test_init_with_valid_score(self, sample_score):
        """Test initialization with a valid score."""
        writer = MusicXMLWriter(sample_score)
        assert writer.score == sample_score

    def test_init_with_none_raises_error(self):
        """Test that None raises ValueError."""
        with pytest.raises(ValueError):
            MusicXMLWriter(None)


class TestDurationConversion:
    """Test duration conversion to music21."""

    def test_convert_whole_note(self, sample_score):
        """Test whole note conversion."""
        writer = MusicXMLWriter(sample_score)
        d = writer._convert_duration(WHOLE)
        assert d.type == 'whole'
        assert d.dots == 0

    def test_convert_half_note(self, sample_score):
        """Test half note conversion."""
        writer = MusicXMLWriter(sample_score)
        d = writer._convert_duration(HALF)
        assert d.type == 'half'
        assert d.dots == 0

    def test_convert_quarter_note(self, sample_score):
        """Test quarter note conversion."""
        writer = MusicXMLWriter(sample_score)
        d = writer._convert_duration(QUARTER)
        assert d.type == 'quarter'

    def test_convert_eighth_note(self, sample_score):
        """Test eighth note conversion."""
        writer = MusicXMLWriter(sample_score)
        d = writer._convert_duration(EIGHTH)
        assert d.type == 'eighth'

    def test_convert_dotted_half(self, sample_score):
        """Test dotted half note (3.0 quarter notes)."""
        writer = MusicXMLWriter(sample_score)
        d = writer._convert_duration(3.0)
        assert d.type == 'half'
        assert d.dots == 1

    def test_convert_dotted_quarter(self, sample_score):
        """Test dotted quarter note (1.5 quarter notes)."""
        writer = MusicXMLWriter(sample_score)
        d = writer._convert_duration(1.5)
        assert d.type == 'quarter'
        assert d.dots == 1

    def test_convert_complex_duration(self, sample_score):
        """Test non-standard duration."""
        writer = MusicXMLWriter(sample_score)
        d = writer._convert_duration(0.75)
        assert d.quarterLength == 0.75


class TestNoteConversion:
    """Test individual note conversion."""

    def test_convert_simple_note(self, sample_score):
        """Test converting a simple C4 quarter note."""
        writer = MusicXMLWriter(sample_score)
        note = Note("C4", QUARTER, velocity=90)
        m21_note = writer._convert_note(note)

        assert isinstance(m21_note, m21.note.Note)
        assert m21_note.pitch.name == 'C'
        assert m21_note.pitch.octave == 4
        assert m21_note.duration.quarterLength == QUARTER

    def test_convert_sharp_note(self, sample_score):
        """Test converting a sharp note (F#4)."""
        writer = MusicXMLWriter(sample_score)
        note = Note("F#4", QUARTER)
        m21_note = writer._convert_note(note)

        assert m21_note.pitch.name == 'F'
        assert m21_note.pitch.accidental.alter == 1

    def test_convert_flat_note(self, sample_score):
        """Test converting a flat note (Bb3)."""
        writer = MusicXMLWriter(sample_score)
        note = Note("Bb3", QUARTER)
        m21_note = writer._convert_note(note)

        assert m21_note.pitch.name == 'B'
        assert m21_note.pitch.accidental.alter == -1

    def test_convert_rest(self, sample_score):
        """Test converting a rest."""
        writer = MusicXMLWriter(sample_score)
        rest = Rest(QUARTER)
        m21_rest = writer._convert_note(rest)

        assert isinstance(m21_rest, m21.note.Rest)
        assert m21_rest.duration.quarterLength == QUARTER

    def test_convert_staccato_note(self, sample_score):
        """Test converting a note with staccato articulation."""
        writer = MusicXMLWriter(sample_score)
        note = Note("C4", QUARTER, articulation=".")
        m21_note = writer._convert_note(note)

        assert len(m21_note.articulations) > 0
        assert any(isinstance(a, m21.articulations.Staccato)
                   for a in m21_note.articulations)

    def test_convert_accented_note(self, sample_score):
        """Test converting a note with accent."""
        writer = MusicXMLWriter(sample_score)
        note = Note("C4", QUARTER, articulation=">")
        m21_note = writer._convert_note(note)

        assert any(isinstance(a, m21.articulations.Accent)
                   for a in m21_note.articulations)

    def test_convert_tied_note(self, sample_score):
        """Test converting a tied note."""
        writer = MusicXMLWriter(sample_score)
        note = Note("C4", QUARTER, tied=True)
        m21_note = writer._convert_note(note)

        # music21 ties are handled differently - check for tie attribute
        assert m21_note.tie is not None


class TestKeySignatureConversion:
    """Test key signature conversion."""

    def test_convert_c_major(self, sample_score):
        """Test C major (no sharps/flats)."""
        writer = MusicXMLWriter(sample_score)
        ks = writer._convert_key_signature("C")
        assert ks.sharps == 0

    def test_convert_g_major(self, sample_score):
        """Test G major (1 sharp)."""
        writer = MusicXMLWriter(sample_score)
        ks = writer._convert_key_signature("G")
        assert ks.sharps == 1

    def test_convert_f_major(self, sample_score):
        """Test F major (1 flat)."""
        writer = MusicXMLWriter(sample_score)
        ks = writer._convert_key_signature("F")
        assert ks.sharps == -1

    def test_convert_a_minor(self, sample_score):
        """Test A minor (relative minor of C, no sharps/flats)."""
        writer = MusicXMLWriter(sample_score)
        ks = writer._convert_key_signature("Am")
        # A minor has no sharps/flats
        assert ks.sharps == 0

    def test_convert_e_minor(self, sample_score):
        """Test E minor (1 sharp)."""
        writer = MusicXMLWriter(sample_score)
        ks = writer._convert_key_signature("Em")
        assert ks.sharps == 1


class TestTimeSignatureConversion:
    """Test time signature conversion."""

    def test_convert_4_4(self, sample_score):
        """Test 4/4 time signature."""
        writer = MusicXMLWriter(sample_score)
        ts = writer._convert_time_signature("4/4")
        assert ts.numerator == 4
        assert ts.denominator == 4

    def test_convert_3_4(self, sample_score):
        """Test 3/4 time signature."""
        writer = MusicXMLWriter(sample_score)
        ts = writer._convert_time_signature("3/4")
        assert ts.numerator == 3
        assert ts.denominator == 4

    def test_convert_6_8(self, sample_score):
        """Test 6/8 time signature."""
        writer = MusicXMLWriter(sample_score)
        ts = writer._convert_time_signature("6/8")
        assert ts.numerator == 6
        assert ts.denominator == 8


class TestMusic21ScoreCreation:
    """Test conversion to music21 Score."""

    def test_to_music21_creates_score(self, sample_score):
        """Test that to_music21 returns a music21 Score."""
        writer = MusicXMLWriter(sample_score)
        m21_score = writer.to_music21()

        assert isinstance(m21_score, m21.stream.Score)

    def test_to_music21_has_correct_parts(self, sample_score):
        """Test that converted score has correct number of parts."""
        writer = MusicXMLWriter(sample_score)
        m21_score = writer.to_music21()

        assert len(m21_score.parts) == len(sample_score.parts)

    def test_to_music21_preserves_title(self, sample_score):
        """Test that title is preserved."""
        sample_score.title = "Test Composition"
        writer = MusicXMLWriter(sample_score)
        m21_score = writer.to_music21()

        assert m21_score.metadata.title == "Test Composition"

    def test_to_music21_preserves_tempo(self, sample_score):
        """Test that tempo is preserved."""
        sample_score.tempo = 120
        writer = MusicXMLWriter(sample_score)
        m21_score = writer.to_music21()

        # Check for metronome mark
        mm = m21_score.flatten().getElementsByClass(m21.tempo.MetronomeMark)
        assert len(mm) > 0
        assert mm[0].number == 120


class TestMusicXMLFileWriting:
    """Test writing MusicXML files."""

    def test_write_musicxml_file(self, sample_score, tmp_path):
        """Test writing a basic MusicXML file."""
        writer = MusicXMLWriter(sample_score)
        output_path = tmp_path / "output.musicxml"

        result = writer.write_musicxml(output_path)

        assert result == output_path
        assert output_path.exists()

    def test_write_creates_valid_xml(self, sample_score, tmp_path):
        """Test that written file is valid XML."""
        writer = MusicXMLWriter(sample_score)
        output_path = tmp_path / "output.musicxml"

        writer.write_musicxml(output_path)

        # Should be parseable as XML
        tree = ET.parse(output_path)
        root = tree.getroot()

        # Check for MusicXML root element
        assert root.tag.endswith('score-partwise')

    def test_write_has_part_elements(self, sample_score, tmp_path):
        """Test that written file has part elements."""
        writer = MusicXMLWriter(sample_score)
        output_path = tmp_path / "output.musicxml"

        writer.write_musicxml(output_path)

        tree = ET.parse(output_path)
        root = tree.getroot()

        # MusicXML uses namespaces
        namespaces = {'musicxml': 'http://www.musicxml.org/2008/mnmdl'}
        parts = root.findall('.//musicxml:part', namespaces)

        # At least one part should exist
        assert len(parts) > 0

    def test_write_has_measure_elements(self, sample_score, tmp_path):
        """Test that written file has measure elements."""
        writer = MusicXMLWriter(sample_score)
        output_path = tmp_path / "output.musicxml"

        writer.write_musicxml(output_path)

        tree = ET.parse(output_path)
        root = tree.getroot()

        # Look for measure elements
        measures = root.findall('.//measure')
        assert len(measures) > 0

    def test_validate_musicxml_valid_file(self, sample_score, tmp_path):
        """Test validation of a valid MusicXML file."""
        writer = MusicXMLWriter(sample_score)
        output_path = tmp_path / "output.musicxml"

        writer.write_musicxml(output_path)

        assert MusicXMLWriter.validate_musicxml(output_path) is True

    def test_validate_musicxml_invalid_file(self, tmp_path):
        """Test validation rejects invalid file."""
        invalid_path = tmp_path / "invalid.xml"

        # Write invalid content
        invalid_path.write_text("not valid xml")

        assert MusicXMLWriter.validate_musicxml(invalid_path) is False


class TestMusicXMLReading:
    """Test reading MusicXML files back."""

    def test_read_musicxml_file(self, sample_score, tmp_path):
        """Test reading a MusicXML file back."""
        # Write first
        writer = MusicXMLWriter(sample_score)
        output_path = tmp_path / "output.musicxml"
        writer.write_musicxml(output_path)

        # Read back
        m21_score = MusicXMLReader.read(output_path)

        assert isinstance(m21_score, m21.stream.Score)
        assert len(m21_score.parts) > 0


class TestPartExtraction:
    """Test extracting individual parts."""

    def test_extract_single_part(self, sample_score, tmp_path):
        """Test extracting a single part to a separate file."""
        output_path = tmp_path / "violin_part.musicxml"

        result = MusicXMLWriter.get_part_excerpt(
            sample_score,
            ["violin"],
            output_path
        )

        assert result == output_path
        assert output_path.exists()

    def test_extract_multiple_parts(self, sample_score, tmp_path):
        """Test extracting multiple parts."""
        output_path = tmp_path / "parts.musicxml"

        result = MusicXMLWriter.get_part_excerpt(
            sample_score,
            ["violin", "viola"],
            output_path
        )

        assert result.exists()


class TestInstrumentMapping:
    """Test instrument to music21 instrument mapping."""

    def test_violin_mapping(self):
        """Test Violin is correctly mapped."""
        assert 'violin' in MusicXMLWriter.INSTRUMENT_MAP
        assert MusicXMLWriter.INSTRUMENT_MAP['violin'] == m21.instrument.Violin

    def test_common_instruments_exist(self):
        """Test that common orchestral instruments are mapped."""
        required = ['violin', 'viola', 'cello', 'flute', 'oboe',
                    'clarinet', 'bassoon', 'trumpet', 'horn', 'trombone']
        for instrument in required:
            assert instrument in MusicXMLWriter.INSTRUMENT_MAP


# Fixtures
@pytest.fixture
def violin():
    """Create a violin instrument."""
    return Instrument(
        name="violin",
        midi_program=40,
        clef="treble"
    )


@pytest.fixture
def cello():
    """Create a cello instrument."""
    return Instrument(
        name="cello",
        midi_program=42,
        clef="bass"
    )


@pytest.fixture
def violin_part(violin):
    """Create a simple violin part."""
    notes = [
        Note("C4", QUARTER),
        Note("D4", QUARTER),
        Note("E4", QUARTER),
        Note("F4", QUARTER),
    ]
    return Part(instrument=violin, notes=notes, name="Violin")


@pytest.fixture
def cello_part(cello):
    """Create a simple cello part."""
    notes = [
        Note("C3", HALF),
        Note("G3", HALF),
    ]
    return Part(instrument=cello, notes=notes, name="Cello")


@pytest.fixture
def sample_score(violin_part, cello_part):
    """Create a sample score with violin and cello."""
    return Score(
        parts=[violin_part, cello_part],
        title="Test Piece",
        composer="Test Composer",
        tempo=100,
        time_signature="4/4",
        key_signature="C"
    )
```

## Example Script

### `examples/generate_sheet_music.py`

Create this example demonstrating the MusicXML export functionality:

```python
#!/usr/bin/env python3
"""Example: Generate sheet music in MusicXML format.

This script demonstrates creating a simple composition and exporting
it to MusicXML for use in notation software like MuseScore.
"""

from musicgen import Note, Rest, Chord, QUARTER, HALF, EIGHTH, MAJOR, MINOR, MF, F
from musicgen.orchestration import Instrument, Part, Score
from musicgen.theory import Scale, Progression
from musicgen.composition import Melody
from musicgen.io import MusicXMLWriter


def create_simple_melody():
    """Create a simple melody in C major."""
    return [
        Note("C4", QUARTER),
        Note("D4", QUARTER),
        Note("E4", QUARTER),
        Note("F4", QUARTER),
        Note("G4", HALF),
        Note("E4", QUARTER),
        Note("C4", QUARTER),
    ]


def create_harmony():
    """Create simple harmony chords."""
    return [
        Chord("C", MAJOR, root_octave=3, duration=HALF),
        Chord("G", MAJOR, root_octave=2, duration=HALF),
        Chord("C", MAJOR, root_octave=3, duration=QUARTER),
        Chord("C", MAJOR, root_octave=3, duration=QUARTER),
    ]


def create_bass_line():
    """Create a simple bass line."""
    return [
        Note("C3", HALF),
        Note("G2", HALF),
        Note("C3", QUARTER),
        Note("C3", QUARTER),
    ]


def main():
    """Generate and export sheet music."""
    print("Creating sheet music example...")

    # Create instruments
    violin = Instrument(name="violin", midi_program=40, clef="treble")
    viola = Instrument(name="viola", midi_program=41, clef="alto")
    cello = Instrument(name="cello", midi_program=42, clef="bass")

    # Create parts
    melody_part = Part(
        instrument=violin,
        notes=create_simple_melody(),
        name="Violin"
    )

    harmony_part = Part(
        instrument=viola,
        notes=create_harmony(),
        name="Viola"
    )

    bass_part = Part(
        instrument=cello,
        notes=create_bass_line(),
        name="Cello"
    )

    # Create score
    score = Score(
        parts=[melody_part, harmony_part, bass_part],
        title="Simple Trio",
        composer="Music Generation Library",
        tempo=100,
        time_signature="4/4",
        key_signature="C"
    )

    # Export to MusicXML
    output_path = "simple_trio.musicxml"
    writer = MusicXMLWriter(score)

    print(f"Writing MusicXML to: {output_path}")
    writer.write_musicxml(output_path)

    # Also create compressed version
    compressed_path = "simple_trio.mxl"
    print(f"Writing compressed MusicXML to: {compressed_path}")
    writer.write_mxl(compressed_path)

    # Validate the file
    if MusicXMLWriter.validate_musicxml(output_path):
        print("MusicXML file is valid!")
    else:
        print("Warning: MusicXML file may have issues.")

    # Create individual part files
    print("\nCreating individual part files...")
    for part_name in ["Violin", "Viola", "Cello"]:
        part_path = f"simple_trio_{part_name.lower()}.musicxml"
        MusicXMLWriter.get_part_excerpt(score, [part_name], part_path)
        print(f"  Created: {part_path}")

    print("\nDone! You can now open the MusicXML files in:")
    print("  - MuseScore (https://musescore.org/)")
    print("  - Sibelius")
    print("  - Finale")
    print("  - Or any other notation software that supports MusicXML")


if __name__ == "__main__":
    main()
```

## Validation Criteria

After implementation, verify the following:

### 1. Basic Functionality Tests

```python
from musicgen import Note, QUARTER, MAJOR
from musicgen.orchestration import Instrument, Part, Score
from musicgen.io import MusicXMLWriter
import music21

# Create a simple score
violin = Instrument(name="violin", midi_program=40, clef="treble")
part = Part(
    instrument=violin,
    notes=[Note("C4", QUARTER), Note("D4", QUARTER), Note("E4", QUARTER)],
    name="Violin"
)
score = Score(
    parts=[part],
    title="Test",
    composer="Test",
    tempo=100,
    time_signature="4/4",
    key_signature="C"
)

# Test conversion to music21
writer = MusicXMLWriter(score)
m21_score = writer.to_music21()
assert isinstance(m21_score, music21.stream.Score)
assert len(m21_score.parts) == 1
```

### 2. File Writing Tests

```python
# Test writing
output_path = "test_output.musicxml"
writer.write_musicxml(output_path)
assert Path(output_path).exists()

# Test validation
assert MusicXMLWriter.validate_musicxml(output_path) is True
```

### 3. Round-Trip Tests

```python
# Write and read back
writer.write_musicxml("test.musicxml")
read_score = MusicXMLReader.read("test.musicxml")
assert isinstance(read_score, music21.stream.Score)
```

### 4. MuseScore Import Test

Manually test that the generated MusicXML file can be opened in MuseScore:
1. Run the example script
2. Open `simple_trio.musicxml` in MuseScore
3. Verify that all parts, notes, and markings are displayed correctly
4. Check that the score layout is reasonable

### 5. XML Structure Tests

```python
import xml.etree.ElementTree as ET

# Parse the generated file
tree = ET.parse("test.musicxml")
root = tree.getroot()

# Verify required elements exist
assert root.tag.endswith('score-partwise')
assert root.find('.//part') is not None
assert root.find('.//measure') is not None
```

## Implementation Notes

1. **Music21 Integration**: Music21 is a mature library for musicology. Use its built-in conversion methods where possible rather than manually constructing XML.

2. **Handling Ties**: music21 represents ties differently than raw MusicXML. Use `m21.note.tie` and tie types (start, stop, continue).

3. **Beams**: music21 automatically handles beaming for eighth notes and shorter. You may want to disable auto-beaming and add explicit beams for control.

4. **Transposition**: For transposing instruments (clarinet, horn), decide whether to write at concert pitch or transposed pitch. Concert pitch is usually simpler for file exchange.

5. **Clef Selection**: Use the instrument's default clef, but handle instruments that use multiple clefs (cello, bassoon, etc.).

6. **Measure Grouping**: music21 automatically groups notes into measures based on time signature. Ensure your part durations align with measure boundaries.

7. **Error Handling**: MusicXML files can be malformed. Always wrap XML parsing in try-except blocks.

8. **File Extensions**: Use `.musicxml` for uncompressed XML and `.mxl` for compressed (ZIP) format.

9. **Namespaces**: MusicXML uses XML namespaces. When parsing with ElementTree, handle namespaces correctly.

10. **Version Compatibility**: music21 supports MusicXML 3.0 and 3.1. Target MusicXML 3.1 for maximum compatibility.

## Dependencies

This step requires the following dependencies in `pyproject.toml`:

```toml
[project]
dependencies = [
    # ... existing dependencies ...
    "music21>=9.0",  # Should already be present
    "lxml>=4.9",     # For faster XML parsing (optional but recommended)
]
```

## Success Criteria

Step 10 is complete when:

1. `src/musicgen/io/musicxml_writer.py` is implemented with all required methods
2. `pytest tests/test_musicxml_writer.py` passes with all tests green
3. Test coverage for `musicxml_writer.py` is > 80%
4. Generated MusicXML files can be opened in MuseScore without errors
5. Round-trip conversion (write/read) preserves essential musical information
6. The example script `examples/generate_sheet_music.py` runs successfully
7. All validation criteria tests pass

## Next Steps

After completing this step, proceed to Step 11: "Sheet Music Generation (LilyPond)" which will implement PDF sheet music generation using the Abjad library and LilyPond.

## References

- [Music21 Documentation](https://www.music21.org/)
- [MusicXML Specification](https://www.musicxml.com/)
- [MuseScore](https://musescore.org/)
- [music21 converter module](https://web.mit.edu/music21/doc/moduleReference/moduleConverter.html)
