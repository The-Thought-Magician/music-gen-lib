# MusicGen AI Composition - Step Plan & Context

## Project Overview

Building an AI-first music generation library that uses Google Gemini 2.5 Pro to generate note-level compositions directly from natural language prompts, then renders them to MIDI/audio with SFZ high-quality sound rendering.

**Repository:** `/home/chiranjeet/projects-cc/projects/music-gen-lib`
**Current Version:** V3.0 (Fully Implemented)
**Last Updated:** January 17, 2026

---

## Phase 1: Foundation (COMPLETED)

### ✅ Step 1: Configuration System
- Created `config/musicgen.yaml` with defaults
- Created `.env.example` for API keys
- Extended `src/musicgen/config/` with `Config`, `get_config`
- Supports YAML config + environment variable overrides

### ✅ Step 2: Schema Generation Engine
- Created `src/musicgen/schema/generator.py` - `SchemaGenerator`
- Created `src/musicgen/schema/models.py` - schema dataclasses
- Auto-generates YAML schemas from data models
- Includes music theory reference for AI

### ✅ Step 3: AI Note Sequence Models
- Created `src/musicgen/ai_models/notes.py` - `AINote`, `AIRest`
- Created `src/musicgen/ai_models/parts.py` - `AIPart`
- Created `src/musicgen/ai_models/composition.py` - `AIComposition`
- Pydantic models with validation

### ✅ Step 4: Gemini 2.5 Pro Client
- Created `src/musicgen/ai_client/client.py` - `GeminiClient`
- Created `src/musicgen/ai_client/exceptions.py` - custom exceptions
- Created `src/musicgen/ai_client/prompts.py` - `PromptBuilder`
- Retry logic with exponential backoff
- Request/response logging to `logs/ai_calls/`

### ✅ Step 5: AI Composer
- Created `src/musicgen/composer_new/composer.py` - `AIComposer`
- Created `src/musicgen/composer_new/presets.py` - prompt presets
- Orchestrates schema + AI client + validation

### ✅ Step 6: Rendering Engine
- Created `src/musicgen/renderer/midi.py` - `MIDIRenderer`
- Created `src/musicgen/renderer/audio.py` - `AudioRenderer`
- Created `src/musicgen/renderer/renderer.py` - `Renderer`
- Converts `AIComposition` → MIDI → WAV

### ✅ Step 7: CLI Redesign
- Updated `src/musicgen/__main__.py` with `compose` command
- Added `presets` command
- AI-first interface: `musicgen compose "prompt"`

### ✅ Step 8: Type Safety
- Updated `pyproject.toml` with ruff/mypy config
- All code passes `ruff check`
- Added comprehensive ruff rules with per-file ignores

---

## Phase 1.5: Quality Improvements (COMPLETED - Jan 16, 2025)

