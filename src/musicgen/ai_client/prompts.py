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

POLYPHONY (Chords and Simultaneous Notes):
You can create chords by setting the same start_time for multiple notes:
- To play a C Major chord (C-E-G) at beat 1:
  {{"note_name": "C4", "start_time": 0.0, "duration": 2.0, "velocity": 75}}
  {{"note_name": "E4", "start_time": 0.0, "duration": 2.0, "velocity": 75}}
  {{"note_name": "G4", "start_time": 0.0, "duration": 2.0, "velocity": 75}}

- The start_time is the ABSOLUTE position in quarter notes from the part start
- Notes with the same start_time play simultaneously (creating chords)
- Notes with different start_times play sequentially
- If start_time is omitted, notes play sequentially (one after another)

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

6. Return ONLY the JSON object - no markdown code blocks, no explanations

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
        {{"note_name": "C4", "duration": 2.0, "velocity": 75}},
        {{"note_name": "E4", "duration": 1.0, "velocity": 70}},
        {{"note_name": "G4", "duration": 1.0, "velocity": 72}},
        ... (150+ more notes for 2+ minutes at this tempo)
      ]
    }},
    {{
      "name": "piano_bass",
      "midi_program": 0,
      "midi_channel": 1,
      "role": "bass",
      "notes": [
        {{"note_name": "C3", "duration": 4.0, "velocity": 65}},
        ... (80+ more notes)
      ]
    }}
  ]
}}

REMEMBER: Generate ORIGINAL music with 150-300+ notes per part for a full 2-3 minute composition!
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
