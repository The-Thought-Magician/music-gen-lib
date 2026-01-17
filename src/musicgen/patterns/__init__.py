"""
Pattern manipulation system for music-gen-lib V4.

This module provides TidalCycles-inspired pattern manipulation capabilities
including mini-notation parsing, transformation functions, and pattern combinators.
"""

from musicgen.patterns.combinators import (
    aaba,
    append,
    cat,
    choose,
    choose_by,
    degrade_by,
    fastcat,
    fold,  # alias for unfold
    freeze,
    from_dict,
    from_list,
    never,
    often,
    once,
    overlay,
    range_pattern,
    rot,
    rotate_values,
    silence,
    silence_in,
    spread,
    stack,
    unfold,
    unfreeze,
    verse_chorus,
)
from musicgen.patterns.combinators import (
    zip_patterns as zip,
)
from musicgen.patterns.parser import PatternParser, parse_pattern
from musicgen.patterns.transform import (
    degrade,
    density,
    fast,
    palindrome,
    rev,
    rotate,
    slow,
)
from musicgen.patterns.transform import (
    repeat as repeat_transform,
)
from musicgen.patterns.world_rhythms import (
    BOSSA_NOVA,
    BOSSA_NOVA_CLAVE,
    CLAVE_PATTERNS,
    RUPAK,
    SAMBA_ENREDO,
    SON_CLAVE,
    TALAS,
    TEENTAL,
    TUMBAO_MODERN,
    PolyrhythmGenerator,
    RhythmComposer,
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
    "repeat_transform",
    "degrade",
    "degrade_by",
    # Combinators
    "stack",
    "cat",
    "fastcat",
    "overlay",
    "choose",
    "choose_by",
    "zip",
    "append",
    # Utilities
    "silence",
    "repeat_transform",
    "silence_in",
    "freeze",
    "unfold",
    "unfreeze",
    "once",
    "every",
    "range_pattern",
    "sometimes",
    "often",
    "rarely",
    "never",
    "sometimes_cycle",
    # Construction
    "from_list",
    "from_dict",
    "spread",
    "rot",
    "rotate_values",
    # Structural
    "verse_chorus",
    "aaba",
    "fold",
    # World Rhythms
    "Tala",
    "TEENTAL",
    "TALAS",
    "PolyrhythmGenerator",
    "RhythmComposer",
    "SON_CLAVE",
    "CLAVE_PATTERNS",
    "SAMBA_ENREDO",
    "BOSSA_NOVA",
    "TUMBAO_MODERN",
]
