# V4-15: Indian Raga System

## Overview

Implement the Indian raga system including scales, talas, and composition structure.

## Objectives

1. Define common ragas with their swaras
2. Define that (parent scales) system
3. Define tala (rhythm cycle) system
4. Implement raga composition structure (alap, jor, gat)
5. Create raga-to-JSON/MIDI conversion

## Raga Definition

```python
class Raga(BaseModel):
    """Indian raga definition"""
    name: str
    that: str  # Parent scale
    aroha: list[str]  # Ascending notes
    avaroha: list[str]  # Descending notes
    vadi: str  # Most important note
    samvadi: str  # Second most important
    pakad: list[str]  # Characteristic phrase
    time: str | None  # Recommended performance time
    rasa: str  # Emotional mood
    thaat: str  # Parent scale name
```

## Common Ragas

```yaml
# Major ragas
ragas:

  # Evening Ragas (6 PM - 9 PM)
  yaman:
    name: "Yaman (Yaman Kalyan)"
    that: "Bilaval"
    aroha: ["Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni", "Sa'"]
    avaroha: ["Sa'", "Ni", "Dha", "Pa", "Ma", "Ga", "Re", "Sa"]
    vadi: "Ga"  # Gandhar (3rd)
    samvadi: "Ni"  # Nishad (7th)
    pakad: ["Ni Re Ga", "Ma Pa Dha Pa", "Ma Ga", "Re Sa"]
    time: "evening (first prahar: 6-9 PM)"
    rasa: "peaceful, romantic"
    chalan: "ascent and descent are straight"

  bhairavi:
    name: "Bhairavi"
    that: "Bhairavi"
    aroha: ["Sa", "Re_k", "Ga_k", "Ma", "Pa", "Dh_k", "Ni_k", "Sa'"]
    avaroha: ["Sa'", "Ni_k", "Dh_k", "Pa", "Ma", "Ga_k", "Re_k", "Sa"]
    vadi: "Ma"  # Madhyam (4th)
    samvadi: "Sa"  # Tonic
    pakad: ["Ga_k Ma Dha_k Ni_k Dha_k Ma", "Pa Ma Ga_k Ma Re_k Sa"]
    time: "morning (second prahar: 9-12 AM)"
    rasa: "devotional, early morning"

  # Late Night Ragas (9 PM - 12 AM)
  darbari:
    name: "Darbari Kanada"
    that: "Asavari"
    aroha: ["Sa", "Re_k", "Ga_k", "Ma", "Pa", "Dh_k", "Ni_k", "Sa'"]
    avaroha: ["Sa'", "Ni_k", "Dh_k", "Pa", "Ma", "Pa", "Ga_k", "Ma", "Re_k", "Sa"]
    vadi: "Dh_k"  # Komal Dha (flat 6th)
    samvadi: "Ga_k"  # Komal Ga (flat 3rd)
    pakad: ["Re_k Sa Ma Pa", "Ma Pa Ni_k Dha_k Ma", "Pa Ma Ga_k Ma Re_k Sa"]
    time: "late night (midnight: 12-3 AM)"
    rasa: "deep, melancholic, romantic"
    notes: "all komal except Pa and Ma"

  # Morning Ragas (6 AM - 9 AM)
  ahir_bhairav:
    name: "Ahir Bhairav"
    that: "Bhairav"
    aroha: ["Sa", "Re_k", "Ga_k", "Ma", "Pa", "Dh", "Ni_k", "Sa'"]
    avaroha: ["Sa'", "Ni_k", "Dh", "Pa", "Ma", "Ga_k", "Re_k", "Sa"]
    vadi: "Sa"  # Tonic
    samvadi: "Pa"  # Pancham (5th)
    pakad: ["Sa Re_k Ma Pa", "Ga_k Ma Dha Ni_k Dha Ma Pa"]
    time: "early morning (first prahar: 6-9 AM)"
    rasa: "devotional, contemplative"

  bhimpalasi:
    name: "Bhimpalasi"
    that: "Kafi"
    aroha: ["Sa", "Ga_k", "Ma", "Pa", "Ni_k", "Sa'"]
    avaroha: ["Sa'", "Ni_k", "Dh_k", "Pa", "Ma", "Ga_k", "Re_k", "Sa"]
    vadi: "Ga_k"  # Komal Gandhar
    samvadi: "Dh_k"  # Komal Dha
    pakad: ["Ga_k Ma Dha_k Ni_k", "Dha_k Ma Pa", "Ga_k Ma Re_k Sa"]
    time: "late afternoon (fifth prahar: 3-6 PM)"
    rasa: "pathos, yearning"

  # Other Notable Ragas
  malkauns:
    name: "Malkauns"
    that: "Bhairavi"
    aroha: ["Sa", "Ga_k", "Ma", "Dh_k", "Ni_k", "Sa'"]
    avaroha: ["Sa'", "Ni_k", "Dh_k", "Ma", "Ga_k", "Sa"]
    vadi: "Dh_k"
    samvadi: "Ga_k"
    pakad: ["Ga_k Ma Dha_k Ni_k Dha_k Ma", "Pa Ga_k Ma"]
    time: "midnight (third prahar: 12-3 AM)"
    rasa: "serious, mysterious"

  rageshri:
    name: "Rageshri"
    that: "Khamaj"
    aroha: ["Sa", "Re", "Ga", "Ma", "Pa", "Dh", "Ni", "Sa'"]
    avaroha: ["Sa'", "Ni", "Dh", "Pa", "Ma", "Ga", "Re", "Sa"]
    vadi: "Ma"  # But with Pa and Ma both important
    samvadi: "Sa"
    pakad: ["Re Ga Ma Pa", "Ma Pa Dha Ni Sa'", "Dha Ma Pa Ga Ma Re Sa"]
    time: "late evening (second prahar: 9-12 PM)"
    rasa: "romantic, serene"

  bageshri:
    name: "Bageshri"
    that: "Kafi"
    aroha: ["Sa", "Ga_k", "Ma", "Pa", "Ni", "Sa'"]
    avaroha: ["Sa'", "Ni", "Dh_k", "Pa", "Ma", "Ga_k", "Re_k", "Sa"]
    vadi: "Ma"
    samvadi: "Sa"
    pakad: ["Ga_k Ma Pa", "Ma Pa Ni Dha_k Ni Pa", "Ma Ga_k Re_k Sa"]
    time: "late night (third prahar: 12-3 AM)"
    rasa: "romantic, devotional"

  tilak_kamod:
    name: "Tilak Kamod"
    that: "Khamaj"
    aroha: ["Sa", "Re", "Ga", "Pa", "Dh", "Ni", "Sa'"]
    avaroha: ["Sa'", "Ni", "Dh, "Pa", "Ga", "Re", "Sa"]
    vadi: "Ga"
    samvadi: "Ni"
    pakad: ["Sa Re Ga Pa", "Ga Ma Dha Ni", "Ni Dha Pa Ga Re Sa"]
    time: "evening (first prahar: 6-9 PM)"
    rasa: "playful, romantic"

  charukesi:
    name: "Charukesi"
    that: "None (mixed that)"
    aroha: ["Sa", "Re", "Ga", "Ma_t", "Pa", "Dh", "Ni", "Sa'"]
    avaroha: ["Sa'", "Ni", "Dh", "Pa", "Ma", "Ga", "Re", "Sa"]
    vadi: "Pa"
    samvadi: "Sa"
    pakad: ["Ga Ma_t Pa", "Ma_t Pa Dha Ni", "Dha Ma_t Ga Re Sa"]
    time: "evening"
    rasa: "devotional, intense"
```

