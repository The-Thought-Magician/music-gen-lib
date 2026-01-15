"""AI Composer module."""

from musicgen.composer_new.composer import (
    AIComposer,
    ValidationError,
    compose,
    compose_from_file,
)
from musicgen.composer_new.presets import (
    MODIFIERS,
    PRESETS,
    apply_modifier,
    get_preset,
    list_presets,
)

__all__ = [
    "AIComposer",
    "ValidationError",
    "compose",
    "compose_from_file",
    "get_preset",
    "list_presets",
    "apply_modifier",
    "PRESETS",
    "MODIFIERS",
]
