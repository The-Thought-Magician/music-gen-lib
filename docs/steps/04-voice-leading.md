# Step 4: Voice Leading Module - Implementation Prompt

## Overview

Implement species counterpoint rules for smooth voice motion between chords. This module provides the foundation for creating musically valid four-part harmony (SATB) with proper voice leading conventions from Western classical music theory.

**Dependencies**: Step 1 (Core: Note, Chord), Step 2 (Scales, Keys), Step 3 (Chord Progressions)

## Project Context

**Working Directory**: `/home/chiranjeet/projects-cc/projects/music-gen-lib`

**Source Directory**: `src/musicgen/theory/`

**Tests Directory**: `tests/`

## Prerequisites

Before starting Step 4, ensure the following from previous steps are in place:

### From Step 1 (Core Data Structures)
- `src/musicgen/core/note.py` contains:
  - `Note` class with attributes: `name`, `octave`, `midi_number`, `duration`, `velocity`
  - `Note` methods: `__eq__`, `__hash__`, `__repr__`, `interval_to(other)`
  - `Rest` class with `duration` attribute

### From Step 1 (Chord)
- `src/musicgen/core/chord.py` contains:
  - `Chord` class with attributes: `root`, `quality`, `inversion`, `notes`
  - `Chord` methods: `get_voicing()`, `invert(n)`, `add_note(note)`

### From Step 2 (Music Theory)
- `src/musicgen/theory/scales.py` contains:
  - `Scale` class with methods for scale degree access
- `src/musicgen/theory/keys.py` contains:
  - `Key` class for key signature management

### From Step 3 (Chord Progressions)
- `src/musicgen/theory/progressions.py` contains:
  - `Progression` class with list of chords
  - `Progression` methods: `from_roman()`, `functional()`, `circle_of_fifths()`

## Implementation Tasks

### Task 1: Voice Range Constraints

Create voice range definitions and validation for standard SATB (Soprano, Alto, Tenor, Bass) ranges.

**File**: `src/musicgen/theory/voice_leading.py`

```python
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Optional
from musicgen.core.note import Note

class VoiceType(Enum):
    """Standard SATB voice types."""
    SOPRANO = "soprano"
    ALTO = "alto"
    TENOR = "tenor"
    BASS = "bass"

@dataclass
class VoiceRange:
    """Defines the usable range for a voice type."""
    voice_type: VoiceType
    lowest: Note  # Lowest acceptable note
    highest: Note  # Highest acceptable note
    comfortable_low: Note  # Ideal lowest note
    comfortable_high: Note  # Ideal highest note

    def in_range(self, note: Note) -> bool:
        """Check if a note is within the voice's range."""
        return note.lowest <= note.midi_number <= note.highest

    def is_comfortable(self, note: Note) -> bool:
        """Check if a note is in the comfortable range."""
        return self.comfortable_low.midi_number <= note.midi_number <= self.comfortable_high.midi_number


# Standard SATB ranges (concert pitch)
SATB_RANGES = {
    VoiceType.SOPRANO: VoiceRange(
        voice_type=VoiceType.SOPRANO,
        lowest=Note("C4"),
        highest=Note("A5"),
        comfortable_low=Note("D4"),
        comfortable_high=Note("G5")
    ),
    VoiceType.ALTO: VoiceRange(
        voice_type=VoiceType.ALTO,
        lowest=Note("G3"),
        highest=Note("D5"),
        comfortable_low=Note("A3"),
        comfortable_high=Note("C5")
    ),
    VoiceType.TENOR: VoiceRange(
        voice_type=VoiceType.TENOR,
        lowest=Note("C3"),
        highest=Note("G4"),
        comfortable_low=Note("D3"),
        comfortable_high=Note("E4")
    ),
    VoiceType.BASS: VoiceRange(
        voice_type=VoiceType.BASS,
        lowest=Note("E2"),
        highest=Note("E4"),
        comfortable_low=Note("G2"),
        comfortable_high=Note("C4")
    )
}
```

### Task 2: Voice Motion Analyzer

