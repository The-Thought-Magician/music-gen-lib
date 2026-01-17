# V4-14: Indian Classical Instruments

## Overview

Define specifications for Indian classical instruments with their unique playing techniques and microtonal requirements.

## Objectives

1. Define Sitar instrument specifications
2. Define Sarod specifications
3. Define Bansuri specifications
4. Define Tanpura specifications
5. Define Santoor specifications
6. Implement microtonal support

## Sitar

```yaml
sitar:
  name: "Sitar"
  region: "India"
  family: "chordophone"
  midi_program: 104  # GM sitar
  strings:
    main:
      count: 6 or 7
      tuning: ["F#2", "F#2", "C3", "C3", "G3", "G3", "C4"]  # Pa system
      # Or: ["C2", "C2", "G2", "G2", "C3", "C3", "C4"]  # Viyaas system
    sympathetic:
      count: 11-13
      tuning: "variable (raga-specific)"
    chikari:
      count: 2
      tuning: ["C4", "C4"]  # Drone strings
  range: {min: 43, max: 96}  # G#2 to C6
  frets:
    type: "movable"
    count: 20-22
    microtonal: true
  techniques:
    meend:
      name: "Meend (Glissando)"
      description: "Smooth slide between notes"
      duration: "variable"
    gamak:
      name: "Gamak"
      description: "Oscillation around note"
      oscillation: "5-10 cents"
    krintan:
      name: "Krintan"
      description: "Pull across frets (like hammer-on)"
      direction: "pull only"
    zamzama:
      name: "Zamzama"
      description: "Tremolo on one string"
    sparsh:
      name: "Sparsh"
      description: "Pluck with fingernail"
    da:
      name: "Da"
      description: "Downward stroke"
    ra:
      name: "Ra"
      description: "Upward stroke"
    dir_dir:
      name: "Dir Dir"
      description: "Fast double stroke (tremolo)"
```

## Sarod

```yaml
sarod:
  name: "Sarod"
  region: "India"
  family: "chordophone"
  strings:
    main:
      count: 4
      tuning: ["C2", "G2", "C3", "C3"]  # Pa to Pa
    sympathetic:
      count: 11
    chikari:
      count: 2
  range: {min: 36, max: 84}  # C2 to C5
  frets:
    type: "none (fretless)"
    fingering: "fingernail cuticle"
  techniques:
    mind:
      name: "Mind"
      description: "Deflected stroke with fingernail"
    meend:
      name: "Meend"
      description: "Slide (smooth on fretless)"
    gamak:
      name: "Gamak"
      description: "Wide vibrato with finger pressure"
    sparc:
      name: "Sparc"
      description: "Fast tremolo with fingernail"
```

## Bansuri

```yaml
bansuri:
  name: "Bansuri (Bamboo Flute)"
  region: "India"
  family: "aerophone"
  midi_program: 73  # GM flute (use with specific tuning)
  types:
    bass:
      name: "Bansuri (Bass)"
      length: "~32 inch"
      range: {min: 48, max: 72}  # C3 to C5
      tuning: "E bass"
    male:
      name: "Bansuri (Male/Medium)"
      length: "~28 inch"
      range: {min: 55, max: 81}  # G3 to A5
      tuning: "E medium"
    female:
      name: "Bansuri (Female/Treble)"
      length: "~20 inch"
      range: {min: 64, max: 88}  # E4 to E5
      tuning: "E treble"
  fingering:
    type: "six or seven holes"
    holes: 6  # Or 7 for professional
  techniques:
    meend:
      name: "Meend"
      description: "Glissando between notes"
      implementation: "rolling fingerholes"
    gamak:
      name: "Gamak"
      description: "Shake or oscillation"
    kana:
      name: "Kana"
      description: "Grace note (ornament)"
    murki:
      name: "Murki"
      description: "Quick ornament (2-3 notes)"
    zatka:
      name: "Zatka"
      description: "Quick grace to lower note and back"
  blowing:
    embouchure: "variable tone control"
    breath_pressure: "dynamic control"
```

## Tanpura

```yaml
tanpura:
  name: "Tanpura"
  region: "India"
  family: "chordophone"
  role: "drone"
  strings:
    count: 4 or 5
    tuning:
      # Female/High scale
      female: ["G#3", "G#3", "C#4", "C#4", "C#5"]
      # Male/Medium scale
      male: ["C3", "C3", "G3", "G3", "C4"]
      # Bass/Low scale
      bass: ["F#2", "F#2", "C#3", "C#3", "F#3"]
  playing:
    stroke: "continuous"
    timing: "regular pulse"
    jiva:
      name: "Jiva"
      description: "Slight timing variation for liveliness"
      variation: "2-3 cents"
```

