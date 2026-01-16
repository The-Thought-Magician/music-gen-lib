# V3 Implementation Prompt

Copy and paste this prompt into a new chat session to implement the complete V3 roadmap.

---

# Music-Gen-Lib V3 Implementation: World-Class Orchestral Music Generation

## Context

You are implementing the V3 roadmap for music-gen-lib, a Python-based AI music generation system. The goal is to create world-class orchestral music generation using:

1. **SFZ format** for professional sample library support with articulations
2. **Comprehensive music theory knowledge** encoded in system prompts
3. **Full validation pipeline** for voice leading and orchestration rules
4. **End-to-end rendering** from prompt to audio

## Project Structure

```
music-gen-lib/
├── src/musicgen/
│   ├── ai_models/          # Pydantic models
│   ├── composer/           # Composer classes
│   ├── validation/         # Validation tools
│   ├── midi/               # MIDI generation
│   ├── sfz/                # SFZ rendering
│   ├── theory/             # Music theory (existing)
│   └── orchestration/      # Orchestration (existing)
├── docs/steps/             # Roadmap steps (V3 defined, V1/V2 completed)
├── resources/
│   ├── system_prompt.txt   # Music theory system prompt
│   ├── instrument_definitions.yaml  # Instrument configs
│   └── sfz_libraries/      # SFZ libraries (user-provided)
├── tests/                  # Test suite
└── pyproject.toml
```

## Implementation Plan

### Step 1: Setup and Foundation

1. **Create todo list tracking** - Use TodoWrite to track all V3-01 through V3-11 steps
2. **Review existing codebase** - Use Explore agent to understand current architecture
3. **Create new package structure** - Create directories for validation, midi, sfz

### Step 2: Read All Roadmap Steps

Read all V3 step files to understand complete requirements:
- `docs/steps/v3-01-sfz-introduction-and-research.md`
- `docs/steps/v3-02-sfz-instrument-definition-layer.md`
- `docs/steps/v3-03-sfz-renderer-integration.md`
- `docs/steps/v3-04-articulation-system.md`
- `docs/steps/v3-05-music-theory-system-prompt.md`
- `docs/steps/v3-06-composition-schema.md`
- `docs/steps/v3-07-validation-tools.md`
- `docs/steps/v3-08-midi-generator.md`
- `docs/steps/v3-09-ai-composer-integration.md`
- `docs/steps/v3-10-testing.md`
- `docs/steps/v3-11-documentation.md`

### Step 3: Implementation Order

**CRITICAL: Follow this exact order with commits after each step:**

#### Phase 1: Core Models (V3-06 first, as others depend on it)
1. Create Pydantic models in `src/musicgen/ai_models/v3/`:
   - `articulation.py` - ArticulationType, KeyswitchEvent
   - `notes.py` - Note, CCEvent, PitchBendEvent
   - `parts.py` - InstrumentPart
   - `composition.py` - Composition, CompositionRequest
   - `__init__.py` - Exports

**Commit:** "feat(v3): add core Pydantic models for composition"

#### Phase 2: Instrument Definitions (V3-02)
2. Create `resources/instrument_definitions.yaml` with:
   - All orchestral instruments (strings, woodwinds, brass, percussion, keyboards)
   - Ranges per dynamic
   - Articulation mappings with keyswitches
   - Ensemble presets

3. Create `src/musicgen/orchestration/definitions.py`:
   - Load YAML definitions
   - InstrumentDefinition model
   - Helper functions

**Commit:** "feat(v3): add instrument definition layer with YAML configs"

#### Phase 3: Validation (V3-07)
4. Create `src/musicgen/validation/`:
   - `voice_leading.py` - VoiceLeadingValidator
   - `orchestration.py` - OrchestrationValidator
   - `validator.py` - CompositionValidator
   - `models.py` - ValidationResult, error models

**Commit:** "feat(v3): add validation tools for voice leading and orchestration"

#### Phase 4: MIDI Generation (V3-08)
5. Create `src/musicgen/midi/`:
   - `generator.py` - EnhancedMIDIGenerator
   - `articulations.py` - ArticulationHelper
   - Export functions for stems

**Commit:** "feat(v3): add enhanced MIDI generator with keyswitch support"

#### Phase 5: SFZ Renderer (V3-03)
6. Create `src/musicgen/sfz/`:
   - `renderer.py` - SFZRenderer, MultiInstrumentRenderer
   - `installation.py` - Installation checker
   - Post-processing helpers

7. Add dependencies to `pyproject.toml`:
   - `mido` for MIDI I/O
   - `pyyaml` for YAML parsing
   - Keep `pretty-midi` as fallback
   - Keep `pydub` for audio processing

