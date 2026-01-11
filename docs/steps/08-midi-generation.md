# Implementation Prompt: Step 8 - MIDI File Generation

## Overview

This step implements the MIDI file generation module for the music generation library. The MIDI writer exports compositions to standard MIDI files that can be played back, edited in DAW software, or used as input for audio synthesis.

**Step Objective**: Export compositions to MIDI format for playback and editing.

**Dependencies**:
- Step 1: Core data structures (Note, Chord, Rest, duration/dynamic constants)
- Step 5: Melody Generation Engine (for melodic content)
- Step 6: Orchestration Module (for instrument definitions)
- Step 7: Musical Form Structures (for complete composition structure)

## Reading Context

Before implementing, read these files to understand the project structure and existing code:

1. `/home/chiranjeet/projects-cc/projects/music-gen-lib/docs/plan.md` - Overall implementation plan
2. `/home/chiranjeet/projects-cc/projects/music-gen-lib/docs/research.md` - Technical research
3. `/home/chiranjeet/projects-cc/projects/music-gen-lib/claude.md` - Project context and conventions
4. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/core/__init__.py` - Core module exports
5. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/core/note.py` - Note class definition
6. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/orchestration/instruments.py` - Instrument definitions

## Implementation Tasks

### Task 1: Create the IO Module Structure

Create the IO package directory and init file:

```
src/musicgen/io/
    __init__.py
    midi_writer.py
```

The `__init__.py` should export:
- `MIDIWriter` class
- `MIDITime` class (for MIDI time/tick calculations)
- `write_midi()` convenience function

### Task 2: Define Score and Part Data Classes

Since MIDI files require a structured representation of a composition, define these classes in `midi_writer.py` (or in a separate `composition.py` if preferred):

```python
from dataclasses import dataclass, field
from typing import List, Union, Optional
from musicgen.core import Note, Rest, Chord

@dataclass
class Part:
    """
    Represents a single instrument part in a score.

    Attributes:
        name: The part/instrument name (e.g., "violin", "flute")
        midi_program: General MIDI program number (0-127)
        midi_channel: MIDI channel (0-15, 10 reserved for percussion)
        notes: List of Note and Rest objects
        volume: Initial volume (0-127)
        pan: Pan position (-64 to 63, 0 = center)
    """
    name: str
    notes: List[Union[Note, Rest]] = field(default_factory=list)
    midi_program: int = 0
    midi_channel: int = 0
    volume: int = 100
    pan: int = 0
    pitch_bend_range: int = 2  # Semitones

    def add_note(self, note: Union[Note, Rest]) -> None:
        """Add a note or rest to this part."""
        pass

    def add_notes(self, notes: List[Union[Note, Rest]]) -> None:
        """Add multiple notes/rests to this part."""
        pass

    def duration(self) -> float:
        """Return total duration in quarter notes."""
        pass

    def clear(self) -> None:
        """Clear all notes from this part."""
        pass


@dataclass
class Score:
    """
    Represents a complete musical composition.

    Attributes:
        title: Title of the composition
        composer: Composer name
        parts: List of Part objects
        tempo: Initial tempo in BPM
        time_signature: Time signature as (numerator, denominator)
        key_signature: Key signature (0=C, 1=G, -1=F, etc.)
    """
    title: str = "Untitled"
    composer: str = "Unknown"
    parts: List[Part] = field(default_factory=list)
    tempo: float = 120.0
    time_signature: tuple[int, int] = (4, 4)
    key_signature: int = 0  # MIDI key signature format

    def add_part(self, part: Part) -> None:
        """Add a part to the score."""
        pass

    def remove_part(self, part_name: str) -> None:
        """Remove a part by name."""
        pass

    def get_part(self, name: str) -> Optional[Part]:
        """Get a part by name."""
        pass

    def duration(self) -> float:
        """Return total duration in quarter notes."""
        pass

    def total_tracks(self) -> int:
        """Return total number of parts (tracks)."""
        pass
```

### Task 3: Implement MIDITime Helper Class

Create a helper class for converting between musical time and MIDI ticks:

```python
from dataclasses import dataclass

