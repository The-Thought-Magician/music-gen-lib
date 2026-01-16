# V3-08: Enhanced MIDI Generator

**Status:** Pending
**Priority:** High
**Dependencies:** V3-02, V3-04, V3-06

## Overview

Create an enhanced MIDI generator that properly outputs keyswitches, CC events, and all necessary MIDI messages for SFZ rendering with articulations.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   Composition (AI Output)                       │
│     Notes with articulations, keyswitches, CC events            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              MIDI File Generator (Enhanced)                     │
│  1. Process keyswitches → MIDI note events                      │
│  2. Process notes → MIDI note-on/note-off                       │
│  3. Apply articulation duration/velocity modifiers              │
│  4. Process CC events → MIDI CC messages                        │
│  5. Process pitch bends → MIDI pitch bend                       │
│  6. Add tempo, time signature, meta events                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MIDI File (.mid)                           │
│              Ready for sfizz-render                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation

```python
from pathlib import Path
from typing import List, Dict, Optional
import mido
from mido import Message, MetaMessage, MidiFile, MidiTrack

from musicgen.ai_models import (
    Composition, InstrumentPart, Note, KeyswitchEvent,
    CCEvent, PitchBendEvent, ProgramChangeEvent,
    ArticulationType, DynamicMarking
)

class EnhancedMIDIGenerator:
    """Generate MIDI files from Composition with full SFZ support."""

    # Standard keyswitch range (C-1 to G-1, MIDI 0-31)
    KEYSWITCH_RANGE_START = 0
    KEYSWITCH_RANGE_END = 31

    # Standard MIDI CC numbers
    CC_MOD_WHEEL = 1
    CC_BREATH = 2
    CC_FOOT = 4
    CC_PORTAMENTO = 5
    CC_VOLUME = 7
    CC_PAN = 10
    CC_EXPRESSION = 11
    CC_SUSTAIN = 64
    CC_SOSTENUTO = 66
    CC_SOFT_PEDAL = 67
    CC_HOLD_2 = 69
    CC_HARMONIC_CONTENT = 71
    CC_RELEASE_TIME = 72
    CC_ATTACK_TIME = 73
    CC_BRIGHTNESS = 74
    CC_DECAY_TIME = 75
    CC_VIBRATO_RATE = 76
    CC_VIBRATO_DEPTH = 77
    CC_VIBRATO_DELAY = 78

    def __init__(
        self,
        ticks_per_beat: int = 480,
        keyswitch_timing_ms: int = 50,
    ):
        """Initialize MIDI generator.

        Args:
            ticks_per_beat: MIDI resolution (PPQ)
            keyswitch_timing_ms: How long before note to send keyswitch (ms)
        """
        self.ticks_per_beat = ticks_per_beat
        self.keyswitch_timing_ms = keyswitch_timing_ms

    def generate(
        self,
        composition: Composition,
        output_path: Path,
    ) -> Path:
        """Generate a MIDI file from a composition.

        Args:
            composition: The composition to render
            output_path: Where to save the MIDI file

        Returns:
            Path to the generated MIDI file
        """
        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)

        # Create track for each part
        for part in composition.parts:
            track = self._generate_part_track(part, composition)
            mid.tracks.append(track)

        # Create tempo/metadata track (track 0)
        meta_track = self._generate_meta_track(composition)
        mid.tracks.insert(0, meta_track)

        # Write file
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        mid.save(str(output_path))

        return output_path

    def _generate_meta_track(
        self,
        composition: Composition,
    ) -> MidiTrack:
        """Generate the metadata track (tempo, time sig, etc.)."""
        track = MidiTrack()
        track.name = "Meta"

        # Time signature
        track.append(MetaMessage(
            'time_signature',
            numerator=composition.time_signature.numerator,
            denominator=composition.time_signature.denominator,
            time=0
        ))

        # Key signature (meta message)
        key_number = self._key_signature_to_number(composition.key_signature)
        track.append(MetaMessage(
            'key_signature',
            key=key_number,
            time=0
        ))

        # Initial tempo
        tempo = mido.bpm2tempo(composition.initial_tempo_bpm)
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

        # Track name
        track.append(MetaMessage(
            'track_name',
            name=composition.title,
            time=0
        ))

        return track

    def _generate_part_track(
        self,
        part: InstrumentPart,
        composition: Composition,
    ) -> MidiTrack:
        """Generate a MIDI track for a single instrument part."""
        track = MidiTrack()
        track.name = part.instrument_name

        # Program change (if specified)
        if part.midi_program is not None:
            track.append(Message(
                'program_change',
                program=part.midi_program,
                channel=part.midi_channel,
                time=0
            ))

        # Collect all events with times
        events = self._collect_events(part, composition)
        events.sort(key=lambda e: e['time'])

        # Convert to delta times and add to track
        last_time = 0
        for event in events:
            delta_ticks = self._seconds_to_ticks(event['time'] - last_time, composition.initial_tempo_bpm)
            last_time = event['time']

            msg = self._event_to_message(event, part.midi_channel)
            if msg:
                msg.time = delta_ticks
                track.append(msg)

        # End of track
        track.append(MetaMessage('end_of_track', time=0))

        return track

    def _collect_events(
        self,
        part: InstrumentPart,
        composition: Composition,
    ) -> List[Dict]:
        """Collect all MIDI events for a part, sorted by time."""
        events = []

        # Add keyswitches
        for ks in part.keyswitches:
            events.append({
                'type': 'keyswitch',
                'time': ks.time,
                'keyswitch': ks.keyswitch,
                'channel': ks.channel
            })

        # Add program changes
        for pc in part.program_changes:
            events.append({
                'type': 'program_change',
                'time': pc.time,
                'program': pc.program,
                'channel': pc.channel
            })

        # Add CC events
        for cc in part.cc_events:
            events.append({
                'type': 'cc',
                'time': cc.start_time,
                'controller': cc.controller,
                'value': cc.value,
                'channel': cc.channel
            })

        # Add pitch bends
        for pb in part.pitch_bends:
            events.append({
                'type': 'pitch_bend',
                'time': pb.start_time,
                'value': pb.value,
                'channel': pb.channel
            })

        # Add notes
        for note in part.notes:
            events.append({
                'type': 'note_on',
                'time': note.start_time,
                'pitch': note.pitch,
                'velocity': note.velocity,
                'duration': note.duration,
                'channel': part.midi_channel,
                'note': note
            })

            # Note off event
            events.append({
                'type': 'note_off',
                'time': note.start_time + note.duration,
                'pitch': note.pitch,
                'channel': part.midi_channel
            })

        return events

    def _event_to_message(
        self,
        event: Dict,
        channel: int,
    ) -> Optional[Message]:
        """Convert an event dict to a MIDI message."""
        event_type = event['type']

        if event_type == 'keyswitch':
            # Keyswitches are just note events at low velocity
            return Message(
                'note_on',
                note=event['keyswitch'],
                velocity=0,  # Keyswitches typically use velocity 0
                channel=event['channel']
            )

        elif event_type == 'program_change':
            return Message(
                'program_change',
                program=event['program'],
                channel=event['channel']
            )

        elif event_type == 'cc':
            return Message(
                'control_change',
                control=event['controller'],
                value=event['value'],
                channel=event['channel']
            )

        elif event_type == 'pitch_bend':
            return Message(
                'pitchwheel',
                pitch=event['value'] - 8192,  # Convert to signed
                channel=event['channel']
            )

        elif event_type == 'note_on':
            return Message(
                'note_on',
                note=event['pitch'],
                velocity=event['velocity'],
                channel=channel
            )

        elif event_type == 'note_off':
            return Message(
                'note_off',
                note=event['pitch'],
                velocity=0,
                channel=channel
            )

        return None

    def _seconds_to_ticks(
        self,
        seconds: float,
        tempo_bpm: float,
    ) -> int:
        """Convert time in seconds to MIDI ticks."""
        seconds_per_beat = 60.0 / tempo_bpm
        beats = seconds / seconds_per_beat
        return int(beats * self.ticks_per_beat)

    def _key_signature_to_number(self, key_signature: str) -> int:
        """Convert key signature string to MIDI key number."""
        # MIDI key: -7 = 7 flats, 0 = C major/A minor, +7 = 7 sharps
        key_map = {
            # Major keys
            "Cb major": -7, "Gb major": -6, "Db major": -5, "Ab major": -4,
            "Eb major": -3, "Bb major": -2, "F major": -1, "C major": 0,
            "G major": 1, "D major": 2, "A major": 3, "E major": 4,
            "B major": 5, "F# major": 6, "C# major": 7,
            # Minor keys
            "Ab minor": -7, "Eb minor": -6, "Bb minor": -5, "F minor": -4,
            "C minor": -3, "G minor": -2, "D minor": -1, "A minor": 0,
            "E minor": 1, "B minor": 2, "F# minor": 3, "C# minor": 4,
            "G# minor": 5, "D# minor": 6, "A# minor": 7,
        }
        return key_map.get(key_signature, 0)

    def generate_with_keyswitch_timing(
        self,
        composition: Composition,
        output_path: Path,
        keyswitch_timing_ms: int = 50,
    ) -> Path:
        """Generate MIDI with proper keyswitch timing.

        Keyswitches should be sent slightly before the notes they affect.

        Args:
            composition: The composition
            output_path: Output file path
            keyswitch_timing_ms: How long before notes to send keyswitch
        """
        # Adjust keyswitch timing in each part
        for part in composition.parts:
            self._adjust_keyswitch_timing(part, keyswitch_timing_ms)

        return self.generate(composition, output_path)

    def _adjust_keyswitch_timing(
        self,
        part: InstrumentPart,
        timing_ms: float,
    ) -> None:
        """Adjust keyswitch events to occur before their notes."""
        for ks in part.keyswitches:
            # Find first note after this keyswitch
            next_notes = [
                n for n in part.notes
                if n.start_time >= ks.time
            ]
            if next_notes:
                next_note = min(next_notes, key=lambda n: n.start_time)
                # Place keyswitch before the note
                ks.time = max(0, next_note.start_time - (timing_ms / 1000.0))
```

