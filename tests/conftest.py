"""Pytest configuration and shared fixtures for musicgen tests."""

import shutil
import tempfile
from pathlib import Path
from typing import Any

import pytest

from musicgen.core.chord import MAJOR, Chord
from musicgen.core.note import QUARTER, Note
from musicgen.theory.keys import Key
from musicgen.theory.progressions import Progression
from musicgen.theory.scales import Scale


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
# NOTE: V3 modules have been removed. These fixtures are no longer available.
# ============================================================================


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
