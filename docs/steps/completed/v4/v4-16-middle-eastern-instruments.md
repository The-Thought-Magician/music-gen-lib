# V4-16: Middle Eastern Instruments

## Overview

Define Middle Eastern and Arabic instruments with quarter-tone support.

## Objectives

1. Define Oud specifications
2. Define Ney (flute) specifications
3. Define Darbuka specifications
4. Define Kanun specifications
5. Implement quarter-tone system

## Oud

```yaml
oud:
  name: "Oud"
  region: "Middle East"
  family: "chordophone (lute)"
  midi_program: 24  # Acoustic Guitar (nylon) - closest match
  strings:
    count: 11 or 13
    courses: 6  # Pairs in courses, plus lowest string
    tuning: ["G2", "G2", "A2", "A2", "D3", "D3", "G3", "G3", "C4", "C4", "F4", "F4", "C4"]  # Arabic tuning
  range: {min: 43, max: 84}  # G#2 to C5
  frets:
    type: "none (fretless)"
    microtonal: true
  techniques:
    risha:
      name: "Risha (Feather)"
      description: "Long feather quill plectrum"
      attack: "soft"
    mizrab:
      name: "Mizrab"
      description: "Traditional plectrum"
      attack: "sharp"
    tremolo:
      name: "Tremolo"
      description: "Rapid alternation"
    dumm:
      name: "Dumm"
      description: "Bass stroke"
    tak:
      name: "Tak"
      description: "Treble stroke"
```

## Ney

```yaml
ney:
  name: "Ney"
  region: "Middle East"
  family: "aerophone (reed flute)"
  midi_program: 73  # Flute
  types:
    bass:
      name: "Ney (Bass/Doga)"
      length: "~50 inch"
      range: {min: 48, max: 72}
      key: "D"
    medium:
      name: "Ney (Mansur)"
      length: "~40 inch"
      range: {min: 55, max: 81}
      key: "D"
    piccolo:
      name: "Ney (Kabas)"
      length: "~30 inch"
      range: {min: 64, max: 88}
      key: "D"
  technique:
    embouchure: "angle-controlled pitch"
    breath: "pressure-controlled volume"
  techniques:
    tremolo:
      name: "Tremolo"
      description: "Breath vibrato"
    grace:
      name: "Grace note"
      description: "Quick upper neighbor"
```

## Kanun

```yaml
kanun:
  name: "Kanun"
  region: "Middle East"
  family: "chordophone (zither)"
  strings:
    count: 72-84
  range: {min: 48, max: 84}
  bridges:
    type: "movable"
    mandal: "small levers for microtones"
  techniques:
    tremolo:
      name: "Tremolo"
      description: "Rapid picking"
    glissando:
      name: "Glissando"
      description: "Sweep across strings"
```

## Buq (Horn)

```yaml
buq:
  name: "Buq"
  region: "Middle East"
  family: "aerophone (brass)"
  midi_program: 57  # Trombone
  range: {min: 40, max: 72}
  playing:
    lip: "variable pitch"
  techniques:
    drone: "Continuous tone"
    melody: "Ornamented melody"
```

## Files to Create

- `resources/instrument_definitions_world.yaml` (Middle Eastern)
- `src/musicgen/instruments/middle_eastern.py`

## Success Criteria

- [ ] All Middle Eastern instruments defined
- [ ] Quarter-tone system implemented
- [ ] Techniques mapped to MIDI

## Next Steps

After completion, proceed to V4-17: Arabic Maqam System
