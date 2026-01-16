# Step 5: Melody Generation Engine - Implementation Prompt

## Overview

This step implements the melody generation engine for the music generation library. The engine uses rule-based composition techniques (not AI) to create musically coherent melodies with motivic development, proper contour, and phrase structure.

## Dependencies

This step depends on the following previous steps being completed:

- **Step 1 (Core Data Structures)**: `Note`, `Chord`, `Rest`, duration constants
- **Step 2 (Scales and Keys)**: `Scale` class with scale degree access
- **Step 3 (Chord Progressions)**: `Progression` class with chord sequences
- **Step 4 (Voice Leading)**: Voice motion analysis and constraints

### Required Imports

```python
from musicgen.core.note import Note, Rest
from musicgen.core.chord import Chord
from musicgen.theory.scales import Scale
from musicgen.theory.progressions import Progression
from musicgen.theory.keys import Key
```

## File Structure

Create the following new files:

```
src/musicgen/composition/
├── __init__.py          # Composition module exports
└── melody.py            # Melody generation implementation
tests/
└── test_melody.py       # Comprehensive tests
```

## Implementation Requirements

### 1. Module Structure (`src/musicgen/composition/__init__.py`)

Export the main classes:

```python
"""
Composition module for rule-based music generation.

This module provides melody generation with motivic development,
phrase structure, and melodic contour control.
"""

from musicgen.composition.melody import (
    Melody,
    Motif,
    MelodicContour,
    RhythmPattern,
    Phrase,
    MelodyGenerator,
)

__all__ = [
    "Melody",
    "Motif",
    "MelodicContour",
    "RhythmPattern",
    "Phrase",
    "MelodyGenerator",
]
```

### 2. Melodic Contour Templates (`MelodicContour`)

Create an enum or class defining standard melodic contours:

```python
from enum import Enum

class MelodicContour(Enum):
    """Standard melodic contour patterns for melody generation."""
    ASCENDING = "ascending"      # Overall upward motion
    DESCENDING = "descending"    # Overall downward motion
    ARCH = "arch"               # Rise then fall
    INVERTED_ARCH = "inverted_arch"  # Fall then rise
    WAVE = "wave"               # Alternating up and down
    STATIC = "static"           # Limited pitch range
    ASCENDING_DESCENDING = "ascending_descending"  # Two part contour
```

**Requirements:**
- Each contour should define a target interval pattern
- Contours should be parameterized by range (number of scale degrees)

### 3. Rhythm Pattern Generator (`RhythmPattern`)

Create a class for generating and managing rhythmic patterns:

```python
class RhythmPattern:
    """Represents a rhythmic pattern for melodies."""

    # Predefined rhythm patterns (durations in quarter notes)
    PATTERNS = {
        "basic": [1.0, 1.0, 1.0, 1.0],           # Four quarter notes
        "marching": [1.0, 1.0, 0.5, 0.5],         # Two quarters, two eighths
        "waltz": [0.5, 0.25, 0.25],               # One quarter, two eighths
        "syncopated": [0.75, 0.25, 0.5, 0.5],     # Dotted eighth, sixteenth, two eighths
        "flowing": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],  # Eight eighths
        "suspended": [2.0, 1.0, 0.5, 0.5],        # Half, quarter, two eighths
        "pointillist": [0.25, 0.25, 0.25, 0.25, 0.5, 0.5],  # Four sixteenths, two eighths
        "breathing": [1.5, 0.5, 1.0, 1.0],        # Dotted quarter, eighth, two quarters
    }

    def __init__(self, durations: list[float]):
        """Initialize with a list of durations (in quarter notes)."""
        self.durations = durations

    @classmethod
    def from_preset(cls, name: str) -> "RhythmPattern":
        """Create a pattern from a predefined preset name."""
        if name not in cls.PATTERNS:
            raise ValueError(f"Unknown rhythm pattern: {name}")
        return cls(cls.PATTERNS[name].copy())

    def total_beats(self) -> float:
        """Return the total number of beats in this pattern."""
        return sum(self.durations)

    def repeat(self, times: int) -> "RhythmPattern":
        """Return a new pattern with this one repeated."""
        return RhythmPattern(self.durations * times)

    def reverse(self) -> "RhythmPattern":
        """Return a new pattern with durations reversed."""
        return RhythmPattern(self.durations[::-1])

    def vary(self, variation_type: str = "subtle") -> "RhythmPattern":
        """
        Create a varied version of this pattern.

        Args:
            variation_type: "subtle", "moderate", or "radical"
        """
        # Implementation should vary some durations slightly
        # while maintaining the overall character
        pass
```

### 4. Motif Class (`Motif`)

Implement a motif (short melodic idea) class with development capabilities:

