"""
Pattern manipulation system for music-gen-lib V4.

This module provides TidalCycles-inspired pattern manipulation capabilities
including mini-notation parsing, transformation functions, and pattern combinators.
"""

from musicgen.patterns.parser import PatternParser, parse_pattern
from musicgen.patterns.transform import (
    degrade,
    degrade_by,
    density,
    fast,
    palindrome,
    repeat,
    rev,
    rotate,
    slow,
)

__all__ = [
    # Parser
    "PatternParser",
    "parse_pattern",
    # Transform functions
    "slow",
    "fast",
    "density",
    "rev",
    "palindrome",
    "rotate",
    "repeat",
    "degrade",
    "degrade_by",
]
