"""Core note and rest classes for music representation.

This module provides the fundamental classes for representing musical notes
and rests, including duration and dynamic constants.
"""

from __future__ import annotations

from dataclasses import dataclass

# Duration constants (in quarter notes)
WHOLE = 4.0
HALF = 2.0
QUARTER = 1.0
EIGHTH = 0.5
SIXTEENTH = 0.25

# Dotted durations
DOTTED_HALF = 3.0
DOTTED_QUARTER = 1.5
DOTTED_EIGHTH = 0.75

# Triplet durations
TRIPLET_HALF = 2.0 / 3 * 2
TRIPLET_QUARTER = 1.0 / 3 * 2
TRIPLET_EIGHTH = 0.5 / 3 * 2

# Dynamic marking constants (velocity values 0-127)
PP = 30
P = 50
MP = 70
MF = 90
F = 100
FF = 120

# Note names and accidentals
NOTE_NAMES = ["C", "D", "E", "F", "G", "A", "B"]
ACCIDENTALS = ["", "#", "b", "x", "bb"]

# Pitch classes for note names
PITCH_CLASS = {
    "C": 0, "C#": 1, "Db": 1,
    "D": 2, "D#": 3, "Eb": 3,
    "E": 4,
    "F": 5, "F#": 6, "Gb": 6,
    "G": 7, "G#": 8, "Ab": 8,
    "A": 9, "A#": 10, "Bb": 10,
    "B": 11,
}