**Commit:** "feat(v3): add SFZ renderer integration"

#### Phase 6: System Prompt (V3-05)
8. Create `resources/system_prompt_v3.txt`:
   - Copy full content from V3-05 step
   - Include all music theory knowledge

9. Create `src/musicgen/prompts/`:
   - `loader.py` - Load and format system prompts
   - `templates.py` - Prompt templates for different styles

**Commit:** "feat(v3): add comprehensive music theory system prompt"

#### Phase 7: AI Composer (V3-09)
10. Create `src/musicgen/composer_v3.py`:
    - AIComposerV3 main class
    - Integration of all components
    - Retry logic with validation feedback
    - Render pipeline

11. Update CLI in `src/musicgen/cli/`:
    - Add `musicgen-v3 compose` command
    - Support all options (style, form, ensemble, etc.)

**Commit:** "feat(v3): add AI composer integration"

#### Phase 8: Articulation System (V3-04)
12. Extend articulation support:
    - Add articulation_duration modifiers
    - Add articulation_velocity modifiers
    - Keyswitch timing helpers

**Commit:** "feat(v3): add articulation system with timing and modifiers"

#### Phase 9: Testing (V3-10)
13. Create comprehensive test suite:
    - `tests/test_v3_models.py` - Model tests
    - `tests/test_v3_midi.py` - MIDI generator tests
    - `tests/test_v3_validation.py` - Validation tests
    - `tests/test_v3_integration.py` - End-to-end tests
    - `tests/conftest.py` - Pytest fixtures

14. Update `pyproject.toml` with test dependencies:
    - `pytest`
    - `pytest-cov`
    - `hypothesis` (for property-based tests)

**Commit:** "feat(v3): add comprehensive test suite"

#### Phase 10: Documentation (V3-11)
15. Create documentation:
    - `docs/INSTALLATION.md` - Installation with SFZ
    - `docs/V3_QUICKSTART.md` - Quick start guide
    - `docs/V3_API.md` - API reference
    - `docs/V3_EXAMPLES.md` - Usage examples

**Commit:** "feat(v3): add V3 documentation"

#### Phase 11: Research and Setup (V3-01)
16. Create setup guide:
    - `docs/SFZ_SETUP.md` - SFZ library download instructions
    - Scripts to download free SFZ libraries

**Commit:** "docs(v3): add SFZ setup and library download guide"

### Step 4: Testing and Quality Assurance

1. Run all tests:
   ```bash
   uv run pytest tests/ -v --cov=src/musicgen
   ```

2. Fix any failing tests

3. Create example script `examples/v3_demo.py`:
   - Generate a simple composition
   - Validate it
   - Export to MIDI
   - Demonstrate full pipeline

**Commit:** "test(v3): add example demo and fix test issues"

### Step 5: Final Integration

1. Update main package `__init__.py` to export V3 classes

2. Create changelog entry

3. Final test run

**Commit:** "chore(v3): final integration and cleanup"

## Commands to Use

### Package Management (uv)
```bash
# Install dependencies
uv sync

# Run tests
uv run pytest tests/

# Run example
uv run python examples/v3_demo.py

# Try CLI
uv run musicgen-v3 compose "A gentle melody" --output test.wav
```

### Git Workflow
After each major phase:
```bash
git add .
git commit -m "feat(v3): descriptive message"
```

## Important Notes

1. **Use Task agents** for complex multi-file work:
   - Use `general-purpose` agent for implementation
   - Use `code-reviewer` agents to review code
   - Use `unit-testing` agent to write tests

2. **Read before writing** - Always read existing files before modifying

3. **Follow existing patterns** - Match the code style of V2 modules

4. **Type hints required** - All functions must have type hints

5. **Docstrings required** - All public classes/functions need docstrings

6. **Validate against schema** - Run `uv run pydantic-core` checks

## Success Criteria

- [ ] All V3 models created and validated
- [ ] Instrument definitions YAML exists
- [ ] Validation tools catch parallel fifths
- [ ] MIDI generator produces files with keyswitches
- [ ] SFZ renderer wrapper works with sfizz
- [ ] System prompt contains full theory content
- [ ] AIComposerV3 integrates all components
- [ ] Tests pass with >80% coverage
- [ ] Documentation is complete
- [ ] Example script demonstrates full pipeline

## Getting Help

- Reference `docs/steps/README.md` for overview
- Reference individual step files for detailed specs
- Use Explore agent to understand existing code
- Use code-review agents to validate implementations