@dataclass
class MIDITime:
    """
    Handles conversion between musical time and MIDI ticks.

    MIDI files use ticks to represent time. The number of ticks per quarter note
    (PPQN or "ticks per quarter note") determines timing resolution.

    Attributes:
        ppqn: Pulses Per Quarter Note (resolution), typically 480 or 960
        tempo: Current tempo in BPM
    """
    ppqn: int = 480
    tempo: float = 120.0

    def quarters_to_ticks(self, quarters: float) -> int:
        """Convert quarter notes to MIDI ticks."""
        pass

    def ticks_to_quarters(self, ticks: int) -> float:
        """Convert MIDI ticks to quarter notes."""
        pass

    def duration_to_ticks(self, duration: float) -> int:
        """Convert a duration value (in quarter notes) to ticks."""
        pass

    def seconds_to_ticks(self, seconds: float) -> int:
        """Convert seconds to ticks based on current tempo."""
        pass

    def ticks_to_seconds(self, ticks: int) -> float:
        """Convert ticks to seconds based on current tempo."""
        pass

    def tempo_to_microseconds(self, tempo: float) -> int:
        """
        Convert BPM to microseconds per quarter note.
        Formula: 60,000,000 / BPM
        """
        pass

    @staticmethod
    def calculate_delta_time(previous_tick: int, current_tick: int) -> int:
        """Calculate the delta time between two events in ticks."""
        pass
```

### Task 4: Implement the MIDIWriter Class

Create `src/musicgen/io/midi_writer.py` with the main `MIDIWriter` class:

```python
from typing import List, Optional, Union, Dict, Tuple
import struct
from pathlib import Path
from musicgen.core import Note, Rest, Chord
from musicgen.orchestration import Instrument, ORCHESTRAL_INSTRUMENTS


class MIDIWriter:
    """
    Writes musical compositions to MIDI files.

    This class handles the conversion of Note, Rest, and Chord objects
    into MIDI format, including proper timing, velocity, and channel
    assignment.

    Usage:
        writer = MIDIWriter()
        writer.write(score, "output.mid")

    Or use the convenience function:
        write_midi(score, "output.mid")
    """

    def __init__(self, ppqn: int = 480, velocity_multiplier: float = 1.0):
        """
        Initialize the MIDI writer.

        Args:
            ppqn: Pulses per quarter note (resolution), default 480
            velocity_multiplier: Multiplier for note velocities (0.5-1.5)
        """
        self.ppqn = ppqn
        self.velocity_multiplier = velocity_multiplier

    def write(self, score: Score, filepath: Union[str, Path]) -> None:
        """
        Write a Score to a MIDI file.

        Args:
            score: The Score object to write
            filepath: Output file path (will use .mid extension if not provided)

        Raises:
            ValueError: If score has no parts
            IOError: If file cannot be written
        """
        pass

    def write_to_bytes(self, score: Score) -> bytes:
        """
        Write a Score to MIDI file as bytes.

        Args:
            score: The Score object to write

        Returns:
            MIDI file content as bytes
        """
        pass

    def _write_header(self, num_tracks: int) -> bytes:
        """Write the MIDI header chunk."""
        pass

    def _write_tempo_track(self, score: Score) -> bytes:
        """Write track 0 with tempo and time signature meta-events."""
        pass

    def _write_part_track(self, part: Part, score: Score) -> bytes:
        """Write a track for a single part."""
        pass

    def _note_on_message(self, note: Note, start_tick: int) -> bytes:
        """Generate a note-on MIDI message."""
        pass

    def _note_off_message(self, note: Note, end_tick: int) -> bytes:
        """Generate a note-off MIDI message."""
        pass

    def _program_change_message(self, program: int, channel: int) -> bytes:
        """Generate a program change MIDI message."""
        pass

    def _control_change_message(self, control: int, value: int, channel: int) -> bytes:
        """Generate a control change MIDI message."""
        pass

    def _pitch_bend_message(self, value: int, channel: int) -> bytes:
        """Generate a pitch bend message (value 0-16383, center=8192)."""
        pass

    def _meta_event(self, meta_type: int, data: bytes) -> bytes:
        """Generate a meta event."""
        pass

    def _variable_length_quantity(self, value: int) -> bytes:
        """Encode a value as a MIDI variable-length quantity."""
        pass

    def _apply_velocity_curve(self, velocity: int) -> int:
        """
        Apply a velocity curve to the MIDI velocity.

        This ensures better dynamics by:
        1. Applying the multiplier
        2. Clamping to valid range (1-127)
        3. Optionally applying a non-linear curve
        """
        pass

    def _handle_chord(self, chord: Chord, start_tick: int) -> List[bytes]:
        """
        Generate MIDI messages for a chord.

        All notes in a chord start at the same time.
        """
        pass

    def _quantize_tick(self, tick: int, grid: int = None) -> int:
        """
        Quantize a tick value to a grid.

        Args:
            tick: The tick position to quantize
            grid: Grid resolution in ticks (default: ppqn/4 for 16th notes)

        Returns:
            Quantized tick value
        """
        pass

    def set_quantization(self, enabled: bool, grid: str = "16th") -> None:
        """
        Enable or disable quantization.

        Args:
            enabled: Whether to quantize note positions
            grid: Grid resolution ("quarter", "eighth", "16th", "32nd")
        """
        pass
