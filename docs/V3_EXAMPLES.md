# V3 Usage Examples

Practical examples for generating music with music-gen-lib V3.

## Classical String Quartet

Generate a Classical-era string quartet movement with sonata form:

```python
#!/usr/bin/env python3
"""Classical String Quartet Example"""

from pathlib import Path
from musicgen import generate, CompositionRequest
from musicgen.theory.keys import Key
from musicgen.theory.scales import Scale
from musicgen.composition.melody import MelodyGenerator, MelodicContour
from musicgen.theory.progressions import Progression
from musicgen.io.midi_writer import MIDIWriter, Part, Score

# Create a Classical string quartet
def create_classical_quartet():
    """Generate a Classical string quartet movement."""

    # Set up key and scale
    key = Key("G", "major")
    scale = Scale("G", "major")

    # Generate sonata-form progression
    # Exposition: I -> IV -> V -> I (tonic)
    exposition = Progression.from_roman("I-IV-V-I", key="G")

    # Development: relative minor, modulations
    development = Progression.from_roman("i-iv-VII-III-vi-V7", key="E")

    # Recapitulation: return to tonic
    recapitulation = Progression.from_roman("I-IV-V-I", key="G")

    # Create melody generator
    melody_gen = MelodyGenerator(scale, key, tempo=120)
    melody_gen.set_seed(42)  # For reproducibility

    # Generate first violin theme
    first_violin_melody = melody_gen.generate_melody(
        progression=exposition,
        contour=MelodicContour.WAVE,
        motivic_unity=0.8,  # High motivic unity for Classical style
        length=16
    )

    # Create score
    score = Score(
        title="String Quartet in G Major",
        composer="MusicGen AI (Classical Style)"
    )

    # First violin - carries melody
    violin1 = Part(name="Violin I")
    violin1.notes = first_violin_melody.notes

    # Second violin - provides accompaniment and counter-melody
    violin2 = Part(name="Violin II")
    violin2_melody = melody_gen.generate_melody(
        progression=exposition,
        contour=MelodicContour.INVERTED_ARCH,
        motivic_unity=0.6,
        length=16
    )
    # Offset and simplify for accompaniment role
    violin2.notes = [n for i, n in enumerate(violin2_melody.notes) if i % 2 == 0]

    # Viola - inner harmony
    viola = Part(name="Viola")
    for chord in exposition.chords * 4:  # Repeat for full phrase
        # Add third of chord
        viola.add_note(chord.notes[1])

    # Cello - bass line (Alberti bass style)
    cello = Part(name="Cello")
    for chord in exposition.chords * 4:
        # Root and fifth alternating
        cello.add_note(chord.notes[0])
        cello.add_note(chord.notes[2])

    # Add parts to score
    for part in [violin1, violin2, viola, cello]:
        score.add_part(part)

    # Export
    output_path = Path("output/classical_quartet.mid")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    MIDIWriter.write(score, str(output_path), tempo=120)

    return score, output_path

if __name__ == "__main__":
    score, path = create_classical_quartet()
    print(f"Generated Classical String Quartet: {path}")
```

## Film Score Cue

Generate an epic orchestral film score cue with building tension:

