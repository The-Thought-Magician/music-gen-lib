# V3 Quick Start Guide

Get started with music-gen-lib V3 for AI-powered orchestral music generation with SFZ support.

## Installation

### 1. Install the Package

```bash
# Install with pip
pip install music-gen-lib

# Or install with uv
uv pip install music-gen-lib

# Or clone and install in development mode
git clone https://github.com/musicgen/music-gen-lib.git
cd music-gen-lib
uv pip install -e .
```

### 2. Install System Dependencies

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install sfizz ffmpeg
```

**macOS:**
```bash
brew install sfizz ffmpeg
```

**Windows:**
Download sfizz from [sfztools.github.io](https://sfztools.github.io/sfizz/)

### 3. Download SFZ Libraries

For professional orchestral sounds, download free SFZ libraries:

```bash
# Create libraries directory
mkdir -p ~/sfz_libraries
cd ~/sfz_libraries

# Download Sonatina Symphonic Orchestra (recommended)
git clone https://github.com/peastman/sso.git

# Or download manually from:
# https://sfzinstruments.github.io/orchestra/sso/
```

## Basic Usage

### Python API

The simplest way to generate music:

```python
from musicgen import generate, CompositionRequest

# Generate a composition
result = generate(CompositionRequest(
    mood="peaceful",
    duration=30,
    export_formats=["midi", "audio"]
))

print(f"Generated: {result.title}")
print(f"MIDI: {result.midi_path}")
print(f"Audio: {result.audio_path}")
```

### Using the V3 AI Composer

For AI-powered composition with natural language prompts:

```python
from pathlib import Path
from musicgen.ai import GeminiComposer

# Initialize composer
composer = GeminiComposer(
    sfz_libraries_root=Path("~/sfz_libraries")
)

# Generate from a prompt
composition = composer.generate(
    prompt="A melancholic string quartet in D minor",
    duration_seconds=120,
    key="D minor",
    style="romantic",
    ensemble="string_quartet"
)

print(f"Title: {composition.title}")
print(f"Duration: {composition.duration_seconds}s")
```

### Command Line Interface

Generate music directly from the terminal:

```bash
# Basic generation
musicgen compose "A peaceful melody" --duration 30

# With specific parameters
musicgen compose "An epic orchestral piece" \
    --style film_score \
    --ensemble full_orchestra \
    --key D minor \
    --duration 90 \
    --output epic.wav

# Generate with specific form
musicgen compose "A piano sonata movement" \
    --style classical \
    --form sonata \
    --key C minor \
    --duration 180
```

## A Complete Example

Here's a complete script that generates and renders a composition:

```python
#!/usr/bin/env python3
"""Generate a classical string quartet."""

from pathlib import Path
from musicgen.ai_models import AIComposition, AIPart, AINote
from musicgen.io.midi_writer import MIDIWriter, Part, Score
from musicgen.theory.keys import Key
from musicgen.theory.scales import Scale
from musicgen.composition.melody import MelodyGenerator, MelodicContour
from musicgen.theory.progressions import Progression

# Set up musical elements
key = Key("D", "minor")
scale = Scale("D", "minor")
progression = Progression.from_roman("i-iv-VII-i", key="D")

# Generate melody
melody_gen = MelodyGenerator(scale, key, tempo=100)
melody = melody_gen.generate_melody(
    progression=progression,
    contour=MelodicContour.WAVE,
    motivic_unity=0.7
)

# Create score
score = Score(
    title="String Quartet in D minor",
    composer="MusicGen AI"
)

# Create parts
violin1 = Part(name="Violin I")
violin1.notes = melody.notes

violin2 = Part(name="Violin II")
violin2.notes = melody.notes  # Simplified for demo

viola = Part(name="Viola")
# Add harmony notes
for chord in progression.chords:
    viola.add_note(chord.notes[1])  # Third

cello = Part(name="Cello")
# Add bass line
for chord in progression.chords:
    cello.add_note(chord.notes[0])  # Root

# Add parts to score
for part in [violin1, violin2, viola, cello]:
    score.add_part(part)

# Export to MIDI
output_path = Path("output/quartet.mid")
output_path.parent.mkdir(parents=True, exist_ok=True)
MIDIWriter.write(score, str(output_path), tempo=100)

print(f"Generated: {output_path}")
```

## Configuration

### Set API Key

For AI-powered generation, set your Gemini API key:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or in Python:

```python
import os
os.environ["GEMINI_API_KEY"] = "your-api-key-here"
```

### Configure SFZ Libraries

Tell music-gen-lib where to find SFZ libraries:

```python
from pathlib import Path
from musicgen.config import Settings

settings = Settings(
    sfz_libraries_root=Path("~/sfz_libraries"),
    default_library="sso"
)
```

## Available Options

### Mood Presets

```python
from musicgen import list_available_moods

print(list_available_moods())
# Output: ['peaceful', 'melancholic', 'epic', 'playful', ...]
```

### Musical Styles

- `baroque` - 160-1750, ornate, contrapuntal
- `classical` - 1750-1820, balanced, elegant
- `romantic` - 1820-1900, expressive, emotional
- `modern` - 20th century, experimental
- `film_score` - Cinematic, dramatic

### Musical Forms

- `binary` - AB structure
- `ternary` - ABA structure
- `rondo` - ABACA... refrain alternating
- `sonata` - Exposition-development-recapitulation
- `through_composed` - Continuous, no repetition

### Ensemble Presets

- `string_quartet` - 2 violins, viola, cello
- `woodwind_quintet` - Flute, oboe, clarinet, bassoon, horn
- `full_orchestra` - Complete orchestra
- `chamber_orchestra` - Smaller orchestra
- `piano_solo` - Single piano

## Next Steps

- Read the [API Reference](V3_API.md) for detailed documentation
- See [Examples](V3_EXAMPLES.md) for more usage patterns
- Check [SFZ Setup](SFZ_SETUP.md) for library configuration

## Troubleshooting

**"sfizz not found"**
- Install sfizz: `sudo apt install sfizz` (Linux) or `brew install sfizz` (macOS)

**"No SFZ libraries found"**
- Download and extract an SFZ library (e.g., Sonatina Symphonic Orchestra)
- Set the `sfz_libraries_root` configuration

**"GEMINI_API_KEY not set"**
- Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Set it: `export GEMINI_API_KEY=your-key`

**Generated MIDI sounds like basic beeps**
- That's expected without SFZ libraries. Follow the SFZ Setup guide for professional sounds.
