#!/usr/bin/env python3
"""Examples of mood-based music generation.

This script demonstrates how to use the music generation library
to create music with different moods.
"""

from pathlib import Path

from musicgen import CompositionRequest, generate


def example_epic():
    """Generate epic orchestral music."""
    request = CompositionRequest(
        mood="epic",
        duration=30,
        export_formats=["midi"],
        output_dir="examples/output"
    )
    result = generate(request)
    print(f"Generated epic composition: {result.title}")
    print(f"  Key: {result.key}")
    print(f"  Tempo: {result.tempo} BPM")
    print(f"  MIDI: {result.midi_path}")
    return result


def example_peaceful():
    """Generate peaceful ambient music."""
    request = CompositionRequest(
        mood="peaceful",
        duration=30,
        key="F",
        tempo=70,
        export_formats=["midi"],
        output_dir="examples/output"
    )
    result = generate(request)
    print(f"Generated peaceful composition: {result.title}")
    print(f"  Key: {result.key}")
    print(f"  Tempo: {result.tempo} BPM")
    print(f"  MIDI: {result.midi_path}")
    return result


def example_mysterious():
    """Generate mysterious atmospheric music."""
    request = CompositionRequest(
        mood="mysterious",
        duration=30,
        export_formats=["midi"],
        output_dir="examples/output"
    )
    result = generate(request)
    print(f"Generated mysterious composition: {result.title}")
    print(f"  Key: {result.key}")
    print(f"  Tempo: {result.tempo} BPM")
    print(f"  MIDI: {result.midi_path}")
    return result


def example_custom_mood():
    """Generate music with custom parameters."""
    request = CompositionRequest(
        mood="melancholic",
        duration=20,
        key="Am",
        tempo=55,
        export_formats=["midi"],
        output_dir="examples/output"
    )
    result = generate(request)
    print(f"Generated custom composition: {result.title}")
    print(f"  Key: {result.key}")
    print(f"  Tempo: {result.tempo} BPM")
    print(f"  MIDI: {result.midi_path}")
    return result


def example_all_moods():
    """Generate examples of all available moods."""
    moods = ["epic", "peaceful", "mysterious", "triumphant",
             "melancholic", "playful", "romantic", "tense"]

    for mood in moods:
        print(f"\nGenerating {mood} example...")
        request = CompositionRequest(
            mood=mood,
            duration=15,
            export_formats=["midi"],
            output_dir="examples/output",
            title=f"{mood.capitalize()} Example"
        )
        result = generate(request)
        print(f"  {result.title}: {result.key} at {result.tempo} BPM")


if __name__ == "__main__":
    # Create output directory
    Path("examples/output").mkdir(parents=True, exist_ok=True)

    print("Generating mood-based music examples...")
    print("\n1. Epic example:")
    example_epic()

    print("\n2. Peaceful example:")
    example_peaceful()

    print("\n3. Mysterious example:")
    example_mysterious()

    print("\n4. Custom mood example:")
    example_custom_mood()

    print("\nAll examples generated successfully!")
    print("\nTo generate all moods, uncomment example_all_moods() in __main__")
