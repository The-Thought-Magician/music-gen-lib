"""Exceptions for AI client."""



class AIClientError(Exception):
    """Base exception for AI client errors."""

    def __init__(self, message: str, cause: Exception | None = None):
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
