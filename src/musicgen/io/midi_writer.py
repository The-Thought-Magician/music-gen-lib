"""MIDI file writer.

This module provides functionality for writing musical scores to MIDI files.
"""

from __future__ import annotations
from typing import List, Union, Optional, Dict
from dataclasses import dataclass, field
from pathlib import Path
import struct

from musicgen.core.note import Note, Rest, QUARTER
from musicgen.core.chord import Chord


class MIDIWriter:
    """Writes musical scores to MIDI files."""

    # MIDI constants
    HEADER_CHUNK_ID = b"MThd"
    TRACK_CHUNK_ID = b"MTrk"

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
        writer = MIDIWriter()
        writer.tempo = tempo
        data = writer._generate_midi_data(score)

        with open(filepath, "wb") as f:
            f.write(data)

        return filepath

    def _generate_midi_data(self, score: "Score") -> bytes:
        """Generate MIDI file data from a score.

        Args:
            score: The score

        Returns:
            MIDI file as bytes
        """
        tracks = []

        # Create a track for each part
        for part in score.parts:
            track_data = self._generate_track(part)
            tracks.append(track_data)

        # Build header
        header = self._build_header(len(tracks))

        # Combine all chunks
        midi_data = header
        for track in tracks:
            midi_data += track

        return midi_data

    def _build_header(self, num_tracks: int) -> bytes:
        """Build the MIDI header chunk.

        Args:
            num_tracks: Number of tracks

        Returns:
            Header chunk as bytes
        """
        format_type = 0 if num_tracks == 1 else 1

        header = self.HEADER_CHUNK_ID
        header += struct.pack(">I", 6)  # Header length
        header += struct.pack(">H", format_type)  # Format
        header += struct.pack(">H", num_tracks)  # Number of tracks
        header += struct.pack(">H", self.ticks_per_quarter)  # Ticks per quarter

        return header

    def _generate_track(self, part: "Part") -> bytes:
        """Generate a MIDI track for a part.

        Args:
            part: The part

        Returns:
            Track chunk as bytes
        """
        events = bytearray()

        # Set tempo
        microseconds_per_quarter = int(60000000 / self.tempo)
        events.extend(self._encode_tempo(microseconds_per_quarter))

        # Set instrument
        if hasattr(part, "instrument") and part.instrument:
            midi_program = getattr(part.instrument, "midi_program", 0)
            events.extend(self._encode_program_change(midi_program))

        # Add notes
        current_time = 0
        for note_obj in part.notes:
            if isinstance(note_obj, Note):
                # Note on
                events.extend(self._encode_note_on(
                    note_obj.midi_number,
                    note_obj.velocity,
                    0  # Delta time (simplified)
                ))
                # Note off after duration
                ticks = int(note_obj.duration * self.ticks_per_quarter)
                events.extend(self._encode_note_off(
                    note_obj.midi_number,
                    0,
                    ticks  # Delta time
                ))
                current_time += ticks

        # End of track
        events.extend(self._encode_end_of_track(0))

        # Build track chunk
        track = self.TRACK_CHUNK_ID
        track += struct.pack(">I", len(events))  # Track length
        track += events

        return track

    def _encode_tempo(self, microseconds: int) -> bytes:
        """Encode a tempo meta event.

        Args:
            microseconds: Microseconds per quarter note

        Returns:
            Encoded event
        """
        data = struct.pack(">I", microseconds)[1:]  # 3 bytes
        return b"\x00\xFF\x51\x03" + data

    def _encode_program_change(self, program: int) -> bytes:
        """Encode a program change event.

        Args:
            program: MIDI program number (0-127)

        Returns:
            Encoded event
        """
        return bytes([0xC0, program & 0x7F])

    def _encode_note_on(self, note: int, velocity: int, delta_time: int) -> bytes:
        """Encode a note on event.

        Args:
            note: MIDI note number
            velocity: MIDI velocity
            delta_time: Delta time in ticks

        Returns:
            Encoded event (simplified - no variable length encoding)
        """
        if delta_time == 0:
            return bytes([0x90, note & 0x7F, velocity & 0x7F])
        return bytes([0x90, note & 0x7F, velocity & 0x7F])

    def _encode_note_off(self, note: int, velocity: int, delta_time: int) -> bytes:
        """Encode a note off event.

        Args:
            note: MIDI note number
            velocity: Release velocity
            delta_time: Delta time in ticks

        Returns:
            Encoded event
        """
        return bytes([0x80, note & 0x7F, velocity & 0x7F])

    def _encode_end_of_track(self, delta_time: int) -> bytes:
        """Encode an end of track meta event.

        Args:
            delta_time: Delta time

        Returns:
            Encoded event
        """
        return b"\x00\xFF\x2F\x00"


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
