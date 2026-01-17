# V4-12: World Percussion Definitions

## Overview

Define comprehensive world percussion instruments beyond standard drum kits.

## Objectives

1. Define Latin percussion instruments
2. Define African percussion instruments
3. Define Indian percussion instruments
4. Define Middle Eastern percussion instruments
5. Define East Asian percussion instruments

## Latin Percussion

```yaml
# Latin American percussion instruments

# Congas
conga:
  name: "Conga"
  region: "Cuba"
  family: "membranophone"
  pieces:
    quinto:
      name: "Quinto (Highest)"
      size: "11 inch"
      pitch: "high"
      midi_note: 64  # Low Conga (use lower for quinto)
    conga:
      name: "Conga (Mid)"
      size: "11.75 inch"
      pitch: "mid"
      midi_note: 63
    tumbadora:
      name: "Tumbadora (Lowest)"
      size: "12.5 inch"
      pitch: "low"
      midi_note: 62
  techniques:
    open_tone:
      description: "Open palm strike on drum head"
      tone: "resonant"
      duration: 0.5
    slap_tone:
      description: "Fingertips slap on drum head"
      tone: "sharp, cracking"
      duration: 0.15
    bass_tone:
      description: "Palm strike on drum head"
      tone: "deep"
      duration: 0.3
    heel:
      description: "Heel of hand press (mute)"
      tone: "muted"
      duration: 0.1

# Bongos
bongo:
  name: "Bongo"
  region: "Cuba"
  family: "membranophone"
  pieces:
    macho:
      name: "Macho (Small, high)"
      size: "7 inch"
      midi_note: 60  # Hi Bongo
    hembra:
      name: "Hembra (Large, low)"
      size: "8.5 inch"
      midi_note: 61  # Low Bongo
  techniques:
    martillo:
      description: "Standard striking stroke"
      tone: "bright"
    rim_shot:
      description: "Strike on rim"
      tone: "sharp"

# Timbales
timbale:
  name: "Timbale"
  region: "Cuba"
  family: "membranophone"
  pieces:
    high:
      name: "High Timbale"
      size: "13 inch"
      midi_note: 65
    low:
      name: "Low Timbale"
      size: "14 inch"
      midi_note: 66
  techniques:
    cascara:
      description: "Rim pattern played on shell"
      tone: "metallic"
    center:
      description: "Strike on center"
      tone: "bright"

# Cowbell
cowbell:
  name: "Cowbell (Cencerro)"
  region: "Cuba"
  family: "idiophone"
  midi_note: 56
  techniques:
    normal:
      description: "Strike with stick"
    rim:
      description: "Strike on rim"

# Claves
claves:
  name: "Claves"
  region: "Cuba"
  family: "idiophone"
  midi_note: 75
  techniques:
    normal:
      description: "Two wooden sticks struck together"
      duration: 0.05

# Guiro
guiro:
  name: "Guiro"
  region: "Caribbean"
  family: "idiophone"
  pieces:
    long:
      midi_note: 74  # Long Guiro
    short:
      midi_note: 73  # Short Guiro
  techniques:
    long:
      description: "Long scrape"
    short:
      description: "Short scrape"

# Maracas
maracas:
  name: "Maracas"
  region: "Latin America"
  family: "idiophone"
  midi_note: 70
  techniques:
    shake:
      description: "Shaking motion"
    roll:
      description: "Fast shaking"

# Agogo
agogo:
  name: "Agogo Bell"
  region: "Brazil"
  family: "idiophone"
  pieces:
    low:
      midi_note: 67
    high:
      midi_note: 68

# Surdo
surdo:
  name: "Surdo"
  region: "Brazil"
  family: "membranophone"
  pieces:
    alto:
      name: "Alto (Mid)"
      size: "20 inch"
      midi_note: 50
    baixo:
      name: "Baixo (Bass)"
      size: "24 inch"
      midi_note: 36
```

## African Percussion

```yaml
# Djembe
djembe:
  name: "Djembe"
  region: "West Africa"
  family: "membranophone"
  size: "12-14 inch"
  pieces:
    bass:
      name: "Bass tone"
      technique: "center palm"
      midi_note: 35
    tone:
      name: "Open tone"
      technique: "near rim"
      midi_note: 38
    slap:
      name: "Slap tone"
      technique: "rim slap"
      midi_note: 40

# Dunun (Dundun)
dunun:
  name: "Dunun"
  region: "West Africa"
  family: "membranophone"
  pieces:
    dununba:
      name: "Dununba (Largest)"
      size: "26 inch"
      midi_note: 35
    sangban:
      name: "Sangban (Middle)"
      size: "22 inch"
      midi_note: 38
    kenkeni:
      name: "Kenkeni (Smallest)"
      size: "18 inch"
      midi_note: 42

# Talking Drum
talking_drum:
  name: "Talking Drum (Tama)"
  region: "West Africa"
  family: "membranophone"
  midi_note: 43
  techniques:
    squeeze:
      description: "Squeeze ropes to change pitch"
      pitch_bend: true

# Shekere
shekere:
  name: "Shekere"
  region: "West Africa"
  family: "idiophone"
  midi_note: 70
  description: "Gourd with beaded net"

# Balafon
balafon:
  name: "Balafon"
  region: "West Africa"
  family: "idiophone"
  type: "marimba"
  range: {min: 48, max: 72}
  tuning: "pentatonic"

# Udu
udu:
  name: "Udu"
  region: "Nigeria"
  family: "membranophone"
  midi_note: 44
  description: "Clay pot drum"
```

