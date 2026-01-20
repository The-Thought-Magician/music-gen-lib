"""Indian classical music genre rule implementation.

This module implements the GenreRule interface for Indian classical music,
integrating raga, tala, and ornamentation engines to generate authentic music.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from musicgen.core.note import Note
from musicgen.engine import GenreRule
from musicgen.engine.ornamentation import OrnamentationEngine
from musicgen.engine.parser import CompositionSpec, InstrumentSpec, SectionSpec
from musicgen.engine.raga import RagaEngine
from musicgen.engine.tala import TalaEngine

if TYPE_CHECKING:
    from collections.abc import Sequence


class IndianClassicalRule(GenreRule):
    """Genre rule for Indian classical music generation.

    Implements authentic Indian classical music generation using:
    - Raga system for melody (aroha/avaroha, vadi/samvadi)
    - Tala system for rhythm (teental, jhaptal, etc.)
    - Ornamentation system (meend, gamaka, krintan)
    """

    @property
    def genre_name(self) -> str:
        return "indian_classical"

    def __init__(self) -> None:
        self._raga_engine = RagaEngine()
        self._tala_engine = TalaEngine()
        self._ornamentation_engine = OrnamentationEngine()

    def generate_melody(
        self,
        spec: CompositionSpec,
        section: SectionSpec,
        instrument: InstrumentSpec,
    ) -> list[Note]:
        """Generate melody notes for Indian classical music.

        Uses raga-based note selection following:
        - Aroha/avaroha patterns
        - Vadi/samvadi emphasis
        - Pakad (characteristic phrases) where available
        - Tala cycle alignment (sam resolution)

        Args:
            spec: Full composition specification
            section: Section specification (alap, gat, etc.)
            instrument: Instrument specification

        Returns:
            List of Note objects forming the melody
        """
        # Get raga from melody rules
        raga_name = spec.melody_rules.raga or "yaman"
        raga = self._raga_engine.get_raga(raga_name)

        # Get section parameters
        section_bars = section.duration_bars
        beats_per_bar = spec.time_signature.numerator
        total_beats = section_bars * beats_per_bar

        # Get tala if specified
        tala_name = section.tala or spec.rhythm_rules.tala if spec.rhythm_rules else "teental"
        tala = self._tala_engine.get_tala(tala_name)

        # Calculate timing
        beat_duration = 60.0 / spec.tempo.bpm
        section_duration = section_bars * beats_per_bar * beat_duration

        # Determine note density from rules
        density = spec.melody_rules.density
        notes_per_min = random.randint(*density.notes_per_minute)
        avg_duration = random.uniform(*density.avg_duration_beats) * beat_duration

        # Estimate number of notes
        estimated_notes = int(notes_per_min * (section_duration / 60.0))

        # Get allowed notes from raga
        allowed_notes = raga.get_allowed_notes()

        # Generate melody
        notes: list[Note] = []
        current_time = 0.0

        # Get phrase structure
        phrase_spec = spec.melody_rules.phrases
        register_spec = spec.melody_rules.register

        # Determine octave range
        min_octave = register_spec.lowest_octave
        max_octave = register_spec.highest_octave

        # Generate notes aligned to tala cycles
        tala_cycle_duration = (tala.matras / spec.tempo.bpm) * 60.0
        current_cycle = 0

        # Start from tonic (sa) often
        start_from_tonic = True
        current_note_idx = 0

        while current_time < section_duration:
            # Check if we're at sam (start of tala cycle)
            cycle_time = current_time % tala_cycle_duration
            at_sam = cycle_time < beat_duration

            if at_sam:
                # At sam, emphasize tonic or vadi
                if start_from_tonic and current_note_idx == 0:
                    # Start from tonic
                    pitch = 60  # C4 as tonic base
                elif random.random() < 0.6:
                    pitch = raga.vadi
                else:
                    pitch = random.choice(allowed_notes)

                start_from_tonic = False
            else:
                # Within cycle, use raga-constrained selection
                beat_in_cycle = int(cycle_time / beat_duration)
                accent = tala.get_accent_for_beat(beat_in_cycle)

                # Stronger beats get vadi/samvadi
                if accent >= 2 and random.random() < 0.5:
                    pitch = raga.vadi if accent == 3 else raga.samvadi
                else:
                    # Conjunct motion - prefer nearby notes
                    if notes:
                        last_midi = notes[-1].midi_number
                        # Find nearby notes in raga
                        nearby = [n for n in allowed_notes if abs(n - last_midi) <= 4]
                        if nearby:
                            pitch = random.choice(nearby)
                        else:
                            pitch = random.choice(allowed_notes)
                    else:
                        pitch = random.choice(allowed_notes)

            # Calculate duration
            duration = random.uniform(*density.duration_range) * beat_duration
            duration = min(duration, section_duration - current_time)

            # Determine velocity based on tala accent
            beat_in_cycle = int(cycle_time / beat_duration)
            accent = tala.get_accent_for_beat(beat_in_cycle)
            base_velocity = 70 + accent * 15

            # Get note name and octave from pitch
            note = Note.from_midi(pitch)
            octave = note.octave

            # Clamp to register range
            if octave < min_octave:
                octave = min_octave
            elif octave > max_octave:
                octave = max_octave

            # Create the note
            melody_note = Note(
                note.name,
                octave,
                duration,
                min(base_velocity + random.randint(-5, 5), 127),
            )
            melody_note.start_time = current_time
            notes.append(melody_note)

            current_time += duration
            current_note_idx += 1

        # Apply ornamentation if specified
        if spec.melody_rules.ornamentation:
            notes = self._apply_section_ornamentation(
                notes, spec, section, raga_name
            )

        return notes

    def generate_rhythm(
        self,
        spec: CompositionSpec,
        section: SectionSpec,
        instrument: InstrumentSpec,
    ) -> list[Note]:
        """Generate rhythm notes for Indian classical music.

        For tabla, generates bols mapped to MIDI notes.
        For other percussion, uses tala-based patterns.

        Args:
            spec: Full composition specification
            section: Section specification
            instrument: Instrument specification

        Returns:
            List of Note objects for rhythm
        """
        # Get tala
        tala_name = section.tala or (spec.rhythm_rules.tala if spec.rhythm_rules else "teental")
        tala = self._tala_engine.get_tala(tala_name)

        # Get stroke mapping for tabla
        stroke_mapping = instrument.stroke_mapping or {
            "ghe": 43,  # Low bass (bayan)
            "ke": 40,   # Rim (dayan closed)
            "na": 52,   # Rim (dayan open)
            "tun": 57,  # High resonant
            "dha": 50,  # Combined
            "dhin": 49, # Combined resonant
            "kat": 45,  # Flat
        }

        # Calculate timing
        beat_duration = 60.0 / spec.tempo.bpm
        section_duration = section.duration_bars * spec.time_signature.numerator * beat_duration
        num_cycles = int(section_duration / ((tala.matras * beat_duration)))

        notes: list[Note] = []

        # Get bols for this tala
        bols = tala.bols or ["dha"] * tala.matras

        # Get cycle pattern
        pattern = self._tala_engine.generate_cycle_pattern(
            tala_name, num_cycles, spec.tempo.bpm
        )

        # Generate rhythm notes
        for beat, time, accent in pattern:
            if time >= section_duration:
                break

            # Get bol for this beat
            bol_idx = beat % len(bols)
            bol = bols[bol_idx]

            # Map bol to MIDI note
            midi_note = stroke_mapping.get(bol, 50)

            # Velocity based on accent
            velocity = 64 + accent * 20

            # Duration - tabla strokes are typically short
            duration = beat_duration * 0.8 if accent > 0 else beat_duration * 0.5

            # Create note
            from_midi = Note.from_midi(midi_note)
            note = Note(
                from_midi.name,
                from_midi.octave,
                duration,
                velocity,
            )
            note.start_time = time
            notes.append(note)

        return notes

    def _apply_section_ornamentation(
        self,
        notes: list[Note],
        spec: CompositionSpec,
        section: SectionSpec,
        raga_name: str,
    ) -> list[Note]:
        """Apply ornamentation appropriate for the section.

        Alap gets more meend (slow, expressive)
        Gat gets more gamaka and rhythmic ornamentation

        Args:
            notes: Base melody notes
            spec: Composition specification
            section: Section specification
            raga_name: Name of the raga

        Returns:
            Notes with ornamentation applied
        """
        ornament_spec = spec.melody_rules.ornamentation

        # Determine ornamentation frequency
        match ornament_spec.meend:
            case "frequent":
                meend_freq = "frequent"
            case "occasional":
                meend_freq = "occasional"
            case "rare":
                meend_freq = "rare"
            case _:
                meend_freq = "occasional"

        # Get suggestions from ornamentation engine
        suggestions = self._ornamentation_engine.suggest_ornamentations_for_raga(
            raga_name, notes, frequency=meend_freq
        )

        # Apply ornamentations
        for idx, ornament_types in suggestions.items():
            for ornament_type in ornament_types:
                match ornament_type:
                    case "meend":
                        if idx < len(notes) - 1:
                            self._ornamentation_engine.apply_meend(
                                notes, idx, idx + 1, intensity=0.8
                            )
                    case "gamaka":
                        self._ornamentation_engine.apply_gamaka(
                            notes[idx], oscillations=3, width=2
                        )
                    case "krintan":
                        self._ornamentation_engine.apply_krintan(
                            notes, idx, grace_interval=-2, grace_duration=0.05
                        )
                    case "andolan":
                        self._ornamentation_engine.apply_andolan(
                            notes[idx], width=1, speed=2.0
                        )

        return notes

    def apply_ornamentation(
        self,
        notes: list[Note],
        spec: CompositionSpec,
        instrument: InstrumentSpec,
    ) -> list[Note]:
        """Apply ornamentation to melody notes.

        This is called after melody generation to add the final
        ornamentation layer.

        Args:
            notes: Base melody notes
            spec: Full composition specification
            instrument: Instrument specification

        Returns:
            List of notes with added ornamentation
        """
        if not spec.melody_rules or not spec.melody_rules.raga:
            return notes

        raga_name = spec.melody_rules.raga

        # Create a dummy section for compatibility
        from musicgen.engine.parser import SectionSpec
        section = SectionSpec(name="main")

        return self._apply_section_ornamentation(notes, spec, section, raga_name)