## Santoor

```yaml
santoor:
  name: "Santoor"
  region: "Kashmir/India"
  family: "chordophone (zither)"
  strings:
    count: 87+
    courses: 29  # 3-string courses
  range: {min: 48, max: 84}  # C3 to C6
  bridges:
    type: "movable"
    left: "low strings"
    right: "high strings"
  techniques:
    krintan:
      name: "Krintan"
      description: "Strike on one string, slide to bridge"
    meend:
      name: "Meend"
      description: "Slide across strings"
    gamak:
      name: "Gamak"
      description: "Oscillation on string"
    chhand:
      name: "Chhand"
      description: "Tremolo between two strings"
```

## Additional Instruments

```yaml
shehnai:
  name: "Shehnai"
  region: "India (North)"
  family: "aerophone (double reed)"
  midi_program: 56  # Trumpet (closest)
  range: {min: 60, max: 88}
  techniques:
    meend: "Limited (finger keys)"
    glissando: "Common"

harmonium:
  name: "Harmonium"
  region: "India"
  family: "aerophone (reed)"
  type: "portable"
  range: {min: 48, max: 84}
  limitations:
    meend: "Very limited"
    vibrato: "Manual (wobble key)"

tabla:
  name: "Tabla"
  region: "India"
  family: "membranophone"
  see: V4-15 Indian Raga System
```

## Microtonal Implementation

```python
class IndianMicrotonalSystem:
    """Handle Indian microtonal requirements"""

    # Sruti (microtone) system
    SRUTI_COUNT = 22  # Shruti in an octave

    # Note that Indian octave is divided into 22 shrutis
    # Approximate cents for each shruti
    SHRUTI_CENTS = [
        0,      # Sa
        56,     # Re komal (flat 2nd)
        112,    # Re (natural 2nd)
        164,    # Ga komal (flat 3rd)
        182,    # Ga (natural 3rd)
        204,    # Ma (perfect 4th)
        246,    # Ma tivra (augmented 4th)
        273,    # Pa (perfect 5th)
        316,    # Dha komal (flat 6th)
        350,    # Dha (natural 6th)
        392,    # Ni komal (flat 7th)
        411,    # Ni (natural 7th)
        453,    # (between Ni and Sa')
        498,    # Sa' (octave)
    ]

    @staticmethod
    def note_to_cents(note: str, shruti_offset: int) -> float:
        """Convert note with shruti offset to cents"""

    @staticmethod
    def cents_to_pitch_bend(cents: float) -> int:
        """Convert cents to MIDI pitch bend value"""
        # MIDI pitch bend: 0 = -2 semitones, 8192 = center, 16383 = +2 semitones
        return int(8192 + (cents / 100) * 4096)
```

## Raga-Specific Tunings

```python
# Common ragas with their approximate tunings
RAGA_TUNINGS = {
    "Yaman": {
        "notes": ["Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni", "Sa'"],
        "intervals": [0, 204, 386, 498, 702, 906, 1108, 1200],  # Cents
        "that": "Bilaval"
    },
    "Bhairavi": {
        "notes": ["Sa", "Re_k", "Ga_k", "Ma", "Pa", "Dh_k", "Ni_k", "Sa'"],
        "intervals": [0, 112, 182, 498, 702, 784, 880, 1200],
        "that": "Bhairavi"
    },
    "Bhairav": {
        "notes": ["Sa", "Re_k", "Ga_k", "Ma", "Pa", "Dh", "Ni_k", "Sa'"],
        "intervals": [0, 112, 164, 498, 702, 906, 880, 1200],
        "that": "Bhairav"
    },
    # ... more ragas
}
```

## Files to Create

- `resources/instrument_definitions_world.yaml` (Indian section)
- `src/musicgen/instruments/indian.py`
- `src/musicgen/scales/ragas.py`

## Success Criteria

- [ ] All major Indian instruments defined
- [ ] Techniques documented with MIDI implementation
- [ ] Microtonal system functional
- [ ] Raga tuning system working
- [ ] Tests for Indian instruments

## Next Steps

After completion, proceed to V4-15: Indian Raga System
