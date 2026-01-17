# V4-08: Guitar/Bass MIDI Generation

## Overview

Implement realistic MIDI generation for guitar and bass instruments, including fretboard position calculation, string assignment, and technique simulation.

## Objectives

1. Implement fretboard position calculator
2. Implement string assignment logic
3. Implement chord voicing optimization
4. Implement realistic picking patterns
5. Implement technique simulation (slides, bends, vibrato)

## Fretboard Model

```python
class Fretboard:
    """Guitar fretboard model for position calculation"""

    def __init__(
        self,
        tuning: list[str] = None,
        fret_count: int = 24,
        string_count: int = 6
    ):
        self.tuning = tuning or ["E2", "A2", "D3", "G3", "B3", "E4"]
        self.fret_count = fret_count
        self.string_count = string_count

    def find_positions(self, note: str) -> list[tuple[int, int]]:
        """Find all (string, fret) positions for a given note"""
        positions = []
        for string_num, open_note in enumerate(self.tuning, start=1):
            fret = self.note_distance(open_note, note)
            if 0 <= fret <= self.fret_count:
                positions.append((string_num, fret))
        return positions

    def find_optimal_position(
        self,
        note: str,
        previous_position: tuple[int, int] | None = None,
        prefer_high_strings: bool = False
    ) -> tuple[int, int]:
        """Find best position considering hand movement"""

    def calculate_stretch(
        self,
        positions: list[tuple[int, int]]
    ) -> int:
        """Calculate fret span for a chord"""
```

## String Assignment Logic

```python
class GuitarStringAssigner:
    """Assign notes to strings for realistic guitar parts"""

    def __init__(self, fretboard: Fretboard):
        self.fretboard = fretboard

    def assign_melody(
        self,
        notes: list[AINote],
        prefer_position: tuple[int, int] | None = None
    ) -> list[tuple[str, int, int]]:  # (note, string, fret)
        """Assign melody notes to strings minimizing movement"""

    def assign_chord(
        self,
        chord_notes: list[str],
        voicing_type: Literal["open", "barre", "jazz", "power"]
    ) -> list[tuple[str, int, int]]:
        """Assign chord notes to strings for specific voicing"""

    def find_playable_voicing(
        self,
        notes: list[str],
        max_fret_span: int = 4,
        min_string: int = 1,
        max_string: int = 6
    ) -> list[tuple[str, int, int]] | None:
        """Find physically playable voicing"""
```

## Chord Voicing Optimization

```python
class ChordVoicer:
    """Generate optimal guitar chord voicings"""

    def voice_chord(
        self,
        chord: Chord,
        position: int,
        style: Literal["open", "barre", "jazz", "power"]
    ) -> GuitarChord:
        """Voice a chord in specified style"""

    def drop_voicing(
        self,
        chord_notes: list[str],
        drop_voice: int = 2
    ) -> list[str]:
        """Create drop voicing (raise 2nd highest voice an octave)"""

    def invert(
        self,
        chord_notes: list[str],
        inversion: int  # 0=root, 1=first, etc.
    ) -> list[str]:
        """Create chord inversion"""

    def add_extensions(
        self,
        chord: Chord,
        extensions: list[int],  # [7, 9, 11, 13]
        max_fret_span: int = 5
    ) -> list[str]:
        """Add extensions to chord in playable range"""
```

## Realistic Picking Patterns

```python
class GuitarPickingEngine:
    """Generate realistic picking patterns"""

    def create_strum(
        self,
        chord: GuitarChord,
        pattern: StrumPattern,
        swing: float = 0.0
    ) -> list[AINote]:
        """Create strummed chord with pattern"""

    def create_fingerstyle(
        self,
        pattern: list[Literal["p", "i", "m", "a"]],  # Thumb, index, middle, ring
        chord_notes: list[str]
    ) -> list[AINote]:
        """Create fingerstyle pattern"""

    def create_hybrid_picking(
        self,
        pattern: list[Literal["pick", "m", "a"]],
        chord_notes: list[str]
    ) -> list[AINote]:
        """Create hybrid picking pattern"""

    def create_sweep(
        self,
        chord: GuitarChord,
        direction: Literal["up", "down"]
    ) -> list[AINote]:
        """Create sweep picking arpeggio"""
```

