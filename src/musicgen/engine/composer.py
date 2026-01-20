"""Composition engine for YAML-based music generation.

This module provides the main composition engine that interprets YAML
specifications and generates music using genre-specific rules.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from musicgen.core.note import Note
from musicgen.engine.parser import (
    CompositionSpec,
    InstrumentSpec,
    SectionSpec,
    ValidationError,
    load_yaml,
    validate_spec,
)
from musicgen.io.midi_writer import Part, Score


class CompositionEngine:
    """Main composition engine for YAML-based music generation.

    The engine:
    1. Loads and validates YAML specifications
    2. Selects the appropriate genre rule
    3. Generates notes for each instrument
    4. Orchestrates timing across sections
    5. Applies ornamentation
    6. Outputs to MIDI or other formats
    """

    def __init__(self) -> None:
        self._current_spec: CompositionSpec | None = None
        self._genre_rule: Any = None  # GenreRule instance

    def load_specification(self, yaml_path: str | Path) -> CompositionSpec:
        """Load a YAML composition specification.

        Args:
            yaml_path: Path to YAML file

        Returns:
            Parsed CompositionSpec

        Raises:
            FileNotFoundError: If file doesn't exist
            ValidationError: If spec is invalid
        """
        spec = load_yaml(yaml_path)

        # Validate the specification
        errors = validate_spec(spec)
        if errors:
            raise ValidationError(f"Invalid specification:\n" + "\n".join(errors))

        self._current_spec = spec

        # Get the genre rule (import here to avoid circular import)
        from musicgen.engine import GenreRuleRegistry
        self._genre_rule = GenreRuleRegistry.get(spec.genre)

        return spec

    def load_specification_from_dict(
        self, data: dict[str, Any]
    ) -> CompositionSpec:
        """Load a composition specification from a dictionary.

        Args:
            data: Dictionary representation of spec

        Returns:
            Parsed CompositionSpec

        Raises:
            ValidationError: If spec is invalid
        """
        spec = CompositionSpec(**data)

        # Validate the specification
        errors = validate_spec(spec)
        if errors:
            raise ValidationError(f"Invalid specification:\n" + "\n".join(errors))

        self._current_spec = spec
        # Get the genre rule (import here to avoid circular import)
        from musicgen.engine import GenreRuleRegistry
        self._genre_rule = GenreRuleRegistry.get(spec.genre)

        return spec

    def generate(self) -> Score:
        """Generate a complete composition from the loaded specification.

        Returns:
            Score with all parts and notes

        Raises:
            RuntimeError: If no specification is loaded
        """
        if self._current_spec is None:
            raise RuntimeError("No specification loaded. Call load_specification first.")

        spec = self._current_spec

        # Create the score
        score = Score(
            title=spec.title,
            composer=spec.composer,
        )

        # Track current time for section placement
        current_time = 0.0

        # Process each section
        for section in spec.sections:
            # Calculate section duration
            beats_per_bar = spec.time_signature.numerator
            beat_duration = 60.0 / spec.tempo.bpm
            section_duration = (
                section.duration_bars * beats_per_bar * beat_duration
            )

            # Generate notes for each instrument in this section
            for instrument in spec.instruments:
                # Check if instrument should play in this section
                # (For now, all instruments play all sections)
                notes = self._generate_instrument_notes(
                    spec, section, instrument, current_time
                )

                # Add to score
                if notes:
                    part = self._notes_to_part(notes, instrument, spec)
                    score.add_part(part)

            current_time += section_duration

        return score

    def _generate_instrument_notes(
        self,
        spec: CompositionSpec,
        section: SectionSpec,
        instrument: InstrumentSpec,
        start_time: float,
    ) -> list[Note]:
        """Generate notes for an instrument in a section.

        Args:
            spec: Full composition specification
            section: Section specification
            instrument: Instrument specification
            start_time: Start time for this section

        Returns:
            List of Note objects
        """
        notes: list[Note] = []

        match instrument.role:
            case "melody":
                notes = self._genre_rule.generate_melody(spec, section, instrument)

            case "rhythm":
                notes = self._genre_rule.generate_rhythm(spec, section, instrument)

            case "drone":
                notes = self._genre_rule.generate_drone(spec, instrument)

            case "harmony":
                # For now, generate simplified melody for harmony
                notes = self._genre_rule.generate_melody(spec, section, instrument)

            case "bass":
                # Generate simplified bass line
                notes = self._generate_bass(spec, section, instrument, start_time)

            case _:
                # Default to melody generation
                notes = self._genre_rule.generate_melody(spec, section, instrument)

        # Apply ornamentation
        if notes and instrument.role in ("melody", "harmony"):
            notes = self._genre_rule.apply_ornamentation(notes, spec, instrument)

        # Adjust note times by section start time
        if start_time > 0:
            for note in notes:
                note.start_time += start_time

        return notes

    def _generate_bass(
        self,
        spec: CompositionSpec,
        section: SectionSpec,
        instrument: InstrumentSpec,
        start_time: float,
    ) -> list[Note]:
        """Generate a simple bass line.

        Args:
            spec: Composition specification
            section: Section specification
            instrument: Instrument specification
            start_time: Start time offset

        Returns:
            List of bass notes
        """
        notes: list[Note] = []

        # Simple bass: tonic on beat 1, fifth on beat 3
        beat_duration = 60.0 / spec.tempo.bpm
        section_duration = (
            section.duration_bars * spec.time_signature.numerator * beat_duration
        )

        current_time = 0.0
        beat = 0

        while current_time < section_duration:
            # Determine pitch (alternating tonic and dominant)
            if beat % 4 == 0:
                # Tonic
                pitch = 36  # C2
            elif beat % 4 == 2:
                # Dominant
                pitch = 43  # G2
            else:
                current_time += beat_duration
                beat += 1
                continue

            note = Note(
                note_name=Note.from_midi(pitch).pitch,
                octave=Note.from_midi(pitch).octave,
                start_time=current_time,
                duration=beat_duration * 0.9,
                velocity=80,
            )
            notes.append(note)

            current_time += beat_duration
            beat += 1

        return notes

    def _notes_to_part(
        self,
        notes: list[Note],
        instrument: InstrumentSpec,
        spec: CompositionSpec,
    ) -> Part:
        """Convert notes to a MIDI part.

        Args:
            notes: List of notes
            instrument: Instrument specification
            spec: Composition specification

        Returns:
            MIDI Part
        """
        # Create a Part with the notes
        part = Part(name=instrument.name)
        part.notes = notes.copy()
        return part

    def generate_to_midi(
        self,
        yaml_path: str | Path,
        output_path: str | Path | None = None,
    ) -> str:
        """Generate composition from YAML and write to MIDI file.

        Args:
            yaml_path: Path to YAML specification
            output_path: Output MIDI path (defaults to yaml_path with .mid extension)

        Returns:
            Path to generated MIDI file
        """
        # Load specification
        self.load_specification(yaml_path)

        # Generate score
        score = self.generate()

        # Determine output path
        if output_path is None:
            yaml_path = Path(yaml_path)
            output_path = yaml_path.with_suffix(".mid")

        # Write MIDI
        from musicgen.io.midi_writer import MIDIWriter
        MIDIWriter.write(score, str(output_path))

        return str(output_path)


def generate_from_yaml(
    yaml_path: str | Path,
    output_path: str | Path | None = None,
) -> str:
    """Convenience function to generate music from YAML specification.

    Args:
        yaml_path: Path to YAML specification
        output_path: Output MIDI path (optional)

    Returns:
        Path to generated MIDI file
    """
    engine = CompositionEngine()
    return engine.generate_to_midi(yaml_path, output_path)
