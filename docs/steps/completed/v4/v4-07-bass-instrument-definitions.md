# V4-07: Bass Instrument Definitions

## Overview

Define complete specifications for all bass guitar and upright bass types.

## Objectives

1. Define acoustic/upright bass specifications
2. Define electric bass specifications
3. Define synth bass specifications
4. Define bass-specific playing techniques
5. Create bass pattern library

## Bass Types

### Acoustic/Upright Bass

```yaml
upright_bass:
  name: "Acoustic Bass (Upright)"
  midi_program: 32
  family: "bass"
  category: "guitar"
  subcategory: "acoustic"
  range: {min: 28, max: 55}  # E1 to G4
  string_count: 4
  tuning: ["E1", "A1", "D2", "G2"]
  play_styles:
    arco:
      description: "Bowed"
      attack: 0.1
      decay: 0.3
      vibrato: true
    pizzicato:
      description: "Plucked"
      attack: 0.01
      decay: 0.5
      vibrato: false
  technique_markers:
    arco: "arco"
    pizzicato: "pizz."
    sul_ponticello: "sul pont."
    legato: "legato"
```

### Electric Bass (Finger)

```yaml
electric_bass_finger:
  name: "Electric Bass (Finger)"
  midi_program: 33
  family: "bass"
  category: "guitar"
  subcategory: "electric"
  range: {min: 28, max: 48}  # E1 to C4
  string_count: 4
  fret_count: 20
  tuning: ["E1", "A1", "D2", "G2"]
  pickup: "passive"
  play_position: "neck"
  attack: 0.005
  decay: 0.4
  sustain: 0.3
  techniques:
    finger: {velocity_mod: 1.0, duration_mod: 1.0}
    mute: {velocity_mod: 0.6, duration_mod: 0.5}
    harmonic: {velocity_mod: 0.5, duration_mod: 1.5}
    slide: {glissando: true, duration_extend: 0.1}
```

### Electric Bass (Pick)

```yaml
electric_bass_pick:
  name: "Electric Bass (Pick)"
  midi_program: 34
  family: "bass"
  category: "guitar"
  subcategory: "electric"
  range: {min: 28, max: 48}
  string_count: 4
  tuning: ["E1", "A1", "D2", "G2"]
  pickup: "passive"
  play_position: "bridge"
  attack: 0.003  # Faster attack
  decay: 0.3
  sustain: 0.4
  brighter: true
  techniques:
    pick: {velocity_mod: 1.1, duration_mod: 0.9}
    palm_mute: {velocity_mod: 0.7, duration_mod: 0.5}
    pop: {velocity_mod: 1.3, attack: 0.001}
```

### Fretless Bass

```yaml
fretless_bass:
  name: "Fretless Bass"
  midi_program: 35
  family: "bass"
  category: "guitar"
  subcategory: "electric"
  range: {min: 28, max: 48}
  string_count: 4
  fret_count: 0  # Fretless
  tuning: ["E1", "A1", "D2", "G2"]
  microtonal: true
  slide: true
  glissando: true
  attack: 0.01
  decay: 0.5
  sustain: 0.5
  expression: true  # Pitch control
```

### Slap Bass

```yaml
slap_bass_1:
  name: "Slap Bass 1"
  midi_program: 36
  family: "bass"
  category: "guitar"
  subcategory: "electric"
  range: {min: 28, max: 55}
  string_count: 4
  tuning: ["E1", "A1", "D2", "G2"]
  style: "slap_pop"
  techniques:
    thumb:
      description: "Thumb slap on low strings"
      velocity_range: [100, 127]
      attack: 0.001
      decay: 0.2
    pop:
      description: "Pop on high strings"
      velocity_range: [80, 110]
      attack: 0.001
      decay: 0.15
    ghost:
      description: "Ghost notes (percussive)"
      velocity_range: [30, 50]
      fretted: false
```

### Synth Bass

