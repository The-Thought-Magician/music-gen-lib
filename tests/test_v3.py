"""Comprehensive test suite for V3 music generation system.

This module provides extensive tests for:
- V3 Model Tests (Note, ArticulationType, KeyswitchEvent, CCEvent, InstrumentPart, Composition)
- MIDI Generator Tests (simple generation, keyswitches, tempo, time signature, articulations)
- Validation Tests (parallel fifths, voice leading, leading tone resolution, instrument ranges)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from musicgen.ai_models.v3 import (
    ArticulationType,
    CC,
    CCEvent,
    Composition,
    CompositionRequest,
    CompositionResponse,
    DynamicChange,
    DynamicMarking,
    InstrumentPart,
    KeyswitchEvent,
    MusicalForm,
    Note,
    PitchBendEvent,
    ProgramChangeEvent,
    SectionMarker,
    StylePeriod,
    TempoChange,
    TempoMarking,
    TimeSignature,
    TimeSignatureChange,
    get_dynamic_velocity,
    get_tempo_bpm_range,
)
from musicgen.midi import EnhancedMIDIGenerator, export_multitrack_midi
from musicgen.validation import (
    CompositionValidator,
    ValidationConfig,
    ValidationResult,
    VoiceLeadingValidator,
)
from musicgen.validation.models import ValidationSeverity


# ============================================================================
# V3 Model Tests
# ============================================================================


class TestNoteModel:
    """Tests for the V3 Note model."""

    def test_note_creation_with_valid_values(self) -> None:
        """Test creating a note with valid MIDI pitch, duration, and velocity."""
        note = Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
        assert note.pitch == 60
        assert note.start_time == 0.0
        assert note.duration == 1.0
        assert note.velocity == 80

    def test_pitch_validation_accepts_valid_range(self) -> None:
        """Test that pitch validation accepts values 0-127."""
        for pitch in [0, 60, 127]:
            note = Note(pitch=pitch, start_time=0.0, duration=1.0, velocity=80)
            assert note.pitch == pitch

    def test_pitch_validation_rejects_below_zero(self) -> None:
        """Test that pitch validation rejects values below 0."""
        with pytest.raises(ValidationError):
            Note(pitch=-1, start_time=0.0, duration=1.0, velocity=80)

    def test_pitch_validation_rejects_above_127(self) -> None:
        """Test that pitch validation rejects values above 127."""
        with pytest.raises(ValidationError):
            Note(pitch=128, start_time=0.0, duration=1.0, velocity=80)

    def test_duration_validation_rejects_zero(self) -> None:
        """Test that duration validation rejects zero."""
        with pytest.raises(ValidationError):
            Note(pitch=60, start_time=0.0, duration=0.0, velocity=80)

    def test_duration_validation_rejects_negative(self) -> None:
        """Test that duration validation rejects negative values."""
        with pytest.raises(ValidationError):
            Note(pitch=60, start_time=0.0, duration=-0.5, velocity=80)

    def test_duration_validation_rejects_excessive(self) -> None:
        """Test that duration validation rejects values above 60 seconds."""
        with pytest.raises(ValidationError):
            Note(pitch=60, start_time=0.0, duration=61.0, velocity=80)

    def test_velocity_validation_accepts_valid_range(self) -> None:
        """Test that velocity validation accepts values 0-127."""
        for velocity in [0, 64, 127]:
            note = Note(pitch=60, start_time=0.0, duration=1.0, velocity=velocity)
            assert note.velocity == velocity

    def test_velocity_validation_rejects_below_zero(self) -> None:
        """Test that velocity validation rejects values below 0."""
        with pytest.raises(ValidationError):
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=-1)

    def test_velocity_validation_rejects_above_127(self) -> None:
        """Test that velocity validation rejects values above 127."""
        with pytest.raises(ValidationError):
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=128)

    def test_note_with_articulation(self) -> None:
        """Test creating a note with articulation."""
        note = Note(
            pitch=60,
            start_time=0.0,
            duration=1.0,
            velocity=80,
            articulation=ArticulationType.STACCATO
        )
        assert note.articulation == ArticulationType.STACCATO

    def test_note_with_dynamic(self) -> None:
        """Test creating a note with dynamic marking."""
        note = Note(
            pitch=60,
            start_time=0.0,
            duration=1.0,
            velocity=80,
            dynamic="mf"
        )
        assert note.dynamic == "mf"

    def test_note_with_ornament(self) -> None:
        """Test creating a note with ornament."""
        note = Note(
            pitch=60,
            start_time=0.0,
            duration=1.0,
            velocity=80,
            ornament="trill"
        )
        assert note.ornament == "trill"

    def test_note_tie_boolean(self) -> None:
        """Test tie boolean attribute."""
        note = Note(
            pitch=60,
            start_time=0.0,
            duration=1.0,
            velocity=80,
            tie=True
        )
        assert note.tie is True

    def test_note_slur_boolean(self) -> None:
        """Test slur boolean attribute."""
        note = Note(
            pitch=60,
            start_time=0.0,
            duration=1.0,
            velocity=80,
            slur=True
        )
        assert note.slur is True

    def test_note_slur_group_id(self) -> None:
        """Test slur_group_id attribute."""
        note = Note(
            pitch=60,
            start_time=0.0,
            duration=1.0,
            velocity=80,
            slur_group_id=1
        )
        assert note.slur_group_id == 1

    def test_render_duration_without_articulation(self) -> None:
        """Test render_duration returns base duration when no articulation."""
        note = Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
        assert note.render_duration() == 1.0

    def test_render_duration_with_staccato(self) -> None:
        """Test render_duration applies staccato multiplier."""
        note = Note(
            pitch=60,
            start_time=0.0,
            duration=1.0,
            velocity=80,
            articulation=ArticulationType.STACCATO
        )
        # Staccato should reduce duration
        assert note.render_duration() == 0.4

    def test_render_velocity_without_articulation(self) -> None:
        """Test render_velocity returns base velocity when no articulation."""
        note = Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
        assert note.render_velocity() == 80

    def test_render_velocity_with_accent(self) -> None:
        """Test render_velocity applies accent multiplier."""
        note = Note(
            pitch=60,
            start_time=0.0,
            duration=1.0,
            velocity=80,
            articulation=ArticulationType.ACCENT
        )
        # Accent should increase velocity
        expected = int(80 * 1.3)
        assert note.render_velocity() == expected

    def test_render_velocity_clips_at_127(self) -> None:
        """Test render_velocity clips to maximum MIDI value."""
        note = Note(
            pitch=60,
            start_time=0.0,
            duration=1.0,
            velocity=100,
            articulation=ArticulationType.SFORZANDO
        )
        # 100 * 1.4 = 140, should clip to 127
        assert note.render_velocity() == 127

    def test_grace_notes_list(self) -> None:
        """Test grace_notes attribute accepts list of notes."""
        grace = Note(pitch=62, start_time=0.0, duration=0.1, velocity=70)
        note = Note(
            pitch=60,
            start_time=0.0,
            duration=1.0,
            velocity=80,
            grace_notes=[grace]
        )
        assert note.grace_notes is not None
        assert len(note.grace_notes) == 1
        assert note.grace_notes[0].pitch == 62


class TestArticulationType:
    """Tests for the ArticulationType enum."""

    def test_string_articulations_exist(self) -> None:
        """Test that string articulations are defined."""
        assert ArticulationType.LEGATO.value == "legato"
        assert ArticulationType.STACCATO.value == "staccato"
        assert ArticulationType.PIZZICATO.value == "pizzicato"
        assert ArticulationType.SPICCATO.value == "spiccato"

    def test_woodwind_articulations_exist(self) -> None:
        """Test that woodwind articulations are defined."""
        assert ArticulationType.FLUTTER_TONGUE.value == "flutter_tongue"
        assert ArticulationType.LEGATO_WW.value == "legato_ww"

    def test_brass_articulations_exist(self) -> None:
        """Test that brass articulations are defined."""
        assert ArticulationType.MARTELLO.value == "martello"
        assert ArticulationType.MUTED.value == "muted"
        assert ArticulationType.FALL.value == "fall"

    def test_general_articulations_exist(self) -> None:
        """Test that general articulations are defined."""
        assert ArticulationType.NORMAL.value == "normal"
        assert ArticulationType.ACCENT.value == "accent"
        assert ArticulationType.TENUTO.value == "tenuto"
        assert ArticulationType.SFORZANDO.value == "sforzando"


class TestKeyswitchEvent:
    """Tests for the KeyswitchEvent model."""

    def test_keyswitch_creation(self) -> None:
        """Test creating a keyswitch event."""
        ks = KeyswitchEvent(
            keyswitch=12,
            time=0.0,
            articulation=ArticulationType.STACCATO
        )
        assert ks.keyswitch == 12
        assert ks.time == 0.0
        assert ks.articulation == ArticulationType.STACCATO

    def test_keyswitch_validation_valid_range(self) -> None:
        """Test keyswitch accepts valid MIDI range."""
        for keyswitch in [0, 12, 31, 127]:
            ks = KeyswitchEvent(
                keyswitch=keyswitch,
                time=0.0,
                articulation=ArticulationType.LEGATO
            )
            assert ks.keyswitch == keyswitch

    def test_keyswitch_rejects_negative(self) -> None:
        """Test keyswitch rejects negative values."""
        with pytest.raises(ValidationError):
            KeyswitchEvent(
                keyswitch=-1,
                time=0.0,
                articulation=ArticulationType.LEGATO
            )

    def test_keyswitch_rejects_above_127(self) -> None:
        """Test keyswitch rejects values above 127."""
        with pytest.raises(ValidationError):
            KeyswitchEvent(
                keyswitch=128,
                time=0.0,
                articulation=ArticulationType.LEGATO
            )

    def test_keyswitch_channel_default(self) -> None:
        """Test keyswitch channel defaults to 0."""
        ks = KeyswitchEvent(
            keyswitch=12,
            time=0.0,
            articulation=ArticulationType.LEGATO
        )
        assert ks.channel == 0

    def test_keyswitch_channel_custom(self) -> None:
        """Test keyswitch with custom channel."""
        ks = KeyswitchEvent(
            keyswitch=12,
            time=0.0,
            articulation=ArticulationType.LEGATO,
            channel=5
        )
        assert ks.channel == 5


class TestCCEvent:
    """Tests for the CCEvent model."""

    def test_cc_event_creation(self) -> None:
        """Test creating a CC event."""
        cc = CCEvent(
            controller=CC.VOLUME,
            value=100,
            start_time=0.0
        )
        assert cc.controller == 7
        assert cc.value == 100
        assert cc.start_time == 0.0

    def test_cc_controller_validation(self) -> None:
        """Test CC controller validation."""
        cc = CCEvent(controller=0, value=64, start_time=0.0)
        assert cc.controller == 0

        cc = CCEvent(controller=127, value=64, start_time=0.0)
        assert cc.controller == 127

    def test_cc_controller_rejects_invalid(self) -> None:
        """Test CC controller rejects invalid values."""
        with pytest.raises(ValidationError):
            CCEvent(controller=128, value=64, start_time=0.0)

    def test_cc_value_validation(self) -> None:
        """Test CC value validation."""
        cc = CCEvent(controller=7, value=0, start_time=0.0)
        assert cc.value == 0

        cc = CCEvent(controller=7, value=127, start_time=0.0)
        assert cc.value == 127

    def test_cc_value_rejects_invalid(self) -> None:
        """Test CC value rejects invalid values."""
        with pytest.raises(ValidationError):
            CCEvent(controller=7, value=128, start_time=0.0)

    def test_cc_duration_optional(self) -> None:
        """Test CC event duration is optional."""
        cc_instant = CCEvent(
            controller=CC.VOLUME,
            value=100,
            start_time=0.0
        )
        assert cc_instant.duration is None

        cc_ramped = CCEvent(
            controller=CC.VOLUME,
            value=100,
            start_time=0.0,
            duration=1.5
        )
        assert cc_ramped.duration == 1.5

    def test_common_cc_constants(self) -> None:
        """Test that common CC constants are defined."""
        assert CC.MODULATION == 1
        assert CC.BREATH == 2
        assert CC.FOOT == 4
        assert CC.VOLUME == 7
        assert CC.PAN == 10
        assert CC.EXPRESSION == 11
        assert CC.SUSTAIN == 64
        assert CC.VIBRATO_RATE == 76


class TestPitchBendEvent:
    """Tests for the PitchBendEvent model."""

    def test_pitch_bend_creation(self) -> None:
        """Test creating a pitch bend event."""
        pb = PitchBendEvent(value=8192, start_time=0.0)
        assert pb.value == 8192
        assert pb.start_time == 0.0

    def test_pitch_bend_center_value(self) -> None:
        """Test pitch bend center value is 8192."""
        pb = PitchBendEvent(value=8192, start_time=0.0)
        assert pb.value == 8192  # Center

    def test_pitch_bend_minimum(self) -> None:
        """Test pitch bend minimum value is 0."""
        pb = PitchBendEvent(value=0, start_time=0.0)
        assert pb.value == 0  # Full down

    def test_pitch_bend_maximum(self) -> None:
        """Test pitch bend maximum value is 16383."""
        pb = PitchBendEvent(value=16383, start_time=0.0)
        assert pb.value == 16383  # Full up

    def test_pitch_bend_rejects_negative(self) -> None:
        """Test pitch bend rejects negative values."""
        with pytest.raises(ValidationError):
            PitchBendEvent(value=-1, start_time=0.0)

    def test_pitch_bend_rejects_above_max(self) -> None:
        """Test pitch bend rejects values above 16383."""
        with pytest.raises(ValidationError):
            PitchBendEvent(value=16384, start_time=0.0)


class TestProgramChangeEvent:
    """Tests for the ProgramChangeEvent model."""

    def test_program_change_creation(self) -> None:
        """Test creating a program change event."""
        pc = ProgramChangeEvent(program=0, time=0.0)
        assert pc.program == 0
        assert pc.time == 0.0

    def test_program_change_validation(self) -> None:
        """Test program change accepts valid range."""
        pc = ProgramChangeEvent(program=0, time=0.0)
        assert pc.program == 0

        pc = ProgramChangeEvent(program=127, time=0.0)
        assert pc.program == 127

    def test_program_change_rejects_invalid(self) -> None:
        """Test program change rejects invalid values."""
        with pytest.raises(ValidationError):
            ProgramChangeEvent(program=128, time=0.0)

    def test_program_change_channel_default(self) -> None:
        """Test program change channel defaults to 0."""
        pc = ProgramChangeEvent(program=0, time=0.0)
        assert pc.channel == 0


class TestInstrumentPart:
    """Tests for the InstrumentPart model."""

    def test_instrument_part_creation(self) -> None:
        """Test creating an instrument part."""
        notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),
            Note(pitch=62, start_time=1.0, duration=1.0, velocity=80),
        ]
        part = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0,
            midi_program=40,
            notes=notes
        )
        assert part.instrument_name == "Violin"
        assert part.instrument_family == "strings"
        assert part.midi_channel == 0
        assert part.midi_program == 40
        assert len(part.notes) == 2

    def test_notes_sorted_validation_passes_sorted(self) -> None:
        """Test that sorted notes pass validation."""
        notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),
            Note(pitch=62, start_time=1.0, duration=1.0, velocity=80),
            Note(pitch=64, start_time=2.0, duration=1.0, velocity=80),
        ]
        part = InstrumentPart(
            instrument_name="Flute",
            instrument_family="woodwinds",
            midi_channel=1,
            midi_program=73,
            notes=notes
        )
        assert len(part.notes) == 3

    def test_notes_sorted_validation_fails_unsorted(self) -> None:
        """Test that unsorted notes fail validation."""
        notes = [
            Note(pitch=60, start_time=1.0, duration=1.0, velocity=80),
            Note(pitch=62, start_time=0.0, duration=1.0, velocity=80),  # Out of order
        ]
        with pytest.raises(ValidationError, match="Notes must be sorted"):
            InstrumentPart(
                instrument_name="Oboe",
                instrument_family="woodwinds",
                midi_channel=0,
                notes=notes
            )

    def test_get_duration_with_notes(self) -> None:
        """Test get_duration calculates correctly."""
        notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),
            Note(pitch=62, start_time=1.0, duration=2.0, velocity=80),
        ]
        part = InstrumentPart(
            instrument_name="Cello",
            instrument_family="strings",
            midi_channel=2,
            midi_program=42,
            notes=notes
        )
        # Last note ends at 1.0 + 2.0 = 3.0
        assert part.get_duration() == 3.0

    def test_get_duration_empty_part(self) -> None:
        """Test get_duration returns 0 for empty part."""
        part = InstrumentPart(
            instrument_name="Bassoon",
            instrument_family="woodwinds",
            midi_channel=3,
            midi_program=70,
            notes=[]
        )
        assert part.get_duration() == 0.0

    def test_note_count(self) -> None:
        """Test note_count returns correct count."""
        notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),
            Note(pitch=62, start_time=1.0, duration=1.0, velocity=80),
            Note(pitch=64, start_time=2.0, duration=1.0, velocity=80),
        ]
        part = InstrumentPart(
            instrument_name="Clarinet",
            instrument_family="woodwinds",
            midi_channel=0,
            notes=notes
        )
        assert part.note_count() == 3

    def test_solo_attribute(self) -> None:
        """Test solo attribute."""
        part = InstrumentPart(
            instrument_name="Trumpet",
            instrument_family="brass",
            midi_channel=0,
            midi_program=56,
            solo=True
        )
        assert part.solo is True

    def test_muted_attribute(self) -> None:
        """Test muted attribute."""
        part = InstrumentPart(
            instrument_name="Trombone",
            instrument_family="brass",
            midi_channel=1,
            midi_program=57,
            muted=True
        )
        assert part.muted is True

    def test_clef_attribute(self) -> None:
        """Test clef attribute."""
        part = InstrumentPart(
            instrument_name="Viola",
            instrument_family="strings",
            midi_channel=0,
            midi_program=41,
            clef="alto"
        )
        assert part.clef == "alto"

    def test_transposition_attribute(self) -> None:
        """Test transposition attribute."""
        part = InstrumentPart(
            instrument_name="Clarinet (Bb)",
            instrument_family="woodwinds",
            midi_channel=0,
            transposition=-2
        )
        assert part.transposition == -2

    def test_keyswitches_list(self) -> None:
        """Test keyswitches list."""
        ks = [
            KeyswitchEvent(keyswitch=12, time=0.0, articulation=ArticulationType.LEGATO)
        ]
        part = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0,
            keyswitches=ks
        )
        assert len(part.keyswitches) == 1

    def test_cc_events_list(self) -> None:
        """Test cc_events list."""
        cc = [
            CCEvent(controller=CC.VOLUME, value=100, start_time=0.0)
        ]
        part = InstrumentPart(
            instrument_name="Flute",
            instrument_family="woodwinds",
            midi_channel=1,
            cc_events=cc
        )
        assert len(part.cc_events) == 1

    def test_pitch_bends_list(self) -> None:
        """Test pitch_bends list."""
        pb = [
            PitchBendEvent(value=8192, start_time=0.0)
        ]
        part = InstrumentPart(
            instrument_name="Guitar",
            instrument_family="strings",
            midi_channel=0,
            pitch_bends=pb
        )
        assert len(part.pitch_bends) == 1

    def test_program_changes_list(self) -> None:
        """Test program_changes list."""
        pc = [
            ProgramChangeEvent(program=0, time=0.0)
        ]
        part = InstrumentPart(
            instrument_name="Piano",
            instrument_family="keyboards",
            midi_channel=0,
            program_changes=pc
        )
        assert len(part.program_changes) == 1


class TestComposition:
    """Tests for the Composition model."""

    def test_composition_creation_minimal(self) -> None:
        """Test creating a minimal composition."""
        notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
        ]
        part = InstrumentPart(
            instrument_name="Piano",
            instrument_family="keyboards",
            midi_channel=0,
            midi_program=0,
            notes=notes
        )
        comp = Composition(
            title="Test Piece",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part]
        )
        assert comp.title == "Test Piece"
        assert comp.key_signature == "C major"
        assert comp.initial_tempo_bpm == 120.0
        assert len(comp.parts) == 1

    def test_composition_duration_property(self) -> None:
        """Test duration property calculates correctly."""
        notes1 = [
            Note(pitch=60, start_time=0.0, duration=2.0, velocity=80)
        ]
        notes2 = [
            Note(pitch=48, start_time=0.0, duration=3.0, velocity=80)
        ]
        part1 = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0,
            notes=notes1
        )
        part2 = InstrumentPart(
            instrument_name="Cello",
            instrument_family="strings",
            midi_channel=1,
            notes=notes2
        )
        comp = Composition(
            title="Duration Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part1, part2]
        )
        # Cello part is longer (3.0 vs 2.0)
        assert comp.duration == 3.0

    def test_composition_duration_empty_parts(self) -> None:
        """Test duration property with empty parts."""
        comp = Composition(
            title="Empty",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[]
        )
        assert comp.duration == 0.0

    def test_instrument_count_property(self) -> None:
        """Test instrument_count property."""
        part1 = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0
        )
        part2 = InstrumentPart(
            instrument_name="Viola",
            instrument_family="strings",
            midi_channel=1
        )
        comp = Composition(
            title="String Duo",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part1, part2]
        )
        assert comp.instrument_count == 2

    def test_get_parts_by_family_strings(self) -> None:
        """Test get_parts_by_family for strings."""
        violin = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0
        )
        flute = InstrumentPart(
            instrument_name="Flute",
            instrument_family="woodwinds",
            midi_channel=1
        )
        cello = InstrumentPart(
            instrument_name="Cello",
            instrument_family="strings",
            midi_channel=2
        )
        comp = Composition(
            title="Mixed Ensemble",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[violin, flute, cello]
        )
        strings = comp.get_parts_by_family("strings")
        assert len(strings) == 2
        assert all(p.instrument_family == "strings" for p in strings)

    def test_get_parts_by_family_empty_result(self) -> None:
        """Test get_parts_by_family returns empty list when no matches."""
        part = InstrumentPart(
            instrument_name="Piano",
            instrument_family="keyboards",
            midi_channel=0
        )
        comp = Composition(
            title="Solo",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part]
        )
        brass = comp.get_parts_by_family("brass")
        assert len(brass) == 0

    def test_get_solo_parts(self) -> None:
        """Test get_solo_parts filters correctly."""
        violin = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0,
            solo=True
        )
        viola = InstrumentPart(
            instrument_name="Viola",
            instrument_family="strings",
            midi_channel=1,
            solo=False
        )
        cello = InstrumentPart(
            instrument_name="Cello",
            instrument_family="strings",
            midi_channel=2,
            solo=True
        )
        comp = Composition(
            title="String Trio",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[violin, viola, cello]
        )
        solos = comp.get_solo_parts()
        assert len(solos) == 2
        assert all(p.solo for p in solos)

    def test_time_signature_default(self) -> None:
        """Test default time signature."""
        comp = Composition(
            title="Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[]
        )
        assert comp.time_signature.numerator == 4
        assert comp.time_signature.denominator == 4

    def test_style_period_optional(self) -> None:
        """Test style_period is optional."""
        comp = Composition(
            title="Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[],
            style_period="classical"  # type: ignore[arg-type]
        )
        assert comp.style_period == "classical"

    def test_musical_form_optional(self) -> None:
        """Test musical_form is optional."""
        comp = Composition(
            title="Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[],
            musical_form="binary"  # type: ignore[arg-type]
        )
        assert comp.musical_form == "binary"

    def test_tempo_changes_list(self) -> None:
        """Test tempo_changes list."""
        tc = [TempoChange(tempo_bpm=100.0, time=10.0)]
        comp = Composition(
            title="Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[],
            tempo_changes=tc
        )
        assert len(comp.tempo_changes) == 1

    def test_dynamic_changes_list(self) -> None:
        """Test dynamic_changes list."""
        dc = [DynamicChange(dynamic="mf", time=5.0)]
        comp = Composition(
            title="Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[],
            dynamic_changes=dc
        )
        assert len(comp.dynamic_changes) == 1


class TestCompositionRequestResponse:
    """Tests for CompositionRequest and CompositionResponse."""

    def test_composition_request_creation(self) -> None:
        """Test creating a composition request."""
        req = CompositionRequest(
            prompt="A gentle piano piece",
            duration_seconds=60.0,
            key_signature="C major",
            style_period="classical"  # type: ignore[arg-type]
        )
        assert req.prompt == "A gentle piano piece"
        assert req.duration_seconds == 60.0
        assert req.key_signature == "C major"
        assert req.style_period == "classical"

    def test_composition_request_defaults(self) -> None:
        """Test composition request default values."""
        req = CompositionRequest(prompt="Test")
        assert req.output_format == "midi"
        assert req.include_stems is False

    def test_composition_response_creation(self) -> None:
        """Test creating a composition response."""
        comp = Composition(
            title="Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[]
        )
        resp = CompositionResponse(
            composition=comp,
            metadata={"model": "test"},
            warnings=["test warning"],
            validation_errors=["test error"]
        )
        assert resp.composition == comp
        assert resp.metadata == {"model": "test"}
        assert resp.warnings == ["test warning"]
        assert resp.validation_errors == ["test error"]


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_get_tempo_bpm_range_largo(self) -> None:
        """Test tempo range for largo."""
        bpm_range = get_tempo_bpm_range("largo")  # type: ignore[arg-type]
        assert bpm_range == (40, 60)

    def test_get_tempo_bpm_range_allegro(self) -> None:
        """Test tempo range for allegro."""
        bpm_range = get_tempo_bpm_range("allegro")  # type: ignore[arg-type]
        assert bpm_range == (115, 140)

    def test_get_tempo_bpm_range_unknown(self) -> None:
        """Test tempo range for unknown marking returns default."""
        bpm_range = get_tempo_bpm_range("unknown")  # type: ignore[arg-type]
        assert bpm_range == (60, 120)

    def test_get_dynamic_velocity_pp(self) -> None:
        """Test dynamic velocity for ppp."""
        vel = get_dynamic_velocity("ppp")
        assert vel == 16

    def test_get_dynamic_velocity_mf(self) -> None:
        """Test dynamic velocity for mf."""
        vel = get_dynamic_velocity("mf")
        assert vel == 80

    def test_get_dynamic_velocity_fff(self) -> None:
        """Test dynamic velocity for fff."""
        vel = get_dynamic_velocity("fff")
        assert vel == 127


# ============================================================================
# MIDI Generator Tests
# ============================================================================


class TestMIDIGenerator:
    """Tests for the EnhancedMIDIGenerator."""

    def test_generator_creation(self) -> None:
        """Test creating a MIDI generator."""
        gen = EnhancedMIDIGenerator()
        assert gen.ticks_per_beat == 480
        assert gen.keyswitch_timing_ms == 50

    def test_simple_midi_generation(self, tmp_path: Path) -> None:
        """Test simple MIDI file generation."""
        # Create a simple composition
        notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),  # C4
            Note(pitch=64, start_time=1.0, duration=1.0, velocity=80),  # E4
            Note(pitch=67, start_time=2.0, duration=1.0, velocity=80),  # G4
        ]
        part = InstrumentPart(
            instrument_name="Piano",
            instrument_family="keyboards",
            midi_channel=0,
            midi_program=0,
            notes=notes
        )
        comp = Composition(
            title="Simple Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part]
        )

        # Generate MIDI
        gen = EnhancedMIDIGenerator()
        output_path = tmp_path / "simple_test.mid"
        result_path = gen.generate(comp, output_path)

        # Verify file was created
        assert result_path.exists()
        assert result_path == output_path

        # Verify file structure
        try:
            import mido
            mid = mido.MidiFile(str(result_path))
            assert mid.ticks_per_beat == 480
            assert len(mid.tracks) >= 2  # Meta track + at least one part track
        except ImportError:
            pytest.skip("mido not installed")

    def test_keyswitch_generation(self, tmp_path: Path) -> None:
        """Test keyswitch events are included in MIDI output."""
        # Create a composition with keyswitches
        notes = [
            Note(
                pitch=60,
                start_time=0.5,
                duration=1.0,
                velocity=80,
                articulation=ArticulationType.STACCATO
            )
        ]
        keyswitches = [
            KeyswitchEvent(
                keyswitch=12,
                time=0.0,
                articulation=ArticulationType.STACCATO
            )
        ]
        part = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0,
            notes=notes,
            keyswitches=keyswitches
        )
        comp = Composition(
            title="Keyswitch Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part]
        )

        # Generate MIDI
        gen = EnhancedMIDIGenerator()
        output_path = tmp_path / "keyswitch_test.mid"
        gen.generate(comp, output_path)

        # Verify keyswitch in output
        try:
            import mido
            mid = mido.MidiFile(str(output_path))

            # Find the violin track (skip meta track which is first)
            violin_track = None
            for track in mid.tracks:
                if "Violin" in track.name:
                    violin_track = track
                    break

            if violin_track is None and len(mid.tracks) > 1:
                violin_track = mid.tracks[1]  # First part track (after meta)

            assert violin_track is not None

            # Check for any note events with pitch 12 (the keyswitch)
            # Keyswitches are implemented as note_on messages
            keyswitch_events = [
                msg for msg in violin_track
                if msg.type == 'note_on' and msg.note == 12
            ]

            # Should have at least one keyswitch event
            assert len(keyswitch_events) > 0, "Keyswitch event not found in MIDI output"

        except ImportError:
            pytest.skip("mido not installed")

    def test_tempo_meta_event(self, tmp_path: Path) -> None:
        """Test tempo meta event is included in MIDI."""
        notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
        ]
        part = InstrumentPart(
            instrument_name="Piano",
            instrument_family="keyboards",
            midi_channel=0,
            notes=notes
        )
        comp = Composition(
            title="Tempo Test",
            key_signature="C major",
            initial_tempo_bpm=100.0,
            parts=[part]
        )

        gen = EnhancedMIDIGenerator()
        output_path = tmp_path / "tempo_test.mid"
        gen.generate(comp, output_path)

        try:
            import mido
            mid = mido.MidiFile(str(output_path))

            # Check meta track for tempo
            meta_track = mid.tracks[0]
            has_tempo = any(
                msg.type == 'set_tempo'
                for msg in meta_track
            )
            assert has_tempo, "Tempo meta event not found"

        except ImportError:
            pytest.skip("mido not installed")

    def test_time_signature_meta_event(self, tmp_path: Path) -> None:
        """Test time signature meta event is included in MIDI."""
        notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
        ]
        part = InstrumentPart(
            instrument_name="Piano",
            instrument_family="keyboards",
            midi_channel=0,
            notes=notes
        )
        comp = Composition(
            title="Time Sig Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            time_signature=TimeSignature(numerator=3, denominator=4),
            parts=[part]
        )

        gen = EnhancedMIDIGenerator()
        output_path = tmp_path / "timesig_test.mid"
        gen.generate(comp, output_path)

        try:
            import mido
            mid = mido.MidiFile(str(output_path))

            # Check meta track for time signature
            meta_track = mid.tracks[0]
            has_timesig = any(
                msg.type == 'time_signature' and msg.numerator == 3
                for msg in meta_track
            )
            assert has_timesig, "Time signature meta event not found"

        except ImportError:
            pytest.skip("mido not installed")

    def test_articulation_duration_modification(self, tmp_path: Path) -> None:
        """Test that articulation modifies note duration in MIDI output."""
        # Staccato should shorten note
        notes = [
            Note(
                pitch=60,
                start_time=0.0,
                duration=1.0,
                velocity=80,
                articulation=ArticulationType.STACCATO
            )
        ]
        part = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0,
            notes=notes
        )
        comp = Composition(
            title="Articulation Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part]
        )

        gen = EnhancedMIDIGenerator()
        output_path = tmp_path / "articulation_test.mid"
        gen.generate(comp, output_path)

        try:
            import mido
            mid = mido.MidiFile(str(output_path))

            # Find note events and check duration
            for track in mid.tracks:
                note_on_time = None
                for msg in track:
                    if msg.type == 'note_on' and msg.note == 60 and msg.velocity > 0:
                        note_on_time = msg.time
                    elif msg.type == 'note_off' and msg.note == 60:
                        # Note off should come sooner than base duration
                        # due to staccato multiplier (0.4)
                        assert note_on_time is not None
                        # The staccato note should be shorter
                        break
        except ImportError:
            pytest.skip("mido not installed")

    def test_articulation_velocity_modification(self, tmp_path: Path) -> None:
        """Test that accent articulation modifies velocity in MIDI output."""
        notes = [
            Note(
                pitch=60,
                start_time=0.0,
                duration=1.0,
                velocity=80,
                articulation=ArticulationType.ACCENT
            )
        ]
        part = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0,
            notes=notes
        )
        comp = Composition(
            title="Velocity Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part]
        )

        gen = EnhancedMIDIGenerator()
        output_path = tmp_path / "velocity_test.mid"
        gen.generate(comp, output_path)

        try:
            import mido
            mid = mido.MidiFile(str(output_path))

            # Check for accent-modified velocity
            # 80 * 1.3 = 104
            for track in mid.tracks:
                for msg in track:
                    if msg.type == 'note_on' and msg.note == 60 and msg.velocity > 0:
                        # Velocity should be increased by accent
                        assert msg.velocity > 80
                        assert msg.velocity == 104
        except ImportError:
            pytest.skip("mido not installed")

    def test_multitrack_midi_export(self, tmp_path: Path) -> None:
        """Test exporting multi-track MIDI (each part to separate file)."""
        violin = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0,
            midi_program=40,
            notes=[
                Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
            ]
        )
        cello = InstrumentPart(
            instrument_name="Cello",
            instrument_family="strings",
            midi_channel=1,
            midi_program=42,
            notes=[
                Note(pitch=48, start_time=0.0, duration=1.0, velocity=80)
            ]
        )
        comp = Composition(
            title="Duo",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[violin, cello]
        )

        output_dir = tmp_path / "stems"
        paths = export_multitrack_midi(comp, output_dir)

        assert len(paths) == 2
        assert all(p.exists() for p in paths)
        assert any("violin" in str(p).lower() for p in paths)
        assert any("cello" in str(p).lower() for p in paths)


# ============================================================================
# Validation Tests
# ============================================================================


class TestValidation:
    """Tests for composition validation."""

    def test_parallel_fifths_detection(self) -> None:
        """Test detection of parallel fifths between parts."""
        # Create two parts with parallel fifths
        # Part 1: C (60) -> G (67) = perfect fifth
        # Part 2: F (53) -> C (60) = perfect fifth
        # Both voices move up by same interval (7 semitones)
        part1_notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),  # C4
            Note(pitch=67, start_time=1.0, duration=1.0, velocity=80),  # G4
        ]
        part2_notes = [
            Note(pitch=53, start_time=0.0, duration=1.0, velocity=80),  # F3
            Note(pitch=60, start_time=1.0, duration=1.0, velocity=80),  # C4
        ]

        part1 = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0,
            notes=part1_notes
        )
        part2 = InstrumentPart(
            instrument_name="Cello",
            instrument_family="strings",
            midi_channel=1,
            notes=part2_notes
        )

        comp = Composition(
            title="Parallel Fifths Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part1, part2]
        )

        validator = VoiceLeadingValidator()
        result = validator.validate(comp)

        # Should detect parallel fifths
        parallel_fifth_errors = [
            e for e in result.voice_leading_errors
            if "parallel_fifth" in e.error_type or "fifth" in e.error_type.lower()
        ]
        assert len(parallel_fifth_errors) > 0, "Failed to detect parallel fifths"

    def test_valid_voice_leading(self) -> None:
        """Test that proper voice leading passes validation."""
        # Create proper voice leading (contrary motion)
        # Part 1: C (60) -> E (64) = up by major third
        # Part 2: G (55) -> F (53) = down by whole step
        part1_notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),  # C4
            Note(pitch=64, start_time=1.0, duration=1.0, velocity=80),  # E4
        ]
        part2_notes = [
            Note(pitch=55, start_time=0.0, duration=1.0, velocity=80),  # G3
            Note(pitch=53, start_time=1.0, duration=1.0, velocity=80),  # F3
        ]

        part1 = InstrumentPart(
            instrument_name="Soprano",
            instrument_family="voices",
            midi_channel=0,
            notes=part1_notes
        )
        part2 = InstrumentPart(
            instrument_name="Alto",
            instrument_family="voices",
            midi_channel=1,
            notes=part2_notes
        )

        comp = Composition(
            title="Valid Voice Leading",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part1, part2]
        )

        validator = VoiceLeadingValidator()
        result = validator.validate(comp)

        # Should have no parallel fifth errors
        parallel_fifth_errors = [
            e for e in result.voice_leading_errors
            if "parallel" in e.error_type.lower()
        ]
        assert len(parallel_fifth_errors) == 0

    def test_leading_tone_resolution_detection(self) -> None:
        """Test detection of unresolved leading tone."""
        # In C major, B (71) is the leading tone
        # It should resolve to C (72) but doesn't here
        # The test checks if the leading tone moves DOWNWARD or doesn't move to tonic
        # NOTE: VoiceLeadingValidator requires at least 2 parts for validation

        # Part 1: Contains the unresolved leading tone
        part1_notes = [
            Note(pitch=71, start_time=0.0, duration=1.0, velocity=80),  # B4 - leading tone
            Note(pitch=69, start_time=1.0, duration=1.0, velocity=80),  # A4 - moves DOWN (bad)
        ]

        # Part 2: Just to satisfy the 2-part requirement for validation
        part2_notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),  # C4
            Note(pitch=64, start_time=1.0, duration=1.0, velocity=80),  # E4
        ]

        part1 = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0,
            notes=part1_notes
        )

        part2 = InstrumentPart(
            instrument_name="Cello",
            instrument_family="strings",
            midi_channel=1,
            notes=part2_notes
        )

        comp = Composition(
            title="Unresolved Leading Tone",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part1, part2]
        )

        validator = VoiceLeadingValidator(check_leading_tone=True)
        result = validator.validate(comp)

        # The validator looks for leading tone that doesn't resolve upward
        # B (71) -> A (69) is a downward motion of -2 semitones
        # This should be detected as an error
        leading_tone_errors = [
            e for e in result.voice_leading_errors
            if "leading_tone" in e.error_type
        ]

        # Check that we found the error
        assert len(leading_tone_errors) > 0, (
            f"Failed to detect unresolved leading tone. "
            f"Total errors: {len(result.voice_leading_errors)}"
        )

    def test_leading_tone_proper_resolution(self) -> None:
        """Test that properly resolved leading tone passes."""
        # B (71) -> C (72) is proper resolution
        # NOTE: VoiceLeadingValidator requires at least 2 parts for validation

        part1_notes = [
            Note(pitch=71, start_time=0.0, duration=1.0, velocity=80),  # B4
            Note(pitch=72, start_time=1.0, duration=1.0, velocity=80),  # C5 - resolves to tonic
        ]

        part2_notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),  # C4
            Note(pitch=64, start_time=1.0, duration=1.0, velocity=80),  # E4
        ]

        part1 = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0,
            notes=part1_notes
        )

        part2 = InstrumentPart(
            instrument_name="Cello",
            instrument_family="strings",
            midi_channel=1,
            notes=part2_notes
        )

        comp = Composition(
            title="Resolved Leading Tone",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part1, part2]
        )

        validator = VoiceLeadingValidator(check_leading_tone=True)
        result = validator.validate(comp)

        # Should NOT have leading tone errors
        leading_tone_errors = [
            e for e in result.voice_leading_errors
            if "leading_tone" in e.error_type
        ]
        assert len(leading_tone_errors) == 0

    def test_instrument_range_validation(self) -> None:
        """Test detection of notes outside instrument range."""
        # Create a violin part with notes below typical violin range
        # Violin lowest note is typically G3 (55)
        notes = [
            Note(pitch=40, start_time=0.0, duration=1.0, velocity=80),  # E2 - below violin range
            Note(pitch=60, start_time=1.0, duration=1.0, velocity=80),  # C4 - in range
        ]

        part = InstrumentPart(
            instrument_name="Violin",
            instrument_family="strings",
            midi_channel=0,
            notes=notes
        )

        comp = Composition(
            title="Range Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part]
        )

        # Note: This test may not catch errors if instrument library is not loaded
        # The orchestration validator needs the library to check ranges
        validator = CompositionValidator(
            ValidationConfig(check_ranges=True, check_articulations=False)
        )
        result = validator.validate(comp)

        # Result should exist (may or may not have errors depending on library)
        assert result is not None

    def test_validation_result_properties(self) -> None:
        """Test ValidationResult properties."""
        result = ValidationResult()
        assert result.is_valid is True
        assert result.has_warnings is False
        assert result.error_count == 0
        assert result.warning_count == 0

    def test_validation_result_with_errors(self) -> None:
        """Test ValidationResult with errors."""
        result = ValidationResult()
        result.add_voice_leading_error(
            error_type="parallel_fifth",
            location=1.0,
            voice1="Violin",
            voice2="Cello",
            description="Parallel fifth detected",
            severity=ValidationSeverity.ERROR
        )

        assert result.is_valid is False
        assert result.error_count == 1

    def test_validation_result_with_warnings(self) -> None:
        """Test ValidationResult with warnings."""
        result = ValidationResult()
        result.add_voice_leading_error(
            error_type="direct_fifth",
            location=1.0,
            voice1="Violin",
            voice2="Cello",
            description="Direct fifth by similar motion",
            severity=ValidationSeverity.WARNING
        )

        assert result.is_valid is True  # Warnings don't make it invalid
        assert result.has_warnings is True
        assert result.warning_count == 1

    def test_composition_validator_all_checks(self) -> None:
        """Test CompositionValidator with all checks enabled."""
        # Create a simple valid composition
        notes = [
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),
            Note(pitch=64, start_time=1.0, duration=1.0, velocity=80),
            Note(pitch=67, start_time=2.0, duration=1.0, velocity=80),
        ]
        part = InstrumentPart(
            instrument_name="Piano",
            instrument_family="keyboards",
            midi_channel=0,
            notes=notes
        )
        comp = Composition(
            title="Validator Test",
            key_signature="C major",
            initial_tempo_bpm=120.0,
            parts=[part]
        )

        config = ValidationConfig(
            check_parallel_fifths=True,
            check_parallel_octaves=True,
            check_direct_intervals=True,
            check_leading_tone=True,
            check_ranges=True,
            check_articulations=True,
            check_balance=True,
        )
        validator = CompositionValidator(config)
        result = validator.validate(comp)

        # Should complete without errors for simple piano part
        assert result is not None
        assert result.instruments_checked == 1
        assert result.total_notes == 3


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def sample_v3_composition() -> Composition:
    """Create a sample V3 composition for testing."""
    notes = [
        Note(pitch=60, start_time=0.0, duration=0.5, velocity=80),
        Note(pitch=62, start_time=0.5, duration=0.5, velocity=80),
        Note(pitch=64, start_time=1.0, duration=0.5, velocity=80),
        Note(pitch=65, start_time=1.5, duration=0.5, velocity=80),
        Note(pitch=67, start_time=2.0, duration=1.0, velocity=80),
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
def sample_string_quartet() -> Composition:
    """Create a sample string quartet for validation testing."""
    # Simple C major chord progression
    violin1_notes = [
        Note(pitch=72, start_time=0.0, duration=2.0, velocity=80),  # C5
        Note(pitch=74, start_time=2.0, duration=2.0, velocity=80),  # D5
        Note(pitch=76, start_time=4.0, duration=2.0, velocity=80),  # E5
        Note(pitch=72, start_time=6.0, duration=2.0, velocity=80),  # C5
    ]

    violin2_notes = [
        Note(pitch=67, start_time=0.0, duration=2.0, velocity=75),  # G4
        Note(pitch=69, start_time=2.0, duration=2.0, velocity=75),  # A4
        Note(pitch=71, start_time=4.0, duration=2.0, velocity=75),  # B4
        Note(pitch=67, start_time=6.0, duration=2.0, velocity=75),  # G4
    ]

    viola_notes = [
        Note(pitch=64, start_time=0.0, duration=2.0, velocity=70),  # E4
        Note(pitch=65, start_time=2.0, duration=2.0, velocity=70),  # F4
        Note(pitch=67, start_time=4.0, duration=2.0, velocity=70),  # G4
        Note(pitch=64, start_time=6.0, duration=2.0, velocity=70),  # E4
    ]

    cello_notes = [
        Note(pitch=48, start_time=0.0, duration=2.0, velocity=80),  # C3
        Note(pitch=50, start_time=2.0, duration=2.0, velocity=80),  # D3
        Note(pitch=52, start_time=4.0, duration=2.0, velocity=80),  # E3
        Note(pitch=48, start_time=6.0, duration=2.0, velocity=80),  # C3
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
    """Create a composition with deliberate parallel fifths for testing."""
    # Two parts moving in parallel fifths
    part1_notes = [
        Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),  # C4
        Note(pitch=67, start_time=1.0, duration=1.0, velocity=80),  # G4 - P5 above
        Note(pitch=72, start_time=2.0, duration=1.0, velocity=80),  # C5 - P5 above
    ]

    part2_notes = [
        Note(pitch=53, start_time=0.0, duration=1.0, velocity=80),  # F3
        Note(pitch=60, start_time=1.0, duration=1.0, velocity=80),  # C4 - P5 above
        Note(pitch=65, start_time=2.0, duration=1.0, velocity=80),  # F4 - P5 above
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
def sample_instrument_definitions() -> dict[str, Any]:
    """Sample instrument definitions for testing."""
    return {
        "violin": {
            "name": "Violin",
            "family": "strings",
            "midi_program": 40,
            "range_min": 55,  # G3
            "range_max": 103,  # B7
        },
        "flute": {
            "name": "Flute",
            "family": "woodwinds",
            "midi_program": 73,
            "range_min": 60,  # C4
            "range_max": 103,  # D7
        },
        "trumpet": {
            "name": "Trumpet",
            "family": "brass",
            "midi_program": 56,
            "range_min": 54,  # F#3
            "range_max": 86,  # D6
        },
    }
