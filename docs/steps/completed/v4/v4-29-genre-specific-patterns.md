# V4-29: Genre Specific Patterns

## Overview

Create pattern libraries specific to each musical genre.

## Objectives

1. Define genre-specific drum patterns
2. Define genre-specific bass patterns
3. Define genre-specific chord progressions
4. Define genre-specific melodic patterns

## Pattern Libraries

```yaml
genre_patterns:

  # Rock patterns
  rock:
    drums:
      basic_8th: "kick x . x . | snare . . x . | hihat x x x x"
      basic_16th: "kick x . x . x . x . x . | hihat x x x x x x x x"
      halftime: "kick x . . . x . . ."
    bass:
      root_8th: "1 _ 1 _ 1 _ 1 _"
      root_5th: "1 _ 5 _ 1 _ 5 _"
    guitar:
      power_chords: "[I5 V5] [I5 V5] [iv5 V5] [I5 V5]"

  # Jazz patterns
  jazz:
    drums:
      basic_swing: "ride: x x x x | kick: x . . . | snare: . . x ."
      brushes: "snare: brush_sweep"
    bass:
      walking: "1 2 3 5 | 1 2 3 b7"  # Scale tones
      bossa: "1 _ 5 _ 3 _ b7 _ 5 _"
    piano:
      comping: "chords: [3 5 b7 9] [3 5 b7 9]"

  # Electronic patterns
  electronic:
    techno:
      kick: "x . . . x . . ."
      hat: ". x . . . x . ."
      clap: ". . . . x . . ."
    house:
      kick: "x . . . x . . ."
      hat: "x x x x x x x x"
    drum_and_bass:
      breakbeat: "[16th notes fast]"
```

## Files to Create

- `resources/genre_patterns.yaml`
- `src/musicgen/genres/patterns.py`

## Success Criteria

- [ ] All genres have patterns
- [ ] Patterns in mini-notation
- [ ] Cross-referenced with genre profiles

## Next Steps

After completion, proceed to V4-30: Style Transfer System
