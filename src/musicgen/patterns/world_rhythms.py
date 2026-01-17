"""
World rhythm patterns for music-gen-lib V4.

This module provides authentic rhythm patterns for Afro-Cuban, Brazilian,
Indian, and West African percussion traditions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    pass


# =============================================================================
# Afro-Cuban Rhythms
# =============================================================================


@dataclass
class ClavePattern:
    """
    Clave rhythm pattern - the foundational rhythm of Afro-Cuban music.

    Attributes:
        name: Pattern name
        region: Geographic origin
        pattern_3: The "3" side of the clave
        pattern_2: The "2" side of the clave
        combined: Full pattern
        subdivision: Note subdivision
    """

    name: str
    region: str
    pattern_3: str
    pattern_2: str
    combined: str
    subdivision: int = 16


SON_CLAVE = ClavePattern(
    name="Son Clave (3-2)",
    region="Cuba",
    pattern_3="x . x . . x .",
    pattern_2=". x . x . . x",
    combined="x . x . . x . . x . x . . x",
)

RUMBA_CLAVE = ClavePattern(
    name="Rumba Clave (3-2)",
    region="Cuba",
    pattern_3="x . x . . . x",
    pattern_2=". x . x . x .",
    combined="x . x . . . x . x . x . x .",
)

BOSSA_NOVA_CLAVE = ClavePattern(
    name="Bossa Nova Clave (3-2)",
    region="Brazil",
    pattern_3="x . x . . x .",
    pattern_2=". x . x . x . x . x",  # Modified for bossa
    combined="x . x . . x . . x . . x x .",
)

CLAVE_PATTERNS: dict[str, ClavePattern] = {
    "son": SON_CLAVE,
    "son_3_2": SON_CLAVE,
    "rumba": RUMBA_CLAVE,
    "rumba_3_2": RUMBA_CLAVE,
    "bossa_nova": BOSSA_NOVA_CLAVE,
}


@dataclass
class TumbaoPattern:
    """
    Tumbao pattern - the foundational conga rhythm in salsa.

    Attributes:
        name: Pattern name
        pattern_quinto: Quinto (highest conga) pattern
        pattern_conga: Conga pattern
        pattern_tumba: Tumba (lowest conga) pattern
    """

    name: str
    pattern_quinto: str
    pattern_conga: str
    pattern_tumba: str


TUMBAO_MODERN = TumbaoPattern(
    name="Tumbao (Modern)",
    pattern_quinto=". . . . . . . . . x . . . .",
    pattern_conga=". . x . x x . x x . x . x x .",
    pattern_tumba="x . . . x . . . x . . . x . .",
)

TUMBAO_TRADITIONAL = TumbaoPattern(
    name="Tumbao (Traditional)",
    pattern_quinto="",
    pattern_conga=". . x . x x . x x . x . x x .",
    pattern_tumba="",
)


# =============================================================================
# Brazilian Rhythms
# =============================================================================


@dataclass
class SambaPattern:
    """Samba rhythm pattern for carnival/bateria."""

    name: str
    surdo_marca: str  # Large bass drum - downbeat
    surdo_resposta: str  # Backbeat
    agogo: str  # Bell
    tamborim: str  # Shaker
    repinique: str  # Lead drum
    chocalho: str  # Shaker/friction


SAMBA_escola = SambaPattern(
    name="Samba Escola",
    surdo_marca="x . . . . . . .",
    surdo_resposta=". . . . x . . .",
    agogo="x . x . x . x .",
    tamborim="x x x x x x x x",
    repinique="x x x x . x . . x x",
    chocalho="x x x x x x x x",
)

SAMBA_ENREDO = SambaPattern(
    name="Samba Enredo",
    surdo_marca="x . . . . . . .",
    surdo_resposta=". . . . x . . .",
    agogo="x . x . x . x .",
    tamborim="x x x x x x x x",
    repinique="x x x x . x . . x x",
    chocalho="x x x x x x x x",
)


@dataclass
class BossaNovaPattern:
    """Bossa Nova rhythm pattern."""

    name: str
    guitar: str  # Classic guitar rhythm
    guiro: str
    agogo: str


BOSSA_NOVA = BossaNovaPattern(
    name="Bossa Nova",
    guitar="x . x . x . x .",
    guiro="x . x . x . x . x . x . x . x .",
    agogo="x . . x . . . x . . x . . .",
)


# =============================================================================
# Indian Talas (Rhythmic Cycles)
# =============================================================================


@dataclass
class Tala:
    """
    Indian tala (rhythmic cycle).

    Attributes:
        name: Tala name
        matra: Number of beats (matras) in the cycle
        vibhag: Sections of the tala
        bols: Syllables representing the rhythm
        clapping: Clapping pattern
    """

    name: str
    matra: int
    vibhag: list[int]
    bols: list[str]
    clapping: list[str] | None = None


TEENTAL = Tala(
    name="Teental (Tintal)",
    matra=16,
    vibhag=[4, 4, 4, 4],
    bols=["dha", "dhin", "dhin", "dha"] * 4,
    clapping=["+ x 2 +", "x 2 + x", "2 + x 2", "+ x 2 +"],
)

JHAPTAL = Tala(
    name="Jhaptal",
    matra=10,
    vibhag=[2, 3, 4],
    bols=["dha", "dhin", "na", "dha", "dhin", "na", "dha", "dhin", "na", "dha"],
    clapping=["x 2", "+ 2 3", "x 2 3 4"],
)

RUPAK = Tala(
    name="Rupak",
    matra=7,
    vibhag=[3, 2, 2],
    bols=["tin", "tin", "na", "dha", "dhin", "na", "dha"],
    clapping=None,
)

EKTAL = Tala(
    name="Ektal",
    matra=12,
    vibhag=[4, 4],
    bols=["dha", "dha", "dha", "dhin"] * 3,
    clapping=["x 2 x 2", "x 2 x 2"],
)

DADRA = Tala(
    name="Dadra",
    matra=6,
    vibhag=[3, 3],
    bols=["dha", "dhin", "dha", "dha", "dhin", "dha"],
    clapping=["x 2 x", "x 2 x"],
)

ROOPAK = Tala(
    name="Roopak",
    matra=7,
    vibhag=[3, 2, 2],
    bols=["dha", "dha", "dha", "tirakita", "dha", "dha"],
    clapping=None,
)

JHAPTAAL = Tala(
    name="Jhaptal (modified)",
    matra=10,
    vibhag=[2, 4, 4],
    bols=["dha", "dha", "dhin", "dha", "dhin", "na", "dha", "tirakita", "dha", "dha"],
    clapping=["x 2", "+ 2 3 4", "x 2 3 4"],
)


TALAS: dict[str, Tala] = {
    "teental": TEENTAL,
    "tintal": TEENTAL,
    "jhaptal": JHAPTAL,
    "rupak": RUPAK,
    "ektal": EKTAL,
    "dadra": DADRA,
    "roopak": ROOPAK,
    "jhaptaal": JHAPTAAL,
}


# =============================================================================
# West African Polyrhythms
# =============================================================================


@dataclass
class Polyrhythm:
    """
    Polyrhythmic pattern for layering.

    Attributes:
        name: Pattern name
        region: Geographic origin
        patterns: Dictionary mapping instruments to their patterns
        pulse_lengths: Length of each pulse cycle
    """

    name: str
    region: str
    patterns: dict[str, str]
    pulse_lengths: dict[str, int] | None = None


# 3-over-2 cross-rhythm (common in African music)
CROSS_RHYTHM_3_2 = Polyrhythm(
    name="3-over-2 Cross-rhythm",
    region="West Africa",
    patterns={
        "pulse_3": "x . x",  # 3 hits in 2 beats
        "pulse_2": "x .",  # 2 hits in 2 beats
    },
    pulse_lengths={"pulse_3": 3, "pulse_2": 2},
)

# 6-over-4 (3-over-2 at double speed)
CROSS_RHYTHM_6_4 = Polyrhythm(
    name="6-over-4 Cross-rhythm",
    region="West Africa",
    patterns={
        "pulse_6": "x . x . x .",
        "pulse_4": "x . x .",
    },
    pulse_lengths={"pulse_6": 6, "pulse_4": 4},
)


# =============================================================================
# Pattern Generator
# =============================================================================


@dataclass
class PolyrhythmGenerator:
    """Generate polyrhythmic patterns."""

    def cross_rhythm(
        self,
        main_pulse: int,
        cross_pulse: int,
        length: int = 12,
    ) -> dict[str, list[bool]]:
        """
        Generate cross-rhythm (e.g., 3 over 4).

        Args:
            main_pulse: Number of hits in main pulse
            cross_pulse: Number of hits in cross pulse
            length: Total length in beats (should be LCM)

        Returns:
            Dictionary with two boolean patterns
        """
        # Generate main pulse pattern
        main_pattern: list[bool] = [False] * length
        for i in range(main_pulse):
            pos = int(i * length / main_pulse)
            if pos < length:
                main_pattern[pos] = True

        # Generate cross pulse pattern
        cross_pattern: list[bool] = [False] * length
        for i in range(cross_pulse):
            pos = int(i * length / cross_pulse)
            if pos < length:
                cross_pattern[pos] = True

        return {"main": main_pattern, "cross": cross_pattern}

    def euclidean_polyrhythm(
        self,
        pulses1: int,
        total1: int,
        pulses2: int,
        total2: int,
    ) -> dict[str, list[bool]]:
        """
        Generate Euclidean cross-rhythm using Bjorklund algorithm.

        Args:
            pulses1: Number of hits in first pattern
            total1: Total steps in first pattern
            pulses2: Number of hits in second pattern
            total2: Total steps in second pattern

        Returns:
            Dictionary with two boolean patterns
        """
        from musicgen.patterns.parser import PatternParser

        parser = PatternParser()

        # Use the parser's Bjorklund algorithm
        pattern1_events = parser._bjorklund(pulses1, total1)
        pattern2_events = parser._bjorklund(pulses2, total2)

        return {"pattern1": pattern1_events, "pattern2": pattern2_events}

    def lcm(self, a: int, b: int) -> int:
        """Calculate least common multiple."""
        import math

        return a * b // math.gcd(a, b)


# =============================================================================
# Rhythm Composer
# =============================================================================


@dataclass
class RhythmComposer:
    """Compose rhythm parts with world percussion."""

    def create_afro_cuban(
        self,
        style: Literal["son", "rumba", "salsa", "cha_cha"] = "son",
    ) -> dict[str, str]:
        """
        Create complete Afro-Cuban rhythm section.

        Returns:
            Dictionary mapping instruments to patterns
        """
        clave = SON_CLAVE if style in ["son", "salsa"] else RUMBA_CLAVE

        if style == "cha_cha":
            return {
                "clave": clave.combined,
                "timbale_mambo": "x . . x . . x . x . x x . . x",
                "congas": "x . . x . x x . x x . x x x",
                "guiro": "x . x . x . x . x . x . x . x .",
                "maracas": "x x x x x x x x x x x x x",
            }

        return {
            "clave": clave.combined,
            "timbale_cascara": "x . x . x x . x . x . x x .",
            "congas": ". . x . x x . x x . x . x x .",
            "guiro": "x . x . x . x . x . x . x . x .",
            "maracas": "x x x x x x x x x x x x x",
            "cowbell": "x . . x . . x . . x x . . x",
        }

    def create_brazilian(
        self,
        style: Literal["samba", "bossa", "forro"] = "samba",
    ) -> dict[str, str]:
        """Create complete Brazilian rhythm section."""
        if style == "samba":
            return {
                "surdo_1": SAMBA_ENREDO.surdo_marca,
                "surdo_2": SAMBA_ENREDO.surdo_resposta,
                "agogo": SAMBA_ENREDO.agogo,
                "tamborim": SAMBA_ENREDO.tamborim,
                "repinique": SAMBA_ENREDO.repinique,
                "chocalho": SAMBA_ENREDO.chocalho,
            }
        elif style == "bossa":
            return {
                "drum_kit_kick": "x . . . . . . . . . . . x .",
                "drum_kit_snare": ". . x . . . x . . . . x . . .",
                "drum_kit_hihat": ". x . x . x . x . . x . x . x .",
                "guitar": BOSSA_NOVA.guitar,
                "guiro": BOSSA_NOVA.guiro,
                "agogo": BOSSA_NOVA.agogo,
            }
        else:  # forro
            return {
                "zabumba": "x . . . x . . .",
                "triangle": "x x x x x x x x",
            }

    def create_indian(
        self,
        tala: str = "teental",  # noqa: ARG002
    ) -> dict[str, str]:
        """Create Indian tala with tabla bols."""
        tala_obj = TALAS.get(tala, TEENTAL)

        return {
            "tabla_bayan": " ".join([b for i, b in enumerate(tala_obj.bols) if i % 2 == 0]),
            "tabla_dayan": " ".join([b for i, b in enumerate(tala_obj.bols) if i % 2 == 1]),
        }

    def create_west_african(
        self,
        rhythm: str = "agbadza",
    ) -> dict[str, str]:
        """Create West African polyrhythmic ensemble."""
        if rhythm == "agbadza":
            return {
                "bell": "x . x . x x . x . x x . x .",
                "rattle": "x x x x x x x x x x x x x",
                "drum_1": "x . x . x . x . x . x . x .",
                "drum_2": "x x . . x x . . x x . . x x",
            }
        elif rhythm == "gahu":
            return {
                "bell": "x . x x . x x x . x x x . x x",
                "rattle": "x . x . x . x . x . x . x . x",
            }
        else:
            return {}

    def create_middle_eastern(
        self,
        style: Literal["baladi", "saidi", "khaliji"] = "baladi",
    ) -> dict[str, str]:
        """Create Middle Eastern percussion ensemble."""
        if style == "baladi":
            return {
                "darbuka_doum": "x . . . x . . . x . . . x .",
                "darbuka_tek": ". x . . . . . . . x . . . . x",
                "riq": "x x . x x x . x x x . x .",
            }
        elif style == "saidi":
            return {
                "darbuka_doum": "x . x . x . . . x . . . .",
                "darbuba_tek": ". x . . . . . . . x . . .",
                "riq": "x . x . x . x . x . x . x",
            }
        else:  # khaliji
            return {
                "darbuka_doum": "x . . . x . . . . . . . .",
                "darbuka_tek": ". x . x . . . . x . . . . x",
            }


__all__ = [
    # Afro-Cuban
    "ClavePattern",
    "SON_CLAVE",
    "RUMBA_CLAVE",
    "BOSSA_NOVA_CLAVE",
    "CLAVE_PATTERNS",
    "TUMBAO_MODERN",
    "TUMBAO_TRADITIONAL",
    # Brazilian
    "SambaPattern",
    "SAMBA_escola",
    "SAMBA_ENREDO",
    "BossaNovaPattern",
    "BOSSA_NOVA",
    # Indian
    "Tala",
    "TEENTAL",
    "JHAPTAL",
    "RUPAK",
    "EKTAL",
    "DADRA",
    "ROOPAK",
    "TALAS",
    # West African
    "Polyrhythm",
    "CROSS_RHYTHM_3_2",
    "CROSS_RHYTHM_6_4",
    # Generators
    "PolyrhythmGenerator",
    "RhythmComposer",
]