```

### Task 5: Implement MIDI Event Generation

The following helper methods handle specific MIDI message types:

```python
def _note_on_event(self, channel: int, note: int, velocity: int, delta: int) -> bytes:
    """Create a note-on event with delta time."""
    # Status byte: 0x90 | channel (note on)
    # Data bytes: note number, velocity
    pass

def _note_off_event(self, channel: int, note: int, velocity: int, delta: int) -> bytes:
    """Create a note-off event with delta time."""
    # Status byte: 0x80 | channel (note off)
    # Data bytes: note number, velocity (usually 0)
    pass

def _set_tempo_event(self, microseconds: int, delta: int = 0) -> bytes:
    """Create a set tempo meta event."""
    # Meta type: 0x51
    # Data: 3 bytes (microseconds per quarter note, big-endian)
    pass

def _time_signature_event(self, numerator: int, denominator: int,
                          clocks_per_click: int = 24,
                          thirty_seconds_per_24_clocks: int = 8) -> bytes:
    """Create a time signature meta event."""
    # Meta type: 0x58
    # Denominator is stored as power of 2 (e.g., 4 for quarter, 8 for eighth)
    pass

def _key_signature_event(self, key: int, scale: int = 0) -> bytes:
    """
    Create a key signature meta event.

    Args:
        key: Number of sharps (positive) or flats (negative)
        scale: 0 for major, 1 for minor
    """
    pass

def _track_end_event(self) -> bytes:
    """Create an end-of-track meta event."""
    # Meta type: 0x2F, data length: 0
    pass
```

### Task 6: Implement Note Conversion

Convert Note objects to MIDI values:

```python
def _note_to_midi_number(self, note: Note) -> int:
    """
    Convert a Note object to MIDI note number.

    Uses the note's midi_number property if available,
    otherwise calculates from name and octave.

    C4 = 60, A4 = 69
    """
    pass

def _dynamic_to_velocity(self, note: Note) -> int:
    """
    Convert a note's dynamic to MIDI velocity.

    Mapping:
        - pp (30) -> 30-50
        - p (50)  -> 50-70
        - mp (70) -> 70-90
        - mf (90) -> 90-110
        - f (100) -> 100-120
        - ff (120)-> 120-127
    """
    pass

def _articulation_to_velocity_adjustment(self, articulation: str) -> float:
    """
    Adjust velocity based on articulation.

    Returns:
        Multiplier for velocity:
        - "." (staccato): 1.1 (shorter, but accented)
        - ">" (accent): 1.2
        - "-" (tenuto): 1.0 (sustained, normal)
        - "^" (martellato): 1.15
    """
    pass
```

### Task 7: Implement Convenience Function

Create a top-level convenience function:

```python
def write_midi(score: Score,
               filepath: Union[str, Path],
               ppqn: int = 480,
               velocity_multiplier: float = 1.0) -> None:
    """
    Convenience function to write a Score to a MIDI file.

    Args:
        score: The Score to write
        filepath: Output file path
        ppqn: Resolution (pulses per quarter note)
        velocity_multiplier: Velocity multiplier

    Example:
        score = Score(title="My Piece")
        part = Part(name="piano", midi_program=0)
        part.add_notes([Note("C4"), Note("E4"), Note("G4")])
        score.add_part(part)
        write_midi(score, "output.mid")
    """
    writer = MIDIWriter(ppqn=ppqn, velocity_multiplier=velocity_multiplier)
    writer.write(score, filepath)
```

### Task 8: Add MIDI Reading Support (Optional but Recommended)

Add basic MIDI file reading capability:

```python
class MIDIReader:
    """Reads MIDI files and converts them to Score objects."""

    def __init__(self):
        """Initialize the MIDI reader."""
        pass

    def read(self, filepath: Union[str, Path]) -> Score:
        """
        Read a MIDI file and convert to a Score.

        Args:
            filepath: Path to MIDI file

        Returns:
            A Score object with Parts and Notes

        Raises:
            ValueError: If file is not a valid MIDI file
        """
        pass

    def read_from_bytes(self, data: bytes) -> Score:
        """Read a Score from MIDI file bytes."""
        pass

    def _parse_header(self, data: bytes, offset: int) -> Tuple[int, int]:
        """Parse MIDI header, return (format, num_tracks)."""
        pass

    def _parse_track(self, data: bytes, offset: int) -> List[Tuple]:
        """Parse a track, return list of events."""
        pass

    def _read_variable_length_quantity(self, data: bytes, offset: int) -> Tuple[int, int]:
        """Read variable length quantity, return (value, new_offset)."""
        pass