## That System (Parent Scales)

```yaml
# Bhatkhande's 10 Thats
thats:
  bilaval:
    name: "Bilaval (Lydian)"
    pattern: "Sa Re Ga Ma Pa Dha Ni Sa"
    notes: ["Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni"]

  khamaj:
    name: "Khamaj (Mixolydian)"
    pattern: "Sa Re Ga Ma Pa Dha Ni_k Sa"
    notes: ["Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni_k"]

  kafi:
    name: "Kafi (Dorian)"
    pattern: "Sa Re Ga_k Ma Pa Dha_k Ni_k Sa"
    notes: ["Sa", "Re", "Ga_k", "Ma", "Pa", "Dh_k", "Ni_k"]

  bhairavi:
    name: "Bhairavi (Phrygian)"
    pattern: "Sa Re_k Ga_k Ma Pa Dh_k Ni_k Sa"
    notes: ["Sa", "Re_k", "Ga_k", "Ma", "Pa", "Dh_k", "Ni_k"]

  kalyan:
    name: "Kalyan / Yaman (Lydian #4)"
    pattern: "Sa Re Ga Ma_t Pa Dha Ni Sa"
    notes: ["Sa", "Re", "Ga", "Ma_t", "Pa", "Dha", "Ni"]

  asavari:
    name: "Asavari (Aeolian)"
    pattern: "Sa Re Ga_k Ma Pa Dh_k Ni_k Sa"
    notes: ["Sa", "Re", "Ga_k", "Ma", "Pa", "Dh_k", "Ni_k"]

  bhairav:
    name: "Bhairav (double harmonic)"
    pattern: "Sa Re_k Ga_k Ma Pa Dha Ni_k Sa"
    notes: ["Sa", "Re_k", "Ga_k", "Ma", "Pa", "Dha", "Ni_k"]

  purvi:
    name: "Purvi"
    pattern: "Sa Re_k Ga Ma_t Pa Dha Ni_k Sa"
    notes: ["Sa", "Re_k", "Ga", "Ma_t", "Pa", "Dha", "Ni_k"]

  marwa:
    name: "Marwa"
    pattern: "Sa Re_k Ga Ma_t Pa Dha Ni Sa"
    notes: ["Sa", "Re_k", "Ga", "Ma_t", "Pa", "Dha", "Ni"]

  todi:
    name: "Todi"
    pattern: "Sa Re_k Ga_k Ma_t Pa Dh_k Ni_k Sa"
    notes: ["Sa", "Re_k", "Ga_k", "Ma_t", "Pa", "Dh_k", "Ni_k"]
```

