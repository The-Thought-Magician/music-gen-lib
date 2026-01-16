"""Default configuration values."""

from __future__ import annotations

DEFAULT_CONFIG = {
    "model": {
        "default_model": "gemini-2.5-pro",
        "default_temperature": 0.5,
        "default_max_tokens": None,
        "retry_attempts": 3,
        "retry_delay": 1.0,
    },
    "schema": {
        "include_form_structure": True,
        "include_dynamics": True,
        "include_articulation": True,
        "include_tempo_changes": True,
        "include_time_signature_changes": True,
        "include_key_changes": True,
    },
    "notes": {
        "default_format": "detailed",
        "duration_unit": "quarter",
        "velocity_min": 60,
        "velocity_max": 100,
    },
    # Export defaults: MIDI for editing, MP3 for easy playback/sharing
    "export": {
        "default_output_dir": ".",
        "default_formats": ["midi", "mp3"],
        "sample_rate": 44100,
        "bit_depth": 16,
    },
    "orchestration": {
        "max_instruments": 16,
        "midi_channels": "auto",
    },
    "validation": {
        "strict_schema_validation": True,
        "validate_music_theory": False,
        "max_duration": 600,
    },
}