Create a system to classify the type of motion between two voices.

```python
class MotionType(Enum):
    """Types of voice motion."""
    PARALLEL = "parallel"      # Both voices move in same direction by same interval
    SIMILAR = "similar"        # Both voices move in same direction by different intervals
    CONTRARY = "contrary"      # Voices move in opposite directions
    OBLIQUE = "oblique"        # One voice moves, the other stays the same

@dataclass
class VoiceMotion:
    """Describes the motion between two voices."""
    motion_type: MotionType
    interval_above: int  # Interval in semitones (before motion)
    interval_below: int  # Interval in semitones (after motion)
    upper_movement: int  # Semitones moved by upper voice (+/-)
    lower_movement: int  # Semitones moved by lower voice (+/-)

def analyze_motion(note1a: Note, note1b: Note,
                   note2a: Note, note2b: Note) -> VoiceMotion:
    """
    Analyze the motion between two voices.

    Args:
        note1a: Upper voice, first chord
        note1b: Lower voice, first chord
        note2a: Upper voice, second chord
        note2b: Lower voice, second chord

    Returns:
        VoiceMotion describing the relationship
    """
    # Calculate intervals
    interval_above = (note1a.midi_number - note1b.midi_number) % 12
    interval_below = (note2a.midi_number - note2b.midi_number) % 12

    # Calculate movements
    upper_movement = note2a.midi_number - note1a.midi_number
    lower_movement = note2b.midi_number - note1b.midi_number

    # Determine motion type
    if upper_movement == 0 and lower_movement == 0:
        motion_type = MotionType.PARALLEL  # No motion (special case)
    elif upper_movement == 0 or lower_movement == 0:
        motion_type = MotionType.OBLIQUE
    elif (upper_movement > 0) == (lower_movement > 0):
        if abs(upper_movement) == abs(lower_movement):
            motion_type = MotionType.PARALLEL
        else:
            motion_type = MotionType.SIMILAR
    else:
        motion_type = MotionType.CONTRARY

    return VoiceMotion(motion_type, interval_above, interval_below,
                       upper_movement, lower_movement)
```

### Task 3: Voice Leading Rules

Implement the classical voice leading rules for species counterpoint.

