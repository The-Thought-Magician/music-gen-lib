"""Music Generation Library - Rule-based orchestral music composition.

This library generates orchestral music using traditional music theory
principles including scales, chords, progressions, voice leading, and
musical forms.
"""

__version__ = "0.1.0"

# Core exports
from musicgen.core.note import Note, Rest
from musicgen.core.note import (
    WHOLE, HALF, QUARTER, EIGHTH, SIXTEENTH,
    DOTTED_HALF, DOTTED_QUARTER, DOTTED_EIGHTH,
    TRIPLET_HALF, TRIPLET_QUARTER, TRIPLET_EIGHTH,
    PP, P, MP, MF, F, FF,
)
from musicgen.core.chord import Chord
from musicgen.core.chord import (
    MAJOR, MINOR, DIMINISHED, AUGMENTED,
    MAJOR_SEVENTH, MINOR_SEVENTH, DOMINANT_SEVENTH,
    DIMINISHED_SEVENTH, HALF_DIMINISHED,
)

# Theory exports
from musicgen.theory.scales import Scale, ScaleType
from musicgen.theory.keys import Key, KeySignature
from musicgen.theory.progressions import Progression

# Composition exports
from musicgen.composition.melody import (
    MelodicContour, Motif, Phrase, Melody, MelodyGenerator,
)
from musicgen.composition.forms import FormType, Section, Form

# Orchestration exports
from musicgen.orchestration.instruments import Instrument, InstrumentFamily, Voice
from musicgen.orchestration.ensembles import Texture, TextureType, Ensemble

# IO exports
from musicgen.io.midi_writer import MIDIWriter, Part, Score
from musicgen.io.audio_synthesizer import AudioSynthesizer
from musicgen.io.musicxml_writer import MusicXMLWriter
from musicgen.io.lilypond_writer import LilyPondWriter

# Config exports
from musicgen.config.moods import MoodPreset, get_mood_preset, list_moods

# Main generator
from musicgen.generator import generate, CompositionRequest, CompositionResult


__all__ = [
    # Version
    "__version__",
    # Core classes
    "Note", "Rest", "Chord",
    # Durations
    "WHOLE", "HALF", "QUARTER", "EIGHTH", "SIXTEENTH",
    "DOTTED_HALF", "DOTTED_QUARTER", "DOTTED_EIGHTH",
    "TRIPLET_HALF", "TRIPLET_QUARTER", "TRIPLET_EIGHTH",
    # Dynamics
    "PP", "P", "MP", "MF", "F", "FF",
    # Chord qualities
    "MAJOR", "MINOR", "DIMINISHED", "AUGMENTED",
    "MAJOR_SEVENTH", "MINOR_SEVENTH", "DOMINANT_SEVENTH",
    "DIMINISHED_SEVENTH", "HALF_DIMINISHED",
    # Theory
    "Scale", "ScaleType", "Key", "KeySignature", "Progression",
    # Composition
    "MelodicContour", "Motif", "Phrase", "Melody", "MelodyGenerator",
    "FormType", "Section", "Form",
    # Orchestration
    "Instrument", "InstrumentFamily", "Voice",
    "Texture", "TextureType", "Ensemble",
    # IO
    "MIDIWriter", "Part", "Score",
    "AudioSynthesizer",
    "MusicXMLWriter",
    "LilyPondWriter",
    # Config
    "MoodPreset", "get_mood_preset", "list_moods",
    # Main generator
    "generate", "CompositionRequest", "CompositionResult",
]
