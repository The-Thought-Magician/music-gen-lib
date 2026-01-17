# V4-18: East Asian Instruments

## Overview

Define East Asian instruments with their unique scales and playing techniques.

## Objectives

1. Define Koto specifications
2. Define Shakuhachi specifications
3. Define Guzheng specifications
4. Define Erhu specifications
5. Implement East Asian scale systems

## Koto (Japan)

```yaml
koto:
  name: "Koto"
  region: "Japan"
  family: "chordophone (zither)"
  midi_program: 6  # Harpsichord (closest)
  strings:
    count: 13
    tuning: "hexatonic scale"
    bridge_movable: true
  range: {min: 48, max: 84}
  tuning:
    hira_joshi: ["G3", "A3", "B3", "D4", "E4", "G4", "A4", "B4", "D5", "E5", "G5", "A5", "B5"]
  techniques:
    atoshi:
      name: "Atoshi"
      description: "Press string to bend pitch"
    mura_iki:
      name: "Mura-iki"
      description: "Tremolo on string"
    sherasher:
      name: "Sherasher"
      description: "Glissando across strings"
```

## Shakuhachi (Japan)

```yaml
shakuhachi:
  name: "Shakuhachi"
  region: "Japan"
  family: "aerophone (flute)"
  midi_program: 72  # Clarinet (closest)
  types:
    1.8:
      name: "1.8 Shakuhachi"
      length: "1.8 shaku"
      range: {min: 52, max: 76}
      key: "D"
  techniques:
    mura_iki:
      name: "Mura-iki"
      description: "Tremolo"
    atoshi:
      name: "Atoshi"
      description: "Head movements for pitch bend"
    sasuari:
      name: "Sasuari"
      description: "Portamento"
```

## Guzheng (China)

```yaml
guzheng:
  name: "Guzheng"
  region: "China"
  family: "chordophone (zither)"
  midi_program: 6  # Harpsichord
  strings:
    count: 21
  range: {min: 48, max: 96}
  tuning:
    pentatonic: ["D3", "E3", "G3", "A3", "B3", "D4", "E4", "G4", "A4", "B4", "D5", ...]
  techniques:
    yaozhi:
      name: "Yaozhi"
      description: "Bend string with left hand"
    glissando: "Common across multiple strings"
```

## Erhu (China)

```yaml
erhu:
  name: "Erhu"
  region: "China"
  family: "chordophone (bowed)"
  midi_program: 40  # Violin (closest)
  strings:
    count: 2
    tuning: ["D4", "A4"]
  range: {min: 52, max: 88}
  techniques:
    vibrato: "Finger position variation"
    glissando: "Slide between notes"
```

## Files to Create

- `resources/instrument_definitions_world.yaml` (East Asian)
- `src/musicgen/instruments/east_asian.py`

## Success Criteria

- [ ] All East Asian instruments defined
- [ ] Pentatonic scale systems working
- [ ] Techniques implemented

## Next Steps

After completion, proceed to V4-19: Pentatonic Scale Systems
