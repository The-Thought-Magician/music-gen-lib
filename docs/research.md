# Research: Music Generation Library

## Overview

> **Note**: This research was originally conducted for a rule-based composition system. MusicGen has since evolved to use Google Gemini AI for music generation, while still applying the music theory principles documented here.

This document presents comprehensive research on orchestral music generation, covering music theory principles that inform both the AI prompting strategy and the validation rules for generated compositions.

---

## Recommended Technology Stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| Language | Python | Excellent ecosystem for music processing, easy to read/write, extensive library support |
| Music Theory | music21 + mingus | music21 provides comprehensive musicology tools; mingus offers intuitive scale/chord/progression APIs |
| MIDI File I/O | mido + pretty_midi | mido for low-level MIDI manipulation; pretty_midi for high-level analysis and conversion |
| Audio Synthesis | FluidSynth + pyfluidsynth | Realistic instrument playback via SoundFonts; widely supported, cross-platform |
| SoundFont | GeneralUser GS | Free, GM/GS-compatible, 259 instrument presets including orchestral sounds |
| Sheet Music (Notation) | Abjad + LilyPond | Abjad provides Pythonic API; LilyPond produces publication-quality scores |
| MusicXML | music21 / partitura | For interchange with commercial notation software (Sibelius, Finale, MuseScore) |
| Audio Processing | pydub | Simple API for format conversion, normalization, effects |
| Composition Framework | SCAMP | Excellent for managing musical time, quantization, and playback |

---

## Key Packages & Tools

### Core Music Libraries

| Package | Purpose | Installation |
|---------|---------|--------------|
| **music21** | Comprehensive musicology toolkit (MIT-developed) | `pip install music21` |
| **mingus** | Intuitive music theory (scales, chords, progressions) | `pip install mingus` |
| **mido** | Low-level MIDI file handling and messaging | `pip install mido` |
| **pretty_midi** | High-level MIDI manipulation and analysis | `pip install pretty_midi` |
| **abjad** | Python API for LilyPond notation | `pip install abjad` |
| **scamp** | Composition framework with quantization/playback | `pip install scamp` |
| **partitura** | Symbolic music processing (MusicXML/MIDI) | `pip install partitura` |

### Audio & Synthesis

| Package | Purpose | Installation |
|---------|---------|--------------|
| **pyfluidsynth** | Python bindings for FluidSynth | `pip install pyfluidsynth` |
| **fluidsynth** | SoundFont-based synthesizer (system pkg) | `apt install fluidsynth` |
| **pydub** | Audio processing, format conversion | `pip install pydub` |
| **numpy** | Numerical operations for audio arrays | `pip install numpy` |

### System Dependencies

| Dependency | Purpose |
|------------|---------|
| **FluidSynth** | Real-time MIDI synthesis with SoundFonts |
| **LilyPond** | High-quality sheet music engraving |
| **Timidity++** (optional) | Alternative MIDI synthesis backend |

---

## Music Theory Fundamentals

### Scales and Modes

#### Diatonic Scales (for Orchestral Composition)

| Scale Type | Intervals (from root) | Character | Common Use in Orchestral Music |
|------------|----------------------|-----------|-------------------------------|
| **Major (Ionian)** | W-W-H-W-W-W-H | Bright, happy | Triumphant themes, joyful movements |
| **Natural Minor (Aeolian)** | W-H-W-W-H-W-W | Dark, sad | Melancholic, somber passages |
| **Harmonic Minor** | W-H-W-W-H-W+H-H | Exotic, dramatic | EasternEuropean influence, dramatic tension |
| **Melodic Minor** | Asc: W-H-W-W-W-W-H / Desc: natural | Complex, fluid | Jazz-influenced orchestral writing |

#### Church Modes (Historical/Emotional)

