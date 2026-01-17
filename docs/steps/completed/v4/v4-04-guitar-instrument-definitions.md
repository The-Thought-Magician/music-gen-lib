# V4-04: Guitar Instrument Definitions

## Overview

Define complete instrument specifications for all guitar types in the system.

## Objectives

1. Create YAML definitions for acoustic guitars
2. Create YAML definitions for electric guitars
3. Define string tunings (standard, alternate)
4. Specify ranges and dynamics
5. Define SFZ/sample configurations

## Guitar Types to Define

### Acoustic Guitars

- **Acoustic Guitar (Nylon)** - GM 24
  - Range: E3 (40) to B5 (83)
  - 6 strings, standard tuning: E2 A2 D3 G3 B3 E4
  - Warm, mellow tone
  - Classical, folk, Latin styles

- **Acoustic Guitar (Steel)** - GM 25
  - Range: E3 (40) to C6 (84)
  - 6 strings, standard tuning: E2 A2 D3 G3 B3 E4
  - Brighter, crisp tone
  - Folk, country, pop styles

### Electric Guitars

- **Electric Guitar (Jazz)** - GM 26
  - Range: E3 (40) to C6 (84)
  - Clean, warm neck pickup tone
  - Jazz, smooth jazz, R&B

- **Electric Guitar (Clean)** - GM 27
  - Range: E3 (40) to C6 (84)
  - Clean bridge/middle pickup
  - Pop, rock, funk

- **Electric Guitar (Muted)** - GM 28
  - Range: E3 (40) to C6 (84)
  - Palm-muted bridge pickup
  - Rock, metal, punk

- **Electric Guitar (Overdriven)** - GM 29
  - Range: E3 (40) to B5 (83)
  - Mild overdrive, crunchy
  - Blues, classic rock

- **Electric Guitar (Distortion)** - GM 30
  - Range: E3 (40) to A5 (81)
  - High gain distortion
  - Hard rock, metal

- **Guitar Harmonics** - GM 31
  - Range: E4 (52) to E6 (88)
  - Natural/artificial harmonics
  - Special effect

### Bass Guitars

- **Acoustic Bass** - GM 32
  - Range: E1 (28) to G4 (55)
  - Upright bass simulation
  - Jazz, orchestral

- **Electric Bass (Finger)** - GM 33
  - Range: E1 (28) to C4 (48)
  - Finger-style electric
  - Most common bass tone

- **Electric Bass (Pick)** - GM 34
  - Range: E1 (28) to C4 (48)
  - Pick-style electric
  - Rock, pop

- **Fretless Bass** - GM 35
  - Range: E1 (28) to C4 (48)
  - Smooth, singing tone
  - Jazz, fusion

- **Slap Bass 1** - GM 36
  - Range: E1 (28) to G4 (55)
  - Thumb slap, pop
  - Funk, R&B

- **Slap Bass 2** - GM 37
  - Range: E1 (28) to G4 (55)
  - Percussive slap
  - Funk, disco

- **Synth Bass 1** - GM 38
  - Range: C1 (24) to C4 (48)
  - Simple synth bass
  - Electronic, pop

- **Synth Bass 2** - GM 39
  - Range: C1 (24) to C4 (48)
  - Deep synth bass
  - EDM, techno

## YAML Structure

```yaml
# resources/instrument_definitions_world.yaml

guitars:
  acoustic_nylon:
    name: "Acoustic Guitar (Nylon)"
    midi_program: 24
    family: "guitars"
    category: "guitar"
    subcategory: "acoustic"
    range: {min: 40, max: 83}
    string_count: 6
    fret_count: 12  # Usually 12 frets accessible
    tuning: ["E2", "A2", "D3", "G3", "B3", "E4"]
    pick_noise: true
    finger_noise: true
    body_resonance: true

  acoustic_steel:
    name: "Acoustic Guitar (Steel)"
    midi_program: 25
    family: "guitars"
    category: "guitar"
    subcategory: "acoustic"
    range: {min: 40, max: 84}
    string_count: 6
    fret_count: 14
    tuning: ["E2", "A2", "D3", "G3", "B3", "E4"]
    brighter: true
    string_gauge: "light"

  electric_clean:
    name: "Electric Guitar (Clean)"
    midi_program: 27
    family: "guitars"
    category: "guitar"
    subcategory: "electric"
    range: {min: 40, max: 84}
    string_count: 6
    fret_count: 22
    tuning: ["E2", "A2", "D3", "G3", "B3", "E4"]
    pickup_position: "middle"
    pickup_type: "single_coil"
    clean_tone: true

basses:
  electric_bass_finger:
    name: "Electric Bass (Finger)"
    midi_program: 33
    family: "bass"
    category: "guitar"
    subcategory: "bass"
    range: {min: 28, max: 48}
    string_count: 4
    fret_count: 20
    tuning: ["E1", "A1", "D2", "G2"]
    play_style: "finger"
    round: true
```

## Alternate Tunings

```yaml
alternate_tunings:
  drop_d:
    tuning: ["D2", "A2", "D3", "G3", "B3", "E4"]
    description: "Lowered 6th string to D"

  open_d:
    tuning: ["D2", "A2", "D3", "F#3", "A3", "D4"]
    description: "D major chord when strummed open"

  open_g:
    tuning: ["D2", "G2", "D3", "G3", "B3", "D4"]
    description: "G major chord when strummed open"

  d_adgbe:
    tuning: ["D2", "A2", "D3", "G3", "B3", "E4"]
    description: "DADGAD - modal tuning"

  open_e:
    tuning: ["E2", "B2", "E3", "G#3", "B3", "E4"]
    description: "E major chord when strummed open"

  nashville:
    tuning: ["E2", "A2", "E3", "A3", "C#4", "E4"]
    description: "High strung for country"

  banjo:
    tuning: ["C3", "G3", "D4", "A4"]
    description: "5-string banjo (without high drone string)"
```

## Files to Create

- `resources/instrument_definitions_world.yaml` (with guitar definitions)
- `src/musicgen/instruments/guitars.py`
- `src/musicgen/instruments/tunings.py`

## Success Criteria

- [ ] All GM guitar types defined
- [ ] All GM bass types defined
- [ ] Standard tunings specified
- [ ] Common alternate tunings included
- [ ] Range specifications accurate
- [ ] YAML schema validated
- [ ] Lookup utilities functional

## Next Steps

After completion, proceed to V4-05: Guitar Articulation System
