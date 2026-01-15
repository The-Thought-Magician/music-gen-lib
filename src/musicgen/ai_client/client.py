"""Gemini AI client for music composition."""

from __future__ import annotations

import json
import time
from typing import Any

try:
    from google import genai
    from google.api_core.exceptions import (
        GoogleAPIError,
        InvalidArgument,
        ResourceExhausted,
        ServiceUnavailable,
    )
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    GoogleAPIError = Exception
    genai = None

from musicgen.ai_client.exceptions import (
    APICallError,
    APIKeyError,
    InvalidResponseError,
    RateLimitError,
)
from musicgen.ai_client.prompts import PromptBuilder
from musicgen.config import Config, get_config


class GeminiClient:
    """Client for Google Gemini 2.5 Pro API.

    Features:
    - Configurable model, temperature, max_tokens
    - Retry logic with exponential backoff
    - Schema-aware prompting
    - JSON response parsing
    """

    # Default model
    DEFAULT_MODEL = "gemini-2.5-pro"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        config: Config | None = None,
    ):
        """Initialize the Gemini client.

        Args:
            api_key: Google API key. If None, reads from config.
            model: Model name. If None, reads from config.
            temperature: Sampling temperature (0.0-1.0). If None, reads from config.
            max_tokens: Max output tokens. If None, reads from config (usually unlimited).
            config: Optional config object.

        Raises:
            RuntimeError: If google-genai is not installed.
            APIKeyError: If no API key is available.
        """
        if not GENAI_AVAILABLE:
            raise RuntimeError(
                "google-genai package is required. Install with:\n"
                "  pip install google-genai"
            )

        self.config = config or get_config()

        # Get API key
        self.api_key = api_key or self.config.api_key
        if not self.api_key:
            raise APIKeyError(
                "Google API key required. Set GOOGLE_API_KEY environment variable "
                "or pass api_key parameter."
            )

        # Model settings
        self.model_name = model or self.config.model
        self.temperature = temperature if temperature is not None else self.config.temperature
        self.max_tokens = max_tokens if max_tokens is not None else self.config.max_tokens

        # Retry settings
        self.max_retries = self.config.retry_attempts
        self.retry_delay = self.config.retry_delay

        # Initialize client
        self.client = genai.Client(api_key=self.api_key)

    def generate(
        self,
        prompt: str,
        schema: str | None = None,
        system_instructions: str | None = None,
    ) -> dict[str, Any]:
        """Generate a composition from a prompt.

        Args:
            prompt: User's description of desired music.
            schema: Optional YAML schema to include in prompt.
            system_instructions: Optional custom system instructions.

        Returns:
            Parsed JSON response as dict.

        Raises:
            APICallError: If API call fails after retries.
            InvalidResponseError: If response cannot be parsed.
        """
        # Build prompts
        prompt_builder = PromptBuilder(system_instructions=system_instructions)
        system_prompt, user_prompt = prompt_builder.build_prompt(prompt, schema)

        # Call API with retry
        response_text = self._call_with_retry(system_prompt, user_prompt)

        # Parse response
        return self._parse_response(response_text)

    def _call_with_retry(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> str:
        """Call API with retry logic.

        Args:
            system_prompt: System instructions
            user_prompt: User prompt

        Returns:
            Response text

        Raises:
            APICallError: If all retries fail
        """
        last_error = None

        for attempt in range(self.max_retries):
            try:
                return self._make_call(system_prompt, user_prompt)

            except ResourceExhausted as e:
                last_error = e
                # Rate limited - wait with exponential backoff
                wait_time = self.retry_delay * (2 ** attempt)
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                else:
                    raise RateLimitError(
                        f"Rate limit exceeded after {self.max_retries} attempts",
                        cause=e
                    )

            except (ServiceUnavailable, InvalidArgument) as e:
                last_error = e
                # Temporary error or invalid request
                wait_time = self.retry_delay * (attempt + 1)
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                else:
                    raise APICallError(
                        f"API call failed: {e}",
                        cause=e
                    )

            except GoogleAPIError as e:
                last_error = e
                raise APICallError(f"API error: {e}", cause=e)

        raise APICallError(
            f"Failed after {self.max_retries} attempts",
            cause=last_error
        )

    def _make_call(self, system_prompt: str, user_prompt: str) -> str:
        """Make a single API call.

        Args:
            system_prompt: System instructions
            user_prompt: User prompt

        Returns:
            Response text
        """
        # Build generation config
        config_dict = {
            "temperature": self.temperature,
        }
        if self.max_tokens is not None:
            config_dict["max_output_tokens"] = self.max_tokens

        generation_config = types.GenerateContentConfig(**config_dict)

        # Make the call
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=user_prompt,
            config=generation_config,
        )

        return response.text

    def _parse_response(self, response: str) -> dict[str, Any]:
        """Parse JSON response from AI.

        Args:
            response: Raw response text

        Returns:
            Parsed JSON dict

        Raises:
            InvalidResponseError: If response cannot be parsed
        """
        # Clean response
        cleaned = self._clean_json_response(response)

        # Parse JSON
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise InvalidResponseError(
                f"Failed to parse JSON response: {e}\n\nResponse was:\n{response[:500]}...",
                cause=e
            )

    def _clean_json_response(self, response: str) -> str:
        """Clean response text to extract JSON.

        Handles:
        - Markdown code blocks (```json, ```)
        - Leading/trailing text
        - Comments (though we tell AI not to include them)

        Args:
            response: Raw response

        Returns:
            Cleaned JSON string
        """
        response = response.strip()

        # Remove markdown code blocks
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        # Extract JSON object if there's surrounding text
        # Find first { and last }
        start = response.find("{")
        end = response.rfind("}")

        if start != -1 and end != -1 and end > start:
            response = response[start:end + 1]

        return response


# Convenience function
def generate_composition(
    prompt: str,
    api_key: str | None = None,
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> dict[str, Any]:
    """Generate a composition from a prompt.

    Args:
        prompt: User's description of desired music
        api_key: Optional API key
        model: Optional model name
        temperature: Optional sampling temperature
        max_tokens: Optional max output tokens

    Returns:
        Parsed JSON response

    Raises:
        AIClientError: If generation fails
    """
    client = GeminiClient(
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return client.generate(prompt)


def check_availability() -> dict[str, bool]:
    """Check if Gemini API is available.

    Returns:
        Dict with availability info:
        - package_installed: bool
        - api_key_set: bool
        - available: bool
    """
    config = get_config()
    return {
        "package_installed": GENAI_AVAILABLE,
        "api_key_set": bool(config.api_key),
        "available": GENAI_AVAILABLE and bool(config.api_key),
    }
