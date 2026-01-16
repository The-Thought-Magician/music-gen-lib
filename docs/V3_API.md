# V3 API Reference

Complete API documentation for music-gen-lib V3.

## Core Classes

### CompositionRequest

Request parameters for music generation.

```python
from musicgen.generator import CompositionRequest

request = CompositionRequest(
    mood="peaceful",           # Mood preset name
    key="C major",             # Key signature (overrides mood)
    scale="major",             # Scale type (overrides mood)
    tempo=120,                 # BPM (overrides mood preset)
    duration=30,               # Duration in seconds
    instruments=["piano"],     # Instrument list
    title="My Composition",    # Composition title
    composer="AI",             # Composer name
    output_dir=".",            # Output directory
    export_formats=["midi"],   # Formats: midi, audio, musicxml, pdf
    seed=42                    # Random seed for reproducibility
)
```

**Attributes:**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `mood` | str | "peaceful" | Mood preset to use |
| `key` | str \| None | None | Key signature (e.g., "C minor") |
| `scale` | str \| None | None | Scale type (major, minor, dorian, etc.) |
| `tempo` | int \| None | None | Tempo in BPM |
| `duration` | int | 30 | Duration in seconds |
| `instruments` | list[str] \| None | None | List of instrument names |
| `title` | str | "" | Composition title |
| `composer` | str | "MusicGen" | Composer name |
| `output_dir` | str | "." | Output directory |
| `export_formats` | list[str] | ["midi"] | Export formats |
| `seed` | int \| None | None | Random seed |

### CompositionResult

Result of a music generation request.

```python
result = generate(request)

print(result.score)           # Generated Score object
print(result.key)             # "C major"
print(result.scale_type)      # "major"
print(result.tempo)           # 120
print(result.instruments)     # ["piano", "strings", ...]
print(result.midi_path)       # Path to MIDI file
print(result.audio_path)      # Path to audio file
print(result.title)           # Composition title
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `score` | Score | The generated music score |
| `key` | str | Key signature used |
| `scale_type` | str | Scale type used |
| `tempo` | int | Tempo used |
| `instruments` | list[str] | Instruments used |
| `midi_path` | str \| None | Path to MIDI file |
| `audio_path` | str \| None | Path to audio file |
| `musicxml_path` | str \| None | Path to MusicXML file |
| `pdf_path` | str \| None | Path to PDF file |
| `title` | str | Composition title |

## V3 AI Models

### AIComposition

Main model for AI-generated compositions.

```python
from musicgen.ai_models.composition import AIComposition

composition = AIComposition(
    title="My Piece",
    composer="AI",
    tempo=120,
    time_signature=TimeSignature(numerator=4, denominator=4),
    key=KeySignature(tonic="C", mode="major"),
    parts=[...],  # List of AIPart
    structure_type=StructureType.PART_BASED
)
```

**Attributes:**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | str | required | Composition title |
| `composer` | str \| None | None | Composer name |
| `tempo` | int | 120 | Initial tempo in BPM (40-300) |
| `time_signature` | TimeSignature | TimeSignature() | Time signature |
| `key` | KeySignature | KeySignature("C", "major") | Key signature |
| `parts` | list[AIPart] | [] | Instrument parts |
| `measures` | list[AIMeasure] | [] | Measure-based structure |
| `tempo_changes` | list[TempoEvent] | [] | Tempo changes |
| `time_signature_changes` | list[TimeSignatureEvent] | [] | Time sig changes |
| `form` | str \| None | None | Musical form |
| `mood` | str \| None | None | Mood description |
| `initial_dynamic` | str \| None | None | Starting dynamic |
| `structure_type` | StructureType | PART_BASED | Organization type |

**Methods:**

```python
# Get parts (converts from measures if needed)
parts = composition.get_parts()

# Get tempo at a specific time
tempo = composition.get_tempo_at(10.5)  # At quarter note 10.5

# Get time signature at measure
ts = composition.get_time_signature_at(5)  # At measure 5

# Get total duration
duration = composition.duration_quarters  # In quarter notes
duration_sec = composition.duration_seconds  # In seconds

# Get parts by role
melodies = composition.get_melody_parts()
basses = composition.get_bass_parts()

# Get specific part
part = composition.get_part_by_name("Violin I")
```

### AIPart

An instrument part with notes.

```python
from musicgen.ai_models.parts import AIPart, InstrumentRole

part = AIPart(
    name="Violin I",
    midi_program=40,      # Violin
    midi_channel=0,
    role=InstrumentRole.MELODY,
    notes=[...],          # List of AINote or AIRest
    dynamics_marking="mf",
    volume_adjustment=0,
    default_articulation="legato",
    cc_events=[...],      # Control change events
    sustain_pedal=True
)
```

**Attributes:**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | str | required | Instrument name |
| `midi_program` | int | required | MIDI program (0-127) |
| `midi_channel` | int | 0 | MIDI channel (0-15) |
| `role` | InstrumentRole | MELODY | Part role |
| `notes` | list | [] | Notes and rests |
| `dynamics_marking` | str \| None | None | Dynamic (pp, p, mp, mf, f, ff, fff) |
| `volume_adjustment` | int | 0 | Volume in dB (-127 to 127) |
| `default_articulation` | str \| None | None | Default articulation |
| `cc_events` | list | [] | CC events |
| `sustain_pedal` | bool | False | Auto-generate sustain |

**Instrument Roles:**

- `MELODY` - Main melodic line
- `HARMONY` - Harmonic support
- `BASS` - Bass line
- `ACCOMPANIMENT` - Accompaniment figures
- `COUNTERMELODY` - Counter-melody
- `PAD` - Sustained pads
- `PERCUSSION` - Percussion

**Methods:**

```python
# Get note events
events = part.get_note_events()

