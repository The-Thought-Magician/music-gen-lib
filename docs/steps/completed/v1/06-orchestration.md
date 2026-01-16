# Implementation Prompt: Step 6 - Orchestration Module

## Overview

This step implements the orchestration module for the music generation library. The orchestration module defines instrument characteristics (ranges, transposition, articulations), provides an orchestral instrument library, and creates ensemble/texture templates for combining instruments musically.

**Step Objective**: Define instrument characteristics and create orchestration templates.

**Dependencies**:
- Step 1: Core data structures (Note, Chord, Rest, duration/dynamic constants)
- Step 2: Scales and Keys (for key-based transposition)

## Reading Context

Before implementing, read these files to understand the project structure and existing code:

1. `/home/chiranjeet/projects-cc/projects/music-gen-lib/docs/plan.md` - Overall implementation plan
2. `/home/chiranjeet/projects-cc/projects/music-gen-lib/docs/research.md` - Technical research and orchestration reference
3. `/home/chiranjeet/projects-cc/projects/music-gen-lib/claude.md` - Project context and conventions
4. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/core/__init__.py` - Core module exports
5. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/core/note.py` - Note class definition
6. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/core/chord.py` - Chord class definition
7. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/theory/__init__.py` - Theory module exports

## Implementation Tasks

### Task 1: Create the Orchestration Module Structure

Create the orchestration package directory and init file:

```
src/musicgen/orchestration/
    __init__.py
    instruments.py
    ensembles.py
```

The `__init__.py` should export the main classes:
- `Instrument`
- `InstrumentFamily`
- `Ensemble`
- `Texture`
- `ORCHESTRRAL_INSTRUMENTS` (dictionary of predefined instruments)

### Task 2: Implement the Instrument Class

Create `src/musicgen/orchestration/instruments.py` with the following:

#### 2.1 InstrumentFamily Enum

```python
from enum import Enum

class InstrumentFamily(Enum):
    """Categories of musical instruments in an orchestra."""
    STRINGS = "strings"
    WOODWINDS = "woodwinds"
    BRASS = "brass"
    PERCUSSION = "percussion"
    KEYBOARD = "keyboard"
```

#### 2.2 Instrument Class

The `Instrument` class should have the following attributes and methods:

```python
from dataclasses import dataclass, field
from typing import Optional, List, Tuple

@dataclass
class Instrument:
    """
    Represents a musical instrument with its characteristics.

    Attributes:
        name: The name of the instrument (e.g., "violin", "flute")
        family: The instrument family (strings, woodwinds, brass, percussion)
        lowest_note: Lowest playable note (e.g., "G3" for violin)
        highest_note: Highest playable note (e.g., "A7" for violin)
        transposition: Semitones to add to written pitch to get concert pitch
                       (0 for non-transposing instruments, 2 for Bb clarinet, -2 for Bb trumpet)
        clef: Default clef for notation ("treble", "bass", "alto", "tenor")
        midi_program: General MIDI program number (0-127)
        dynamic_range: (min_velocity, max_velocity) for this instrument
        articulations: List of supported articulations
    """
    name: str
    family: InstrumentFamily
    lowest_note: str
    highest_note: str
    transposition: int = 0
    clef: str = "treble"
    midi_program: int = 0
    dynamic_range: Tuple[int, int] = (30, 120)
    articulations: List[str] = field(default_factory=list)

    @property
    def lowest_midi(self) -> int:
        """Convert lowest_note to MIDI number."""
        pass

    @property
    def highest_midi(self) -> int:
        """Convert highest_note to MIDI number."""
        pass

    def in_range(self, note: Note) -> bool:
        """Check if a note is within this instrument's playable range."""
        pass

    def clamp_to_range(self, note: Note) -> Note:
        """Return a note within the instrument's range (transpose octaves if needed)."""
        pass

    def written_to_concert(self, written_note: Note) -> Note:
        """Convert a written note to concert pitch (for transposing instruments)."""
        pass

    def concert_to_written(self, concert_note: Note) -> Note:
        """Convert a concert pitch note to written pitch (for transposing instruments)."""
        pass

    def effective_dynamic(self, marked_dynamic: str) -> int:
        """
        Get the MIDI velocity for a given dynamic marking for this instrument.
        Different instruments have different perceived volumes at the same dynamic.
        """
        pass

    def can_playArticulation(self, articulation: str) -> bool:
        """Check if the instrument supports a given articulation."""
        pass
```

