# Implementation Prompt: Step 12 - Mood-to-Music Configuration System

## Overview

This step implements the high-level mood-based music generation interface. It ties together all previous components (scales, progressions, melody, orchestration, forms, and export modules) into a user-friendly API that allows users to generate music based on mood descriptors.

**Step Objective**: Implement the mood-based music generation interface with CLI support.

**Dependencies**:
- Step 1: Core data structures (Note, Chord, Rest)
- Step 2: Scales and Keys
- Step 3: Chord Progression Engine
- Step 4: Voice Leading Module
- Step 5: Melody Generation Engine
- Step 6: Orchestration Module
- Step 7: Musical Form Structures
- Step 8: MIDI File Generation
- Step 9: Audio Synthesis Pipeline
- Step 10: Sheet Music Generation (MusicXML)
- Step 11: Sheet Music Generation (LilyPond)

## Reading Context

Before implementing, read these files to understand the project structure and existing code:

1. `/home/chiranjeet/projects-cc/projects/music-gen-lib/docs/plan.md` - Overall implementation plan
2. `/home/chiranjeet/projects-cc/projects/music-gen-lib/claude.md` - Project context and conventions
3. `/home/chiranjeet/projects-cc/projects/music-gen-lib/docs/research.md` - Technical research
4. All previous step implementations in `src/musicgen/` for integration

## Implementation Tasks

### Task 1: Create Mood Configuration Module

Create `src/musicgen/config/moods.py` with mood-to-music parameter mappings.

#### 1.1 MoodConfiguration Data Class

```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class MoodConfiguration:
    """
    Configuration for music generation based on a mood.

    Attributes:
        name: The mood name (e.g., "epic", "peaceful", "mysterious")
        description: Human-readable description of the mood
        key: Preferred key (e.g., "C", "Dm", "F#")
        scale: Scale type (e.g., "major", "minor", "harmonic_minor")
        tempo_bpm: Tempo in beats per minute
        time_signature: Time signature as tuple (numerator, denominator)
        dynamics: Dynamic level (pp, p, mp, mf, f, ff)
        primary_instruments: List of primary instrument names
        secondary_instruments: List of secondary/accompaniment instruments
        form_type: Musical form (binary, ternary, rondo)
        texture_type: Texture type (homophonic, polyphonic, etc.)
        progression_templates: List of Roman numeral progressions
        melody_contour: Preferred melodic contour
        articulations: Common articulations for this mood
        duration_minutes: Typical duration in minutes
    """
    name: str
    description: str
    key: str = "C"
    scale: str = "major"
    tempo_bpm: int = 120
    time_signature: tuple = (4, 4)
    dynamics: str = "mf"
    primary_instruments: List[str] = field(default_factory=list)
    secondary_instruments: List[str] = field(default_factory=list)
    form_type: str = "binary"
    texture_type: str = "homophonic"
    progression_templates: List[str] = field(default_factory=list)
    melody_contour: str = "arch"
    articulations: List[str] = field(default_factory=list)
    duration_minutes: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MoodConfiguration':
        """Create configuration from dictionary."""
        pass
```

#### 1.2 Predefined Mood Configurations

Create the following mood presets:

