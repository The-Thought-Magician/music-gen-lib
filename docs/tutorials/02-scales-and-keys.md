# Scales and Keys

This tutorial explores the music theory foundation of MusicGen: scales, keys, and their relationships.

## Scale Types

MusicGen supports many scale types:

```python
from musicgen import Scale

# Major scale
major = Scale("C", "major")
print(f"Major: {major.notes}")

# Natural minor
minor = Scale("C", "natural_minor")
print(f"Minor: {minor.notes}")

# Harmonic minor (raised 7th)
harmonic_minor = Scale("C", "harmonic_minor")
print(f"Harmonic minor: {harmonic_minor.notes}")

# Dorian mode
dorian = Scale("D", "dorian")
print(f"D Dorian: {dorian.notes}")

# Major pentatonic
pentatonic = Scale("C", "major_pentatonic")
print(f"Pentatonic: {pentatonic.notes}")
```

## Scale Degrees

Access individual scale degrees:

```python
scale = Scale("C", "major")

# Get scale degrees
tonic = scale.get_degree(1)      # C
supertonic = scale.get_degree(2)  # D
mediant = scale.get_degree(3)     # E
subdominant = scale.get_degree(4) # F
dominant = scale.get_degree(5)    # G
submediant = scale.get_degree(6)  # A
leading_tone = scale.get_degree(7) # B

# Degrees beyond 7 extend to next octave
high_tonic = scale.get_degree(8)  # C5 (octave higher)
```

## Checking Scale Membership

Test if notes belong to a scale:

```python
scale = Scale("C", "major")

# Check individual notes
print(scale.contains("C"))   # True
print(scale.contains("F#"))  # False

# Find scale degree of a note
degree = scale.get_note_index("G")
print(f"G is degree {degree} of C major")  # degree 5
```

## Key Signatures

Working with keys and key signatures:

```python
from musicgen import Key

# Create a key
c_major = Key("C", "major")
print(f"Key: {c_major}")
print(f"Accidentals: {c_major.signature.accidentals}")

# Keys with accidentals
g_major = Key("G", "major")
print(f"G major sharps: {g_major.signature.sharps}")

f_major = Key("F", "major")
print(f"F major flats: {f_major.signature.flats}")
```

## Relative and Parallel Keys

Explore key relationships:

```python
c_major = Key("C", "major")

# Relative minor (same key signature, different tonic)
a_minor = c_major.relative()
print(f"Relative of C major: {a_minor}")

# Parallel minor (same tonic, different key signature)
c_minor = c_major.parallel()
print(f"Parallel of C major: {c_minor}")
```

## Diatonic Chords

Generate chords from a scale:

```python
scale = Scale("C", "major")

# Get all diatonic triads
chords = scale.diatonic_chords()

print("Diatonic chords in C major:")
for i, chord in enumerate(chords):
    print(f"  {i+1}: {chord.root_name} {chord.quality}")
```

## Scale Transposition

Transpose scales to different keys:

```python
# Transpose up a perfect fifth (7 semitones)
c_major = Scale("C", "major")
g_major = c_major.transpose(7)

print(f"Original: {c_major.notes}")
print(f"Transposed: {g_major.notes}")
```

## Putting It Together

Create a simple chord progression using diatonic chords:

```python
from musicgen import Key

key = Key("C", "major")

# I-IV-V-I progression
progression = key.diatonic_chords()
chords = [progression[i-1] for i in [1, 4, 5, 1]]

print("Chord progression:")
for chord in chords:
    print(f"  {chord.root_name} {chord.quality}")
```

## What's Next

In the next tutorial, you'll learn about:
- Melody generation with contours
- Motivic development techniques
- Phrase structure

Continue to [Melody Generation](03-melody-generation.md).