### ✅ Step 9: Schema Fixes
- Fixed key signature format to match Pydantic model: `{"tonic": "C", "mode": "major"}`
- Fixed time signature format: `{"numerator": 4, "denominator": 4}`
- Added explicit valid role values to schema
- Fixed note name parsing: converts flats to sharps (Eb → D#)

### ✅ Step 10: Enhanced Prompts
- Added explicit duration calculations and note count requirements
- Added guidance limiting to 2-4 parts for better note density
- Added section on valid part roles
- Improved note density instructions

### ✅ Step 11: Quality Validation
- Added duration validation (target: 2+ minutes)
- Added minimum note count validation per part role
- Logs warnings when requirements aren't met

### Test Results After Improvements

| Piece | Duration | Note Counts | Status |
|-------|----------|-------------|--------|
| Sunset on Sycamore Street (nostalgic piano) | 3.1 min | 87/126/60/54 | ✅ Good |
| Midnight on the Seine (jazz trio) | 3.5 min | 165/190/113 | ✅ Excellent |
| Summit's Triumph (orchestral) | 1.4 min | 99/84/57 | ⚠️ Short |

---

## Phase 2: Critical Architecture Fixes (PLANNED)

### Overview

After reviewing the system, **critical architectural issues** were identified that prevent the generation of truly musical, performable compositions. The current schema works for simple monophonic melodies but cannot represent:

1. **Polyphony** (chords, simultaneous notes)
2. **Synchronization** (global timing across parts)
3. **Expression** (continuous controllers, dynamics)
4. **Tempo/Meter changes** (ritardandi, time signature changes)
5. **Long compositions** (token economy limits)

---

## Step 12: Add Polyphony Support

### Problem
The current `notes` array is sequential. A C Major chord (C-E-G played simultaneously) must be represented as three separate notes starting at the same time.

### Solution Options

**Option A: Add `start_time` (Absolute Timing)**
```python
class AINote(BaseModel):
    note_name: str
    duration: float
    start_time: float  # Absolute position in quarter notes
    velocity: int
```

**Option B: Add `time_delta` (MIDI-style)**
```python
class AINote(BaseModel):
    note_name: str
    duration: float
    time_delta: float  # Time since previous event
    velocity: int
```

**Option C: Note Groups/Chords**
```python
class AINoteGroup(BaseModel):
    start_time: float
    duration: float
    notes: list[NoteWithPitch]  # Multiple notes at same time
```

### Recommendation
Use **Option A** (`start_time`) as it's the most flexible and aligns with how DAWs and MIDI editors represent music.

### Files to Modify
- `src/musicgen/ai_models/notes.py` - Add `start_time` field
- `src/musicgen/ai_models/parts.py` - Update validation
- `src/musicgen/renderer/midi.py` - Update rendering logic
- `src/musicgen/schema/generator.py` - Update schema

---

## Step 13: Add Global Timeline/Synchronization

### Problem
Each part has independent timing. If Flute has a rest of 0.5 and Violin has a note of 0.5, ensuring they align at Measure 15 requires complex calculation. Floating-point errors cause desync.

### Solution Options

**Option A: Measure-Based Structure**
```json
{
  "measures": [
    {
      "number": 1,
      "beats": 4,
      "parts": {
        "violin": [{"note": "C4", "start": 0, "duration": 1}],
        "flute": [{"note": "E4", "start": 0, "duration": 1}]
      }
    }
  ]
}
```

**Option B: Global Timeline Events**
```json
{
  "timeline": [
    {"time": 0, "events": [...]},
    {"time": 0.5, "events": [...]}
  ]
}
```

**Option C: Keep Part-Based but Add Sync Markers**
```json
{
  "parts": [...],
  "sync_points": [
    {"measure": 16, "time": 48.0}
  ]
}
```

### Recommendation
Start with **Option A** (Measure-Based) for new compositions, but keep the current Part-based structure for backwards compatibility. Add a `structure_type` field to choose.

---

## Step 14: Add Continuous Controllers (Expression)

### Problem
Music is not just Note On/Off. A violin crescendo while holding a note cannot be represented by a single `velocity` value.

### Solution: Add CC Events

```python
class ControlChangeEvent(BaseModel):
    controller: int  # CC number (64=sustain, 11=expression, 7=volume, etc.)
    value: int       # 0-127
    time: float      # When this occurs

class AIPart(BaseModel):
    notes: list[AINote]
    cc_events: list[ControlChangeEvent]  # NEW
```

### Essential CC Numbers
- CC 1: Modulation (vibrato)
- CC 7: Volume (master volume)
- CC 10: Pan (stereo position)
- CC 11: Expression (dynamic swells)
- CC 64: Sustain Pedal (on/off)
- CC 64/67: Sostenuto/Sostenuto pedal

### Files to Modify
- `src/musicgen/ai_models/notes.py` - Add `ControlChangeEvent` class
- `src/musicgen/ai_models/parts.py` - Add `cc_events` to `AIPart`
- `src/musicgen/renderer/midi.py` - Render CC events to MIDI

---

## Step 15: Add Tempo and Meter Fluidity

### Problem
Real music breathes. A ritardando at the end, or a 4/4 to 3/4 switch, is impossible with static `tempo` and `time_signature` fields.

### Solution: Event-Based Maps

```python
class TempoEvent(BaseModel):
    time: float      # When this tempo change takes effect
    bpm: int

class TimeSignatureEvent(BaseModel):
    measure: int     # At which measure
    numerator: int
    denominator: int

class AIComposition(BaseModel):
    tempo: int                    # Default/initial
    tempo_map: list[TempoEvent]   # Changes
    time_signature: TimeSignature
    time_signature_changes: list[TimeSignatureEvent]
```

### Files to Modify
- `src/musicgen/ai_models/composition.py` - Add event lists
- `src/musicgen/renderer/midi.py` - Render tempo/meta events

---

## Step 16: Chunking Strategy for Long Compositions

### Problem
A 2-minute orchestral piece has 2000+ notes. LLMs will:
- Hit output token limits
- Make syntax errors in large JSON
- Lose coherence across long generations

### Solution: Section-by-Section Generation

```python
class SectionalComposer:
    def generate_section(
        self,
        prompt: str,
        section_name: str,  # "A", "B", "bridge", etc.
        context: dict,      # Previous sections, key, etc.
        length_bars: int = 16
    ) -> AISection:
        """Generate one section at a time."""

class AISection(BaseModel):
    name: str
    start_bar: int
    end_bar: int
    parts: dict[str, list[AINote]]
```

### Files to Create
- `src/musicgen/composer_new/sectional.py` - New section-based composer

---

## Implementation Priority

### High Priority (Do First)
1. **Step 12: Polyphony** - Essential for chords, piano pieces
2. **Step 14: CC Events** - Essential for expression, sustain pedal

### Medium Priority (Do Second)
3. **Step 15: Tempo/Meter Fluidity** - Important for musicality
4. **Step 13: Synchronization** - Important for complex pieces

### Lower Priority (Do Later)
5. **Step 16: Chunking** - Only needed for very long pieces

---

## Proposed New Schema (Draft)

```json
{
  "title": "Composition Title",
  "tempo": {"initial": 120, "changes": [{"time": 32, "bpm": 110}]},
  "time_signature": {"initial": {"numerator": 4, "denominator": 4}},
  "key": {"tonic": "C", "mode": "major"},
  "structure_type": "measure_based",
  "measures": [
    {
      "number": 1,
      "beats": 4,
      "parts": [
        {
          "name": "piano",
          "role": "harmony",
          "events": [
            {
              "time": 0,
              "notes": [
                {"note_name": "C4", "duration": 4, "velocity": 80},
                {"note_name": "E4", "duration": 4, "velocity": 75},  # CHORD!
                {"note_name": "G4", "duration": 4, "velocity": 75}
              ]
            },
            {
              "time": 4,
              "cc": {"controller": 64, "value": 127}  # Sustain on
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Files Created/Modified (Current State)

```
src/musicgen/
├── ai_client/
│   ├── __init__.py
│   ├── client.py          # GeminiClient with logging
│   ├── exceptions.py      # Custom exceptions
│   └── prompts.py         # Improved prompts with duration requirements
├── ai_models/
│   ├── __init__.py
│   ├── composition.py     # AIComposition model
│   ├── notes.py          # AINote, AIRest (with flat-to-sharp conversion)
│   └── parts.py          # AIPart model
├── composer_new/
│   ├── __init__.py
│   ├── composer.py       # AIComposer with quality validation
│   └── presets.py        # Prompt templates
├── config/
│   ├── defaults.py       # Default config values
│   ├── settings.py       # Config class
│   └── __init__.py
├── renderer/
│   ├── __init__.py
│   ├── midi.py          # MIDIRenderer
│   ├── audio.py         # AudioRenderer
│   └── renderer.py      # Renderer orchestration
├── schema/
│   ├── __init__.py
│   ├── generator.py     # SchemaGenerator (fixed key format)
│   └── models.py        # Schema models
└── __main__.py           # CLI with compose command
```

---

## Environment Setup

```bash
# Using uv (recommended)
uv sync

# Dependencies include:
# - google-genai (Gemini 2.5 Pro client)
# - pydantic (validation)
# - mido (MIDI file I/O)
# - pretty-midi (MIDI rendering)
# - numpy (audio processing)
# - pyyaml (config)
```

---

## Git History Reference

Recent commits:
```
409ff18 feat: add request/response logging and improve AI prompts
37ea414 feat: add log_requests parameter to AIComposer
e13a658 docs: add comprehensive step plan with context
```

---

## Commands Reference

```bash
# Check system
musicgen check

# Generate from prompt
musicgen compose "your prompt here" --output-dir output -f midi wav

# Using Python directly
.venv/bin/python3 << 'EOF'
from musicgen.composer_new import AIComposer
from musicgen.renderer import Renderer

composer = AIComposer(log_requests=True)
comp = composer.generate("A peaceful piano melody")

renderer = Renderer(output_dir="output")
renderer.render(comp, formats=["midi", "wav"])
EOF
```

---

## Environment Variables Required

```bash
# .env file
GOOGLE_API_KEY=AIzaSy...  # Required
GEMINI_MODEL=gemini-2.5-pro  # Optional
GEMINI_TEMPERATURE=0.5        # Optional
```

---

## V3 Implementation Status (COMPLETED - January 17, 2026)

### ✅ All V3 Steps Completed (1-11)

| Step | Description | Status |
|------|-------------|--------|
| V3-01 | SFZ Introduction and Research | ✅ Completed |
| V3-02 | SFZ Instrument Definition Layer | ✅ Completed |
| V3-03 | SFZ Renderer Integration | ✅ Completed |
| V3-04 | Articulation System | ✅ Completed |
| V3-05 | Music Theory System Prompt | ✅ Completed |
| V3-06 | Composition Schema | ✅ Completed |
| V3-07 | Validation Tools | ✅ Completed |
| V3-08 | MIDI Generator with Keyswitch Support | ✅ Completed |
| V3-09 | AI Composer Integration | ✅ Completed |
| V3-10 | Testing | ✅ Completed |
| V3-11 | Documentation | ✅ Completed |

### Supported Instruments - Current Inventory

#### ✅ Western Orchestral (Fully Implemented via SFZ)

| Family | Instruments |
|--------|-------------|
| **Strings** | Violin (Solo/Section), Viola (Solo/Section), Cello (Solo/Section), Double Bass (Solo/Section), Harp |
| **Woodwinds** | Piccolo, Flute, Oboe, English Horn, Clarinet (Bb), Bass Clarinet, Bassoon, Contrabassoon |
| **Brass** | Trumpet (C/Bb), French Horn, Trombone, Bass Trombone, Tuba |
| **Percussion** | Timpani, Glockenspiel, Xylophone, Marimba, Vibraphone, Celesta, Tubular Bells |
| **Keyboards** | Piano, Harpsichord |

#### ✅ Ensemble Presets

- String Quartet, String Orchestra, Woodwind Quintet, Brass Quintet
- Chamber Orchestra, Full Orchestra, Symphony Orchestra
- Wind Ensemble, Early Music Ensemble, Solo Piano

#### ❌ NOT Currently Implemented

| Category | Missing Instruments |
|----------|---------------------|
| **World Strings** | Sitar, Balalaika, Bouzouki, Ukulele, Mandolin, Banjo, Shamisen, Koto |
| **World Plucked** | Oud, Santoor, Sarod, Veena, Charango, Tar |
| **World Bowed** | Erhu, Morin Khuur, Hardanger Fiddle, Nyckelharpa |
| **World Winds** | Shakuhachi, Bansuri, Dizi, Ney, Shakuhachi, Irish Tin Whistle |
| **World Percussion** | Tabla, Djembe, Conga, Bongo, Cajon, Doumbek, Taiko, Bodhrán |
| **Electronic** | Synthesizers, Drum Machines, Electronic Pads |
| **Guitars** | Acoustic Guitar, Electric Guitar, Hawaiian Guitar (Steel Guitar) |
| **Bass Guitars** | Electric Bass, Upright Bass (jazz) |
| **Drum Kits** | Standard Rock Kit, Jazz Kit, Electronic Kit |
| **Keyboards (Extended)** | Organ, Accordion, Harmonium |
| **Other** | Bagpipe, Harmonica, Melodica, Glass Armonica |

### Recent Test Results (January 17, 2026)

**SFZ High-Energy Test:**
- Prompt: "An epic battle scene with explosive energy! Thunderous timpani rolls..."
- Generated: "The Sundering of Ages"
- Key: D minor, Tempo: 140 BPM, Duration: 85.3s
- Instruments: Violins, Brass Section, Cello & Double Bass, Orchestral Percussion
- Output: `epic_battle_sfz.mid` (3.3K), `epic_battle_sfz.mp3` (1.1M)
- Status: ✅ SFZ rendering working

---

## Phase 4: World Instruments Integration (NEXT STEPS)

### Overview

To enable world-class music generation across all genres, we need to expand the instrument library beyond Western orchestral instruments to include:
1. World/ethnic instruments
2. Contemporary instruments (guitars, basses, drums)
3. Electronic instruments
4. Extended articulations and techniques

### Step W1: Research World Instrument SFZ Libraries

**Goal:** Identify and document free SFZ libraries for world instruments.

**Tasks:**
- Research free SFZ libraries for: Sitar, Tabla, Hawaiian Guitar, etc.
- Document licensing and usage terms
- Create compatibility matrix

**Potential Sources:**
- [SFZ Instruments](https://sfzinstruments.github.io/) - Community SFZ library index
- [Versilian Studios](https://versilian.studio/) - Free VST/SFZ instruments
- [SKYLER](https://sampleswap.org/) - Free samples
- [Philharmonia](https://philharmonia.co.uk/resources/sound-samples/) - Free samples
- [University of Iowa](https://theremin.music.uiowa.edu/) - MIS instrument samples

### Step W2: Extend Instrument Definition Schema

**Goal:** Add world instrument categories to `instrument_definitions.yaml`.

**New Categories:**
```yaml
instruments:
  # World Strings
  sitar:
    name: "Sitar"
    family: "world_strings"
    midi_program: 104  # GM Sitar
    range: {min: 48, max: 96}
    articulations: [sustain, meend, gamak, krintan]
    sfz_file: "libraries/world/sitar.sfz"

  tabla:
    name: "Tabla"
    family: "world_percussion"
    midi_program: 115  # GM - custom assignment
    articulations: [bayan, dayan, gehi, ke]
    sfz_file: "libraries/world/tabla.sfz"

  # Guitars
  acoustic_guitar:
    name: "Acoustic Guitar"
    family: "guitars"
    midi_program: 24  # GM Acoustic Guitar (steel)
    range: {min: 40, max: 84}
    articulations: [sustain, strum, pick, harmonics, palm_mute]
    sfz_file: "libraries/guitars/acoustic.sfz"

  electric_guitar:
    name: "Electric Guitar"
    family: "guitars"
    midi_program: 27  # GM Electric Guitar (clean)
    range: {min: 40, max: 84}
    articulations: [sustain, mute, harmonics, slide, bend]
    sfz_file: "libraries/guitars/electric_clean.sfz"

  # Drum Kits
  drum_kit_standard:
    name: "Standard Drum Kit"
    family: "drum_kits"
    midi_program: 0  # Channel 10
    kit_pieces: [kick, snare, hihat_closed, hihat_open, tom1, tom2, crash, ride]
    sfz_file: "libraries/drums/standard_kit.sfz"
```

### Step W3: Create Custom SFZ Instruments

**Goal:** Build custom SFZ instruments for instruments without free libraries.

**Approach:**
1. Source sample recordings (Creative Commons or public domain)
2. Create SFZ definition files with:
   - Round-robin samples for variation
   - Velocity layers
   - Articulation keyswitches
   - Proper release/decay envelopes

**Tools:**
- [SFZ Editor](https://sfzeditor.github.io/) - For editing SFZ files
- [Peaks](https://github.com/jpcima/peaks) - For sample analysis
- Audacity - For sample editing

### Step W4: Extend AI Prompts for World Instruments

**Goal:** Update system prompt to include world instrument knowledge.

**Add to `resources/system_prompt_v3.txt`:**
- World instrument characteristics and playing techniques
- Genre-appropriate instrument combinations
- Cultural context and authentic usage patterns

### Step W5: Add Genre-Specific Ensembles

**New Ensemble Presets:**
```yaml
ensembles:
  indian_classical:
    name: "Indian Classical Ensemble"
    instruments: [sitar, tabla, tanpura, bansuri, sarod]

  latin_band:
    name: "Latin Band"
    instruments: [acoustic_guitar, trumpet, trombone, congas, bongos, piano, bass]

  rock_band:
    name: "Rock Band"
    instruments: [electric_guitar, electric_bass, drum_kit, keyboard]

  jazz_combo:
    name: "Jazz Combo"
    instruments: [piano, acoustic_bass, drum_kit_jazz, trumpet, saxophone]

  celtic:
    name: "Celtic Ensemble"
    instruments: [fiddle, tin_whistle, bodhran, acoustic_guitar, bouzouki]

  middle_eastern:
    name: "Middle Eastern Ensemble"
    instruments: [oud, ney, darbuka, kanun, violin]

  african:
    name: "African Ensemble"
    instruments: [kora, djembe, balafon, talking_drum, shaker]

  electronic:
    name: "Electronic Setup"
    instruments: [synth_lead, synth_pad, synth_bass, drum_machine, sampler]
```

### Step W6: Update MIDI Program Mapping

**Goal:** Ensure proper GM/GM2/GS standard mappings.

**File:** `src/musicgen/ai_models/instruments.py` (create)

```python
# MIDI Program Numbers (0-127)
# Standard GM (0-127)
MIDI_PROGRAMS = {
    # Piano (0-7)
    0: "acoustic_grand",
    1: "bright_acoustic",
    2: "electric_grand",
    3: "honky_tonk",
    4: "electric_piano_1",
    5: "electric_piano_2",
    6: "harpsichord",
    7: "clavinet",

    # Chromatic Percussion (8-15)
    8: "celesta",
    9: "glockenspiel",
    # ...

    # Guitars (24-31)
    24: "acoustic_guitar_nylon",
    25: "acoustic_guitar_steel",
    26: "electric_guitar_jazz",
    27: "electric_guitar_clean",
    28: "electric_guitar_muted",
    29: "overdriven_guitar",
    30: "distortion_guitar",
    31: "guitar_harmonics",

    # Ethnic (104-111)
    104: "sitar",
    105: "banjo",
    106: "shamisen",
    107: "koto",
    108: "kalimba",
    109: "bagpipe",
    110: "fiddle",
    111: "shanai",
}
```

### Step W7: Extend Validation for World Instruments

**Goal:** Add music theory validation for non-Western scales and modes.

**New Scales to Add:**
- Indian: Raga scales (Bhairavi, Yaman, Bhairav, etc.)
- Middle Eastern: Maqam scales (Hijaz, Sikah, etc.)
- Japanese: Pentatonic variations (In, Hirajoshi, etc.)
- Blues: Minor/major pentatonic, blues scale
- Latin: Montuno, Bossa Nova patterns

### Implementation Priority

#### Phase 4A: Guitars and Bass (High Priority)
1. Acoustic Guitar (steel/nylon)
2. Electric Guitar (clean/distortion)
3. Electric Bass
4. Drum Kit (standard/jazz)

#### Phase 4B: World Percussion (High Priority)
1. Tabla
2. Djembe
3. Conga/Bongo
4. Cajon
5. Taiko

#### Phase 4C: Indian Instruments (Medium Priority)
1. Sitar
2. Sarod
3. Bansuri
4. Tanpura
5. Indian Raga scales

#### Phase 4D: Other World Instruments (Medium Priority)
1. Hawaiian/Steel Guitar
2. Bagpipe
3. Irish Tin Whistle
4. Oud
5. Koto

#### Phase 4E: Electronic (Lower Priority)
1. Synthesizers
2. Drum machines
3. Electronic pads

### Files to Create/Modify

**New Files:**
- `src/musicgen/ai_models/instruments.py` - MIDI program mappings
- `src/musicgen/theory/world_scales.py` - Non-Western scales
- `resources/instrument_definitions_world.yaml` - World instrument defs

**Modified Files:**
- `resources/instrument_definitions.yaml` - Add world instruments
- `resources/system_prompt_v3.txt` - Add world instrument knowledge
- `src/musicgen/validation/orchestration.py` - Add world instrument validation

---

## Quick Reference

### Generate Music

```bash
# Activate venv
source .venv/bin/activate

# Basic generation
musicgen compose "A peaceful piano melody"

# With output options
musicgen compose "Epic orchestral battle" --output-dir output --output-name my_piece --format mp3

# Verbose output
musicgen compose "Jazz trio in a smoky bar" --verbose
```

### Check System

```bash
musicgen check
```

### List Available Moods

```bash
musicgen list-moods
```

### Using Python API

```python
from musicgen.composer_new import AIComposer
from musicgen.renderer import Renderer

composer = AIComposer()
composition = composer.generate("Your prompt here")

renderer = Renderer(output_dir="output")
renderer.render(composition, formats=["midi", "mp3"])
```
