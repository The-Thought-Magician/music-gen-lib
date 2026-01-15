"""Voice leading classes for music theory.

This module provides classes for generating proper voice leading
between chords following species counterpoint rules.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum

from musicgen.core.chord import Chord
from musicgen.core.note import Note


class VoiceType(Enum):
    """Types of voices in SATB writing."""

    SOPRANO = "soprano"
    ALTO = "alto"
    TENOR = "tenor"
    BASS = "bass"


# Voice ranges (MIDI note numbers)
VOICE_RANGES = {
    VoiceType.SOPRANO: (60, 84),   # C4 - C6
    VoiceType.ALTO: (53, 76),      # F3 - E5
    VoiceType.TENOR: (48, 69),     # C3 - A4
    VoiceType.BASS: (36, 60),      # C2 - C4
}


@dataclass
class Voice:
    """A single voice part.

    Attributes:
        voice_type: Type of voice (soprano, alto, tenor, bass)
        notes: List of notes in this voice
    """

    voice_type: VoiceType
    notes: list[Note]

    @property
    def range(self) -> tuple[int, int]:
        """Return the range for this voice type."""
        return VOICE_RANGES[self.voice_type]

    def in_range(self, note: Note) -> bool:
        """Check if a note is within this voice's range.

        Args:
            note: Note to check

        Returns:
            True if note is in range
        """
        low, high = self.range
        return low <= note.midi_number <= high

    def get_nearest_in_range(self, target: Note) -> Note:
        """Get the nearest note to target that's in range.

        Args:
            target: Target note

        Returns:
            A Note in range (moved by octave if needed)
        """
        while not self.in_range(target):
            if target.midi_number < self.range[0]:
                target = target.transpose(12)
            elif target.midi_number > self.range[1]:
                target = target.transpose(-12)
        return target


@dataclass
class Voicing:
    """A four-part voicing of a chord.

    Attributes:
        soprano: Soprano note
        alto: Alto note
        tenor: Tenor note
        bass: Bass note
        chord: The chord being voiced
    """

    soprano: Note
    alto: Note
    tenor: Note
    bass: Note
    chord: Chord

    @property
    def notes(self) -> list[Note]:
        """Return all notes in the voicing."""
        return [self.soprano, self.alto, self.tenor, self.bass]

    def get_intervals(self) -> list[int]:
        """Get intervals between adjacent voices (top to bottom)."""
        return [
            self.soprano.midi_number - self.alto.midi_number,
            self.alto.midi_number - self.tenor.midi_number,
            self.tenor.midi_number - self.bass.midi_number,
        ]

    def has_parallel_fifths(self, other: Voicing) -> bool:
        """Check for parallel fifths with another voicing.

        Args:
            other: The next voicing to check against

        Returns:
            True if parallel fifths exist
        """
        my_intervals = self.get_intervals()
        other_intervals = other.get_intervals()

        for i, (m, o) in enumerate(zip(my_intervals, other_intervals, strict=False)):
            if m == 7 and o == 7:  # Perfect fifth (inverted)
                return True
        return False

    def has_parallel_octaves(self, other: Voicing) -> bool:
        """Check for parallel octaves with another voicing.

        Args:
            other: The next voicing to check against

        Returns:
            True if parallel octaves exist
        """
        my_notes = self.notes
        other_notes = other.notes

        for i in range(4):
            for j in range(i + 1, 4):
                my_interval = abs(my_notes[i].midi_number - my_notes[j].midi_number)
                other_interval = abs(other_notes[i].midi_number - other_notes[j].midi_number)

                if my_interval == 12 and other_interval == 12:
                    return True

        return False

    def __repr__(self) -> str:
        """String representation."""
        return f"Voicing(S:{self.soprano.name}, A:{self.alto.name}, T:{self.tenor.name}, B:{self.bass.name})"


def voice_lead(chord1: Chord, chord2: Chord, num_voices: int = 4,
               prev_voicing: Voicing | None = None) -> Voicing:
    """Generate proper voice leading between two chords.

    Args:
        chord1: First chord
        chord2: Second chord
        num_voices: Number of voices (default 4)
        prev_voicing: Previous voicing for continuity

    Returns:
        A Voicing for chord2
    """
    chord1_notes = chord1.notes
    chord2_notes = chord2.notes

    # If we have a previous voicing, try to maintain voice continuity
    if prev_voicing:
        voices = [prev_voicing.soprano, prev_voicing.alto, prev_voicing.tenor, prev_voicing.bass]

        # Find nearest notes in new chord
        new_voices = []
        for voice in voices:
            nearest = None
            min_distance = float('inf')

            for note in chord2_notes:
                distance = abs(note.midi_number - voice.midi_number)
                if distance < min_distance:
                    min_distance = distance
                    nearest = note

            if nearest:
                # Adjust octave if needed
                while nearest.midi_number < voice.midi_number - 6:
                    nearest = nearest.transpose(12)
                while nearest.midi_number > voice.midi_number + 6:
                    nearest = nearest.transpose(-12)
                new_voices.append(nearest)
            else:
                new_voices.append(voice)

        # Sort by pitch (highest to lowest)
        new_voices.sort(key=lambda n: n.midi_number, reverse=True)

        return Voicing(
            soprano=new_voices[0] if len(new_voices) > 0 else chord2_notes[0],
            alto=new_voices[1] if len(new_voices) > 1 else chord2_notes[0],
            tenor=new_voices[2] if len(new_voices) > 2 else chord2_notes[0],
            bass=new_voices[3] if len(new_voices) > 3 else chord2_notes[0],
            chord=chord2
        )

    # Otherwise, create a standard voicing
    # Bass gets the root
    bass_note = chord2.root

    # Other voices get chord tones
    if len(chord2_notes) >= 3:
        alto_note = chord2_notes[1]
        tenor_note = chord2_notes[2] if len(chord2_notes) > 2 else chord2_notes[1]
        soprano_note = chord2_notes[0] if len(chord2_notes) > 0 else chord2.root

        # Double the root in the soprano or alto
        if random.random() < 0.5:
            soprano_note = chord2.root
    else:
        soprano_note = chord2.root
        alto_note = chord2.root
        tenor_note = chord2.root
        bass_note = chord2.root

    return Voicing(
        soprano=soprano_note,
        alto=alto_note,
        tenor=tenor_note,
        bass=bass_note,
        chord=chord2
    )


def generate_harmony(progression, scale, num_voices: int = 4) -> list[Voicing]:
    """Generate full harmony for a chord progression.

    Args:
        progression: Chord progression
        scale: Scale for the key
        num_voices: Number of voices

    Returns:
        List of Voicings
    """
    voicings = []
    current_voicing = None

    for chord in progression.chords:
        voicing = voice_lead(chord, chord, num_voices, current_voicing)
        voicings.append(voicing)
        current_voicing = voicing

    return voicings


def check_voice_leading_violations(voicings: list[Voicing]) -> list[str]:
    """Check a sequence of voicings for voice leading errors.

    Args:
        voicings: List of voicings to check

    Returns:
        List of violation descriptions
    """
    violations = []

    for i in range(len(voicings) - 1):
        v1, v2 = voicings[i], voicings[i + 1]

        if v1.has_parallel_fifths(v2):
            violations.append(f"Parallel fifths between positions {i} and {i + 1}")

        if v1.has_parallel_octaves(v2):
            violations.append(f"Parallel octaves between positions {i} and {i + 1}")

    return violations
