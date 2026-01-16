# Step 14: Add Continuous Controllers (Expression)

## Status: PENDING

## Priority: HIGH

## Problem

Music is more than just Note On/Off events. The current schema cannot represent:

1. **Sustain pedal** - Essential for piano music
2. **Crescendo/decrescendo** - Volume changes while holding a note
3. **Vibrato** - Expressive technique for strings, winds
4. **Pan position** - Stereo placement
5. **Pitch bend** - Glissando, portamento

### Example Problem

A pianist plays a chord, holds the sustain pedal, and lets the notes ring while playing new notes. Current schema:

```json
{
  "notes": [
    {"note_name": "C4", "duration": 0.5},  // Stops too early!
    {"note_name": "E4", "duration": 0.5},
    {"note_name": "G4", "duration": 0.5}
  ]
}
```

Without sustain pedal, notes cut off abruptly.

## Solution: Add CC Events

```python
class ControlChangeEvent(BaseModel):
    """A MIDI Continuous Controller event."""

    controller: int = Field(
        ...,
        ge=0,
        le=127,
        description="MIDI CC number"
    )
    value: int = Field(
        ...,
        ge=0,
        le=127,
        description="Controller value (0-127)"
    )
    time: float = Field(
        ...,
        ge=0,
        description="When this event occurs (quarter notes)"
    )
```

## Essential CC Numbers

| CC | Name | Range | Use |
|----|------|-------|-----|
| 0 | Bank Select MSB | 0-127 | Sound bank selection |
| 1 | Modulation | 0-127 | Vibrato depth |
| 7 | Volume | 0-127 | Master volume |
| 10 | Pan | 0-127 | Stereo position (64=center) |
| 11 | Expression | 0-127 | Dynamic swells |
| 64 | Sustain Pedal | <63/off, ≥64/on | Damper pedal |
| 65 | Portamento | <63/off, ≥64/on | Slide between notes |
| 66 | Sostenuto | <63/off, ≥64/on | Middle pedal |
| 67 | Soft Pedal | <63/off, ≥64/on | Una corda |

## Implementation

### 1. Update `src/musicgen/ai_models/notes.py`

```python
class ControlChangeEvent(BaseModel):
    """A MIDI Continuous Controller event for expression."""

    controller: int = Field(
        ...,
        ge=0,
        le=127,
        description="MIDI CC number (64=sustain, 11=expression, etc.)"
    )
    value: int = Field(
        ...,
        ge=0,
        le=127,
        description="Controller value (0-127)"
    )
    time: float = Field(
        default=0.0,
        ge=0,
        description="Time in quarter notes from part start"
    )

    def get_midi_message(self) -> mido.Message:
        """Convert to MIDI message."""
        return mido.Message(
            'control_change',
            control=self.controller,
            value=self.value
        )
```

### 2. Update `src/musicgen/ai_models/parts.py`

```python
class AIPart(BaseModel):
    """An instrument part with notes and expression events."""

    # ... existing fields ...

    # NEW: Expression events
    cc_events: list[ControlChangeEvent] = Field(
        default_factory=list,
        description="Continuous controller events for expression"
    )

    # Common shortcuts
    sustain_pedal: bool = Field(
        default=False,
        description="Whether sustain pedal is used (auto-generates CC64 events)"
    )
```

### 3. Update `src/musicgen/renderer/midi.py`

```python
def _render_part(self, part: AIPart, composition: AIComposition) -> mido.MidiTrack:
    """Render a part with CC events."""
    track = mido.MidiTrack()

    # Combine note events and CC events, sort by time
    all_events = []

    # Note events
    current_time = 0
    for note in part.notes:
        start = note.start_time * TICKS_PER_QUARTER
        duration = note.duration * TICKS_PER_QUARTER
        all_events.append((start, 'note_on', note))
        all_events.append((start + duration, 'note_off', note))

    # CC events
    for cc in part.cc_events:
        time = cc.time * TICKS_PER_QUARTER
        all_events.append((time, 'cc', cc))

    # Sort by time
    all_events.sort(key=lambda x: x[0])

    # Render events
    current_time = 0
    for time, event_type, data in all_events:
        delta = int(time - current_time)

        if delta > 0:
            track.append(mido.MetaMessage('delta_time', time=delta))
            current_time = time

        if event_type == 'note_on':
            track.append(mido.Message(
                'note_on',
                note=data.get_midi_number(),
                velocity=data.velocity,
                channel=part.midi_channel
            ))
        elif event_type == 'note_off':
            track.append(mido.Message(
                'note_off',
                note=data.get_midi_number(),
                velocity=0,
                channel=part.midi_channel
            ))
        elif event_type == 'cc':
            track.append(mido.Message(
                'control_change',
                control=data.controller,
                value=data.value,
                channel=part.midi_channel
            ))

    return track
```

### 4. Helper: Auto-Generate Sustain

```python
# src/musicgen/ai_models/parts.py

def add_sustain_pedal(
    self,
    on_time: float = 0.0,
    off_time: float | None = None
) -> None:
    """Add sustain pedal CC events.

    Args:
        on_time: When to press sustain (quarter notes)
        off_time: When to release (None = end of part)
    """
    self.cc_events.append(ControlChangeEvent(
        controller=64,
        value=127,  # On
        time=on_time
    ))

    if off_time is None:
        off_time = sum(n.duration for n in self.notes)

    self.cc_events.append(ControlChangeEvent(
        controller=64,
        value=0,  # Off
        time=off_time
    ))
```

## AI Prompt Updates

```python
# src/musicgen/ai_client/prompts.py

CONTINUOUS CONTROLLERS (Expression):
For piano parts, add sustain pedal:
"cc_events": [
  {"controller": 64, "value": 127, "time": 0},    # Sustain ON
  {"controller": 64, "value": 0, "time": 32}     # Sustain OFF
]

For string swells, use expression:
"cc_events": [
  {"controller": 11, "value": 60, "time": 0},    # Start quiet
  {"controller": 11, "value": 100, "time": 4},   # Crescendo
  {"controller": 11, "value": 60, "time": 8}     # Diminuendo
]
```

## Testing

```python
# Test sustain pedal
part = AIPart(
    name="piano",
    notes=[...],
    sustain_pedal=True
)

# Manual CC events
part.cc_events = [
    ControlChangeEvent(controller=64, value=127, time=0),  # On
    ControlChangeEvent(controller=64, value=0, time=32),   # Off
]
```

## Files to Modify

1. `src/musicgen/ai_models/notes.py` - Add `ControlChangeEvent`
2. `src/musicgen/ai_models/parts.py` - Add `cc_events` field
3. `src/musicgen/renderer/midi.py` - Render CC events
4. `src/musicgen/schema/generator.py` - Update schema
5. `src/musicgen/ai_client/prompts.py` - Document CC usage
