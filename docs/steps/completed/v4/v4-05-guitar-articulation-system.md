# V4-05: Guitar Articulation System

## Overview

Define and implement guitar-specific articulations and playing techniques with proper MIDI implementation.

## Objectives

1. Define guitar articulation types
2. Create strumming patterns
3. Define picking techniques
4. Implement fretting techniques
5. Create articulation-to-MIDI mappings

## Guitar Articulations

### Strumming Techniques

```python
class StrumPattern(BaseModel):
    """Guitar strumming pattern"""
    name: str
    strokes: list[Literal["down", "up", "mute"]]
    timing: list[float]  # Relative timing within beat
    accent: list[bool | None]  # Which strokes are accented

# Common patterns
STRUM_PATTERNS = {
    "basic_4": StrumPattern(
        name="Basic 4/4",
        strokes=["down", "down", "up", "up"],
        timing=[0.0, 0.5, 0.75, 1.0],
        accent=[True, False, False, False]
    ),
    "folk": StrumPattern(
        name="Folk/Country",
        strokes=["down", "down_up", "down_up", "down_up"],
        timing=[0.0, 0.5, 0.75, 1.0],
        accent=[True, False, False, False]
    ),
    "rock": StrumPattern(
        name="Rock",
        strokes=["down", "down", "up", "down_up"],
        timing=[0.0, 0.5, 0.75, 1.0],
        accent=[True, True, False, False]
    ),
    "bossa": StrumPattern(
        name="Bossa Nova",
        strokes=["down", "up", "down_up", "up"],
        timing=[0.0, 0.4, 0.6, 1.0],
        accent=[True, False, False, False]
    ),
    "reggae": StrumPattern(
        name="Reggae (skank)",
        strokes=["up", "mute", "up", "mute"],
        timing=[0.0, 0.5, 0.5, 1.0],
        accent=[True, False, True, False]
    ),
}
```

### Picking Techniques

```python
class PickingTechnique(BaseModel):
    """Single-note picking technique"""
    name: str
    direction: Literal["down", "up", "hybrid"]
    attack_time: float  # Seconds
    velocity_modifier: float
    duration_modifier: float

PICKING_TECHNIQUES = {
    "normal": PickingTechnique(
        name="Normal Pick",
        direction="down",
        attack_time=0.01,
        velocity_modifier=1.0,
        duration_modifier=1.0
    ),
    "hammer_on": PickingTechnique(
        name="Hammer-on",
        direction="none",
        attack_time=0.005,  # Faster attack
        velocity_modifier=0.85,
        duration_modifier=0.9
    ),
    "pull_off": PickingTechnique(
        name="Pull-off",
        direction="none",
        attack_time=0.008,
        velocity_modifier=0.8,
        duration_modifier=0.85
    ),
    "slide": PickingTechnique(
        name="Slide",
        direction="none",
        attack_time=0.02,  # Smear attack
        velocity_modifier=0.9,
        duration_modifier=1.1  # Extend through slide
    ),
    "bend": PickingTechnique(
        name="Bend",
        direction="none",
        attack_time=0.05,  # Gradual bend
        velocity_modifier=1.1,
        duration_modifier=1.2
    ),
    "vibrato": PickingTechnique(
        name="Vibrato",
        direction="none",
        attack_time=0.0,
        velocity_modifier=1.0,
        duration_modifier=1.0
    ),
    "palm_mute": PickingTechnique(
        name="Palm Mute",
        direction="down",
        attack_time=0.01,
        velocity_modifier=0.7,  # Softer
        duration_modifier=0.6  # Shorter decay
    ),
}
```

### Fretting Techniques

```python
class FrettingTechnique(BaseModel):
    """Left-hand fretting technique"""
    name: str
    string_pressure: float  # 0-1
    vibration: bool = False
    slide_distance: int | None = None  # In frets
    bend_amount: float | None = None  # In semitones

FRETTING_TECHNIQUES = {
    "normal": FrettingTechnique(
        name="Normal fret",
        string_pressure=1.0
    ),
    "legato": FrettingTechnique(
        name="Legato",
        string_pressure=0.9,
        vibration=False
    ),
    "vibrato": FrettingTechnique(
        name="Vibrato",
        string_pressure=1.0,
        vibration=True
    ),
    "bend_full": FrettingTechnique(
        name="Full bend",
        string_pressure=1.0,
        bend_amount=1.0  # One whole step
    ),
    "bend_half": FrettingTechnique(
        name="Half bend",
        string_pressure=1.0,
        bend_amount=0.5  # Half step
    ),
    "slide_up": FrettingTechnique(
        name="Slide up",
        slide_distance=2  # 2 frets
    ),
}
```