#### 2.3 Note Helper Methods

The class should use the Note class from core. Note conversion methods:

```python
@staticmethod
def note_name_to_midi(note_name: str) -> int:
    """Convert note name like 'C4' to MIDI number."""
    # C4 = 60, A4 = 69
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_name = note_name[:-1]
    octave = int(note_name[-1])
    return notes.index(note_name) + (octave + 1) * 12

@staticmethod
def midi_to_note_name(midi: int) -> str:
    """Convert MIDI number to note name like 'C4'."""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi // 12) - 1
    note = notes[midi % 12]
    return f"{note}{octave}"
```

### Task 3: Define the Orchestral Instrument Library

Create a dictionary `ORCHESTRAL_INSTRUMENTS` containing predefined instruments:

#### 3.1 Strings Family

```python
# Violin
Instrument(
    name="violin",
    family=InstrumentFamily.STRINGS,
    lowest_note="G3",
    highest_note="A7",
    transposition=0,
    clef="treble",
    midi_program=40,
    dynamic_range=(40, 120),
    articulations=["legato", "staccato", "spiccato", "pizzicato", "tremolo", "sul ponticello"]
)

# Viola
Instrument(
    name="viola",
    family=InstrumentFamily.STRINGS,
    lowest_note="C3",
    highest_note="E6",
    transposition=0,
    clef="alto",
    midi_program=41,
    dynamic_range=(40, 115),
    articulations=["legato", "staccato", "spiccato", "pizzicato", "tremolo"]
)

# Cello
Instrument(
    name="cello",
    family=InstrumentFamily.STRINGS,
    lowest_note="C2",
    highest_note="E5",
    transposition=0,
    clef="bass",
    midi_program=42,
    dynamic_range=(45, 120),
    articulations=["legato", "staccato", "pizzicato", "tremolo", "sul ponticello"]
)

# Double Bass
Instrument(
    name="double_bass",
    family=InstrumentFamily.STRINGS,
    lowest_note="E1",
    highest_note="C5",
    transposition=-12,  # Sounds octave lower than written
    clef="bass",
    midi_program=43,
    dynamic_range=(50, 115),
    articulations=["legato", "staccato", "pizzicato", "tremolo"]
)

# Harp
Instrument(
    name="harp",
    family=InstrumentFamily.STRINGS,
    lowest_note="Cb1",
    highest_note="G#7",
    transposition=0,
    clef="treble",
    midi_program=46,
    dynamic_range=(35, 110),
    articulations=["glissando", "arpeggio", "harmonic"]
)
```

#### 3.2 Woodwinds Family

```python
# Flute
Instrument(
    name="flute",
    family=InstrumentFamily.WOODWINDS,
    lowest_note="C4",
    highest_note="D7",
    transposition=0,
    clef="treble",
    midi_program=73,
    dynamic_range=(35, 120),
    articulations=["legato", "staccato", "flutter_tongue", "trill"]
)

# Piccolo
Instrument(
    name="piccolo",
    family=InstrumentFamily.WOODWINDS,
    lowest_note="D5",
    highest_note="C8",
    transposition=12,  # Sounds octave higher
    clef="treble",
    midi_program=72,
    dynamic_range=(30, 115),
    articulations=["legato", "staccato", "flutter_tongue"]
)

# Oboe
Instrument(
    name="oboe",
    family=InstrumentFamily.WOODWINDS,
    lowest_note="Bb3",
    highest_note="A6",
    transposition=0,
    clef="treble",
    midi_program=74,
    dynamic_range=(40, 115),
    articulations=["legato", "staccato", "trill"]
)

# Clarinet (Bb)
Instrument(
    name="clarinet",
    family=InstrumentFamily.WOODWINDS,
    lowest_note="E3",
    highest_note="C7",
    transposition=-2,  # Bb clarinet sounds major 2nd lower
    clef="treble",
    midi_program=75,
    dynamic_range=(35, 120),
    articulations=["legato", "staccato", "glissando"]
)

# Bassoon
Instrument(
    name="bassoon",
    family=InstrumentFamily.WOODWINDS,
    lowest_note="Bb1",
    highest_note="Eb5",
    transposition=0,
    clef="bass",
    midi_program=76,
    dynamic_range=(45, 115),
    articulations=["legato", "staccato", "staccatissimo", "trill"]
)
```

