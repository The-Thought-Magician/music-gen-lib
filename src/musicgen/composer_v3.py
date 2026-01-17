"""V3 AI Composer integration module.

This module provides the AIComposerV3 class that integrates all V3 components:
- System prompt loading with music theory knowledge
- Instrument definitions from YAML
- Schema-guided generation with Gemini API
- Validation pipeline with voice leading and orchestration rules
- MIDI generation with keyswitch support
- SFZ rendering with fallback to pretty_midi
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    pass

from musicgen.ai_client import GeminiClient
from musicgen.ai_client.exceptions import AIClientError
from musicgen.ai_models.v3 import (
    Composition,
    CompositionRequest,
    CompositionResponse,
    MusicalForm,
    StylePeriod,
    TimeSignature,
)
from musicgen.midi import EnhancedMIDIGenerator
from musicgen.orchestration.definitions import (
    InstrumentDefinition,
    InstrumentLibrary,
    get_instrument_library,
)
from musicgen.sfz import (
    MultiInstrumentRenderer,
    SFZRenderer,
    SFZRendererError,
)
from musicgen.validation import (
    CompositionValidator,
    ValidationConfig,
    ValidationResult,
)

logger = logging.getLogger(__name__)

# Default configuration values
DEFAULT_MAX_RETRIES = 3
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_TEMPERATURE = 0.8
DEFAULT_MODEL = "gemini-2.5-pro"


class ComposerConfig:
    """Configuration for AIComposerV3.

    Attributes:
        max_retries: Maximum number of generation attempts for validation failures
        validate_before_rendering: Whether to run validation before returning composition
        auto_fix_violations: Whether to automatically fix validation violations
        default_output_format: Default output format (midi, wav, mp3, all)
        default_sample_rate: Default audio sample rate
        temperature: AI sampling temperature
        model: AI model name
        validation_config: Validation behavior configuration
    """

    def __init__(
        self,
        max_retries: int = DEFAULT_MAX_RETRIES,
        validate_before_rendering: bool = True,
        auto_fix_violations: bool = False,
        default_output_format: Literal["midi", "wav", "mp3", "all"] = "midi",
        default_sample_rate: int = DEFAULT_SAMPLE_RATE,
        temperature: float = DEFAULT_TEMPERATURE,
        model: str | None = None,
        validation_config: ValidationConfig | None = None,
    ):
        self.max_retries = max_retries
        self.validate_before_rendering = validate_before_rendering
        self.auto_fix_violations = auto_fix_violations
        self.default_output_format = default_output_format
        self.default_sample_rate = default_sample_rate
        self.temperature = temperature
        self.model = model or DEFAULT_MODEL
        self.validation_config = validation_config or ValidationConfig()


class AIComposerV3:
    """AI-powered music composer with SFZ support and validation.

    This class integrates all V3 components to provide end-to-end music generation:
    - Loads system prompt with comprehensive music theory knowledge
    - Loads instrument definitions with SFZ mappings
    - Generates compositions using Gemini API with schema validation
    - Validates voice leading and orchestration rules
    - Generates MIDI with keyswitch support
    - Renders to audio using SFZ libraries or pretty_midi fallback

    Example:
        >>> from musicgen.composer_v3 import AIComposerV3
        >>> composer = AIComposerV3()
        >>> response = composer.compose(
        ...     prompt="A gentle string quartet in C major",
        ...     duration_seconds=120,
        ...     style="classical"
        ... )
        >>> # Render to audio
        >>> audio_path = composer.render(
        ...     response.composition,
        ...     output_path="output.wav"
        ... )
    """

    def __init__(
        self,
        system_prompt_path: Path | str | None = None,
        instrument_definitions_path: Path | str | None = None,
        sfz_libraries_root: Path | str | None = None,
        gemini_api_key: str | None = None,
        config: ComposerConfig | None = None,
    ):
        """Initialize the AI composer.

        Args:
            system_prompt_path: Path to music theory system prompt file.
                If None, uses resources/system_prompt_v3.txt.
            instrument_definitions_path: Path to YAML instrument definitions.
                If None, uses resources/instrument_definitions.yaml.
            sfz_libraries_root: Root directory for SFZ libraries.
            gemini_api_key: Google Gemini API key. If None, reads from config.
            config: Optional composer configuration.

        Raises:
            FileNotFoundError: If system prompt file not found.
            RuntimeError: If required dependencies are missing.
        """
        self.config = config or ComposerConfig()

        # Load system prompt
        self.system_prompt = self._load_system_prompt(system_prompt_path)

        # Load instrument definitions
        self.instrument_library: InstrumentLibrary = self._load_instrument_definitions(
            instrument_definitions_path
        )

        # Initialize validators
        self.validator = CompositionValidator(
            config=self.config.validation_config
        )

        # Initialize MIDI generator
        self.midi_generator = EnhancedMIDIGenerator()

        # Initialize SFZ renderer
        try:
            self.sfz_renderer = SFZRenderer(
                libraries_root=sfz_libraries_root,
                sample_rate=self.config.default_sample_rate,
            )
            self.multi_renderer = MultiInstrumentRenderer(self.sfz_renderer)
            self._sfz_available = True
        except SFZRendererError:
            logger.warning(
                "SFZ renderer not available. "
                "Audio rendering will fall back to pretty_midi."
            )
            self.sfz_renderer = None
            self.multi_renderer = None
            self._sfz_available = False

        # Initialize AI client
        self.client = GeminiClient(
            api_key=gemini_api_key,
            model=self.config.model,
            temperature=self.config.temperature,
            log_requests=True,
        )

        # Feedback storage for retry loop
        self._last_validation_feedback: list[str] = []

    def _load_system_prompt(self, path: Path | str | None) -> str:
        """Load the music theory system prompt.

        Args:
            path: Path to system prompt file. If None, uses default location.

        Returns:
            System prompt text.
        """
        if path is None:
            # Default path relative to this file
            base_dir = Path(__file__).parent.parent.parent
            path = base_dir / "resources" / "system_prompt_v3.txt"

        path = Path(path)

        if path.exists():
            logger.debug(f"Loading system prompt from {path}")
            return path.read_text(encoding="utf-8")

        # Fallback to basic prompt
        logger.warning(f"System prompt not found at {path}, using default")
        return self._get_default_system_prompt()

    def _get_default_system_prompt(self) -> str:
        """Get a basic default system prompt."""
        return """You are an expert music composer with deep knowledge of Western classical music theory.

