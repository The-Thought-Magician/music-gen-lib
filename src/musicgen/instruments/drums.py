"""
Drum pattern system for music-gen-lib V4.

This module provides drum pattern definitions and generation for various genres
including rock, pop, jazz, funk, hip-hop, and electronic styles.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    pass


@dataclass
class DrumPattern:
    """
    Drum pattern definition using mini-notation.

    Attributes:
        name: Pattern name
        genre: Musical genre
        time_signature: (numerator, denominator)
        subdivision: Note subdivision (8=eighth, 16=sixteenth)
        pattern: Dictionary mapping drum pieces to mini-notation patterns
        velocity_map: Custom velocities per piece
        swing: Swing amount (0-1)
        bpm_range: Optional (min, max) BPM range
    """

    name: str
    genre: str
    time_signature: tuple[int, int] = (4, 4)
    subdivision: int = 16
    pattern: dict[str, str] = field(default_factory=dict)
    velocity_map: dict[str, list[int]] = field(default_factory=dict)
    swing: float = 0.0
    bpm_range: tuple[int, int] | None = None

    def parse_piece(self, piece: str) -> list[bool]:
        """
        Parse a drum piece mini-notation pattern.

        Args:
            piece: Drum piece name (e.g., "kick", "snare")

        Returns:
            List of booleans indicating hits
        """
        if piece not in self.pattern:
            return []

        pattern_str = self.pattern[piece]
        result: list[bool] = []

        for char in pattern_str:
            if char == "x":
                result.append(True)
            elif char == ".":
                result.append(False)
            elif char in " \t\n":
                continue

        return result

    def get_velocity_for_step(self, piece: str, step: int, default: int = 100) -> int:
        """Get velocity for a specific step of a piece."""
        if piece not in self.velocity_map:
            return default
        velocities = self.velocity_map[piece]
        if step >= len(velocities):
            return default
        return velocities[step]


# =============================================================================
# Rock Patterns
# =============================================================================

ROCK_BASIC_8TH = DrumPattern(
    name="Basic Rock 8th",
    genre="rock",
    time_signature=(4, 4),
    subdivision=8,
    pattern={
        "kick": "x . x . . . x .",
        "snare": ". . x . . . x .",
        "hihat": "x x x x x x x x",
    },
    swing=0.0,
)

ROCK_BASIC_16TH = DrumPattern(
    name="Basic Rock 16th",
    genre="rock",
    time_signature=(4, 4),
    subdivision=16,
    pattern={
        "kick": "x . . . x . . . . . x . . . x .",
        "snare": ". . x . . . x . . . x . . . x .",
        "hihat": "x x x x x x x x x x x x x x x x",
    },
    swing=0.0,
)

ROCK_HARD = DrumPattern(
    name="Hard Rock",
    genre="rock",
    time_signature=(4, 4),
    subdivision=16,
    pattern={
        "kick": "x . x . x . x . x . x . x . x .",
        "snare": ". . x . . . x . . . x . . . x .",
        "crash": "x . . . . . . . . . . . . . . .",
        "ride": ". . . . . . . . x x x x x x x x",
    },
    swing=0.0,
)

ROCK_PUNK = DrumPattern(
    name="Punk/Fast",
    genre="punk",
    time_signature=(4, 4),
    subdivision=8,
    bpm_range=(160, 200),
    pattern={
        "kick": "x . x . x . x .",
        "snare": ". . x . . . x .",
        "hihat": "x x x x x x x x",
    },
    swing=0.0,
)


# =============================================================================
# Pop Patterns
# =============================================================================

POP_BASIC = DrumPattern(
    name="Basic Pop",
    genre="pop",
    time_signature=(4, 4),
    subdivision=16,
    pattern={
        "kick": "x . . . . . x . . . x . . . . .",
        "snare": ". . x . . . . . . . x . . . . .",
        "hihat": "x x x x x x x x x x x x x x x x",
    },
    swing=0.05,
)

POP_DISCO = DrumPattern(
    name="Disco",
    genre="disco",
    time_signature=(4, 4),
    subdivision=16,
    pattern={
        "kick": "x . x . x . x . x . x . x . x .",
        "snare": ". . . . x . . . . . . . x . . .",
        "hihat_open": "x . . . . . . . . . . . . . . .",
        "hihat_closed": ". . . . x . . . . . . . x . . .",
    },
    swing=0.1,
)

POP_ROCK = DrumPattern(
    name="Pop Rock",
    genre="pop",
    time_signature=(4, 4),
    subdivision=16,
    pattern={
        "kick": "x . . . x . . . x . . . . . x .",
        "snare": ". . x . . . . . . . x . . . x .",
        "hihat": "x x x x x x x x x x x x x x x x",
    },
    swing=0.0,
)


# =============================================================================
# Jazz Patterns
# =============================================================================

JAZZ_BASIC_SWING = DrumPattern(
    name="Basic Swing",
    genre="jazz",
    time_signature=(4, 4),
    subdivision=8,
    pattern={
        "kick": "x . . . . . x .",
        "snare": ". . x . . . . .",
        "ride": "x x x x x x x x",
    },
    swing=0.3,
)

JAZZ_RIDE = DrumPattern(
    name="Jazz Ride Pattern",
    genre="jazz",
    time_signature=(4, 4),
    subdivision=8,
    pattern={
        "kick": "x . . . . . x .",
        "snare": ". . x . . . . .",
        "ride_bell": "x . . . x . . .",
        "ride": ". x x x . x x x",
    },
    swing=0.35,
)

JAZZ_BRUSHES = DrumPattern(
    name="Brushes",
    genre="jazz",
    time_signature=(4, 4),
    subdivision=8,
    pattern={
        "kick": "x . . . . . x .",
        "snare": ". x . x . x . x",
    },
    swing=0.3,
)

JAZZ_BEBOP = DrumPattern(
    name="Bebop",
    genre="jazz",
    time_signature=(4, 4),
    subdivision=8,
    pattern={
        "kick": "x x . . x . x .",
        "snare": ". . x . . . x .",
        "ride": "x x x x x x x x",
    },
    swing=0.4,
)


# =============================================================================
# Funk Patterns
# =============================================================================

FUNK_BASIC = DrumPattern(
    name="Basic Funk",
    genre="funk",
    time_signature=(4, 4),
    subdivision=16,
    pattern={
        "kick": "x . . x . . x . x . x . . . x .",
        "snare": ". . x . . . x . . . x . . . x .",
        "ghost": ". x . . . x . . . x . . x . . .",
        "hihat": "x x x x x x x x x x x x x x x x",
    },
    swing=0.15,
)

FUNK_JAMES_BROWN = DrumPattern(
    name="James Brown Style",
    genre="funk",
    time_signature=(4, 4),
    subdivision=16,
    pattern={
        "kick": "x . x . x . x . . . x . x . . .",
        "snare": ". . x . . . . . . x . . . . .",
        "ghost": ". x . . . x . . . x . . . x . .",
        "hihat": "x . x . x . x . x . x . x . x . x .",
    },
    swing=0.2,
)


# =============================================================================
# Hip-Hop Patterns
# =============================================================================

HIPHOP_BOOM_BAP = DrumPattern(
    name="Boom Bap",
    genre="hiphop",
    time_signature=(4, 4),
    subdivision=16,
    pattern={
        "kick": "x . . . x . . . . . . . . . x .",
        "snare": ". . . . x . . . . . . . x . . .",
        "hihat": "x . x . x . x . x . x . x . x . x .",
    },
    swing=0.1,
)

HIPHOP_TRAP = DrumPattern(
    name="Trap",
    genre="hiphop",
    time_signature=(4, 4),
    subdivision=16,
    pattern={
        "kick": "x . . . . . . . x . . . . . . .",
        "snare": ". . . . x . . . . . . . x . . .",
        "hihat": "x x x x x x x x x x x x x x x x",
        "hihat_open": ". . . . . . . . . . . . . . x .",
    },
    swing=0.05,
)

HIPHOP_TRAP_HALF = DrumPattern(
    name="Trap Half-Time",
    genre="hiphop",
    time_signature=(4, 4),
    subdivision=8,
    pattern={
        "kick": "x . . . . . . .",
        "snare": ". . . . x . . .",
        "hihat": "x x x x x x x x",
    },
    swing=0.0,
)


# =============================================================================
# Electronic/EDM Patterns
# =============================================================================

EDM_FOUR_ON_FLOOR = DrumPattern(
    name="4-on-the-Floor",
    genre="house",
    time_signature=(4, 4),
    subdivision=16,
    pattern={
        "kick": "x . . . x . . . x . . . x . . .",
        "clap": ". . . . x . . . . . . . x . . .",
        "hihat": ". x . x . x . x . x . x . x . x .",
    },
    swing=0.0,
)

EDM_TECHNO = DrumPattern(
    name="Techno",
    genre="techno",
    time_signature=(4, 4),
    subdivision=16,
    pattern={
        "kick": "x . . . x . . . x . . . x . . .",
        "clap": ". . . . . . x . . . . . . . x .",
        "hihat": ". x . . . x . . . x . . . x . .",
    },
    swing=0.0,
)

EDM_DNB = DrumPattern(
    name="Drum and Bass",
    genre="dnb",
    time_signature=(4, 4),
    subdivision=16,
    bpm_range=(170, 180),
    pattern={
        "kick": "x . . . . . . . . . . . . . . .",
        "snare": ". . . . x . . . . . . . x . . .",
        "breakbeat": "x x . x x . x . x . . x x x . x .",
    },
    swing=0.05,
)

EDM_DUBSTEP = DrumPattern(
    name="Dubstep",
    genre="dubstep",
    time_signature=(4, 4),
    subdivision=8,
    bpm_range=(140, 145),
    pattern={
        "kick": "x . . . . . . .",
        "snare": ". . . . x . . .",
        "hihat": ". x . x . x . x",
    },
    swing=0.2,
)


# =============================================================================
# Pattern Registry
# =============================================================================

DRUM_PATTERNS: dict[str, DrumPattern] = {
    # Rock
    "rock_basic_8th": ROCK_BASIC_8TH,
    "rock_basic_16th": ROCK_BASIC_16TH,
    "rock_hard": ROCK_HARD,
    "punk": ROCK_PUNK,
    # Pop
    "pop_basic": POP_BASIC,
    "disco": POP_DISCO,
    "pop_rock": POP_ROCK,
    # Jazz
    "jazz_basic_swing": JAZZ_BASIC_SWING,
    "jazz_ride": JAZZ_RIDE,
    "jazz_brushes": JAZZ_BRUSHES,
    "bebop": JAZZ_BEBOP,
    # Funk
    "funk_basic": FUNK_BASIC,
    "james_brown": FUNK_JAMES_BROWN,
    # Hip-Hop
    "boom_bap": HIPHOP_BOOM_BAP,
    "trap": HIPHOP_TRAP,
    "trap_half": HIPHOP_TRAP_HALF,
    # Electronic
    "four_on_floor": EDM_FOUR_ON_FLOOR,
    "techno": EDM_TECHNO,
    "dnb": EDM_DNB,
    "dubstep": EDM_DUBSTEP,
}


# =============================================================================
# Fill Generator
# =============================================================================


@dataclass
class DrumFillGenerator:
    """Generate drum fills."""

    style: str = "rock"

    def generate_fill(
        self,
        length: Literal["1", "2", "4"] = "1",
        end_phrase: bool = True,  # Reserved for future use  # noqa: ARG002
    ) -> DrumPattern:
        """
        Generate a fill in specified style.

        Args:
            length: Length in beats (1, 2, or 4)
            end_phrase: Whether fill ends a phrase

        Returns:
            DrumPattern for the fill
        """
        if length == "1":
            return self._one_beat_fill()
        elif length == "2":
            return self._two_beat_fill()
        else:
            return self._four_beat_fill()

    def _one_beat_fill(self) -> DrumPattern:
        """Generate single beat fill."""
        return DrumPattern(
            name="1 Beat Fill",
            genre=self.style,
            subdivision=16,
            pattern={
                "snare": "x x x x",
                "kick": "x",
            },
        )

    def _two_beat_fill(self) -> DrumPattern:
        """Generate two beat fill."""
        return DrumPattern(
            name="2 Beat Fill",
            genre=self.style,
            subdivision=16,
            pattern={
                "snare": "x x x x x x x x",
                "kick": "x . . .",
                "tom1": ". x . .",
                "tom2": ". . x .",
                "crash": ". . . x",
            },
        )

    def _four_beat_fill(self) -> DrumPattern:
        """Generate four beat fill (tom run)."""
        return DrumPattern(
            name="4 Beat Fill",
            genre=self.style,
            subdivision=16,
            pattern={
                "snare": "x x x x x x x x x x x x",
                "kick": "x . . .",
                "tom1": ". x . .",
                "tom2": ". . x .",
                "floor_tom": ". . . x",
                "crash": ". . . x",
            },
        )


# =============================================================================
# Helper Functions
# =============================================================================


def get_pattern(name: str) -> DrumPattern | None:
    """Get a drum pattern by name."""
    return DRUM_PATTERNS.get(name)


def get_patterns_by_genre(genre: str) -> dict[str, DrumPattern]:
    """Get all patterns for a specific genre."""
    return {k: v for k, v in DRUM_PATTERNS.items() if v.genre.lower() == genre.lower()}


def apply_groove(
    pattern: DrumPattern,
    swing: float | None = None,
    humanize: float = 0.0,  # Reserved for future MIDI rendering  # noqa: ARG001
) -> DrumPattern:
    """
    Apply groove feel to a drum pattern.

    Args:
        pattern: Base pattern
        swing: Swing amount (overrides pattern swing)
        humanize: Timing variation amount (0-1)

    Returns:
        New DrumPattern with groove applied
    """
    new_pattern = DrumPattern(
        name=f"{pattern.name} (grooved)",
        genre=pattern.genre,
        time_signature=pattern.time_signature,
        subdivision=pattern.subdivision,
        pattern=pattern.pattern.copy(),
        velocity_map=pattern.velocity_map.copy(),
        swing=swing if swing is not None else pattern.swing,
        bpm_range=pattern.bpm_range,
    )
    # Humanization would be applied during MIDI rendering
    return new_pattern


__all__ = [
    "DrumPattern",
    "DrumFillGenerator",
    "DRUM_PATTERNS",
    "get_pattern",
    "get_patterns_by_genre",
    "apply_groove",
]