#### 3.3 Brass Family

```python
# Trumpet (C)
Instrument(
    name="trumpet",
    family=InstrumentFamily.BRASS,
    lowest_note="E3",
    highest_note="C6",
    transposition=0,
    clef="treble",
    midi_program=56,
    dynamic_range=(50, 127),
    articulations=["legato", "staccato", "mute", "flutter_tongue"]
)

# French Horn
Instrument(
    name="french_horn",
    family=InstrumentFamily.BRASS,
    lowest_note="B1",
    highest_note="F5",
    transposition=-7,  # F horn sounds perfect 5th lower
    clef="treble",
    midi_program=60,
    dynamic_range=(45, 115),
    articulations=["legato", "staccato", "mute", "stopped"]
)

# Trombone
Instrument(
    name="trombone",
    family=InstrumentFamily.BRASS,
    lowest_note="E2",
    highest_note="F5",
    transposition=0,
    clef="bass",
    midi_program=57,
    dynamic_range=(50, 120),
    articulations=["legato", "staccato", "mute", "glissando"]
)

# Tuba
Instrument(
    name="tuba",
    family=InstrumentFamily.BRASS,
    lowest_note="D1",
    highest_note="F4",
    transposition=0,
    clef="bass",
    midi_program=58,
    dynamic_range=(55, 115),
    articulations=["legato", "staccato"]
)
```

#### 3.4 Percussion Family

```python
# Timpani
Instrument(
    name="timpani",
    family=InstrumentFamily.PERCUSSION,
    lowest_note="F2",
    highest_note="C3",
    transposition=0,
    clef="bass",
    midi_program=47,
    dynamic_range=(50, 120),
    articulations=["roll", "accent"]
)

# Orchestral Bells
Instrument(
    name="glockenspiel",
    family=InstrumentFamily.PERCUSSION,
    lowest_note="C5",
    highest_note="C6",
    transposition=12,  # Sounds 2 octaves higher
    clef="treble",
    midi_program=14,
    dynamic_range=(40, 110),
    articulations=["roll", "let_vibrate"]
)

# Xylophone
Instrument(
    name="xylophone",
    family=InstrumentFamily.PERCUSSION,
    lowest_note="F4",
    highest_note="C7",
    transposition=0,
    clef="treble",
    midi_program=13,
    dynamic_range=(40, 115),
    articulations=["roll", "glissando"]
)
```

### Task 4: Implement the Ensemble Class

Create `src/musicgen/orchestration/ensembles.py` with the following:

#### 4.1 Ensemble Class

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from .instruments import Instrument, ORCHESTRAL_INSTRUMENTS

