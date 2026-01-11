# Implementation Plan: Music Generation Library

## Overview

This project is a Python library that generates orchestral instrumental music using traditional music theory principles (rule-based composition, not AI). The library will produce both sheet music (MusicXML/LilyPond format) and audio files (WAV/FLAC) from programmatic input based on mood/theme parameters.

The library implements:
- Music theory foundations (scales, chords, progressions, voice leading)
- Melody generation with motivic development
- Multi-instrument orchestration
- Musical form structures (binary, ternary, rondo)
- MIDI, audio, and sheet music export capabilities

---

## Implementation Steps

### Step 1: Project Setup and Core Data Structures

**Objective**: Establish the project structure and define fundamental music data representations.

**Tasks**:
- [ ] Create project directory structure (`src/musicgen/`, `tests/`, `examples/`)
- [ ] Set up `pyproject.toml` with project metadata and dependencies
- [ ] Create `__init__.py` files for package structure
- [ ] Implement `Note` class (pitch, duration, velocity, articulation)
- [ ] Implement `Chord` class (collection of notes, inversion, quality)
- [ ] Implement `Rest` class (duration only)
- [ ] Define duration constants (WHOLE, HALF, QUARTER, EIGHTH, SIXTEENTH)
- [ ] Define dynamic constants (PP, P, MP, MF, F, FF)

**Deliverables**:
- `src/musicgen/__init__.py`
- `src/musicgen/core/__init__.py`
- `src/musicgen/core/note.py` (Note, Rest, duration/dynamic constants)
- `src/musicgen/core/chord.py` (Chord class)
- `pyproject.toml`
- `tests/test_note.py`
- `tests/test_chord.py`

**Validation**:
```python
# Test note creation and conversion
note = Note("C4", QUARTER, velocity=90)
assert note.name == "C"
assert note.octave == 4
assert note.midi_number == 60
assert note.frequency == approx(261.63)

# Test chord creation
chord = Chord("C", "major", root_octave=4)
assert [n.name for n in chord.notes] == ["C", "E", "G"]
assert chord.inversion == 0
```

---

### Step 2: Music Theory Module - Scales and Keys

**Objective**: Implement scale generation, key signatures, and modal relationships.

**Tasks**:
- [ ] Create scale pattern definitions (major, minor, modes, pentatonic)
- [ ] Implement `Scale` class with scale degree access
- [ ] Implement `Key` class for key signature management
- [ ] Add scale interval calculations
- [ ] Implement diatonic chord generation from scales
- [ ] Add parallel and relative key relationships
- [ ] Create scale degree to note name conversion

**Deliverables**:
- `src/musicgen/theory/__init__.py`
- `src/musicgen/theory/scales.py`
- `src/musicgen/theory/keys.py`
- `tests/test_scales.py`
- `tests/test_keys.py`

**Validation**:
```python
# Test scale generation
c_major = Scale("C", "major")
assert c_major.notes == ["C", "D", "E", "F", "G", "A", "B"]
assert c_major.get_degree(1) == Note("C4")
assert c_major.get_degree(5) == Note("G4")

# Test modes
d_dorian = Scale("D", "dorian")
assert d_dorian.notes == ["D", "E", "F", "G", "A", "B", "C"]

# Test harmonic minor
a_harmonic_minor = Scale("A", "harmonic_minor")
assert "G#" in a_harmonic_minor.notes

# Test diatonic chords
c_major_diatonic = c_major.diatonic_chords()
assert c_major_diatonic[0].quality == "major"  # I
assert c_major_diatonic[1].quality == "minor"  # ii
```

---

### Step 3: Chord Progression Engine

**Objective**: Create a system for generating musically valid chord progressions.

**Tasks**:
- [ ] Define common progression templates (I-IV-V-I, I-vi-IV-V, ii-V-I, etc.)
- [ ] Implement Roman numeral analysis conversion
- [ ] Add functional harmony labels (tonic, subdominant, dominant)
- [ ] Create progression generator with constraints
- [ ] Implement cadence detection (authentic, plagal, deceptive, half)
- [ ] Add modulation capabilities (pivot chords, common-tone)

**Deliverables**:
- `src/musicgen/theory/progressions.py`
- `tests/test_progressions.py`

**Validation**:
```python
# Test progression templates
prog = Progression.from_roman("I-IV-V-I", key="C")
assert [chord.root_name for chord in prog.chords] == ["C", "F", "G", "C"]

# Test functional generation
prog = Progression.functional(key="C", length=8, cadence="authentic")
assert prog.chords[-1].is_tonic()

# Test circle of fifths
circle = Progression.circle_of_fifths("C", length=4)
assert [c.root_name for c in circle.chords] == ["C", "F", "Bb", "Eb"]
```