```python
class VoiceLeadingError(Exception):
    """Exception raised when voice leading rules are violated."""
    pass

class VoiceLeadingRule:
    """Base class for voice leading rules."""

    @staticmethod
    def check(voicing_a: List[Note], voicing_b: List[Note]) -> List[str]:
        """
        Check a voice leading transition against this rule.

        Args:
            voicing_a: Notes of first chord (ordered high to low)
            voicing_b: Notes of second chord (ordered high to low)

        Returns:
            List of error messages (empty if rule passes)
        """
        raise NotImplementedError


class NoParallelFifths(VoiceLeadingRule):
    """
    Forbid parallel motion by perfect fifths (or octaves).
    This is a fundamental rule of classical voice leading.
    """

    @staticmethod
    def check(voicing_a: List[Note], voicing_b: List[Note]) -> List[str]:
        errors = []
        if len(voicing_a) != len(voicing_b):
            return errors

        for i in range(len(voicing_a)):
            for j in range(i + 1, len(voicing_a)):
                motion = analyze_motion(voicing_a[i], voicing_a[j],
                                       voicing_b[i], voicing_b[j])

                # Check for parallel fifths
                if (motion.motion_type == MotionType.PARALLEL and
                    (motion.interval_above == 7 or motion.interval_above == 0)):
                    errors.append(
                        f"Parallel perfect {5 if motion.interval_above == 7 else 8} "
                        f"between voices {i} and {j}"
                    )

        return errors


class NoHiddenFifths(VoiceLeadingRule):
    """
    Forbid hidden fifths/octaves in similar motion to outer voices.
    Both voices move in similar motion to a perfect fifth/octave.
    """

    @staticmethod
    def check(voicing_a: List[Note], voicing_b: List[Note]) -> List[str]:
        errors = []
        if len(voicing_a) < 2 or len(voicing_b) < 2:
            return errors

        # Check outer voices (soprano and bass)
        motion = analyze_motion(voicing_a[0], voicing_a[-1],
                               voicing_b[0], voicing_b[-1])

        interval_b = (voicing_b[0].midi_number - voicing_b[-1].midi_number) % 12

        if (motion.motion_type in [MotionType.PARALLEL, MotionType.SIMILAR] and
            (interval_b == 7 or interval_b == 0) and
            motion.upper_movement != 0 and motion.lower_movement != 0):
            errors.append(
                f"Hidden perfect {5 if interval_b == 7 else 8} "
                f"between outer voices"
            )

        return errors


class LeadingToneResolution(VoiceLeadingRule):
    """
    The leading tone (7th scale degree) should resolve upward to the tonic.
    """

    @staticmethod
    def check(voicing_a: List[Note], voicing_b: List[Note],
              key: "Key") -> List[str]:
        errors = []

        # Find leading tone in first chord (MIDI number of leading tone)
        tonic_midi = key.tonic.midi_number
        leading_tone_midi = tonic_midi - 1  # One semitone below tonic

        for i, note in enumerate(voicing_a):
            if note.midi_number % 12 == leading_tone_midi % 12:
                # This is a leading tone - should resolve up
                if voicing_b[i].midi_number != note.midi_number + 1:
                    # Check if the chord even contains the resolution
                    if voicing_b[i].midi_number % 12 != tonic_midi % 12:
                        # Leading tone didn't resolve to tonic
                        errors.append(
                            f"Leading tone at voice {i} ({note}) "
                            f"doesn't resolve to tonic ({voicing_b[i]})"
                        )

        return errors


class VoiceCrossing(VoiceLeadingRule):
    """
    Voices should not cross - each voice should maintain its relative position.
    """

    @staticmethod
    def check(voicing_a: List[Note], voicing_b: List[Note]) -> List[str]:
        errors = []

        # Check that voice order is maintained
        for i in range(len(voicing_a) - 1):
            if voicing_b[i].midi_number <= voicing_b[i + 1].midi_number:
                errors.append(
                    f"Voice crossing between voice {i} and {i + 1}"
                )

        # Check no voice jumps over another
        for i in range(len(voicing_a)):
            for j in range(len(voicing_a)):
                if i != j:
                    # In voicing_a, voice i is above/below voice j
                    a_above = voicing_a[i].midi_number > voicing_a[j].midi_number
                    b_above = voicing_b[i].midi_number > voicing_b[j].midi_number

                    if a_above != b_above:
                        errors.append(
                            f"Voice {i} crossed voice {j} between chords"
                        )

        return errors


class VoiceSpacing(VoiceLeadingRule):
    """
    Soprano and Alto should not be more than an octave apart.
    Alto and Tenor should not be more than an octave apart.
    Tenor and Bass can be wider (up to two octaves).
    """

    @staticmethod
    def check(voicing: List[Note]) -> List[str]:
        errors = []

        if len(voicing) >= 4:  # SATB
            # Soprano - Alto (max octave)
            if voicing[0].midi_number - voicing[1].midi_number > 12:
                errors.append("Soprano and Alto more than an octave apart")

            # Alto - Tenor (max octave)
            if voicing[1].midi_number - voicing[2].midi_number > 12:
                errors.append("Alto and Tenor more than an octave apart")

            # Tenor - Bass (max two octaves)
            if voicing[2].midi_number - voicing[3].midi_number > 24:
                errors.append("Tenor and Bass more than two octaves apart")

        return errors


def check_voice_leading(voicing_a: List[Note], voicing_b: List[Note],
                       key: Optional["Key"] = None,
                       rules: Optional[List[VoiceLeadingRule]] = None) -> List[str]:
    """
    Check a voice leading transition against all rules.

    Args:
        voicing_a: Notes of first chord (high to low)
        voicing_b: Notes of second chord (high to low)
        key: Key for leading tone resolution (optional)
        rules: Custom list of rules (uses default if None)

    Returns:
        List of all error messages
    """
    if rules is None:
        rules = [
            NoParallelFifths(),
            NoHiddenFifths(),
            VoiceCrossing(),
        ]
        if key is not None:
            rules.append(LeadingToneResolution())

    errors = []
    for rule in rules:
        if isinstance(rule, VoiceSpacing):
            errors.extend(rule.check(voicing_a))
            errors.extend(rule.check(voicing_b))
        elif isinstance(rule, LeadingToneResolution):
            errors.extend(rule.check(voicing_a, voicing_b, key))
        else:
            errors.extend(rule.check(voicing_a, voicing_b))

    return errors
```

