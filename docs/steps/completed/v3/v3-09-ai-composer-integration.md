# V3-09: AI Composer Integration

**Status:** Pending
**Priority:** Critical
**Dependencies:** V3-05, V3-06, V3-07, V3-08

## Overview

Integrate all components into the AI Composer: system prompt injection, schema-guided generation, validation, and MIDI/audio rendering pipeline.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER PROMPT                                       │
│                   "An epic orchestral piece..."                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      COMPOSER REQUEST BUILDER                               │
│  • Load system prompt (music theory knowledge)                              │
│  • Add instrument/ensemble definitions                                      │
│  • Add orchestration constraints                                            │
│  • Configure validation requirements                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI (GEMINI)                                         │
│  • Receives: System prompt + user request + schema                          │
│  • Generates: Structured composition output                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       VALIDATION LAYER                                      │
│  • Parse JSON to Pydantic models                                            │
│  • Run voice leading validation                                            │
│  • Run orchestration validation                                             │
│  • Check minimum duration requirements                                      │
│  • Return errors or continue                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
              ❌ Validation Errors          ✓ Validation Passed
                    │                               │
                    ▼                               ▼
          Retry with feedback               MIDI GENERATOR
                                                │
                                                ▼
                                        ┌───────────────┴───────────────┐
                                        ▼                               ▼
                                  MIDI File                    STEM Export
                                        │                               │
                                        ▼                               ▼
                                  SFZ RENDERER                    SFZ RENDERER
                                        │                               │
                                        └───────────────┬───────────────┘
                                                        ▼
                                                AUDIO POST-PROCESS
                                                        │
                                                        ▼
                                              ┌─────────┴─────────┐
                                              ▼                   ▼
                                           MIXED AUDIO          INDIVIDUAL STEMS
                                              (WAV/MP3)            (WAV)
```

---

## Implementation

### Main Composer Class

```python
from pathlib import Path
from typing import Optional, Literal
import json
import logging

from musicgen.ai_models import (
    Composition, CompositionRequest, CompositionResponse,
    InstrumentFamily, StylePeriod, MusicalForm
)
from musicgen.validation import CompositionValidator, ValidationResult
from musicgen.midi import EnhancedMIDIGenerator
from musicgen.sfz import SFZRenderer, MultiInstrumentRenderer

logger = logging.getLogger(__name__)

