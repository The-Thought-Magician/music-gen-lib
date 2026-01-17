"""AI-generated section models for long compositions."""

from __future__ import annotations

from pydantic import BaseModel, Field

from musicgen.ai_models.composition import KeySignature
from musicgen.ai_models.notes import AINote


class AISection(BaseModel):
    """A section of a composition (e.g., "A", "B", "bridge", "chorus")."""

    name: str = Field(..., description="Section name (A, B, bridge, chorus, etc.)")
    start_bar: int = Field(..., ge=1, description="Starting bar number (1-indexed)")
    end_bar: int = Field(..., ge=1, description="Ending bar number (1-indexed)")

    # Optional musical attributes
    key: KeySignature | None = Field(None, description="Key for this section")
    tempo: int | None = Field(None, ge=20, le=300, description="Tempo for this section (BPM)")
    mood: str | None = Field(None, description="Mood description for this section")

    # Parts for this section only
    parts: dict[str, list[AINote | dict]] = Field(
        default_factory=dict,
        description="Part name -> notes in this section"
    )

    # Transition to next section
    transition: str | None = Field(
        None,
        description="How this section leads to the next (e.g., 'fade_out', 'ritardando', 'direct')"
    )

    @property
    def length_bars(self) -> int:
        """Get the length of this section in bars."""
        return self.end_bar - self.start_bar + 1

    @property
    def length_quarters(self) -> float:
        """Get the length of this section in quarter notes (assuming 4/4)."""
        # This is a rough approximation - actual length depends on time signature
        return self.length_bars * 4.0
