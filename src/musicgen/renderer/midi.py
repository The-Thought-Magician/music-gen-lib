"""MIDI rendering from AIComposition."""

from __future__ import annotations

from pathlib import Path

try:
    import mido
    from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False

from musicgen.ai_models import (
    AIComposition,
    AINote,
    AIPart,
    AIRest,
    ControlChangeEvent,
)


class MIDIRenderer:
    """Render AIComposition to MIDI file."""

    def __init__(self, ticks_per_beat: int = 480):
        """Initialize MIDI renderer.

        Args:
            ticks_per_beat: MIDI resolution (PPQ)
        """
        if not MIDO_AVAILABLE:
            raise RuntimeError("mido package required. Install with: pip install mido")
        self.ticks_per_beat = ticks_per_beat

    def render(
        self,
        composition: AIComposition,
        output_path: Path,
    ) -> None:
        """Render composition to MIDI file.

        Args:
            composition: AIComposition to render
            output_path: Output MIDI file path
        """
        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)

        # Create tempo track
        tempo_track = MidiTrack()
        mid.tracks.append(tempo_track)

        # Set tempo
        tempo_track.append(MetaMessage('set_tempo', tempo=bpm2tempo(composition.tempo)))
        # Set time signature
        numerator = composition.time_signature.numerator
        denominator = composition.time_signature.denominator
        tempo_track.append(MetaMessage('time_signature', numerator=numerator, denominator=denominator))
        # End of track markers (for compatibility)
        tempo_track.append(MetaMessage('end_of_track'))

        # Get parts (handles both part-based and measure-based structures)
        parts = composition.get_parts()

        # Create track for each part
        for part in parts:
            track = self._render_part(part, composition)
            mid.tracks.append(track)

        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        mid.save(output_path)

    def _render_part(self, part: AIPart, composition: AIComposition) -> MidiTrack:
        """Render a single part to a MIDI track.

        Args:
            part: Part to render
            composition: Full composition (for tempo context)

        Returns:
            MidiTrack
        """
        track = MidiTrack()

        # Track name
        track.append(MetaMessage('track_name', name=part.name))

        # Set instrument (program change)
        track.append(Message('program_change', program=part.midi_program, channel=part.midi_channel))

        # Set initial volume
        track.append(Message('control_change', control=7, value=100, channel=part.midi_channel))

        # Track events
        current_time = 0
        events = self._part_to_events(part)

        for event_time, message in sorted(events, key=lambda x: x[0]):
            delta = event_time - current_time
            track.append(message.copy(time=int(delta)))
            current_time = event_time

        # End of track
        track.append(MetaMessage('end_of_track', time=0))

        return track

    def _part_to_events(self, part: AIPart) -> list[tuple[int, Message]]:
        """Convert part to list of (time, message) tuples.

        Args:
            part: Part to convert

        Returns:
            List of (tick_time, Message)
        """
        events = []
        current_tick = 0
        channel = part.midi_channel

        # Check if any note has explicit start_time (polyphony mode)
        has_absolute_timing = any(
            isinstance(n, AINote) and n.start_time is not None
            for n in part.get_note_events()
        )

        if has_absolute_timing:
            # Polyphony mode: use absolute timing
            for note_event in part.get_note_events():
                if isinstance(note_event, AINote):
                    midi_note = note_event.get_midi_number()
                    start_tick = self._duration_to_ticks(
                        note_event.start_time if note_event.start_time is not None else current_tick
                    )
                    duration_ticks = self._duration_to_ticks(note_event.duration)
                    velocity = note_event.velocity

                    # Note on at absolute time
                    events.append((
                        start_tick,
                        Message('note_on', note=midi_note, velocity=velocity, channel=channel)
                    ))

                    # Note off at absolute time + duration
                    events.append((
                        start_tick + duration_ticks,
                        Message('note_off', note=midi_note, velocity=0, channel=channel)
                    ))

                elif isinstance(note_event, AIRest):
                    # Rests in absolute timing mode are implicit (silence between notes)
                    pass
        else:
            # Sequential mode (original behavior)
            for note_event in part.get_note_events():
                if isinstance(note_event, AIRest):
                    # Just advance time
                    current_tick += self._duration_to_ticks(note_event.duration)

                elif isinstance(note_event, AINote):
                    midi_note = note_event.get_midi_number()
                    duration_ticks = self._duration_to_ticks(note_event.duration)
                    velocity = note_event.velocity

                    # Note on
                    events.append((
                        current_tick,
                        Message('note_on', note=midi_note, velocity=velocity, channel=channel)
                    ))

                    # Note off
                    events.append((
                        current_tick + duration_ticks,
                        Message('note_off', note=midi_note, velocity=0, channel=channel)
                    ))

                    current_tick += duration_ticks

        # Add CC events
        for cc_event in part.get_cc_events():
            cc_tick = self._duration_to_ticks(cc_event.time)
            events.append((
                cc_tick,
                Message('control_change', control=cc_event.controller, value=cc_event.value, channel=channel)
            ))

        return events

    def _duration_to_ticks(self, duration_quarters: float) -> int:
        """Convert duration in quarter notes to ticks.

        Args:
            duration_quarters: Duration in quarter notes

        Returns:
            Duration in ticks
        """
        return int(duration_quarters * self.ticks_per_beat)
