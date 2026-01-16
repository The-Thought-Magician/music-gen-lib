"""Pytest configuration and shared fixtures for musicgen tests."""

import tempfile
import shutil
from pathlib import Path
from typing import Any

import pytest

from musicgen.core.note import Note as CoreNote, Rest, QUARTER, WHOLE, HALF, MF
from musicgen.core.chord import Chord, MAJOR, MINOR
from musicgen.theory.scales import Scale
from musicgen.theory.keys import Key
from musicgen.theory.progressions import Progression

# V3 imports
from musicgen.ai_models.v3 import (
    ArticulationType,
    CC,
    CCEvent,
    Composition,
    DynamicChange,
    InstrumentPart,
    KeyswitchEvent,
    Note as V3Note,
    PitchBendEvent,
    ProgramChangeEvent,
    TempoChange,
    TimeSignature,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def c_major_scale():
    """C major scale fixture."""
    return Scale("C", "major")


@pytest.fixture
def a_minor_scale():
    """A natural minor scale fixture."""
    return Scale("A", "natural_minor")


@pytest.fixture
def c_major_key():
    """C major key fixture."""
    return Key("C", "major")


@pytest.fixture
def sample_notes():
    """Sample notes for testing."""
    return [
        Note("C4", QUARTER),
        Note("D4", QUARTER),
        Note("E4", QUARTER),
        Note("F4", QUARTER),
        Note("G4", QUARTER),
        Note("A4", QUARTER),
        Note("B4", QUARTER),
        Note("C5", QUARTER),
    ]


@pytest.fixture
def sample_chord():
    """C major chord fixture."""
    return Chord(_root_name="C", _quality=MAJOR, root_octave=4)


@pytest.fixture
def sample_progression():
    """I-IV-V-I progression in C major."""
    return Progression.from_roman("I-IV-V-I", key="C")


@pytest.fixture
def output_path(temp_dir):
    """Path for output files in temp directory."""
    return temp_dir


# SoundFont fixture (skip if not available)
@pytest.fixture
def soundfont_path():
    """Path to test SoundFont file."""
    # Check for common SoundFont locations
    possible_paths = [
        Path("/usr/share/sounds/sf2/FluidR3_GM.sf2"),
        Path("/usr/share/soundfonts/FluidR3_GM.sf2"),
        Path("resources/soundfonts/GeneralUser GS.sf2"),
    ]
    for path in possible_paths:
        if path.exists():
            return str(path)
    # Return None if not found - tests should skip
    return None


# ============================================================================
# V3 Fixtures
# ============================================================================


@pytest.fixture
def sample_v3_composition() -> Composition:
    """Create a sample V3 composition for testing.

    Returns a simple piano piece with a C major scale melody.
    """
    notes = [
        V3Note(pitch=60, start_time=0.0, duration=0.5, velocity=80),
        V3Note(pitch=62, start_time=0.5, duration=0.5, velocity=80),
        V3Note(pitch=64, start_time=1.0, duration=0.5, velocity=80),
        V3Note(pitch=65, start_time=1.5, duration=0.5, velocity=80),
        V3Note(pitch=67, start_time=2.0, duration=1.0, velocity=80),
    ]

    part = InstrumentPart(
        instrument_name="Piano",
        instrument_family="keyboards",
        midi_channel=0,
        midi_program=0,
        notes=notes
    )

    return Composition(
        title="Sample Composition",
        key_signature="C major",
        initial_tempo_bpm=120.0,
        time_signature=TimeSignature(numerator=4, denominator=4),
        parts=[part]
    )


@pytest.fixture
def sample_v3_notes():
    """Sample V3 notes for testing."""
    return [
        V3Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),
        V3Note(pitch=62, start_time=1.0, duration=1.0, velocity=80),
        V3Note(pitch=64, start_time=2.0, duration=1.0, velocity=80),
        V3Note(pitch=65, start_time=3.0, duration=1.0, velocity=80),
        V3Note(pitch=67, start_time=4.0, duration=2.0, velocity=80),
    ]


@pytest.fixture
def sample_v3_instrument_part(sample_v3_notes):
    """Sample V3 instrument part for testing."""
    return InstrumentPart(
        instrument_name="Test Instrument",
        instrument_family="strings",
        midi_channel=0,
        midi_program=40,
        notes=sample_v3_notes
    )


