# V4-01: Project Setup and Planning

## Overview

Initial setup for V4 implementation, creating the foundation for universal music generation.

## Objectives

1. Create todo list tracking for all 50 V4 steps
2. Review V3 completion status and existing architecture
3. Create new V4 package structure
4. Set up development dependencies
5. Create initial documentation structure

## Tasks

### 1. Todo List Creation

Create tracking for all V4-01 through V4-50 steps with statuses:
- pending
- in_progress
- completed

### 2. Architecture Review

Review completed V3 components:
- `src/musicgen/ai_models/` - Pydantic models
- `src/musicgen/composer_new/` - AI composer
- `src/musicgen/validation/` - Validation tools
- `src/musicgen/sfz/` - SFZ rendering
- `resources/instrument_definitions.yaml` - Orchestral instruments

Identify extension points for V4 features.

### 3. Directory Structure

Create new directories:
```
src/musicgen/
├── patterns/           # Pattern manipulation system
│   ├── __init__.py
│   ├── parser.py       # Mini-notation parser
│   ├── transform.py    # Transformation functions
│   ├── combine.py      # Pattern combinators
│   └── state.py        # Pattern state management
├── instruments/        # Extended instrument definitions
│   ├── __init__.py
│   ├── guitars.py      # Guitar-specific logic
│   ├── drums.py        # Drum kit logic
│   ├── world.py        # World instrument logic
│   └── electronic.py   # Synth/electronic logic
├── genres/             # Genre-specific styles
│   ├── __init__.py
│   ├── profiles.py     # Genre definitions
│   ├── patterns.py     # Genre patterns
│   └── transfer.py     # Style transfer
└── scales/             # World music scales
    ├── __init__.py
    ├── indian.py       # Indian ragas
    ├── arabic.py       # Arabic maqamat
    ├── japanese.py     # Japanese scales
    └── pentatonic.py   # Pentatonic modes
```

### 4. Resource Files

Create placeholder resource files:
```
resources/
├── instrument_definitions_world.yaml
├── genre_profiles.yaml
├── scale_definitions.yaml
└── pattern_library.yaml
```

### 5. Dependencies

Add to `pyproject.toml`:
```toml
[project.optional-dependencies]
v4 = [
    "websockets>=12.0",  # For live coding
    "scipy>=1.11.0",     # For pattern calculations
]
```

## Files to Create

- `src/musicgen/patterns/__init__.py`
- `src/musicgen/instruments/__init__.py`
- `src/musicgen/genres/__init__.py`
- `src/musicgen/scales/__init__.py`
- `resources/instrument_definitions_world.yaml` (placeholder)
- `resources/genre_profiles.yaml` (placeholder)
- `resources/scale_definitions.yaml` (placeholder)

## Success Criteria

- [ ] All new directories created
- [ ] All `__init__.py` files with proper exports
- [ ] Placeholder YAML files with basic structure
- [ ] Dependencies added to pyproject.toml
- [ ] No import errors when importing new modules

## Next Steps

After completion, proceed to V4-02: Extended Instrument Schema
