# V4 Remaining Tasks: Implementation Guide

## Overview

This document guides you through completing the remaining V4 implementation tasks. The **foundation is complete** (patterns, instruments, scales, genres), but these need to be integrated into the AI composition pipeline.

**Key Insight:** The AI already knows about world instruments (it named tracks correctly in the Indian test), but it's using GM fallback because the SFZ world instruments and MIDI routing aren't connected.

---

## Quick Status Check

```bash
# Verify what's implemented
ls src/musicgen/patterns/*.py      # ✅ Pattern system exists
ls src/musicgen/instruments/*.py     # ✅ Instrument definitions exist
ls src/musicgen/scales/*.py          # ✅ World scales exist
ls src/musicgen/genres/*.py          # ✅ Genre profiles exist
```

---

## Task 1: Connect World Instruments to AI Composer (CRITICAL)

**Problem:** AI generates "Sitar, Tabla, Bansuri" but renders to GM programs.

**Solution:** Update the AI composer's system prompt and instrument mapping.

### 1a. Update Instrument Selection Logic

**File:** `src/musicgen/composer_new/presets.py` or instrument selection

Add world instrument options:

```python
WORLD_INSTRUMENTS = {
    # Indian
    "sitar": {"midi_program": 104, "channel": 0, "name": "Sitar"},
    "tabla": {"midi_program": 115, "channel": 9, "drum": True, "name": "Tabla"},
    "bansuri": {"midi_program": 73, "channel": 1, "name": "Bansuri (Flute)"},
    "tanpura": {"midi_program": 104, "channel": 2, "drone": True, "name": "Tanpura"},
    "sarod": {"midi_program": 104, "channel": 3, "name": "Sarod"},
    "santoor": {"midi_program": 15, "channel": 4, "name": "Santoor (Dulcimer)"},

    # Middle Eastern
    "oud": {"midi_program": 24, "channel": 0, "name": "Oud (Guitar)"},
    "ney": {"midi_program": 73, "channel": 1, "name": "Ney (Flute)"},
    "darbuka": {"midi_program": 0, "channel": 9, "drum": True, "name": "Darbuka"},
    "kanun": {"midi_program": 6, "channel": 2, "name": "Kanun (Zither)"},

    # East Asian
    "koto": {"midi_program": 6, "channel": 0, "name": "Koto (Zither)"},
    "shakuhachi": {"midi_program": 72, "channel": 1, "name": "Shakuhachi (Flute)"},
    "guzheng": {"midi_program": 6, "channel": 2, "name": "Guzheng (Zither)"},

    # Guitars (need proper handling)
    "acoustic_guitar_steel": {"midi_program": 25, "channel": 0, "name": "Acoustic Guitar (Steel)"},
    "electric_guitar_clean": {"midi_program": 27, "channel": 0, "name": "Electric Guitar (Clean)"},
    "electric_bass": {"midi_program": 33, "channel": 1, "name": "Electric Bass"},
}
```

### 1b. Update System Prompt

**File:** `resources/system_prompt_v3.txt` or wherever the AI prompt is built

Add the world instrument knowledge:

```yaml
# Add to the instruments section

## World Instruments Available

### Indian Classical
- **Sitar**: Plucked string instrument, meend (glissando), gamak (oscillation)
- **Tabla**: Paired drums (bayan, dayan), bols (dha, din, tet), complex rhythmic cycles
- **Bansuri**: Bamboo flute, meend ornaments, ragas appropriate
- **Tanpura**: Drone instrument, provides Sa-PaSa or Sa-Ma-Sa-Sa-Sa
- **Sarod**: Fretless string, meend, gamak

### Middle Eastern
- **Oud**: Pear-shaped lute, microtonal (quarter tones), maqam system
- **Ney**: Reed flute, quarter tones, breathy tone
- **Darbuka**: Goblet drum, stroke types (doum, tek)
- **Kanun**: Zither with movable bridges, quarter tones

### East Asian
- **Koto**: 13-string zither, five-tone scales
- **Shakuhachi**: End-blown flute, pentatonic scales
- **Guzheng**: Chinese zither, pentatonic scales
```

---

## Task 2: Fix Test Import Errors

**Problem:** Tests importing `fold` function that doesn't exist.

**Solution:** Update test to use implemented functions.

**File:** `tests/test_v4_patterns.py`

```python
# Remove or fix the fold import
# from musicgen.patterns.combinators import fold  # Remove this line

# Use available functions:
from musicgen.patterns.combinators import (
    stack, cat, fastcat, overlay, choose
)
```

Run tests:
```bash
source .venv/bin/activate
uv run pytest tests/test_v4* -v
```

---

## Task 3: Create SFZ Instrument Definitions for World Instruments

**Problem:** SFZ files for sitar, tabla, bansuri don't exist.

**Solution:** Create placeholder SFZ definitions or reference free SFZ libraries.

### Option A: Reference Free SFZ Libraries

Document free SFZ libraries that have world instruments:

- **Sfatima Free SFZ**: https://sfzinstruments.github.io/
- **Versilian Studios**: https://versilian.studio/
- **VPO (Virtual Playing Orchestra)**: Has sitar sections
- **Sonatina Symphonic Orchestra**: Limited world instruments

### Option B: Create Simple SFZ Definitions

**File:** `resources/sfz/world/` (new directory)

Create minimal SFZ definitions for:

```
resources/sfz/world/
├── sitar.sfz
├── tabla.sfz
├── bansuri.sfz
├── tanpura.sfz
└── oud.sfz
```

