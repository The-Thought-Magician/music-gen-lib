#!/usr/bin/env python
"""V3 Demo Script - Full Pipeline Demonstration.

This script demonstrates the complete V3 music generation pipeline:
1. Create a composition programmatically
2. Validate the composition
3. Export to MIDI with keyswitches
4. Display results
"""

from pathlib import Path

from musicgen.ai_models.v3 import (
    ArticulationType,
    Composition,
    InstrumentPart,
    KeyswitchEvent,
    Note,
    SectionMarker,
    TimeSignature,
    get_dynamic_velocity,
    get_tempo_bpm_range,
)
from musicgen.midi import EnhancedMIDIGenerator
from musicgen.validation import CompositionValidator


def create_demo_composition() -> Composition:
    """Create a demonstration composition showcasing V3 features.

    Returns:
        A complete composition with multiple instruments, articulations,
        and structural events.
    """
    # Violin I part with melody and articulations
    violin1 = InstrumentPart(
        instrument_name="Violin I",
        instrument_family="strings",
        midi_program=40,
        midi_channel=0,
        clef="treble",
        keyswitches=[
            KeyswitchEvent(keyswitch=24, time=0.0, articulation=ArticulationType.LEGATO),
            KeyswitchEvent(keyswitch=26, time=4.0, articulation=ArticulationType.STACCATO),
            KeyswitchEvent(keyswitch=24, time=6.0, articulation=ArticulationType.LEGATO),
        ],
        notes=[
            # Legato melody
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=90, articulation=ArticulationType.LEGATO),
            Note(pitch=62, start_time=1.0, duration=1.0, velocity=85, articulation=ArticulationType.LEGATO),
            Note(pitch=64, start_time=2.0, duration=2.0, velocity=80, articulation=ArticulationType.LEGATO),
            # Staccato section
            Note(pitch=67, start_time=4.0, duration=0.5, velocity=95, articulation=ArticulationType.STACCATO),
            Note(pitch=67, start_time=4.5, duration=0.5, velocity=95, articulation=ArticulationType.STACCATO),
            Note(pitch=65, start_time=5.0, duration=0.5, velocity=90, articulation=ArticulationType.STACCATO),
            # Return to legato
            Note(pitch=64, start_time=6.0, duration=1.0, velocity=85, articulation=ArticulationType.LEGATO),
            Note(pitch=62, start_time=7.0, duration=1.5, velocity=80, articulation=ArticulationType.LEGATO),
            Note(pitch=60, start_time=8.5, duration=1.5, velocity=75, articulation=ArticulationType.LEGATO),
        ],
    )

    # Violin II part with harmony
    violin2 = InstrumentPart(
        instrument_name="Violin II",
        instrument_family="strings",
        midi_program=40,
        midi_channel=1,
        clef="treble",
        keyswitches=[
            KeyswitchEvent(keyswitch=24, time=0.0, articulation=ArticulationType.LEGATO),
            KeyswitchEvent(keyswitch=26, time=4.0, articulation=ArticulationType.STACCATO),
            KeyswitchEvent(keyswitch=24, time=6.0, articulation=ArticulationType.LEGATO),
        ],
        notes=[
            # Lower harmony
            Note(pitch=57, start_time=0.0, duration=1.0, velocity=80, articulation=ArticulationType.LEGATO),
            Note(pitch=57, start_time=1.0, duration=1.0, velocity=75, articulation=ArticulationType.LEGATO),
            Note(pitch=60, start_time=2.0, duration=2.0, velocity=70, articulation=ArticulationType.LEGATO),
            # Staccato harmony
            Note(pitch=60, start_time=4.0, duration=0.5, velocity=85, articulation=ArticulationType.STACCATO),
            Note(pitch=60, start_time=4.5, duration=0.5, velocity=85, articulation=ArticulationType.STACCATO),
            Note(pitch=57, start_time=5.0, duration=0.5, velocity=80, articulation=ArticulationType.STACCATO),
            # Return to legato
            Note(pitch=60, start_time=6.0, duration=1.0, velocity=75, articulation=ArticulationType.LEGATO),
            Note(pitch=57, start_time=7.0, duration=1.5, velocity=70, articulation=ArticulationType.LEGATO),
            Note(pitch=55, start_time=8.5, duration=1.5, velocity=65, articulation=ArticulationType.LEGATO),
        ],
    )

    # Viola part
    viola = InstrumentPart(
        instrument_name="Viola",
        instrument_family="strings",
        midi_program=41,
        midi_channel=2,
        clef="alto",
        keyswitches=[
            KeyswitchEvent(keyswitch=24, time=0.0, articulation=ArticulationType.LEGATO),
            KeyswitchEvent(keyswitch=26, time=4.0, articulation=ArticulationType.STACCATO),
            KeyswitchEvent(keyswitch=24, time=6.0, articulation=ArticulationType.LEGATO),
        ],
        notes=[
            Note(pitch=53, start_time=0.0, duration=1.0, velocity=75, articulation=ArticulationType.LEGATO),
            Note(pitch=53, start_time=1.0, duration=1.0, velocity=70, articulation=ArticulationType.LEGATO),
            Note(pitch=55, start_time=2.0, duration=2.0, velocity=65, articulation=ArticulationType.LEGATO),
            Note(pitch=57, start_time=4.0, duration=0.5, velocity=80, articulation=ArticulationType.STACCATO),
            Note(pitch=57, start_time=4.5, duration=0.5, velocity=80, articulation=ArticulationType.STACCATO),
            Note(pitch=55, start_time=5.0, duration=0.5, velocity=75, articulation=ArticulationType.STACCATO),
            Note(pitch=55, start_time=6.0, duration=1.0, velocity=70, articulation=ArticulationType.LEGATO),
            Note(pitch=53, start_time=7.0, duration=1.5, velocity=65, articulation=ArticulationType.LEGATO),
            Note(pitch=52, start_time=8.5, duration=1.5, velocity=60, articulation=ArticulationType.LEGATO),
        ],
    )

    # Cello part with bass line
    cello = InstrumentPart(
        instrument_name="Cello",
        instrument_family="strings",
        midi_program=42,
        midi_channel=3,
        clef="bass",
        keyswitches=[
            KeyswitchEvent(keyswitch=24, time=0.0, articulation=ArticulationType.LEGATO),
            KeyswitchEvent(keyswitch=26, time=4.0, articulation=ArticulationType.STACCATO),
            KeyswitchEvent(keyswitch=24, time=6.0, articulation=ArticulationType.LEGATO),
        ],
        notes=[
            Note(pitch=48, start_time=0.0, duration=1.0, velocity=70, articulation=ArticulationType.LEGATO),
            Note(pitch=48, start_time=1.0, duration=1.0, velocity=65, articulation=ArticulationType.LEGATO),
            Note(pitch=50, start_time=2.0, duration=2.0, velocity=60, articulation=ArticulationType.LEGATO),
            Note(pitch=50, start_time=4.0, duration=0.5, velocity=75, articulation=ArticulationType.STACCATO),
            Note(pitch=50, start_time=4.5, duration=0.5, velocity=75, articulation=ArticulationType.STACCATO),
            Note(pitch=48, start_time=5.0, duration=0.5, velocity=70, articulation=ArticulationType.STACCATO),
            Note(pitch=48, start_time=6.0, duration=1.0, velocity=65, articulation=ArticulationType.LEGATO),
            Note(pitch=50, start_time=7.0, duration=1.5, velocity=60, articulation=ArticulationType.LEGATO),
            Note(pitch=48, start_time=8.5, duration=1.5, velocity=55, articulation=ArticulationType.LEGATO),
        ],
    )

    # Create the composition
    composition = Composition(
        title="V3 Demo - String Quartet",
        composer="AI Composer V3",
        description="A demonstration piece showcasing V3 features",
        style_period="classical",
        musical_form="ternary",
        key_signature="C major",
        initial_tempo_bpm=120.0,
        tempo_marking="andante",
        time_signature=TimeSignature(numerator=4, denominator=4),
        section_markers=[
            SectionMarker(label="A", time=0.0, rehearsal_letter="A"),
            SectionMarker(label="B", time=4.0, rehearsal_letter="B"),
            SectionMarker(label="A'", time=6.0, rehearsal_letter="C"),
        ],
        parts=[violin1, violin2, viola, cello],
    )

    return composition


