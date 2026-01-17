"""Tests for Chord class."""

import pytest

from musicgen.core.chord import (
    AUGMENTED,
    DIMINISHED,
    DOMINANT_SEVENTH,
    MAJOR,
    MAJOR_SEVENTH,
    MINOR,
    MINOR_SEVENTH,
    Chord,
)
from musicgen.core.note import Note


class TestChordCreation:
    """Test Chord class initialization."""

    def test_create_major_triad(self):
        chord = Chord(_root_name="C", _quality=MAJOR)
        assert chord.root_name == "C"
        assert chord.quality == MAJOR
        assert len(chord.notes) == 3
        assert [n.name for n in chord.notes] == ["C", "E", "G"]

    def test_create_minor_triad(self):
        chord = Chord(_root_name="C", _quality=MINOR)
        assert chord.quality == MINOR
        # Check using to_pitch_string which includes accidental
        assert [n.to_pitch_string() for n in chord.notes] == ["C4", "D#4", "G4"]

    def test_create_diminished_triad(self):
        chord = Chord(_root_name="C", _quality=DIMINISHED)
        assert chord.quality == DIMINISHED

    def test_create_augmented_triad(self):
        chord = Chord(_root_name="C", _quality=AUGMENTED)
        assert chord.quality == AUGMENTED

    def test_invalid_quality_raises_error(self):
        with pytest.raises(ValueError):
            Chord(_root_name="C", _quality="invalid")


class TestChordInversions:
    """Test chord inversion functionality."""

    def test_root_position(self):
        chord = Chord(_root_name="C", _quality=MAJOR, _inversion=0)
        assert chord.inversion == 0

    def test_first_inversion(self):
        chord = Chord(_root_name="C", _quality=MAJOR, _inversion=1)
        assert chord.inversion == 1

    def test_invert_method(self):
        chord = Chord(_root_name="C", _quality=MAJOR)
        inverted = chord.invert(1)
        assert inverted.inversion == 1


class TestChordSevenths:
    """Test seventh chord creation."""

    def test_major_seventh(self):
        chord = Chord(_root_name="C", _quality=MAJOR_SEVENTH)
        assert len(chord.notes) == 4

    def test_dominant_seventh(self):
        chord = Chord(_root_name="C", _quality=DOMINANT_SEVENTH)
        assert len(chord.notes) == 4

    def test_minor_seventh(self):
        chord = Chord(_root_name="C", _quality=MINOR_SEVENTH)
        assert len(chord.notes) == 4


class TestChordTranspose:
    """Test chord transposition."""

    def test_transpose_up(self):
        chord = Chord(_root_name="C", _quality=MAJOR)
        transposed = chord.transpose(2)
        assert transposed.root_name == "D"

    def test_transpose_preserves_quality(self):
        chord = Chord(_root_name="C", _quality=MINOR)
        transposed = chord.transpose(4)
        assert transposed.quality == MINOR


class TestChordContains:
    """Test chord note membership."""

    def test_contains_root(self):
        chord = Chord(_root_name="C", _quality=MAJOR)
        assert chord.contains(Note("C", octave=4))

    def test_contains_third(self):
        chord = Chord(_root_name="C", _quality=MAJOR)
        assert chord.contains(Note("E", octave=4))

    def test_does_not_contain_non_chord_tone(self):
        chord = Chord(_root_name="C", _quality=MAJOR)
        assert not chord.contains(Note("D", octave=4))


class TestChordEquality:
    """Test Chord equality and hashing."""

    def test_same_chords_equal(self):
        chord1 = Chord(_root_name="C", _quality=MAJOR)
        chord2 = Chord(_root_name="C", _quality=MAJOR)
        assert chord1 == chord2

    def test_different_root_not_equal(self):
        chord1 = Chord(_root_name="C", _quality=MAJOR)
        chord2 = Chord(_root_name="D", _quality=MAJOR)
        assert chord1 != chord2


class TestChordFromNotes:
    """Test creating chords from note collections."""

    def test_from_notes_major(self):
        notes = [Note("C", octave=4), Note("E", octave=4), Note("G", octave=4)]
        chord = Chord.from_notes(notes)
        assert chord.root_name == "C"
        assert chord.quality == MAJOR
