"""MIDI file writer.

This module provides functionality for writing musical scores to MIDI files.
"""

from __future__ import annotations
from typing import List, Union, Optional, Dict
from dataclasses import dataclass, field
from pathlib import Path

try:
    import mido
except ImportError:
    mido = None

from musicgen.core.note import Note, Rest, QUARTER
from musicgen.core.chord import Chord


class MIDIWriter:
    """Writes musical scores to MIDI files."""

    # MIDI program numbers for instruments
    INSTRUMENT_PROGRAMS = {
        "piano": 0,
        "acoustic_piano": 0,
        "violin": 40,
        "viola": 41,
        "cello": 42,
        "double_bass": 43,
        "flute": 73,
        "piccolo": 72,
        "clarinet": 71,
        "oboe": 68,
        "bassoon": 70,
        "trumpet": 56,
        "french_horn": 60,
        "trombone": 57,
        "timpani": 47,
        "pizzicato": 45,
    }

    def __init__(self, ticks_per_quarter: int = 480):
        """Initialize the MIDI writer.

        Args:
            ticks_per_quarter: Ticks per quarter note (resolution)
        """
        self.ticks_per_quarter = ticks_per_quarter
        self.tempo = 120  # Default tempo

    @staticmethod
    def write(score: "Score", filepath: str, tempo: int = 120) -> str:
        """Write a score to a MIDI file.

        Args:
            score: The score to write
            filepath: Path to output file
            tempo: Tempo in BPM

        Returns:
            Path to the written file
        """
        if mido is None:
            raise RuntimeError("mido library is required for MIDI export")

        writer = MIDIWriter()
        writer.tempo = tempo
        data = writer._generate_midi_file(score)

        data.save(filepath)

        return filepath

    def _generate_midi_file(self, score: "Score") -> "mido.MidiFile":
        """Generate a MIDI file from a score.

        Args:
            score: The score

        Returns:
            A mido.MidiFile object
        """
        mid = mido.MidiFile(ticks_per_beat=self.ticks_per_quarter)

        # Create a track for each part
        for part in score.parts:
            track = self._generate_track(part)
            mid.tracks.append(track)

        return mid

    def _generate_track(self, part: "Part") -> "mido.MidiTrack":
        """Generate a MIDI track for a part.

        Args:
            part: The part

        Returns:
            A mido.MidiTrack object
        """
        track = mido.MidiTrack()
        track.name = part.name or "Untitled"

        # Set tempo meta event
        microseconds_per_quarter = int(60000000 / self.tempo)
        track.append(mido.MetaMessage(
            'set_tempo',
            tempo=microseconds_per_quarter,
            time=0
        ))

        # Set instrument (program change)
        program = 0
        if hasattr(part, "instrument") and part.instrument:
            program = getattr(part.instrument, "midi_program", 0)
        else:
            # Try to guess from part name
            part_name_lower = part.name.lower() if part.name else ""
            for inst_name, prog in self.INSTRUMENT_PROGRAMS.items():
                if inst_name in part_name_lower:
                    program = prog
                    break

        track.append(mido.Message(
            'program_change',
            program=program,
            time=0,
            channel=0
        ))

        # Add notes
        for note_obj in part.notes:
            if isinstance(note_obj, Note):
                # Note on
                track.append(mido.Message(
                    'note_on',
                    note=note_obj.midi_number,
                    velocity=note_obj.velocity,
                    time=0,
                    channel=0
                ))

                # Note off after duration
                ticks = int(note_obj.duration * self.ticks_per_quarter)
                track.append(mido.Message(
                    'note_off',
                    note=note_obj.midi_number,
                    velocity=0,
                    time=ticks,
                    channel=0
                ))

        # End of track
        track.append(mido.MetaMessage('end_of_track', time=0))

        return track


@dataclass
class Part:
    """A part in a score.

    Attributes:
        name: Part name
        instrument: The instrument for this part
        notes: List of notes in this part
    """

    name: str = ""
    instrument: Optional = None
    notes: List[Union[Note, Rest]] = field(default_factory=list)

    @property
    def length(self) -> int:
        """Return number of notes."""
        return len(self.notes)

    def add_note(self, note: Union[Note, Rest]) -> None:
        """Add a note to this part.

        Args:
            note: Note or Rest to add
        """
        self.notes.append(note)

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Part({self.name or 'Untitled'}, {len(self.notes)} notes)"


@dataclass
class Score:
    """A musical score containing multiple parts.

    Attributes:
        parts: List of parts in the score
        title: Score title
        composer: Composer name
    """

    parts: List[Part] = field(default_factory=list)
    title: str = ""
    composer: str = ""

    @property
    def num_parts(self) -> int:
        """Return number of parts."""
        return len(self.parts)

    def add_part(self, part: Part) -> None:
        """Add a part to the score.

        Args:
            part: Part to add
        """
        self.parts.append(part)

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Score({self.title or 'Untitled'}, {self.num_parts} parts)"