```python
class Motif:
    """
    A motif is a short melodic idea that can be developed.

    A motif typically contains 3-7 notes and has a recognizable
    rhythmic and melodic character.
    """

    def __init__(
        self,
        notes: list[Note | Rest],
        contour: MelodicContour = MelodicContour.WAVE,
        name: str | None = None,
    ):
        """
        Initialize a motif.

        Args:
            notes: List of notes and/or rests
            contour: The melodic contour of this motif
            name: Optional name for identification
        """
        self.notes = notes
        self.contour = contour
        self.name = name or f"motif_{id(self)}"

    @property
    def length(self) -> int:
        """Return the number of notes (excluding rests)."""
        return len([n for n in self.notes if isinstance(n, Note)])

    @property
    def total_duration(self) -> float:
        """Return the total duration in quarter notes."""
        return sum(n.duration for n in self.notes)

    @property
    def interval_pattern(self) -> list[int]:
        """
        Return the pattern of intervals between consecutive notes.

        Returns a list of semitone intervals. Rests are skipped.
        """
        pattern = []
        prev_note = None
        for item in self.notes:
            if isinstance(item, Note):
                if prev_note is not None:
                    pattern.append(item.midi_number - prev_note.midi_number)
                prev_note = item
        return pattern

    @property
    def rhythm_pattern(self) -> list[float]:
        """Return the rhythm as a list of durations."""
        return [item.duration for item in self.notes]

    def transpose(self, interval: int) -> "Motif":
        """
        Transpose the motif by a given interval (in semitones).

        Args:
            interval: Number of semitones to transpose (positive = up)

        Returns:
            A new Motif with transposed notes
        """
        new_notes = []
        for item in self.notes:
            if isinstance(item, Note):
                new_notes.append(item.transpose(interval))
            else:
                new_notes.append(item)
        return Motif(new_notes, self.contour, f"{self.name}_transposed")

    def invert(self, axis: Note | None = None) -> "Motif":
        """
        Invert the motif around an axis note.

        If no axis is specified, uses the first note as axis.

        Args:
            axis: The note to invert around (defaults to first note)

        Returns:
            A new Motif with inverted intervals
        """
        if axis is None:
            for item in self.notes:
                if isinstance(item, Note):
                    axis = item
                    break

        if axis is None:
            return Motif(self.notes.copy(), self.contour, f"{self.name}_inverted")

        new_notes = []
        for item in self.notes:
            if isinstance(item, Note):
                # Invert around axis: new = axis - (old - axis) = 2*axis - old
                new_interval = axis.midi_number - item.midi_number
                new_note = Note.from_midi(axis.midi_number + new_interval, item.duration)
                new_notes.append(new_note)
            else:
                new_notes.append(item)

        return Motif(new_notes, self.contour, f"{self.name}_inverted")

    def retrograde(self) -> "Motif":
        """
        Return the motif in reverse order (retrograde).

        Returns:
            A new Motif with notes in reverse order
        """
        return Motif(
            self.notes[::-1],
            self.contour,
            f"{self.name}_retrograde"
        )

    def develop(
        self,
        method: str = "sequence",
        **kwargs
    ) -> "Motif":
        """
        Develop the motif using a specific development technique.

        Args:
            method: Development method - one of:
                - "sequence": Transposed repetition
                - "inversion": Interval inversion
                - "retrograde": Reverse order
                - "augmentation": Double the durations
                - "diminution": Halve the durations
                - "fragmentation": Use only part of the motif
                - "ornamentation": Add decorative notes
            **kwargs: Method-specific arguments

        Returns:
            A new Motif developed from this one
        """
        if method == "sequence":
            interval = kwargs.get("interval", 5)  # Default: up a fifth
            return self.transpose(interval)

        elif method == "inversion":
            axis = kwargs.get("axis")
            return self.invert(axis)

        elif method == "retrograde":
            return self.retrograde()

        elif method == "augmentation":
            new_notes = []
            for item in self.notes:
                if isinstance(item, Note):
                    new_note = Note(item.name, item.octave, item.duration * 2)
                    new_notes.append(new_note)
                else:
                    new_notes.append(Rest(item.duration * 2))
            return Motif(new_notes, self.contour, f"{self.name}_augmented")

        elif method == "diminution":
            new_notes = []
            for item in self.notes:
                if isinstance(item, Note):
                    new_note = Note(item.name, item.octave, item.duration / 2)
                    new_notes.append(new_note)
                else:
                    new_notes.append(Rest(item.duration / 2))
            return Motif(new_notes, self.contour, f"{self.name}_diminished")

        elif method == "fragmentation":
            start = kwargs.get("start", 0)
            end = kwargs.get("end", len(self.notes) // 2)
            return Motif(
                self.notes[start:end],
                self.contour,
                f"{self.name}_fragment"
            )

        elif method == "ornamentation":
            # Add passing tones between leaps
            new_notes = []
            for i, item in enumerate(self.notes):
                new_notes.append(item)
                if isinstance(item, Note) and i < len(self.notes) - 1:
                    next_item = self.notes[i + 1]
                    if isinstance(next_item, Note):
                        interval = abs(next_item.midi_number - item.midi_number)
                        if interval >= 4:  # Add passing tone for larger leaps
                            passing_midi = (item.midi_number + next_item.midi_number) // 2
                            passing_note = Note.from_midi(
                                passing_midi,
                                item.duration / 2
                            )
                            new_notes.append(passing_note)
            return Motif(new_notes, self.contour, f"{self.name}_ornamented")

        else:
            raise ValueError(f"Unknown development method: {method}")

    def related_to(self, other: "Motif") -> bool:
        """
        Check if this motif is melodically related to another.

        Two motifs are related if they share similar interval patterns
        or rhythmic patterns.

        Args:
            other: Another Motif to compare with

        Returns:
            True if motifs are related
        """
        # Check if interval patterns are similar (allowing for transposition)
        self_intervals = self.interval_pattern
        other_intervals = other.interval_pattern

        if len(self_intervals) != len(other_intervals):
            return False

        # Check if patterns match or are inversions
        direct_match = self_intervals == other_intervals
        inverted_match = self_intervals == [-i for i in other_intervals]

        return direct_match or inverted_match

    @classmethod
    def generate(
        cls,
        scale: Scale,
        length: int = 5,
        contour: MelodicContour = MelodicContour.WAVE,
        rhythm: RhythmPattern | None = None,
        octave_range: tuple[int, int] = (4, 5),
    ) -> "Motif":
        """
        Generate a new motif using the given parameters.

        Args:
            scale: The scale to use for note selection
            length: Number of notes to generate
            contour: The melodic contour to follow
            rhythm: Optional rhythm pattern (defaults to even eighths)
            octave_range: (min_octave, max_octave) for the motif

        Returns:
            A new Motif instance
        """
        pass  # Implementation detail
```

