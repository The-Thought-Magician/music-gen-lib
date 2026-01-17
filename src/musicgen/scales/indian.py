"""
Indian raga scale definitions for music-gen-lib V4.

This module provides scale definitions for common Indian ragas,
including the that (parent scales) and jati (scale types).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


# =============================================================================
# Indian Raga Scale Classes
# =============================================================================


@dataclass
class RagaScale:
    """
    Indian raga scale definition.

    Attributes:
        name: Raga name (English transliteration)
        name_hindi: Raga name in Devanagari script
        that: Parent scale (one of the 10 thats)
        ascending: Ascending scale (aroha) in semitones from tonic
        descending: Descending scale (avaroha) in semitones from tonic
        vadi: Most important note (1-7, relative to tonic)
        samvadi: Second most important note
        pakad: Characteristic phrase/motif
        thaat: Parent thaat classification
        time: Recommended time of performance (prahar)
        mood: Emotional mood (rasa)
    """

    name: str
    name_hindi: str
    that: str
    ascending: list[int]
    descending: list[int]
    vadi: int
    samvadi: int
    pakad: str = ""
    thaat: str = ""
    time: str = ""
    mood: str = ""


# =============================================================================
# Thats (Parent Scales)
# =============================================================================

# Bilaval (equivalent to major scale)
THAT_BILAVAL = [0, 2, 4, 5, 7, 9, 11]  # S R G m P D N

# Bhairavi (equivalent to natural minor)
THAT_BHAIRAVI = [0, 1, 3, 5, 7, 8, 10]  # S r g m P d n

# Kalyan (Lydian)
THAT_KALYAN = [0, 2, 4, 6, 7, 9, 11]  # S R G M P D N

# Khamaj (Mixolydian with raised 4th in ascent)
THAT_KHAMAJ = [0, 2, 4, 5, 7, 9, 10]  # S R G m P D n

# Kafi (Dorian)
THAT_KAFI = [0, 2, 3, 5, 7, 9, 10]  # S R g m P D n

# Asavari (Aeolian/natural minor with flattened 7th)
THAT_ASAVARI = [0, 2, 3, 5, 7, 8, 10]  # S R g m P d n

# Bhairav (double harmonic)
THAT_BHAIRAV = [0, 1, 3, 4, 7, 8, 11]  # S r G m P d N

# Purvi
THAT_PURVI = [0, 1, 4, 6, 7, 8, 11]  # S r G M P d N

# Marwa
THAT_MARWA = [0, 1, 4, 6, 7, 9, 11]  # S r G M P D N

# Todi
THAT_TODI = [0, 1, 3, 6, 7, 8, 10]  # S r g M P d n


# =============================================================================
# Common Ragas
# =============================================================================

# Raga Yaman (Kalyan That) - Evening raga
RAGA_YAMAN = RagaScale(
    name="Yaman",
    name_hindi="यमन",
    that="Kalyan",
    ascending=[0, 2, 4, 6, 7, 9, 11],  # S R G M P D N (all shuddha except M)
    descending=[11, 9, 7, 6, 4, 2, 0],  # N D P M G R S
    vadi=4,  # G (Gandhar)
    samvadi=1,  # N (Nishad) - wait, numbering is different
    pakad="N-R-G-M-P, D-N-S-R",
    thaat="Kalyan",
    time="Evening (1st prahar)",
    mood="Devotional, peaceful",
)

# Raga Bhairavi (Bhairavi Thaat) - Morning raga
RAGA_BHAIRAVI = RagaScale(
    name="Bhairavi",
    name_hindi="भैरवी",
    that="Bhairavi",
    ascending=[0, 1, 3, 5, 7, 8, 10],  # S r g m P d n (all komal)
    descending=[10, 8, 7, 5, 3, 1, 0],  # n d P m g r S
    vadi=2,  # g (Gandhar)
    samvadi=5,  # d (Dhaivat)
    pakad="G-M-D-P, M-P-G-M-g-R-S",
    thaat="Bhairavi",
    time="Morning",
    mood="Devotional, early morning",
)

# Raga Bhairav (Bhairav Thaat) - Morning raga
RAGA_BHAIRAV = RagaScale(
    name="Bhairav",
    name_hindi="भैरव",
    that="Bhairav",
    ascending=[0, 1, 4, 5, 7, 8, 11],  # S r G m P d N (r and d komal)
    descending=[11, 8, 7, 5, 4, 1, 0],  # N d P m G r S
    vadi=1,  # r (Rishabh)
    samvadi=4,  # P (Pancham)
    pakad="S-r-G-M-P-G-M-r-S",
    thaat="Bhairav",
    time="Early morning",
    mood="Serious, majestic",
)

# Raga Todi (Todi Thaat) - Morning raga
RAGA_TODI = RagaScale(
    name="Todi",
    name_hindi="तोड़ी",
    that="Todi",
    ascending=[0, 1, 3, 6, 7, 8, 10],  # S r g M P d n
    descending=[10, 8, 7, 6, 3, 1, 0],  # n d P M g r S
    vadi=3,  # g (Gandhar)
    samvadi=7,  # P (Pancham)
    pakad="S-r-g-M-P-M-g-r-S",
    thaat="Todi",
    time="Late morning",
    mood="Deep, serious, romantic",
)

# Raga Bhimpalasi (Kafi Thaat) - Afternoon raga
RAGA_BHIMPALASI = RagaScale(
    name="Bhimpalasi",
    name_hindi="भीमपलासी",
    that="Kafi",
    ascending=[0, 2, 3, 5, 7, 9, 10],  # S R g m P D n
    descending=[10, 9, 7, 5, 3, 2, 0],  # n D P m g R S
    vadi=3,  # g (Gandhar)
    samvadi=9,  # D (Dhaivat)
    pakad="n-S-R-g-M-P-D-P-M-g-R-S",
    thaat="Kafi",
    time="Afternoon",
    mood="Pathos, yearning",
)

# Raga Darbari (Asavari Thaat) - Midnight raga
RAGA_DARBARI = RagaScale(
    name="Darbari",
    name_hindi="दरबारी",
    that="Asavari",
    ascending=[0, 2, 3, 5, 7, 8, 10],  # S R g m P d n (slow ascent)
    descending=[10, 8, 7, 5, 3, 2, 0],  # n d P m g R S
    vadi=3,  # g (Gandhar)
    samvadi=8,  # d (Dhaivat)
    pakad="S-R-g-M-d-P-M-g-R-g-M-P-d-P",
    thaat="Asavari",
    time="Midnight",
    mood="Deep, serious, majestic",
)

# Raga Malkauns (Bhairavi Thaat) - Midnight raga
RAGA_MALKAUNS = RagaScale(
    name="Malkauns",
    name_hindi="मालकौंस",
    that="Bhairavi",
    ascending=[0, 3, 5, 7, 8, 10],  # S-g-m-d-n-S (pentatonic)
    descending=[10, 8, 7, 5, 3, 0],  # n-d-m-g-S
    vadi=3,  # g (Gandhar)
    samvadi=8,  # d (Dhaivat)
    pakad="g-m-d-S'-S-d-m-g-R-g",
    thaat="Bhairavi",
    time="Midnight",
    mood="Deep, romantic, devotional",
)

# Raga Desh (Khamaj Thaat) - Evening raga
RAGA_DESH = RagaScale(
    name="Desh",
    name_hindi="देश",
    that="Khamaj",
    ascending=[0, 2, 4, 5, 7, 9, 10],  # S R G m P D n
    descending=[10, 9, 7, 5, 4, 2, 0],  # n D P m G R S
    vadi=5,  # P (Pancham)
    samvadi=2,  # R (Rishabh)
    pakad="S-R-G-M-P-n-D-P",
    thaat="Khamaj",
    time="Evening",
    mood="Romantic, patriotic",
)

# Raga Bageshri (Kafi Thaat) - Late night raga
RAGA_BAGESHRI = RagaScale(
    name="Bageshri",
    name_hindi="बागेश्री",
    that="Kafi",
    ascending=[0, 2, 3, 5, 7, 9, 10],  # S R g m P D n
    descending=[10, 9, 7, 5, 3, 2, 0],  # n D P m g R S
    vadi=3,  # g (Gandhar)
    samvadi=9,  # D (Dhaivat)
    pakad="S-R-g-M-P-n-D-n-S",
    thaat="Kafi",
    time="Late night",
    mood="Romantic, devotional",
)


# =============================================================================
# Raga Registry
# =============================================================================

INDIAN_RAGAS: dict[str, RagaScale] = {
    "yaman": RAGA_YAMAN,
    "bhairavi": RAGA_BHAIRAVI,
    "bhairav": RAGA_BHAIRAV,
    "todi": RAGA_TODI,
    "bhimpalasi": RAGA_BHIMPALASI,
    "darbari": RAGA_DARBARI,
    "malkauns": RAGA_MALKAUNS,
    "desh": RAGA_DESH,
    "bageshri": RAGA_BAGESHRI,
}


# =============================================================================
# Helper Functions
# =============================================================================


def get_raga_by_name(name: str) -> RagaScale | None:
    """Get a raga scale by name."""
    return INDIAN_RAGAS.get(name.lower())


def get_ragas_by_that(thaat: str) -> dict[str, RagaScale]:
    """Get all ragas from a specific thaat."""
    return {k: v for k, v in INDIAN_RAGAS.items() if v.that.lower() == thaat.lower()}


def get_ragas_by_time(time: str) -> dict[str, RagaScale]:
    """Get ragas suitable for a given time of day."""
    return {k: v for k, v in INDIAN_RAGAS.items() if time.lower() in v.time.lower()}


def raga_to_midi_scale(raga: RagaScale, root: int = 60) -> list[int]:
    """
    Convert a raga scale to MIDI note numbers.

    Args:
        raga: The raga scale
        root: Root note MIDI number (default: C4 = 60)

    Returns:
        List of MIDI note numbers for the ascending scale
    """
    return [root + semitone for semitone in raga.ascending]


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "RagaScale",
    "INDIAN_RAGAS",
    "RAGA_YAMAN",
    "RAGA_BHAIRAVI",
    "RAGA_BHAIRAV",
    "RAGA_TODI",
    "RAGA_BHIMPALASI",
    "RAGA_DARBARI",
    "RAGA_MALKAUNS",
    "RAGA_DESH",
    "RAGA_BAGESHRI",
    "get_raga_by_name",
    "get_ragas_by_that",
    "get_ragas_by_time",
    "raga_to_midi_scale",
]
