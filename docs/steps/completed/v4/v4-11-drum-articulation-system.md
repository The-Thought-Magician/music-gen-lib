# V4-11: Drum Articulation System

## Overview

Define and implement drum-specific articulations and playing techniques.

## Objectives

1. Define drum stick types
2. Define hi-hat techniques
3. Define cymbal articulations
4. Define kick drum techniques
5. Implement MIDI rendering for all articulations

## Drum Stick Types

```python
class StickType(BaseModel):
    """Drum stick type characteristics"""
    name: str
    material: str
    tip: Literal["round", "acorn", "barrel", "diamond", "triangle"]
    length: str  # e.g., "16", "16-3/8"
    diameter: str
    velocity_modifier: float = 1.0
    attack_character: Literal["sharp", "muted", "warm"] = "sharp"

STICK_TYPES = {
    "5a": StickType(name="5A", material="hickory", tip="acorn", velocity_mod=1.0),
    "5b": StickType(name="5B", material="hickory", tip="acorn", velocity_mod=1.05),
    "7a": StickType(name="7A", material="hickory", tip="acorn", velocity_mod=0.9),
    "rock": StickType(name="Rock", material="hickory", tip="round", velocity_mod=1.1),
    "brushes": StickType(
        name="Brushes",
        material="wire",
        tip="none",
        velocity_mod=0.6,
        attack_character="muted"
    ),
    "mallets": StickType(
        name="Mallets",
        material="rubber",
        tip="round",
        velocity_mod=0.85,
        attack_character="warm"
    ),
    "rods": StickType(
        name="Rods",
        material="birch",
        tip="bundle",
        velocity_mod=0.75,
        attack_character="warm"
    ),
    "hands": StickType(
        name="Hands",
        material="none",
        tip="none",
        velocity_mod=0.7,
        attack_character="muted"
    ),
}
```

## Hi-Hat Techniques

```python
class HiHatArticulation(BaseModel):
    """Hi-hat playing technique"""
    name: str
    midi_note_base: int
    open_duration: float  # How long hat stays open
    velocity_mod: float
    duration_mod: float

HIHAT_ARTICULATIONS = {
    "closed": HiHatArticulation(
        name="Closed",
        midi_note_base=42,
        open_duration=0.0,
        velocity_mod=1.0,
        duration_mod=0.05
    ),
    "half_open": HiHatArticulation(
        name="Half Open",
        midi_note_base=42,
        open_duration=0.1,
        velocity_mod=0.95,
        duration_mod=0.15
    ),
    "open": HiHatArticulation(
        name="Open",
        midi_note_base=46,
        open_duration=0.3,
        velocity_mod=1.0,
        duration_mod=0.4
    ),
    "loose": HiHatArticulation(
        name="Loose",
        midi_note_base=46,
        open_duration=0.2,
        velocity_mod=0.9,
        duration_mod=0.25
    ),
    "foot_chick": HiHatArticulation(
        name="Foot Chick",
        midi_note_base=44,
        open_duration=0.0,
        velocity_mod=0.7,
        duration_mod=0.02
    ),
    "splash": HiHatArticulation(
        name="Splash",
        midi_note_base=46,
        open_duration=0.15,
        velocity_mod=1.1,
        duration_mod=0.2
    ),
}
```

## Snare Techniques

```python
class SnareArticulation(BaseModel):
    """Snare drum playing technique"""
    name: str
    hit_zone: Literal["center", "edge", "rim", "cross_stick"]
    stick_type: str
    velocity_mod: float
    duration_mod: float
    tone_mod: float  # Brightness adjustment (0-1)
    snare_wires: bool = True

SNARE_ARTICULATIONS = {
    "center": SnareArticulation(
        name="Center Hit",
        hit_zone="center",
        stick_type="5a",
        velocity_mod=1.0,
        duration_mod=0.15,
        tone_mod=0.5
    ),
    "rimshot": SnareArticulation(
        name="Rimshot",
        hit_zone="rim",
        stick_type="5a",
        velocity_mod=1.3,
        duration_mod=0.12,
        tone_mod=0.9,
        midi_note_override=37  # Side stick GM
    ),
    "cross_stick": SnareArticulation(
        name="Cross Stick",
        hit_zone="cross_stick",
        stick_type="5a",
        velocity_mod=0.8,
        duration_mod=0.08,
        tone_mod=0.3,
        midi_note_override=37
    ),
    "ghost": SnareArticulation(
        name="Ghost Note",
        hit_zone="center",
        stick_type="5a",
        velocity_mod=0.4,
        duration_mod=0.08,
        tone_mod=0.4
    ),
    "brush_sweep": SnareArticulation(
        name="Brush Sweep",
        hit_zone="center",
        stick_type="brushes",
        velocity_mod=0.6,
        duration_mod=0.2,
        tone_mod=0.6
    ),
}
```

## Cymbal Articulations

