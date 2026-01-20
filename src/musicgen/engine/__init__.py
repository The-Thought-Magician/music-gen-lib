"""Base interfaces and genre rule registry."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from musicgen.core.note import Note

from musicgen.engine.composer import CompositionEngine, generate_from_yaml
from musicgen.engine.parser import (
    CompositionSpec,
    InstrumentSpec,
    OrnamentationSpec,
    SectionSpec,
)


# =============================================================================
# Genre Rule Interface
# =============================================================================


class GenreRule(ABC):
    """Base class for genre-specific composition rules.

    Each genre (indian_classical, jazz, rock, etc.) implements this interface
    to provide domain-specific music generation logic.
    """

    @property
    @abstractmethod
    def genre_name(self) -> str:
        """Return the genre name this rule handles."""

    @abstractmethod
    def generate_melody(
        self,
        spec: CompositionSpec,
        section: SectionSpec,
        instrument: InstrumentSpec,
    ) -> list[Note]:
        """Generate melody notes for a section.

        Args:
            spec: Full composition specification
            section: Section specification
            instrument: Instrument to generate notes for

        Returns:
            List of Note objects with timing, pitch, velocity
        """

    @abstractmethod
    def generate_rhythm(
        self,
        spec: CompositionSpec,
        section: SectionSpec,
        instrument: InstrumentSpec,
    ) -> list[Note]:
        """Generate rhythm notes for a section.

        Args:
            spec: Full composition specification
            section: Section specification
            instrument: Instrument to generate notes for

        Returns:
            List of Note objects with timing, pitch, velocity
        """

    def generate_drone(
        self,
        spec: CompositionSpec,
        instrument: InstrumentSpec,
    ) -> list[Note]:
        """Generate continuous drone notes.

        Args:
            spec: Full composition specification
            instrument: Drone instrument specification

        Returns:
            List of overlapping notes creating continuous drone
        """
        if instrument.role != "drone":
            return []

        notes = []
        start_time = 0.0

        for drone_note in instrument.drone_notes or []:
            # Create overlapping notes for continuous drone
            # Duration is composition duration minus small offset for overlap
            duration = spec.duration_seconds - start_time + drone_note.start_offset

            # Parse note name to get pitch and octave
            note_name = drone_note.note
            # Assuming format like "C4" - note + octave
            if len(note_name) >= 2:
                note_char = note_name[0]
                octave = int(note_name[-1])
            else:
                note_char = note_name[0]
                octave = 4

            from musicgen.core.note import Note as CoreNote
            core_note = CoreNote(note_char, octave=octave)

            notes.append(Note(
                core_note.name,
                core_note.octave,
                duration,
                drone_note.velocity,
            ))
            notes[-1].start_time = start_time

            # Start next note slightly before this one ends for overlap
            start_time += duration - 0.1

        return notes

    def apply_ornamentation(
        self,
        notes: list[Note],
        spec: CompositionSpec,
        instrument: InstrumentSpec,
    ) -> list[Note]:
        """Apply ornamentation to melody notes.

        Args:
            notes: Base melody notes
            spec: Full composition specification
            instrument: Instrument specification

        Returns:
            List of notes with added ornamentation (grace notes, pitch bends, CC events)
        """
        # Base implementation returns notes unchanged
        return notes


class GenreRuleRegistry:
    """Registry for genre-specific composition rules."""

    _rules: dict[str, type[GenreRule]] = {}

    @classmethod
    def register(cls, rule: type[GenreRule]) -> None:
        """Register a genre rule."""
        instance = rule()
        cls._rules[instance.genre_name] = instance

    @classmethod
    def get(cls, genre: str) -> GenreRule:
        """Get a genre rule by name."""
        rule = cls._rules.get(genre)
        if rule is None:
            raise ValueError(f"No rule registered for genre: {genre}")
        return rule

    @classmethod
    def list_genres(cls) -> list[str]:
        """List all available genres."""
        return list(cls._rules.keys())


# =============================================================================
# Import all genre rules
# =============================================================================

# Import and register genre rules when they exist
try:
    from musicgen.engine.rules.indian import IndianClassicalRule
    GenreRuleRegistry.register(IndianClassicalRule)
except ImportError:
    pass

try:
    from musicgen.engine.rules.jazz import JazzRule
    GenreRuleRegistry.register(JazzRule)
except ImportError:
    pass

try:
    from musicgen.engine.rules.rock import RockRule
    GenreRuleRegistry.register(RockRule)
except ImportError:
    pass

try:
    from musicgen.engine.rules.electronic import ElectronicRule
    GenreRuleRegistry.register(ElectronicRule)
except ImportError:
    pass

try:
    from musicgen.engine.rules.classical import ClassicalRule
    GenreRuleRegistry.register(ClassicalRule)
except ImportError:
    pass
