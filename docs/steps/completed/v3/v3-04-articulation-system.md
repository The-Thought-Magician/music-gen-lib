# V3-04: Articulation System Design

**Status:** Pending
**Priority:** High
**Dependencies:** V3-02, V3-03

## Overview

Design and implement a comprehensive articulation system that maps playing techniques to MIDI keyswitches, duration/velocity modifications, and CC messages. This enables the AI to specify "staccato" or "legato" and have it rendered correctly.

## The Articulation Model

### What is an Articulation?

An articulation defines **how** a note is played, not just **what** note is played. In orchestral music, this dramatically changes the character:

```
A violin playing "C4" at mezzo-forte:
├── legato       → Smooth, connected, 100% duration
├── staccato     → Short, detached, 40% duration
├── spiccato     → Bounced bow, 30% duration
├── pizzicato    → Plucked, 25% duration, plucky attack
├── tremolo      → Rapid bow motion, sustained with texture
├── sul tasto    → Over fingerboard, warm, mellow tone
├── sul ponticello → Near bridge, metallic, bright
└── col legno    → With wood, percussive, woody
```

### Articulation Properties

```python
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class ArticulationType(str, Enum):
    # Strings
    LEGATO = "legato"
    DETACHE = "detache"
    STACCATO = "staccato"
    SPICCATO = "spiccato"
    MARCATO = "marcato"
    PIZZICATO = "pizzicato"
    TREMOLO = "tremolo"
    TRILL = "trill"
    SUL_TASTO = "sul_tasto"
    SUL_PONTICELLO = "sul_ponticello"
    COL_LEGNO = "col_legno"
    HARMONIC = "harmonic"

    # Woodwinds
    FLUTTER = "flutter_tongue"
    FLUTTER_WW = "flutter_ww"
    STACCATO_WW = "staccato_ww"
    LEGATO_WW = "legato_ww"

    # Brass
    MARTMELLO_BRASS = "martello"
    STACCATO_BRASS = "staccato_brass"
    LEGATO_BRASS = "legato_brass"
    MUZZLE_BRASS = "muted"
    FALL = "fall"
    DOIT = "doit"
    SHAKE = "shake"

    # General
    NORMAL = "normal"
    ACCENT = "accent"
    MARCATO_SHORT = "marcato_short"
    TENUTO = "tenuto"

class Articulation(BaseModel):
    """Definition of an articulation for an instrument."""

    name: str
    type: ArticulationType

    # MIDI keyswitch (note below range to trigger articulation)
    keyswitch: int | None = None

    # Duration modification (multiplier)
    duration_multiplier: float = 1.0

    # Velocity modification (multiplier)
    velocity_multiplier: float = 1.0

    # CC messages for this articulation
    cc_messages: dict[int, int] = {}  # CC number -> value

    # Description for AI understanding
    description: str = ""

    # When to use this articulation (AI guidance)
    usage_context: str = ""
```

### Instrument-Specific Articulation Mappings

#### Violin Section Articulations

```yaml
violin_section_articulations:
  sustain:
    type: legato
    keyswitch: 24  # C1
    duration_multiplier: 1.0
    velocity_multiplier: 1.0
    description: "Normal bowing, sustained notes"
    usage_context: "Default for melodic lines and pad-like passages"

  detache:
    type: detache
    keyswitch: 25  # C#1
    duration_multiplier: 0.85
    velocity_multiplier: 1.0
    description: "Separated but connected strokes"
    usage_context: "Medium-length notes, neither staccato nor legato"

  staccato:
    type: staccato
    keyswitch: 26  # D1
    duration_multiplier: 0.4
    velocity_multiplier: 1.15
    description: "Short, detached notes"
    usage_context: "Rhythmic passages, punctuated accents"

  spiccato:
    type: spiccato
    keyswitch: 27  # D#1
    duration_multiplier: 0.3
    velocity_multiplier: 1.1
    description: "Bowed spiccato, bounced bow"
    usage_context: "Fast, bouncing passages, allegro"

  pizzicato:
    type: pizzicato
    keyswitch: 28  # E1
    duration_multiplier: 0.25
    velocity_multiplier: 1.2
    description: "Plucked with fingers"
    usage_context: "Special effect, jazz-influenced passages"

  tremolo:
    type: tremolo
    keyswitch: 29  # F1
    duration_multiplier: 1.0
    velocity_multiplier: 0.85
    description: "Rapid bow motion for sustained tension"
    usage_context: "Building tension, eerie textures, high drama"

  sul_ponticello:
    type: sul_ponticello
    keyswitch: 30  # F#1
    duration_multiplier: 1.0
    velocity_multiplier: 0.9
    description: "Bowing near the bridge, metallic and bright"
    usage_context: "Tense, eerie, aggressive passages"

  col_legno:
    type: col_legno
    keyswitch: 31  # G1
    duration_multiplier: 0.5
    velocity_multiplier: 0.8
    description: "Struck with the wood of the bow"
    usage_context: "Percussive effects, horror, avant-garde"
```

#### Flute Articulations