---

### Step 4: Voice Leading Module

**Objective**: Implement species counterpoint rules for smooth voice motion.

**Tasks**:
- [ ] Implement voice range constraints (SATB ranges)
- [ ] Create voice motion analyzer (parallel, contrary, oblique, similar)
- [ ] Implement voice leading rules (no parallel fifths/octaves)
- [ ] Add leading tone resolution rules
- [ ] Create four-part harmony generator
- [ ] Implement chord voicing with doublings
- [ ] Add voice spacing rules

**Deliverables**:
- `src/musicgen/theory/voice_leading.py`
- `tests/test_voice_leading.py`

**Validation**:
```python
# Test voice leading between chords
chord_i = Chord("C", "major")
chord_iv = Chord("F", "major")
voices = voice_lead(chord_i, chord_iv, num_voices=4)

# Check no parallel fifths
assert not has_parallel_fifths(voices)

# Check range compliance
for voice in voices:
    assert all(in_range(v.note, v.range) for v in voice)

# Test leading tone resolution
v_i_progression = voice_lead(chord_i, Chord("G", "dominant"))
assert v_i_progression[-1].resolves_upward()  # Leading tone -> tonic
```

---

### Step 5: Melody Generation Engine

**Objective**: Create rule-based melody generation with motivic development.

**Tasks**:
- [ ] Define melodic contour templates (ascending, descending, arch, wave)
- [ ] Implement rhythmic pattern generators
- [ ] Create scale-based note selection with constraint rules
- [ ] Add motif generation and development (repetition, sequence, inversion)
- [ ] Implement interval constraint rules (no awkward leaps)
- [ ] Add phrase structure (antecedent-consequent)
- [ ] Create melody-to-chord alignment

**Deliverables**:
- `src/musicgen/composition/melody.py`
- `tests/test_melody.py`

**Validation**:
```python
# Test melody generation
scale = Scale("C", "major")
progression = Progression.from_roman("I-IV-V-I", key="C")
melody = Melody.generate(scale, progression, length=8)

# Check notes are in scale
assert all(note in scale for note in melody.notes)

# Check contour
assert melody.contour in ["ascending", "descending", "arch", "wave"]

# Test motivic development
motif = Motif.generate(scale, length=4)
developed = motif.develop(method="sequence")
assert developed.length == motif.length
assert developed.related_to(motif)
```

---

### Step 6: Orchestration Module

**Objective**: Define instrument characteristics and create orchestration templates.

**Tasks**:
- [ ] Create `Instrument` class with range, transposition, and characteristics
- [ ] Define orchestral instrument library (strings, woodwinds, brass, percussion)
- [ ] Implement instrument combination presets
- [ ] Add dynamic balance factors per instrument
- [ ] Create texture templates (melody + accompaniment, polyphonic, homophonic)
- [ ] Implement doubling rules (octave doublings, unisons)
- [ ] Add articulation and dynamics assignment

**Deliverables**:
- `src/musicgen/orchestration/__init__.py`
- `src/musicgen/orchestration/instruments.py`
- `src/musicgen/orchestration/ensembles.py`
- `tests/test_instruments.py`
- `tests/test_ensembles.py`

**Validation**:
```python
# Test instrument ranges
violin = Instrument("violin", range="G3-A7")
assert violin.in_range(Note("A4"))
assert not violin.in_range(Note("E3"))

# Test transposition
clarinet = Instrument("clarinet", key="Bb", transposition=2)
assert clarinet.written_to_concert(Note("C4")) == Note("Bb3")

# Test ensemble presets
orchestra = Ensemble.preset("string_quartet")
assert len(orchestra.instruments) == 4
assert "violin" in orchestra.instruments

# Test texture
texture = Texture.homophonic(melody_instruments=["violin"],
                            harmony_instruments=["viola", "cello"])
```

---

### Step 7: Musical Form Structures

**Objective**: Implement formal structures for complete compositions.

**Tasks**:
- [ ] Create `Form` base class and structure definition
- [ ] Implement binary form (AB)
- [ ] Implement ternary form (ABA)
- [ ] Implement rondo form (ABACA)
- [ ] Implement basic sonata form (exposition, development, recapitulation)
- [ ] Add section transition handling
- [ ] Create thematic return and variation logic

**Deliverables**:
- `src/musicgen/composition/forms.py`
- `tests/test_forms.py`

