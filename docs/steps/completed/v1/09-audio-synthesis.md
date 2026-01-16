# Step 9: Audio Synthesis Pipeline

## Overview

This is Step 9 of 13 steps for the Music Generation Library. This step implements the audio synthesis pipeline that converts MIDI files to high-quality audio using FluidSynth with SoundFont-based instrument synthesis.

## Context

You are building a Python library for generating orchestral instrumental music using traditional music theory principles (rule-based composition, NOT AI). The library will produce sheet music (MusicXML/LilyPond) and audio files (WAV/FLAC) from programmatic input based on mood/theme parameters.

This step depends on **Step 8: MIDI File Generation** which creates the MIDI files that this step will convert to audio.

### Prerequisites

Before implementing this step, ensure the following are complete:

- **Step 1**: Core data structures (Note, Chord, Rest)
- **Step 6**: Orchestration module (Instrument class with proper definitions)
- **Step 8**: MIDI file generation (`MIDIWriter` class that produces valid MIDI files)

### What This Step Builds On

From Step 8, you should have:
- `src/musicgen/io/midi_writer.py` - The `MIDIWriter` class with `write()` method
- MIDI files can be generated from `Score` objects
- MIDI tracks contain proper tempo, time signature, and program change messages

## Project Structure

```
music-gen-lib/
├── src/
│   └── musicgen/
│       ├── io/
│       │   ├── __init__.py           # Export MIDIWriter, AudioSynthesizer
│       │   ├── midi_writer.py        # Already exists from Step 8
│       │   └── audio_synthesizer.py  # NEW: Main file for this step
│       └── resources/
│           └── soundfonts/
│               └── .gitkeep          # Placeholder for SoundFont files
├── tests/
│   ├── __init__.py
│   └── test_audio_synthesizer.py     # NEW: Tests for this step
├── resources/
│   └── soundfonts/
│       └── .gitkeep                  # Directory for user-provided SoundFonts
└── docs/
    └── steps/
        └── 09-audio-synthesis.md     # This file
```

## Dependencies

### Python Packages (add to pyproject.toml if not present)

```toml
dependencies = [
    # ... existing dependencies
    "pyfluidsynth>=1.3.0",    # Python bindings for FluidSynth
    "pydub>=0.25.0",          # Audio processing, format conversion
    "numpy>=1.24.0",          # Audio array manipulation
]
```

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install fluidsynth
```

**macOS:**
```bash
brew install fluidsynth
```

**Windows:**
Download from: https://www.fluidsynth.org/

### SoundFont

The default SoundFont is **GeneralUser GS** which is free and includes orchestral instruments.

- Download: https://schristiancollins.com/generaluser.php
- Place in: `resources/soundfonts/GeneralUser GS.sf2`

**Note**: The SoundFont file should NOT be committed to git. Users should download it separately.

## Implementation Tasks

### Task 1: Create AudioSynthesizer Class

Create `src/musicgen/io/audio_synthesizer.py` with the following structure:

```python
"""Audio synthesis module using FluidSynth.

This module provides functionality to convert MIDI files to audio using
FluidSynth with SoundFont-based instrument synthesis.
"""

import os
import io
from pathlib import Path
from typing import Optional, Union, List, Dict, Tuple
import struct
import tempfile

import numpy as np
from numpy.typing import NDArray


class SynthesisError(Exception):
    """Raised when audio synthesis fails."""
    pass


class SoundFontNotFoundError(SynthesisError):
    """Raised when a SoundFont file cannot be found or loaded."""
    pass


