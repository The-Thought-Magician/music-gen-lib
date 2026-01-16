"""Improved prompt building for AI composition."""

from __future__ import annotations

from musicgen.ai_client.tools import (
    DEFAULT_COMPOSITION_TOOLS,
    FunctionDeclaration,
)
from musicgen.schema import SchemaConfig, get_schema


class PromptBuilder:
    """Builds detailed, specific prompts for AI composition."""

    def __init__(
        self,
        schema_config: SchemaConfig | None = None,
        system_instructions: str | None = None,
        tools: list[FunctionDeclaration] | None = None,
    ):
        """Initialize prompt builder.

        Args:
            schema_config: Optional schema configuration
            system_instructions: Optional custom system instructions
            tools: Optional list of function declarations for tool calling
        """
        self.schema_config = schema_config
        self.tools = tools
        self.system_instructions = system_instructions or self._default_system_instructions(tools)

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
        # Add tool usage instructions if tools are provided
        tool_instructions = self._build_tool_instructions() if self.tools else ""

        return f"""{self.system_instructions}

{tool_instructions}
COMPOSITION SCHEMA:
You must generate compositions that follow this schema exactly:

```yaml
{schema}
```

CRITICAL DURATION REQUIREMENTS:
You MUST generate 2-3 minutes of music. Here is how to calculate this:

Duration (seconds) = (Total quarter notes in part × 60) / Tempo

For 2 minutes at 120 BPM: 240 quarter notes needed
For 2 minutes at 70 BPM: 140 quarter notes needed
For 3 minutes at 120 BPM: 360 quarter notes needed
For 3 minutes at 70 BPM: 210 quarter notes needed

MINIMUM NOTE COUNTS BY PART:
- Melody parts: 150-300 notes minimum (depending on tempo)
- Harmony parts: 120-250 notes minimum
- Bass parts: 80-150 notes minimum (typically longer durations)
- Accompaniment parts: 100-200 notes minimum

DO NOT generate compositions shorter than 2 minutes. Always err on the side of MORE notes.

MUSICAL STRUCTURE GUIDELINES:
1. Create clear musical form: A-B-A, verse-chorus, or through-composed
2. Each section should be 16-32 bars long (64-128 quarter notes at 4/4)
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
- AVOID excessive rests - music should have flowing continuity

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

VALID PART ROLES (use exactly these values):
- "melody" - Main melodic line
- "harmony" - Harmonic support
- "bass" - Bass line
- "accompaniment" - Background accompaniment
- "countermelody" - Secondary melodic line
- "pad" - Sustained chord pad
- "percussion" - Percussion parts

DO NOT combine roles (e.g., don't use "harmony_bass"). Use ONE valid role per part.

POLYPHONY (Chords and Simultaneous Notes) - CRITICAL:
start_time is REQUIRED for ALL notes in harmony/accompaniment/pad parts. You MUST specify start_time for every note to enable proper polyphony.

HARMONY PARTS MUST USE start_time FOR CHORDS - notes without start_time will not play simultaneously

To create chords, set the same start_time for multiple notes:
- C Major chord (C-E-G) at beat 1:
  {{"note_name": "C4", "start_time": 0.0, "duration": 2.0, "velocity": 75}}
  {{"note_name": "E4", "start_time": 0.0, "duration": 2.0, "velocity": 75}}
  {{"note_name": "G4", "start_time": 0.0, "duration": 2.0, "velocity": 75}}

- D Minor chord at beat 3:
  {{"note_name": "D4", "start_time": 2.0, "duration": 2.0, "velocity": 75}}
  {{"note_name": "F4", "start_time": 2.0, "duration": 2.0, "velocity": 75}}
  {{"note_name": "A4", "start_time": 2.0, "duration": 2.0, "velocity": 75}}

RULES FOR start_time:
1. start_time is the ABSOLUTE position in quarter notes from the part start (always starts at 0.0)
2. Notes with the same start_time play simultaneously (creating chords)
3. Notes with different start_times play sequentially
4. ALWAYS increment start_time based on the previous note's duration for sequential notes
5. For chord progressions: all notes in a chord share the same start_time

Example sequential melody with start_time:
  {{"note_name": "C4", "start_time": 0.0, "duration": 1.0, "velocity": 75}}  # Beat 1
  {{"note_name": "D4", "start_time": 1.0, "duration": 1.0, "velocity": 75}}  # Beat 2 (0.0 + 1.0)
  {{"note_name": "E4", "start_time": 2.0, "duration": 1.0, "velocity": 75}}  # Beat 3 (1.0 + 1.0)
  {{"note_name": "F4", "start_time": 3.0, "duration": 1.0, "velocity": 75}}  # Beat 4 (2.0 + 1.0)

Use polyphony for:
- Piano chords and harmonies
- String sections
- Brass stabs
- Any time multiple notes should sound together

CONTINUOUS CONTROLLERS (Expression):
For piano/keyboard parts, use sustain_pedal or add cc_events:
- "sustain_pedal": true - Automatically adds sustain pedal (CC64) for the duration
- Manual CC events: "cc_events": [{{"controller": 64, "value": 127, "time": 0}}, {{"controller": 64, "value": 0, "time": 32}}]

Useful CC numbers:
- 64: Sustain pedal (value 127=on, 0=off)
- 11: Expression (0-127, for crescendo/decrescendo)
- 7: Volume (0-127)
- 10: Pan (0=center, 0=left, 127=right)
- 1: Modulation/vibrato depth

Example string swell with expression:
"cc_events": [
  {{"controller": 11, "value": 60, "time": 0}},   # Start quiet
  {{"controller": 11, "value": 100, "time": 4}},  # Crescendo
  {{"controller": 11, "value": 60, "time": 8}}    # Diminuendo
]

TEMPO AND TIME SIGNATURE CHANGES:
You can change tempo and time signature during the piece:
- "tempo_changes": [{{"time": 0, "bpm": 120}}, {{"time": 48, "bpm": 100}}, {{"time": 56, "bpm": 80}}]
- "time_signature_changes": [{{"measure": 17, "numerator": 3, "denominator": 4}}, {{"measure": 33, "numerator": 4, "denominator": 4}}]

Common patterns:
- Ritardando (slow down): Gradually decrease BPM in tempo_changes
- Accelerando (speed up): Gradually increase BPM
- Time signature change: Switch to 3/4 for waltz section, then back to 4/4
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

CRITICAL REQUIREMENTS - READ CAREFULLY:

1. DURATION: Your composition MUST be 2-3 minutes long at the specified tempo.
   Calculate needed notes: (Tempo / 60) × Duration(seconds) = quarter notes needed
   Example: At 80 BPM, 2 minutes = 160 quarter notes minimum per part

2. NUMBER OF PARTS: Limit to 2-4 parts maximum.
   - More parts = fewer notes per part = shorter duration
   - Better to have 3 well-developed parts than 6 sparse parts
   - Recommended: melody + bass + 1-2 harmony/accompaniment parts

3. NOTE COUNTS BY PART:
   - Melody: 150-350 notes (depending on tempo and note durations)
   - Harmony: 120-280 notes
   - Bass: 80-180 notes (bass notes are longer, so fewer needed)
   - Accompaniment: 100-220 notes

4. MUSICAL STRUCTURE:
   - Create 3-4 distinct sections (e.g., A-A-B-A or verse-chorus-bridge)
   - Each section: 16-32 bars (64-128 quarter notes in 4/4 time)
   - Use repetition AND variation - don't just play random notes
   - Include a clear climax/build toward the middle or end

5. MUSICAL QUALITY:
   - Vary rhythms: mix eighth, quarter, half, whole notes (not all same length)
   - Use rests SPARINGLY - music should flow
   - Create phrases that "breathe" but don't have awkward silences
   - Include dynamic contrast (some parts louder/softer)
   - Make the melody memorable and singable

6. POLYPHONY REQUIREMENT:
   - start_time is REQUIRED for ALL notes - always specify it
   - For harmony/accompaniment parts: use start_time to create chords
   - Same start_time = notes play together (chord)
   - Different start_time = notes play sequentially
   - CRITICAL: HARMONY PARTS MUST USE start_time FOR CHORDS

7. Return ONLY the JSON object - no markdown code blocks, no explanations

EXAMPLE FORMAT (structure only - create ORIGINAL music):
{{
  "title": "Your Original Title",
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
        {{"note_name": "C4", "start_time": 0.0, "duration": 1.0, "velocity": 75}},
        {{"note_name": "E4", "start_time": 1.0, "duration": 1.0, "velocity": 70}},
        {{"note_name": "G4", "start_time": 2.0, "duration": 1.0, "velocity": 72}},
        ... (150+ more notes for 2+ minutes at this tempo)
      ]
    }},
    {{
      "name": "piano_harmony",
      "midi_program": 0,
      "midi_channel": 1,
      "role": "harmony",
      "notes": [
        {{"note_name": "C4", "start_time": 0.0, "duration": 2.0, "velocity": 65}},
        {{"note_name": "E4", "start_time": 0.0, "duration": 2.0, "velocity": 65}},
        {{"note_name": "G4", "start_time": 0.0, "duration": 2.0, "velocity": 65}},
        {{"note_name": "D4", "start_time": 2.0, "duration": 2.0, "velocity": 65}},
        {{"note_name": "F4", "start_time": 2.0, "duration": 2.0, "velocity": 65}},
        {{"note_name": "A4", "start_time": 2.0, "duration": 2.0, "velocity": 65}},
        ... (120+ more notes)
      ]
    }},
    {{
      "name": "piano_bass",
      "midi_program": 0,
      "midi_channel": 2,
      "role": "bass",
      "notes": [
        {{"note_name": "C3", "start_time": 0.0, "duration": 4.0, "velocity": 65}},
        ... (80+ more notes)
      ]
    }}
  ]
}}

REMEMBER: Generate ORIGINAL music with 150-300+ notes per part for a full 2-3 minute composition!
"""

    def _default_system_instructions(self, tools: list[FunctionDeclaration] | None = None) -> str:
        """Default system instructions - more specific than before.

        Args:
            tools: Optional list of tools - if provided, includes tool instructions

        Returns:
            System instructions string
        """
        base_instructions = """You are an expert AI composer who creates note-by-note musical compositions.

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

        if tools:
            tool_names = ", ".join([f"'{t.name}'" for t in tools])
            base_instructions += f"""