**Validation**:
```python
# Test binary form
binary = Form.binary(a_length=8, b_length=8, key="C")
assert len(binary.sections) == 2
assert binary.sections[0].key == "C"
assert binary.sections[1].key in ["G", "Am"]  # Dominant or relative

# Test ternary form
ternary = Form.ternary(a_length=8, b_length=8, key="C")
assert len(binary.sections) == 3
assert ternary.sections[0].theme == ternary.sections[2].theme

# Test rondo
rondo = Form.rondo(refrain_length=8, episode_length=4, num_episodes=3)
assert rondo.form_pattern == "A-B-A-C-A-D-A"
```

---

### Step 8: MIDI File Generation

**Objective**: Export compositions to MIDI format for playback and editing.

**Tasks**:
- [ ] Implement MIDI file writer using mido
- [ ] Convert Note/Rest to MIDI messages
- [ ] Handle tempo and time signature meta-events
- [ ] Implement multi-track output (one per instrument)
- [ ] Add program change messages for instrument sounds
- [ ] Implement velocity/dynamic mapping
- [ ] Add quantization options

**Deliverables**:
- `src/musicgen/io/midi_writer.py`
- `tests/test_midi_writer.py`
- `examples/generate_midi.py`

**Validation**:
```python
# Test MIDI generation
score = Score()
score.add_part(Part(instrument="violin", notes=[...]))
score.add_part(Part(instrument="cello", notes=[...]))

midi_path = "output.mid"
MIDIWriter.write(score, midi_path)

# Verify file created and valid
assert os.path.exists(midi_path)
midi_file = mido.MidiFile(midi_path)
assert len(midi_file.tracks) == 3  # 2 instruments + tempo track
```

---

### Step 9: Audio Synthesis Pipeline

**Objective**: Convert MIDI to high-quality audio using FluidSynth.

**Tasks**:
- [ ] Implement FluidSynth wrapper class
- [ ] Add SoundFont loading and management
- [ ] Create MIDI-to-audio conversion function
- [ ] Implement instrument program selection
- [ ] Add audio mixing and balance control
- [ ] Implement WAV/FLAC export
- [ ] Add normalization and basic effects (reverb)

**Deliverables**:
- `src/musicgen/io/audio_synthesizer.py`
- `tests/test_audio_synthesizer.py`

**Validation**:
```python
# Test audio synthesis
synth = AudioSynthesizer(soundfont_path="GeneralUser GS.sf2")
audio_path = synth.render(midi_path, output_format="wav")

# Verify audio file
assert os.path.exists(audio_path)
assert audio_file.sample_rate == 44100
assert audio_file.channels == 2  # Stereo

# Test different instruments
synth.set_instrument(track=0, program=40)  # Violin
synth.set_instrument(track=1, program=42)  # Cello
```

---

### Step 10: Sheet Music Generation (MusicXML)

**Objective**: Export compositions to MusicXML for notation software.

**Tasks**:
- [ ] Implement MusicXML writer using music21
- [ ] Convert Score to music21 stream
- [ ] Handle key and time signatures
- [ ] Add dynamic markings
- [ ] Implement part extraction
- [ ] Add articulation and expression marks
- [ ] Test import in MuseScore

**Deliverables**:
- `src/musicgen/io/musicxml_writer.py`
- `tests/test_musicxml_writer.py`
- `examples/generate_sheet_music.py`

**Validation**:
```python
# Test MusicXML export
xml_path = "output.musicxml"
MusicXMLWriter.write(score, xml_path)

# Verify file validity
assert os.path.exists(xml_path)
tree = ET.parse(xml_path)
assert tree.find(".//part") is not None

# Test import in music21
s = music21.converter.parse(xml_path)
assert len(s.parts) == len(score.parts)
```

---

### Step 11: Sheet Music Generation (LilyPond)

**Objective**: Generate publication-quality sheet music using LilyPond.

**Tasks**:
- [ ] Implement LilyPond writer using Abjad
- [ ] Convert Score to Abjad Score object
- [ ] Add layout and formatting
- [ ] Implement PDF generation
- [ ] Add custom style templates
- [ ] Handle multipart scores

**Deliverables**:
- `src/musicgen/io/lilypond_writer.py`
- `tests/test_lilypond_writer.py`
- `examples/generate_pdf.py`

**Validation**:
```python
# Test LilyPond export
pdf_path = "output.pdf"
ly_path = "output.ly"
LilyPondWriter.write(score, output_pdf=pdf_path)

# Verify files
assert os.path.exists(pdf_path)
assert os.path.exists(ly_path)

# Check PDF is valid
assert is_valid_pdf(pdf_path)
```

---

### Step 12: Mood-to-Music Configuration System

**Objective**: Implement the mood-based music generation interface.

