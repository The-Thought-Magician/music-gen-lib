# Orchestration

This tutorial covers working with instruments and ensembles in MusicGen.

## Instrument Definitions

MusicGen includes definitions for orchestral instruments:

```python
from musicgen import Instrument, Note

# Create an instrument
violin = Instrument.preset("violin")

print(f"Violin range: {violin.range}")
print(f"MIDI program: {violin.midi_program}")

# Check if a note is in range
note = Note("A4", QUARTER)
print(f"Is A4 in violin range? {violin.in_range(note)}")
```

## Available Instruments

Common orchestral instruments:

```python
# Strings
violin = Instrument.preset("violin")
viola = Instrument.preset("viola")
cello = Instrument.preset("cello")
bass = Instrument.preset("double_bass")

# Woodwinds
flute = Instrument.preset("flute")
oboe = Instrument.preset("oboe")
clarinet = Instrument.preset("clarinet")
bassoon = Instrument.preset("bassoon")

# Brass
trumpet = Instrument.preset("trumpet")
horn = Instrument.preset("french_horn")
trombone = Instrument.preset("trombone")
tuba = Instrument.preset("tuba")
```

## Transposing Instruments

Handle instruments that transpose:

```python
# Clarinet in Bb (sounds a major second lower than written)
clarinet = Instrument.preset("clarinet")

written_note = Note("C4", QUARTER)
sounding_note = clarinet.written_to_concert(written_note)

print(f"Written: {written_note}")
print(f"Sounding: {sounding_note}")  # Bb3
```

## Ensemble Presets

Use pre-defined ensemble configurations:

```python
from musicgen import Ensemble

# String quartet
string_quartet = Ensemble.preset("string_quartet")
print("String quartet instruments:")
for inst in string_quartet.instruments:
    print(f"  - {inst.name}")

# Full orchestra
orchestra = Ensemble.preset("orchestra")
print(f"\nOrchestra has {len(orchestra.instruments)} instruments")
```

## Custom Ensembles

Create your own ensemble:

```python
from musicgen import Ensemble, Instrument

# Chamber ensemble
instruments = [
    Instrument.preset("violin"),
    Instrument.preset("viola"),
    Instrument.preset("cello"),
    Instrument.preset("piano"),
]

ensemble = Ensemble(name="chamber_group", instruments=instruments)
```

## Texture Types

Specify musical texture:

```python
from musicgen import Texture

# Homophonic - melody with accompaniment
texture = Texture.homophonic(
    melody_instruments=["violin", "flute"],
    harmony_instruments=["viola", "cello"],
    bass_instruments=["double_bass"]
)

# Polyphonic - independent voices
texture = Texture.polyphonic(
    instruments=["violin", "viola", "cello"]
)
```

## What's Next

In the final tutorial, you'll learn about:
- Exporting to MIDI
- Generating audio
- Creating sheet music

Continue to [Exporting Music](05-exporting-music.md).