```

## File Structure

Create the following files:

```
src/musicgen/io/
    __init__.py       # Module exports: MIDIWriter, write_midi, MIDIReader (optional)
    midi_writer.py    # MIDIWriter, Score, Part, MIDITime classes
```

Update `src/musicgen/__init__.py` to include:
```python
from .io import (
    MIDIWriter,
    MIDIReader,
    MIDITime,
    Score,
    Part,
    write_midi,
    read_midi,
)
```

## Test Requirements

Create `tests/test_midi_writer.py`:

```python
import pytest
import tempfile
import os
from pathlib import Path
from musicgen.io import MIDIWriter, Score, Part, write_midi, MIDITime
from musicgen.core import Note, Rest, QUARTER, EIGHTH, HALF, MF, F
from musicgen.orchestration import ORCHESTRAL_INSTRUMENTS


class TestMIDITime:
    """Test MIDI time conversions."""

    def test_quarters_to_ticks(self):
        time = MIDITime(ppqn=480)
        assert time.quarters_to_ticks(1) == 480
        assert time.quarters_to_ticks(0.5) == 240
        assert time.quarters_to_ticks(2) == 960

    def test_ticks_to_quarters(self):
        time = MIDITime(ppqn=480)
        assert time.ticks_to_quarters(480) == 1.0
        assert time.ticks_to_quarters(240) == 0.5

    def test_tempo_to_microseconds(self):
        time = MIDITime()
        # 120 BPM = 500,000 microseconds per quarter
        assert time.tempo_to_microseconds(120) == 500000
        # 60 BPM = 1,000,000 microseconds per quarter
        assert time.tempo_to_microseconds(60) == 1000000

    def test_different_ppqn(self):
        time = MIDITime(ppqn=960)
        assert time.quarters_to_ticks(1) == 960


class TestPart:
    """Test Part class."""

    def test_create_part(self):
        part = Part(name="piano", midi_program=0)
        assert part.name == "piano"
        assert part.midi_program == 0
        assert part.midi_channel == 0
        assert len(part.notes) == 0

    def test_add_note(self):
        part = Part(name="piano")
        note = Note("C4", QUARTER)
        part.add_note(note)
        assert len(part.notes) == 1
        assert part.notes[0] == note

    def test_add_notes(self):
        part = Part(name="piano")
        notes = [Note("C4"), Note("E4"), Note("G4")]
        part.add_notes(notes)
        assert len(part.notes) == 3

    def test_part_duration(self):
        part = Part(name="piano")
        part.add_notes([
            Note("C4", QUARTER),
            Note("E4", QUARTER),
            Note("G4", HALF)
        ])
        assert part.duration() == 4.0  # 1 + 1 + 2 quarter notes

    def test_clear(self):
        part = Part(name="piano")
        part.add_notes([Note("C4"), Note("E4")])
        assert len(part.notes) == 2
        part.clear()
        assert len(part.notes) == 0


class TestScore:
    """Test Score class."""

    def test_create_score(self):
        score = Score(title="Test Piece")
        assert score.title == "Test Piece"
        assert score.tempo == 120.0
        assert score.time_signature == (4, 4)
        assert len(score.parts) == 0

    def test_add_part(self):
        score = Score()
        part = Part(name="piano")
        score.add_part(part)
        assert len(score.parts) == 1

    def test_remove_part(self):
        score = Score()
        part = Part(name="piano")
        score.add_part(part)
        score.remove_part("piano")
        assert len(score.parts) == 0

    def test_get_part(self):
        score = Score()
        part = Part(name="piano")
        score.add_part(part)
        retrieved = score.get_part("piano")
        assert retrieved is not None
        assert retrieved.name == "piano"

    def test_get_nonexistent_part(self):
        score = Score()
        assert score.get_part("nonexistent") is None

    def test_score_duration(self):
        score = Score()
        part1 = Part(name="piano")
        part1.add_notes([Note("C4", QUARTER)])
        part2 = Part(name="violin")
        part2.add_notes([Note("E4", HALF)])
        score.add_part(part1)
        score.add_part(part2)
        # Duration should be max of all parts
        assert score.duration() == 2.0


