# V3-10: Testing and Quality Assurance

**Status:** Pending
**Priority:** High
**Dependencies:** All previous V3 steps

## Overview

Create comprehensive test suite covering all components: schema validation, MIDI generation, SFZ rendering, validation tools, and end-to-end composition.

---

## Test Categories

### 1. Unit Tests

#### Schema Tests

```python
import pytest
from musicgen.ai_models import (
    Note, InstrumentPart, Composition,
    ArticulationType, DynamicMarking, TimeSignature
)

class TestNoteModel:
    """Test Note data model."""

    def test_note_creation(self):
        """Test creating a valid note."""
        note = Note(
            pitch=60,
            start_time=0.0,
            duration=1.0,
            velocity=90
        )
        assert note.pitch == 60
        assert note.start_time == 0.0
        assert note.duration == 1.0
        assert note.velocity == 90

    def test_pitch_validation(self):
        """Test pitch range validation."""
        with pytest.raises(ValueError):
            Note(pitch=-1, start_time=0.0, duration=1.0, velocity=90)

        with pytest.raises(ValueError):
            Note(pitch=128, start_time=0.0, duration=1.0, velocity=90)

    def test_velocity_validation(self):
        """Test velocity range validation."""
        with pytest.raises(ValueError):
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=-1)

        with pytest.raises(ValueError):
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=128)

    def test_duration_validation(self):
        """Test duration validation."""
        with pytest.raises(ValueError):
            Note(pitch=60, start_time=0.0, duration=0.0, velocity=90)

        with pytest.raises(ValueError):
            Note(pitch=60, start_time=0.0, duration=61.0, velocity=90)

    def test_articulation(self):
        """Test articulation assignment."""
        note = Note(
            pitch=60,
            start_time=0.0,
            duration=1.0,
            velocity=90,
            articulation=ArticulationType.STACCATO
        )
        assert note.articulation == ArticulationType.STACCATO

class TestInstrumentPart:
    """Test InstrumentPart data model."""

    def test_part_creation(self):
        """Test creating a valid instrument part."""
        part = InstrumentPart(
            instrument_name="Violin Solo",
            instrument_family="strings",
            midi_program=40,
            midi_channel=0,
            notes=[
                Note(pitch=60, start_time=0.0, duration=1.0, velocity=90),
                Note(pitch=62, start_time=1.0, duration=1.0, velocity=85),
            ]
        )
        assert len(part.notes) == 2
        assert part.get_duration() == 2.0

    def test_notes_sorted_validation(self):
        """Test that notes must be sorted by start time."""
        with pytest.raises(ValueError):
            InstrumentPart(
                instrument_name="Violin",
                instrument_family="strings",
                midi_program=40,
                midi_channel=0,
                notes=[
                    Note(pitch=62, start_time=1.0, duration=1.0, velocity=85),
                    Note(pitch=60, start_time=0.0, duration=1.0, velocity=90),
                ]
            )

class TestComposition:
    """Test Composition data model."""

    def test_composition_creation(self):
        """Test creating a valid composition."""
        composition = Composition(
            title="Test Piece",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            time_signature=TimeSignature(numerator=4, denominator=4),
            parts=[
                InstrumentPart(
                    instrument_name="Violin",
                    instrument_family="strings",
                    midi_program=40,
                    midi_channel=0,
                    notes=[
                        Note(pitch=60, start_time=0.0, duration=1.0, velocity=90),
                    ]
                )
            ]
        )
        assert composition.title == "Test Piece"
        assert composition.duration == 1.0
        assert composition.instrument_count == 1
```

#### MIDI Generation Tests

