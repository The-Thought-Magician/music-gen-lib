# V4-03: MIDI Program Number Mapping

## Overview

Create a comprehensive mapping of all 128 General MIDI (GM) program numbers to instrument names, plus GM2 and GS extensions.

## Objectives

1. Complete GM program number registry (0-127)
2. GM2 extensions
3. Roland GS standard mappings
4. Drum key mapping (standard GM drum map)
5. Lookup utilities for instrument selection

## General MIDI Program Map (0-127)

### Piano Family (0-7)
```python
0:  Acoustic Grand Piano
1:  Bright Acoustic Piano
2:  Electric Grand Piano
3:  Honky-tonk Piano
4:  Electric Piano 1 (Rhodes)
5:  Electric Piano 2 (FM)
6:  Harpsichord
7:  Clavinet
```

### Chromatic Percussion (8-15)
```python
8:  Celesta
9:  Glockenspiel
10: Music Box
11: Vibraphone
12: Marimba
13: Xylophone
14: Tubular Bells
15: Dulcimer
```

### Organ Family (16-23)
```python
16: Drawbar Organ
17: Percussive Organ
18: Rock Organ
19: Church Organ
20: Reed Organ
21: Accordion
22: Harmonica
23: Tango Accordion
```

### Guitar Family (24-31)
```python
24: Acoustic Guitar (nylon)
25: Acoustic Guitar (steel)
26: Electric Guitar (jazz)
27: Electric Guitar (clean)
28: Electric Guitar (muted)
29: Overdriven Guitar
30: Distortion Guitar
31: Guitar Harmonics
```

### Bass Family (32-39)
```python
32: Acoustic Bass
33: Electric Bass (finger)
34: Electric Bass (pick)
35: Fretless Bass
36: Slap Bass 1
37: Slap Bass 2
38: Synth Bass 1
39: Synth Bass 2
```

### Strings Family (40-47)
```python
40: Violin Section
41: Viola Section
42: Cello Section
43: Contrabass Section
44: Tremolo Strings
45: Pizzicato Strings
46: Orchestral Harp
47: Timpani
```

### Ensemble Family (48-55)
```python
48: String Ensemble 1
49: String Ensemble 2
50: Synth Strings 1
51: Synth Strings 2
52: Choir Aahs
53: Voice Oohs
54: Synth Choir
55: Orchestra Hit
```

### Brass Family (56-63)
```python
56: Trumpet
57: Trombone
58: Tuba
59: Muted Trumpet
60: French Horn
61: Brass Section
62: Synth Brass 1
63: Synth Brass 2
```

### Reed Family (64-71)
```python
64: Soprano Sax
65: Alto Sax
66: Tenor Sax
67: Baritone Sax
68: Oboe
69: English Horn
70: Bassoon
71: Clarinet
```

### Pipe Family (72-79)
```python
72: Piccolo
73: Flute
74: Recorder
75: Pan Flute
76: Blown Bottle
77: Shakuhachi
78: Whistle
79: Ocarina
```

### Synth Lead Family (80-87)
```python
80: Lead 1 (square)
81: Lead 2 (sawtooth)
82: Lead 3 (calliope)
83: Lead 4 (chiff)
84: Lead 5 (charang)
85: Lead 6 (voice)
86: Lead 7 (fifths)
87: Lead 8 (bass + lead)
```

### Synth Pad Family (88-95)
```python
88: Pad 1 (new age)
89: Pad 2 (warm)
90: Pad 3 (polysynth)
91: Pad 4 (choir)
92: Pad 5 (bowed)
93: Pad 6 (metallic)
94: Pad 7 (halo)
95: Pad 8 (sweep)
```

### Synth Effects Family (96-103)
```python
96: FX 1 (rain)
97: FX 2 (soundtrack)
98: FX 3 (crystal)
99: FX 4 (atmosphere)
100: FX 5 (brightness)
101: FX 6 (goblins)
102: FX 7 (echoes)
103: FX 8 (sci-fi)
```