**Minimal sitar.sfz example:**
```sfz
#include "sitar/samples"

<region>
  sample=0-48
  keyswitch=48
</region>
<group>
  keyswitch=48 sustain
  loop_mode=one_shot
  ampeg_attack=0.01
  ampeg_decay=0.5
  ampeg_release=0.3
  volume=0.7
<sample>
  sample=sitar_0
  pitch_keycenter=60
</sample>
```

---

## Task 4: Update Composer to Use Pattern System

**Problem:** Pattern system exists but not integrated with AI composer.

**Solution:** Connect pattern parser to the composition pipeline.

**File:** `src/musicgen/composer_new/composer.py` or appropriate location

Add pattern transformation options:

```python
def generate_with_pattern_style(
    self,
    prompt: str,
    pattern_style: str | None = None,  # "euclidean", "minimal", etc.
    transformations: list[str] | None = None  # ["slow 2", "rev"]
) -> AIComposition:
    """Generate composition with pattern-based considerations"""
```

---

## Task 5: Add Genre Selection to CLI

**Problem:** Genre selection exists in code but not in CLI.

**Solution:** Add `--genre` option to compose command.

**File:** `src/musicgen/__main__.py`

```python
@cmd_compose.command()
@click.argument("prompt", nargs=-1)
@click.option("--output-dir", default="output")
@click.option("--output-name", default=None)
@click.option("--format", multiple=True, default=["midi", "mp3"])
@click.option("--genre", type=str, help="Genre: rock, jazz, classical, electronic, world, etc.")
@click.option("--pattern-style", type=str, help="Pattern style: euclidean, minimal, etc.")
def compose(prompt, output_dir, output_name, format, genre, pattern_style, **kwargs):
    """Generate music from a prompt."""
    # Pass genre to AI composer
    composer = AIComposer(genre=genre)
    composition = composer.generate(" ".join(prompt))
```

---

## Task 6: Create Examples for New Features

**Create example scripts demonstrating V4 features:**

1. **examples/v4_pattern_demo.py** - Pattern manipulation demo
2. **examples/v4_world_music_demo.py** - Indian classical demo
3. **examples/v4_genre_demo.py** - Genre-specific generation

---

## Task 7: Fix Linting Issues

```bash
# Check for errors
source .venv/bin/activate
uv run ruff check src/musicgen/

# Fix auto-fixable issues
uv run ruff check --fix src/musicgen/

# Format code
uv run ruff format src/musicgen/

# Run type checking
uv run mypy src/musicgen/  # Fix any type issues
```

---

## Task 8: Update Documentation

### 8a. Update README.md

Add V4 features to main README with examples.

### 8b. Create V4 Quick Start

**File:** `docs/V4_QUICKSTART.md`

```markdown
# V4 Quick Start

## New Features in V4

### World Instruments
- Indian: Sitar, Tabla, Bansuri, Tanpura, Sarod
- Middle Eastern: Oud, Ney, Darbuka, Kanun
- East Asian: Koto, Shakuhachi, Guzheng, Erhu

### Pattern System
- Mini-notation: `musicgen pattern "bd(3,8) hh(5,8)"`
- Transformations: `musicgen transform --slow 2 pattern.mid`
- Euclidean rhythms
- World rhythms (clave, samba, talas)

### Genre Support
- Rock, Pop, Jazz, Classical, Electronic
- World genres (Indian, Middle Eastern, Latin, African)

## Usage

# Generate Indian classical music
musicgen compose "A raga in Yaman with alap jor and gat" --genre indian_classical

# Generate with pattern manipulation
musicgen pattern "bd(3,8) hh(5,8)" --visualize
```

---

## Priority Order for Remaining Tasks

| Priority | Task | Impact | Effort |
|----------|------|--------|--------|
| **HIGH** | Fix world instrument routing | AI will use correct sounds | Medium |
| **HIGH** | Add genre CLI option | Users can specify genres | Low |
| **MEDIUM** | Fix test imports | Tests will pass | Low |
| **MEDIUM** | Create world SFZ definitions | Better audio quality | High |
| **LOW** | Integrate pattern system | Advanced users | Medium |
| **LOW** | Live coding features | Niche use case | High |

---

## Quick Win: Immediate Fix

To get the AI to use correct instrument sounds right now (without SFZ), update the GM program mappings to be more accurate:

```python
# In instruments/midi_map.py or wherever mapping happens
WORLD_INSTRUMENT_MAPPINGS = {
    "sitar": 104,  # This already exists in GM!
    "tabla": None,  # Use custom drum mapping on channel 10
    "bansuri": 73,  # Flute is close enough
    "tanpura": 104,  # Sitar (drone mode)
    "oud": 24,  # Guitar nylon
    "koto": 6,   # Harpsichord (closest)
}
```

---

## Implementation Checklist

- [ ] Fix test import errors
- [ ] Update AI prompt with world instrument knowledge
- [ ] Connect world instruments to MIDI routing
- [ ] Add `--genre` CLI option
- [ ] Create V4 example scripts
- [ ] Update main README with V4 features
- [ ] Run ruff/format/linting
- [ ] Create SFZ instrument definitions (optional but recommended)

---

## Next Steps

1. **Decide priority** - What's most important: better sound (SFZ) or genre selection (CLI)?
2. **Create implementation plan** - I can generate specific code for any task
3. **Execute** - I can implement the fixes step by step

What would you like to tackle first?
