"""Music theory module.

This module provides classes for scales, keys, and chord progressions.
"""

from musicgen.theory.keys import Key, KeySignature
from musicgen.theory.progressions import Progression
from musicgen.theory.scales import Scale, ScaleType

__all__ = [
    "Scale",
    "ScaleType",
    "Key",
    "KeySignature",
    "Progression",
]
