"""
World music scales for music-gen-lib V4.

This module provides scale definitions for Indian ragas, Arabic maqamat,
Japanese scales, and other non-Western scale systems.
"""

from musicgen.scales.arabic import (
    ARABIC_MAQAMAT,
    MAQAM_BAYATI,
    MAQAM_HIJAZ,
    MAQAM_RAST,
    MAQAM_SIKAH,
    get_maqam_by_name,
)
from musicgen.scales.indian import (
    INDIAN_RAGAS,
    RAGA_BHAIRAV,
    RAGA_BHAIRAVI,
    RAGA_TODI,
    RAGA_YAMAN,
    get_raga_by_name,
    get_ragas_by_that,
)
from musicgen.scales.japanese import (
    JAPANESE_SCALES,
    SCALE_HIRAJOUSHI,
    SCALE_IN_SENPOU,
    SCALE_KUMOI,
    SCALE_MIYAKOBUCHI,
)
from musicgen.scales.pentatonic import (
    PENTATONIC_SCALES,
    SCALE_BLUES,
    SCALE_MAJOR_PENTATONIC,
    SCALE_MINOR_PENTATONIC,
    get_pentatonic_scale,
)

__all__ = [
    # Indian
    "INDIAN_RAGAS",
    "RAGA_YAMAN",
    "RAGA_BHAIRAVI",
    "RAGA_BHAIRAV",
    "RAGA_TODI",
    "get_raga_by_name",
    "get_ragas_by_that",
    # Arabic
    "ARABIC_MAQAMAT",
    "MAQAM_HIJAZ",
    "MAQAM_RAST",
    "MAQAM_SIKAH",
    "MAQAM_BAYATI",
    "get_maqam_by_name",
    # Japanese
    "JAPANESE_SCALES",
    "SCALE_IN_SENPOU",
    "SCALE_HIRAJOUSHI",
    "SCALE_MIYAKOBUCHI",
    "SCALE_KUMOI",
    # Pentatonic
    "PENTATONIC_SCALES",
    "SCALE_MAJOR_PENTATONIC",
    "SCALE_MINOR_PENTATONIC",
    "SCALE_BLUES",
    "get_pentatonic_scale",
]
