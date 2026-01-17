"""
Genre-specific styles and patterns for music-gen-lib V4.

This module provides genre profiles, patterns, and style transfer
capabilities for intelligent genre-aware composition.
"""

from musicgen.genres.profiles import (
    CLASSICAL,
    ELECTRONIC,
    GENRE_PROFILES,
    JAZZ,
    POP,
    ROCK,
    WORLD,
    GenreProfile,
    get_all_genres,
    get_genre_profile,
    get_genres_by_tempo,
)

__all__ = [
    "GenreProfile",
    # Genres
    "ROCK",
    "POP",
    "JAZZ",
    "CLASSICAL",
    "ELECTRONIC",
    "WORLD",
    # Registry
    "GENRE_PROFILES",
    # Helpers
    "get_genre_profile",
    "get_all_genres",
    "get_genres_by_tempo",
]
