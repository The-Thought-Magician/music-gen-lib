"""Gemini AI client for music composition."""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from pathlib import Path
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
from musicgen.ai_client.tools import FunctionDeclaration, format_tools_for_gemini
from musicgen.config import Config, get_config

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for Google Gemini 2.5 Pro API.

    Features:
    - Configurable model, temperature, max_tokens
    - Retry logic with exponential backoff
    - Schema-aware prompting
    - JSON response parsing
    - Request/response logging
    - Function calling support
    """

    # Default model
    DEFAULT_MODEL = "gemini-2.5-pro"

    # Logging directory
    LOG_DIR = Path("logs/ai_calls")

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        config: Config | None = None,
        log_requests: bool = True,
    ):
        """Initialize the Gemini client.

        Args:
            api_key: Google API key. If None, reads from config.
            model: Model name. If None, reads from config.
            temperature: Sampling temperature (0.0-1.0). If None, reads from config.
            max_tokens: Max output tokens. If None, reads from config (usually unlimited).
            config: Optional config object.
            log_requests: Whether to log requests/responses to files.

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
        self.log_requests = log_requests

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

        # Create log directory
        if self.log_requests:
            self.LOG_DIR.mkdir(parents=True, exist_ok=True)

    def generate(
        self,
        prompt: str,
        schema: str | None = None,
        system_instructions: str | None = None,
        tools: list[FunctionDeclaration] | None = None,
    ) -> dict[str, Any]:
        """Generate a composition from a prompt.

        Args:
            prompt: User's description of desired music.
            schema: Optional YAML schema to include in prompt.
            system_instructions: Optional custom system instructions.
            tools: Optional list of function declarations for tool calling.

        Returns:
            Parsed JSON response as dict. If tools are provided and the AI
            makes tool calls, the response will include a "tool_calls" key
            with the list of function calls.

        Raises:
            APICallError: If API call fails after retries.
            InvalidResponseError: If response cannot be parsed.
        """
        # Build prompts
        prompt_builder = PromptBuilder(
            system_instructions=system_instructions,
            tools=tools
        )
        system_prompt, user_prompt = prompt_builder.build_prompt(prompt, schema)

        # Log the request
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if self.log_requests:
            self._log_request(timestamp, prompt, system_prompt, user_prompt, schema, tools)

        # Call API with retry
        response_text = self._call_with_retry(
            system_prompt,
            user_prompt,
            tools=format_tools_for_gemini(tools) if tools else None,
        )

        # Log the response
        if self.log_requests:
            self._log_response(timestamp, response_text)

        # Parse response
        return self._parse_response(response_text)

    def _call_with_retry(
        self,
        system_prompt: str,
        user_prompt: str,
        tools: dict[str, Any] | None = None,
    ) -> str:
        """Call API with retry logic.

        Args:
            system_prompt: System instructions
            user_prompt: User prompt
            tools: Optional formatted tools for function calling

        Returns:
            Response text

        Raises:
            APICallError: If all retries fail
        """
        last_error = None

        for attempt in range(self.max_retries):
            try:
                return self._make_call(system_prompt, user_prompt, tools)

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

    def _make_call(
        self,
        system_prompt: str,
        user_prompt: str,
        tools: dict[str, Any] | None = None,
    ) -> str:
        """Make a single API call.

        Args:
            system_prompt: System instructions
            user_prompt: User prompt
            tools: Optional formatted tools for function calling

        Returns:
            Response text (including tool calls if present)
        """
        # Build generation config
        config_dict = {
            "temperature": self.temperature,
            "system_instruction": system_prompt,
        }
        if self.max_tokens is not None:
            config_dict["max_output_tokens"] = self.max_tokens

        # Add tools if provided - tools go in the config for the Google GenAI SDK
        if tools:
            config_dict["tools"] = [types.Tool(**tools)]

        generation_config = types.GenerateContentConfig(**config_dict)

        # Build kwargs for API call
        kwargs = {
            "model": self.model_name,
            "contents": user_prompt,
            "config": generation_config,
        }

        # Make the call - use client.models.generate_content() for tool support
        response = self.client.models.generate_content(**kwargs)

        # Check for tool calls in response
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                # Extract text and any tool calls
                parts = candidate.content.parts
                result_text = ""
                tool_calls = []

                for part in parts:
                    if hasattr(part, 'text') and part.text:
                        result_text += part.text
                    if hasattr(part, 'function_call') and part.function_call:
                        # Convert function call to dict format
                        fc = part.function_call
                        tool_calls.append({
                            "name": fc.name,
                            "args": dict(fc.args) if hasattr(fc, 'args') else {},
                        })

                # If we have tool calls, wrap the response
                if tool_calls:
                    result_dict = json.loads(result_text) if result_text.strip() else {}
                    result_dict["tool_calls"] = tool_calls
                    return json.dumps(result_dict)

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
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise InvalidResponseError(
                f"Failed to parse JSON response: {e}\n\nResponse was:\n{response[:500]}...",
                cause=e
            )

        # Handle nested composition structure - if response has a 'composition' key,
        # unwrap it to match the AIComposition model structure
        if isinstance(parsed, dict) and "composition" in parsed:
            composition_data = parsed.get("composition", {})
            # Merge top-level metadata with composition data
            if isinstance(composition_data, dict):
                result = {**composition_data}
                # Preserve certain top-level metadata if not in composition
                for key in ["version", "description", "note_format", "duration_unit", "pitch_representation"]:
                    if key in parsed:
                        result[key] = parsed[key]
                return result

        return parsed

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


    def _log_request(
        self,
        timestamp: str,
        prompt: str,
        system_prompt: str,
        user_prompt: str,
        schema: str | None = None,
        tools: list[FunctionDeclaration] | None = None,
    ) -> None:
        """Log the request details.

        Args:
            timestamp: Timestamp for the log file
            prompt: Original user prompt
            system_prompt: System instructions sent to AI
            user_prompt: User prompt sent to AI
            schema: Schema YAML (if provided)
            tools: Function declarations (if provided)
        """
        log_dir = self.LOG_DIR / timestamp
        log_dir.mkdir(parents=True, exist_ok=True)

        # Save original prompt
        (log_dir / "prompt.txt").write_text(prompt, encoding="utf-8")

        # Save system prompt
        (log_dir / "system_prompt.txt").write_text(system_prompt, encoding="utf-8")

        # Save user prompt
        (log_dir / "user_prompt.txt").write_text(user_prompt, encoding="utf-8")

        # Save schema if provided
        if schema:
            (log_dir / "schema.yaml").write_text(schema, encoding="utf-8")

        # Save tools if provided
        if tools:
            tools_data = [tool.to_dict() for tool in tools]
            (log_dir / "tools.json").write_text(
                json.dumps(tools_data, indent=2), encoding="utf-8"
            )

        # Save request metadata
        metadata = {
            "model": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timestamp": timestamp,
            "has_tools": tools is not None,
            "tool_count": len(tools) if tools else 0,
        }
        (log_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2), encoding="utf-8"
        )

        logger.info(f"Request logged to: {log_dir}")

    def _log_response(self, timestamp: str, response_text: str) -> None:
        """Log the AI response.

        Args:
            timestamp: Timestamp for the log file (should match request)
            response_text: Raw response text from AI
        """
        log_dir = self.LOG_DIR / timestamp

        # Save raw response
        (log_dir / "response_raw.txt").write_text(response_text, encoding="utf-8")

        # Try to save parsed response
        try:
            cleaned = self._clean_json_response(response_text)
            parsed = json.loads(cleaned)
            (log_dir / "response_parsed.json").write_text(
                json.dumps(parsed, indent=2), encoding="utf-8"
            )
        except Exception as e:
            (log_dir / "parse_error.txt").write_text(str(e), encoding="utf-8")

        logger.info(f"Response logged to: {log_dir}")


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