## Articulation Helper

```python
class ArticulationHelper:
    """Helper for managing articulations in MIDI generation."""

    # Default duration multipliers by articulation
    DURATION_MULTIPLIERS = {
        ArticulationType.LEGATO: 1.0,
        ArticulationType.DETACHE: 0.85,
        ArticulationType.STACCATO: 0.4,
        ArticulationType.SPICCATO: 0.3,
        ArticulationType.MARCATO: 0.7,
        ArticulationType.PIZZICATO: 0.25,
        ArticulationType.TREMOLO: 1.0,
        ArticulationType.SUL_PONTICELLO: 1.0,
        ArticulationType.COL_LEGNO: 0.5,
    }

    # Default velocity multipliers by articulation
    VELOCITY_MULTIPLIERS = {
        ArticulationType.LEGATO: 0.95,
        ArticulationType.DETACHE: 1.0,
        ArticulationType.STACCATO: 1.15,
        ArticulationType.SPICCATO: 1.1,
        ArticulationType.MARCATO: 1.2,
        ArticulationType.PIZZICATO: 1.2,
        ArticulationType.TREMOLO: 0.85,
        ArticulationType.ACCENT: 1.3,
        ArticulationType.SFORZANDO: 1.4,
    }

    @classmethod
    def apply_articulation_to_note(
        cls,
        note: Note,
        articulation: ArticulationType,
    ) -> tuple[int, float]:
        """Apply articulation modifiers to a note.

        Args:
            note: The note to modify
            articulation: The articulation to apply

        Returns:
            Tuple of (modified_velocity, modified_duration)
        """
        vel_mult = cls.VELOCITY_MULTIPLIERS.get(articulation, 1.0)
        dur_mult = cls.DURATION_MULTIPLIERS.get(articulation, 1.0)

        modified_velocity = min(127, int(note.velocity * vel_mult))
        modified_duration = note.duration * dur_mult

        return modified_velocity, modified_duration

    @classmethod
    def get_keyswitch_for_articulation(
        cls,
        instrument_name: str,
        articulation: ArticulationType,
        keyswitch_map: dict,
    ) -> Optional[int]:
        """Get the keyswitch number for an instrument's articulation.

        Args:
            instrument_name: Name of the instrument
            articulation: The articulation type
            keyswitch_map: Mapping of instrument/articulation to keyswitch numbers

        Returns:
            Keyswitch MIDI note number, or None if not found
        """
        return keyswitch_map.get(f"{instrument_name}.{articulation}")
```

