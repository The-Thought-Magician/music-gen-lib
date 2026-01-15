"""Prompt building for AI composition."""

from __future__ import annotations

from musicgen.schema import SchemaConfig, get_schema


class PromptBuilder:
    """Builds prompts for AI composition."""

    def __init__(
        self,
        schema_config: SchemaConfig | None = None,
        system_instructions: str | None = None
    ):
        """Initialize prompt builder.

        Args:
            schema_config: Optional schema configuration
            system_instructions: Optional custom system instructions
        """
        self.schema_config = schema_config
        self.system_instructions = system_instructions or self._default_system_instructions()

    def build_prompt(
        self,
        user_prompt: str,
        schema: str | None = None
    ) -> tuple[str, str]:
        """Build system and user prompts.

        Args:
            user_prompt: User's description of desired music
            schema: Optional schema YAML (generated if not provided)

        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        if schema is None:
            schema = get_schema(self.schema_config)

        system_prompt = self._build_system_prompt(schema)
        full_user_prompt = self._build_user_prompt(user_prompt)

        return system_prompt, full_user_prompt

    def _build_system_prompt(self, schema: str) -> str:
        """Build system prompt with schema.

        Args:
            schema: YAML schema string

        Returns:
            System prompt
        """
        return f"""{self.system_instructions}

COMPOSITION SCHEMA:
You must generate compositions that follow this schema exactly:

```yaml
{schema}
```

OUTPUT FORMAT:
Return ONLY valid JSON. No markdown formatting, no explanations, no additional text.
The JSON must match the schema above exactly.

COMPOSITION GUIDELINES:
1. Generate musically coherent note sequences
2. Consider voice leading and harmonic progressions
3. Create balanced phrases with proper cadences
4. Use dynamics to create expression
5. Match the mood/style described in the user prompt
6. Keep total duration reasonable (typically 30-180 seconds)
"""

    def _build_user_prompt(self, user_prompt: str) -> str:
        """Build user prompt.

        Args:
            user_prompt: User's description

        Returns:
            Full user prompt
        """
        return f"""Generate a complete composition based on this description:

"{user_prompt}"

Return ONLY the JSON object matching the schema. Do not include any other text."""

    def _default_system_instructions(self) -> str:
        """Default system instructions."""
        return """You are an expert AI composer capable of generating complete musical compositions.

You create note-by-note compositions that follow standard music theory while being creative and expressive.

Your compositions include:
- Melodically interesting lines with proper phrasing
- Harmonically coherent progressions
- Appropriate voice leading
- Dynamic markings for expression
- Proper instrumental roles (melody, harmony, bass, accompaniment)

You are fluent in all musical styles: classical, jazz, pop, folk, electronic, etc."""


def build_prompt(
    user_prompt: str,
    schema: str | None = None,
    schema_config: SchemaConfig | None = None
) -> tuple[str, str]:
    """Convenience function to build prompts.

    Args:
        user_prompt: User's description
        schema: Optional schema YAML
        schema_config: Optional schema configuration

    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    builder = PromptBuilder(schema_config=schema_config)
    return builder.build_prompt(user_prompt, schema)