def main():
    """Run the V3 demo."""
    print("=" * 60)
    print("V3 Demo: Full Pipeline Demonstration")
    print("=" * 60)
    print()

    # Create composition
    print("1. Creating composition...")
    composition = create_demo_composition()
    print(f"   Title: {composition.title}")
    print(f"   Style: {composition.style_period}")
    print(f"   Form: {composition.musical_form}")
    print(f"   Key: {composition.key_signature}")
    print(f"   Tempo: {composition.initial_tempo_bpm} BPM ({composition.tempo_marking})")
    print(f"   Duration: {composition.duration:.1f} seconds")
    print(f"   Instruments: {composition.instrument_count}")
    print()

    # Show helper function usage
    print("2. Helper functions demo...")
    print(f"   Andante BPM range: {get_tempo_bpm_range('andante')}")
    print(f"   mf velocity: {get_dynamic_velocity('mf')}")
    print()

    # Validate composition
    print("3. Validating composition...")
    validator = CompositionValidator()
    result = validator.validate(composition)
    print(f"   Valid: {result.is_valid}")
    print(f"   Errors: {result.error_count}")
    print(f"   Warnings: {result.warning_count}")
    print()

    # Export to MIDI
    print("4. Exporting to MIDI...")
    output_dir = Path("/tmp/musicgen_v3_demo")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "string_quartet.mid"

    generator = EnhancedMIDIGenerator()
    generated = generator.generate(composition, output_path)
    print(f"   Exported to: {generated}")
    print()

    # Show statistics
    print("5. Composition statistics...")
    for part in composition.parts:
        print(f"   {part.instrument_name}:")
        print(f"     Notes: {part.note_count()}")
        print(f"     Keyswitches: {len(part.keyswitches)}")
        print(f"     CC events: {len(part.cc_events)}")
        print(f"     Articulations used: { {n.articulation for n in part.notes if n.articulation} }")
    print()

    print("=" * 60)
    print("Demo complete!")
    print(f"MIDI file saved to: {output_path}")
    print("You can play this file with any MIDI player or DAW.")
    print("=" * 60)


if __name__ == "__main__":
    main()