# Get duration
duration = part.duration_quarters  # In quarter notes

# Get CC events
cc = part.get_cc_events()

# Add sustain pedal
part.add_sustain_pedal(on_time=0.0, off_time=4.0)
```

### AINote

A single note.

```python
from musicgen.ai_models.notes import AINote, ArticulationType

note = AINote(
    note_name="C4",      # Or use midi_number or frequency
    duration=1.0,        # In quarter notes
    start_time=0.0,      # In quarter notes from part start
    velocity=80,         # 0-127
    tied=False,
    articulation=ArticulationType.LEGATO
)
```

**Attributes:**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `note_name` | str \| None | None | Note like "C4", "Ab3" |
| `midi_number` | int \| None | None | MIDI note (0-127) |
| `frequency` | float \| None | None | Frequency in Hz |
| `duration` | float | required | Duration in quarters |
| `start_time` | float | 0.0 | Start time in quarters |
| `velocity` | int | 80 | MIDI velocity (0-127) |
| `tied` | bool | False | Tied to next note |
| `articulation` | ArticulationType \| None | None | Articulation |

**Articulation Types:**

- `STACCATO` - Short and detached
- `LEGATO` - Smooth and connected
- `ACCENT` - Emphasized attack
- `MARCATO` - Strongly emphasized
- `TENUTO` - Held for full value
- `SFORZANDO` - Strong sudden accent

**Methods:**

```python
# Get MIDI number
midi = note.get_midi_number()  # 60 for C4

# Get frequency
freq = note.get_frequency()  # ~261.63 Hz for C4
```

### AIRest

A rest (silence).

```python
from musicgen.ai_models.notes import AIRest

rest = AIRest(
    duration=1.0,      # In quarter notes
    start_time=0.0     # In quarter notes
)
```

### ControlChangeEvent

MIDI Continuous Controller event.

```python
from musicgen.ai_models.notes import ControlChangeEvent, CC

cc = ControlChangeEvent(
    controller=CC.EXPRESSION,  # CC number
    value=100,                 # 0-127
    time=0.0                   # In quarter notes
)
```

**Common CC Numbers:**

| CC | Name | Description |
|----|------|-------------|
| 1 | MODULATION | Vibrato depth |
| 7 | VOLUME | Channel volume |
| 10 | PAN | Stereo pan |
| 11 | EXPRESSION | Expression (volume layer) |
| 64 | DAMPER_PEDAL | Sustain pedal |
| 71 | TIMBRE | Brightness/filter |
| 74 | BRIGHTNESS | Filter cutoff |

## Main Generator Function

### generate()

Generate a complete music composition.

```python
from musicgen import generate, CompositionRequest