```python
# EPIC mood configuration
MoodConfiguration(
    name="epic",
    description="Grand, heroic, and powerful music suitable for trailers and dramatic moments",
    key="C",
    scale="major",
    tempo_bpm=140,
    time_signature=(4, 4),
    dynamics="ff",
    primary_instruments=["violin_i", "violin_ii", "french_horn", "trumpet"],
    secondary_instruments=["viola", "cello", "double_bass", "timpani"],
    form_type="ternary",
    texture_type="homophonic",
    progression_templates=["I-IV-V-I", "I-vi-IV-V", "I-V-vi-IV"],
    melody_contour="ascending",
    articulations=["marcato", "accent"],
    duration_minutes=2.0
)

# PEACEFUL mood configuration
MoodConfiguration(
    name="peaceful",
    description="Calm, serene, and gentle music for relaxation",
    key="C",
    scale="major",
    tempo_bpm=70,
    time_signature=(3, 4),
    dynamics="p",
    primary_instruments=["flute", "violin_i"],
    secondary_instruments=["viola", "cello", "harp"],
    form_type="ternary",
    texture_type="melody_accompaniment",
    progression_templates=["I-IV-V-I", "I-vi-ii-V", "I-iii-IV-IV"],
    melody_contour="wave",
    articulations=["legato", "dolce"],
    duration_minutes=1.5
)

# MYSTERIOUS mood configuration
MoodConfiguration(
    name="mysterious",
    description="Enigmatic, atmospheric music with tension and ambiguity",
    key="D",
    scale="harmonic_minor",
    tempo_bpm=80,
    time_signature=(4, 4),
    dynamics="mp",
    primary_instruments=["clarinet", "viola", "cello"],
    secondary_instruments=["bassoon", "double_bass", "glockenspiel"],
    form_type="binary",
    texture_type="polyphonic",
    progression_templates=["i-iv-VII-i", "i-VI-iv-V", "i-ii-dim-V"],
    melody_contour="wave",
    articulations=["legato", "sul ponticello"],
    duration_minutes=1.5
)

# TRIUMPHANT mood configuration
MoodConfiguration(
    name="triumphant",
    description="Victorious and celebratory music with fanfare qualities",
    key="C",
    scale="major",
    tempo_bpm=130,
    time_signature=(4, 4),
    dynamics="f",
    primary_instruments=["trumpet", "french_horn", "trombone", "violin_i"],
    secondary_instruments=["violin_ii", "viola", "cello", "timpani", "tuba"],
    form_type="rondo",
    texture_type="homophonic",
    progression_templates=["I-IV-V-I", "I-V-vi-IV", "I-vi-IV-V"],
    melody_contour="ascending",
    articulations=["marcato", "staccato", "accent"],
    duration_minutes=2.0
)

# MELANCHOLIC mood configuration
MoodConfiguration(
    name="melancholic",
    description="Sad, reflective, and somber music",
    key="A",
    scale="minor",
    tempo_bpm=60,
    time_signature=(4, 4),
    dynamics="mp",
    primary_instruments=["oboe", "violin_i", "cello"],
    secondary_instruments=["viola", "bassoon"],
    form_type="binary",
    texture_type="melody_accompaniment",
    progression_templates=["i-iv-V-i", "i-VI-iv-V", "i-vi-iv-V"],
    melody_contour="descending",
    articulations=["legato", "espressivo"],
    duration_minutes=1.5
)

# DARK mood configuration
MoodConfiguration(
    name="dark",
    description="Ominous, foreboding, and intense music",
    key="E",
    scale="harmonic_minor",
    tempo_bpm=90,
    time_signature=(4, 4),
    dynamics="mf",
    primary_instruments=["french_horn", "trombone", "cello", "double_bass"],
    secondary_instruments=["bassoon", "tuba", "timpani"],
    form_type="binary",
    texture_type="homophonic",
    progression_templates=["i-dim-iv-V", "i-VI-iv-V", "i-ii-dim7-V"],
    melody_contour="descending",
    articulations=["marcato", "accent"],
    duration_minutes=1.5
)

# ROMANTIC mood configuration
MoodConfiguration(
    name="romantic",
    description="Warm, expressive, and emotionally rich music",
    key="F",
    scale="major",
    tempo_bpm=80,
    time_signature=(4, 4),
    dynamics="mf",
    primary_instruments=["violin_i", "flute"],
    secondary_instruments=["viola", "cello", "harp", "oboe"],
    form_type="ternary",
    texture_type="melody_accompaniment",
    progression_templates=["I-iii-IV-I", "I-vi-IV-V", "I-IV-vi-V"],
    melody_contour="arch",
    articulations=["legato", "dolce", "vibrato"],
    duration_minutes=2.0
)

# WHIMSICAL mood configuration
MoodConfiguration(
    name="whimsical",
    description="Playful, lighthearted, and quirky music",
    key="G",
    scale="major",
    tempo_bpm=110,
    time_signature=(3, 4),
    dynamics="mf",
    primary_instruments=["flute", "clarinet", "violin_i"],
    secondary_instruments=["oboe", "violin_ii", "viola", "cello", "glockenspiel"],
    form_type="rondo",
    texture_type="polyphonic",
    progression_templates=["I-IV-V-I", "I-V-vi-IV", "I-iii-IV-I"],
    melody_contour="wave",
    articulations=["staccato", "legato"],
    duration_minutes=1.5
)
```

#### 1.3 Mood Configuration Registry

