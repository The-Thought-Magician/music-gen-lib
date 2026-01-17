"""Tests for Scale class."""

import pytest

from musicgen.theory.scales import Scale


class TestScaleCreation:
    """Test Scale class initialization."""

    def test_create_major_scale(self):
        scale = Scale("C", "major")
        assert scale.tonic == "C"
        assert scale.notes == ["C", "D", "E", "F", "G", "A", "B"]

    def test_create_minor_scale(self):
        scale = Scale("A", "natural_minor")
        assert scale.tonic == "A"
        assert "A" in scale.notes

    def test_invalid_scale_type_raises_error(self):
        with pytest.raises(ValueError):
            Scale("C", "invalid_scale")


class TestScaleDegrees:
    """Test getting scale degrees."""

    def test_get_degree_1(self):
        scale = Scale("C", "major")
        note = scale.get_degree(1)
        assert note.name == "C"
        assert note.octave == 4

    def test_get_degree_5(self):
        scale = Scale("C", "major")
        note = scale.get_degree(5)
        assert note.name == "G"

    def test_get_degree_wraps(self):
        scale = Scale("C", "major")
        note = scale.get_degree(8)
        assert note.name == "C"
        assert note.octave == 5


class TestScaleContains:
    """Test scale membership."""

    def test_contains_note_in_scale(self):
        scale = Scale("C", "major")
        assert scale.contains("C")
        assert scale.contains("G")

    def test_does_not_contain_note_outside_scale(self):
        scale = Scale("C", "major")
        assert not scale.contains("F#")
        assert not scale.contains("Bb")


class TestScaleTranspose:
    """Test scale transposition."""

    def test_transpose_up(self):
        c_major = Scale("C", "major")
        d_major = c_major.transpose(2)
        assert d_major.tonic == "D"
        assert d_major.notes == ["D", "E", "F#", "G", "A", "B", "C#"]

    def test_transpose_down(self):
        c_major = Scale("C", "major")
        g_major = c_major.transpose(-5)
        assert g_major.tonic == "G"


class TestScaleDiatonicChords:
    """Test diatonic chord generation."""

    def test_diatonic_chords_major(self):
        scale = Scale("C", "major")
        chords = scale.diatonic_chords()
        assert len(chords) == 7
        assert chords[0].quality == "major"
        assert chords[1].quality == "minor"

    def test_diatonic_chords_minor(self):
        scale = Scale("A", "natural_minor")
        chords = scale.diatonic_chords()
        assert len(chords) == 7
        assert chords[0].quality == "minor"


class TestScaleTypes:
    """Test various scale types."""

    def test_pentatonic_major(self):
        scale = Scale("C", "major_pentatonic")
        assert len(scale.notes) == 5
        assert "C" in scale.notes
        assert "G" in scale.notes

    def test_pentatonic_minor(self):
        scale = Scale("A", "minor_pentatonic")
        assert len(scale.notes) == 5

    def test_blues_scale(self):
        scale = Scale("C", "blues")
        assert len(scale.notes) == 6
