"""Audio rendering from MIDI."""

from __future__ import annotations

import logging
from pathlib import Path

try:
    import pretty_midi
    PRETTY_MIDI_AVAILABLE = True
except ImportError:
    PRETTY_MIDI_AVAILABLE = False

logger = logging.getLogger(__name__)


class AudioRenderer:
    """Render MIDI to audio using pretty_midi and FluidSynth."""

    def __init__(
        self,
        soundfont_path: Optional[Path] = None,
        sample_rate: int = 44100,
    ):
        """Initialize audio renderer.

        Args:
            soundfont_path: Path to SoundFont file (uses default if None)
            sample_rate: Audio sample rate
        """
        if not PRETTY_MIDI_AVAILABLE:
            raise RuntimeError(
                "pretty_midi package required. Install with: pip install pretty-midi"
            )
        self.soundfont_path = soundfont_path
        self.sample_rate = sample_rate

    def render(
        self,
        midi_path: Path,
        output_path: Path,
        format: str = "wav",
    ) -> None:
        """Render MIDI file to audio.

        Args:
            midi_path: Input MIDI file
            output_path: Output audio file
            format: Output format ("wav", "mp3")
        """
        # Load MIDI
        try:
            midi = pretty_midi.PrettyMIDI(str(midi_path))
        except Exception as e:
            logger.error(f"Failed to load MIDI: {e}")
            raise RuntimeError(f"Failed to load MIDI file: {e}") from e

        # Synthesize audio
        try:
            audio = midi.synthesize(
                fs=self.sample_rate,
                wave_type='sine'  # Can be 'sine', 'square', 'sawtooth', etc.
            )
        except Exception as e:
            logger.error(f"Failed to synthesize audio: {e}")
            raise RuntimeError(f"Failed to synthesize audio: {e}") from e

        # Save audio
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "wav":
            self._save_wav(audio, output_path, self.sample_rate)
        elif format == "mp3":
            self._save_mp3(audio, output_path, self.sample_rate)
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Rendered audio to {output_path}")

    def _save_wav(self, audio, output_path: Path, sample_rate: int) -> None:
        """Save as WAV file.

        Args:
            audio: Audio data
            output_path: Output path
            sample_rate: Sample rate
        """
        try:
            import wave

            import numpy as np
        except ImportError:
            raise ImportError("numpy required for WAV output")

        # Convert to 16-bit PCM
        audio_int16 = (audio * 32767).astype(np.int16)

        with wave.open(str(output_path), 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_int16.tobytes())

    def _save_mp3(self, audio, output_path: Path, sample_rate: int) -> None:
        """Save as MP3 file.

        Args:
            audio: Audio data
            output_path: Output path
            sample_rate: Sample rate
        """
        try:
            from pydub import AudioSegment
        except ImportError:
            raise ImportError("pydub required for MP3 output. Install with: pip install pydub")

        import tempfile

        # First save as WAV
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wav:
            self._save_wav(audio, Path(tmp_wav.name), sample_rate)

            # Convert to MP3
            audio_segment = AudioSegment.from_wav(tmp_wav.name)
            audio_segment.export(str(output_path), format='mp3', bitrate='192k')

            # Cleanup temp file
            import os
            os.unlink(tmp_wav.name)
