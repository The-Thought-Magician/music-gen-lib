# V3-02: SFZ Instrument Definition Layer

**Status:** Pending
**Priority:** High
**Dependencies:** V3-01

## Overview

Create a comprehensive YAML-based configuration system that defines every orchestral instrument with its SFZ properties, including ranges, articulations, keyswitches, and dynamic layers.

## Goals

1. Define all orchestral instruments with SFZ-specific properties
2. Support per-dynamic ranges (pp range ≠ ff range)
3. Define articulation mappings with keyswitch values
4. Enable ensemble definitions for quick orchestration

## Data Model

### Instrument Definition

```yaml
instruments:
  violin_section:
    name: "Violin Section"
    family: "strings"
    midi_program: 40  # GM violin
    default_clef: "treble"

    # Pitch range (MIDI note numbers)
    range:
      min: 55  # G3
      max: 123 # B7

    # Range per dynamic (important! pp range is smaller)
    dynamic_ranges:
      ppp: {min: 60, max: 84}
      pp:  {min: 55, max: 88}
      p:   {min: 55, max: 96}
      mp:  {min: 55, max: 103}
      mf:  {min: 55, max: 110}
      f:   {min: 55, max: 116}
      ff:  {min: 55, max: 120}
      fff: {min: 60, max: 123}

    # Articulations with keyswitch values
    articulations:
      sustain:
        keyswitch: 24  # C1
        duration_mod: 1.0
        velocity_mod: 1.0
        description: "Normal bowing, sustained notes"

      staccato:
        keyswitch: 25  # C#1
        duration_mod: 0.4
        velocity_mod: 1.15
        description: "Short, detached notes"

      pizzicato:
        keyswitch: 26  # D1
        duration_mod: 0.3
        velocity_mod: 1.2
        description: "Plucked strings"

      tremolo:
        keyswitch: 27  # D#1
        duration_mod: 1.0
        velocity_mod: 0.85
        description: "Rapid bow motion"

      legato:
        keyswitch: 28  # E1
        duration_mod: 1.0
        velocity_mod: 0.95
        description: "Smooth, connected notes"

      spiccato:
        keyswitch: 29  # F1
        duration_mod: 0.3
        velocity_mod: 1.1
        description: "Bounced bow"

      sul_ponticello:
        keyswitch: 30  # F#1
        duration_mod: 1.0
        velocity_mod: 0.9
        description: "Bowing near bridge, metallic"

      col_legno:
        keyswitch: 31  # G1
        duration_mod: 0.5
        velocity_mod: 0.8
        description: "With wood of the bow"

    # SFZ file reference
    sfz_file: "libraries/sso/strings/violin_section.sfz"
    sfz_library: "sso"  # Sonatina Symphonic Orchestra

    # MIDI channel assignment (for multi-port setups)
    midi_channel: 0
```

### Complete Instrument List

#### Strings

| Instrument | MIDI Program | Range (MIDI) | Clef |
|------------|--------------|--------------|------|
| Violin Section | 40 | 55-123 | treble |
| Violin Solo | 40 | 55-127 | treble |
| Viola Section | 41 | 48-110 | alto |
| Viola Solo | 41 | 48-116 | alto |
| Cello Section | 42 | 36-76 | bass |
| Cello Solo | 42 | 36-82 | bass |
| Double Bass Section | 43 | 28-67 | bass |
| Double Bass Solo | 43 | 28-70 | bass |
| Harp | 46 | 23-103 | treble/bass |

#### Woodwinds

| Instrument | MIDI Program | Range (MIDI) | Clef |
|------------|--------------|--------------|------|
| Piccolo | 71 | 74-127 | treble |
| Flute | 73 | 60-96 | treble |
| Oboe | 74 | 58-88 | treble |
| English Horn | 75 | 52-76 | treble |
| Clarinet (Bb) | 76 | 50-94 | treble |
| Bass Clarinet | 77 | 38-76 | treble |
| Bassoon | 78 | 34-76 | bass |
| Contrabassoon | 79 | 28-62 | bass |

#### Brass

| Instrument | MIDI Program | Range (MIDI) | Clef |
|------------|--------------|--------------|------|
| Trumpet (C) | 56 | 52-83 | treble |
| Trumpet (Bb) | 56 | 54-85 | treble |
| French Horn | 60 | 34-77 | treble |
| Trombone | 57 | 34-76 | bass |
| Bass Trombone | 57 | 34-73 | bass |
| Tuba | 58 | 28-64 | bass |

