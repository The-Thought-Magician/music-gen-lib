"""YAML generation prompts for AI-based composition specification.

This module provides prompts for AI to generate YAML specifications
that are then interpreted by the rule-based engine for authentic music.
"""

from __future__ import annotations


def get_yaml_schema() -> str:
    """Get the YAML schema for composition specification."""
    return """# Indian Classical Music YAML Specification Schema

title: string                    # Composition title
composer: string                  # Composer name (optional)
duration_seconds: float           # Total duration in seconds

# Key and time signature
key:
  root: string                    # Root note (C, D, E, F, G, A, B)
  mode: string                    # Scale mode (major, minor, etc.)
  octave: int                     # Starting octave (default: 4)

tempo:
  bpm: float                      # Tempo in beats per minute

time_signature:
  numerator: int                  # Top number of time signature
  denominator: int                # Bottom number

# Genre (must be "indian_classical" for this system)
genre: "indian_classical"

style:
  complexity: "low" | "medium" | "high"
  mood: string                    # Any mood descriptor
  ornamentation: "none" | "light" | "medium" | "heavy"

# Sections of the composition
sections:
  - name: string                  # Section name (alap, gat, etc.)
    duration_bars: float          # Length in bars
    tempo_multiplier: float       # Tempo adjustment (0.5 = half, 1.5 = 1.5x)
    tala: string | null           # Tala name (teental, jhaptal, rupak, dadra, etc.)
    laya: string | null           # Speed (vilambit, madhya, drut)

# Instruments
instruments:
  - name: string                  # Instrument name
    family: string                # strings, percussion, drone, winds, brass, keyboards
    role: string                  # melody, harmony, bass, rhythm, drone
    channel: int                  # MIDI channel (0-15)
    midi_program: int | null      # MIDI program number
    drone_notes:                  # For drone instruments only
      - note: string              # Note like "C3"
        detune_cents: int         # Detuning in cents
        velocity: int             # Velocity (0-127)
        start_offset: float       # Start offset for overlap
    stroke_mapping:               # For tabla/percussion
      string: int                 # bol_name: midi_note

# Melody generation rules
melody_rules:
  source: "raga"                  # Must be "raga" for Indian classical
  raga: string                    # Raga name (yaman, bhairavi, todi, darbari, etc.)
  density:
    notes_per_minute: [int, int]  # Range of notes per minute
    avg_duration_beats: [float, float]  # Average note duration range
    duration_range: [float, float]  # Min/max note duration
  phrases:
    length_bars: [int, int]       # Phrase length in bars
    development: string           # ascending, descending, arc, mixed
    repetition: bool             # Whether to use repetition
  register:
    lowest_octave: int            # Lowest octave to use
    highest_octave: int           # Highest octave to use
    emphasis: string              # low, middle, high
  ornamentation:
    meend: "none" | "rare" | "occasional" | "frequent"
    gamaka: "none" | "light" | "medium" | "heavy"
    krintan: "none" | "rare" | "occasional" | "frequent"

# Rhythm generation rules
rhythm_rules:
  source: "tala"                  # Must be "tala" for Indian classical
  tala: string                    # Tala name
  cycle_beats: int                # Beats per cycle
  division: list[int]             # Vibhag divisions (e.g., [4,4,4,4] for teental)
  accent_pattern: list[int]       # Accent levels per beat (0-3)
"""


def build_yaml_prompt(user_prompt: str) -> tuple[str, str]:
    """Build prompts for generating YAML specification from user description.

    Args:
        user_prompt: User's description of desired music

    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    system_prompt = f"""You are an expert Indian classical music composer and scholar.

You have deep knowledge of:
- Raga system: Raga definitions with aroha/avaroha, vadi/samvadi, pakad phrases
- Tala system: Rhythmic cycles including teental (16), jhaptal (10), rupak (7), dadra (6), ektal (12)
- Laya: Temporal layers - vilambit (slow), madhya (medium), drut (fast)
- Instrumentation: Sitar, sarod, bansuri, tabla, tanpura, santoor, sarangi
- Ornamentation: Meend (glissando), gamaka (oscillation), krintan (spiccato)
- Performance structure: Alap (free rhythm), jor, gat (composition)

AVAILABLE RAGAS (with their characteristics):

Morning Ragas (6-9 AM):
- Bhairav: Serious, devotional. Uses komal Re and Dha. Vadi=Dha, Samvadi=Re.
- Lalit: Meditative, uses both shuddha and komal Re.
- Todi: Deep, profound. Komal Re, Ga, Dha. Vadi=Ga, Samvadi=Dha.

Late Morning (9-12 AM):
- Bilaskhani: Melancholic, derived from Bhairav.

Afternoon Ragas (12-4 PM):
- Bhimpalasi: Romantic, thumri style. Komal Ga and Ni. Vadi=Dha, Samvadi=Ga.
- Bageshree: Romantic, devotional. Komal Ga, Dha, Ni. Vadi=Ga, Samvadi=Ni.

