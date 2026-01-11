# Getting Started with MusicGen

Welcome to the Music Generation Library! This tutorial will guide you through the basics of creating music programmatically using traditional music theory.

## Installation

Install MusicGen using pip:

```bash
pip install musicgen
```

For development, install with optional dependencies:

```bash
pip install musicgen[dev]
```

## Your First Note

Let's start by creating a simple musical note:

```python
from musicgen import Note, QUARTER

# Create a C quarter note
note = Note("C4", QUARTER)

print(f"Note: {note.name}{note.octave}")
print(f"MIDI number: {note.midi_number}")
print(f"Frequency: {note.frequency:.2f} Hz")
```

Output:
```
Note: C4
MIDI number: 60
Frequency: 261.63 Hz
```

## Creating a Scale

Now let's create a musical scale and explore its properties:

```python
from musicgen import Scale

# Create C major scale
c_major = Scale("C", "major")

print("Notes in C major:")
for note_name in c_major.notes:
    print(f"  {note_name}")

# Access scale degrees
tonic = c_major.get_degree(1)  # C
dominant = c_major.get_degree(5)  # G

print(f"\nTonic: {tonic}")
print(f"Dominant: {dominant}")
```

## Building a Chord

Create chords using the scale:

```python
from musicgen import Chord, MAJOR

# C major triad
c_chord = Chord(_root_name="C", _quality=MAJOR)

print("C major chord notes:")
for note in c_chord.notes:
    print(f"  {note}")
```

## Generating a Simple Melody

Create a simple ascending melody:

```python
from musicgen import Note, QUARTER, Scale

# Create a scale
scale = Scale("C", "major")

# Create an ascending scale melody
notes = [scale.get_degree(i + 1) for i in range(8)]

# Assign duration to each note
for note in notes:
    note.duration = QUARTER

print("Simple ascending melody:")
for note in notes:
    print(f"  {note.name}{note.octave}")
```

## Exporting to MIDI

Export your melody to a MIDI file:

```python
from musicgen import MIDIWriter, Score, Part

# Create a score
score = Score()

# Add a melody part
part = Part(name="melody")
part.notes = notes
score.add_part(part)

# Write to MIDI
MIDIWriter.write(score, "my_first_melody.mid")

print("MIDI file created: my_first_melody.mid")
```

## What's Next

In the next tutorial, you'll learn about:
- Different scale types (minor, modes, pentatonic)
- Key signatures and their relationships
- Diatonic chords in a key

Continue to [Scales and Keys](02-scales-and-keys.md).
