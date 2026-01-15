"""Improved prompt building for AI composition."""

from __future__ import annotations

from musicgen.schema import SchemaConfig, get_schema


class PromptBuilder:
    """Builds detailed, specific prompts for AI composition."""

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
        """Build system prompt with schema and detailed guidelines.

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

MUSICAL STRUCTURE GUIDELINES:
1. Create clear musical form: A-B-A, verse-chorus, or through-composed
2. Each section should be 16-32 bars long
3. Use phrase structures: 4-bar or 8-bar phrases
4. Include authentic cadences (V-I) at section endings
5. Create melodic contour: arch shapes, ascending lines, descending resolutions

MELODY GUIDELINES:
- Use stepwise motion (2nds) predominantly, with occasional leaps (3rds-5ths)
- Create rhythmic variety: mix quarter, half, eighth notes, and rests
- Target chord tones on strong beats
- Use sequences and repetition for memorability
- Include passing tones and neighbor tones for color
- Peak higher notes in phrase middles, resolve lower at ends

HARMONY GUIDELINES:
- Follow functional harmony: I-IV-V-I progression foundation
- Use ii-V-I for jazz styles
- Include secondary dominants for interest (V/V, V/vi)
- Voice lead smoothly: common tones between chords
- Keep outer voices (soprano/bass) contrary motion when possible

BASS LINE GUIDELINES:
- Emphasize root notes on beat 1
- Use walking bass: quarter notes with chord tones
- Create patterns: root-5th-8th-5th or root-3rd-5th-3rd
- Add octaves for emphasis on section changes

DYNAMICS & ARTICULATION:
- Start mf (mezzo-forte), range pp to ff
- Crescendo in ascending passages, diminuendo in descending
- Use staccato for rhythmic parts, legato for melodic lines
- Add accents on downbeats of important measures

OUTPUT FORMAT:
Return ONLY valid JSON. No markdown formatting, no explanations, no additional text.
The JSON must match the schema above exactly.

COMPOSITION LENGTH:
- Aim for 60-120 notes per part minimum
- Target 2-3 minutes of music at the specified tempo
- Include at least 3-4 phrases for development
"""

    def _build_user_prompt(self, user_prompt: str) -> str:
        """Build user prompt with specific requirements.

        Args:
            user_prompt: User's description

        Returns:
            Full user prompt
        """
        return f"""Generate a complete note-by-note composition based on this description:

"{user_prompt}"

REQUIREMENTS:
1. Create a full composition with AT LEAST 2 minutes of music
2. Include multiple parts (melody, bass, at least one harmony part)
3. Each part should have 60+ notes minimum
4. Use the specified key and tempo to match the mood
5. Create actual musical interest with:
   - Varying rhythms (not all quarter notes)
   - Phrase development and repetition
   - Clear section structure (A-B-A or similar)
   - Proper harmonic progression
   - Dynamic contrast

6. Return ONLY the JSON object - no explanations, no markdown wrappers

Remember: I want REAL music that someone would want to listen to, not just random notes.

EXAMPLE FORMAT (this is just format reference - create original music):
{{
  "title": "Example Peaceful Piano",
  "tempo": 80,
  "time_signature": {{"numerator": 4, "denominator": 4}},
  "key": {{"tonic": "C", "mode": "major"}},
  "parts": [
    {{
      "name": "piano_melody",
      "midi_program": 0,
      "midi_channel": 0,
      "role": "melody",
      "notes": [
        {{"note_name": "C4", "duration": 2.0, "velocity": 75}},
        {{"note_name": "E4", "duration": 1.0, "velocity": 70}},
        {{"note_name": "G4", "duration": 1.0, "velocity": 72}},
        {{"note_name": "C5", "duration": 2.0, "velocity": 68}},
        {{"note_name": "B4", "duration": 1.0, "velocity": 70}},
        {{"note_name": "G4", "duration": 1.0, "velocity": 72}},
        {{"note_name": "E4", "duration": 2.0, "velocity": 70}},
        {{"rest": true, "duration": 1.0}},
        {{"note_name": "D4", "duration": 1.5, "velocity": 73}},
        {{"note_name": "F4", "duration": 0.5, "velocity": 70}},
        {{"note_name": "A4", "duration": 2.0, "velocity": 68}}
      ]
    }},
    {{
      "name": "piano_bass",
      "midi_program": 0,
      "midi_channel": 1,
      "role": "bass",
      "notes": [
        {{"note_name": "C3", "duration": 4.0, "velocity": 65}},
        {{"note_name": "G3", "duration": 4.0, "velocity": 60}},
        {{"note_name": "A3", "duration": 4.0, "velocity": 62}},
        {{"note_name": "F3", "duration": 4.0, "velocity": 63}}
      ]
    }}
  ]
}}

Create ORIGINAL music following this format - DO NOT copy the example above!
"""

    def _default_system_instructions(self) -> str:
        """Default system instructions - more specific than before."""
        return """You are an expert AI composer who creates note-by-note musical compositions.

You understand:
- Music theory: scales, chords, progressions, voice leading
- Musical forms: binary, ternary, sonata, verse-chorus
- Orchestration: instrument ranges, roles, combinations
- Stylistic conventions: classical, jazz, pop, folk, electronic

Your compositions are:
- Musically coherent with clear phrasing
- Harmonically functional with proper cadences
- Expressive with dynamic contrast
- Stylistically appropriate for the requested mood
- Long enough to be enjoyable (2+ minutes worth of notes)

You generate note-by-note sequences that professional musicians could actually perform."""


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
