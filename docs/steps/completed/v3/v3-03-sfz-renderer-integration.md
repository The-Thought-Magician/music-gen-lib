# V3-03: SFZ Renderer Integration

**Status:** Pending
**Priority:** High
**Dependencies:** V3-01, V3-02

## Overview

Build a Python wrapper around `sfizz-render` that handles MIDI-to-audio conversion with proper SFZ library routing, supporting multiple instruments, keyswitches, and continuous controllers.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Composition Output                           │
│              (from AI, with articulations)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MIDI File Generator                           │
│  - Note events with pitch, duration, velocity                   │
│  - Keyswitch events for articulation changes                    │
│  - CC events for expression (modulation, sustain, etc.)         │
│  - Program changes for instrument selection                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SFZ Renderer Wrapper                           │
│  - Calls sfizz-render via subprocess                           │
│  - Handles multi-output (stems)                                 │
│  - Manages SFZ library paths                                   │
│  - Processes output audio (normalize, reverb)                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Final Audio                                │
│                    WAV / MP3 / FLAC                             │
└─────────────────────────────────────────────────────────────────┘
```

## Python Implementation

### Core Renderer Class

```python
from pathlib import Path
from typing import Optional
import subprocess
import logging
import tempfile
import numpy as np

logger = logging.getLogger(__name__)