| Mode | Scale Degrees | Emotional Quality | Orchestral Application |
|------|---------------|-------------------|------------------------|
| **Dorian** | 1-2-b3-4-5-6-b7 | Hopeful, medieval | Celtic-inspired, ancient atmosphere |
| **Phrygian** | 1-b2-b3-4-5-b6-b7 | Dark, Spanish/middle-eastern | Dramatic, tense passages |
| **Lydian** | 1-2-3-#4-5-6-7 | Dreamy, floating | Fantasy, wonder, otherworldly |
| **Mixolydian** | 1-2-3-4-5-6-b7 | Folk-like, open | Americana, pastoral scenes |
| **Locrian** | 1-b2-b3-4-b5-b6-b7 | Unstable, diminished | Rarely used; tension/horror |

#### Pentatonic and Other Scales

| Scale | Notes | Use Case |
|-------|-------|----------|
| **Major Pentatonic** | 1-2-3-5-6 | Simple melodies, Asian-influenced |
| **Minor Pentatonic** | 1-b3-4-5-b7 | Blues, folk influence |
| **Whole Tone** | W-W-W-W-W-W | Dream sequences, surrealism |
| **Octatonic (Diminished)** | W-H-W-H-W-H-W-H | Tension, horror, dramatic |

**Python Code Example (mingus):**

```python
from mingus.containers import Note, Scale
from mingus.keys import Key

# Get scale notes
C_major = Scale("C", "major").ascending()
print(f"C Major: {C_major}")  # ['C', 'D', 'E', 'F', 'G', 'A', 'B']

D_dorian = Scale("D", "dorian").ascending()
print(f"D Dorian: {D_dorian}")  # ['D', 'E', 'F', 'G', 'A', 'B', 'C']

# Harmonic minor for dramatic effect
A_harmonic_minor = Scale("A", "harmonic_minor").ascending()
print(f"A Harmonic Minor: {A_harmonic_minor}")  # ['A', 'B', 'C', 'D', 'E', 'F', 'G#']
```

### Chord Progressions

#### Common Practice Period Progressions

The foundation of Western orchestral harmony rests on several well-established progressions:

| Progression | Roman Numerals (C Major) | Emotional Effect |
|-------------|--------------------------|------------------|
| **Authentic Cadence** | V - I (G - C) | Final resolution, conclusive |
| **Plagal Cadence** | IV - I (F - C) | Amen cadence, softer resolution |
| **Deceptive Cadence** | V - vi (G - Am) | Unexpected continuation, surprise |
| **Half Cadence** | I/V - V (C/D - G) | Pause, continuation expected |

#### Essential Progressions for Orchestral Writing

```
1. I - IV - V - I (Basic Foundation)
   C Major: C - F - G - C
   Use: Establishing key, simple themes

2. I - vi - IV - V (Pop/Orchestral hybrid)
   C Major: C - Am - F - G
   Use: Emotional depth, cinematic buildup

3. ii - V - I (Jazz-influenced classical)
   C Major: Dm - G - C
   Use: Sophisticated harmonic motion

4. Circle of Fifths (Baroque foundation)
   I - IV - vii - iii - vi - ii - V - I
   C Major: C - F - Bdim - Em - Am - Dm - G - C
   Use: Extended harmonic journeys

5. Descending Fifths Sequence
   I - IV - vii - iii - vi - ii - V - I
   Creates strong forward momentum

6. I - V - vi - iii - IV - I - IV - V (Pachelbel's Canon)
   Use: Ground bass variations, repetitive structures
```

#### Romantic/Era-Specific Progressions

| Era | Characteristic Progressions |
|-----|----------------------------|
| **Baroque** | Circle of fifths, sequences, ground bass |
| **Classical** | I - IV - V - I, simple modulations |
| **Romantic** | Extended chords (9th, 11th), chromatic mediants |
| **20th Century** | Polychords, quartal harmony, bitonality |

**Python Code Example (mingus):**