@dataclass
class Ensemble:
    """
    A collection of instruments playing together.

    Attributes:
        name: Name of the ensemble (e.g., "string_quartet", "full_orchestra")
        instruments: Dictionary mapping instrument names to (Instrument, count) tuples
    """
    name: str
    instruments: Dict[str, tuple[Instrument, int]] = field(default_factory=dict)

    def add_instrument(self, instrument: Instrument, count: int = 1) -> None:
        """Add an instrument to the ensemble."""
        pass

    def remove_instrument(self, instrument_name: str) -> None:
        """Remove an instrument from the ensemble."""
        pass

    def get_instrument(self, name: str) -> Optional[Instrument]:
        """Get an instrument by name."""
        pass

    def get_instruments_by_family(self, family: InstrumentFamily) -> List[Instrument]:
        """Get all instruments of a specific family."""
        pass

    def get_melody_instruments(self) -> List[Instrument]:
        """Get instruments typically used for melody (violin, flute, oboe, trumpet)."""
        pass

    def get_harmony_instruments(self) -> List[Instrument]:
        """Get instruments typically used for harmony (viola, cello, woodwinds)."""
        pass

    def get_bass_instruments(self) -> List[Instrument]:
        """Get instruments typically used for bass (cello, bass, bassoon, tuba)."""
        pass

    def total_instruments(self) -> int:
        """Return the total number of instruments (counting multiples)."""
        pass

    @classmethod
    def preset(cls, preset_name: str) -> 'Ensemble':
        """
        Create an ensemble from a preset template.

        Preset names:
            - "string_quartet": 2 violins, viola, cello
            - "string_orchestra": violins I, violins II, violas, cellos, basses
            - "woodwind_quartet": flute, oboe, clarinet, bassoon
            - "full_orchestra": strings, woodwinds, brass, percussion
            - "chamber_orchestra": reduced forces
            - "brass_section": trumpets, horns, trombones, tuba
        """
        pass
```

#### 4.2 Preset Implementations

```python
# String Quartet
{
    "violin_i": (ORCHESTRAL_INSTRUMENTS["violin"], 1),
    "violin_ii": (ORCHESTRAL_INSTRUMENTS["violin"], 1),
    "viola": (ORCHESTRAL_INSTRUMENTS["viola"], 1),
    "cello": (ORCHESTRAL_INSTRUMENTS["cello"], 1),
}

# String Orchestra
{
    "violin_i": (ORCHESTRAL_INSTRUMENTS["violin"], 8),
    "violin_ii": (ORCHESTRAL_INSTRUMENTS["violin"], 6),
    "viola": (ORCHESTRAL_INSTRUMENTS["viola"], 4),
    "cello": (ORCHESTRAL_INSTRUMENTS["cello"], 4),
    "double_bass": (ORCHESTRAL_INSTRUMENTS["double_bass"], 2),
}

# Full Orchestra
{
    # Strings
    "violin_i": (ORCHESTRAL_INSTRUMENTS["violin"], 8),
    "violin_ii": (ORCHESTRAL_INSTRUMENTS["violin"], 6),
    "viola": (ORCHESTRAL_INSTRUMENTS["viola"], 4),
    "cello": (ORCHESTRAL_INSTRUMENTS["cello"], 4),
    "double_bass": (ORCHESTRAL_INSTRUMENTS["double_bass"], 2),
    # Woodwinds (pairs)
    "flute": (ORCHESTRAL_INSTRUMENTS["flute"], 2),
    "oboe": (ORCHESTRAL_INSTRUMENTS["oboe"], 2),
    "clarinet": (ORCHESTRAL_INSTRUMENTS["clarinet"], 2),
    "bassoon": (ORCHESTRAL_INSTRUMENTS["bassoon"], 2),
    # Brass
    "trumpet": (ORCHESTRAL_INSTRUMENTS["trumpet"], 2),
    "french_horn": (ORCHESTRAL_INSTRUMENTS["french_horn"], 2),
    "trombone": (ORCHESTRAL_INSTRUMENTS["trombone"], 2),
    # Percussion
    "timpani": (ORCHESTRAL_INSTRUMENTS["timpani"], 1),
}
```

### Task 5: Implement the Texture Class

The Texture class defines how instruments are combined musically:

```python
from enum import Enum
from typing import List

class TextureType(Enum):
    """Types of musical texture."""
    HOMOPHONIC = "homophhonic"  # Melody with chordal accompaniment
    POLYPHONIC = "polyphonic"   # Multiple independent melodies
    MONOPHONIC = "monophonic"   # Single melody line
    MELODY_ACCOMPANIMENT = "melody_accompaniment"  # Melody + accompaniment
    PAD = "pad"                 # Sustained chords
    OSTINATO = "ostinato"       # Repeated pattern

