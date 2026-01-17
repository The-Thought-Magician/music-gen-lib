# V4 Implementation Prompt

Copy and paste this prompt into a new chat session to implement the complete V4 roadmap.

---

# Music-Gen-Lib V4 Implementation: Universal Music Generation System

## Context

You are implementing the V4 roadmap for music-gen-lib, building on the completed V3 orchestral music generation system. V4's goal is to create a **universal music generation system** that supports:

1. **All instrument types** - Guitars, drums, world/ethnic instruments, electronic
2. **Pattern manipulation** - TidalCycles-inspired transformation functions
3. **Advanced rhythm** - Euclidean rhythms, polymetric structures
4. **Extended scales** - Indian ragas, Middle Eastern maqamat, Japanese scales
5. **Genre intelligence** - Style-aware composition for all musical genres
6. **Live coding mode** - Real-time pattern manipulation (basic)

## Project Structure

```
music-gen-lib/
├── src/musicgen/
│   ├── ai_models/          # Existing Pydantic models
│   ├── composer_new/       # Existing AI composer
│   ├── validation/         # Existing validation
│   ├── renderer/           # Existing rendering
│   ├── sfz/                # Existing SFZ integration
│   ├── theory/             # Existing music theory
│   ├── orchestration/      # Existing orchestration
│   ├── patterns/           # NEW: Pattern manipulation
│   ├── instruments/        # NEW: Extended instrument definitions
│   ├── genres/             # NEW: Genre-specific styles
│   └── scales/             # NEW: World music scales
├── docs/steps/             # Roadmap steps (V4 defined below, V3 completed)
├── resources/
│   ├── system_prompt_v3.txt  # Existing system prompt
│   ├── system_prompt_v4.txt  # NEW: Extended with world music
│   ├── instrument_definitions.yaml    # Existing orchestral
│   ├── instrument_definitions_world.yaml # NEW: World instruments
│   ├── genre_profiles.yaml              # NEW: Genre definitions
│   └── scale_definitions.yaml           # NEW: World scales
├── tests/                  # Test suite
└── pyproject.toml
```

## Prerequisites

### Environment Setup

**CRITICAL: Always use `uv` for package management, NEVER pip without explicit user approval:**

```bash
# Activate virtual environment
source .venv/bin/activate

# Install/add dependencies
uv add package-name

# Install dev dependencies
uv add --dev package-name

# Run commands
uv run python script.py
uv run pytest tests/
uv run ruff check .
uv run ruff format .
```

### Code Quality Standards

**Always run linting and formatting before committing:**

```bash
# Format code
uv run ruff format src/ tests/

# Check for issues
uv run ruff check src/ tests/

# Fix auto-fixable issues
uv run ruff check --fix src/ tests/

# Type checking
uv run mypy src/musicgen/
```

**Ruff Configuration (pyproject.toml):**
- Line length: 100
- Quote style: Double
- Indent style: Spaces

### Commit Standards

After each step:
```bash
git add .
git commit -m "feat(v4): brief description"
```

Commit message prefixes:
- `feat(v4):` - New feature
- `fix(v4):` - Bug fix
- `refactor(v4):` - Code refactoring
- `test(v4):` - Tests
- `docs(v4):` - Documentation
- `chore(v4):` - Maintenance

## Implementation Plan

### Phase 0: Foundation (Steps V4-01 to V4-03)

#### Step V4-01: Project Setup and Planning
- Create todo list with all V4 steps
- Review V3 completion status
- Create V4 package structure
- Set up new dependencies

#### Step V4-02: Extended Instrument Schema
- Extend Pydantic models for new instrument types
- Add guitar-specific attributes (frets, strings, techniques)
- Add drum kit models
- Add world instrument models

#### Step V4-03: MIDI Program Number Mapping
- Create complete GM/GM2/GS program number registry
- Map all 128 MIDI programs to instrument names
- Create lookup utilities

### Phase 1: Guitar and Bass Instruments (Steps V4-04 to V4-08)

#### Step V4-04: Guitar Instrument Definitions
- Acoustic Guitar (nylon/steel)
- Electric Guitar (clean, overdrive, distortion)
- Electric Bass
- Techniques: strumming, picking, harmonics, slides, bends

#### Step V4-05: Guitar Articulation System
- Strum patterns (down, up, down-up)
- Palm muting
- Hammer-ons, pull-offs
- Bends, vibrato, slides
- Harmonics (natural, artificial, pinch)

