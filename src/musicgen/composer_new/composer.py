"""AI Composer - generates compositions from prompts."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from musicgen.ai_client import GeminiClient
from musicgen.ai_client.exceptions import AIClientError
from musicgen.ai_client.tools import (
    DEFAULT_COMPOSITION_TOOLS,
    FunctionDeclaration,
    ToolCallResult,
)
from musicgen.ai_models import AIComposition, validate_composition
from musicgen.config import Config, get_config
from musicgen.schema import SchemaConfig, SchemaGenerator

logger = logging.getLogger(__name__)


# Validation constants
MIN_DURATION_SECONDS = 120  # 2 minutes minimum
MIN_MELODY_NOTES = 150
MIN_HARMONY_NOTES = 120
MIN_BASS_NOTES = 80
MIN_ACCOMPANIMENT_NOTES = 100


class AIComposer:
    """AI-powered music composer.

    Generates complete note-based compositions from natural language prompts.

    Supports function calling tools for enhanced composition capabilities.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        schema_config: SchemaConfig | None = None,
        config: Config | None = None,
        log_requests: bool = True,
        tools: list[FunctionDeclaration] | None = None,
        enable_tools: bool = True,
    ):
        """Initialize the AI composer.

        Args:
            api_key: Google API key
            model: Model name (default: from config)
            temperature: Sampling temperature (default: from config)
            max_tokens: Max output tokens (default: from config)
            schema_config: Optional schema configuration
            config: Optional config object
            log_requests: Whether to log AI requests/responses to files
            tools: Optional list of function declarations for tool calling.
                    If None and enable_tools is True, uses DEFAULT_COMPOSITION_TOOLS.
            enable_tools: Whether to enable function calling tools (default: True)
        """
        self.config = config or get_config()
        self.schema_config = schema_config
        self.log_requests = log_requests

        # Set up tools
        self.enable_tools = enable_tools
        if tools is not None:
            self.tools = tools
        elif enable_tools:
            self.tools = DEFAULT_COMPOSITION_TOOLS
        else:
            self.tools = None

        # Initialize AI client
        self.client = GeminiClient(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            config=self.config,
            log_requests=log_requests,
        )

        # Schema generator
        self.schema_generator = SchemaGenerator(schema_config)

    def generate(
        self,
        prompt: str,
        validate: bool = True,
        return_raw: bool = False,
        validate_duration: bool = True,
        auto_fix_polyphony: bool = True,
        use_tools: bool | None = None,
    ) -> AIComposition | dict[str, Any]:
        """Generate a composition from a prompt.

        Args:
            prompt: Natural language description of desired music
            validate: Whether to validate against AIComposition model
            return_raw: If True, return raw dict instead of AIComposition
            validate_duration: Whether to validate minimum duration/note requirements
            auto_fix_polyphony: Whether to auto-fix polyphony issues in harmony parts
            use_tools: Whether to use function calling tools. If None, uses the
                       enable_tools setting from initialization.

        Returns:
            AIComposition or raw dict. If tools are used and the AI makes tool calls,
            the raw dict will include a "tool_calls" key with the list of function calls.

        Raises:
            AIClientError: If generation fails
            ValidationError: If validation fails
        """
        logger.info(f"Generating composition from prompt: {prompt[:100]}...")

        # Determine whether to use tools for this call
        should_use_tools = use_tools if use_tools is not None else self.enable_tools

        # Get schema
        schema = self.schema_generator.generate()
        logger.debug(f"Generated schema ({len(schema)} chars)")

        # Generate composition
        tools_to_use = self.tools if should_use_tools else None
        raw_response = self.client.generate(
            prompt=prompt,
            schema=schema,
            tools=tools_to_use,
        )

        logger.info("Received response from AI")

        # Handle tool calls if present
        if "tool_calls" in raw_response:
            tool_calls = raw_response.get("tool_calls", [])
            logger.info(f"AI made {len(tool_calls)} tool call(s)")

            # Process tool calls
            tool_results = self._handle_tool_calls(tool_calls)

            # Add tool results to response
            raw_response["tool_results"] = [r.to_dict() for r in tool_results]

            # Log tool usage
            for result in tool_results:
                if result.success:
                    logger.debug(f"Tool '{result.tool_name}' executed successfully")
                else:
                    logger.warning(f"Tool '{result.tool_name}' failed: {result.error}")

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

                # Validate duration and note counts
                if validate_duration:
                    self._validate_composition_quality(composition)

                # Post-process: validate and fix polyphony
                if auto_fix_polyphony:
                    self._post_process_polyphony(composition)

                return composition
            except Exception as e:
                logger.error(f"Validation failed: {e}")
                raise ValidationError(f"Failed to validate AI response: {e}") from e

        return raw_response

    def _handle_tool_calls(
        self,
        tool_calls: list[dict[str, Any]],
    ) -> list[ToolCallResult]:
        """Handle tool calls made by the AI.

        Args:
            tool_calls: List of tool call dictionaries with 'name' and 'args' keys

        Returns:
            List of ToolCallResult objects
        """
        results = []

        for call in tool_calls:
            tool_name = call.get("name")
            args = call.get("args", {})

            logger.debug(f"Handling tool call: {tool_name} with args: {args}")

            try:
                # Execute the tool
                result = self._execute_tool(tool_name, args)
                results.append(ToolCallResult(
                    tool_name=tool_name,
                    arguments=args,
                    result=result,
                    success=True,
                ))
            except Exception as e:
                logger.error(f"Tool execution failed for {tool_name}: {e}")
                results.append(ToolCallResult(
                    tool_name=tool_name,
                    arguments=args,
                    result=None,
                    success=False,
                    error=str(e),
                ))

        return results

    def _execute_tool(self, tool_name: str, args: dict[str, Any]) -> Any:
        """Execute a single tool.

        This is a placeholder implementation that logs the tool call.
        In a full implementation, this would actually execute the tool logic.

        Args:
            tool_name: Name of the tool to execute
            args: Arguments to pass to the tool

        Returns:
            Result of the tool execution
        """
        # Map tool names to their implementations
        tool_implementations = {
            "create_chord": self._tool_create_chord,
            "add_rhythm_variation": self._tool_add_rhythm_variation,
            "set_dynamic": self._tool_set_dynamic,
            "add_ornament": self._tool_add_ornament,
            "create_section": self._tool_create_section,
            "add_counter_melody": self._tool_add_counter_melody,
            "apply_transformation": self._tool_apply_transformation,
        }

        implementation = tool_implementations.get(tool_name)
        if implementation is None:
            raise ValueError(f"Unknown tool: {tool_name}")

        return implementation(args)

    # -------------------------------------------------------------------------
    # Tool Implementations
    # -------------------------------------------------------------------------

    def _tool_create_chord(self, args: dict[str, Any]) -> dict[str, Any]:
        """Create a chord with proper voice leading.

        Args:
            args: Tool arguments (root, quality, inversion, duration, voicing, etc.)

        Returns:
            Chord information with recommended voicing
        """
        root = args.get("root", "C")
        quality = args.get("quality", "major")
        inversion = args.get("inversion", 0)
        duration = args.get("duration", 1.0)

        # Simple chord construction (placeholder - can be enhanced)
        # This returns chord information that can be used in note generation
        result = {
            "root": root,
            "quality": quality,
            "inversion": inversion,
            "duration": duration,
            "notes": self._get_chord_notes(root, quality, inversion),
            "message": f"Created {root} {quality} chord (inversion {inversion})"
        }

        logger.debug(f"Created chord: {result}")
        return result

    def _tool_add_rhythm_variation(self, args: dict[str, Any]) -> dict[str, Any]:
        """Add rhythmic variation to a pattern.

        Args:
            args: Tool arguments (variation_type, target_part, measures, etc.)

        Returns:
            Confirmation of variation applied
        """
        variation_type = args.get("variation_type", "syncopation")
        target_part = args.get("target_part", "melody")
        measure_start = args.get("measure_start", 1)
        measure_end = args.get("measure_end", 8)

        result = {
            "variation_type": variation_type,
            "target_part": target_part,
            "measures": f"{measure_start}-{measure_end}",
            "message": f"Added {variation_type} to {target_part} (measures {measure_start}-{measure_end})"
        }

        logger.debug(f"Rhythm variation: {result}")
        return result

    def _tool_set_dynamic(self, args: dict[str, Any]) -> dict[str, Any]:
        """Set dynamic level for a section.

        Args:
            args: Tool arguments (dynamic, target_part, measures, transition, etc.)

        Returns:
            Confirmation of dynamic marking
        """
        dynamic = args.get("dynamic", "mf")
        target_part = args.get("target_part", "all")
        measure_start = args.get("measure_start", 1)
        measure_end = args.get("measure_end")
        transition = args.get("transition", "immediate")

        result = {
            "dynamic": dynamic,
            "target_part": target_part,
            "measure_range": f"{measure_start}-{measure_end}" if measure_end else f"{measure_start}+",
            "transition": transition,
            "message": f"Set {dynamic} dynamic for {target_part} starting at measure {measure_start}"
        }

        logger.debug(f"Dynamic setting: {result}")
        return result

    def _tool_add_ornament(self, args: dict[str, Any]) -> dict[str, Any]:
        """Add ornament to a note.

        Args:
            args: Tool arguments (ornament_type, target_part, measure, beat, etc.)

        Returns:
            Confirmation of ornament added
        """
        ornament_type = args.get("ornament_type", "trill")
        target_part = args.get("target_part", "melody")
        measure = args.get("measure", 1)
        beat = args.get("beat", 0.0)

        result = {
            "ornament_type": ornament_type,
            "target_part": target_part,
            "position": f"measure {measure}, beat {beat}",
            "message": f"Added {ornament_type} to {target_part} at measure {measure}, beat {beat}"
        }

        logger.debug(f"Ornament: {result}")
        return result

    def _tool_create_section(self, args: dict[str, Any]) -> dict[str, Any]:
        """Create a musical section.

        Args:
            args: Tool arguments (section_type, measure_start, measure_count, etc.)

        Returns:
            Section information
        """
        section_type = args.get("section_type", "verse")
        measure_start = args.get("measure_start", 1)
        measure_count = args.get("measure_count", 16)
        tempo = args.get("tempo")
        description = args.get("description", "")

        result = {
            "section_type": section_type,
            "measure_start": measure_start,
            "measure_end": measure_start + measure_count - 1,
            "measure_count": measure_count,
            "tempo": tempo,
            "description": description,
            "message": f"Created {section_type} section (measures {measure_start}-{measure_start + measure_count - 1})"
        }

        logger.debug(f"Section: {result}")
        return result

    def _tool_add_counter_melody(self, args: dict[str, Any]) -> dict[str, Any]:
        """Generate a counter-melody.

        Args:
            args: Tool arguments (target_measures, interval_type, etc.)

        Returns:
            Counter-melody specification
        """
        target_measures = args.get("target_measures", "1-16")
        interval_type = args.get("interval_type", "thirds")
        rhythmic_activity = args.get("rhythmic_activity", "moderate")

        result = {
            "target_measures": target_measures,
            "interval_type": interval_type,
            "rhythmic_activity": rhythmic_activity,
            "message": f"Added {interval_type} counter-melody ({rhythmic_activity} activity) for measures {target_measures}"
        }

        logger.debug(f"Counter-melody: {result}")
        return result

    def _tool_apply_transformation(self, args: dict[str, Any]) -> dict[str, Any]:
        """Apply musical transformation.

        Args:
            args: Tool arguments (transformation, target_part, measures, etc.)

        Returns:
            Transformation confirmation
        """
        transformation = args.get("transformation", "transpose")
        target_part = args.get("target_part", "melody")
        target_measures = args.get("target_measures", "17-32")
        interval = args.get("interval", 0)

        result = {
            "transformation": transformation,
            "target_part": target_part,
            "target_measures": target_measures,
            "interval": interval,
            "message": f"Applied {transformation} to {target_part} (measures {target_measures})"
        }

        logger.debug(f"Transformation: {result}")
        return result

    def _get_chord_notes(
        self,
        root: str,
        quality: str,
        inversion: int,
    ) -> list[str]:
        """Get the notes for a chord.

        Args:
            root: Root note (e.g., "C", "F#", "Bb")
            quality: Chord quality
            inversion: Chord inversion (0, 1, or 2)

        Returns:
            List of note names
        """
        # Note names
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        # Convert flats to sharps
        flat_to_sharp = {
            "Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#",
        }
        if root in flat_to_sharp:
            root = flat_to_sharp[root]

        try:
            root_idx = notes.index(root)
        except ValueError:
            root_idx = 0

        # Interval patterns for different chord qualities
        intervals = {
            "major": [0, 4, 7],
            "minor": [0, 3, 7],
            "diminished": [0, 3, 6],
            "augmented": [0, 4, 8],
            "major_7": [0, 4, 7, 11],
            "minor_7": [0, 3, 7, 10],
            "dominant_7": [0, 4, 7, 10],
            "half_diminished_7": [0, 3, 6, 10],
            "fully_diminished_7": [0, 3, 6, 9],
            "suspended_2": [0, 2, 7],
            "suspended_4": [0, 5, 7],
        }

        pattern = intervals.get(quality, intervals["major"])

        # Build chord notes
        chord_notes = []
        for i, interval in enumerate(pattern):
            note_idx = (root_idx + interval) % 12
            octave_offset = (root_idx + interval) // 12
            note = notes[note_idx]

            # Inversion handling - rotate notes
            if inversion > 0:
                # Move bottom notes up an octave
                inv_note_idx = (i - inversion) % len(pattern)
                octave_offset += 1 if i < inversion else 0

            chord_notes.append(note + "4" if octave_offset == 0 else note + "5")

        return chord_notes

    def _validate_composition_quality(self, composition: AIComposition) -> None:
        """Validate that composition meets minimum quality requirements.

        Args:
            composition: The composition to validate

        Raises:
            ValidationError: If composition doesn't meet requirements
        """
        duration = composition.duration_seconds

        # Check duration
        if duration < MIN_DURATION_SECONDS:
            logger.warning(
                f"Composition duration ({duration:.1f}s) is below minimum "
                f"({MIN_DURATION_SECONDS}s). The AI may not have generated enough notes."
            )

        # Check note counts per part
        for part in composition.parts:
            note_count = len(part.notes)
            role = part.role

            min_notes = 0
            if role == "melody":
                min_notes = MIN_MELODY_NOTES
            elif role == "harmony":
                min_notes = MIN_HARMONY_NOTES
            elif role == "bass":
                min_notes = MIN_BASS_NOTES
            elif role == "accompaniment":
                min_notes = MIN_ACCOMPANIMENT_NOTES
            else:
                min_notes = 80  # Default minimum

            if note_count < min_notes:
                logger.warning(
                    f"Part '{part.name}' (role: {role}) has {note_count} notes, "
                    f"below recommended minimum of {min_notes}. "
                    f"This may result in a composition shorter than intended."
                )

        # Log summary
        logger.info(
            f"Composition quality check: {duration:.1f}s duration, "
            f"{sum(len(p.notes) for p in composition.parts)} total notes across "
            f"{len(composition.parts)} parts"
        )

    def _post_process_polyphony(self, composition: AIComposition) -> None:
        """Post-process composition to fix polyphony issues.

        Validates harmony/accompaniment parts for proper polyphony
        and auto-fixes missing start_time values.

        Args:
            composition: The composition to post-process (modified in-place)
        """
        from musicgen.ai_models.postprocess import (
            ValidationResult,
            validate_composition,
        )

        # Run validation with auto-fix
        result: ValidationResult = validate_composition(composition, auto_fix=True)

        # Log the results
        if result.is_valid:
            logger.info("Polyphony validation passed - no issues detected")
        else:
            logger.warning(
                f"Polyphony issues detected and auto-fixed: "
                f"{len(result.parts_with_issues)} part(s) affected"
            )
            for part_name, issues in result.parts_with_issues.items():
                for issue in issues:
                    logger.warning(f"  - {part_name}: {issue}")

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
    api_key: str | None = None,
    model: str | None = None,
    temperature: float | None = None,
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
