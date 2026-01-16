"""AI client for Gemini 2.5 Pro."""

from musicgen.ai_client.client import (
    GeminiClient,
    check_availability,
    generate_composition,
)
from musicgen.ai_client.exceptions import (
    AIClientError,
    APICallError,
    APIKeyError,
    InvalidResponseError,
    RateLimitError,
)
from musicgen.ai_client.prompts import PromptBuilder, build_prompt
from musicgen.ai_client.tools import (
    DEFAULT_COMPOSITION_TOOLS,
    FunctionDeclaration,
    ToolCallResult,
    add_counter_melody_tool,
    add_ornament_tool,
    add_rhythm_variation_tool,
    apply_transformation_tool,
    create_chord_tool,
    create_section_tool,
    format_tools_for_gemini,
    get_all_tools,
    get_expression_tools,
    get_harmony_tools,
    get_structural_tools,
    set_dynamic_tool,
)

__all__ = [
    # Client
    "GeminiClient",
    "generate_composition",
    "check_availability",
    # Prompts
    "PromptBuilder",
    "build_prompt",
    # Exceptions
    "AIClientError",
    "APIKeyError",
    "RateLimitError",
    "APICallError",
    "InvalidResponseError",
    # Tools - Core classes
    "FunctionDeclaration",
    "ToolCallResult",
    "DEFAULT_COMPOSITION_TOOLS",
    "format_tools_for_gemini",
    # Tools - Individual tool functions
    "create_chord_tool",
    "add_rhythm_variation_tool",
    "set_dynamic_tool",
    "add_ornament_tool",
    "create_section_tool",
    "add_counter_melody_tool",
    "apply_transformation_tool",
    # Tools - Collections
    "get_all_tools",
    "get_harmony_tools",
    "get_expression_tools",
    "get_structural_tools",
]
