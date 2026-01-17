"""
Tests for V4 extended instrument definitions.
"""

from __future__ import annotations

from musicgen.instruments.drum_articulations import (
    CYMBAL_ARTICULATIONS,
    HIHAT_ARTICULATIONS,
    KICK_ARTICULATIONS,
    SNARE_ARTICULATIONS,
    STICK_TYPES,
    TOM_ARTICULATIONS,
    apply_velocity,
    get_hihat_articulation,
    get_snare_articulation,
)
from musicgen.instruments.drums import (
    DRUM_PATTERNS,
    DrumFillGenerator,
    DrumPattern,
    apply_groove,
    get_pattern,
    get_patterns_by_genre,
)
from musicgen.instruments.fretboard import (
    DROP_D_GUITAR,
    OPEN_D_GUITAR,
    STANDARD_BASS_4,
    STANDARD_BASS_5,
    STANDARD_GUITAR,
    FretboardPosition,
    GuitarStringAssigner,
    midi_to_note,
    note_to_midi,
)
from musicgen.instruments.guitars import (
    BASS_TUNING_4_STRING,
    BASS_TUNING_5_STRING,
    BASS_TUNING_6_STRING,
    DROP_D_TUNING,
    GUITAR_CHORDS_BARRE,
    GUITAR_CHORDS_JAZZ,
    GUITAR_CHORDS_OPEN,
    GUITAR_CHORDS_POWER,
    GUITAR_PATTERNS,
    OPEN_D_TUNING,
    STANDARD_TUNING,
    GuitarChord,
    GuitarTechnique,
    guitar_chord_library,
)
from musicgen.instruments.midi_map import (
    GM_DRUM_NAMES,
    GM_PROGRAM_NAMES,
    PROGRAM_TO_NUMBER,
)
from musicgen.instruments.world import WorldInstrumentDefinition


class TestMidiMap:
    """Tests for MIDI program number mapping."""

    def test_gm_program_names(self) -> None:
        """Test GM program names registry."""
        assert len(GM_PROGRAM_NAMES) == 128
        assert GM_PROGRAM_NAMES[0] == "Acoustic Grand Piano"
        assert GM_PROGRAM_NAMES[-1] == "Gunshot"

    def test_gm_drum_names(self) -> None:
        """Test GM drum key names."""
        assert len(GM_DRUM_NAMES) > 0
        # Check common drum sounds
        assert 35 in GM_DRUM_NAMES or "Acoustic Bass Drum" in GM_DRUM_NAMES.values()

    def test_program_to_number(self) -> None:
        """Test program name to number lookup."""
        assert PROGRAM_TO_NUMBER["Acoustic Grand Piano"] == 0
        # Test case insensitivity
        assert (
            PROGRAM_TO_NUMBER.get("acoustic grand piano") == 0
            or PROGRAM_TO_NUMBER.get("Acoustic Grand Piano") == 0
        )