```python
class MoodRegistry:
    """Registry for mood configurations."""

    def __init__(self):
        self._moods: Dict[str, MoodConfiguration] = {}

    def register(self, config: MoodConfiguration) -> None:
        """Register a mood configuration."""
        pass

    def get(self, name: str) -> Optional[MoodConfiguration]:
        """Get a mood configuration by name."""
        pass

    def list_moods(self) -> List[str]:
        """Return list of available mood names."""
        pass

    def get_all(self) -> Dict[str, MoodConfiguration]:
        """Return all mood configurations."""
        pass

    @classmethod
    def default(cls) -> 'MoodRegistry':
        """Create a registry with default mood configurations."""
        pass
```

### Task 2: Implement CompositionRequest Class

Create `src/musicgen/generator.py` with the main request and result classes.

#### 2.1 CompositionRequest Class

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Literal
from pathlib import Path

ExportFormat = Literal["midi", "wav", "flac", "musicxml", "pdf", "all"]

@dataclass
class CompositionRequest:
    """
    Request for music generation.

    Attributes:
        mood: The mood name (must match a registered mood)
        duration: Duration in seconds (overrides mood default)
        key: Optional key override (e.g., "C", "Dm", "F#m")
        tempo: Optional tempo override in BPM
        export_formats: List of export formats
        output_dir: Output directory for generated files
        filename: Base filename (without extension)
        time_signature: Optional time signature override as (num, den)
        custom_config: Optional custom configuration overrides
    """
    mood: str
    duration: Optional[float] = None
    key: Optional[str] = None
    tempo: Optional[int] = None
    export_formats: List[ExportFormat] = field(default_factory=lambda: ["midi", "wav"])
    output_dir: str = "output"
    filename: Optional[str] = None
    time_signature: Optional[tuple] = None
    custom_config: Dict[str, Any] = field(default_factory=dict)

    def validate(self, mood_registry: MoodRegistry) -> None:
        """Validate the request against available moods."""
        pass

    def get_config(self, mood_registry: MoodRegistry) -> MoodConfiguration:
        """Get the full configuration for this request."""
        pass

    def get_output_path(self, extension: str) -> Path:
        """Get the full output path for a given extension."""
        pass
```

#### 2.2 CompositionResult Class

```python
@dataclass
class CompositionResult:
    """
    Result of music generation.

    Attributes:
        request: The original request
        config: The configuration used
        score: The generated Score object
        midi_path: Path to generated MIDI file (if exported)
        audio_path: Path to generated audio file (if exported)
        musicxml_path: Path to generated MusicXML file (if exported)
        pdf_path: Path to generated PDF file (if exported)
        tempo: Actual tempo used
        key: Actual key used
        duration: Actual duration in seconds
        instruments: List of instruments used
        form: Musical form used
    """
    request: CompositionRequest
    config: MoodConfiguration
    score: Any  # Score object from composition module
    midi_path: Optional[Path] = None
    audio_path: Optional[Path] = None
    musicxml_path: Optional[Path] = None
    pdf_path: Optional[Path] = None
    tempo: int = 120
    key: str = "C"
    duration: float = 0.0
    instruments: List[str] = field(default_factory=list)
    form: str = "binary"

    def get_summary(self) -> str:
        """Get a human-readable summary of the result."""
        pass

    def has_export(self, format_type: str) -> bool:
        """Check if a specific export format was generated."""
        pass
```

### Task 3: Implement Main Generator

Create the main `generate()` function in `src/musicgen/generator.py`:

```python
from typing import Optional

def generate(request: CompositionRequest,
             mood_registry: Optional[MoodRegistry] = None,
             soundfont_path: Optional[str] = None) -> CompositionResult:
    """
    Generate music based on a mood request.

    This is the main entry point for music generation. It:
    1. Resolves the mood configuration
    2. Creates the musical structure (form, progression, melody)
    3. Orchestrates with appropriate instruments
    4. Exports to requested formats

    Args:
        request: The composition request
        mood_registry: Optional custom mood registry (uses default if None)
        soundfont_path: Optional path to SoundFont for audio export

    Returns:
        CompositionResult with generated music and export paths

    Raises:
        ValueError: If mood is not found or request is invalid
        RuntimeError: If generation fails
    """
    pass
