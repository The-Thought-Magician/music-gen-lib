"""Basic Melody Generation Example.

This example demonstrates how to create a simple melody
using MusicGen's core classes.
"""

from musicgen import HALF, MAJOR, QUARTER, Chord, Scale


def main():
    """Create and display a basic melody."""

    # Create a scale
    print("Creating C major scale...")
    scale = Scale("C", "major")
    print(f"Scale notes: {scale.notes}")

    # Create a simple ascending melody
    print("\nCreating melody...")
    melody_notes = []
    rhythm = [QUARTER, QUARTER, HALF, QUARTER, QUARTER, QUARTER, HALF]

    for i, duration in enumerate(rhythm):
        degree = (i % 7) + 1
        note = scale.get_degree(degree)
        note.duration = duration
        melody_notes.append(note)
        print(f"  {note.name}{note.octave} ({duration} beats)")

    # Create chords for accompaniment
    print("\nCreating chord progression...")
    progression = [
        Chord(_root_name="C", _quality=MAJOR),
        Chord(_root_name="F", _quality=MAJOR),
        Chord(_root_name="G", _quality=MAJOR),
        Chord(_root_name="C", _quality=MAJOR),
    ]

    for chord in progression:
        chord_notes = [n.name for n in chord.notes]
        print(f"  {chord.root_name} {chord.quality}: {chord_notes}")

    # Calculate total duration
    total_duration = sum(n.duration for n in melody_notes)
    print(f"\nTotal melody duration: {total_duration} beats ({total_duration/4:.1f} measures in 4/4)")


if __name__ == "__main__":
    main()
