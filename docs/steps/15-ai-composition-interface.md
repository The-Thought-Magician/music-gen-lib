# Step 15: AI-Powered Composition Interface

## Objective

Create an intelligent interface that uses Google Gemini 2.5 Flash Lite to interpret natural language prompts and generate detailed orchestral composition parameters.

## Overview

The mood presets are limited. This step creates an AI agent that:
1. Interprets user prompts in natural language
2. Extracts musical parameters (key, tempo, instruments, form, mood, etc.)
3. Generates complete multi-section orchestration plans
4. Returns structured data for creating 3-minute compositions with proper timing

## Dependencies

- **google-genai** >= 1.0.0 - Google Gemini SDK
- **pydantic** >= 2.0 - Data validation and parsing

## Tasks

### 15.1 AI Prompt Engineering

- [ ] Design prompt template for parameter extraction
- [ ] Create system prompt for music theory context
- [ ] Design output schema (JSON structure)
- [ ] Create few-shot examples for different musical styles
- [ ] Add constraints for valid musical parameters

### 15.2 Data Models

- [ ] Create `src/musicgen/ai/models.py` with Pydantic models:
  - `OrchestrationPlan` - Complete composition structure
  - `Section` - Musical section (A, B, C, etc.)
  - `InstrumentAssignment` - Which instruments play what
  - `DynamicsPlan` - Dynamic changes over time
  - `TextureChanges` - Orchestration density changes

### 15.3 Gemini Client Module

- [ ] Create `src/musicgen/ai/client.py`
- [ ] Implement `GeminiComposer` class:
  - API key management
  - Retry logic with exponential backoff
  - Rate limiting
  - Error handling
  - Response validation
- [ ] Add streaming support for long responses
- [ ] Implement caching for repeated prompts

### 15.4 Parameter Extraction

- [ ] Implement `extract_parameters(prompt: str) -> OrchestrationPlan`
- [ ] Parse structured JSON from Gemini
- [ ] Validate parameters against music theory rules
- [ ] Fill in missing values with sensible defaults
- [ ] Handle ambiguous prompts (ask for clarification or use defaults)

### 15.5 Composition Builder

- [ ] Implement `build_composition(plan: OrchestrationPlan) -> Score`
- [ ] Map sections to musical forms (binary, ternary, rondo, etc.)
- [ ] Generate separate parts for each instrument
- [ ] Handle timing and transitions between sections
- [ ] Apply dynamic markings
- [ ] Coordinate melody, harmony, and accompaniment

### 15.6 Prompt File Interface

- [ ] Create `userprompt.txt` interface
- [ ] Watch for file changes or manual trigger
- [ ] Read prompt from file
- [ ] Write output to `output/` directory
- [ ] Log generation details

### 15.7 Testing

- [ ] Create `tests/test_ai_composer.py`
- [ ] Test parameter extraction from various prompts
- [ ] Test JSON parsing and validation
- [ ] Test composition building
- [ ] Create test prompts for different genres
- [ ] Mock Gemini API responses for unit tests

### 15.8 Examples

- [ ] Create `examples/ai_composition_example.py`
- [ ] Create sample `userprompt.txt` files
- [ ] Document prompt best practices
- [ ] Show example prompts and their outputs

## Deliverables

- `src/musicgen/ai/__init__.py`
- `src/musicgen/ai/models.py` - Pydantic data models
- `src/musicgen/ai/client.py` - Gemini client
- `src/musicgen/ai/composer.py` - Main composition logic
- `tests/test_ai_composer.py`
- `examples/ai_composition_example.py`
- `userprompt.txt` - Template file
- Documentation

## Data Schema

```python
class OrchestrationPlan(BaseModel):
    """Complete orchestration plan from AI."""
    title: str
    duration_seconds: int = 180  # 3 minutes
    key: str
    scale_type: str
    tempo: int

    sections: List[Section]
    instruments: List[InstrumentAssignment]
    form_type: str  # "binary", "ternary", "rondo", "sonata", "through_composed"

    mood_description: str
    dynamics_plan: DynamicsPlan
    texture_changes: List[TextureChange]

class Section(BaseModel):
    """A musical section."""
    name: str  # "A", "B", "C", "development", etc.
    duration_seconds: int
    key: Optional[str]  # For modulations
    tempo_change: Optional[int]
    mood: str
    instrumentation: List[str]  # Which instruments play
    melody_role: str  # "new", "variation", "development"
    harmonic_role: str  # "tonic", "dominant", "modulation"

class InstrumentAssignment(BaseModel):
    """Instrument part configuration."""
    name: str
    section: str  # "strings", "woodwinds", "brass", "percussion"
    role: str  # "melody", "harmony", "bass", "accompaniment"
    dynamics: str
    when_playing: List[str]  # Which sections
```

## Prompt Template

```
You are an expert orchestral composer and music theory specialist.
Given a user's description, generate a complete orchestration plan
for a 3-minute composition.

User prompt: {user_prompt}

Generate a JSON object with:
- title: A fitting title
- key: Musical key (e.g., "C", "Am", "F#m")
- scale_type: Scale (major, minor, harmonic_minor, etc.)
- tempo: BPM (60-140)
- sections: Array of sections with timing
- instruments: List of orchestral instruments
- form_type: Musical form
- mood_description: Brief description
- dynamics_plan: Dynamic arc
- texture_changes: When to add/remove instruments

Rules:
1. Duration should total ~180 seconds
2. Use standard orchestral instruments
3. Sections should flow logically
4. Include at least 4 instruments
5. Dynamics should create interest (crescendo, diminuendo)
```

## Validation

```python
# Test AI composition
from musicgen.ai import GeminiComposer

composer = GeminiComposer(api_key="...")

# Simple prompt
plan = composer.extract_parameters(
    "A heroic battle scene with drums and trumpets"
)
assert plan.tempo > 100
assert "trumpet" in [i.name for i in plan.instruments]
assert "drums" in [i.name for i in plan.instruments] or "timpani" in [i.name for i in plan.instruments]

# Build composition
score = composer.build_composition(plan)
assert len(score.parts) >= 4

# Export
request = CompositionRequest(
    orchestration_plan=plan,
    export_formats=["midi", "wav", "mp3"]
)
result = generate(request)
```

## API Key Setup

```bash
# Set environment variable
export GOOGLE_API_KEY="your-api-key"

# Or create .env file
echo "GOOGLE_API_KEY=your-api-key" > .env
```

## Example Prompts

1. "A peaceful forest scene with birds chirping, flutes, and strings"
2. "Epic cinematic trailer music with full orchestra"
3. "Sad nostalgic piano and cello melody"
4. "Upbeat jazz-inspired piece with saxophone and drums"
5. "Tense horror movie underscore with dissonant harmonies"
