# Step 13: Add Global Timeline/Synchronization

## Status: PENDING

## Priority: MEDIUM

## Problem

Each part currently has independent timing. This causes **synchronization issues**:

1. **Floating point errors**: Accumulate over long pieces, parts drift apart
2. **Complex coordination**: Hard to ensure all parts align at measure 16
3. **No measure awareness**: Can't easily represent "all parts hit beat 1 together"

### Example Problem

```python
# Flute part
[{"note": "C4", "duration": 0.5}, {"note": "rest", "duration": 0.5}, ...]  # Many events

# Violin part
[{"note": "E4", "duration": 0.5}, {"note": "rest", "duration": 0.5}, ...]  # Many events

# After 100 events, a small timing error means they're no longer aligned!
```

## Solution Options

### Option A: Measure-Based Structure ✅ RECOMMENDED

```python
class AIMeasure(BaseModel):
    number: int
    beats: int  # Usually 4, but could be 3 for waltz time
    parts: dict[str, list[AINote]]  # Part name -> notes in this measure

class AIComposition(BaseModel):
    # ... existing fields ...
    structure_type: Literal["part_based", "measure_based"] = "part_based"
    measures: list[AIMeasure] = []  # NEW: Optional measure-based view
```

**Example:**
```json
{
  "measures": [
    {
      "number": 1,
      "beats": 4,
      "parts": {
        "violin": [
          {"note_name": "E4", "start_time": 0, "duration": 4}
        ],
        "cello": [
          {"note_name": "A3", "start_time": 0, "duration": 4}
        ]
      }
    }
  ]
}
```

**Pros:**
- Clear measure boundaries
- Easy to align parts
- Natural for musical thinking

**Cons:**
- More complex structure
- Harder for AI to generate

### Option B: Global Timeline Events

```python
class TimelineEvent(BaseModel):
    time: float  # Absolute time in quarter notes
    part_name: str
    note_data: AINote

class AIComposition(BaseModel):
    timeline: list[TimelineEvent]  # All events sorted by time
```

**Pros:**
- Time-sorted events
- Easy to render sequentially

**Cons:**
- Loses part grouping
- Harder to read/edit

### Option C: Keep Part-Based + Sync Markers

```python
class SyncPoint(BaseModel):
    measure: int
    time: float  # Expected time in quarter notes
    description: str | None = None

class AIComposition(BaseModel):
    parts: list[AIPart]
    sync_points: list[SyncPoint] = []  # NEW: Alignment markers
```

**Pros:**
- Minimal change to existing structure
- Backward compatible

**Cons:**
- Doesn't fully solve the problem
- Still requires calculation

## Implementation Plan (Hybrid Approach)

Support **both** part-based (current) and measure-based (new) structures:

### Phase 1: Add Measure-Based Composition Type

```python
# src/musicgen/ai_models/composition.py

class StructureType(str, Enum):
    PART_BASED = "part_based"  # Current: each part has its own note list
    MEASURE_BASED = "measure_based"  # NEW: measures contain all parts

class AIMeasure(BaseModel):
    """A single measure with all parts' events."""

    number: int = Field(..., ge=1)
    time_signature: TimeSignature | None = None
    parts: dict[str, list[AINote]] = Field(default_factory=dict)

class AIComposition(BaseModel):
    """Supports both part-based and measure-based structures."""

    structure_type: StructureType = StructureType.PART_BASED

    # For part-based (current)
    parts: list[AIPart] = []

    # For measure-based (new)
    measures: list[AIMeasure] = []

    def get_parts(self) -> list[AIPart]:
        """Get parts, converting from measures if needed."""
        if self.structure_type == StructureType.MEASURE_BASED:
            return self._measures_to_parts()
        return self.parts

    def _measures_to_parts(self) -> list[AIPart]:
        """Convert measure-based to part-based structure."""
        # Collect all notes by part name
        part_notes: dict[str, list] = {}
        time_offset = 0

        for measure in self.measures:
            for part_name, notes in measure.parts.items():
                if part_name not in part_notes:
                    part_notes[part_name] = []
                # Add measure offset to note start times
                for note in notes:
                    note_with_offset = note.model_copy()
                    note_with_offset.start_time += time_offset
                    part_notes[part_name].append(note_with_offset)

            time_offset += 4  # Assuming 4/4 for now

        # Create AIPart objects
        return [AIPart(name=name, notes=notes) for name, notes in part_notes.items()]
```

### Phase 2: Update Schema Generator

```python
# src/musicgen/schema/generator.py

def _composition_schema(self) -> dict[str, Any]:
    return {
        "structure_type": "Either 'part_based' or 'measure_based'",
        "title": "string",
        "tempo": "int (40-200 BPM)",
        "key": '{"tonic": "string", "mode": "string"}',
        # Part-based
        "parts": "array of Part objects (for part_based structure)",
        # Measure-based
        "measures": "array of Measure objects (for measure_based structure)",
    }
```

### Phase 3: Update Renderer

```python
# src/musicgen/renderer/midi.py

def render(self, composition: AIComposition, path: Path) -> None:
    """Render composition to MIDI."""
    # Always convert to part-based for rendering
    parts = composition.get_parts()

    for part in parts:
        track = self._render_part(part, composition)
        midi_file.tracks.append(track)
```

## Migration Strategy

1. **Start**: Part-based remains default, works as before
2. **Add**: Measure-based as alternative for new generations
3. **Experiment**: Test which AI handles better
4. **Decide**: Keep both or choose one based on results

## AI Prompt Considerations

Measure-based is harder for AI because:

```
# Part-based (easier)
{"name": "melody", "notes": [200 notes]}
{"name": "bass", "notes": [150 notes]}

# Measure-based (harder)
{"measure": 1, "parts": {"melody": [...], "bass": [...]}}
{"measure": 2, "parts": {"melody": [...], "bass": [...]}}
...
{"measure": 32, "parts": {"melody": [...], "bass": [...]}}
```

**Recommendation**: Start with part-based + `start_time` (Step 12), then experiment with measure-based for complex orchestral pieces.

## Files to Modify

1. `src/musicgen/ai_models/composition.py` - Add measure-based models
2. `src/musicgen/ai_models/parts.py` - Add conversion logic
3. `src/musicgen/schema/generator.py` - Update schema
4. `src/musicgen/renderer/midi.py` - Handle both structure types
5. `src/musicgen/ai_client/prompts.py` - Document both approaches
