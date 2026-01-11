# Project Decisions

## Project Setup Phase

### Date: 2025-01-11

---

## Decision 1: Project Name and Structure

**Date**: 2025-01-11
**Status**: Accepted

**Context**: Need to name the project and establish directory structure.

**Decision**:
- **Project Name**: `musicgen-lib`
- **Structure**: Standard Python package with `src/musicgen/` layout
- **Documentation**: Centralized in `docs/` folder

**Rationale**: Follows Python packaging best practices (src layout), separates documentation from code.

---

## Decision 2: Technology Stack

**Date**: 2025-01-11
**Status**: Accepted

**Context**: Need to select libraries for music theory, MIDI, audio, and sheet music.

**Decision**:

| Component | Library | Justification |
|-----------|---------|---------------|
| Music Theory | music21, mingus | music21: comprehensive; mingus: practical |
| MIDI I/O | mido, pretty_midi | mido: low-level; pretty_midi: high-level |
| Audio Synthesis | pyfluidsynth | Python bindings for FluidSynth |
| SoundFont | GeneralUser GS | Free, comprehensive orchestral sounds |
| Sheet Music | Abjad + LilyPond | Publication-quality output |
| MusicXML | music21 | Built-in MusicXML support |

**Rationale**: This stack provides:
- Full music theory capabilities
- Industry-standard MIDI support
- High-quality audio synthesis
- Professional sheet music output
- No AI/ML dependencies (rule-based approach)

---

## Decision 3: Output Format Order

**Date**: 2025-01-11
**Status**: Accepted

**Context**: User wants both sheet music AND audio files.

**Decision**: Implement in this order:
1. MIDI (Step 8) - Validates composition logic, universally compatible
2. Audio (Step 9) - Uses MIDI as input, adds synthesis
3. MusicXML (Step 10) - For notation software compatibility
4. LilyPond/PDF (Step 11) - For publication-quality sheet music

**Rationale**: MIDI → Audio builds on previous output. Sheet music formats are independent but benefit from validated composition logic.

---

## Decision 4: Plugin Configuration

**Date**: 2025-01-11
**Status**: Accepted

**Context**: Choose Claude Code plugins for this Python project.

**Decision**:
- `python-development` - Python-specific support
- `unit-testing` - Automated test generation
- `code-review-ai` - Architectural review
- `comprehensive-review` - Multi-perspective review
- `code-documentation` - Documentation help

**Rationale**: Covers Python development, testing, quality assurance, and documentation needs.

---

## Decision 5: Step Breakdown

**Date**: 2025-01-11
**Status**: Accepted

**Context**: How to break down this complex project?

**Decision**: 13 steps following dependency chain:
1. Project Setup + Core Data Structures
2. Scales and Keys
3. Chord Progressions
4. Voice Leading
5. Melody Generation
6. Orchestration
7. Musical Forms
8. MIDI Export
9. Audio Synthesis
10. MusicXML Export
11. LilyPond Export
12. Mood Interface
13. Testing & Documentation

**Rationale**: Bottom-up approach - build foundations (data structures, theory) before higher-level features (composition, export).

---

## Pending Decisions

*This section will be updated as the project progresses.*

---

## Rejected Decisions

*None yet.*
