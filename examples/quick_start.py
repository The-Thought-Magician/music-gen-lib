#!/usr/bin/env python3
"""Quick start example for music generation.

This demonstrates the simplest way to generate music with the library.
"""

from musicgen import generate, CompositionRequest


# Generate music with a single line of code
result = generate(CompositionRequest(
    mood="peaceful",
    duration=30
))

print(f"Generated {result.title}!")
print(f"  Key: {result.key}")
print(f"  Tempo: {result.tempo} BPM")
print(f"  Duration: 30 seconds")
print(f"  MIDI: {result.midi_path}")