class AIComposerV3:
    """AI-powered music composer with SFZ support and validation."""

    def __init__(
        self,
        system_prompt_path: Path | None = None,
        instrument_definitions_path: Path | None = None,
        sfz_libraries_root: Path | None = None,
        gemini_api_key: str | None = None,
    ):
        """Initialize the AI composer.

        Args:
            system_prompt_path: Path to music theory system prompt
            instrument_definitions_path: Path to YAML instrument definitions
            sfz_libraries_root: Root directory for SFZ libraries
            gemini_api_key: Google Gemini API key
        """
        # Load system prompt
        self.system_prompt = self._load_system_prompt(system_prompt_path)

        # Load instrument definitions
        self.instrument_definitions = self._load_instrument_definitions(
            instrument_definitions_path
        )

        # Initialize validators
        self.validator = CompositionValidator(self.instrument_definitions)

        # Initialize MIDI generator
        self.midi_generator = EnhancedMIDIGenerator()

        # Initialize SFZ renderer
        self.sfz_renderer = SFZRenderer(libraries_root=sfz_libraries_root)
        self.multi_renderer = MultiInstrumentRenderer(self.sfz_renderer)

        # Gemini client
        self.api_key = gemini_api_key

        # Configuration
        self.config = {
            "max_retries": 3,
            "validate_before_rendering": True,
            "auto_fix_violations": False,
            "default_output_format": "wav",
            "default_sample_rate": 44100,
        }

    def _load_system_prompt(self, path: Path | None) -> str:
        """Load the music theory system prompt."""
        if path is None:
            path = Path(__file__).parent / "resources" / "system_prompt.txt"

        default_prompt = """You are an expert music composer with deep knowledge of Western classical music theory..."""
        # [Full system prompt from V3-05]

        try:
            return Path(path).read_text()
        except FileNotFoundError:
            logger.warning(f"System prompt not found at {path}, using default")
            return default_prompt

    def _load_instrument_definitions(self, path: Path | None) -> dict:
        """Load instrument definitions from YAML."""
        if path is None:
            path = Path(__file__).parent / "resources" / "instrument_definitions.yaml"

        try:
            import yaml
            return yaml.safe_load(Path(path).read_text())
        except FileNotFoundError:
            logger.warning(f"Instrument definitions not found at {path}")
            return {}

    def compose(
        self,
        prompt: str,
        duration_seconds: float | None = None,
        key: str | None = None,
        style: StylePeriod | None = None,
        form: MusicalForm | None = None,
        ensemble: str | None = None,
        instruments: list[str] | None = None,
        output_format: Literal["midi", "wav", "mp3", "all"] = "midi",
        validate: bool = True,
        max_retries: int | None = None,
    ) -> CompositionResponse:
        """Generate a musical composition from a natural language prompt.

        Args:
            prompt: Natural language description of desired music
            duration_seconds: Target duration in seconds
            key: Key signature (e.g., "C minor")
            style: Stylistic period
            form: Musical form
            ensemble: Ensemble preset (e.g., "string_quartet")
            instruments: Specific instruments to include
            output_format: Output format(s)
            validate: Run validation before returning
            max_retries: Maximum retry attempts for validation failures

        Returns:
            CompositionResponse with composition and metadata
        """
        max_retries = max_retries or self.config["max_retries"]

        # Build request
        request = CompositionRequest(
            prompt=prompt,
            duration_seconds=duration_seconds,
            key_signature=key,
            style_period=style,
            musical_form=form,
            ensemble=ensemble,
            instruments=instruments,
            output_format=output_format,
        )

        # Generate with retry loop
        for attempt in range(max_retries):
            try:
                response = self._generate_with_retry(request, attempt, validate)
                return response

            except Exception as e:
                logger.error(f"Generation attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise

        raise RuntimeError("Failed to generate composition after maximum retries")

    def _generate_with_retry(
        self,
        request: CompositionRequest,
        attempt: int,
        validate: bool,
    ) -> CompositionResponse:
        """Generate composition with validation and retry logic."""
        # Build full prompt
        full_prompt = self._build_generation_prompt(request, attempt)

        # Call AI
        composition = self._call_gemini(full_prompt)

        # Validate if requested
        if validate:
            validation_result = self.validator.validate(composition)

            if not validation_result.valid:
                logger.warning(
                    f"Validation failed on attempt {attempt + 1}: "
                    f"{validation_result.error_count} errors"
                )

                # Build feedback for retry
                feedback = self._build_validation_feedback(validation_result)

                # If this is the last attempt, still return with errors
                if attempt >= self.config["max_retries"] - 1:
                    return CompositionResponse(
                        composition=composition,
                        metadata={"attempts": attempt + 1},
                        validation_errors=[e.description for e in
                                         validation_result.voice_leading_errors +
                                         validation_result.orchestration_errors],
                    )

                # Otherwise raise for retry
                raise ValueError(f"Validation failed: {feedback}")

        return CompositionResponse(
            composition=composition,
            metadata={"attempts": attempt + 1}
        )

    def _build_generation_prompt(
        self,
        request: CompositionRequest,
        attempt: int,
    ) -> str:
        """Build the full prompt for AI generation."""
        prompt_parts = [
            self.system_prompt,
            "\n\n",
            "=" * 60,
            "\nINSTRUMENT DEFINITIONS:\n\n",
            json.dumps(self._get_relevant_instruments(request), indent=2),
            "\n",
            "=" * 60,
            "\nREQUEST:\n\n",
            f"Prompt: {request.prompt}\n",
        ]

        # Add specific constraints
        if request.duration_seconds:
            prompt_parts.append(f"Target Duration: {request.duration_seconds} seconds\n")

        if request.key_signature:
            prompt_parts.append(f"Key: {request.key_signature}\n")

        if request.style_period:
            prompt_parts.append(f"Style: {request.style_period}\n")

        if request.musical_form:
            prompt_parts.append(f"Form: {request.musical_form}\n")

        if request.ensemble:
            ensemble_def = self.instrument_definitions.get("ensembles", {}).get(request.ensemble)
            if ensemble_def:
                prompt_parts.append(f"\nEnsemble: {ensemble_def['name']}\n")
                prompt_parts.append(f"Instruments: {', '.join(ensemble_def['instruments'])}\n")

        if request.instruments:
            prompt_parts.append(f"\nInstruments: {', '.join(request.instruments)}\n")

        # Add retry feedback
        if attempt > 0:
            prompt_parts.append("\n[PREVIOUS ATTEMPT HAD VALIDATION ERRORS. ")
            prompt_parts.append("PLEASE CORRECT THE FOLLOWING ISSUES:]\n")
            prompt_parts.append(self._get_previous_feedback())

        # Add schema instructions
        prompt_parts.extend([
            "\n" + "=" * 60,
            "\nOUTPUT SCHEMA:\n",
            "Please respond with a JSON object matching the Composition schema. ",
            "Include all required fields: title, key_signature, initial_tempo_bpm, ",
            "time_signature, and parts (with notes, keyswitches, cc_events, etc.).\n",
        ])

        return "".join(prompt_parts)

    def _get_relevant_instruments(self, request: CompositionRequest) -> dict:
        """Get relevant instrument definitions for the request."""
        if request.ensemble:
            ensemble = self.instrument_definitions.get("ensembles", {}).get(request.ensemble)
            if ensemble:
                return {
                    k: v for k, v in self.instrument_definitions.get("instruments", {}).items()
                    if k in ensemble.get("instruments", [])
                }

        if request.instruments:
            return {
                k: v for k, v in self.instrument_definitions.get("instruments", {}).items()
                if k in request.instruments
            }

        # Return all instruments if no filter
        return self.instrument_definitions.get("instruments", {})

    def _call_gemini(self, prompt: str) -> Composition:
        """Call Gemini API with structured output."""
        import google.generativeai as genai

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel('gemini-2.5-pro')

        # Generate with schema
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                response_schema=Composition.model_json_schema(),
            )
        )

        # Parse response
        data = json.loads(response.text)
        return Composition(**data)

    def render(
        self,
        composition: Composition,
        output_path: Path,
        format: str = "wav",
        stems: bool = False,
    ) -> Path:
        """Render a composition to audio.

        Args:
            composition: The composition to render
            output_path: Output file path
            format: Output format (wav, mp3)
            stems: Also export individual instrument stems

        Returns:
            Path to rendered audio file
        """
        # Generate MIDI
        midi_path = output_path.with_suffix('.mid')
        self.midi_generator.generate(composition, midi_path)

        # Build instrument mapping for SFZ
        instrument_mapping = {}
        for part in composition.parts:
            inst_def = self.instrument_definitions.get(part.instrument_name, {})
            sfz_file = inst_def.get("sfz_file")
            if sfz_file:
                instrument_mapping[part.midi_channel] = Path(sfz_file)

        # Render to audio
        if stems:
            # Render stems and mix
            return self.multi_renderer.render_composition(
                midi_path,
                output_path,
                instrument_mapping,
                render_stems=True,
            )
        else:
            # Single file render (using first SFZ)
            if instrument_mapping:
                sfz_file = next(v for v in instrument_mapping.values() if v is not None)
                return self.sfz_renderer.render(midi_path, output_path, sfz_file)
            else:
                # Fallback to pretty_midi
                return self._render_with_pretty_midi(midi_path, output_path, format)

    def _render_with_pretty_midi(
        self,
        midi_path: Path,
        output_path: Path,
        format: str,
    ) -> Path:
        """Fallback rendering with pretty_midi."""
        import pretty_midi

        midi = pretty_midi.PrettyMIDI(str(midi_path))
        audio = midi.synthesize(fs=self.config["default_sample_rate"])

        # Save audio
        output_path = Path(output_path)
        if format == "wav":
            self._save_wav(audio, output_path)
        elif format == "mp3":
            self._save_mp3(audio, output_path)

        return output_path

    def compose_and_render(
        self,
        prompt: str,
        output_path: Path,
        **kwargs,
    ) -> tuple[Composition, Path]:
        """Convenience method: compose and render in one call.

        Args:
            prompt: Natural language description
            output_path: Where to save the rendered audio
            **kwargs: Passed to compose()

        Returns:
            Tuple of (composition, rendered_audio_path)
        """
        response = self.compose(prompt, **kwargs)
        audio_path = self.render(response.composition, output_path, **kwargs)
        return response.composition, audio_path
