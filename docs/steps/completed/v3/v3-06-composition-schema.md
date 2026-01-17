# V3-06: Enhanced Composition Output Schema

**Status:** Pending
**Priority:** High
**Dependencies:** V3-02, V3-04, V3-05

## Overview

Design a comprehensive Pydantic schema for AI composition output that includes all necessary information for SFZ rendering: notes with articulations, keyswitches, CC events, dynamics, and orchestration metadata.

## Schema Design Principles

1. **Complete Rendering Information:** Everything needed for MIDI/Audio output
2. **Validation-Friendly:** AI output can be validated before rendering
3. **Human-Readable:** Easy to inspect and debug
4. **Extensible:** Can grow with new features
5. **Backwards Compatible:** Can export to MIDI even without SFZ

---

## Complete Data Models

```python
from __future__ import annotations
from enum import IntEnum
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
from pathlib import Path

# ============================================================================
# Enums and Constants
# ============================================================================

class DynamicMarking(str):
    """Standard dynamic markings."""
    PPP = "ppp"
    PP = "pp"
    P = "p"
    MP = "mp"
    MF = "mf"
    F = "f"
    FF = "ff"
    FFF = "fff"

    @property
    def velocity_value(self) -> int:
        """Approximate MIDI velocity for this dynamic."""
        return {
            "ppp": 16, "pp": 32, "p": 48, "mp": 64,
            "mf": 80, "f": 96, "ff": 112, "fff": 127
        }[self]

class TempoMarking(str):
    """Standard tempo markings."""
    LARGHISSIMO = "larghissimo"
    GRAVE = "grave"
    LARGO = "largo"
    LENTO = "lento"
    ADAGIO = "adagio"
    LARGHETTO = "larghetto"
    ADAGIETTO = "adagietto"
    ANDANTE = "andante"
    ANDANTINO = "andantino"
    MODERATO = "moderato"
    ALLEGRETTO = "allegretto"
    ALLEGRO = "allegro"
    VIVACE = "vivace"
    PRESTO = "presto"
    PRESTISSIMO = "prestissimo"

    @property
    def bpm_range(self) -> tuple[int, int]:
        """Typical BPM range for this marking."""
        return {
            "larghissimo": (20, 40),
            "grave": (30, 45),
            "largo": (40, 60),
            "lento": (45, 60),
            "adagio": (50, 70),
            "larghetto": (60, 70),
            "adagietto": (65, 80),
            "andante": (70, 85),
            "andantino": (80, 95),
            "moderato": (85, 100),
            "allegretto": (100, 115),
            "allegro": (115, 140),
            "vivace": (135, 160),
            "presto": (150, 180),
            "prestissimo": (170, 220),
        }[self]

class Clef(str):
    """Musical clefs."""
    TREBLE = "treble"
    BASS = "bass"
    ALTO = "alto"
    TENOR = "tenor"
    GRAND_STAFF = "grand_staff"

class InstrumentFamily(str):
    """Instrument families."""
    STRINGS = "strings"
    WOODWINDS = "woodwinds"
    BRASS = "brass"
    PERCUSSION = "percussion"
    KEYBOARDS = "keyboards"
    ELECTRONIC = "electronic"
    VOICES = "voices"

class StylePeriod(str):
    """Stylistic periods."""
    BAROQUE = "baroque"
    CLASSICAL = "classical"
    ROMANTIC = "romantic"
    MODERN = "modern"
    FILM_SCORE = "film_score"
    CONTEMPORARY = "contemporary"

class MusicalForm(str):
    """Musical forms."""
    BINARY = "binary"  # AB
    TERNARY = "ternary"  # ABA
    RONDO = "rondo"  # ABACA...
    SONATA = "sonata"  # Exposition-Development-Recapitulation
    THEME_AND_VARIATIONS = "theme_and_variations"
    MINUET = "minuet"  # Minuet-Trio-Minuet
    SCHERZO = "scherzo"
    THROUGH_COMPOSED = "through_composed"
    STROPHIC = "strophic"

# ============================================================================
# Articulation Models
# ============================================================================

class ArticulationType(str):
    """Types of articulations."""
    # Strings
    LEGATO = "legato"
    DETACHE = "detache"
    STACCATO = "staccato"
    SPICCATO = "spiccato"
    MARCATO = "marcato"
    PIZZICATO = "pizzicato"
    TREMOLO = "tremolo"
    TRILL = "trill"
    SUL_TASTO = "sul_tasto"
    SUL_PONTICELLO = "sul_ponticello"
    COL_LEGNO = "col_legno"
    HARMONIC = "harmonic"
    VIBRATO = "vibrato"
    SENZA_VIBRATO = "senza_vibrato"

    # Woodwinds
    FLUTTER_TONGUE = "flutter_tongue"
    FLUTTER_WW = "flutter_ww"
    STACCATO_WW = "staccato_ww"
    LEGATO_WW = "legato_ww"
    BREATH_ATTACK = "breath_attack"

    # Brass
    MARTELLO = "martello"
    STACCATO_BRASS = "staccato_brass"
    LEGATO_BRASS = "legato_brass"
    MUTED = "muted"
    FALL = "fall"
    DOIT = "doit"
    SHAKE = "shake"
    FLIP = "flip"
    SMEAR = "smear"
    HALF_VALVE = "half_valve"

    # General
    NORMAL = "normal"
    ACCENT = "accent"
    MARCATO_SHORT = "marcato_short"
    TENUTO = "tenuto"
    SFORZANDO = "sforzando"
    SFP = "sforzando_piano"
    FP = "forte_piano"
    RINFORZANDO = "rinforzando"

# ============================================================================
# Note and Event Models
# ============================================================================

class Note(BaseModel):
    """A single musical note with full rendering information."""

    # Pitch
    pitch: int = Field(ge=0, le=127, description="MIDI note number")

    # Timing
    start_time: float = Field(ge=0, description="Start time in seconds")
    duration: float = Field(gt=0, description="Duration in seconds")

    # Velocity
    velocity: int = Field(ge=0, le=127, description="MIDI velocity")

    # Articulation
    articulation: ArticulationType | None = Field(
        default=None,
        description="Articulation to apply to this note"
    )

    # Expressive markings
    dynamic: DynamicMarking | None = Field(
        default=None,
        description="Dynamic marking for this note"
    )

    # Ornamentation
    ornament: str | None = Field(
        default=None,
        description="Ornament (trill, mordent, turn, etc.)"
    )

    # Technical
    tie: bool = Field(default=False, description="Is this note tied to next?")
    slur: bool = Field(default=False, description="Is this note slurred?")
    slur_group_id: int | None = Field(
        default=None,
        description="ID for grouping slurred notes"
    )

    # Extended techniques
    grace_notes: list[Note] | None = Field(
        default=None,
        description="Grace notes before this note"
    )

    # Validation
    @field_validator("pitch")
    def validate_pitch_range(cls, v):
        """Ensure pitch is in valid MIDI range."""
        if not 0 <= v <= 127:
            raise ValueError(f"Pitch must be 0-127, got {v}")
        return v

    @field_validator("duration")
    def validate_duration(cls, v):
        """Ensure duration is positive and reasonable."""
        if v <= 0:
            raise ValueError(f"Duration must be positive, got {v}")
        if v > 60:  # 1 minute per note is excessive
            raise ValueError(f"Duration too long: {v}s")
        return v

class KeyswitchEvent(BaseModel):
    """A keyswitch event to change articulation."""

    keyswitch: int = Field(ge=0, le=127, description="MIDI note for keyswitch")
    time: float = Field(ge=0, description="Time in seconds")
    articulation: ArticulationType
    channel: int = Field(default=0, ge=0, le=15)

class CCEvent(BaseModel):
    """A continuous controller message."""

    controller: int = Field(ge=0, le=127, description="CC number")
    value: int = Field(ge=0, le=127, description="CC value")
    start_time: float = Field(ge=0, description="Start time in seconds")
    duration: float | None = Field(
        default=None,
        description="Duration for ramped changes (None = instantaneous)"
    )
    channel: int = Field(default=0, ge=0, le=15)

    # Common CC numbers
    CC_MOD_WHEEL = 1
    CC_BREATH = 2
    CC_FOOT = 4
    CC_PORTAMENTO = 5
    CC_DATA_ENTRY = 6
    CC_VOLUME = 7
    CC_PAN = 10
    CC_EXPRESSION = 11
    CC_SUSTAIN = 64
    CC_SOSTENUTO = 66
    CC_SOFT_PEDAL = 67
    CC_HOLD_2 = 69
    CC_HARMONIC_CONTENT = 71
    CC_RELEASE_TIME = 72
    CC_ATTACK_TIME = 73
    CC_BRIGHTNESS = 74
    CC_DECAY_TIME = 75
    CC_VIBRATO_RATE = 76
    CC_VIBRATO_DEPTH = 77
    CC_VIBRATO_DELAY = 78

class PitchBendEvent(BaseModel):
    """A pitch bend message."""

    value: int = Field(ge=0, le=16383, description="Pitch bend value (0-16383, 8192=center)")
    start_time: float = Field(ge=0, description="Time in seconds")
    channel: int = Field(default=0, ge=0, le=15)

class ProgramChangeEvent(BaseModel):
    """A program change event."""

    program: int = Field(ge=0, le=127, description="MIDI program number")
    time: float = Field(ge=0, description="Time in seconds")
    channel: int = Field(default=0, ge=0, le=15)

# ============================================================================
# Instrument and Part Models
# ============================================================================

class InstrumentPart(BaseModel):
    """A single instrument's part in the composition."""

    # Identification
    instrument_name: str
    instrument_family: InstrumentFamily
    midi_program: int | None = Field(default=None, ge=0, le=127)
    midi_channel: int = Field(ge=0, le=15)

    # Notation
    clef: Clef = Clef.TREBLE
    transposition: int = Field(default=0, description="Semitones to transpose (for transposing instruments)")

    # Events
    notes: list[Note] = Field(default_factory=list)
    keyswitches: list[KeyswitchEvent] = Field(default_factory=list)
    cc_events: list[CCEvent] = Field(default_factory=list)
    pitch_bends: list[PitchBendEvent] = Field(default_factory=list)
    program_changes: list[ProgramChangeEvent] = Field(default_factory=list)

    # Part metadata
    solo: bool = Field(default=False, description="Is this a solo part?")
    muted: bool = Field(default=False, description="Should this part be muted?")

    # Validation
    @field_validator("notes")
    def validate_notes(cls, notes):
        """Ensure notes are sorted by start time."""
        if notes:
            if notes != sorted(notes, key=lambda n: n.start_time):
                raise ValueError("Notes must be sorted by start_time")
        return notes

    def get_duration(self) -> float:
        """Get the total duration of this part."""
        if not self.notes:
            return 0.0
        return max(n.start_time + n.duration for n in self.notes)

# ============================================================================
# Structural Models
# ============================================================================

class SectionMarker(BaseModel):
    """A marker for musical sections (A, B, bridge, etc.)."""

    label: str
    time: float = Field(ge=0, description="Time in seconds")
    rehearsal_letter: str | None = Field(
        default=None,
        description="Rehearsal letter (A, B, C, etc.)"
    )

class TempoChange(BaseModel):
    """A tempo change event."""

    tempo_bpm: float = Field(gt=0, description="Tempo in beats per minute")
    time: float = Field(ge=0, description="Time in seconds")
    tempo_marking: TempoMarking | None = None

class TimeSignature(BaseModel):
    """A time signature."""

    numerator: int = Field(ge=1, description="Top number (beats per measure)")
    denominator: int = Field(
        ge=1,
        description="Bottom number (note value for one beat)"
    )

class TimeSignatureChange(BaseModel):
    """A time signature change event."""

    time_signature: TimeSignature
    time: float = Field(ge=0, description="Time in seconds")

class DynamicChange(BaseModel):
    """A dynamic marking change."""

    dynamic: DynamicMarking
    time: float = Field(ge=0, description="Time in seconds")
    ramp_duration: float | None = Field(
        default=None,
        description="Duration for crescendo/diminuendo"
    )

# ============================================================================
# Full Composition Model
# ============================================================================

class Composition(BaseModel):
    """A complete musical composition."""

    # Metadata
    title: str
    composer: str | None = Field(default="AI Composer", description="Composer name")
    description: str | None = Field(default=None, description="Description of the piece")

    # Style and Form
    style_period: StylePeriod | None = None
    musical_form: MusicalForm | None = None
    key_signature: str = Field(description="Key signature (e.g., 'C major', 'A minor')")

    # Tempo and Meter
    initial_tempo_bpm: float = Field(gt=0, description="Initial tempo in BPM")
    tempo_marking: TempoMarking | None = None
    time_signature: TimeSignature = Field(
        default=TimeSignature(numerator=4, denominator=4)
    )

    # Structural Events
    tempo_changes: list[TempoChange] = Field(default_factory=list)
    time_signature_changes: list[TimeSignatureChange] = Field(default_factory=list)
    section_markers: list[SectionMarker] = Field(default_factory=list)
    dynamic_changes: list[DynamicChange] = Field(default_factory=list)

    # Instrumentation
    parts: list[InstrumentPart]

    # Performance notes
    performance_notes: str | None = Field(
        default=None,
        description="Notes for performers/conductors"
    )

    # Computed properties
    @property
    def duration(self) -> float:
        """Get total duration of the composition."""
        if not self.parts:
            return 0.0
        return max(part.get_duration() for part in self.parts)

    @property
    def instrument_count(self) -> int:
        """Get number of instruments."""
        return len(self.parts)

    def get_parts_by_family(self, family: InstrumentFamily) -> list[InstrumentPart]:
        """Get all parts of a specific instrument family."""
        return [p for p in self.parts if p.instrument_family == family]

    def get_solo_parts(self) -> list[InstrumentPart]:
        """Get all solo parts."""
        return [p for p in self.parts if p.solo]

# ============================================================================
# Request Models
# ============================================================================

class CompositionRequest(BaseModel):
    """Request for AI composition generation."""

    # User input
    prompt: str = Field(description="Natural language description of desired music")

    # Constraints
    duration_seconds: float | None = Field(
        default=None,
        ge=10,
        le=600,
        description="Target duration in seconds"
    )
    key_signature: str | None = Field(
        default=None,
        description="Key signature (or let AI decide)"
    )

    # Style guidance
    style_period: StylePeriod | None = None
    musical_form: MusicalForm | None = None
    mood: str | None = None

    # Orchestration
    ensemble: str | None = Field(
        default=None,
        description="Ensemble preset (e.g., 'string_quartet', 'full_orchestra')"
    )
    instruments: list[str] | None = Field(
        default=None,
        description="Specific instruments to include"
    )

    # Output options
    output_format: Literal["midi", "wav", "mp3", "all"] = "midi"
    include_stems: bool = Field(
        default=False,
        description="Export individual instrument stems"
    )

class CompositionResponse(BaseModel):
    """Response from AI composition generation."""

    composition: Composition
    metadata: dict = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    validation_errors: list[str] = Field(default_factory=list)
```