```python
from musicgen.midi import EnhancedMIDIGenerator
from musicgen.ai_models import Composition, InstrumentPart, Note, KeyswitchEvent
import mido

class TestMIDIGenerator:
    """Test MIDI file generation."""

    def test_simple_midi_generation(self, tmp_path):
        """Test generating a simple MIDI file."""
        composition = Composition(
            title="Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[
                InstrumentPart(
                    instrument_name="Violin",
                    instrument_family="strings",
                    midi_program=40,
                    midi_channel=0,
                    notes=[
                        Note(pitch=60, start_time=0.0, duration=1.0, velocity=90),
                        Note(pitch=64, start_time=1.0, duration=1.0, velocity=85),
                    ]
                )
            ]
        )

        generator = EnhancedMIDIGenerator()
        output_path = tmp_path / "test.mid"
        generator.generate(composition, output_path)

        assert output_path.exists()

        # Verify MIDI file
        mid = mido.MidiFile(str(output_path))
        assert len(mid.tracks) > 0

    def test_keyswitch_generation(self, tmp_path):
        """Test that keyswitches are generated correctly."""
        composition = Composition(
            title="Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[
                InstrumentPart(
                    instrument_name="Violin",
                    instrument_family="strings",
                    midi_program=40,
                    midi_channel=0,
                    keyswitches=[
                        KeyswitchEvent(
                            keyswitch=24,
                            time=0.0,
                            articulation=ArticulationType.LEGATO
                        )
                    ],
                    notes=[
                        Note(pitch=60, start_time=0.1, duration=1.0, velocity=90),
                    ]
                )
            ]
        )

        generator = EnhancedMIDIGenerator()
        output_path = tmp_path / "test.mid"
        generator.generate(composition, output_path)

        # Verify keyswitch in MIDI
        mid = mido.MidiFile(str(output_path))
        track = mid.tracks[1]  # First instrument track

        # Should have a note_on for the keyswitch
        keyswitch_found = False
        for msg in track:
            if msg.type == 'note_on' and msg.note == 24:
                keyswitch_found = True
                break

        assert keyswitch_found, "Keyswitch not found in MIDI output"

    def test_tempo_track(self, tmp_path):
        """Test that tempo is correctly set."""
        composition = Composition(
            title="Test",
            key_signature="C major",
            initial_tempo_bpm=100.0,
            parts=[]
        )

        generator = EnhancedMIDIGenerator()
        output_path = tmp_path / "test.mid"
        generator.generate(composition, output_path)

        mid = mido.MidiFile(str(output_path))
        meta_track = mid.tracks[0]

        # Find tempo message
        tempo_found = False
        for msg in meta_track:
            if msg.type == 'set_tempo':
                # Convert tempo back to BPM
                bpm = mido.tempo2bpm(msg.tempo)
                assert abs(bpm - 100.0) < 0.1
                tempo_found = True
                break

        assert tempo_found, "Tempo message not found"

    def test_time_signature(self, tmp_path):
        """Test that time signature is correctly set."""
        composition = Composition(
            title="Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            time_signature=TimeSignature(numerator=3, denominator=4),
            parts=[]
        )

        generator = EnhancedMIDIGenerator()
        output_path = tmp_path / "test.mid"
        generator.generate(composition, output_path)

        mid = mido.MidiFile(str(output_path))
        meta_track = mid.tracks[0]

        # Find time signature message
        ts_found = False
        for msg in meta_track:
            if msg.type == 'time_signature':
                assert msg.numerator == 3
                assert msg.denominator == 4
                ts_found = True
                break

        assert ts_found, "Time signature message not found"
```

#### Validation Tests

```python
from musicgen.validation import VoiceLeadingValidator, CompositionValidator

class TestVoiceLeadingValidation:
    """Test voice leading validation."""

    def test_parallel_fifths_detection(self):
        """Test that parallel fifths are detected."""
        part1 = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_program=40,
            midi_channel=0,
            notes=[
                Note(pitch=60, start_time=0.0, duration=1.0, velocity=90),
                Note(pitch=67, start_time=1.0, duration=1.0, velocity=90),  # Perfect fifth above
            ]
        )

        part2 = InstrumentPart(
            instrument_name="Cello",
            instrument_family="strings",
            midi_program=42,
            midi_channel=1,
            notes=[
                Note(pitch=53, start_time=0.0, duration=1.0, velocity=90),
                Note(pitch=60, start_time=1.0, duration=1.0, velocity=90),  # Perfect fifth above, parallel!
            ]
        )

        validator = VoiceLeadingValidator()
        errors = validator.validate_parallel_perfect_intervals([part1, part2])

        assert len(errors) > 0
        assert any("parallel fifth" in e.description.lower() for e in errors)

    def test_valid_voice_leading(self):
        """Test that valid voice leading passes."""
        part1 = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_program=40,
            midi_channel=0,
            notes=[
                Note(pitch=60, start_time=0.0, duration=1.0, velocity=90),
                Note(pitch=64, start_time=1.0, duration=1.0, velocity=90),  # Step up
            ]
        )

        part2 = InstrumentPart(
            instrument_name="Cello",
            instrument_family="strings",
            midi_program=42,
            midi_channel=1,
            notes=[
                Note(pitch=53, start_time=0.0, duration=1.0, velocity=90),
                Note(pitch=57, start_time=1.0, duration=1.0, velocity=90),  # Step up, not parallel
            ]
        )

        validator = VoiceLeadingValidator()
        errors = validator.validate_parallel_perfect_intervals([part1, part2])

        # Should have no parallel perfect interval errors
        parallel_errors = [e for e in errors if "parallel" in e.description.lower()]
        assert len(parallel_errors) == 0
```

### 2. Integration Tests

