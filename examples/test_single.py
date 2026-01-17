#!/usr/bin/env python
"""Test single composition generation with full flow."""

import os
from pathlib import Path

from musicgen.composer_v3 import AIComposerV3

# Set API key
os.environ["GOOGLE_API_KEY"] = "***REMOVED***"


def main():
    """Test single composition generation."""
    print("=" * 70)
    print("Single Composition Test - Full Flow")
    print("=" * 70)
    print()

    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Initialize composer
    print("1. Initializing AI Composer...")
    composer = AIComposerV3()
    print(f"   System prompt loaded: {len(composer.system_prompt)} chars")
    print(f"   Instrument library: {len(composer.instrument_library.instruments)} instruments")
    print(f"   SFZ available: {composer._sfz_available}")
    print()

    # Simple test prompt
    prompt = "A gentle piano melody in C major, slow and peaceful like a sunrise"
    output_path = output_dir / "test_single.mp3"

    print("2. Generating composition...")
    print(f"   Prompt: {prompt}")
    print(f"   Output: {output_path}")
    print()

    try:
        # First, just generate the composition (no rendering)
        print("   Step 1: Generate composition...")
        response = composer.compose(
            prompt=prompt,
            duration_seconds=30,
            key_signature="C major",
            style_period="classical",
            ensemble="solo_piano",
            validate=False,  # Skip validation for now
        )

        composition = response.composition
        print(f"   Title: {composition.title}")
        print(f"   Key: {composition.key_signature}")
        print(f"   Tempo: {composition.initial_tempo_bpm} BPM")
        print(f"   Parts: {composition.instrument_count}")
        for part in composition.parts:
            print(f"     - {part.instrument_name}: {part.note_count()} notes")
        print()

        # Export to MIDI
        print("   Step 2: Export to MIDI...")
        midi_path = output_dir / "test_single.mid"
        composer.midi_generator.generate(composition, midi_path)
        print(f"   MIDI saved: {midi_path}")
        print(f"   File size: {midi_path.stat().st_size} bytes")
        print()

        # Render to audio
        print("   Step 3: Render to audio...")
        print("   Using pretty_midi fallback (SFZ not configured)...")
        audio_path = composer.render(
            composition,
            output_path,
            format="mp3",
        )
        print(f"   Audio saved: {audio_path}")
        print(f"   File size: {audio_path.stat().st_size} bytes")
        print()

        print("=" * 70)
        print("SUCCESS! Full flow completed.")
        print("=" * 70)

    except Exception as e:
        print()
        print("=" * 70)
        print(f"ERROR: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