class AudioSynthesizer:
    """Synthesizes audio from MIDI using FluidSynth.

    This class wraps FluidSynth to provide high-quality audio rendering
    of MIDI files using SoundFont instruments.

    Attributes:
        soundfont_path: Path to the SoundFont file (.sf2)
        sample_rate: Audio sample rate in Hz (default: 44100)
        channels: Number of audio channels (1=mono, 2=stereo)
        buffer_size: Internal processing buffer size
        gain: Master gain/volume (0.0 to 1.0)
    """

    # Default sample rates
    SAMPLE_RATE_44100 = 44100
    SAMPLE_RATE_48000 = 48000
    SAMPLE_RATE_96000 = 96000

    # Common MIDI program numbers for orchestral instruments
    INSTRUMENTS = {
        # Strings (0-7)
        "acoustic_grand_piano": 0,
        "bright_acoustic_piano": 1,
        "electric_grand_piano": 2,
        "honky_tonk_piano": 3,
        "electric_piano_1": 4,
        "electric_piano_2": 5,
        "harpsichord": 6,
        "clavinet": 7,

        # Chromatic Percussion (8-15)
        "celesta": 8,
        "glockenspiel": 9,
        "music_box": 10,
        "vibraphone": 11,
        "marimba": 12,
        "xylophone": 13,
        "tubular_bells": 14,
        "dulcimer": 15,

        # Organs (16-23)
        "drawbar_organ": 16,
        "percussive_organ": 17,
        "rock_organ": 18,
        "church_organ": 19,
        "reed_organ": 20,
        "accordion": 21,
        "harmonica": 22,
        "tango_accordion": 23,

        # Guitar (24-31)
        "acoustic_guitar_nylon": 24,
        "acoustic_guitar_steel": 25,
        "electric_guitar_jazz": 26,
        "electric_guitar_clean": 27,
        "electric_guitar_muted": 28,
        "overdriven_guitar": 29,
        "distortion_guitar": 30,
        "guitar_harmonics": 31,

        # Bass (32-39)
        "acoustic_bass": 32,
        "electric_bass_finger": 33,
        "electric_bass_pick": 34,
        "fretless_bass": 35,
        "slap_bass_1": 36,
        "slap_bass_2": 37,
        "synth_bass_1": 38,
        "synth_bass_2": 39,

        # Strings (40-47) - KEY FOR ORCHESTRAL
        "violin": 40,
        "viola": 41,
        "cello": 42,
        "contrabass": 43,
        "tremolo_strings": 44,
        "pizzicato_strings": 45,
        "orchestral_harp": 46,
        "timpani": 47,

        # Ensemble (48-55)
        "string_ensemble_1": 48,
        "string_ensemble_2": 49,
        "synth_strings_1": 50,
        "synth_strings_2": 51,
        "choir_aahs": 52,
        "voice_oohs": 53,
        "synth_choir": 54,
        "orchestra_hit": 55,

        # Brass (56-63)
        "trumpet": 56,
        "trombone": 57,
        "tuba": 58,
        "muted_trumpet": 59,
        "french_horn": 60,
        "brass_section": 61,
        "synth_brass_1": 62,
        "synth_brass_2": 63,

        # Reed (64-71)
        "soprano_sax": 64,
        "alto_sax": 65,
        "tenor_sax": 66,
        "baritone_sax": 67,
        "oboe": 68,
        "english_horn": 69,
        "bassoon": 70,
        "clarinet": 71,

        # Pipe (72-79)
        "piccolo": 72,
        "flute": 73,
        "recorder": 74,
        "pan_flute": 75,
        "blown_bottle": 76,
        "shakuhachi": 77,
        "whistle": 78,
        "ocarina": 79,

        # Synth Lead (80-87)
        "lead_1_square": 80,
        "lead_2_sawtooth": 81,
        "lead_3_calliope": 82,
        "lead_4_chiff": 83,
        "lead_5_charang": 84,
        "lead_6_voice": 85,
        "lead_7_fifths": 86,
        "lead_8_bass_and_lead": 87,

        # Synth Pad (88-95)
        "pad_1_new_age": 88,
        "pad_2_warm": 89,
        "pad_3_polysynth": 90,
        "pad_4_choir": 91,
        "pad_5_bowed": 92,
        "pad_6_metallic": 93,
        "pad_7_halo": 94,
        "pad_8_sweep": 95,

        # Effects (96-103)
        "fx_1_rain": 96,
        "fx_2_soundtrack": 97,
        "fx_3_crystal": 98,
        "fx_4_atmosphere": 99,
        "fx_5_brightness": 100,
        "fx_6_goblins": 101,
        "fx_7_echoes": 102,
        "fx_8_sci_fi": 103,

        # Ethnic (104-111)
        "sitar": 104,
        "banjo": 105,
        "shamisen": 106,
        "koto": 107,
        "kalimba": 108,
        "bagpipe": 109,
        "fiddle": 110,
        "shanai": 111,

        # Percussion (112-119)
        "tinkle_bell": 112,
        "agogo": 113,
        "steel_drums": 114,
        "woodblock": 115,
        "taiko_drum": 116,
        "melodic_tom": 117,
        "synth_drum": 118,
        "reverse_cymbal": 119,

        # Sound Effects (120-127)
        "guitar_fret_noise": 120,
        "breath_noise": 121,
        "seashore": 122,
        "bird_tweet": 123,
        "telephone_ring": 124,
        "helicopter": 125,
        "applause": 126,
        "gunshot": 127,
    }

    # Orchestral instrument presets (for quick reference)
    ORCHESTRAL = {
        "strings": {
            "violin": 40,
            "viola": 41,
            "cello": 42,
            "double_bass": 43,
            "harp": 46,
        },
        "woodwinds": {
            "flute": 73,
            "piccolo": 72,
            "oboe": 68,
            "english_horn": 69,
            "clarinet": 71,
            "bassoon": 70,
        },
        "brass": {
            "trumpet": 56,
            "french_horn": 60,
            "trombone": 57,
            "tuba": 58,
        },
        "percussion": {
            "timpani": 47,
            "glockenspiel": 9,
            "xylophone": 13,
            "tubular_bells": 14,
            "celesta": 8,
        },
    }

    def __init__(
        self,
        soundfont_path: Optional[Union[str, Path]] = None,
        sample_rate: int = SAMPLE_RATE_44100,
        channels: int = 2,
        buffer_size: int = 512,
        gain: float = 0.7,
    ):
        """Initialize the AudioSynthesizer.

        Args:
            soundfont_path: Path to .sf2 SoundFont file. If None, will search
                in common locations including resources/soundfonts/
            sample_rate: Audio sample rate in Hz (44100, 48000, 96000)
            channels: Number of audio channels (1=mono, 2=stereo)
            buffer_size: FluidSynth buffer size for processing
            gain: Master gain/volume multiplier (0.0 to 1.0)

        Raises:
            SoundFontNotFoundError: If SoundFont cannot be found
            SynthesisError: If FluidSynth cannot be initialized
        """
        self.soundfont_path = self._find_soundfont(soundfont_path)
        self.sample_rate = sample_rate
        self.channels = channels
        self.buffer_size = buffer_size
        self.gain = gain

        # FluidSynth instance (lazy loaded)
        self._synth = None
        self._soundfont_id = None

    def _find_soundfont(self, soundfont_path: Optional[Union[str, Path]]) -> Path:
        """Find a SoundFont file, checking common locations.

        Args:
            soundfont_path: User-provided path or None

        Returns:
            Path to the SoundFont file

        Raises:
            SoundFontNotFoundError: If no SoundFont can be found
        """
        if soundfont_path is not None:
            path = Path(soundfont_path)
            if path.exists():
                return path
            raise SoundFontNotFoundError(
                f"SoundFont not found at: {soundfont_path}"
            )

        # Search in common locations
        search_paths = [
            # Project resources directory
            Path(__file__).parent.parent.parent.parent / "resources" / "soundfonts" / "GeneralUser GS.sf2",
            Path(__file__).parent.parent.parent.parent / "resources" / "soundfonts" / "GeneralUserGSv1.471.sf2",
            # System locations
            Path("/usr/share/sounds/sf2/GeneralUser-GS.sf2"),
            Path("/usr/share/soundfonts/GeneralUser-GS.sf2"),
            Path("/usr/local/share/soundfonts/GeneralUser-GS.sf2"),
            # Home directory
            Path.home() / ".local" / "share" / "soundfonts" / "GeneralUser-GS.sf2",
            Path.home() / "soundfonts" / "GeneralUser-GS.sf2",
            # Windows
            Path("C:/soundfonts/GeneralUser-GS.sf2"),
        ]

        for path in search_paths:
            if path.exists():
                return path

        # Not found - provide helpful error
        raise SoundFontNotFoundError(
            "No SoundFont found. Please download GeneralUser-GS.sf2 from:\n"
            "  https://schristiancollins.com/generaluser.php\n"
            "And place it in one of these locations:\n" +
            "\n".join(f"  - {p}" for p in search_paths[:3]) +
            "\n\nOr specify the path when creating AudioSynthesizer:\n"
            "  synth = AudioSynthesizer(soundfont_path='/path/to/soundfont.sf2')"
        )

    @property
    def synth(self):
        """Get or create the FluidSynth synthesizer instance.

        Lazy-loads FluidSynth to avoid errors if not installed.

        Returns:
            FluidSynth Synth instance

        Raises:
            SynthesisError: If FluidSynth is not available
        """
        if self._synth is None:
            try:
                import fluidsynth
            except ImportError as e:
                raise SynthesisError(
                    "pyfluidsynth is not installed. Install it with:\n"
                    "  pip install pyfluidsynth\n"
                    "And ensure FluidSynth is installed on your system."
                ) from e

            try:
                self._synth = fluidsynth.Synth(
                    sample_rate=self.sample_rate,
                )
                # Load the SoundFont
                self._soundfont_id = self._synth.sfload(str(self.soundfont_path))

                # Set initial gain
                self._synth.gain(self.gain)

            except Exception as e:
                raise SynthesisError(
                    f"Failed to initialize FluidSynth: {e}"
                ) from e

        return self._synth

    def set_instrument(
        self,
        channel: int,
        program: int,
        bank: int = 0,
    ) -> None:
        """Set the instrument for a MIDI channel.

        Args:
            channel: MIDI channel number (0-15)
            program: MIDI program number (0-127) - see INSTRUMENTS dict
            bank: MIDI bank number (default: 0)

        Raises:
            ValueError: If channel or program is out of range
        """
        if not 0 <= channel <= 15:
            raise ValueError(f"Channel must be 0-15, got {channel}")
        if not 0 <= program <= 127:
            raise ValueError(f"Program must be 0-127, got {program}")

        self.synth.program_select(channel, self._soundfont_id, bank, program)

    def set_instrument_by_name(
        self,
        channel: int,
        name: str,
        bank: int = 0,
    ) -> None:
        """Set the instrument for a channel by name.

        Args:
            channel: MIDI channel number (0-15)
            name: Instrument name from INSTRUMENTS dict
            bank: MIDI bank number (default: 0)

        Raises:
            ValueError: If instrument name is not found
        """
        name_lower = name.lower().replace(" ", "_")

        if name_lower not in self.INSTRUMENTS:
            available = ", ".join(sorted(set(self.INSTRUMENTS.keys()))[:10])
            raise ValueError(
                f"Instrument '{name}' not found. Available include: {available}..."
            )

        program = self.INSTRUMENTS[name_lower]
        self.set_instrument(channel, program, bank)

    def render(
        self,
        midi_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        output_format: str = "wav",
        normalize: bool = True,
        start_time: float = 0.0,
        duration: Optional[float] = None,
    ) -> Path:
        """Render a MIDI file to audio.

        This is the main method for converting MIDI to audio. It loads the MIDI,
        renders it using FluidSynth, and saves to the specified format.

        Args:
            midi_path: Path to input MIDI file
            output_path: Path for output audio file. If None, generates from
                MIDI filename with appropriate extension
            output_format: Output format - "wav", "flac", or "raw"
            normalize: Whether to normalize audio to prevent clipping
            start_time: Start time in seconds (for partial rendering)
            duration: Duration in seconds (None = full file)

        Returns:
            Path to the output audio file

        Raises:
            SynthesisError: If rendering fails
            FileNotFoundError: If MIDI file doesn't exist
        """
        midi_path = Path(midi_path)
        if not midi_path.exists():
            raise FileNotFoundError(f"MIDI file not found: {midi_path}")

        # Generate output path if not specified
        if output_path is None:
            output_path = midi_path.with_suffix(f".{output_format}")
        else:
            output_path = Path(output_path)

        # Load MIDI file
        try:
            import mido
            midi_file = mido.MidiFile(str(midi_path))
        except ImportError as e:
            raise SynthesisError(
                "mido is not installed. Install it with: pip install mido"
            ) from e
        except Exception as e:
            raise SynthesisError(f"Failed to load MIDI file: {e}") from e

        # Calculate duration if not specified
        if duration is None:
            duration = self._get_midi_duration(midi_file) - start_time

        # Render the audio
        audio_data = self._render_midi(
            midi_file,
            start_time=start_time,
            duration=duration,
        )

        # Normalize if requested
        if normalize and audio_data.size > 0:
            audio_data = self._normalize(audio_data)

        # Save to file
        self._save_audio(audio_data, output_path, output_format)

        return output_path

    def _get_midi_duration(self, midi_file) -> float:
        """Calculate the duration of a MIDI file in seconds.

        Args:
            midi_file: mido.MidiFile instance

        Returns:
            Duration in seconds
        """
        import mido

        total_ticks = 0
        max_time = 0.0

        for track in midi_file.tracks:
            track_time = 0.0
            ticks = 0
            tempo = 500000  # Default tempo (120 BPM)

            for msg in track:
                ticks += msg.time
                if msg.type == 'set_tempo':
                    tempo = msg.tempo

                # Convert ticks to seconds
                seconds = mido.tick2second(msg.time, midi_file.ticks_per_beat, tempo)
                track_time += seconds

            max_time = max(max_time, track_time)

        return max_time

    def _render_midi(
        self,
        midi_file,
        start_time: float = 0.0,
        duration: Optional[float] = None,
    ) -> NDArray[np.float32]:
        """Render MIDI file to audio array.

        Args:
            midi_file: mido.MidiFile instance
            start_time: Start time in seconds
            duration: Duration in seconds (None = to end)

        Returns:
            Audio array as numpy float32 array
        """
        import mido

        # Calculate sample positions
        start_sample = int(start_time * self.sample_rate)
        if duration is None:
            total_samples = int(self._get_midi_duration(midi_file) * self.sample_rate)
        else:
            total_samples = int(duration * self.sample_rate)

        total_samples = max(total_samples, start_sample + self.sample_rate)  # At least 1 second

        # Create output array
        if self.channels == 2:
            shape = (total_samples - start_sample, 2)
        else:
            shape = (total_samples - start_sample,)

        audio = np.zeros(shape, dtype=np.float32)

        # Process MIDI messages
        current_sample = 0
        tempo = 500000  # Default tempo (120 BPM)

        # Reset synth
        self.synth.system_reset()

        # Track current position
        accumulated_ticks = 0
        ticks_per_sample = midi_file.ticks_per_beat / (self.sample_rate * (tempo / 1_000_000))

        for track in midi_file.tracks:
            track_ticks = 0

            for msg in track:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                    ticks_per_sample = midi_file.ticks_per_beat / (
                        self.sample_rate * (tempo / 1_000_000)
                    )

                track_ticks += msg.time

                # Calculate sample position for this message
                msg_sample = int(track_ticks / ticks_per_sample)

                if msg_sample >= start_sample:
                    relative_sample = msg_sample - start_sample

                    # Generate audio up to this point
                    if relative_sample > 0:
                        samples_to_get = min(
                            relative_sample - current_sample,
                            len(audio) - current_sample
                        )
                        if samples_to_get > 0:
                            chunk = self.synth.get_samples(samples_to_get * self.channels)
                            chunk_array = np.array(chunk, dtype=np.float32)
                            if self.channels == 2:
                                chunk_array = chunk_array.reshape(-1, 2)

                            end_sample = current_sample + samples_to_get
                            audio[current_sample:end_sample] = chunk_array[:samples_to_get]
                            current_sample = end_sample

                    # Send MIDI message
                    if not msg.is_meta:
                        # Convert mido message to bytes
                        msg_bytes = msg.bytes()
                        if msg_bytes:
                            self.synth.send(msg_bytes)

        # Get remaining samples
        if current_sample < len(audio):
            remaining = len(audio) - current_sample
            chunk = self.synth.get_samples(remaining * self.channels)
            chunk_array = np.array(chunk, dtype=np.float32)
            if self.channels == 2:
                chunk_array = chunk_array.reshape(-1, 2)
            audio[current_sample:] = chunk_array[:remaining]

        # Convert from int16 to float32 [-1, 1]
        audio = audio.astype(np.float32) / 32768.0

        return audio

    def _normalize(self, audio: NDArray[np.float32]) -> NDArray[np.float32]:
        """Normalize audio to prevent clipping.

        Args:
            audio: Input audio array

        Returns:
            Normalized audio array
        """
        max_val = np.abs(audio).max()
        if max_val > 0:
            # Normalize to -0.99 dB to prevent any clipping
            target = 0.99
            audio = audio * (target / max_val)
        return audio

    def _save_audio(
        self,
        audio: NDArray[np.float32],
        output_path: Path,
        output_format: str,
    ) -> None:
        """Save audio to file.

        Args:
            audio: Audio array (float32, range -1 to 1)
            output_path: Output file path
            output_format: Format ("wav", "flac", "raw")

        Raises:
            SynthesisError: If save fails
        """
        output_path = Path(output_path)
        output_format = output_format.lower().lstrip(".")

        try:
            if output_format in ("wav", "wave"):
                self._save_wav(audio, output_path)
            elif output_format == "flac":
                self._save_flac(audio, output_path)
            elif output_format == "raw":
                self._save_raw(audio, output_path)
            elif output_format in ("mp3", "ogg"):
                self._save_with_pydub(audio, output_path, output_format)
            else:
                raise SynthesisError(f"Unsupported format: {output_format}")
        except Exception as e:
            raise SynthesisError(f"Failed to save audio: {e}") from e

    def _save_wav(self, audio: NDArray[np.float32], output_path: Path) -> None:
        """Save audio as WAV file.

        Args:
            audio: Audio array
            output_path: Output path
        """
        # Convert to int16 for WAV
        audio_int16 = (audio * 32767.0).clip(-32768, 32767).astype(np.int16)

        # Write WAV using standard library
        import wave

        with wave.open(str(output_path), 'wb') as wav_file:
            if audio.ndim == 1:
                channels = 1
            else:
                channels = audio.shape[1]

            wav_file.setnchannels(channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)

            # Flatten for writing
            if audio.ndim > 1:
                audio_int16 = audio_int16.flatten()

            wav_file.writeframes(audio_int16.tobytes())

    def _save_flac(self, audio: NDArray[np.float32], output_path: Path) -> None:
        """Save audio as FLAC file.

        Args:
            audio: Audio array
            output_path: Output path
        """
        try:
            import soundfile as sf

            if audio.ndim == 1:
                audio = audio.reshape(-1, 1)

            sf.write(
                str(output_path),
                audio,
                self.sample_rate,
                format='FLAC',
                subtype='PCM_16'
            )
        except ImportError:
            # Fallback: save as WAV then convert with pydub
            temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            try:
                self._save_wav(audio, Path(temp_wav.name))
                self._save_with_pydub(audio, output_path, 'flac')
            finally:
                temp_wav.close()
                Path(temp_wav.name).unlink(missing_ok=True)

    def _save_raw(self, audio: NDArray[np.float32], output_path: Path) -> None:
        """Save audio as raw PCM data.

        Args:
            audio: Audio array
            output_path: Output path
        """
        audio_int16 = (audio * 32767.0).clip(-32768, 32767).astype(np.int16)
        if audio.ndim > 1:
            audio_int16 = audio_int16.flatten()
        output_path.write_bytes(audio_int16.tobytes())

    def _save_with_pydub(
        self,
        audio: NDArray[np.float32],
        output_path: Path,
        output_format: str,
    ) -> None:
        """Save audio using pydub for format conversion.

        Args:
            audio: Audio array
            output_path: Output path
            output_format: Format name
        """
        try:
            from pydub import AudioSegment
        except ImportError as e:
            raise SynthesisError(
                f"pydub is required for {output_format.upper()} output. "
                "Install it with: pip install pydub"
            ) from e

        # Create temporary WAV
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        try:
            self._save_wav(audio, Path(temp_wav.name))

            # Load with pydub and convert
            audio_segment = AudioSegment.from_wav(temp_wav.name)

            if output_format == 'flac':
                audio_segment.export(str(output_path), format='flac')
            elif output_format == 'mp3':
                audio_segment.export(str(output_path), format='mp3', bitrate='192k')
            elif output_format == 'ogg':
                audio_segment.export(str(output_path), format='ogg', codec='libvorbis')
            else:
                raise SynthesisError(f"Unsupported format for pydub: {output_format}")
        finally:
            temp_wav.close()
            Path(temp_wav.name).unlink(missing_ok=True)

    def add_reverb(
        self,
        audio: NDArray[np.float32],
        room_size: float = 0.7,
        damping: float = 0.5,
        wet_level: float = 0.3,
        dry_level: float = 0.7,
    ) -> NDArray[np.float32]:
        """Add reverb effect to audio (simple implementation).

        This is a basic reverb simulation. For high-quality reverb,
        consider using external processing.

        Args:
            audio: Input audio array
            room_size: Reverb room size (0.0 to 1.0)
            damping: High-frequency damping (0.0 to 1.0)
            wet_level: Level of reverb signal (0.0 to 1.0)
            dry_level: Level of dry signal (0.0 to 1.0)

        Returns:
            Audio with reverb applied
        """
        # Simple delay-based reverb
        delay_samples = int(0.05 * self.sample_rate)  # 50ms delay
        decay = room_size * damping

        # Create output array
        output = np.zeros_like(audio)

        # Add dry signal
        output += audio * dry_level

        # Add delayed/decayed copies for reverb effect
        for i, delay in enumerate([1, 2, 3, 4]):
            delay_samples_i = delay_samples * i * 2
            if delay_samples_i < len(audio):
                decay_factor = decay ** (i + 1)
                wet = wet_level * decay_factor

                # Pad and add delayed signal
                if audio.ndim == 1:
                    delayed = np.zeros_like(audio)
                    if delay_samples_i < len(audio):
                        delayed[delay_samples_i:] = audio[:-delay_samples_i] * wet
                else:
                    delayed = np.zeros_like(audio)
                    if delay_samples_i < len(audio):
                        delayed[delay_samples_i:] = audio[:-delay_samples_i] * wet

                output += delayed

        # Normalize to prevent clipping
        return self._normalize(output)

    def render_with_effects(
        self,
        midi_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        output_format: str = "wav",
        normalize: bool = True,
        reverb: bool = False,
        reverb_room_size: float = 0.5,
        reverb_wet_level: float = 0.2,
    ) -> Path:
        """Render MIDI to audio with optional effects.

        Convenience method that combines rendering and effects processing.

        Args:
            midi_path: Path to input MIDI file
            output_path: Path for output audio file
            output_format: Output format
            normalize: Whether to normalize audio
            reverb: Whether to add reverb effect
            reverb_room_size: Reverb room size
            reverb_wet_level: Reverb wet level

        Returns:
            Path to the output audio file
        """
        # First render to memory
        import mido
        midi_file = mido.MidiFile(str(midi_path))

        audio = self._render_midi(midi_file)

        if normalize:
            audio = self._normalize(audio)

        if reverb:
            audio = self.add_reverb(
                audio,
                room_size=reverb_room_size,
                wet_level=reverb_wet_level,
            )
            audio = self._normalize(audio)

        # Save
        if output_path is None:
            output_path = Path(midi_path).with_suffix(f".{output_format}")
        else:
            output_path = Path(output_path)

        self._save_audio(audio, output_path, output_format)

        return output_path

    def get_audio_info(
        self,
        midi_path: Union[str, Path],
    ) -> Dict[str, any]:
        """Get information about the MIDI file.

        Args:
            midi_path: Path to MIDI file

        Returns:
            Dictionary with MIDI information
        """
        import mido

        midi_file = mido.MidiFile(str(midi_path))

        return {
            "format": midi_file.type,
            "tracks": len(midi_file.tracks),
            "ticks_per_beat": midi_file.ticks_per_beat,
            "duration_seconds": self._get_midi_duration(midi_file),
            "track_count": len(midi_file.tracks),
        }

    def close(self) -> None:
        """Clean up FluidSynth resources."""
        if self._synth is not None:
            try:
                self._synth.delete()
            except Exception:
                pass
            self._synth = None
            self._soundfont_id = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"AudioSynthesizer("
            f"soundfont={self.soundfont_path.name}, "
            f"sample_rate={self.sample_rate}, "
            f"channels={self.channels}"
            f")"
        )