```yaml
flute_articulations:
  sustain:
    type: legato_ww
    keyswitch: 24
    description: "Normal breathy tone, connected"

  staccato:
    type: staccato_ww
    keyswitch: 25
    duration_multiplier: 0.35
    velocity_multiplier: 1.1
    description: "Short, detached breaths"

  flutter:
    type: flutter
    keyswitch: 26
    duration_multiplier: 1.0
    description: "Flutter tongue for percussive effect"
    usage_context: "Contemporary, dramatic, or jazz styles"
```

#### Trumpet Articulations

```yaml
trumpet_articulations:
  sustain:
    type: legato_brass
    keyswitch: 24
    description: "Normal tongued tone"

  staccato:
    type: staccato_brass
    keyswitch: 25
    duration_multiplier: 0.35
    velocity_multiplier: 1.15
    description: "Sharp, detached tonguing"

  muted:
    type: muzzle_brass
    keyswitch: 26
    description: "With straight mute, quieter and more focused"
    usage_context: "Jazz, quieter passages, specific color"

  fall:
    type: fall
    keyswitch: 27
    cc_messages:
      # Pitch bend drop at end of note
      1: 0  # Mod wheel for fall depth
    description: "Pitch drops at end of note"
    usage_context: "Jazz, commercial, big band styles"
```

## Articulation Change Events in MIDI

### Keyswitch Approach

Keyswitches are MIDI notes sent **before** the notes they affect. They live in a low range (typically C0-C2) that's outside the instrument's playing range.

```
Timeline:
├───────┬──────────┬──────────┬──────────┬──────────┐
│Keysw  │ Note     │ Note     │ Keysw    │ Note     │
│ C1=24 │ C4 vel80 │ E4 vel75 │ D1=26    │ G4 vel90 │
│(legato│          │          │(staccato │          │
│ mode) │          │          │  mode)   │          │
└───────┴──────────┴──────────┴──────────┴──────────┘
```

### Data Model for Articulation Events

```python
class KeyswitchEvent(BaseModel):
    """A keyswitch event in the MIDI timeline."""

    keyswitch: int           # MIDI note number for keyswitch
    time: float              # Time in seconds
    articulation: ArticulationType
    channel: int = 0         # MIDI channel

class NoteWithArticulation(BaseModel):
    """A note with articulation applied."""

    pitch: int               # MIDI note number
    start_time: float        # Seconds
    duration: float          # Seconds (before articulation mods)
    velocity: int            # 0-127 (before articulation mods)
    articulation: ArticulationType | None = None

    def render_duration(self, articulation_def: Articulation | None) -> float:
        """Get actual duration after articulation modification."""
        base = self.duration
        if articulation_def:
            return base * articulation_def.duration_multiplier
        return base

    def render_velocity(self, articulation_def: Articulation | None) -> int:
        """Get actual velocity after articulation modification."""
        base = self.velocity
        if articulation_def:
            vel = base * articulation_def.velocity_multiplier
            return max(0, min(127, int(vel)))
        return base
```

## AI Output for Articulations

The AI needs to specify articulations in its composition output:

```python
class InstrumentPartWithArticulation(BaseModel):
    """An instrument part with articulation changes."""

    instrument_name: str
    midi_channel: int

    # Articulation changes (keyswitches)
    articulation_changes: list[KeyswitchEvent] = []

    # Notes (inherit current articulation)
    notes: list[NoteWithArticulation] = []

    # CC events (for expression, vibrato, etc.)
    cc_events: list[CCEvent] = []
```

## Articulation Transition Rules

### Practical Guidelines for AI

```yaml
articulation_transition_rules: |
  When changing articulations:

  1. Keyswitch Timing: Send keyswitch 50-100ms before first note
     with new articulation

  2. Minimum Duration: Don't change articulations more frequently than
     every 2-4 beats unless musically justified

  3. Phrase Cohesion: Keep articulations consistent within phrases
     - A phrase typically 4-8 measures
     - Change articulations at phrase boundaries

  4. Default Articulations by Style:
     - Lyrical melodic lines: legato
     - Rhythmic accompaniment: staccato or spiccato
     - Building tension: tremolo or sustained
     - Light, playful: staccato or spiccato
     - Dark, mysterious: sul ponticello or tremolo
     - Aggressive, marcato: martellato or marcatissimo

  5. Articulation Combinations:
     - Strings can combine: sul ponticello + tremolo
     - Winds can combine: flutter + staccato (rare)
     - Brass: falls + muted is common in jazz

  6. Dynamic Considerations:
     - pp passages: lighter articulations (legato, sul tasto)
     - ff passages: heavier articulations (marcato, detache)
     - Extreme dynamics: consider articulation's dynamic range
```

## Implementation Tasks

1. [ ] Define `Articulation` data model
2. [ ] Create `KeyswitchEvent` model
3. [ ] Create instrument-specific articulation mappings (YAML)
4. [ ] Update `Note` model to include articulation
5. [ ] Implement keyswitch insertion in MIDI generator
6. [ ] Add articulation duration/velocity modification
7. [ ] Document articulation transition rules for AI
8. [ ] Add validation for keyswitch ranges

## Success Criteria

- All articulations defined for each instrument family
- Keyswitch events properly placed in MIDI output
- Note duration/velocity modified correctly
- AI can specify articulations by name

## Next Steps

- V3-05: Enhanced MIDI Generator with Keyswitches
- V3-06: Comprehensive Music Theory System Prompt
