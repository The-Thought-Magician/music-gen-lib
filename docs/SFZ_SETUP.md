# SFZ Setup Guide

Complete guide to setting up SFZ libraries for professional orchestral sounds with music-gen-lib V3.

## What is SFZ?

SFZ is an open, text-based file format for sampled instruments. Unlike SoundFont (.sf2) which is a binary format, SFZ files are human-readable and can be edited with any text editor.

### Why SFZ Matters for Orchestral Music

| Feature | SoundFont (.sf2) | SFZ | Impact on Quality |
|---------|-----------------|-----|-------------------|
| **Articulations** | One sample per note | Keyswitchable (legato, staccato, pizzicato, tremolo) | Huge |
| **Dynamic Layers** | 1-2 layers | 3-8 velocity layers | High |
| **Round Robins** | Rare | Multiple samples per note for variety | Medium |
| **Expression** | Limited | CC-controlled vibrato, dynamics | High |
| **Crossfading** | Basic | Smooth velocity crossfading | Medium |

### Articulations: The Key Difference

Orchestral playing is defined by how notes are played:

```
Violin section playing "C4" could be:
- legato       (smooth, connected bowing)
- staccato     (short, detached)
- pizzicato    (plucked with finger)
- tremolo      (rapid bow movement)
- sul ponticello (bowing near bridge = metallic)
- spiccato     (bounced bow)
```

Each produces a dramatically different sound. SFZ enables keyswitching between these via MIDI events.

## Installing sfizz

**sfizz** is the recommended open-source SFZ player for local rendering.

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install sfizz
```

Verify installation:
```bash
sfizz-render --version
```

### macOS

```bash
brew install sfizz
```

### Windows

Download from [sfztools.github.io](https://sfztools.github.io/sfizz/)

## Free SFZ Libraries

### Sonatina Symphonic Orchestra (SSO)

**Recommended for getting started**

- **Size:** ~440MB
- **Format:** SFZ (16-bit, 44.1kHz)
- **License:** Creative Commons Sampling Plus 1.0
- **Download:** [GitHub](https://github.com/peastman/sso)

**Instruments:**
- Strings: Violin, Viola, Cello, Double Bass sections
- Woodwinds: Flute, Clarinet, Oboe, Bassoon, Contrabassoon
- Brass: Trumpet, Trombone, Tuba, French Horn
- Percussion: Timpani, Glockenspiel, Marimba, Xylophone, Chimes
- Keyboard: Piano, Harp

**Download with git:**
```bash
mkdir -p ~/sfz_libraries
cd ~/sfz_libraries
git clone https://github.com/peastman/sso.git
```

### Virtual Playing Orchestra

- **Size:** ~1.3GB
- **Format:** SFZ + Kontakt
- **License:** Freeware
- **Download:** [virtualplaying.com](https://virtualplaying.com/virtual-playing-orchestra/)

More detailed than SSO with better dynamic layering.

### Salamander Grand Piano

- **Size:** ~3.5GB (48kHz, 24-bit)
- **Format:** SFZ 2.0
- **Source:** Yamaha C5 grand piano
- **Download:** [GitHub](https://github.com/sfzinstruments/SalamanderGrandPiano)

Features:
- 16 velocity layers
- 3 microphone positions
- Pedal down samples
- Sympathetic resonance

### VSCO Chamber Orchestra

- **Size:** ~500MB
- **Format:** SFZ
- **License:** Freeware
- **Source:** Versilian Studios

Focus on chamber music and smaller ensembles.

## Organizing SFZ Libraries

### Recommended Directory Structure

```
~/sfz_libraries/
|-- sso/
|   |-- Violin/
|   |   |-- 01 Violin.sfz
|   |   |-- samples/
|   |-- Cello/
|   |-- Flute/
|   |-- Piano/
|   |-- Timpani/
|   `-- ...
|-- vpo/
|-- salamander/
`── other/
```

### Configuration

Tell music-gen-lib where to find your libraries:

**Option 1: Environment Variable**
```bash
export SFZ_LIBRARIES_ROOT=~/sfz_libraries
```

**Option 2: Configuration File**

Create `~/.config/musicgen/config.yaml`:
```yaml
sfz_libraries_root: ~/sfz_libraries
default_library: sso
```

**Option 3: In Code**
```python
from pathlib import Path
from musicgen.config import Settings

