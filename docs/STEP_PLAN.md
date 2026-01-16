# MusicGen AI Composition - Step Plan & Context

## Project Overview

Building an AI-first music generation library that uses Google Gemini 2.5 Pro to generate note-level compositions directly from natural language prompts, then renders them to MIDI/audio.

**Repository:** `/home/chiranjeet/projects-cc/projects/music-gen-lib`

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