```python
#!/usr/bin/env python3
"""Film Score Cue Example"""

from pathlib import Path
from musicgen import generate, CompositionRequest
from musicgen.ai_models.composition import AIComposition, AIPart, AINote
from musicgen.ai_models.notes import ArticulationType
from musicgen.ai_models.parts import InstrumentRole
from musicgen.io.midi_writer import MIDIWriter, Part, Score
from musicgen.theory.keys import Key
from musicgen.theory.progressions import Progression

def create_film_score_cue():
    """Generate an epic orchestral film score cue."""

    # D minor for dramatic effect
    key = Key("D", "minor")

    # Building progression: i -> VI -> iv -> V -> i
    progression = Progression.from_roman("i-VI-iv-V-i", key="D")

    # Create score
    score = Score(
        title="Epic Film Cue",
        composer="MusicGen AI (Film Score Style)"
    )

    # Solo cello opening
    cello = Part(name="Cello")
    cello_notes = []
    start = 0
    for chord in progression.chords:
        cello_notes.extend([
            AINote(note_name="D3", duration=2, start_time=start, velocity=70),
            AINote(note_name="F3", duration=1, start_time=start+2, velocity=65),
            AINote(note_name="A3", duration=1, start_time=start+3, velocity=60),
        ])
        start += 4
    cello.notes = cello_notes

    # Low strings - pedal point on D
    basses = Part(name="Basses")
    bass_notes = [
        AINote(note_name="D2", duration=16, start_time=0, velocity=50,
               articulation=ArticulationType.LEGATO)
    ]
    basses.notes = bass_notes

    # Horns - building entrance
    horns = Part(name="Horns")
    horn_notes = []
    for i, chord in enumerate(progression.chords):
        # Enter gradually
        start = i * 4
        horn_notes.append(
            AINote(
                note_name="D3",
                duration=2,
                start_time=start,
                velocity=50 + i * 10,  # Building volume
                articulation=ArticulationType.MARCATO
            )
        )
    horns.notes = horn_notes

    # Violins - ostinato pattern
    violins = Part(name="Violins")
    violin_notes = []
    for i in range(16):
        # Sixteenth note ostinato
        violin_notes.append(
            AINote(
                note_name="D5" if i % 4 == 0 else "A4",
                duration=0.25,
                start_time=i * 0.5,
                velocity=40,
                articulation=ArticulationType.STACCATO
            )
        )
    violins.notes = violin_notes

    # Full orchestra climax at end
    tutti_brass = Part(name="Tutti Brass")
    tutti_notes = [
        AINote(note_name="D4", duration=4, start_time=16, velocity=110,
               articulation=ArticulationType.ACCENT),
        AINote(note_name="F4", duration=4, start_time=20, velocity=115),
        AINote(note_name="A4", duration=4, start_time=20, velocity=115),
        AINote(note_name="D5", duration=4, start_time=24, velocity=120),
    ]
    tutti_brass.notes = tutti_notes

    # Add all parts
    for part in [cello, basses, horns, violins, tutti_brass]:
        score.add_part(part)

    # Export
    output_path = Path("output/film_score_cue.mid")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    MIDIWriter.write(score, str(output_path), tempo=80)

    return score, output_path

if __name__ == "__main__":
    score, path = create_film_score_cue()
    print(f"Generated Film Score Cue: {path}")
```

## Piano Solo

Generate a Romantic-style piano nocturne:

```python
#!/usr/bin/env python3
"""Piano Solo Example - Nocturne Style"""

from pathlib import Path
from musicgen import generate, CompositionRequest
from musicgen.theory.keys import Key
from musicgen.theory.scales import Scale
from musicgen.composition.melody import MelodyGenerator, MelodicContour
from musicgen.theory.progressions import Progression
from musicgen.io.midi_writer import MIDIWriter, Part, Score
from musicgen.core.note import Note, QUARTER, EIGHTH, HALF, WHOLE

def create_piano_nocturne():
    """Generate a Romantic piano nocturne."""

    # C# minor for melancholic feeling
    key = Key("C#", "minor")
    scale = Scale("C#", "harmonic_minor")

    # Nocturne-style progression: extended chords, slow harmonic rhythm
    progression = Progression.from_roman("i-VII-i-V7-iv-VII-i-V7", key="C#")

    # Create melody with expressive contour
    melody_gen = MelodyGenerator(scale, key, tempo=72)
    melody_gen.set_seed(123)

    # Generate main theme
    melody = melody_gen.generate_melody(
        progression=progression,
        contour=MelodicContour.ARCH,  # Rise to climax then fall
        motivic_unity=0.75,
        length=24
    )

    # Create score
    score = Score(
        title="Nocturne in C# Minor",
        composer="MusicGen AI (Romantic Style)"
    )

    # Right hand - melody
    right_hand = Part(name="Piano RH")
    right_hand.notes = melody.notes

    # Left hand - arpeggiated accompaniment
    left_hand = Part(name="Piano LH")
    left_notes = []

    for i, chord in enumerate(progression.chords):
        # Arpeggio pattern for each chord
        base_time = i * 4

        # Root, third, fifth, third pattern (broken)
        for j in range(4):
            time = base_time + j
            note_idx = j % 3  # 0, 1, 2, 1, 0, 1, 2, 1...

            chord_note = chord.notes[note_idx]
            left_notes.append(
                Note(
                    chord_note.name,
                    chord_note.octave - 1,  # Lower octave
                    EIGHTH
                )
            )

            # Add octave bass on beat 1
            if j == 0:
                left_notes.append(
                    Note(
                        chord_note.name,
                        chord_note.octave - 2,
                        QUARTER
                    )
                )

    left_hand.notes = left_notes

    # Add parts
    score.add_part(right_hand)
    score.add_part(left_hand)

    # Export
    output_path = Path("output/nocturne.mid")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    MIDIWriter.write(score, str(output_path), tempo=72)

    return score, output_path

if __name__ == "__main__":
    score, path = create_piano_nocturne()
    print(f"Generated Piano Nocturne: {path}")
```

