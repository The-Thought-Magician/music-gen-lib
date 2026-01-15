"""Ensemble definitions and classes.

This module provides classes for representing musical ensembles
and their configurations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from musicgen.orchestration.instruments import Instrument, InstrumentFamily


class TextureType(Enum):
    """Types of musical texture."""

    MONOPHONIC = "monophonic"     # Single melody
    HOMOPHONIC = "homophonic"     # Melody with accompaniment
    POLYPHONIC = "polyphonic"     # Independent voices
    HETEROPHONIC = "heterophonic" # Simultaneous variation


@dataclass
class Texture:
    """Represents musical texture.

    Attributes:
        texture_type: The type of texture
        melody_instruments: Instruments carrying the melody
        harmony_instruments: Instruments providing harmony
        bass_instruments: Instruments providing bass
    """

    texture_type: TextureType = TextureType.HOMOPHONIC
    melody_instruments: list[str] = field(default_factory=list)
    harmony_instruments: list[str] = field(default_factory=list)
    bass_instruments: list[str] = field(default_factory=list)

    @classmethod
    def monophonic(cls, melody_instruments: list[str]) -> Texture:
        """Create a monophonic texture.

        Args:
            melody_instruments: Instruments playing the melody

        Returns:
            A new Texture
        """
        return cls(
            texture_type=TextureType.MONOPHONIC,
            melody_instruments=melody_instruments
        )

    @classmethod
    def homophonic(cls, melody_instruments: list[str],
                   harmony_instruments: list[str] | None = None,
                   bass_instruments: list[str] | None = None) -> Texture:
        """Create a homophonic texture.

        Args:
            melody_instruments: Instruments playing the melody
            harmony_instruments: Instruments playing harmony
            bass_instruments: Instruments playing bass

        Returns:
            A new Texture
        """
        return cls(
            texture_type=TextureType.HOMOPHONIC,
            melody_instruments=melody_instruments,
            harmony_instruments=harmony_instruments or [],
            bass_instruments=bass_instruments or []
        )

    @classmethod
    def polyphonic(cls, instruments: list[str]) -> Texture:
        """Create a polyphonic texture.

        Args:
            instruments: All instruments (with independent lines)

        Returns:
            A new Texture
        """
        return cls(
            texture_type=TextureType.POLYPHONIC,
            melody_instruments=instruments
        )


@dataclass
class Ensemble:
    """Represents a musical ensemble.

    Attributes:
        name: The ensemble name
        instruments: List of instruments in the ensemble
        texture: The default texture
    """

    name: str
    instruments: list[Instrument] = field(default_factory=list)
    texture: Texture | None = None

    # Common ensemble presets
    _PRESETS: dict[str, list[dict]] = field(default_factory=dict, repr=False)

    def __post_init__(self):
        """Initialize ensemble and set up presets."""
        if not self._PRESETS:
            self._PRESETS = {
                "string_quartet": [
                    {"name": "violin", "role": "violin_i"},
                    {"name": "violin", "role": "violin_ii"},
                    {"name": "viola", "role": "viola"},
                    {"name": "cello", "role": "cello"},
                ],
                "string_orchestra": [
                    {"name": "violin", "role": "violin_i"},
                    {"name": "violin", "role": "violin_ii"},
                    {"name": "viola", "role": "viola"},
                    {"name": "cello", "role": "cello"},
                    {"name": "double_bass", "role": "bass"},
                ],
                "woodwind_quintet": [
                    {"name": "flute", "role": "flute"},
                    {"name": "oboe", "role": "oboe"},
                    {"name": "clarinet", "role": "clarinet"},
                    {"name": "bassoon", "role": "bassoon"},
                    {"name": "french_horn", "role": "horn"},
                ],
                "orchestra": [
                    # Strings
                    {"name": "violin", "role": "violin_i"},
                    {"name": "violin", "role": "violin_ii"},
                    {"name": "viola", "role": "viola"},
                    {"name": "cello", "role": "cello"},
                    {"name": "double_bass", "role": "bass"},
                    # Woodwinds
                    {"name": "flute", "role": "flute"},
                    {"name": "oboe", "role": "oboe"},
                    {"name": "clarinet", "role": "clarinet"},
                    {"name": "bassoon", "role": "bassoon"},
                    # Brass
                    {"name": "trumpet", "role": "trumpet"},
                    {"name": "french_horn", "role": "horn"},
                    {"name": "trombone", "role": "trombone"},
                    # Percussion/Keyboard
                    {"name": "piano", "role": "piano"},
                ],
                "piano_trio": [
                    {"name": "piano", "role": "piano"},
                    {"name": "violin", "role": "violin"},
                    {"name": "cello", "role": "cello"},
                ],
            }

    @property
    def size(self) -> int:
        """Return the number of instruments."""
        return len(self.instruments)

    def get_instruments_by_family(self, family: InstrumentFamily) -> list[Instrument]:
        """Get all instruments of a specific family.

        Args:
            family: The instrument family

        Returns:
            List of instruments in that family
        """
        return [i for i in self.instruments if i.family == family]

    def add_instrument(self, instrument: Instrument) -> None:
        """Add an instrument to the ensemble.

        Args:
            instrument: Instrument to add
        """
        self.instruments.append(instrument)

    @classmethod
    def preset(cls, name: str) -> Ensemble:
        """Create an ensemble from a preset name.

        Args:
            name: Preset name

        Returns:
            A new Ensemble with preset configuration
        """
        # Create a dummy instance to access presets
        dummy = cls(name=name)
        presets = dummy._PRESETS

        if name.lower() not in presets:
            return cls(name=name)

        config = presets[name.lower()]
        instruments = []

        for inst_config in config:
            inst = Instrument.preset(inst_config["name"])
            inst.role = inst_config.get("role", inst_config["name"])
            instruments.append(inst)

        # Set default texture
        texture = Texture.homophonic(
            melody_instruments=[i.name for i in instruments[:1]],
            harmony_instruments=[i.name for i in instruments[1:-1]],
            bass_instruments=[instruments[-1].name] if instruments else []
        )

        return cls(name=name, instruments=instruments, texture=texture)

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Ensemble({self.name}, {self.size} instruments)"

    def __iter__(self):
        """Allow iteration over instruments."""
        return iter(self.instruments)

    def __len__(self) -> int:
        """Return length."""
        return len(self.instruments)
