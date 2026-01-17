# V4-10: Drum Pattern System

## Overview

Create a comprehensive drum pattern system covering all common genres and styles.

## Objectives

1. Define basic drum patterns by genre
2. Create pattern variation system
3. Implement fill generation
4. Implement groove/shank system
5. Create pattern composition utilities

## Pattern Notation

```python
class DrumPattern(BaseModel):
    """Drum pattern definition using mini-notation"""
    name: str
    genre: str
    time_signature: tuple[int, int]  # (numerator, denominator)
    subdivision: int  # 8 = eighth notes, 16 = sixteenth
    pattern: dict[str, str]  # piece_name -> mini-notation
    velocity_map: dict[str, list[int]]  # Custom velocities per piece
    swing: float = 0.0  # Swing amount (0-1)
```

## Rock Patterns

```yaml
drum_patterns:
  rock:
    basic_8th:
      name: "Basic Rock 8th"
      genre: "rock"
      time_signature: [4, 4]
      subdivision: 8
      pattern:
        kick: "x . x . . . x ."  # x = hit, . = rest
        snare: ". . x . . . x ."
        hihat: "x x x x x x x x"
      swing: 0.0

    basic_16th:
      name: "Basic Rock 16th"
      genre: "rock"
      time_signature: [4, 4]
      subdivision: 16
      pattern:
        kick: "x . . . x . . . . . x . . . x ."
        snare: ". . x . . . x . . . x . . . x ."
        hihat: "x x x x x x x x x x x x x x x x"
      swing: 0.0

    hard_rock:
      name: "Hard Rock"
      genre: "rock"
      time_signature: [4, 4]
      subdivision: 16
      pattern:
        kick: "x . x . x . x . x . x . x . x ."
        snare: ". . x . . . x . . . x . . . x ."
        crash: "x . . . . . . . . . . . . . . ."
        ride: ". . . . . . . . x x x x x x x x"
      swing: 0.0

    punk:
      name: "Punk/Fast"
      genre: "punk"
      time_signature: [4, 4]
      subdivision: 8
      bpm_range: [160, 200]
      pattern:
        kick: "x . x . x . x ."
        snare: ". . x . . . x ."
        hihat: "x x x x x x x x"
      swing: 0.0
```

## Pop Patterns

```yaml
  pop:
    basic_pop:
      name: "Basic Pop"
      genre: "pop"
      time_signature: [4, 4]
      subdivision: 16
      pattern:
        kick: "x . . . . . x . . . x . . . . ."
        snare: ". . x . . . . . . . x . . . . ."
        hihat: "x x x x x x x x x x x x x x x x"
      swing: 0.05

    disco:
      name: "Disco"
      genre: "disco"
      time_signature: [4, 4]
      subdivision: 16
      pattern:
        kick: "x . x . x . x . x . x . x . x ."
        snare: ". . . . x . . . . . . . x . . ."
        hihat_open: "x . . . . . . . . . . . . . . ."
        hihat_closed: ". . . . x . . . . . . . x . . ."
      swing: 0.1

    pop_rock:
      name: "Pop Rock"
      genre: "pop"
      time_signature: [4, 4]
      subdivision: 16
      pattern:
        kick: "x . . . x . . . x . . . . . x ."
        snare: ". . x . . . . . . . x . . . x ."
        hihat: "x x x x x x x x x x x x x x x x"
      swing: 0.0
```

## Jazz Patterns

```yaml
  jazz:
    basic_swing:
      name: "Basic Swing"
      genre: "jazz"
      time_signature: [4, 4]
      subdivision: 8  # But played with triplet feel
      pattern:
        kick: "x . . . . . x ."
        snare: ". . x . . . . ."
        ride: "x x x x x x x x"  # Quarter note pattern
      swing: 0.3

    jazz_ride:
      name: "Jazz Ride Pattern"
      genre: "jazz"
      time_signature: [4, 4]
      subdivision: 8
      pattern:
        kick: "x . . . . . x ."
        snare: ". . x . . . . ."
        ride_bell: "x . . . x . . ."
        ride: ". x x x . x x x"
      swing: 0.35

    brushes:
      name: "Brushes"
      genre: "jazz"
      time_signature: [4, 4]
      subdivision: 8
      pattern:
        kick: "x . . . . . x ."
        snare: ". x . x . x . x"  # Sweeping pattern
        hihat: ". . . . . . . ."  # No hihat
      swing: 0.3

    bebop:
      name: "Bebop"
      genre: "jazz"
      time_signature: [4, 4]
      subdivision: 8
      pattern:
        kick: "x x . . x . x ."  # More active
        snare: ". . x . . . x ."
        ride: "x x x x x x x x"
      swing: 0.4
```

## Funk Patterns

