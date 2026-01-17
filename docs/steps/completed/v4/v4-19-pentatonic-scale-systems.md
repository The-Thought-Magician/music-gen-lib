# V4-19: Pentatonic Scale Systems

## Overview

Implement pentatonic scale systems used in world music.

## Objectives

1. Define Japanese pentatonic scales
2. Define other pentatonic modes
3. Create scale-to-MIDI conversion
4. Implement pentatonic composition patterns

## Japanese Pentatonic Scales

```yaml
pentatonic_scales:
  # Japanese scales
  in_scale:
    name: "In-senchi (In scale)"
    region: "Japan"
    intervals: [0, 200, 400, 600, 700]  # Cents from root
    notes: ["C", "D", "F", "G", "Bb"]
    mood: "solemn, temple-like"

  hirajoshi:
    name: "Hirajoshi"
    region: "Japan"
    intervals: [0, 200, 400, 600, 900]
    notes: ["C", "D", "F", "G", "A"]
    mood: "melancholic, folk"

  miyakobushi:
    name: "Miyakobushi"
    region: "Japan"
    intervals: [0, 200, 400, 700, 900]
    notes: ["C", "D", "F", "G", "A"]
    mood: "sad, folk"

  kumoijoshi:
    name: "Kumoijoshi"
    region: "Japan"
    intervals: [0, 300, 400, 600, 900]
    notes: ["C", "Eb", "F", "G", "A"]
    mood: "ancient, ritual"

  # Western pentatonic scales
  major_pentatonic:
    name: "Major Pentatonic"
    intervals: [0, 200, 400, 700, 900]
    notes: ["C", "D", "E", "G", "A"]
    usage: "Rock, pop, country"

  minor_pentatonic:
    name: "Minor Pentatonic"
    intervals: [0, 300, 500, 700, 1000]
    notes: ["C", "Eb", "F", "G", "Bb"]
    usage: "Blues, rock"

  blues:
    name: "Blues Scale"
    intervals: [0, 300, 400, 500, 700, 1000]
    notes: ["C", "Eb", "E", "F", "G", "Bb"]
    blue_note: "Eb (between minor and major 3rd)"
    usage: "Blues, rock, jazz"

  # Other pentatonic scales
  egyptian:
    name: "Egyptian Pentatonic"
    intervals: [0, 200, 500, 700, 900]
    notes: ["C", "D", "F", "G", "A"]

  pelog:
    name: "Pelog (Bali/Java)"
    intervals: [0, 150, 300, 450, 600]
    notes: ["C", "Db", "Eb", "E", "F"]
    temperament: "5-tone unequal division"

  slendro:
    name: "Slendro (Bali/Java)"
    intervals: [0, 240, 480, 720, 960]
    notes: ["C", "D", "E", "G", "A"]
    temperament: "5-tone equal division"
```

## Pentatonic Pattern Generation

```python
class PentatonicComposer:
    """Generate music using pentatonic scales"""

    def generate_melody(
        self,
        scale: PentatonicScale,
        length: int,
        style: str
    ) -> list[str]:
        """Generate melody notes from scale"""

    def generate_ostinato:
        """Generate repeating pattern"""

    def generate_riffs:
        """Generate guitar riffs in pentatonic"""
```

## Files to Create

- `src/musicgen/scales/pentatonic.py`
- `resources/pentatonic_scales.yaml`

## Success Criteria

- [ ] All pentatonic scales defined
- [ ] Scale to MIDI working
- [ ] Pattern generation functional

## Next Steps

After completion, proceed to V4-20: Other World Instruments