**Tasks**:
- [ ] Create mood configuration dictionary (mood -> key, scale, tempo, instruments)
- [ ] Implement `CompositionRequest` class for user input
- [ ] Create mood analyzer/selector
- [ ] Implement main `generate()` function
- [ ] Add CLI interface
- [ ] Create example presets (epic, peaceful, mysterious, triumphant, melancholic)

**Deliverables**:
- `src/musicgen/config/moods.py`
- `src/musicgen/generator.py`
- `src/musicgen/__main__.py` (CLI)
- `examples/mood_examples.py`

**Validation**:
```python
# Test mood-based generation
request = CompositionRequest(mood="epic", duration=60)
result = generate(request)

assert result.score is not None
assert result.midi_path is not None
assert result.audio_path is not None
assert result.sheet_music_path is not None

# Verify mood characteristics
assert result.tempo >= 120  # Epic is fast
assert "violin" in result.instruments
assert "timpani" in result.instruments

# Test CLI
# $ musicgen generate --mood peaceful --duration 30
# Output: Generated peaceful composition (30 seconds)
#   MIDI: peaceful_20250111.mid
#   Audio: peaceful_20250111.wav
#   Sheet: peaceful_20250111.pdf
```

---

### Step 13: Testing and Documentation

**Objective**: Complete test coverage and API documentation.

**Tasks**:
- [ ] Achieve >80% test coverage
- [ ] Add integration tests (full composition pipeline)
- [ ] Write API documentation with docstrings
- [ ] Create Sphinx documentation site
- [ ] Add tutorial notebook(s)
- [ ] Create example gallery with audio samples
- [ ] Write README with quick start guide

**Deliverables**:
- `docs/api/` (Sphinx documentation)
- `docs/tutorials/` (Jupyter notebooks)
- `README.md`
- `CONTRIBUTING.md`
- `examples/` (runnable examples)

**Validation**:
```bash
# Run tests
pytest --cov=src/musicgen --cov-report=html
# Coverage > 80%

# Build docs
cd docs && make html
# Documentation builds without errors

# Run examples
python examples/basic_composition.py
python examples/mood_examples.py
# All examples run successfully
```

---

## Dependencies

### Python Packages (from pyproject.toml)
```toml
[project]
name = "musicgen"
version = "0.1.0"
dependencies = [
    "music21>=9.0",
    "mingus>=0.5",
    "mido>=1.2",
    "pretty-midi>=0.2",
    "abjad>=3.0",
    "pyfluidsynth>=0.1",
    "pydub>=0.25",
    "numpy>=1.24",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-cov>=4.0", "sphinx>=5.0"]
```

### System Dependencies
```bash
# Ubuntu/Debian
sudo apt install fluidsynth lilypond

# macOS
brew install fluidsynth lilypond

# Windows (use WSL or install binaries separately)
```

### SoundFont
- Download GeneralUser GS SoundFont from: https://schristiancollins.com/generaluser.php
- Place in project: `resources/soundfonts/GeneralUser GS.sf2`

---

## Order of Implementation

This implementation order is designed to:

1. **Build bottom-up**: Start with core data structures (Note, Chord) that everything else depends on
2. **Establish theory foundation early**: Scales and progressions are needed before composition
3. **Compose before export**: Melody and orchestration must be implemented before we can export
4. **Audio before notation**: MIDI/audio synthesis is simpler than sheet music and validates composition logic
5. **Mood interface last**: The high-level interface depends on all lower-level components

**Dependencies diagram**:
```
Step 1 (Core)
  -> Step 2 (Scales) -> Step 3 (Progressions) -> Step 4 (Voice Leading)
  -> Step 5 (Melody)
  -> Step 6 (Orchestration)
  -> Step 7 (Forms)
    -> Step 8 (MIDI) -> Step 9 (Audio)
    -> Step 10 (MusicXML) -> Step 11 (LilyPond)
  -> Step 12 (Mood Interface)
  -> Step 13 (Testing/Docs)
```

Each step is designed to be completable in a single session and provides working, testable functionality.

---

## Step Completion Status

| Step | Name | Status |
|------|------|--------|
| 1 | Project Setup and Core Data Structures | Pending |
| 2 | Music Theory Module - Scales and Keys | Pending |
| 3 | Chord Progression Engine | Pending |
| 4 | Voice Leading Module | Pending |
| 5 | Melody Generation Engine | Pending |
| 6 | Orchestration Module | Pending |
| 7 | Musical Form Structures | Pending |
| 8 | MIDI File Generation | Pending |
| 9 | Audio Synthesis Pipeline | Pending |
| 10 | Sheet Music Generation (MusicXML) | Pending |
| 11 | Sheet Music Generation (LilyPond) | Pending |
| 12 | Mood-to-Music Configuration System | Pending |
| 13 | Testing and Documentation | Pending |