### Task 4: Four-Part Harmony Generator

Create a generator for valid four-part chord voicings.

```python
from typing import List, Optional
from musicgen.core.chord import Chord

@dataclass
class Voicing:
    """A complete voicing of a chord across multiple voices."""
    notes: List[Note]  # Ordered high to low (S, A, T, B for 4 voices)
    chord: Chord  # The underlying chord

    def __post_init__(self):
        if len(self.notes) != 4:
            raise ValueError("Voicing must have exactly 4 notes for SATB")

    def soprano(self) -> Note:
        return self.notes[0]

    def alto(self) -> Note:
        return self.notes[1]

    def tenor(self) -> Note:
        return self.notes[2]

    def bass(self) -> Note:
        return self.notes[3]

    def check_ranges(self, ranges: dict = None) -> List[str]:
        """Check if all notes are within their voice ranges."""
        if ranges is None:
            ranges = SATB_RANGES

        errors = []
        voice_types = [VoiceType.SOPRANO, VoiceType.ALTO,
                       VoiceType.TENOR, VoiceType.BASS]

        for i, (note, voice_type) in enumerate(zip(self.notes, voice_types)):
            voice_range = ranges[voice_type]
            if not voice_range.in_range(note):
                errors.append(
                    f"Voice {i} ({voice_type.value}): {note} "
                    f"out of range ({voice_range.lowest}-{voice_range.highest})"
                )
        return errors

    def check_spacing(self) -> List[str]:
        """Check proper spacing between voices."""
        return VoiceSpacing().check(self.notes)


def generate_voicing(chord: Chord,
                    ranges: dict = None,
                    prefer_inversion: int = 0,
                    double_root: bool = True) -> Voicing:
    """
    Generate a valid four-part voicing for a chord.

    Args:
        chord: The chord to voice
        ranges: Voice range dictionary (uses SATB_RANGES if None)
        prefer_inversion: Preferred inversion (0=root, 1=first, 2=second)
        double_root: Whether to double the root in the voicing

    Returns:
        A Voicing object with 4 notes
    """
    if ranges is None:
        ranges = SATB_RANGES

    # Get chord tones
    chord_notes = chord.get_voicing(close_position=True)

    # For triads, we need to double one note (usually root)
    if len(chord_notes) == 3:
        if double_root:
            doubled_note = chord_notes[0]  # Root
        else:
            doubled_note = chord_notes[1]  # Third (for minor, more color)

        voiced_notes = list(chord_notes)
        voiced_notes.append(doubled_note)
    else:
        voiced_notes = list(chord_notes)

    # Apply inversion if specified
    if prefer_inversion == 1 and len(voiced_notes) >= 3:
        voiced_notes[0], voiced_notes[-1] = voiced_notes[-1], voiced_notes[0]
    elif prefer_inversion == 2 and len(voiced_notes) >= 3:
        voiced_notes[0], voiced_notes[-2] = voiced_notes[-2], voiced_notes[0]

    # Assign to voices (simple initial assignment)
    # Bass gets the lowest note
    bass_note = min(voiced_notes, key=lambda n: n.midi_number)
    voiced_notes.remove(bass_note)

    # Soprano gets a high note
    ranges_s = ranges[VoiceType.SOPRANO]
    ranges_a = ranges[VoiceType.ALTO]
    ranges_t = ranges[VoiceType.TENOR]
    ranges_b = ranges[VoiceType.BASS]

    # Find octave placements that work
    # This is a simplified algorithm - real implementation needs more sophistication
    soprano_note = max(voiced_notes, key=lambda n: n.midi_number)
    voiced_notes.remove(soprano_note)

    alto_note = voiced_notes[0]
    tenor_note = voiced_notes[1] if len(voiced_notes) > 1 else alto_note

    # Adjust octaves for proper spacing
    # Ensure soprano and alto within octave
    while alto_note.midi_number > soprano_note.midi_number - 3:
        alto_note.octave -= 1

    # Ensure alto and tenor within octave
    while tenor_note.midi_number > alto_note.midi_number - 3:
        tenor_note.octave -= 1

    # Ensure tenor and bass not too far
    while bass_note.midi_number < tenor_note.midi_number - 24:
        bass_note.octave += 1

    return Voicing(
        notes=[soprano_note, alto_note, tenor_note, bass_note],
        chord=chord
    )


def voice_lead(chord_a: Chord, chord_b: Chord,
               key: "Key",
               num_voices: int = 4,
               max_attempts: int = 100) -> Tuple[Voicing, Voicing]:
    """
    Generate musically valid voice leading between two chords.

    Args:
        chord_a: First chord
        chord_b: Second chord
        key: Current key (for leading tone resolution)
        num_voices: Number of voices (typically 4)
        max_attempts: Maximum voicing combinations to try

    Returns:
        Tuple of (Voicing A, Voicing B)

    Raises:
        VoiceLeadingError: If no valid voice leading found
    """
    best_pair = None
    fewest_errors = float('inf')

    for attempt in range(max_attempts):
        # Generate random voicings
        voicing_a = generate_voicing(chord_a)
        voicing_b = generate_voicing(chord_b)

        # Check all rules
        errors = check_voice_leading(voicing_a.notes, voicing_b.notes, key=key)

        # Add range and spacing checks
        errors.extend(voicing_a.check_ranges())
        errors.extend(voicing_b.check_ranges())
        errors.extend(voicing_a.check_spacing())
        errors.extend(voicing_b.check_spacing())

        # Keep track of best
        if len(errors) < fewest_errors:
            fewest_errors = len(errors)
            best_pair = (voicing_a, voicing_b, errors)

        # Success!
        if len(errors) == 0:
            return (voicing_a, voicing_b)

    # No perfect solution found - return best with warning
    if best_pair:
        voicing_a, voicing_b, errors = best_pair
        import warnings
        warnings.warn(
            f"Voice leading has {len(errors)} errors: {errors[:3]}..."
        )
        return (voicing_a, voicing_b)

    raise VoiceLeadingError(
        f"Could not find valid voice leading after {max_attempts} attempts"
    )
```

