"""AI-powered composition module.

This module provides intelligent music generation using Google Gemini
to interpret natural language prompts and generate orchestration parameters.
"""

from musicgen.ai.client import GeminiComposer
from musicgen.ai.composer import build_composition_from_plan
from musicgen.ai.models import (
    DynamicsPlan,
    InstrumentAssignment,
    OrchestrationPlan,
    Section,
    TextureChange,
)

__all__ = [
    "OrchestrationPlan",
    "Section",
    "InstrumentAssignment",
    "DynamicsPlan",
    "TextureChange",
    "GeminiComposer",
    "build_composition_from_plan",
]