### 5. Phrase Class (`Phrase`)

Implement a musical phrase (typically 4-8 measures) with structure:

```python
class Phrase:
    """
    A musical phrase is a complete musical thought.

    Phrases are typically 4-8 measures and often have a
    question-answer (antecedent-consequent) structure.
    """

    def __init__(
        self,
        notes: list[Note | Rest],
        phrase_type: str = "antecedent",  # or "consequent"
        cadence: str | None = None,
    ):
        """
        Initialize a phrase.

        Args:
            notes: List of notes and/or rests
            phrase_type: "antecedent" (question) or "consequent" (answer)
            cadence: Type of cadence ending this phrase
        """
        self.notes = notes
        self.phrase_type = phrase_type
        self.cadence = cadence

    @property
    def length(self) -> int:
        """Return the number of notes."""
        return len([n for n in self.notes if isinstance(n, Note)])

    @property
    def total_duration(self) -> float:
        """Return total duration in quarter notes."""
        return sum(n.duration for n in self.notes)

    @property
    def contour(self) -> str:
        """
        Analyze and return the melodic contour.

        Returns one of: ascending, descending, arch, inverted_arch, wave
        """
        # Get the pitch classes of notes
        pitches = [n.midi_number for n in self.notes if isinstance(n, Note)]

        if len(pitches) < 2:
            return "static"

        start = pitches[0]
        mid = pitches[len(pitches) // 2]
        end = pitches[-1]
        highest = max(pitches)
        lowest = min(pitches)

        # Determine contour based on pitch relationships
        if start < end and abs(highest - mid) < 3:
            return "ascending"
        elif start > end and abs(lowest - mid) < 3:
            return "descending"
        elif start < end and highest == mid:
            return "inverted_arch"
        elif start > end and lowest == mid:
            return "arch"
        else:
            return "wave"

    def is_period_partner(self, other: "Phrase") -> bool:
        """
        Check if this phrase forms a period with another phrase.

        A period is two phrases where the first ends with a weak cadence
        and the second ends with a strong cadence.

        Args:
            other: Another Phrase to check for period formation

        Returns:
            True if these phrases form a period
        """
        # Antecedent should end on weak cadence (half)
        # Consequent should end on strong cadence (authentic)
        return (
            self.phrase_type == "antecedent" and
            other.phrase_type == "consequent" and
            self.cadence in ["half", "deceptive"] and
            other.cadence in ["authentic", "perfect"]
        )
```

### 6. Melody Class (`Melody`)

The main melody class combining phrases and motifs:

```python
class Melody:
    """
    A complete melody composed of one or more phrases.

    Melodies have contour, rhythm, and typically relate to
    an underlying chord progression.
    """

    def __init__(
        self,
        notes: list[Note | Rest],
        scale: Scale,
        phrases: list[Phrase] | None = None,
        contour: MelodicContour = MelodicContour.WAVE,
        name: str | None = None,
    ):
        """
        Initialize a melody.

        Args:
            notes: List of notes and/or rests
            scale: The scale this melody is based on
            phrases: Optional list of Phrase objects
            contour: The overall melodic contour
            name: Optional name for this melody
        """
        self.notes = notes
        self.scale = scale
        self.phrases = phrases or []
        self.contour = contour
        self.name = name or f"melody_{id(self)}"

    @property
    def length(self) -> int:
        """Return the number of notes."""
        return len([n for n in self.notes if isinstance(n, Note)])

    @property
    def total_duration(self) -> float:
        """Return total duration in quarter notes."""
        return sum(n.duration for n in self.notes)

    @property
    def range(self) -> int:
        """
        Return the melodic range in semitones.

        The difference between the highest and lowest notes.
        """
        pitches = [n.midi_number for n in self.notes if isinstance(n, Note)]
        if not pitches:
            return 0
        return max(pitches) - min(pitches)

    @property
    def centroid(self) -> int:
        """
        Return the average pitch (centroid) in MIDI number.

        Useful for determining register and balance.
        """
        pitches = [n.midi_number for n in self.notes if isinstance(n, Note)]
        if not pitches:
            return 60
        return sum(pitches) // len(pitches)

    def align_to_chords(
        self,
        chords: list[Chord],
        chord_changes: list[int],
    ) -> "Melody":
        """
        Adjust melody notes to better align with chord changes.

        Args:
            chords: List of chords in the progression
            chord_changes: Indices of notes where chords change

        Returns:
            A new Melody with adjusted notes
        """
        # Ensure notes on chord changes are chord tones
        new_notes = self.notes.copy()

        for change_idx in chord_changes:
            if change_idx < len(new_notes):
                note = new_notes[change_idx]
                if isinstance(note, Note):
                    chord_idx = min(chord_changes.index(change_idx), len(chords) - 1)
                    chord = chords[chord_idx]

                    # If note is not in chord, adjust to nearest chord tone
                    if not chord.contains_note(note):
                        chord_tone = chord.nearest_note(note)
                        new_notes[change_idx] = chord_tone

        return Melody(
            new_notes,
            self.scale,
            self.phrases,
            self.contour,
            f"{self.name}_aligned"
        )

    def get_motif(self, start: int = 0, length: int = 5) -> Motif:
        """
        Extract a motif from the melody.

        Args:
            start: Starting index
            length: Number of notes to extract

        Returns:
            A Motif extracted from this melody
        """
        end = min(start + length, len(self.notes))
        notes = self.notes[start:end]
        return Motif(notes, self.contour, f"{self.name}_motif")

    def add_development(
        self,
        motif: Motif,
        method: str = "sequence",
        position: int = -1,
    ) -> "Melody":
        """
        Add a developed version of a motif to the melody.

        Args:
            motif: The motif to develop
            method: Development method (see Motif.develop)
            position: Where to insert (-1 = append)

        Returns:
            A new Melody with the developed motif added
        """
        developed = motif.develop(method)

        if position == -1:
            new_notes = self.notes + developed.notes
        else:
            new_notes = self.notes.copy()
            for note in developed.notes:
                new_notes.insert(position, note)

        return Melody(
            new_notes,
            self.scale,
            self.phrases,
            self.contour,
            f"{self.name}_developed"
        )

    @classmethod
    def generate(
        cls,
        scale: Scale,
        progression: Progression | None = None,
        length: int = 16,
        contour: MelodicContour = MelodicContour.WAVE,
        rhythm: RhythmPattern | str | None = None,
        octave_range: tuple[int, int] = (4, 5),
        use_motivic_development: bool = True,
    ) -> "Melody":
        """
        Generate a complete melody.

        Args:
            scale: The scale for note selection
            progression: Optional chord progression to align with
            length: Number of notes to generate
            contour: The melodic contour to follow
            rhythm: Rhythm pattern or preset name
            octave_range: (min, max) octave range
            use_motivic_development: Whether to use motivic development

        Returns:
            A new Melody instance
        """
        # Implementation should:
        # 1. Generate initial motif
        # 2. Develop motif if enabled
        # 3. Apply contour
        # 4. Align to chord progression if provided
        # 5. Ensure notes are in scale
        # 6. Apply interval constraints
        pass
```

### 7. Melody Generator Class (`MelodyGenerator`)

A comprehensive class for generating melodies with various parameters:

