# Step 5: AI Composer (Orchestration)

## Objective

Create the AI Composer that orchestrates the entire flow:
1. Takes user prompt
2. Generates schema
3. Calls Gemini client
4. Validates response against Pydantic models
5. Returns `AIComposition` ready for rendering

## Overview

The AI Composer is the high-level interface that combines all the previous components.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  User                                                        │
│  "Create a jazz piece with piano and saxophone"             │
├─────────────────────────────────────────────────────────────┤
│  AIComposer.generate(prompt)                                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 1. Get schema (from SchemaGenerator)                   ││
│  │ 2. Build prompt (with schema)                           ││
│  │ 3. Call GeminiClient                                    ││
│  │ 4. Parse JSON response                                  ││
│  │ 5. Validate against AIComposition model                ││
│  │ 6. Return validated AIComposition                      ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│  Output: AIComposition                                       │
│  - Ready to pass to Renderer                                 │
└─────────────────────────────────────────────────────────────┘
```

## Tasks

### 5.1 Create Composer Package

Create `src/musicgen/composer/`:
```
src/musicgen/composer/
├── __init__.py
├── composer.py    # Main AIComposer class
└── presets.py     # Optional: prompt presets/templates
```

### 5.2 AI Composer

Create `src/musicgen/composer/composer.py`:

```python
"""AI Composer - generates compositions from prompts."""

from __future__ import annotations
from typing import Optional, List, Any
from pathlib import Path
import logging

from musicgen.config import get_config, Config
from musicgen.schema import SchemaGenerator, SchemaConfig, get_schema
from musicgen.ai_client import GeminiClient, generate_composition
from musicgen.ai_client.exceptions import AIClientError
from musicgen.ai_models import AIComposition

logger = logging.getLogger(__name__)


