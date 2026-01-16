"""V3 Instrument part models.

These models represent individual instrument parts in a composition,
including all notes, keyswitches, CC events, and metadata.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from musicgen.ai_models.v3.articulation import ArticulationType, KeyswitchEvent
from musicgen.ai_models.v3.notes import CCEvent, Note, PitchBendEvent, ProgramChangeEvent


# Type aliases for instrument family and clef
InstrumentFamily = Literal[
    "strings",
    "woodwinds",
    "brass",
    "percussion",
    "keyboards",
    "electronic",
    "voices",
]

Clef = Literal[
    "treble",
    "bass",
    "alto",
    "tenor",
    "grand_staff",
    "percussion",
]


class InstrumentPart(BaseModel):
    """A single instrument's part in the composition.

    Contains all notes, keyswitches, CC events, and metadata for one
    instrument in the composition.
    """

    # Identification
    instrument_name: str = Field(
        description="Name of the instrument (e.g., 'Violin Section')"
    )
    instrument_family: InstrumentFamily = Field(
        description="Instrument family"
    )
    midi_program: int | None = Field(
        default=None,
        ge=0,
        le=127,
        description="MIDI program number (0-127)"
    )
    midi_channel: int = Field(
        ge=0,
        le=15,
        description="MIDI channel (0-15)"
    )

    # Notation
    clef: Clef = Field(
        default="treble",
        description="Default clef for this part"
    )
    transposition: int = Field(
        default=0,
        description="Semitones to transpose (for transposing instruments)"
    )

    # Events
    notes: list[Note] = Field(
        default_factory=list,
        description="Notes in this part"
    )
    keyswitches: list[KeyswitchEvent] = Field(
        default_factory=list,
        description="Keyswitch events for articulation changes"
    )
    cc_events: list[CCEvent] = Field(
        default_factory=list,
        description="Continuous controller events"
    )
    pitch_bends: list[PitchBendEvent] = Field(
        default_factory=list,
        description="Pitch bend events"
    )
    program_changes: list[ProgramChangeEvent] = Field(
        default_factory=list,
        description="Program change events"
    )

    # Part metadata
    solo: bool = Field(
        default=False,
        description="Is this a solo part?"
    )
    muted: bool = Field(
        default=False,
        description="Should this part be muted?"
    )

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, notes: list[Note]) -> list[Note]:
        """Ensure notes are sorted by start time."""
        if notes:
            sorted_notes = sorted(notes, key=lambda n: n.start_time)
            if notes != sorted_notes:
                raise ValueError("Notes must be sorted by start_time")
        return notes

    def get_duration(self) -> float:
        """Get the total duration of this part in seconds."""
        if not self.notes:
            return 0.0
        return max(n.start_time + n.duration for n in self.notes)

    def note_count(self) -> int:
        """Get the number of notes in this part."""
        return len(self.notes)