# Convenience functions for common operations

def midi_to_audio(
    midi_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    soundfont_path: Optional[Union[str, Path]] = None,
    output_format: str = "wav",
    sample_rate: int = 44100,
    normalize: bool = True,
) -> Path:
    """Convert a MIDI file to audio.

    This is a convenience function that creates an AudioSynthesizer,
    renders the MIDI, and cleans up.

    Args:
        midi_path: Path to input MIDI file
        output_path: Path for output audio file (auto-generated if None)
        soundfont_path: Path to SoundFont file
        output_format: Output format ("wav", "flac", etc.)
        sample_rate: Sample rate in Hz
        normalize: Whether to normalize audio

    Returns:
        Path to the output audio file

    Example:
        >>> audio_path = midi_to_audio("composition.mid", "output.wav")
        >>> print(f"Audio saved to: {audio_path}")
    """
    with AudioSynthesizer(
        soundfont_path=soundfont_path,
        sample_rate=sample_rate,
    ) as synth:
        return synth.render(
            midi_path=midi_path,
            output_path=output_path,
            output_format=output_format,
            normalize=normalize,
        )


def batch_midi_to_audio(
    midi_paths: List[Union[str, Path]],
    output_dir: Optional[Union[str, Path]] = None,
    soundfont_path: Optional[Union[str, Path]] = None,
    output_format: str = "wav",
    sample_rate: int = 44100,
) -> List[Path]:
    """Convert multiple MIDI files to audio.

    Args:
        midi_paths: List of MIDI file paths
        output_dir: Directory for output files (same as input if None)
        soundfont_path: Path to SoundFont file
        output_format: Output format
        sample_rate: Sample rate in Hz

    Returns:
        List of output file paths
    """
    output_paths = []

    with AudioSynthesizer(
        soundfont_path=soundfont_path,
        sample_rate=sample_rate,
    ) as synth:
        for midi_path in midi_paths:
            midi_path = Path(midi_path)

            if output_dir is None:
                output_path = midi_path.with_suffix(f".{output_format}")
            else:
                output_dir = Path(output_dir)
                output_dir.mkdir(parents=True, exist_ok=True)
                output_path = output_dir / f"{midi_path.stem}.{output_format}"

            try:
                result = synth.render(
                    midi_path=midi_path,
                    output_path=output_path,
                    output_format=output_format,
                )
                output_paths.append(result)
            except SynthesisError as e:
                print(f"Warning: Failed to render {midi_path}: {e}")

    return output_paths
