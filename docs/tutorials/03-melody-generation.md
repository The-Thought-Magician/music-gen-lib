# Melody Generation

This tutorial covers creating melodies with MusicGen, including contours, motivic development, and phrase structure.

## Basic Melody Creation

Create a melody with a specific contour:

```python
from musicgen import Scale, Key, MelodyGenerator, MelodicContour

scale = Scale("C", "major")
key = Key("C", "major")

generator = MelodyGenerator(scale, key, tempo=120)

# Generate a melody with an arch contour
melody = generator.generate_melody(
    contour=MelodicContour.ARCH,
    motivic_unity=0.8
)

print(f"Generated melody with {melody.length} notes")
print(f"Range: {melody.range} semitones")
```

## Melodic Contours

MusicGen provides several predefined contour types:

```python
from musicgen import MelodicContour

# Available contours
contours = [
    MelodicContour.ASCENDING,      # Overall upward motion
    MelodicContour.DESCENDING,     # Overall downward motion
    MelodicContour.ARCH,           # Rise then fall
    MelodicContour.INVERTED_ARCH,  # Fall then rise
    MelodicContour.WAVE,           # Alternating up and down
    MelodicContour.STATIC,         # Limited pitch range
]
```

## Working with Motifs

A motif is a short melodic idea that can be developed:

```python
from musicgen import Motif, Scale, MelodicContour, QUARTER

# Create a simple motif
scale = Scale("C", "major")
notes = [
    scale.get_degree(1),  # C
    scale.get_degree(3),  # E
    scale.get_degree(5),  # G
    scale.get_degree(8),  # C (high)
]

for note in notes:
    note.duration = QUARTER

motif = Motif(notes=notes, contour=MelodicContour.ASCENDING)

print(f"Motif length: {motif.length}")
print(f"Motif duration: {motif.total_duration} beats")
```

## Motivic Development

Develop your motif using classical techniques:

```python
# Sequence (transposed repetition)
sequence = motif.develop("sequence", interval=5)

# Inversion (mirror intervals)
inverted = motif.develop("inversion")

# Retrograde (reverse order)
reversed_motif = motif.develop("retrograde")

# Augmentation (double durations)
augmented = motif.develop("augmentation")

# Diminution (halve durations)
diminished = motif.develop("diminution")
```

## Phrase Structure

Create musical phrases with proper cadences:

```python
from musicgen import Phrase

# An antecedent phrase (question)
notes_antecedent = [
    Note("C", octave=4, duration=QUARTER),
    Note("D", octave=4, duration=QUARTER),
    Note("E", octave=4, duration=QUARTER),
    Note("F", octave=4, duration=QUARTER),
]
antecedent = Phrase(notes=notes_antecedent, phrase_type="antecedent", cadence="half")

# A consequent phrase (answer)
notes_consequent = [
    Note("G", octave=4, duration=QUARTER),
    Note("F", octave=4, duration=QUARTER),
    Note("E", octave=4, duration=QUARTER),
    Note("C", octave=4, duration=QUARTER),
]
consequent = Phrase(notes=notes_consequent, phrase_type="consequent", cadence="authentic")

# Check if they form a period
if antecedent.is_period_partner(consequent):
    print("Forms a proper period!")
```

## Complete Melody Example

Put it all together:

```python
from musicgen import Scale, Key, MelodyGenerator, MelodicContour
from musicgen.theory.progressions import Progression

# Set up
scale = Scale("D", "minor")
key = Key("D", "minor")
progression = Progression.from_roman("i-iv-VII-i", key="D")

# Generate
generator = MelodyGenerator(scale, key, tempo=100)
generator.set_seed(42)  # For reproducibility

melody = generator.generate_melody(
    progression=progression,
    contour=MelodicContour.WAVE,
    form_structure="period",
    motivic_unity=0.75
)

print(f"Generated melody:")
print(f"  Notes: {melody.length}")
print(f"  Duration: {melody.total_duration} beats")
print(f"  Range: {melody.range} semitones")
```

## What's Next

In the next tutorial, you'll learn about:
- Instrument definitions and ranges
- Ensemble presets
- Orchestration techniques

Continue to [Orchestration](04-orchestration.md).