```python
class CymbalArticulation(BaseModel):
    """Cymbal playing technique"""
    name: str
    cymbal_type: Literal["crash", "ride", "splash", "china", "effect"]
    hit_zone: Literal["bell", "bow", "edge"]
    velocity_mod: float
    duration_mod: float
    choke: bool = False

CYMBAL_ARTICULATIONS = {
    "crash_normal": CymbalArticulation(
        name="Crash",
        cymbal_type="crash",
        hit_zone="bow",
        velocity_mod=1.0,
        duration_mod=2.0
    ),
    "crash_accent": CymbalArticulation(
        name="Crash Accent",
        cymbal_type="crash",
        hit_zone="bow",
        velocity_mod=1.3,
        duration_mod=2.5
    ),
    "crash_choke": CymbalArticulation(
        name="Crash Choke",
        cymbal_type="crash",
        hit_zone="bow",
        velocity_mod=1.2,
        duration_mod=0.3,
        choke=True
    ),
    "ride_bow": CymbalArticulation(
        name="Ride Bow",
        cymbal_type="ride",
        hit_zone="bow",
        velocity_mod=0.9,
        duration_mod=1.0
    ),
    "ride_bell": CymbalArticulation(
        name="Ride Bell",
        cymbal_type="ride",
        hit_zone="bell",
        velocity_mod=1.1,
        duration_mod=1.5,
        midi_note_override=53
    ),
    "china": CymbalArticulation(
        name="China",
        cymbal_type="china",
        hit_zone="bow",
        velocity_mod=1.2,
        duration_mod=2.5
    ),
    "splash": CymbalArticulation(
        name="Splash",
        cymbal_type="splash",
        hit_zone="bow",
        velocity_mod=1.0,
        duration_mod=0.3
    ),
}
```

## Kick Drum Techniques

```python
class KickArticulation(BaseModel):
    """Kick drum playing technique"""
    name: str
    beater_type: Literal["felt", "plastic", "wood", "fuzzy"]
    velocity_mod: float
    duration_mod: float
    pitch_mod: float = 0.0  # For electronic kicks

KICK_ARTICULATIONS = {
    "normal": KickArticulation(
        name="Normal Kick",
        beater_type="felt",
        velocity_mod=1.0,
        duration_mod=0.3
    ),
    "soft": KickArticulation(
        name="Soft Kick",
        beater_type="felt",
        velocity_mod=0.7,
        duration_mod=0.25
    ),
    "hard": KickArticulation(
        name="Hard Kick",
        beater_type="plastic",
        velocity_mod=1.2,
        duration_mod=0.35
    ),
    "dead": KickArticulation(
        name="Dead/Stroke Kick",
        beater_type="felt",
        velocity_mod=0.9,
        duration_mod=0.1
    ),
}
```

## Tom Articulations

```python
class TomArticulation(BaseModel):
    """Tom drum playing technique"""
    name: str
    tom_size: Literal["floor", "low", "mid", "high"]
    hit_zone: Literal["center", "rim"]
    velocity_mod: float
    duration_mod: float

TOM_ARTICULATIONS = {
    "floor_center": TomArticulation(
        name="Floor Tom",
        tom_size="floor",
        hit_zone="center",
        velocity_mod=1.0,
        duration_mod=0.5
    ),
    "floor_rim": TomArticulation(
        name="Floor Tom Rim",
        tom_size="floor",
        hit_zone="rim",
        velocity_mod=0.9,
        duration_mod=0.4
    ),
}
```

## MIDI Implementation

```python
def render_drum_hit(
    piece: str,
    articulation: str,
    time: float,
    velocity: int = 100
) -> list[MidiEvent]:
    """Render a single drum hit with articulation"""

    events = []

    # Get articulation parameters
    art = get_articulation(piece, articulation)

    # Note on
    midi_note = art.midi_note_override or get_midi_note(piece)
    events.append(MidiEvent(
        type="note_on",
        note=midi_note,
        velocity=int(velocity * art.velocity_mod),
        time=time
    ))

    # Note off
    events.append(MidiEvent(
        type="note_off",
        note=midi_note,
        time=time + art.duration_mod
    ))

    # Choke if applicable
    if art.choke:
        events.append(MidiEvent(
            type="note_off",
            note=midi_note,
            time=time + art.duration_mod * 0.1
        ))

    return events

def render_cymbal_choke(
    midi_note: int,
    start_time: float
) -> list[MidiEvent]:
    """Send immediate note-off to choke cymbal"""

def render_brush_sweep(
    time: float,
    duration: float
) -> list[MidiEvent]:
    """Render brush sweep as series of low-velocity notes"""
```

## Files to Create

- `src/musicgen/instruments/drums.py` (articulations)
- `resources/drum_articulations.yaml`

## Success Criteria

- [ ] All stick types defined
- [ ] All hi-hat articulations working
- [ ] All cymbal articulations working
- [ ] Snare techniques complete
- [ ] Kick techniques complete
- [ ] MIDI rendering for all articulations
- [ ] Tests for all drum techniques

## Next Steps

After completion, proceed to V4-12: World Percussion Definitions
