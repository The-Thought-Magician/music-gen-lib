# Step 15: Add Tempo and Meter Fluidity

## Status: PENDING

## Priority: MEDIUM

## Problem

Real music "breathes" - it changes tempo and time signature. Current schema has static values:

```python
class AIComposition(BaseModel):
    tempo: int  # Fixed forever?
    time_signature: TimeSignature  # Can't change?
```

This prevents representing:
- **Ritardando** - Gradual slowing at end
- **Accelerando** - Gradual speeding up
- **Time signature changes** - 4/4 → 3/4 → 4/4
- **Rubato** - Expressive timing
- ** fermata** - Hold a note longer

## Solution: Event-Based Tempo and Meter Maps

```python
class TempoEvent(BaseModel):
    """A tempo change event."""

    time: float = Field(
        ...,
        ge=0,
        description="When this tempo takes effect (quarter notes)"
    )
    bpm: int = Field(
        ...,
        ge=20,
        le=300,
        description="New tempo in BPM"
    )
    duration: float | None = Field(
        None,
        description="If specified, return to previous tempo after this duration"
    )

class TimeSignatureEvent(BaseModel):
    """A time signature change event."""

    measure: int = Field(..., ge=1)
    numerator: int = Field(..., ge=1, le=32)
    denominator: int = Field(
        ...,
        ge=1,
        le=32,
        description="Power of 2 (2, 4, 8, 16)"
    )
```

## Implementation

### 1. Update `src/musicgen/ai_models/composition.py`

```python
class AIComposition(BaseModel):
    """A composition with fluid tempo and meter."""

    # Initial/default values
    tempo: int = Field(default=120, ge=20, le=300)
    time_signature: TimeSignature = Field(
        default_factory=TimeSignature
    )

    # NEW: Change events
    tempo_changes: list[TempoEvent] = Field(
        default_factory=list,
        description="Tempo changes throughout the piece"
    )

    time_signature_changes: list[TimeSignatureEvent] = Field(
        default_factory=list,
        description="Time signature changes by measure"
    )

    def get_tempo_at(self, time: float) -> int:
        """Get the effective tempo at a given time.

        Args:
            time: Position in quarter notes

        Returns:
            Tempo in BPM
        """
        current_tempo = self.tempo
        for change in sorted(self.tempo_changes, key=lambda x: x.time):
            if change.time <= time:
                current_tempo = change.bpm
        return current_tempo

    def get_time_signature_at(self, measure: int) -> TimeSignature:
        """Get the effective time signature at a given measure."""
        current_ts = self.time_signature
        for change in sorted(self.time_signature_changes, key=lambda x: x.measure):
            if change.measure <= measure:
                current_ts = TimeSignature(
                    numerator=change.numerator,
                    denominator=change.denominator
                )
        return current_ts
```

### 2. Update `src/musicgen/renderer/midi.py`

```python
def _add_tempo_track(
    self,
    midi_file: mido.MidiFile,
    composition: AIComposition
) -> None:
    """Add tempo track with tempo changes."""
    track = mido.MidiTrack()
    track.name = "Tempo"

    # Initial tempo
    track.append(mido.MetaMessage(
        'set_tempo',
        tempo=mido.bpm2tempo(composition.tempo)
    ))

    # Tempo changes
    current_time = 0
    for change in sorted(composition.tempo_changes, key=lambda x: x.time):
        delta_ticks = int(change.time * TICKS_PER_QUARTER) - current_time

        if delta_ticks > 0:
            track.append(mido.MetaMessage('delta_time', time=delta_ticks))
            current_time += delta_ticks

        track.append(mido.MetaMessage(
            'set_tempo',
            tempo=mido.bpm2tempo(change.bpm)
        ))

    # End of track
    track.append(mido.MetaMessage('end_of_track'))

    # Insert tempo track at position 0
    midi_file.tracks.insert(0, track)

def _add_time_sigs(
    self,
    track: mido.MidiTrack,
    composition: AIComposition
) -> None:
    """Add time signature events."""
    # Initial time signature
    track.append(mido.MetaMessage(
        'time_signature',
        numerator=composition.time_signature.numerator,
        denominator=composition.time_signature.denominator,
        clocks_per_click=24,
        notated_32nd_notes_beats_per_quarter=8
    ))

    # Changes
    for change in composition.time_signature_changes:
        # Calculate position
        # (This is complex - need to convert measure to ticks)
        ticks = self._measure_to_ticks(change.measure)
        track.append(mido.MetaMessage('delta_time', time=ticks))
        track.append(mido.MetaMessage(
            'time_signature',
            numerator=change.numerator,
            denominator=change.denominator,
            clocks_per_click=24,
            notated_32nd_notes_beats_per_quarter=8
        ))
```

### 3. Update Schema

```python
# src/musicgen/schema/generator.py

def _composition_schema(self) -> dict[str, Any]:
    return {
        "title": "string",
        "tempo": "int (40-200 BPM) - initial tempo",
        "tempo_changes": "array of {time (quarters), bpm}",
        "time_signature": '{"numerator": int, "denominator": int} - initial',
        "time_signature_changes": "array of {measure, numerator, denominator}",
        "key": '{"tonic": "string", "mode": "string"}',
        "parts": "array of Part objects",
    }
```

## Common Patterns

### Ritardando (Slow Down)

```json
{
  "tempo": 120,
  "tempo_changes": [
    {"time": 60, "bpm": 100},
    {"time": 64, "bpm": 80},
    {"time": 68, "bpm": 60}
  ]
}
```

### Accelerando (Speed Up)

```json
{
  "tempo": 80,
  "tempo_changes": [
    {"time": 32, "bpm": 100},
    {"time": 36, "bpm": 120}
  ]
}
```

### Time Signature Change

```json
{
  "time_signature": {"numerator": 4, "denominator": 4},
  "time_signature_changes": [
    {"measure": 17, "numerator": 3, "denominator": 4},  // Waltz section
    {"measure": 33, "numerator": 4, "denominator": 4}   // Back to 4/4
  ]
}
```

## Fermata (Hold Note Longer)

Instead of a tempo change, extend the note duration:

```json
{
  "note_name": "C4",
  "duration": 4.0,     // Normal quarter note
  "fermata": true      // NEW: Hold 2x longer
}
```

Or just use longer duration:
```json
{
  "note_name": "C4",
  "duration": 6.0      // Held longer
}
```

## AI Prompt Updates

```python
# src/musicgen/ai_client/prompts.py

TEMPO AND METER:
You can change tempo and time signature mid-piece:

"tempo_changes": [
  {"time": 0, "bpm": 120},     // Start at 120
  {"time": 48, "bpm": 100},    // Slow down
  {"time": 56, "bpm": 80}      // Slower still
]

"time_signature_changes": [
  {"measure": 17, "numerator": 3, "denominator": 4},  // Switch to 3/4
  {"measure": 33, "numerator": 4, "denominator": 4}   // Back to 4/4
]
```

## Files to Modify

1. `src/musicgen/ai_models/composition.py` - Add event lists
2. `src/musicgen/ai_models/notes.py` - Optionally add `fermata` field
3. `src/musicgen/renderer/midi.py` - Render tempo/meta events
4. `src/musicgen/schema/generator.py` - Update schema
