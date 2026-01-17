"""
World instrument definitions for music-gen-lib V4.

This module provides definitions for world/ethnic instruments including
Indian, Middle Eastern, East Asian, and other traditional instruments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    pass

# =============================================================================
# World Instrument Base Classes
# =============================================================================


@dataclass
class MicrotonalNote:
    """
    For world instruments requiring microtones.

    Attributes:
        note_name: MIDI note name
        cents: Deviation in cents (-50 to +50)
        frequency_ratio: For just intonation ratios
    """

    note_name: str
    cents: int = 0
    frequency_ratio: float | None = None


@dataclass
class WorldInstrumentDefinition:
    """
    Extended instrument definition for world instruments.

    Attributes:
        name: Instrument name
        region: Geographic/cultural origin
        traditional_name: Name in native language
        midi_program: GM program number (if applicable)
        range: Playing range dict with min/max
        microtonal: Whether instrument uses microtones
        tuning_system: Type of tuning system
        microtone_divisions: Number of microtones per semitone
        techniques: Playing techniques specific to this instrument
        instrument_family: Hornbostel-Sachs classification
        sfz_file: SFZ definition file path
    """

    name: str
    region: str
    traditional_name: str | None = None
    midi_program: int | None = None
    range: dict[str, int] = field(default_factory=lambda: {"min": 48, "max": 84})
    microtonal: bool = False
    tuning_system: Literal["equal", "just", "meantone", "indian", "arabic", "other"] = "equal"
    microtone_divisions: int = 1
    techniques: dict[str, dict] = field(default_factory=dict)
    instrument_family: str = "chordophone"  # Hornbostel-Sachs
    sfz_file: str | None = None


# =============================================================================
# Indian Classical Instruments
# =============================================================================

INDIAN_INSTRUMENTS: dict[str, WorldInstrumentDefinition] = {
    "sitar": WorldInstrumentDefinition(
        name="Sitar",
        region="India",
        traditional_name="सितार",
        midi_program=104,  # GM Sitar
        range={"min": 48, "max": 96},
        microtonal=True,
        tuning_system="indian",
        microtone_divisions=2,  # Sruti (quarter tones)
        instrument_family="chordophone",
        techniques={
            "meend": {
                "description": "Gliding between notes",
                "midi_cc": None,
                "continuous": True,
            },
            "gamak": {
                "description": "Ornamental shake",
                "midi_cc": None,
                "continuous": False,
            },
            "krintan": {
                "description": "Pulling string across fret",
                "midi_cc": None,
                "continuous": False,
            },
            "jamjama": {
                "description": "Fast tremolo",
                "midi_cc": None,
                "continuous": True,
            },
        },
    ),
    "sarod": WorldInstrumentDefinition(
        name="Sarod",
        region="India",
        traditional_name="सरोद",
        midi_program=None,
        range={"min": 48, "max": 88},
        microtonal=True,
        tuning_system="indian",
        microtone_divisions=2,
        instrument_family="chordophone",
        techniques={
            "meend": {"description": "Gliding between notes"},
            "gamak": {"description": "Ornamental shake"},
            "bol": {"description": "Percussive strokes"},
        },
    ),
    "bansuri": WorldInstrumentDefinition(
        name="Bansuri",
        region="India",
        traditional_name="बांसुरी",
        midi_program=73,  # GM Flute (approximation)
        range={"min": 60, "max": 84},
        microtonal=False,
        tuning_system="just",
        instrument_family="aerophone",
        techniques={
            "meend": {"description": "Gliding between notes"},
            "gamak": {"description": "Ornamental shake"},
        },
    ),
    "tabla": WorldInstrumentDefinition(
        name="Tabla",
        region="India",
        traditional_name="तबला",
        midi_program=None,
        range={"min": 36, "max": 60},
        microtonal=False,
        tuning_system="just",
        instrument_family="membranophone",
        techniques={
            "bayan": {"description": "Bass drum stroke", "midi_note": 36},
            "dayan": {"description": "Treble drum stroke", "midi_note": 60},
            "ge": {"description": "Open stroke", "midi_note": 38},
            "ke": {"description": "Closed stroke", "midi_note": 40},
            "tun": {"description": "Rim stroke", "midi_note": 42},
        },
    ),
    "mridangam": WorldInstrumentDefinition(
        name="Mridangam",
        region="India",
        traditional_name="मृदंग",
        midi_program=None,
        range={"min": 36, "max": 60},
        microtonal=False,
        tuning_system="just",
        instrument_family="membranophone",
        techniques={
            "thom": {"description": "Bass stroke"},
            "nam": {"description": "Open stroke"},
            "din": {"description": "Closed stroke"},
        },
    ),
    "tanpura": WorldInstrumentDefinition(
        name="Tanpura",
        region="India",
        traditional_name="तानपूरा",
        midi_program=None,
        range={"min": 36, "max": 60},
        microtonal=True,
        tuning_system="just",
        instrument_family="chordophone",
        techniques={"drone": {"description": "Sustained drone"}},
    ),
    "santoor": WorldInstrumentDefinition(
        name="Santoor",
        region="India/Kashmir",
        traditional_name="संतूर",
        midi_program=None,
        range={"min": 48, "max": 84},
        microtonal=False,
        tuning_system="just",
        instrument_family="chordophone",
        techniques={"glissando": {"description": "Gliding across strings"}},
    ),
}


# =============================================================================
# Middle Eastern Instruments
# =============================================================================

MIDDLE_EASTERN_INSTRUMENTS: dict[str, WorldInstrumentDefinition] = {
    "oud": WorldInstrumentDefinition(
        name="Oud",
        region="Middle East/North Africa",
        traditional_name="عود",
        midi_program=24,  # GM Acoustic Guitar (approximation)
        range={"min": 40, "max": 76},
        microtonal=True,
        tuning_system="arabic",
        microtone_divisions=2,  # Quarter tones
        instrument_family="chordophone",
        techniques={
            "mordent": {"description": "Rapid alternation"},
            "tremolo": {"description": "Rapid repetition"},
            "glissando": {"description": "Slide between notes"},
        },
    ),
    "ney": WorldInstrumentDefinition(
        name="Ney",
        region="Middle East",
        traditional_name="ناي",
        midi_program=73,  # GM Flute (approximation)
        range={"min": 60, "max": 84},
        microtonal=True,
        tuning_system="arabic",
        microtone_divisions=2,
        instrument_family="aerophone",
        techniques={
            "breath": {"description": "Breath accents"},
            "glissando": {"description": "Slide between notes"},
        },
    ),
    "darbuka": WorldInstrumentDefinition(
        name="Darbuka",
        region="Middle East/North Africa",
        traditional_name="دربكة",
        midi_program=None,
        range={"min": 36, "max": 60},
        microtonal=False,
        tuning_system="just",
        instrument_family="membranophone",
        techniques={
            "doum": {"description": "Bass center stroke", "midi_note": 36},
            "tek": {"description": "Rim stroke", "midi_note": 40},
            "ka": {"description": "Closed rim stroke", "midi_note": 42},
        },
    ),
    "kanun": WorldInstrumentDefinition(
        name="Kanun",
        region="Middle East",
        traditional_name="قانون",
        midi_program=14,  # GM Dulcimer/Tubular Bells
        range={"min": 48, "max": 84},
        microtonal=True,
        tuning_system="arabic",
        microtone_divisions=2,
        instrument_family="chordophone",
        techniques={
            "tremolo": {"description": "Rapid repetition"},
            "glissando": {"description": "Slide across strings"},
        },
    ),
    "buq": WorldInstrumentDefinition(
        name="Buq",
        region="Middle East",
        traditional_name="بوق",
        midi_program=56,  # GM Trumpet (approximation)
        range={"min": 48, "max": 72},
        microtonal=True,
        tuning_system="arabic",
        microtone_divisions=2,
        instrument_family="aerophone",
        techniques={
            "fall": {"description": "Pitch fall at end"},
            "shake": {"description": "Lip trill"},
        },
    ),
    "riq": WorldInstrumentDefinition(
        name="Riq",
        region="Middle East",
        traditional_name="رق",
        midi_program=None,
        range={"min": 60, "max": 72},
        microtonal=False,
        tuning_system="just",
        instrument_family="membranophone",
        techniques={
            "shake": {"description": "Jingle shake"},
            "hit": {"description": "Frame hit"},
        },
    ),
    "daf": WorldInstrumentDefinition(
        name="Daf",
        region="Iran/Kurdistan",
        traditional_name="دف",
        midi_program=None,
        range={"min": 36, "max": 60},
        microtonal=False,
        tuning_system="just",
        instrument_family="membranophone",
        techniques={
            "hit": {"description": "Frame hit"},
            "snap": {"description": "Snap on rings"},
        },
    ),
}


# =============================================================================
# East Asian Instruments
# =============================================================================

EAST_ASIAN_INSTRUMENTS: dict[str, WorldInstrumentDefinition] = {
    "koto": WorldInstrumentDefinition(
        name="Koto",
        region="Japan",
        traditional_name="箏",
        midi_program=107,  # GM Koto
        range={"min": 48, "max": 84},
        microtonal=False,
        tuning_system="just",
        instrument_family="chordophone",
        techniques={
            "atoshi": {"description": "Pressing string for bend"},
            "suriae": {"description": "Sliding pitch"},
            "shan": {"description": "Tremolo"},
        },
    ),
    "shakuhachi": WorldInstrumentDefinition(
        name="Shakuhachi",
        region="Japan",
        traditional_name="尺八",
        midi_program=77,  # GM Shakuhachi
        range={"min": 60, "max": 84},
        microtonal=True,
        tuning_system="just",
        microtone_divisions=2,
        instrument_family="aerophone",
        techniques={
            "meri": {"description": "Head lowering (pitch bend down)"},
            "kari": {"description": "Head raising (pitch bend up)"},
            "muraiki": {"description": "Vibrato with head movement"},
        },
    ),
    "guzheng": WorldInstrumentDefinition(
        name="Guzheng",
        region="China",
        traditional_name="古筝",
        midi_program=107,  # GM Koto (approximation)
        range={"min": 48, "max": 84},
        microtonal=False,
        tuning_system="just",
        instrument_family="chordophone",
        techniques={
            "bend": {"description": "String bend with left hand"},
            "glissando": {"description": "Slide across strings"},
            "tremolo": {"description": "Rapid plucking"},
        },
    ),
    "erhu": WorldInstrumentDefinition(
        name="Erhu",
        region="China",
        traditional_name="二胡",
        midi_program=40,  # GM Violin (approximation)
        range={"min": 55, "max": 88},
        microtonal=True,
        tuning_system="just",
        microtone_divisions=2,
        instrument_family="chordophone",
        techniques={
            "vibrato": {"description": "Finger vibrato"},
            "glissando": {"description": "Slide between notes"},
            "portamento": {"description": "Expressive slide"},
        },
    ),
    "dizi": WorldInstrumentDefinition(
        name="Dizi",
        region="China",
        traditional_name="笛子",
        midi_program=73,  # GM Flute (approximation)
        range={"min": 60, "max": 84},
        microtonal=False,
        tuning_system="just",
        instrument_family="aerophone",
        techniques={
            "trill": {"description": "Finger trill"},
            "flutter": {"description": "Tongue flutter"},
        },
    ),
    "gayageum": WorldInstrumentDefinition(
        name="Gayageum",
        region="Korea",
        traditional_name="가야금",
        midi_program=107,  # GM Koto (approximation)
        range={"min": 48, "max": 84},
        microtonal=False,
        tuning_system="just",
        instrument_family="chordophone",
        techniques={
            "bend": {"description": "String bend"},
            "vibrato": {"description": "String vibration"},
            "glissando": {"description": "Slide across strings"},
        },
    ),
    "taiko": WorldInstrumentDefinition(
        name="Taiko",
        region="Japan",
        traditional_name="太鼓",
        midi_program=116,  # GM Taiko Drum
        range={"min": 36, "max": 48},
        microtonal=False,
        tuning_system="just",
        instrument_family="membranophone",
        techniques={
            "center": {"description": "Center hit"},
            "rim": {"description": "Rim hit"},
            "bounce": {"description": "Bounce stroke"},
        },
    ),
}


# =============================================================================
# Other World Instruments
# =============================================================================

OTHER_WORLD_INSTRUMENTS: dict[str, WorldInstrumentDefinition] = {
    "bagpipe": WorldInstrumentDefinition(
        name="Bagpipe",
        region="Scotland/Ireland",
        traditional_name="Pìob Mhòr",
        midi_program=109,  # GM Bagpipe
        range={"min": 48, "max": 72},
        microtonal=False,
        tuning_system="just",
        instrument_family="aerophone",
        techniques={
            "grace": {"description": "Grace note"},
            "doubling": {"description": "Double grace note"},
        },
    ),
    "tin_whistle": WorldInstrumentDefinition(
        name="Tin Whistle",
        region="Ireland",
        traditional_name="Feadóg Stáin",
        midi_program=74,  # GM Pan Flute/Recorder
        range={"min": 60, "max": 84},
        microtonal=False,
        tuning_system="just",
        instrument_family="aerophone",
        techniques={
            "cut": {"description": "Grace note from above"},
            "strike": {"description": "Grace note from below"},
            "roll": {"description": "Cut + strike"},
        },
    ),
    "uilleann_pipes": WorldInstrumentDefinition(
        name="Uilleann Pipes",
        region="Ireland",
        traditional_name="Píobaí Uilleann",
        midi_program=109,  # GM Bagpipe (approximation)
        range={"min": 48, "max": 72},
        microtonal=True,
        tuning_system="just",
        microtone_divisions=2,
        instrument_family="aerophone",
        techniques={
            "grace": {"description": "Grace note"},
            "regulator": {"description": "Chordal accompaniment"},
        },
    ),
    "accordion": WorldInstrumentDefinition(
        name="Accordion",
        region="Europe",
        traditional_name="Akkordeon",
        midi_program=21,  # GM Accordion
        range={"min": 48, "max": 84},
        microtonal=False,
        tuning_system="equal",
        instrument_family="aerophone",
        techniques={
            "bellows": {"description": "Bellows expression"},
            "tremolo": {"description": "Reed tremolo"},
        },
    ),
    "bandoneon": WorldInstrumentDefinition(
        name="Bandoneon",
        region="Argentina/Uruguay",
        traditional_name="Bandoneón",
        midi_program=23,  # GM Tango Accordion
        range={"min": 48, "max": 84},
        microtonal=False,
        tuning_system="equal",
        instrument_family="aerophone",
        techniques={
            "bellows": {"description": "Bellows expression"},
            "bellow_shake": {"description": "Rapid bellows movement"},
        },
    ),
    "djembe": WorldInstrumentDefinition(
        name="Djembe",
        region="West Africa",
        traditional_name="Jembe",
        midi_program=None,
        range={"min": 36, "max": 60},
        microtonal=False,
        tuning_system="just",
        instrument_family="membranophone",
        techniques={
            "bass": {"description": "Center hit", "midi_note": 36},
            "tone": {"description": "Edge hit", "midi_note": 40},
            "slap": {"description": "Slap hit", "midi_note": 42},
        },
    ),
    "conga": WorldInstrumentDefinition(
        name="Conga",
        region="Cuba",
        traditional_name="Conga",
        midi_program=64,  # GM (in drum map)
        range={"min": 36, "max": 60},
        microtonal=False,
        tuning_system="just",
        instrument_family="membranophone",
        techniques={
            "open": {"description": "Open tone", "midi_note": 63},
            "closed": {"description": "Closed tone", "midi_note": 62},
            "slap": {"description": "Slap tone", "midi_note": 64},
        },
    ),
    "bongo": WorldInstrumentDefinition(
        name="Bongo",
        region="Cuba",
        traditional_name="Bongó",
        midi_program=None,  # Percussion uses channel 10
        range={"min": 48, "max": 60},
        microtonal=False,
        tuning_system="just",
        instrument_family="membranophone",
        techniques={
            "hembra": {"description": "Large drum", "midi_note": 61},
            "macho": {"description": "Small drum", "midi_note": 60},
        },
    ),
    "steel_drum": WorldInstrumentDefinition(
        name="Steel Drum",
        region="Trinidad & Tobago",
        traditional_name="Steelpan",
        midi_program=114,  # GM Steel Drums
        range={"min": 48, "max": 84},
        microtonal=False,
        tuning_system="just",
        instrument_family="idiophone",
        techniques={
            "strike": {"description": "Normal strike"},
            "damp": {"description": "Damped strike"},
        },
    ),
}


# =============================================================================
# Combined Library
# =============================================================================

WORLD_INSTRUMENTS: dict[str, WorldInstrumentDefinition] = {
    **INDIAN_INSTRUMENTS,
    **MIDDLE_EASTERN_INSTRUMENTS,
    **EAST_ASIAN_INSTRUMENTS,
    **OTHER_WORLD_INSTRUMENTS,
}


# =============================================================================
# Helper Functions
# =============================================================================


def get_world_instrument(name: str) -> WorldInstrumentDefinition | None:
    """Get a world instrument definition by name."""
    return WORLD_INSTRUMENTS.get(name.lower())


def get_instruments_by_region(region: str) -> dict[str, WorldInstrumentDefinition]:
    """Get all instruments from a specific region."""
    return {k: v for k, v in WORLD_INSTRUMENTS.items() if region.lower() in v.region.lower()}


def get_microtonal_instruments() -> dict[str, WorldInstrumentDefinition]:
    """Get all microtonal instruments."""
    return {k: v for k, v in WORLD_INSTRUMENTS.items() if v.microtonal}


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Classes
    "WorldInstrumentDefinition",
    "MicrotonalNote",
    # Instrument collections
    "WORLD_INSTRUMENTS",
    "INDIAN_INSTRUMENTS",
    "MIDDLE_EASTERN_INSTRUMENTS",
    "EAST_ASIAN_INSTRUMENTS",
    "OTHER_WORLD_INSTRUMENTS",
    # Helpers
    "get_world_instrument",
    "get_instruments_by_region",
    "get_microtonal_instruments",
]
