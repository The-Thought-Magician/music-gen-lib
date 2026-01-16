"""V3 Articulation models for SFZ-based rendering.

These models define articulation types and keyswitch events for orchestral
instruments, enabling the AI to specify playing techniques like legato,
staccato, pizzicato, etc.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ArticulationType(str, Enum):
    """Types of articulations for orchestral instruments.

    These define how a note is played, which dramatically changes the
    character of the sound in SFZ libraries.
    """

    # Strings
    LEGATO = "legato"
    DETACHE = "detache"
    STACCATO = "staccato"
    SPICCATO = "spiccato"
    MARCATO = "marcato"
    PIZZICATO = "pizzicato"
    TREMOLO = "tremolo"
    TRILL = "trill"
    SUL_TASTO = "sul_tasto"
    SUL_PONTICELLO = "sul_ponticello"
    COL_LEGNO = "col_legno"
    HARMONIC = "harmonic"
    VIBRATO = "vibrato"
    SENZA_VIBRATO = "senza_vibrato"

    # Woodwinds
    FLUTTER_TONGUE = "flutter_tongue"
    FLUTTER_WW = "flutter_ww"
    STACCATO_WW = "staccato_ww"
    LEGATO_WW = "legato_ww"
    BREATH_ATTACK = "breath_attack"

    # Brass
    MARTELLO = "martello"
    STACCATO_BRASS = "staccato_brass"
    LEGATO_BRASS = "legato_brass"
    MUTED = "muted"
    FALL = "fall"
    DOIT = "doit"
    SHAKE = "shake"
    FLIP = "flip"
    SMEAR = "smear"
    HALF_VALVE = "half_valve"

    # General/Unaccented
    NORMAL = "normal"
    ACCENT = "accent"
    MARCATO_SHORT = "marcato_short"
    TENUTO = "tenuto"
    SFORZANDO = "sforzando"
    SFP = "sforzando_piano"
    FP = "forte_piano"
    RINFORZANDO = "rinforzando"


class KeyswitchEvent(BaseModel):
    """A keyswitch event in the MIDI timeline.

    Keyswitches are MIDI notes sent before the notes they affect to
    change the articulation in SFZ libraries. They typically live in
    a low range (C0-C2) outside the instrument's playing range.
    """

    keyswitch: int = Field(
        ge=0,
        le=127,
        description="MIDI note number for keyswitch (typically 0-31)"
    )
    time: float = Field(
        ge=0,
        description="Time in seconds when keyswitch should be sent"
    )
    articulation: ArticulationType = Field(
        description="The articulation this keyswitch activates"
    )
    channel: int = Field(
        default=0,
        ge=0,
        le=15,
        description="MIDI channel for this keyswitch"
    )


class ArticulationDefinition(BaseModel):
    """Definition of an articulation for an instrument.

    Provides metadata about how an articulation affects note playback.
    """

    name: str = Field(description="Display name of the articulation")
    type: ArticulationType = Field(description="Type of articulation")
    keyswitch: int | None = Field(
        default=None,
        ge=0,
        le=127,
        description="MIDI keyswitch note (0-31 typically)"
    )
    duration_multiplier: float = Field(
        default=1.0,
        gt=0,
        description="Duration modifier (1.0 = no change, 0.5 = half duration)"
    )
    velocity_multiplier: float = Field(
        default=1.0,
        gt=0,
        description="Velocity modifier (1.0 = no change, 1.2 = louder)"
    )
    cc_messages: dict[int, int] = Field(
        default_factory=dict,
        description="CC messages for this articulation (cc_number -> value)"
    )
    description: str = Field(
        default="",
        description="Human-readable description of this articulation"
    )
    usage_context: str = Field(
        default="",
        description="When to use this articulation (AI guidance)"
    )


# Default duration multipliers by articulation
DEFAULT_DURATION_MULTIPLIERS: dict[ArticulationType, float] = {
    ArticulationType.LEGATO: 1.0,
    ArticulationType.DETACHE: 0.85,
    ArticulationType.STACCATO: 0.4,
    ArticulationType.SPICCATO: 0.3,
    ArticulationType.MARCATO: 0.7,
    ArticulationType.PIZZICATO: 0.25,
    ArticulationType.TREMOLO: 1.0,
    ArticulationType.SUL_PONTICELLO: 1.0,
    ArticulationType.COL_LEGNO: 0.5,
    ArticulationType.STACCATO_WW: 0.35,
    ArticulationType.STACCATO_BRASS: 0.35,
}


# Default velocity multipliers by articulation
DEFAULT_VELOCITY_MULTIPLIERS: dict[ArticulationType, float] = {
    ArticulationType.LEGATO: 0.95,
    ArticulationType.DETACHE: 1.0,
    ArticulationType.STACCATO: 1.15,
    ArticulationType.SPICCATO: 1.1,
    ArticulationType.MARCATO: 1.2,
    ArticulationType.PIZZICATO: 1.2,
    ArticulationType.TREMOLO: 0.85,
    ArticulationType.ACCENT: 1.3,
    ArticulationType.SFORZANDO: 1.4,
    ArticulationType.FP: 1.3,
}