```python
class MelodyGenerator:
    """
    Generator for creating melodies with various constraints and styles.

    This class provides high-level control over melody generation
    including mood-based presets and detailed parameter control.
    """

    # Maximum allowed intervals (in semitones) for melodic motion
    MAX_INTERVALS = {
        "step": 2,          # Major second
        "skip": 4,          # Major third
        "leap": 12,         # Octave
        "reasonable": 7,    # Perfect fifth
    }

    def __init__(
        self,
        scale: Scale,
        key: Key,
        tempo: float = 120.0,
    ):
        """
        Initialize the melody generator.

        Args:
            scale: The scale for note selection
            key: The key for tonal center
            tempo: Tempo in BPM
        """
        self.scale = scale
        self.key = key
        self.tempo = tempo
        self._rng = random.Random()  # Use seeded random for reproducibility

    def set_seed(self, seed: int) -> None:
        """Set random seed for reproducible generation."""
        self._rng.seed(seed)

    def generate_motif(
        self,
        length: int = 5,
        contour: MelodicContour = MelodicContour.WAVE,
        rhythm: RhythmPattern | None = None,
        octave_range: tuple[int, int] = (4, 5),
        allow_leaps: bool = True,
    ) -> Motif:
        """
        Generate a single motif.

        Args:
            length: Number of notes
            contour: Melodic contour
            rhythm: Rhythm pattern (defaults to eighths)
            octave_range: (min_octave, max_octave)
            allow_leaps: Whether to allow intervals larger than a skip

        Returns:
            A generated Motif
        """
        pass

    def generate_phrase(
        self,
        length_measures: int = 4,
        time_signature: tuple[int, int] = (4, 4),
        phrase_type: str = "antecedent",
        end_cadence: str | None = None,
    ) -> Phrase:
        """
        Generate a musical phrase.

        Args:
            length_measures: Number of measures (usually 4 or 8)
            time_signature: (beats_per_measure, beat_unit)
            phrase_type: "antecedent" or "consequent"
            end_cadence: Type of cadence for phrase ending

        Returns:
            A generated Phrase
        """
        pass

    def generate_period(
        self,
        length_measures: int = 8,
        time_signature: tuple[int, int] = (4, 4),
    ) -> tuple[Phrase, Phrase]:
        """
        Generate a period (antecedent + consequent phrases).

        Args:
            length_measures: Total length (each phrase is half)
            time_signature: Time signature

        Returns:
            Tuple of (antecedent_phrase, consequent_phrase)
        """
        antecedent = self.generate_phrase(
            length_measures=length_measures // 2,
            time_signature=time_signature,
            phrase_type="antecedent",
            end_cadence="half",
        )
        consequent = self.generate_phrase(
            length_measures=length_measures // 2,
            time_signature=time_signature,
            phrase_type="consequent",
            end_cadence="authentic",
        )
        return antecedent, consequent

    def generate_melody(
        self,
        progression: Progression,
        contour: MelodicContour = MelodicContour.WAVE,
        form_structure: str = "period",  # "period", "sentence", "parallel"
        motivic_unity: float = 0.7,  # 0-1, how much to reuse motifs
    ) -> Melody:
        """
        Generate a complete melody over a chord progression.

        Args:
            progression: Chord progression for the melody
            contour: Overall melodic contour
            form_structure: Formal structure type
            motivic_unity: Degree of motivic development (0-1)

        Returns:
            A complete Melody
        """
        pass

    def _select_note(
        self,
        contour: MelodicContour,
        previous_note: Note | None,
        octave_range: tuple[int, int],
        chord: Chord | None = None,
        max_interval: int = 7,
    ) -> Note:
        """
        Select the next note based on contour and constraints.

        Args:
            contour: The desired contour direction
            previous_note: The previous note (for interval calculation)
            octave_range: Allowed octave range
            chord: Optional chord for chord tone preference
            max_interval: Maximum allowed interval in semitones

        Returns:
            A selected Note
        """
        pass

    def _check_interval_validity(
        self,
        interval: int,
        allow_leaps: bool = True,
    ) -> bool:
        """
        Check if an interval is melodically valid.

        Rules:
        - Steps (1-2 semitones) are always valid
        - Skips (3-4 semitones) are always valid
        - Leaps (5+ semitones) require careful handling
        - Intervals > octave should be rare
        - Augmented/diminished intervals should be avoided

        Args:
            interval: Interval in semitones
            allow_leaps: Whether to allow leaps

        Returns:
            True if interval is valid
        """
        pass

    def _resolve_leap(self, from_note: Note, to_note: Note) -> Note | None:
        """
        After a leap, suggest a step in the opposite direction.

        This is a fundamental rule of melodic writing:
        large leaps should be followed by stepwise motion
        in the opposite direction.

        Args:
            from_note: The note before the leap
            to_note: The landing note of the leap

        Returns:
            Suggested next note, or None if no specific suggestion
        """
        pass
```

## Melodic Constraints and Rules

### Interval Constraints

Implement these rules for melodic intervals:

```python
# Valid melodic intervals by category
VALID_INTERVALS = {
    "step": [1, 2],           # Minor second, Major second
    "skip": [3, 4],           # Minor third, Major third
    "small_leap": [5, 6],     # Perfect fourth, tritone (use sparingly)
    "large_leap": [7, 8, 9, 10, 11, 12],  # Fifth through octave
}

# Rules:
# 1. Steps and skips should comprise ~80% of intervals
# 2. Leaps should be followed by stepwise motion in opposite direction
# 3. Consecutive leaps in same direction should be avoided
# 4. Tritones should resolve properly
# 5. Seventh intervals should resolve stepwise
```

### Scale-Based Note Selection

Implement weighted random selection favoring:

```python
NOTE_WEIGHTS = {
    "tonic": 3.0,        # Most stable
    "dominant": 2.5,     # Strong tendency
    "subdominant": 2.0,  # Moderate stability
    "other": 1.0,        # Less stable
}

# Chord tones (when chord present) get 2x weight
# Non-harmonic tones: passing, neighbor, suspension, escape
```

### Rhythmic Constraints

```python
# Rhythmic principles:
# 1. Longest notes typically at phrase endings
# 2. Repeated rhythms create motivic identity
# 3. Syncopation should be used sparingly (10-20% of notes)
# 4. Rests should mark phrase boundaries
# 5. Note duration should correlate with harmonic rhythm
```

## Test Requirements

Create comprehensive tests in `tests/test_melody.py`:

### 1. MelodicContour Tests

```python
def test_melodic_contour_enum():
    """Test that all contour types are defined."""
    assert MelodicContour.DESCENDING.value == "descending"
    assert MelodicContour.ARCH.value == "arch"
    assert MelodicContour.WAVE.value == "wave"
```

### 2. RhythmPattern Tests

