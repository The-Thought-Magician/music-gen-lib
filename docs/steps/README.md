# V3 Roadmap: World-Class Orchestral Music Generation

**Goal:** Create an AI-powered music generation system that produces world-class orchestral music while preserving centuries of music theory knowledge.

**Vision:** Unlike black-box AI music generators (Suno, etc.), this system encodes music theory knowledge explicitly, ensuring AI compositions respect voice leading, orchestration practices, and formal structures.

---

## Overview

The V3 roadmap focuses on three major pillars:

1. **SFZ Integration** — Professional sample library support with articulations
2. **Music Theory Knowledge** — Comprehensive system prompt encoding centuries of theory
3. **Quality Pipeline** — Validation, MIDI generation, and audio rendering

---

## Steps

### Phase 1: SFZ Foundation

| Step | Title | Status | Description |
|------|-------|--------|-------------|
| [V3-01](./v3-01-sfz-introduction-and-research.md) | SFZ Introduction and Research | Pending | Research SFZ format, free libraries, sfizz renderer |
| [V3-02](./v3-02-sfz-instrument-definition-layer.md) | SFZ Instrument Definition Layer | Pending | YAML configuration for all orchestral instruments with ranges, articulations, keyswitches |
| [V3-03](./v3-03-sfz-renderer-integration.md) | SFZ Renderer Integration | Pending | Python wrapper for sfizz-render with multi-instrument support |
| [V3-04](./v3-04-articulation-system.md) | Articulation System Design | Pending | Articulation model, keyswitch handling, expression |

### Phase 2: Music Theory & AI

| Step | Title | Status | Description |
|------|-------|--------|-------------|
| [V3-05](./v3-05-music-theory-system-prompt.md) | Music Theory System Prompt | Pending | Comprehensive system prompt encoding theory, orchestration, forms |
| [V3-06](./v3-06-composition-schema.md) | Enhanced Composition Output Schema | Pending | Pydantic models for notes with articulations, keyswitches, CC events |
| [V3-07](./v3-07-validation-tools.md) | Validation Tools for Music Theory Rules | Pending | Voice leading, orchestration, and range validation |

### Phase 3: Generation & Rendering

| Step | Title | Status | Description |
|------|-------|--------|-------------|
| [V3-08](./v3-08-midi-generator.md) | Enhanced MIDI Generator | Pending | MIDI generation with keyswitches, CC events, proper timing |
| [V3-09](./v3-09-ai-composer-integration.md) | AI Composer Integration | Pending | End-to-end pipeline: prompt → AI → validation → MIDI → audio |
| [V3-10](./v3-10-testing.md) | Testing and Quality Assurance | Pending | Unit tests, integration tests, property-based tests |
| [V3-11](./v3-11-documentation.md) | Documentation and Examples | Pending | User guides, API reference, examples |

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER PROMPT                                 │
│              "A melancholic string quartet..."                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│              SYSTEM PROMPT + INSTRUMENT DEFINITIONS                 │
│  • Music theory knowledge (voice leading, harmony, forms)           │
│  • Orchestration practices (ranges, balance, articulations)        │
│  • Stylistic guidelines (Baroque, Classical, Romantic, etc.)       │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         AI (GEMINI)                                 │
│  Generates: Composition with notes, articulations, keyswitches     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      VALIDATION LAYER                               │
│  • Voice leading checks (parallel 5ths/octaves)                    │
│  • Orchestration checks (ranges, balance)                          │
│  • Structure checks (duration, completeness)                       │
└─────────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              ❌ Errors            ✓ Valid
                    │                   │
                    ▼                   ▼
            Retry with feedback   MIDI GENERATOR
                                        │
                                        ▼
                                ┌───────────────┴───────────────┐
                                ▼                               ▼
                          MIDI File                    STEM Export
                                │                               │
                                ▼                               ▼
                          SFZ RENDERER                    SFZ RENDERER
                                │                               │
                                └───────────────┬───────────────┘
                                                ▼
                                        AUDIO POST-PROCESS
                                                │
                                                ▼
                                    ┌───────────────────┐
                                    ▼                   ▼
                              MIXED AUDIO          INDIVIDUAL STEMS
                              (WAV/MP3)              (WAV)
```

---

## Key Features

### Articulations

Support for realistic playing techniques:

| Strings | Woodwinds | Brass |
|---------|-----------|-------|
| Legato | Flutter | Muted |
| Staccato | Staccato | Falls |
| Spiccato | Legato | Doits |
| Pizzicato | Breath Attack | Shakes |
| Tremolo | | |
| Sul Ponticello | | |
| Col Legno | | |

### Music Theory

Encoded knowledge includes:

- **Counterpoint**: Fuxian species, Bach practices
- **Voice Leading**: No parallel 5ths/octaves, proper resolution
- **Harmony**: Functional harmony, circle of fifths, secondary dominants
- **Forms**: Sonata, rondo, binary, ternary, through-composed
- **Orchestration**: Ranges per dynamic, balance, doubling practices

### Validation

Automated checks for:

- Parallel perfect intervals
- Unresolved tendency tones
- Instrument range violations
- Balance issues
- Minimum duration requirements

---

## Free SFZ Libraries

| Library | Size | Instruments | License |
|---------|------|-------------|----------|
| [Sonatina Symphonic Orchestra](https://github.com/peastman/sso) | 440MB | Full orchestra | CC-BY |
| [Virtual Playing Orchestra](https://virtualplaying.com/virtual-playing-orchestra/) | 1.3GB | Full orchestra | Freeware |
| [Salamander Grand Piano](https://github.com/sfzinstruments/SalamanderGrandPiano) | 3.5GB | Piano | CC0 |

---

## Progress Tracking

- [ ] V3-01: SFZ Introduction and Research
- [ ] V3-02: SFZ Instrument Definition Layer
- [ ] V3-03: SFZ Renderer Integration
- [ ] V3-04: Articulation System Design
- [ ] V3-05: Music Theory System Prompt
- [ ] V3-06: Enhanced Composition Output Schema
- [ ] V3-07: Validation Tools
- [ ] V3-08: Enhanced MIDI Generator
- [ ] V3-09: AI Composer Integration
- [ ] V3-10: Testing
- [ ] V3-11: Documentation

---

## Completed Versions

### V2

- Configuration system
- Schema generation
- AI note sequence models
- Gemini client integration
- AI composer
- Rendering engine
- CLI redesign
- Type safety
- Schema fixes
- Enhanced prompts
- Quality validation
- Polyphony support
- Global timeline
- Continuous controllers
- Tempo/meter fluidity
- Chunking strategy

### V1

- Project setup and core structures
- Scales and keys
- Chord progressions
- Voice leading
- Melody generation
- Orchestration basics
- Musical forms
- MIDI generation
- Audio synthesis (FluidSynth)
- MusicXML generation
- Lilypond generation
- Mood interface
- Testing and documentation
- Audio export
- AI composition interface
- Complete orchestration
- CLI enhancements
