"""Configuration module.

This module provides mood configuration presets.
"""

from musicgen.config.moods import (
    MoodPreset,
    MOOD_PRESETS,
    get_mood_preset,
    list_moods,
    get_all_presets,
)

__all__ = [
    "MoodPreset",
    "MOOD_PRESETS",
    "get_mood_preset",
    "list_moods",
    "get_all_presets",
]
