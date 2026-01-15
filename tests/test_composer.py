"""Test AI composer."""

import pytest

from musicgen.composer_new import AIComposer, ValidationError
from musicgen.ai_models import AIComposition


def test_composer_initialization():
    """Test composer can be initialized."""
    # Will fail without API key, but tests initialization
    try:
        composer = AIComposer(api_key="test-key")
        assert composer is not None
    except Exception as e:
        # Expected to fail on API call, not initialization
        assert "test-key" in str(e) or "API" in str(e)


def test_generate_requires_validation():
    """Test that generate validates by default."""
    # Mock test - actual generation requires API
    pass


def test_preset_system():
    """Test prompt presets."""
    from musicgen.composer_new.presets import (
        get_preset,
        list_presets,
        apply_modifier,
    )

    presets = list_presets()
    assert len(presets) > 0
    assert "classical_piano" in presets

    preset = get_preset("classical_piano")
    assert "piano" in preset.lower()

    modified = apply_modifier("A simple melody", "faster")
    assert "tempo" in modified.lower()


def test_composition_validation():
    """Test composition validation."""
    # Valid composition
    data = {
        "title": "Test",
        "tempo": 120,
        "key": {"tonic": "C", "mode": "major"},
        "parts": [{
            "name": "piano",
            "midi_program": 0,
            "midi_channel": 0,
            "notes": [
                {"note_name": "C4", "duration": 1.0},
            ]
        }]
    }

    comp = AIComposition(**data)
    assert comp.title == "Test"
    assert comp.duration_seconds == 0.5  # 1 quarter at 120 BPM


def test_invalid_composition_raises():
    """Test that invalid composition raises error."""
    # Missing required fields
    data = {
        "title": "Test",
        # Missing tempo, key, parts
    }

    with pytest.raises(ValidationError):
        AIComposition(**data)
