"""Enhanced MIDI generation for V3 compositions.

This module provides MIDI file generation with full SFZ support.
"""

from musicgen.midi.generator import (
    ArticulationHelper,
    EnhancedMIDIGenerator,
    export_multitrack_midi,
)

__all__ = [
    "EnhancedMIDIGenerator",
    "ArticulationHelper",
    "export_multitrack_midi",
]