```yaml
  funk:
    basic_funk:
      name: "Basic Funk"
      genre: "funk"
      time_signature: [4, 4]
      subdivision: 16
      pattern:
        kick: "x . . x . . x . x . x . . . x ."
        snare: ". . x . . . x . . . x . . . x ."
        ghost_notes: ". x . . . x . . . x . . x . . ."
        hihat: "x x x x x x x x x x x x x x x x"
      swing: 0.15

    james_brown:
      name: "James Brown Style"
      genre: "funk"
      time_signature: [4, 4]
      subdivision: 16
      pattern:
        kick: "x . x . x . x . . . x . x . . ."
        snare: ". . x . . . . . . x . . . . ."
        ghost: ". x . . . x . . . x . . . x . ."
        hihat: "x . x . x . x . x . x . x . x . x ."
      swing: 0.2

    slap_bass_funk:
      name: "Slap Bass Funk"
      genre: "funk"
      time_signature: [4, 4]
      subdivision: 16
      pattern:
        kick: "x . . . x . . . . . . . x . . ."
        snare: ". . x . . . . . . . x . . . . ."
        hihat_open: ". . . . x . . . . . . . x . . ."
        hihat_closed: "x . x . . . x . x . x . x . . . x ."
      swing: 0.15
```

## Hip-Hop Patterns

```yaml
  hiphop:
    basic_boombap:
      name: "Boom Bap"
      genre: "hiphop"
      time_signature: [4, 4]
      subdivision: 16
      pattern:
        kick: "x . . . x . . . . . . . . . x ."
        snare: ". . . . x . . . . . . . x . . ."
        hihat: "x . x . x . x . x . x . x . x . x ."
      swing: 0.1

    trap:
      name: "Trap"
      genre: "hiphop"
      time_signature: [4, 4]
      subdivision: 16
      pattern:
        kick: "x . . . . . . . x . . . . . . ."
        snare: ". . . . x . . . . . . . x . . ."
        hihat: "x x x x x x x x x x x x x x x x"
        hihat_open: ". . . . . . . . . . . . . . x ."
      swing: 0.05

    trap_half_time:
      name: "Trap Half-Time"
      genre: "hiphop"
      time_signature: [4, 4]
      subdivision: 8
      pattern:
        kick: "x . . . . . . ."
        snare: ". . . . x . . ."
        hihat: "x x x x x x x x"
      swing: 0.0
```

## Electronic/EDM Patterns

```yaml
  electronic:
    four_on_floor:
      name: "4-on-the-Floor"
      genre: "house"
      time_signature: [4, 4]
      subdivision: 16
      pattern:
        kick: "x . . . x . . . x . . . x . . ."
        clap: ". . . . x . . . . . . . x . . ."
        hihat: ". x . x . x . x . x . x . x . x ."
      swing: 0.0

    techno:
      name: "Techno"
      genre: "techno"
      time_signature: [4, 4]
      subdivision: 16
      pattern:
        kick: "x . . . x . . . x . . . x . . ."
        clap: ". . . . . . x . . . . . . . x ."
        hihat: ". x . . . x . . . x . . . x . ."
      swing: 0.0

    dnb:
      name: "Drum and Bass"
      genre: "dnb"
      time_signature: [4, 4]
      subdivision: 16
      bpm_range: [170, 180]
      pattern:
        kick: "x . . . . . . . . . . . . . . ."
        snare: ". . . . x . . . . . . . x . . ."
        breakbeat: "x x . x x . x . x . . x x x . x ."
      swing: 0.05

    dubstep:
      name: "Dubstep"
      genre: "dubstep"
      time_signature: [4, 4]
      subdivision: 8
      bpm_range: [140, 145]
      pattern:
        kick: "x . . . . . . ."
        snare: ". . . . x . . ."
        hihat: ". x . x . x . x"
      swing: 0.2
```

## Fill System

```python
class DrumFillGenerator:
    """Generate drum fills"""

    def generate_fill(
        self,
        style: str,
        length: Literal["1", "2", "4"],  # In beats
        end_phrase: bool = True
    ) -> DrumPattern:
        """Generate a fill in specified style"""

    FILL_PATTERNS = {
        "rock_basic": {
            "1": "kick+snare+hh"  # Single hit of each
        },
        "roll": {
            "2": "snare: x x x x"  # Snare roll
        },
        "tom_run": {
            "4": "toms: descending"
        },
        "crash_ending": {
            "2": "crash: x"
        }
    }
```

## Groove System

```python
def apply_groove(
    pattern: DrumPattern,
    swing: float,
    humanize: float = 0.0,
    accent_pattern: list[int] | None = None
) -> DrumPattern:
    """Apply groove feel to a drum pattern"""
    # Swing: delay off-beats
    # Humanize: add random timing variation
    # Accent: emphasize certain beats
```

## Files to Create

- `src/musicgen/patterns/drums.py`
- `resources/drum_patterns.yaml`
- `src/musicgen/instruments/fill_generator.py`

## Success Criteria

- [ ] All genre patterns defined
- [ ] Mini-notation parser working
- [ ] Fill generation functional
- [ ] Groove system with swing
- [ ] Humanization system
- [ ] Pattern combination utilities
- [ ] Complete test coverage

## Next Steps

After completion, proceed to V4-11: Drum Articulation System
