# V4-02: Extended Instrument Schema

## Overview

Extend Pydantic models to support all instrument types beyond orchestral: guitars, drums, world instruments, and electronic instruments.

## Objectives

1. Extend instrument definition models with new attributes
2. Add guitar-specific models (frets, strings, techniques)
3. Add drum kit models (kit pieces, mapping)
4. Add world instrument models (microtones, specific techniques)
5. Add electronic instrument models (synth parameters)

## Extended Instrument Model

### New Attributes

```python
class InstrumentTechnique(BaseModel):
    """Extended technique definitions for non-orchestral instruments"""
    name: str
    midi_cc: int | None = None  # MIDI CC for continuous control
    keyswitch: int | None = None
    parameters: dict[str, float] = {}  # Technique-specific parameters

class GuitarTechnique(InstrumentTechnique):
    """Guitar-specific techniques"""
    fret: int | None = None
    string: int | None = None
    pluck_type: Literal["finger", "pick", "thumb", "slap"] = "pick"
    articulation: Literal["normal", "hammer_on", "pull_off",
                         "slide", "bend", "vibrato"] = "normal"

class DrumTechnique(InstrumentTechnique):
    """Drum-specific techniques"""
    stick_type: Literal["stick", "brush", "mallet", "hand", "rod"] = "stick"
    hit_type: Literal["center", "edge", "rimshot", "cross_stick"] = "center"
    damping: bool = False

class MicrotonalNote(BaseModel):
    """For world instruments requiring microtones"""
    note_name: str
    cents: int  # -50 to +50 cents deviation
    frequency_ratio: float | None = None  # For just intonation
```

### Extended Instrument Definition

```python
class ExtendedInstrumentDefinition(BaseModel):
    """Extended model for all instrument types"""
    # Base fields from V3
    name: str
    family: str  # Extended: guitars, drums, world_strings, etc.
    midi_program: int
    default_clef: str
    range: dict[str, int]

    # New extended fields
    category: Literal["orchestral", "guitar", "bass", "drums",
                      "world_strings", "world_winds", "world_percussion",
                      "electronic", "keyboard"]
    subcategory: str | None = None

    # Guitar/Bass specific
    string_count: int | None = None
    fret_count: int | None = None
    tuning: list[str] | None = None  # e.g., ["E2", "A2", "D3", "G3", "B3", "E4"]

    # Drum specific
    kit_pieces: list[str] | None = None
    midi_channel: int = 10  # Channel 10 for drums

    # World instrument specific
    microtonal: bool = False
    playing_techniques: list[str] = []

    # Electronic specific
    synth_type: Literal["subtractive", "fm", "wavetable",
                        "granular", "additive", "physical"] | None = None
    polyphony: int = 16
    multitimbral: bool = False

    # Articulations (extended from V3)
    articulations: dict[str, InstrumentTechnique] = {}

    # SFZ/sample configuration
    sfz_file: str | None = None
    sfz_library: str | None = None
```

## Guitar-Specific Models

```python
class GuitarChord(BaseModel):
    """Represent a guitar chord with fingering"""
    name: str  # e.g., "C", "Am", "F#m7b5"
    voicing: str  # "open", "barre", "jazz", "power"
    fingering: list[tuple[int, int | None]]  # (fret, string) pairs
        # Example: [(0, None), (1, 2), (0, None), (2, 3), (3, 3), (None, None)]
        # Strings: E(6) A(5) D(4) G(3) B(2) E(1)
    fret_range: tuple[int, int]  # Min and max fret used
   难度: Literal["easy", "medium", "hard"] = "medium"

class GuitarPattern(BaseModel):
    """Guitar strumming/picking patterns"""
    name: str
    pattern: list[Literal["down", "up", "mute"]]
    rhythm: str  # Mini-notation
    style: Literal["strum", "pick", "fingerstyle", "slap", "hybrid"]
```

## Drum Kit Models

```python
class DrumPiece(BaseModel):
    """Individual drum in a kit"""
    name: str  # e.g., "kick", "snare", "hihat_closed"
    midi_note: int  # GM drum map note number
    articulations: list[DrumTechnique] = []
    dynamic_range: tuple[int, int] = (1, 127)

class DrumKit(BaseModel):
    """Complete drum kit definition"""
    name: str  # e.g., "standard_rock", "jazz", "electronic_808"
    category: Literal["acoustic", "electronic", "world", "hybrid"]
    pieces: dict[str, DrumPiece]
    defaults: dict[str, Any] = {}
```

## World Instrument Models

```python
class WorldInstrumentDefinition(ExtendedInstrumentDefinition):
    """Extended model for world instruments"""
    region: str  # e.g., "India", "West Africa", "Middle East"
    traditional_name: str | None = None
    instrument_family: str  # e.g., "chordophone", "membranophone"

    # Microtonal specifications
    tuning_system: Literal["equal", "just", "meantone",
                          "indian", "arabic", "other"] = "equal"
    microtone_divisions: int = 1  # Number of microtones per semitone

    # Playing techniques specific to instrument
    techniques: dict[str, dict] = {}  # e.g., {"gamak": {"description": "..."}}
```

## Electronic Instrument Models

```python
class SynthPreset(BaseModel):
    """Synthesizer preset/patch definition"""
    name: str
    type: str  # pad, lead, bass, pluck, etc.
    parameters: dict[str, float] = {}
        # oscillator type, filter cutoff, envelope times, etc.
    mod_routing: dict[str, str] = {}  # LFO -> filter, etc.

class ElectronicInstrumentDefinition(ExtendedInstrumentDefinition):
    """Electronic instrument specifications"""
    synth_type: Literal["subtractive", "fm", "wavetable",
                        "granular", "additive", "sampler"]
    oscillators: int = 1
    filters: int = 0
    lfos: int = 0
    envelopes: int = 1
    effects: list[str] = []  # reverb, delay, etc.
```

## Files to Modify

- `src/musicgen/ai_models/instruments.py` (create)
- `src/musicgen/ai_models/composition.py` (extend)
- `resources/instrument_definitions_world.yaml` (create)

## Success Criteria

- [ ] All extended models defined
- [ ] Guitar chord model with fingering support
- [ ] Drum kit model with GM mapping
- [ ] World instrument model with microtonal support
- [ ] Electronic instrument model with synth parameters
- [ ] All models pass Pydantic validation
- [ ] Type hints complete
- [ ] Docstrings complete

## Next Steps

After completion, proceed to V4-03: MIDI Program Number Mapping
