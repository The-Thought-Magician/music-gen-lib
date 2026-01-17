"""
Guitar fretboard model for position calculation and string assignment.

This module provides the fretboard model for calculating playing positions
on guitar and bass instruments.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    pass

# Note names for MIDI conversion
NOTE_NAMES: list[str] = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
]

# Note to MIDI number conversion
NOTE_TO_MIDI: dict[str, int] = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
}


def note_to_midi(note: str) -> int:
    """Convert note name to MIDI number (C4 = 60)."""
    # Parse note like "C4", "F#3", "Bb2"
    if len(note) < 2:
        raise ValueError(f"Invalid note name: {note}")

    # Find the octave (last character(s))
    octave_str = ""
    for i in range(len(note) - 1, -1, -1):
        if note[i].isdigit():
            octave_str = note[i] + octave_str
        else:
            break

    if not octave_str:
        raise ValueError(f"No octave in note: {note}")

    octave = int(octave_str)
    note_name = note[: len(note) - len(octave_str)]

    note_num = NOTE_TO_MIDI.get(note_name)
    if note_num is None:
        raise ValueError(f"Unknown note name: {note_name}")

    return note_num + (octave + 1) * 12


def midi_to_note(midi: int) -> str:
    """Convert MIDI number to note name."""
    note_num = midi % 12
    octave = (midi // 12) - 1
    note_name = NOTE_NAMES[note_num]
    return f"{note_name}{octave}"


@dataclass
class FretboardPosition:
    """A position on the fretboard."""

    string: int  # 1-6, 1=highest pitch string
    fret: int  # 0=open, 1-24=fret number
    midi_note: int
    note_name: str

    def __str__(self) -> str:
        if self.fret == 0:
            return f"{self.note_name} (string {self.string}, open)"
        return f"{self.note_name} (string {self.string}, fret {self.fret})"


@dataclass
class Fretboard:
    """
    Guitar fretboard model for position calculation.

    Attributes:
        tuning: List of open string notes (low to high)
        fret_count: Number of frets
        string_count: Number of strings
    """

    tuning: list[str]
    fret_count: int = 24
    string_count: int = 6

    def __post_init__(self) -> None:
        """Calculate MIDI notes for open strings."""
        self.open_string_midi: list[int] = [note_to_midi(note) for note in self.tuning]

    def find_positions(self, note: str) -> list[FretboardPosition]:
        """
        Find all (string, fret) positions for a given note.

        Args:
            note: Note name (e.g., "C4", "F#3")

        Returns:
            List of FretboardPosition objects
        """
        target_midi = note_to_midi(note)
        positions: list[FretboardPosition] = []

        for string_num, open_midi in enumerate(self.open_string_midi, start=1):
            fret = target_midi - open_midi
            if 0 <= fret <= self.fret_count:
                positions.append(
                    FretboardPosition(
                        string=string_num,
                        fret=fret,
                        midi_note=target_midi,
                        note_name=note,
                    )
                )

        return positions

    def find_optimal_position(
        self,
        note: str,
        previous_position: FretboardPosition | None = None,
        prefer_high_strings: bool = False,
        max_fret_span: int = 4,  # Reserved for future use  # noqa: ARG002
    ) -> FretboardPosition | None:
        """
        Find best position considering hand movement.

        Args:
            note: Note name to find position for
            previous_position: Previous position played
            prefer_high_strings: Prefer higher strings for melody
            max_fret_span: Maximum fret distance from previous position

        Returns:
            Best FretboardPosition or None if note not playable
        """
        positions = self.find_positions(note)
        if not positions:
            return None

        if previous_position is None:
            # No previous position, prefer open or low fret positions
            positions.sort(key=lambda p: (p.fret, p.string if prefer_high_strings else -p.string))
            return positions[0]

        # Score each position based on distance from previous
        def score_position(pos: FretboardPosition) -> tuple[int, int, int]:
            fret_dist = abs(pos.fret - previous_position.fret)
            string_dist = abs(pos.string - previous_position.string)
            # Lower score is better
            return (fret_dist, string_dist, pos.fret)

        positions.sort(key=score_position)
        return positions[0]

    def calculate_stretch(self, positions: list[FretboardPosition]) -> int:
        """
        Calculate fret span for a set of positions (chord).

        Args:
            positions: List of positions to calculate span for

        Returns:
            Fret span (difference between min and max fret)
        """
        if not positions:
            return 0
        frets = [p.fret for p in positions if p.fret > 0]  # Exclude open strings
        if not frets:
            return 0
        return max(frets) - min(frets)

    def is_playable_chord(
        self,
        positions: list[FretboardPosition],
        max_fret_span: int = 4,
        min_string: int = 1,
        max_string: int = 6,
    ) -> bool:
        """
        Check if a set of positions forms a playable chord.

        Args:
            positions: List of positions for chord notes
            max_fret_span: Maximum fret distance
            min_string: Minimum string number to use
            max_string: Maximum string number to use

        Returns:
            True if chord is playable
        """
        if not positions:
            return False

        # Check string range
        strings = [p.string for p in positions]
        if min(strings) < min_string or max(strings) > max_string:
            return False

        # Check fret span
        return self.calculate_stretch(positions) <= max_fret_span


@dataclass
class GuitarStringAssigner:
    """Assign notes to strings for realistic guitar parts."""

    fretboard: Fretboard
    prefer_high_strings: bool = False
    max_fret_span: int = 4

    def assign_melody(
        self,
        notes: list[str],
        prefer_position: FretboardPosition | None = None,
    ) -> list[FretboardPosition]:
        """
        Assign melody notes to strings minimizing movement.

        Args:
            notes: List of note names to assign
            prefer_position: Starting position to prefer

        Returns:
            List of FretboardPosition objects
        """
        positions: list[FretboardPosition] = []
        prev_pos = prefer_position

        for note in notes:
            pos = self.fretboard.find_optimal_position(
                note,
                previous_position=prev_pos,
                prefer_high_strings=self.prefer_high_strings,
                max_fret_span=self.max_fret_span,
            )
            if pos:
                positions.append(pos)
                prev_pos = pos
            else:
                # Note not playable, skip
                continue

        return positions

    def assign_chord(
        self,
        chord_notes: list[str],
        voicing_type: Literal["open", "barre", "jazz", "power"] = "open",
    ) -> list[FretboardPosition]:
        """
        Assign chord notes to strings for specific voicing type.

        Args:
            chord_notes: List of note names in the chord
            voicing_type: Type of voicing to create

        Returns:
            List of FretboardPosition objects
        """
        # Get all possible positions for each note
        all_positions: dict[str, list[FretboardPosition]] = {}
        for note in chord_notes:
            all_positions[note] = self.fretboard.find_positions(note)

        # Find playable voicings
        voicings = self._find_playable_voicings(chord_notes, all_positions)

        if not voicings:
            return []

        # Sort by fret position and voicing preference
        voicings.sort(key=lambda v: (sum(p.fret for p in v), self._voicing_score(v, voicing_type)))

        return voicings[0]

    def _find_playable_voicings(
        self,
        chord_notes: list[str],
        all_positions: dict[str, list[FretboardPosition]],
    ) -> list[list[FretboardPosition]]:
        """Find all physically playable voicings for a chord."""
        voicings: list[list[FretboardPosition]] = []

        # This is a simplified approach - try combinations of positions
        # A more sophisticated version would use backtracking
        for note in chord_notes:
            if note not in all_positions or not all_positions[note]:
                continue
            for pos in all_positions[note]:
                # Check if we can add this position to existing voicings
                added = False
                for voicing in voicings:
                    # Check if this note is already in voicing
                    if any(v.note_name == pos.note_name for v in voicing):
                        continue
                    # Check if position is on a different string
                    if any(v.string == pos.string for v in voicing):
                        continue
                    # Check fret span
                    temp_voicing = voicing + [pos]
                    if self.fretboard.is_playable_chord(temp_voicing, self.max_fret_span):
                        voicing.append(pos)
                        added = True
                        break
                if not added and self.fretboard.is_playable_chord([pos], self.max_fret_span):
                    # Start new voicing
                    voicings.append([pos])

        # Filter to complete voicings with all notes
        complete = [v for v in voicings if len(v) >= len(chord_notes)]

        return complete if complete else voicings

    def _voicing_score(
        self,
        voicing: list[FretboardPosition],
        voicing_type: str,
    ) -> int:
        """Score a voicing for compatibility with type."""
        score = 0

        if voicing_type == "open":
            # Prefer open strings and low frets
            if any(p.fret == 0 for p in voicing):
                score -= 10
            score += sum(p.fret for p in voicing)

        elif voicing_type == "barre":
            # Prefer positions on same fret
            frets = [p.fret for p in voicing if p.fret > 0]
            if frets and len(set(frets)) <= 2:
                score -= 10
            score += sum(p.fret for p in voicing)

        elif voicing_type == "jazz":
            # Prefer higher positions
            avg_fret = sum(p.fret for p in voicing) / len(voicing) if voicing else 0
            if avg_fret >= 5:
                score -= 10
            else:
                score += int(avg_fret)

        elif voicing_type == "power":
            # Prefer root and fifth on low strings
            if voicing and voicing[0].string >= 4:
                score -= 5

        return score


# Standard fretboards
STANDARD_GUITAR: Fretboard = Fretboard(
    tuning=["E2", "A2", "D3", "G3", "B3", "E4"],
    fret_count=24,
    string_count=6,
)

DROP_D_GUITAR: Fretboard = Fretboard(
    tuning=["D2", "A2", "D3", "G3", "B3", "E4"],
    fret_count=24,
    string_count=6,
)

OPEN_D_GUITAR: Fretboard = Fretboard(
    tuning=["D2", "A2", "D3", "F#3", "A3", "D4"],
    fret_count=24,
    string_count=6,
)

STANDARD_BASS_4: Fretboard = Fretboard(
    tuning=["E1", "A1", "D2", "G2"],
    fret_count=24,
    string_count=4,
)

STANDARD_BASS_5: Fretboard = Fretboard(
    tuning=["B0", "E1", "A1", "D2", "G2"],
    fret_count=24,
    string_count=5,
)


__all__ = [
    "FretboardPosition",
    "Fretboard",
    "GuitarStringAssigner",
    "note_to_midi",
    "midi_to_note",
    "STANDARD_GUITAR",
    "DROP_D_GUITAR",
    "OPEN_D_GUITAR",
    "STANDARD_BASS_4",
    "STANDARD_BASS_5",
]
