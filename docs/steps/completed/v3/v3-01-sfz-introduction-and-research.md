# V3-01: SFZ Introduction and Research

**Status:** Pending
**Priority:** Foundation
**Dependencies:** None

## Overview

This step establishes the foundation for world-class orchestral music generation by migrating from basic SoundFont (.sf2) synthesis to SFZ format with proper sample libraries.

## What is SFZ?

SFZ is an open, text-based file format for sampled instruments. Unlike SoundFont (.sf2) which is a binary format, SFZ files are human-readable and can be edited with any text editor.

### Why SFZ Matters for World-Class Orchestral Music

| Feature | SoundFont (.sf2) | SFZ | Impact on Quality |
|---------|-----------------|-----|-------------------|
| **Articulations** | One sample per note | Keyswitchable (legato, staccato, pizzicato, tremolo) | **Huge** |
| **Dynamic Layers** | 1-2 layers | 3-8 velocity layers | **High** |
| **Round Robins** | Rare | Multiple samples per note for variety | **Medium** |
| **Expression** | Limited | CC-controlled vibrato, dynamics | **High** |
| **Crossfading** | Basic | Smooth velocity crossfading | **Medium** |

### The Key Differentiator: Articulations

Orchestral playing is defined by how notes are played, not just what notes are played:

```
Violin section playing "C4" could be:
├── legato       (smooth, connected bowing)
├── staccato     (short, detached)
├── pizzicato    (plucked with finger)
├── tremolo      (rapid bow movement)
├── sul ponticello (bowing near bridge = metallic)
├── col legno    (with the wood of the bow)
└── spiccato     (bounced bow)
```

Each of these produces a dramatically different sound. SFZ enables keyswitching between these articulations via MIDI events.

## Free SFZ Libraries for Local Use

### 1. Sonatina Symphonic Orchestra (SSO)

**Size:** ~440MB
**Format:** SFZ (16-bit, 44.1kHz)
**License:** Creative Commons Sampling Plus 1.0
**Download:** [GitHub](https://github.com/peastman/sso) | [SFZ Instruments](https://sfzinstruments.github.io/orchestra/sso/)

**Instruments:**
- Strings: Violin section, Viola section, Cello section, Double bass section
- Woodwinds: Flute, Clarinet, Oboe, Bassoon, Contrabassoon
- Brass: Trumpet, Trombone, Tuba, French Horn
- Percussion: Timpani, Glockenspiel, Marimba, Xylophone, Chimes
- Keyboard: Piano, Harp

**Articulations per instrument:** 2-5 (varies by instrument)

### 2. Virtual Playing Orchestra

**Size:** ~1.3GB
**Format:** SFZ + Kontakt
**License:** Freeware
**Download:** [virtualplaying.com](https://virtualplaying.com/virtual-playing-orchestra/)

**Instruments:**
- Complete orchestral sections with solo instruments
- More detailed than SSO
- Better dynamic layering

### 3. Salamander Grand Piano

**Size:** ~3.5GB (48kHz, 24-bit)
**Format:** SFZ 2.0 + ARIA extensions
**Source:** Yamaha C5 grand piano
**Download:** [GitHub](https://github.com/sfzinstruments/SalamanderGrandPiano)

**Features:**
- 16 velocity layers
- 3 microphone positions
- Pedal down samples
- Sympathetic resonance

### 4. VSCO Chamber Orchestra

**Size:** ~500MB
**Format:** SFZ
**License:** Freeware
**Source:** Versilian Studios

**Focus:** Chamber music, smaller ensembles

## SFZ Player: sfizz

**sfizz** is the recommended open-source SFZ player for local rendering.

### Why sfizz?

| Feature | sfizz | sforzando (paid) |
|---------|-------|------------------|
| Open Source | ✓ | ✗ |
| Command-line render | ✓ | ✗ |
| Python integration | ✓ (via subprocess) | ✗ |
| SFZ v2 support | ✓ | ✓ |
| Cross-platform | ✓ | ✓ |

### Installation

```bash
# Linux
sudo apt install sfizz

# macOS
brew install sfizz

# Windows
# Download from https://sfztools.github.io/sfizz/
```

### Command Line Rendering

```bash
sfizz-render input.mid output.wav --soundfont=/path/to/library.sfz
```

## SFZ Format Basics

### File Structure

```sfz
// Violin Section - Legato
<region>
sample=violin/legato/C4.wav
lokey=48 hikey=60 pitch_keycenter=60
lovel=0 hivel=64

<region>
sample=violin/legato/C4_ff.wav
lokey=48 hikey=60 pitch_keycenter=60
lovel=65 hivel=127

// Keyswitch for staccato
<region>
sample=violin/staccato/C4.wav
sw_last=24
lokey=48 hikey=60 pitch_keycenter=60
```

### Key Opcodes

| Opcode | Purpose | Example |
|--------|---------|---------|
| `sample` | Path to audio file | `sample=C4.wav` |
| `lokey/hikey` | Note range | `lokey=48 hikey=60` |
| `pitch_keycenter` | Original pitch | `pitch_keycenter=60` |
| `lovel/hivel` | Velocity range | `lovel=0 hivel=64` |
| `sw_last` | Keyswitch last | `sw_last=24` |
| `sw_default` | Default keyswitch | `sw_default=24` |

## Implementation Tasks

1. [ ] Install sfizz locally
2. [ ] Download and organize at least one free SFZ library
3. [ ] Test basic rendering with sfizz-render
4. [ ] Document library structure and available articulations
5. [ ] Create YAML configuration for instrument definitions

## Success Criteria

- sfizz-render successfully converts MIDI to WAV
- At least one orchestral SFZ library is integrated
- Basic articulation switching works

## Next Steps

After this step:
- V3-02: SFZ Instrument Definition Layer
- V3-03: SFZ Renderer Integration
- V3-04: Articulation System Design

## References

- [SFZ Format Official Documentation](https://sfzformat.com/)
- [sfizz GitHub](https://github.com/sfztools/sfizz)
- [sfztools.github.io](https://sfztools.github.io/sfizz/)
- [Sonatina Symphonic Orchestra](https://github.com/peastman/sso)
- [Salamander Grand Piano](https://github.com/sfzinstruments/SalamanderGrandPiano)
- [Virtual Playing Orchestra](https://virtualplaying.com/virtual-playing-orchestra/)