---

## Usage Examples

### Creating a Simple Melody

```python
melody = InstrumentPart(
    instrument_name="Violin Solo",
    instrument_family=InstrumentFamily.STRINGS,
    midi_program=40,
    midi_channel=0,
    clef=Clef.TREBLE,
    notes=[
        Note(pitch=60, start_time=0.0, duration=1.0, velocity=90, articulation=ArticulationType.LEGATO),
        Note(pitch=62, start_time=1.0, duration=1.0, velocity=85, articulation=ArticulationType.LEGATO),
        Note(pitch=64, start_time=2.0, duration=1.0, velocity=80, articulation=ArticulationType.LEGATO),
        Note(pitch=65, start_time=3.0, duration=2.0, velocity=75, articulation=ArticulationType.LEGATO),
    ],
    keyswitches=[
        KeyswitchEvent(keyswitch=24, time=0.0, articulation=ArticulationType.LEGATO)
    ]
)

composition = Composition(
    title="Simple Melody",
    key_signature="C major",
    initial_tempo_bpm=120.0,
    tempo_marking=TempoMarking.ANDANTE,
    parts=[melody]
)
```

### Creating a Full Orchestral Composition

```python
from musicgen.ai_models import Composition, InstrumentPart, Note, SectionMarker

# Create orchestral composition
orchestra = Composition(
    title="Epic Fanfare",
    key_signature="C minor",
    initial_tempo_bpm=100.0,
    tempo_marking=TempoMarking.MAESTOSO,
    style_period=StylePeriod.FILM_SCORE,
    musical_form=MusicalForm.TERNARY,
    time_signature=TimeSignature(numerator=4, denominator=4),
    parts=[
        # Violin section
        InstrumentPart(...),
        # Cello section
        InstrumentPart(...),
        # Trumpet section
        InstrumentPart(...),
        # Timpani
        InstrumentPart(...),
    ],
    section_markers=[
        SectionMarker(label="A", time=0.0, rehearsal_letter="A"),
        SectionMarker(label="B", time=32.0, rehearsal_letter="B"),
        SectionMarker(label="A'", time=64.0, rehearsal_letter="C"),
    ],
    tempo_changes=[
        TempoChange(tempo_bpm=120.0, time=48.0, tempo_marking=TempoMarking.ACCELERANDO),
    ]
)
```

---

## Implementation Tasks

1. [ ] Create all Pydantic models in `src/musicgen/ai_models/`
2. [ ] Add JSON serialization for all models
3. [ ] Create model validation helpers
4. [ ] Add schema export to JSON for documentation
5. [ ] Create example compositions for testing
6. [ ] Add model versioning for backwards compatibility

## Success Criteria

- All models validate correctly
- Models can serialize to/from JSON
- Examples demonstrate proper usage
- Schema can be used for AI output validation

## Next Steps

- V3-07: Validation Tools for Music Theory Rules
- V3-08: Enhanced MIDI Generator
