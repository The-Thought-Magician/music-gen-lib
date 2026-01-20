"""Raga database and raga-based note selection engine.

This module provides authentic Indian classical raga definitions including
ascending/descending patterns (aroha/avaroha), vadi/samvadi notes, and
characteristic phrases (pakad).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from musicgen.core.note import Note


# =============================================================================
# Indian Note Name Mapping
# =============================================================================

# Indian svaras to Western notes (assuming C as tonic/Sa)
# Lowercase = komal (flat), Uppercase = shuddha (natural)
# M with tik =tivra Ma (F#) - represented as M+
_INDIAN_NOTE_MAP = {
    # Shuddha (natural) notes
    "S": "C",   # Sa - tonic
    "R": "D",   # Re - second
    "G": "E",   # Ga - third
    "M": "F",   # Ma - fourth
    "P": "G",   # Pa - fifth
    "D": "A",   # Dha - sixth
    "N": "B",   # Ni - seventh
    # Komal (flat) notes
    "r": "Db",  # Komal Re
    "g": "Eb",  # Komal Ga
    "d": "Ab",  # Komal Dha
    "n": "Bb",  # Komal Ni
    # Tivra (sharp) Ma
    "M+": "F#", # Tivra Ma
}

# Octave markers
_OCTAVE_DOWN = "'"   # Indicates octave below (in Indian notation)
_OCTAVE_UP = "''"    # Indicates octave above


def indian_to_western(note_name: str, octave: int = 4) -> tuple[str, int]:
    """Convert Indian svara name to Western note name and octave.

    Args:
        note_name: Indian note name (S, R, g, M+, etc.)
        octave: Base octave (default 4)

    Returns:
        Tuple of (western_note_name, octave)
    """
    base_name = note_name

    # Handle octave markers
    if note_name.endswith("''"):
        base_name = note_name[:-2]
        octave += 1
    elif note_name.endswith("'"):
        base_name = note_name[:-1]
        octave += 1

    # Get the Western note name
    western_name = _INDIAN_NOTE_MAP.get(base_name, base_name)

    return western_name, octave


# =============================================================================
# Raga Definitions
# =============================================================================


@dataclass
class Raga:
    """Definition of an Indian classical raga."""

    name: str
    aroha: list[str]  # Ascending pattern (Indian note names)
    avaroha: list[str]  # Descending pattern
    vadi: int  # Most important note (MIDI number)
    samvadi: int  # Second most important note (MIDI number)
    that: int | None = None  # Note that creates the raga's character (optional)
    anga: str | None = None  # Prime time (morning, evening, etc.)
    saptak: list[int] | None = None  # All note MIDI numbers in the raga

    def get_allowed_notes(self) -> list[int]:
        """Get all MIDI note numbers in this raga."""
        if self.saptak:
            return self.saptak.copy()

        # Build from aroha using Indian note mapping
        saptak = []
        octave = 4  # Base octave

        for note_name in self.aroha + self.avaroha:
            western_name, note_octave = indian_to_western(note_name, octave)

            # Handle octave changes within the scale
            if "'" in note_name:
                note_octave += note_name.count("'")

            note = Note(western_name, octave=note_octave)
            midi_num = note.midi_number
            if midi_num not in saptak:
                saptak.append(midi_num)
        saptak.sort()
        return saptak

    def get_pakad(self) -> list[Note]:
        """Get characteristic phrase (pakad) for this raga.

        Returns a simple sequence of notes representing the pakad.
        """
        # Simple pakad representation - can be expanded
        if self.name.lower() == "yaman":
            return [
                Note.from_pitch_string("N4", duration=0.5),
                Note.from_pitch_string("R4", duration=0.5),
                Note.from_pitch_string("S4", duration=0.5),
            ]
        elif self.name.lower() == "bhairavi":
            return [
                Note.from_pitch_string("S4", duration=0.5),
                Note.from_pitch_string("R4", duration=0.5),
                Note.from_pitch_string("g4", duration=0.5),
                Note.from_pitch_string("M4", duration=0.5),
                Note.from_pitch_string("P4", duration=0.5),
                Note.from_pitch_string("S4", duration=0.5),
            ]
        # Add more ragas as needed
        return []

    def suggest_ornamentation_points(
        self,
        notes: list[Note]
    ) -> list[int]:
        """Suggest which notes should have ornamentation based on raga rules.

        Returns indices of notes that should receive ornamentation.
        """
        # Vadi note gets heavy ornamentation
        # Samvadi gets medium
        # That gets some
        if not notes:
            return []

        indices = []
        vadi_count = 0
        samvadi_count = 0
        that_count = 0

        for i, note in enumerate(notes):
            midi = note.midi_number

            if midi == self.vadi and vadi_count < 3:
                indices.append(i)
                vadi_count += 1
            elif midi == self.samvadi and samvadi_count < 2:
                indices.append(i)
                samvadi_count += 1
            elif self.that and midi == self.that and that_count < 1:
                indices.append(i)
                that_count += 1

        return indices


# =============================================================================
# Raga Database
# =============================================================================


_RAGA_DATABASE = {
    "yaman": Raga(
        name="Yaman",
        aroha=["S", "R", "G", "M", "P", "D", "N", "S'"],  # All shuddha
        avaroha=["S'", "N", "D", "P", "M", "G", "R", "S"],  # All shuddha
        vadi=67,  # G (Gandhar)
        samvadi=71,  # N (Nishad)
        that=None,
        anga="evening",
    ),
    "bhairavi": Raga(
        name="Bhairavi",
        aroha=["S", "r", "g", "M", "P", "d", "N", "S'"],
        avaroha=["S'", "N", "d", "P", "M", "g", "r", "S"],
        vadi=69,  # D (Dhaivat)
        samvadi=64,  # E (Ekar)
        that=62,  # G (Gandhar)
        anga="morning",
    ),
    "bhairav": Raga(
        name="Bhairav",
        aroha=["S", "r", "g", "M", "P", "d", "N", "S'"],
        avaroha=["S'", "N", "d", "P", "M", "g", "r", "S"],
        vadi=62,  # G (Gandhar)
        samvadi=67,  # G (Gandhar) - same note for Bhairav
        that=None,
        anga="morning",
    ),
    "bilaskhani": Raga(
        name="Bilaskhani",
        aroha=["S", "g", "M", "P", "D", "N", "S'"],
        avaroha=["S'", "N", "D", "P", "M", "g", "S"],
        vadi=62,  # G
        samvadi=71,  # N
        that=None,
        anga="late afternoon",
    ),
    "khamaj": Raga(
        name="Khamaj",
        aroha=["S", "g", "M", "P", "D", "N", "S'"],
        avaroha=["S'", "N", "D", "P", "M", "g", "S"],
        vadi=69,  # D
        samvadi=71,  # N
        that=74,  # A (Andolan)
        anga="late evening",
    ),
    "darbari": Raga(
        name="Darbari",
        aroha=["S", "R", "G", "M", "P", "D", "N", "S'"],
        avaroha=["S'", "N", "R", "G", "M", "P", "D", "N", "S'"],
        vadi=69,  # D (Dhaivat)
        samvadi=62,  # R (Rishabh)
        that=None,
        anga="late evening",
    ),
    "malkauns": Raga(
        name="Malkauns",
        aroha=["S", "g", "M", "P", "D", "N", "S'"],
        avaroha=["S'", "N", "D", "P", "M", "g", "S"],
        vadi=62,  # G
        samvadi=71,  # N
        that=None,
        anga="early morning",
    ),
    "bimpalasi": Raga(
        name="Bimpalasi",
        aroha=["S", "r", "g", "M", "P", "d", "N", "S'"],
        avaroha=["S'", "N", "d", "P", "M", "g", "r", "S"],
        vadi=69,  # D
        samvadi=67,  # G
        that=None,
        anga="late morning",
    ),
    "bageshree": Raga(
        name="Bageshree",
        aroha=["S", "r", "g", "M", "P", "d", "N", "S'"],
        avaroha=["S'", "N", "d", "P", "M", "g", "r", "S"],
        vadi=64,  # E
        samvadi=69,  # D
        that=None,
        anga="late afternoon",
    ),
    "todi": Raga(
        name="Todi",
        aroha=["S", "r", "g", "M", "d", "P", "D", "N", "S'"],
        avaroha=["S'", "N", "d", "P", "M", "g", "r", "S"],
        vadi=62,  # G (Gandhar)
        samvadi=67,  # G (Gandhar) - same for Todi
        that=None,
        anga="morning",
    ),
    "bhairav": Raga(
        name="Bhairav",
        aroha=["S", "r", "g", "M", "P", "d", "N", "S'"],
        avaroha=["S'", "N", "d", "P", "M", "g", "r", "S"],
        vadi=62,  # G
        samvadi=67,  # G
        that=None,
        anga="morning",
    ),
}


def get_raga(name: str) -> Raga:
    """Get a raga definition by name.

    Args:
        name: Raga name (case-insensitive)

    Returns:
        Raga definition

    Raises:
        KeyError: If raga not found
    """
    name_lower = name.lower()

    # Try exact match first
    for raga_name, raga in _RAGA_DATABASE.items():
        if raga_name.lower() == name_lower:
            return raga

    # Try partial match
    for raga_name, raga in _RAGA_DATABASE.items():
        if name_lower in raga_name.lower():
            return raga

    raise KeyError(f"Raga not found: {name}")


def list_ragas() -> list[str]:
    """List all available ragas."""
    return list(_RAGA_DATABASE.keys())


# =============================================================================
# Raga Engine
# =============================================================================


class RagaEngine:
    """Engine for raga-based note selection and composition."""

    def __init__(self) -> None:
        self._cache: dict[str, Raga] = {}

    def get_raga(self, name: str) -> Raga:
        """Get a raga from cache or database."""
        if name not in self._cache:
            self._cache[name] = get_raga(name)
        return self._cache[name]

    def generate_scale_notes(
        self,
        raga_name: str,
        start_octave: int = 4,
        ascending: bool = True,
    ) -> list[Note]:
        """Generate scale notes for a raga.

        Args:
            raga_name: Name of the raga
            start_octave: Starting octave
            ascending: Whether to use aroha (ascending) or avaroha (descending)

        Returns:
            List of Note objects forming the raga scale
        """
        raga = self.get_raga(raga_name)
        pattern = raga.aroha if ascending else raga.avaroha

        notes = []
        octave = start_octave
        current_note = None

        for note_name in pattern:
            # Handle octave markers (', indicates octave up)
            if note_name.endswith("'"):
                note_name = note_name[:-1]
                octave += 1
            elif note_name.endswith("''"):
                note_name = note_name[:-2]
                octave += 1

            # Handle flat/sharp
            if note_name.endswith("b"):
                note_name = note_name[:-1].upper()
            elif note_name.endswith("#"):
                note_name = note_name[:-1].upper()

            try:
                note = Note(note_name, octave=octave)
            except ValueError:
                # Skip invalid note names
                continue

            notes.append(note)
            current_note = note

        return notes

    def suggest_note_sequence(
        self,
        raga_name: str,
        num_notes: int,
        start_beat: float = 0.0,
        beat_duration: float = 1.0,
        vadi_emphasis: bool = True,
    ) -> list[Note]:
        """Suggest a note sequence following raga rules.

        Args:
            raga_name: Name of the raga
            num_notes: Number of notes to generate
            start_beat: Starting beat position
            beat_duration: Duration of each beat
            vadi_emphasis: Whether to emphasize vadi/samvadi

        Returns:
            List of Note objects with proper timing
        """
        raga = self.get_raga(raga_name)
        allowed_notes = raga.get_allowed_notes()

        notes = []
        current_beat = start_beat
        octave = 4

        # Start and return to tonic often
        if 60 in allowed_notes:  # C4
            tonic_octave = 4
        else:
            tonic_octave = 4

        # Simple algorithm: traverse raga scale favoring vadi
        for i in range(num_notes):
            # Bias toward vadi note every 4th note
            if vadi_emphasis and i % 4 == 0 and raga.vadi in allowed_notes:
                pitch = raga.vadi
            elif i % 4 == 1 and raga.samvadi in allowed_notes:
                pitch = raga.samvadi
            else:
                # Get random note from allowed notes
                import random
                pitch = random.choice(allowed_notes)

            # Map MIDI to note name and octave
            note = Note.from_midi(pitch)

            # Adjust octave based on previous note
            if notes:
                # Keep within reasonable range
                if abs(pitch - notes[-1].midi_number) > 12:
                    octave = notes[-1].octave + (1 if pitch > notes[-1].midi_number else -1)

            notes.append(Note(
                note_name=note.pitch,
                octave=octave,
                start_time=current_beat * beat_duration,
                duration=beat_duration,
                velocity=80 if i % 2 == 0 else 70,
            ))

            current_beat += beat_duration

        return notes


def get_allowed_notes_for_raga(raga_name: str) -> list[int]:
    """Get all MIDI note numbers allowed in a raga.

    Utility function for other modules.

    Args:
        raga_name: Name of the raga

    Returns:
        Sorted list of MIDI note numbers
    """
    raga = get_raga(raga_name)
    return raga.get_allowed_notes()