@dataclass
class Texture:
    """
    Defines how instruments are combined musically.

    Attributes:
        texture_type: The type of texture
        melody_instruments: List of instruments playing the melody
        harmony_instruments: List of instruments playing harmony
        bass_instruments: List of instruments playing bass
        countermelody_instruments: List of instruments playing countermelody
    """
    texture_type: TextureType
    melody_instruments: List[str] = field(default_factory=list)
    harmony_instruments: List[str] = field(default_factory=list)
    bass_instruments: List[str] = field(default_factory=list)
    countermelody_instruments: List[str] = field(default_factory=list)

    @classmethod
    def homophonic(cls, melody_instruments: List[str], harmony_instruments: List[str],
                   bass_instruments: Optional[List[str]] = None) -> 'Texture':
        """Create a homophonic texture (melody with chordal accompaniment)."""
        pass

    @classmethod
    def polyphonic(cls, instruments: List[str]) -> 'Texture':
        """Create a polyphonic texture (multiple independent melodies)."""
        pass

    @classmethod
    def melody_and_accompaniment(cls, melody_instrument: str,
                                  accompaniment_instruments: List[str]) -> 'Texture':
        """Create a melody + accompaniment texture."""
        pass

    @classmethod
    def pad(cls, instruments: List[str]) -> 'Texture':
        """Create a pad texture (sustained chords)."""
        pass

    @classmethod
    def orchestral_unison(cls, instruments: List[str]) -> 'Texture':
        """Create an orchestral unison (multiple instruments playing same melody)."""
        pass

    def get_all_instruments(self) -> List[str]:
        """Return all instruments involved in this texture."""
        pass
```

### Task 6: Implement Doubling Rules

Doubling defines when instruments play the same material:

```python
@dataclass
class Doubling:
    """
    Defines instrument doubling configurations.

    Attributes:
        primary_instrument: The main instrument
        doubling_instruments: List of instruments doubling the primary
        interval: Interval at which to double (0=unison, 12=octave)
    """
    primary_instrument: str
    doubling_instruments: List[tuple[str, int]]  # (instrument_name, interval)

    @classmethod
    def octave_double(cls, primary: str, doubling: List[str]) -> 'Doubling':
        """Create octave doubling configuration."""
        pass

    @classmethod
    def unison_double(cls, primary: str, doubling: List[str]) -> 'Doubling':
        """Create unison doubling configuration."""
        pass

    @classmethod
    def orchestral_doublings(cls) -> Dict[str, List[tuple[str, int]]]:
        """
        Return common orchestral doublings.

        Returns:
            Dictionary of primary instruments to their common doublings.
        """
        return {
            "flute": [("piccolo", 24), ("violin_i", 12)],
            "oboe": [("clarinet", 0), ("violin_ii", 12)],
            "violin_i": [("flute", 12)],
            "trumpet": [("flute", 12), ("oboe", 12)],
            "cello": [("bassoon", 12), ("double_bass", -12)],
            "french_horn": [("viola", 0)],
        }
```

### Task 7: Dynamic Balance Factors

Implement dynamic adjustment based on instrument balance:

```python
INSTRUMENT_LOUDNESS_FACTORS = {
    # Relative loudness at the same dynamic marking (1.0 = reference)
    "violin": 1.0,
    "viola": 0.85,
    "cello": 0.9,
    "double_bass": 0.7,
    "flute": 0.75,
    "piccolo": 0.8,
    "oboe": 0.85,
    "clarinet": 0.8,
    "bassoon": 0.75,
    "trumpet": 1.2,
    "french_horn": 1.0,
    "trombone": 1.1,
    "tuba": 1.0,
    "timpani": 1.3,
    "harp": 0.5,
}

def balance_velocity(instrument_name: str, base_velocity: int) -> int:
    """
    Adjust velocity based on instrument's relative loudness.

    Args:
        instrument_name: Name of the instrument
        base_velocity: Base MIDI velocity

    Returns:
        Adjusted MIDI velocity
    """
    factor = INSTRUMENT_LOUDNESS_FACTORS.get(instrument_name, 1.0)
    adjusted = int(base_velocity * factor)
    return max(0, min(127, adjusted))
