# V3-11: Documentation and Examples

**Status:** Pending
**Priority:** Medium
**Dependencies:** All previous V3 steps

## Overview

Create comprehensive documentation including user guides, API reference, examples, and tutorials for the V3 music generation system.

---

## Documentation Structure

```
docs/
├── README.md                    # Main documentation index
├── installation.md              # Installation guide
├── quickstart.md                # Quick start guide
├── user_guide/
│   ├── prompts.md               # Prompt writing guide
│   ├── orchestration.md         # Orchestration options
│   ├── styles.md                # Style period reference
│   └── ensembles.md             # Ensemble presets
├── api_reference/
│   ├── composer.md              # AIComposerV3 API
│   ├── models.md                # Data models
│   ├── midi.md                  # MIDI generation
│   └── validation.md            # Validation API
├── examples/
│   ├── classical.md             # Classical music examples
│   ├── film_score.md            # Film score examples
│   ├── contemporary.md          # Contemporary examples
│   └── advanced.md              # Advanced techniques
└── troubleshooting.md           # Common issues and solutions
```

---

## Quick Start Guide

```markdown
# Quick Start

## Installation

### 1. Install the package

\`\`\`bash
pip install music-gen-lib
\`\`\`

### 2. Install system dependencies

**Linux:**
\`\`\`bash
sudo apt install sfizz ffmpeg
\`\`\`

**macOS:**
\`\`\`bash
brew install sfizz ffmpeg
\`\`\`

### 3. Download SFZ libraries

\`\`\`bash
# Create libraries directory
mkdir -p ~/sfz_libraries

# Download Sonatina Symphonic Orchestra
cd ~/sfz_libraries
git clone https://github.com/peastman/sso.git
\`\`\`

## Basic Usage

### Python API

\`\`\`python
from musicgen.v3 import AIComposerV3

# Initialize composer
composer = AIComposerV3(
    sfz_libraries_root=Path("~/sfz_libraries")
)

# Generate a composition
composition, audio_path = composer.compose_and_render(
    prompt="A melancholic string quartet piece in D minor",
    output_path="output/melancholic_quartet.wav",
    style="romantic",
    form="ternary",
    ensemble="string_quartet",
)

print(f"Generated: {composition.title}")
print(f"Duration: {composition.duration:.1f} seconds")
\`\`\`

### Command Line

\`\`\`bash
# Generate a piece
musicgen-v3 compose "An epic orchestral fanfare in C major" \\
    --style film_score \\
    --ensemble full_orchestra \\
    --output epic_fanfare.wav

# Generate with specific form
musicgen-v3 compose "A piano sonata movement" \\
    --style classical \\
    --form sonata \\
    --key C minor \\
    --duration 180
\`\`\`
```

---

## Prompt Writing Guide

```markdown
# Writing Effective Prompts

## Prompt Components

A good prompt includes several components:

### 1. Mood or Emotion

Describe the emotional character:

\`\`\`
"A peaceful, serene melody..."
"A dark, ominous texture..."
"A joyful, triumphant fanfare..."
"A melancholic, longing theme..."
\`\`\`

### 2. Instrumentation

Specify which instruments or ensemble:

\`\`\`
"...for string quartet"
"...for full orchestra with prominent brass"
"...for solo piano"
"...for woodwind quintet"
\`\`\`

### 3. Style Period

Reference a historical style:

\`\`\`
"...in the style of Classical period"
"...reminiscent of Romantic era..."
"...with contemporary techniques..."
"...like a film score by Hans Zimmer..."
\`\`\`

### 4. Musical Elements

Add specific musical details:

\`\`\`
"...with a slow build from piano to fortissimo"
"...using a descending chromatic bass line"
"...with contrapuntal interplay between violin and cello"
"...in ternary form (ABA)"
\`\`\`

## Example Prompts

### Classical

\`\`\`
"A Classical-era minuet and trio for string quartet in G major,
with balanced phrases, Alberti bass in cello, and elegant
trills in the first violin."
\`\`\`

### Romantic

\`\`\`
"A Romantic piano piece in C# minor with expressive rubato,
chromatic harmony building to passionate climax, then
subsiding to quiet reflection."
\`\`\`

### Film Score

\`\`\`
"An epic orchestral cue building from solo viola to full
tutti, using ostinati in strings and brass, culminating
in powerful chord at ff."
\`\`\`

### Ambient

\`\`\`
"A serene ambient texture for string orchestra, slow
harmonic changes, minimal melody, sustained high
register in violins creating ethereal atmosphere."
\`\`\`
```

---

## API Reference

