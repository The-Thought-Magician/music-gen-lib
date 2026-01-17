"""
Pentatonic scale definitions for music-gen-lib V4.

This module provides pentatonic scale definitions used in various
musical traditions including blues, rock, folk, and world music.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


# =============================================================================
# Pentatonic Scale Classes
# =============================================================================


@dataclass
class PentatonicScale:
    """
    Pentatonic scale definition.

    Attributes:
        name: Scale name
        intervals: Intervals from tonic (in semitones)
        ascending: Ascending scale in semitones from tonic
        descending: Descending scale in semitones from tonic
        mode: Scale mode (major, minor, etc.)
        usage: Common usage contexts
        mood: Emotional quality
    """

    name: str
    intervals: list[int]
    ascending: list[int]
    descending: list[int]
    mode: str = "major"
    usage: str = ""
    mood: str = ""


# =============================================================================
# Major Pentatonic Scales
# =============================================================================

# Major Pentatonic: 1, 2, 3, 5, 6
SCALE_MAJOR_PENTATONIC = PentatonicScale(
    name="Major Pentatonic",
    intervals=[0, 2, 4, 7, 9],
    ascending=[0, 2, 4, 7, 9, 12],
    descending=[12, 9, 7, 4, 2, 0],
    mode="major",
    usage="Country, folk, pop, rock, children's music",
    mood="Bright, happy, optimistic",
)

# Chinese Pentatonic (same as major pentatonic)
SCALE_CHINESE = SCALE_MAJOR_PENTATONIC

# Egyptian Pentatonic: 1, 2, 4, 5, 7
SCALE_EGYPTIAN = PentatonicScale(
    name="Egyptian Pentatonic",
    intervals=[0, 2, 5, 7, 10],
    ascending=[0, 2, 5, 7, 10, 12],
    descending=[12, 10, 7, 5, 2, 0],
    mode="major",
    usage="Middle Eastern, Egyptian music",
    mood="Exotic, Middle Eastern",
)


# =============================================================================
# Minor Pentatonic Scales
# =============================================================================

# Minor Pentatonic: 1, b3, 4, 5, b7
SCALE_MINOR_PENTATONIC = PentatonicScale(
    name="Minor Pentatonic",
    intervals=[0, 3, 5, 7, 10],
    ascending=[0, 3, 5, 7, 10, 12],
    descending=[12, 10, 7, 5, 3, 0],
    mode="minor",
    usage="Blues, rock, jazz, metal",
    mood="Melancholic, soulful, bluesy",
)

# Blues Scale (minor pentatonic with added #4/b5)
SCALE_BLUES = PentatonicScale(
    name="Blues",
    intervals=[0, 3, 5, 6, 7, 10],  # Hexatonic really
    ascending=[0, 3, 5, 6, 7, 10, 12],
    descending=[12, 10, 7, 6, 5, 3, 0],
    mode="minor",
    usage="Blues, rock, jazz, funk",
    mood="Soulful, bluesy, gritty",
)


# =============================================================================
# Other Pentatonic Scales
# =============================================================================

# Pelog (Bali) - 5-tone uneven scale
SCALE_PELOG = PentatonicScale(
    name="Pelog",
    intervals=[0, 1, 3, 7, 8],
    ascending=[0, 1, 3, 7, 8, 12],
    descending=[12, 8, 7, 3, 1, 0],
    mode="other",
    usage="Balinese gamelan",
    mood="Mysterious, exotic",
)

# Slendro (Java) - 5-tone roughly equidistant
SCALE_SLENDRO = PentatonicScale(
    name="Slendro",
    intervals=[0, 2, 5, 7, 9],  # Approximation
    ascending=[0, 2, 5, 7, 9, 12],
    descending=[12, 9, 7, 5, 2, 0],
    mode="other",
    usage="Javanese gamelan",
    mood="Mystical, meditative",
)

# Hirajoushi (Japan)
SCALE_HIRAJOUSHI = PentatonicScale(
    name="Hirajoushi",
    intervals=[0, 2, 4, 7, 9],
    ascending=[0, 2, 4, 7, 9, 12],
    descending=[12, 9, 7, 4, 2, 0],
    mode="other",
    usage="Japanese koto music",
    mood="Peaceful, traditional",
)

# In Sen Pou (Japan)
SCALE_IN_SENPOU = PentatonicScale(
    name="In Sen Pou",
    intervals=[0, 1, 5, 7, 8],
    ascending=[0, 1, 5, 7, 8, 12],
    descending=[12, 8, 7, 5, 1, 0],
    mode="other",
    usage="Japanese gagaku (court music)",
    mood="Dark, solemn",
)

# Kumoi (Japan)
SCALE_KUMOI_JOSHI = PentatonicScale(
    name="Kumoi Joshi",
    intervals=[0, 2, 3, 7, 9],
    ascending=[0, 2, 3, 7, 9, 12],
    descending=[12, 9, 7, 3, 2, 0],
    mode="other",
    usage="Japanese folk music",
    mood="Bright, playful",
)

# Lydian Pentatonic: 1, 2, 3, #4, #5
SCALE_LYDIAN_PENTATONIC = PentatonicScale(
    name="Lydian Pentatonic",
    intervals=[0, 2, 4, 6, 8],
    ascending=[0, 2, 4, 6, 8, 12],
    descending=[12, 8, 6, 4, 2, 0],
    mode="major",
    usage="Jazz, fusion",
    mood="Dreamy, floating",
)

# Mixolydian Pentatonic: 1, 2, 3, 5, b7
SCALE_MIXOLYDIAN_PENTATONIC = PentatonicScale(
    name="Mixolydian Pentatonic",
    intervals=[0, 2, 4, 7, 10],
    ascending=[0, 2, 4, 7, 10, 12],
    descending=[12, 10, 7, 4, 2, 0],
    mode="major",
    usage="Rock, country, folk",
    mood="Upbeat, rural",
)

# Dorian Pentatonic: 1, 2, b3, 5, 6
SCALE_DORIAN_PENTATONIC = PentatonicScale(
    name="Dorian Pentatonic",
    intervals=[0, 2, 3, 7, 9],
    ascending=[0, 2, 3, 7, 9, 12],
    descending=[12, 9, 7, 3, 2, 0],
    mode="minor",
    usage="Jazz, modal music",
    mood="Sophisticated, jazzy",
)

# Phrygian Pentatonic: 1, b2, b3, 5, b7
SCALE_PHRYGIAN_PENTATONIC = PentatonicScale(
    name="Phrygian Pentatonic",
    intervals=[0, 1, 3, 7, 10],
    ascending=[0, 1, 3, 7, 10, 12],
    descending=[12, 10, 7, 3, 1, 0],
    mode="minor",
    usage="Flamenco, Middle Eastern",
    mood="Passionate, dark",
)


# =============================================================================
# Pentatonic Scale Registry
# =============================================================================

PENTATONIC_SCALES: dict[str, PentatonicScale] = {
    "major": SCALE_MAJOR_PENTATONIC,
    "major_pentatonic": SCALE_MAJOR_PENTATONIC,
    "chinese": SCALE_CHINESE,
    "egyptian": SCALE_EGYPTIAN,
    "minor": SCALE_MINOR_PENTATONIC,
    "minor_pentatonic": SCALE_MINOR_PENTATONIC,
    "blues": SCALE_BLUES,
    "blues_scale": SCALE_BLUES,
    "pelog": SCALE_PELOG,
    "slendro": SCALE_SLENDRO,
    "hirajoushi": SCALE_HIRAJOUSHI,
    "insenpou": SCALE_IN_SENPOU,
    "in_sen_pou": SCALE_IN_SENPOU,
    "kumoi": SCALE_KUMOI_JOSHI,
    "kumoi_joshi": SCALE_KUMOI_JOSHI,
    "lydian": SCALE_LYDIAN_PENTATONIC,
    "lydian_pentatonic": SCALE_LYDIAN_PENTATONIC,
    "mixolydian": SCALE_MIXOLYDIAN_PENTATONIC,
    "mixolydian_pentatonic": SCALE_MIXOLYDIAN_PENTATONIC,
    "dorian": SCALE_DORIAN_PENTATONIC,
    "dorian_pentatonic": SCALE_DORIAN_PENTATONIC,
    "phrygian": SCALE_PHRYGIAN_PENTATONIC,
    "phrygian_pentatonic": SCALE_PHRYGIAN_PENTATONIC,
}


# =============================================================================
# Helper Functions
# =============================================================================


def get_pentatonic_scale(name: str) -> PentatonicScale | None:
    """Get a pentatonic scale by name."""
    return PENTATONIC_SCALES.get(name.lower())


def scale_to_midi_scale(scale: PentatonicScale, root: int = 60) -> list[int]:
    """
    Convert a pentatonic scale to MIDI note numbers.

    Args:
        scale: The pentatonic scale
        root: Root note MIDI number (default: C4 = 60)

    Returns:
        List of MIDI note numbers for the ascending scale
    """
    return [root + semitone for semitone in scale.ascending]


def get_blues_scale(root: int = 60) -> list[int]:
    """Convenience function to get blues scale from root note."""
    return scale_to_midi_scale(SCALE_BLUES, root)


def get_minor_pentatonic_scale(root: int = 60) -> list[int]:
    """Convenience function to get minor pentatonic scale from root note."""
    return scale_to_midi_scale(SCALE_MINOR_PENTATONIC, root)


def get_major_pentatonic_scale(root: int = 60) -> list[int]:
    """Convenience function to get major pentatonic scale from root note."""
    return scale_to_midi_scale(SCALE_MAJOR_PENTATONIC, root)


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "PentatonicScale",
    "PENTATONIC_SCALES",
    "SCALE_MAJOR_PENTATONIC",
    "SCALE_MINOR_PENTATONIC",
    "SCALE_BLUES",
    "SCALE_EGYPTIAN",
    "SCALE_CHINESE",
    "SCALE_PELOG",
    "SCALE_SLENDRO",
    "SCALE_HIRAJOUSHI",
    "SCALE_IN_SENPOU",
    "SCALE_KUMOI_JOSHI",
    "SCALE_LYDIAN_PENTATONIC",
    "SCALE_MIXOLYDIAN_PENTATONIC",
    "SCALE_DORIAN_PENTATONIC",
    "SCALE_PHRYGIAN_PENTATONIC",
    "get_pentatonic_scale",
    "scale_to_midi_scale",
    "get_blues_scale",
    "get_minor_pentatonic_scale",
    "get_major_pentatonic_scale",
]