#### Step V4-06: Guitar Chord Library
- Common chord voicings (open, barre, power)
- Jazz extensions (7th, 9th, 11th, 13th)
- Folk/Country voicings
- Alternate tunings support

#### Step V4-07: Bass Instrument Definitions
- Electric Bass (finger, pick, slap)
- Upright Bass (jazz arco/pizz)
- Bass effects and techniques

#### Step V4-08: Guitar/Bass MIDI Generation
- Fretboard position calculation
- String assignment logic
- Chord voicing optimization
- Realistic picking patterns

### Phase 2: Drum Kits and Percussion (Steps V4-09 to V4-13)

#### Step V4-09: Drum Kit Definitions
- Standard Rock Kit
- Jazz Kit
- Electronic Kit
- World percussion kits
- GM drum map implementation

#### Step V4-10: Drum Pattern System
- Basic patterns (rock, pop, jazz, funk)
- Fill generation
- Ghost notes and accents
- Swing and groove implementation

#### Step V4-11: Drum Articulation System
- Sticks, brushes, mallets
- Hi-hat techniques (open, closed, pedal)
- Cymbal articulations (crash, ride, splash, china)
- Kick drum techniques

#### Step V4-12: World Percussion Definitions
- Latin (conga, bongo, timbale, claves)
- African (djimbe, dunun, talking drum)
- Indian (tabla, mridangam)
- Japanese (taiko)
- Middle Eastern (darbuka, riq, daf)

#### Step V4-13: Percussion Pattern Generation
- Afro-Cuban rhythms
- Brazilian patterns
- Indian talas
- West African polyrhythms

### Phase 3: World Instruments (Steps V4-14 to V4-20)

#### Step V4-14: Indian Classical Instruments
- Sitar (meend, gamak, krintan)
- Sarod
- Bansuri
- Tanpura (drone)
- Santoor

#### Step V4-15: Indian Raga System
- Raga definitions (Yaman, Bhairavi, Bhairav, etc.)
- Alap, jor, gat structure
- Tala cycles (teental, jhaptal, rupak, etc.)
- Microtonal support (sruti)

#### Step V4-16: Middle Eastern Instruments
- Oud
- Ney (flute)
- Darbuka
- Kanun (zither)
- Buq (horn)

#### Step V4-17: Arabic Maqam System
- Maqam definitions (Hijaz, Sikah, Rast, etc.)
- Quarter-tone implementation
- Ajnas (scale fragments)
- Taqsim (improvisation) patterns

#### Step V4-18: East Asian Instruments
- Koto (Japan)
- Shakuhachi (Japan)
- Guzheng (China)
- Erhu (China)
- Gayageum (Korea)

#### Step V4-19: Pentatonic Scale Systems
- Japanese scales (In, Hirajoshi, Miyakobushi)
- Pentatonic modes (major, minor, blues)
- Slendro and Pelog (Indonesia)

#### Step V4-20: Other World Instruments
- Hawaiian/Steel Guitar
- Bagpipe
- Irish Tin Whistle
- Uilleann Pipes
- Accordion
- Bandoneon

### Phase 4: Pattern Manipulation (Steps V4-21 to V4-27)

#### Step V4-21: Pattern Mini-notation Parser
- Parse TidalCycles-style patterns
- Support rests, grouping, repetition
- Support alternation and randomization
- Support Euclidean rhythms

#### Step V4-22: Euclidean Rhythm Implementation
- Bjorklund algorithm
- Euclidean rhythm functions
- Offset support
- Visual pattern representation

#### Step V4-23: Pattern Transformation Functions
- `slow`, `fast`, `density`
- `rev`, `palindrome`
- `rotate`, `repeat`
- `degrade`, `degradeBy`

#### Step V4-24: Pattern Combinators
- `stack` (layer patterns)
- `cat`, `fastcat` (concatenate)
- `overlay` (superimpose)
- `choose` (random selection)

#### Step V4-25: Polymetric and Polyrhythmic Support
- Independent time signatures per part
- Polyrhythmic pattern generation
- Cross-ratio handling
- Phasing patterns

#### Step V4-26: Randomness and Stochastic Patterns
- `rand`, `irand`
- `choose`, `chooseBy`
- `shuffle`
- `sometimes` (probabilistic application)

#### Step V4-27: Pattern State and History
- Cycle tracking
- Pattern iteration
- Pattern freezing/unfreezing
- Cycle-based addressing

### Phase 5: Genre Intelligence (Steps V4-28 to V4-33)

#### Step V4-28: Genre Profile Definitions
- Rock/Pop
- Jazz (swing, bebop, fusion)
- Classical (periods: baroque, classical, romantic, modern)
- Electronic (techno, house, ambient, DnB)
- World (regional styles)

