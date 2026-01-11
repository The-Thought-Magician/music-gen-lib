"""Full Composition Example.

Demonstrates a complete music generation workflow from scale to export.
"""

from pathlib import Path
from musicgen import (
    Scale, Key, Progression,
    MelodyGenerator, MelodicContour,
    Ensemble, Texture,
    MIDIWriter, Score, Part, QUARTER
)


def main():
    """Generate a complete composition."""

    # Setup
    print("Setting up composition...")
    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)

    # Musical elements
    scale = Scale("D", "harmonic_minor")
    key = Key("D", "minor")
    progression = Progression.from_roman("i-iv-VII-i", key="D")

    print(f"Key: {key}")
    print(f"Scale: {scale.notes}")
    print(f"Progression: {[c.root_name for c in progression.chords]}")

    # Create melody
    print("\nGenerating melody...")
    generator = MelodyGenerator(scale, key, tempo=110)
    generator.set_seed(42)  # Reproducible

    melody = generator.generate_melody(
        progression=progression,
        contour=MelodicContour.WAVE,
        form_structure="period",
        motivic_unity=0.8
    )

    print(f"Generated melody with {melody.length} notes")
    print(f"Range: {melody.range} semitones")
    print(f"Duration: {melody.total_duration} beats")

    # Create ensemble
    print("\nSetting up ensemble...")
    ensemble = Ensemble.preset("string_quartet")
    print(f"Instruments: {[inst.name for inst in ensemble.instruments]}")

    # Create score
    print("\nCreating score...")
    score = Score(title="String Quartet in D Minor", composer="MusicGen")

    # Add melody to violin part
    violin_part = Part(name="violin")
    violin_part.notes = melody.notes
    score.add_part(violin_part)

    # Add simple accompaniment parts
    for instrument_name in ["viola", "cello"]:
        harmony_notes = []
        for chord in progression.chords:
            for note in chord.notes[:2]:  # Root and third
                n = Note(note.name, note.octave - 1, QUARTER)
                harmony_notes.append(n)

        part = Part(name=instrument_name)
        part.notes = harmony_notes
        score.add_part(part)

    # Export
    print("\nExporting...")

    # MIDI
    midi_path = output_dir / "composition.mid"
    MIDIWriter.write(score, str(midi_path))
    print(f"  MIDI: {midi_path}")

    # Print summary
    print("\n" + "="*50)
    print("Composition Summary")
    print("="*50)
    print(f"Title: {score.title}")
    print(f"Key: {key}")
    print(f"Tempo: {generator.tempo} BPM")
    print(f"Parts: {len(score.parts)}")
    print(f"Total notes: {sum(len(p.notes) for p in score.parts)}")
    print(f"\nFiles saved to: {output_dir.absolute()}")


if __name__ == "__main__":
    main()