```

The generation process should follow these steps:

1. **Resolve Configuration**
   ```python
   registry = mood_registry or MoodRegistry.default()
   config = request.get_config(registry)
   ```

2. **Create Musical Structure**
   ```python
   # Create scale and key
   scale = Scale(config.key, config.scale)

   # Generate chord progression
   progression = Progression.from_template(
       random.choice(config.progression_templates),
       key=config.key
   )

   # Determine form structure
   form = Form.from_type(
       config.form_type,
       key=config.key,
       progression=progression
   )
   ```

3. **Generate Melody and Harmony**
   ```python
   # Generate melody based on contour
   melody = Melody.generate(
       scale=scale,
       progression=progression,
       contour=config.melody_contour,
       duration=request.duration
   )

   # Generate harmony using voice leading
   harmony = generate_harmony(
       progression=progression,
       scale=scale,
       num_voices=4
   )
   ```

4. **Orchestrate**
   ```python
   # Create ensemble from mood instruments
   ensemble = Ensemble.from_instrument_lists(
       primary=config.primary_instruments,
       secondary=config.secondary_instruments
   )

   # Apply texture
   texture = Texture.from_type(
       config.texture_type,
       ensemble=ensemble
   )

   # Assign parts to instruments
   score = orchestrate(melody, harmony, texture, ensemble)
   ```

5. **Export Files**
   ```python
   result = CompositionResult(request=request, config=config, score=score)

   if "midi" in request.export_formats or "all" in request.export_formats:
       result.midi_path = MIDIWriter.write(score, result.get_output_path("mid"))

   if "wav" in request.export_formats or "flac" in request.export_formats or "all" in request.export_formats:
       audio_format = "wav" if "wav" in request.export_formats else "flac"
       synth = AudioSynthesizer(soundfont_path=soundfont_path)
       result.audio_path = synth.render(
           result.midi_path,
           output_path=result.get_output_path(audio_format),
           format=audio_format
       )

   if "musicxml" in request.export_formats or "all" in request.export_formats:
       result.musicxml_path = MusicXMLWriter.write(score, result.get_output_path("musicxml"))

   if "pdf" in request.export_formats or "all" in request.export_formats:
       result.pdf_path = LilyPondWriter.write(score, result.get_output_path("pdf"))
   ```

### Task 4: Implement CLI Interface

Create `src/musicgen/__main__.py`:

```python
#!/usr/bin/env python3
"""Command-line interface for music generation."""

import argparse
import sys
from pathlib import Path

from musicgen.generator import generate, CompositionRequest, MoodRegistry
from musicgen.config.moods import MoodRegistry