#### Step V4-29: Genre-Specific Patterns
- Drum patterns per genre
- Bass line patterns
- Chord progression tendencies
- Instrumentation conventions

#### Step V4-30: Style Transfer System
- Apply genre characteristics to compositions
- Hybrid genre support
- Style intensity control

#### Step V4-31: Form and Structure Templates
- Song forms (verse-chorus, AABA, etc.)
- Classical forms (sonata, rondo, theme & variations)
- Electronic forms (building arrangements)
- Indian classical forms

#### Step V4-32: Arrangement Intelligence
- Instrument density by section
- Dynamic arcs
- Texture layering
- Transitions and modulations

#### Step V4-33: Groove and Feel System
- Swing amount control
- Groove templates
- Humanization (timing, velocity)
- Micro-timing adjustments

### Phase 6: Electronic Instruments (Steps V4-34 to V4-37)

#### Step V4-34: Synthesizer Definitions
- Subtractive synth basics
- FM synthesis parameters
- Wavetable synthesis
- Granular synthesis

#### Step V4-35: Synthesizer Patterns
- Arpeggiator patterns
- Sequencer patterns
- Modulation routing
- Patch management

#### Step V4-36: Drum Machine Definitions
- Roland TR-808/909 kits
- Vintage drum machines
- Electronic percussion
- Pattern storage

#### Step V4-37: Electronic Effects
- Filter sweeps
- LFO modulation
- Delay, reverb, chorus
- Distortion and saturation

### Phase 7: Live Coding Mode (Steps V4-38 to V4-42)

#### Step V4-38: Live Coding Server
- WebSocket or OSC server
- Real-time code evaluation
- Pattern state management
- Multi-user support

#### Step V4-39: Stream-Based Rendering
- Continuous audio output
- Buffer management
- Dropout prevention

#### Step V4-40: Pattern Manipulation API
- Live pattern transformation
- Parameter modulation
- Cue and transition system

#### Step V4-41: Visual Feedback
- Pattern visualization
- Cycle indicator
- Instrument status

#### Step V4-42: Performance Presets
- Prepared patterns
- Scene management
- Transition patterns

### Phase 8: Integration and Testing (Steps V4-43 to V4-47)

#### Step V4-43: Extended System Prompt
- Update with all new instruments
- Add world music theory
- Add genre-specific guidance
- Pattern manipulation documentation

#### Step V4-44: Instrument Selection Intelligence
- Automatic instrument choice from genre
- Substitute instrument suggestions
- Combination validation

#### Step V4-45: Comprehensive Test Suite
- Tests for all new instruments
- Pattern manipulation tests
- Genre pattern tests
- World scale tests

#### Step V4-46: Integration Testing
- End-to-end composition tests
- Cross-genre generation tests
- Multi-instrument validation
- Performance benchmarks

#### Step V4-47: Examples and Documentation
- Genre-specific examples
- World music examples
- Pattern manipulation examples
- Live coding guide

### Phase 9: Final Polish (Steps V4-48 to V4-50)

#### Step V4-48: CLI Enhancements
- New commands for patterns
- Genre selection
- Instrument listing
- Preview mode

#### Step V4-49: Performance Optimization
- Caching for patterns
- Lazy evaluation
- Parallel processing where possible

#### Step V4-50: Release Preparation
- Version bump
- Migration guide
- CHANGELOG update
- Release notes

## Step-by-Step Execution

### Initial Setup

1. **Create tracking todo list:**
```python
todos = [
    {"content": "V4-01: Project Setup and Planning", "status": "pending"},
    {"content": "V4-02: Extended Instrument Schema", "status": "pending"},
    # ... all 50 steps
]
```

2. **Read all V4 step files** in `docs/steps/v4-*.md`

3. **Create new package directories:**
```bash
mkdir -p src/musicgen/patterns
mkdir -p src/musicgen/instruments
mkdir -p src/musicgen/genres
mkdir -p src/musicgen/scales
mkdir -p resources/instruments
```

4. **Add new dependencies:**
```bash
uv add websockets  # For live coding
uv add numpy      # For pattern calculations
```

### Implementation Order

**CRITICAL: Follow phases in order, but steps within phases can be parallelized:**

