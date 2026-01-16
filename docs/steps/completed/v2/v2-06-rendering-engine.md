# Step 6: Rendering Engine (AIComposition → MIDI/Audio)

## Objective

Create a rendering engine that converts `AIComposition` objects into:
1. MIDI files
2. Audio files (WAV, MP3)
3. MusicXML (optional, for notation)
4. PDF score (optional, via LilyPond)

## Overview

The rendering engine is a pure synthesis layer - no composition logic, just conversion from note data to sound.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  AIComposition                                              │
│  - title, tempo, key                                        │
│  - parts[]: name, midi_program, notes[]                     │
├─────────────────────────────────────────────────────────────┤
│  Renderer                                                    │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ MIDIRenderer                                             ││
│  │   - AIComposition → MIDI file                           ││
│  │   - Uses mido for MIDI I/O                              ││
│  ├─────────────────────────────────────────────────────────┤│
│  │ AudioRenderer                                            ││
│  │   - MIDI → WAV/MP3                                      ││
│  │   - Uses pretty-midi + FluidSynth                       ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│  Output Files                                               │
│  - composition.mid                                          │
│  - composition.wav                                          │
│  - composition.mp3                                          │
└─────────────────────────────────────────────────────────────┘
```

## Tasks

### 6.1 Create Renderer Package

Create `src/musicgen/renderer/`:
```
src/musicgen/renderer/
├── __init__.py
├── midi.py        # MIDI rendering
├── audio.py       # Audio synthesis
└── renderer.py    # Main Renderer class
```

### 6.2 MIDI Renderer

Create `src/musicgen/renderer/midi.py`:

```python
"""MIDI rendering from AIComposition."""

from __future__ import annotations
from typing import List, Optional
from pathlib import Path

try:
    import mido
    from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False

from musicgen.ai_models import AIComposition, AIPart, AINote, AIRest


class MIDIRenderer:
    """Render AIComposition to MIDI file."""

    def __init__(self, ticks_per_beat: int = 480):
        """Initialize MIDI renderer.

        Args:
            ticks_per_beat: MIDI resolution (PPQ)
        """
        if not MIDO_AVAILABLE:
            raise RuntimeError("mido package required. Install with: pip install mido")
        self.ticks_per_beat = ticks_per_beat

    def render(
        self,
        composition: AIComposition,
        output_path: Path,
    ) -> None:
        """Render composition to MIDI file.

        Args:
            composition: AIComposition to render
            output_path: Output MIDI file path
        """
        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)

        # Create tempo track
        tempo_track = MidiTrack()
        mid.tracks.append(tempo_track)

        # Set tempo
        tempo_track.append(MetaMessage('set_tempo', tempo=bpm2tempo(composition.tempo)))
        # Set time signature
        numerator = composition.time_signature.numerator
        denominator = composition.time_signature.denominator
        tempo_track.append(MetaMessage('time_signature', numerator=numerator, denominator=denominator))
        # End of track markers (for compatibility)
        tempo_track.append(MetaMessage('end_of_track'))

        # Create track for each part
        for part in composition.parts:
            track = self._render_part(part, composition)
            mid.tracks.append(track)

        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        mid.save(output_path)

    def _render_part(self, part: AIPart, composition: AIComposition) -> MidiTrack:
        """Render a single part to a MIDI track.

        Args:
            part: Part to render
            composition: Full composition (for tempo context)

        Returns:
            MidiTrack
        """
        track = MidiTrack()

        # Track name
        track.append(MetaMessage('track_name', name=part.name))

        # Set instrument (program change)
        track.append(Message('program_change', program=part.midi_program, channel=part.midi_channel))

        # Set initial volume
        track.append(Message('control_change', control=7, value=100, channel=part.midi_channel))

        # Track events
        current_time = 0
        events = self._part_to_events(part)

        for event_time, message in sorted(events):
            delta = event_time - current_time
            track.append(message.copy(time=int(delta)))
            current_time = event_time

        # End of track
        track.append(MetaMessage('end_of_track', time=0))

        return track

    def _part_to_events(self, part: AIPart) -> List[tuple[int, Message]]:
        """Convert part to list of (time, message) tuples.

        Args:
            part: Part to convert

        Returns:
            List of (tick_time, Message)
        """
        events = []
        current_tick = 0
        channel = part.midi_channel

        for note_event in part.get_note_events():
            if isinstance(note_event, AIRest):
                # Just advance time
                current_tick += self._duration_to_ticks(note_event.duration)

            elif isinstance(note_event, AINote):
                midi_note = note_event.get_midi_number()
                duration_ticks = self._duration_to_ticks(note_event.duration)
                velocity = note_event.velocity

                # Note on
                events.append((
                    current_tick,
                    Message('note_on', note=midi_note, velocity=velocity, channel=channel)
                ))

                # Note off
                events.append((
                    current_tick + duration_ticks,
                    Message('note_off', note=midi_note, velocity=0, channel=channel)
                ]))

                current_tick += duration_ticks

        return events

    def _duration_to_ticks(self, duration_quarters: float) -> int:
        """Convert duration in quarter notes to ticks.

        Args:
            duration_quarters: Duration in quarter notes

        Returns:
            Duration in ticks
        """
        return int(duration_quarters * self.ticks_per_beat)
