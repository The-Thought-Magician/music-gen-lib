# V4-28: Genre Profile Definitions

## Overview

Define comprehensive genre profiles with instrumentation, rhythms, and characteristics.

## Objectives

1. Define Rock/Pop profiles
2. Define Jazz profiles
3. Define Classical profiles
4. Define Electronic profiles
5. Define World genre profiles

## Genre Profile Structure

```python
class GenreProfile(BaseModel):
    """Genre characteristics profile"""
    name: str
    parent: str | None = None
    instrumentation: dict[str, list[str]]  # Role -> instruments
    drum_style: str
    tempo_range: tuple[int, int]
    time_signatures: list[tuple[int, int]]
    key_characteristics: list[str]  # Common keys
    chord_progressions: list[list[str]]
    patterns: dict[str, str]
    mood: str | None = None
```

## Genre Definitions

```yaml
genres:
  rock:
    name: "Rock"
    tempo_range: [100, 140]
    time_signatures: [[4, 4]]
    instrumentation:
      drums: ["kick", "snare", "hihat", "crash", "ride"]
      bass: ["electric_bass"]
      guitar: ["electric_guitar_clean", "electric_guitar_overdrive"]
      keys: ["piano", "organ"]
      vocals: ["male_vocal", "female_vocal"]
    patterns:
      drum: "basic_16th"
      guitar: "power_chords"
      bass: "root_fifth"
    chord_progressions: [["I", "V", "vi", "IV"], ["I", "IV", "V", "IV"]]

  jazz:
    name: "Jazz"
    tempo_range: [80, 160]
    time_signatures: [[4, 4], [3, 4], [5, 4]]
    instrumentation:
      drums: ["kick", "snare", "ride", "hihat"]
      bass: ["acoustic_bass", "electric_bass"]
      keys: ["piano"]
      winds: ["saxophone", "trumpet"]
    patterns:
      drum: "swing"
      bass: "walking"
    chord_progressions: [["ii7", "V7", "Imaj7"], ["vi7", "ii7", "V7", "Imaj7"]]

  classical_orchestral:
    name: "Classical (Orchestral)"
    tempo_range: [60, 120]
    time_signatures: [[2, 4], [3, 4], [4, 4], [6, 8]]
    instrumentation: "full_orchestra"
    forms: ["sonata", "symphony", "concerto"]

  electronic:
    subgenres:
      techno:
        tempo_range: [120, 140]
        instrumentation: ["synth", "drum_machine"]
        patterns: ["four_on_floor"]
      house:
        tempo_range: [115, 130]
        instrumentation: ["synth", "drum_machine"]
      ambient:
        tempo_range: [60, 100]
        instrumentation: ["synth_pad", "textures"]

  blues:
    tempo_range: [60, 100]
    instrumentation: ["electric_guitar", "electric_bass", "drums", "harmonica"]
    chord_progressions: [["I7", "IV7", "I7", "V7"]]

  country:
    tempo_range: [80, 140]
    instrumentation: ["acoustic_guitar_steel", "acoustic_guitar_nylon", "fiddle", "banjo"]

  folk:
    tempo_range: [80, 120]
    instrumentation: ["acoustic_guitar", "violin", "vocals", "light_percussion"]

  reggae:
    tempo_range: [60, 90]
    instrumentation: ["electric_guitar", "electric_bass", "drums", "organ", "percussion"]
    patterns:
      guitar: "island_strum"
      bass: "syncopated"
      drums: "one_drop"

  hiphop:
    tempo_range: [80, 120]
    instrumentation: ["synth_bass", "drums", "samples", "vocals"]
    subgenres:
      boombap: [80, 100]
      trap: [120, 140]

  latin:
    subgenres:
      salsa:
        instrumentation: "latin_section"
        tempo_range: [180, 220]
      bossa_nova:
        instrumentation: ["guitar", "piano", "bass", "drums", "percussion"]
        tempo_range: [120, 140]

  edm:
    subgenres:
      drum_and_bass:
        tempo_range: [160, 180]
        time_signatures: [[4, 4], [3, 4]]
      dubstep:
        tempo_range: [130, 150]
      trance:
        tempo_range: [125, 150]
```

## Files to Create

- `resources/genre_profiles.yaml`
- `src/musicgen/genres/profiles.py`

## Success Criteria

- [ ] All major genres defined
- [ ] Subgenres where appropriate
- [ ] Instrumentation per genre
- [ ] Common patterns defined
- [ ] Chord progressions listed

## Next Steps

After completion, proceed to V4-29: Genre Specific Patterns
