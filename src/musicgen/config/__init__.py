"""Configuration module.

This module provides:
- Mood configuration presets (existing)
- YAML + environment variable configuration (new)
"""

from musicgen.config.moods import (
    MOOD_PRESETS,
    MoodPreset,
    get_all_presets,
    get_mood_preset,
    list_moods,
)

# New configuration system
from musicgen.config.settings import (
    DEFAULT_CONFIG,
    Config,
    get_config,
    set_config,
)

__all__ = [
    # Mood presets (existing)
    "MoodPreset",
    "MOOD_PRESETS",
    "get_mood_preset",
    "list_moods",
    "get_all_presets",
    # New configuration system
    "Config",
    "get_config",
    "set_config",
    "DEFAULT_CONFIG",
]