### Harmonics

```python
class HarmonicType(BaseModel):
    """Guitar harmonic technique"""
    name: str
    fret_position: int  # Fret number for natural harmonics
    string: int | None = None  # String number (1-6)
    velocity_modifier: float
    duration_modifier: float
    filter_freq: float  # For filtering effect

HARMONICS = {
    "natural_12": HarmonicType(
        name="Natural Harmonic (12th fret)",
        fret_position=12,
        velocity_modifier=0.7,
        duration_modifier=1.5,
        filter_freq=2000
    ),
    "natural_7": HarmonicType(
        name="Natural Harmonic (7th fret)",
        fret_position=7,
        velocity_modifier=0.75,
        duration_modifier=1.3,
        filter_freq=3000
    ),
    "natural_5": HarmonicType(
        name="Natural Harmonic (5th fret)",
        fret_position=5,
        velocity_modifier=0.8,
        duration_modifier=1.2,
        filter_freq=4000
    ),
    "artificial": HarmonicType(
        name="Artificial Harmonic",
        fret_position=12,  # Relative to fretted note
        velocity_modifier=0.65,
        duration_modifier=1.4,
        filter_freq=2500
    ),
    "pinch": HarmonicType(
        name="Pinch Harmonic",
        fret_position=0,  # At bridge pickup
        velocity_modifier=0.6,
        duration_modifier=1.6,
        filter_freq=3500
    ),
}
```

## MIDI Implementation

### Articulation to MIDI Mapping

```python
def guitar_articulation_to_midi(
    note: AINote,
    articulation: str,
    technique: PickingTechnique | None = None
) -> list[MidiEvent]:
    """Convert guitar articulation to MIDI events"""

    events = []

    # Note on with modified velocity
    velocity = int(note.velocity * technique.velocity_modifier)
    events.append(MidiEvent(
        type="note_on",
        note=note.note_name,
        velocity=velocity,
        time=note.start_time
    ))

    # Duration modification
    duration = note.duration * technique.duration_modifier

    # Pitch bend for bends/vibrato
    if articulation in ["bend", "bend_full", "bend_half"]:
        bend_amount = FRETTING_TECHNIQUES[articulation].bend_amount
        events.extend(create_pitch_bend(
            start_time=note.start_time,
            amount=bend_amount,
            duration=0.1  # Bend duration
        ))

    # Note off
    events.append(MidiEvent(
        type="note_off",
        note=note.note_name,
        time=note.start_time + duration
    ))

    return events
```

## Strumming Implementation

```python
def create_strum(
    chord: list[str],  # List of note names
    pattern: StrumPattern,
    start_time: float,
    velocity: int = 100
) -> list[AINote]:
    """Create a strummed chord from a pattern"""

    notes = []
    current_time = start_time

    for stroke, timing, accent in zip(
        pattern.strokes,
        pattern.timing,
        pattern.accent
    ):
        # Calculate velocity with accent
        stroke_velocity = velocity * 1.2 if accent else velocity * 0.8

        # Strum direction affects timing slightly
        # Down strum: low strings first
        # Up strum: high strings first
        if stroke == "down":
            string_order = chord
        elif stroke == "up":
            string_order = list(reversed(chord))
        else:  # mute
            string_order = []

        # Slight delay between strings for realism
        for i, note_name in enumerate(string_order):
            delay = i * 0.005  # 5ms per string
            notes.append(AINote(
                note_name=note_name,
                duration=timing - delay,
                start_time=current_time + delay,
                velocity=stroke_velocity
            ))

        current_time += timing

    return notes
```

## Files to Create/Modify

- `src/musicgen/instruments/guitars.py` (articulations)
- `src/musicgen/patterns/guitar_patterns.py`
- `src/musicgen/renderer/guitar_midi.py`

## Success Criteria

- [ ] All strumming patterns defined
- [ ] All picking techniques implemented
- [ ] All fretting techniques implemented
- [ ] Harmonics system working
- [ ] MIDI generation for all articulations
- [ ] Tests pass for all techniques
- [ ] Realistic guitar sound achieved

## Next Steps

After completion, proceed to V4-06: Guitar Chord Library