```python
def test_rhythm_pattern_from_preset():
    """Test creating rhythm patterns from presets."""
    pattern = RhythmPattern.from_preset("basic")
    assert pattern.durations == [1.0, 1.0, 1.0, 1.0]
    assert pattern.total_beats() == 4.0

def test_rhythm_pattern_repeat():
    """Test pattern repetition."""
    pattern = RhythmPattern.from_preset("waltz")
    repeated = pattern.repeat(2)
    assert len(repeated.durations) == 6

def test_rhythm_pattern_reverse():
    """Test pattern reversal."""
    pattern = RhythmPattern([1.0, 0.5, 0.5, 1.0])
    reversed_pattern = pattern.reverse()
    assert reversed_pattern.durations == [1.0, 0.5, 0.5, 1.0]
```

### 3. Motif Tests

```python
def test_motif_creation():
    """Test basic motif creation."""
    notes = [
        Note("C4", QUARTER),
        Note("D4", QUARTER),
        Note("E4", HALF),
    ]
    motif = Motif(notes)
    assert motif.length == 3
    assert motif.total_duration == 2.0

def test_motif_transpose():
    """Test motif transposition."""
    notes = [Note("C4", QUARTER), Note("E4", QUARTER)]
    motif = Motif(notes)
    transposed = motif.transpose(5)  # Up a perfect fourth
    assert transposed.notes[0].name == "F"
    assert transposed.notes[1].name == "A"

def test_motif_inversion():
    """Test motif inversion."""
    notes = [Note("C4", QUARTER), Note("E4", QUARTER), Note("G4", QUARTER)]
    motif = Motif(notes)
    inverted = motif.invert()
    # First note stays same, intervals are inverted
    assert inverted.notes[0].name == "C"
    assert inverted.notes[1].name == "Ab"  # Inverted major third

def test_motif_retrograde():
    """Test retrograde (reverse order)."""
    notes = [Note("C4", QUARTER), Note("D4", QUARTER), Note("E4", QUARTER)]
    motif = Motif(notes)
    retrograde = motif.retrograde()
    assert retrograde.notes[0].name == "E"
    assert retrograde.notes[2].name == "C"

def test_motif_development_sequence():
    """Test motivic development by sequence."""
    motif = Motif([Note("C4", QUARTER), Note("D4", QUARTER)])
    developed = motif.develop("sequence", interval=5)
    assert developed.related_to(motif)

def test_motif_development_augmentation():
    """Test motivic development by augmentation."""
    motif = Motif([Note("C4", QUARTER), Note("D4", QUARTER)])
    augmented = motif.develop("augmentation")
    assert augmented.notes[0].duration == HALF
    assert augmented.notes[1].duration == HALF

def test_motif_development_diminution():
    """Test motivic development by diminution."""
    motif = Motif([Note("C4", QUARTER), Note("D4", QUARTER)])
    diminished = motif.develop("diminution")
    assert diminished.notes[0].duration == EIGHTH
    assert diminished.notes[1].duration == EIGHTH

def test_motif_related_to():
    """Test motif relationship detection."""
    motif1 = Motif([Note("C4", QUARTER), Note("D4", QUARTER), Note("E4", QUARTER)])
    motif2 = Motif([Note("G4", QUARTER), Note("A4", QUARTER), Note("B4", QUARTER)])
    assert motif2.related_to(motif1)  # Same pattern, different key
```

### 4. Phrase Tests

```python
def test_phrase_creation():
    """Test phrase creation."""
    notes = [Note("C4", QUARTER) for _ in range(4)]
    phrase = Phrase(notes, phrase_type="antecedent")
    assert phrase.length == 4
    assert phrase.phrase_type == "antecedent"

def test_phrase_contour_analysis():
    """Test phrase contour analysis."""
    # Ascending phrase
    notes = [
        Note("C4", QUARTER),
        Note("E4", QUARTER),
        Note("G4", QUARTER),
        Note("C5", QUARTER),
    ]
    phrase = Phrase(notes)
    assert phrase.contour == "ascending"

def test_period_detection():
    """Test period (antecedent-consequent) detection."""
    antecedent = Phrase(
        [Note("C4", QUARTER) for _ in range(4)],
        phrase_type="antecedent",
        cadence="half"
    )
    consequent = Phrase(
        [Note("G4", QUARTER) for _ in range(4)],
        phrase_type="consequent",
        cadence="authentic"
    )
    assert antecedent.is_period_partner(consequent)
```

### 5. Melody Tests

