# Step 16: Chunking Strategy for Long Compositions

## Status: PENDING

## Priority: LOW

## Problem

A 2-3 minute orchestral piece has 2000+ notes. LLMs struggle with this:

1. **Token limits**: Output gets cut off mid-JSON
2. **Syntax errors**: Higher probability in large JSON
3. **Coherence loss**: AI forgets earlier musical material
4. **Inconsistency**: Later sections don't relate to earlier themes

### Current Failure Mode

```
User: "Generate a 3-minute orchestral piece"

AI: (generates 500 notes, then cuts off)
{"title": "Epic Symphony", "parts": [{"name": "violin", "notes": [
  {"note_name": "E4", "duration": 1.0},
  ...

[ERROR: Incomplete JSON. Token limit reached.]
```

## Solution: Section-by-Section Generation

Generate compositions in smaller chunks, then stitch together:

```python
class SectionalComposer:
    """Generate compositions section by section."""

    def generate_section(
        self,
        prompt: str,
        section_name: str,
        previous_sections: list[AISection],
        length_bars: int = 16
    ) -> AISection:
        """Generate one section at a time."""
```

## Implementation

### 1. Define Section Model

```python
# src/musicgen/ai_models/sections.py

from pydantic import BaseModel, Field

class AISection(BaseModel):
    """A section of a composition (e.g., "A", "B", "bridge")."""

    name: str = Field(..., description="Section name (A, B, bridge, etc.)")
    start_bar: int = Field(..., ge=1)
    end_bar: int = Field(..., ge=1)
    key: KeySignature | None = None
    tempo: int | None = None
    mood: str | None = None

    # Parts for this section only
    parts: dict[str, list[AINote]] = Field(
        default_factory=dict,
        description="Part name -> notes in this section"
    )

    # Transition to next section
    transition: str | None = Field(
        None,
        description="How this section leads to the next"
    )
```

### 2. Sectional Composer

```python
# src/musicgen/composer_new/sectional.py

class SectionalComposer(AIComposer):
    """Generate compositions section by section."""

    def generate_composition(
        self,
        prompt: str,
        structure: list[dict],  # [{"name": "A", "bars": 16}, ...]
        context: dict | None = None
    ) -> AIComposition:
        """Generate a full composition section by section.

        Args:
            prompt: Overall composition description
            structure: Section definitions
            context: Musical context (key, tempo, etc.)

        Returns:
            Complete AIComposition
        """
        sections = []
        context = context or {}
        current_bar = 1

        for section_def in structure:
            # Generate this section
            section = self._generate_section(
                prompt=prompt,
                section_name=section_def["name"],
                start_bar=current_bar,
                length_bars=section_def.get("bars", 16),
                context=context,
                previous_sections=sections
            )

            sections.append(section)
            current_bar = section.end_bar + 1

            # Update context with this section's material
            context = self._update_context(context, section)

        # Stitch sections together
        return self._stitch_sections(sections, context)

    def _generate_section(
        self,
        prompt: str,
        section_name: str,
        start_bar: int,
        length_bars: int,
        context: dict,
        previous_sections: list[AISection]
    ) -> AISection:
        """Generate a single section."""

        # Build section prompt with context
        section_prompt = self._build_section_prompt(
            prompt=prompt,
            section_name=section_name,
            start_bar=start_bar,
            length_bars=length_bars,
            context=context,
            previous_sections=previous_sections
        )

        # Generate just this section's notes
        schema = self._build_section_schema(length_bars)
        raw = self.client.generate(prompt=section_prompt, schema=schema)

        # Parse as section
        return AISection(**raw)

    def _build_section_prompt(
        self,
        prompt: str,
        section_name: str,
        start_bar: int,
        length_bars: int,
        context: dict,
        previous_sections: list[AISection]
    ) -> str:
        """Build prompt for section generation."""

        # Get themes from previous sections
        themes = self._extract_themes(previous_sections)

        return f"""Generate section "{section_name}" (bars {start_bar}-{start_bar + length_bars - 1}) for:

{prompt}

CONTEXT:
- Key: {context.get('key', {'tonic': 'C', 'mode': 'major'})}
- Tempo: {context.get('tempo', 120)} BPM
- Previous themes: {themes}

REQUIREMENTS:
- Generate exactly {length_bars} bars ({length_bars * 4} quarter notes at 4/4)
- If this is a repeat of a previous section, vary the material (don't copy exactly)
- Include a transition if not the final section
- Return ONLY JSON for this section's notes
"""

    def _stitch_sections(
        self,
        sections: list[AISection],
        context: dict
    ) -> AIComposition:
        """Combine sections into full composition."""

        # Collect all parts across sections
        all_parts: dict[str, list[AINote]] = {}

        for section in sections:
            bar_offset = (section.start_bar - 1) * 4  # Quarter notes

            for part_name, notes in section.parts.items():
                if part_name not in all_parts:
                    all_parts[part_name] = []

                # Adjust note times
                for note in notes:
                    adjusted = note.model_copy()
                    adjusted.start_time += bar_offset
                    all_parts[part_name].append(adjusted)

        # Create AIPart objects
        parts = [
            AIPart(name=name, notes=notes)
            for name, notes in all_parts.items()
        ]

        return AIComposition(
            title=context.get('title', 'Generated Composition'),
            tempo=context.get('tempo', 120),
            time_signature=context.get('time_signature', {'numerator': 4, 'denominator': 4}),
            key=context.get('key', {'tonic': 'C', 'mode': 'major'}),
            parts=parts
        )
```

