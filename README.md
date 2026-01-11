# Music Generation Library

> A Python library for generating orchestral instrumental music using traditional music theory (not AI).

**Status**: 🚧 In Development - Phase 1: Project Setup

---

## Overview

This library creates original orchestral music programmatically using classical music theory principles:
- Scales, chords, and progressions
- Voice leading and counterpoint
- Melodic development and motivic variation
- Orchestration for ensembles from solo to full orchestra
- Export to MIDI, audio (WAV/FLAC), and sheet music (MusicXML/PDF)

**This is NOT an AI/ML project** - all composition is rule-based.

---

## Features (Planned)

- 🎵 **Music Theory**: Complete implementation of scales, modes, chords, progressions
- 🎼 **Composition**: Melody, harmony, voice leading, musical forms
- 🎻 **Orchestration**: Full orchestral instrument library with range/capability data
- 🎹 **MIDI Export**: Standard MIDI file output
- 🔊 **Audio Synthesis**: High-quality audio using FluidSynth + SoundFonts
- 📄 **Sheet Music**: MusicXML and LilyPond/PDF export
- 🎭 **Mood-based**: Generate music by mood (epic, peaceful, mysterious, etc.)

---

## Installation (Not Yet Available)

```bash
# Will be available once Step 1 is complete
pip install musicgen-lib
```

### System Dependencies

```bash
# Ubuntu/Debian
sudo apt install fluidsynth lilypond

# macOS
brew install fluidsynth lilypond
```

---

## Quick Start (Planned Usage)

```python
from musicgen import generate, CompositionRequest

# Generate music by mood
request = CompositionRequest(
    mood="epic",
    duration=60  # seconds
)

result = generate(request)

# Outputs created:
# - result.midi_path      # MIDI file
# - result.audio_path     # WAV audio file
# - result.sheet_path     # PDF sheet music
```

---

## Project Structure

```
music-gen-lib/
├── src/musicgen/          # Main package
│   ├── core/              # Note, Chord, Rest
│   ├── theory/            # Scales, keys, progressions, voice leading
│   ├── composition/       # Melody, forms
│   ├── orchestration/     # Instruments, ensembles
│   ├── io/                # MIDI, audio, sheet music writers
│   └── config/            # Mood configurations
├── tests/                 # Test suite
├── docs/                  # Documentation
└── examples/              # Usage examples
```

---

## Development Status

| Step | Description | Status |
|------|-------------|--------|
| 1 | Project Setup + Core Data Structures | 🔲 Pending |
| 2 | Scales and Keys | 🔲 Pending |
| 3 | Chord Progressions | 🔲 Pending |
| 4 | Voice Leading | 🔲 Pending |
| 5 | Melody Generation | 🔲 Pending |
| 6 | Orchestration | 🔲 Pending |
| 7 | Musical Forms | 🔲 Pending |
| 8 | MIDI Export | 🔲 Pending |
| 9 | Audio Synthesis | 🔲 Pending |
| 10 | MusicXML Export | 🔲 Pending |
| 11 | LilyPond Export | 🔲 Pending |
| 12 | Mood Interface | 🔲 Pending |
| 13 | Testing & Documentation | 🔲 Pending |

---

## Documentation

- [Idea Document](docs/idea.md) - Original project concept
- [Research](docs/research.md) - Technical research and stack decisions
- [Implementation Plan](docs/plan.md) - Step-by-step implementation plan

---

## Contributing

This project follows the master workflow defined in [master-docs/master-idea.md](../master-docs/master-idea.md).

---

## License

TBD
