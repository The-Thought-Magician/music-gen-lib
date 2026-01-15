"""Main rendering engine."""

from __future__ import annotations

import logging
from pathlib import Path

from musicgen.ai_models import AIComposition
from musicgen.renderer.audio import AudioRenderer
from musicgen.renderer.midi import MIDIRenderer

logger = logging.getLogger(__name__)


class Renderer:
    """Main rendering engine for AIComposition.

    Converts AIComposition to MIDI and audio files.
    """

    def __init__(
        self,
        output_dir: Path = Path("."),
        soundfont_path: Path | None = None,
        sample_rate: int = 44100,
    ):
        """Initialize renderer.

        Args:
            output_dir: Default output directory
            soundfont_path: Optional SoundFont path
            sample_rate: Audio sample rate
        """
        self.output_dir = Path(output_dir)
        self.soundfont_path = soundfont_path
        self.sample_rate = sample_rate

        # Initialize renderers
        self.midi_renderer = MIDIRenderer()
        self.audio_renderer = AudioRenderer(
            soundfont_path=soundfont_path,
            sample_rate=sample_rate,
        )

    def render(
        self,
        composition: AIComposition,
        formats: list[str],
        output_name: str | None = None,
    ) -> dict[str, Path]:
        """Render composition to requested formats.

        Args:
            composition: AIComposition to render
            formats: List of formats ("midi", "wav", "mp3")
            output_name: Optional base name (uses title if None)

        Returns:
            Dict mapping format to output path
        """
        # Generate output name
        if output_name is None:
            output_name = composition.title.lower().replace(" ", "_").replace("'", "")

        results = {}

        # MIDI (needed for audio)
        if "midi" in formats or any(f in formats for f in ["wav", "mp3"]):
            midi_path = self.output_dir / f"{output_name}.mid"
            logger.info(f"Rendering MIDI to {midi_path}")
            self.midi_renderer.render(composition, midi_path)
            results["midi"] = midi_path

        # Audio formats
        if "wav" in formats:
            wav_path = self.output_dir / f"{output_name}.wav"
            logger.info(f"Rendering WAV to {wav_path}")
            self.audio_renderer.render(results["midi"], wav_path, format="wav")
            results["wav"] = wav_path

        if "mp3" in formats:
            mp3_path = self.output_dir / f"{output_name}.mp3"
            logger.info(f"Rendering MP3 to {mp3_path}")
            self.audio_renderer.render(results["midi"], mp3_path, format="mp3")
            results["mp3"] = mp3_path

        return results

    def render_to_midi(
        self,
        composition: AIComposition,
        output_path: Path,
    ) -> Path:
        """Render to MIDI file.

        Args:
            composition: AIComposition to render
            output_path: Output MIDI path

        Returns:
            Path to rendered file
        """
        self.midi_renderer.render(composition, Path(output_path))
        return output_path

    def render_to_audio(
        self,
        midi_path: Path,
        output_path: Path,
        format: str = "wav",
    ) -> Path:
        """Render MIDI file to audio.

        Args:
            midi_path: Input MIDI file
            output_path: Output audio path
            format: Audio format ("wav" or "mp3")

        Returns:
            Path to rendered file
        """
        self.audio_renderer.render(midi_path, Path(output_path), format=format)
        return output_path


# Convenience function
def render(
    composition: AIComposition,
    formats: list[str] = None,
    output_dir: Path = Path("."),
    output_name: str | None = None,
) -> dict[str, Path]:
    """Render a composition.

    Args:
        composition: AIComposition to render
        formats: List of formats (default: ["midi"])
        output_dir: Output directory
        output_name: Optional base name

    Returns:
        Dict mapping format to output path
    """
    if formats is None:
        formats = ["midi"]

    renderer = Renderer(output_dir=output_dir)
    return renderer.render(composition, formats, output_name)