## MIDI Export with Tracks

```python
def export_multitrack_midi(
    composition: Composition,
    output_dir: Path,
) -> List[Path]:
    """Export each part to a separate MIDI file.

    Useful for rendering each instrument separately with different SFZ libraries.

    Args:
        composition: The composition to export
        output_dir: Directory to save MIDI files

    Returns:
        List of paths to exported MIDI files
    """
    generator = EnhancedMIDIGenerator()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    exported_paths = []

    for part in composition.parts:
        # Create single-part composition
        single_part = Composition(
            title=f"{composition.title} - {part.instrument_name}",
            key_signature=composition.key_signature,
            initial_tempo_bpm=composition.initial_tempo_bpm,
            time_signature=composition.time_signature,
            parts=[part]
        )

        # Generate filename
        filename = f"{part.instrument_name.replace(' ', '_').lower()}.mid"
        output_path = output_dir / filename

        # Export
        generator.generate(single_part, output_path)
        exported_paths.append(output_path)

    return exported_paths
```

---

## Implementation Tasks

1. [ ] Create `EnhancedMIDIGenerator` class
2. [ ] Implement keyswitch timing
3. [ ] Implement CC and pitch bend handling
4. [ ] Add tempo and time signature handling
5. [ ] Create `ArticulationHelper` class
6. [ ] Add multitrack export functionality
7. [ ] Write unit tests for MIDI generation
8. [ ] Add validation for keyswitch ranges

## Success Criteria

- Generates valid MIDI files
- Keyswitches placed before notes
- CC events correctly encoded
- Tempo and time signature included
- Can export individual parts

## Next Steps

- V3-09: AI Composer Integration
- V3-10: Testing and Quality Assurance
