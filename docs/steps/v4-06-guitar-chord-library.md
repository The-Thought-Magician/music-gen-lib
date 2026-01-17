# V4-06: Guitar Chord Library

## Overview

Create a comprehensive library of guitar chords with proper fingerings, voicings, and practical usage patterns.

## Objectives

1. Define common open chords
2. Define barre chord shapes
3. Define jazz chord voicings
4. Define power chords
5. Create chord lookup and generation utilities
6. Support alternate tunings

## Chord Types

### Open Chords (Standard Tuning)

```yaml
# Open position chords in standard tuning EADGBE
open_chords:
  C_major:
    name: "C"
    quality: "major"
    fingering: [null, 3, 2, 0, 1, 0]  # x32010
    strings: [6, 5, 4, 3, 2, 1]
    fret_range: [0, 3]
    difficulty: "easy"

  A_major:
    name: "A"
    quality: "major"
    fingering: [null, 0, 2, 2, 2, 0]  # x02220
    difficulty: "easy"

  G_major:
    name: "G"
    quality: "major"
    fingering: [3, 2, 0, 0, 0, 3]  # 320003
    difficulty: "easy"

  E_major:
    name: "E"
    quality: "major"
    fingering: [0, 2, 2, 1, 0, 0]  # 022100
    difficulty: "easy"

  D_major:
    name: "D"
    quality: "major"
    fingering: [null, null, 0, 2, 3, 2]  # xx0232
    difficulty: "easy"

  A_minor:
    name: "Am"
    quality: "minor"
    fingering: [null, 0, 2, 2, 1, 0]  # x02210
    difficulty: "easy"

  E_minor:
    name: "Em"
    quality: "minor"
    fingering: [0, 2, 2, 0, 0, 0]  # 022000
    difficulty: "easy"

  D_minor:
    name: "Dm"
    quality: "minor"
    fingering: [null, null, 0, 2, 3, 1]  # xx0231
    difficulty: "medium"
```

### Barre Chord Shapes (Movable)

```yaml
barre_chords:
  E_shape_major:
    name: "E Shape (Major)"
    root_string: 6  # Low E string
    root_fret: 0  # Relative to root
    fingering: [0, 1, 3, 3, 2, 1]  # Relative to barre position
    barre_fret: 1
    description: "Major barre chord based on E open shape"

  E_shape_minor:
    name: "Em Shape (Minor)"
    root_string: 6
    root_fret: 0
    fingering: [0, 1, 3, 2, 0, 0]
    barre_fret: 1
    description: "Minor barre chord based on Em open shape"

  A_shape_major:
    name: "A Shape (Major)"
    root_string: 5  # A string
    root_fret: 0
    fingering: [null, 0, 2, 2, 2, 0]  # Relative
    barre_fret: 2
    description: "Major barre chord based on A open shape"

  A_shape_minor:
    name: "Am Shape (Minor)"
    root_string: 5
    root_fret: 0
    fingering: [null, 0, 2, 2, 1, 0]
    barre_fret: 2
    description: "Minor barre chord based on Am open shape"
```

### Jazz Chord Voicings

```yaml
jazz_chords:
  major_7th_drop2:
    name: "Maj7 Drop 2"
    root_string: 5
    voicing: "R_5_7_3"  # Root, 5th, 7th, 3rd
    fingerings:
      C_major_7: [null, 3, 2, 0, 0, 0]  # x32000
      F_major_7: [1, 3, 3, 2, 1, 0]  # 133200

  minor_7th_drop2:
    name: "m7 Drop 2"
    root_string: 5
    voicing: "R_b7_3_b3"
    fingerings:
      A_minor_7: [null, 0, 2, 0, 1, 0]  # x02110

  dominant_7th_drop2:
    name: "7 Drop 2"
    root_string: 5
    voicing: "R_b7_3_b3"
    fingerings:
      G7: [null, 0, 2, 0, 1, 0]  # 320001

  half_diminished:
    name: "m7b5 (Half Diminished)"
    root_string: 5
    voicing: "R_b5_b7_b3"
    fingerings:
      Bm7b5: [null, 2, 3, 2, 3, 0]  # x23230
```

### Power Chords

```yaml
power_chords:
  fifth:
    name: "5 (Power Chord)"
    intervals: [1, 5]  # Root, perfect fifth
    fingerings:
      e_shape: [null, 0, 0, 2, 2, 0]  # xx02xx
      a_shape: [null, 0, 2, 2, null, null]  # xx2xxx

  octave:
    name: "Octave (8ve)"
    intervals: [1, 8]  # Root, octave
    fingerings:
      two_string: [null, null, 0, 2, null, null]  # xx0xxx

  sus2:
    name: "sus2"
    intervals: [1, 2, 5]  # Root, second, fifth
    fingerings:
      open: [null, 0, 0, 2, 3, 0]  # xx0230

  sus4:
    name: "sus4"
    intervals: [1, 4, 5]  # Root, fourth, fifth
    fingerings:
      open: [0, 0, 2, 2, 3, 0]  # 002230
```

## Chord Generation System

```python
class GuitarChordGenerator:
    """Generate guitar chord fingerings programmatically"""

    def __init__(self, tuning: list[str] = None):
        self.tuning = tuning or ["E2", "A2", "D3", "G3", "B3", "E4"]

    def generate_barre_chord(
        self,
        root: str,
        quality: str,
        shape: str,  # "E" or "A" shape
        position: int  # Fret number
    ) -> GuitarChord:
        """Generate a barre chord at specified position"""

    def generate_drop2_voicing(
        self,
        root: str,
        quality: str,
        root_string: int
    ) -> GuitarChord:
        """Generate drop-2 jazz voicing"""

    def find_fingering(
        self,
        chord_notes: list[str],
        max_fret_span: int = 4
    ) -> list[int] | None:
        """Find practical fingering for given notes"""

    def is_playable(
        self,
        fingering: list[int | None],
        hand_span: int = 4  # Frets
    ) -> bool:
        """Check if chord is physically playable"""
```

## Chord Progression Patterns

```python
GUITAR_PROGRESSIONS = {
    "pop_rock": [
        ["I", "V", "vi", "IV"],  # I-V-vi-IV
        ["I", "vi", "IV", "V"],  # I-vi-IV-V
        ["I", "V", "vi", "iii"],  # Canon
    ],
    "jazz_ii_v_i": [
        ["ii", "V", "I"],
        ["ii7", "V7", "Imaj7"],
        ["iim7", "V7", "Imaj7"],
    ],
    "jazz_vi_ii_v_i": [
        ["vi", "ii", "V", "I"],
        ["vim7", "iim7", "V7", "Imaj7"],
    ],
    "blues": [
        ["I", "I", "I", "I"],
        ["IV", "IV", "I", "I"],
        ["V", "IV", "I", "V"],
    ],
    "country": [
        ["I", "IV", "I", "V"],
        ["I", "I", "IV", "IV"],
        ["I", "I", "V", "V"],
    ],
}
```

## Files to Create

- `src/musicgen/instruments/chords.py`
- `resources/chord_library.yaml`
- `src/musicgen/instruments/chord_generator.py`

## Success Criteria

- [ ] All common open chords defined
- [ ] Barre chord shapes complete
- [ ] Jazz voicings for common chords
- [ ] Power chords and variations
- [ ] Chord generation system working
- [ ] Lookup by name and by notes
- [ ] Playability validation
- [ ] Alternate tuning support

## Next Steps

After completion, proceed to V4-07: Bass Instrument Definitions
