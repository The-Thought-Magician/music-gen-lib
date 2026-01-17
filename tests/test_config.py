"""Test configuration system."""

import os
import tempfile
from pathlib import Path

from musicgen.config import Config, get_config


def test_default_config():
    """Test default configuration values."""
    config = Config()
    assert config.model == "gemini-2.5-pro"
    assert config.temperature == 0.5
    assert config.max_tokens is None


def test_env_override():
    """Test environment variable overrides."""
    os.environ["GEMINI_MODEL"] = "gemini-2.5-pro"
    os.environ["GEMINI_TEMPERATURE"] = "0.7"

    try:
        config = Config()
        assert config.temperature == 0.7
    finally:
        # Cleanup
        del os.environ["GEMINI_MODEL"]
        del os.environ["GEMINI_TEMPERATURE"]


def test_yaml_loading():
    """Test YAML configuration loading."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("model:\n  default_temperature: 0.6\n")
        f.flush()

        config = Config(config_path=Path(f.name))
        assert config.temperature == 0.6

        # Cleanup
        os.unlink(f.name)


def test_get_nested():
    """Test getting nested configuration values."""
    config = Config()
    assert config.get("model", "default_model") == "gemini-2.5-pro"
    assert config.get("nonexistent", "key", default="fallback") == "fallback"


def test_retry_settings():
    """Test retry settings."""
    config = Config()
    assert config.retry_attempts == 3
    assert config.retry_delay == 1.0


def test_global_config():
    """Test global config instance."""
    config1 = get_config()
    config2 = get_config()
    assert config1 is config2

    # Test reload
    config3 = get_config(reload=True)
    assert config3 is config2  # Same instance, reloaded