```python
from mingus.containers import Note, Chord
from mingus.keys import Key

# Basic triads
C_major = Chord("C")
print(f"C Major chord: {C_major}")  # C- E- G

# Extended chords
C_major_7 = Chord("Cmaj7")
print(f"Cmaj7: {C_major_7}")  # C- E- G- B

# Diatonic chords in C Major
key_c = Key("C", "major")
for degree in ["I", "ii", "iii", "IV", "V", "vi", "vii"]:
    chord = key_c.get_chord(degree)
    print(f"{degree}: {chord}")
```

### Voice Leading

Voice leading is the art of moving individual melodic lines smoothly between chords. Following species counterpoint principles (Fux):

#### First Species (Note Against Note)

1. **Contrary motion** is preferred (voices move in opposite directions)
2. **Parallel perfect intervals** (P5, P8) are forbidden between outer voices
3. **Leading tone** (7th scale degree) should resolve upward to tonic
4. **Sevenths** should resolve downward by step

#### General Rules for SATB Writing

| Rule | Description |
|------|-------------|
| **Range Limits** | Soprano: C4-A5, Alto: G3-F5, Tenor: C3-C5, Bass: E2-E4 |
| **Spacing** | No more than an octave between adjacent upper voices |
| **Doubling** | Double the root in primary triads; avoid doubling the leading tone |
| **Common Tones** | Keep common tones between chords when possible |
| **Stepwise Motion** | Prefer stepwise motion; skip> should be followed by step in opposite direction |

#### Voice Leading Principles for Orchestration

```python
# Example: Smooth voice leading between I and IV in C Major
# I (C-E-G) to IV (F-A-C)

# GOOD voice leading (common tone C, stepwise motion):
# Soprano: G -> A (step up)
# Alto: E -> F (step up)
# Tenor: C -> C (common tone)
# Bass: C -> F (4th down, necessary for root progression)

# POOR voice leading:
# All voices jumping in parallel motion
# Soprano: G -> C
# Alto: E -> A
# Tenor: C -> F
# Bass: C -> F (parallel perfect intervals)
```

### Orchestration Basics

#### Instrument Families and Standard Ranges

**Strings Family**

| Instrument | Written Range | Sounding Range | Transposition |
|------------|---------------|----------------|---------------|
| **Violin** | G3 - A7 | G3 - A7 | None (treble clef) |
| **Viola** | C3 - E6 | C3 - E6 | None (alto clef primarily) |
| **Cello** | C2 - E5 | C2 - E5 | None (bass/tenor clef) |
| **Double Bass** | E1 - C5 | E1 - C5 | Sounds octave lower |
| **Harp** | Cb1 - G#7 | Cb1 - G#7 | None |

**Woodwinds Family**

| Instrument | Written Range | Concert Range | Transposition |
|------------|---------------|---------------|---------------|
| **Flute** | C4 - D7 | C4 - D7 | None |
| **Piccolo** | D5 - C8 | D5 - C8 | Sounds octave higher |
| **Oboe** | Bb3 - A6 | Bb3 - A6 | None |
| **Clarinet (Bb)** | E3 - C7 | D3 - Bb6 | Major 2nd higher |
| **Bassoon** | Bb1 - Eb5 | Bb1 - Eb5 | None |

**Brass Family**

| Instrument | Written Range | Concert Range | Transposition |
|------------|---------------|---------------|---------------|
| **Trumpet (C)** | E3 - C6 | E3 - C6 | None |
| **Trumpet (Bb)** | E3 - C6 | F3 - Bb5 | Major 2nd lower |
| **French Horn** | B1 - F5 | varies | F horn sounds P5 lower |
| **Trombone** | E2 - F5 | E2 - F5 | None (bass clef) |
| **Tuba** | D1 - F4 | D1 - F4 | None |

**Percussion (Key Instruments)**

| Instrument | Range | Notation |
|------------|-------|----------|
| **Timpani** | Typically 2-4 drums, F2-C3 | Bass clef |
| **Orchestral Bells** | C5-C6 | Treble clef, 8va |
| **Xylophone** | F4-C7 | Treble clef |
| **Glockenspiel** | C5-C8 | Treble clef, 2 octaves higher sounding |