class TestMIDIWriter:
    """Test MIDIWriter class."""

    def test_writer_init(self):
        writer = MIDIWriter(ppqn=480)
        assert writer.ppqn == 480
        assert writer.velocity_multiplier == 1.0

    def test_write_to_bytes(self):
        writer = MIDIWriter()
        score = Score(title="Test")
        part = Part(name="piano", midi_program=0)
        part.add_notes([Note("C4", QUARTER)])
        score.add_part(part)

        midi_bytes = writer.write_to_bytes(score)
        assert len(midi_bytes) > 0
        # Check for MThd header
        assert midi_bytes[:4] == b'MThd'

    def test_write_file(self):
        writer = MIDIWriter()
        score = Score(title="Test")
        part = Part(name="piano", midi_program=0)
        part.add_notes([Note("C4", QUARTER)])
        score.add_part(part)

        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
            filepath = f.name

        try:
            writer.write(score, filepath)
            assert os.path.exists(filepath)
            assert os.path.getsize(filepath) > 0
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_write_multiple_parts(self):
        writer = MIDIWriter()
        score = Score(title="Test")
        part1 = Part(name="piano", midi_program=0, midi_channel=0)
        part2 = Part(name="violin", midi_program=40, midi_channel=1)
        part1.add_notes([Note("C4", QUARTER)])
        part2.add_notes([Note("E4", QUARTER)])
        score.add_part(part1)
        score.add_part(part2)

        midi_bytes = writer.write_to_bytes(score)
        assert len(midi_bytes) > 0
        # Should have 3 tracks: tempo + 2 instrument tracks
        # Check header format 1 (multitrack)
        format_num = int.from_bytes(midi_bytes[8:10], 'big')
        assert format_num == 1

    def test_velocity_multiplier(self):
        writer = MIDIWriter(velocity_multiplier=0.5)
        assert writer.velocity_multiplier == 0.5

    def test_write_with_rests(self):
        writer = MIDIWriter()
        score = Score(title="Test")
        part = Part(name="piano")
        part.add_notes([
            Note("C4", QUARTER),
            Rest(QUARTER),
            Note("E4", QUARTER)
        ])
        score.add_part(part)

        midi_bytes = writer.write_to_bytes(score)
        assert len(midi_bytes) > 0

    def test_write_with_different_durations(self):
        writer = MIDIWriter()
        score = Score(title="Test")
        part = Part(name="piano")
        part.add_notes([
            Note("C4", WHOLE),
            Note("E4", HALF),
            Note("G4", QUARTER),
            Note("C5", EIGHTH)
        ])
        score.add_part(part)

        midi_bytes = writer.write_to_bytes(score)
        assert len(midi_bytes) > 0

    def test_write_with_different_velocities(self):
        writer = MIDIWriter()
        score = Score(title="Test")
        part = Part(name="piano")
        part.add_notes([
            Note("C4", QUARTER, velocity=PP),
            Note("E4", QUARTER, velocity=MF),
            Note("G4", QUARTER, velocity=FF)
        ])
        score.add_part(part)

        midi_bytes = writer.write_to_bytes(score)
        assert len(midi_bytes) > 0

    def test_quantization(self):
        writer = MIDIWriter()
        writer.set_quantization(enabled=True, grid="16th")
        time = MIDITime(ppqn=480)
        tick = time.quarters_to_ticks(0.25)  # Sixteenth note
        quantized = writer._quantize_tick(tick)
        assert quantized == tick

    def test_variable_length_quantity(self):
        writer = MIDIWriter()
        # Test values that require different byte lengths
        assert writer._variable_length_quantity(0) == b'\x00'
        assert writer._variable_length_quantity(127) == b'\x7f'
        assert writer._variable_length_quantity(128) == b'\x81\x00'
        assert writer._variable_length_quantity(16383) == b'\xff\x7f'


class TestWriteMidiFunction:
    """Test convenience function."""

    def test_write_midi_function(self):
        score = Score(title="Test")
        part = Part(name="piano", midi_program=0)
        part.add_notes([Note("C4", QUARTER)])
        score.add_part(part)

        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
            filepath = f.name

        try:
            write_midi(score, filepath)
            assert os.path.exists(filepath)
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_write_midi_auto_extension(self):
        score = Score(title="Test")
        part = Part(name="piano", midi_program=0)
        part.add_notes([Note("C4", QUARTER)])
        score.add_part(part)

        with tempfile.NamedTemporaryFile(delete=False) as f:
            filepath = f.name

        try:
            # Write without .mid extension
            write_midi(score, filepath)
            # File should exist with .mid added
            assert os.path.exists(filepath + '.mid')
        finally:
            for ext in ['', '.mid']:
                if os.path.exists(filepath + ext):
                    os.unlink(filepath + ext)


