# V4-20: Other World Instruments

## Overview

Define remaining world instruments not covered in previous steps.

## Objectives

1. Define Hawaiian/Steel Guitar
2. Define Bagpipe
3. Define Irish Tin Whistle
4. Define Uilleann Pipes
5. Define Accordion
6. Define Bandoneon

## Hawaiian/Steel Guitar

```yaml
steel_guitar:
  name: "Hawaiian Steel Guitar"
  region: "Hawaii"
  family: "chordophone"
  midi_program: 25  # Acoustic Guitar (steel)
  playing: "horizontal (lap steel)"
  technique:
    slide: "steel bar slide"
    vibrato: "bar movement"
  tunings:
    taropatch: ["E3", "B3", "E3", "G3", "B3", "E3"]  # Open G
    waikiki: ["E3", "A3", "E3", "A3", "C#4", "E3"]
```

## Bagpipe

```yaml
bagpipe:
  name: "Great Highland Bagpipe"
  region: "Scotland"
  family: "aerophone"
  midi_program: 109  # Bagpipe
  chanter:
    range: {min: 67, max: 84}
    scale: "mixolydian mode (9-note scale)"
  drones:
    count: 3
    tuning: ["A3", "A3", "E4"]
  regulators:
    count: 3  # Optional
  technique:
    continuous: "continuous sound (no staccato)"
    gracing: "rapid grace notes"
```

## Irish Tin Whistle

```yaml
tin_whistle:
  name: "Tin Whistle (Penny Whistle)"
  region: "Ireland"
  family: "aerophone (fipple flute)"
  midi_program: 72  # Clarinet
  types:
    D:
      name: "D Whistle"
      range: {min: 67, max: 88}
    C:
      name: "C Whistle"
      range: {min: 60, max: 84}
  technique:
    breathing: "diaphragm vibrato"
    ornamentation: ["grace note", "roll", "crann", "birl"]
```

## Uilleann Pipes

```yaml
uilleann_pipes:
  name: "Uilleann Pipes"
  region: "Ireland"
  family: "aerophone"
  chanter:
    range: {min: 64, max: 88}
    keys: "two-octave fully chromatic"
  regulators:
    count: 3
  drones:
    count: 3
```

## Accordion

```yaml
accordion:
  name: "Piano Accordion"
  region: "Europe"
  family: "aerophone (free reed)"
  midi_program: 21  # Accordion
  registers:
    treble: 41 keys
    bass: 120 buttons
  bellows: "pressure direction controls volume"
```

## Bandoneon

```yaml
bandoneon:
  name: "Bandoneon"
  region: "Argentina"
  family: "aerophone (free reed)"
  midi_program: 21  # Accordion
  type: "bisonoric (different note in/out)"
  usage: "Tango"
```

## Files to Create

- `resources/instrument_definitions_world.yaml` (remaining)
- `src/musicgen/instruments/other_world.py`

## Success Criteria

- [ ] All remaining world instruments defined
- [ ] Techniques documented
- [ ] MIDI mappings assigned

## Next Steps

After completion, proceed to Phase 4: Pattern Manipulation (V4-21)