class AIComposer:
    """AI-powered music composer.

    Generates complete note-based compositions from natural language prompts.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        schema_config: Optional[SchemaConfig] = None,
        config: Optional[Config] = None,
    ):
        """Initialize the AI composer.

        Args:
            api_key: Google API key
            model: Model name (default: from config)
            temperature: Sampling temperature (default: from config)
            max_tokens: Max output tokens (default: from config)
            schema_config: Optional schema configuration
            config: Optional config object
        """
        self.config = config or get_config()
        self.schema_config = schema_config

        # Initialize AI client
        self.client = GeminiClient(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            config=self.config,
        )

        # Schema generator
        self.schema_generator = SchemaGenerator(schema_config)

    def generate(
        self,
        prompt: str,
        validate: bool = True,
        return_raw: bool = False,
    ) -> AIComposition | dict[str, Any]:
        """Generate a composition from a prompt.

        Args:
            prompt: Natural language description of desired music
            validate: Whether to validate against AIComposition model
            return_raw: If True, return raw dict instead of AIComposition

        Returns:
            AIComposition or raw dict

        Raises:
            AIClientError: If generation fails
            ValidationError: If validation fails
        """
        logger.info(f"Generating composition from prompt: {prompt[:100]}...")

        # Get schema
        schema = self.schema_generator.generate()
        logger.debug(f"Generated schema ({len(schema)} chars)")

        # Generate composition
        raw_response = self.client.generate(
            prompt=prompt,
            schema=schema,
        )

        logger.info(f"Received response from AI")

        if return_raw:
            return raw_response

        # Validate and parse
        if validate:
            try:
                composition = AIComposition(**raw_response)
                logger.info(
                    f"Validated composition: {composition.title}, "
                    f"{len(composition.parts)} parts, "
                    f"{composition.duration_seconds:.1f}s"
                )
                return composition
            except Exception as e:
                logger.error(f"Validation failed: {e}")
                raise ValidationError(f"Failed to validate AI response: {e}") from e

        return raw_response

    def generate_to_file(
        self,
        prompt: str,
        output_path: Path,
        format: str = "json",
    ) -> AIComposition:
        """Generate and save composition to file.

        Args:
            prompt: Natural language description
            output_path: Where to save the composition
            format: Output format ("json", "yaml")

        Returns:
            AIComposition
        """
        composition = self.generate(prompt)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            import json
            output_path.write_text(
                composition.model_dump_json(indent=2)
            )
        elif format == "yaml":
            try:
                import yaml
            except ImportError:
                raise ImportError("yaml required for YAML output")
            with open(output_path, "w") as f:
                yaml.dump(composition.model_dump(), f, default_flow_style=False)
        else:
            raise ValueError(f"Unknown format: {format}")

        logger.info(f"Saved composition to {output_path}")
        return composition

    def generate_with_retry(
        self,
        prompt: str,
        max_attempts: int = 3,
    ) -> AIComposition:
        """Generate with validation retry.

        If validation fails, retry generation (useful for handling
        occasional malformed AI output).

        Args:
            prompt: Natural language description
            max_attempts: Maximum number of generation attempts

        Returns:
            AIComposition

        Raises:
            AIClientError: If all attempts fail
        """
        last_error = None

        for attempt in range(max_attempts):
            try:
                return self.generate(prompt)
            except ValidationError as e:
                last_error = e
                logger.warning(
                    f"Attempt {attempt + 1}/{max_attempts} failed: {e}. Retrying..."
                )

        raise AIClientError(
            f"Failed to generate valid composition after {max_attempts} attempts",
            cause=last_error
        )


class ValidationError(Exception):
    """Raised when AI response validation fails."""
    pass


# Convenience functions
def compose(
    prompt: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
) -> AIComposition:
    """Generate a composition from a prompt.

    Args:
        prompt: Natural language description of desired music
        api_key: Optional API key
        model: Optional model name
        temperature: Optional sampling temperature

    Returns:
        AIComposition

    Raises:
        AIClientError: If generation fails
    """
    composer = AIComposer(
        api_key=api_key,
        model=model,
        temperature=temperature,
    )
    return composer.generate(prompt)


def compose_from_file(
    prompt_file: Path,
    **kwargs
) -> AIComposition:
    """Generate from a prompt file.

    Args:
        prompt_file: Path to file containing prompt
        **kwargs: Additional arguments for compose()

    Returns:
        AIComposition
    """
    prompt = Path(prompt_file).read_text().strip()
    return compose(prompt, **kwargs)
```

### 5.3 Prompt Presets

Create `src/musicgen/composer/presets.py`:

```python
"""Prompt presets for common composition types."""

from typing import Dict, List


PRESETS: Dict[str, str] = {
    "classical_piano": "A classical piano piece with expressive melodies and rich harmonies. Include rubato and dynamic contrast.",
    "jazz_trio": "A jazz piano trio piece with walking bass and drums. Include swing rhythm, ii-V-I progressions, and improvisational sections.",
    "epic_orchestral": "An epic orchestral composition with full orchestra. Building intensity, powerful brass, soaring strings, and dramatic percussion.",
    "ambient_pad": "An ambient electronic piece with evolving synth pads, slow harmonic changes, and ethereal textures.",
    "folk_acoustic": "A folk-style acoustic guitar piece with simple melodies, major key tonality, and gentle rhythms.",
    "blues": "A 12-bar blues composition with guitar, bass, and drums. Include blues scale melodies and call-and-response patterns.",
    "minimalist": "A minimalist piece with repetitive patterns, gradual changes, and sparse textures inspired by Steve Reich or Philip Glass.",
    "romantic_string_quartet": "A romantic string quartet with expressive melodies, rich harmonies, and intimate dialogue between instruments.",
}


def get_preset(name: str) -> str:
    """Get a prompt preset by name.

    Args:
        name: Preset name

    Returns:
        Preset prompt string

    Raises:
        KeyError: If preset not found
    """
    return PRESETS[name]


def list_presets() -> List[str]:
    """List available preset names.

    Returns:
        List of preset names
    """
    return list(PRESETS.keys())


# Style modifiers that can be appended to prompts
MODIFIERS = {
    "faster": "Increase the tempo and use shorter note durations.",
    "slower": "Decrease the tempo and use longer, sustained notes.",
    "more_dynamics": "Add more dynamic contrast with wider velocity ranges.",
    "simpler": "Use simpler melodies with less motion and more repetition.",
    "more_complex": "Add more melodic and rhythmic complexity with varied patterns.",
    "darker": "Use minor key, lower register instruments, and more dissonance.",
    "brighter": "Use major key, higher register instruments, and consonant harmonies.",
}


def apply_modifier(prompt: str, modifier: str) -> str:
    """Apply a style modifier to a prompt.

    Args:
        prompt: Original prompt
        modifier: Modifier name

    Returns:
        Modified prompt
    """
    if modifier in MODIFIERS:
        return f"{prompt} {MODIFIERS[modifier]}"
    return prompt
```

### 5.4 Package Init

Create `src/musicgen/composer/__init__.py`:

```python
"""AI Composer module."""

from musicgen.composer.composer import (
    AIComposer,
    ValidationError,
    compose,
    compose_from_file,
)
from musicgen.composer.presets import (
    get_preset,
    list_presets,
    apply_modifier,
    PRESETS,
    MODIFIERS,
)

__all__ = [
    "AIComposer",
    "ValidationError",
    "compose",
    "compose_from_file",
    "get_preset",
    "list_presets",
    "apply_modifier",
    "PRESETS",
    "MODIFIERS",
]
```

### 5.5 Testing

Create `tests/test_composer.py`:

```python
"""Test AI composer."""

from musicgen.composer import AIComposer, ValidationError
from musicgen.ai_models import AIComposition


def test_composer_initialization():
    """Test composer can be initialized."""
    # Will fail without API key, but tests initialization
    try:
        composer = AIComposer(api_key="test-key")
        assert composer is not None
    except Exception as e:
        # Expected to fail on API call, not initialization
        assert "test-key" in str(e) or "API" in str(e)


def test_generate_requires_validation():
    """Test that generate validates by default."""
    # Mock test - actual generation requires API
    pass


def test_preset_system():
    """Test prompt presets."""
    from musicgen.composer.presets import (
        get_preset,
        list_presets,
        apply_modifier,
    )

    presets = list_presets()
    assert len(presets) > 0
    assert "classical_piano" in presets

    preset = get_preset("classical_piano")
    assert "piano" in preset.lower()

    modified = apply_modifier("A simple melody", "faster")
    assert "tempo" in modified.lower()


def test_composition_validation():
    """Test composition validation."""
    # Valid composition
    data = {
        "title": "Test",
        "tempo": 120,
        "key": {"tonic": "C", "mode": "major"},
        "parts": [{
            "name": "piano",
            "midi_program": 0,
            "midi_channel": 0,
            "notes": [
                {"note_name": "C4", "duration": 1.0},
            ]
        }]
    }

    comp = AIComposition(**data)
    assert comp.title == "Test"
    assert comp.duration_seconds == 0.5  # 1 quarter at 120 BPM


def test_invalid_composition_raises():
    """Test that invalid composition raises error."""
    # Missing required fields
    data = {
        "title": "Test",
        # Missing tempo, key, parts
    }

    with pytest.raises(ValidationError):
        AIComposition(**data)
```

## Deliverables

- `src/musicgen/composer/__init__.py`
- `src/musicgen/composer/composer.py`
- `src/musicgen/composer/presets.py`
- `tests/test_composer.py`

## Usage Examples

### Basic usage
```python
from musicgen.composer import compose

composition = compose("A peaceful piano melody in C major")
print(f"Generated: {composition.title}")
print(f"Duration: {composition.duration_seconds:.1f}s")
print(f"Instruments: {composition.instrument_names}")
```

### With custom settings
```python
from musicgen.composer import AIComposer

composer = AIComposer(
    temperature=0.6,  # More creative
    max_tokens=None,  # Unlimited
)
composition = composer.generate("An epic orchestral piece")
```

### Using presets
```python
from musicgen.composer import compose, get_preset, apply_modifier

preset = get_preset("jazz_trio")
prompt = apply_modifier(preset, "more_complex")
composition = compose(prompt)
```

### Save to file
```python
from musicgen.composer import AIComposer

composer = AIComposer()
composer.generate_to_file(
    "A romantic string quartet",
    output_path="output/composition.json",
    format="json"
)
```

## Next Steps

After completing this step:
- Step 6: Rendering engine (convert AIComposition → MIDI/Audio)
- Step 7: CLI redesign
- Step 8: Type safety