class TestMIDIIntegration:
    """Integration tests with actual MIDI file validation."""

    def test_simple_melody_roundtrip(self):
        """Create a simple melody and verify it can be written."""
        score = Score(title="Simple Melody", tempo=120)
        part = Part(name="piano", midi_program=0)
        part.add_notes([
            Note("C4", QUARTER, velocity=MF),
            Note("D4", QUARTER, velocity=MF),
            Note("E4", QUARTER, velocity=MF),
            Note("F4", QUARTER, velocity=MF),
            Note("G4", HALF, velocity=F),
        ])
        score.add_part(part)

        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
            filepath = f.name

        try:
            write_midi(score, filepath)
            assert os.path.exists(filepath)

            # Verify it's a valid MIDI file by checking header
            with open(filepath, 'rb') as f:
                header = f.read(14)
                assert header[:4] == b'MThd'
                assert header[8:10] == b'\x00\x01'  # Format 1

        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_multi_instrument_score(self):
        """Test a score with multiple instruments."""
        score = Score(title="Ensemble", tempo=100)

        # Piano
        piano = Part(name="piano", midi_program=0, midi_channel=0)
        piano.add_notes([
            Note("C4", WHOLE, velocity=MF),
            Note("E4", WHOLE, velocity=MF),
            Note("G4", WHOLE, velocity=MF),
        ])

        # Violin
        violin = Part(name="violin", midi_program=40, midi_channel=1)
        violin.add_notes([
            Note("E5", HALF, velocity=F),
            Note("G5", HALF, velocity=F),
        ])

        score.add_part(piano)
        score.add_part(violin)

        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
            filepath = f.name

        try:
            write_midi(score, filepath)
            assert os.path.exists(filepath)

            # Check file size is reasonable
            size = os.path.getsize(filepath)
            assert size > 100  # At minimum header + some tracks

        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_time_signature(self):
        """Test writing different time signatures."""
        for time_sig in [(3, 4), (2, 4), (6, 8), (12, 8)]:
            score = Score(title=f"{time_sig[0]}/{time_sig[1]} Time")
            score.time_signature = time_sig
            part = Part(name="piano")
            part.add_notes([Note("C4", QUARTER)])
            score.add_part(part)

            with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
                filepath = f.name

            try:
                write_midi(score, filepath)
                assert os.path.exists(filepath)
            finally:
                if os.path.exists(filepath):
                    os.unlink(filepath)

    def test_key_signatures(self):
        """Test writing different key signatures."""
        # Test major keys: C (0), G (1), F (-1)
        for key in [0, 1, -1, 2, -2]:
            score = Score(title=f"Key {key}")
            score.key_signature = key
            part = Part(name="piano")
            part.add_notes([Note("C4", QUARTER)])
            score.add_part(part)

            midi_bytes = MIDIWriter().write_to_bytes(score)
            assert len(midi_bytes) > 0


class TestMIDIReader:
    """Test MIDI reading (if implemented)."""

    def test_read_written_file(self):
        """Write a MIDI file and read it back."""
        original_score = Score(title="Test Write/Read")
        part = Part(name="piano", midi_program=0)
        part.add_notes([
            Note("C4", QUARTER, velocity=MF),
            Note("E4", QUARTER, velocity=MF),
            Note("G4", HALF, velocity=F),
        ])
        original_score.add_part(part)

        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
            filepath = f.name

        try:
            # Write
            write_midi(original_score, filepath)

            # Read back
            reader = MIDIReader()
            read_score = reader.read(filepath)

            # Verify basic properties
            assert read_score.title == original_score.title
            assert len(read_score.parts) == len(original_score.parts)

        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)
```

## Example Script

Create `examples/generate_midi.py`:

```python
#!/usr/bin/env python3
"""
Example script demonstrating MIDI file generation.

This script creates a simple composition and exports it to MIDI format.
"""

from musicgen.io import Score, Part, write_midi
from musicgen.core import Note, Chord, Rest, QUARTER, HALF, WHOLE, MF, F
from musicgen.orchestration import ORCHESTRAL_INSTRUMENTS


