"""
Genre profile definitions for music-gen-lib V4.

This module provides detailed genre profiles including typical instrumentation,
rhythmic patterns, chord progressions, and structural conventions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


@dataclass
class GenreProfile:
    """
    Profile defining the characteristics of a musical genre.

    Attributes:
        name: Genre name
        tempo_range: (min_bpm, max_bpm)
        time_signatures: Common time signatures
        instruments: Typical instrument set
        drum_patterns: Common drum pattern names
        bass_patterns: Common bass line patterns
        chord_progressions: Typical chord movements
        forms: Common musical forms
        articulation_preferences: Typical articulations
        dynamics: Dynamic range characteristics
    """

    name: str
    tempo_range: tuple[int, int]
    time_signatures: list[tuple[int, int]] = field(default_factory=lambda: [(4, 4)])
    instruments: dict[str, list[str]] = field(default_factory=dict)
    drum_patterns: list[str] = field(default_factory=list)
    bass_patterns: list[str] = field(default_factory=list)
    chord_progressions: list[list[str]] = field(default_factory=list)
    forms: list[str] = field(default_factory=list)
    articulation_preferences: dict[str, list[str]] = field(default_factory=dict)
    dynamics: dict[str, str] = field(default_factory=dict)


# =============================================================================
# Rock Genre
# =============================================================================

ROCK = GenreProfile(
    name="Rock",
    tempo_range=(100, 140),
    time_signatures=[(4, 4), (6, 8)],
    instruments={
        "rhythm": ["electric_guitar_clean", "electric_guitar_overdrive"],
        "lead": ["electric_guitar_distortion", "electric_guitar_overdrive"],
        "bass": ["electric_bass_pick", "electric_bass_finger"],
        "drums": ["drum_kit_rock"],
        "keyboards": ["electric_piano", "organ"],
    },
    drum_patterns=[
        "basic_rock",
        "hard_rock",
        "punk",
        "half_time",
        "double_time",
    ],
    bass_patterns=[
        "root_eighth",
        "root_fifth",
        "octave_jump",
        "syncopated",
    ],
    chord_progressions=[
        ["I", "IV", "V", "IV"],
        ["I", "V", "vi", "IV"],
        ["i", "III", "VII", "VI"],  # Minor rock
        ["I", "bVII", "IV", "bVII"],  # Blues rock
    ],
    forms=["verse_chorus", "bridge_solo", "intro_outro"],
    articulation_preferences={
        "guitar": ["distortion", "power_chord", "palm_mute", "bend"],
        "bass": ["pick", "finger", "slap"],
        "drums": ["accent", "crash", "ride"],
    },
    dynamics={
        "range": "wide",
        "pattern": "verse_quiet_chorus_loud",
        "accent": "strong_downbeat",
    },
)


# =============================================================================
# Pop Genre
# =============================================================================

POP = GenreProfile(
    name="Pop",
    tempo_range=(90, 130),
    time_signatures=[(4, 4)],
    instruments={
        "rhythm": ["acoustic_guitar_steel", "electric_guitar_clean", "piano"],
        "lead": ["electric_guitar_clean", "synth_lead", "vocals"],
        "bass": ["electric_bass_finger", "synth_bass"],
        "drums": ["drum_kit_pop", "electronic_drums"],
        "keyboards": ["piano", "electric_piano", "synth_pad"],
        "strings": ["string_section", "violin_section"],
    },
    drum_patterns=[
        "basic_pop",
        "disco",
        "funk",
        "dance_pop",
        "ballad",
    ],
    bass_patterns=[
        "root_eighth",
        "syncopated",
        "walking",
    ],
    chord_progressions=[
        ["I", "V", "vi", "IV"],  # The "pop punk" progression
        ["I", "vi", "IV", "V"],  # The '50s progression
        ["I", "V", "vi", "iii", "IV", "I", "IV", "V"],  # Pachelbel
        ["vi", "IV", "I", "V"],  # i–V–vi–IV variant
    ],
    forms=["verse_chorus", "pre_chorus", "bridge", "intro_outro"],
    articulation_preferences={
        "guitar": ["clean", "fingerstyle", "strum"],
        "bass": ["finger", "smooth"],
        "drums": ["steady", "backbeat"],
        "keys": ["pad", "comping"],
    },
    dynamics={
        "range": "medium",
        "pattern": "chorus_louder",
        "accent": "backbeat",
    },
)


# =============================================================================
# Jazz Genre
# =============================================================================

JAZZ = GenreProfile(
    name="Jazz",
    tempo_range=(80, 200),
    time_signatures=[(4, 4), (3, 4), (6, 8)],
    instruments={
        "rhythm": ["piano", "electric_guitar_jazz", "electric_guitar_clean"],
        "lead": ["trumpet", "saxophone", "trombone", "flute", "vibraphone"],
        "bass": ["acoustic_bass", "electric_bass_finger"],
        "drums": ["drum_kit_jazz"],
        "keyboards": ["piano", "electric_piano", "organ"],
    },
    drum_patterns=[
        "swing_basic",
        "swing_traditional",
        "swing_upbeat",
        "bossa_nova",
        "afro_cuban",
    ],
    bass_patterns=[
        "walking",
        "walking_half_time",
        "bossa",
        "two_feel",
    ],
    chord_progressions=[
        ["ii7", "V7", "I", "vi7"],  # ii-V-I-vi
        ["iii7", "vi7", "ii7", "V7"],  # iii-vi-ii-V (turnaround)
        ["I7", "IV7", "ii7", "V7"],  # Blues changes
        ["iim7", "V7", "Imaj7", "VImaj7"],  # Coltrane
    ],
    forms=["aaba", "blues_12_bar", "blues_32_bar", "through_composed"],
    articulation_preferences={
        "piano": ["comping", "voicing_3_7", "block_chords"],
        "guitar": [" Freddie Green style", "comping"],
        "bass": ["walking", "swing"],
        "drums": ["swing", "brushes", "ride"],
        "horns": ["bend", "growl", "flutter_tongue"],
    },
    dynamics={
        "range": "wide",
        "pattern": "improvisational",
        "accent": "off_beat_swing",
    },
)


# =============================================================================
# Classical Genre
# =============================================================================

CLASSICAL = GenreProfile(
    name="Classical",
    tempo_range=(40, 180),
    time_signatures=[(4, 4), (3, 4), (6, 8), (2, 4), (3, 8), (2, 2)],
    instruments={
        "strings": ["violin_section", "viola_section", "cello_section", "contrabass_section"],
        "woodwinds": ["flute", "oboe", "clarinet", "bassoon"],
        "brass": ["trumpet", "french_horn", "trombone", "tuba"],
        "percussion": ["timpani", "glockenspiel", "xylophone"],
        "keyboards": ["piano", "harpsichord"],
        "harp": ["orchestral_harp"],
    },
    drum_patterns=[],
    bass_patterns=[],
    chord_progressions=[
        ["I", "IV", "V", "I"],
        ["I", "vi", "ii", "V"],
        ["I", "IV", "vii°", "I"],
        ["I", "V", "vi", "iii", "IV", "I", "IV", "V"],
    ],
    forms=["sonata", "rondo", "theme_and_variations", "minuet_and_trio", "concerto"],
    articulation_preferences={
        "strings": ["legato", "staccato", "spiccato", "tremolo", "pizzicato", "vibrato"],
        "winds": ["legato", "staccato", "flutter_tongue"],
        "brass": ["legato", "staccato", "mute", "brilliant"],
        "percussion": ["roll", "damp"],
        "keyboards": ["legato", "staccato", "non_legato", "ornamented"],
    },
    dynamics={
        "range": "extreme",
        "pattern": "arched_phrased",
        "accent": "metric",
    },
)


# =============================================================================
# Electronic Genre
# =============================================================================

ELECTRONIC = GenreProfile(
    name="Electronic",
    tempo_range=(120, 180),
    time_signatures=[(4, 4)],
    instruments={
        "lead": ["synth_lead_square", "synth_lead_sawtooth", "synth_lead_voice"],
        "pad": ["synth_pad_warm", "synth_pad_new_age", "synth_pad_polysynth"],
        "bass": ["synth_bass_1", "synth_bass_2", "electric_bass_finger"],
        "drums": ["drum_machine_808", "drum_machine_909", "electronic_drums"],
        "fx": ["fx_rain", "fx_atmosphere", "fx_crystal"],
    },
    drum_patterns=[
        "four_on_floor",
        "trance",
        "dnb_amen",
        "hip_hop",
        "trap",
        "dubstep",
    ],
    bass_patterns=[
        "four_on_floor",
        "off_beat",
        "syncopated",
        "sub_bass",
    ],
    chord_progressions=[
        ["i", "VI", "iii", "VII"],  # Minor trance
        ["I", "V", "vi", "IV"],  # EDM pop
        ["i", "iv", "v", "v"],  # Minimal
        ["I", "III", "VI", "VII"],  # House
    ],
    forms=["building_arrangement", "dj_transition", "intro_drop"],
    articulation_preferences={
        "synth": ["portamento", "filter_sweep", "lfo_modulation", "arpeggio"],
        "bass": ["sub", "pluck", "sidechain"],
        "drums": ["four_on_floor", "snap", "clap"],
    },
    dynamics={
        "range": "compressed",
        "pattern": "building_breakdown",
        "accent": "four_on_floor",
    },
)


# =============================================================================
# World Genre
# =============================================================================

WORLD = GenreProfile(
    name="World",
    tempo_range=(60, 140),
    time_signatures=[(4, 4), (3, 4), (6, 8), (7, 8), (10, 8)],
    instruments={
        "indian": ["sitar", "tabla", "tanpura", "bansuri", "sarod"],
        "middle_eastern": ["oud", "ney", "darbuka", "kanun"],
        "east_asian": ["koto", "shakuhachi", "guzheng", "erhu", "taiko"],
        "latin": ["acoustic_guitar_nylon", "conga", "bongo", "timbale", "trumpet"],
        "african": ["djembe", "kora", "balafon", "talking_drum"],
        "celtic": ["fiddle", "tin_whistle", "bodhran", "acoustic_guitar_steel"],
    },
    drum_patterns=[
        "indian_tintal",
        "middle_eastern_baladi",
        "latin_clave",
        "afro_cuban",
        "west_african_polyrhythm",
    ],
    bass_patterns=[
        "indian_drone",
        "latin_tumbao",
        "arabic_maqsoum",
    ],
    chord_progressions=[
        ["I", "IV", "V", "I"],  # Universal
        ["i", "IV", "i", "V"],  # Minor
    ],
    forms=["raga", "maqam", "call_response", "cyclic"],
    articulation_preferences={
        "indian": ["meend", "gamak", "glissando"],
        "middle_eastern": ["mordent", "tremolo", "quarter_tone"],
        "east_asian": ["bend", "vibrato", "glissando"],
        "latin": ["syncopation", "montuno"],
    },
    dynamics={
        "range": "medium",
        "pattern": "regional_specific",
        "accent": "microtiming",
    },
)


# =============================================================================
# Genre Registry
# =============================================================================

GENRE_PROFILES: dict[str, GenreProfile] = {
    "rock": ROCK,
    "pop": POP,
    "jazz": JAZZ,
    "classical": CLASSICAL,
    "electronic": ELECTRONIC,
    "world": WORLD,
}


# =============================================================================
# Helper Functions
# =============================================================================


def get_genre_profile(name: str) -> GenreProfile | None:
    """Get a genre profile by name."""
    return GENRE_PROFILES.get(name.lower())


def get_all_genres() -> list[str]:
    """Get all available genre names."""
    return list(GENRE_PROFILES.keys())


def get_genres_by_tempo(bpm: int) -> list[str]:
    """Get genres compatible with a given tempo."""
    return [
        name
        for name, profile in GENRE_PROFILES.items()
        if profile.tempo_range[0] <= bpm <= profile.tempo_range[1]
    ]


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "GenreProfile",
    "GENRE_PROFILES",
    "ROCK",
    "POP",
    "JAZZ",
    "CLASSICAL",
    "ELECTRONIC",
    "WORLD",
    "get_genre_profile",
    "get_all_genres",
    "get_genres_by_tempo",
]