class SFZRenderer:
    """Render MIDI files to audio using sfizz-render."""

    def __init__(
        self,
        sfizz_path: str = "sfizz-render",
        libraries_root: Path | None = None,
        sample_rate: int = 44100,
        bit_depth: int = 24,
    ):
        """Initialize SFZ renderer.

        Args:
            sfizz_path: Path to sfizz-render executable
            libraries_root: Root directory for SFZ libraries
            sample_rate: Output sample rate
            bit_depth: Output bit depth (16 or 24)
        """
        self.sfizz_path = sfizz_path
        self.libraries_root = libraries_root or Path("resources/sfz_libraries")
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth

        # Verify sfizz is available
        self._check_sfizz_available()

    def _check_sfizz_available(self) -> None:
        """Verify sfizz-render is installed and accessible."""
        try:
            result = subprocess.run(
                [self.sfizz_path, "--help"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                raise RuntimeError("sfizz-render not found")
        except FileNotFoundError:
            raise RuntimeError(
                "sfizz-render not found. Install with: sudo apt install sfizz"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("sfizz-render timed out")

    def render(
        self,
        midi_path: Path,
        output_path: Path,
        sfz_file: Path,
        normalize: bool = True,
        fade_out: float = 0.0,
    ) -> Path:
        """Render a MIDI file to audio.

        Args:
            midi_path: Input MIDI file
            output_path: Output audio file
            sfz_file: SFZ instrument definition file
            normalize: Normalize output audio
            fade_out: Fade out duration in seconds

        Returns:
            Path to rendered audio file
        """
        output_path = Path(output_path)
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

        logger.info(f"Rendering with command: {' '.join(cmd)}")

        # Execute
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                check=True,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("sfizz-render timed out")
        except subprocess.CalledProcessError as e:
            logger.error(f"sfizz-render failed: {e.stderr}")
            raise RuntimeError(f"sfizz-render failed: {e.stderr}")

        # Post-process
        if normalize or fade_out > 0:
            self._post_process(output_path, normalize=normalize, fade_out=fade_out)

        logger.info(f"Rendered to {output_path}")
        return output_path

    def _resolve_sfz_path(self, sfz_file: Path) -> Path:
        """Resolve SFZ file path relative to libraries root."""
        sfz_file = Path(sfz_file)

        if sfz_file.is_absolute():
            return sfz_file

        # Check in libraries root
        resolved = self.libraries_root / sfz_file
        if resolved.exists():
            return resolved

        # Check if it's a library name
        resolved = self.libraries_root / sfz_file
        if resolved.exists():
            return resolved

        raise FileNotFoundError(f"SFZ file not found: {sfz_file}")

    def _post_process(
        self,
        audio_path: Path,
        normalize: bool = True,
        fade_out: float = 0.0,
    ) -> None:
        """Post-process audio file.

        Args:
            audio_path: Path to audio file
            normalize: Normalize to -0.1 dB
            fade_out: Add fade out at end (seconds)
        """
        try:
            from pydub import AudioSegment
        except ImportError:
            logger.warning("pydub not available, skipping post-processing")
            return

        audio = AudioSegment.from_wav(str(audio_path))

        if normalize:
            # Normalize to -0.1 dBFS
            target_dBFS = -0.1
            change_in_dBFS = target_dBFS - audio.dBFS
            audio = audio.apply_gain(change_in_dBFS)

        if fade_out > 0:
            # Add fade out
            fade_ms = int(fade_out * 1000)
            audio = audio.fade_out(fade_ms)

        # Export
        audio.export(str(audio_path), format="wav", bitrate="320k")
```

### Multi-Instrument Renderer

For compositions with multiple instruments:

```python
class MultiInstrumentRenderer:
    """Render compositions with multiple SFZ instruments."""

    def __init__(self, renderer: SFZRenderer):
        self.renderer = renderer
        self.temp_dir = Path(tempfile.gettempdir()) / "musicgen_renders"

    def render_composition(
        self,
        midi_path: Path,
        output_path: Path,
        instrument_mapping: dict[int, Path],  # MIDI channel -> SFZ file
        render_stems: bool = False,
    ) -> Path:
        """Render a multi-instrument composition.

        Args:
            midi_path: Input MIDI file (16 channels)
            output_path: Final mixed output
            instrument_mapping: Channel to SFZ file mapping
            render_stems: Also export individual instrument stems

        Returns:
            Path to final mixed audio
        """
        stems = []

        # Render each channel/instrument
        for channel, sfz_file in instrument_mapping.items():
            if sfz_file is None:
                continue

            # Extract single channel from MIDI
            channel_midi = self._extract_midi_channel(midi_path, channel)

            # Render
            stem_path = self.temp_dir / f"channel_{channel:02d}.wav"
            self.renderer.render(channel_midi, stem_path, sfz_file)
            stems.append(stem_path)

        # Mix stems
        return self._mix_stems(stems, output_path)

    def _extract_midi_channel(self, midi_path: Path, channel: int) -> Path:
        """Extract a single channel from a MIDI file."""
        import mido

        mid = mido.MidiFile(str(midi_path))
        output_mid = mido.MidiFile()

        for track in mid.tracks:
            output_track = mido.MidiTrack()
            for msg in track:
                # Keep meta messages and channel-specific messages
                if msg.is_meta or msg.channel == channel:
                    output_track.append(msg)
            output_mid.tracks.append(output_track)

        output_path = self.temp_dir / f"ch{channel:02d}_{midi_path.name}"
        output_mid.save(str(output_path))
        return output_path

    def _mix_stems(self, stems: list[Path], output_path: Path) -> Path:
        """Mix multiple audio stems together."""
        from pydub import AudioSegment

        # Load first stem
        mixed = AudioSegment.from_wav(str(stems[0]))

        # Mix in remaining stems
        for stem_path in stems[1:]:
            stem = AudioSegment.from_wav(str(stem_path))
            mixed = mixed.overlay(stem)

        # Export
        mixed.export(str(output_path), format="wav")
        return output_path
```

## Installation Helper

```python
def check_sfizz_installation() -> dict[str, bool]:
    """Check if sfizz and dependencies are installed."""
    checks = {}

    # Check sfizz-render
    try:
        result = subprocess.run(
            ["sfizz-render", "--version"],
            capture_output=True,
            timeout=5,
        )
        checks["sfizz-render"] = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        checks["sfizz-render"] = False

    # Check ffmpeg (for MP3 export)
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=5,
        )
        checks["ffmpeg"] = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        checks["ffmpeg"] = False

    # Check Python packages
    try:
        import pydub
        checks["pydub"] = True
    except ImportError:
        checks["pydub"] = False

    try:
        import numpy
        checks["numpy"] = True
    except ImportError:
        checks["numpy"] = False

    return checks

def print_installation_instructions():
    """Print installation instructions for missing dependencies."""
    checks = check_sfizz_installation()

    if all(checks.values()):
        print("✓ All dependencies installed!")
        return

    print("Missing dependencies:\n")

    if not checks["sfizz-render"]:
        print("📦 sfizz-render:")
        print("   Linux:  sudo apt install sfizz")
        print("   macOS:  brew install sfizz")
        print("   Source: https://sfztools.github.io/sfizz/\n")

    if not checks["ffmpeg"]:
        print("📦 ffmpeg:")
        print("   Linux:  sudo apt install ffmpeg")
        print("   macOS:  brew install ffmpeg\n")

    if not checks["pydub"]:
        print("📦 pydub:")
        print("   pip install pydub\n")

    if not checks["numpy"]:
        print("📦 numpy:")
        print("   pip install numpy\n")
```

## Implementation Tasks

1. [ ] Create `SFZRenderer` class with subprocess wrapper
2. [ ] Create `MultiInstrumentRenderer` for multi-channel MIDI
3. [ ] Add channel extraction from MIDI files
4. [ ] Add audio mixing capabilities
5. [ ] Add post-processing (normalize, fade)
6. [ ] Create installation checker
7. [ ] Add error handling and logging
8. [ ] Write unit tests

## Success Criteria

- `sfizz-render` successfully called from Python
- Multi-instrument MIDI files render correctly
- Stems can be exported individually
- Final mixed output is produced

## Next Steps

- V3-04: Articulation System Design
- V3-05: Enhanced MIDI Generator with Keyswitches
