"""Tests for mood configuration system."""

import pytest
from musicgen.config.moods import MoodPreset, get_mood_preset, list_moods, get_all_presets
from musicgen.generator import CompositionRequest


class TestMoodPreset:
    """Test MoodPreset class and functions."""

    def test_get_epic_mood(self):
        """Test getting epic mood preset."""
        preset = get_mood_preset("epic")
        assert preset.key == "D"
        assert preset.scale == "harmonic_minor"
        assert preset.tempo_min == 120
        assert preset.tempo_max == 140
        assert preset.dynamics == "ff"

    def test_get_peaceful_mood(self):
        """Test getting peaceful mood preset."""
        preset = get_mood_preset("peaceful")
        assert preset.key == "G"
        assert preset.scale == "major"
        assert preset.tempo_min == 60
        assert preset.tempo_max == 80
        assert preset.dynamics == "mp"

    def test_get_mysterious_mood(self):
        """Test getting mysterious mood preset."""
        preset = get_mood_preset("mysterious")
        assert preset.key == "D"
        assert preset.scale == "harmonic_minor"
        assert preset.tempo_min == 80

    def test_get_mood_case_insensitive(self):
        """Test that mood lookup is case-insensitive."""
        preset1 = get_mood_preset("EPIC")
        preset2 = get_mood_preset("epic")
        preset3 = get_mood_preset("Epic")

        assert preset1.key == preset2.key == preset3.key

    def test_get_invalid_mood_raises(self):
        """Test that invalid mood raises ValueError."""
        with pytest.raises(ValueError):
            get_mood_preset("nonexistent")

    def test_list_moods(self):
        """Test listing available moods."""
        moods = list_moods()
        assert isinstance(moods, list)
        assert len(moods) > 0
        assert "epic" in moods
        assert "peaceful" in moods

    def test_get_all_presets(self):
        """Test getting all presets."""
        presets = get_all_presets()
        assert isinstance(presets, dict)
        assert len(presets) > 0
        for mood, preset in presets.items():
            assert isinstance(preset, MoodPreset)


class TestCompositionRequest:
    """Test CompositionRequest class."""

    def test_create_request(self):
        """Test creating a composition request."""
        request = CompositionRequest(
            mood="epic",
            duration=60,
            key="C"
        )
        assert request.mood == "epic"
        assert request.duration == 60
        assert request.key == "C"

    def test_request_defaults(self):
        """Test request default values."""
        request = CompositionRequest()
        assert request.mood == "peaceful"
        assert request.duration == 30
        assert request.export_formats == ["midi"]

    def test_request_with_various_formats(self):
        """Test request with multiple export formats."""
        request = CompositionRequest(
            mood="peaceful",
            export_formats=["midi", "musicxml", "pdf"]
        )
        assert "midi" in request.export_formats
        assert "musicxml" in request.export_formats
        assert "pdf" in request.export_formats


class TestMoodCharacteristics:
    """Test specific mood characteristics."""

    def test_epic_has_high_tempo(self):
        """Test that epic mood has high tempo."""
        preset = get_mood_preset("epic")
        assert preset.tempo_min >= 120

    def test_peaceful_has_low_tempo(self):
        """Test that peaceful mood has low tempo."""
        preset = get_mood_preset("peaceful")
        assert preset.tempo_max <= 80

    def test_triumphant_has_loud_dynamics(self):
        """Test that triumphant mood has loud dynamics."""
        preset = get_mood_preset("triumphant")
        assert preset.dynamics == "f"

    def test_melancholic_has_soft_dynamics(self):
        """Test that melancholic mood has soft dynamics."""
        preset = get_mood_preset("melancholic")
        assert preset.dynamics == "mp"

    def test_mysterious_has_minor_scale(self):
        """Test that mysterious mood uses minor scale."""
        preset = get_mood_preset("mysterious")
        assert "minor" in preset.scale

    def test_playful_has_staccato_articulation(self):
        """Test that playful mood uses staccato."""
        preset = get_mood_preset("playful")
        assert preset.articulation == "staccato"


@pytest.mark.slow
class TestIntegrationGenerate:
    """Integration tests for the generate function."""

    def test_generate_peaceful_mood(self, tmp_path):
        """Test generating peaceful mood music."""
        from musicgen.generator import generate

        request = CompositionRequest(
            mood="peaceful",
            duration=15,
            export_formats=["midi"],
            output_dir=str(tmp_path)
        )

        result = generate(request)

        assert result.key == "G major"
        assert result.midi_path is not None

    def test_generate_with_key_override(self, tmp_path):
        """Test generating with key override."""
        from musicgen.generator import generate

        request = CompositionRequest(
            mood="peaceful",
            key="F",
            duration=15,
            export_formats=["midi"],
            output_dir=str(tmp_path)
        )

        result = generate(request)

        assert result.key == "F major"

    def test_generate_with_tempo_override(self, tmp_path):
        """Test generating with tempo override."""
        from musicgen.generator import generate

        request = CompositionRequest(
            mood="peaceful",
            tempo=100,
            duration=15,
            export_formats=["midi"],
            output_dir=str(tmp_path)
        )

        result = generate(request)

        assert result.tempo == 100

    def test_generate_with_seed_reproducible(self, tmp_path):
        """Test that seed produces reproducible results."""
        from musicgen.generator import generate

        request1 = CompositionRequest(
            mood="peaceful",
            duration=15,
            export_formats=["midi"],
            output_dir=str(tmp_path),
            seed=42
        )

        request2 = CompositionRequest(
            mood="peaceful",
            duration=15,
            export_formats=["midi"],
            output_dir=str(tmp_path),
            seed=42
        )

        result1 = generate(request1)
        result2 = generate(request2)

        # Same seed should produce same tempo
        assert result1.tempo == result2.tempo
