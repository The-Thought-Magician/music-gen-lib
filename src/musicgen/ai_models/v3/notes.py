"""V3 Note and event models for composition.

These models represent individual notes, continuous controller events,
pitch bends, and other MIDI events with full SFZ rendering support.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from musicgen.ai_models.v3.articulation import (
    ArticulationType,
    DEFAULT_DURATION_MULTIPLIERS,
    DEFAULT_VELOCITY_MULTIPLIERS,
)


class Note(BaseModel):
    """A single musical note with full rendering information.

    This represents a note event with all necessary information for
    MIDI generation and SFZ rendering.
    """

    # Pitch
    pitch: int = Field(
        ge=0,
        le=127,
        description="MIDI note number (0-127)"
    )

    # Timing (in seconds for V3, not quarter notes like V2)
    start_time: float = Field(
        ge=0,
        description="Start time in seconds from composition start"
    )
    duration: float = Field(
        gt=0,
        description="Duration in seconds (before articulation modification)"
    )

    # Velocity
    velocity: int = Field(
        ge=0,
        le=127,
        description="MIDI velocity (0-127)"
    )

    # Articulation
    articulation: ArticulationType | None = Field(
        default=None,
        description="Articulation to apply to this note"
    )

    # Expressive markings
    dynamic: str | None = Field(
        default=None,
        description="Dynamic marking (ppp, pp, p, mp, mf, f, ff, fff)"
    )

    # Ornamentation
    ornament: str | None = Field(
        default=None,
        description="Ornament (trill, mordent, turn, etc.)"
    )

    # Technical markings
    tie: bool = Field(
        default=False,
        description="Is this note tied to the next?"
    )
    slur: bool = Field(
        default=False,
        description="Is this note slurred?"
    )
    slur_group_id: int | None = Field(
        default=None,
        description="ID for grouping slurred notes"
    )

    # Extended techniques
    grace_notes: list[Note] | None = Field(
        default=None,
        description="Grace notes before this note"
    )

    @field_validator("pitch")
    @classmethod
    def validate_pitch(cls, v: int) -> int:
        """Ensure pitch is in valid MIDI range."""
        if not 0 <= v <= 127:
            raise ValueError(f"Pitch must be 0-127, got {v}")
        return v

    @field_validator("duration")
    @classmethod
    def validate_duration(cls, v: float) -> float:
        """Ensure duration is positive and reasonable."""
        if v <= 0:
            raise ValueError(f"Duration must be positive, got {v}")
        if v > 60:  # 1 minute per note is excessive
            raise ValueError(f"Duration too long: {v}s")
        return v

    def render_duration(self) -> float:
        """Get actual duration after articulation modification."""
        base = self.duration
        if self.articulation:
            mult = DEFAULT_DURATION_MULTIPLIERS.get(self.articulation, 1.0)
            return base * mult
        return base

    def render_velocity(self) -> int:
        """Get actual velocity after articulation modification."""
        base = self.velocity
        if self.articulation:
            mult = DEFAULT_VELOCITY_MULTIPLIERS.get(self.articulation, 1.0)
            vel = base * mult
            return max(0, min(127, int(vel)))
        return base


class CCEvent(BaseModel):
    """A continuous controller message.

    Used for expression, dynamics, vibrato, and other real-time controls.
    """

    controller: int = Field(
        ge=0,
        le=127,
        description="MIDI CC number"
    )
    value: int = Field(
        ge=0,
        le=127,
        description="CC value"
    )
    start_time: float = Field(
        ge=0,
        description="Start time in seconds"
    )
    duration: float | None = Field(
        default=None,
        description="Duration for ramped changes (None = instantaneous)"
    )
    channel: int = Field(
        default=0,
        ge=0,
        le=15,
        description="MIDI channel"
    )


# Common CC numbers
class CC:
    """MIDI Continuous Controller numbers."""

    # Bank and Program
    BANK_SELECT_MSB = 0
    BANK_SELECT_LSB = 32
    MODULATION = 1
    BREATH = 2
    FOOT = 4
    PORTAMENTO = 5
    DATA_ENTRY = 6
    VOLUME = 7
    PAN = 10
    EXPRESSION = 11
    SUSTAIN = 64
    SOSTENUTO = 66
    SOFT_PEDAL = 67
    HOLD_2 = 69
    HARMONIC_CONTENT = 71
    RELEASE_TIME = 72
    ATTACK_TIME = 73
    BRIGHTNESS = 74
    DECAY_TIME = 75
    VIBRATO_RATE = 76
    VIBRATO_DEPTH = 77
    VIBRATO_DELAY = 78


class PitchBendEvent(BaseModel):
    """A pitch bend message."""

    value: int = Field(
        ge=0,
        le=16383,
        description="Pitch bend value (0-16383, 8192=center)"
    )
    start_time: float = Field(
        ge=0,
        description="Time in seconds"
    )
    channel: int = Field(
        default=0,
        ge=0,
        le=15,
        description="MIDI channel"
    )


class ProgramChangeEvent(BaseModel):
    """A program change event."""

    program: int = Field(
        ge=0,
        le=127,
        description="MIDI program number"
    )
    time: float = Field(
        ge=0,
        description="Time in seconds"
    )
    channel: int = Field(
        default=0,
        ge=0,
        le=15,
        description="MIDI channel"
    )