@pytest.fixture
def sample_v3_part_with_keyswitches():
    """Sample V3 part with keyswitches for testing."""
    notes = [
        V3Note(
            pitch=60,
            start_time=0.5,
            duration=1.0,
            velocity=80,
            articulation=ArticulationType.STACCATO
        ),
    ]

    keyswitches = [
        KeyswitchEvent(
            keyswitch=12,
            time=0.0,
            articulation=ArticulationType.STACCATO
        )
    ]

    return InstrumentPart(
        instrument_name="Violin",
        instrument_family="strings",
        midi_channel=0,
        midi_program=40,
        notes=notes,
        keyswitches=keyswitches
    )


@pytest.fixture
def sample_v3_part_with_cc():
    """Sample V3 part with CC events for testing."""
    notes = [
        V3Note(pitch=60, start_time=0.0, duration=2.0, velocity=80),
    ]

    cc_events = [
        CCEvent(
            controller=CC.VOLUME,
            value=100,
            start_time=0.0
        ),
        CCEvent(
            controller=CC.EXPRESSION,
            value=64,
            start_time=1.0
        )
    ]

    return InstrumentPart(
        instrument_name="Flute",
        instrument_family="woodwinds",
        midi_channel=1,
        midi_program=73,
        notes=notes,
        cc_events=cc_events
    )


@pytest.fixture
def sample_v3_string_quartet() -> Composition:
    """Create a sample string quartet for validation testing.

    Returns a composition with 4 parts (Violin I, Violin II, Viola, Cello)
    playing a simple C major chord progression.
    """
    # Simple C major chord progression
    violin1_notes = [
        V3Note(pitch=72, start_time=0.0, duration=2.0, velocity=80),  # C5
        V3Note(pitch=74, start_time=2.0, duration=2.0, velocity=80),  # D5
        V3Note(pitch=76, start_time=4.0, duration=2.0, velocity=80),  # E5
        V3Note(pitch=72, start_time=6.0, duration=2.0, velocity=80),  # C5
    ]

    violin2_notes = [
        V3Note(pitch=67, start_time=0.0, duration=2.0, velocity=75),  # G4
        V3Note(pitch=69, start_time=2.0, duration=2.0, velocity=75),  # A4
        V3Note(pitch=71, start_time=4.0, duration=2.0, velocity=75),  # B4
        V3Note(pitch=67, start_time=6.0, duration=2.0, velocity=75),  # G4
    ]

    viola_notes = [
        V3Note(pitch=64, start_time=0.0, duration=2.0, velocity=70),  # E4
        V3Note(pitch=65, start_time=2.0, duration=2.0, velocity=70),  # F4
        V3Note(pitch=67, start_time=4.0, duration=2.0, velocity=70),  # G4
        V3Note(pitch=64, start_time=6.0, duration=2.0, velocity=70),  # E4
    ]

    cello_notes = [
        V3Note(pitch=48, start_time=0.0, duration=2.0, velocity=80),  # C3
        V3Note(pitch=50, start_time=2.0, duration=2.0, velocity=80),  # D3
        V3Note(pitch=52, start_time=4.0, duration=2.0, velocity=80),  # E3
        V3Note(pitch=48, start_time=6.0, duration=2.0, velocity=80),  # C3
    ]

    return Composition(
        title="String Quartet",
        key_signature="C major",
        initial_tempo_bpm=100.0,
        time_signature=TimeSignature(numerator=4, denominator=4),
        parts=[
            InstrumentPart(
                instrument_name="Violin I",
                instrument_family="strings",
                midi_channel=0,
                midi_program=40,
                notes=violin1_notes
            ),
            InstrumentPart(
                instrument_name="Violin II",
                instrument_family="strings",
                midi_channel=1,
                midi_program=40,
                notes=violin2_notes
            ),
            InstrumentPart(
                instrument_name="Viola",
                instrument_family="strings",
                midi_channel=2,
                midi_program=41,
                notes=viola_notes
            ),
            InstrumentPart(
                instrument_name="Cello",
                instrument_family="strings",
                midi_channel=3,
                midi_program=42,
                notes=cello_notes
            ),
        ]
    )