settings = Settings(
    sfz_libraries_root=Path("~/sfz_libraries"),
    default_library="sso"
)
```

## Using SFZ with music-gen-lib

### Basic Rendering

```python
from pathlib import Path
from musicgen.io.midi_writer import MIDIWriter, Score, Part
from musicgen.renderer.audio import SFZRenderer

# Generate MIDI
score = Score(title="My Piece")
# ... add parts and notes ...
midi_path = Path("output/piece.mid")
MIDIWriter.write(score, str(midi_path))

# Render with SFZ
renderer = SFZRenderer(libraries_root=Path("~/sfz_libraries"))
audio_path = renderer.render(
    midi_path=midi_path,
    output_path=Path("output/piece.wav"),
    sfz_library="sso"
)
```

### With Articulation Switching

```python
from musicgen.ai_models.composition import AIComposition, AIPart, AINote
from musicgen.ai_models.notes import ArticulationType
from musicgen.ai_models.parts import InstrumentRole

# Create part with articulations
part = AIPart(
    name="Violin I",
    midi_program=40,
    midi_channel=0,
    role=InstrumentRole.MELODY,
    notes=[
        AINote(
            note_name="A4",
            duration=1.0,
            start_time=0.0,
            velocity=80,
            articulation=ArticulationType.LEGATO
        ),
        AINote(
            note_name="B4",
            duration=0.5,
            start_time=1.0,
            velocity=80,
            articulation=ArticulationType.STACCATO
        ),
    ]
)
```

## Available Articulations

### Strings

| Articulation | SFZ Region | Description |
|-------------|------------|-------------|
| legato | sustain_long | Smooth, connected |
| detache | sustain_short | Moderately detached |
| staccato | staccato | Short, detached |
| spiccato | spiccato | Bounced bow |
| pizzicato | pizzicato | Plucked |
| tremolo | tremolo | Rapid bow motion |
| sul ponticello | ponticello | Bridge tone (metallic) |
| col legno | col_legno | With wood of bow |

### Woodwinds

| Articulation | Description |
|-------------|-------------|
| legato | Smooth, connected |
| staccato | Short, detached |
| flutter | Flutter tongue (flutes) |

### Brass

| Articulation | Description |
|-------------|-------------|
| legato | Smooth |
| staccato | Short |
| marcato | Accented |
| mute | With mute |

## Troubleshooting

### "sfizz not found"

**Problem:** The sfizz renderer is not installed.

**Solution:** Install sfizz for your platform (see above).

### "SFZ file not found"

**Problem:** music-gen-lib cannot locate the SFZ library.

**Solution:** Check your library path configuration:
```python
from pathlib import Path
import os

# Verify path exists
lib_path = Path("~/sfz_libraries/sso").expanduser()
print(f"Library exists: {lib_path.exists()}")

# Check for specific instrument
sfz_file = lib_path / "Violin/01 Violin.sfz"
print(f"SFZ file exists: {sfz_file.exists()}")
```

### "No sound / very quiet output"

**Problem:** MIDI notes may be outside instrument range or velocity too low.

**Solution:** Check instrument ranges:
```python
# In your composition generation
for note in part.notes:
    midi = note.get_midi_number()
    if midi < 48 or midi > 84:
        print(f"Warning: Note {midi} may be outside typical range")
```

### "Keyswitches not working"

**Problem:** Articulation changes not being applied.

**Solution:** Ensure keyswitches are sent before notes:
```python
# Keyswitch should come before the note
keyswitch_time = note.start_time - 0.1  # 100ms before
```

### "Audio clipping/distortion"

**Problem:** Multiple loud instruments causing distortion.

**Solution:** Adjust dynamics or use normalize during rendering:
```python
renderer = SFZRenderer(
    normalize_output=True,
    headroom_db=-3.0
)
```

## Performance Tips

1. **Use smaller libraries for testing** - SSO is good for quick renders

2. **Render stems separately** - Allows mixing after the fact:
   ```python
   renderer.render_stems(
       midi_path="input.mid",
       output_dir="stems/"
   )
   ```

3. **Batch render** - Render multiple pieces in one session to keep samples in memory

4. **Use lower quality for previews** - Some libraries offer "lite" versions

## Next Steps

- Try the [Quick Start Guide](V3_QUICKSTART.md)
- See [Examples](V3_EXAMPLES.md) for usage patterns
- Read the [API Reference](V3_API.md) for full documentation
