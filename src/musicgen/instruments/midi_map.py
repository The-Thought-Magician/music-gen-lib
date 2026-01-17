"""
MIDI program number mappings for General MIDI (GM), GM2, and GS standards.

This module provides complete mappings of MIDI program numbers (0-127)
and drum key numbers for instrument selection.
"""

from enum import IntEnum
from typing import Final

# =============================================================================
# General MIDI Program Numbers (0-127)
# =============================================================================


class GMProgram(IntEnum):
    """General MIDI Program Numbers (0-127)."""

    # Piano Family (0-7)
    ACOUSTIC_GRAND = 0
    BRIGHT_ACOUSTIC = 1
    ELECTRIC_GRAND = 2
    HONKY_TONK = 3
    ELECTRIC_PIANO_1 = 4
    ELECTRIC_PIANO_2 = 5
    HARPSICHORD = 6
    CLAVINET = 7

    # Chromatic Percussion (8-15)
    CELESTA = 8
    GLOCKENSPIEL = 9
    MUSIC_BOX = 10
    VIBRAPHONE = 11
    MARIMBA = 12
    XYLOPHONE = 13
    TUBULAR_BELLS = 14
    DULCIMER = 15

    # Organ Family (16-23)
    DRAWBAR_ORGAN = 16
    PERCUSSIVE_ORGAN = 17
    ROCK_ORGAN = 18
    CHURCH_ORGAN = 19
    REED_ORGAN = 20
    ACCORDION = 21
    HARMONICA = 22
    TANGO_ACCORDION = 23

    # Guitar Family (24-31)
    ACOUSTIC_GUITAR_NYLON = 24
    ACOUSTIC_GUITAR_STEEL = 25
    ELECTRIC_GUITAR_JAZZ = 26
    ELECTRIC_GUITAR_CLEAN = 27
    ELECTRIC_GUITAR_MUTED = 28
    OVERDRIVEN_GUITAR = 29
    DISTORTION_GUITAR = 30
    GUITAR_HARMONICS = 31

    # Bass Family (32-39)
    ACOUSTIC_BASS = 32
    ELECTRIC_BASS_FINGER = 33
    ELECTRIC_BASS_PICK = 34
    FRETLESS_BASS = 35
    SLAP_BASS_1 = 36
    SLAP_BASS_2 = 37
    SYNTH_BASS_1 = 38
    SYNTH_BASS_2 = 39

    # Strings Family (40-47)
    VIOLIN_SECTION = 40
    VIOLA_SECTION = 41
    CELLO_SECTION = 42
    CONTRABASS_SECTION = 43
    TREMOLO_STRINGS = 44
    PIZZICATO_STRINGS = 45
    ORCHESTRAL_HARP = 46
    TIMPANI = 47

    # Ensemble Family (48-55)
    STRING_ENSEMBLE_1 = 48
    STRING_ENSEMBLE_2 = 49
    SYNTH_STRINGS_1 = 50
    SYNTH_STRINGS_2 = 51
    CHOIR_AAHS = 52
    VOICE_OOHS = 53
    SYNTH_CHOIR = 54
    ORCHESTRA_HIT = 55

    # Brass Family (56-63)
    TRUMPET = 56
    TROMBONE = 57
    TUBA = 58
    MUTED_TRUMPET = 59
    FRENCH_HORN = 60
    BRASS_SECTION = 61
    SYNTH_BRASS_1 = 62
    SYNTH_BRASS_2 = 63

    # Reed Family (64-71)
    SOPRANO_SAX = 64
    ALTO_SAX = 65
    TENOR_SAX = 66
    BARITONE_SAX = 67
    OBOE = 68
    ENGLISH_HORN = 69
    BASSOON = 70
    CLARINET = 71

    # Pipe Family (72-79)
    PICCOLO = 72
    FLUTE = 73
    RECORDER = 74
    PAN_FLUTE = 75
    BLOWN_BOTTLE = 76
    SHAKUHACHI = 77
    WHISTLE = 78
    OCARINA = 79

    # Synth Lead Family (80-87)
    LEAD_1_SQUARE = 80
    LEAD_2_SAWTOOTH = 81
    LEAD_3_CALLIOPE = 82
    LEAD_4_CHIFF = 83
    LEAD_5_CHARANG = 84
    LEAD_6_VOICE = 85
    LEAD_7_FIFTHS = 86
    LEAD_8_BASS_PLUS_LEAD = 87

    # Synth Pad Family (88-95)
    PAD_1_NEW_AGE = 88
    PAD_2_WARM = 89
    PAD_3_POLYSYNTH = 90
    PAD_4_CHOIR = 91
    PAD_5_BOWED = 92
    PAD_6_METALLIC = 93
    PAD_7_HALO = 94
    PAD_8_SWEEP = 95

    # Synth Effects Family (96-103)
    FX_1_RAIN = 96
    FX_2_SOUNDTRACK = 97
    FX_3_CRYSTAL = 98
    FX_4_ATMOSPHERE = 99
    FX_5_BRIGHTNESS = 100
    FX_6_GOBLINS = 101
    FX_7_ECHOES = 102
    FX_8_SCI_FI = 103

    # World/Ethnic Instruments (104-111)
    SITAR = 104
    BANJO = 105
    SHAMISEN = 106
    KOTO = 107
    KALIMBA = 108
    BAGPIPE = 109
    FIDDLE = 110
    SHANAI = 111

    # Percussive Family (112-119)
    TINKLE_BELL = 112
    AGOGO = 113
    STEEL_DRUMS = 114
    WOODBLOCK = 115
    TAIKO_DRUM = 116
    MELODIC_TOM = 117
    SYNTH_DRUM = 118
    REVERSE_CYMBAL = 119

    # Sound Effects (120-127)
    GUITAR_FRET_NOISE = 120
    BREATH_NOISE = 121
    SEASHORE = 122
    BIRD_TWEET = 123
    TELEPHONE_RING = 124
    HELICOPTER = 125
    APPLAUSE = 126
    GUNSHOT = 127


