"""Chord Progression Examples.

Demonstrates various chord progression patterns and how to use them.
"""

from musicgen import Key, Progression


def main():
    """Explore chord progressions."""

    # Working in C major
    key = Key("C", "major")
    print(f"Key: {key}\n")

    # Example 1: Basic I-IV-V-I
    print("1. Basic I-IV-V-I (authentic cadence):")
    prog1 = Progression.from_roman("I-IV-V-I", key="C")
    for chord in prog1.chords:
        print(f"   {chord.root_name} {chord.quality}")

    # Example 2: I-vi-IV-V (pop/rock progression)
    print("\n2. I-vi-IV-V (pop progression):")
    prog2 = Progression.from_roman("I-vi-IV-V", key="C")
    for chord in prog2.chords:
        print(f"   {chord.root_name} {chord.quality}")

    # Example 3: ii-V-I (jazz turnaround)
    print("\n3. ii-V-I (jazz turnaround):")
    prog3 = Progression.from_roman("ii-V-I", key="C")
    for chord in prog3.chords:
        print(f"   {chord.root_name} {chord.quality}")

    # Example 4: Circle of fifths
    print("\n4. Circle of fifths progression:")
    prog4 = Progression.circle_of_fifths("C", length=4)
    for chord in prog4.chords:
        print(f"   {chord.root_name} {chord.quality}")

    # Example 5: Functional generation
    print("\n5. Functionally generated progression:")
    prog5 = Progression.functional(
        key="C",
        length=8,
        cadence="authentic",
        allow_secondary=False
    )
    for i, chord in enumerate(prog5.chords, 1):
        print(f"   {i}. {chord.root_name} {chord.quality}")


if __name__ == "__main__":
    main()
