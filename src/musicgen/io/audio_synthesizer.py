"""Audio synthesis module for converting MIDI to audio formats.

This module provides functionality for synthesizing audio from MIDI files
using FluidSynth and converting to various formats (WAV, MP3, FLAC).
"""

from __future__ import annotations
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, List
import struct

try:
    import pydub
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

from musicgen.io.soundfont import get_soundfont_manager, ensure_soundfont


class AudioSynthesizer:
    """Synthesizes audio from MIDI using FluidSynth."""

    def __init__(
        self,
        soundfont_path: Optional[str | Path] = None,
        sample_rate: int = 44100,
        bits: int = 16,
        channels: int = 2
    ):
        """Initialize the audio synthesizer.

        Args:
            soundfont_path: Path to SoundFont file. If None, uses default.
            sample_rate: Output sample rate in Hz.
            bits: Bit depth (16 or 24 or 32).
            channels: Number of audio channels (1=mono, 2=stereo).
        """
        self.soundfont_path = Path(soundfont_path) if soundfont_path else None
        self.sample_rate = sample_rate
        self.bits = bits
        self.channels = channels

        # Get default SoundFont if not specified
        if self.soundfont_path is None:
            self.soundfont_path = ensure_soundfont()

        # Verify SoundFont exists
        if not self.soundfont_path.exists():
            raise RuntimeError(
                f"SoundFont not found: {self.soundfont_path}\n"
                f"Please install a SoundFont or run the downloader."
            )

    def render(
        self,
        midi_path: str | Path,
        output_path: Optional[str | Path] = None,
        output_format: str = "wav"
    ) -> str:
        """Render a MIDI file to audio.

        Args:
            midi_path: Path to input MIDI file.
            output_path: Path for output audio file. If None, uses MIDI filename.
            output_format: Output format (wav, mp3, flac, ogg).

        Returns:
            Path to the generated audio file.

        Raises:
            RuntimeError: If FluidSynth is not available or rendering fails.
        """
        midi_path = Path(midi_path)

        # Determine output path
        if output_path is None:
            output_path = midi_path.with_suffix(f".{output_format}")
        else:
            output_path = Path(output_path)

        # First generate WAV using FluidSynth
        wav_path = self._render_with_fluidsynth(midi_path)

        # Convert if needed
        if output_format.lower() != "wav":
            wav_path = self._convert_audio(wav_path, output_path, output_format)
        else:
            # Normalize the WAV
            wav_path = self._normalize_audio(wav_path, output_path)

        return str(wav_path)

    def _render_with_fluidsynth(self, midi_path: Path) -> Path:
        """Render MIDI to WAV using FluidSynth.

        Args:
            midi_path: Path to input MIDI file.

        Returns:
            Path to generated WAV file.

        Raises:
            RuntimeError: If FluidSynth is not available.
        """
        # Output to temp file first
        output_path = midi_path.with_suffix(".wav")

        # Build FluidSynth command
        cmd = [
            "fluidsynth",
            "-ni",  # No interactive mode
            str(self.soundfont_path),
            str(midi_path),
            "-F", str(output_path),
            "-r", str(self.sample_rate),
        ]

        # Add options for quality
        if self.channels == 1:
            cmd.insert(1, "-g")  # Gain for mono
        if self.bits == 24:
            cmd.extend(["-O", "24bit"])

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"FluidSynth failed: {e.stderr}\n"
                f"Ensure FluidSynth is installed: sudo apt install fluidsynth"
            )
        except FileNotFoundError:
            raise RuntimeError(
                "FluidSynth not found. Install it with:\n"
                "  Ubuntu/Debian: sudo apt install fluidsynth\n"
                "  macOS: brew install fluidsynth\n"
                "  Windows: Download from https://github.com/FluidSynth/fluidsynth/releases"
            )

        if not output_path.exists():
            raise RuntimeError(f"FluidSynth did not create output file: {output_path}")

        return output_path

    def _convert_audio(
        self,
        input_path: Path,
        output_path: Path,
        output_format: str
    ) -> Path:
        """Convert audio to a different format.

        Args:
            input_path: Input audio file.
            output_path: Desired output path.
            output_format: Target format.

        Returns:
            Path to converted file.
        """
        if not PYDUB_AVAILABLE:
            # Try using ffmpeg directly
            return self._convert_with_ffmpeg(input_path, output_path, output_format)

        # Use pydub
        audio = AudioSegment.from_wav(input_path)

        # Normalize
        audio = audio.normalize()

        # Export
        if output_format.lower() == "mp3":
            audio.export(output_path, format="mp3", bitrate="192k")
        elif output_format.lower() == "flac":
            audio.export(output_path, format="flac")
        elif output_format.lower() == "ogg":
            audio.export(output_path, format="ogg", codec="libvorbis")
        else:
            audio.export(output_path, format=output_format.lower())

        return output_path

    def _convert_with_ffmpeg(
        self,
        input_path: Path,
        output_path: Path,
        output_format: str
    ) -> Path:
        """Convert audio using ffmpeg directly.

        Args:
            input_path: Input audio file.
            output_path: Desired output path.
            output_format: Target format.

        Returns:
            Path to converted file.

        Raises:
            RuntimeError: If ffmpeg is not available.
        """
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output
            "-i", str(input_path),
        ]

        # Add normalization filter
        cmd.extend(["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"])

        # Output format specific options
        if output_format.lower() == "mp3":
            cmd.extend(["-codec:a", "libmp3lame", "-b:a", "192k"])
        elif output_format.lower() == "flac":
            cmd.extend(["-codec:a", "flac"])

        cmd.append(str(output_path))

        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"ffmpeg conversion failed: {e.stderr}\n"
                f"Install ffmpeg: sudo apt install ffmpeg"
            )
        except FileNotFoundError:
            # ffmpeg not available, just return the wav
            return input_path

        return output_path

    def _normalize_audio(self, input_path: Path, output_path: Path) -> Path:
        """Normalize audio file.

        Args:
            input_path: Input audio file.
            output_path: Output path for normalized audio.

        Returns:
            Path to normalized file.
        """
        if PYDUB_AVAILABLE:
            audio = AudioSegment.from_wav(input_path)
            normalized = audio.normalize()
            normalized.export(output_path, format="wav")
            return output_path
        else:
            # Just copy if pydub not available
            import shutil
            shutil.copy2(input_path, output_path)
            return output_path

    def render_to_memory(self, midi_path: str | Path) -> bytes:
        """Render MIDI to audio in memory.

        Args:
            midi_path: Path to input MIDI file.

        Returns:
            WAV audio data as bytes.

        Raises:
            RuntimeError: If rendering fails.
        """
        midi_path = Path(midi_path)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            self._render_with_fluidsynth(midi_path)
            wav_data = tmp_path.read_bytes()
            return wav_data
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

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