def create_simple_melody():
    """Create a simple C major melody."""
    score = Score(
        title="Simple Melody",
        composer="MusicGen Library",
        tempo=120,
        time_signature=(4, 4),
        key_signature=0  # C major
    )

    # Create a piano part with a simple melody
    piano = Part(
        name="piano",
        midi_program=0,  # Acoustic Grand Piano
        midi_channel=0,
        volume=100
    )

    # Add a melody: C major scale
    melody = [
        Note("C4", QUARTER, velocity=MF),
        Note("D4", QUARTER, velocity=MF),
        Note("E4", QUARTER, velocity=MF),
        Note("F4", QUARTER, velocity=MF),
        Note("G4", QUARTER, velocity=F),
        Note("A4", QUARTER, velocity=F),
        Note("G4", HALF, velocity=F),  # Descending
        Note("E4", WHOLE, velocity=MF),
    ]

    piano.add_notes(melody)
    score.add_part(piano)

    return score


def create_string_quartet():
    """Create a simple string quartet piece."""
    score = Score(
        title="String Quartet in C",
        composer="MusicGen Library",
        tempo=100,
        time_signature=(4, 4)
    )

    # Get instrument definitions
    violin = ORCHESTRAL_INSTRUMENTS["violin"]
    viola = ORCHESTRAL_INSTRUMENTS["viola"]
    cello = ORCHESTRAL_INSTRUMENTS["cello"]

    # First violin - melody
    violin_i = Part(
        name="violin_i",
        midi_program=40,
        midi_channel=0
    )
    violin_i.add_notes([
        Note("E5", QUARTER, velocity=F),
        Note("G5", QUARTER, velocity=F),
        Note("C5", HALF, velocity=MF),
        Rest(QUARTER),
        Note("D5", QUARTER, velocity=MF),
        Note("E5", WHOLE, velocity=MF),
    ])

    # Second violin - harmony
    violin_ii = Part(
        name="violin_ii",
        midi_program=40,
        midi_channel=1
    )
    violin_ii.add_notes([
        Note("C5", QUARTER, velocity=MF),
        Note("E5", QUARTER, velocity=MF),
        Note("G4", HALF, velocity=MF),
        Rest(QUARTER),
        Note("B4", QUARTER, velocity=MF),
        Note("C5", WHOLE, velocity=MF),
    ])

    # Viola
    viola_part = Part(
        name="viola",
        midi_program=41,
        midi_channel=2
    )
    viola_part.add_notes([
        Note("G4", QUARTER, velocity=MF),
        Note("C5", QUARTER, velocity=MF),
        Note("E4", HALF, velocity=MF),
        Rest(QUARTER),
        Note("G4", QUARTER, velocity=MF),
        Note("G4", WHOLE, velocity=MF),
    ])

    # Cello - bass line
    cello_part = Part(
        name="cello",
        midi_program=42,
        midi_channel=3
    )
    cello_part.add_notes([
        Note("C3", HALF, velocity=MF),
        Note("G3", QUARTER, velocity=MF),
        Note("C3", QUARTER, velocity=MF),
        Rest(QUARTER),
        Note("G2", QUARTER, velocity=F),
        Note("C3", WHOLE, velocity=MF),
    ])

    score.add_part(violin_i)
    score.add_part(violin_ii)
    score.add_part(viola_part)
    score.add_part(cello_part)

    return score


def create_chord_progression():
    """Create a piece demonstrating chord progressions."""
    score = Score(
        title="Chord Progression Demo",
        composer="MusicGen Library",
        tempo=90
    )

    piano = Part(name="piano", midi_program=0)

    # I - IV - V - I progression in C major
    # Each chord lasts one measure
    progression = [
        Chord("C", "major", root_octave=4, duration=WHOLE),  # I
        Chord("F", "major", root_octave=3, duration=WHOLE),  # IV
        Chord("G", "dominant_7th", root_octave=3, duration=WHOLE),  # V7
        Chord("C", "major", root_octave=4, duration=WHOLE),  # I
    ]

    for chord in progression:
        # Convert chord to individual notes
        for note in chord.notes:
            note_copy = Note(note.to_pitch_string(), chord.duration, velocity=MF)
            piano.add_note(note_copy)

    score.add_part(piano)
    return score


def main():
    """Generate example MIDI files."""
    import os

    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Generate examples
    examples = [
        ("simple_melody.mid", create_simple_melody()),
        ("string_quartet.mid", create_string_quartet()),
        ("chord_progression.mid", create_chord_progression()),
    ]

    for filename, score in examples:
        filepath = output_dir / filename
        write_midi(score, filepath)
        print(f"Generated: {filepath}")
        print(f"  Parts: {score.total_tracks()}")
        print(f"  Duration: {score.duration()} quarter notes")
        print()


