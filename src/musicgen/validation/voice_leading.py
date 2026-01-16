"""Voice leading validation for V3 compositions.

This module provides validation for common voice leading errors
including parallel perfect intervals, direct motion issues, and
leading tone resolution problems.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from musicgen.ai_models.v3.notes import Note
from musicgen.validation.models import ValidationResult, ValidationSeverity

if TYPE_CHECKING:
    from musicgen.ai_models.v3.composition import Composition
    from musicgen.ai_models.v3.parts import InstrumentPart


# Standard intervals in semitones
PERFECT_UNISON = 0
MINOR_SECOND = 1
MAJOR_SECOND = 2
MINOR_THIRD = 3
MAJOR_THIRD = 4
PERFECT_FOURTH = 5
TRITONE = 6
PERFECT_FIFTH = 7
MINOR_SIXTH = 8
MAJOR_SIXTH = 9
MINOR_SEVENTH = 10
MAJOR_SEVENTH = 11
PERFECT_OCTAVE = 12


# Leading tone scale degrees (in major/minor)
LEADING_TONE_DEGREES = {7}  # 7th scale degree
# Also check for #4 in minor (leading tone to 5)
SUBMEDIANT_RAISED = {4}  # When raised in harmonic minor


@dataclass
class NoteEvent:
    """A note event with voice/part information.

    Attributes:
        note: The V3 Note object
        part_name: Name of the instrument/voice part
        start_time: Start time in seconds
        end_time: End time in seconds
        pitch_class: Pitch class (0-11)
    """

    note: Note
    part_name: str
    start_time: float
    end_time: float

    @property
    def pitch_class(self) -> int:
        """Get pitch class (0-11)."""
        return self.note.pitch % 12

    @property
    def midi_pitch(self) -> int:
        """Get MIDI pitch number."""
        return self.note.pitch


class VoiceLeadingValidator:
    """Validator for voice leading rules in compositions.

    Checks for common voice leading errors including:
    - Parallel perfect intervals (5ths and octaves)
    - Direct perfect intervals by skip motion
    - Improper leading tone resolution

    This validator works with V3 Composition models using
    time-based note events (in seconds).
    """

    # Maximum time gap (seconds) to consider notes simultaneous for
    # voice leading analysis
    SIMULTANEITY_THRESHOLD: float = 0.05

    # Minimum interval to consider "skip motion" for direct intervals
    SKIP_THRESHOLD: int = 3

    def __init__(
        self,
        check_parallel_fifths: bool = True,
        check_parallel_octaves: bool = True,
        check_direct_intervals: bool = True,
        check_leading_tone: bool = True,
        strictness: str = "standard",
    ) -> None:
        """Initialize the voice leading validator.

        Args:
            check_parallel_fifths: Enable parallel fifth checking
            check_parallel_octaves: Enable parallel octave checking
            check_direct_intervals: Enable direct interval checking
            check_leading_tone: Enable leading tone resolution checking
            strictness: Validation strictness ('strict', 'standard', 'lenient')
        """
        self.check_parallel_fifths = check_parallel_fifths
        self.check_parallel_octaves = check_parallel_octaves
        self.check_direct_intervals = check_direct_intervals
        self.check_leading_tone = check_leading_tone

        # Adjust thresholds based on strictness
        if strictness == "strict":
            self.simultaneity_threshold = 0.02
        elif strictness == "lenient":
            self.simultaneity_threshold = 0.1
        else:  # standard
            self.simultaneity_threshold = self.SIMULTANEITY_THRESHOLD

    def validate(self, composition: Composition) -> ValidationResult:
        """Validate voice leading in a composition.

        Args:
            composition: The V3 Composition to validate

        Returns:
            ValidationResult with all found issues
        """
        result = ValidationResult()

        # Need at least 2 parts for voice leading analysis
        parts = [p for p in composition.parts if p.notes]
        if len(parts) < 2:
            return result

        # Get key signature for leading tone analysis
        key_signature = composition.key_signature
        tonic_pc = self._parse_tonic_pitch_class(key_signature)
        is_minor = "minor" in key_signature.lower()

        # Validate each pair of parts
        for i in range(len(parts)):
            for j in range(i + 1, len(parts)):
                part1 = parts[i]
                part2 = parts[j]

                if self.check_parallel_fifths:
                    self._validate_parallel_perfect_intervals(
                        part1, part2, PERFECT_FIFTH, result
                    )

                if self.check_parallel_octaves:
                    self._validate_parallel_perfect_intervals(
                        part1, part2, PERFECT_OCTAVE, result
                    )

                if self.check_direct_intervals:
                    self._validate_direct_perfect_intervals(
                        part1, part2, PERFECT_FIFTH, tonic_pc, is_minor, result
                    )
                    self._validate_direct_perfect_intervals(
                        part1, part2, PERFECT_OCTAVE, tonic_pc, is_minor, result
                    )

        if self.check_leading_tone:
            self._validate_leading_tone_resolution(
                parts, key_signature, result
            )

        result.instruments_checked = len(parts)
        result.total_notes = sum(len(p.notes) for p in parts)

        return result

    def _validate_parallel_perfect_intervals(
        self,
        part1: InstrumentPart,
        part2: InstrumentPart,
        interval: int,
        result: ValidationResult,
    ) -> None:
        """Check for parallel perfect intervals between two parts.

        Parallel perfect intervals (5ths and octaves) are traditionally
        avoided in common practice voice leading.

        Args:
            part1: First instrument part
            part2: Second instrument part
            interval: Interval to check (7 for 5th, 12 for octave)
            result: ValidationResult to add errors to
        """
        interval_name = "fifth" if interval == PERFECT_FIFTH else "octave"

        # Get simultaneous note pairs
        pairs = self._get_simultaneous_note_pairs(part1, part2)

        prev_interval = None
        prev_time = None

        for time, note1, note2 in pairs:
            current_interval = abs(note1.pitch - note2.pitch)

            # Check if this is the same interval class as target
            if current_interval % 12 == interval % 12:
                # If we had the same interval class before, check if it's parallel
                if prev_interval is not None and prev_interval % 12 == interval % 12:
                    # Check if both voices moved in the same direction
                    time_diff = time - prev_time if prev_time else 0
                    if time_diff < 2.0:  # Within reasonable time window
                        result.add_voice_leading_error(
                            error_type=f"parallel_{interval_name}",
                            location=time,
                            voice1=part1.instrument_name,
                            voice2=part2.instrument_name,
                            description=(
                                f"Parallel {interval_name}s: "
                                f"both voices moved from {prev_interval} to "
                                f"{current_interval} semitones"
                            ),
                            severity=ValidationSeverity.ERROR,
                        )

                prev_interval = current_interval
                prev_time = time

    def _validate_direct_perfect_intervals(
        self,
        part1: InstrumentPart,
        part2: InstrumentPart,
        interval: int,
        tonic_pc: int,
        is_minor: bool,
        result: ValidationResult,
    ) -> None:
        """Check for direct perfect intervals by skip motion.

        Direct (or exposed) perfect intervals occur when the outer
        voices skip/leap to a perfect interval in similar motion.

        Args:
            part1: First instrument part
            part2: Second instrument part
            interval: Interval to check (7 for 5th, 12 for octave)
            tonic_pc: Pitch class of tonic (for key context)
            is_minor: Whether the key is minor
            result: ValidationResult to add errors to
        """
        interval_name = "fifth" if interval == PERFECT_FIFTH else "octave"

        # Get simultaneous note pairs
        pairs = self._get_simultaneous_note_pairs(part1, part2)

        if len(pairs) < 2:
            return

        for i in range(1, len(pairs)):
            curr_time, curr_note1, curr_note2 = pairs[i]
            prev_time, prev_note1, prev_note2 = pairs[i - 1]

            # Get current interval
            current_interval = abs(curr_note1.pitch - curr_note2.pitch)

            # Check if we arrived at a perfect interval
            if current_interval % 12 == interval % 12:
                # Calculate voice movement
                movement1 = curr_note1.pitch - prev_note1.pitch
                movement2 = curr_note2.pitch - prev_note2.pitch

                # Check for similar motion (both moving same direction)
                same_direction = (movement1 > 0 and movement2 > 0) or (
                    movement1 < 0 and movement2 < 0
                )

                # Check for skip motion in at least one voice
                skip_motion = (
                    abs(movement1) >= self.SKIP_THRESHOLD
                    or abs(movement2) >= self.SKIP_THRESHOLD
                )

                if same_direction and skip_motion:
                    result.add_voice_leading_error(
                        error_type=f"direct_{interval_name}",
                        location=curr_time,
                        voice1=part1.instrument_name,
                        voice2=part2.instrument_name,
                        description=(
                            f"Direct {interval_name} by similar motion: "
                            f"voice1 moved {movement1:+d}, voice2 moved {movement2:+d}"
                        ),
                        severity=ValidationSeverity.WARNING,
                    )

    def _validate_leading_tone_resolution(
        self,
        parts: list[InstrumentPart],
        key_signature: str,
        result: ValidationResult,
    ) -> None:
        """Check that leading tones resolve properly to the tonic.

        The leading tone (7th scale degree) should resolve upward
        by step to the tonic (1st scale degree).

        Args:
            parts: List of instrument parts
            key_signature: Key signature string
            result: ValidationResult to add errors to
        """
        tonic_pc = self._parse_tonic_pitch_class(key_signature)
        is_minor = "minor" in key_signature.lower()

        for part in parts:
            notes = part.notes
            if len(notes) < 2:
                continue

            for i in range(len(notes) - 1):
                current_note = notes[i]
                next_note = notes[i + 1]

                # Get pitch classes
                current_pc = current_note.pitch % 12
                next_pc = next_note.pitch % 12

                # Check if current note is a leading tone
                # Leading tone is one semitone below tonic
                leading_tone_pc = (tonic_pc - 1) % 12

                if current_pc == leading_tone_pc:
                    # Check if it resolves to tonic
                    if next_pc != tonic_pc:
                        # Check if it's at least moving upward
                        interval = next_note.pitch - current_note.pitch
                        if interval <= 0:
                            result.add_voice_leading_error(
                                error_type="leading_tone_resolution",
                                location=current_note.start_time,
                                voice1=part.instrument_name,
                                voice2="(tonic)",
                                description=(
                                    f"Leading tone at {current_note.pitch} "
                                    f"does not resolve upward to tonic "
                                    f"(moves {interval:+d} instead)"
                                ),
                                severity=ValidationSeverity.WARNING,
                            )

    def _get_simultaneous_note_pairs(
        self,
        part1: InstrumentPart,
        part2: InstrumentPart,
    ) -> list[tuple[float, Note, Note]]:
        """Get pairs of notes that sound simultaneously.

        Args:
            part1: First instrument part
            part2: Second instrument part

        Returns:
            List of (time, note1, note2) tuples
        """
        pairs = []

        for note1 in part1.notes:
            for note2 in part2.notes:
                # Check temporal overlap
                if self._notes_overlap(note1, note2):
                    # Use the later start time as the reference
                    time = max(note1.start_time, note2.start_time)
                    pairs.append((time, note1, note2))

        # Sort by time
        pairs.sort(key=lambda x: x[0])

        return pairs

    def _notes_overlap(self, note1: Note, note2: Note) -> bool:
        """Check if two notes overlap in time.

        Args:
            note1: First note
            note2: Second note

        Returns:
            True if notes overlap
        """
        start1 = note1.start_time
        end1 = note1.start_time + note1.duration
        start2 = note2.start_time
        end2 = note2.start_time + note2.duration

        # Check for overlap with threshold
        return not (end1 < start2 + self.simultaneity_threshold or
                    end2 < start1 + self.simultaneity_threshold)

    def _parse_tonic_pitch_class(self, key_signature: str) -> int:
        """Parse the tonic pitch class from a key signature string.

        Args:
            key_signature: Key signature (e.g., "C major", "A minor")

        Returns:
            Pitch class (0-11) of the tonic
        """
        # Map note names to pitch classes
        pitch_classes = {
            "C": 0, "C#": 1, "Db": 1,
            "D": 2, "D#": 3, "Eb": 3,
            "E": 4,
            "F": 5, "F#": 6, "Gb": 6,
            "G": 7, "G#": 8, "Ab": 8,
            "A": 9, "A#": 10, "Bb": 10,
            "B": 11,
        }

        # Extract the tonic note
        key_upper = key_signature.strip().upper()

        # Handle sharp/flat in tonic
        for name, pc in pitch_classes.items():
            if key_upper.startswith(name.upper()):
                return pc

        # Default to C
        return 0
