# MusicGen AI Composition - Step Plan & Context

## Project Overview

Building an AI-first music generation library that uses Google Gemini 2.5 Pro to generate note-level compositions directly from natural language prompts, then renders them to MIDI/audio.

**Repository:** `/home/chiranjeet/projects-cc/projects/music-gen-lib`

---

## Completed Steps (1-8)

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
- **Request/response logging to `logs/ai_calls/`**

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

## Current State

### Files Created/Modified
```
src/musicgen/
├── ai_client/
│   ├── __init__.py
│   ├── client.py          # GeminiClient with logging
│   ├── exceptions.py      # Custom exceptions
│   └── prompts.py         # Improved prompts with examples
├── ai_models/
│   ├── __init__.py
│   ├── composition.py     # AIComposition model
│   ├── notes.py          # AINote, AIRest
│   └── parts.py          # AIPart model
├── composer_new/
│   ├── __init__.py
│   ├── composer.py       # AIComposer with log_requests
│   └── presets.py        # Prompt templates
├── config/
│   ├── defaults.py       # Default config values
│   ├── settings.py       # Config class
│   └── __init__.py       # Extended exports
├── renderer/
│   ├── __init__.py
│   ├── midi.py          # MIDIRenderer
│   ├── audio.py         # AudioRenderer (fixed wave_type issue)
│   └── renderer.py      # Renderer orchestration
├── schema/
│   ├── __init__.py
│   ├── generator.py     # SchemaGenerator
│   └── models.py        # Schema models
└── __main__.py           # Updated CLI with compose command
```

### Generated Audio Files (Output)
```
output/
├── Peaceful_Piano.mid/wav     # ~2 min
├── Jazz_Piano_Trio.mid/wav    # ~2.5 min
├── Melancholy_Strings.mid/wav  # ~5.5 min
└── Electronic_Ambient.mid/wav  # ~14 min (bug - too long)
```

### Environment Setup
```bash
# Dependencies installed in .venv/
.venv/bin/pip list | grep -E "(google|pydantic|yaml|mido|pretty)"
google-api-core
google-auth
google-genai
pydantic
pyyaml
mido
pretty-midi
numpy
```

---

## Known Issues

### 1. AI Generated Compositions Too Generic
The AI returns valid JSON but compositions lack:
- Sufficient note count (often 30-50 notes instead of 60-120 required)
- Musical coherence and development
- Distinctive style based on prompt
- Proper 2-3 minute duration

**Root Cause:** The prompt may not be emphasizing quantity enough. The AI focuses on quality/structure but doesn't generate enough notes.

### 2. Ambient Piece Duration Bug
The ambient composition generated ~850 notes instead of intended amount, creating a 14-minute piece instead of 2-3 minutes. This was due to how the note generation loop was structured.

### 3. Response Logging Working
The logging is saving to `logs/ai_calls/<timestamp>/` with:
- `prompt.txt` - Original user prompt
- `system_prompt.txt` - Full system instructions
- `user_prompt.txt` - User prompt with schema
- `schema.yaml` - Schema sent to AI
- `response_raw.txt` - Raw AI response
- `response_parsed.json` - Parsed composition
- `metadata.json` - Model, temperature, etc.

---

## Descriptive Prompts Created

These paragraph-length prompts were designed to evoke specific emotional responses:

1. **Nostalgic Sunset (A minor, 70 BPM)**
   - Childhood neighborhood at sunset, bittersweet nostalgia
   - Piano + gentle strings, simple touching melody
   - Emotional builds and releases, breathing with pauses

2. **Epic Triumph (D major/minor, 120-130 BPM)**
   - Adventure movie climax, hero achieves impossible quest
   - Full orchestra: trumpets, soaring strings, tympani, french horns
   - Building anticipation, massive crescendos, triumphant moments

3. **Late Night Jazz (F/Bb minor, 90-100 BPM)**
   - Paris jazz club at 2 AM, telepathic musical conversation
   - Piano trio (piano, double bass, drums)
   - Bill Evans-inspired harmonies, warm walking bass, syncopated rhythms

