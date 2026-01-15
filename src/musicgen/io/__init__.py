"""Input/output module.

This module provides classes for writing music to various formats.
"""

from musicgen.io.audio_synthesizer import AudioSynthesizer
from musicgen.io.lilypond_writer import LilyPondWriter
from musicgen.io.midi_writer import MIDIWriter, Part, Score
from musicgen.io.musicxml_writer import MusicXMLWriter

__all__ = [
    "MIDIWriter",
    "Part",
    "Score",
    "AudioSynthesizer",
    "MusicXMLWriter",
    "LilyPondWriter",
]