#### Percussion (Keyed/Pitched)

| Instrument | MIDI Program | Range (MIDI) | Clef |
|------------|--------------|--------------|------|
| Timpani | 47 | 36-52 | bass |
| Glockenspiel | 9 | 84-108 | treble |
| Xylophone | 13 | 60-96 | treble |
| Marimba | 12 | 48-84 | treble |
| Vibraphone | 11 | 48-79 | treble |
| Celesta | 8 | 60-96 | treble |
| Tubular Bells | 14 | 48-77 | treble |
| Chimes | 14 | 48-77 | treble |

#### Keyboards

| Instrument | MIDI Program | Range (MIDI) | Clef |
|------------|--------------|--------------|------|
| Piano | 0 | 21-108 | grand staff |
| Harpsichord | 6 | 21-108 | grand staff |

### Ensemble Definitions

```yaml
ensembles:
  string_quartet:
    name: "String Quartet"
    instruments:
      - violin_solo
      - violin_solo
      - viola_solo
      - cello_solo

  string_orchestra:
    name: "String Orchestra"
    instruments:
      - violin_section
      - violin_section
      - viola_section
      - cello_section
      - double_bass_section
      - harp

  woodwind_quintet:
    name: "Woodwind Quintet"
    instruments:
      - flute
      - oboe
      - clarinet
      - bassoon
      - french_horn

  full_orchestra:
    name: "Full Orchestra"
    instruments:
      # Strings
      - violin_section
      - violin_section
      - viola_section
      - cello_section
      - double_bass_section
      # Woodwinds (2 each)
      - flute
      - flute
      - oboe
      - oboe
      - clarinet
      - clarinet
      - bassoon
      - bassoon
      # Brass
      - french_horn
      - french_horn
      - trumpet
      - trumpet
      - trombone
      - tuba
      # Percussion
      - timpani
      - glockenspiel
```

## Python Schema

```python
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, Field

class DynamicRange(BaseModel):
    min: int = Field(ge=0, le=127)
    max: int = Field(ge=0, le=127)

class Articulation(BaseModel):
    keyswitch: int = Field(ge=0, le=127, description="MIDI keyswitch note")
    duration_mod: float = Field(gt=0, description="Duration multiplier")
    velocity_mod: float = Field(gt=0, description="Velocity multiplier")
    description: str = ""

class InstrumentDefinition(BaseModel):
    name: str
    family: Literal["strings", "woodwinds", "brass", "percussion", "keyboards"]
    midi_program: int = Field(ge=0, le=127)
    default_clef: Literal["treble", "bass", "alto", "tenor", "grand_staff"]
    range: DynamicRange
    dynamic_ranges: dict[str, DynamicRange]
    articulations: dict[str, Articulation]
    sfz_file: Path
    sfz_library: str
    midi_channel: int = Field(ge=0, le=15)

class EnsembleDefinition(BaseModel):
    name: str
    instruments: list[str]  # References to instrument keys

class InstrumentLibrary(BaseModel):
    instruments: dict[str, InstrumentDefinition]
    ensembles: dict[str, EnsembleDefinition]
```

## Directory Structure

```
resources/
├── sfz_libraries/
│   ├── sso/
│   │   ├── strings/
│   │   ├── woodwinds/
│   │   ├── brass/
│   │   └── percussion/
│   ├── vpo/
│   │   └── ...
│   └── salamander_piano/
│       └── ...
└── instrument_definitions.yaml
```

## Implementation Tasks

1. [ ] Create `InstrumentDefinition` Pydantic models
2. [ ] Create `instrument_definitions.yaml` with all orchestral instruments
3. [ ] Add per-dynamic ranges for all instruments
4. [ ] Define articulation mappings for each instrument
5. [ ] Create ensemble definitions
6. [ ] Add validation for SFZ file existence
7. [ ] Create loader for YAML definitions

## Success Criteria

- All orchestral instruments defined with complete properties
- YAML file validates against Pydantic schema
- Dynamic ranges properly reflect real instrument capabilities
- Articulation keyswitches documented

## Next Steps

- V3-03: SFZ Renderer Integration
- V3-04: Articulation System Design
