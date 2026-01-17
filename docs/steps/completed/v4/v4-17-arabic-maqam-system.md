# V4-17: Arabic Maqam System

## Overview

Implement the Arabic maqam system with quarter-tone scales and ajnas.

## Objectives

1. Define common maqamat (plural of maqam)
2. Define ajna (scale fragments)
3. Implement quarter-tone system
4. Define taqsim (improvisation) patterns
5. Create maqam-to-MIDI conversion

## Maqam Definition

```python
class Maqam(BaseModel):
    """Arabic maqam definition"""
    name: str
    family: str  # Maqam family
    ajnas: list[str]  # Scale fragments
    tonic: str  # Root note
    ghammaz: list[str]  # Dominant notes
    sayr: list[str]  # Melodic progression
    mood: str  # Emotional quality
```

## Common Maqamat

```yaml
maqamat:
  rast:
    name: "Rast"
    family: "Rast"
    tonic: "C"
    ajnas: ["Rast", "Sikah", "Jaharkah"]
    intervals: [0, 100, 200, 300, 350, 500, 600, 700, 800, 900, 1000, 1100, 1200]  # Cents
    notes: ["C", "D_half_flat", "D", "E_half_flat", "F", "G", "A_half_flat", "A", "B_half_flat", "C'"]
    quarter_tones: ["D_half_flat", "E_half_flat", "A_half_flat", "B_half_flat"]
    mood: "proud, majestic"

  bayati:
    name: "Bayati"
    family: "Sikah"
    tonic: "D"
    ajnas: ["Bayati", "Sikah", "Jaharkah"]
    intervals: [0, 200, 300, 500, 600, 700, 900, 1000, 1200]
    notes: ["D", "E_half_flat", "F", "G", "A", "Bb", "C'", "D'"]
    quarter_tones: ["E_half_flat"]
    mood: "populist, sad"

  sikah:
    name: "Sikah"
    family: "Sikah"
    tonic: "E_half_flat"
    intervals: [0, 150, 300, 500, 650, 800, 1000, 1200]
    quarter_tones: ["E_half_flat", "B_half_flat"]

  hijaz:
    name: "Hijaz"
    family: "Hijaz"
    tonic: "D"
    ajnas: ["Hijaz", "Nikriz", "Athar Kurd"]
    intervals: [0, 200, 400, 500, 700, 900, 1000, 1200]
    notes: ["D", "E", "F", "G", "A", "Bb", "C'", "D'"]
    mood: "distant, exotic"

  saba:
    name: "Saba"
    family: "Saba"
    tonic: "D"
    intervals: [0, 200, 250, 500, 600, 700, 900, 1000, 1200]
    mood: "sad, nostalgic"

  kurd:
    name: "Kurd"
    family: "Hijaz"
    tonic: "D"
    intervals: [0, 200, 350, 500, 700, 850, 1000, 1200]
    quarter_tones: true
    mood: "freedom, openness"

  nahawand:
    name: "Nahawand (Minor)"
    family: "Nahawand"
    tonic: "D"
    intervals: [0, 200, 300, 500, 600, 700, 900, 1000, 1200]
    notes: ["D", "E", "F", "G", "A", "Bb", "C'", "D'"]
    mood: "emotional, romantic"

  ajam:
    name: "Ajam (Major)"
    family: "Ajam"
    tonic: "C"
    intervals: [0, 200, 400, 500, 700, 900, 1100, 1200]
    notes: ["C", "D", "E", "F", "G", "A", "B", "C'"]
    mood: "western, familiar"
```

## Quarter-Tone Implementation

```python
# Quarter-tones in Arabic music (approximate cents)
QUARTER_TONES = {
    "half_flat": -50,    # Semi-flat
    "half_sharp": +50,   # Semi-sharp
}

class QuarterToneSystem:
    @staticmethod
    def to_pitch_bend(cents: float) -> int:
        """Convert cents deviation to MIDI pitch bend"""

    @staticmethod
    def note_to_midi(
        note: str,
        quarter_tone: str | None = None
    ) -> tuple[int, int]:
        """Returns (midi_note, pitch_bend)"""
```

## Taqsim (Improvisation)

```python
class TaqsimGenerator:
    """Generate Arabic taqsim (improvisation)"""

    def generate_taqsim(
        self,
        maqam: Maqam,
        duration: float,
        instrument: str = "oud"
    ) -> AIComposition:
        """Generate taqsim with sayr (progression)"""
```

## Files to Create

- `src/musicgen/scales/maqam.py`
- `resources/maqam_definitions.yaml`

## Success Criteria

- [ ] Major maqamat defined
- [ ] Quarter-tone system working
- [ ] Ajnas system implemented
- [ ] Taqsim generation functional

## Next Steps

After completion, proceed to V4-18: East Asian Instruments