result = generate(
    CompositionRequest(
        mood="peaceful",
        duration=60,
        export_formats=["midi", "audio"]
    )
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | CompositionRequest | Generation parameters |

**Returns:** `CompositionResult`

### list_available_moods()

Get list of available mood presets.

```python
from musicgen.generator import list_available_moods

moods = list_available_moods()
# ['peaceful', 'melancholic', 'epic', 'playful', 'mysterious', ...]
```

## Score and Parts

### Score

Container for a complete musical score.

```python
from musicgen.io.midi_writer import Score

score = Score(
    title="My Piece",
    composer="AI"
)

# Add parts
score.add_part(part1)
score.add_part(part2)

# Access parts
for part in score.parts:
    print(part.name)
```

### Part

A single instrument part.

```python
from musicgen.io.midi_writer import Part

part = Part(name="Piano")
part.notes = [note1, note2, ...]

# Add individual notes
part.add_note(note)

# Get part info
print(part.name)
print(len(part.notes))
```

## Theory API

### Key

Represent a musical key.

```python
from musicgen.theory.keys import Key

key = Key("C", "major")  # tonic, key_type

# Get scale
scale = key.get_scale()

# Get chords
chords = key.get_diatonic_chords()

# Get relative/parallel
relative = key.get_relative_minor()
parallel = key.get_parallel_major()
```

### Scale

Musical scale with pitches.

```python
from musicgen.theory.scales import Scale, ScaleType

scale = Scale("C", "major")

# Get pitches
pitches = scale.pitches  # [C, D, E, F, G, A, B]

# Get degrees
degree = scale.get_degree(5)  # G

# Check if note in scale
in_scale = scale.contains("G#")

# Available scale types
ScaleType.MAJOR
ScaleType.MINOR
ScaleType.HARMONIC_MINOR
ScaleType.MELODIC_MINOR
ScaleType.DORIAN
ScaleType.PHRYGIAN
ScaleType.LYDIAN
ScaleType.MIXOLYDIAN
ScaleType.LOCRIAN
```

### Progression

Chord progression.

```python
from musicgen.theory.progressions import Progression

# From Roman numerals
prog = Progression.from_roman("I-IV-V-I", key="C")

# Functional generation
prog = Progression.functional(key=key, length=8)

# Access chords
for chord in prog.chords:
    print(chord)
```

## Melody Generation

### MelodyGenerator

Generate melodic lines.

```python
from musicgen.composition.melody import MelodyGenerator, MelodicContour
from musicgen.theory.scales import Scale
from musicgen.theory.keys import Key

scale = Scale("C", "major")
key = Key("C", "major")

gen = MelodyGenerator(scale, key, tempo=120)

# Set seed for reproducibility
gen.set_seed(42)

# Generate melody
melody = gen.generate_melody(
    progression=progression,
    contour=MelodicContour.WAVE,
    motivic_unity=0.7,
    length=16
)

# Generate a motif
motif = gen.generate_motif(length=8, contour=MelodicContour.ASCENDING)
```

**Melodic Contours:**

- `ASCENDING` - Generally rising
- `DESCENDING` - Generally falling
- `WAVE` - Wave-like motion
- `ARCH` - Rising then falling
- `INVERTED_ARCH` - Falling then rising

### Melody

Container for melodic material.

```python
from musicgen.composition.melody import Melody

melody = Melody(notes=[...])

# Access
for note in melody.notes:
    print(note)

# Get length
length = melody.length  # Number of notes
duration = melody.duration  # In quarter notes
```

## Orchestration

### Instrument

Instrument definition.

```python
from musicgen.orchestration.instruments import Instrument, InstrumentFamily, Voice

instrument = Instrument(
    name="Violin",
    family=InstrumentFamily.STRINGS,
    range=(55, 100),  # MIDI range
    transposition=0
)
```

**Instrument Families:**

- `STRINGS` - Violin, viola, cello, bass
- `WOODWINDS` - Flute, oboe, clarinet, bassoon
- `BRASS` - Trumpet, horn, trombone, tuba
- `PERCUSSION` - Timpani, bells, etc.
- `KEYBOARDS` - Piano, harpsichord, etc.

### Ensemble

Preset ensemble configurations.

```python
from musicgen.orchestration.ensembles import Ensemble

# Get preset ensemble
ensemble = Ensemble.get_preset("string_quartet")

# Custom ensemble
ensemble = Ensemble(
    name="My Ensemble",
    instruments=["Violin", "Violin", "Viola", "Cello"],
    texture=TextureType.HOMOPHONIC
)
```

## MIDI Export

### MIDIWriter

Write scores to MIDI files.

```python
from musicgen.io.midi_writer import MIDIWriter

# Write score
MIDIWriter.write(
    score=score,
    filepath="output.mid",
    tempo=120
)

# Write with custom options
MIDIWriter.write(
    score=score,
    filepath="output.mid",
    tempo=100,
    time_signature=(4, 4),
    key_signature=0  # 0 = C major
)
```

## Configuration

### Mood Presets

Get and use mood presets.

```python
from musicgen.config.moods import get_mood_preset, list_moods

# List available moods
moods = list_moods()

# Get specific preset
preset = get_mood_preset("peaceful")

print(preset.key)         # "C"
print(preset.scale)       # "major"
print(preset.tempo_min)   # 60
print(preset.tempo_max)   # 80
print(preset.instruments) # ["piano", "strings", ...]
```

## AI Client (V3)

### GeminiComposer

AI-powered composition using Google Gemini.

```python
from musicgen.ai.client import GeminiComposer

composer = GeminiComposer(api_key="your-key")

# Generate orchestration plan
plan = composer.generate_plan(
    prompt="A melancholic string quartet",
    duration_seconds=120,
    key="D minor"
)

# Access plan
print(plan.title)
print(plan.key)
for section in plan.sections:
    print(section.name)
```

**Methods:**

```python
# Generate orchestration plan
plan = composer.generate_plan(
    prompt="...",
    duration_seconds=120,
    key="C major",
    mood="peaceful"
)

# Generate from mood
plan = composer.generate_from_mood(
    mood="epic",
    duration_seconds=60
)

# Build composition from plan
from musicgen.ai.composer import build_composition_from_plan
score = build_composition_from_plan(plan, seed=42)
```

## Validation API

### Voice Leading Validation

Check for common voice leading errors.

```python
from musicgen.theory.voice_leading import VoiceLeadingValidator

validator = VoiceLeadingValidator()

# Check for parallel fifths/octaves
errors = validator.check_parallel_intervals(part1, part2)

# Check leading tone resolution
errors = validator.check_leading_tone_resolution(part, key="C major")

# Check direct intervals
errors = validator.check_direct_intervals(part1, part2)
```

### Progression Validation

Validate chord progressions.

```python
from musicgen.theory.progressions import validate_progression

is_valid, errors = validate_progression(
    progression=prog,
    key="C major",
    style="common_practice"
)
```