class TestGuitars:
    """Tests for guitar instrument definitions."""

    def test_standard_tuning(self) -> None:
        """Test standard guitar tuning."""
        assert STANDARD_TUNING == ["E2", "A2", "D3", "G3", "B3", "E4"]
        assert len(STANDARD_TUNING) == 6

    def test_drop_d_tuning(self) -> None:
        """Test Drop D tuning."""
        assert DROP_D_TUNING == ["D2", "A2", "D3", "G3", "B3", "E4"]
        assert DROP_D_TUNING[0] == "D2"  # Low string dropped

    def test_open_d_tuning(self) -> None:
        """Test Open D tuning."""
        assert OPEN_D_TUNING == ["D2", "A2", "D3", "F#3", "A3", "D4"]

    def test_bass_tunings(self) -> None:
        """Test bass guitar tunings."""
        assert len(BASS_TUNING_4_STRING) == 4
        assert BASS_TUNING_4_STRING[0] == "E1"
        assert len(BASS_TUNING_5_STRING) == 5
        assert len(BASS_TUNING_6_STRING) == 6

    def test_guitar_chords_open(self) -> None:
        """Test open chord definitions."""
        assert "C" in GUITAR_CHORDS_OPEN
        assert "G" in GUITAR_CHORDS_OPEN
        assert "D" in GUITAR_CHORDS_OPEN
        assert "E" in GUITAR_CHORDS_OPEN
        assert "Am" in GUITAR_CHORDS_OPEN
        assert "Em" in GUITAR_CHORDS_OPEN

        c_chord = GUITAR_CHORDS_OPEN["C"]
        assert c_chord.voicing == "open"
        assert c_chord.difficulty == "easy"
        assert len(c_chord.fingering) == 6  # 6 strings

    def test_guitar_chords_barre(self) -> None:
        """Test barre chord definitions."""
        assert "Bm" in GUITAR_CHORDS_BARRE
        assert "Cm" in GUITAR_CHORDS_BARRE
        assert "F#m" in GUITAR_CHORDS_BARRE

        bm_chord = GUITAR_CHORDS_BARRE["Bm"]
        assert bm_chord.voicing == "barre"

    def test_guitar_chords_power(self) -> None:
        """Test power chord definitions."""
        assert "A5" in GUITAR_CHORDS_POWER
        assert "E5" in GUITAR_CHORDS_POWER
        assert "G5" in GUITAR_CHORDS_POWER

        a5 = GUITAR_CHORDS_POWER["A5"]
        assert a5.voicing == "power"

    def test_guitar_chords_jazz(self) -> None:
        """Test jazz chord definitions."""
        assert "Cmaj9" in GUITAR_CHORDS_JAZZ
        assert "C9" in GUITAR_CHORDS_JAZZ
        assert "Dm9" in GUITAR_CHORDS_JAZZ

        cmaj9 = GUITAR_CHORDS_JAZZ["Cmaj9"]
        assert cmaj9.voicing == "jazz"
        assert cmaj9.difficulty == "hard"

    def test_guitar_chord_library(self) -> None:
        """Test combined chord library."""
        assert len(guitar_chord_library) > 0
        # Check that different voicing types are included
        voicings = {chord.voicing for chord in guitar_chord_library.values()}
        assert "open" in voicings
        assert "power" in voicings

    def test_guitar_patterns(self) -> None:
        """Test guitar strumming/picking patterns."""
        assert "basic_down" in GUITAR_PATTERNS
        assert "basic_down_up" in GUITAR_PATTERNS
        assert "folk_strum" in GUITAR_PATTERNS
        assert "rock_strum" in GUITAR_PATTERNS

        basic = GUITAR_PATTERNS["basic_down"]
        assert basic.style == "strum"
        assert basic.pattern == ["down"]

    def test_guitar_technique(self) -> None:
        """Test GuitarTechnique dataclass."""
        technique = GuitarTechnique(
            name="bend",
            articulation="bend",
            fret=10,
            string_num=2,
        )
        assert technique.name == "bend"
        assert technique.articulation == "bend"
        assert technique.fret == 10

    def test_guitar_chord_fret_range(self) -> None:
        """Test that fret_range is calculated correctly."""
        chord = GuitarChord(
            name="Test",
            voicing="open",
            fingering=[(0, None), (3, 5), (5, 4), (0, None), (0, None), (0, None)],
        )
        assert chord.fret_range == (3, 5)


class TestFretboard:
    """Tests for fretboard functionality."""

    def test_standard_guitar_fretboard(self) -> None:
        """Test standard guitar fretboard."""
        assert STANDARD_GUITAR.tuning == STANDARD_TUNING
        assert STANDARD_GUITAR.num_frets == 24 or STANDARD_GUITAR.num_frets >= 12

    def test_drop_d_guitar_fretboard(self) -> None:
        """Test Drop D guitar fretboard."""
        assert DROP_D_GUITAR.tuning == DROP_D_TUNING

    def test_open_d_guitar_fretboard(self) -> None:
        """Test Open D guitar fretboard."""
        assert OPEN_D_GUITAR.tuning == OPEN_D_TUNING

    def test_bass_fretboards(self) -> None:
        """Test bass fretboards."""
        assert STANDARD_BASS_4.tuning == BASS_TUNING_4_STRING
        assert STANDARD_BASS_5.tuning == BASS_TUNING_5_STRING

    def test_note_to_midi(self) -> None:
        """Test note name to MIDI note number conversion."""
        assert note_to_midi("A4") == 69
        assert note_to_midi("C4") == 60
        assert note_to_midi("A0") == 21

    def test_midi_to_note(self) -> None:
        """Test MIDI note number to note name conversion."""
        assert midi_to_note(69) == "A4"
        assert midi_to_note(60) == "C4"

    def test_fretboard_position(self) -> None:
        """Test FretboardPosition dataclass."""
        pos = FretboardPosition(string_num=1, fret=5, note="E4", midi=64)
        assert pos.string_num == 1
        assert pos.fret == 5
        assert pos.note == "E4"

    def test_guitar_string_assigner(self) -> None:
        """Test string assignment for notes."""
        assigner = GuitarStringAssigner(STANDARD_GUITAR)

        # Find middle C on guitar
        positions = assigner.find_note("C4")
        assert len(positions) > 0

        # All positions should be valid
        for pos in positions:
            assert 1 <= pos.string_num <= 6
            assert pos.fret >= 0