```

## File Structure

Create the following files:

```
src/musicgen/orchestration/
    __init__.py       # Module exports
    instruments.py    # Instrument class and library
    ensembles.py      # Ensemble and Texture classes
```

Update `src/musicgen/__init__.py` to include:
```python
from .orchestration import (
    Instrument,
    InstrumentFamily,
    Ensemble,
    Texture,
    TextureType,
    ORCHESTRAL_INSTRUMENTS,
)
```

## Test Requirements

Create `tests/test_instruments.py`:

```python
import pytest
from musicgen.orchestration import Instrument, InstrumentFamily, ORCHESTRAL_INSTRUMENTS
from musicgen.core import Note

def test_instrument_creation():
    violin = Instrument(
        name="violin",
        family=InstrumentFamily.STRINGS,
        lowest_note="G3",
        highest_note="A7"
    )
    assert violin.name == "violin"
    assert violin.family == InstrumentFamily.STRINGS
    assert violin.transposition == 0

def test_instrument_range_checking():
    violin = ORCHESTRAL_INSTRUMENTS["violin"]
    assert violin.in_range(Note("A4"))
    assert violin.in_range(Note("G3"))  # Lowest note
    assert not violin.in_range(Note("E3"))  # Below range

def test_transposition():
    clarinet = ORCHESTRAL_INSTRUMENTS["clarinet"]
    # Bb clarinet sounds major 2nd lower
    written = Note("C4")
    concert = clarinet.written_to_concert(written)
    assert concert.name == "Bb"
    assert concert.octave == 3

def test_double_bass_octave_transposition():
    bass = ORCHESTRAL_INSTRUMENTS["double_bass"]
    # Bass sounds octave lower
    written = Note("C3")
    concert = bass.written_to_concert(written)
    assert concert.name == "C"
    assert concert.octave == 2

def test_clamp_to_range():
    flute = ORCHESTRAL_INSTRUMENTS["flute"]
    # C4 is in flute range
    note = Note("C4")
    clamped = flute.clamp_to_range(note)
    assert clamped.name == "C"
    assert clamped.octave == 4

    # C3 is below flute range
    low_note = Note("C3")
    clamped = flute.clamp_to_range(low_note)
    assert clamped.octave == 4  # Moved up an octave

def test_dynamic_range():
    violin = ORCHESTRAL_INSTRUMENTS["violin"]
    assert violin.effective_dynamic("f") > violin.effective_dynamic("p")
    assert 30 <= violin.effective_dynamic("pp") <= 50
    assert 100 <= violin.effective_dynamic("ff") <= 127

def test_all_instruments_valid():
    """Ensure all predefined instruments have valid ranges."""
    for name, instrument in ORCHESTRAL_INSTRUMENTS.items():
        assert instrument.lowest_midi < instrument.highest_midi
        assert 0 <= instrument.lowest_midi <= 127
        assert 0 <= instrument.highest_midi <= 127

def test_instrument_families():
    """Check that instruments are assigned to correct families."""
    assert ORCHESTRAL_INSTRUMENTS["violin"].family == InstrumentFamily.STRINGS
    assert ORCHESTRAL_INSTRUMENTS["flute"].family == InstrumentFamily.WOODWINDS
    assert ORCHESTRAL_INSTRUMENTS["trumpet"].family == InstrumentFamily.BRASS
    assert ORCHESTRAL_INSTRUMENTS["timpani"].family == InstrumentFamily.PERCUSSION
```

Create `tests/test_ensembles.py`:

```python
import pytest
from musicgen.orchestration import (
    Ensemble, Texture, TextureType, InstrumentFamily,
    ORCHESTRAL_INSTRUMENTS
)

def test_string_quartet_preset():
    quartet = Ensemble.preset("string_quartet")
    assert quartet.name == "string_quartet"
    assert quartet.total_instruments() == 4
    assert "violin" in quartet.get_instruments_by_family(InstrumentFamily.STRINGS)

def test_add_remove_instrument():
    ensemble = Ensemble(name="test")
    violin = ORCHESTRAL_INSTRUMENTS["violin"]
    ensemble.add_instrument(violin, 2)
    assert ensemble.total_instruments() == 2

    ensemble.remove_instrument("violin")
    assert ensemble.total_instruments() == 0