```

### 6.3 Audio Renderer

Create `src/musicgen/renderer/audio.py`:

```python
"""Audio rendering from MIDI."""

from __future__ import annotations
from pathlib import Path
import logging

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

    def _save_wav(self, audio: bytes, output_path: Path, sample_rate: int) -> None:
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

    def _save_mp3(self, audio: bytes, output_path: Path, sample_rate: int) -> None:
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

        import numpy as np
        import tempfile

        # First save as WAV
        with tempfile.NamedTemporaryFile(suffix='.wav') as tmp_wav:
            self._save_wav(audio, Path(tmp_wav.name), sample_rate)

            # Convert to MP3
            audio_segment = AudioSegment.from_wav(tmp_wav.name)
            audio_segment.export(str(output_path), format='mp3', bitrate='192k')
```

### 6.4 Main Renderer

Create `src/musicgen/renderer/renderer.py`:

```python
"""Main rendering engine."""

from __future__ import annotations
from pathlib import Path
from typing import List, Optional
import logging

from musicgen.ai_models import AIComposition
from musicgen.renderer.midi import MIDIRenderer
from musicgen.renderer.audio import AudioRenderer

logger = logging.getLogger(__name__)


class Renderer:
    """Main rendering engine for AIComposition.

    Converts AIComposition to MIDI and audio files.
    """

    def __init__(
        self,
        output_dir: Path = Path("."),
        soundfont_path: Optional[Path] = None,
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
        ) if soundfont_path or True else None  # Always initialize

    def render(
        self,
        composition: AIComposition,
        formats: List[str],
        output_name: Optional[str] = None,
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
    formats: List[str] = None,
    output_dir: Path = Path("."),
    output_name: Optional[str] = None,
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
```

### 6.5 Package Init

Create `src/musicgen/renderer/__init__.py`:

```python
"""Rendering engine for AIComposition."""

from musicgen.renderer.renderer import Renderer, render
from musicgen.renderer.midi import MIDIRenderer
from musicgen.renderer.audio import AudioRenderer

__all__ = [
    "Renderer",
    "render",
    "MIDIRenderer",
    "AudioRenderer",
]
```

### 6.6 Testing

Create `tests/test_renderer.py`:

```python
"""Test rendering engine."""

from pathlib import Path
import tempfile

from musicgen.ai_models import AIComposition, AIPart, AINote
from musicgen.renderer import Renderer, MIDIRenderer


def test_midi_renderer():
    """Test MIDI rendering."""
    # Create simple composition
    comp = AIComposition(
        title="Test",
        tempo=120,
        key={"tonic": "C", "mode": "major"},
        parts=[{
            "name": "piano",
            "midi_program": 0,
            "midi_channel": 0,
            "notes": [
                {"note_name": "C4", "duration": 1.0},
                {"note_name": "D4", "duration": 1.0},
                {"note_name": "E4", "duration": 1.0},
            ]
        }]
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        renderer = MIDIRenderer()
        output_path = Path(tmpdir) / "test.mid"
        renderer.render(comp, output_path)

        assert output_path.exists()


def test_renderer():
    """Test main renderer."""
    comp = AIComposition(
        title="Renderer Test",
        tempo=100,
        key={"tonic": "F", "mode": "major"},
        parts=[{
            "name": "flute",
            "midi_program": 73,
            "midi_channel": 0,
            "notes": [{"note_name": "F4", "duration": 2.0}]
        }]
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        renderer = Renderer(output_dir=Path(tmpdir))
        results = renderer.render(comp, formats=["midi"])

        assert "midi" in results
        assert results["midi"].exists()


def test_render_convenience():
    """Test convenience function."""
    from musicgen.renderer import render

    comp = AIComposition(
        title="Convenience Test",
        tempo=110,
        key={"tonic": "G", "mode": "minor"},
        parts=[{
            "name": "violin",
            "midi_program": 40,
            "midi_channel": 0,
            "notes": [{"note_name": "G3", "duration": 1.0}]
        }]
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        results = render(comp, formats=["midi"], output_dir=Path(tmpdir))
        assert results["midi"].exists()
```

## Deliverables

- `src/musicgen/renderer/__init__.py`
- `src/musicgen/renderer/midi.py`
- `src/musicgen/renderer/audio.py`
- `src/musicgen/renderer/renderer.py`
- `tests/test_renderer.py`

## Usage Examples

```python
from musicgen.composer import compose
from musicgen.renderer import render

# Generate composition
composition = compose("A peaceful piano melody")

# Render to MIDI and audio
results = render(
    composition,
    formats=["midi", "wav", "mp3"],
    output_dir="output",
)

print(f"Generated files:")
for fmt, path in results.items():
    print(f"  {fmt}: {path}")
```

## Next Steps

After completing this step:
- Step 7: CLI redesign (unified AI-first interface)
- Step 8: Type safety with ruff/mypy
