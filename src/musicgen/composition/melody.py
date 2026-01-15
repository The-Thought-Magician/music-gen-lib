"""Melody generation classes.

This module provides classes for generating melodies with various
contours and motivic development techniques.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from musicgen.core.note import EIGHTH, HALF, QUARTER, Note, Rest
from musicgen.theory.keys import Key
from musicgen.theory.scales import Scale


class MelodicContour(Enum):
    """Types of melodic contours."""

    ASCENDING = "ascending"          # Overall upward motion
    DESCENDING = "descending"        # Overall downward motion
    ARCH = "arch"                    # Rise then fall
    INVERTED_ARCH = "inverted_arch"  # Fall then rise
    WAVE = "wave"                    # Alternating up and down
    STATIC = "static"                # Limited pitch range


@dataclass
class Motif:
    """A short melodic idea that can be developed.

    Attributes:
        notes: List of notes in the motif
        contour: The melodic contour type
    """

    notes: list[Note | Rest] = field(default_factory=list)
    contour: MelodicContour = MelodicContour.STATIC

    @property
    def length(self) -> int:
        """Return the number of notes."""
        return len([n for n in self.notes if isinstance(n, Note)])

    @property
    def total_duration(self) -> float:
        """Return total duration in quarter notes."""
        return sum(n.duration for n in self.notes)

    @property
    def range(self) -> int:
        """Return pitch range in semitones."""
        note_list = [n for n in self.notes if isinstance(n, Note)]
        if not note_list:
            return 0
        midi_nums = [n.midi_number for n in note_list]
        return max(midi_nums) - min(midi_nums)

    def develop(self, technique: str, **kwargs) -> Motif:
        """Create a developed version of this motif.

        Args:
            technique: Development technique ("sequence", "inversion",
                       "retrograde", "augmentation", "diminution")
            **kwargs: Additional arguments for the technique

        Returns:
            A new Motif with the development applied
        """
        new_notes = []

        if technique == "sequence":
            interval = kwargs.get("interval", 5)
            for n in self.notes:
                if isinstance(n, Note):
                    new_notes.append(n.transpose(interval))
                else:
                    new_notes.append(n)

        elif technique == "inversion":
            # Mirror intervals around a central pitch
            note_list = [n for n in self.notes if isinstance(n, Note)]
            if note_list:
                center = sum(n.midi_number for n in note_list) / len(note_list)
                for n in self.notes:
                    if isinstance(n, Note):
                        diff = n.midi_number - center
                        new_midi = int(center - diff)
                        new_note = Note.from_midi(new_midi, n.duration, n.velocity)
                        new_notes.append(new_note)
                    else:
                        new_notes.append(n)

        elif technique == "retrograde":
            new_notes = list(reversed(self.notes))

        elif technique == "augmentation":
            for n in self.notes:
                if isinstance(n, Note):
                    new_note = Note(n.name, n.octave, n.duration * 2, n.velocity,
                                    n.accidental, n.tied, n.articulation)
                    new_notes.append(new_note)
                else:
                    n.duration *= 2
                    new_notes.append(n)

        elif technique == "diminution":
            for n in self.notes:
                if isinstance(n, Note):
                    new_note = Note(n.name, n.octave, n.duration / 2, n.velocity,
                                    n.accidental, n.tied, n.articulation)
                    new_notes.append(new_note)
                else:
                    n.duration /= 2
                    new_notes.append(n)

        else:
            new_notes = self.notes.copy()

        return Motif(notes=new_notes, contour=self.contour)

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Motif({len(self.notes)} events, {self.contour.value})"


@dataclass
class Phrase:
    """A musical phrase, typically 4-8 measures.

    Attributes:
        notes: List of notes in the phrase
        phrase_type: Type of phrase ("antecedent", "consequent", "standalone")
        cadence: Type of cadence ("authentic", "half", "deceptive", "plagal", "none")
    """

    notes: list[Note | Rest] = field(default_factory=list)
    phrase_type: str = "standalone"
    cadence: str = "none"

    @property
    def length(self) -> int:
        """Return the number of notes."""
        return len([n for n in self.notes if isinstance(n, Note)])

    @property
    def total_duration(self) -> float:
        """Return total duration in quarter notes."""
        return sum(n.duration for n in self.notes)

    def is_period_partner(self, other: Phrase) -> bool:
        """Check if this phrase forms a period with another.

        Args:
            other: Another phrase to check

        Returns:
            True if they form a proper period
        """
        # Simple check: antecedent + consequent with proper cadences
        return (self.phrase_type == "antecedent" and
                other.phrase_type == "consequent" and
                self.cadence in ["half", "none"] and
                other.cadence in ["authentic", "plagal"])

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Phrase({len(self.notes)} events, {self.cadence} cadence)"


@dataclass
class Melody:
    """A complete melody consisting of notes and phrases.

    Attributes:
        notes: List of notes in the melody
        phrases: List of phrases (optional)
    """

    notes: list[Note | Rest] = field(default_factory=list)
    phrases: list[Phrase] = field(default_factory=list)

    @property
    def length(self) -> int:
        """Return the number of notes."""
        return len([n for n in self.notes if isinstance(n, Note)])

    @property
    def total_duration(self) -> float:
        """Return total duration in quarter notes."""
        return sum(n.duration for n in self.notes)

    @property
    def range(self) -> int:
        """Return pitch range in semitones."""
        note_list = [n for n in self.notes if isinstance(n, Note)]
        if not note_list:
            return 0
        midi_nums = [n.midi_number for n in note_list]
        return max(midi_nums) - min(midi_nums)

    def add_note(self, note: Note | Rest) -> None:
        """Add a note or rest to the melody.

        Args:
            note: Note or Rest to add
        """
        self.notes.append(note)

    def extend(self, other: Melody) -> None:
        """Extend this melody with another.

        Args:
            other: Melody to append
        """
        self.notes.extend(other.notes)

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Melody({len(self.notes)} events, {self.total_duration} quarters)"

    def __iter__(self):
        """Allow iteration over notes."""
        return iter(self.notes)

    def __len__(self) -> int:
        """Return length."""
        return len(self.notes)


@dataclass
class MelodyGenerator:
    """Generates melodies using rule-based composition.

    Attributes:
        scale: The scale to use for note selection
        key: The key for the melody
        tempo: Tempo in BPM
        seed: Random seed for reproducibility
    """

    scale: Scale
    key: Key
    tempo: int = 120
    seed: int | None = None

    def __post_init__(self):
        """Initialize the generator."""
        if self.seed is not None:
            random.seed(self.seed)

    def set_seed(self, seed: int) -> None:
        """Set the random seed.

        Args:
            seed: Seed value
        """
        self.seed = seed
        random.seed(seed)

    def generate_motif(self, length: int = 8,
                       contour: MelodicContour = MelodicContour.WAVE) -> Motif:
        """Generate a melodic motif.

        Args:
            length: Number of notes
            contour: Melodic contour to use

        Returns:
            A new Motif
        """
        notes = []
        current_note = self.scale.get_degree(1)
        current_note.duration = QUARTER
        notes.append(current_note)

        # Direction based on contour
        if contour == MelodicContour.ASCENDING:
            direction = 1
        elif contour == MelodicContour.DESCENDING:
            direction = -1
        elif contour == MelodicContour.ARCH:
            direction = 1
        elif contour == MelodicContour.INVERTED_ARCH:
            direction = -1
        else:
            direction = 0

        for i in range(1, length):
            # Change direction at midpoint for arch contours
            if contour == MelodicContour.ARCH and i > length // 2:
                direction = -1
            elif contour == MelodicContour.INVERTED_ARCH and i > length // 2:
                direction = 1
            elif contour == MelodicContour.WAVE:
                direction = 1 if direction <= 0 else -1

            # Choose next degree
            degree_step = random.randint(-2, 2) + direction
            next_degree = max(1, min(len(self.scale.notes),
                                     (i % len(self.scale.notes)) + 1 + degree_step))

            next_note = self.scale.get_degree(next_degree)
            next_note.duration = random.choice([QUARTER, QUARTER, EIGHTH, HALF])
            notes.append(next_note)

        return Motif(notes=notes, contour=contour)

    def generate_phrase(self, length: int = 16,
                        progression: Optional = None,  # noqa: ARG002
                        phrase_type: str = "standalone",
                        cadence: str = "none") -> Phrase:
        """Generate a musical phrase.

        Args:
            length: Number of notes
            progression: Chord progression to follow
            phrase_type: Type of phrase
            cadence: Type of cadence

        Returns:
            A new Phrase
        """
        notes = []

        for _i in range(length):
            # Generate note from scale
            degree = random.randint(1, len(self.scale.notes))
            note = self.scale.get_degree(degree)
            note.duration = random.choice([QUARTER, QUARTER, EIGHTH])
            notes.append(note)

        return Phrase(notes=notes, phrase_type=phrase_type, cadence=cadence)

    def generate_melody(self, progression: Optional = None,  # noqa: ARG002
                        contour: MelodicContour = MelodicContour.WAVE,
                        form_structure: str = "binary",
                        motivic_unity: float = 0.7) -> Melody:
        """Generate a complete melody.

        Args:
            progression: Chord progression to follow
            contour: Overall melodic contour
            form_structure: Form structure ("binary", "ternary", "period")
            motivic_unity: How much to reuse motifs (0-1)

        Returns:
            A new Melody
        """
        melody = Melody()

        # Generate initial motif
        motif_length = random.randint(6, 10)
        motif = self.generate_motif(motif_length, contour)
        melody.notes.extend(motif.notes)

        # Develop based on motivic unity
        if random.random() < motivic_unity:
            # Use developed motif
            techniques = ["sequence", "inversion", "retrograde"]
            technique = random.choice(techniques)
            developed = motif.develop(technique, interval=5 if technique == "sequence" else None)
            melody.notes.extend(developed.notes)
        else:
            # Generate new contrasting material
            new_motif = self.generate_motif(motif_length, contour)
            melody.notes.extend(new_motif.notes)

        # Add cadence
        if form_structure == "period":
            # Add consequent phrase
            consequent = self.generate_phrase(
                length=8,
                phrase_type="consequent",
                cadence="authentic"
            )
            melody.notes.extend(consequent.notes)

        return melody

    def __repr__(self) -> str:
        """Return string representation."""
        return f"MelodyGenerator({self.scale}, {self.tempo} BPM)"
