# Getting Started with MusicGen

Welcome to MusicGen! This tutorial will guide you through generating your first AI-powered orchestral composition using natural language.

## What is MusicGen?

MusicGen is a Python library that uses Google Gemini AI to transform natural language descriptions into complete musical compositions. Instead of writing notes manually, you describe what you want—"a heroic battle theme," "a peaceful piano melody," or "a jazz trio piece"—and MusicGen handles the music theory, orchestration, and structure.

## Prerequisites

1. **Python 3.10 or higher**
2. **A Google API key** (get one at https://ai.google.dev/)

## Installation

```bash
# Install the package
pip install musicgen

# Or for development
git clone https://github.com/musicgen/music-gen-lib.git
cd music-gen-lib
uv sync
```

## Setting Up Your API Key

Set your Google API key as an environment variable:

```bash
# Linux/macOS
export GOOGLE_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:GOOGLE_API_KEY="your-api-key-here"

# Windows (Command Prompt)
set GOOGLE_API_KEY=your-api-key-here
```

Or create a `.env` file in your project directory:

```
GOOGLE_API_KEY=your-api-key-here
```

## Quick Start: Command Line

The fastest way to generate music is using the command line interface.

### Your First Composition

```bash
musicgen compose "A heroic battle theme" --format midi mp3
```

This will:
1. Send your prompt to Google Gemini
2. Generate a complete orchestral composition
3. Export to MIDI and MP3 files

You should see output like:

```
Prompt: A heroic battle theme...
Generating composition...
Generated: The Siege of Crimson Peaks
  Key: C minor
  Tempo: 140 BPM
  Duration: 177.4s
  Instruments: Trumpet, String Section, Cello & Bass, Timpani
Rendering MIDI to the_siege_of_crimson_peaks.mid
Rendering MP3 to the_siege_of_crimson_peaks.mp3
```

### Using Presets

MusicGen includes preset prompts for common styles:

```bash
# List all presets
musicgen presets list

# Use a preset
musicgen compose --preset epic_orchestral --format midi wav mp3

# Combine preset with your own ideas
musicgen compose --preset classical_piano "with a melancholic mood"
```

### Available Formats

- **midi**: Standard MIDI file (works in DAWs, notation software)
- **wav**: Uncompressed audio
- **mp3**: Compressed audio (easy sharing)
- **json**: Full composition data

## Quick Start: Python API

For more control, use the Python API.

### Basic Usage

```python
from musicgen.composer_new import AIComposer
from musicgen.renderer import Renderer

# Initialize the composer
composer = AIComposer()

# Generate from natural language
composition = composer.generate(
    "A peaceful piano melody in C major with gentle arpeggios"
)

# Export to files
renderer = Renderer(output_dir="output")
results = renderer.render(composition, formats=["midi", "mp3"])

# Access composition details
print(f"Title: {composition.title}")
print(f"Key: {composition.key}")
print(f"Tempo: {composition.tempo} BPM")
print(f"Duration: {composition.duration_seconds:.1f}s")
print(f"Instruments: {', '.join(composition.instrument_names)}")
```

### Working with Parts

```python
# Access individual instrument parts
for part in composition.parts:
    print(f"\n{part.name} ({part.role}):")
    print(f"  MIDI program: {part.midi_program}")
    print(f"  Note events: {len(list(part.get_note_events()))}")

    # Access notes
    for note in part.get_note_events():
        if hasattr(note, 'note_name'):
            print(f"  {note.note_name}: {note.duration} quarters @ {note.start_time}")
```

### Customizing Generation

```python
# Set temperature (0.0 = more deterministic, 1.0 = more creative)
composer = AIComposer(temperature=0.7)

# Use a specific model
composer = AIComposer(model="gemini-2.5-pro")
```

## Understanding the Output

### File Types

| File | Description | Use With |
|------|-------------|----------|
| `.mid` | MIDI file | DAWs, notation software, media players |
| `.wav` | Uncompressed audio | Audio editing, professional use |
| `.mp3` | Compressed audio | Sharing, streaming, portable players |
| `.json` | Composition data | Custom processing, analysis |

### Composition Structure

MusicGen generates compositions with:

- **Multiple instrument parts** (melody, harmony, bass, percussion)
- **Proper voice leading** (smooth motion between chords)
- **Musical form** (intro, sections, outro)
- **Dynamic expression** (tempo changes, key changes, dynamics)

## Tips for Better Prompts

1. **Be specific about mood**: "peaceful and relaxing" vs "music"
2. **Specify instruments**: "piano and cello" vs generic "music"
3. **Include tempo suggestions**: "at 120 BPM" or "slow and flowing"
4. **Mention key if desired**: "in D minor" or "major key"
5. **Describe form**: "with a recurring melody" or "through-composed"

### Example Prompts

```
# Style-based
"A jazz piece with walking bass and swing rhythm"
"A classical string quartet with expressive melodies"
"Ambient electronic with slow harmonic changes"

# Mood-based
"Epic and heroic with building intensity"
"Gentle and peaceful for relaxation"
"Dark and mysterious with dissonant harmonies"

# Specific
"Piano solo in C major, moderate tempo, minimal style"
"Full orchestra, D minor, dramatic crescendo"
```

## Checking System Capabilities

Verify your setup:

```bash
musicgen check
```

This shows:
- AI package availability
- API key status
- Rendering capabilities (MIDI, audio formats)

## Next Steps

- [Scales and Keys](02-scales-and-keys.md) - Understanding musical keys and modes
- [Melody Generation](03-melody-generation.md) - How melodies are structured
- [Orchestration](04-orchestration.md) - Working with different instruments
- [Exporting Music](05-exporting-music.md) - Advanced export options

## Troubleshooting

### "API key not set"

Make sure your `GOOGLE_API_KEY` environment variable is set correctly.

### "Package not found"

Install with: `pip install musicgen[ai,audio]`

### "Audio generation failed"

For MP3/WAV export, ensure you have the required dependencies:
```bash
pip install pydub pretty-midi
```

### Empty or short compositions

Try increasing the temperature (more creative freedom) or providing a more detailed prompt.

## Getting Help

- Check the [documentation](../)
- Browse [examples](../../examples/)
- Open an issue on [GitHub](https://github.com/musicgen/music-gen-lib/issues)
