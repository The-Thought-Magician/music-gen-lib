"""Gemini AI client for music composition.

This module provides the interface to Google Gemini 2.5 Flash Lite
for interpreting natural language prompts and generating orchestration plans.
"""

from __future__ import annotations
import os
import json
from typing import Optional, List
from pathlib import Path
import time

try:
    from google import genai
    from google.genai import types
    from google.api_core.exceptions import (
        GoogleAPIError,
        InvalidArgument,
        ResourceExhausted,
        ServiceUnavailable
    )
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    GoogleAPIError = Exception
    genai = None

from musicgen.ai.models import (
    OrchestrationPlan,
    Section,
    InstrumentAssignment,
    DynamicsPlan,
    TextureChange,
    InstrumentRole,
    InstrumentSection,
    DynamicsLevel,
    ScaleType,
    FormType,
    ORCHESTRAL_INSTRUMENTS,
)


class GeminiComposer:
    """AI composer using Google Gemini for music generation.

    This client interprets natural language prompts and generates
    structured orchestration plans for music composition.
    """

    # Default model
    DEFAULT_MODEL = "gemini-2.0-flash-exp"  # or "gemini-2.5-flash-lite-exp"

    # Maximum retries for API calls
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0  # seconds

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 8192
    ):
        """Initialize the Gemini composer.

        Args:
            api_key: Google API key. If None, reads from GOOGLE_API_KEY env var.
            model: Model name to use. If None, uses DEFAULT_MODEL.
            temperature: Sampling temperature (0.0-1.0).
            max_output_tokens: Maximum output tokens.

        Raises:
            RuntimeError: If google-genai is not installed.
            ValueError: If no API key is provided.
        """
        if not GENAI_AVAILABLE:
            raise RuntimeError(
                "google-genai package is required. Install with:\n"
                "  uv add --optional ai google-genai"
            )

        # Get API key
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Google API key required. Set GOOGLE_API_KEY environment "
                "variable or pass api_key parameter."
            )

        # Configure client
        genai.configure(api_key=self.api_key)

        self.model_name = model or self.DEFAULT_MODEL
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.client = genai.Client()

        # Generation config
        self.generation_config = types.GenerateContentConfig(
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
            response_mime_type="application/json",
        )

    def extract_parameters(
        self,
        prompt: str,
        duration_seconds: int = 180,
        form_type: Optional[str] = None
    ) -> OrchestrationPlan:
        """Extract musical parameters from a natural language prompt.

        Args:
            prompt: User's description of desired music.
            duration_seconds: Target duration in seconds.
            form_type: Optional form type hint.

        Returns:
            OrchestrationPlan with all parameters.

        Raises:
            GoogleAPIError: If API call fails.
            ValueError: If response is invalid.
        """
        system_prompt = self._build_system_prompt(duration_seconds, form_type)
        user_prompt = self._build_user_prompt(prompt)

        response = self._call_gemini(system_prompt, user_prompt)
        plan = self._parse_response(response)

        return plan

    def _build_system_prompt(
        self,
        duration_seconds: int,
        form_type: Optional[str]
    ) -> str:
        """Build the system prompt for Gemini.

        Args:
            duration_seconds: Target duration.
            form_type: Optional form type.

        Returns:
            System prompt string.
        """
        form_hint = f"\n- Form type: {form_type}" if form_type else ""

        return f"""You are an expert orchestral composer and music theory specialist.
Given a user's description, generate a complete orchestration plan for a {duration_seconds}-second composition.

Return ONLY a valid JSON object with this exact structure:

{{
  "title": "composition title",
  "duration_seconds": {duration_seconds},
  "key": "C",
  "key_type": "major",
  "scale_type": "major",
  "tempo": 120,
  "time_signature": "4/4",
  "form_type": "binary",
  "mood_description": "brief mood description",
  "has_intro": false,
  "has_outro": false,
  "sections": [
    {{
      "name": "A",
      "duration_seconds": {duration_seconds // 2},
      "key": "C",
      "key_type": "major",
      "scale_type": "major",
      "tempo": 120,
      "time_signature": "4/4",
      "mood_description": "mood for this section",
      "instrumentation": ["all"],
      "melody_source": "new",
      "harmonic_center": "tonic",
      "dynamics_start": "mf",
      "dynamics_end": "f",
      "texture": "homophonic"
    }},
    {{
      "name": "B",
      "duration_seconds": {duration_seconds // 2},
      "key": "G",
      "key_type": "major",
      "scale_type": "major",
      "tempo": 120,
      "time_signature": "4/4",
      "mood_description": "contrasting mood",
      "instrumentation": ["all"],
      "melody_source": "new",
      "harmonic_center": "dominant",
      "dynamics_start": "mf",
      "dynamics_end": "mf",
      "texture": "homophonic"
    }}
  ],
  "instruments": [
    {{"name": "violin", "section": "strings", "role": "melody", "dynamics": "f", "midi_program": 40}},
    {{"name": "viola", "section": "strings", "role": "harmony", "dynamics": "mf", "midi_program": 41}},
    {{"name": "cello", "section": "strings", "role": "harmony", "dynamics": "mf", "midi_program": 42}}
  ],
  "dynamics_plan": {{
    "initial_dynamic": "mf",
    "climax_dynamic": "f",
    "final_dynamic": "mp",
    "climax_point": 0.75,
    "has_crescendo": true,
    "has_diminuendo": true
  }},
  "texture_changes": []
}}

MUSICAL RULES:
1. Key signatures: Use C, G, D, A, E, B, F, Bb, Eb, Ab (most common)
2. Key types: "major" or "minor"
3. Scale types: major, minor, harmonic_minor, melodic_minor, dorian, phrygian, lydian, mixolydian, locrian
4. Tempo: 40-200 BPM (slower=40-60, moderate=60-120, fast=120-200)
5. Time signatures: "4/4", "3/4", "6/8", "2/4", "cut-time"
6. Form types: binary, ternary, rondo, sonata, through_composed
7. Dynamics: pp, p, mp, mf, f, ff, fff
8. Instrument roles: melody, harmony, bass, accompaniment, countermelody
9. Instrument sections: strings, woodwinds, brass, percussion, keyboard
10. Texture: homophonic, polyphonic, melody+accompaniment
11. MIDI programs: violin=40, viola=41, cello=42, bass=43, flute=73, clarinet=71, oboe=68, bassoon=70, trumpet=56, horn=60, trombone=57, timpani=47, piano=0

COMMON INSTRUMENTS:
- Strings: violin, viola, cello, double_bass
- Woodwinds: flute, clarinet, oboe, bassoon
- Brass: trumpet, french_horn, trombone
- Percussion: timpani
- Keyboard: piano

FORM GUIDELINES:
- Binary (AB): Section A (tonic) -> Section B (dominant/relative)
- Ternary (ABA): Section A -> Section B (contrast) -> Section A (return)
- Rondo (ABACA): Alternating refrain with episodes
- Sonata: Exposition -> Development -> Recapitulation
- Through-composed: Continuous with no literal repetition{form_hint}

Ensure total duration equals {duration_seconds} seconds across all sections."""

    def _build_user_prompt(self, user_prompt: str) -> str:
        """Build the user prompt.

        Args:
            user_prompt: Raw user input.

        Returns:
            Formatted user prompt.
        """
        return f"""User prompt: "{user_prompt}"

Generate the orchestration plan JSON. Return ONLY the JSON, no additional text."""

    def _call_gemini(self, system_prompt: str, user_prompt: str) -> str:
        """Call Gemini API with retry logic.

        Args:
            system_prompt: System instructions.
            user_prompt: User query.

        Returns:
            Response text.

        Raises:
            GoogleAPIError: If all retries fail.
        """
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=user_prompt,
                    config=self.generation_config,
                )
                return response.text

            except ResourceExhausted:
                # Quota exceeded, wait longer
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY * (2 ** attempt))
                else:
                    raise

            except (ServiceUnavailable, InvalidArgument) as e:
                # Temporary error or invalid request
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY * (attempt + 1))
                else:
                    raise

            except GoogleAPIError as e:
                # Other API errors
                raise

        raise GoogleAPIError("Max retries exceeded")

    def _parse_response(self, response: str) -> OrchestrationPlan:
        """Parse Gemini response into OrchestrationPlan.

        Args:
            response: JSON response string.

        Returns:
            OrchestrationPlan object.

        Raises:
            ValueError: If response is invalid.
        """
        # Clean up response
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()

        # Parse JSON
        try:
            data = json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}\n\nResponse was:\n{response}")

        # Convert to OrchestrationPlan
        try:
            return self._json_to_plan(data)
        except Exception as e:
            raise ValueError(f"Failed to parse plan: {e}")

    def _json_to_plan(self, data: dict) -> OrchestrationPlan:
        """Convert JSON dict to OrchestrationPlan.

        Args:
            data: Parsed JSON data.

        Returns:
            OrchestrationPlan object.
        """
        # Convert sections
        sections = []
        for s_data in data.get("sections", []):
            sections.append(Section(**s_data))

        # Convert instruments
        instruments = []
        for i_data in data.get("instruments", []):
            # Map string enums to actual enums
            if "section" in i_data and isinstance(i_data["section"], str):
                i_data["section"] = InstrumentSection(i_data["section"])
            if "role" in i_data and isinstance(i_data["role"], str):
                i_data["role"] = InstrumentRole(i_data["role"])
            if "dynamics" in i_data and isinstance(i_data["dynamics"], str):
                i_data["dynamics"] = DynamicsLevel(i_data["dynamics"])
            instruments.append(InstrumentAssignment(**i_data))

        # Convert dynamics plan
        dp_data = data.get("dynamics_plan", {})
        if "initial_dynamic" in dp_data and isinstance(dp_data["initial_dynamic"], str):
            dp_data["initial_dynamic"] = DynamicsLevel(dp_data["initial_dynamic"])
        if "climax_dynamic" in dp_data and isinstance(dp_data["climax_dynamic"], str):
            dp_data["climax_dynamic"] = DynamicsLevel(dp_data["climax_dynamic"])
        if "final_dynamic" in dp_data and isinstance(dp_data["final_dynamic"], str):
            dp_data["final_dynamic"] = DynamicsLevel(dp_data["final_dynamic"])
        dynamics_plan = DynamicsPlan(**dp_data)

        # Convert form type
        form_type = data.get("form_type", "binary")
        if isinstance(form_type, str):
            form_type = FormType(form_type)

        # Convert scale type
        scale_type = data.get("scale_type", "major")
        if isinstance(scale_type, str):
            scale_type = ScaleType(scale_type)

        # Create main plan
        plan_data = {
            "title": data.get("title", "Untitled"),
            "duration_seconds": data.get("duration_seconds", 180),
            "key": data.get("key", "C"),
            "key_type": data.get("key_type", "major"),
            "scale_type": scale_type,
            "tempo": data.get("tempo", 120),
            "time_signature": data.get("time_signature", "4/4"),
            "sections": sections,
            "instruments": instruments,
            "form_type": form_type,
            "mood_description": data.get("mood_description", ""),
            "dynamics_plan": dynamics_plan,
            "texture_changes": data.get("texture_changes", []),
            "repeat_sections": data.get("repeat_sections", False),
            "has_intro": data.get("has_intro", False),
            "has_outro": data.get("has_outro", False),
        }

        return OrchestrationPlan(**plan_data)


def extract_from_prompt(
    prompt: str,
    api_key: Optional[str] = None,
    duration_seconds: int = 180
) -> OrchestrationPlan:
    """Convenience function to extract parameters from a prompt.

    Args:
        prompt: User's natural language description.
        api_key: Optional API key (uses GOOGLE_API_KEY if None).
        duration_seconds: Target duration.

    Returns:
        OrchestrationPlan for the composition.

    Raises:
        RuntimeError: If google-genai is not available.
        ValueError: If API key is missing or response is invalid.
    """
    composer = GeminiComposer(api_key=api_key)
    return composer.extract_parameters(prompt, duration_seconds)


def check_gemini_available() -> dict:
    """Check if Gemini API is available.

    Returns:
        Dict with availability info:
        - available: bool
        - api_key_set: bool
        - package_installed: bool
    """
    return {
        "available": GENAI_AVAILABLE,
        "api_key_set": bool(os.environ.get("GOOGLE_API_KEY")),
        "package_installed": GENAI_AVAILABLE,
    }
