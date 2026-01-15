"""Music Generation Library - Rule-based orchestral music composition.

This library generates orchestral music using traditional music theory
principles including scales, chords, progressions, voice leading, and
musical forms.
"""

__version__ = "0.1.0"

# Core exports
from musicgen.composition.forms import Form, FormType, Section

# Composition exports
from musicgen.composition.melody import (
    MelodicContour,
    Melody,
    MelodyGenerator,
    Motif,
    Phrase,
)

# Config exports
from musicgen.config.moods import MoodPreset, get_mood_preset, list_moods
from musicgen.core.chord import (
    AUGMENTED,
    DIMINISHED,
    DIMINISHED_SEVENTH,
    DOMINANT_SEVENTH,
    HALF_DIMINISHED,
    MAJOR,
    MAJOR_SEVENTH,
    MINOR,
    MINOR_SEVENTH,
    Chord,
)
from musicgen.core.note import (
    DOTTED_EIGHTH,
    DOTTED_HALF,
    DOTTED_QUARTER,
    EIGHTH,
    FF,
    HALF,
    MF,
    MP,
    PP,
    QUARTER,
    SIXTEENTH,
    TRIPLET_EIGHTH,
    TRIPLET_HALF,
    TRIPLET_QUARTER,
    WHOLE,
    F,
    Note,
    P,
    Rest,
)

# Main generator
from musicgen.generator import CompositionRequest, CompositionResult, generate
from musicgen.io.audio_synthesizer import AudioSynthesizer
from musicgen.io.lilypond_writer import LilyPondWriter

# IO exports
from musicgen.io.midi_writer import MIDIWriter, Part, Score
from musicgen.io.musicxml_writer import MusicXMLWriter
from musicgen.orchestration.ensembles import Ensemble, Texture, TextureType

# Orchestration exports
from musicgen.orchestration.instruments import Instrument, InstrumentFamily, Voice
from musicgen.theory.keys import Key, KeySignature
from musicgen.theory.progressions import Progression

# Theory exports
from musicgen.theory.scales import Scale, ScaleType

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
