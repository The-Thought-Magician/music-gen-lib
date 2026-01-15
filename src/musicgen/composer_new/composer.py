"""AI Composer - generates compositions from prompts."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from musicgen.ai_client import GeminiClient
from musicgen.ai_client.exceptions import AIClientError
from musicgen.ai_models import AIComposition
from musicgen.config import Config, get_config
from musicgen.schema import SchemaConfig, SchemaGenerator

logger = logging.getLogger(__name__)


class AIComposer:
    """AI-powered music composer.

    Generates complete note-based compositions from natural language prompts.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        schema_config: SchemaConfig | None = None,
        config: Config | None = None,
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

        logger.info("Received response from AI")

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