Evening Ragas (4-7 PM):
- Yaman: Peaceful, romantic. All shuddha notes except Tivra Ma. Vadi=Ga, Samvadi=Ni.
- Khamaj: Romantic, light classical. Uses both shuddha and komal Ni.

Late Evening/Night (7-10 PM):
- Darbari: Deep, serious. Komal Ga and Dha. Vadi=Dha, Samvadi=Re.
- Malkauns: Devotional, pentatonic. Komal Ga, Dha, Ni.
- Bageshri: Romantic, thumri style.

Midnight Ragas (10 PM - 1 AM):
- Marwa: Restless, tense. Uses both shuddha and komal Re.
- Poorvi: Serious, rare.
- Todi: Also performed at midnight.

AVAILABLE TALAS (rhythmic cycles):

- Teental (16 beats): [4,4,4,4] - Most common, balanced structure
  Accent pattern: [3,0,0,0, 2,0,0,0, 1,0,0,0, 2,0,0,0]
  Bols: dha dhin dhin dha | dha dhin dhin dha | dha tin tin ta | kat ge dhi na

- Jhaptal (10 beats): [2,3,2,3] - Asymmetric, energetic
  Accent pattern: [3,0, 2,0,0, 1,0, 2,0,0]
  Bols: dha dhin | dhin dha dhin | dha dhin | dhin dha

- Rupak (7 beats): [3,2,2] - Flowing, distinctive
  Accent pattern: [3,0,0, 1,0, 2,0] (no clap on sam!)
  Bols: tin tin na | dhin na | dha ge

- Dadra (6 beats): [3,3] - Light, romantic
  Accent pattern: [3,0,0, 2,0,0]
  Bols: dha dhin dha | dha dhin dha

- Ektal (12 beats): [2,2,2,2,2,2] - Symmetrical, formal
  Accent pattern: [3,0, 2,0, 1,0, 2,0, 1,0, 2,0]

- Deepchandi (14 beats): [3,4,3,4] - majestic, expansive

MUSICAL STRUCTURE:

Typical Indian classical performance structure:
1. Alap (vilambit, no tala): 5-10 minutes of slow exploration
2. Jor (vilambit, pulse emerges): Rhythmic feeling develops
3. Gat (vilambit): Composition in slow tempo with tala
4. Gat (drut): Fast composition with tala

For shorter pieces (3-5 minutes):
- Short alap: 30-60 seconds
- Vilambit gat: 2 minutes
- Drut gat: 1-2 minutes

INSTRUMENT ROLES:

Melody instruments (Sitar, Sarod, Bansuri, Sarangi):
- role: "melody"
- Use raga-constrained notes
- Apply ornamentation (meend, gamaka)
- Emphasize vadi/samvadi notes

Rhythm instrument (Tabla):
- role: "rhythm"
- Use stroke_mapping for bols
- Follow tala cycle

Drone (Tanpura):
- role: "drone"
- Continuous tonic + fifth + octave
- Typically: Sa (tonic), Pa (fifth), Sa' (upper octave)

ORCHESTRATION RECOMMENDATIONS:

For full ensemble:
- Sitar (melody) - MIDI program 104, channel 0
- Sarangi (secondary melody) - MIDI program 40 (violin), channel 1
- Tabla (rhythm) - channel 2, custom stroke mapping
- Tanpura (drone) - channel 3, drone notes

For duet:
- Sitar or Bansuri (melody)
- Tabla (rhythm)
- Tanpura (drone)

For solo:
- Any melody instrument
- Tanpura (drone)

COMPLEXITY LEVELS:

- Low: Simple phrases, minimal ornamentation, basic tala
- Medium: Mixed phrase lengths, moderate ornamentation, standard talas
- High: Complex phrases, heavy ornamentation, uncommon talas

ORNAMENTATION LEVELS:

- None: Plain notes, no decorative elements
- Light: Occasional meend on important notes
- Medium: Regular meend, some gamaka, occasional krintan
- Heavy: Frequent meend, extensive gamaka, krintan on strong beats

OUTPUT REQUIREMENTS:

1. Return ONLY valid YAML - no markdown code blocks, no explanations
2. Duration should be 3-5 minutes (180-300 seconds)
3. Include at minimum: alap (no tala) and 1-2 gat sections
4. Always include tanpura drone for authenticity
5. Choose raga appropriate to the mood/time of day described
6. Match tala to the character (teental for balanced, jhaptal for asymmetric)

Example structure for a 4-minute piece:
- Alap: 48 bars (~2 minutes at slow tempo)
- Vilambit Gat: 32 bars (~1 minute, teental)
- Drut Gat: 32 bars (~1 minute, teental faster)"""

    user_prompt_full = f"""Generate a YAML specification for Indian classical music based on this description:

