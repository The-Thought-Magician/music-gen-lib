# Implementation Plan: Music Generation Library

## Overview

This project is a Python library that generates orchestral instrumental music using traditional music theory principles (rule-based composition, not AI). The library will produce both sheet music (MusicXML/LilyPond format) and audio files (WAV/MP3) from programmatic input based on mood/theme parameters.

The library implements:
- Music theory foundations (scales, chords, progressions, voice leading)
- Melody generation with motivic development
- Multi-instrument orchestration
- Musical form structures (binary, ternary, rondo)
- MIDI, audio, and sheet music export capabilities
- **NEW**: AI-powered composition interface using Gemini

---

## Implementation Steps

### Phase 1: Foundation (COMPLETED)

See `docs/steps/completed/` for details on completed steps 1-13.

| Step | Name | Status |
|------|------|--------|
| 1 | Project Setup and Core Data Structures | :white_check_mark: Completed |
| 2 | Music Theory Module - Scales and Keys | :white_check_mark: Completed |
| 3 | Chord Progression Engine | :white_check_mark: Completed |
| 4 | Voice Leading Module | :white_check_mark: Completed |
| 5 | Melody Generation Engine | :white_check_mark: Completed |
| 6 | Orchestration Module | :white_check_mark: Completed |
| 7 | Musical Form Structures | :white_check_mark: Completed |
| 8 | MIDI File Generation | :white_check_mark: Completed |
| 9 | Audio Synthesis Pipeline | :white_check_mark: Partial (needs FluidSynth) |
| 10 | Sheet Music Generation (MusicXML) | :white_check_mark: Completed |
| 11 | Sheet Music Generation (LilyPond) | :white_check_mark: Partial (needs Abjad) |
| 12 | Mood-to-Music Configuration System | :white_check_mark: Completed |
| 13 | Testing and Documentation | :white_check_mark: Completed |

### Phase 2: Audio & AI Integration (IN PROGRESS)

#### Step 14: Audio Export (WAV/MP3)

**Objective**: Implement high-quality audio export functionality to convert generated MIDI compositions to WAV and MP3 formats.

**Status**: :black_square_button: Pending

**Details**: `docs/steps/14-audio-export.md`

**Key Tasks**:
- SoundFont management and download
- FluidSynth-based audio synthesis
- WAV export with normalization
- MP3 encoding via ffmpeg
- Integration with generate() function

---

#### Step 15: AI-Powered Composition Interface

**Objective**: Create an intelligent interface using Google Gemini 2.5 Flash Lite to interpret natural language prompts and generate detailed orchestral composition parameters.

**Status**: :black_square_button: Pending

**Details**: `docs/steps/15-ai-composition-interface.md`

**Key Tasks**:
- Design prompt templates for parameter extraction
- Create Pydantic data models for orchestration plans
- Implement Gemini client with retry logic
- Build composition from AI parameters
- Create `userprompt.txt` interface

**Dependencies**:
- `google-genai` >= 1.0.0

---

#### Step 16: Complete Orchestration Engine

**Objective**: Enhance the composition engine to create true multi-part orchestrations with proper voice leading, counterpoint, and timing for complete 3-minute compositions.

**Status**: :black_square_button: Pending

**Details**: `docs/steps/16-complete-orchestration.md`

**Key Tasks**:
- Multi-part voice leading
- Orchestration strategies (homophonic, polyphonic)
- Thematic development across sections
- Form structure with proper timing
- Dynamics and expression planning

---

#### Step 17: CLI and User Interface Enhancements

**Objective**: Create a comprehensive command-line interface and user-friendly tools for music generation.

**Status**: :black_square_button: Pending

**Details**: `docs/steps/17-cli-enhancements.md`

**Key Tasks**:
- Enhanced CLI with all options
- `musicgen ai <prompt>` command
- Configuration file support
- Prompt file watching interface
- Batch processing mode

---

#### Step 18: Testing and Quality Assurance

**Objective**: Comprehensive testing coverage and quality assurance for the new features.

**Status**: :black_square_button: Pending

**Details**: `docs/steps/18-testing-and-quality.md`

**Key Tasks**:
- Unit tests for audio and AI modules
- Integration tests for full pipeline
- Quality validation (MIDI, audio)
- Performance benchmarks
- >80% code coverage target