@dataclass
class Note:
    """Represents a musical note with pitch, duration, and attributes.

    Attributes:
        name: The note name (C, D, E, F, G, A, B)
        octave: The octave number (0-9)
        duration: Duration in quarter notes
        velocity: MIDI velocity (0-127)
        accidental: Accidental ("", "#", "b", "x", "bb")
        tied: Whether this note is tied to the next
        articulation: Articulation mark (".", ">", "-", "^")
    """

    name: str
    octave: int
    duration: float = QUARTER
    velocity: int = MF
    accidental: str = ""
    tied: bool = False
    articulation: str = ""

    def __post_init__(self):
        """Validate note parameters after initialization."""
        # Clean up the note name
        self.name = self.name.strip().upper()

        # Validate note name
        if self.name not in NOTE_NAMES:
            raise ValueError(f"Invalid note name: {self.name}. Must be one of {NOTE_NAMES}")

        # Validate octave
        if not 0 <= self.octave <= 9:
            raise ValueError(f"Invalid octave: {self.octave}. Must be 0-9")

        # Validate velocity
        if not 0 <= self.velocity <= 127:
            raise ValueError(f"Invalid velocity: {self.velocity}. Must be 0-127")

        # Validate accidental
        if self.accidental not in ACCIDENTALS:
            raise ValueError(f"Invalid accidental: {self.accidental}. Must be one of {ACCIDENTALS}")

    @classmethod
    def from_pitch_string(cls, pitch: str, duration: float = QUARTER,
                          velocity: int = MF, **kwargs) -> Note:
        """Create a Note from a pitch string (e.g., "C4", "A#5", "Bb3").

        Args:
            pitch: Pitch string (e.g., "C4", "A#5", "Bb3")
            duration: Duration in quarter notes
            velocity: MIDI velocity 0-127
            **kwargs: Additional arguments to pass to Note

        Returns:
            A new Note instance

        Raises:
            ValueError: If pitch string is invalid
        """
        pitch = pitch.strip()

        # Parse accidental
        accidental = ""
        name = ""

        if "##" in pitch or "x" in pitch.lower():
            accidental = "x"
            name_part = pitch.replace("##", "").replace("x", "").replace("X", "")
        elif "bb" in pitch:
            accidental = "bb"
            name_part = pitch.replace("bb", "")
        elif "#" in pitch:
            accidental = "#"
            name_part = pitch.replace("#", "")
        elif "b" in pitch and pitch[0] != "b":  # Avoid catching "B" note
            accidental = "b"
            name_part = pitch.replace("b", "")
        else:
            name_part = pitch

        # Find where octave starts
        i = 0
        while i < len(name_part) and not name_part[i].isdigit():
            name += name_part[i]
            i += 1

        # Get octave
        if i < len(name_part):
            octave = int(name_part[i:])
        else:
            raise ValueError(f"Missing octave in pitch string: {pitch}")

        # Override accidental if detected in pitch string
        kwargs["accidental"] = accidental

        return cls(name=name, octave=octave, duration=duration, velocity=velocity, **kwargs)

    @property
    def midi_number(self) -> int:
        """Return the MIDI note number (0-127).

        C4 = 60, A4 = 69
        """
        base = (self.octave + 1) * 12
        pitch_class = PITCH_CLASS.get(f"{self.name}{self.accidental}", 0)
        return base + pitch_class

    @property
    def frequency(self) -> float:
        """Return the frequency in Hz using A4 = 440Hz standard."""
        return 440.0 * (2.0 ** ((self.midi_number - 69) / 12.0))

    @property
    def pitch_class(self) -> int:
        """Return the pitch class (0-11, where C=0, C#=1, etc.)."""
        return PITCH_CLASS.get(f"{self.name}{self.accidental}", 0) % 12

    def transpose(self, semitones: int) -> Note:
        """Return a new Note transposed by the given semitones.

        Args:
            semitones: Number of semitones to transpose (positive = up, negative = down)

        Returns:
            A new Note instance
        """
        new_midi = self.midi_number + semitones

        # Clamp to valid MIDI range
        new_midi = max(0, min(127, new_midi))

        # Create new note from MIDI and copy attributes
        note = Note.from_midi(new_midi, duration=self.duration, velocity=self.velocity)
        # Preserve articulation
        if hasattr(self, 'articulation'):
            note.articulation = self.articulation

        return note

    def to_pitch_string(self) -> str:
        """Return the note as a pitch string (e.g., 'C#4', 'Bb3')."""
        return f"{self.name}{self.accidental}{self.octave}"

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Note({self.to_pitch_string()}, {self.duration})"

    def __eq__(self, other) -> bool:
        """Check equality based on pitch and duration."""
        if not isinstance(other, Note):
            return False
        return (self.name == other.name and
                self.octave == other.octave and
                self.accidental == other.accidental and
                self.duration == other.duration and
                self.velocity == other.velocity)

    def __hash__(self) -> int:
        """Make Note hashable for use in sets/dicts."""
        return hash((self.name, self.octave, self.accidental, self.duration, self.velocity))

    @classmethod
    def from_midi(cls, midi_number: int, duration: float = QUARTER,
                  velocity: int = MF, prefer_sharp: bool = True) -> Note:
        """Create a Note from a MIDI note number.

        Args:
            midi_number: MIDI note number (0-127)
            duration: Duration in quarter notes
            velocity: MIDI velocity
            prefer_sharp: If True, use sharps for black keys; otherwise use flats

        Returns:
            A new Note instance
        """
        if not 0 <= midi_number <= 127:
            raise ValueError(f"MIDI number must be 0-127, got {midi_number}")

        # Calculate octave and note within octave
        octave = (midi_number // 12) - 1
        pitch_class = midi_number % 12

        # Mapping from pitch class to note name
        if prefer_sharp:
            pitch_to_note = {
                0: ("C", ""), 1: ("C", "#"), 2: ("D", ""),
                3: ("D", "#"), 4: ("E", ""), 5: ("F", ""),
                6: ("F", "#"), 7: ("G", ""), 8: ("G", "#"),
                9: ("A", ""), 10: ("A", "#"), 11: ("B", "")
            }
        else:
            pitch_to_note = {
                0: ("C", ""), 1: ("D", "b"), 2: ("D", ""),
                3: ("E", "b"), 4: ("E", ""), 5: ("F", ""),
                6: ("G", "b"), 7: ("G", ""), 8: ("A", "b"),
                9: ("A", ""), 10: ("B", "b"), 11: ("B", "")
            }

        name, accidental = pitch_to_note[pitch_class]

        return cls(name=name, octave=octave, duration=duration, velocity=velocity,
                   accidental=accidental)


@dataclass
class Rest:
    """Represents a musical rest (silence) with a duration.

    Attributes:
        duration: Duration in quarter notes
    """

    duration: float = QUARTER

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Rest({self.duration})"

    def __eq__(self, other) -> bool:
        """Check equality based on duration."""
        if not isinstance(other, Rest):
            return False
        return self.duration == other.duration