```markdown
# AIComposerV3 API Reference

## Class: AIComposerV3

### Constructor

\`\`\`python
AIComposerV3(
    system_prompt_path: Path | None = None,
    instrument_definitions_path: Path | None = None,
    sfz_libraries_root: Path | None = None,
    gemini_api_key: str | None = None,
)
\`\`\`

**Parameters:**
- `system_prompt_path`: Path to custom music theory system prompt
- `instrument_definitions_path`: Path to instrument definitions YAML
- `sfz_libraries_root`: Root directory containing SFZ libraries
- `gemini_api_key`: Google Gemini API key (or set GEMINI_API_KEY env var)

### Methods

#### compose()

\`\`\`python
def compose(
    prompt: str,
    duration_seconds: float | None = None,
    key: str | None = None,
    style: StylePeriod | None = None,
    form: MusicalForm | None = None,
    ensemble: str | None = None,
    instruments: list[str] | None = None,
    output_format: Literal["midi", "wav", "mp3", "all"] = "midi",
    validate: bool = True,
    max_retries: int | None = None,
) -> CompositionResponse
\`\`\`

Generate a musical composition from a natural language prompt.

**Parameters:**
- `prompt`: Natural language description
- `duration_seconds`: Target duration (10-600 seconds)
- `key`: Key signature (e.g., "C minor", "F# major")
- `style`: Stylistic period ("baroque", "classical", "romantic", "modern", "film_score")
- `form`: Musical form ("binary", "ternary", "rondo", "sonata", "through_composed")
- `ensemble`: Ensemble preset name
- `instruments`: List of specific instruments
- `output_format`: Output format(s)
- `validate`: Run validation before returning
- `max_retries`: Maximum retry attempts for validation failures

**Returns:** `CompositionResponse` with composition and metadata

**Example:**
\`\`\`python
response = composer.compose(
    prompt="A gentle string quartet",
    duration_seconds=120,
    key="F major",
    style="classical",
    ensemble="string_quartet",
)

print(response.composition.title)
print(response.composition.duration)
\`\`\`

#### render()

\`\`\`python
def render(
    composition: Composition,
    output_path: Path,
    format: str = "wav",
    stems: bool = False,
) -> Path
\`\`\`

Render a composition to audio.

**Parameters:**
- `composition`: The composition to render
- `output_path`: Output file path
- `format`: Output format ("wav" or "mp3")
- `stems`: Export individual instrument stems

**Returns:** Path to rendered audio file

#### compose_and_render()

\`\`\`python
def compose_and_render(
    prompt: str,
    output_path: Path,
    **kwargs,
) -> tuple[Composition, Path]
\`\`\`

Convenience method: compose and render in one call.

\`\`\`python
composition, audio_path = composer.compose_and_render(
    prompt="An epic orchestral piece",
    output_path="output/epic.wav",
    style="film_score",
    ensemble="full_orchestra",
)
\`\`\`
```

---

## Examples

### Classical String Quartet

```python
from musicgen.v3 import AIComposerV3

composer = AIComposerV3()

# Generate a Classical string quartet movement
response = composer.compose(
    prompt=(
        "A Classical-era string quartet movement in G major. "
        "First violin carries the melody with elegant phrasing. "
        "Second violin provides accompaniment. Viola adds harmonic "
        "fill. Cello provides Alberti bass foundation. "
        "Use sonata form with clear exposition, development, "
        "and recapitulation."
    ),
    duration_seconds=240,
    key="G major",
    style="classical",
    form="sonata",
    ensemble="string_quartet",
)

# Render
audio_path = composer.render(response.composition, "output/quartet.wav")
print(f"Generated: {audio_path}")
```

### Film Score Cue

```python
# Generate an epic film score cue
response = composer.compose(
    prompt=(
        "An epic orchestral building cue. Starts with solo "
        "cello playing melancholic theme. Strings gradually "
        "enter in layers. Horns add pedal point. Timpani "
        "builds with rolling. Full tutti arrives at climax "
        "with powerful brass melody. Ends with dying "
        "orchestral decay."
    ),
    duration_seconds=90,
    key="D minor",
    style="film_score",
    ensemble="full_orchestra",
)

audio_path = composer.render(response.composition, "output/film_cue.wav")
```

### Piano Solo

```python
# Generate a piano piece
response = composer.compose(
    prompt=(
        "A Romantic piano nocturne. Rubato tempo with "
        "expressive melodies. Left hand provides arpeggiated "
        "accompaniment. Building to passionate climax with "
        "wide chords and chromaticism. Returns to opening "
        "material in quieter dynamic."
    ),
    duration_seconds=180,
    key="C# minor",
    style="romantic",
    instruments=["piano"],
)

audio_path = composer.render(response.composition, "output/nocturne.wav")
```

---

## Implementation Tasks

1. [ ] Create main README
2. [ ] Write installation guide
3. [ ] Write quick start guide
4. [ ] Write prompt writing guide
5. [ ] Create API reference
6. [ ] Write example scripts
7. [ ] Create troubleshooting guide
8. [ ] Add JSDoc-style docstrings to all code

## Success Criteria

- All public APIs documented
- Examples demonstrate major use cases
- Installation instructions are clear
- Troubleshooting covers common issues

## Next Steps

- V3-12: Performance Optimization
- V3-13: Release Preparation