---

## Dependencies

### Python Packages

```toml
[project]
name = "musicgen"
version = "0.1.0"
dependencies = [
    "music21>=9.0",
    "mido>=1.2",
    "pretty-midi>=0.2",
    "numpy>=1.24",
]

[project.optional-dependencies]
# Core development tools (Python 3.10+)
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "sphinx>=5.0",
    "sphinx-rtd-theme>=1.0",
    "myst-parser>=1.0",
]

# Audio synthesis (requires system dependencies: fluidsynth)
audio = [
    "pydub>=0.25.0",
]

# LilyPond/PDF export (requires Python <3.12)
lilypond = [
    "abjad>=3.0",
]

# AI-powered composition (Gemini)
ai = [
    "google-genai>=1.0.0",
]

# All optional dependencies (except lilypond for Python 3.12+)
all = [
    "musicgen[dev,audio,ai]",
]
```

### System Dependencies

```bash
# Ubuntu/Debian
sudo apt install fluidsynth ffmpeg

# macOS
brew install fluidsynth ffmpeg

# Windows
# Download from:
# - FluidSynth: https://github.com/FluidSynth/fluidsynth/releases
# - ffmpeg: https://ffmpeg.org/download.html
```

### SoundFont

Download GeneralUser GS SoundFont:
- URL: https://schristiancollins.com/generaluser.php
- File: GeneralUser-GS-v1.471.sf2
- Size: ~30MB
- License: ISC
- Target: `resources/soundfonts/GeneralUser-GS-v1.471.sf2`

---

## Order of Implementation

Phase 2 dependencies:
```
Step 14 (Audio Export)
    -> Step 15 (AI Interface)
        -> Step 16 (Complete Orchestration)
            -> Step 17 (CLI Enhancements)
                -> Step 18 (Testing/QA)
```

---

## Current Status

### Completed
- Core music theory modules (scales, chords, progressions)
- Voice leading and melody generation
- Basic orchestration and forms
- MIDI export (via mido)
- MusicXML export (via music21)
- Mood-based generation
- CLI (basic)
- 96 tests passing

### In Progress
- Audio export (WAV/MP3) via FluidSynth
- AI interface with Gemini

### TODO
- Complete orchestration engine
- Enhanced CLI
- Full testing suite for new features

---

## Codebase Structure

```
music-gen-lib/
├── src/musicgen/
│   ├── core/          # Note, Chord, Rest
│   ├── theory/        # Scales, Keys, Progressions, Voice Leading
│   ├── composition/   # Melody, Forms, Development
│   ├── orchestration/ # Instruments, Ensembles, Strategies
│   ├── io/            # MIDI, Audio, MusicXML, LilyPond
│   ├── config/        # Mood presets
│   ├── ai/            # AI composer (NEW)
│   └── generator.py   # Main generation function
├── tests/
├── examples/
├── docs/
│   ├── steps/         # Implementation steps
│   │   ├── completed/ # Steps 1-13
│   │   ├── 14-audio-export.md
│   │   ├── 15-ai-composition-interface.md
│   │   ├── 16-complete-orchestration.md
│   │   ├── 17-cli-enhancements.md
│   │   └── 18-testing-and-quality.md
│   └── ...
└── resources/
    └── soundfonts/    # SoundFont files (NEW)
```

---

## Usage Examples

### Basic Mood Generation
```bash
musicgen generate --mood peaceful --duration 30 --formats midi,wav,mp3
```

### AI-Powered Generation (Coming Soon)
```bash
# Via prompt file
echo "A heroic battle scene with drums and trumpets" > userprompt.txt
musicgen from-file userprompt.txt

# Via CLI
musicgen ai "A heroic battle scene with drums and trumpets" --duration 180
```

### Python API
```python
from musicgen import generate, CompositionRequest

# Mood-based
request = CompositionRequest(
    mood="epic",
    duration=60,
    export_formats=["midi", "wav", "mp3"]
)
result = generate(request)

# AI-based (Coming Soon)
from musicgen.ai import GeminiComposer
composer = GeminiComposer()
plan = composer.extract_parameters("Cinematic adventure music")
result = generate(CompositionRequest(orchestration_plan=plan))
```
