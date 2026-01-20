"""Tala (rhythmic cycle) database and tala-based rhythm generation engine.

This module provides authentic Indian classical tala definitions including
beat patterns (matras), vibhag divisions, and accent patterns.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


# =============================================================================
# Tala Definitions
# =============================================================================


@dataclass
class Vibhag:
    """A division (vibhag) within a tala cycle."""

    beats: int  # Number of beats (matras) in this vibhag
    accent: Literal["heavy", "light", "medium"]  # Accent strength
    clap: bool  # Whether to clap on this beat (for marking tala)


@dataclass
class Tala:
    """Definition of an Indian classical tala (rhythmic cycle)."""

    name: str
    matras: int  # Total beats in the cycle
    vibhags: list[Vibhag]  # Divisions of the cycle
    bols: list[str] | None = None  # Syllabic representation (dha, din, etc.)
    avart: float = 1.0  # Time for one cycle in seconds (at reference tempo)

    @property
    def beat_pattern(self) -> list[int]:
        """Get the accent pattern as a list of velocities (0-3).

        0 = no accent, 1 = light, 2 = medium, 3 = heavy
        """
        pattern = []
        for vibhag in self.vibhags:
            # First beat of vibhag gets the accent
            match vibhag.accent:
                case "heavy":
                    pattern.append(3)
                case "medium":
                    pattern.append(2)
                case "light":
                    pattern.append(1)
            # Remaining beats in vibhag get no accent
            pattern.extend([0] * (vibhag.beats - 1))
        return pattern

    @property
    def division_points(self) -> list[int]:
        """Get the beat numbers where each vibhag starts."""
        points = [0]
        for vibhag in self.vibhags[:-1]:
            points.append(points[-1] + vibhag.beats)
        return points

    def get_accent_for_beat(self, beat: int) -> int:
        """Get accent level for a specific beat in the cycle.

        Args:
            beat: Beat number within the cycle (0-indexed)

        Returns:
            Accent level 0-3 (none, light, medium, heavy)
        """
        pattern = self.beat_pattern
        return pattern[beat % len(pattern)]

    def get_vibhag_for_beat(self, beat: int) -> int:
        """Get which vibhag a beat belongs to.

        Args:
            beat: Beat number within the cycle (0-indexed)

        Returns:
            Vibhag index (0-based)
        """
        count = 0
        for i, vibhag in enumerate(self.vibhags):
            if count <= beat < count + vibhag.beats:
                return i
            count += vibhag.beats
        return 0


# =============================================================================
# Tala Database
# =============================================================================


_TALA_DATABASE = {
    "teental": Tala(
        name="Teental",
        matras=16,
        vibhags=[
            Vibhag(beats=4, accent="heavy", clap=True),    # Sam (first beat)
            Vibhag(beats=4, accent="light", clap=False),  # Tal
            Vibhag(beats=4, accent="medium", clap=True),  # Khali
            Vibhag(beats=4, accent="light", clap=False),  # Tal
        ],
        bols=["dha", "dhin", "dhin", "dha",  # Vibhag 1 (Sam)
              "dha", "dhin", "dhin", "dha",  # Vibhag 2
              "dha", "tin", "tin", "ta",     # Vibhag 3 (Khali)
              "kat", "ge", "dhi", "na"],     # Vibhag 4
    ),
    "jhaptal": Tala(
        name="Jhaptal",
        matras=10,
        vibhags=[
            Vibhag(beats=2, accent="heavy", clap=True),    # Sam
            Vibhag(beats=3, accent="light", clap=False),
            Vibhag(beats=2, accent="medium", clap=True),   # Khali
            Vibhag(beats=3, accent="light", clap=False),
        ],
        bols=["dha", "dhin",
              "dhin", "dha", "dhin",
              "dha", "dhin",
              "dhin", "dha"],
    ),
    "rupak": Tala(
        name="Rupak",
        matras=7,
        vibhags=[
            Vibhag(beats=3, accent="heavy", clap=False),   # Sam (no clap in Rupak!)
            Vibhag(beats=2, accent="medium", clap=True),
            Vibhag(beats=2, accent="light", clap=False),
        ],
        bols=["tin", "tin", "na",
              "dhin", "na",
              "dha", "ge"],
    ),
    "dadra": Tala(
        name="Dadra",
        matras=6,
        vibhags=[
            Vibhag(beats=3, accent="heavy", clap=True),
            Vibhag(beats=3, accent="light", clap=False),
        ],
        bols=["dha", "dhin", "dha",
              "dha", "dhin", "dha"],
    ),
    "keherwa": Tala(
        name="Keherwa",
        matras=8,
        vibhags=[
            Vibhag(beats=4, accent="heavy", clap=True),
            Vibhag(beats=4, accent="light", clap=False),
        ],
        bols=["dha", "ge", "na", "ti",
              "na", "ke", "dhi", "na"],
    ),
    "ektal": Tala(
        name="Ektal",
        matras=12,
        vibhags=[
            Vibhag(beats=2, accent="heavy", clap=True),    # Sam
            Vibhag(beats=2, accent="light", clap=False),
            Vibhag(beats=2, accent="medium", clap=True),   # Khali
            Vibhag(beats=2, accent="light", clap=False),
            Vibhag(beats=2, accent="medium", clap=True),
            Vibhag(beats=2, accent="light", clap=False),
        ],
        bols=["dhin", "dhin",
              "dha", "dha",
              "dhin", "dhin",
              "dha", "dha",
              "dhin", "dhin",
              "dha", "dha"],
    ),
    "chautal": Tala(
        name="Chautal",
        matras=12,
        vibhags=[
            Vibhag(beats=2, accent="heavy", clap=True),
            Vibhag(beats=2, accent="light", clap=False),
            Vibhag(beats=2, accent="medium", clap=True),
            Vibhag(beats=2, accent="light", clap=False),
            Vibhag(beats=2, accent="medium", clap=True),
            Vibhag(beats=2, accent="light", clap=False),
        ],
        bols=["dha", "dha",
              "dhin", "dhin",
              "dha", "dha",
              "dhin", "dhin",
              "dha", "dha",
              "dhin", "dhin"],
    ),
    "deepchandi": Tala(
        name="Deepchandi",
        matras=14,
        vibhags=[
            Vibhag(beats=3, accent="heavy", clap=True),    # Sam
            Vibhag(beats=4, accent="light", clap=False),
            Vibhag(beats=3, accent="medium", clap=True),   # Khali
            Vibhag(beats=4, accent="light", clap=False),
        ],
        bols=["dha", "dhin", "dhin",
              "dha", "dhin", "dhin", "dha",
              "dha", "tin", "tin",
              "ta", "dhin", "dhin", "dha"],
    ),
    "tilwada": Tala(
        name="Tilwada",
        matras=16,
        vibhags=[
            Vibhag(beats=4, accent="heavy", clap=True),    # Sam
            Vibhag(beats=4, accent="light", clap=False),
            Vibhag(beats=4, accent="medium", clap=True),   # Khali
            Vibhag(beats=4, accent="light", clap=False),
        ],
        bols=["dha", "dhin", "dhin", "dha",
              "dha", "dhin", "dhin", "dha",
              "dha", "tin", "tin", "ta",
              "kat", "ge", "dhi", "na"],
    ),
    "bammbai": Tala(
        name="Bammbai",
        matras=16,
        vibhags=[
            Vibhag(beats=4, accent="heavy", clap=True),
            Vibhag(beats=4, accent="light", clap=False),
            Vibhag(beats=4, accent="medium", clap=True),
            Vibhag(beats=4, accent="light", clap=False),
        ],
    ),
    "punjabi": Tala(
        name="Punjabi",
        matras=16,
        vibhags=[
            Vibhag(beats=4, accent="heavy", clap=True),
            Vibhag(beats=4, accent="light", clap=False),
            Vibhag(beats=4, accent="medium", clap=True),
            Vibhag(beats=4, accent="light", clap=False),
        ],
    ),
}


# =============================================================================
# Tala Query Functions
# =============================================================================


def get_tala(name: str) -> Tala:
    """Get a tala definition by name.

    Args:
        name: Tala name (case-insensitive)

    Returns:
        Tala definition

    Raises:
        KeyError: If tala not found
    """
    name_lower = name.lower()

    # Try exact match first
    for tala_name, tala in _TALA_DATABASE.items():
        if tala_name.lower() == name_lower:
            return tala

    # Try partial match
    for tala_name, tala in _TALA_DATABASE.items():
        if name_lower in tala_name.lower():
            return tala

    raise KeyError(f"Tala not found: {name}")


def list_talas() -> list[str]:
    """List all available talas."""
    return list(_TALA_DATABASE.keys())


# =============================================================================
# Tala Engine
# =============================================================================


class TalaEngine:
    """Engine for tala-based rhythm generation."""

    def __init__(self) -> None:
        self._cache: dict[str, Tala] = {}

    def get_tala(self, name: str) -> Tala:
        """Get a tala from cache or database."""
        if name not in self._cache:
            self._cache[name] = get_tala(name)
        return self._cache[name]

    def generate_cycle_pattern(
        self,
        tala_name: str,
        num_cycles: int = 1,
        bpm: float = 60.0,
    ) -> list[tuple[int, float, int]]:
        """Generate a rhythmic pattern based on tala.

        Args:
            tala_name: Name of the tala
            num_cycles: Number of cycles (avart) to generate
            bpm: Tempo in beats per minute

        Returns:
            List of (beat_number, time, accent) tuples
            beat_number: Position in cycle (0-indexed)
            time: Absolute time in seconds
            accent: Accent level 0-3
        """
        tala = self.get_tala(tala_name)

        pattern = []
        beat_duration = 60.0 / bpm  # Seconds per beat

        for cycle in range(num_cycles):
            for beat in range(tala.matras):
                absolute_beat = cycle * tala.matras + beat
                time = absolute_beat * beat_duration
                accent = tala.get_accent_for_beat(beat)
                pattern.append((beat, time, accent))

        return pattern

    def suggest_tabla_strokes(
        self,
        tala_name: str,
        complexity: str = "medium",
    ) -> list[str]:
        """Suggest tabla bols for a tala pattern.

        Args:
            tala_name: Name of the tala
            complexity: "simple", "medium", or "complex"

        Returns:
            List of tabla bols (syllables)
        """
        tala = self.get_tala(tala_name)

        if tala.bols and complexity == "simple":
            # Return the basic bols for the tala
            return tala.bols.copy()

        # For medium/complex, we could have variations
        # For now, return basic bols
        return tala.bols[:] if tala.bols else []

    def get_layakari(
        self,
        tala_name: str,
        laya: str = "vilambit",
    ) -> tuple[int, float]:
        """Get the appropriate tempo multipliers for different layas.

        Args:
            tala_name: Name of the tala
            laya: "vilambit" (slow), "madhya" (medium), or "drut" (fast)

        Returns:
            Tuple of (beats_per_cycle, tempo_multiplier)
        """
        tala = self.get_tala(tala_name)

        match laya.lower():
            case "vilambit":
                # Slow tempo - often counted in half-beats
                return (tala.matras // 2, 0.5)
            case "madhya":
                # Medium tempo
                return (tala.matras, 1.0)
            case "drut":
                # Fast tempo - often double
                return (tala.matras, 2.0)
            case _:
                return (tala.matras, 1.0)

    def calculate_cycle_duration(
        self,
        tala_name: str,
        bpm: float,
        laya: str = "madhya",
    ) -> float:
        """Calculate the duration of one tala cycle.

        Args:
            tala_name: Name of the tala
            bpm: Base tempo in beats per minute
            laya: Speed of rendition

        Returns:
            Duration in seconds for one cycle
        """
        tala = self.get_tala(tala_name)
        _, tempo_mult = self.get_layakari(tala_name, laya)
        effective_bpm = bpm * tempo_mult
        return (tala.matras / effective_bpm) * 60.0

    def get_sam_positions(
        self,
        tala_name: str,
        total_duration: float,
        bpm: float,
    ) -> list[float]:
        """Get the time positions of all Sam (first beat) occurrences.

        Args:
            tala_name: Name of the tala
            total_duration: Total duration in seconds
            bpm: Tempo in beats per minute

        Returns:
            List of times when Sam occurs
        """
        tala = self.get_tala(tala_name)
        cycle_duration = (tala.matras / bpm) * 60.0

        positions = []
        time = 0.0
        while time < total_duration:
            positions.append(time)
            time += cycle_duration

        return positions


# =============================================================================
# Utility Functions
# =============================================================================


def get_beats_for_tala(tala_name: str) -> int:
    """Get the number of beats (matras) in a tala.

    Utility function for other modules.

    Args:
        tala_name: Name of the tala

    Returns:
        Number of beats in one cycle
    """
    tala = get_tala(tala_name)
    return tala.matras


def get_accent_pattern(tala_name: str) -> list[int]:
    """Get the accent pattern for a tala.

    Args:
        tala_name: Name of the tala

    Returns:
        List of accent levels (0-3) for each beat
    """
    tala = get_tala(tala_name)
    return tala.beat_pattern.copy()
