"""SFZ renderer integration for V3 music generation system.

This module provides Python wrappers around sfizz-render for rendering
MIDI files to audio using SFZ format sample libraries.

The renderer supports:
- Single-instrument rendering with SFZ libraries
- Multi-instrument compositions with separate SFZ files per channel
- Audio post-processing (normalization, fade out)
- Stem export for individual instruments
"""

from __future__ import annotations

import contextlib
import logging
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

logger = logging.getLogger(__name__)


class SFZRendererError(RuntimeError):
    """Base exception for SFZ renderer errors."""

    pass


class SFZNotFoundError(SFZRendererError):
    """Raised when SFZ file is not found."""

    pass


class SFZRenderError(SFZRendererError):
    """Raised when sfizz-render process fails."""

    pass


class SFZNotAvailableError(SFZRendererError):
    """Raised when sfizz-render is not installed."""

    pass


class SFZRenderer:
    """Render MIDI files to audio using sfizz-render.

    This class wraps the sfizz-render command-line tool, providing
    a Python interface for rendering MIDI to audio with SFZ libraries.

    Example:
        >>> renderer = SFZRenderer(
        ...     libraries_root=Path("resources/sfz_libraries"),
        ...     sample_rate=44100
        ... )
        >>> output = renderer.render(
        ...     midi_path=Path("composition.mid"),
        ...     output_path=Path("output.wav"),
        ...     sfz_file=Path("VSL/Violin.sfz")
        ... )
    """

    def __init__(
        self,
        sfizz_path: str | Path = "sfizz_render",
        libraries_root: Path | str | None = None,
        sample_rate: int = 44100,
        bit_depth: int = 24,
    ):
        """Initialize SFZ renderer.

        Args:
            sfizz_path: Path to sfizz-render executable or command name
            libraries_root: Root directory for SFZ libraries
            sample_rate: Output sample rate in Hz
            bit_depth: Output bit depth (16 or 24)

        Raises:
            SFZNotAvailableError: If sfizz-render is not installed
        """
        self.sfizz_path = str(sfizz_path)
        self.libraries_root = (
            Path(libraries_root) if libraries_root else Path("resources/sfz_libraries")
        )
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth

        # Verify sfizz is available
        self._check_sfizz_available()

    def _check_sfizz_available(self) -> None:
        """Verify sfizz-render is installed and accessible.

        Raises:
            SFZNotAvailableError: If sfizz-render is not found or fails to run
        """
        # First check if command exists
        if not shutil.which(self.sfizz_path):
            raise SFZNotAvailableError(
                "sfizz-render not found. "
                "Install with: sudo apt install sfizz (Linux) or brew install sfizz (macOS)"
            )

        # Try to run it
        try:
            result = subprocess.run(
                [self.sfizz_path, "--help"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            # sfizz returns 0 even for --help, but non-zero for errors
            if result.returncode != 0 and "sfizz" not in result.stderr.lower():
                raise SFZNotAvailableError(
                    f"sfizz-render exists but failed to run. "
                    f"Output: {result.stderr}"
                )
        except subprocess.TimeoutExpired as err:
            raise SFZNotAvailableError("sfizz-render timed out during availability check") from err
        except FileNotFoundError as err:
            raise SFZNotAvailableError(
                f"sfizz-render not found at '{self.sfizz_path}'. "
                f"Install with: sudo apt install sfizz (Linux) or brew install sfizz (macOS)"
            ) from err

    def render(
        self,
        midi_path: Path | str,
        output_path: Path | str,
        sfz_file: Path | str,
        normalize: bool = True,
        fade_out: float = 0.0,
        extra_args: list[str] | None = None,
    ) -> Path:
        """Render a MIDI file to audio using an SFZ library.

        Args:
            midi_path: Input MIDI file path
            output_path: Output audio file path
            sfz_file: SFZ instrument definition file (relative to libraries_root or absolute)
            normalize: Normalize output audio to -0.1 dBFS
            fade_out: Fade out duration in seconds at the end
            extra_args: Additional arguments to pass to sfizz-render

        Returns:
            Path to rendered audio file

        Raises:
            SFZNotFoundError: If SFZ file is not found
            SFZRenderError: If rendering fails
        """
        midi_path = Path(midi_path)
        output_path = Path(output_path)

        if not midi_path.exists():
            raise FileNotFoundError(f"MIDI file not found: {midi_path}")

        # Create output directory
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Resolve SFZ path
        sfz_path = self._resolve_sfz_path(sfz_file)

        # Build command
        cmd = [
            self.sfizz_path,
            str(midi_path),
            str(output_path),
            f"--soundfont={sfz_path}",
            f"--sample-rate={self.sample_rate}",
        ]

        if extra_args:
            cmd.extend(extra_args)

        logger.debug(f"Rendering with command: {' '.join(cmd)}")

        # Execute sfizz-render
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                check=False,
            )
        except subprocess.TimeoutExpired as e:
            raise SFZRenderError("sfizz-render timed out after 5 minutes") from e
        except FileNotFoundError as err:
            raise SFZNotAvailableError(
                f"sfizz-render not found at '{self.sfizz_path}'"
            ) from err

        # Check result
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Unknown error"
            raise SFZRenderError(f"sfizz-render failed with code {result.returncode}: {error_msg}")

        # Verify output was created
        if not output_path.exists():
            raise SFZRenderError(
                f"sfizz-render completed but output file not created: {output_path}"
            )

        # Post-process
        if normalize or fade_out > 0:
            self._post_process(output_path, normalize=normalize, fade_out=fade_out)

        logger.info(f"Rendered {midi_path} to {output_path}")
        return output_path

    def _resolve_sfz_path(self, sfz_file: Path | str) -> Path:
        """Resolve SFZ file path relative to libraries root.

        Args:
            sfz_file: SFZ file path (relative or absolute)

        Returns:
            Resolved absolute Path to SFZ file

        Raises:
            SFZNotFoundError: If SFZ file is not found
        """
        sfz_file = Path(sfz_file)

        if sfz_file.is_absolute():
            if sfz_file.exists():
                return sfz_file
            raise SFZNotFoundError(f"SFZ file not found at absolute path: {sfz_file}")

        # Check in libraries root
        resolved = self.libraries_root / sfz_file
        if resolved.exists():
            return resolved

        # Try as library name (look for sfz file in subdirectory)
        if self.libraries_root.exists():
            # Search recursively
            for candidate in self.libraries_root.rglob("*.sfz"):
                if sfz_file.name in candidate.name or sfz_file.name in str(candidate):
                    return candidate

        raise SFZNotFoundError(
            f"SFZ file not found: {sfz_file} (searched in {self.libraries_root})"
        )

    def _post_process(
        self,
        audio_path: Path,
        normalize: bool = True,
        fade_out: float = 0.0,
    ) -> None:
        """Post-process audio file with normalization and fade out.

        Args:
            audio_path: Path to audio file to process
            normalize: Normalize to -0.1 dBFS
            fade_out: Add fade out at end (seconds)
        """
        try:
            from pydub import AudioSegment
        except ImportError:
            logger.warning("pydub not available, skipping post-processing")
            return

        try:
            audio = AudioSegment.from_wav(str(audio_path))
        except Exception as e:
            logger.error(f"Failed to load audio for post-processing: {e}")
            return

        original_length = len(audio)

        if normalize:
            # Normalize to -0.1 dBFS
            try:
                target_dBFS = -0.1
                change_in_dBFS = target_dBFS - audio.dBFS
                audio = audio.apply_gain(change_in_dBFS)
            except Exception as e:
                logger.warning(f"Normalization failed: {e}")

        if fade_out > 0:
            # Add fade out
            try:
                fade_ms = int(fade_out * 1000)
                # Don't fade longer than the audio
                fade_ms = min(fade_ms, original_length)
                audio = audio.fade_out(fade_ms)
            except Exception as e:
                logger.warning(f"Fade out failed: {e}")

        # Export back to same path
        try:
            audio.export(
                str(audio_path),
                format="wav",
                parameters=["-ar", str(self.sample_rate)],
            )
        except Exception as e:
            logger.error(f"Failed to export post-processed audio: {e}")


class MultiInstrumentRenderer:
    """Render compositions with multiple SFZ instruments.

    This class handles multi-channel MIDI files where each channel
    represents a different instrument with its own SFZ library.

    Example:
        >>> renderer = SFZRenderer()
        >>> multi = MultiInstrumentRenderer(renderer)
        >>>
        >>> mapping = {
        ...     0: Path("VSL/Violin.sfz"),
        ...     1: Path("VSL/Cello.sfz"),
        ...     2: Path("VSL/Flute.sfz"),
        ... }
        >>>
        >>> output = multi.render_composition(
        ...     midi_path=Path("orchestral.mid"),
        ...     output_path=Path("orchestral.wav"),
        ...     instrument_mapping=mapping,
        ...     render_stems=True
        ... )
    """

    def __init__(
        self,
        renderer: SFZRenderer | None = None,
        temp_dir: Path | str | None = None,
    ):
        """Initialize multi-instrument renderer.

        Args:
            renderer: SFZRenderer instance (creates default if None)
            temp_dir: Temporary directory for intermediate files
        """
        if renderer is None:
            renderer = SFZRenderer()

        self.renderer = renderer
        self.temp_dir = (
            Path(temp_dir) if temp_dir else Path(tempfile.gettempdir()) / "musicgen_renders"
        )
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def render_composition(
        self,
        midi_path: Path | str,
        output_path: Path | str,
        instrument_mapping: Mapping[int, Path | str | None],
        render_stems: bool = False,
        stem_output_dir: Path | str | None = None,
        normalize: bool = True,
        fade_out: float = 0.0,
    ) -> Path:
        """Render a multi-instrument composition.

        Each MIDI channel is rendered separately with its assigned SFZ library,
        then mixed together into a final output.

        Args:
            midi_path: Input MIDI file (16 channels)
            output_path: Final mixed output path
            instrument_mapping: Channel to SFZ file mapping (channel 0-15)
            render_stems: Also export individual instrument stems
            stem_output_dir: Directory for stem files (uses temp_dir if None)
            normalize: Normalize final output
            fade_out: Fade out duration in seconds

        Returns:
            Path to final mixed audio file
        """
        midi_path = Path(midi_path)
        output_path = Path(output_path)

        if not midi_path.exists():
            raise FileNotFoundError(f"MIDI file not found: {midi_path}")

        stems = []
        stem_paths = {}

        # Render each channel/instrument
        for channel, sfz_file in sorted(instrument_mapping.items()):
            if sfz_file is None:
                continue

            if channel < 0 or channel > 15:
                logger.warning(f"Invalid MIDI channel {channel}, skipping")
                continue

            # Extract single channel from MIDI
            channel_midi = self._extract_midi_channel(midi_path, channel)

            # Render this channel
            stem_path = self.temp_dir / f"channel_{channel:02d}_{midi_path.stem}.wav"
            try:
                self.renderer.render(
                    midi_path=channel_midi,
                    output_path=stem_path,
                    sfz_file=sfz_file,
                    normalize=False,  # Normalize after mixing
                    fade_out=0.0,  # Fade out after mixing
                )
                stems.append(stem_path)
                stem_paths[channel] = stem_path
            except SFZRendererError as e:
                logger.error(f"Failed to render channel {channel}: {e}")
                continue

        if not stems:
            raise SFZRenderError("No instruments were successfully rendered")

        # Mix stems
        mixed_path = self._mix_stems(stems, output_path)

        # Apply post-processing to mix
        if normalize or fade_out > 0:
            self.renderer._post_process(mixed_path, normalize=normalize, fade_out=fade_out)

        # Copy stems to output directory if requested
        if render_stems:
            output_dir = Path(stem_output_dir) if stem_output_dir else output_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)

            for channel, stem_path in stem_paths.items():
                stem_output = output_dir / f"stem_{channel:02d}_{output_path.stem}.wav"
                shutil.copy2(stem_path, stem_output)
                logger.info(f"Exported stem: {stem_output}")

        # Cleanup temp files
        self._cleanup_temp_stems(stems)

        logger.info(f"Rendered composition to {mixed_path}")
        return mixed_path

    def _extract_midi_channel(self, midi_path: Path, channel: int) -> Path:
        """Extract a single channel from a MIDI file.

        Creates a new MIDI file containing only the events for the
        specified channel, plus all meta events.

        Args:
            midi_path: Source MIDI file
            channel: MIDI channel to extract (0-15)

        Returns:
            Path to extracted single-channel MIDI file
        """
        try:
            import mido
        except ImportError as err:
            raise RuntimeError("mido library is required. Install with: pip install mido") from err

        mid = mido.MidiFile(str(midi_path))
        output_mid = mido.MidiFile(ticks_per_beat=mid.ticks_per_beat)

        for track in mid.tracks:
            output_track = mido.MidiTrack()
            for msg in track:
                # Keep meta messages and channel-specific messages
                if msg.is_meta or (hasattr(msg, "channel") and msg.channel == channel):
                    output_track.append(msg)
            output_mid.tracks.append(output_track)

        output_path = self.temp_dir / f"ch{channel:02d}_{midi_path.name}"
        output_mid.save(str(output_path))
        return output_path

    def _mix_stems(self, stems: list[Path], output_path: Path) -> Path:
        """Mix multiple audio stems together.

        Args:
            stems: List of audio file paths to mix
            output_path: Output path for mixed audio

        Returns:
            Path to mixed audio file
        """
        try:
            from pydub import AudioSegment
        except ImportError as err:
            raise RuntimeError("pydub library is required for mixing. Install with: pip install pydub") from err

        if not stems:
            raise ValueError("No stems to mix")

        # Load first stem as base
        mixed = AudioSegment.from_wav(str(stems[0]))

        # Overlay remaining stems
        for stem_path in stems[1:]:
            try:
                stem = AudioSegment.from_wav(str(stem_path))
                # Pad shorter stems to match length
                if len(stem) < len(mixed):
                    stem = stem + AudioSegment.silent(duration=len(mixed) - len(stem))
                elif len(stem) > len(mixed):
                    mixed = mixed + AudioSegment.silent(duration=len(stem) - len(mixed))
                mixed = mixed.overlay(stem)
            except Exception as e:
                logger.warning(f"Failed to mix stem {stem_path}: {e}")
                continue

        # Create output directory
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Export mixed audio
        mixed.export(str(output_path), format="wav")
        return output_path

    def _cleanup_temp_stems(self, stems: list[Path]) -> None:
        """Clean up temporary stem files.

        Args:
            stems: List of stem file paths to delete
        """
        for stem_path in stems:
            try:
                if stem_path.exists():
                    stem_path.unlink()
            except Exception as e:
                logger.debug(f"Failed to delete temp file {stem_path}: {e}")

        # Also clean up extracted MIDI files
        for midi_file in self.temp_dir.glob("ch*_*.mid"):
            with contextlib.suppress(Exception):
                midi_file.unlink()


