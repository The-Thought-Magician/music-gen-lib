"""Main music generation module.

This module provides the primary interface for generating music compositions.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from pathlib import Path

from musicgen.composition.melody import MelodicContour, MelodyGenerator
from musicgen.config.moods import get_mood_preset, list_moods
from musicgen.core.note import QUARTER, Note
from musicgen.io.lilypond_writer import LilyPondWriter
from musicgen.io.midi_writer import MIDIWriter, Part, Score
from musicgen.io.musicxml_writer import MusicXMLWriter
from musicgen.theory.keys import Key
from musicgen.theory.progressions import Progression
from musicgen.theory.scales import Scale


@dataclass
class CompositionRequest:
    """Request parameters for music generation.

    Attributes:
        mood: The mood preset to use
        key: The key (overrides mood preset)
        scale: The scale type (overrides mood preset)
        tempo: Tempo in BPM (overrides mood preset)
        duration: Duration in seconds
        instruments: List of instrument names (overrides mood preset)
        title: Composition title
        composer: Composer name
        output_dir: Output directory for files
        export_formats: List of formats to export ("midi", "audio", "musicxml", "pdf")
        seed: Random seed for reproducibility
    """

    mood: str = "peaceful"
    key: str | None = None
    scale: str | None = None
    tempo: int | None = None
    duration: int = 30
    instruments: list[str] | None = None
    title: str = ""
    composer: str = "MusicGen"
    output_dir: str = "."
    export_formats: list[str] = field(default_factory=lambda: ["midi"])
    seed: int | None = None


@dataclass
class CompositionResult:
    """Result of a music generation request.

    Attributes:
        score: The generated score
        key: The key used
        scale_type: The scale type used
        tempo: The tempo used
        instruments: List of instruments used
        midi_path: Path to MIDI file
        audio_path: Path to audio file
        musicxml_path: Path to MusicXML file
        pdf_path: Path to PDF file
        title: Composition title
    """

    score: Score
    key: str
    scale_type: str
    tempo: int
    instruments: list[str]
    midi_path: str | None = None
    audio_path: str | None = None
    musicxml_path: str | None = None
    pdf_path: str | None = None
    title: str = ""


def generate(request: CompositionRequest) -> CompositionResult:
    """Generate a complete music composition.

    Args:
        request: The composition request parameters

    Returns:
        A CompositionResult with the generated music
    """
    # Get mood preset
    preset = get_mood_preset(request.mood)

    # Set seed for reproducibility BEFORE any random operations
    if request.seed is not None:
        random.seed(request.seed)

    # Determine parameters
    key_name = request.key or preset.key
    scale_type = request.scale or preset.scale
    tempo = request.tempo or random.randint(preset.tempo_min, preset.tempo_max)
    instrument_names = request.instruments or preset.instruments[:4]
    title = request.title or f"{request.mood.capitalize()} Composition"

    # Parse key name to extract tonic (remove 'm' suffix like "Am" -> "A")
    tonic = key_name.strip().upper()
    if tonic.endswith("M"):
        tonic = tonic[:-1]  # Remove trailing 'M' from keys like "AM"

    # Determine key type from scale or suffix
    if "minor" in scale_type.lower() or key_name.lower().endswith("m") and "major" not in scale_type.lower():
        key_type = "minor"
    else:
        key_type = "major"

    # Create music elements
    key = Key(tonic, key_type)
    scale = Scale(tonic, scale_type)
    progression = Progression.functional(key=key, length=8)

    # Generate melody
    melody_gen = MelodyGenerator(scale, key, tempo=tempo)
    melody_gen.set_seed(request.seed or random.randint(1, 10000))
    melody = melody_gen.generate_melody(
        progression=progression,
        contour=MelodicContour.WAVE,
        motivic_unity=0.75
    )

    # Calculate number of notes for duration
    # At tempo BPM, quarter notes per second = tempo / 60
    quarters_per_second = tempo / 60
    total_quarters = int(request.duration * quarters_per_second)
    notes_to_generate = total_quarters

    # Extend melody if needed
    while melody.length < notes_to_generate:
        additional = melody_gen.generate_motif(8, MelodicContour.WAVE)
        melody.notes.extend(additional.notes)

    # Trim to target duration
    melody.notes = melody.notes[:notes_to_generate]

    # Create score with parts
    score = Score(title=title, composer=request.composer)

    # Add melody part
    melody_part = Part(name="melody")
    melody_part.notes = melody.notes
    score.add_part(melody_part)

    # Add accompaniment parts for remaining instruments
    for inst_name in instrument_names[1:4]:
        accompaniment_part = Part(name=inst_name)
        # Generate simple accompaniment from chord progression
        for chord in progression.chords:
            for note in chord.notes[:2]:  # Root and third
                n = Note(note.name, note.octave - 1, QUARTER)
                accompaniment_part.add_note(n)
        score.add_part(accompaniment_part)

    # Create output directory
    output_path = Path(request.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Export files
    midi_path = None
    audio_path = None
    musicxml_path = None
    pdf_path = None

    base_name = title.lower().replace(" ", "_")

    if "midi" in request.export_formats:
        midi_path = str(output_path / f"{base_name}.mid")
        MIDIWriter.write(score, midi_path, tempo=tempo)

    if "audio" in request.export_formats and midi_path:
        from musicgen.io.audio_synthesizer import AudioSynthesizer
        try:
            synth = AudioSynthesizer()
            audio_path = synth.render(midi_path, output_format="wav")
        except RuntimeError:
            audio_path = None  # FluidSynth not available

    if "musicxml" in request.export_formats:
        musicxml_path = str(output_path / f"{base_name}.musicxml")
        MusicXMLWriter.write(score, musicxml_path)

    if "pdf" in request.export_formats:
        pdf_path = str(output_path / f"{base_name}.pdf")
        ly_path = str(output_path / f"{base_name}.ly")
        try:
            LilyPondWriter.write(
                score,
                output_ly=ly_path,
                output_pdf=pdf_path,
                title=title,
                composer=request.composer
            )
        except RuntimeError:
            pdf_path = None  # LilyPond not available

    return CompositionResult(
        score=score,
        key=f"{tonic} {key_type}",
        scale_type=scale_type,
        tempo=tempo,
        instruments=instrument_names,
        midi_path=midi_path,
        audio_path=audio_path,
        musicxml_path=musicxml_path,
        pdf_path=pdf_path,
        title=title
    )


def list_available_moods() -> list[str]:
    """Return list of available mood presets.

    Returns:
        List of mood names
    """
    return list_moods()