```

---

## CLI Integration

```python
import click

@click.command()
@click.argument("prompt")
@click.option("--duration", type=float, help="Duration in seconds")
@click.option("--key", help="Key signature (e.g., 'C minor')")
@click.option("--style", type=click.Choice(["baroque", "classical", "romantic", "modern", "film_score"]),
              help="Stylistic period")
@click.option("--form", type=click.Choice(["binary", "ternary", "rondo", "sonata", "through_composed"]),
              help="Musical form")
@click.option("--ensemble", help="Ensemble preset")
@click.option("--output", "-o", default="output", help="Output directory")
@click.option("--format", type=click.Choice(["midi", "wav", "mp3", "all"]), default="wav")
@click.option("--stems", is_flag=True, help="Export individual instrument stems")
@click.option("--no-validate", is_flag=True, help="Skip validation")
def compose(
    prompt: str,
    duration: float | None,
    key: str | None,
    style: str | None,
    form: str | None,
    ensemble: str | None,
    output: str,
    format: str,
    stems: bool,
    no_validate: bool,
):
    """Generate music from a natural language prompt."""
    from musicgen.composer_v3 import AIComposerV3

    composer = AIComposerV3()

    # Generate
    response = composer.compose(
        prompt=prompt,
        duration_seconds=duration,
        key_signature=key,
        style_period=style,
        musical_form=form,
        ensemble=ensemble,
        output_format=format,
        validate=not no_validate,
    )

    click.echo(f"Generated: {response.composition.title}")
    click.echo(f"Duration: {response.composition.duration:.1f}s")
    click.echo(f"Instruments: {response.composition.instrument_count}")

    if response.validation_errors:
        click.echo(f"\nValidation Warnings ({len(response.validation_errors)}):")
        for error in response.validation_errors:
            click.echo(f"  - {error}")

    # Render if requested
    if format in ("wav", "mp3", "all"):
        output_dir = Path(output)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{response.composition.title.replace(' ', '_')}"
        audio_path = composer.render(
            response.composition,
            output_path,
            format=format if format != "all" else "wav",
            stems=stems,
        )

        click.echo(f"\nRendered to: {audio_path}")
```

---

## Implementation Tasks

1. [ ] Create `AIComposerV3` main class
2. [ ] Integrate system prompt loading
3. [ ] Integrate instrument definition loading
4. [ ] Implement schema-guided generation with Gemini
5. [ ] Integrate validation layer
6. [ ] Add retry logic with feedback
7. [ ] Integrate MIDI generator
8. [ ] Integrate SFZ renderer
9. [ ] Create CLI command
10. [ ] Add error handling and logging

## Success Criteria

- End-to-end generation works from prompt to audio
- Validation catches errors before rendering
- Retry loop improves output quality
- CLI provides good user feedback
- All components integrate cleanly

## Next Steps

- V3-10: Testing and Quality Assurance
- V3-11: Documentation and Examples
