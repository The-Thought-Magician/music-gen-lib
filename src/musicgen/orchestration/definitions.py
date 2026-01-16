"""Instrument definition layer for V3 SFZ rendering.

This module loads and manages instrument definitions from YAML,
providing access to instrument properties, ranges, articulations,
and ensemble presets.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, field_validator


# Type aliases
InstrumentFamily = Literal[
    "strings", "woodwinds", "brass", "percussion", "keyboards"
]

Clef = Literal[
    "treble", "bass", "alto", "tenor", "grand_staff", "percussion"
]

DynamicMarking = Literal[
    "ppp", "pp", "p", "mp", "mf", "f", "ff", "fff"
]


class DynamicRange(BaseModel):
    """Pitch range for a specific dynamic level."""

    min: int = Field(ge=0, le=127)
    max: int = Field(ge=0, le=127)


class Articulation(BaseModel):
    """An articulation definition for an instrument."""

    keyswitch: int = Field(ge=0, le=127)
    duration_mod: float = Field(gt=0)
    velocity_mod: float = Field(gt=0)
    description: str = ""


class InstrumentDefinition(BaseModel):
    """Complete definition of an orchestral instrument."""

    name: str
    family: InstrumentFamily
    midi_program: int = Field(ge=0, le=127)
    default_clef: Clef
    range: DynamicRange
    dynamic_ranges: dict[DynamicMarking, DynamicRange]
    articulations: dict[str, Articulation]
    sfz_file: str
    sfz_library: str
    midi_channel: int = Field(ge=0, le=15)

    @field_validator("dynamic_ranges")
    @classmethod
    def validate_dynamic_ranges(cls, v: dict) -> dict:
        """Ensure dynamic ranges are valid."""
        for dynamic, drange in v.items():
            if not isinstance(drange, dict):
                continue
            if "min" not in drange or "max" not in drange:
                continue
            if drange["min"] > drange["max"]:
                raise ValueError(f"Invalid range for {dynamic}: min > max")
        return v

    def get_range_for_dynamic(self, dynamic: DynamicMarking | str) -> DynamicRange:
        """Get the pitch range for a specific dynamic level."""
        key = str(dynamic).lower().replace("_", "")
        if key in self.dynamic_ranges:
            dr = self.dynamic_ranges[key]
            if isinstance(dr, dict):
                return DynamicRange(**dr)
            return dr
        # Fall back to default range
        return self.range

    def get_articulation_keyswitch(self, articulation: str) -> int | None:
        """Get the keyswitch for an articulation."""
        art = self.articulations.get(articulation)
        if art:
            if isinstance(art, dict):
                return art.get("keyswitch")
            return art.keyswitch
        return None


class EnsembleDefinition(BaseModel):
    """Definition of an ensemble preset."""

    name: str
    instruments: list[str]  # References to instrument keys


class InstrumentLibrary(BaseModel):
    """Complete instrument library with ensembles."""

    instruments: dict[str, InstrumentDefinition]
    ensembles: dict[str, EnsembleDefinition]

    def get_instrument(self, key: str) -> InstrumentDefinition | None:
        """Get an instrument definition by key."""
        inst = self.instruments.get(key)
        if inst and isinstance(inst, dict):
            return InstrumentDefinition(**inst)
        return inst

    def get_ensemble(self, key: str) -> EnsembleDefinition | None:
        """Get an ensemble definition by key."""
        ens = self.ensembles.get(key)
        if ens and isinstance(ens, dict):
            return EnsembleDefinition(**ens)
        return ens

    def get_ensemble_instruments(self, key: str) -> list[InstrumentDefinition]:
        """Get all instrument definitions for an ensemble."""
        ensemble = self.get_ensemble(key)
        if not ensemble:
            return []

        instruments = []
        for inst_key in ensemble.instruments:
            inst = self.get_instrument(inst_key)
            if inst:
                instruments.append(inst)
        return instruments

    def list_instruments_by_family(self, family: InstrumentFamily) -> list[str]:
        """List all instrument keys for a family."""
        return [
            key for key, inst in self.instruments.items()
            if (inst.family if isinstance(inst, InstrumentDefinition)
                else inst.get("family")) == family
        ]

    def list_ensembles(self) -> list[str]:
        """List all available ensemble keys."""
        return list(self.ensembles.keys())


def load_instrument_definitions(
    path: str | Path | None = None
) -> InstrumentLibrary:
    """Load instrument definitions from YAML file.

    Args:
        path: Path to YAML file. If None, uses default location.

    Returns:
        InstrumentLibrary with all definitions.

    Raises:
        FileNotFoundError: If the YAML file doesn't exist.
        ValueError: If the YAML is invalid.
    """
    if path is None:
        # Default path
        from musicgen import __file__ as musicgen_init
        base_dir = Path(musicgen_init).parent.parent.parent
        path = base_dir / "resources" / "instrument_definitions.yaml"

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Instrument definitions not found: {path}")

    with open(path) as f:
        data = yaml.safe_load(f)

    # Validate structure
    if "instruments" not in data:
        raise ValueError("Invalid instrument definitions: missing 'instruments'")

    # Convert nested dicts to models
    instruments = {}
    for key, inst_data in data.get("instruments", {}).items():
        # Convert dynamic ranges dict values to DynamicRange
        if "dynamic_ranges" in inst_data:
            dranges = {}
            for dyn, drange in inst_data["dynamic_ranges"].items():
                if isinstance(drange, dict):
                    dranges[dyn] = DynamicRange(**drange)
                else:
                    dranges[dyn] = drange
            inst_data["dynamic_ranges"] = dranges

        # Convert articulations dict values to Articulation
        if "articulations" in inst_data:
            artics = {}
            for art_name, artic in inst_data["articulations"].items():
                if isinstance(artic, dict):
                    artics[art_name] = Articulation(**artic)
                else:
                    artics[art_name] = artic
            inst_data["articulations"] = artics

        # Convert main range
        if "range" in inst_data and isinstance(inst_data["range"], dict):
            inst_data["range"] = DynamicRange(**inst_data["range"])

        instruments[key] = InstrumentDefinition(**inst_data)

    ensembles = {}
    for key, ens_data in data.get("ensembles", {}).items():
        ensembles[key] = EnsembleDefinition(**ens_data)

    return InstrumentLibrary(
        instruments=instruments,
        ensembles=ensembles,
    )


# Singleton instance
_library_cache: InstrumentLibrary | None = None


def get_instrument_library() -> InstrumentLibrary:
    """Get the singleton instrument library instance.

    Loads from default location on first call.
    """
    global _library_cache
    if _library_cache is None:
        _library_cache = load_instrument_definitions()
    return _library_cache


def get_instrument(key: str) -> InstrumentDefinition | None:
    """Get an instrument definition by key."""
    return get_instrument_library().get_instrument(key)


def get_ensemble(key: str) -> EnsembleDefinition | None:
    """Get an ensemble definition by key."""
    return get_instrument_library().get_ensemble(key)


def list_ensembles() -> list[str]:
    """List all available ensemble keys."""
    return get_instrument_library().list_ensembles()


def list_instruments_by_family(family: InstrumentFamily) -> list[str]:
    """List all instrument keys for a family."""
    return get_instrument_library().list_instruments_by_family(family)