```python
def test_melody_creation():
    """Test basic melody creation."""
    scale = Scale("C", "major")
    notes = [Note("C4", QUARTER), Note("D4", QUARTER), Note("E4", HALF)]
    melody = Melody(notes, scale)
    assert melody.length == 3
    assert melody.total_duration == 2.0

def test_melody_range():
    """Test melody range calculation."""
    scale = Scale("C", "major")
    notes = [
        Note("C4", QUARTER),
        Note("E4", QUARTER),
        Note("G4", QUARTER),
        Note("C5", QUARTER),
    ]
    melody = Melody(notes, scale)
    assert melody.range == 12  # One octave

def test_melody_centroid():
    """Test melody pitch centroid calculation."""
    scale = Scale("C", "major")
    notes = [
        Note("C4", QUARTER),  # MIDI 60
        Note("G4", QUARTER),  # MIDI 67
    ]
    melody = Melody(notes, scale)
    assert melody.centroid == 63  # Average of 60 and 67

def test_melody_alignment():
    """Test melody-to-chord alignment."""
    scale = Scale("C", "major")
    notes = [
        Note("D4", QUARTER),  # Non-chord tone
        Note("F4", QUARTER),
        Note("A4", QUARTER),
        Note("D4", QUARTER),
    ]
    melody = Melody(notes, scale)

    chords = [Chord("C", "major")]
    chord_changes = [0]  # First note should align

    aligned = melody.align_to_chords(chords, chord_changes)
    # First note should now be a chord tone
    assert chords[0].contains_note(aligned.notes[0])

def test_melody_generate():
    """Test melody generation."""
    scale = Scale("C", "major")
    progression = Progression.from_roman("I-IV-V-I", key="C")
    melody = Melody.generate(scale, progression, length=8)

    # Check notes are in scale
    for note in melody.notes:
        if isinstance(note, Note):
            assert note.name in scale.notes

    # Check contour is valid
    assert melody.contour in MelodicContour

def test_melody_motif_extraction():
    """Test extracting motif from melody."""
    scale = Scale("C", "major")
    notes = [Note(f"{n}4", QUARTER) for n in ["C", "D", "E", "F", "G", "A", "B", "C"]]
    melody = Melody(notes, scale)

    motif = melody.get_motif(start=0, length=4)
    assert motif.length == 4
    assert motif.notes[0].name == "C"
```

### 6. MelodyGenerator Tests

```python
def test_generator_initialization():
    """Test generator setup."""
    scale = Scale("C", "major")
    key = Key("C", "major")
    generator = MelodyGenerator(scale, key)
    assert generator.scale == scale
    assert generator.tempo == 120.0

def test_generator_seed_reproducibility():
    """Test that seeding produces reproducible results."""
    scale = Scale("C", "major")
    key = Key("C", "major")

    gen1 = MelodyGenerator(scale, key)
    gen1.set_seed(42)
    motif1 = gen1.generate_motif()

    gen2 = MelodyGenerator(scale, key)
    gen2.set_seed(42)
    motif2 = gen2.generate_motif()

    assert motif1.notes == motif2.notes

def test_generate_motif():
    """Test motif generation."""
    scale = Scale("C", "major")
    key = Key("C", "major")
    generator = MelodyGenerator(scale, key)
    generator.set_seed(42)

    motif = generator.generate_motif(length=5)
    assert motif.length == 5
    # All notes should be in scale
    for note in motif.notes:
        if isinstance(note, Note):
            assert note.name in scale.notes

def test_generate_period():
    """Test period generation."""
    scale = Scale("C", "major")
    key = Key("C", "major")
    generator = MelodyGenerator(scale, key)
    generator.set_seed(42)

    antecedent, consequent = generator.generate_period()
    assert antecedent.phrase_type == "antecedent"
    assert consequent.phrase_type == "consequent"
    assert antecedent.cadence == "half"
    assert consequent.cadence == "authentic"

def test_interval_validity():
    """Test interval validity checking."""
    scale = Scale("C", "major")
    key = Key("C", "major")
    generator = MelodyGenerator(scale, key)

    # Steps should be valid
    assert generator._check_interval_validity(1) == True
    assert generator._check_interval_validity(2) == True

    # Skips should be valid
    assert generator._check_interval_validity(3) == True
    assert generator._check_interval_validity(4) == True

    # Leaps depend on allow_leaps parameter
    assert generator._check_interval_validity(7, allow_leaps=True) == True
    assert generator._check_interval_validity(7, allow_leaps=False) == False
```

### 7. Integration Tests

```python
def test_full_melody_generation_pipeline():
    """Test complete melody generation from scale to melody."""
    scale = Scale("D", "minor")
    key = Key("D", "minor")
    progression = Progression.from_roman("i-iv-VII-i", key="D")

    generator = MelodyGenerator(scale, key, tempo=100)
    melody = generator.generate_melody(progression)

    assert len(melody.notes) > 0
    assert melody.scale == scale

    # Verify all notes are in scale
    for note in melody.notes:
        if isinstance(note, Note):
            assert note.name in scale.notes or \
                   any(note.name == n for n in scale.notes)

def test_mood_based_melody():
    """Test melody generation for different moods."""
    # Epic mood - D minor, faster tempo
    epic_scale = Scale("D", "harmonic_minor")
    epic_key = Key("D", "minor")
    epic_gen = MelodyGenerator(epic_scale, epic_key, tempo=130)

    epic_melody = epic_gen.generate_melody(
        Progression.from_roman("i-iv-VII-i", key="D"),
        contour=MelodicContour.ASCENDING
    )

    # Peaceful mood - G major, slower tempo
    peaceful_scale = Scale("G", "major")
    peaceful_key = Key("G", "major")
    peaceful_gen = MelodyGenerator(peaceful_scale, peaceful_key, tempo=70)

    peaceful_melody = peaceful_gen.generate_melody(
        Progression.from_roman("I-IV-V-I", key="G"),
        contour=MelodicContour.WAVE
    )

    assert epic_melody.total_duration > 0
    assert peaceful_melody.total_duration > 0
```