```yaml
synth_bass_1:
  name: "Synth Bass 1"
  midi_program: 38
  family: "bass"
  category: "electronic"
  subcategory: "synth"
  range: {min: 24, max: 48}  # C1 to C4
  synth_type: "subtractive"
  oscillator: "sawtooth"
  filter: "lowpass_24db"
  filter_envelope:
    attack: 0.01
    decay: 0.2
    sustain: 0.5
    release: 0.1
  amp_envelope:
    attack: 0.01
    decay: 0.1
    sustain: 0.8
    release: 0.2

synth_bass_2:
  name: "Synth Bass 2 (Deep)"
  midi_program: 39
  family: "bass"
  category: "electronic"
  subcategory: "synth"
  range: {min: 24, max: 48}
  synth_type: "subtractive"
  oscillator: "square"
  filter: "lowpass_24db"
  filter_envelope:
    attack: 0.005
    decay: 0.3
    sustain: 0.6
    release: 0.15
  sub_oscillator: true
  sub_octave: -1
```

## Extended Range Basses

```yaml
five_string_bass:
  name: "5-String Bass"
  midi_program: 33  # Uses same program
  extended_range: true
  string_count: 5
  tuning: ["B0", "E1", "A1", "D2", "G2"]
  range: {min: 23, max: 55}  # B0 to G4

six_string_bass:
  name: "6-String Bass"
  extended_range: true
  string_count: 6
  tuning: ["B0", "E1", "A1", "D2", "G2", "C3"]
  range: {min: 23, max: 60}  # B0 to C4
```

## Bass Articulations

```python
BASS_ARTICULATIONS = {
    # Acoustic bass
    "arco": {
        "duration_mod": 1.2,
        "velocity_mod": 0.95,
        "attack": 0.1,
        "vibrato": True
    },
    "pizzicato": {
        "duration_mod": 0.8,
        "velocity_mod": 1.1,
        "attack": 0.005
    },
    # Electric bass
    "finger": {
        "duration_mod": 1.0,
        "velocity_mod": 1.0,
        "attack": 0.01
    },
    "mute": {
        "duration_mod": 0.5,
        "velocity_mod": 0.7,
        "attack": 0.005
    },
    "ghost": {
        "duration_mod": 0.3,
        "velocity_mod": 0.4,
        "attack": 0.001
    },
    "slide": {
        "duration_mod": 1.1,
        "velocity_mod": 0.95,
        "pitch_bend": True
    },
    # Slap
    "thumb": {
        "duration_mod": 0.3,
        "velocity_mod": 1.2,
        "attack": 0.001
    },
    "pop": {
        "duration_mod": 0.2,
        "velocity_mod": 1.1,
        "attack": 0.001
    },
}
```

## Bass Pattern Library

```python
BASS_PATTERNS = {
    "root_eighth": {
        "description": "Root notes on eighth notes",
        "pattern": "1 _ 1 _ 1 _ 1 _",  # Mini-notation
        "styles": ["rock", "pop", "blues"]
    },
    "root_fifth": {
        "description": "Root and fifth alternation",
        "pattern": "1 5 _ 1 5 _ _ _",
        "styles": ["rock", "country"]
    },
    "walking": {
        "description": "Walking bass line",
        "pattern": "1 3 5 b7 _ 1 3 5",  # Scale tones
        "styles": ["jazz", "blues"]
    },
    "syncopated": {
        "description": "Syncopated bass line",
        "pattern": "1 _ _ 5 _ b7 _ 1",
        "styles": ["funk", "r&b"]
    },
    "motorik": {
        "description": "Driving eighth notes",
        "pattern": "1 1 1 1 1 1 1 1",
        "styles": ["krautrock", "techno"]
    },
    "dub": {
        "description": "Sparse dub bass",
        "pattern": "1 _ _ _ _ _ _ _",
        "styles": ["dub", "reggae"]
    },
}
```

## Files to Create

- `resources/instrument_definitions_world.yaml` (bass section)
- `src/musicgen/instruments/bass.py`
- `src/musicgen/patterns/bass_patterns.py`

## Success Criteria

- [ ] All GM bass programs defined
- [ ] Extended range basses included
- [ ] All articulations specified
- [ ] Bass pattern library complete
- [ ] MIDI mapping for all techniques
- [ ] Tests for bass-specific features

## Next Steps

After completion, proceed to V4-08: Guitar/Bass MIDI Generation