def test_get_instruments_by_family():
    orchestra = Ensemble.preset("full_orchestra")
    strings = orchestra.get_instruments_by_family(InstrumentFamily.STRINGS)
    assert len(strings) > 0
    assert all(i.family == InstrumentFamily.STRINGS for i in strings)

def test_melody_instruments():
    orchestra = Ensemble.preset("full_orchestra")
    melody = orchestra.get_melody_instruments()
    assert len(melody) > 0
    # Check for typical melody instruments
    names = [i.name for i in melody]
    assert "violin" in names or "flute" in names

def test_bass_instruments():
    orchestra = Ensemble.preset("full_orchestra")
    bass = orchestra.get_bass_instruments()
    assert len(bass) > 0
    names = [i.name for i in bass]
    assert "cello" in names or "double_bass" in names

def test_homophonic_texture():
    texture = Texture.homophonic(
        melody_instruments=["violin_i"],
        harmony_instruments=["viola", "cello"],
        bass_instruments=["cello"]
    )
    assert texture.texture_type == TextureType.HOMOPHONIC
    assert "violin_i" in texture.melody_instruments
    assert "viola" in texture.harmony_instruments

def test_polyphonic_texture():
    texture = Texture.polyphonic(instruments=["violin_i", "violin_ii", "viola"])
    assert texture.texture_type == TextureType.POLYPHONIC
    assert len(texture.get_all_instruments()) == 3

def test_melody_accompaniment_texture():
    texture = Texture.melody_and_accompaniment(
        melody_instrument="flute",
        accompaniment_instruments=["violin_i", "viola", "cello"]
    )
    assert texture.texture_type == TextureType.MELODY_ACCOMPANIMENT
    assert texture.melody_instruments == ["flute"]

def test_orchestral_unison():
    texture = Texture.orchestral_unison(
        instruments=["flute", "oboe", "violin_i"]
    )
    assert len(texture.get_all_instruments()) == 3
```

## Validation Criteria

After implementation, verify these behaviors:

```python
# 1. Instrument range checking
violin = ORCHESTRAL_INSTRUMENTS["violin"]
assert violin.in_range(Note("A4"))
assert not violin.in_range(Note("E3"))

# 2. Transposition
clarinet = ORCHESTRAL_INSTRUMENTS["clarinet"]
written = Note("C4")
concert = clarinet.written_to_concert(written)
assert concert.name == "Bb"
assert concert.octave == 3

# 3. Ensemble preset
quartet = Ensemble.preset("string_quartet")
assert len(quartet.instruments) == 4
assert quartet.total_instruments() == 4

# 4. Texture creation
texture = Texture.homophonic(
    melody_instruments=["violin_i"],
    harmony_instruments=["viola", "cello"]
)
assert texture.texture_type == TextureType.HOMOPHONIC
```

## Dependencies on Previous Steps

This step depends on:

1. **Step 1 (Core)**: Uses `Note` class for pitch representation and duration constants
2. **Step 2 (Scales/Keys)**: May reference key signatures for transposition calculations

The Note class must have:
- `name` property: Note name (C, D, E, etc.)
- `octave` property: Octave number
- `midi_number` property: MIDI note number (60 = C4)

## Success Criteria

Step 6 is complete when:

1. All `Instrument` class methods are implemented and tested
2. `ORCHESTRAL_INSTRUMENTS` dictionary contains at least 15 instruments
3. `Ensemble.preset()` creates valid ensembles
4. `Texture` class methods create valid texture configurations
5. All tests pass: `pytest tests/test_instruments.py tests/test_ensembles.py`
6. Test coverage is at least 80% for the orchestration module

## Notes

- Use `@dataclass` for cleaner class definitions
- The MIDI program numbers follow General MIDI standard
- Instrument ranges are practical ranges, not absolute extremes
- Transposition is positive when the written pitch is higher than concert pitch
- Dynamic balance factors are approximate and can be adjusted based on testing
- Articulations are stored as strings for later expansion