#### Standard Orchestral Combinations

**Effective Instrument Doublings**

| Combination | Effect |
|-------------|--------|
| **Flute + Violin I** (octave) | Bright, reinforced melody |
| **Clarinet + Viola** | Warm, mellow blend |
| **Bassoon + Cello** (octave) | Rich bass foundation |
| **Horn + Low Strings** | Powerful bass support |
| **Oboe + Clarinet** (3rds) | Distinctive woodwind color |
| **Trumpet + Flute** (octave) | Bright, cutting melody |

**Instrumental Roles**

| Role | Typical Instruments |
|------|---------------------|
| **Melody** | Violin I, flute, oboe, trumpet, horn |
| **Counter-melody** | Violin II, viola, clarinet, bassoon |
| **Harmony** | Violas, cellos, woodwinds in pairs |
| **Bass** | Cello, double bass, bassoon, tuba |
| **Color** | Harp, percussion, solo woodwinds |

#### Dynamic Balance (Relative Loudness)

```
Loudest to Softest (at forte):
Trumpets/Trombones > Horns > Timpani > Violins I > Cello >
Violas > Woodwinds > Double Bass > Harp
```

---

## Implementation Considerations

### Note Representation in Code

#### MIDI Note Numbers

| Note | MIDI Number | Frequency (Hz) |
|------|-------------|----------------|
| C4 (Middle C) | 60 | 261.63 |
| A4 (Concert A) | 69 | 440.00 |
| C5 | 72 | 523.25 |

**Conversion Formula:**
```
MIDI to Frequency: f = 440 * 2^((n - 69) / 12)
Frequency to MIDI: n = 12 * log2(f/440) + 69
```

**Python Implementation:**

```python
import math

def midi_to_frequency(midi_note: int) -> float:
    """Convert MIDI note number to frequency in Hz."""
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))

def frequency_to_midi(frequency: float) -> int:
    """Convert frequency in Hz to nearest MIDI note number."""
    return round(12 * math.log2(frequency / 440.0) + 69)

def note_name_to_midi(note: str) -> int:
    """Convert note name (e.g., 'C4', 'A#3') to MIDI number."""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_name = note[:-1]
    octave = int(note[-1])
    return notes.index(note_name) + (octave + 1) * 12

def midi_to_note_name(midi: int) -> str:
    """Convert MIDI number to note name."""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi // 12) - 1
    note = notes[midi % 12]
    return f"{note}{octave}"
```

#### Duration Representation

**Standard Durations (in quarter notes):**

| Symbol | Name | Quarter Note Value |
|--------|------|-------------------|
| 𝅝 | Whole | 4.0 |
| 𝅗𝅥 | Half | 2.0 |
| 𝅘𝅥 | Quarter | 1.0 |
| 𝅘𝅥𝅮 | Eighth | 0.5 |
| 𝅘𝅥𝅯 | Sixteenth | 0.25 |
| 𝅘𝅥𝅰𝅮 | Thirty-second | 0.125 |

**Dotted Values:** Multiply duration by 1.5

```python
# Duration constants
WHOLE = 4.0
HALF = 2.0
QUARTER = 1.0
EIGHTH = 0.5
SIXTEENTH = 0.25

DOTTED_QUARTER = QUARTER * 1.5  # 1.5
DOTTED_HALF = HALF * 1.5         # 3.0
```

#### Velocity (Dynamics)

| Dynamic | MIDI Velocity Range | Typical Use |
|---------|---------------------|-------------|
| pp (pianissimo) | 20-40 | Very soft passages |
| p (piano) | 41-60 | Soft |
| mp (mezzo-piano) | 61-80 | Medium-soft |
| mf (mezzo-forte) | 81-100 | Medium-loud |
| f (forte) | 101-115 | Loud |
| ff (fortissimo) | 116-127 | Very loud |