@pytest.fixture
def parallel_fifths_composition() -> Composition:
    """Create a composition with deliberate parallel fifths for testing.

    This fixture creates two parts that move in parallel perfect fifths,
    which is traditionally avoided in common practice voice leading.
    """
    part1_notes = [
        V3Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),  # C4
        V3Note(pitch=67, start_time=1.0, duration=1.0, velocity=80),  # G4 - P5 above
        V3Note(pitch=72, start_time=2.0, duration=1.0, velocity=80),  # C5 - P5 above
    ]

    part2_notes = [
        V3Note(pitch=53, start_time=0.0, duration=1.0, velocity=80),  # F3
        V3Note(pitch=60, start_time=1.0, duration=1.0, velocity=80),  # C4 - P5 above
        V3Note(pitch=65, start_time=2.0, duration=1.0, velocity=80),  # F4 - P5 above
    ]

    return Composition(
        title="Parallel Fifths Example",
        key_signature="C major",
        initial_tempo_bpm=120.0,
        parts=[
            InstrumentPart(
                instrument_name="Upper Voice",
                instrument_family="strings",
                midi_channel=0,
                notes=part1_notes
            ),
            InstrumentPart(
                instrument_name="Lower Voice",
                instrument_family="strings",
                midi_channel=1,
                notes=part2_notes
            ),
        ]
    )


@pytest.fixture
def unresolved_leading_tone_composition() -> Composition:
    """Create a composition with an unresolved leading tone for testing.

    In C major, B (71) is the leading tone and should resolve to C (72).
    This fixture has it resolving downward instead.

    NOTE: Requires 2 parts for voice leading validation.
    """
    # Part 1: Contains the unresolved leading tone
    part1_notes = [
        V3Note(pitch=71, start_time=0.0, duration=1.0, velocity=80),  # B4 - leading tone
        V3Note(pitch=69, start_time=1.0, duration=1.0, velocity=80),  # A4 - doesn't resolve to tonic
    ]

    # Part 2: Just to satisfy the 2-part requirement for validation
    part2_notes = [
        V3Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),  # C4
        V3Note(pitch=64, start_time=1.0, duration=1.0, velocity=80),  # E4
    ]

    return Composition(
        title="Unresolved Leading Tone",
        key_signature="C major",
        initial_tempo_bpm=120.0,
        parts=[
            InstrumentPart(
                instrument_name="Violin",
                instrument_family="strings",
                midi_channel=0,
                notes=part1_notes
            ),
            InstrumentPart(
                instrument_name="Cello",
                instrument_family="strings",
                midi_channel=1,
                notes=part2_notes
            ),
        ]
    )


@pytest.fixture
def sample_instrument_definitions() -> dict[str, Any]:
    """Sample instrument definitions for testing.

    Provides a dictionary of common instruments with their MIDI programs
    and typical ranges.
    """
    return {
        "violin": {
            "name": "Violin",
            "family": "strings",
            "midi_program": 40,
            "range_min": 55,  # G3
            "range_max": 103,  # B7
        },
        "viola": {
            "name": "Viola",
            "family": "strings",
            "midi_program": 41,
            "range_min": 48,  # C3
            "range_max": 88,  # E6
        },
        "cello": {
            "name": "Cello",
            "family": "strings",
            "midi_program": 42,
            "range_min": 36,  # C2
            "range_max": 76,  # E5
        },
        "flute": {
            "name": "Flute",
            "family": "woodwinds",
            "midi_program": 73,
            "range_min": 60,  # C4
            "range_max": 103,  # D7
        },
        "clarinet": {
            "name": "Clarinet",
            "family": "woodwinds",
            "midi_program": 71,
            "range_min": 50,  # D3
            "range_max": 98,  # Bb6
        },
        "trumpet": {
            "name": "Trumpet",
            "family": "brass",
            "midi_program": 56,
            "range_min": 54,  # F#3
            "range_max": 86,  # D6
        },
        "piano": {
            "name": "Piano",
            "family": "keyboards",
            "midi_program": 0,
            "range_min": 21,  # A0
            "range_max": 108,  # C8
        },
    }
