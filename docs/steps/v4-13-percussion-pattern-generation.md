# V4-13: Percussion Pattern Generation

## Overview

Create authentic rhythm patterns for world percussion instruments.

## Objectives

1. Define Afro-Cuban rhythm patterns
2. Define Brazilian rhythm patterns
3. Define Indian tala patterns
4. Define West African polyrhythms
5. Create rhythm composition utilities

## Afro-Cuban Patterns

### Clave Rhythms

```yaml
# The foundational rhythm of Afro-Cuban music
clave_patterns:
  son_clave:
    name: "Son Clave (3-2)"
    region: "Cuba"
    measure_count: 2
    pattern_3: "x . x . . x ."  # 3 side
    pattern_2: ". x . x . . x"  # 2 side
    combined: "x . x . . x . . x . x . . x"
    subdivision: 16

  rumba_clave:
    name: "Rumba Clave (3-2)"
    region: "Cuba"
    pattern_3: "x . x . . . x"
    pattern_2: ". x . x . x ."
    combined: "x . x . . . x . x . x . x ."

  bossa_nova_clave:
    name: "Bossa Nova Clave (3-2)"
    region: "Brazil"
    pattern: "x . x . . x . . x . . x x ."

  6_8_clave:
    name: "6/8 Clave"
    region: "Cuba"
    time_signature: [6, 8]
    pattern: "x . . x x . x ."
```

### Cascara

```yaml
cascara:
  name: "Cascara"
  instrument: "timbale (rim)"
  pattern: "x . x . x x . x . x . x x ."
  region: "Cuba"
  styles: ["son", "salsa"]

# Palito pattern
palito:
  name: "Palito"
  instrument: "timbale (woodblock)"
  pattern: ". x . x . . x . . x . x . ."
```

### Bell Patterns

```yaml
bell_patterns:
  mambo_bell:
    name: "Mambo Bell Pattern"
    instrument: "cowbell"
    pattern: "x . . x . . x . . x x . . x"
    region: "Cuba"

  cha-cha_bell:
    name: "Cha-Cha Bell"
    instrument: "cowbell"
    pattern: "x . x . x . x . x . x . x . x"
    region: "Cuba"
```

### Conga Patterns

```yaml
conga_patterns:
  tumbao:
    name: "Tumbao (Modern)"
    instrument: "congas"
    pattern_quinto: ". . . . . . . . . x . . . ."
    pattern_conga: ". . x . x x . x x . x . x x ."
    pattern_tumba: "x . . . x . . . x . . . x . ."
    region: "Cuba"
    style: "salsa"

  tumbao_traditional:
    name: "Tumbao (Traditional)"
    instrument: "congas"
    pattern: ". . x . x x . x x . x . x x ."

  martillo:
    name: "Martillo"
    instrument: "bongos"
    pattern: "x . x . x x . x . x . x x ."
    region: "Cuba/Puerto Rico"
```

## Brazilian Patterns

### Samba

```yaml
samba:
  name: "Samba"
  region: "Brazil"
  instruments:
    surdo:
      marca: "x . . . . . . ."  # Downbeat
      resposta: ". . . . x . . ."  # Backbeat
    agogo:
      pattern: "x . x . x . x ."
    tamborim:
      pattern: "x x x x x x x x"  # Sixteenth notes
    repinique:
      pattern: "x x x x . x . . x x"
    chocalho:
      pattern: "x x x x x x x x"

  samba_enredo:
    name: "Samba Enredo (Carnival)"
    patterns:
      surdo_1: "x . . . . . . ."
      surdo_2: ". . . . x . . ."
      surdo_3: ". . x . . . x ."
```

### Bossa Nova

```yaml
bossa_nova:
  name: "Bossa Nova"
  region: "Brazil"
  patterns:
    drum_kit:
      kick: "x . . . . . . . . . . . x ."
      snare: ". . x . . . x . . . . x . . ."
      hihat: ". x . x . x . x . . x . x . x ."
    guitar:
      pattern: "x . x . x . x . x"  # Classic rhythm
    percussion:
      guiro: "x . x . x . x . x . x . x . x ."
      agogo: "x . . x . . . x . . x . . ."
```

### Forró

```yaml
forro:
  name: "Forró"
  region: "Brazil"
  patterns:
    zabumba:
      pattern: "x . . . x . . ."
    triangle:
      pattern: "x x x x x x x x"
```

## Indian Rhythm (Tala)

### Tala Definitions

