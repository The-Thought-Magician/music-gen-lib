"""Test rendering engine."""

import tempfile
from pathlib import Path

from musicgen.ai_models import AIComposition
from musicgen.renderer import MIDIRenderer, Renderer


def test_midi_renderer():
    """Test MIDI rendering."""
    # Create simple composition
    comp = AIComposition(
        title="Test",
        tempo=120,
        key={"tonic": "C", "mode": "major"},
        parts=[{
            "name": "piano",
            "midi_program": 0,
            "midi_channel": 0,
            "notes": [
                {"note_name": "C4", "duration": 1.0},
                {"note_name": "D4", "duration": 1.0},
                {"note_name": "E4", "duration": 1.0},
            ]
        }]
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        renderer = MIDIRenderer()
        output_path = Path(tmpdir) / "test.mid"
        renderer.render(comp, output_path)

        assert output_path.exists()


def test_renderer():
    """Test main renderer."""
    comp = AIComposition(
        title="Renderer Test",
        tempo=100,
        key={"tonic": "F", "mode": "major"},
        parts=[{
            "name": "flute",
            "midi_program": 73,
            "midi_channel": 0,
            "notes": [{"note_name": "F4", "duration": 2.0}]
        }]
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        renderer = Renderer(output_dir=Path(tmpdir))
        results = renderer.render(comp, formats=["midi"])

        assert "midi" in results
        assert results["midi"].exists()


def test_render_convenience():
    """Test convenience function."""
    from musicgen.renderer import render

    comp = AIComposition(
        title="Convenience Test",
        tempo=110,
        key={"tonic": "G", "mode": "minor"},
        parts=[{
            "name": "violin",
            "midi_program": 40,
            "midi_channel": 0,
            "notes": [{"note_name": "G3", "duration": 1.0}]
        }]
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        results = render(comp, formats=["midi"], output_dir=Path(tmpdir))
        assert results["midi"].exists()