if __name__ == "__main__":
    main()
```

## Validation Criteria

After implementation, verify these behaviors:

```python
# 1. Basic MIDI file creation
from musicgen.io import Score, Part, write_midi
from musicgen.core import Note, QUARTER, MF

score = Score(title="Test")
part = Part(name="piano", midi_program=0)
part.add_notes([
    Note("C4", QUARTER, velocity=MF),
    Note("E4", QUARTER, velocity=MF),
    Note("G4", QUARTER, velocity=MF),
])
score.add_part(part)

write_midi(score, "test.mid")
assert os.path.exists("test.mid")
assert os.path.getsize("test.mid") > 0

# 2. MIDI header validation
with open("test.mid", "rb") as f:
    header = f.read(14)
    assert header[:4] == b'MThd'  # MIDI header marker
    assert header[8:10] == b'\x00\x01'  # Format 1 (multitrack)

# 3. Verify MIDI can be opened by standard libraries
import mido
midi_file = mido.MidiFile("test.mid")
assert len(midi_file.tracks) > 0

# 4. Multi-part MIDI
score2 = Score(title="Ensemble")
score2.add_part(Part(name="piano", midi_program=0))
score2.add_part(Part(name="violin", midi_program=40))
score2.add_part(Part(name="cello", midi_program=42))

write_midi(score2, "ensemble.mid")
midi_file = mido.MidiFile("ensemble.mid")
assert len(midi_file.tracks) >= 3  # Tempo track + 2+ instrument tracks

# 5. Test velocity mapping
from musicgen.core import PP, FF
note_quiet = Note("C4", QUARTER, velocity=PP)
note_loud = Note("C4", QUARTER, velocity=FF)
assert note_quiet.velocity < note_loud.velocity
```

## Dependencies on Previous Steps

This step depends on:

1. **Step 1 (Core)**: Uses `Note`, `Rest`, `Chord` classes and duration/dynamic constants
2. **Step 6 (Orchestration)**: Uses `Instrument` class for MIDI program mapping

The Note class must have:
- `to_pitch_string()` or `name` and `octave` properties
- `midi_number` property
- `duration` property
- `velocity` property

The Instrument class must have:
- `midi_program` attribute

## Technical Notes

### MIDI File Format

A MIDI file consists of:
1. **Header chunk** (MThd): Contains format, number of tracks, time division
2. **Track chunks** (MTrk): Each contains a sequence of MIDI events

### MIDI Messages

Key MIDI messages used:
- **Note On**: `0x90 | channel, note, velocity`
- **Note Off**: `0x80 | channel, note, velocity` (or Note On with velocity=0)
- **Program Change**: `0xC0 | channel, program`
- **Control Change**: `0xB0 | channel, control, value`

### Meta Events

Meta events used:
- **Set Tempo** (0x51): Microseconds per quarter note
- **Time Signature** (0x58): Numerator, denominator, etc.
- **Key Signature** (0x59): Sharps/flats, major/minor
- **End of Track** (0x2F): Marks track end

### Variable Length Quantities

MIDI uses variable-length encoding for delta times. A value is encoded as:
- 1 byte if value < 128
- 2 bytes if value < 16384
- 3 bytes if value < 2097152
- 4 bytes otherwise

Each byte uses the high bit as a "continue" flag.

### Velocity to Dynamic Mapping

Recommended mapping:
```python
DYNAMIC_TO_VELOCITY = {
    "pp": (30, 50),
    "p": (50, 70),
    "mp": (70, 90),
    "mf": (90, 110),
    "f": (100, 120),
    "ff": (115, 127),
}
```

### Quantization

By default, don't quantize. When enabled, round note positions to the nearest grid:
- Quarter note grid: PPQN ticks
- Eighth note grid: PPQN/2 ticks
- Sixteenth note grid: PPQN/4 ticks

## Success Criteria

Step 8 is complete when:

1. `MIDIWriter` class can write valid MIDI files
2. `Score` and `Part` classes are implemented
3. MIDI files can be opened by standard MIDI software (mido, DAWs)
4. Multi-track MIDI files work correctly
5. Tempo, time signature, and key signature are properly encoded
6. Velocities are correctly mapped from dynamics
7. All tests pass: `pytest tests/test_midi_writer.py`
8. Test coverage is at least 80% for the MIDI writer module
9. The example script runs without errors and produces valid MIDI files

## Next Steps

After completing this step, proceed to Step 9: "Audio Synthesis Pipeline" which will use the MIDI files generated here to produce audio output using FluidSynth.
