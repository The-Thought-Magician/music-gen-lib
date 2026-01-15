"""Orchestration strategies for different textures and ensembles.

This module provides strategies for creating different orchestral textures
and assigning instruments to musical roles.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from musicgen.core.note import Note
from musicgen.theory.keys import Key
from musicgen.theory.progressions import Progression
from musicgen.theory.scales import Scale


class TextureType(Enum):
    """Types of orchestral texture."""
    HOMOPHONIC = "homophonic"  # Melody with chordal accompaniment
    POLYPHONIC = "polyphonic"  # Independent melodic lines
    MELODY_PLUS_ACCOMPANIMENT = "melody+accompaniment"
    PAD = "pad"  # Sustained chords
    TUTTI = "tutti"  # All instruments playing
    SOLO = "solo"  # Single instrument
    DIALOGUE = "dialogue"  # Call and response between groups


class TextureDensity(Enum):
    """Density of orchestration."""
    THIN = "thin"  # 1-2 instruments
    LIGHT = "light"  # 3-4 instruments
    MEDIUM = "medium"  # 5-8 instruments
    THICK = "thick"  # 9-12 instruments
    TUTTI = "tutti"  # All instruments


@dataclass
class InstrumentRole:
    """Role assignment for an instrument."""

    instrument: str
    role: str  # "melody", "harmony", "bass", "accompaniment", "countermelody"
    voice_index: int = 0  # For voice leading (0=soprano/highest)
    doubling: str | None = None  # What instrument to double
    divisi: int = 1  # Number of parts


@dataclass
class TexturePlan:
    """Plan for orchestration texture."""

    texture_type: TextureType
    density: TextureDensity
    roles: list[InstrumentRole]
    dynamics: str = "mf"


class OrchestrationStrategies:
    """Collection of orchestration strategies."""

    @staticmethod
    def homophonic(
        melody_instruments: list[str],
        harmony_instruments: list[str],
        bass_instruments: list[str] | None = None
    ) -> TexturePlan:
        """Create homophonic texture (melody + chordal accompaniment).

        Args:
            melody_instruments: Instruments playing melody.
            harmony_instruments: Instruments playing harmony.
            bass_instruments: Instruments playing bass line.

        Returns:
            Texture plan for homophonic texture.
        """
        roles = []

        # Melody roles
        for i, inst in enumerate(melody_instruments):
            roles.append(InstrumentRole(
                instrument=inst,
                role="melody",
                voice_index=i
            ))

        # Harmony roles
        for i, inst in enumerate(harmony_instruments):
            roles.append(InstrumentRole(
                instrument=inst,
                role="harmony",
                voice_index=len(melody_instruments) + i
            ))

        # Bass roles
        if bass_instruments:
            for inst in bass_instruments:
                roles.append(InstrumentRole(
                    instrument=inst,
                    role="bass",
                    voice_index=99  # Always lowest
                ))

        return TexturePlan(
            texture_type=TextureType.HOMOPHONIC,
            density=OrchestrationStrategies._calculate_density(len(roles)),
            roles=roles
        )

    @staticmethod
    def polyphonic(instruments: list[str]) -> TexturePlan:
        """Create polyphonic texture (independent melodic lines).

        Args:
            instruments: All instruments playing independent lines.

        Returns:
            Texture plan for polyphonic texture.
        """
        roles = []
        for i, inst in enumerate(instruments):
            roles.append(InstrumentRole(
                instrument=inst,
                role="countermelody",
                voice_index=i
            ))

        return TexturePlan(
            texture_type=TextureType.POLYPHONIC,
            density=OrchestrationStrategies._calculate_density(len(roles)),
            roles=roles
        )

    @staticmethod
    def melody_with_accompaniment(
        melody_instrument: str,
        accompaniment_instruments: list[str],
        bass_instrument: str | None = None
    ) -> TexturePlan:
        """Create melody + accompaniment texture.

        Args:
            melody_instrument: Solo melody instrument.
            accompaniment_instruments: Accompaniment instruments.
            bass_instrument: Optional bass instrument.

        Returns:
            Texture plan for melody + accompaniment.
        """
        roles = [
            InstrumentRole(melody_instrument, "melody", 0)
        ]

        for i, inst in enumerate(accompaniment_instruments):
            roles.append(InstrumentRole(
                instrument=inst,
                role="accompaniment",
                voice_index=i + 1
            ))

        if bass_instrument:
            roles.append(InstrumentRole(
                instrument=bass_instrument,
                role="bass",
                voice_index=99
            ))

        return TexturePlan(
            texture_type=TextureType.MELODY_PLUS_ACCOMPANIMENT,
            density=OrchestrationStrategies._calculate_density(len(roles)),
            roles=roles
        )

    @staticmethod
    def pad(instruments: list[str]) -> TexturePlan:
        """Create pad texture (sustained chords).

        Args:
            instruments: Instruments providing pad.

        Returns:
            Texture plan for pad texture.
        """
        roles = []
        for i, inst in enumerate(instruments):
            roles.append(InstrumentRole(
                instrument=inst,
                role="harmony",
                voice_index=i
            ))

        return TexturePlan(
            texture_type=TextureType.PAD,
            density=OrchestrationStrategies._calculate_density(len(roles)),
            roles=roles
        )

    @staticmethod
    def tutti(instruments: list[str]) -> TexturePlan:
        """Create tutti texture (all instruments playing).

        Args:
            instruments: All instruments.

        Returns:
            Texture plan for tutti texture.
        """
        roles = []
        for i, inst in enumerate(instruments):
            roles.append(InstrumentRole(
                instrument=inst,
                role="melody" if i == 0 else "harmony",
                voice_index=i
            ))

        return TexturePlan(
            texture_type=TextureType.TUTTI,
            density=TextureDensity.TUTTI,
            roles=roles
        )

    @staticmethod
    def dialogue(group1: list[str], group2: list[str]) -> TexturePlan:
        """Create dialogue texture (call and response).

        Args:
            group1: First group of instruments.
            group2: Second group of instruments.

        Returns:
            Texture plan for dialogue texture.
        """
        roles = []

        # Group 1
        for i, inst in enumerate(group1):
            roles.append(InstrumentRole(
                instrument=inst,
                role="melody",
                voice_index=i
            ))

        # Group 2
        for i, inst in enumerate(group2):
            roles.append(InstrumentRole(
                instrument=inst,
                role="melody",
                voice_index=len(group1) + i
            ))

        return TexturePlan(
            texture_type=TextureType.DIALOGUE,
            density=OrchestrationStrategies._calculate_density(len(roles)),
            roles=roles
        )

    @staticmethod
    def _calculate_density(num_instruments: int) -> TextureDensity:
        """Calculate texture density from number of instruments.

        Args:
            num_instruments: Number of instruments.

        Returns:
            TextureDensity value.
        """
        if num_instruments <= 2:
            return TextureDensity.THIN
        elif num_instruments <= 4:
            return TextureDensity.LIGHT
        elif num_instruments <= 8:
            return TextureDensity.MEDIUM
        elif num_instruments <= 12:
            return TextureDensity.THICK
        else:
            return TextureDensity.TUTTI


class OrchestrationBuilder:
    """Builds orchestrations from texture plans."""

    def __init__(self, key: Key, scale: Scale):
        """Initialize orchestration builder.

        Args:
            key: Musical key.
            scale: Musical scale.
        """
        self.key = key
        self.scale = scale

    def apply_texture(
        self,
        texture_plan: TexturePlan,
        progression: Progression,
        duration_bars: int = 8
    ) -> dict[str, list[Note]]:
        """Apply a texture plan to a chord progression.

        Args:
            texture_plan: The texture plan to apply.
            progression: Chord progression.
            duration_bars: Number of bars to generate.

        Returns:
            Dictionary mapping instrument names to note lists.
        """
        result = {}

        for role in texture_plan.roles:
            notes = self._generate_part(
                role,
                progression,
                duration_bars
            )
            result[role.instrument] = notes

        return result

    def _generate_part(
        self,
        role: InstrumentRole,
        progression: Progression,
        duration_bars: int
    ) -> list[Note]:
        """Generate notes for an instrument based on its role.

        Args:
            role: Instrument role assignment.
            progression: Chord progression.
            duration_bars: Duration in bars.

        Returns:
            List of notes for this part.
        """
        if role.role == "melody":
            return self._generate_melody(progression, duration_bars)
        elif role.role == "bass":
            return self._generate_bass(progression, duration_bars)
        elif role.role == "harmony":
            return self._generate_harmony(progression, duration_bars, role.voice_index)
        elif role.role == "accompaniment":
            return self._generate_accompaniment(progression, duration_bars)
        elif role.role == "countermelody":
            return self._generate_countermelody(progression, duration_bars)
        else:
            return self._generate_harmony(progression, duration_bars, role.voice_index)

    def _generate_melody(
        self,
        progression: Progression,
        duration_bars: int
    ) -> list[Note]:
        """Generate melodic line.

        Args:
            progression: Chord progression.
            duration_bars: Duration in bars.

        Returns:
            Melody notes.
        """
        from musicgen.composition.melody import MelodicContour, MelodyGenerator

        melody_gen = MelodyGenerator(self.scale, self.key)
        melody = melody_gen.generate_melody(
            progression=progression,
            contour=MelodicContour.WAVE,
            length=duration_bars * 4
        )

        return melody.notes

    def _generate_bass(
        self,
        progression: Progression,
        duration_bars: int
    ) -> list[Note]:
        """Generate bass line.

        Args:
            progression: Chord progression.
            duration_bars: Duration in bars.

        Returns:
            Bass notes.
        """
        from musicgen.core.note import HALF

        notes = []
        beats_per_chord = 4
        chords_per_bar = 1

        for chord in progression.chords:
            root = chord.notes[0]
            bass_note = Note(root.name, root.octave - 1, HALF)
            notes.append(bass_note)

            # Add fifth
            if len(chord.notes) >= 3:
                fifth = chord.notes[2]
                bass_fifth = Note(fifth.name, fifth.octave - 1, HALF)
                notes.append(bass_fifth)

        return notes

    def _generate_harmony(
        self,
        progression: Progression,
        duration_bars: int,
        voice_index: int
    ) -> list[Note]:
        """Generate harmony part.

        Args:
            progression: Chord progression.
            duration_bars: Duration in bars.
            voice_index: Which voice (0=lowest).

        Returns:
            Harmony notes.
        """
        from musicgen.core.note import WHOLE

        notes = []
        voice_index = min(voice_index, 2)  # Limit to 3rds and 5ths

        for chord in progression.chords:
            if len(chord.notes) > voice_index:
                note = chord.notes[voice_index]
                harmony_note = Note(note.name, note.octave, WHOLE)
                notes.append(harmony_note)

        return notes

    def _generate_accompaniment(
        self,
        progression: Progression,
        duration_bars: int
    ) -> list[Note]:
        """Generate accompaniment pattern.

        Args:
            progression: Chord progression.
            duration_bars: Duration in bars.

        Returns:
            Accompaniment notes.
        """
        from musicgen.core.note import QUARTER

        notes = []

        for chord in progression.chords:
            # Alberti bass pattern
            if len(chord.notes) >= 3:
                root = chord.notes[0]
                third = chord.notes[1]
                fifth = chord.notes[2]

                notes.append(Note(root.name, root.octave - 1, QUARTER))
                notes.append(Note(fifth.name, fifth.octave - 1, QUARTER))
                notes.append(Note(third.name, third.octave - 1, QUARTER))
                notes.append(Note(fifth.name, fifth.octave - 1, QUARTER))

        return notes

    def _generate_countermelody(
        self,
        progression: Progression,
        duration_bars: int
    ) -> list[Note]:
        """Generate countermelody.

        Args:
            progression: Chord progression.
            duration_bars: Duration in bars.

        Returns:
            Countermelody notes.
        """
        from musicgen.composition.melody import MelodicContour, MelodyGenerator

        melody_gen = MelodyGenerator(self.scale, self.key)
        melody = melody_gen.generate_melody(
            progression=progression,
            contour=MelodicContour.DESCENDING,
            length=duration_bars * 3
        )

        # Offset by one beat for rhythmic interest
        from musicgen.core.note import Rest
        offset_melody = [Rest(QUARTER)] + melody.notes

        return offset_melody


# Preset orchestrations
ORCHESTRATION_PRESETS = {
    "string_quartet": OrchestrationStrategies.homophonic(
        melody_instruments=["violin"],
        harmony_instruments=["viola"],
        bass_instruments=["cello"]
    ),

    "full_orchestra": OrchestrationStrategies.homophonic(
        melody_instruments=["violin", "flute"],
        harmony_instruments=["viola", "clarinet", "french_horn"],
        bass_instruments=["cello", "double_bass", "bassoon"]
    ),

    "chamber_ensemble": OrchestrationStrategies.polyphonic(
        instruments=["violin", "viola", "cello", "flute"]
    ),

    "piano_trio": OrchestrationStrategies.melody_with_accompaniment(
        melody_instrument="violin",
        accompaniment_instruments=["piano"],
        bass_instrument="cello"
    ),

    "brass_ensemble": OrchestrationStrategies.tutti(
        instruments=["trumpet", "trumpet", "french_horn", "french_horn", "trombone"]
    ),

    "woodwind_choir": OrchestrationStrategies.homophonic(
        melody_instruments=["flute"],
        harmony_instruments=["clarinet", "oboe"],
        bass_instruments=["bassoon"]
    ),
}


def get_preset(name: str) -> TexturePlan | None:
    """Get an orchestration preset by name.

    Args:
        name: Preset name.

    Returns:
        TexturePlan or None if not found.
    """
    return ORCHESTRATION_PRESETS.get(name)