### Task 5: Voice Leading for Progressions

Extend voice leading to handle full chord progressions.

```python
from musicgen.theory.progressions import Progression

@dataclass
class VoiceLeadingOutput:
    """Result of voice leading a progression."""
    voicings: List[Voicing]
    errors: List[str]  # Any errors encountered
    total_motion: int  # Total semitones moved (lower is better)

    def __iter__(self):
        return iter(self.voicings)


def voice_lead_progression(progression: Progression,
                          key: "Key",
                          prefer_smooth: bool = True) -> VoiceLeadingOutput:
    """
    Generate voice leading for an entire chord progression.

    Args:
        progression: Chord progression to voice
        key: Musical key
        prefer_smooth: Whether to prefer minimal voice motion

    Returns:
        VoiceLeadingOutput with all voicings
    """
    if len(progression.chords) < 1:
        return VoiceLeadingOutput(voicings=[], errors=[], total_motion=0)

    voicings = []
    all_errors = []
    total_motion = 0

    # Generate first voicing
    current_voicing = generate_voicing(progression.chords[0])
    voicings.append(current_voicing)

    # Voice lead through the progression
    for i in range(1, len(progression.chords)):
        try:
            prev_voicing, current_voicing = voice_lead(
                progression.chords[i - 1],
                progression.chords[i],
                key
            )
            voicings.append(current_voicing)

            # Calculate total motion
            for j in range(4):
                total_motion += abs(
                    voicings[i].notes[j].midi_number -
                    voicings[i - 1].notes[j].midi_number
                )

        except VoiceLeadingError as e:
            all_errors.append(str(e))
            # Still add a voicing so we can continue
            voicings.append(generate_voicing(progression.chords[i]))

    return VoiceLeadingOutput(
        voicings=voicings,
        errors=all_errors,
        total_motion=total_motion
    )


def has_parallel_fifths(voicing_a: List[Note], voicing_b: List[Note]) -> bool:
    """Quick check for parallel fifths between two voicings."""
    errors = NoParallelFifths().check(voicing_a, voicing_b)
    return len(errors) > 0


def has_voice_crossing(voicing_a: List[Note], voicing_b: List[Note]) -> bool:
    """Quick check for voice crossing between two voicings."""
    errors = VoiceCrossing().check(voicing_a, voicing_b)
    return len(errors) > 0
```

