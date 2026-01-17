# V4-09: Drum Kit Definitions

## Overview

Define comprehensive drum kit specifications for all common kit types with General MIDI drum mapping.

## Objectives

1. Define standard acoustic drum kit
2. Define jazz drum kit
3. Define electronic drum kits
4. Define world percussion kits
5. Implement GM drum key mapping
6. Create kit piece definitions

## Drum Kit Structure

```python
class DrumKit(BaseModel):
    """Complete drum kit definition"""
    name: str
    category: Literal["acoustic", "electronic", "world", "hybrid"]
    pieces: dict[str, DrumPiece]  # piece_name -> definition
    defaults: DrumKitDefaults

class DrumPiece(BaseModel):
    """Individual drum/cymbal in a kit"""
    name: str
    midi_note: int  # GM drum key
    category: Literal[
        "kick", "snare", "tom", "hihat",
        "crash", "ride", "effect", "percussion"
    ]
    range: tuple[int, int] = (1, 127)
    articulations: dict[str, DrumArticulation] = {}

class DrumArticulation(BaseModel):
    """Drum playing technique"""
    name: str
    velocity_modifier: float = 1.0
    duration_modifier: float = 1.0
    pitch_offset: int = 0  # For pitch variation
    midi_note_override: int | None = None  # If different articulation uses different key
```

## Standard Rock Kit

```yaml
# Standard acoustic rock kit
standard_rock_kit:
  name: "Standard Rock Kit"
  category: "acoustic"
  pieces:
    kick:
      midi_note: 35  # Acoustic Bass Drum
      category: "kick"
      range: [40, 127]
      articulations:
        normal: {velocity_mod: 1.0, duration: 0.3}
        soft: {velocity_mod: 0.7, midi_note: 36}  # Bass Drum 1
        hard: {velocity_mod: 1.2}

    snare:
      midi_note: 38  # Acoustic Snare
      category: "snare"
      range: [30, 127]
      articulations:
        normal: {velocity_mod: 1.0, duration: 0.15}
        center: {velocity_mod: 1.1}
        rimshot: {velocity_mod: 1.2, midi_note: 37}  # Side Stick
        cross_stick: {velocity_mod: 0.8, midi_note: 37}

    hi_hat_closed:
      midi_note: 42  # Closed Hi-Hat
      category: "hihat"
      articulations:
        normal: {velocity_mod: 1.0, duration: 0.05}
        tight: {velocity_mod: 0.9, duration: 0.03}

    hi_hat_open:
      midi_note: 46  # Open Hi-Hat
      category: "hihat"
      articulations:
        normal: {velocity_mod: 1.0, duration: 0.3}
        half: {velocity_mod: 0.9, duration: 0.15, midi_note: 44}  # Pedal

    hi_hat_pedal:
      midi_note: 44  # Pedal Hi-Hat
      category: "hihat"
      articulations:
        chick: {velocity_mod: 0.8, duration: 0.02}

    tom1:
      midi_note: 45  # Low Tom
      category: "tom"
      articulations:
        normal: {velocity_mod: 1.0, duration: 0.4}

    tom2:
      midi_note: 48  # Hi-Mid Tom
      category: "tom"
      articulations:
        normal: {velocity_mod: 1.0, duration: 0.35}

    crash1:
      midi_note: 49  # Crash Cymbal 1
      category: "crash"
      articulations:
        normal: {velocity_mod: 1.0, duration: 1.5}
        accent: {velocity_mod: 1.3, duration: 2.0}

    ride:
      midi_note: 51  # Ride Cymbal 1
      category: "ride"
      articulations:
        normal: {velocity_mod: 1.0, duration: 1.0}
        bell: {velocity_mod: 1.1, midi_note: 53}  # Ride Bell
        crash: {velocity_mod: 1.2, duration: 1.5}
```

## Jazz Kit

