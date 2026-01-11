# Step 3: Chord Progression Engine - Implementation Prompt

## Overview

This step implements a system for generating musically valid chord progressions based on traditional music theory principles. The progression engine will be used throughout the library for composition, harmonization, and form generation.

**Prerequisites**: Step 1 (Core Data Structures) and Step 2 (Music Theory Module - Scales and Keys) must be completed.

## Project Context

You are implementing the third step of a Python library that generates orchestral instrumental music using rule-based composition (NOT AI). The library produces sheet music (MusicXML/LilyPond) and audio files (WAV/FLAC) from programmatic input.

**Important**: This is a new project. The `src/` directory may not exist yet. You will need to create the full package structure as part of this implementation.

## File Structure

Create the following files:

```
src/musicgen/theory/progressions.py    # Main implementation
tests/test_progressions.py             # Test suite
```

The file should integrate with existing (or to-be-created) modules:

```
src/musicgen/
  __init__.py
  core/
    __init__.py
    note.py          # Note, Rest, duration constants
    chord.py         # Chord class
  theory/
    __init__.py
    scales.py        # Scale class from Step 2
    keys.py          # Key class from Step 2
    progressions.py  # This file (to be created)
```

## Dependencies on Previous Steps

### From Step 1 (Core Data Structures)

Your implementation should expect these classes to be available (or you may need to create them if they don't exist):

```python
# From src/musicgen/core/note.py
class Note:
    """Represents a musical note with pitch and duration."""
    def __init__(self, name: str, octave: int = 4, duration: float = 1.0, velocity: int = 90):
        self.name = name          # "C", "D#", "Bb", etc.
        self.octave = octave      # 0-9
        self.duration = duration  # In quarter notes
        self.velocity = velocity  # 0-127

    @property
    def midi_number(self) -> int:
        """Returns MIDI note number (e.g., C4 = 60)."""

# Duration constants
WHOLE = 4.0
HALF = 2.0
QUARTER = 1.0
EIGHTH = 0.5
SIXTEENTH = 0.25

# Dynamic constants
PP = 30    # pianissimo
P = 50     # piano
MP = 70    # mezzo-piano
MF = 90    # mezzo-forte
F = 110    # forte
FF = 127   # fortissimo

# From src/musicgen/core/chord.py
class Chord:
    """Represents a musical chord."""
    def __init__(self, root: str, quality: str, inversion: int = 0,
                 root_octave: int = 3, duration: float = 4.0):
        self.root = root            # Root note name ("C", "F#", etc.)
        self.quality = quality      # "major", "minor", "diminished", "augmented", "dominant7"
        self.inversion = inversion  # 0=root, 1=first, 2=second
        self.root_octave = root_octave
        self.duration = duration
        self.notes: list[Note] = []  # List of Note objects in the chord

    @property
    def root_name(self) -> str:
        """Returns the root note name (e.g., 'C')."""

    def is_tonic(self) -> bool:
        """Check if this chord functions as a tonic (I)."""
```

### From Step 2 (Scales and Keys)

Your implementation should expect these classes:

```python
# From src/musicgen/theory/scales.py
class Scale:
    """Represents a musical scale."""

    SCALE_PATTERNS = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],  # Natural minor
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "melodic_minor_asc": [0, 2, 3, 5, 7, 9, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "phrygian": [0, 1, 3, 5, 7, 8, 10],
        "lydian": [0, 2, 4, 6, 7, 9, 11],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "locrian": [0, 1, 3, 5, 6, 8, 10],
        "major_pentatonic": [0, 2, 4, 7, 9],
        "minor_pentatonic": [0, 3, 5, 7, 10],
    }

    def __init__(self, root: str, scale_type: str):
        self.root = root
        self.scale_type = scale_type
        self.notes: list[str] = []  # Note names in the scale

    def get_degree(self, degree: int) -> Note:
        """Get a Note object for a scale degree (1-7)."""

    def diatonic_chords(self) -> list[Chord]:
        """Return all diatonic triads in this scale."""
```

## Implementation Requirements

### 1. Roman Numeral Analysis

Implement conversion between Roman numerals and actual chords:

```python
class RomanNumeral:
    """
    Represents a chord using Roman numeral notation.

    Examples:
        I  = Tonic major triad (1st degree)
        ii = Supertonic minor triad (2nd degree)
        iii = Mediant minor triad (3rd degree)
        IV = Subdominant major triad (4th degree)
        V = Dominant major triad (5th degree)
        vi = Submediant minor triad (6th degree)
        vii° = Leading tone diminished triad (7th degree)
        V7 = Dominant seventh chord
    """

    # Roman numerals 1-7
    NUMERALS = {
        1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII"
    }

    def __init__(self, numeral: str, inversion: int = 0,
                 added: str = None, key: str = "C", scale_type: str = "major"):
        """
        Args:
            numeral: Roman numeral (e.g., "I", "ii", "V", "viio")
            inversion: 0=root, 1=first, 2=second inversion
            added: Added intervals (e.g., "7" for seventh)
            key: The key center (e.g., "C", "F#")
            scale_type: "major", "minor", "harmonic_minor", etc.
        """
        self.numeral = numeral
        self.inversion = inversion
        self.added = added  # e.g., "7" for seventh chords
        self.key = key
        self.scale_type = scale_type

    @property
    def degree(self) -> int:
        """Extract scale degree from Roman numeral (1-7)."""

    @property
    def quality(self) -> str:
        """Determine chord quality from scale degree and scale type."""

    def to_chord(self) -> Chord:
        """Convert to a Chord object with actual notes."""

    @classmethod
    def from_string(cls, notation: str, key: str = "C",
                    scale_type: str = "major") -> "RomanNumeral":
        """
        Parse Roman numeral notation.

        Examples:
            "I" -> RomanNumeral("I", ...)
            "V7" -> RomanNumeral("V", added="7", ...)
            "ii6" -> RomanNumeral("ii", inversion=1, ...)
            "iv" -> RomanNumeral("iv", ...)  # lowercase = minor
            "viio" -> RomanNumeral("vii", ...)  # o = diminished
        """
```

### 2. Functional Harmony Labels

Implement functional harmony classification:

```python
class Function(Enum):
    """Harmonic functions in tonal music."""
    TONIC = "T"           # Tonic (I, vi, iii in major)
    SUBDOMINANT = "S"     # Subdominant (IV, ii in major)
    DOMINANT = "D"        # Dominant (V, vii in major)
    SUBMEDIANT = "SM"     # Submediant (vi)
    LEADING_TONE = "LT"   # Leading tone (vii°)


def get_function(chord: Chord, key: str, scale_type: str = "major") -> Function:
    """
    Determine the harmonic function of a chord in a given key.

    In major:
    - Tonic: I, vi, (iii)
    - Subdominant: IV, ii
    - Dominant: V, vii°
    """
```

### 3. Progression Class

Implement the main progression container:

```python
class Progression:
    """
    A sequence of chords forming a harmonic progression.

    Example:
        prog = Progression.from_roman("I-IV-V-I", key="C")
        # Creates: C - F - G - C
    """

    def __init__(self, chords: list[Chord], key: str = "C",
                 scale_type: str = "major", time_signature: str = "4/4"):
        self.chords = chords
        self.key = key
        self.scale_type = scale_type
        self.time_signature = time_signature
        self._annotations: list[str] = []  # Optional analysis labels

    @property
    def length(self) -> int:
        """Number of chords in the progression."""

    def add_chord(self, chord: Chord) -> None:
        """Append a chord to the progression."""

    def insert_chord(self, chord: Chord, position: int) -> None:
        """Insert a chord at a specific position."""

    def remove_chord(self, position: int) -> Chord:
        """Remove and return a chord."""

    def get_chord(self, position: int) -> Chord:
        """Get chord at position (supports negative indexing)."""

    def transpose(self, new_key: str) -> "Progression":
        """
        Transpose the entire progression to a new key.

        Example:
            prog = Progression.from_roman("I-IV-V-I", key="C")
            prog_g = prog.transpose("G")
            # Result: G - C - D - G
        """

    def extend(self, other: "Progression") -> "Progression":
        """Concatenate two progressions."""

    def repeat(self, times: int) -> "Progression":
        """Repeat the progression n times."""

    def to_roman(self) -> str:
        """
        Convert progression to Roman numeral notation.

        Example:
            prog = Progression.from_roman("I-IV-V-I", key="C")
            prog.to_roman() -> "I-IV-V-I"
        """

    def analyze_functions(self) -> list[Function]:
        """Return harmonic function for each chord."""

    def __iter__(self):
        """Iterate over chords."""

    def __len__(self):
        """Return number of chords."""

    def __getitem__(self, index):
        """Index chords."""
```

### 4. Progression Templates

Implement common progression templates:

```python
class ProgressionTemplate:
    """
    Pre-defined progression templates for common harmonic patterns.

    Templates are defined using Roman numerals and can be applied
    to any key.
    """

    # Common progression templates
    TEMPLATES = {
        # Basic cadences
        "authentic": "V-I",
        "authentic_extended": "ii-V-I",
        "plagal": "IV-I",
        "deceptive": "V-vi",
        "half": "I-V",  # or IV-V

        # Common progressions
        "basic": "I-IV-V-I",
        "pop": "I-vi-IV-V",  # Also called "doo-wop"
        "jazz": "ii-V-I",
        "circle_of_fifths": "I-IV-vii-iii-vi-ii-V-I",
        "pachelbel": "I-V-vi-iii-IV-I-IV-V",
        "fifty_six": "I-bVI-bVII-V",  # Rock/pop
        "blues": "I-IV-I-V-I",  # 12-bar basic

        # Classical era progressions
        "mozart_twentysix": "I-V-I-IV-I-V-I-V",  # K.545 opening
        "bach_circle": "I-IV-vii-iii-vi-ii-V-I",

        # Romantic/expressive
        "descending_bass": "I-V-vi-iii-IV-i-ii-V",
        "chromatic_mediant": "I-VI-bIII-VII",  # Chromatic mediants
    }

    @classmethod
    def get(cls, name: str) -> str:
        """Get a template by name."""

    @classmethod
    def list_templates(cls) -> list[str]:
        """Return all available template names."""

    @classmethod
    def apply(cls, template: str, key: str = "C",
              scale_type: str = "major") -> "Progression":
        """
        Apply a template to a specific key.

        Args:
            template: Either a template name or Roman numeral string
            key: The key to apply the template to
            scale_type: "major" or "minor" etc.

        Returns:
            A Progression object
        """
```

Add factory methods to Progression class:

```python
class Progression:
    # ... existing code ...

    @classmethod
    def from_roman(cls, roman_string: str, key: str = "C",
                   scale_type: str = "major") -> "Progression":
        """
        Create a progression from Roman numeral notation.

        Args:
            roman_string: Chords separated by hyphens (e.g., "I-IV-V-I")
            key: The key center
            scale_type: Scale type for determining chord qualities

        Example:
            prog = Progression.from_roman("I-IV-V-I", key="C")
            # Creates progression: C major - F major - G major - C major
        """

    @classmethod
    def from_template(cls, template_name: str, key: str = "C",
                      scale_type: str = "major") -> "Progression":
        """
        Create a progression from a predefined template.

        Example:
            prog = Progression.from_template("pop", key="G")
        """

    @classmethod
    def circle_of_fifths(cls, key: str, length: int = 4,
                         direction: str = "descending") -> "Progression":
        """
        Generate a circle of fifths progression.

        Args:
            key: Starting key
            length: Number of chords
            direction: "descending" (IV->VII->III...) or "ascending" (V->II->VI...)

        Example:
            prog = Progression.circle_of_fifths("C", length=4)
            # C - F - Bb - Eb
        """

    @classmethod
    def functional(cls, key: str, length: int = 8,
                   cadence: str = "authentic",
                   scale_type: str = "major") -> "Progression":
        """
        Generate a functional harmony progression.

        Creates a musically valid progression using functional harmony
        principles, ending with the specified cadence.

        Args:
            key: The tonal center
            length: Number of chords
            cadence: Type of cadence ("authentic", "plagal", "deceptive", "half")
            scale_type: "major" or "minor"

        Example:
            prog = Progression.functional(key="C", length=8, cadence="authentic")
            # Might generate: I - IV - ii - V - I - vi - ii - V - I
        """
```

### 5. Cadence Detection

Implement cadence identification:

```python
class CadenceType(Enum):
    """Types of musical cadences."""
    AUTHENTIC = "authentic"       # V-I (PAC if melody is scale degree 1->1, IAC otherwise)
    PLAGAL = "plagal"             # IV-I
    DECEPTIVE = "deceptive"       # V-vi (in major)
    HALF = "half"                 # I-V or IV-V (ends on V)
    EVaded = "evaded"             # V-vi ( deceptive variant)
    PHRYGIAN = "phrygian"         # iv-V in minor


def detect_cadence(progression: Progression, look_at_end: int = 2) -> CadenceType:
    """
    Detect the type of cadence at the end of a progression.

    Analyzes the final 2-3 chords to identify cadence type based on:
    - Root movement
    - Chord qualities
    - Harmonic functions

    Args:
        progression: The progression to analyze
        look_at_end: Number of final chords to examine

    Returns:
        The detected CadenceType

    Example:
        prog = Progression.from_roman("I-IV-V-I", key="C")
        detect_cadence(prog) -> CadenceType.AUTHENTIC
    """


def has_cadence(progression: Progression, cadence_type: CadenceType) -> bool:
    """Check if progression ends with a specific cadence type."""


def with_cadence(progression: Progression, cadence_type: str,
                 key: str = None) -> "Progression":
    """
    Append a cadence to a progression.

    If the progression already ends with the requested cadence,
    returns it unchanged. Otherwise, adds appropriate chords.

    Args:
        progression: Base progression
        cadence_type: "authentic", "plagal", "deceptive", "half"
        key: Key for the cadence (defaults to progression.key)

    Example:
        prog = Progression.from_roman("I-IV-V", key="C")
        final = with_cadence(prog, "authentic", key="C")
        # Result: I - IV - V - I
    """
```

### 6. Modulation

Implement key modulation capabilities:

```python
class Modulation:
    """
    Handles key modulation in progressions using pivot chords.

    Common modulation targets (from C major):
    - Dominant: G major (V)
    - Subdominant: F major (IV)
    - Relative minor: A minor (vi)
    - Parallel minor: C minor
    - Chromatic mediants: E major, Ab major, etc.
    """

    # Common key relationships
    RELATIONSHIPS = {
        "dominant": 5,      # Up a perfect fifth
        "subdominant": 4,   # Up a perfect fourth
        "relative_minor": -3,  # Down 3 semitones (from major)
        "relative_major": 3,   # Up 3 semitones (from minor)
        "parallel_minor": None,  # Same root, minor quality
        "parallel_major": None,  # Same root, major quality
        "chromatic_mediator_+": None,  # Up major third
        "chromatic_mediator_-": None,  # Down major third
    }

    @staticmethod
    def get_pivot_chords(old_key: str, new_key: str) -> list[RomanNumeral]:
        """
        Find pivot chords common to both keys.

        A pivot chord is diatonic to both the original key
        and the target key, enabling smooth modulation.

        Args:
            old_key: Starting key (e.g., "C")
            new_key: Target key (e.g., "G")

        Returns:
            List of RomanNumerals that work in both keys

        Example:
            Modulation.get_pivot_chords("C", "G")
            # Returns: [I(C)/IV(G), V(C)/I(G), vi(C)/ii(G)]
        """

    @staticmethod
    def modulate(progression: Progression, new_key: str,
                 method: str = "pivot", pivot_chord: str = None) -> "Progression":
        """
        Create a modulation sequence to a new key.

        Args:
            progression: Original progression
            new_key: Target key
            method: "pivot" (uses common chord), "direct" (V of new key),
                    "common_tone" (uses common tone)
            pivot_chord: Optional specific pivot chord (as Roman numeral)

        Returns:
            Extended progression with modulation

        Example:
            prog = Progression.from_roman("I-IV-V-I", key="C")
            modulated = Modulation.modulate(prog, "G", method="pivot")
            # Creates: I-IV-V-I | (pivot) | ii-V-I in G
        """


def circle_progression(start_key: str, steps: int) -> Progression:
    """
    Create a progression following the circle of fifths.

    Each step moves to a key a fifth higher/lower.

    Args:
        start_key: Starting key
        steps: Number of keys to visit

    Example:
        circle_progression("C", 4)
        # C -> F -> Bb -> Eb -> Ab
    """
```

### 7. Progression Analysis

Add analysis methods:

```python
class ProgressionAnalyzer:
    """
    Analyzes chord progressions for various musical properties.
    """

    def __init__(self, progression: Progression):
        self.progression = progression

    def root_movement(self) -> list[int]:
        """
        Calculate root movement between adjacent chords.

        Returns intervals in semitones.

        Example:
            I-IV-V-I in C: 0->5 (up P4), 5->7 (up M2), 7->0 (up P4)
        """

    def has_parallel_fifths(self) -> list[tuple[int, int]]:
        """
        Detect potential parallel fifths in progression.

        Returns indices of problematic chord pairs.
        """

    def voice_leading_difficulty(self) -> float:
        """
        Estimate voice leading difficulty (0-1).

        Considers:
        - Root motion (smooth is easier)
        - Common tones between chords
        - Inversion usage
        """

    def tonal_tension(self) -> list[float]:
        """
        Calculate tonal tension for each chord.

        Dominant function = high tension
        Tonic = low tension
        """

    def suggest_inversions(self) -> Progression:
        """
        Suggest inversions for smoother voice leading.

        Returns a new progression with suggested inversions.
        """

    def analyze(self) -> dict:
        """
        Return comprehensive analysis of the progression.

        Includes:
        - Key center
        - Cadence type
        - Functional labels
        - Tension profile
        - Modulation points
        """
```

## Test Requirements

Create comprehensive tests in `/home/chiranjeet/projects-cc/projects/music-gen-lib/tests/test_progressions.py`:

### Test Structure

```python
import pytest
from musicgen.theory.progressions import (
    Progression,
    RomanNumeral,
    ProgressionTemplate,
    Function,
    CadenceType,
    Modulation,
    ProgressionAnalyzer,
    detect_cadence,
    with_cadence,
    circle_progression,
    get_function,
)
from musicgen.core.note import Note, QUARTER
from musicgen.core.chord import Chord
from musicgen.theory.scales import Scale
```

### Required Test Cases

#### 1. Roman Numeral Tests

```python
class TestRomanNumeral:
    def test_basic_numerals(self):
        """Test basic Roman numeral creation."""
        rn = RomanNumeral("I", key="C", scale_type="major")
        assert rn.degree == 1
        assert rn.quality == "major"

    def test_minor_numerals(self):
        """Test lowercase Roman numerals (minor)."""
        rn = RomanNumeral("ii", key="C", scale_type="major")
        assert rn.degree == 2
        assert rn.quality == "minor"

    def test_diminished_numeral(self):
        """Test diminished symbol."""
        rn = RomanNumeral("vii°", key="C", scale_type="major")
        assert rn.degree == 7
        assert rn.quality == "diminished"

    def test_augmented_numeral(self):
        """Test augmented symbol."""
        rn = RomanNumeral("III+", key="C", scale_type="harmonic_minor")
        assert rn.degree == 3
        assert rn.quality == "augmented"

    def test_inversion(self):
        """Test inversion handling."""
        rn = RomanNumeral("I", inversion=1, key="C")
        assert rn.inversion == 1

    def test_seventh_chords(self):
        """Test seventh chord notation."""
        rn = RomanNumeral("V7", key="C")
        assert rn.numeral == "V"
        assert rn.added == "7"

    def test_from_string(self):
        """Test parsing from string notation."""
        rn = RomanNumeral.from_string("V7", key="C")
        assert rn.numeral == "V"
        assert rn.added == "7"

        rn = RomanNumeral.from_string("ii6", key="C")
        assert rn.numeral == "ii"
        assert rn.inversion == 1

    def test_to_chord(self):
        """Test conversion to Chord object."""
        rn = RomanNumeral("I", key="C", scale_type="major")
        chord = rn.to_chord()
        assert chord.root == "C"
        assert chord.quality == "major"

        rn = RomanNumeral("IV", key="C", scale_type="major")
        chord = rn.to_chord()
        assert chord.root == "F"

    def test_all_diatonic_chords_major(self):
        """Test all diatonic chords in C major."""
        key = "C"
        for numeral, expected_root, expected_quality in [
            ("I", "C", "major"),
            ("ii", "D", "minor"),
            ("iii", "E", "minor"),
            ("IV", "F", "major"),
            ("V", "G", "major"),
            ("vi", "A", "minor"),
            ("vii°", "B", "diminished"),
        ]:
            rn = RomanNumeral(numeral, key=key, scale_type="major")
            chord = rn.to_chord()
            assert chord.root == expected_root
            assert chord.quality == expected_quality

    def test_all_diatonic_chords_minor(self):
        """Test all diatonic chords in A minor."""
        key = "A"
        for numeral, expected_root, expected_quality in [
            ("i", "A", "minor"),
            ("ii°", "B", "diminished"),
            ("III", "C", "major"),
            ("iv", "D", "minor"),
            ("v", "E", "minor"),
            ("VI", "F", "major"),
            ("VII", "G", "major"),
        ]:
            rn = RomanNumeral(numeral, key=key, scale_type="minor")
            chord = rn.to_chord()
            assert chord.root == expected_root
            assert chord.quality == expected_quality
```

#### 2. Progression Tests

```python
class TestProgression:
    def test_create_progression(self):
        """Test basic progression creation."""
        chords = [
            Chord("C", "major"),
            Chord("F", "major"),
            Chord("G", "major"),
            Chord("C", "major"),
        ]
        prog = Progression(chords, key="C")
        assert len(prog) == 4
        assert prog.key == "C"

    def test_from_roman(self):
        """Test creating progression from Roman numerals."""
        prog = Progression.from_roman("I-IV-V-I", key="C")
        assert len(prog) == 4
        assert prog[0].root == "C"
        assert prog[1].root == "F"
        assert prog[2].root == "G"
        assert prog[3].root == "C"

    def test_from_roman_minor(self):
        """Test Roman numerals in minor key."""
        prog = Progression.from_roman("i-iv-V-i", key="Am", scale_type="minor")
        assert prog[0].root == "A"
        assert prog[0].quality == "minor"
        assert prog[1].root == "D"
        assert prog[1].quality == "minor"

    def test_to_roman(self):
        """Test converting progression back to Roman numerals."""
        prog = Progression.from_roman("I-IV-V-I", key="C")
        roman = prog.to_roman()
        assert roman == "I-IV-V-I"

    def test_add_chord(self):
        """Test adding a chord."""
        prog = Progression.from_roman("I-IV", key="C")
        prog.add_chord(Chord("G", "major"))
        assert len(prog) == 3
        assert prog[2].root == "G"

    def test_insert_chord(self):
        """Test inserting a chord."""
        prog = Progression.from_roman("I-V", key="C")
        prog.insert_chord(Chord("F", "major"), 1)
        assert len(prog) == 3
        assert prog[1].root == "F"

    def test_remove_chord(self):
        """Test removing a chord."""
        prog = Progression.from_roman("I-IV-V-I", key="C")
        removed = prog.remove_chord(2)
        assert removed.root == "G"
        assert len(prog) == 3

    def test_transpose(self):
        """Test transposing to new key."""
        prog = Progression.from_roman("I-IV-V-I", key="C")
        transposed = prog.transpose("G")
        assert transposed.key == "G"
        assert transposed[0].root == "G"
        assert transposed[1].root == "C"
        assert transposed[2].root == "D"
        assert transposed[3].root == "G"

    def test_extend(self):
        """Test concatenating progressions."""
        prog1 = Progression.from_roman("I-IV", key="C")
        prog2 = Progression.from_roman("V-I", key="C")
        combined = prog1.extend(prog2)
        assert len(combined) == 4

    def test_repeat(self):
        """Test repeating progression."""
        prog = Progression.from_roman("I-IV-V", key="C")
        repeated = prog.repeat(2)
        assert len(repeated) == 6
        assert repeated[0].root == repeated[3].root

    def test_iteration(self):
        """Test iterating over chords."""
        prog = Progression.from_roman("I-IV-V-I", key="C")
        roots = [chord.root for chord in prog]
        assert roots == ["C", "F", "G", "C"]

    def test_indexing(self):
        """Test indexing and negative indexing."""
        prog = Progression.from_roman("I-IV-V-I", key="C")
        assert prog[0].root == "C"
        assert prog[-1].root == "C"

    def test_functional_generation(self):
        """Test functional harmony generation."""
        prog = Progression.functional(key="C", length=4, cadence="authentic")
        assert len(prog) == 4
        # Should end on tonic
        assert prog[-1].is_tonic()
```

#### 3. Template Tests

```python
class TestProgressionTemplate:
    def test_get_template(self):
        """Test getting predefined templates."""
        template = ProgressionTemplate.get("basic")
        assert template == "I-IV-V-I"

    def test_list_templates(self):
        """Test listing all templates."""
        templates = ProgressionTemplate.list_templates()
        assert "basic" in templates
        assert "pop" in templates
        assert "jazz" in templates
        assert "authentic" in templates

    def test_apply_template(self):
        """Test applying template to key."""
        prog = ProgressionTemplate.apply("basic", key="C")
        assert len(prog) == 4
        assert prog.key == "C"

    def test_pop_template(self):
        """Test the pop progression template."""
        prog = Progression.from_template("pop", key="C")
        assert len(prog) == 4
        assert prog[0].root == "C"  # I
        assert prog[1].root == "A"  # vi
        assert prog[2].root == "F"  # IV
        assert prog[3].root == "G"  # V

    def test_jazz_template(self):
        """Test jazz ii-V-I template."""
        prog = Progression.from_template("jazz", key="C")
        assert len(prog) == 3
        assert prog[0].root == "D"  # ii
        assert prog[0].quality == "minor"
        assert prog[1].root == "G"  # V
        assert prog[2].root == "C"  # I

    def test_circle_of_fifths_template(self):
        """Test circle of fifths progression."""
        prog = Progression.from_template("circle_of_fifths", key="C")
        assert len(prog) == 7
```

#### 4. Cadence Tests

```python
class TestCadences:
    def test_authentic_cadence(self):
        """Test authentic cadence detection."""
        prog = Progression.from_roman("I-IV-V-I", key="C")
        cadence = detect_cadence(prog)
        assert cadence == CadenceType.AUTHENTIC

    def test_plagal_cadence(self):
        """Test plagal cadence detection."""
        prog = Progression.from_roman("I-IV-I", key="C")
        cadence = detect_cadence(prog)
        assert cadence == CadenceType.PLAGAL

    def test_deceptive_cadence(self):
        """Test deceptive cadence detection."""
        prog = Progression.from_roman("I-V-vi", key="C")
        cadence = detect_cadence(prog)
        assert cadence == CadenceType.DECEPTIVE

    def test_half_cadence(self):
        """Test half cadence detection."""
        prog = Progression.from_roman("I-IV-V", key="C")
        cadence = detect_cadence(prog)
        assert cadence == CadenceType.HALF

    def test_with_cadence_authentic(self):
        """Test adding authentic cadence."""
        prog = Progression.from_roman("I-IV-V", key="C")
        final = with_cadence(prog, "authentic", key="C")
        assert len(final) == 4
        assert final[-1].root == "C"

    def test_with_cadence_plagal(self):
        """Test adding plagal cadence."""
        prog = Progression.from_roman("I-IV-V", key="C")
        final = with_cadence(prog, "plagal", key="C")
        assert final[-1].root == "C"
        # Last two should be IV-I
        assert final[-2].root == "F"
```

#### 5. Modulation Tests

```python
class TestModulation:
    def test_pivot_chords_C_to_G(self):
        """Test finding pivot chords from C to G."""
        pivots = Modulation.get_pivot_chords("C", "G")
        # C (I=C, IV=G), Am (vi=C, ii=G), Em (iii=C, vi=G)
        assert len(pivots) > 0

    def test_pivot_chords_C_to_F(self):
        """Test finding pivot chords from C to F."""
        pivots = Modulation.get_pivot_chords("C", "F")
        # C (I=C, V=F), F (IV=C, I=F), Am (vi=C, iii=F)
        assert len(pivots) > 0

    def test_modulate_by_pivot(self):
        """Test modulation using pivot chord."""
        prog = Progression.from_roman("I-IV-V-I", key="C")
        modulated = Modulation.modulate(prog, "G", method="pivot")
        # Should be longer than original
        assert len(modulated) > len(prog)
        # Should end in new key
        assert modulated.chords[-1].root == "G"

    def test_modulate_direct(self):
        """Test direct modulation (V of new key)."""
        prog = Progression.from_roman("I-IV", key="C")
        modulated = Modulation.modulate(prog, "G", method="direct")
        assert modulated.chords[-1].root == "G"

    def test_circle_of_fifths_progression(self):
        """Test circle of fifths progression function."""
        prog = circle_progression("C", 4)
        # C -> F -> Bb -> Eb -> Ab
        assert prog[0].root == "C"
        assert prog[1].root == "F"
```

#### 6. Functional Analysis Tests

```python
class TestFunctionalAnalysis:
    def test_get_function_tonic(self):
        """Test tonic function detection."""
        chord = Chord("C", "major")
        func = get_function(chord, "C", "major")
        assert func == Function.TONIC

    def test_get_function_subdominant(self):
        """Test subdominant function detection."""
        chord = Chord("F", "major")
        func = get_function(chord, "C", "major")
        assert func == Function.SUBDOMINANT

    def test_get_function_dominant(self):
        """Test dominant function detection."""
        chord = Chord("G", "major")
        func = get_function(chord, "C", "major")
        assert func == Function.DOMINANT

    def test_analyze_functions(self):
        """Test analyzing all functions in progression."""
        prog = Progression.from_roman("I-IV-V-I", key="C")
        functions = prog.analyze_functions()
        assert functions[0] == Function.TONIC
        assert functions[1] == Function.SUBDOMINANT
        assert functions[2] == Function.DOMINANT
        assert functions[3] == Function.TONIC
```

#### 7. Analyzer Tests

```python
class TestProgressionAnalyzer:
    def test_root_movement(self):
        """Test root movement calculation."""
        prog = Progression.from_roman("I-IV-V-I", key="C")
        analyzer = ProgressionAnalyzer(prog)
        movement = analyzer.root_movement()
        # I to IV = up P4 = 5 semitones
        # IV to V = up M2 = 2 semitones
        # V to I = up P4 = 5 semitones
        assert len(movement) == 3

    def test_tonal_tension(self):
        """Test tonal tension calculation."""
        prog = Progression.from_roman("I-IV-V-I", key="C")
        analyzer = ProgressionAnalyzer(prog)
        tension = analyzer.tonal_tension()
        assert len(tension) == 4
        # V should have highest tension, I lowest
        assert tension[2] > tension[0]  # V > I
        assert tension[3] < tension[2]  # I < V

    def test_comprehensive_analysis(self):
        """Test comprehensive analysis."""
        prog = Progression.from_roman("I-IV-V-I", key="C")
        analyzer = ProgressionAnalyzer(prog)
        analysis = analyzer.analyze()
        assert "key" in analysis
        assert "cadence" in analysis
        assert "functions" in analysis
```

### Test Fixtures

Create test fixtures for common test data:

```python
@pytest.fixture
def c_major_scale():
    """Return C major scale."""
    return Scale("C", "major")

@pytest.fixture
def basic_progression():
    """Return I-IV-V-I progression in C."""
    return Progression.from_roman("I-IV-V-I", key="C")

@pytest.fixture
def pop_progression():
    """Return I-vi-IV-V progression in C."""
    return Progression.from_roman("I-vi-IV-V", key="C")
```

## Implementation Notes

1. **Error Handling**: Raise appropriate exceptions for invalid inputs:
   - `InvalidRomanNumeralError` for malformed Roman numeral strings
   - `InvalidKeyError` for non-existent keys
   - `InvalidTemplateError` for undefined template names

2. **Type Hints**: Use Python type hints throughout for clarity:
   ```python
   from typing import Optional, List, Dict, Tuple, Union
   ```

3. **Immutability Consider**: Make Progression immutable where possible, or use copy-on-write for operations like transpose().

4. **Documentation**: Include docstrings for all public methods with:
   - Description
   - Args section
   - Returns section
   - Raises section (if applicable)
   - Examples (for complex methods)

5. **Music Theory Rules**:
   - In major keys: I, IV, V are major; ii, iii, vi are minor; vii° is diminished
   - In minor keys: i, iv are minor; III, VI, VII are major; ii° is diminished
   - Follow common voice leading rules when suggesting inversions

## Validation Checklist

After implementation, verify:

- [ ] All Roman numerals (I-vii°) convert correctly to chords
- [ ] All templates produce valid progressions
- [ ] Cadence detection accurately identifies all 4 types
- [ ] Modulation produces valid chord sequences
- [ ] Transposition preserves chord quality relationships
- [ ] All tests pass with >90% coverage
- [ ] Code is documented with docstrings
- [ ] No external dependencies beyond standard library and project modules

## References

See `/home/chiranjeet/projects-cc/projects/music-gen-lib/docs/research.md` for:
- Complete list of common chord progressions
- Music theory fundamentals
- Voice leading rules
- Functional harmony principles

See `/home/chiranjeet/projects-cc/projects/music-gen-lib/docs/plan.md` for:
- Overall project architecture
- Dependencies on other steps
- Integration points