1. **Phase 0 (Foundation)** - MUST BE FIRST
2. **Phase 1 (Guitars)** - High priority, commonly used
3. **Phase 2 (Drums)** - High priority, commonly used
4. **Phase 3 (World)** - Medium priority
5. **Phase 4 (Patterns)** - Can be done in parallel with 1-3
6. **Phase 5 (Genres)** - Depends on instruments
7. **Phase 6 (Electronic)** - Lower priority
8. **Phase 7 (Live)** - Depends on patterns
9. **Phase 8 (Testing)** - After all implementation
10. **Phase 9 (Polish)** - LAST

## Testing Commands

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test
uv run pytest tests/test_v4_guitars.py -v

# Run with coverage
uv run pytest tests/ --cov=src/musicgen --cov-report=html

# Run type checking
uv run mypy src/musicgen/

# Run linting
uv run ruff check src/ tests/

# Format code
uv run ruff format src/ tests/
```

## Git Workflow

After **each step** (or after closely related steps):
```bash
git add .
git commit -m "feat(v4): step-name-here"
```

Major milestones should be tagged:
```bash
git tag v4.0.0-alpha.1
```

## Important Notes from V3 Experience

1. **Read before writing** - Always use Read tool before Edit
2. **Use Task agents** - For complex multi-file operations
3. **Test incrementally** - Don't wait until the end
4. **Document as you go** - Don't leave documentation for last
5. **Type hints everywhere** - No exceptions
6. **Validation is key** - Validate early and often
7. **Error messages matter** - Make them helpful
8. **Performance matters** - Profile before optimizing

## Success Criteria

- [ ] All 50 steps completed
- [ ] Guitar instruments working with realistic patterns
- [ ] Drum kits with genre-specific patterns
- [ ] At least 10 world instrument families
- [ ] Pattern manipulation system functional
- [ ] Euclidean rhythms working
- [ ] Genre profiles for 10+ genres
- [ ] Live coding basic mode working
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Examples for each major feature

## Getting Help

- Reference `docs/STEP_PLAN.md` for overview
- Reference individual V4 step files for specs
- Reference V3 completed steps for patterns
- Use Explore agent to understand existing code
- Use code-review agents to validate implementations

## V4 Step Files Reference

- `v4-01-project-setup.md`
- `v4-02-extended-instrument-schema.md`
- `v4-03-midi-program-mapping.md`
- `v4-04-guitar-instrument-definitions.md`
- `v4-05-guitar-articulation-system.md`
- `v4-06-guitar-chord-library.md`
- `v4-07-bass-instrument-definitions.md`
- `v4-08-guitar-bass-midi-generation.md`
- `v4-09-drum-kit-definitions.md`
- `v4-10-drum-pattern-system.md`
- `v4-11-drum-articulation-system.md`
- `v4-12-world-percussion-definitions.md`
- `v4-13-percussion-pattern-generation.md`
- `v4-14-indian-classical-instruments.md`
- `v4-15-indian-raga-system.md`
- `v4-16-middle-eastern-instruments.md`
- `v4-17-arabic-maqam-system.md`
- `v4-18-east-asian-instruments.md`
- `v4-19-pentatonic-scale-systems.md`
- `v4-20-other-world-instruments.md`
- `v4-21-pattern-mini-notation-parser.md`
- `v4-22-euclidean-rhythm-implementation.md`
- `v4-23-pattern-transformation-functions.md`
- `v4-24-pattern-combinators.md`
- `v4-25-polymetric-polyrhythmic-support.md`
- `v4-26-randomness-stochastic-patterns.md`
- `v4-27-pattern-state-history.md`
- `v4-28-genre-profile-definitions.md`
- `v4-29-genre-specific-patterns.md`
- `v4-30-style-transfer-system.md`
- `v4-31-form-structure-templates.md`
- `v4-32-arrangement-intelligence.md`
- `v4-33-groove-feel-system.md`
- `v4-34-synthesizer-definitions.md`
- `v4-35-synthesizer-patterns.md`
- `v4-36-drum-machine-definitions.md`
- `v4-37-electronic-effects.md`
- `v4-38-live-coding-server.md`
- `v4-39-stream-based-rendering.md`
- `v4-40-pattern-manipulation-api.md`
- `v4-41-visual-feedback.md`
- `v4-42-performance-presets.md`
- `v4-43-extended-system-prompt.md`
- `v4-44-instrument-selection-intelligence.md`
- `v4-45-comprehensive-test-suite.md`
- `v4-46-integration-testing.md`
- `v4-47-examples-documentation.md`
- `v4-48-cli-enhancements.md`
- `v4-49-performance-optimization.md`
- `v4-50-release-preparation.md`

---

**Begin implementation by reading all V4 step files and creating the todo list. Good luck!**
