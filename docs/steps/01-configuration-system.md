# Step 1: Configuration System

## Objective

Create a dual-layer configuration system:
1. **`.env`** - User secrets and overrides (not committed)
2. **`config/musicgen.yaml`** - Default values (committed)

## Overview

The configuration system supports:
- Model settings (gemini-2.5-pro, temperature, max tokens)
- Schema generation options
- Export defaults
- Runtime overrides

## File Structure

```
.env                          # User secrets (gitignore)
config/musicgen.yaml          # Default config (committed)
src/musicgen/config/__init__.py
```

## Tasks

### 1.1 Create Config Module Structure

- [ ] Create `src/musicgen/config/` package
- [ ] Create `__init__.py` with public API

### 1.2 YAML Configuration File

Create `config/musicgen.yaml`:

```yaml
# AI Model Configuration
model:
  # Model to use for composition
  default_model: "gemini-2.5-pro"
  # Sampling temperature (0.0-1.0), lower = more deterministic
  default_temperature: 0.5
  # Maximum output tokens (null = unlimited)
  default_max_tokens: null
  # Retry attempts for failed API calls
  retry_attempts: 3
  # Delay between retries (seconds)
  retry_delay: 1.0

# Schema Generation
schema:
  # Include form structure in schema
  include_form_structure: true
  # Include dynamics markings
  include_dynamics: true
  # Include articulation markings
  include_articulation: true
  # Include tempo changes
  include_tempo_changes: true
  # Include time signature changes
  include_time_signature_changes: true
  # Include key changes (modulation)
  include_key_changes: true

# Note Sequence Options
notes:
  # Representation format: "json", "compact", "detailed"
  default_format: "detailed"
  # Duration unit: "quarter", "second", "tick"
  duration_unit: "quarter"
  # Velocity range (0-127)
  velocity_min: 60
  velocity_max: 100

# Export Defaults
export:
  # Default output directory
  default_output_dir: "."
  # Default export formats
  default_formats: ["midi", "wav"]
  # Audio sample rate
  sample_rate: 44100
  # Audio bit depth
  bit_depth: 16

# Orchestration
orchestration:
  # Maximum number of instruments
  max_instruments: 16
  # Default MIDI channel mapping
  midi_channels: auto

# Validation
validation:
  # Validate AI output against schema
  strict_schema_validation: true
  # Validate music theory rules
  validate_music_theory: false  # AI is responsible
  # Maximum duration per composition (seconds)
  max_duration: 600
```

### 1.3 Environment Variables

Create `.env.example`:

```bash
# Google AI Configuration
GOOGLE_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-2.5-pro
GEMINI_TEMPERATURE=0.5
GEMINI_MAX_TOKENS=

# Export Configuration
DEFAULT_OUTPUT_DIR=./output
DEFAULT_FORMATS=midi,wav

# SoundFont Path (optional, uses default if not set)
SOUNDFONT_PATH=
```

Update `.gitignore`:
```
.env
.env.local
config/musicgen.local.yaml
```

### 1.4 Configuration Module

Create `src/musicgen/config/settings.py`:

```python
"""Configuration management for MusicGen.

Loads configuration from YAML file and environment variables.
Environment variables override YAML defaults.
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Optional
import os

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from .defaults import DEFAULT_CONFIG


class Config:
    """Configuration manager for MusicGen.

    Loads from:
    1. config/musicgen.yaml (defaults, committed)
    2. config/musicgen.local.yaml (local overrides, not committed)
    3. Environment variables (runtime overrides)
    """

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration.

        Args:
            config_path: Optional path to config file.
        """
        self._data: dict[str, Any] = {}
        self._load_config(config_path)

    def _load_config(self, config_path: Optional[Path]) -> None:
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

    def _find_config_file(self) -> Optional[Path]:
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
        with open(path, "r") as f:
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
    def max_tokens(self) -> Optional[int]:
        """Get max output tokens."""
        env_val = os.environ.get("GEMINI_MAX_TOKENS")
        if env_val:
            return int(env_val) if env_val else None
        return self.get("model", "default_max_tokens")

    @property
    def api_key(self) -> Optional[str]:
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
_config: Optional[Config] = None


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
```

### 1.5 Default Configuration

Create `src/musicgen/config/defaults.py`:

```python
"""Default configuration values."""

DEFAULT_CONFIG = {
    "model": {
        "default_model": "gemini-2.5-pro",
        "default_temperature": 0.5,
        "default_max_tokens": None,
        "retry_attempts": 3,
        "retry_delay": 1.0,
    },
    "schema": {
        "include_form_structure": True,
        "include_dynamics": True,
        "include_articulation": True,
        "include_tempo_changes": True,
        "include_time_signature_changes": True,
        "include_key_changes": True,
    },
    "notes": {
        "default_format": "detailed",
        "duration_unit": "quarter",
        "velocity_min": 60,
        "velocity_max": 100,
    },
    "export": {
        "default_output_dir": ".",
        "default_formats": ["midi", "wav"],
        "sample_rate": 44100,
        "bit_depth": 16,
    },
    "orchestration": {
        "max_instruments": 16,
        "midi_channels": "auto",
    },
    "validation": {
        "strict_schema_validation": True,
        "validate_music_theory": False,
        "max_duration": 600,
    },
}
```

### 1.6 Update Dependencies

Update `pyproject.toml`:

```toml
[project.dependencies]
pyyaml >= 6.0
python-dotenv >= 1.0
```

### 1.7 Testing

Create `tests/test_config.py`:

```python
"""Test configuration system."""

import os
from pathlib import Path
import tempfile

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

    config = Config()
    assert config.temperature == 0.7

    # Cleanup
    del os.environ["GEMINI_MODEL"]
    del os.environ["GEMINI_TEMPERATURE"]


def test_yaml_loading():
    """Test YAML configuration loading."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml") as f:
        f.write("model:\n  default_temperature: 0.6\n")
        f.flush()

        config = Config(config_path=Path(f.name))
        assert config.temperature == 0.6


def test_get_nested():
    """Test getting nested configuration values."""
    config = Config()
    assert config.get("model", "default_model") == "gemini-2.5-pro"
    assert config.get("nonexistent", "key", default="fallback") == "fallback"
```

### 1.8 Documentation

- [ ] Update README with configuration documentation
- [ ] Document all config options
- [ ] Add `.env.example` to repo
- [ ] Document environment variable overrides

## Deliverables

- `config/musicgen.yaml` - Default configuration
- `.env.example` - Environment variable template
- `src/musicgen/config/__init__.py`
- `src/musicgen/config/settings.py`
- `src/musicgen/config/defaults.py`
- `tests/test_config.py`
- Updated README

## Validation

```python
# Test config loading
from musicgen.config import get_config

config = get_config()

# Model settings
assert config.model == "gemini-2.5-pro"
assert config.temperature == 0.5
assert config.api_key is None  # Unless set in env

# Export settings
assert config.get("export", "default_formats") == ["midi", "wav"]
```

## Next Steps

After completing this step:
- Step 2: Schema generation engine
- Step 3: AI note sequence models
