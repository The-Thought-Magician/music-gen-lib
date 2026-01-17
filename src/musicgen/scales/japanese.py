"""
Japanese scale definitions for music-gen-lib V4.

This module provides scale definitions for traditional Japanese scales
used in gagaku, folk music, and contemporary Japanese music.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


# =============================================================================
# Japanese Scale Classes
# =============================================================================


@dataclass
class JapaneseScale:
    """
    Traditional Japanese scale definition.

    Attributes:
        name: Scale name (Romanized)
        name_japanese: Scale name in Japanese
        type: Scale type (pentatonic, hexatonic, etc.)
        ascending: Ascending scale in semitones from tonic
        descending: Descending scale in semitones from tonic
        interval_pattern: Pattern of intervals (H=half, W=whole, m3=minor third)
        usage: Context where this scale is used
        mood: Emotional quality
    """

    name: str
    name_japanese: str
    type: str
    ascending: list[int]
    descending: list[int]
    interval_pattern: str = ""
    usage: str = ""
    mood: str = ""


# =============================================================================
# Japanese Scales
# =============================================================================

# In Sen Pou - "hidden 1" scale
SCALE_IN_SENPOU = JapaneseScale(
    name="In Sen Pou",
    name_japanese="陰旋法",
    type="pentatonic",
    ascending=[0, 1, 4, 6, 8, 12],  # C Db E F# G C (with octave)
    descending=[12, 8, 6, 4, 1, 0],
    interval_pattern="H m3 H W H",
    usage="Gagaku (court music), traditional",
    mood="Dark, mysterious, solemn",
)

# Hirajoushi - common koto tuning
SCALE_HIRAJOUSHI = JapaneseScale(
    name="Hirajoushi",
    name_japanese="平調子",
    type="pentatonic",
    ascending=[0, 2, 4, 7, 9, 12],  # C D E G B C
    descending=[12, 9, 7, 4, 2, 0],
    interval_pattern="W W H+W W H",
    usage="Koto music, most common Japanese scale",
    mood="Peaceful, bright, balanced",
)

# Miyakobushi - "Okinawan" scale
SCALE_MIYAKOBUCHI = JapaneseScale(
    name="Miyakobushi",
    name_japanese="都節",
    type="pentatonic",
    ascending=[0, 1, 4, 6, 8, 12],  # C Db E F# G C (same as In but different context)
    descending=[12, 8, 6, 4, 1, 0],
    interval_pattern="H m3 H W H",
    usage="Ryukyuan/Okinawan music, folk",
    mood="Melancholic, distinctive",
)

# Kumoi - common pentatonic
SCALE_KUMOI = JapaneseScale(
    name="Kumoi",
    name_japanese="雲井",
    type="pentatonic",
    ascending=[0, 2, 3, 7, 9, 12],  # C D Eb G B C
    descending=[12, 9, 7, 3, 2, 0],
    interval_pattern="W H H+W W H",
    usage="Folk songs, children's music",
    mood="Bright, playful",
)

# Sakadaira - pentatonic variant
SCALE_SAKADAIRA = JapaneseScale(
    name="Sakadaira",
    name_japanese="逆平調子",
    type="pentatonic",
    ascending=[0, 2, 5, 7, 9, 12],  # C D F G B C
    descending=[12, 9, 7, 5, 2, 0],
    interval_pattern="W H+W W H W",
    usage="Court music",
    mood="Serene, dignified",
)

# Iwato - "rock door" scale
SCALE_IWATO = JapaneseScale(
    name="Iwato",
    name_japanese="岩音",
    type="pentatonic",
    ascending=[0, 1, 5, 6, 10, 12],  # C Db F F# Ab C
    descending=[12, 10, 6, 5, 1, 0],
    interval_pattern="H H+W H H+W H",
    usage="Shinto music, ceremonial",
    mood="Sacred, ancient, dark",
)

# Yo Sen Pou - "yang" scale (rare)
SCALE_YO_SENPOU = JapaneseScale(
    name="Yo Sen Pou",
    name_japanese="陽旋法",
    type="pentatonic",
    ascending=[0, 2, 4, 7, 9, 12],  # C D E G B C (same as Hirajoushi)
    descending=[12, 9, 7, 4, 2, 0],
    interval_pattern="W W H+W W H",
    usage="Gagaku (court music)",
    mood="Bright, positive (yang)",
)

# Ryukyu - Ryukyuan scale
SCALE_RYUKYU = JapaneseScale(
    name="Ryukyu",
    name_japanese="琉球",
    type="pentatonic",
    ascending=[0, 3, 5, 7, 10, 12],  # C Eb F G Bb C
    descending=[12, 10, 7, 5, 3, 0],
    interval_pattern="H+W H W H+W H",
    usage="Okinawan folk music",
    mood="Tropical, distinctive",
)

# Nohaikake - hexatonic scale
SCALE_NOHAIKAKE = JapaneseScale(
    name="Nohaikake",
    name_japanese="附加音階",
    type="hexatonic",
    ascending=[0, 1, 4, 5, 7, 8, 12],  # C Db E F G Ab C
    descending=[12, 8, 7, 5, 4, 1, 0],
    interval_pattern="H m3 H W H W H",
    usage="Noh theater music",
    mood="Dramatic, tense",
)


# =============================================================================
# Japanese Scale Registry
# =============================================================================

JAPANESE_SCALES: dict[str, JapaneseScale] = {
    "insen": SCALE_IN_SENPOU,
    "insenpou": SCALE_IN_SENPOU,
    "in_sen_pou": SCALE_IN_SENPOU,
    "hirajoushi": SCALE_HIRAJOUSHI,
    "miyakobushi": SCALE_MIYAKOBUCHI,
    "miyako": SCALE_MIYAKOBUCHI,
    "kumoi": SCALE_KUMOI,
    "kumoi_joshi": SCALE_KUMOI,
    "sakadaira": SCALE_SAKADAIRA,
    "iwato": SCALE_IWATO,
    "yosennpou": SCALE_YO_SENPOU,
    "yo_sen_pou": SCALE_YO_SENPOU,
    "ryukyu": SCALE_RYUKYU,
    "nohaikake": SCALE_NOHAIKAKE,
}


# =============================================================================
# Helper Functions
# =============================================================================


def get_japanese_scale(name: str) -> JapaneseScale | None:
    """Get a Japanese scale by name."""
    return JAPANESE_SCALES.get(name.lower().replace(" ", "_").replace("-", "_"))


def scale_to_midi_scale(scale: JapaneseScale, root: int = 60) -> list[int]:
    """
    Convert a Japanese scale to MIDI note numbers.

    Args:
        scale: The Japanese scale
        root: Root note MIDI number (default: C4 = 60)

    Returns:
        List of MIDI note numbers for the ascending scale
    """
    return [root + semitone for semitone in scale.ascending]


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "JapaneseScale",
    "JAPANESE_SCALES",
    "SCALE_IN_SENPOU",
    "SCALE_HIRAJOUSHI",
    "SCALE_MIYAKOBUCHI",
    "SCALE_KUMOI",
    "SCALE_SAKADAIRA",
    "SCALE_IWATO",
    "SCALE_YO_SENPOU",
    "SCALE_RYUKYU",
    "SCALE_NOHAIKAKE",
    "get_japanese_scale",
    "scale_to_midi_scale",
]