## Using Different Styles

Generate pieces in various historical styles:

```python
#!/usr/bin/env python3
"""Different Style Examples"""

from pathlib import Path
from musicgen import generate, CompositionRequest
from musicgen.theory.keys import Key
from musicgen.theory.scales import Scale, ScaleType
from musicgen.composition.melody import MelodyGenerator, MelodicContour
from musicgen.theory.progressions import Progression
from musicgen.io.midi_writer import MIDIWriter, Part, Score

def generate_in_style(style: str, output_dir: Path):
    """Generate a piece in a specific style."""

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if style == "baroque":
        # Baroque: contrapuntal, ornamented, major/minor
        key = Key("D", "major")
        scale = Scale("D", "major")

        # Circle of fifths progression
        progression = Progression.from_roman("I-IV-vii-iii-vi-ii-V-I", key="D")

        title = "Baroque Invention"
        tempo = 100

    elif style == "classical":
        # Classical: balanced phrases, Alberti bass
        key = Key("F", "major")
        scale = Scale("F", "major")

        # Simple functional progression
        progression = Progression.from_roman("I-ii-V-I-V7-I", key="F")

        title = "Classical Minuet"
        tempo = 120

    elif style == "romantic":
        # Romantic: expressive, chromatic
        key = Key("E", "minor")
        scale = Scale("E", "harmonic_minor")

        # More complex chromatic progression
        progression = Progression.from_roman("i-VI-iv-VII-V7-i", key="E")

        title = "Romantic Lied"
        tempo = 80

    elif style == "impressionist":
        # Impressionist: extended harmonies, modal
        key = Key("D", "major")
        scale = Scale("D", ScaleType.LYDIAN)

        # Planing and parallel motion
        progression = Progression.from_roman("I-ii-I-IV-I", key="D")

        title = "Impressionist Sketch"
        tempo = 70

    else:
        raise ValueError(f"Unknown style: {style}")

    # Generate melody appropriate to style
    melody_gen = MelodyGenerator(scale, key, tempo=tempo)
    melody_gen.set_seed(hash(style) % 10000)

    contour = {
        "baroque": MelodicContour.WAVE,
        "classical": MelodicContour.ARCH,
        "romantic": MelodicContour.ASCENDING,
        "impressionist": MelodicContour.WAVE,
    }[style]

    melody = melody_gen.generate_melody(
        progression=progression,
        contour=contour,
        motivic_unity={"baroque": 0.9, "classical": 0.8, "romantic": 0.7,
                       "impressionist": 0.6}[style],
        length=16
    )

    # Create and export
    score = Score(title=title, composer=f"MusicGen AI ({style.title()} Style)")

    main_part = Part(name="Melody")
    main_part.notes = melody.notes
    score.add_part(main_part)

    output_path = output_dir / f"{style.lower()}_piece.mid"
    MIDIWriter.write(score, str(output_path), tempo=tempo)

    return score, output_path

# Generate all styles
if __name__ == "__main__":
    styles = ["baroque", "classical", "romantic", "impressionist"]

    for style in styles:
        score, path = generate_in_style(style, Path("output/styles"))
        print(f"Generated {style.title()}: {path}")
```

## Using AI-Powered Generation

Generate music with natural language prompts:

```python
#!/usr/bin/env python3
"""AI-Powered Composition Examples"""

from pathlib import Path
from musicgen.ai import GeminiComposer
from musicgen.ai.composer import build_composition_from_plan

# Initialize AI composer
composer = GeminiComposer()

# Example 1: Mood-based generation
plan1 = composer.generate_from_mood(
    mood="epic",
    duration_seconds=60
)
score1 = build_composition_from_plan(plan1, seed=42)
print(f"Generated epic piece: {plan1.title}")

# Example 2: Natural language prompt
plan2 = composer.generate_plan(
    prompt="A mysterious nocturne for solo piano with chromatic harmonies",
    duration_seconds=90,
    key="C minor",
    mood="mysterious"
)
score2 = build_composition_from_plan(plan2, seed=123)
print(f"Generated: {plan2.title}")

# Example 3: Specify ensemble
plan3 = composer.generate_plan(
    prompt="A joyful chamber piece for woodwind quintet",
    duration_seconds=120,
    instruments=["flute", "oboe", "clarinet", "bassoon", "horn"]
)
score3 = build_composition_from_plan(plan3, seed=456)
print(f"Generated: {plan3.title}")
```

## Using Mood Presets

Generate music with predefined mood presets:

```python
#!/usr/bin/env python3
"""Mood Preset Examples"""

from pathlib import Path
from musicgen import generate, CompositionRequest, list_available_moods
from musicgen.config.moods import get_mood_preset

# List all available moods
moods = list_available_moods()
print("Available moods:", moods)

# Generate with different moods
output_dir = Path("output/moods")
output_dir.mkdir(parents=True, exist_ok=True)

for mood in ["peaceful", "melancholic", "epic", "playful"]:
    result = generate(CompositionRequest(
        mood=mood,
        duration=30,
        export_formats=["midi"],
        output_dir=str(output_dir),
        seed=hash(mood) % 10000  # Different seed for each mood
    ))

    print(f"{mood.title()}: {result.midi_path}")
    print(f"  Key: {result.key}")
    print(f"  Tempo: {result.tempo}")
    print(f"  Instruments: {', '.join(result.instruments)}")
```

## Export to Multiple Formats

Export a composition to MIDI, audio, MusicXML, and PDF:

```python
#!/usr/bin/env python3
"""Multi-format Export Example"""

from pathlib import Path
from musicgen import generate, CompositionRequest

# Generate composition
result = generate(CompositionRequest(
    mood="peaceful",
    duration=60,
    title="Serenity",
    export_formats=["midi", "audio", "musicxml", "pdf"],
    output_dir="output/multi_format"
))

print("Generated files:")
print(f"  MIDI:      {result.midi_path}")
print(f"  Audio:     {result.audio_path}")
print(f"  MusicXML:  {result.musicxml_path}")
print(f"  PDF:       {result.pdf_path}")

# Note: PDF export requires LilyPond to be installed
# Note: Audio export requires FluidSynth to be installed
```

## Reproducible Generation

Generate the same composition multiple times using a seed:

```python
#!/usr/bin/env python3
"""Reproducible Generation Example"""

from musicgen import generate, CompositionRequest

# Generate with seed for reproducibility
seed = 42

result1 = generate(CompositionRequest(
    mood="peaceful",
    duration=30,
    seed=seed
))

result2 = generate(CompositionRequest(
    mood="peaceful",
    duration=30,
    seed=seed
))

# Both will have identical musical content
assert result1.title == result2.title

print(f"Reproducible generation confirmed!")
print(f"Both produced: {result1.title}")
```

## Custom Instrumentation

Specify exact instruments for your composition:

```python
#!/usr/bin/env python3
"""Custom Instrumentation Example"""

from musicgen import generate, CompositionRequest

# Woodwind trio
result = generate(CompositionRequest(
    mood="playful",
    duration=45,
    instruments=["flute", "clarinet", "bassoon"],
    title="Woodwind Trio",
    export_formats=["midi"]
))

# Unusual ensemble
result = generate(CompositionRequest(
    mood="mysterious",
    duration=60,
    instruments=["violin", "viola", "marimba", "celesta"],
    title="Chamber Mystery",
    export_formats=["midi"]
))
```
