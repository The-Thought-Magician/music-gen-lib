"""Mood-Based Music Generation Example.

Demonstrates generating music for different moods using presets.
"""

from pathlib import Path

from musicgen import CompositionRequest, generate


def main():
    """Generate compositions for different moods."""

    output_dir = Path("./mood_output")
    output_dir.mkdir(exist_ok=True)

    # Available moods
    moods = [
        "epic",
        "peaceful",
        "mysterious",
        "melancholic"
    ]

    print("MusicGen Mood-Based Generation")
    print("=" * 50)

    for mood in moods:
        print(f"\nGenerating '{mood}' composition...")

        request = CompositionRequest(
            mood=mood,
            duration=15,  # 15 seconds for quick demo
            output_dir=str(output_dir / mood)
        )

        result = generate(request)

        print(f"  Key: {result.key}")
        print(f"  Scale: {result.scale_type}")
        print(f"  Tempo: {result.tempo} BPM")
        print(f"  Instruments: {', '.join(result.instruments[:5])}")

        # Check output files
        if result.midi_path and Path(result.midi_path).exists():
            print(f"  MIDI: {result.midi_path}")

    print("\n" + "=" * 50)
    print(f"All compositions saved to: {output_dir.absolute()}")


if __name__ == "__main__":
    main()