```

### Task 2: Update Package Exports

Update `src/musicgen/io/__init__.py` to export the new classes:

```python
"""Input/output module for music file generation and synthesis."""

from musicgen.io.midi_writer import MIDIWriter
from musicgen.io.audio_synthesizer import (
    AudioSynthesizer,
    SynthesisError,
    SoundFontNotFoundError,
    midi_to_audio,
    batch_midi_to_audio,
)

__all__ = [
    "MIDIWriter",
    "AudioSynthesizer",
    "SynthesisError",
    "SoundFontNotFoundError",
    "midi_to_audio",
    "batch_midi_to_audio",
]
```

### Task 3: Create Resources Directory

Create placeholder for SoundFont files:

```bash
mkdir -p resources/soundfonts
touch resources/soundfonts/.gitkeep
```

Add to `.gitignore`:
```
# SoundFont files (user should download separately)
resources/soundfonts/*.sf2
!resources/soundfonts/.gitkeep
```

Create `resources/soundfonts/README.md`:
```markdown
# SoundFont Directory

This directory is for SoundFont files (.sf2) used by the audio synthesizer.

## Recommended SoundFont

Download **GeneralUser GS** from:
https://schristiancollins.com/generaluser.php

Place the file in this directory as `GeneralUser GS.sf2` or `GeneralUserGSv1.471.sf2`.

## Other SoundFonts

Any General MIDI compatible SoundFont (.sf2) can be used. Specify the path
when creating an AudioSynthesizer:

```python
synth = AudioSynthesizer(soundfont_path="/path/to/your/soundfont.sf2")
```
```

### Task 4: Create High-Level Convenience Function

Create `src/musicgen/io/export.py` for unified export functionality:

```python
"""High-level export functions for the music generation library.

This module provides convenience functions that combine MIDI generation
and audio synthesis for complete music export workflows.
"""

from pathlib import Path
from typing import Union, Optional, List

from musicgen.io.audio_synthesizer import AudioSynthesizer, midi_to_audio


def export_composition(
    score,  # Score object from composition module
    output_base: Union[str, Path],
    formats: List[str] = None,
    soundfont_path: Optional[Union[str, Path]] = None,
) -> dict:
    """Export a composition to multiple formats.

    This is a high-level function that handles the complete export pipeline:
    1. Generate MIDI from Score
    2. Synthesize audio from MIDI

    Args:
        score: The Score object to export
        output_base: Base path for output files (without extension)
        formats: List of formats to export ("midi", "wav", "flac")
        soundfont_path: Path to SoundFont for audio synthesis

    Returns:
        Dictionary with paths to generated files

    Example:
        >>> from musicgen import Score
        >>> score = Score(...)
        >>> result = export_composition(score, "my_music", formats=["midi", "wav"])
        >>> print(result)
        {'midi': 'my_music.mid', 'wav': 'my_music.wav'}
    """
    if formats is None:
        formats = ["midi", "wav"]

    output_base = Path(output_base)
    result = {}

    # Import MIDIWriter here to avoid circular dependency
    from musicgen.io.midi_writer import MIDIWriter

    # Generate MIDI
    if "midi" in formats:
        midi_path = output_base.with_suffix(".mid")
        MIDIWriter.write(score, midi_path)
        result["midi"] = midi_path

    # Synthesize audio formats
    audio_formats = [f for f in formats if f in ("wav", "flac", "mp3", "ogg")]

    if audio_formats and "midi" in result:
        with AudioSynthesizer(soundfont_path=soundfont_path) as synth:
            for fmt in audio_formats:
                audio_path = output_base.with_suffix(f".{fmt}")
                try:
                    synth.render(
                        midi_path=result["midi"],
                        output_path=audio_path,
                        output_format=fmt,
                    )
                    result[fmt] = audio_path
                except Exception as e:
                    print(f"Warning: Failed to export {fmt.upper()}: {e}")

    return result
```

## Test Requirements

Create `tests/test_audio_synthesizer.py`:

```python
"""Tests for the AudioSynthesizer class."""

import pytest
from pathlib import Path
import tempfile
import numpy as np

from musicgen.io.audio_synthesizer import (
    AudioSynthesizer,
    SynthesisError,
    SoundFontNotFoundError,
    midi_to_audio,
    batch_midi_to_audio,
    INSTRUMENTS,
    ORCHESTRAL,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_midi(temp_dir):
    """Create a simple test MIDI file."""
    import mido

    midi_path = temp_dir / "test.mid"
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Add tempo
    track.append(mido.MetaMessage('set_tempo', tempo=500000))

    # Add a simple C major scale
    notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C4 to C5
    for note in notes:
        track.append(mido.Message('note_on', note=note, velocity=80, time=0))
        track.append(mido.Message('note_off', note=note, velocity=80, time=480))

    mid.save(str(midi_path))
    return midi_path


@pytest.fixture
def mock_soundfont(temp_dir):
    """Create a mock SoundFont for testing (if real one not available)."""
    # This is a placeholder - tests will skip if no real SoundFont
    return None


class TestAudioSynthesizerInit:
    """Test AudioSynthesizer initialization."""

    def test_init_with_defaults(self):
        """Test initialization with default parameters."""
        # This test will fail if no SoundFont is found
        # In real tests, configure a test SoundFont path
        with pytest.raises(SoundFontNotFoundError):
            AudioSynthesizer(soundfont_path="/nonexistent/soundfont.sf2")

    def test_soundfont_search_paths(self):
        """Test that SoundFont search works."""
        # Test with explicit None to trigger search
        with pytest.raises(SoundFontNotFoundError):
            AudioSynthesizer(soundfont_path=None)

    def test_repr(self):
        """Test string representation."""
        synth = AudioSynthesizer(soundfont_path="/test/path.sf2")
        repr_str = repr(synth)
        assert "AudioSynthesizer" in repr_str
        assert "44100" in repr_str


class TestInstrumentPresets:
    """Test instrument preset dictionaries."""

    def test_instruments_dict_exists(self):
        """Test that INSTRUMENTS dictionary is populated."""
        assert isinstance(INSTRUMENTS, dict)
        assert len(INSTRUMENTS) > 100  # Should have GM presets

    def test_orchestral_dict_exists(self):
        """Test that ORCHESTRAL dictionary exists."""
        assert isinstance(ORCHESTRAL, dict)
        assert "strings" in ORCHESTRAL
        assert "woodwinds" in ORCHESTRAL
        assert "brass" in ORCHESTRAL
        assert "percussion" in ORCHESTRAL

    def test_orchestral_strings(self):
        """Test orchestral string instruments."""
        strings = ORCHESTRAL["strings"]
        assert "violin" in strings
        assert "viola" in strings
        assert "cello" in strings
        assert "double_bass" in strings
        assert strings["violin"] == 40
        assert strings["cello"] == 42

    def test_orchestral_woodwinds(self):
        """Test orchestral woodwind instruments."""
        woodwinds = ORCHESTRAL["woodwinds"]
        assert "flute" in woodwinds
        assert "oboe" in woodwinds
        assert "clarinet" in woodwinds
        assert "bassoon" in woodwinds

    def test_orchestral_brass(self):
        """Test orchestral brass instruments."""
        brass = ORCHESTRAL["brass"]
        assert "trumpet" in brass
        assert "french_horn" in brass
        assert "trombone" in brass
        assert "tuba" in brass

    def test_orchestral_percussion(self):
        """Test orchestral percussion instruments."""
        percussion = ORCHESTRAL["percussion"]
        assert "timpani" in percussion
        assert "glockenspiel" in percussion


@pytest.mark.skipif(
    True,  # Skip if no SoundFont available - remove when configured
    reason="Requires FluidSynth and SoundFont"
)
class TestAudioSynthesizerWithSoundFont:
    """Tests that require a real SoundFont."""

    @pytest.fixture
    def synthesizer(self, soundfont_path):
        """Create a synthesizer instance."""
        return AudioSynthesizer(soundfont_path=soundfont_path)

    def test_set_instrument_by_program(self, synthesizer):
        """Test setting instrument by program number."""
        synthesizer.set_instrument(channel=0, program=40)  # Violin
        # No exception means success

    def test_set_instrument_by_name(self, synthesizer):
        """Test setting instrument by name."""
        synthesizer.set_instrument_by_name(channel=0, name="violin")
        synthesizer.set_instrument_by_name(channel=1, name="Violin")  # Case insensitive
        synthesizer.set_instrument_by_name(channel=2, name="VIOLIN")

    def test_set_invalid_channel_raises(self, synthesizer):
        """Test that invalid channel raises ValueError."""
        with pytest.raises(ValueError):
            synthesizer.set_instrument(channel=16, program=40)  # Channel 16 invalid

    def test_set_invalid_program_raises(self, synthesizer):
        """Test that invalid program raises ValueError."""
        with pytest.raises(ValueError):
            synthesizer.set_instrument(channel=0, program=128)  # Program 128 invalid

    def test_set_invalid_instrument_name_raises(self, synthesizer):
        """Test that invalid instrument name raises ValueError."""
        with pytest.raises(ValueError):
            synthesizer.set_instrument_by_name(channel=0, name="nonexistent_instrument")

    def test_render_midi_to_wav(self, synthesizer, sample_midi, temp_dir):
        """Test rendering MIDI to WAV."""
        output_path = temp_dir / "output.wav"
        result = synthesizer.render(sample_midi, output_path, output_format="wav")

        assert result == output_path
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_render_auto_output_path(self, synthesizer, sample_midi):
        """Test rendering with auto-generated output path."""
        result = synthesizer.render(sample_midi)

        assert result.exists()
        assert result.suffix == ".wav"
        assert result.stem == sample_midi.stem

    def test_render_nonexistent_midi_raises(self, synthesizer, temp_dir):
        """Test that rendering non-existent MIDI raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            synthesizer.render(temp_dir / "nonexistent.mid")

    def test_get_audio_info(self, synthesizer, sample_midi):
        """Test getting MIDI file information."""
        info = synthesizer.get_audio_info(sample_midi)

        assert isinstance(info, dict)
        assert "format" in info
        assert "tracks" in info
        assert "duration_seconds" in info
        assert info["tracks"] >= 1

    def test_render_partial_duration(self, synthesizer, sample_midi, temp_dir):
        """Test rendering only part of the MIDI."""
        output_path = temp_dir / "partial.wav"
        result = synthesizer.render(
            sample_midi,
            output_path=output_path,
            start_time=0.0,
            duration=1.0,  # Only 1 second
        )

        assert result.exists()
        # File should be smaller than full rendering

    def test_context_manager(self, soundfont_path):
        """Test using synthesizer as context manager."""
        with AudioSynthesizer(soundfont_path=soundfont_path) as synth:
            synth.set_instrument(0, 40)
        # Should close without error


class TestNormalization:
    """Test audio normalization."""

    def test_normalize_clipping_audio(self):
        """Test that normalization prevents clipping."""
        # Create audio that would clip
        audio = np.array([2.0, -2.0, 1.5, -1.5], dtype=np.float32)

        synth = AudioSynthesizer(soundfont_path="/dummy.sf2")
        normalized = synth._normalize(audio)

        # After normalization, max should be <= 1.0
        assert np.abs(normalized).max() <= 1.0

    def test_normalize_zero_audio(self):
        """Test normalizing silent audio."""
        audio = np.zeros(100, dtype=np.float32)

        synth = AudioSynthesizer(soundfont_path="/dummy.sf2")
        normalized = synth._normalize(audio)

        # Should still be silent
        assert np.allclose(normalized, 0.0)


class TestReverb:
    """Test reverb effect."""

    def test_add_reverb_returns_array(self):
        """Test that reverb returns an array."""
        audio = np.random.randn(1000).astype(np.float32)

        synth = AudioSynthesizer(soundfont_path="/dummy.sf2")
        with_reverb = synth.add_reverb(audio, wet_level=0.3)

        assert isinstance(with_reverb, np.ndarray)
        assert with_reverb.shape == audio.shape

    def test_reverb_wet_level_affects_output(self):
        """Test that wet level affects the reverb amount."""
        audio = np.random.randn(1000).astype(np.float32)

        synth = AudioSynthesizer(soundfont_path="/dummy.sf2")
        dry = synth.add_reverb(audio, wet_level=0.0, dry_level=1.0)
        wet = synth.add_reverb(audio, wet_level=0.5, dry_level=0.5)

        # Results should be different
        assert not np.allclose(dry, wet)


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_midi_to_audio_function(self, sample_midi, temp_dir):
        """Test the midi_to_audio convenience function."""
        # This will fail without a real SoundFont
        with pytest.raises(SoundFontNotFoundError):
            midi_to_audio(sample_midi, output_path=temp_dir / "output.wav")

    def test_batch_midi_to_audio(self, sample_midi, temp_dir):
        """Test batch conversion."""
        midi_files = [sample_midi]

        with pytest.raises(SoundFontNotFoundError):
            batch_midi_to_audio(midi_files, output_dir=temp_dir)


class TestWavSaving:
    """Test WAV file saving."""

    def test_save_wav_creates_file(self, temp_dir):
        """Test that _save_wav creates a valid WAV file."""
        synth = AudioSynthesizer(soundfont_path="/dummy.sf2")

        # Create simple audio
        audio = np.zeros(1000, dtype=np.float32)
        output_path = temp_dir / "test.wav"

        synth._save_wav(audio, output_path)

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_save_wav_stereo(self, temp_dir):
        """Test saving stereo WAV."""
        synth = AudioSynthesizer(soundfont_path="/dummy.sf2", channels=2)

        audio = np.zeros((1000, 2), dtype=np.float32)
        output_path = temp_dir / "stereo.wav"

        synth._save_wav(audio, output_path)

        assert output_path.exists()

    def test_save_wav_mono(self, temp_dir):
        """Test saving mono WAV."""
        synth = AudioSynthesizer(soundfont_path="/dummy.sf2", channels=1)

        audio = np.zeros(1000, dtype=np.float32)
        output_path = temp_dir / "mono.wav"

        synth._save_wav(audio, output_path)

        assert output_path.exists()


class TestRawSaving:
    """Test raw PCM saving."""

    def test_save_raw_creates_file(self, temp_dir):
        """Test that _save_raw creates a file."""
        synth = AudioSynthesizer(soundfont_path="/dummy.sf2")

        audio = np.random.randn(100).astype(np.float32)
        output_path = temp_dir / "test.raw"

        synth._save_raw(audio, output_path)

        assert output_path.exists()
        assert output_path.stat().st_size == 100 * 2  # 100 samples * 2 bytes (int16)


class TestInstrumentLookup:
    """Test instrument name lookup."""

    def test_find_orchestral_instruments(self):
        """Test looking up orchestral instruments."""
        assert "violin" in INSTRUMENTS
        assert INSTRUMENTS["violin"] == 40

        assert "cello" in INSTRUMENTS
        assert INSTRUMENTS["cello"] == 42

    def test_case_insensitive_lookup(self):
        """Test that instrument lookup is case-insensitive."""
        synth = AudioSynthesizer(soundfont_path="/dummy.sf2")

        # The actual implementation should handle case
        # This tests the lookup logic
        name_lower = "Violin".lower().replace(" ", "_")
        assert name_lower in INSTRUMENTS

    def test_all_128_midi_programs_defined(self):
        """Verify all 128 GM programs are defined."""
        # GM standard has 128 programs (0-127)
        programs = set(INSTRUMENTS.values())
        assert len(programs) == 128
        assert all(0 <= p <= 127 for p in programs)
```

## Validation Criteria

After implementation, verify the following:

### 1. Package Structure

```bash
# Verify files exist
ls -la src/musicgen/io/audio_synthesizer.py
ls -la resources/soundfonts/.gitkeep
```

### 2. Import Test

```python
# Verify module can be imported
from musicgen.io import AudioSynthesizer, midi_to_audio
from musicgen.io.audio_synthesizer import INSTRUMENTS, ORCHESTRAL

# Test instrument dictionaries
assert "violin" in INSTRUMENTS
assert INSTRUMENTS["violin"] == 40
assert "strings" in ORCHESTRAL
```

### 3. Functional Validation

```python
from musicgen.io import AudioSynthesizer
from pathlib import Path

# Initialize synthesizer (requires SoundFont)
synth = AudioSynthesizer(soundfont_path="/path/to/GeneralUser GS.sf2")

# Test instrument selection
synth.set_instrument_by_name(channel=0, name="violin")
synth.set_instrument_by_name(channel=1, name="cello")

# Test MIDI info
info = synth.get_audio_info("composition.mid")
assert info["duration_seconds"] > 0

# Test rendering
audio_path = synth.render("composition.mid", "output.wav")
assert Path(audio_path).exists()

# Test with effects
audio_with_reverb = synth.render_with_effects(
    "composition.mid",
    "output_reverb.wav",
    reverb=True,
    reverb_wet_level=0.3,
)
```

### 4. Audio Quality Validation

```bash
# Generate test audio
python -c "
from musicgen.io import AudioSynthesizer
synth = AudioSynthesizer()
synth.render('test.mid', 'output.wav')
"

# Check output file
ffprobe -show_streams output.wav  # Should show 44100 Hz, stereo
sox output.wav -n stat            # Should show no clipping
```

### 5. Test Suite Validation

```bash
# Run tests
pytest tests/test_audio_synthesizer.py -v

# Run with coverage
pytest tests/test_audio_synthesizer.py --cov=src/musicgen/io/audio_synthesizer --cov-report=term-missing
```

## Implementation Notes

1. **FluidSynth Integration**: The `pyfluidsynth` package is a Python wrapper around the FluidSynth C library. Ensure the system library is installed.

2. **Lazy Loading**: FluidSynth is initialized lazily (on first use) to avoid import errors when the library is not installed.

3. **Audio Format Support**:
   - WAV: Built-in support using Python's `wave` module
   - FLAC: Requires `soundfile` or falls back to `pydub`
   - MP3/OGG: Requires `pydub` with ffmpeg installed

4. **Instrument Programs**: MIDI program numbers 0-127 correspond to General MIDI instruments. The ORCHESTRAL dict provides quick access to common orchestral instruments.

5. **Channel Limitations**: MIDI has 16 channels (0-15). Channel 10 is reserved for percussion in GM. For orchestral music, plan your channel usage accordingly.

6. **Normalization**: Audio is normalized to prevent clipping (distortion) from multiple instruments playing simultaneously.

7. **Reverb**: The included reverb is a simple delay-based effect. For professional-quality reverb, consider post-processing with dedicated tools.

## Dependencies to Install

```bash
# Install Python packages
pip install pyfluidsynth pydub numpy

# Install system dependencies
# Ubuntu/Debian:
sudo apt-get install fluidsynth

# macOS:
brew install fluidsynth

# For MP3 export with pydub:
# Ensure ffmpeg is installed on your system
```

## SoundFont Setup

```bash
# Download GeneralUser GS SoundFont
# From: https://schristiancollins.com/generaluser.php

# Create directory
mkdir -p resources/soundfonts

# Move downloaded file
mv ~/Downloads/GeneralUser*.sf2 resources/soundfonts/

# Or use system-wide location
sudo mkdir -p /usr/share/soundfonts
sudo mv ~/Downloads/GeneralUser*.sf2 /usr/share/soundfonts/
```

## Success Criteria

Step 9 is complete when:

1. All files are created in the correct locations
2. `pytest tests/test_audio_synthesizer.py` runs without errors (tests may skip if no SoundFont)
3. Test coverage is > 80% for the audio_synthesizer module
4. MIDI files can be converted to WAV audio
5. Instrument selection works correctly
6. Audio files are valid and can be played by standard audio players
7. The module can be imported: `from musicgen.io import AudioSynthesizer`

## Example Usage

```python
from musicgen.io import AudioSynthesizer, midi_to_audio

# Quick conversion
audio_path = midi_to_audio("composition.mid", "output.wav")

# Advanced usage with custom settings
with AudioSynthesizer(
    soundfont_path="/path/to/custom.sf2",
    sample_rate=48000,
    gain=0.8,
) as synth:
    # Set up instruments for each MIDI channel
    synth.set_instrument_by_name(0, "violin")
    synth.set_instrument_by_name(1, "viola")
    synth.set_instrument_by_name(2, "cello")
    synth.set_instrument_by_name(3, "double_bass")

    # Render with reverb
    synth.render_with_effects(
        "composition.mid",
        "orchestral.wav",
        reverb=True,
        reverb_room_size=0.6,
        reverb_wet_level=0.2,
    )

# Batch processing
from musicgen.io import batch_midi_to_audio

results = batch_midi_to_audio(
    ["piece1.mid", "piece2.mid", "piece3.mid"],
    output_dir="audio_output/",
    output_format="flac",
)
```

## Integration with Step 8

This step directly integrates with the MIDIWriter from Step 8:

```python
from musicgen.composition import Score
from musicgen.io import MIDIWriter, AudioSynthesizer

# Create a score
score = Score(...)

# Generate MIDI
MIDIWriter.write(score, "composition.mid")

# Synthesize to audio
synth = AudioSynthesizer()
synth.render("composition.mid", "composition.wav")

# Or use the export convenience function
from musicgen.io import export_composition

result = export_composition(
    score,
    "my_composition",
    formats=["midi", "wav", "flac"],
)
```

## Troubleshooting

### Common Issues

1. **"FluidSynth not found"**: Install the system package
   ```bash
   sudo apt install fluidsynth  # Linux
   brew install fluidsynth      # macOS
   ```

2. **"SoundFont not found"**: Download GeneralUser GS or specify path
   ```python
   synth = AudioSynthesizer(soundfont_path="/path/to/soundfont.sf2")
   ```

3. **"No audio output"**: Check that the MIDI file contains note events
   ```python
   info = synth.get_audio_info("test.mid")
   print(info)  # Check duration and track count
   ```

4. **Distorted audio**: Lower the gain or ensure normalization is enabled
   ```python
   synth = AudioSynthesizer(gain=0.5)  # Lower master gain
   ```

## Next Steps

After completing this step, proceed to:

- **Step 10**: Sheet Music Generation (MusicXML) - Export compositions to notation format
- **Step 11**: Sheet Music Generation (LilyPond) - High-quality PDF engraving
- **Step 12**: Mood-to-Music Configuration System - High-level generation interface

The audio synthesis pipeline enables users to hear their compositions, providing immediate feedback on the music generation system.