def check_audio_support() -> dict:
    """Check what audio synthesis support is available.

    Returns:
        Dictionary with availability status:
        - fluidsynth: bool
        - pydub: bool
        - ffmpeg: bool
        - soundfont: bool or path
    """
    result = {
        "fluidsynth": False,
        "pydub": PYDUB_AVAILABLE,
        "ffmpeg": False,
        "soundfont": None
    }

    # Check FluidSynth
    try:
        subprocess.run(
            ["fluidsynth", "--version"],
            check=True,
            capture_output=True
        )
        result["fluidsynth"] = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Check ffmpeg
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            check=True,
            capture_output=True
        )
        result["ffmpeg"] = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Check SoundFont
    sf_manager = get_soundfont_manager()
    sf_path = sf_manager.get_soundfont_path()
    result["soundfont"] = sf_path if sf_path else False

    return result


def get_default_synthesizer() -> AudioSynthesizer:
    """Get a default AudioSynthesizer instance.

    Returns:
        Configured AudioSynthesizer.

    Raises:
        RuntimeError: If audio synthesis is not properly set up.
    """
    support = check_audio_support()

    if not support["fluidsynth"]:
        raise RuntimeError(
            "FluidSynth is required for audio synthesis.\n"
            "Install it with: sudo apt install fluidsynth (Linux)\n"
            "              brew install fluidsynth (macOS)"
        )

    if not support["soundfont"]:
        # Try to download
        ensure_soundfont()

    return AudioSynthesizer()