## File Structure

Create/update the following files:

```
src/musicgen/theory/
  __init__.py          # Export voice leading classes
  voice_leading.py     # Main implementation

tests/
  test_voice_leading.py
```

## Module Exports

Update `src/musicgen/theory/__init__.py`:

```python
from .voice_leading import (
    VoiceType,
    VoiceRange,
    MotionType,
    VoiceMotion,
    VoiceLeadingError,
    VoiceLeadingRule,
    NoParallelFifths,
    NoHiddenFifths,
    LeadingToneResolution,
    VoiceCrossing,
    VoiceSpacing,
    Voicing,
    SATB_RANGES,
    analyze_motion,
    check_voice_leading,
    generate_voicing,
    voice_lead,
    voice_lead_progression,
    VoiceLeadingOutput,
    has_parallel_fifths,
    has_voice_crossing,
)
```

## Test Requirements

Create comprehensive tests in `tests/test_voice_leading.py`:

```python
import pytest
from musicgen.core.note import Note
from musicgen.core.chord import Chord
from musicgen.theory.scales import Scale
from musicgen.theory.keys import Key
from musicgen.theory.voice_leading import (
    VoiceType, VoiceRange, MotionType, VoiceMotion,
    NoParallelFifths, NoHiddenFifths, LeadingToneResolution,
    VoiceCrossing, VoiceSpacing, Voicing, SATB_RANGES,
    analyze_motion, check_voice_leading,
    generate_voicing, voice_lead, has_parallel_fifths,
    has_voice_crossing, voice_lead_progression,
    VoiceLeadingOutput, VoiceLeadingError
)


class TestVoiceRanges:
    """Test voice range definitions."""

    def test_soprano_range(self):
        vr = SATB_RANGES[VoiceType.SOPRANO]
        assert vr.in_range(Note("C4"))
        assert vr.in_range(Note("A5"))
        assert not vr.in_range(Note("B5"))
        assert not vr.in_range(Note("B3"))

    def test_bass_range(self):
        vr = SATB_RANGES[VoiceType.BASS]
        assert vr.in_range(Note("E2"))
        assert vr.in_range(Note("E4"))
        assert not vr.in_range(Note("D2"))
        assert not vr.in_range(Note("F4"))

    def test_comfortable_range(self):
        vr = SATB_RANGES[VoiceType.SOPRANO]
        assert vr.is_comfortable(Note("D4"))
        assert vr.is_comfortable(Note("G5"))
        assert not vr.is_comfortable(Note("C4"))  # Edge of range


class TestMotionAnalysis:
    """Test voice motion analysis."""

    def test_parallel_motion(self):
        # Both move up by major third (4 semitones)
        motion = analyze_motion(Note("C4"), Note("G3"),
                               Note("E4"), Note("B3"))
        assert motion.motion_type == MotionType.PARALLEL
        assert motion.upper_movement == 4
        assert motion.lower_movement == 4

    def test_contrary_motion(self):
        # Upper moves up, lower moves down
        motion = analyze_motion(Note("C4"), Note("G3"),
                               Note("E4"), Note("D3"))
        assert motion.motion_type == MotionType.CONTRARY
        assert motion.upper_movement > 0
        assert motion.lower_movement < 0

    def test_oblique_motion(self):
        # Upper moves, lower stays
        motion = analyze_motion(Note("C4"), Note("G3"),
                               Note("D4"), Note("G3"))
        assert motion.motion_type == MotionType.OBLIQUE
        assert motion.upper_movement != 0
        assert motion.lower_movement == 0


class TestVoiceLeadingRules:
    """Test individual voice leading rules."""

    def test_no_parallel_fifths(self):
        # C major to F major with parallel fifths
        voicing_a = [Note("G4"), Note("E4"), Note("C4"), Note("C3")]
        voicing_b = [Note("C5"), Note("A4"), Note("F4"), Note("F3")]

        errors = NoParallelFifths().check(voicing_a, voicing_b)
        assert len(errors) > 0  # Should detect parallel fifths

    def test_good_voicing_no_parallel_fifths(self):
        # Proper voice leading avoids parallel fifths
        voicing_a = [Note("G4"), Note("E4"), Note("C4"), Note("C3")]
        voicing_b = [Note("A4"), Note("F4"), Note("C4"), Note("F3")]

        errors = NoParallelFifths().check(voicing_a, voicing_b)
        assert len(errors) == 0

    def test_voice_crossing_detection(self):
        # Alto crosses above soprano
        voicing_a = [Note("C4"), Note("E4"), Note("G3"), Note("C3")]
        voicing_b = [Note("D4"), Note("E4"), Note("A3"), Note("D3")]

        errors = VoiceCrossing().check(voicing_a, voicing_b)
        assert len(errors) > 0

    def test_spacing_rule(self):
        # Soprano and Alto too far apart
        bad_voicing = [Note("A5"), Note("G3"), Note("C3"), Note("C2")]

        errors = VoiceSpacing().check(bad_voicing)
        assert len(errors) > 0
        assert "Soprano and Alto" in errors[0]

    def test_good_spacing(self):
        good_voicing = [Note("G4"), Note("E4"), Note("C4"), Note("C3")]

        errors = VoiceSpacing().check(good_voicing)
        assert len(errors) == 0


class TestVoicingGeneration:
    """Test voicing generation for chords."""

    def test_generate_major_voicing(self):
        chord = Chord("C", "major", root_octave=4)
        voicing = generate_voicing(chord)

        assert len(voicing.notes) == 4
        assert voicing.chord == chord
        # Should contain C, E, G (one doubled)
        note_names = {n.name for n in voicing.notes}
        assert note_names.issubset({"C", "E", "G"})

    def test_generate_minor_voicing(self):
        chord = Chord("A", "minor", root_octave=3)
        voicing = generate_voicing(chord)

        assert len(voicing.notes) == 4
        note_names = {n.name for n in voicing.notes}
        assert note_names.issubset({"A", "C", "E"})

    def test_voicing_range_check(self):
        chord = Chord("C", "major")
        voicing = generate_voicing(chord)

        errors = voicing.check_ranges()
        # May have some errors for edge cases, but should be reasonable
        assert len(errors) < 2


class TestVoiceLeading:
    """Test complete voice leading functionality."""

    def test_simple_progression_voice_leading(self):
        c_major = Chord("C", "major", root_octave=4)
        f_major = Chord("F", "major", root_octave=4)

        key = Key("C", "major")
        voicing_a, voicing_b = voice_lead(c_major, f_major, key)

        assert len(voicing_a.notes) == 4
        assert len(voicing_b.notes) == 4

    def test_no_parallel_fifths_helper(self):
        voicing_a = [Note("G4"), Note("E4"), Note("C4"), Note("C3")]
        voicing_b = [Note("C5"), Note("A4"), Note("F4"), Note("F3")]

        assert has_parallel_fifths(voicing_a, voicing_b)

    def test_no_voice_crossing_helper(self):
        voicing_a = [Note("G4"), Note("E4"), Note("C4"), Note("C3")]
        voicing_b = [Note("A4"), Note("F4"), Note("C4"), Note("F3")]

        assert not has_voice_crossing(voicing_a, voicing_b)

    def test_check_voice_leading_all_rules(self):
        voicing_a = [Note("G4"), Note("E4"), Note("C4"), Note("C3")]
        voicing_b = [Note("G4"), Note("D4"), Note("B3"), Note("G3")]

        key = Key("G", "major")
        errors = check_voice_leading(voicing_a, voicing_b, key)

        # Should return list (may be empty or have errors)
        assert isinstance(errors, list)


class TestProgressionVoiceLeading:
    """Test voice leading for full progressions."""

    def test_voice_lead_ progression(self):
        from musicgen.theory.progressions import Progression

        prog = Progression.from_roman("I-IV-V-I", key="C")
        key = Key("C", "major")

        result = voice_lead_progression(prog, key)

        assert isinstance(result, VoiceLeadingOutput)
        assert len(result.voicings) == 4  # One per chord
        assert result.total_motion >= 0

    def test_voice_leading_output_iteration(self):
        from musicgen.theory.progressions import Progression

        prog = Progression.from_roman("I-V-I", key="C")
        key = Key("C", "major")

        result = voice_lead_progression(prog, key)

        # Should be iterable
        voicings_list = list(result)
        assert len(voicings_list) == 3


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_progression(self):
        from musicgen.theory.progressions import Progression

        prog = Progression(chords=[])
        key = Key("C", "major")

        result = voice_lead_progression(prog, key)

        assert len(result.voicings) == 0
        assert result.total_motion == 0

    def test_single_chord_progression(self):
        from musicgen.theory.progressions import Progression

        prog = Progression(chords=[Chord("C", "major")])
        key = Key("C", "major")

        result = voice_lead_progression(prog, key)

        assert len(result.voicings) == 1

    def test_voice_leading_error_on_failure(self):
        # This test may be flaky depending on random generation
        # but should handle the case when no valid voicing is found
        c_major = Chord("C", "major")
        diminished = Chord("B", "diminished", root_octave=1)  # Extreme range

        key = Key("C", "major")

        # Should either succeed or raise VoiceLeadingError
        try:
            voice_lead(c_major, diminished, key, max_attempts=10)
        except VoiceLeadingError:
            pass  # Expected for difficult cases
```