Generate compositions following these principles:
1. Voice leading: Avoid parallel fifths and octaves
2. Harmony: Use functional progressions with proper cadences
3. Orchestration: Write idiomatically for each instrument
4. Form: Create coherent musical structures

Your response must be valid JSON matching the Composition schema.
"""

    def _load_instrument_definitions(
        self,
        _path: Path | str | None,
    ) -> InstrumentLibrary:
        """Load instrument definitions from YAML.

        Args:
            _path: Path to instrument definitions YAML (unused, loads from default location).

        Returns:
            InstrumentLibrary with all definitions.
        """
        try:
            return get_instrument_library()
        except FileNotFoundError:
            logger.warning("Instrument definitions not found, using empty library")
            return InstrumentLibrary(instruments={}, ensembles={})

    def compose(
        self,
        prompt: str,
        duration_seconds: float | None = None,
        key: str | None = None,
        key_signature: str | None = None,
        style: StylePeriod | None = None,
        style_period: StylePeriod | None = None,
        form: MusicalForm | None = None,
        musical_form: MusicalForm | None = None,
        ensemble: str | None = None,
        instruments: list[str] | None = None,
        output_format: Literal["midi", "wav", "mp3", "all"] = "midi",
        validate: bool = True,
        max_retries: int | None = None,
    ) -> CompositionResponse:
        """Generate a musical composition from a natural language prompt.

        Args:
            prompt: Natural language description of desired music.
            duration_seconds: Target duration in seconds.
            key: Key signature (e.g., "C minor"). Deprecated: use key_signature.
            key_signature: Key signature (e.g., "C major", "A minor").
            style: Stylistic period. Deprecated: use style_period.
            style_period: Stylistic period (baroque, classical, romantic, etc.).
            form: Musical form. Deprecated: use musical_form.
            musical_form: Musical form (binary, ternary, sonata, etc.).
            ensemble: Ensemble preset (e.g., "string_quartet").
            instruments: Specific instruments to include.
            output_format: Output format(s) - midi, wav, mp3, or all.
            validate: Run validation before returning.
            max_retries: Maximum retry attempts for validation failures.

        Returns:
            CompositionResponse with composition and metadata.

        Raises:
            AIClientError: If AI generation fails after all retries.
            ValidationError: If validation fails and validate=True.
        """
        # Handle deprecated parameter names
        key_signature = key_signature or key
        style_period = style_period or style
        musical_form = musical_form or form

        max_retries = max_retries or self.config.max_retries

        # Build request
        request = CompositionRequest(
            prompt=prompt,
            duration_seconds=duration_seconds,
            key_signature=key_signature,
            style_period=style_period,
            musical_form=musical_form,
            ensemble=ensemble,
            instruments=instruments,
            output_format=output_format,
        )

        # Clear previous feedback
        self._last_validation_feedback = []

        # Generate with retry loop
        last_error = None
        for attempt in range(max_retries):
            try:
                logger.info(f"Generation attempt {attempt + 1}/{max_retries}")
                response = self._generate_with_retry(request, attempt, validate)
                logger.info(f"Generation succeeded on attempt {attempt + 1}")
                return response

            except ValueError as e:
                # Validation error - build feedback and retry
                last_error = e
                feedback = str(e)
                self._last_validation_feedback.append(feedback)
                logger.warning(
                    f"Validation failed on attempt {attempt + 1}: {feedback}"
                )

                if attempt >= max_retries - 1:
                    # Last attempt failed, return response with errors
                    logger.error("Max retries reached, returning with validation errors")
                    return CompositionResponse(
                        composition=self._create_minimal_composition(request),
                        metadata={"attempts": attempt + 1, "max_retries_exceeded": True},
                        validation_errors=self._last_validation_feedback,
                    )

            except AIClientError as e:
                # AI generation error - don't retry for API errors
                last_error = e
                logger.error(f"AI generation failed: {e}")
                raise

        raise RuntimeError(
            f"Failed to generate composition after {max_retries} attempts"
        ) from last_error

    def _generate_with_retry(
        self,
        request: CompositionRequest,
        attempt: int,
        validate: bool,
    ) -> CompositionResponse:
        """Generate composition with validation and retry logic.

        Args:
            request: Composition request.
            attempt: Current attempt number (0-indexed).
            validate: Whether to run validation.

        Returns:
            CompositionResponse with generated composition.

        Raises:
            ValueError: If validation fails.
            AIClientError: If AI generation fails.
        """
        # Build full prompt
        full_prompt = self._build_generation_prompt(request, attempt)

        # Get schema for validation
        schema = self._get_composition_schema()

        # Call AI with schema validation
        try:
            raw_response = self.client.generate(
                prompt=full_prompt,
                schema=schema,
            )
        except AIClientError as e:
            logger.error(f"AI client error: {e}")
            raise

        # Parse response
        composition = self._parse_composition(raw_response)

        # Validate if requested
        if validate and self.config.validate_before_rendering:
            validation_result = self.validator.validate(composition)

            if not validation_result.is_valid:
                logger.warning(
                    f"Validation failed: {validation_result.error_count} errors, "
                    f"{validation_result.warning_count} warnings"
                )

                # Build feedback for retry
                feedback = self._build_validation_feedback(validation_result)
                raise ValueError(feedback)

            # Log validation success
            logger.info(
                f"Validation passed: {validation_result.total_notes} notes, "
                f"{validation_result.instruments_checked} instruments"
            )

        return CompositionResponse(
            composition=composition,
            metadata={"attempts": attempt + 1},
        )

    def _build_generation_prompt(
        self,
        request: CompositionRequest,
        attempt: int,
    ) -> str:
        """Build the full prompt for AI generation.

        Args:
            request: Composition request.
            attempt: Current attempt number.

        Returns:
            Complete prompt string.
        """
        prompt_parts = [
            self.system_prompt,
            "\n\n",
            "=" * 60,
            "\nAVAILABLE INSTRUMENTS:\n\n",
            self._format_instruments_for_prompt(request),
            "\n",
            "=" * 60,
            "\nCOMPOSITION REQUEST:\n\n",
        ]

        # Main prompt
        prompt_parts.append(f"Description: {request.prompt}\n")

        # Add specific constraints
        if request.duration_seconds:
            prompt_parts.append(
                f"Target Duration: {request.duration_seconds} seconds "
                f"(approximately {request.duration_seconds // 60} minutes)\n"
            )

        if request.key_signature:
            prompt_parts.append(f"Key: {request.key_signature}\n")

        if request.style_period:
            prompt_parts.append(f"Style Period: {request.style_period}\n")

        if request.musical_form:
            prompt_parts.append(f"Musical Form: {request.musical_form}\n")

        # Handle ensemble or instruments
        if request.ensemble:
            ensemble_def = self.instrument_library.get_ensemble(request.ensemble)
            if ensemble_def:
                prompt_parts.append(f"\nEnsemble: {ensemble_def.name}\n")
                prompt_parts.append(f"Instruments: {', '.join(ensemble_def.instruments)}\n")

                # Add instrument details
                for inst_key in ensemble_def.instruments:
                    inst = self.instrument_library.get_instrument(inst_key)
                    if inst:
                        prompt_parts.append(
                            f"  - {inst.name}: MIDI program {inst.midi_program}, "
                            f"channel {inst.midi_channel}\n"
                        )
            else:
                logger.warning(f"Ensemble '{request.ensemble}' not found in definitions")

        if request.instruments:
            prompt_parts.append(f"\nInstruments: {', '.join(request.instruments)}\n")

        # Add retry feedback
        if attempt > 0 and self._last_validation_feedback:
            prompt_parts.append("\n")
            prompt_parts.append("=" * 60)
            prompt_parts.append("\n[PREVIOUS ATTEMPT HAD VALIDATION ERRORS. ")
            prompt_parts.append("PLEASE CORRECT THE FOLLOWING ISSUES:]\n")
            for feedback in self._last_validation_feedback[-3:]:  # Last 3 feedbacks
                prompt_parts.append(f"  - {feedback}\n")
            prompt_parts.append("=" * 60)
            prompt_parts.append("\n")

        # Add schema instructions
        prompt_parts.extend([
            "\n" + "=" * 60,
            "\nOUTPUT REQUIREMENTS:\n",
            "Your response must be valid JSON matching the Composition schema:\n",
            "  - title: string (composition title)\n",
            "  - key_signature: string (e.g., 'C major', 'A minor')\n",
            "  - initial_tempo_bpm: number (BPM, e.g., 120)\n",
            "  - time_signature: {numerator: int, denominator: int}\n",
            "  - parts: array of instrument parts with:\n",
            "    - instrument_name: string\n",
            "    - instrument_family: string (strings, woodwinds, brass, percussion, keyboards)\n",
            "    - midi_channel: int (0-15)\n",
            "    - midi_program: int (0-127)\n",
            "    - notes: array with:\n",
            "      - pitch: int (MIDI note number, 0-127)\n",
            "      - start_time: float (seconds)\n",
            "      - duration: float (seconds)\n",
            "      - velocity: int (0-127)\n",
            "    - keyswitches: array (optional) with:\n",
            "      - time: float\n",
            "      - keyswitch: int\n",
            "    - cc_events: array (optional)\n",
            "    - pitch_bends: array (optional)\n",
            "=" * 60,
            "\n",
        ])

        return "".join(prompt_parts)

    def _format_instruments_for_prompt(self, request: CompositionRequest) -> str:
        """Format instrument definitions for the AI prompt.

        Args:
            request: Composition request to filter instruments.

        Returns:
            Formatted instrument definitions string.
        """
        # Get relevant instruments
        if request.ensemble:
            ensemble = self.instrument_library.get_ensemble(request.ensemble)
            if ensemble:
                instruments = [
                    self.instrument_library.get_instrument(key)
                    for key in ensemble.instruments
                ]
                instruments = [i for i in instruments if i is not None]
            else:
                instruments = list(self.instrument_library.instruments.values())
        elif request.instruments:
            instruments = [
                self.instrument_library.get_instrument(name)
                for name in request.instruments
            ]
            instruments = [i for i in instruments if i is not None]
        else:
            # Show all instruments (limit to prevent huge prompts)
            instruments = list(self.instrument_library.instruments.values())[:20]

        lines = []
        for inst in instruments:
            if isinstance(inst, InstrumentDefinition):
                lines.append(f"- {inst.name}")
                lines.append(f"  Family: {inst.family}")
                lines.append(f"  Range: {inst.range.min}-{inst.range.max}")
                lines.append(f"  MIDI Program: {inst.midi_program}")
                lines.append(f"  Default Channel: {inst.midi_channel}")
                if inst.articulations:
                    arts = ", ".join(inst.articulations.keys())
                    lines.append(f"  Articulations: {arts}")
                lines.append("")

        return "\n".join(lines)

    def _get_composition_schema(self) -> str:
        """Get the Composition schema as YAML for the prompt.

        Returns:
            YAML schema string.
        """
        return """Composition:
  title: string (required)
  composer: string (optional, default "AI Composer")
  description: string (optional)
  style_period: string (optional: baroque, classical, romantic, modern, film_score)
  musical_form: string (optional: binary, ternary, rondo, sonata, theme_and_variations)
  key_signature: string (required, e.g. "C major", "A minor")
  initial_tempo_bpm: number (required, >0)
  tempo_marking: string (optional: adagio, andante, moderato, allegro, presto)
  time_signature:
    numerator: int (required, >=1)
    denominator: int (required, >=1)
  tempo_changes: array (optional)
    - tempo_bpm: number
      time: number (seconds)
      tempo_marking: string (optional)
  time_signature_changes: array (optional)
    - time_signature: {numerator, denominator}
      time: number (seconds)
  section_markers: array (optional)
    - label: string
      time: number (seconds)
      rehearsal_letter: string (optional)
  dynamic_changes: array (optional)
    - dynamic: string (ppp, pp, p, mp, mf, f, ff, fff)
      time: number (seconds)
      ramp_duration: number (optional, seconds)
  parts: array (required, at least 1)
    - instrument_name: string (required)
      instrument_family: string (required: strings, woodwinds, brass, percussion, keyboards)
      midi_channel: int (required, 0-15)
      midi_program: int (required, 0-127)
      solo: boolean (optional, default false)
      notes: array (required)
        - pitch: int (0-127, required)
          start_time: float (seconds, >=0, required)
          duration: float (seconds, >0, required)
          velocity: int (0-127, required)
          articulation: string (optional: legato, staccato, spiccato, pizzicato, tremolo, etc.)
      keyswitches: array (optional)
        - time: float (seconds)
          keyswitch: int (0-127)
          channel: int (0-15)
      cc_events: array (optional)
        - controller: int (0-127)
          value: int (0-127)
          start_time: float (seconds)
          channel: int (0-15)
      pitch_bends: array (optional)
        - value: int (0-16383, 8192 is center)
          start_time: float (seconds)
          channel: int (0-15)
      program_changes: array (optional)
        - program: int (0-127)
          time: float (seconds)
          channel: int (0-15)
  performance_notes: string (optional)
