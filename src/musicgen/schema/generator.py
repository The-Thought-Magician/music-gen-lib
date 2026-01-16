"""Schema generation engine.

Auto-generates YAML schemas from Pydantic models and configuration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from musicgen.config import get_config
from musicgen.schema.models import (
    DurationUnit,
    NoteFormat,
    PitchRepresentation,
    SchemaConfig,
)


class SchemaGenerator:
    """Generates YAML schemas for AI composition.

    The schema tells the AI what it can generate.
    """

    def __init__(self, config: SchemaConfig | None = None):
        """Initialize the schema generator.

        Args:
            config: Schema configuration. Uses defaults if None.
        """
        self.config = config or self._default_config()
        self._schema: dict[str, Any] = {}

    def _default_config(self) -> SchemaConfig:
        """Create default config from settings."""
        settings = get_config()

        return SchemaConfig(
            note_format=NoteFormat(
                settings.get("notes", "default_format", default="detailed")
            ),
            duration_unit=DurationUnit(
                settings.get("notes", "duration_unit", default="quarter")
            ),
            pitch_representation=PitchRepresentation.NOTE_NAME,
            include_articulation=settings.get("schema", "include_articulation", default=True),
            include_dynamics=settings.get("schema", "include_dynamics", default=True),
            include_form=settings.get("schema", "include_form_structure", default=True),
            include_key_changes=settings.get("schema", "include_key_changes", default=True),
            include_tempo_changes=settings.get("schema", "include_tempo_changes", default=True),
            include_time_signature_changes=settings.get("schema", "include_time_signature_changes", default=True),
            max_duration=settings.get("validation", "max_duration", default=600),
            max_instruments=settings.get("orchestration", "max_instruments", default=16),
            velocity_min=settings.get("notes", "velocity_min", default=60),
            velocity_max=settings.get("notes", "velocity_max", default=100),
        )

    def generate(self) -> str:
        """Generate the YAML schema.

        Returns:
            YAML schema string
        """
        schema = {
            "version": "1.0",
            "description": "MusicGen AI Composition Schema",
            "note_format": self.config.note_format.value,
            "duration_unit": self.config.duration_unit.value,
            "pitch_representation": self.config.pitch_representation.value,
            "composition": self._composition_schema(),
            "note": self._note_schema(),
            "rest": self._rest_schema(),
            "part": self._part_schema(),
            "constraints": self._constraints_schema(),
            "instruments": self._instrument_schema(),
            "music_theory": self._theory_schema(),
        }

        if YAML_AVAILABLE:
            return yaml.dump(schema, sort_keys=False, default_flow_style=False)
        else:
            return str(schema)

    def _composition_schema(self) -> dict[str, Any]:
        """Schema for top-level composition."""
        comp = {
            "title": "string (composition title)",
            "tempo": "int (40-200 BPM)",
            "time_signature": '{"numerator": int, "denominator": int} (e.g., {"numerator": 4, "denominator": 4})',
            "key": '{"tonic": "string (note name)", "mode": "string (major/minor/dorian/etc.)"} (e.g., {"tonic": "C", "mode": "major"})',
            "parts": "array of Part objects",
        }

        if self.config.include_form:
            comp["form"] = "string (binary, ternary, rondo, sonata, through_composed, etc.)"
        if self.config.include_dynamics:
            comp["initial_dynamic"] = "string (pp, p, mp, mf, f, ff, fff)"
        if self.config.include_key_changes:
            comp["key_changes"] = "array of {measure, new_key}"

        return comp

    def _note_schema(self) -> dict[str, Any]:
        """Schema for a single note."""
        note = {
            "pitch": self._pitch_description(),
            "duration": f"float (in {self.config.duration_unit.value}s)",
            "velocity": f"int ({self.config.velocity_min}-{self.config.velocity_max})",
        }

        if self.config.include_articulation:
            note["articulation"] = "string (staccato, legato, accent, marcato, tenuto)"
        note["tied"] = "boolean (if true, note continues to next)"

        return note

    def _rest_schema(self) -> dict[str, Any]:
        """Schema for a rest."""
        return {
            "rest": True,
            "duration": f"float (in {self.config.duration_unit.value}s)",
        }

    def _part_schema(self) -> dict[str, Any]:
        """Schema for an instrument part."""
        return {
            "name": "string (instrument name)",
            "midi_program": "int (0-127, see instrument list)",
            "midi_channel": "int (0-15, 10 reserved for percussion)",
            "role": "string - MUST be one of: 'melody', 'harmony', 'bass', 'accompaniment', 'countermelody', 'pad', 'percussion'",
            "notes": "array of Note objects",
        }

    def _constraints_schema(self) -> dict[str, Any]:
        """Schema constraints."""
        return {
            "max_duration_seconds": self.config.max_duration,
            "max_instruments": self.config.max_instruments,
            "velocity_range": [self.config.velocity_min, self.config.velocity_max],
            "valid_time_signatures": ["4/4", "3/4", "2/4", "6/8", "cut-time", "5/4", "7/8"],
        }

    def _instrument_schema(self) -> dict[str, Any]:
        """Common instruments with MIDI program numbers."""
        return {
            "piano": 0,
            "acoustic_grand": 0,
            "bright_acoustic": 1,
            "electric_grand": 2,
            "strings": {
                "violin": 40,
                "viola": 41,
                "cello": 42,
                "double_bass": 43,
                "tremolo_strings": 44,
                "pizzicato_strings": 45,
            },
            "brass": {
                "trumpet": 56,
                "trombone": 57,
                "tuba": 58,
                "french_horn": 60,
            },
            "woodwinds": {
                "flute": 73,
                "clarinet": 71,
                "oboe": 68,
                "bassoon": 70,
                "saxophone_soprano": 64,
                "saxophone_alto": 65,
                "saxophone_tenor": 66,
                "saxophone_baritone": 67,
            },
            "percussion": {
                "timpani": 47,
                "orchestral_percussion": "channel 10",
            },
        }

    def _theory_schema(self) -> dict[str, Any]:
        """Music theory reference for AI."""
        return {
            "scales": {
                "major": "whole, whole, half, whole, whole, whole, half",
                "natural_minor": "whole, half, whole, whole, half, whole, whole",
                "harmonic_minor": "whole, half, whole, whole, half, whole+1, half",
                "melodic_minor_up": "whole, half, whole, whole, whole, whole, half",
                "modes": ["dorian", "phrygian", "lydian", "mixolydian", "locrian"],
                "pentatonic_major": ["1", "2", "3", "5", "6"],
                "pentatonic_minor": ["1", "b3", "4", "5", "b7"],
                "blues": ["1", "b3", "4", "b5", "5", "b7"],
            },
            "chord_qualities": {
                "major": ["1", "3", "5"],
                "minor": ["1", "b3", "5"],
                "diminished": ["1", "b3", "b5"],
                "augmented": ["1", "3", "#5"],
                "dominant_7th": ["1", "3", "5", "b7"],
                "major_7th": ["1", "3", "5", "7"],
                "minor_7th": ["1", "b3", "5", "b7"],
            },
            "common_progressions": {
                "pop": ["I-V-vi-IV", "I-IV-V-IV"],
                "jazz": ["ii-V-I", "iii-vi-ii-V"],
                "classical": ["I-IV-V-I", "I-IV-I-V"],
                "blues": ["I-IV-I-V-IV-I"],
            },
            "dynamics": {
                "pp": "pianissimo (very quiet)",
                "p": "piano (quiet)",
                "mp": "mezzo-piano (medium quiet)",
                "mf": "mezzo-forte (medium loud)",
                "f": "forte (loud)",
                "ff": "fortissimo (very loud)",
                "fff": "fortississimo (extremely loud)",
            },
        }

    def _pitch_description(self) -> str:
        """Describe pitch format based on representation."""
        if self.config.pitch_representation == PitchRepresentation.NOTE_NAME:
            return "string (e.g., 'C4', 'Ab3', 'F#5' - note name + octave)"
        elif self.config.pitch_representation == PitchRepresentation.MIDI_NUMBER:
            return "int (0-127, where 60 = C4, 69 = A440)"
        else:
            return "float (Hz, where 440.0 = A4)"

    def save(self, path: Path) -> None:
        """Save schema to file.

        Args:
            path: Output path for schema file
        """
        schema = self.generate()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(schema)

    @staticmethod
    def get_schema_string(config: SchemaConfig | None = None) -> str:
        """Get schema as string (convenience method).

        Args:
            config: Optional schema configuration

        Returns:
            YAML schema string
        """
        gen = SchemaGenerator(config)
        return gen.generate()


# Convenience function
def get_schema(config: SchemaConfig | None = None) -> str:
    """Get the current AI composition schema.

    Args:
        config: Optional schema configuration

    Returns:
        YAML schema string
    """
    return SchemaGenerator.get_schema_string(config)