### MIDI File Generation Example (mido)

```python
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage

def create_simple_midi(output_path: str = "output.mid"):
    """Create a simple MIDI file with a C major scale."""
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Set tempo (120 BPM)
    track.append(MetaMessage('set_tempo', tempo=500000))

    # C major scale ascending
    notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C4 to C5
    duration = 480  # ticks per quarter note

    for note in notes:
        track.append(Message('note_on', note=note, velocity=80, time=0))
        track.append(Message('note_off', note=note, velocity=80, time=duration))

    mid.save(output_path)
```

### Audio Synthesis with FluidSynth

```python
import fluidsynth

def midi_to_audio(midi_path: str, output_path: str,
                  soundfont_path: str = "GeneralUser GS.sf2"):
    """Convert MIDI file to audio using FluidSynth."""
    fs = fluidsynth.Synth()
    fs.start()

    # Load SoundFont
    sfid = fs.sfload(soundfont_path)
    fs.program_select(0, sfid, 0, 0)  # Bank 0, Program 0 (Acoustic Grand Piano)

    # For orchestral instruments, use different programs:
    # Program 40 = Violin, 41 = Viola, 42 = Cello, 43 = Contrabass
    # Program 73 = Flute, 74 = Oboe, 75 = Clarinet, 76 = Bassoon
    # Program 56 = Trumpet, 60 = French Horn, 57 = Trombone

    # Load and play MIDI file
    midi_data = fluidsynth.midi.MIDIFile(midi_path)

    # Render to audio
    fs.program_select(0, sfid, 0, 40)  # Violin
    audio = fs.get_samples(midi_data)

    # Save as WAV
    import numpy as np
    from scipy.io import wavfile

    audio_array = np.array(audio, dtype=np.int16)
    wavfile.write(output_path, 44100, audio_array)

    fs.delete()
```

### Sheet Music Generation with Abjad

```python
from abjad import *

def create_simple_score(output_path: str = "score.pdf"):
    """Create a simple sheet music with Abjad."""
    # Create a staff
    staff = Staff("c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4")

    # Add dynamic markings
    attach(Dynamic('mp'), staff[0])
    attach(Crescendo(), staff[0])
    attach(Dynamic('mf'), staff[4])

    # Create a score
    score = Score([staff])

    # Write to LilyPond file and render
    LilyPondFile(
        items=[score],
        include_file_names=['../ly/stylesheet.ily']
    ).as_pdf(output_path)
```

### MusicXML Export with music21

```python
from music21 import stream, note, key, tempo, meter

def create_musicxml(output_path: str = "output.xml"):
    """Create a MusicXML file using music21."""
    s = stream.Score()

    # Add metadata
    s.insert(0, metadata.Metadata())
    s.insert(0, key.KeySignature(0))  # C major, no sharps/flats
    s.insert(0, meter.TimeSignature('4/4'))
    s.insert(0, tempo.MetronomeMark(number=120))

    # Add notes
    notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
    for n in notes:
        s.append(note.Note(n, quarterLength=1.0))

    # Export to MusicXML
    s.write('musicxml', fp=output_path)
```

### Musical Form Structures

**Binary Form (AB)**
```python
def compose_binary():
    """Simple binary form: A (8 bars) + B (8 bars)"""
    # Section A: Establish theme in tonic
    # Section B: Develop in dominant or relative, return to tonic
    pass
```

**Ternary Form (ABA)**
```python
def compose_ternary():
    """Ternary form: A (8 bars) + B (8 bars) + A' (8 bars)"""
    # Section A: Main theme
    # Section B: Contrasting theme
    # Section A': Return to main theme, possibly with variation
    pass
```

**Sonata Form (Classical)**
```python
def compose_sonata():
    """Sonata-allegro form structure"""
    # Exposition: Theme 1 (tonic) -> Bridge -> Theme 2 (dominant/relative)
    # Development: Themes developed, modulated
    # Recapitulation: Theme 1 (tonic) -> Bridge -> Theme 2 (tonic)
    pass
```