class GMKey(IntEnum):
    """GM Drum Key Numbers (Channel 10)."""

    # Kick drums (35-36)
    ACOUSTIC_BASS_DRUM = 35
    BASS_DRUM_1 = 36

    # Snare (37-40)
    SIDE_STICK = 37
    ACOUSTIC_SNARE = 38
    HAND_CLAP = 39
    ELECTRIC_SNARE = 40

    # Toms (41-43, 45, 47-50)
    LOW_FLOOR_TOM = 41
    CLOSED_HI_HAT = 42  # Also hi-hat
    HIGH_FLOOR_TOM = 43
    PEDAL_HI_HAT = 44
    LOW_TOM = 45
    OPEN_HI_HAT = 46
    LOW_MID_TOM = 47
    HI_MID_TOM = 48

    # Cymbals (49-52, 55, 57, 59)
    CRASH_CYMBAL_1 = 49
    HIGH_TOM = 50
    RIDE_CYMBAL_1 = 51
    CHINESE_CYMBAL = 52
    RIDE_BELL = 53
    TAMBOURINE = 54
    SPLASH_CYMBAL = 55
    COWBELL = 56
    CRASH_CYMBAL_2 = 57
    VIBRASLAP = 58
    RIDE_CYMBAL_2 = 59

    # Percussion (60-81)
    HI_BONGO = 60
    LOW_BONGO = 61
    MUTE_HI_CONGA = 62
    OPEN_HI_CONGA = 63
    LOW_CONGA = 64
    HIGH_TIMBALE = 65
    LOW_TIMBALE = 66
    HIGH_AGOGO = 67
    LOW_AGOGO = 68
    CABASA = 69
    MARACAS = 70
    SHORT_WHISTLE = 71
    LONG_WHISTLE = 72
    SHORT_GUIRO = 73
    LONG_GUIRO = 74
    CLAVES = 75
    HI_WOOD_BLOCK = 76
    LOW_WOOD_BLOCK = 77
    MUTE_CUICA = 78
    OPEN_CUICA = 79
    MUTE_TRIANGLE = 80
    OPEN_TRIANGLE = 81


# =============================================================================
# Program Name Mappings
# =============================================================================

GM_PROGRAM_NAMES: Final[dict[int, str]] = {
    0: "acoustic_grand_piano",
    1: "bright_acoustic_piano",
    2: "electric_grand_piano",
    3: "honky_tonk_piano",
    4: "electric_piano_1",
    5: "electric_piano_2",
    6: "harpsichord",
    7: "clavinet",
    8: "celesta",
    9: "glockenspiel",
    10: "music_box",
    11: "vibraphone",
    12: "marimba",
    13: "xylophone",
    14: "tubular_bells",
    15: "dulcimer",
    16: "drawbar_organ",
    17: "percussive_organ",
    18: "rock_organ",
    19: "church_organ",
    20: "reed_organ",
    21: "accordion",
    22: "harmonica",
    23: "tango_accordion",
    24: "acoustic_guitar_nylon",
    25: "acoustic_guitar_steel",
    26: "electric_guitar_jazz",
    27: "electric_guitar_clean",
    28: "electric_guitar_muted",
    29: "overdriven_guitar",
    30: "distortion_guitar",
    31: "guitar_harmonics",
    32: "acoustic_bass",
    33: "electric_bass_finger",
    34: "electric_bass_pick",
    35: "fretless_bass",
    36: "slap_bass_1",
    37: "slap_bass_2",
    38: "synth_bass_1",
    39: "synth_bass_2",
    40: "violin_section",
    41: "viola_section",
    42: "cello_section",
    43: "contrabass_section",
    44: "tremolo_strings",
    45: "pizzicato_strings",
    46: "orchestral_harp",
    47: "timpani",
    48: "string_ensemble_1",
    49: "string_ensemble_2",
    50: "synth_strings_1",
    51: "synth_strings_2",
    52: "choir_aahs",
    53: "voice_oohs",
    54: "synth_choir",
    55: "orchestra_hit",
    56: "trumpet",
    57: "trombone",
    58: "tuba",
    59: "muted_trumpet",
    60: "french_horn",
    61: "brass_section",
    62: "synth_brass_1",
    63: "synth_brass_2",
    64: "soprano_sax",
    65: "alto_sax",
    66: "tenor_sax",
    67: "baritone_sax",
    68: "oboe",
    69: "english_horn",
    70: "bassoon",
    71: "clarinet",
    72: "piccolo",
    73: "flute",
    74: "recorder",
    75: "pan_flute",
    76: "blown_bottle",
    77: "shakuhachi",
    78: "whistle",
    79: "ocarina",
    80: "lead_1_square",
    81: "lead_2_sawtooth",
    82: "lead_3_calliope",
    83: "lead_4_chiff",
    84: "lead_5_charang",
    85: "lead_6_voice",
    86: "lead_7_fifths",
    87: "lead_8_bass_plus_lead",
    88: "pad_1_new_age",
    89: "pad_2_warm",
    90: "pad_3_polysynth",
    91: "pad_4_choir",
    92: "pad_5_bowed",
    93: "pad_6_metallic",
    94: "pad_7_halo",
    95: "pad_8_sweep",
    96: "fx_1_rain",
    97: "fx_2_soundtrack",
    98: "fx_3_crystal",
    99: "fx_4_atmosphere",
    100: "fx_5_brightness",
    101: "fx_6_goblins",
    102: "fx_7_echoes",
    103: "fx_8_sci_fi",
    104: "sitar",
    105: "banjo",
    106: "shamisen",
    107: "koto",
    108: "kalimba",
    109: "bagpipe",
    110: "fiddle",
    111: "shanai",
    112: "tinkle_bell",
    113: "agogo",
    114: "steel_drums",
    115: "woodblock",
    116: "taiko_drum",
    117: "melodic_tom",
    118: "synth_drum",
    119: "reverse_cymbal",
    120: "guitar_fret_noise",
    121: "breath_noise",
    122: "seashore",
    123: "bird_tweet",
    124: "telephone_ring",
    125: "helicopter",
    126: "applause",
    127: "gunshot",
}