```yaml
jazz_kit:
  name: "Jazz Kit"
  category: "acoustic"
  pieces:
    kick:
      midi_note: 35
      category: "kick"
      range: [30, 100]
      articulations:
        feather: {velocity_mod: 0.5, duration: 0.2}
        normal: {velocity_mod: 0.8, duration: 0.25}

    snare:
      midi_note: 38
      category: "snare"
      range: [20, 110]
      articulations:
        brush_normal: {velocity_mod: 0.6, duration: 0.1}
        brush_slap: {velocity_mod: 0.8, duration: 0.08}
        stick_normal: {velocity_mod: 0.9, duration: 0.12}
        cross_stick: {velocity_mod: 0.5, midi_note: 37}

    ride:
      midi_note: 51
      category: "ride"
      articulations:
        normal: {velocity_mod: 0.9, duration: 2.0}
        bow: {velocity_mod: 0.8, duration: 2.5}
        bell: {velocity_mod: 1.0, midi_note: 53}

    hi_hat:
      midi_note: 42
      category: "hihat"
      articulations:
        closed: {velocity_mod: 0.7, duration: 0.05}
        half_open: {velocity_mod: 0.8, duration: 0.15}
```

## Electronic Kits

### Roland TR-808

```yaml
tr808_kit:
  name: "Roland TR-808"
  category: "electronic"
  pieces:
    kick:
      midi_note: 35
      category: "kick"
      description: "Deep, punchy 808 kick"
      decay: "long"
      pitch_envelope: "drop"

    snare:
      midi_note: 38
      category: "snare"
      description: "Bright 808 snare"
      tone: "bright"

    clap:
      midi_note: 39
      category: "snare"
      description: "808 hand clap"

    hi_hat_closed:
      midi_note: 42
      category: "hihat"
      description: "Short, metallic 808 hi-hat"

    hi_hat_open:
      midi_note: 46
      category: "hihat"
      description: "Long 808 hi-hat"

    cowbell:
      midi_note: 56
      category: "effect"
      description: "Iconic 808 cowbell"
```

### Roland TR-909

```yaml
tr909_kit:
  name: "Roland TR-909"
  category: "electronic"
  pieces:
    kick:
      midi_note: 35
      category: "kick"
      description: "Punchy, processed 909 kick"

    snare:
      midi_note: 38
      category: "snare"
      description: "Aggressive 909 snare"

    rim:
      midi_note: 37
      category: "snare"
      description: "Distinctive 909 rimshot"

    crash:
      midi_note: 49
      category: "crash"
      description: "Metallic 909 crash"
```

## World Percussion Kits

### Latin Kit

```yaml
latin_kit:
  name: "Latin Percussion"
  category: "world"
  pieces:
    conga_low:
      midi_note: 64  # Low Conga
      category: "percussion"
      description: "Quinto (lowest conga)"

    conga_high:
      midi_note: 63  # Mute Hi Conga / Open Hi Conga
      category: "percussion"
      description: "Conga (higher pitch)"

    bongo:
      midi_note: 60  # Hi Bongo
      category: "percussion"
      articulations:
        high: {midi_note: 60}
        low: {midi_note: 61}

    timbale:
      midi_note: 65  # Low Timbale
      category: "percussion"
      articulations:
        high: {midi_note: 65}
        low: {midi_note: 66}

    claves:
      midi_note: 75  # Claves
      category: "percussion"

    guiro:
      midi_note: 73  # Short Guiro
      category: "percussion"
      articulations:
        short: {midi_note: 73}
        long: {midi_note: 74}
```

### African Kit

```yaml
african_kit:
  name: "West African Percussion"
  category: "world"
  pieces:
    djembe_bass:
      midi_note: 35
      category: "kick"
      description: "Djembe bass tone"

    djembe_slap:
      midi_note: 40
      category: "snare"
      description: "Djembe slap tone"

    djembe_tone:
      midi_note: 38
      category: "snare"
      description: "Djembe open tone"

    dunun_bell:
      midi_note: 56
      category: "effect"
      description: "Dunun bell pattern"

    shekere:
      midi_note: 70
      category: "percussion"
      description: "Beaded gourd shaker"

    talking_drum:
      midi_note: 64
      category: "percussion"
      description: "Pressure-modulated drum"
```

## Files to Create

- `resources/instrument_definitions_world.yaml` (drum kits section)
- `src/musicgen/instruments/drums.py`
- `src/musicgen/instruments/gm_drum_map.py`

## Success Criteria

- [ ] All GM drum keys mapped
- [ ] Standard rock kit complete
- [ ] Jazz kit complete
- [ ] 808 and 909 kits complete
- [ ] Latin and African kits defined
- [ ] All articulations specified
- [ ] Lookup utilities working

## Next Steps

After completion, proceed to V4-10: Drum Pattern System