def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate music based on mood parameters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate epic music with default settings
  musicgen generate --mood epic

  # Generate 60 seconds of peaceful music in F major
  musicgen generate --mood peaceful --duration 60 --key F

  # Generate mysterious music and export to all formats
  musicgen generate --mood mysterious --formats all

  # List available moods
  musicgen list-moods

  # Show details for a specific mood
  musicgen show-mood --name epic
        """
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate music')
    gen_parser.add_argument(
        '--mood', '-m',
        required=True,
        help='Mood name (epic, peaceful, mysterious, triumphant, melancholic, dark, romantic, whimsical)'
    )
    gen_parser.add_argument(
        '--duration', '-d',
        type=int,
        default=None,
        help='Duration in seconds (overrides mood default)'
    )
    gen_parser.add_argument(
        '--key', '-k',
        type=str,
        default=None,
        help='Key (e.g., C, Dm, F#m, Bb)'
    )
    gen_parser.add_argument(
        '--tempo', '-t',
        type=int,
        default=None,
        help='Tempo in BPM'
    )
    gen_parser.add_argument(
        '--formats', '-f',
        nargs='+',
        choices=['midi', 'wav', 'flac', 'musicxml', 'pdf', 'all'],
        default=['midi', 'wav'],
        help='Export formats (default: midi wav)'
    )
    gen_parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='output',
        help='Output directory (default: output)'
    )
    gen_parser.add_argument(
        '--filename',
        type=str,
        default=None,
        help='Base filename (default: mood_timestamp)'
    )
    gen_parser.add_argument(
        '--time-signature',
        type=str,
        default=None,
        help='Time signature (e.g., 4/4, 3/4, 6/8)'
    )
    gen_parser.add_argument(
        '--soundfont',
        type=str,
        default=None,
        help='Path to SoundFont file for audio export'
    )

    # List moods command
    list_parser = subparsers.add_parser('list-moods', help='List available moods')

    # Show mood command
    show_parser = subparsers.add_parser('show-mood', help='Show mood details')
    show_parser.add_argument(
        '--name', '-n',
        required=True,
        help='Mood name'
    )

    return parser

def cmd_generate(args) -> int:
    """Handle the generate command."""
    pass

def cmd_list_moods(args) -> int:
    """Handle the list-moods command."""
    pass

def cmd_show_mood(args) -> int:
    """Handle the show-mood command."""
    pass

def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'generate':
        return cmd_generate(args)
    elif args.command == 'list-moods':
        return cmd_list_moods(args)
    elif args.command == 'show-mood':
        return cmd_show_mood(args)
    else:
        parser.print_help()
        return 0

if __name__ == '__main__':
    sys.exit(main())
```

### Task 5: Update Module Exports

Update `src/musicgen/config/__init__.py`:

```python
"""Mood configuration module."""

from musicgen.config.moods import (
    MoodConfiguration,
    MoodRegistry,
    # Predefined moods
    MOOD_EPIC,
    MOOD_PEACEFUL,
    MOOD_MYSTERIOUS,
    MOOD_TRIUMPHANT,
    MOOD_MELANCHOLIC,
    MOOD_DARK,
    MOOD_ROMANTIC,
    MOOD_WHIMSICAL,
)

__all__ = [
    "MoodConfiguration",
    "MoodRegistry",
    "MOOD_EPIC",
    "MOOD_PEACEFUL",
    "MOOD_MYSTERIOUS",
    "MOOD_TRIUMPHANT",
    "MOOD_MELANCHOLIC",
    "MOOD_DARK",
    "MOOD_ROMANTIC",
    "MOOD_WHIMSICAL",
]
```

Update `src/musicgen/__init__.py` to include:

```python
# Generator and mood interface
from musicgen.generator import generate, CompositionRequest, CompositionResult
from musicgen.config import MoodConfiguration, MoodRegistry

__all__.extend([
    "generate",
    "CompositionRequest",
    "CompositionResult",
    "MoodConfiguration",
    "MoodRegistry",
])
```

### Task 6: Create Examples

Create `examples/mood_examples.py`:

```python
#!/usr/bin/env python3
"""Examples of mood-based music generation."""

from pathlib import Path
from musicgen import generate, CompositionRequest

def example_epic():
    """Generate epic orchestral music."""
    request = CompositionRequest(
        mood="epic",
        duration=60,
        export_formats=["midi", "wav", "pdf"],
        output_dir="examples/output"
    )
    result = generate(request)
    print(result.get_summary())
    return result

def example_peaceful():
    """Generate peaceful ambient music."""
    request = CompositionRequest(
        mood="peaceful",
        duration=45,
        key="F",
        tempo=70,
        export_formats=["midi", "wav"],
        output_dir="examples/output"
    )
    result = generate(request)
    print(result.get_summary())
    return result

def example_mysterious():
    """Generate mysterious atmospheric music."""
    request = CompositionRequest(
        mood="mysterious",
        duration=90,
        export_formats=["midi", "wav", "musicxml"],
        output_dir="examples/output"
    )
    result = generate(request)
    print(result.get_summary())
    return result

def example_custom_mood():
    """Generate music with custom parameters."""
    request = CompositionRequest(
        mood="melancholic",
        duration=30,
        key="Am",
        tempo=55,
        time_signature=(3, 4),
        export_formats=["midi", "wav"],
        output_dir="examples/output"
    )
    result = generate(request)
    print(result.get_summary())
    return result

def example_all_formats():
    """Generate music in all available formats."""
    request = CompositionRequest(
        mood="triumphant",
        duration=60,
        export_formats=["all"],
        output_dir="examples/output"
    )
    result = generate(request)
    print(result.get_summary())
    return result

if __name__ == "__main__":
    print("Generating mood-based music examples...")
    print("\n1. Epic example:")
    example_epic()

    print("\n2. Peaceful example:")
    example_peaceful()

    print("\n3. Mysterious example:")
    example_mysterious()

    print("\n4. Custom mood example:")
    example_custom_mood()

    print("\n5. All formats example:")
    example_all_formats()

    print("\nAll examples generated successfully!")
```

Create `examples/quick_start.py`:

```python
#!/usr/bin/env python3
"""Quick start example for music generation."""

from musicgen import generate, CompositionRequest

# Generate music with a single line of code
result = generate(CompositionRequest(
    mood="epic",
    duration=30
))

print(f"Generated {result.config.name} composition!")
print(f"  Key: {result.key}")
print(f"  Tempo: {result.tempo} BPM")
print(f"  Duration: {result.duration} seconds")
print(f"  MIDI: {result.midi_path}")
print(f"  Audio: {result.audio_path}")
```

## File Structure

Create the following files:

```
src/musicgen/config/
    __init__.py       # Module exports
    moods.py          # Mood configurations and registry

src/musicgen/
    __main__.py       # CLI interface
    generator.py      # Main generate() function

examples/
    mood_examples.py  # Mood generation examples
    quick_start.py    # Quick start example
```

## Test Requirements

Create `tests/test_moods.py`:

```python
"""Tests for mood configuration system."""

import pytest
from musicgen.config import MoodConfiguration, MoodRegistry
from musicgen.generator import CompositionRequest, generate


class TestMoodConfiguration:
    """Test MoodConfiguration class."""

    def test_create_configuration(self):
        config = MoodConfiguration(
            name="test",
            description="Test mood",
            key="C",
            scale="major",
            tempo_bpm=120
        )
        assert config.name == "test"
        assert config.key == "C"
        assert config.tempo_bpm == 120

    def test_to_dict(self):
        config = MoodConfiguration(
            name="test",
            description="Test mood",
            key="Am",
            tempo_bpm=90
        )
        data = config.to_dict()
        assert data["name"] == "test"
        assert data["key"] == "Am"
        assert data["tempo_bpm"] == 90

    def test_from_dict(self):
        data = {
            "name": "test",
            "description": "Test mood",
            "key": "F",
            "tempo_bpm": 100,
            "scale": "minor"
        }
        config = MoodConfiguration.from_dict(data)
        assert config.name == "test"
        assert config.key == "F"
        assert config.scale == "minor"


class TestMoodRegistry:
    """Test MoodRegistry class."""

    def test_register_and_get(self):
        registry = MoodRegistry()
        config = MoodConfiguration(name="custom", description="Custom mood")
        registry.register(config)

        retrieved = registry.get("custom")
        assert retrieved is not None
        assert retrieved.name == "custom"

    def test_get_nonexistent_returns_none(self):
        registry = MoodRegistry()
        assert registry.get("nonexistent") is None

    def test_list_moods(self):
        registry = MoodRegistry()
        registry.register(MoodConfiguration(name="mood1", description="1"))
        registry.register(MoodConfiguration(name="mood2", description="2"))

        moods = registry.list_moods()
        assert set(moods) == {"mood1", "mood2"}

    def test_default_registry_has_moods(self):
        registry = MoodRegistry.default()
        moods = registry.list_moods()

        # Check for predefined moods
        assert "epic" in moods
        assert "peaceful" in moods
        assert "mysterious" in moods
        assert "triumphant" in moods
        assert "melancholic" in moods
        assert "dark" in moods
        assert "romantic" in moods
        assert "whimsical" in moods

    def test_epic_configuration(self):
        registry = MoodRegistry.default()
        epic = registry.get("epic")

        assert epic is not None
        assert epic.key == "C"
        assert epic.scale == "major"
        assert epic.tempo_bpm >= 120
        assert "violin" in str(epic.primary_instruments)

    def test_peaceful_configuration(self):
        registry = MoodRegistry.default()
        peaceful = registry.get("peaceful")

        assert peaceful is not None
        assert peaceful.tempo_bpm < 100
        assert peaceful.dynamics in ["p", "pp"]
        assert "flute" in str(peaceful.primary_instruments)

    def test_mysterious_configuration(self):
        registry = MoodRegistry.default()
        mysterious = registry.get("mysterious")

        assert mysterious is not None
        assert mysterious.scale in ["minor", "harmonic_minor", "phrygian"]
        assert mysterious.tempo_bpm >= 60


class TestCompositionRequest:
    """Test CompositionRequest class."""

    def test_create_request(self):
        request = CompositionRequest(
            mood="epic",
            duration=60,
            key="C"
        )
        assert request.mood == "epic"
        assert request.duration == 60
        assert request.key == "C"

    def test_get_output_path(self):
        request = CompositionRequest(
            mood="peaceful",
            filename="test_output",
            output_dir="test_out"
        )

        path = request.get_output_path("mid")
        assert path.parent.name == "test_out"
        assert path.stem == "test_output"
        assert path.suffix == ".mid"

    def test_validate_with_valid_mood(self):
        registry = MoodRegistry.default()
        registry.register(MoodConfiguration(name="test", description="Test"))

        request = CompositionRequest(mood="test")
        # Should not raise
        request.validate(registry)

    def test_validate_with_invalid_mood(self):
        registry = MoodRegistry.default()

        request = CompositionRequest(mood="nonexistent")
        with pytest.raises(ValueError):
            request.validate(registry)


class TestCompositionResult:
    """Test CompositionResult class."""

    def test_create_result(self):
        request = CompositionRequest(mood="epic")
        config = MoodConfiguration(name="epic", description="Epic")

        result = CompositionResult(
            request=request,
            config=config,
            score=None  # Would be actual score in real usage
        )

        assert result.request == request
        assert result.config == config

    def test_has_export(self):
        request = CompositionRequest(mood="epic")
        config = MoodConfiguration(name="epic", description="Epic")

        result = CompositionResult(
            request=request,
            config=config,
            score=None
        )
        result.midi_path = "test.mid"

        assert result.has_export("midi")
        assert not result.has_export("wav")


class TestIntegrationGenerate:
    """Integration tests for the generate function."""

    @pytest.mark.slow
    def test_generate_epic_mood(self):
        request = CompositionRequest(
            mood="epic",
            duration=15,  # Short for testing
            export_formats=["midi"],
            output_dir="tests/output"
        )

        result = generate(request)

        assert result.config.name == "epic"
        assert result.midi_path is not None
        assert result.midi_path.exists()

    @pytest.mark.slow
    def test_generate_with_key_override(self):
        request = CompositionRequest(
            mood="peaceful",
            key="F",
            duration=15,
            export_formats=["midi"],
            output_dir="tests/output"
        )

        result = generate(request)

        # Key should be overridden
        assert result.key == "F" or result.config.key == "F"

    @pytest.mark.slow
    def test_generate_with_tempo_override(self):
        request = CompositionRequest(
            mood="peaceful",
            tempo=100,
            duration=15,
            export_formats=["midi"],
            output_dir="tests/output"
        )

        result = generate(request)

        # Tempo should be overridden
        assert result.tempo == 100

    @pytest.mark.slow
    def test_generate_all_formats(self):
        request = CompositionRequest(
            mood="whimsical",
            duration=15,
            export_formats=["all"],
            output_dir="tests/output"
        )

        result = generate(request)

        assert result.midi_path is not None
        # Other formats depend on external dependencies
        # so we only require MIDI
```

Create `tests/test_cli.py`:

```python
"""Tests for CLI interface."""

import pytest
from pathlib import Path
from musicgen.__main__ import create_parser, cmd_list_moods, cmd_show_mood


class TestCLIParser:
    """Test CLI argument parser."""

    def test_parser_creation(self):
        parser = create_parser()
        assert parser is not None

    def test_generate_command_basic(self):
        parser = create_parser()
        args = parser.parse_args(['generate', '--mood', 'epic'])

        assert args.command == 'generate'
        assert args.mood == 'epic'

    def test_generate_command_with_options(self):
        parser = create_parser()
        args = parser.parse_args([
            'generate',
            '--mood', 'peaceful',
            '--duration', '60',
            '--key', 'F',
            '--tempo', '90',
            '--formats', 'midi', 'wav'
        ])

        assert args.mood == 'peaceful'
        assert args.duration == 60
        assert args.key == 'F'
        assert args.tempo == 90
        assert set(args.formats) == {'midi', 'wav'}

    def test_list_moods_command(self):
        parser = create_parser()
        args = parser.parse_args(['list-moods'])

        assert args.command == 'list-moods'

    def test_show_mood_command(self):
        parser = create_parser()
        args = parser.parse_args(['show-mood', '--name', 'epic'])

        assert args.command == 'show-mood'
        assert args.name == 'epic'


class TestCLICommands:
    """Test CLI command functions."""

    def test_list_moods_returns_zero(self):
        args = create_parser().parse_args(['list-moods'])
        result = cmd_list_moods(args)
        assert result == 0

    def test_show_mood_valid(self):
        args = create_parser().parse_args(['show-mood', '--name', 'epic'])
        result = cmd_show_mood(args)
        assert result == 0

    def test_show_mood_invalid(self):
        args = create_parser().parse_args(['show-mood', '--name', 'invalid'])
        result = cmd_show_mood(args)
        assert result != 0
```

## Validation Criteria

After implementation, verify these behaviors:

### 1. Mood Configuration
```python
from musicgen.config import MoodRegistry

registry = MoodRegistry.default()
assert "epic" in registry.list_moods()
assert "peaceful" in registry.list_moods()

epic = registry.get("epic")
assert epic.tempo_bpm >= 120
assert "violin" in str(epic.primary_instruments)
```

### 2. Request Handling
```python
from musicgen import CompositionRequest

request = CompositionRequest(mood="epic", duration=60)
assert request.mood == "epic"
assert request.duration == 60
```

### 3. Generation (Integration Test)
```python
from musicgen import generate, CompositionRequest

request = CompositionRequest(
    mood="peaceful",
    duration=15,
    export_formats=["midi"],
    output_dir="test_output"
)

result = generate(request)
assert result.config.name == "peaceful"
assert result.midi_path is not None
```

### 4. CLI Usage
```bash
# List moods
musicgen list-moods

# Show mood details
musicgen show-mood --name epic

# Generate music
musicgen generate --mood peaceful --duration 30 --formats midi wav
```

## Dependencies on Previous Steps

This step depends on all previous steps:

1. **Step 1 (Core)**: Note, Chord, Rest classes
2. **Step 2 (Scales/Keys)**: Scale, Key classes for tonal framework
3. **Step 3 (Progressions)**: Progression class for harmonic structure
4. **Step 4 (Voice Leading)**: Voice leading functions for harmony
5. **Step 5 (Melody)**: Melody generation engine
6. **Step 6 (Orchestration)**: Instrument, Ensemble, Texture classes
7. **Step 7 (Forms)**: Form structure classes
8. **Step 8 (MIDI)**: MIDIWriter for export
9. **Step 9 (Audio)**: AudioSynthesizer for WAV/FLAC export
10. **Step 10 (MusicXML)**: MusicXMLWriter for sheet music
11. **Step 11 (LilyPond)**: LilyPondWriter for PDF export

## Success Criteria

Step 12 is complete when:

1. All mood configurations are defined with appropriate parameters
2. `MoodRegistry` manages mood configurations correctly
3. `CompositionRequest` validates and processes user input
4. `CompositionResult` encapsulates generation results
5. `generate()` function produces valid music in requested formats
6. CLI interface works for all commands (generate, list-moods, show-mood)
7. All tests pass: `pytest tests/test_moods.py tests/test_cli.py`
8. Examples run successfully
9. CLI can be invoked: `python -m musicgen list-moods`

## Notes

- The `generate()` function should gracefully handle missing export dependencies (e.g., if FluidSynth is not installed, skip audio export)
- Mood configurations should be extensible - users should be able to register custom moods
- Output filenames should include mood name and timestamp to avoid conflicts
- CLI should provide helpful error messages for invalid inputs
- Consider adding a `--verbose` flag for debugging output
- The generation process may be slow for longer durations; consider adding progress indicators

## CLI Output Format

The CLI should produce output like:

```
$ musicgen generate --mood epic --duration 60
Generating epic composition...
  Key: C major
  Tempo: 140 BPM
  Time signature: 4/4
  Duration: 60 seconds
  Instruments: violin_i, violin_ii, french_horn, trumpet, viola, cello, double_bass, timpani

Generating musical structure...
Generating melody and harmony...
Orchestrating...
Exporting files...

Complete! Generated files:
  MIDI: epic_20250111_143022.mid
  Audio: epic_20250111_143022.wav

$ musicgen list-moods
Available moods:
  epic         - Grand, heroic, and powerful music
  peaceful     - Calm, serene, and gentle music
  mysterious   - Enigmatic, atmospheric music
  triumphant   - Victorious and celebratory music
  melancholic  - Sad, reflective, and somber music
  dark         - Ominous, foreboding, and intense music
  romantic     - Warm, expressive, and emotionally rich music
  whimsical    - Playful, lighthearted, and quirky music
```

## Next Steps

After completing this step, proceed to Step 13: "Testing and Documentation" which will complete the project with comprehensive test coverage, API documentation, and user-facing documentation.