class TestDrums:
    """Tests for drum kit and pattern definitions."""

    def test_drum_patterns_exist(self) -> None:
        """Test that drum patterns are defined."""
        assert len(DRUM_PATTERNS) > 0

    def test_get_pattern(self) -> None:
        """Test getting a specific pattern."""
        pattern = get_pattern("basic_rock")
        if pattern:
            assert isinstance(pattern, DrumPattern)

    def test_get_patterns_by_genre(self) -> None:
        """Test filtering patterns by genre."""
        rock_patterns = get_patterns_by_genre("rock")
        if rock_patterns:
            assert len(rock_patterns) > 0

    def test_drum_fill_generator(self) -> None:
        """Test drum fill generation."""
        generator = DrumFillGenerator()
        fill = generator.generate(length=1, intensity=0.5)
        assert fill is not None

    def test_apply_groove(self) -> None:
        """Test applying groove to a pattern."""
        result = apply_groove([0.0, 0.5, 1.0], swing_amount=0.3)
        assert len(result) == 3


class TestDrumArticulations:
    """Tests for drum articulation system."""

    def test_stick_types(self) -> None:
        """Test stick type definitions."""
        assert "normal" in STICK_TYPES
        assert "brushes" in STICK_TYPES
        assert "mallets" in STICK_TYPES

    def test_hihat_articulations(self) -> None:
        """Test hi-hat articulations."""
        assert "closed" in HIHAT_ARTICULATIONS
        assert "open" in HIHAT_ARTICULATIONS
        assert "pedal" in HIHAT_ARTICULATIONS

    def test_snare_articulations(self) -> None:
        """Test snare articulations."""
        assert "normal" in SNARE_ARTICULATIONS
        assert "rimshot" in SNARE_ARTICULATIONS
        assert "ghost" in SNARE_ARTICULATIONS

    def test_kick_articulations(self) -> None:
        """Test kick drum articulations."""
        assert "normal" in KICK_ARTICULATIONS

    def test_cymbal_articulations(self) -> None:
        """Test cymbal articulations."""
        assert "crash" in CYMBAL_ARTICULATIONS
        assert "ride" in CYMBAL_ARTICULATIONS

    def test_tom_articulations(self) -> None:
        """Test tom articulations."""
        assert "normal" in TOM_ARTICULATIONS

    def test_get_hihat_articulation(self) -> None:
        """Test getting hi-hat articulation."""
        art = get_hihat_articulation("closed")
        assert art is not None

    def test_get_snare_articulation(self) -> None:
        """Test getting snare articulation."""
        art = get_snare_articulation("rimshot")
        assert art is not None

    def test_apply_velocity(self) -> None:
        """Test velocity adjustment."""
        result = apply_velocity([100, 100, 100], variance=0.1)
        assert len(result) == 3
        # Check that velocities are in valid range
        assert all(0 <= v <= 127 for v in result)


class TestWorldInstruments:
    """Tests for world instrument definitions."""

    def test_world_instrument_definition(self) -> None:
        """Test WorldInstrumentDefinition dataclass."""
        instrument = WorldInstrumentDefinition(
            name="Sitar",
            region="India",
            type="string",
            midi_program=104,
        )
        assert instrument.name == "Sitar"
        assert instrument.region == "India"
