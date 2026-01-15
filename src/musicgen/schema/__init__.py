"""Schema generation for AI composition."""

from musicgen.schema.generator import SchemaGenerator, get_schema
from musicgen.schema.models import (
    CompositionSchema,
    DurationUnit,
    NoteFormat,
    NoteSchema,
    PartSchema,
    PitchRepresentation,
    RestSchema,
    SchemaConfig,
)

__all__ = [
    "NoteSchema",
    "RestSchema",
    "PartSchema",
    "CompositionSchema",
    "SchemaConfig",
    "NoteFormat",
    "DurationUnit",
    "PitchRepresentation",
    "SchemaGenerator",
    "get_schema",
]