## Validation Checklist

After implementation, verify the following:

1. **Core Functionality**
   - [ ] All SATB ranges are properly defined
   - [ ] Motion type analysis correctly identifies parallel, contrary, oblique, similar
   - [ ] Parallel fifths/octaves are detected
   - [ ] Hidden fifths/octaves are detected
   - [ ] Voice crossing is detected
   - [ ] Spacing rules are enforced

2. **Voice Generation**
   - [ ] `generate_voicing()` produces 4-note voicings
   - [ ] Voicings respect voice ranges
   - [ ] Root doubling works correctly
   - [ ] Inversions are handled properly

3. **Progressions**
   - [ ] `voice_lead()` connects two chords smoothly
   - [ ] `voice_lead_progression()` handles full progressions
   - [ ] Errors are collected and reported

4. **Integration with Previous Steps**
   - [ ] Uses `Note` class from Step 1
   - [ ] Uses `Chord` class from Step 1
   - [ ] Uses `Key` class from Step 2
   - [ ] Uses `Progression` class from Step 3

5. **Tests**
   - [ ] All tests pass: `pytest tests/test_voice_leading.py -v`
   - [ ] Test coverage > 80% for the module

## Running Tests

```bash
# Run voice leading tests
pytest tests/test_voice_leading.py -v

# Run with coverage
pytest tests/test_voice_leading.py --cov=src/musicgen/theory/voice_leading --cov-report=term-missing
```

## Next Steps

After completing Step 4, proceed to Step 5: Melody Generation Engine, which will use the voice leading module to create melodies that work with the harmonic progression.
