"""Test AI composition models."""

import json
import pytest

from musicgen.ai_models import (
    AINote,
    AIRest,
    AIPart,
    AIComposition,
    TimeSignature,
    KeySignature,
)


def test_ai_note_validation():
    """Test note validation."""
    # Note with note name
    note = AINote(note_name="C4", duration=1.0)
    assert note.get_midi_number() == 60
    assert note.get_frequency() == pytest.approx(261.63, rel=0.001)

    # Note with MIDI number
    note2 = AINote(midi_number=69, duration=1.0)
    assert note2.get_midi_number() == 69
    assert note2.get_frequency() == 440.0


def test_ai_part_validation():
    """Test part validation."""
    part = AIPart(
        name="violin",
        midi_program=40,
        midi_channel=0,
        role="melody",
        notes=[
            {"note_name": "C4", "duration": 1.0, "velocity": 80},
            {"note_name": "E4", "duration": 0.5, "velocity": 75},
            {"note_name": "G4", "duration": 1.5, "velocity": 70},
        ]
    )

    assert part.name == "violin"
    assert part.duration_quarters == 3.0


def test_ai_composition_validation():
    """Test composition validation."""
    comp_data = {
        "title": "Test Composition",
        "tempo": 120,
        "time_signature": {"numerator": 4, "denominator": 4},
        "key": {"tonic": "C", "mode": "major"},
        "parts": [
            {
                "name": "piano",
                "midi_program": 0,
                "midi_channel": 0,
                "role": "melody",
                "notes": [
                    {"note_name": "C4", "duration": 1.0},
                    {"note_name": "D4", "duration": 1.0},
                ]
            },
            {
                "name": "bass",
                "midi_program": 32,
                "midi_channel": 1,
                "role": "bass",
                "notes": [
                    {"note_name": "C2", "duration": 2.0},
                ]
            }
        ]
    }

    comp = AIComposition(**comp_data)
    assert comp.title == "Test Composition"
    assert comp.tempo == 120
    assert len(comp.parts) == 2
    assert comp.duration_quarters == 2.0


def test_json_parsing():
    """Test parsing from JSON string."""
    json_str = json.dumps({
        "title": "JSON Test",
        "tempo": 100,
        "key": {"tonic": "F", "mode": "major"},
        "parts": [{
            "name": "flute",
            "midi_program": 73,
            "midi_channel": 0,
            "notes": [
                {"note_name": "F4", "duration": 1.0},
            ]
        }]
    })

    comp = AIComposition.model_validate_json(json_str)
    assert comp.title == "JSON Test"


def test_rest_in_notes():
    """Test rest handling."""
    part = AIPart(
        name="piano",
        midi_program=0,
        notes=[
            {"note_name": "C4", "duration": 1.0},
            {"rest": True, "duration": 0.5},
            {"note_name": "E4", "duration": 1.0},
        ]
    )

    events = part.get_note_events()
    assert len(events) == 3
    assert isinstance(events[0], AINote)
    assert isinstance(events[1], AIRest)
    assert isinstance(events[2], AINote)