## Indian Percussion

```yaml
# Tabla
tabla:
  name: "Tabla"
  region: "India"
  family: "membranophone"
  pieces:
    bayan:
      name: "Bayan (Left, bass drum)"
      size: "larger"
      midi_note: 36
      techniques:
        gaya:
          description: "Resonant bass stroke"
        ke:
          description: "Flat stroke"
    dayan:
      name: "Dayan (Right, treble drum)"
      size: "smaller"
      midi_note: 38
      techniques:
        na:
          description: "Index finger stroke"
        tin:
          description: "Ring finger stroke"
        tun:
          description: "Middle finger stroke"
        ge:
          description: "Stroke with damping"

    bols:
      dha: {description: "Both drums, resonant"}
    dhin: {description: "Both drums, resonant, heavier"}
    na: {description: "Right hand, rim"}
    tin: {description: "Right hand, smaller tone"}
    te: {description: "Right hand, closed"}
    ke: {description: "Left hand, flat"}

# Mridangam
mridangam:
  name: "Mridangam"
  region: "South India"
  family: "membranophone"
  pieces:
    thoppi:
      name: "Thoppi (Left, bass)"
      midi_note: 36
    valantalai:
      name: "Valantalai (Right, treble)"
      midi_note: 38

# Kanjira
kanjira:
  name: "Kanjira"
  region: "South India"
  family: "membranophone"
  midi_note: 70
  description: "Frame drum with jingles"

# Ghatam
ghatam:
  name: "Ghatam"
  region: "South India"
  family: "membranophone"
  midi_note: 36
  description: "Clay pot"
```

## Middle Eastern Percussion

```yaml
# Darbuka (Doumbek)
darbuka:
  name: "Darbuka (Doumbek)"
  region: "Middle East"
  family: "membranophone"
  midi_note: 40
  techniques:
    doum:
      description: "Center stroke (bass)"
      duration: 0.3
    tek:
      description: "Rim stroke (high)"
      duration: 0.1
    ka:
      description: "Rim stroke (slap)"
      duration: 0.08

# Riq
riq:
  name: "Riq"
  region: "Middle East"
  family: "idiophone"
  midi_note: 70
  description: "Tambourine with fish skin jingles"

# Daf
daf:
  name: "Daf"
  region: "Middle East"
  family: "membranophone"
  midi_note: 40
  description: "Large frame drum"
  techniques:
    snap:
      description: "Finger snap on frame"
    shake:
      description: "Shake for ring sound"

# Tabl
tabl:
  name: "Tabl"
  region: "Egypt"
  family: "membranophone"
  midi_note: 36
  description: "Large copper drum"
```

## East Asian Percussion

```yaml
# Taiko
taiko:
  name: "Taiko"
  region: "Japan"
  family: "membranophone"
  pieces:
    o_daiko:
      name: "O-daiko (Large)"
      size: "6+ feet"
      midi_note: 36
    nagado:
      name: "Nagado-daiko (Medium)"
      size: "3 feet"
      midi_note: 38
    shime:
      name: "Shime-daiko (Small)"
      size: "1.5 feet"
      midi_note: 42
  techniques:
    bachi:
      description: "Oak stick strike"
    hane:
      description: "Rim strike"

# Korean Drums
janggu:
  name: "Janggu"
  region: "Korea"
  family: "membranophone"
  pieces:
    gwaenghyeong:
      name: "Left head (low)"
      midi_note: 36
    chaeyin:
      name: "Right head (high)"
      midi_note: 38

# Chinese Percussion
bo:
  name: "Bo"
  region: "China"
  family: "idiophone"
  midi_note: 56
  description: "Small cymbal pairs"

# Chinese Tom
tanggu:
  name: "Tanggu"
  region: "China"
  family: "membranophone"
  midi_note: 44
```

## Files to Create

- `resources/instrument_definitions_world.yaml` (world percussion)
- `src/musicgen/instruments/world_percussion.py`

## Success Criteria

- [ ] All Latin percussion defined
- [ ] All African percussion defined
- [ ] All Indian percussion defined
- [ ] All Middle Eastern percussion defined
- [ ] All East Asian percussion defined
- [ ] Techniques documented
- [ ] MIDI mappings assigned
- [ ] Tests for world percussion

## Next Steps

After completion, proceed to V4-13: Percussion Pattern Generation