### 3. Usage Example

```python
from musicgen.composer_new.sectional import SectionalComposer

composer = SectionalComposer()

# Define structure
structure = [
    {"name": "A", "bars": 16},
    {"name": "A", "bars": 16},  # Repeat with variation
    {"name": "B", "bars": 16},  # Bridge
    {"name": "A", "bars": 16},  # Return
]

# Generate
composition = composer.generate_composition(
    prompt="A nostalgic piano piece in A minor, 70 BPM",
    structure=structure,
    context={
        "key": {"tonic": "A", "mode": "minor"},
        "tempo": 70
    }
)
```

## Alternative: Parallel Part Generation

Another approach is to generate parts in parallel (one AI call per part):

```python
def generate_parallel_parts(
    self,
    prompt: str,
    parts: list[str],  # ["melody", "bass", "harmony"]
    context: dict
) -> AIComposition:
    """Generate each part separately, then combine."""

    generated_parts = []

    for part_name in parts:
        part_prompt = f"""Generate the {part_name} part for:
        {prompt}

        Context: {context}
        Length: 64 bars (256 quarter notes)
        """

        raw = self.client.generate(prompt=part_prompt)
        generated_parts.append(AIPart(**raw))

    return AIComposition(
        parts=generated_parts,
        **context
    )
```

**Pros:** Each part gets full attention
**Cons:** Parts may not fit together musically

## Comparison: Sequential vs Parallel vs Chunked

| Approach | Token Usage | Coherence | Complexity |
|----------|-------------|-----------|------------|
| Single-shot (current) | High (one large) | Medium | Low |
| Section-by-section | Low (many small) | High (with context) | Medium |
| Parallel parts | Medium (medium per part) | Low (parts unrelated) | Medium |

## Recommendation

Start with **section-by-section generation** for:
- Orchestral pieces (many parts, long duration)
- Multi-movement works
- Pieces with clear sections (sonata form, etc.)

Keep **single-shot** for:
- Solo pieces
- Short pieces (< 1 minute)
- Simple forms

## Files to Create

1. `src/musicgen/ai_models/sections.py` - `AISection` model
2. `src/musicgen/composer_new/sectional.py` - `SectionalComposer`

## Files to Modify

1. `src/musicgen/ai_client/prompts.py` - Add section-specific prompts
2. `src/musicgen/schema/generator.py` - Add section schema
