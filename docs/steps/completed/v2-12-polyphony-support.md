# Step 12: Add Polyphony Support

## Status: PENDING

## Priority: HIGH

## Problem

The current `AINote` model represents notes as a sequential array. This prevents representing **chords** (multiple notes sounding simultaneously).

### Example Problem
A C Major chord (C-E-G played together) must currently be represented as:
```json
{"notes": [
  {"note_name": "C4", "duration": 2.0},
  {"note_name": "E4", "duration": 2.0},  // Plays AFTER C, not WITH it
  {"note_name": "G4", "duration": 2.0}   // Plays AFTER E, not WITH it
]}
```

This creates an arpeggio, not a chord.

## Solution Options

### Option A: Add `start_time` (Absolute Timing) ✅ RECOMMENDED

```python
class AINote(BaseModel):
    note_name: str
    duration: float
    start_time: float  # NEW: Absolute position in quarter notes
    velocity: int
```

Example chord:
```json
{"notes": [
  {"note_name": "C4", "start_time": 0, "duration": 2.0},
  {"note_name": "E4", "start_time": 0, "duration": 2.0},  // Same time = chord!
  {"note_name": "G4", "start_time": 0, "duration": 2.0}
]}
```

**Pros:**
- Most flexible for complex timing
- Aligns with DAW/piano roll representation
- Easy to render to MIDI

**Cons:**
- Requires more careful timing calculations
- AI must understand absolute timing

### Option B: Add `time_delta` (MIDI-style)

```python
class AINote(BaseModel):
    note_name: str
    duration: float
    time_delta: float  # Time since previous event
    velocity: int
```

**Pros:**
- Compact representation
- Matches MIDI file format

**Cons:**
- Harder for AI to reason about
- Cascading errors if one delta is wrong

### Option C: Note Groups/Chords

```python
class AINoteGroup(BaseModel):
    start_time: float
    duration: float
    notes: list[NoteWithPitch]  # Multiple pitches at same time
```

**Pros:**
- Explicit chord representation
- Easy for AI to understand

**Cons:**
- More complex schema
- Can't represent independent voice motion within chords

## Implementation Plan (Option A)

### 1. Update `src/musicgen/ai_models/notes.py`

```python
class AINote(BaseModel):
    """A single note with absolute timing."""

    # Pitch (one required)
    note_name: str | None = Field(None, pattern=r"^[A-G][#b]?[0-8]$")
    midi_number: int | None = Field(None, ge=0, le=127)
    frequency: float | None = Field(None, gt=0)

    # Timing
    start_time: float = Field(  # NEW
        default=0.0,
        ge=0,
        description="Absolute start time in quarter notes from part start"
    )
    duration: float = Field(..., gt=0, description="Duration in quarter notes")

    # Velocity
    velocity: int = Field(default=80, ge=0, le=127)

    # Modifications
    tied: bool = Field(default=False)
    articulation: ArticulationType | None = Field(None)
```

### 2. Update `src/musicgen/ai_models/parts.py`

No changes needed, but add validation:

```python
@field_validator("notes")
@classmethod
def validate_note_timing(cls, v: list) -> list:
    """Ensure notes are sorted by start_time."""
    return sorted(v, key=lambda n: n.start_time if hasattr(n, "start_time") else 0)
```

### 3. Update `src/musicgen/renderer/midi.py`

```python
def _render_part(self, part: AIPart, composition: AIComposition) -> mido.MidiTrack:
    track = mido.MidiTrack()
    # ... header events ...

    # Convert to events with absolute times
    events = []
    for note in part.notes:
        start = note.start_time * 480  # Convert to ticks
        duration = note.duration * 480
        events.append(('note_on', start, note.note, note.velocity))
        events.append(('note_off', start + duration, note.note, 0))

    # Sort and render
    events.sort(key=lambda x: x[1])  # Sort by time
    current_time = 0
    for event_type, time, note, value in events:
        delta = int(time - current_time)
        track.append(mido.MetaMessage('delta_time', time=delta))
        track.append(mido.Message(event_type, note=note, velocity=value))
        current_time = time

    return track
```

### 4. Update `src/musicgen/schema/generator.py`

```python
def _note_schema(self) -> dict[str, Any]:
    return {
        "pitch": self._pitch_description(),
        "start_time": "float (absolute position in quarter notes, e.g., 0, 0.5, 1.0)",  # NEW
        "duration": f"float (in {self.config.duration_unit.value}s)",
        "velocity": f"int ({self.config.velocity_min}-{self.config.velocity_max})",
    }
```

### 5. Update Prompts

Add explanation to `src/musicgen/ai_client/prompts.py`:

```
POLYPHONY (Chords):
To play multiple notes simultaneously, set the same start_time:
- C4 chord: {"note_name": "C4", "start_time": 0, "duration": 2}
- E4 chord: {"note_name": "E4", "start_time": 0, "duration": 2}  # Same time!
- G4 chord: {"note_name": "G4", "start_time": 0, "duration": 2}  # Same time!
```

## Migration Strategy

- Add `start_time` as **optional** with default 0
- Existing sequential notes still work (start_time defaults to previous note end)
- Gradually update AI prompts to use explicit timing
- Eventually deprecate sequential-only mode

## Files to Modify

1. `src/musicgen/ai_models/notes.py` - Add `start_time` field
2. `src/musicgen/ai_models/parts.py` - Add timing validation
3. `src/musicgen/renderer/midi.py` - Update rendering logic
4. `src/musicgen/schema/generator.py` - Update schema
5. `src/musicgen/ai_client/prompts.py` - Document polyphony

## Testing

```python
# Test chord generation
composer = AIComposer()
comp = composer.generate("A C Major chord held for 4 beats")

# Verify notes start at same time
melody = comp.get_melody_parts()[0]
starts = [n.start_time for n in melody.notes]
# Should have multiple notes with start_time == 0
```