4. **Space Ambient (60-70 BPM)**
   - Floating through nebula, shimmering synth pads
   - Timeless, no clear pulse, crystalline melodies
   - Extended chords, deep bass rumbles, meditative

---

## Next Steps to Continue

### Step A: Review AI Response Logs
```bash
# Check the latest AI responses
ls logs/ai_calls/
cat logs/ai_calls/<timestamp>/response_parsed.json | jq
```

Look at:
- How many notes per part is AI actually generating?
- Is the structure there or just random notes?
- Are the styles matching the prompts?

### Step B: Improve Prompt Engineering
The issue may be:
1. Not emphasizing NOTE QUANTITY enough
2. Schema too complex causing token limit issues
3. Temperature too low causing generic outputs

Try these changes in `src/musicgen/ai_client/prompts.py`:

```python
# Add stronger emphasis on note count
"REQUIREMENTS:
1. Create AT LEAST 150-200 notes per part (this is critical!)
2. Duration should be 2-3 minutes minimum at the specified tempo
...
```

Or try higher temperature:
```python
composer = AIComposer(temperature=0.8)  # More creative/random
```

### Step C: Consider Alternative Approach
If note-by-note generation is too difficult for the AI:

1. **Generate parameters, then expand locally**
   - AI generates: chord progression, melody outline, structure
   - Local code expands to full note sequences

2. **Use multiple AI calls**
   - Call 1: Generate structure + chord progression
   - Call 2: Generate melody for one section
   - Call 3: Generate bass line
   - etc.

3. **Use structured generation with constraints**
   - Generate 8-bar phrases separately
   - Stitch them together locally

### Step D: Test with Different Model
```bash
# Try gemini-2.0-flash-exp if 2.5-pro is being too conservative
composer = AIComposer(model="gemini-2.0-flash-exp")
```

---

## Git History Reference

Recent commits:
```
409ff18 feat: add request/response logging and improve AI prompts
733cd6a fix: apply ruff linting fixes and CLI updates
585c6a7 feat(step 2): add schema generation engine
6b7c1b8 feat(step 1): add configuration system
ca3fa61 chore: add .gitignore for output directory
58ebe15 fix: remove unsupported wave_type argument
```

---

## Commands Reference

```bash
# Check system
musicgen check

# Generate from prompt
musicgen compose "your prompt here" --output-dir output -f midi wav

# List presets
musicgen presets list

# Generate with verbose logging
musicgen compose "prompt" --verbose

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

## Files to Review for Debugging

1. **`logs/ai_calls/<timestamp>/response_parsed.json`** - See what AI actually returned
2. **`src/musicgen/ai_client/prompts.py`** - The prompts being sent
3. **`src/musicgen/schema/generator.py`** - The schema being generated
4. **`src/musicgen/composer_new/composer.py`** - The orchestration layer

---

## Key Code Locations

| Functionality | File | Key Class/Function |
|---------------|------|-------------------|
| AI Client | `ai_client/client.py` | `GeminiClient.generate()` |
| Prompt Building | `ai_client/prompts.py` | `PromptBuilder.build_prompt()` |
| Schema Generation | `schema/generator.py` | `SchemaGenerator.generate()` |
| Note Models | `ai_models/notes.py` | `AINote`, `AIRest` |
| Composition Model | `ai_models/composition.py` | `AIComposition` |
| MIDI Rendering | `renderer/midi.py` | `MIDIRenderer.render()` |
| Audio Rendering | `renderer/audio.py` | `AudioRenderer.render()` |
| Main Composer | `composer_new/composer.py` | `AIComposer.generate()` |

---

## Environment Variables Required

```bash
# .env file
GOOGLE_API_KEY=AIzaSy...  # Required
GEMINI_MODEL=gemini-2.5-pro  # Optional
GEMINI_TEMPERATURE=0.5        # Optional
```
