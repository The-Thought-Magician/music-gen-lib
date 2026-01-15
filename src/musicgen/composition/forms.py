"""Musical form structures.

This module provides classes for representing and generating
common musical forms.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from musicgen.composition.melody import Melody
from musicgen.theory.keys import Key


class FormType(Enum):
    """Types of musical forms."""

    BINARY = "binary"           # AB form
    TERNARY = "ternary"         # ABA form
    RONDO = "rondo"             # ABACA or similar
    SONATA = "sonata"           # Exposition-Development-Recapitulation
    STROPHIC = "strophic"       # Same section repeated
    THROUGH_COMPOSED = "through_composed"  # Continuous, no repetition


@dataclass
class Section:
    """A section of a musical form.

    Attributes:
        name: Section identifier (e.g., "A", "B", "exposition")
        melodies: List of melodies in this section
        key: The key for this section
        length: Number of measures
    """

    name: str
    melodies: list[Melody] = field(default_factory=list)
    key: Key | None = None
    length: int = 8

    @property
    def total_events(self) -> int:
        """Return total number of note events."""
        return sum(m.length for m in self.melodies)

    @property
    def total_duration(self) -> float:
        """Return total duration in quarter notes."""
        return sum(m.total_duration for m in self.melodies)

    def add_melody(self, melody: Melody) -> None:
        """Add a melody to this section.

        Args:
            melody: Melody to add
        """
        self.melodies.append(melody)

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Section({self.name}, {len(self.melodies)} melodies)"


@dataclass
class Form:
    """Represents a complete musical form.

    Attributes:
        form_type: The type of form
        sections: List of sections in order
        key: The home key
    """

    form_type: FormType
    sections: list[Section] = field(default_factory=list)
    key: Key | None = None

    @property
    def length(self) -> int:
        """Return number of sections."""
        return len(self.sections)

    @property
    def total_measures(self) -> int:
        """Return total number of measures."""
        return sum(s.length for s in self.sections)

    def add_section(self, section: Section) -> None:
        """Add a section to the form.

        Args:
            section: Section to add
        """
        self.sections.append(section)

    def get_section(self, name: str) -> Section | None:
        """Get a section by name.

        Args:
            name: Section name to find

        Returns:
            Section or None
        """
        for section in self.sections:
            if section.name == name:
                return section
        return None

    @classmethod
    def binary(cls, section_a: Section, section_b: Section,
               key: Key | None = None) -> Form:
        """Create a binary form (AB).

        Args:
            section_a: First section
            section_b: Second section
            key: Home key

        Returns:
            A new Form
        """
        section_a.name = "A"
        section_b.name = "B"
        return cls(
            form_type=FormType.BINARY,
            sections=[section_a, section_b],
            key=key
        )

    @classmethod
    def ternary(cls, section_a: Section, section_b: Section,
                key: Key | None = None) -> Form:
        """Create a ternary form (ABA).

        Args:
            section_a: A section (will be repeated)
            section_b: B section (contrasting)
            key: Home key

        Returns:
            A new Form
        """
        section_a.name = "A"
        section_b.name = "B"

        # Create return of A
        from copy import deepcopy
        a_return = deepcopy(section_a)

        return cls(
            form_type=FormType.TERNARY,
            sections=[section_a, section_b, a_return],
            key=key
        )

    @classmethod
    def rondo(cls, theme: Section, episodes: list[Section],
              key: Key | None = None) -> Form:
        """Create a rondo form (ABACA...).

        Args:
            theme: The recurring theme (A section)
            episodes: Contrasting sections (B, C, etc.)
            key: Home key

        Returns:
            A new Form
        """
        theme.name = "A"
        sections = [theme]

        for i, episode in enumerate(episodes):
            episode.name = chr(66 + i)  # B, C, D, etc.
            sections.append(episode)
            sections.append(theme)  # Return to theme after each episode

        return cls(
            form_type=FormType.RONDO,
            sections=sections,
            key=key
        )

    @classmethod
    def sonata(cls, exposition: Section, development: Section,
               recapitulation: Section, key: Key | None = None) -> Form:
        """Create a sonata form.

        Args:
            exposition: Exposition section
            development: Development section
            recapitulation: Recapitulation section
            key: Home key

        Returns:
            A new Form
        """
        exposition.name = "exposition"
        development.name = "development"
        recapitulation.name = "recapitulation"

        return cls(
            form_type=FormType.SONATA,
            sections=[exposition, development, recapitulation],
            key=key
        )

    def __repr__(self) -> str:
        """Return string representation."""
        section_names = [s.name for s in self.sections]
        return f"Form({self.form_type.value}, {'-'.join(section_names)})"

    def __iter__(self):
        """Allow iteration over sections."""
        return iter(self.sections)

    def __len__(self) -> int:
        """Return length."""
        return len(self.sections)
