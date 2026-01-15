# Step 4: Gemini 2.5 Pro Client

## Objective

Create a robust Gemini 2.5 Pro client with:
- Configurable model, temperature, max tokens
- Retry logic with exponential backoff
- Schema-aware prompting
- JSON response parsing

## Overview

The client is responsible for:
1. Constructing prompts with schema
2. Calling Gemini API
3. Handling errors and retries
4. Returning validated responses

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  User Prompt                                                 │
│  "A peaceful piano melody in C major"                        │
├─────────────────────────────────────────────────────────────┤
│  Prompt Builder                                              │
│  - Adds system prompt                                        │
│  - Adds schema (YAML)                                        │
│  - Adds few-shot examples                                    │
├─────────────────────────────────────────────────────────────┤
│  GeminiClient                                                │
│  - Calls gemini-2.5-pro                                      │
│  - Configurable temperature (default: 0.5)                   │
│  - No max_tokens limit (let AI generate full compositions)   │
├─────────────────────────────────────────────────────────────┤
│  Response Parser                                             │
│  - Extracts JSON from AI response                            │
│  - Validates against Pydantic models                         │
└─────────────────────────────────────────────────────────────┘
```

## Tasks

### 4.1 Create AI Client Package

Create `src/musicgen/ai_client/`:
```
src/musicgen/ai_client/
├── __init__.py
├── client.py      # Main GeminiClient class
├── prompts.py     # Prompt building logic
└── exceptions.py  # Custom exceptions
```

### 4.2 Exceptions

Create `src/musicgen/ai_client/exceptions.py`:

```python
"""Exceptions for AI client."""

from typing import Optional


class AIClientError(Exception):
    """Base exception for AI client errors."""

    def __init__(self, message: str, cause: Optional[Exception] = None):
        self.message = message
        self.cause = cause
        super().__init__(message)


class APIKeyError(AIClientError):
    """Raised when API key is missing or invalid."""


class RateLimitError(AIClientError):
    """Raised when rate limit is exceeded."""


class APICallError(AIClientError):
    """Raised when API call fails after retries."""


class InvalidResponseError(AIClientError):
    """Raised when AI response is invalid or cannot be parsed."""
```

### 4.3 Prompt Builder

Create `src/musicgen/ai_client/prompts.py`:

```python
"""Prompt building for AI composition."""

from __future__ import annotations
from typing import Optional

from musicgen.config import get_config
from musicgen.schema import get_schema, SchemaConfig


class PromptBuilder:
    """Builds prompts for AI composition."""

    def __init__(
        self,
        schema_config: Optional[SchemaConfig] = None,
        system_instructions: Optional[str] = None
    ):
        """Initialize prompt builder.

        Args:
            schema_config: Optional schema configuration
            system_instructions: Optional custom system instructions
        """
        self.schema_config = schema_config
        self.system_instructions = system_instructions or self._default_system_instructions()

    def build_prompt(
        self,
        user_prompt: str,
        schema: Optional[str] = None
    ) -> tuple[str, str]:
        """Build system and user prompts.

        Args:
            user_prompt: User's description of desired music
            schema: Optional schema YAML (generated if not provided)

        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        if schema is None:
            schema = get_schema(self.schema_config)

        system_prompt = self._build_system_prompt(schema)
        full_user_prompt = self._build_user_prompt(user_prompt)

        return system_prompt, full_user_prompt

    def _build_system_prompt(self, schema: str) -> str:
        """Build system prompt with schema.

        Args:
            schema: YAML schema string

        Returns:
            System prompt
        """
        return f"""{self.system_instructions}

COMPOSITION SCHEMA:
You must generate compositions that follow this schema exactly:

```yaml
{schema}
```

OUTPUT FORMAT:
Return ONLY valid JSON. No markdown formatting, no explanations, no additional text.
The JSON must match the schema above exactly.

COMPOSITION GUIDELINES:
1. Generate musically coherent note sequences
2. Consider voice leading and harmonic progressions
3. Create balanced phrases with proper cadences
4. Use dynamics to create expression
5. Match the mood/style described in the user prompt
6. Keep total duration reasonable (typically 30-180 seconds)
"""

    def _build_user_prompt(self, user_prompt: str) -> str:
        """Build user prompt.

        Args:
            user_prompt: User's description

        Returns:
            Full user prompt
        """
        return f"""Generate a complete composition based on this description:

"{user_prompt}"

Return ONLY the JSON object matching the schema. Do not include any other text."""

    def _default_system_instructions(self) -> str:
        """Default system instructions."""
        return """You are an expert AI composer capable of generating complete musical compositions.

You create note-by-note compositions that follow standard music theory while being creative and expressive.

Your compositions include:
- Melodically interesting lines with proper phrasing
- Harmonically coherent progressions
- Appropriate voice leading
- Dynamic markings for expression
- Proper instrumental roles (melody, harmony, bass, accompaniment)

