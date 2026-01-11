"""Tests for Note and Rest classes."""

import pytest
from musicgen.core.note import Note, Rest, QUARTER, HALF, EIGHTH, MF, F, PP, FF


class TestNoteCreation:
    """Test Note class initialization and basic properties."""

    def test_create_simple_note(self):
        note = Note("C", octave=4, duration=QUARTER, velocity=90)
        assert note.name == "C"
        assert note.octave == 4
        assert note.duration == QUARTER
        assert note.velocity == 90
        assert note.accidental == ""

    def test_create_note_with_accidental(self):
        note = Note("C", octave=4, accidental="#")
        assert note.name == "C"
        assert note.accidental == "#"

    def test_invalid_name_raises_error(self):
        with pytest.raises(ValueError):
            Note("H", octave=4)

    def test_invalid_octave_raises_error(self):
        with pytest.raises(ValueError):
            Note("C", octave=10)

    def test_invalid_velocity_raises_error(self):
        with pytest.raises(ValueError):
            Note("C", octave=4, velocity=-1)
        with pytest.raises(ValueError):
            Note("C", octave=4, velocity=128)


class TestNoteFromPitchString:
    """Test Note.from_pitch_string class method."""

    def test_simple_pitch(self):
        note = Note.from_pitch_string("C4")
        assert note.name == "C"
        assert note.octave == 4
        assert note.accidental == ""

    def test_sharp_pitch(self):
        note = Note.from_pitch_string("C#4")
        assert note.name == "C"
        assert note.octave == 4
        assert note.accidental == "#"

    def test_flat_pitch(self):
        note = Note.from_pitch_string("Bb3")
        assert note.name == "B"
        assert note.octave == 3
        assert note.accidental == "b"

    def test_invalid_pitch_raises_error(self):
        with pytest.raises(ValueError):
            Note.from_pitch_string("H4")


class TestNoteMIDI:
    """Test MIDI note number conversions."""

    def test_midi_number_c4(self):
        assert Note("C", octave=4).midi_number == 60

    def test_midi_number_a4(self):
        assert Note("A", octave=4).midi_number == 69

    def test_from_midi(self):
        note = Note.from_midi(60)
        assert note.name == "C"
        assert note.octave == 4

    def test_from_midi_with_sharp(self):
        note = Note.from_midi(61)
        assert note.octave == 4


class TestNoteFrequency:
    """Test frequency calculations."""

    def test_frequency_a4(self):
        assert abs(Note("A", octave=4).frequency - 440.0) < 0.01

    def test_frequency_c4(self):
        assert abs(Note("C", octave=4).frequency - 261.63) < 0.01


class TestNoteTranspose:
    """Test note transposition."""

    def test_transpose_up(self):
        note = Note("C", octave=4)
        transposed = note.transpose(2)
        assert transposed.name == "D"
        assert transposed.octave == 4

    def test_transpose_down(self):
        note = Note("C", octave=4)
        transposed = note.transpose(-2)
        assert transposed.name == "A"
        assert transposed.octave == 3

    def test_transpose_preserves_duration(self):
        note = Note("C", octave=4, duration=HALF)
        transposed = note.transpose(3)
        assert transposed.duration == HALF


class TestNoteString:
    """Test string representations."""

    def test_to_pitch_string(self):
        assert Note("C", octave=4).to_pitch_string() == "C4"
        assert Note("C", octave=4, accidental="#").to_pitch_string() == "C#4"

    def test_repr(self):
        note = Note("C", octave=4, duration=QUARTER)
        assert "C4" in repr(note)


class TestNoteEquality:
    """Test Note equality and hashing."""

    def test_same_notes_equal(self):
        note1 = Note("C", octave=4, duration=QUARTER, velocity=90)
        note2 = Note("C", octave=4, duration=QUARTER, velocity=90)
        assert note1 == note2

    def test_note_is_hashable(self):
        note = Note("C", octave=4)
        note_set = {note, Note("D", octave=4), Note("C", octave=4)}
        assert len(note_set) == 2  # C4 and D4


class TestRest:
    """Test Rest class."""

    def test_create_rest(self):
        rest = Rest(QUARTER)
        assert rest.duration == QUARTER

    def test_rest_equality(self):
        rest1 = Rest(QUARTER)
        rest2 = Rest(QUARTER)
        assert rest1 == rest2


class TestDurationConstants:
    """Test duration constant values."""

    def test_whole_note(self):
        from musicgen.core.note import WHOLE
        assert WHOLE == 4.0

    def test_half_note(self):
        from musicgen.core.note import HALF
        assert HALF == 2.0

    def test_quarter_note(self):
        from musicgen.core.note import QUARTER
        assert QUARTER == 1.0


class TestDynamicConstants:
    """Test dynamic constant values."""

    def test_pp(self):
        assert PP == 30

    def test_mf(self):
        assert MF == 90

    def test_ff(self):
        assert FF == 120