```python
class TestEndToEnd:
    """End-to-end integration tests."""

    def test_simple_composition_generation(self, tmp_path, mock_gemini):
        """Test generating a simple composition from prompt."""
        # Mock Gemini response
        mock_response = {
            "title": "Generated Piece",
            "key_signature": "C major",
            "initial_tempo_bpm": 120.0,
            "time_signature": {"numerator": 4, "denominator": 4},
            "parts": [
                {
                    "instrument_name": "Violin",
                    "instrument_family": "strings",
                    "midi_program": 40,
                    "midi_channel": 0,
                    "notes": [
                        {
                            "pitch": 60,
                            "start_time": 0.0,
                            "duration": 1.0,
                            "velocity": 90
                        },
                        {
                            "pitch": 62,
                            "start_time": 1.0,
                            "duration": 1.0,
                            "velocity": 85
                        }
                    ]
                }
            ]
        }
        mock_gemini.return_value = mock_response

        from musicgen.composer_v3 import AIComposerV3

        composer = AIComposerV3()
        response = composer.compose("A simple melody", validate=False)

        assert response.composition.title == "Generated Piece"
        assert response.composition.duration == 2.0
        assert response.composition.instrument_count == 1

    def test_composition_to_midi(self, tmp_path):
        """Test full pipeline: composition → MIDI."""
        composition = Composition(
            title="Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[
                InstrumentPart(
                    instrument_name="Violin",
                    instrument_family="strings",
                    midi_program=40,
                    midi_channel=0,
                    notes=[
                        Note(pitch=60, start_time=0.0, duration=1.0, velocity=90),
                        Note(pitch=62, start_time=1.0, duration=1.0, velocity=85),
                        Note(pitch=64, start_time=2.0, duration=2.0, velocity=80),
                    ]
                )
            ]
        )

        from musicgen.midi import EnhancedMIDIGenerator

        generator = EnhancedMIDIGenerator()
        midi_path = tmp_path / "output.mid"
        generator.generate(composition, midi_path)

        assert midi_path.exists()

        # Verify we can load it
        import pretty_midi
        midi = pretty_midi.PrettyMIDI(str(midi_path))
        assert len(midi.instruments) > 0
```

### 3. Property-Based Tests

```python
from hypothesis import given, strategies as st
import pytest

class TestPropertyBased:
    """Property-based tests using Hypothesis."""

    @given(
        pitch=st.integers(min_value=0, max_value=127),
        start_time=st.floats(min_value=0, max_value=300),
        duration=st.floats(min_value=0.01, max_value=10),
        velocity=st.integers(min_value=0, max_value=127)
    )
    def test_note_roundtrip(self, pitch, start_time, duration, velocity):
        """Test that notes maintain their properties through serialization."""
        note = Note(
            pitch=pitch,
            start_time=start_time,
            duration=duration,
            velocity=velocity
        )

        # Serialize and deserialize
        data = note.model_dump()
        note2 = Note(**data)

        assert note2.pitch == pitch
        assert note2.start_time == start_time
        assert note2.duration == duration
        assert note2.velocity == velocity

    @given(st.lists(st.integers(min_value=0, max_value=127), min_size=2, max_size=10))
    def test_pitch_intervals(self, pitches):
        """Test interval calculation properties."""
        # Test that interval calculation is commutative with sign
        for i in range(len(pitches) - 1):
            interval = pitches[i + 1] - pitches[i]
            assert -12 <= interval <= 12  # Reasonable interval range
```

---

## Test Configuration

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=src/musicgen
    --cov-report=html
    --cov-report=term-missing

markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow-running tests
    requires_sfz: Tests requiring SFZ libraries
    requires_api: Tests requiring Gemini API
```

### conftest.py

```python
import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def tmp_path():
    """Temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)

@pytest.fixture
def sample_instrument_definitions():
    """Sample instrument definitions for testing."""
    return {
        "instruments": {
            "violin": {
                "name": "Violin",
                "family": "strings",
                "midi_program": 40,
                "range": {"min": 55, "max": 123},
                "dynamic_ranges": {
                    "p": {"min": 55, "max": 96},
                    "f": {"min": 55, "max": 116}
                },
                "articulations": {
                    "legato": {"keyswitch": 24, "duration_mod": 1.0},
                    "staccato": {"keyswitch": 25, "duration_mod": 0.4}
                },
                "sfz_file": "test.sfz"
            }
        },
        "ensembles": {
            "string_quartet": {
                "name": "String Quartet",
                "instruments": ["violin", "violin", "viola", "cello"]
            }
        }
    }

@pytest.fixture
def mock_gemini(monkeypatch):
    """Mock Gemini API for testing."""
    class MockGemini:
        def generate_content(self, prompt, **kwargs):
            class MockResponse:
                def __init__(self):
                    import json
                    self.text = json.dumps({
                        "title": "Test Piece",
                        "key_signature": "C major",
                        "initial_tempo_bpm": 120.0,
                        "time_signature": {"numerator": 4, "denominator": 4},
                        "parts": []
                    })
            return MockResponse()

    monkeypatch.setattr("google.generativeai.GenerativeModel", lambda _: MockGemini())
    return MockGemini()
```

---

## Implementation Tasks

1. [ ] Create test directory structure
2. [ ] Write unit tests for all models
3. [ ] Write unit tests for MIDI generator
4. [ ] Write unit tests for validators
5. [ ] Write integration tests for end-to-end flow
6. [ ] Add property-based tests for critical functions
7. [ ] Configure pytest and coverage
8. [ ] Add CI/CD integration

## Success Criteria

- >80% code coverage
- All unit tests pass
- Integration tests demonstrate end-to-end functionality
- Property tests find no counterexamples

## Next Steps

- V3-11: Documentation and Examples
- V3-12: Performance Optimization