## Non-Chord Tone Handling

Implement proper non-chord tone (embellishment) handling:

```python
class NonChordTone:
    """Types of non-chord tones (embellishments)."""

    PASSING_TONE = "passing"      # Step between chord tones
    NEIGHBOR_TONE = "neighbor"     # Step away and back to chord tone
    APPOGGIATURA = "appoggiatura"  # Leaped suspension
    SUSPENSION = "suspension"      # Carried over, then resolves down
    RETARDATION = "retardation"    # Carried over, then resolves up
    ESCAPE_TONE = "escape"         # Step away, leap to chord tone
    ANTICIPATION = "anticipation"  # Early arrival of next chord tone
    PEDAL_TONE = "pedal"           # Sustained bass note
```

## Implementation Hints

### 1. Contour Direction Selection

Use the contour to bias random note selection:

```python
def _get_direction_bias(self, contour: MelodicContour, position: float) -> float:
    """
    Get directional bias for note selection based on contour.

    Args:
        contour: The melodic contour
        position: Position in melody (0.0 to 1.0)

    Returns:
        Bias value: -1.0 (down) to 1.0 (up), 0 = neutral
    """
    if contour == MelodicContour.ASCENDING:
        return 0.3
    elif contour == MelodicContour.DESCENDING:
        return -0.3
    elif contour == MelodicContour.ARCH:
        return 0.5 - position  # Start up, end down
    elif contour == MelodicContour.INVERTED_ARCH:
        return position - 0.5   # Start down, end up
    elif contour == MelodicContour.WAVE:
        # Alternating based on position
        return 0.3 * ((position * 4) % 2 - 1)
    else:  # STATIC
        return 0.0
```

### 2. Weighted Note Selection

```python
def _weighted_note_selection(
    self,
    chord: Chord | None,
    previous_note: Note | None,
    direction_bias: float,
) -> Note:
    """Select a note using weighted probabilities."""
    scale_notes = self.scale.get_notes_in_range(octave_range)

    # Calculate weights for each note
    weights = []
    for note in scale_notes:
        weight = 1.0

        # Chord tone bonus
        if chord and chord.contains_note(note):
            weight *= 2.0

        # Scale degree weight
        degree = self.scale.get_degree(note)
        if degree == 1:  # Tonic
            weight *= 3.0
        elif degree == 5:  # Dominant
            weight *= 2.5

        # Direction bias
        if previous_note:
            interval = note.midi_number - previous_note.midi_number
            if (interval > 0 and direction_bias > 0) or \
               (interval < 0 and direction_bias < 0):
                weight *= (1 + abs(direction_bias))

        # Leap penalty
        if previous_note:
            interval = abs(note.midi_number - previous_note.midi_number)
            if interval > 7:
                weight *= 0.5

        weights.append(weight)

    # Weighted random selection
    return random.choices(scale_notes, weights=weights)[0]
```

### 3. Leap Resolution

```python
def _resolve_leap(self, from_note: Note, to_note: Note) -> Note:
    """After a leap, suggest a step in opposite direction."""
    interval = to_note.midi_number - from_note.midi_number

    # For ascending leaps, suggest step down
    if interval > 4:
        return Note.from_midi(to_note.midi_number - 2, to_note.duration)
    # For descending leaps, suggest step up
    elif interval < -4:
        return Note.from_midi(to_note.midi_number + 2, to_note.duration)

    return None
```

## Acceptance Criteria

The implementation is complete when:

1. All classes are implemented with full docstrings
2. All tests pass with at least 85% code coverage
3. Melody generation produces musically coherent output
4. Motivic development creates clearly related material
5. Contours are accurately reflected in generated melodies
6. Chord alignment produces chord tones on strong beats
7. Interval constraints prevent awkward leaps
8. Leap resolution follows voice leading rules
9. Phrase structure creates proper periods
10. Integration tests demonstrate end-to-end functionality

## Example Usage

```python
# Basic melody generation
from musicgen.theory.scales import Scale
from musicgen.theory.keys import Key
from musicgen.theory.progressions import Progression
from musicgen.composition.melody import MelodyGenerator, MelodicContour

scale = Scale("C", "major")
key = Key("C", "major")
progression = Progression.from_roman("I-IV-V-I", key="C")

generator = MelodyGenerator(scale, key, tempo=120)
melody = generator.generate_melody(
    progression,
    contour=MelodicContour.ARCH,
    motivic_unity=0.8
)

# Export or use melody
for note in melody.notes:
    print(note)

# Motivic development example
motif = generator.generate_motif(length=5, contour=MelodicContour.WAVE)
developed = motif.develop("sequence", interval=5)
inverted = motif.develop("inversion")
```

## Next Steps

After completing this step, proceed to **Step 6: Orchestration Module** which will:
- Define instrument characteristics
- Create ensemble presets
- Handle instrument combinations
- Apply appropriate ranges and transpositions