---

## Complexity and Challenges

### Technical Challenges

1. **Realistic Orchestral Balance**
   - Different instruments have different perceived volumes
   - Need velocity/dynamic adjustment per instrument
   - Solution: Instrument-specific gain curves

2. **Expressive Performance**
   - Human-like articulation, rubato, phrasing
   - Solution: Templates with micro-timing variations

3. **Polyphony Limitations**
   - MIDI channel limitations (16 channels)
   - Solution: Multiple tracks, program changes

4. **Sheet Music Layout**
   - Automatic part extraction, page turns
   - Solution: LilyPond handles most cases, manual tuning for complex scores

5. **Sound Quality**
   - SoundFont quality varies greatly
   - Solution: High-quality commercial SoundFonts or sample libraries

### Musical Challenges

1. **Generating Memorable Melodies**
   - Avoiding random-sounding sequences
   - Solution: Motivic development, contour templates

2. **Harmonic Coherence**
   - Maintaining tonal center, smooth modulations
   - Solution: Circle of fifths, pivot chords

3. **Voice Leading at Scale**
   - Generating 4+ independent, coherent lines
   - Solution: Species counterpoint rules as constraints

4. **Structural Integrity**
   - Creating satisfying musical forms
   - Solution: Pre-defined form templates with thematic return

---

## Next Steps

### Phase 1: Foundation (Week 1-2)

1. **Set up development environment**
   ```bash
   pip install music21 mingus mido pretty-midi abjad scamp partitura
   pip install pydub pyfluidsynth numpy scipy
   apt install fluidsynth lilypond  # Linux
   ```

2. **Create core data structures**
   - `Note` class (pitch, duration, velocity)
   - `Chord` class (collection of notes)
   - `Scale` class (scale patterns, diatonic chords)
   - `Part` class (single instrument line)
   - `Score` class (collection of parts)

3. **Implement basic music theory module**
   - Scale generators (major, minor, modes)
   - Chord generators (diatonic, extended)
   - Progression templates

### Phase 2: MIDI Output (Week 3)

1. **MIDI writer implementation**
   - Convert Score to MIDI file format
   - Handle tempo, time signatures
   - Multi-track output (per instrument)

2. **MIDI to audio pipeline**
   - FluidSynth integration
   - SoundFont loading
   - Basic mixing

### Phase 3: Composition Engine (Week 4-5)

1. **Melody generation**
   - Scale-based note selection
   - Contour templates (ascending, descending, arch)
   - Rhythmic patterns

2. **Harmonization**
   - Generate chord progression from scale
   - Add bass line (root movement)
   - Add inner voices (voice leading rules)

3. **Orchestration templates**
   - Predefined instrument combinations
   - Dynamic curves
   - Articulation patterns

### Phase 4: Sheet Music Output (Week 6)

1. **MusicXML generation**
   - Use music21 for export
   - Test with MuseScore import

2. **LilyPond generation**
   - Use Abjad for notation
   - Custom layout templates

---

## Sources

- [music21 Documentation](https://www.music21.org/)
- [mingus Documentation](https://bspaans.github.io/python-mingus/)
- [SCAMP Framework](https://scamp.marcevanstein.com/)
- [Abjad LilyPond API](https://abjad.github.io/)
- [Partitura Symbolic Music Processing](https://partitura.readthedocs.io/)
- [GeneralUser GS SoundFont](https://schristiancollins.com/generaluser.php)
- [Open Music Theory - Voice Leading](https://viva.pressbooks.pub/openmusictheory/)
- [Puget Sound Music Theory](https://musictheory.pugetsound.edu/)
- [Classical FM - Musical Modes](https://www.classicfm.com/discover-music/latest/guide-to-musical-modes/)
- [Ranges of Orchestral Instruments](https://www.orchestralibrary.com/reftables/rang.html)
