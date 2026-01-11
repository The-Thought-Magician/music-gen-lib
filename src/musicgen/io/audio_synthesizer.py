"""Audio synthesis module.

This module provides functionality for synthesizing audio from MIDI.
"""

from __future__ import annotations
from typing import Optional, List
from dataclasses import dataclass
from pathlib import Path
import subprocess


@dataclass
class AudioSynthesizer:
    """Synthesizes audio from MIDI files using FluidSynth or similar.

    Attributes:
        soundfont_path: Path to SoundFont file
        sample_rate: Audio sample rate
    """

    soundfont_path: Optional[str] = None
    sample_rate: int = 44100

    @staticmethod
    def find_soundfont() -> Optional[str]:
        """Find a SoundFont file in common locations.

        Returns:
            Path to SoundFont or None
        """
        possible_paths = [
            "/usr/share/sounds/sf2/FluidR3_GM.sf2",
            "/usr/share/soundfonts/FluidR3_GM.sf2",
            "/usr/share/sounds/sf2/FluidR3.GM.sf2",
            "~/fluid-soundfont/FluidR3_GM.sf2",
        ]

        for path in possible_paths:
            expanded = Path(path).expanduser()
            if expanded.exists():
                return str(expanded)

        return None

    def render(self, midi_file: str, output_file: str = "",
               output_format: str = "wav", normalize: bool = True) -> str:
        """Render a MIDI file to audio.

        Args:
            midi_file: Path to input MIDI file
            output_file: Path to output audio file
            output_format: Output format ("wav", "flac", "ogg")
            normalize: Whether to normalize the audio

        Returns:
            Path to rendered audio file
        """
        # Generate output filename if not provided
        if not output_file:
            midi_path = Path(midi_file)
            output_file = str(midi_path.with_suffix(f".{output_format}"))

        # Find soundfont
        soundfont = self.soundfont_path or self.find_soundfont()

        if soundfont is None:
            raise RuntimeError(
                "No SoundFont found. Please specify a soundfont_path "
                "or install fluid-soundfont."
            )

        # Try to use FluidSynth
        try:
            result = subprocess.run(
                [
                    "fluidsynth",
                    "-ni", soundfont,
                    midi_file,
                    "-F", output_file,
                    "-r", str(self.sample_rate)
                ],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                # Try alternative command format
                result = subprocess.run(
                    [
                        "fluidsynth",
                        "-T", output_format,
                        "-F", output_file,
                        "-r", str(self.sample_rate),
                        soundfont,
                        midi_file
                    ],
                    capture_output=True,
                    text=True
                )

            if result.returncode != 0:
                raise RuntimeError(f"FluidSynth failed: {result.stderr}")

        except FileNotFoundError:
            raise RuntimeError(
                "FluidSynth not found. Please install fluidsynth:\n"
                "  Ubuntu/Debian: sudo apt install fluidsynth\n"
                "  macOS: brew install fluidsynth"
            )

        return output_file

    def render_to_memory(self, midi_file: str) -> bytes:
        """Render MIDI to audio in memory.

        Args:
            midi_file: Path to input MIDI file

        Returns:
            Audio data as bytes
        """
        import tempfile
        import numpy as np

        # Render to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            self.render(midi_file, tmp.name, "wav")

            # Read back
            with open(tmp.name, "rb") as f:
                return f.read()

    @staticmethod
    def is_available() -> bool:
        """Check if FluidSynth is available.

        Returns:
            True if FluidSynth is installed
        """
        try:
            result = subprocess.run(
                ["fluidsynth", "--version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
