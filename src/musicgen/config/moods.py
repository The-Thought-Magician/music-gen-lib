"""Mood configuration presets for music generation.

This module provides predefined mood configurations that specify
musical parameters for generating music with specific emotional qualities.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class MoodPreset:
    """Configuration for generating music with a specific mood.

    Attributes:
        key: The recommended key
        scale: The scale type to use
        tempo_min: Minimum tempo in BPM
        tempo_max: Maximum tempo in BPM
        instruments: List of recommended instruments
        dynamics: Dynamic range preference
        articulation: Preferred articulation style
        form: Suggested musical form
    """

    key: str
    scale: str
    tempo_min: int
    tempo_max: int
    instruments: list[str]
    dynamics: str = "mf"
    articulation: str = "legato"
    form: str = "binary"


# Mood presets dictionary
MOOD_PRESETS: dict[str, dict[str, Any]] = {
    "epic": {
        "key": "D",
        "scale": "harmonic_minor",
        "tempo_min": 120,
        "tempo_max": 140,
        "instruments": ["violin", "viola", "cello", "double_bass",
                       "trumpet", "french_horn", "trombone", "timpani"],
        "dynamics": "ff",
        "articulation": "marcato",
        "form": "ternary",
    },
    "peaceful": {
        "key": "G",
        "scale": "major",
        "tempo_min": 60,
        "tempo_max": 80,
        "instruments": ["flute", "clarinet", "violin", "cello", "piano"],
        "dynamics": "mp",
        "articulation": "legato",
        "form": "binary",
    },
    "mysterious": {
        "key": "D",
        "scale": "harmonic_minor",
        "tempo_min": 80,
        "tempo_max": 100,
        "instruments": ["flute", "clarinet", "bassoon", "cello",
                       "french_horn", "piano"],
        "dynamics": "mp",
        "articulation": "legato",
        "form": "through_composed",
    },
    "triumphant": {
        "key": "C",
        "scale": "major",
        "tempo_min": 110,
        "tempo_max": 130,
        "instruments": ["trumpet", "french_horn", "trombone",
                       "violin", "viola", "cello", "timpani"],
        "dynamics": "f",
        "articulation": "marcato",
        "form": "ternary",
    },
    "melancholic": {
        "key": "A",
        "scale": "natural_minor",
        "tempo_min": 60,
        "tempo_max": 80,
        "instruments": ["violin", "viola", "cello", "oboe", "piano"],
        "dynamics": "mp",
        "articulation": "legato",
        "form": "binary",
    },
    "playful": {
        "key": "G",
        "scale": "major_pentatonic",
        "tempo_min": 100,
        "tempo_max": 120,
        "instruments": ["flute", "clarinet", "violin", "piano", "pizzicato"],
        "dynamics": "mf",
        "articulation": "staccato",
        "form": "rondo",
    },
    "romantic": {
        "key": "F",
        "scale": "major",
        "tempo_min": 70,
        "tempo_max": 90,
        "instruments": ["violin", "cello", "flute", "piano"],
        "dynamics": "mf",
        "articulation": "legato",
        "form": "ternary",
    },
    "tense": {
        "key": "C",
        "scale": "harmonic_minor",
        "tempo_min": 90,
        "tempo_max": 110,
        "instruments": ["violin", "viola", "cello", "clarinet",
                       "french_horn", "piano"],
        "dynamics": "mf-f",
        "articulation": "marcato",
        "form": "through_composed",
    },
}


def get_mood_preset(mood: str) -> MoodPreset:
    """Get a mood preset by name.

    Args:
        mood: Name of the mood

    Returns:
        A MoodPreset object

    Raises:
        ValueError: If mood is not found
    """
    mood_lower = mood.lower()

    if mood_lower not in MOOD_PRESETS:
        available = ", ".join(MOOD_PRESETS.keys())
        raise ValueError(f"Unknown mood: {mood}. Available: {available}")

    config = MOOD_PRESETS[mood_lower]
    return MoodPreset(
        key=config["key"],
        scale=config["scale"],
        tempo_min=config["tempo_min"],
        tempo_max=config["tempo_max"],
        instruments=config["instruments"],
        dynamics=config.get("dynamics", "mf"),
        articulation=config.get("articulation", "legato"),
        form=config.get("form", "binary"),
    )


def list_moods() -> list[str]:
    """Return a list of available mood names.

    Returns:
        List of mood names
    """
    return list(MOOD_PRESETS.keys())


def get_all_presets() -> dict[str, MoodPreset]:
    """Get all mood presets as MoodPreset objects.

    Returns:
        Dictionary mapping mood names to MoodPreset objects
    """
    return {mood: get_mood_preset(mood) for mood in MOOD_PRESETS}