```yaml
# Indian rhythmic cycles (talas)
talas:
  teental:
    name: "Teental (Tintal)"
    vibhag: [4, 4, 4, 4]  # 16 beats, 4 sections
    clapping: ["+ x 2 +", "x 2 + x", "2 + x 2", "+ x 2 +"]
    pattern: "x 2 3 4 | 5 6 7 8 | 9 10 11 12 | 13 14 15 16"
    matra: 16
    bols: ["dha", "dhin", "dhin", "dha"] * 4

  jhaptal:
    name: "Jhaptal"
    vibhag: [2, 3, 4]  # 10 beats, 3 sections
    clapping: ["x 2", "+ 2 3", "x 2 3 4"]
    matra: 10
    bols: ["dha", "dhin", "na", "dha", "dhin", "na", "dha", "dhin", "na", "dha"]

  rupak:
    name: "Rupak"
    vibhag: [3, 2, 2]  # 7 beats, 3 sections
    matra: 7
    bols: ["tin", "tin", "na", "dha", "dhin", "na", "dha"]

  ektal:
    name: "Ektal"
    vibhag: [4, 4]  # 12 beats
    matra: 12
```

### Tabla Bols Patterns

```yaml
tabla_patterns:
  kayda:
    name: "Kayda (Composition)"
    gat: "dha dhin dhin dha | dha dhin dhin dha | dha tirakita dha | dha dhin dhin dha"
    palta: ["dha dha dhin dhin", "dha dha dhin dhin", ...]

  rela:
    name: "Rela (Fast composition)"
    gat: "dha dhin dha dhin | tirakita dha dhin"
    speed: "fast"

  tihai:
    name: "Tihai (Cadential figure)"
    description: "Pattern repeated 3 times ending on sam"
    example: "dha dhin dhin dha | dha dhin dhin dha | dha dhin dhin dha"
```

## West African Polyrhythms

### Ewe Rhythms (Ghana)

```yaml
ewe_rhythms:
  agbadza:
    name: "Agbadza"
    region: "Ghana/Ewe"
    time_signature: [12, 8]
    patterns:
      bell: "x . x . x x . x . x x . x ."
      rattle: "x x x x x x x x x x x x x x"
      drum_1: "x . x . x . x . x . x . x ."
      drum_2: "x x . . x x . . x x . . x x"

  gahu:
    name: "Gahu"
    region: "Ghana/Ewe"
    patterns:
      bell: "x . x x . x x x . x x x . x x"
      rattle: "x . x . x . x . x . x . x . x"

  sokyee:
    name: "Sokyee"
    region: "Ghana/Ewe"
    patterns:
      bell: "x x . x . x x . . x x . x . x"
```

### Yoruba Rhythms (Nigeria)

```yaml
yoruba_rhythms:
  bata:
    name: "Bata Rumba"
    region: "Cuba/Nigeria"
    ensemble: ["iya", "itotele", "okonkolo"]
    patterns:
      iya: "x x . x . x x . x . x x . x"
      itotele: "x . x . x . x . x . x . x"
      okonkolo: "x . x . x . x . x . x . x"
```

## Polyrhythm Implementation

```python
class PolyrhythmGenerator:
    """Generate polyrhythmic patterns"""

    def cross_rhythm(
        self,
        main_pulse: int,  # e.g., 4
        cross_pulse: int,  # e.g., 3
        length: int = 12  # LCM
    ) -> dict[str, list[int]]:
        """Generate cross-rhythm (e.g., 3 over 4)"""
        # Returns two patterns that can be layered

    def euclidean_polyrhythm(
        self,
        pulses1: int,
        total1: int,
        pulses2: int,
        total2: int
    ) -> dict[str, list[int]]:
        """Generate Euclidean cross-rhythm"""

    def polymetric(
        self,
        patterns: dict[str, tuple[int, int]]
    ) -> dict[str, list[int]]:
        """Generate independent meters for each part"""
        # e.g., {"drums": (4, 4), "bass": (3, 4), "keys": (6, 8)}
```

## Rhythm Composition Utilities

```python
class RhythmComposer:
    """Compose rhythm parts with world percussion"""

    def create_afro_cuban(
        self,
        style: Literal["son", "rumba", "salsa", "cha-cha"]
    ) -> dict[str, DrumPattern]:
        """Create complete Afro-Cuban rhythm section"""

    def create_brazilian(
        self,
        style: Literal["samba", "bossa", "forro"]
    ) -> dict[str, DrumPattern]:
        """Create complete Brazilian rhythm section"""

    def create_indian(
        self,
        tala: str,
        tempo: int
    ) -> dict[str, DrumPattern]:
        """Create Indian tala with tabla bols"""

    def create_west_african(
        self,
        rhythm: str
    ) -> dict[str, DrumPattern]:
        """Create West African polyrhythmic ensemble"""

    def create_middle_eastern:
        """Create Middle Eastern percussion ensemble"""
```

## Files to Create

- `src/musicgen/patterns/world_rhythms.py`
- `resources/world_rhythm_patterns.yaml`

## Success Criteria

- [ ] All clave rhythms defined
- [ ] All major Brazilian patterns defined
- [ ] Indian tala system implemented
- [ ] West African polyrhythms working
- [ ] Polyrhythm generator functional
- [ ] Rhythm composer for all regions
- [ ] Tests for all patterns

## Next Steps

After completion, proceed to Phase 3: World Instruments (V4-14)