def render_midi_to_audio(
    midi_path: Path | str,
    output_path: Path | str,
    sfz_file: Path | str,
    libraries_root: Path | str | None = None,
    sample_rate: int = 44100,
    normalize: bool = True,
) -> Path:
    """Convenience function to render a MIDI file to audio.

    Args:
        midi_path: Input MIDI file path
        output_path: Output audio file path
        sfz_file: SFZ instrument file
        libraries_root: Root directory for SFZ libraries
        sample_rate: Output sample rate
        normalize: Normalize output audio

    Returns:
        Path to rendered audio file

    Example:
        >>> output = render_midi_to_audio(
        ...     "composition.mid",
        ...     "output.wav",
        ...     "VSL/Strings/Violin.sfz",
        ...     libraries_root=Path("resources/sfz_libraries")
        ... )
    """
    renderer = SFZRenderer(
        libraries_root=libraries_root,
        sample_rate=sample_rate,
    )
    return renderer.render(
        midi_path=midi_path,
        output_path=output_path,
        sfz_file=sfz_file,
        normalize=normalize,
    )


def render_multitrack(
    midi_path: Path | str,
    output_path: Path | str,
    instrument_mapping: Mapping[int, Path | str | None],
    libraries_root: Path | str | None = None,
    render_stems: bool = False,
    stem_output_dir: Path | str | None = None,
) -> Path:
    """Convenience function to render a multi-instrument composition.

    Args:
        midi_path: Input MIDI file path
        output_path: Output audio file path
        instrument_mapping: Channel to SFZ file mapping
        libraries_root: Root directory for SFZ libraries
        render_stems: Also export individual stems
        stem_output_dir: Directory for stem files

    Returns:
        Path to rendered audio file

    Example:
        >>> output = render_multitrack(
        ...     "orchestral.mid",
        ...     "orchestral.wav",
        ...     {
        ...         0: "VSL/Strings/Violin.sfz",
        ...         1: "VSL/Strings/Cello.sfz",
        ...         2: "VSL/Winds/Flute.sfz",
        ...     },
        ...     libraries_root=Path("resources/sfz_libraries")
        ... )
    """
    renderer = SFZRenderer(libraries_root=libraries_root)
    multi = MultiInstrumentRenderer(renderer)
    return multi.render_composition(
        midi_path=midi_path,
        output_path=output_path,
        instrument_mapping=instrument_mapping,
        render_stems=render_stems,
        stem_output_dir=stem_output_dir,
    )
