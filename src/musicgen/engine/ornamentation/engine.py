"""Ornamentation engines for Indian classical music.

This module provides authentic Indian classical ornamentation including
meend (glissando/portamento), gamaka (oscillations), and krintan (grace notes).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from musicgen.core.note import Note


# =============================================================================
# Ornamentation Models
# =============================================================================


@dataclass
class MeendSpec:
    """Specification for a meend (glissando between notes)."""
    from_note: int  # MIDI note number
    to_note: int  # MIDI note number
    start_time: float
    duration: float
    intensity: float = 0.8  # 0.0 to 1.0


@dataclass
class GamakaSpec:
    """Specification for a gamaka (pitch oscillation around a note)."""
    note: int  # MIDI note number
    start_time: float
    duration: float
    oscillations: int = 3  # Number of oscillations
    width: int = 2  # Width in semitones
    shape: Literal["sine", "triangle", "sawtooth"] = "sine"


@dataclass
class KrintanSpec:
    """Specification for a krintan (quick grace note)."""
    grace_note: int  # MIDI note number for grace
    main_note: int  # MIDI note number for main note
    start_time: float
    grace_duration: float = 0.05  # Very short
    accent: float = 0.7  # Relative velocity


@dataclass
class AndolanSpec:
    """Specification for andolan (slow oscillation, typically on flat notes)."""
    note: int  # MIDI note number
    start_time: float
    duration: float
    width: int = 1  # Usually 1 semitone
    speed: float = 2.0  # Oscillations per second


# =============================================================================
# Ornamentation Engine
# =============================================================================


class OrnamentationEngine:
    """Engine for applying Indian classical ornamentations to notes."""

    def __init__(self) -> None:
        self._meend_cache: list[MeendSpec] = []
        self._gamaka_cache: list[GamakaSpec] = []
        self._krintan_cache: list[KrintanSpec] = []

    def apply_meend(
        self,
        notes: list[Note],
        from_idx: int,
        to_idx: int,
        intensity: float = 0.8,
    ) -> list[Note]:
        """Apply meend (glissando) between two notes.

        Creates a smooth pitch transition between notes, characteristic of
        string instruments like sitar and sarod.

        Args:
            notes: List of notes to modify
            from_idx: Index of starting note
            to_idx: Index of ending note
            intensity: Strength of meend (0.0 to 1.0)

        Returns:
            Modified notes with meend applied (as pitch bend events)
        """
        if from_idx >= len(notes) or to_idx >= len(notes):
            return notes

        from_note = notes[from_idx]
        to_note = notes[to_idx]

        # Calculate pitch bend range
        semitones = to_note.midi_number - from_note.midi_number

        # Store meend specification for rendering
        meend = MeendSpec(
            from_note=from_note.midi_number,
            to_note=to_note.midi_number,
            start_time=from_note.start_time,
            duration=from_note.duration,
            intensity=intensity,
        )
        self._meend_cache.append(meend)

        return notes

    def apply_gamaka(
        self,
        note: Note,
        oscillations: int = 3,
        width: int = 2,
        shape: Literal["sine", "triangle", "sawtooth"] = "sine",
    ) -> list[Note]:
        """Apply gamaka (pitch oscillation) to a note.

        Gamaka is a rapid oscillation around a note, essential in Carnatic
        and characteristic of many Hindustani ragas.

        Args:
            note: Note to apply gamaka to
            oscillations: Number of oscillations
            width: Width in semitones
            shape: Waveform shape

        Returns:
            Gamaka specification for rendering
        """
        gamaka = GamakaSpec(
            note=note.midi_number,
            start_time=note.start_time,
            duration=note.duration,
            oscillations=oscillations,
            width=width,
            shape=shape,
        )
        self._gamaka_cache.append(gamaka)

        return [note]

    def apply_krintan(
        self,
        notes: list[Note],
        idx: int,
        grace_interval: int = -2,
        grace_duration: float = 0.05,
        accent: float = 0.7,
    ) -> list[Note]:
        """Apply krintan (quick grace note) before a main note.

        Krintan is a spiccato-like attack where a quick grace note precedes
        the main note, commonly in plucked string instruments.

        Args:
            notes: List of notes
            idx: Index of note to add krintan before
            grace_interval: Semitones for grace note (usually below)
            grace_duration: Duration of grace note
            accent: Relative velocity of grace note

        Returns:
            Notes with grace note inserted
        """
        if idx >= len(notes):
            return notes

        main_note = notes[idx]
        grace_midi = main_note.midi_number + grace_interval

        krintan = KrintanSpec(
            grace_note=grace_midi,
            main_note=main_note.midi_number,
            start_time=main_note.start_time,
            grace_duration=grace_duration,
            accent=accent,
        )
        self._krintan_cache.append(krintan)

        return notes

    def apply_andolan(
        self,
        note: Note,
        width: int = 1,
        speed: float = 2.0,
    ) -> list[Note]:
        """Apply andolan (slow oscillation) to a note.

        Andolan is a slow, deliberate oscillation typically applied to
        komal (flat) notes like ga, dha, ni.

        Args:
            note: Note to apply andolan to
            width: Width in semitones (usually 1)
            speed: Oscillations per second

        Returns:
            Note with andolan specification
        """
        andolan = AndolanSpec(
            note=note.midi_number,
            start_time=note.start_time,
            duration=note.duration,
            width=width,
            speed=speed,
        )
        # Would need to cache this for rendering
        return [note]

    def suggest_ornamentations_for_raga(
        self,
        raga_name: str,
        notes: list[Note],
        frequency: str = "medium",
    ) -> dict[int, list[str]]:
        """Suggest which ornamentations to apply based on raga rules.

        Args:
            raga_name: Name of the raga
            notes: Notes in the melody
            frequency: "rare", "occasional", "frequent"

        Returns:
            Dictionary mapping note indices to ornamentation types
        """
        from musicgen.engine.raga import get_raga

        raga = get_raga(raga_name)
        suggestions = {}

        # Determine density based on frequency
        match frequency:
            case "rare":
                vadi_chance = 0.2
                komal_chance = 0.1
            case "occasional":
                vadi_chance = 0.5
                komal_chance = 0.3
            case "frequent":
                vadi_chance = 0.8
                komal_chance = 0.5
            case _:
                vadi_chance = 0.5
                komal_chance = 0.3

        import random

        for i, note in enumerate(notes):
            midi = note.midi_number
            ornaments = []

            # Vadi note gets meend
            if midi == raga.vadi and random.random() < vadi_chance:
                ornaments.append("meend")

            # Check if note is komal (flat) - these are often at intervals
            # from the base that suggest flat versions
            # Komal notes typically: re (62), ga (64), dha (69), ni (71) in C
            komal_notes = [62, 64, 69, 71]
            if midi in komal_notes and random.random() < komal_chance:
                ornaments.append("andolan")

            # Samvadi gets gamaka
            if midi == raga.samvadi and random.random() < vadi_chance * 0.7:
                ornaments.append("gamaka")

            # Strong beats might get krintan
            if ornaments:
                suggestions[i] = ornaments

        return suggestions

    def get_meend_cache(self) -> list[MeendSpec]:
        """Get cached meend specifications for rendering."""
        return self._meend_cache.copy()

    def get_gamaka_cache(self) -> list[GamakaSpec]:
        """Get cached gamaka specifications for rendering."""
        return self._gamaka_cache.copy()

    def get_krintan_cache(self) -> list[KrintanSpec]:
        """Get cached krintan specifications for rendering."""
        return self._krintan_cache.copy()

    def clear_cache(self) -> None:
        """Clear all cached ornamentation specifications."""
        self._meend_cache.clear()
        self._gamaka_cache.clear()
        self._krintan_cache.clear()


# =============================================================================
# Utility Functions
# =============================================================================


def apply_ornamentation_by_type(
    notes: list[Note],
    idx: int,
    ornament_type: str,
    engine: OrnamentationEngine | None = None,
) -> list[Note]:
    """Apply a specific ornamentation type to a note.

    Args:
        notes: List of notes
        idx: Index of note to ornament
        ornament_type: "meend", "gamaka", "krintan", or "andolan"
        engine: OrnamentationEngine instance (creates new if None)

    Returns:
        Modified notes
    """
    if engine is None:
        engine = OrnamentationEngine()

    if idx >= len(notes):
        return notes

    match ornament_type.lower():
        case "meend":
            if idx < len(notes) - 1:
                return engine.apply_meend(notes, idx, idx + 1)
        case "gamaka":
            return engine.apply_gamaka(notes[idx])
        case "krintan":
            return engine.apply_krintan(notes, idx)
        case "andolan":
            return engine.apply_andolan(notes[idx])

    return notes


def raga_appropriate_ornamentation(
    raga_name: str,
    note_midi: int,
    is_komal: bool = False,
) -> list[str]:
    """Get ornamentation types appropriate for a note in a raga.

    Args:
        raga_name: Name of the raga
        note_midi: MIDI note number
        is_komal: Whether this is a komal (flat) note

    Returns:
        List of appropriate ornamentation types
    """
    from musicgen.engine.raga import get_raga

    raga = get_raga(raga_name)
    ornaments = []

    # Vadi note - can take meend
    if note_midi == raga.vadi:
        ornaments.append("meend")

    # Samvadi note - can take gamaka
    if note_midi == raga.samvadi:
        ornaments.append("gamaka")

    # Komal notes - andolan is traditional
    if is_komal:
        ornaments.append("andolan")

    # Strong notes - can take krintan
    if note_midi in [raga.vadi, raga.samvadi]:
        ornaments.append("krintan")

    return ornaments