### World/ Ethnic Instruments (104-111)
```python
104: Sitar
105: Banjo
106: Shamisen
107: Koto
108: Kalimba
109: Bagpipe
110: Fiddle
111: Shanai
```

### Percussive Family (112-119)
```python
112: Tinkle Bell
113: Agogo
114: Steel Drums
115: Woodblock
116: Taiko Drum
117: Melodic Tom
118: Synth Drum
119: Reverse Cymbal
```

### Sound Effects (120-127)
```python
120: Guitar Fret Noise
121: Breath Noise
122: Seashore
123: Bird Tweet
124: Telephone Ring
125: Helicopter
126: Applause
127: Gunshot
```

## GM Drum Key Map (Channel 10)

```python
# Standard GM Drum Map (key numbers)
{
    35: "acoustic_bass_drum",
    36: "bass_drum_1",
    37: "side_stick",
    38: "acoustic_snare",
    39: "hand_clap",
    40: "electric_snare",
    41: "low_floor_tom",
    42: "closed_hi_hat",
    43: "high_floor_tom",
    44: "pedal_hi_hat",
    45: "low_tom",
    46: "open_hi_hat",
    47: "low_mid_tom",
    48: "hi_mid_tom",
    49: "crash_cymbal_1",
    50: "high_tom",
    51: "ride_cymbal_1",
    52: "chinese_cymbal",
    53: "ride_bell",
    54: "tambourine",
    55: "splash_cymbal",
    56: "cowbell",
    57: "crash_cymbal_2",
    58: "vibraslap",
    59: "ride_cymbal_2",
    60: "hi_bongo",
    61: "low_bongo",
    62: "mute_hi_conga",
    63: "open_hi_conga",
    64: "low_conga",
    65: "high_timbale",
    66: "low_timbale",
    67: "high_agogo",
    68: "low_agogo",
    69: "cabasa",
    70: "maracas",
    71: "short_whistle",
    72: "long_whistle",
    73: "short_guiro",
    74: "long_guiro",
    75: "claves",
    76: "hi_wood_block",
    77: "low_wood_block",
    78: "mute_cuica",
    79: "open_cuica",
    80: "mute_triangle",
    81: "open_triangle",
}
```

## Implementation

```python
# src/musicgen/instruments/midi_map.py

from enum import IntEnum
from typing import Final

class GMProgram(IntEnum):
    """General MIDI Program Numbers (0-127)"""
    ACOUSTIC_GRAND = 0
    BRIGHT_ACOUSTIC = 1
    ELECTRIC_GRAND = 2
    HONKY_TONK = 3
    # ... all 128 programs

class GMKey(IntEnum):
    """GM Drum Key Numbers"""
    ACOUSTIC_BASS_DRUM = 35
    BASS_DRUM_1 = 36
    # ... all drum keys

# Lookup dictionaries
GM_PROGRAM_NAMES: Final[dict[int, str]] = {
    0: "acoustic_grand_piano",
    1: "bright_acoustic_piano",
    # ... complete mapping
}

GM_DRUM_NAMES: Final[dict[int, str]] = {
    35: "kick",
    38: "snare",
    42: "hihat_closed",
    # ... complete mapping
}

# Reverse lookups
PROGRAM_TO_NUMBER: Final[dict[str, int]] = {
    v: k for k, v in GM_PROGRAM_NAMES.items()
}

DRUM_TO_NUMBER: Final[dict[str, int]] = {
    v: k for k, v in GM_DRUM_NAMES.items()
}
```

## Files to Create

- `src/musicgen/instruments/midi_map.py`
- `src/musicgen/instruments/__init__.py`

## Success Criteria

- [ ] All 128 GM programs mapped
- [ ] GM drum map complete (keys 35-81)
- [ ] Reverse lookup dictionaries
- [ ] Helper functions for instrument selection
- [ ] Complete test coverage
- [ ] Type hints and docstrings

## Next Steps

After completion, proceed to Phase 1: Guitar and Bass Instruments (V4-04)