## Swara (Note) Names

```yaml
# Indian note names and their relationships
swaras:
  shuddha:
    Sa: {name: "Shadja", ratio: "1/1", cents: 0}
    Re: {name: "Rishabh", ratio: "9/8", cents: 204}
    Ga: {name: "Gandhar", ratio: "5/4", cents: 386}
    Ma: {name: "Madhyam", ratio: "4/3", cents: 498}
    Pa: {name: "Pancham", ratio: "3/2", cents: 702}
    Dha: {name: "Dhaivat", ratio: "27/16", cents: 906}
    Ni: {name: "Nishad", ratio: "15/8", cents: 1116}

  komal:
    Re_k: {name: "Komal Re", ratio: "16/15", cents: 112}
    Ga_k: {name: "Komal Ga", ratio: "6/5", cents: 316}
    Dha_k: {name: "Komal Dha", ratio: "16/9", cents: 996}
    Ni_k: {name: "Komal Ni", ratio: "9/5", cents: 1018}

  tivra:
    Ma_t: {name: "Tivra Ma", ratio: "45/32", cents: 590}
```

## Tala (Rhythm Cycle) System

```yaml
talas:
  # Most common talas
  teental:
    name: "Teental (Tintal)"
    matra: 16  # Beats
    vibhag: [4, 4, 4, 4]  # Sections
    bol: "dha dhin dhin dha | dha dhin dhin dha | dha dhin dhin dha | dha dhin dhin dha"
    khali: [5, 13]  # Wave (empty) sections
    tali: [1, 5, 13]  # Clap sections

  jhaptal:
    name: "Jhaptal"
    matra: 10
    vibhag: [2, 3, 4, 1]
    bol: "dha dhin na | dha dhin dhin | na dha dhin | dha"
    khali: [6]
    tali: [1, 4, 11]

  rupak:
    name: "Rupak"
    matra: 7
    vibhag: [3, 2, 2]
    bol: "tin tin na | dha dhin | na"
    khali: [1]
    tali: [4, 7]

  ektal:
    name: "Ektal"
    matra: 12
    vibhag: [4, 4, 4]
    bol: "dhin dhin dha dha | dha dhin dha dha | dha dhin dha dha"
    khali: [1, 9]
    tali: [1, 5, 13]

  dadra:
    name: "Dadra"
    matra: 6
    vibhag: [3, 3]
    bol: "dha dhin dha | dha dhin dha"
    khali: [1]
    tali: [4]

  keherwa:
    name: "Keherwa"
    matra: 8
    vibhag: [4, 4]
    bol: "dha ge na te | na ge na te"
    khali: [1]
    tali: [5]
```

## Raga Composition Structure

```python
class RagaComposition(BaseModel):
    """Raga-based composition structure"""
    raga: Raga
    tala: str
    tempo: int  # BPM

    # Alap (introduction without rhythm)
    alap_duration: float  # In minutes
    alap_sections: list[str]  # ["vilambit", "madhya", "drut"]

    # Jor (with rhythm but no tala)
    jor_duration: float
    jor_tempo_progression: list[int]

    # Gat (composed section with tala)
    gat:
      asthai: list[str]  # Main theme
      antara: list[str]  # Second theme
      sanchari: list[str] | None  # Optional third theme
      abhog: list[str] | None  # Optional fourth theme
```

## Raga Generator

```python
class RagaGenerator:
    """Generate music based on raga system"""

    def generate_alap(
        self,
        raga: Raga,
        duration: float,
        instrument: str = "sitar"
    ) -> AIComposition:
        """Generate alap (introduction)"""

    def generate_gat(
        self,
        raga: Raga,
        tala: str,
        asthai: list[str],
        instrument: str = "sitar",
        tabla: bool = True
    ) -> AIComposition:
        """Generate gat with tala cycle"""

    def apply_pakad(
        self,
        raga: Raga,
        composition: AIComposition
    ) -> AIComposition:
        """Apply raga's characteristic phrases"""
```

## Files to Create

- `src/musicgen/scales/ragas.py`
- `resources/raga_definitions.yaml`
- `src/musicgen/genres/indian_classical.py`

## Success Criteria

- [ ] Major ragas defined with correct notes
- [ ] That system implemented
- [ ] Tala system with all common talas
- [ ] Swara mapping to MIDI
- [ ] Raga composition structure working
- [ ] Alap, Jor, Gat generation
- [ ] Tests for raga system

## Next Steps

After completion, proceed to V4-16: Middle Eastern Instruments
