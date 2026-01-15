"""AI client for Gemini 2.5 Pro."""

from musicgen.ai_client.client import (
    GeminiClient,
    check_availability,
    generate_composition,
)
from musicgen.ai_client.exceptions import (
    AIClientError,
    APICallError,
    APIKeyError,
    InvalidResponseError,
    RateLimitError,
)
from musicgen.ai_client.prompts import PromptBuilder, build_prompt

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