"{user_prompt}"

Analyze the emotional content and setting described, then:

1. Choose an appropriate RAGA:
   - Consider the time of day if mentioned
   - Match the mood (devotional→Bhairav/Todi, romantic→Yaman/Khamaj, serious→Darbari)
   - Consider the complexity level

2. Choose an appropriate TALA:
   - Teental for balanced, standard compositions
   - Jhaptal for asymmetric energy
   - Rupak for flowing, romantic pieces
   - Dadra for lighter, romantic pieces

3. Design the SECTIONS:
   - Include an alap (no tala) for raga exploration
   - Add gat sections with tala
   - Use tempo_multiplier to show development (0.7 for vilambit, 1.5 for drut)

4. Specify ORNAMENTATION:
   - Heavy for expressive, emotional pieces
   - Medium for balanced compositions
   - Light for simpler pieces

5. Choose INSTRUMENTS:
   - Minimum: Sitar + Tabla + Tanpura
   - Full ensemble: Add Sarangi or second melody instrument

Return ONLY the YAML specification. No explanations, no markdown formatting.

The YAML must follow this structure exactly:

```yaml
title: "Composition Title"
composer: "MusicGen Indian Classical"
duration_seconds: 240

key:
  root: "C"
  mode: "major"
  octave: 4

tempo:
  bpm: 80

time_signature:
  numerator: 4
  denominator: 4

genre: "indian_classical"

style:
  complexity: "medium"
  mood: "descriptive mood"
  ornamentation: "medium"

sections:
  - name: "alap"
    duration_bars: 16
    tempo_multiplier: 0.7
    tala: null
    laya: "vilambit"
  - name: "gat_vilambit"
    duration_bars: 32
    tempo_multiplier: 1.0
    tala: "teental"
    laya: "vilambit"

instruments:
  - name: "Sitar"
    family: "strings"
    role: "melody"
    channel: 0
    midi_program: 104
  - name: "Tabla"
    family: "percussion"
    role: "rhythm"
    channel: 2
    stroke_mapping:
      "dha": 50
      "dhin": 49
      "tun": 57
      "na": 52
      "ge": 43
      "ke": 40
      "kat": 45
  - name: "Tanpura"
    family: "drone"
    role: "drone"
    channel: 3
    drone_notes:
      - note: "C3"
        detune_cents: 0
        velocity: 60
        start_offset: 0.0
      - note: "G3"
        detune_cents: 0
        velocity: 50
        start_offset: 0.0
      - note: "C4"
        detune_cents: 0
        velocity: 55
        start_offset: 0.1

melody_rules:
  source: "raga"
  raga: "yaman"
  density:
    notes_per_minute: [60, 90]
    avg_duration_beats: [0.5, 1.5]
    duration_range: [0.25, 2.0]
  phrases:
    length_bars: [4, 8]
    development: "mixed"
    repetition: true
  register:
    lowest_octave: 4
    highest_octave: 6
    emphasis: "middle"
  ornamentation:
    meend: "occasional"
    gamaka: "rare"
    krintan: "occasional"

rhythm_rules:
  source: "tala"
  tala: "teental"
  cycle_beats: 16
  division: [4, 4, 4, 4]
  accent_pattern: [3, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0]
```

Remember: Return ONLY valid YAML. No code blocks, no explanations."""

    return system_prompt, user_prompt_full


def build_raga_selection_prompt(description: str) -> str:
    """Build a prompt for selecting an appropriate raga based on description.

    Args:
        description: User's description

    Returns:
        Prompt for raga selection
    """
    return f"""You are an expert Indian classical music scholar. Based on the following description,
recommend the most appropriate raga and explain your choice.

Description: "{description}"

Consider:
1. Time of day (morning ragas vs evening vs midnight)
2. Emotional mood (devotional, romantic, serious, peaceful)
3. Complexity level (basic ragas vs complex ones)

Available ragas to choose from:
- Yaman (evening, peaceful, romantic) - All shuddha except Tivra Ma
- Bhairav (morning, serious, devotional) - Komal Re, Dha
- Bhairavi (morning, versatile, heavy ornamentation) - Komal Re, Ga, Dha, Ni
- Todi (morning/midnight, profound, serious) - Komal Re, Ga, Dha
- Darbari (late night, deep, serious) - Komal Ga, Dha
- Malkauns (late night, devotional, pentatonic) - Komal Ga, Dha, Ni
- Bhimpalasi (afternoon, romantic) - Komal Ga, Ni
- Khamaj (evening, light, romantic) - Shuddha and komal Ni
- Jhinjhoti (late afternoon, romantic)
- Pilu (light, romantic thumri)

Return your recommendation in this format:
Raga: [name]
Reason: [brief explanation of why this raga fits the description]
Vadi: [vadi note and its significance]
Samvadi: [samvadi note and its significance]"""