## Technique Simulation

```python
class GuitarTechniqueRenderer:
    """Render guitar techniques to MIDI"""

    def render_slide(
        self,
        start_note: str,
        end_note: str,
        duration: float
    ) -> list[MidiEvent]:
        """Render slide as pitch bend sequence"""

    def render_bend(
        self,
        note: str,
        bend_amount: float,  # In semitones
        duration: float
    ) -> list[MidiEvent]:
        """Render bend as pitch bend events"""

    def render_vibrato(
        self,
        note: str,
        duration: float,
        depth: float = 0.1,  # Semitones
        rate: float = 5.0  # Hz
    ) -> list[MidiEvent]:
        """Render vibrato as modulated pitch bend"""

    def render_hammer_on(
        self,
        from_note: str,
        to_note: str,
        timing: float
    ) -> list[MidiEvent]:
        """Render hammer-on (note on, note on, note off)"""

    def render_pull_off(
        self,
        from_note: str,
        to_note: str,
        timing: float
    ) -> list[MidiEvent]:
        """Render pull-off"""

    def render_harmonic(
        self,
        note: str,
        harmonic_type: Literal["natural", "artificial", "pinch"],
        duration: float
    ) -> list[MidiEvent]:
        """Render harmonic with modified velocity and filter"""
```

## Bass-Specific Rendering

```python
class BassRenderer:
    """Render realistic bass lines"""

    def render_finger_bass(
        self,
        notes: list[AINote]
    ) -> list[MidiEvent]:
        """Render finger-style bass with slight variation"""

    def render_slap_bass(
        self,
        notes: list[AINote],
        pattern: list[Literal["thumb", "pop", "ghost"]]
    ) -> list[MidiEvent]:
        """Render slap bass with appropriate accents"""

    def render_walking_bass(
        self,
        chord_progression: list[Chord],
        duration: float
    ) -> list[AINote]:
        """Generate walking bass line over chord changes"""

    def render_ghost_notes(
        self,
        pattern: str  # Mini-notation
    ) -> list[AINote]:
        """Render ghost notes at low velocity"""
```

## MIDI Implementation

```python
def guitar_to_midi(
    part: InstrumentPart,
    instrument: ExtendedInstrumentDefinition
) -> mido.MidiFile:
    """Convert guitar part to MIDI with realistic rendering"""

    # Assign strings and frets
    string_assigner = GuitarStringAssigner(instrument)
    fretboard = Fretboard(
        tuning=instrument.tuning,
        fret_count=instrument.fret_count
    )

    midi_tracks = []

    for note_group in part.note_groups:
        # Assign notes to strings
        positions = string_assigner.assign_chord(
            note_group.notes,
            voicing_type=note_group.voicing
        )

        # Render with techniques
        renderer = GuitarTechniqueRenderer()
        for note, pos in zip(note_group.notes, positions):
            midi_events = []
            midi_events.extend(renderer.render_note_on(note, pos))
            midi_events.extend(renderer.render_technique(
                note,
                note_group.articulation
            ))
            midi_events.extend(renderer.render_note_off(note, pos))

    # Combine into MIDI file
    return midi_file
```

## Files to Create/Modify

- `src/musicgen/instruments/fretboard.py`
- `src/musicgen/instruments/string_assigner.py`
- `src/musicgen/instruments/voicing.py`
- `src/musicgen/renderer/guitar_midi.py`
- `src/musicgen/renderer/bass_midi.py`

## Success Criteria

- [ ] Fretboard model accurate for all tunings
- [ ] String assignment minimizes movement
- [ ] Chord voicings are playable
- [ ] Picking patterns sound realistic
- [ ] Techniques render correctly to MIDI
- [ ] Bass patterns work for all styles
- [ ] Complete test coverage

## Next Steps

After completion, proceed to Phase 2: Drum Kits and Percussion (V4-09)
