"""
Arabic maqam scale definitions for music-gen-lib V4.

This module provides scale definitions for Arabic maqamat, including
quarter-tone intervals and ajnas (scale fragments).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


# =============================================================================
# Arabic Maqam Scale Classes
# =============================================================================


@dataclass
class MaqamScale:
    """
    Arabic maqam scale definition.

    Attributes:
        name: Maqam name (English transliteration)
        name_arabic: Maqam name in Arabic script
        family: Maqam family (based on lower jins)
        ajnas: List of ajnas (scale fragments) that make up the maqam
        ascending: Ascending scale in semitones from tonic (with quarter-tones)
        descending: Descending scale in semitones from tonic
        tonic: Starting note
        dominant: Secondary important note (usually 5th)
        ghammaz: Note where modulation occurs
        sayr: Melodic progression pattern
        mood: Emotional mood
    """

    name: str
    name_arabic: str
    family: str
    ajnas: list[str]
    ascending: list[float]  # Quarter-tones represented as .5 values
    descending: list[float]
    tonic: str = "C"
    dominant: str = "G"
    ghammaz: str = ""
    sayr: str = ""
    mood: str = ""


# =============================================================================
# Ajnas (Scale Fragments)
# =============================================================================

# The core ajnas that build maqamat
AJNAS_RAST = [0, 2, 4, 5, 7]  # C D E F G (major 3rd, minor 7th from bottom)
AJNAS_BAYATI = [0, 1.5, 3, 5, 7]  # C Db Eb F G (2nd and 3rd quarter-flat)
AJNAS_SIKAH = [0, 1.5, 3, 6, 7]  # C Db E+ F# G
AJNAS_HIJAZ = [0, 1, 4, 5, 7]  # C Db E F G (augmented 2nd)
AJNAS_SABA = [0, 1, 3, 4, 6]  # C Db Eb E F# (unusual)
AJNAS_KURD = [0, 1, 4, 5, 7]  # C Db E F G (similar to Hijaz but different intervals)
AJNAS_NAHAWAND = [0, 2, 4, 5, 7]  # C D E F G (minor scale)
AJNAS_AJAM = [0, 2, 4, 5, 7]  # C D E F G (major scale)


# =============================================================================
# Common Maqamat
# =============================================================================

# Maqam Rast - "the straight" - very common
MAQAM_RAST = MaqamScale(
    name="Rast",
    name_arabic="راست",
    family="Rast",
    ajnas=["Rast", "Rast"],
    ascending=[0, 2, 3.5, 5, 7, 9, 10.5, 12],  # C D E-half-flat F G A B-half-flat C
    descending=[12, 10.5, 9, 7, 5, 3.5, 2, 0],
    tonic="C",
    dominant="G",
    ghammaz="G",
    sayr="Ascending and descending emphasize half-flat 3rd and 7th",
    mood="Noble, proud, masculine",
)

# Maqam Bayati - very common
MAQAM_BAYATI = MaqamScale(
    name="Bayati",
    name_arabic="بياتي",
    family="Bayati",
    ajnas=["Bayati", "Nahawand"],
    ascending=[0, 1.5, 3, 5, 7, 8, 10, 12],  # C D-half-flat Eb F G Ab Bb C
    descending=[12, 10, 8, 7, 5, 3, 1.5, 0],
    tonic="D",
    dominant="A",
    ghammaz="D",
    sayr="Emphasis on half-flat 2nd",
    mood="Popular, folk-like, feminine",
)

# Maqam Sikah - unusual starting on quarter tone
MAQAM_SIKAH = MaqamScale(
    name="Sikah",
    name_arabic="سيكاه",
    family="Sikah",
    ajnas=["Sikah", "Rast"],
    ascending=[0, 1.5, 3, 4.5, 6, 7, 9, 10.5, 12],  # C-half-flat D E F-half-flat...
    descending=[12, 10.5, 9, 7, 6, 4.5, 3, 1.5, 0],
    tonic="E-half-flat",
    dominant="B-half-flat",
    ghammaz="E-half-flat",
    sayr="Begins and emphasizes quarter tone",
    mood="Emotional, melancholic",
)

# Maqam Hijaz - the "Spanish" sound
MAQAM_HIJAZ = MaqamScale(
    name="Hijaz",
    name_arabic="حجاز",
    family="Hijaz",
    ajnas=["Hijaz", "Rast"],
    ascending=[0, 1, 4, 5, 7, 9, 10.5, 12],  # C Db E F G A B-half-flat C
    descending=[12, 10.5, 9, 7, 5, 4, 1, 0],
    tonic="D",
    dominant="A",
    ghammaz="D",
    sayr="Emphasizes augmented 2nd (Db-E)",
    mood="Deep, serious, desert-like",
)

# Maqam Saba - melancholic
MAQAM_SABA = MaqamScale(
    name="Saba",
    name_arabic="صبا",
    family="Saba",
    ajnas=["Saba", "Hijaz"],
    ascending=[0, 1, 3, 4, 6, 7, 9, 12],  # C Db Eb E F# G B C
    descending=[12, 9, 7, 6, 4, 3, 1, 0],
    tonic="D",
    dominant="A",
    ghammaz="D",
    sayr="Emphasizes the unusual intervallic structure",
    mood="Very sad, mournful",
)

# Maqam Kurd - similar to Hijaz but different
MAQAM_KURD = MaqamScale(
    name="Kurd",
    name_arabic="كرد",
    family="Kurd",
    ajnas=["Kurd", "Rast"],
    ascending=[0, 1, 4, 5, 7, 9, 10.5, 12],  # C Db E F G A B-half-flat C
    descending=[12, 10.5, 9, 7, 5, 4, 1, 0],
    tonic="D",
    dominant="A",
    ghammaz="D",
    sayr="Similar to Hijaz but with different sayr",
    mood="Strong, masculine",
)

# Maqam Nahawand - minor-like
MAQAM_NAHAWAND = MaqamScale(
    name="Nahawand",
    name_arabic="نهاوند",
    family="Nahawand",
    ajnas=["Nahawand", "Nahawand"],
    ascending=[0, 2, 4, 5, 7, 8, 10, 12],  # C D Eb F G Ab Bb C
    descending=[12, 10, 8, 7, 5, 4, 2, 0],
    tonic="C",
    dominant="G",
    ghammaz="C",
    sayr="Similar to Western minor scale",
    mood="European-influenced, romantic",
)

# Maqam Ajam - major-like
MAQAM_AJAM = MaqamScale(
    name="Ajam",
    name_arabic="عجم",
    family="Ajam",
    ajnas=["Ajam", "Ajam"],
    ascending=[0, 2, 4, 5, 7, 9, 11, 12],  # C D E F G A B C
    descending=[12, 11, 9, 7, 5, 4, 2, 0],
    tonic="C",
    dominant="G",
    ghammaz="C",
    sayr="Similar to Western major scale",
    mood="Majestic, proud",
)

# Maqam Suzidil - interesting modulation
MAQAM_SUZIDIL = MaqamScale(
    name="Suzidil",
    name_arabic="سوزدل",
    family="Hijaz",
    ajnas=["Hijaz", "Hijaz", "Hijaz"],
    ascending=[0, 1, 4, 5, 7, 8, 11, 12],  # C Db E F G Ab B C
    descending=[12, 11, 8, 7, 5, 4, 1, 0],
    tonic="C",
    dominant="G",
    ghammaz="C",
    sayr="Multiple modulation points",
    mood="Strange, interesting",
)

# Maqam Huzam - similar to Sikah
MAQAM_HUZAM = MaqamScale(
    name="Huzam",
    name_arabic="هزام",
    family="Sikah",
    ajnas=["Sikah", "Bayati"],
    ascending=[0, 1.5, 3, 4.5, 6, 7, 8.5, 10, 12],
    descending=[12, 10, 8.5, 7, 6, 4.5, 3, 1.5, 0],
    tonic="E-half-flat",
    dominant="B-half-flat",
    ghammaz="E-half-flat",
    sayr="Similar to Sikah but with different development",
    mood="Emotional",
)


# =============================================================================
# Maqam Registry
# =============================================================================

ARABIC_MAQAMAT: dict[str, MaqamScale] = {
    "rast": MAQAM_RAST,
    "bayati": MAQAM_BAYATI,
    "sikah": MAQAM_SIKAH,
    "hijaz": MAQAM_HIJAZ,
    "saba": MAQAM_SABA,
    "kurd": MAQAM_KURD,
    "nahawand": MAQAM_NAHAWAND,
    "ajam": MAQAM_AJAM,
    "suzidil": MAQAM_SUZIDIL,
    "huzam": MAQAM_HUZAM,
}


# =============================================================================
# Helper Functions
# =============================================================================


def get_maqam_by_name(name: str) -> MaqamScale | None:
    """Get a maqam scale by name."""
    return ARABIC_MAQAMAT.get(name.lower())


def get_maqamat_by_family(family: str) -> dict[str, MaqamScale]:
    """Get all maqamat from a specific family."""
    return {k: v for k, v in ARABIC_MAQAMAT.items() if v.family.lower() == family.lower()}


def maqam_to_midi_scale(maqam: MaqamScale, root: int = 60) -> list[int]:
    """
    Convert a maqam scale to MIDI note numbers.

    Note: Quarter-tones are approximated to nearest semitone.

    Args:
        maqam: The maqam scale
        root: Root note MIDI number (default: C4 = 60)

    Returns:
        List of MIDI note numbers for the ascending scale
    """
    return [root + int(round(semitone)) for semitone in maqam.ascending]


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "MaqamScale",
    "ARABIC_MAQAMAT",
    "MAQAM_RAST",
    "MAQAM_BAYATI",
    "MAQAM_SIKAH",
    "MAQAM_HIJAZ",
    "MAQAM_SABA",
    "MAQAM_KURD",
    "MAQAM_NAHAWAND",
    "MAQAM_AJAM",
    "MAQAM_SUZIDIL",
    "MAQAM_HUZAM",
    "get_maqam_by_name",
    "get_maqamat_by_family",
    "maqam_to_midi_scale",
]
