# Exporting Music

This tutorial covers all the ways to export your musical creations from MusicGen.

## MIDI Export

The simplest export format - MIDI files can be played by any DAW or media player.

```python
from musicgen import MIDIWriter, Score, Part, Scale, QUARTER

# Create a simple melody
scale = Scale("C", "major")
notes = [scale.get_degree(i % 7 + 1) for i in range(16)]

for note in notes:
    note.duration = QUARTER

# Create a score
score = Score()
part = Part(name="melody")
part.notes = notes
score.add_part(part)

# Export to MIDI
MIDIWriter.write(score, "output.mid")

print("MIDI file created: output.mid")
```

## Audio Export

Generate actual audio files using a SoundFont:

```python
from musicgen.io.audio_synthesizer import AudioSynthesizer

# Initialize synthesizer with SoundFont
synth = AudioSynthesizer()

# Check if FluidSynth is available
if AudioSynthesizer.is_available():
    audio_path = synth.render("output.mid", output_format="wav")
    print(f"Audio file created: {audio_path}")
else:
    print("FluidSynth not available - install it for audio export")
```

## MusicXML Export

Export to MusicXML for use in notation software like MuseScore, Sibelius, or Finale:

```python
from musicgen import MusicXMLWriter

# Export to MusicXML
MusicXMLWriter.write(score, "output.musicxml")

print("MusicXML file created: output.musicxml")
```

## LilyPond Export

Generate publication-quality sheet music with LilyPond:

```python
from musicgen import LilyPondWriter

writer = LilyPondWriter()

# Check if LilyPond is available
if LilyPondWriter.is_available():
    pdf_path = writer.write(
        score=score,
        output_pdf="output.pdf",
        output_ly="output.ly",
        title="My Composition",
        composer="Your Name"
    )
    print(f"PDF created: {pdf_path}")
else:
    print("LilyPond not available - install it for PDF export")
```

## Mood-Based Complete Generation

Generate complete compositions with all export formats:

```python
from musicgen import generate, CompositionRequest

# Create a composition request
request = CompositionRequest(
    mood="peaceful",
    duration=30,
    title="Peaceful Morning",
    composer="Your Name",
    output_dir="./output",
    export_formats=["midi", "musicxml"]
)

# Generate everything
result = generate(request)

print(f"Generated: {result.title}")
print(f"  MIDI: {result.midi_path}")
print(f"  MusicXML: {result.musicxml_path}")
```

## CLI Usage

You can also generate music from the command line:

```bash
# Generate with default settings
python -m musicgen generate --mood peaceful --duration 30

# Specify output directory
python -m musicgen generate --mood epic --duration 60 --output-dir ./music

# List available moods
python -m musicgen list-moods
```

## Next Steps

You've completed the MusicGen tutorials! You can now:
- Explore the [API Reference](../api/index.md) for detailed documentation
- Check out the [Examples](../examples/) for more code samples
- Read the [Contributing Guide](../contributing.md) to help improve MusicGen

Happy composing!