# =============================================================================
# Drum Key Mappings
# =============================================================================

GM_DRUM_NAMES: Final[dict[int, str]] = {
    35: "acoustic_bass_drum",
    36: "kick",
    37: "side_stick",
    38: "snare",
    39: "hand_clap",
    40: "electric_snare",
    41: "low_floor_tom",
    42: "hihat_closed",
    43: "high_floor_tom",
    44: "hihat_pedal",
    45: "low_tom",
    46: "hihat_open",
    47: "low_mid_tom",
    48: "hi_mid_tom",
    49: "crash_1",
    50: "high_tom",
    51: "ride_1",
    52: "crash_chinese",
    53: "ride_bell",
    54: "tambourine",
    55: "splash",
    56: "cowbell",
    57: "crash_2",
    58: "vibraslap",
    59: "ride_2",
    60: "bongo_hi",
    61: "bongo_lo",
    62: "conga_hi_muted",
    63: "conga_hi_open",
    64: "conga_lo",
    65: "timbale_hi",
    66: "timbale_lo",
    67: "agogo_hi",
    68: "agogo_lo",
    69: "cabasa",
    70: "maracas",
    71: "whistle_short",
    72: "whistle_long",
    73: "guiro_short",
    74: "guiro_long",
    75: "claves",
    76: "woodblock_hi",
    77: "woodblock_lo",
    78: "cuica_muted",
    79: "cuica_open",
    80: "triangle_muted",
    81: "triangle_open",
}


# =============================================================================
# Reverse Lookups
# =============================================================================

PROGRAM_TO_NUMBER: Final[dict[str, int]] = {v: k for k, v in GM_PROGRAM_NAMES.items()}

DRUM_TO_NUMBER: Final[dict[str, int]] = {v: k for k, v in GM_DRUM_NAMES.items()}


# =============================================================================
# Helper Functions
# =============================================================================


def get_program_number(name: str) -> int | None:
    """Get MIDI program number from instrument name."""
    return PROGRAM_TO_NUMBER.get(name.lower().replace(" ", "_").replace("-", "_"))


def get_program_name(number: int) -> str | None:
    """Get instrument name from MIDI program number."""
    return GM_PROGRAM_NAMES.get(number)


def get_drum_key(name: str) -> int | None:
    """Get MIDI key number from drum name."""
    return DRUM_TO_NUMBER.get(name.lower().replace(" ", "_").replace("-", "_"))


def get_drum_name(key: int) -> str | None:
    """Get drum name from MIDI key number."""
    return GM_DRUM_NAMES.get(key)


def is_guitar_program(program: int) -> bool:
    """Check if program is in the guitar family (24-31)."""
    return 24 <= program <= 31


def is_bass_program(program: int) -> bool:
    """Check if program is in the bass family (32-39)."""
    return 32 <= program <= 39


def is_drum_program(program: int) -> bool:
    """Check if program is in the drum family (usually channel 10)."""
    return program == 0  # Or use channel check


def is_world_program(program: int) -> bool:
    """Check if program is in the world/ethnic family (104-111)."""
    return 104 <= program <= 111


def is_synth_program(program: int) -> bool:
    """Check if program is a synthesizer (80-103)."""
    return 80 <= program <= 103
