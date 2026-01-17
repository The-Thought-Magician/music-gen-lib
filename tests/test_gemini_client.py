"""Test Gemini client."""

import pytest

from musicgen.ai_client import (
    APIKeyError,
    GeminiClient,
    PromptBuilder,
    check_availability,
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
