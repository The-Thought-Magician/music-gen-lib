"""Pytest configuration and shared fixtures for musicgen tests."""

import pytest
import tempfile
import shutil
from pathlib import Path

from musicgen.core.note import Note, Rest, QUARTER, WHOLE, HALF, MF
from musicgen.core.chord import Chord, MAJOR, MINOR
from musicgen.theory.scales import Scale
from musicgen.theory.keys import Key
from musicgen.theory.progressions import Progression


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
