# MusicGen

**MusicGen** is a Python library for AI-powered orchestral music generation. Using Google's Gemini AI, it transforms natural language descriptions into complete musical compositions with proper voice leading, orchestration, and structure.

## What This Project Is Achieving

The goal of MusicGen is to make orchestral music composition accessible through natural language. By describing what you want—"a heroic battle theme," "a peaceful piano melody in G major," or "a jazz trio piece"—you get a complete composition with multiple instrument parts, proper harmony, and realistic musical structure. The library handles the complex music theory behind voice leading, chord progressions, orchestration, and formal structure, while you focus on the creative vision.

## Features

- **AI-Powered Composition**: Uses Google Gemini 2.5 Pro for intelligent music generation
- **Natural Language Interface**: Describe music in plain English—no music theory knowledge required
- **Full Orchestration Support**: Generates realistic multi-instrument arrangements
- **Proper Voice Leading**: Classical counterpoint rules for smooth, musical part writing
- **Multiple Output Formats**: MIDI, WAV, MP3, and JSON export
- **Musical Form Support**: Handles binary, ternary, rondo, and sonata forms
- **Dynamic Expression**: Includes tempo changes, key changes, and dynamic markings
- **Quality Validation**: Ensures generated compositions meet minimum duration and note count requirements

## Installation

```bash
pip install musicgen
```

For development with all dependencies:

```bash
git clone https://github.com/musicgen/music-gen-lib.git
cd music-gen-lib
uv sync
```

### Requirements

- Python 3.10+
- Google API key (set `GOOGLE_API_KEY` environment variable)
- Optional: FluidSynth for audio synthesis

## Quick Start

### Command Line

Generate a composition from a natural language prompt:

```bash
# Set your API key first
export GOOGLE_API_KEY="your-api-key-here"

# Generate music
musicgen compose "A heroic battle theme" --format midi mp3

# Use a preset
musicgen compose --preset epic_orchestral --format midi wav mp3

# List available presets
musicgen presets list
```

### Python API

```python
from musicgen.composer_new import AIComposer

# Initialize composer
composer = AIComposer()

# Generate from natural language
composition = composer.generate(
    "A peaceful piano melody in C major with gentle arpeggios"
)

# Export to files
from musicgen.renderer import Renderer
renderer = Renderer(output_dir="output")
renderer.render(composition, formats=["midi", "mp3"])

# Access composition details
print(f"Title: {composition.title}")
print(f"Key: {composition.key}")
print(f"Tempo: {composition.tempo} BPM")
print(f"Duration: {composition.duration_seconds:.1f}s")
print(f"Instruments: {', '.join(composition.instrument_names)}")
```

## Available Presets

| Preset | Description |
|--------|-------------|
| `classical_piano` | Expressive piano with rich harmonies |
| `jazz_trio` | Piano trio with swing and ii-V-I progressions |
| `epic_orchestral` | Full orchestra with building intensity |
| `ambient_pad` | Evolving synth pads with slow harmonies |
| `folk_acoustic` | Simple acoustic guitar melodies |
| `blues` | 12-bar blues with guitar, bass, drums |
| `minimalist` | Repetitive patterns with gradual changes |
| `romantic_string_quartet` | Expressive string quartet dialogue |

## Output Formats

- **MIDI**: Standard MIDI file (.mid) for use in DAWs and notation software
- **WAV**: Uncompressed audio (requires FluidSynth)
- **MP3**: Compressed audio for easy sharing (requires pydub)
- **JSON**: Full composition data for further processing

## Configuration

Create a `config.toml` or set environment variables:

```bash
# Required
export GOOGLE_API_KEY="your-key"

# Optional
export MUSICGEN_MODEL="gemini-2.5-pro"
export MUSICGEN_TEMPERATURE="0.7"
export MUSICGEN_MAX_TOKENS="8192"
```

## Documentation

- [Getting Started Tutorial](docs/tutorials/01-getting-started.md)
- [API Reference](docs/api/)
- [Project Ideas](docs/idea.md)
- [Research Notes](docs/research.md)

## Development

### Running Tests

```bash
pytest
```

### Type Checking

```bash
mypy src/musicgen
```

### Code Formatting

```bash
ruff check src/musicgen
ruff format src/musicgen
```

## Project Status

MusicGen is currently in active development. The AI composition system is functional, with ongoing work on:

- Enhanced prompt engineering for better results
- More sophisticated musical form templates
- Improved orchestration presets
- MusicXML export for notation software

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Uses [Google Gemini 2.5 Pro](https://ai.google.dev/) for AI-powered music generation
- Built with [Pydantic](https://docs.pydantic.dev/) for type-safe data models
- MIDI export via [mido](https://mido.readthedocs.io/)
- Audio synthesis via [pretty-midi](https://github.com/craffel/pretty-midi)