"""

    def _parse_composition(self, raw_response: dict) -> Composition:
        """Parse raw AI response into a Composition object.

        Args:
            raw_response: Raw JSON response from AI.

        Returns:
            Parsed Composition object.

        Raises:
            ValueError: If response is invalid.
        """
        try:
            # Handle nested composition structure (AI may return "Composition" or "composition")
            data = raw_response.get("composition") or raw_response.get("Composition") or raw_response
            if not isinstance(data, dict):
                data = raw_response

            return Composition(**data)

        except Exception as e:
            raise ValueError(f"Failed to parse composition from AI response: {e}") from e

    def _create_minimal_composition(self, request: CompositionRequest) -> Composition:
        """Create a minimal valid composition as fallback.

        Args:
            request: Original composition request.

        Returns:
            Minimal valid Composition.
        """
        from musicgen.ai_models.v3 import Note

        # Determine key from request
        key = request.key_signature or "C major"

        # Create a simple C major scale melody
        notes = [
            Note(pitch=60, start_time=0.0, duration=0.5, velocity=80),  # C4
            Note(pitch=62, start_time=0.5, duration=0.5, velocity=80),  # D4
            Note(pitch=64, start_time=1.0, duration=0.5, velocity=80),  # E4
            Note(pitch=65, start_time=1.5, duration=0.5, velocity=80),  # F4
            Note(pitch=67, start_time=2.0, duration=1.0, velocity=80),  # G4
            Note(pitch=64, start_time=3.0, duration=0.5, velocity=80),  # E4
            Note(pitch=62, start_time=3.5, duration=0.5, velocity=80),  # D4
            Note(pitch=60, start_time=4.0, duration=2.0, velocity=80),  # C4
        ]

        from musicgen.ai_models.v3 import InstrumentPart

        # Create a simple piano part
        part = InstrumentPart(
            instrument_name="Piano",
            instrument_family="keyboards",
            midi_channel=0,
            midi_program=0,
            notes=notes,
        )

        return Composition(
            title=f"Composition: {request.prompt[:50]}",
            key_signature=key,
            initial_tempo_bpm=120.0,
            time_signature=TimeSignature(numerator=4, denominator=4),
            parts=[part],
        )

    def _build_validation_feedback(self, result: ValidationResult) -> str:
        """Build feedback string from validation result.

        Args:
            result: Validation result.

        Returns:
            Formatted feedback string.
        """
        feedback_parts = []

        # Voice leading errors
        if result.voice_leading_errors:
            vl_count = len(result.voice_leading_errors)
            feedback_parts.append(f"{vl_count} voice leading issue(s):")
            for error in result.voice_leading_errors[:5]:  # Limit to 5
                feedback_parts.append(f"  - {error.description}")

        # Orchestration errors
        if result.orchestration_errors:
            orch_count = len(result.orchestration_errors)
            feedback_parts.append(f"{orch_count} orchestration issue(s):")
            for error in result.orchestration_errors[:5]:  # Limit to 5
                feedback_parts.append(f"  - {error.description}")

        return "\n".join(feedback_parts)

    def render(
        self,
        composition: Composition,
        output_path: Path | str,
        format: str = "wav",
        stems: bool = False,
        normalize: bool = True,
        fade_out: float = 0.0,
    ) -> Path:
        """Render a composition to audio.

        Args:
            composition: The composition to render.
            output_path: Output file path.
            format: Output format (wav, mp3, midi).
            stems: Also export individual instrument stems.
            normalize: Normalize output audio.
            fade_out: Fade out duration in seconds.

        Returns:
            Path to rendered audio file.

        Raises:
            FileNotFoundError: If output directory cannot be created.
            RuntimeError: If rendering fails.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # For MIDI-only output, just generate MIDI
        if format == "midi":
            return self._render_to_midi(composition, output_path)

        # Generate MIDI first
        midi_path = output_path.with_suffix(".mid")
        self.midi_generator.generate(composition, midi_path)

        # Build instrument mapping for SFZ
        instrument_mapping = self._build_instrument_mapping(composition)

        # Try SFZ rendering first
        if self._sfz_available and instrument_mapping:
            try:
                if stems and len(instrument_mapping) > 1:
                    # Multi-instrument rendering with stems
                    return self.multi_renderer.render_composition(
                        midi_path=midi_path,
                        output_path=output_path.with_suffix(".wav"),
                        instrument_mapping=instrument_mapping,
                        render_stems=True,
                        stem_output_dir=output_path.parent,
                        normalize=normalize,
                        fade_out=fade_out,
                    )
                elif instrument_mapping:
                    # Single SFZ rendering
                    sfz_file = next(
                        (v for v in instrument_mapping.values() if v is not None),
                        None
                    )
                    if sfz_file:
                        return self.sfz_renderer.render(
                            midi_path=midi_path,
                            output_path=output_path.with_suffix(".wav"),
                            sfz_file=sfz_file,
                            normalize=normalize,
                            fade_out=fade_out,
                        )
            except SFZRendererError as e:
                logger.warning(f"SFZ rendering failed, falling back to pretty_midi: {e}")

        # Fallback to pretty_midi
        return self._render_with_pretty_midi(
            midi_path,
            output_path.with_suffix(".wav"),
            format,
        )

    def _build_instrument_mapping(
        self,
        composition: Composition,
    ) -> dict[int, Path | str | None]:
        """Build MIDI channel to SFZ file mapping.

        Args:
            composition: The composition.

        Returns:
            Mapping of MIDI channel to SFZ file path.
        """
        mapping = {}

        for part in composition.parts:
            # Try to find matching instrument definition
            sfz_file = None
            for inst in self.instrument_library.instruments.values():
                if isinstance(inst, InstrumentDefinition) and inst.name.lower() == part.instrument_name.lower():
                    sfz_file = inst.sfz_file
                    break

            mapping[part.midi_channel] = sfz_file

        return mapping

    def _render_to_midi(
        self,
        composition: Composition,
        output_path: Path,
    ) -> Path:
        """Render composition to MIDI file only.

        Args:
            composition: The composition to render.
            output_path: Output path (will have .mid extension if not present).

        Returns:
            Path to MIDI file.
        """
        if not output_path.suffix:
            output_path = output_path.with_suffix(".mid")

        return self.midi_generator.generate(composition, output_path)

    def _render_with_pretty_midi(
        self,
        midi_path: Path,
        output_path: Path,
        format: str,
    ) -> Path:
        """Fallback rendering with pretty_midi.

        Args:
            midi_path: Path to MIDI file.
            output_path: Output audio path.
            format: Output format (wav, mp3).

        Returns:
            Path to rendered audio file.
        """
        try:
            import pretty_midi
        except ImportError as err:
            raise RuntimeError(
                "pretty_midi library is required for fallback rendering. "
                "Install with: pip install pretty-midi"
            ) from err

        midi = pretty_midi.PrettyMIDI(str(midi_path))
        audio = midi.synthesize(fs=self.config.default_sample_rate)

        # Save audio
        output_path = Path(output_path)
        if not output_path.suffix:
            output_path = output_path.with_suffix(f".{format}")

        if format == "wav":
            self._save_wav(audio, output_path)
        elif format == "mp3":
            self._save_mp3(audio, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

        return output_path

    def _save_wav(self, audio: bytearray, output_path: Path) -> None:
        """Save audio as WAV file.

        Args:
            audio: Audio data from pretty_midi.
            output_path: Output file path.
        """
        try:
            import numpy as np
            from scipy.io import wavfile
        except ImportError as err:
            raise RuntimeError(
                "numpy and scipy are required for WAV output. "
                "Install with: pip install numpy scipy"
            ) from err

        # Convert to int16
        audio_int16 = (audio * 32767).astype(np.int16)

        wavfile.write(
            str(output_path),
            self.config.default_sample_rate,
            audio_int16,
        )

    def _save_mp3(self, audio: bytearray, output_path: Path) -> None:
        """Save audio as MP3 file.

        Args:
            audio: Audio data from pretty_midi.
            output_path: Output file path.
        """
        try:
            from pydub import AudioSegment
        except ImportError as err:
            raise RuntimeError(
                "pydub library is required for MP3 output. "
                "Install with: pip install pydub"
            ) from err

        # First save as temporary WAV
        temp_wav = output_path.with_suffix(".temp.wav")
        self._save_wav(audio, temp_wav)

        # Convert to MP3
        sound = AudioSegment.from_wav(str(temp_wav))
        sound.export(str(output_path), format="mp3")

        # Clean up temp file
        temp_wav.unlink(missing_ok=True)

    def compose_and_render(
        self,
        prompt: str,
        output_path: Path | str,
        **kwargs,
    ) -> tuple[Composition, Path]:
        """Convenience method: compose and render in one call.

        Args:
            prompt: Natural language description.
            output_path: Where to save the rendered audio.
            **kwargs: Passed to compose() and render().
                Render-specific: format, stems, normalize, fade_out

        Returns:
            Tuple of (composition, rendered_audio_path).
        """
        # Extract render-specific kwargs
        render_format = kwargs.pop("format", "wav")
        stems = kwargs.pop("stems", False)
        normalize = kwargs.pop("normalize", True)
        fade_out = kwargs.pop("fade_out", 0.0)

        response = self.compose(prompt, **kwargs)
        audio_path = self.render(
            response.composition,
            output_path,
            format=render_format,
            stems=stems,
            normalize=normalize,
            fade_out=fade_out,
        )
        return response.composition, audio_path


def compose(
    prompt: str,
    api_key: str | None = None,
    **kwargs,
) -> CompositionResponse:
    """Convenience function to generate a composition.

    Args:
        prompt: Natural language description of desired music.
        api_key: Optional Gemini API key.
        **kwargs: Additional arguments passed to AIComposerV3.compose().

    Returns:
        CompositionResponse with generated composition.

    Example:
        >>> from musicgen.composer_v3 import compose
        >>> response = compose("A gentle piano piece in C major")
        >>> print(response.composition.title)
    """
    composer = AIComposerV3(gemini_api_key=api_key)
    return composer.compose(prompt, **kwargs)


def compose_and_save(
    prompt: str,
    output_path: Path | str,
    api_key: str | None = None,
    **kwargs,
) -> tuple[Composition, Path]:
    """Compose and render in one call.

    Args:
        prompt: Natural language description of desired music.
        output_path: Where to save the rendered audio.
        api_key: Optional Gemini API key.
        **kwargs: Additional arguments passed to compose().

    Returns:
        Tuple of (composition, rendered_audio_path).

    Example:
        >>> from musicgen.composer_v3 import compose_and_save
        >>> composition, audio_path = compose_and_save(
        ...     "A string quartet in G minor",
        ...     "output.wav"
        ... )
    """
    composer = AIComposerV3(gemini_api_key=api_key)
    return composer.compose_and_render(prompt, output_path, **kwargs)
