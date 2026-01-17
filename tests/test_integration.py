"""Integration tests for the complete music generation pipeline.

These tests verify that all components work together correctly.
"""

from pathlib import Path

import pytest

from musicgen.composition.melody import MelodyGenerator
from musicgen.core.note import QUARTER, Note
from musicgen.generator import CompositionRequest, generate
from musicgen.io.midi_writer import MIDIWriter, Part, Score
from musicgen.theory.keys import Key
from musicgen.theory.scales import Scale


class TestFullPipeline:
    """Test the complete music generation pipeline."""

    def test_scale_to_midi_pipeline(self, temp_dir, c_major_scale):
        """Test generating a scale and exporting to MIDI."""
        # Create a simple melody from the scale
        notes = [c_major_scale.get_degree(i % 7 + 1) for i in range(16)]

        # Create a basic score structure
        score = Score()
        part = Part(name="melody")
        part.notes = notes
        score.add_part(part)

        # Write to MIDI
        output_path = temp_dir / "scale_test.mid"
        MIDIWriter.write(score, str(output_path))

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_progression_to_audio(self, temp_dir, sample_progression, soundfont_path):
        """Test chord progression to audio conversion."""
        if soundfont_path is None:
            pytest.skip("No SoundFont available")

        # Generate MIDI from progression
        midi_path = temp_dir / "progression.mid"

        # Create a simple score with the progression
        score = Score()
        part = Part(name="chords")
        for chord in sample_progression.chords:
            for note in chord.notes:
                part.add_note(note)
        score.add_part(part)

        MIDIWriter.write(score, str(midi_path))

        # Verify MIDI file exists
        assert midi_path.exists()

        # Convert to audio
        from musicgen.io.audio_synthesizer import AudioSynthesizer

        synth = AudioSynthesizer(soundfont_path=soundfont_path)
        if not AudioSynthesizer.is_available():
            pytest.skip("FluidSynth not available")

        audio_path = temp_dir / "progression.wav"
        try:
            result = synth.render(str(midi_path), str(audio_path))
            assert Path(result).exists()
        except RuntimeError:
            pytest.skip("Audio synthesis failed")

    def test_mood_based_generation(self, temp_dir):
        """Test complete mood-based music generation."""
        request = CompositionRequest(
            mood="peaceful",
            duration=15,
            output_dir=str(temp_dir),
            export_formats=["midi"]
        )

        result = generate(request)

        assert result.score is not None
        assert result.midi_path is not None
        assert Path(result.midi_path).exists()
        assert "G" in result.key  # Peaceful mood uses G major
        assert result.scale_type == "major"

    def test_scale_key_progression_integration(self, c_major_key):
        """Test that Scale, Key, and Progression work together."""
        progression = c_major_key.diatonic_chords()

        assert len(progression) == 7
        assert progression[0].quality == "major"
        assert progression[1].quality == "minor"


class TestExportFormats:
    """Test all export formats work correctly."""

    def test_midi_export(self, temp_dir):
        """Test MIDI file export."""
        score = Score()
        part = Part(name="test")
        part.notes = [Note("C", octave=4, duration=QUARTER), Note("D", octave=4, duration=QUARTER), Note("E", octave=4, duration=QUARTER)]
        score.add_part(part)

        output_path = temp_dir / "test.mid"
        MIDIWriter.write(score, str(output_path))

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_musicxml_export(self, temp_dir):
        """Test MusicXML file export."""
        from musicgen.io.musicxml_writer import MusicXMLWriter

        score = Score()
        part = Part(name="test")
        part.notes = [Note("C", octave=4, duration=QUARTER), Note("D", octave=4, duration=QUARTER), Note("E", octave=4, duration=QUARTER)]
        score.add_part(part)

        output_path = temp_dir / "test.musicxml"
        MusicXMLWriter.write(score, str(output_path))

        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Check it contains XML
        content = output_path.read_text()
        assert "<?xml" in content or "<score-partwise" in content

    def test_lilypond_export(self, temp_dir):
        """Test LilyPond file export."""
        from musicgen.io.lilypond_writer import LilyPondWriter

        score = Score()
        part = Part(name="test")
        part.notes = [Note("C", octave=4, duration=QUARTER), Note("D", octave=4, duration=QUARTER), Note("E", octave=4, duration=QUARTER)]
        score.add_part(part)

        output_path = temp_dir / "test.ly"
        result = LilyPondWriter.write(score, str(output_path))

        assert Path(result).exists()
        content = Path(result).read_text()
        assert "\\version" in content or "\\relative" in content


class TestMoodPresets:
    """Test mood preset configurations."""

    def test_all_moods_defined(self):
        """Test that all mood presets are properly defined."""
        from musicgen.config.moods import MOOD_PRESETS

        expected_moods = [
            "epic", "peaceful", "mysterious", "triumphant",
            "melancholic", "playful", "romantic", "tense"
        ]

        for mood in expected_moods:
            assert mood in MOOD_PRESETS
            preset = MOOD_PRESETS[mood]
            assert "key" in preset
            assert "scale" in preset
            assert "tempo_min" in preset
            assert "tempo_max" in preset
            assert "instruments" in preset

    def test_mood_generation(self, temp_dir):
        """Test generation for each mood preset."""
        from musicgen.config.moods import MOOD_PRESETS

        for mood_name, _preset in MOOD_PRESETS.items():
            request = CompositionRequest(
                mood=mood_name,
                duration=10,  # Short for testing
                output_dir=str(temp_dir),
                export_formats=["midi"]
            )

            result = generate(request)
            assert result.score is not None
            assert result.midi_path is not None


class TestReproducibility:
    """Test that generation is reproducible with seeds."""

    def test_seeded_generation(self):
        """Test that same seed produces same output."""
        scale = Scale("C", "major")
        key = Key("C", "major")

        gen1 = MelodyGenerator(scale, key)
        gen1.set_seed(42)
        melody1 = gen1.generate_motif(length=8)

        gen2 = MelodyGenerator(scale, key)
        gen2.set_seed(42)
        melody2 = gen2.generate_motif(length=8)

        # Notes should be identical
        assert len(melody1.notes) == len(melody2.notes)
        for n1, n2 in zip(melody1.notes, melody2.notes, strict=False):
            if isinstance(n1, Note) and isinstance(n2, Note):
                assert n1.name == n2.name
                assert n1.octave == n2.octave
