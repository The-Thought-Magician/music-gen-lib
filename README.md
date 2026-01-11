# Music Generation Library

A Python library for rule-based orchestral music generation using traditional music theory principles.

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## Features

- **Music Theory Foundation**: Complete implementation of scales, keys, chords, and progressions
- **Melody Generation**: Rule-based melody creation with motivic development
- **Orchestration**: Support for orchestral instruments with realistic ranges
- **Export Formats**: MIDI, WAV, FLAC, MusicXML, and PDF (LilyPond)
- **Mood-Based**: Generate music based on mood presets (epic, peaceful, mysterious, etc.)
- **Voice Leading**: Classical counterpoint rules for smooth part writing
- **Musical Forms**: Binary, ternary, rondo, and sonata form structures

## Installation

```bash
pip install musicgen
```

For development:

```bash
git clone https://github.com/musicgen/music-gen-lib.git
cd music-gen-lib
pip install -e ".[dev]"
```

## Quick Start

```python
from musicgen import generate, CompositionRequest

# Generate music based on mood
request = CompositionRequest(
    mood="peaceful",
    duration=60,
    title="Peaceful Morning"
)

result = generate(request)

print(f"Generated: {result.midi_path}")
```

## Basic Usage

### Creating Notes and Scales

```python
from musicgen import Note, Scale, Chord, MAJOR

# Create notes
note = Note("C4", duration=1.0, velocity=90)
print(f"MIDI: {note.midi_number}, Freq: {note.frequency:.2f}Hz")

# Create scales
scale = Scale("C", "major")
print(f"Notes: {scale.notes}")

# Get scale degrees
tonic = scale.get_degree(1)  # C
dominant = scale.get_degree(5)  # G
```

### Creating Chord Progressions

```python
from musicgen import Progression, Key

key = Key("C", "major")

# From Roman numerals
prog = Progression.from_roman("I-IV-V-I", key="C")
for chord in prog.chords:
    print(f"{chord.root_name} {chord.quality}")
```

### Generating Melodies

```python
from musicgen import MelodyGenerator, MelodicContour

scale = Scale("D", "minor")
key = Key("D", "minor")

generator = MelodyGenerator(scale, key, tempo=120)
melody = generator.generate_melody(
    contour=MelodicContour.ARCH,
    motivic_unity=0.8
)
```

### Exporting Music

```python
from musicgen import MIDIWriter, Score, Part

# Create a score
score = Score()
part = Part(name="violin")
part.notes = melody.notes
score.add_part(part)

# Export to MIDI
MIDIWriter.write(score, "output.mid")
```

## Mood Presets

| Mood | Key | Scale | Tempo | Style |
|------|-----|-------|-------|-------|
| `epic` | D minor | Harmonic minor | 120-140 | Grand, orchestral |
| `peaceful` | G major | Major | 60-80 | Gentle, flowing |
| `mysterious` | D minor | Harmonic minor | 80-100 | Dark, enigmatic |
| `triumphant` | C major | Major | 110-130 | Bold, celebratory |
| `melancholic` | A minor | Natural minor | 60-80 | Sad, reflective |
| `playful` | G major | Major pentatonic | 100-120 | Light, bouncy |
| `romantic` | F major | Major | 70-90 | Warm, expressive |
| `tense` | C minor | Harmonic minor | 90-110 | Dramatic, anxious |

## Command Line Interface

```bash
# Generate music by mood
python -m musicgen generate --mood epic --duration 60

# List available moods
python -m musicgen list-moods

# Specify output directory
python -m musicgen generate --mood peaceful --output-dir ./music
```

## Documentation

- [Getting Started Tutorial](docs/tutorials/01-getting-started.md)
- [API Reference](docs/api/index.md)
- [Examples](examples/)

## Development

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src/musicgen --cov-report=html
```

### Building Documentation

```bash
cd docs/api
make html
```

## Requirements

### Python Packages

- Python 3.10+
- music21 >= 9.0
- mido >= 1.2
- pretty-midi >= 0.2
- numpy >= 1.24

### System Dependencies (Optional)

For audio synthesis:
```bash
# Ubuntu/Debian
sudo apt install fluidsynth

# macOS
brew install fluidsynth
```

For PDF generation:
```bash
# Ubuntu/Debian
sudo apt install lilypond

# macOS
brew install lilypond
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