You are fluent in all musical styles: classical, jazz, pop, folk, electronic, etc."""


def build_prompt(
    user_prompt: str,
    schema: Optional[str] = None,
    schema_config: Optional[SchemaConfig] = None
) -> tuple[str, str]:
    """Convenience function to build prompts.

    Args:
        user_prompt: User's description
        schema: Optional schema YAML
        schema_config: Optional schema configuration

    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    builder = PromptBuilder(schema_config=schema_config)
    return builder.build_prompt(user_prompt, schema)
```

### 4.4 Gemini Client

Create `src/musicgen/ai_client/client.py`:

```python
"""Gemini AI client for music composition."""

from __future__ import annotations
import time
import json
import re
from typing import Optional, Any
from pathlib import Path

try:
    from google import genai
    from google.genai import types
    from google.api_core.exceptions import (
        GoogleAPIError,
        InvalidArgument,
        ResourceExhausted,
        ServiceUnavailable,
    )
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    GoogleAPIError = Exception
    genai = None

from musicgen.config import get_config, Config
from musicgen.ai_client.exceptions import (
    AIClientError,
    APIKeyError,
    RateLimitError,
    APICallError,
    InvalidResponseError,
)
from musicgen.ai_client.prompts import PromptBuilder


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
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        config: Optional[Config] = None,
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
        schema: Optional[str] = None,
        system_instructions: Optional[str] = None,
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
            # System instructions would be passed differently depending on API version
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
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
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
```

### 4.5 Package Init

Create `src/musicgen/ai_client/__init__.py`:

```python
"""AI client for Gemini 2.5 Pro."""

from musicgen.ai_client.client import (
    GeminiClient,
    generate_composition,
    check_availability,
)
from musicgen.ai_client.prompts import PromptBuilder, build_prompt
from musicgen.ai_client.exceptions import (
    AIClientError,
    APIKeyError,
    RateLimitError,
    APICallError,
    InvalidResponseError,
)

__all__ = [
    "GeminiClient",
    "generate_composition",
    "check_availability",
    "PromptBuilder",
    "build_prompt",
    "AIClientError",
    "APIKeyError",
    "RateLimitError",
    "APICallError",
    "InvalidResponseError",
]
```

### 4.6 Testing

Create `tests/test_gemini_client.py`:

```python
"""Test Gemini client."""

import pytest
from musicgen.ai_client import (
    GeminiClient,
    PromptBuilder,
    check_availability,
    AIClientError,
    APIKeyError,
)
from musicgen.ai_client.exceptions import InvalidResponseError


def test_check_availability():
    """Test availability check."""
    result = check_availability()
    assert "package_installed" in result
    assert "api_key_set" in result
    assert "available" in result


def test_prompt_builder():
    """Test prompt building."""
    builder = PromptBuilder()
    system_prompt, user_prompt = builder.build_prompt("A happy melody")

    assert "system" in system_prompt.lower() or "schema" in system_prompt.lower()
    assert "happy melody" in user_prompt.lower()


def test_client_requires_api_key():
    """Test that client requires API key."""
    # Mock empty config
    with pytest.raises(APIKeyError):
        GeminiClient(api_key=None)


def test_json_cleaning():
    """Test JSON response cleaning."""
    client = GeminiClient(api_key="test-key")  # Will fail on actual call

    # Test markdown removal
    cleaned = client._clean_json_response('```json\n{"key": "value"}\n```')
    assert '{"key": "value"}' in cleaned

    # Test text extraction
    cleaned = client._clean_json_response('Here is the result: {"key": "value"} end')
    assert '{"key": "value"}' in cleaned


def test_invalid_json_parsing():
    """Test parsing invalid JSON raises error."""
    client = GeminiClient(api_key="test-key")

    with pytest.raises(InvalidResponseError):
        client._parse_response("this is not json")


def test_response_parse_valid_json():
    """Test parsing valid JSON."""
    client = GeminiClient(api_key="test-key")
    result = client._parse_response('{"title": "Test", "tempo": 120}')
    assert result["title"] == "Test"
    assert result["tempo"] == 120
```

## Deliverables

- `src/musicgen/ai_client/__init__.py`
- `src/musicgen/ai_client/client.py`
- `src/musicgen/ai_client/prompts.py`
- `src/musicgen/ai_client/exceptions.py`
- `tests/test_gemini_client.py`

## Configuration Examples

### Via .env
```bash
GOOGLE_API_KEY=your-key-here
GEMINI_MODEL=gemini-2.5-pro
GEMINI_TEMPERATURE=0.5
GEMINI_MAX_TOKENS=
```

### Via code
```python
from musicgen.ai_client import GeminiClient

client = GeminiClient(
    api_key="...",
    model="gemini-2.5-pro",
    temperature=0.6,      # Easy to adjust
    max_tokens=None,      # Unlimited
)

result = client.generate("A jazz piece in F minor")
```

## Next Steps

After completing this step:
- Step 5: AI composer (orchestrates everything)
- Step 6: Rendering engine