AVAILABLE TOOLS:
You have access to the following tools for enhanced composition: {tool_names}.
Use these tools to create more structured and expressive compositions.
See the TOOL USAGE section below for detailed instructions on when and how to use each tool."""

        return base_instructions

    def _build_tool_instructions(self) -> str:
        """Build instructions for tool usage.

        Returns:
            Tool usage instructions string
        """
        # Get descriptions of available tools
        tool_descriptions = []
        for tool in self.tools or []:
            tool_descriptions.append(f"- {tool.name}: {tool.description}")

        tools_list = "\n".join(tool_descriptions) if tool_descriptions else ""

        return f"""TOOL USAGE:
You have access to function calling tools that can enhance your compositions.

AVAILABLE TOOLS:
{tools_list}

WHEN TO USE TOOLS:
1. Use tools to STRUCTURE your composition before generating notes
2. Call create_section for each major section (intro, verse, chorus, bridge, etc.)
3. Use create_chord when you want specific harmonic progressions with voice leading
4. Use set_dynamic to plan dynamic contrasts between sections
5. Use add_rhythm_variation to add interest to repeated patterns
6. Use add_counter_melody to add secondary melodic lines
7. Use apply_transformation to develop motifs through variation

HOW TO USE TOOLS:
- Make tool calls BEFORE generating your final JSON composition
- Tool calls help you plan and structure the composition
- The composition JSON you return should reflect the planning done through tools
- You can make multiple tool calls in a single response

EXAMPLE TOOL USAGE:
If creating a pop song structure:
1. Call create_section for "intro" (measures 1-8)
2. Call create_section for "verse" (measures 9-24)
3. Call create_section for "chorus" (measures 25-40)
4. Call set_dynamic for "mf" starting at measure 25 (chorus entrance)
5. Generate the full JSON composition reflecting this structure

IMPORTANT:
- Tools are OPTIONAL aids for composition
- Your primary output must still be the JSON composition
- Use tools to make your compositions more structured and expressive
- Not every tool needs to be used for every composition

"""


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
