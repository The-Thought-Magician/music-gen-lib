"""Function calling tools for Gemini AI music generation.

This module defines tools that the AI can use to enhance music generation
through structured function calls rather than generating everything in JSON.

Tools allow the AI to:
- Create chord progressions with proper voice leading
- Add rhythmic variations to existing patterns
- Set dynamics and articulations for sections
- Apply musical transformations
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class FunctionDeclaration:
    """Represents a Gemini function declaration.

    Attributes:
        name: Function name (must be alphanumeric with underscores)
        description: What the function does
        parameters: JSON Schema for parameters object
    """

    name: str
    description: str
    parameters: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert to Gemini API format.

        Returns:
            Dictionary matching Gemini's FunctionDeclaration schema
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


# =============================================================================
# Music Generation Tools
# =============================================================================

def create_chord_tool() -> FunctionDeclaration:
    """Tool for creating chord progressions with voice leading.

    Returns:
        FunctionDeclaration for the create_chord tool
    """
    return FunctionDeclaration(
        name="create_chord",
        description=(
            "Create a chord with proper voice leading from the previous chord. "
            "Use this to build harmonic progressions that flow smoothly. "
            "Returns the chord notes with recommended voicing."
        ),
        parameters={
            "type": "object",
            "properties": {
                "root": {
                    "type": "string",
                    "description": (
                        "Root note of the chord (e.g., 'C', 'F#', 'Bb'). "
                        "Use sharps for black keys."
                    ),
                    "pattern": r"^[A-G][#b]?$",
                },
                "quality": {
                    "type": "string",
                    "description": "Chord quality",
                    "enum": [
                        "major",
                        "minor",
                        "diminished",
                        "augmented",
                        "major_7",
                        "minor_7",
                        "dominant_7",
                        "half_diminished_7",
                        "fully_diminished_7",
                        "suspended_2",
                        "suspended_4",
                    ],
                },
                "inversion": {
                    "type": "integer",
                    "description": "Chord inversion (0=root position, 1=first, 2=second)",
                    "minimum": 0,
                    "maximum": 2,
                },
                "duration": {
                    "type": "number",
                    "description": "Duration in quarter notes",
                    "minimum": 0.25,
                },
                "voicing": {
                    "type": "string",
                    "description": "Preferred voicing style",
                    "enum": ["open", "closed", "wide", "compact"],
                },
                "previous_chord": {
                    "type": "string",
                    "description": (
                        "Previous chord root and quality for voice leading "
                        "(e.g., 'C_major', 'F_minor_7'). "
                        "Omit for first chord."
                    ),
                },
            },
            "required": ["root", "quality", "duration"],
        },
    )


def add_rhythm_variation_tool() -> FunctionDeclaration:
    """Tool for adding rhythmic variation to a pattern.

    Returns:
        FunctionDeclaration for the add_rhythm_variation tool
    """
    return FunctionDeclaration(
        name="add_rhythm_variation",
        description=(
            "Add rhythmic variation to an existing musical pattern. "
            "Use this to create interest through syncopation, accent patterns, "
            "or rhythmic modulation while preserving the melodic content."
        ),
        parameters={
            "type": "object",
            "properties": {
                "variation_type": {
                    "type": "string",
                    "description": "Type of rhythmic variation to apply",
                    "enum": [
                        "syncopation",
                        "accent_shift",
                        "dotting",
                        "tripoliet",
                        "hemiola",
                        "delayed_attack",
                        "anticipation",
                        "subdivision_change",
                    ],
                },
                "target_part": {
                    "type": "string",
                    "description": "Which part to apply variation to (e.g., 'melody', 'bass')",
                },
                "measure_start": {
                    "type": "integer",
                    "description": "Starting measure number (1-indexed)",
                    "minimum": 1,
                },
                "measure_end": {
                    "type": "integer",
                    "description": "Ending measure number (1-indexed)",
                    "minimum": 1,
                },
                "intensity": {
                    "type": "string",
                    "description": "How subtle or pronounced the variation should be",
                    "enum": ["subtle", "moderate", "pronounced"],
                },
            },
            "required": ["variation_type", "target_part", "measure_start", "measure_end"],
        },
    )


def set_dynamic_tool() -> FunctionDeclaration:
    """Tool for setting dynamics for a section.

    Returns:
        FunctionDeclaration for the set_dynamic tool
    """
    return FunctionDeclaration(
        name="set_dynamic",
        description=(
            "Set the dynamic level (volume) for a section of music. "
            "Use this to create expressive contrast between sections "
            "or build tension through crescendo."
        ),
        parameters={
            "type": "object",
            "properties": {
                "dynamic": {
                    "type": "string",
                    "description": "Dynamic marking",
                    "enum": [
                        "pp",
                        "p",
                        "mp",
                        "mf",
                        "f",
                        "ff",
                        "sfz",
                        "fp",
                    ],
                },
                "target_part": {
                    "type": "string",
                    "description": "Which part to apply to (e.g., 'melody', 'bass'), or 'all'",
                },
                "measure_start": {
                    "type": "integer",
                    "description": "Starting measure number (1-indexed)",
                    "minimum": 1,
                },
                "measure_end": {
                    "type": "integer",
                    "description": "Ending measure number (1-indexed), or omit for sustained",
                    "minimum": 1,
                },
                "transition": {
                    "type": "string",
                    "description": "How to transition to this dynamic",
                    "enum": ["immediate", "crescendo", "diminuendo", "gradual"],
                },
                "transition_duration": {
                    "type": "number",
                    "description": "Duration of transition in quarter notes",
                    "minimum": 0,
                },
            },
            "required": ["dynamic", "target_part", "measure_start"],
        },
    )


def add_ornament_tool() -> FunctionDeclaration:
    """Tool for adding ornaments to a note.

    Returns:
        FunctionDeclaration for the add_ornament tool
    """
    return FunctionDeclaration(
        name="add_ornament",
        description=(
            "Add a musical ornament to a specific note. "
            "Ornaments add expressive detail and technical flourish."
        ),
        parameters={
            "type": "object",
            "properties": {
                "ornament_type": {
                    "type": "string",
                    "description": "Type of ornament to add",
                    "enum": [
                        "trill",
                        "mordent",
                        "turn",
                        "grace_note",
                        "grace_note_group",
                        "slide",
                        "glissando",
                        "tremolo",
                    ],
                },
                "target_part": {
                    "type": "string",
                    "description": "Which part contains the note",
                },
                "measure": {
                    "type": "integer",
                    "description": "Measure number containing the note",
                    "minimum": 1,
                },
                "beat": {
                    "type": "number",
                    "description": "Beat position within the measure",
                    "minimum": 0,
                },
                "ornament_duration": {
                    "type": "number",
                    "description": "Duration of the ornament in quarter notes (if applicable)",
                    "minimum": 0.0625,  # 64th note
                },
            },
            "required": ["ornament_type", "target_part", "measure", "beat"],
        },
    )


def create_section_tool() -> FunctionDeclaration:
    """Tool for defining a musical section.

    Returns:
        FunctionDeclaration for the create_section tool
    """
    return FunctionDeclaration(
        name="create_section",
        description=(
            "Define a new musical section with specific characteristics. "
            "Use this to organize the piece into clear structural sections "
            "like verse, chorus, bridge, etc."
        ),
        parameters={
            "type": "object",
            "properties": {
                "section_type": {
                    "type": "string",
                    "description": "Type of section",
                    "enum": [
                        "intro",
                        "verse",
                        "pre_chorus",
                        "chorus",
                        "bridge",
                        "solo",
                        "outro",
                        "interlude",
                        "development",
                        "recapitulation",
                        "coda",
                    ],
                },
                "measure_start": {
                    "type": "integer",
                    "description": "Starting measure number (1-indexed)",
                    "minimum": 1,
                },
                "measure_count": {
                    "type": "integer",
                    "description": "Number of measures in this section",
                    "minimum": 4,
                },
                "tempo": {
                    "type": "number",
                    "description": "Tempo in BPM for this section (optional)",
                    "minimum": 40,
                    "maximum": 240,
                },
                "time_signature_numerator": {
                    "type": "integer",
                    "description": "Top number of time signature (optional)",
                    "minimum": 2,
                    "maximum": 16,
                },
                "time_signature_denominator": {
                    "type": "integer",
                    "description": "Bottom number of time signature (optional, 2/4/8/16)",
                    "minimum": 2,
                    "maximum": 16,
                },
                "dynamic_level": {
                    "type": "string",
                    "description": "Starting dynamic level",
                    "enum": ["pp", "p", "mp", "mf", "f", "ff"],
                },
                "description": {
                    "type": "string",
                    "description": "Brief description of this section's character",
                },
            },
            "required": ["section_type", "measure_start", "measure_count"],
        },
    )


def add_counter_melody_tool() -> FunctionDeclaration:
    """Tool for generating a counter-melody.

    Returns:
        FunctionDeclaration for the add_counter_melody tool
    """
    return FunctionDeclaration(
        name="add_counter_melody",
        description=(
            "Generate a counter-melody that complements the main melody. "
            "The counter-melody will use contrary motion and rhythmic "
            "contrast to enhance the main melody."
        ),
        parameters={
            "type": "object",
            "properties": {
                "target_measures": {
                    "type": "string",
                    "description": (
                        "Measure range for counter-melody "
                        "(e.g., '1-16', '17-32')"
                    ),
                },
                "interval_type": {
                    "type": "string",
                    "description": "Interval relationship to main melody",
                    "enum": [
                        "thirds",
                        "sixths",
                        "tenths",
                        "contrary",
                        "parallel",
                        "oblique",
                    ],
                },
                "rhythmic_activity": {
                    "type": "string",
                    "description": "How active the counter-melody should be",
                    "enum": ["sparse", "moderate", "active", "constant"],
                },
                "instrument": {
                    "type": "string",
                    "description": "MIDI program number or name for counter-melody",
                },
            },
            "required": ["target_measures", "interval_type", "rhythmic_activity"],
        },
    )


def apply_transformation_tool() -> FunctionDeclaration:
    """Tool for applying transformations to existing music.

    Returns:
        FunctionDeclaration for the apply_transformation tool
    """
    return FunctionDeclaration(
        name="apply_transformation",
        description=(
            "Apply a musical transformation to an existing part. "
            "Use this to develop motifs and create variation."
        ),
        parameters={
            "type": "object",
            "properties": {
                "transformation": {
                    "type": "string",
                    "description": "Type of transformation to apply",
                    "enum": [
                        "transpose",
                        "invert",
                        "retrograde",
                        "augmentation",
                        "diminution",
                        "sequence_up",
                        "sequence_down",
                        "fragmentation",
                        "ornamentation",
                    ],
                },
                "target_part": {
                    "type": "string",
                    "description": "Which part to transform",
                },
                "source_measures": {
                    "type": "string",
                    "description": "Source measure range (e.g., '1-8')",
                },
                "target_measures": {
                    "type": "string",
                    "description": "Where to apply the transformation (e.g., '9-16')",
                },
                "interval": {
                    "type": "integer",
                    "description": (
                        "Interval for transposition/sequence in semitones. "
                        "Positive=up, negative=down"
                    ),
                },
            },
            "required": ["transformation", "target_part", "target_measures"],
        },
    )


# =============================================================================
# Tool Collections
# =============================================================================

def get_all_tools() -> list[FunctionDeclaration]:
    """Get all available music generation tools.

    Returns:
        List of all function declarations
    """
    return [
        create_chord_tool(),
        add_rhythm_variation_tool(),
        set_dynamic_tool(),
        add_ornament_tool(),
        create_section_tool(),
        add_counter_melody_tool(),
        apply_transformation_tool(),
    ]


def get_harmony_tools() -> list[FunctionDeclaration]:
    """Get harmony-related tools only.

    Returns:
        List of harmony function declarations
    """
    return [
        create_chord_tool(),
        add_counter_melody_tool(),
    ]


def get_expression_tools() -> list[FunctionDeclaration]:
    """Get expression and articulation tools only.

    Returns:
        List of expression function declarations
    """
    return [
        set_dynamic_tool(),
        add_ornament_tool(),
        add_rhythm_variation_tool(),
    ]


def get_structural_tools() -> list[FunctionDeclaration]:
    """Get structural/form tools only.

    Returns:
        List of structural function declarations
    """
    return [
        create_section_tool(),
        apply_transformation_tool(),
    ]


# =============================================================================
# Tool Call Result Types
# =============================================================================

@dataclass
class ToolCallResult:
    """Result from executing a tool call.

    Attributes:
        tool_name: Name of the tool that was called
        arguments: The arguments passed to the tool
        result: The result of the tool execution
        success: Whether the tool executed successfully
        error: Error message if execution failed
    """

    tool_name: str
    arguments: dict[str, Any]
    result: Any | None
    success: bool
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API response.

        Returns:
            Dictionary representation
        """
        return {
            "tool_name": self.tool_name,
            "arguments": self.arguments,
            "result": self.result,
            "success": self.success,
            "error": self.error,
        }


def format_tools_for_gemini(
    tools: list[FunctionDeclaration] | None = None,
) -> dict[str, Any] | None:
    """Format tools for Gemini API call.

    Args:
        tools: List of function declarations. If None, returns None.

    Returns:
        Formatted tools dict for Gemini API, or None if tools is empty/None
    """
    if not tools:
        return None

    return {
        "function_declarations": [tool.to_dict() for tool in tools],
    }


# =============================================================================
# Default tool set for composition
# =============================================================================

DEFAULT_COMPOSITION_TOOLS = get_all_tools()

"""Default set of tools used for standard composition generation.

This provides the AI with options for:
- Harmonic construction (create_chord)
- Rhythmic interest (add_rhythm_variation)
- Dynamic expression (set_dynamic)
- Ornamentation (add_ornament)
- Structural organization (create_section)
- Texture development (add_counter_melody)
- Motivic development (apply_transformation)
"""
