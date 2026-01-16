"""Enhanced MIDI generator for V3 compositions.

This module provides MIDI file generation with full SFZ support including
keyswitches, CC events, pitch bends, and time-based events.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

try:
    import mido
    from mido import Message, MetaMessage, MidiFile, MidiTrack
except ImportError:
    mido = None
    MidiFile = None
    MidiTrack = None
    Message = None
    MetaMessage = None

if TYPE_CHECKING:
    from musicgen.ai_models.v3.composition import Composition
    from musicgen.ai_models.v3.parts import InstrumentPart
    from musicgen.ai_models.v3.notes import Note

from musicgen.ai_models.v3.articulation import (
    DEFAULT_DURATION_MULTIPLIERS,
    DEFAULT_VELOCITY_MULTIPLIERS,
    ArticulationType,
)


class EnhancedMIDIGenerator:
    """Generate MIDI files from Composition with full SFZ support.

    This generator handles:
    - Note events with pitch, velocity, duration
    - Keyswitch events for articulation changes
    - CC events for expression
    - Pitch bend events
    - Program change events
    - Tempo and time signature meta events
    """

    # Standard keyswitch range (C-1 to G-1, MIDI 0-31)
    KEYSWITCH_RANGE_START = 0
    KEYSWITCH_RANGE_END = 31

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
        if mido is None:
            raise RuntimeError("mido library is required. Install with: pip install mido")

        self.ticks_per_beat = ticks_per_beat
        self.keyswitch_timing_ms = keyswitch_timing_ms

    def generate(
        self,
        composition: Composition,
        output_path: str | Path,
    ) -> Path:
        """Generate a MIDI file from a composition.

        Args:
            composition: The composition to render
            output_path: Where to save the MIDI file

        Returns:
            Path to the generated MIDI file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)

        # Create track for each part
        for part in composition.parts:
            track = self._generate_part_track(part, composition)
            mid.tracks.append(track)

        # Create tempo/metadata track (track 0)
        meta_track = self._generate_meta_track(composition)
        mid.tracks.insert(0, meta_track)

        # Write file
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
        key_str = self._key_signature_to_mido_format(composition.key_signature)
        track.append(MetaMessage(
            'key_signature',
            key=key_str,
            time=0
        ))

        # Initial tempo
        tempo = mido.bpm2tempo(composition.initial_tempo_bpm)
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

        # Track name
        if composition.title:
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
        last_time = 0.0
        for event in events:
            delta_ticks = self._seconds_to_ticks(
                event['time'] - last_time,
                composition.initial_tempo_bpm
            )
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
    ) -> list[dict]:
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
            # Apply articulation modifiers
            duration = note.duration
            velocity = note.velocity

            if note.articulation:
                dur_mult = DEFAULT_DURATION_MULTIPLIERS.get(note.articulation, 1.0)
                vel_mult = DEFAULT_VELOCITY_MULTIPLIERS.get(note.articulation, 1.0)
                duration = duration * dur_mult
                velocity = min(127, max(0, int(velocity * vel_mult)))

            events.append({
                'type': 'note_on',
                'time': note.start_time,
                'pitch': note.pitch,
                'velocity': velocity,
                'duration': duration,
                'channel': part.midi_channel,
            })

            # Note off event
            events.append({
                'type': 'note_off',
                'time': note.start_time + duration,
                'pitch': note.pitch,
                'channel': part.midi_channel
            })

        return events

    def _event_to_message(
        self,
        event: dict,
        channel: int,
    ) -> Message | None:
        """Convert an event dict to a MIDI message."""
        event_type = event['type']

        if event_type == 'keyswitch':
            # Keyswitches are just note events at low velocity
            return Message(
                'note_on',
                note=event['keyswitch'],
                velocity=0,
                channel=event.get('channel', channel)
            )

        elif event_type == 'program_change':
            return Message(
                'program_change',
                program=event['program'],
                channel=event.get('channel', channel)
            )

        elif event_type == 'cc':
            return Message(
                'control_change',
                control=event['controller'],
                value=event['value'],
                channel=event.get('channel', channel)
            )

        elif event_type == 'pitch_bend':
            return Message(
                'pitchwheel',
                pitch=event['value'] - 8192,  # Convert to signed
                channel=event.get('channel', channel)
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

    def _key_signature_to_mido_format(self, key_signature: str) -> str:
        """Convert key signature string to mido format.

        Mido expects keys as strings like 'C', 'Am', 'F#m', 'Bb', etc.
        """
        # Mapping from our format to mido format
        key_map = {
            # Major keys
            "Cb major": "Cb", "Gb major": "Gb", "Db major": "Db", "Ab major": "Ab",
            "Eb major": "Eb", "Bb major": "Bb", "F major": "F", "C major": "C",
            "G major": "G", "D major": "D", "A major": "A", "E major": "E",
            "B major": "B", "F# major": "F#", "C# major": "C#",
            # Minor keys
            "Ab minor": "Abm", "Eb minor": "Ebm", "Bb minor": "Bbm", "F minor": "Fm",
            "C minor": "Cm", "G minor": "Gm", "D minor": "Dm", "A minor": "Am",
            "E minor": "Em", "B minor": "Bm", "F# minor": "F#m", "C# minor": "C#m",
            "G# minor": "G#m", "D# minor": "D#m", "A# minor": "A#m",
        }
        return key_map.get(key_signature, "C")


class ArticulationHelper:
    """Helper for managing articulations in MIDI generation."""

    # Default duration multipliers by articulation
    DURATION_MULTIPLIERS = DEFAULT_DURATION_MULTIPLIERS

    # Default velocity multipliers by articulation
    VELOCITY_MULTIPLIERS = DEFAULT_VELOCITY_MULTIPLIERS

    @classmethod
    def apply_articulation_to_note(
        cls,
        note: Note,
        articulation: ArticulationType | None,
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


def export_multitrack_midi(
    composition: Composition,
    output_dir: Path,
    generator: EnhancedMIDIGenerator | None = None,
) -> list[Path]:
    """Export each part to a separate MIDI file.

    Useful for rendering each instrument separately with different SFZ libraries.

    Args:
        composition: The composition to export
        output_dir: Directory to save MIDI files
        generator: Optional MIDI generator instance

    Returns:
        List of paths to exported MIDI files
    """
    generator = generator or EnhancedMIDIGenerator()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    exported_paths = []

    for part in composition.parts:
        # Create single-part composition
        from musicgen.ai_models.v3.composition import Composition as V3Composition
        single_part = V3Composition(
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
