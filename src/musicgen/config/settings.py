"""Configuration management for MusicGen.

Loads configuration from YAML file and environment variables.
Environment variables override YAML defaults.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from musicgen.config.defaults import DEFAULT_CONFIG


class Config:
    """Configuration manager for MusicGen.

    Loads from:
    1. config/musicgen.yaml (defaults, committed)
    2. config/musicgen.local.yaml (local overrides, not committed)
    3. Environment variables (runtime overrides)
    """

    def __init__(self, config_path: Path | None = None):
        """Initialize configuration.

        Args:
            config_path: Optional path to config file.
        """
        self._data: dict[str, Any] = {}
        self._load_config(config_path)

    def _load_config(self, config_path: Path | None) -> None:
        """Load configuration from file and environment."""
        # Start with defaults
        self._data = DEFAULT_CONFIG.copy()

        if YAML_AVAILABLE:
            # Load base config
            base_path = config_path or self._find_config_file()
            if base_path and base_path.exists():
                self._data.update(self._load_yaml(base_path))

            # Load local overrides
            local_path = base_path.parent / "musicgen.local.yaml" if base_path else None
            if local_path and local_path.exists():
                self._data.update(self._load_yaml(local_path))

        # Apply environment variable overrides
        self._apply_env_overrides()

    def _find_config_file(self) -> Path | None:
        """Find the configuration file.

        Searches in standard locations.
        """
        candidates = [
            Path("config/musicgen.yaml"),
            Path("musicgen.yaml"),
            Path.home() / ".config" / "musicgen" / "config.yaml",
        ]
        for path in candidates:
            if path.exists():
                return path
        return None

    def _load_yaml(self, path: Path) -> dict[str, Any]:
        """Load YAML file."""
        with open(path) as f:
            return yaml.safe_load(f) or {}

    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides.

        Supported env vars:
        - GEMINI_MODEL
        - GEMINI_TEMPERATURE
        - GEMINI_MAX_TOKENS
        - DEFAULT_OUTPUT_DIR
        - DEFAULT_FORMATS
        """
        env_mappings = {
            "GEMINI_MODEL": ("model", "default_model"),
            "GEMINI_TEMPERATURE": ("model", "default_temperature"),
            "GEMINI_MAX_TOKENS": ("model", "default_max_tokens"),
            "DEFAULT_OUTPUT_DIR": ("export", "default_output_dir"),
            "DEFAULT_FORMATS": ("export", "default_formats"),
        }

        for env_var, config_path in env_mappings.items():
            value = os.environ.get(env_var)
            if value is not None:
                # Navigate nested dict
                target = self._data
                for key in config_path[:-1]:
                    target = target.setdefault(key, {})
                final_key = config_path[-1]

                # Parse value based on type
                if final_key == "default_temperature":
                    value = float(value)
                elif final_key == "default_max_tokens":
                    value = int(value) if value else None
                elif final_key == "default_formats":
                    value = value.split(",")

                target[final_key] = value

    def get(self, *path: str, default: Any = None) -> Any:
        """Get configuration value by path.

        Args:
            *path: Keys to navigate (e.g., "model", "default_model")
            default: Default value if not found

        Returns:
            Configuration value
        """
        value = self._data
        for key in path:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    # Convenience properties
    @property
    def model(self) -> str:
        """Get the AI model name."""
        return os.environ.get("GEMINI_MODEL", self.get("model", "default_model", default="gemini-2.5-pro"))

    @property
    def temperature(self) -> float:
        """Get the sampling temperature."""
        env_val = os.environ.get("GEMINI_TEMPERATURE")
        if env_val:
            return float(env_val)
        return self.get("model", "default_temperature", default=0.5)

    @property
    def max_tokens(self) -> int | None:
        """Get max output tokens."""
        env_val = os.environ.get("GEMINI_MAX_TOKENS")
        if env_val:
            return int(env_val) if env_val else None
        return self.get("model", "default_max_tokens")

    @property
    def api_key(self) -> str | None:
        """Get the API key from environment."""
        return os.environ.get("GOOGLE_API_KEY")

    @property
    def retry_attempts(self) -> int:
        """Get retry attempts."""
        return self.get("model", "retry_attempts", default=3)

    @property
    def retry_delay(self) -> float:
        """Get retry delay."""
        return self.get("model", "retry_delay", default=1.0)


# Global config instance
_config: Config | None = None


def get_config(reload: bool = False) -> Config:
    """Get the global configuration instance.

    Args:
        reload: Force reload configuration

    Returns:
        Config instance
    """
    global _config
    if _config is None or reload:
        _config = Config()
    return _config


def set_config(config: Config) -> None:
    """Set the global configuration instance.

    Args:
        config: Config instance to use
    """
    global _config
    _config = config
