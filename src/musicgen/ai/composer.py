"""Build compositions from AI-generated plans.

This module takes OrchestrationPlan objects and generates actual
musical scores using the musicgen composition engine.
"""

from __future__ import annotations

import random

from musicgen.ai.models import (
    DynamicsLevel,
    InstrumentAssignment,
    OrchestrationPlan,
    Section,
)
from musicgen.composition.melody import MelodicContour, MelodyGenerator
from musicgen.core.note import HALF, QUARTER, WHOLE, Note
from musicgen.io.midi_writer import Part, Score
from musicgen.theory.keys import Key
from musicgen.theory.progressions import Progression
from musicgen.theory.scales import Scale


def build_composition_from_plan(
    plan: OrchestrationPlan,
    seed: int | None = None
) -> Score:
    """Build a complete composition from an orchestration plan.

    Args:
        plan: The orchestration plan from AI.
        seed: Random seed for reproducibility.

    Returns:
        Complete Score ready for export.
    """
    if seed is not None:
        random.seed(seed)

    # Create score
    score = Score(
        title=plan.title,
        composer="MusicGen AI"
    )

    # Create key and scale for main key
    key = Key(plan.key, plan.key_type)
    scale = Scale(plan.key, plan.scale_type)

    # Process each section
    all_sections = []

    # Add intro if specified
    if plan.has_intro:
        all_sections.append(_create_intro_section(plan, key, scale))

    # Add main sections
    for section_plan in plan.sections:
        section_score = _build_section(section_plan, plan, key, scale)
        all_sections.append(section_score)

    # Add outro if specified
    if plan.has_outro:
        all_sections.append(_create_outro_section(plan, key, scale))

    # Merge all sections into the score
    _merge_sections_to_score(score, all_sections, plan)

    return score


def _create_intro_section(
    plan: OrchestrationPlan,
    key: Key,
    scale: Scale
) -> Score:
    """Create an introduction section.

    Args:
        plan: Overall orchestration plan.
        key: Main key.
        scale: Main scale.

    Returns:
        Score for intro section.
    """
    intro = Score(title="Intro", composer="MusicGen AI")

    # Simple intro: establish tonic with slow harmony
    progression = Progression.from_roman("I-IV-V-I", key=plan.key)

    # Generate simple pads for each instrument
    for inst in plan.instruments[:4]:  # Use first 4 instruments
        part = Part(name=inst.name)
        part.notes = _generate_pad_notes(progression, scale, inst.dynamics)
        intro.add_part(part)

    return intro


def _create_outro_section(
    plan: OrchestrationPlan,
    key: Key,
    scale: Scale
) -> Score:
    """Create an outro/coda section.

    Args:
        plan: Overall orchestration plan.
        key: Main key.
        scale: Main scale.

    Returns:
        Score for outro section.
    """
    outro = Score(title="Coda", composer="MusicGen AI")

    # Simple outro: resolve to tonic
    progression = Progression.from_roman("ii-V-I", key=plan.key)

    # Generate resolving parts
    for inst in plan.instruments[:4]:
        part = Part(name=inst.name)
        part.notes = _generate_pad_notes(progression, scale, inst.dynamics, slowing=True)
        outro.add_part(part)

    return outro


def _build_section(
    section: Section,
    plan: OrchestrationPlan,
    main_key: Key,
    main_scale: Scale
) -> Score:
    """Build a single section of the composition.

    Args:
        section: Section plan.
        plan: Overall orchestration plan.
        main_key: Main key of composition.
        main_scale: Main scale of composition.

    Returns:
        Score for this section.
    """
    section_score = Score(title=f"Section {section.name}", composer="MusicGen AI")

    # Create key and scale for this section
    section_key = Key(section.key, section.key_type)
    section_scale = Scale(section.key, section.scale_type)

    # Generate chord progression for this section
    num_chords = max(4, section.duration_seconds // 15)  # ~1 chord per 15 seconds
    progression = _generate_progression(
        section_key,
        num_chords,
        section.harmonic_center
    )

    # Determine which instruments play in this section
    active_instruments = _get_active_instruments(section, plan.instruments)

    # Generate parts for each instrument
    for inst in active_instruments:
        part = _generate_instrument_part(
            inst,
            section,
            progression,
            section_scale,
            section_key
        )
        section_score.add_part(part)

    return section_score


def _generate_instrument_part(
    inst: InstrumentAssignment,
    section: Section,
    progression: Progression,
    scale: Scale,
    key: Key
) -> Part:
    """Generate a part for a single instrument.

    Args:
        inst: Instrument assignment.
        section: Section plan.
        progression: Chord progression.
        scale: Scale for this section.
        key: Key for this section.

    Returns:
        Generated Part.
    """
    part = Part(name=inst.name)

    if inst.role == "melody":
        # Generate melodic line
        melody_gen = MelodyGenerator(scale, key, tempo=section.tempo)
        melody = melody_gen.generate_melody(
            progression=progression,
            contour=_select_contour(section.mood_description)
        )
        part.notes = melody.notes

    elif inst.role == "bass":
        # Generate bass line
        part.notes = _generate_bass_line(progression, scale)

    elif inst.role == "countermelody":
        # Generate countermelody
        melody_gen = MelodyGenerator(scale, key, tempo=section.tempo)
        melody = melody_gen.generate_melody(
            progression=progression,
            contour=MelodicContour.WAVE
        )
        # Offset countermelody rhythmically
        part.notes = _rhythmically_displace(melody.notes, offset=1)

    else:
        # Harmony/accompaniment/pad
        part.notes = _generate_harmony(progression, scale, inst.role)

    return part


def _generate_progression(
    key: Key,
    num_chords: int,
    harmonic_center: str
) -> Progression:
    """Generate a chord progression for a section.

    Args:
        key: Key for the section.
        num_chords: Number of chords to generate.
        harmonic_center: Tonic, dominant, etc.

    Returns:
        Chord progression.
    """
    # Common progressions based on harmonic center
    templates = {
        "tonic": ["I", "vi", "ii", "V", "I"],
        "dominant": ["V", "vi", "I", "IV", "V"],
        "subdominant": ["IV", "ii", "V", "I", "IV"],
    }

    template = templates.get(harmonic_center, templates["tonic"])

    # Extend template to match num_chords
    roman = ""
    i = 0
    while len(roman.split("-")) < num_chords:
        roman = "-".join(template + [template[i % len(template)]])
        i += 1

    return Progression.from_roman(roman, key=key.tonic)


def _get_active_instruments(
    section: Section,
    all_instruments: list[InstrumentAssignment]
) -> list[InstrumentAssignment]:
    """Get list of instruments that play in this section.

    Args:
        section: Section plan.
        all_instruments: All instruments in the composition.

    Returns:
        List of active instruments.
    """
    active = []

    for inst in all_instruments:
        if "all" in inst.when_playing or section.name in inst.when_playing:
            active.append(inst)

    # If no instruments specified, use all
    if not active:
        active = all_instruments

    return active


def _select_contour(mood: str) -> MelodicContour:
    """Select melodic contour based on mood description.

    Args:
        mood: Mood description.

    Returns:
        Appropriate melodic contour.
    """
    mood_lower = mood.lower()

    if any(w in mood_lower for w in ["ascending", "rising", "building", "climax"]):
        return MelodicContour.ASCENDING
    elif any(w in mood_lower for w in ["descending", "falling", "fading"]):
        return MelodicContour.DESCENDING
    elif any(w in mood_lower for w in ["wave", "flowing", "gentle", "calm"]):
        return MelodicContour.WAVE
    elif any(w in mood_lower for w in ["arch", "peak", "climax"]):
        return MelodicContour.ARCH
    else:
        return MelodicContour.WAVE  # Default


def _generate_bass_line(progression: Progression, scale: Scale) -> list:
    """Generate a bass line from chord progression.

    Args:
        progression: Chord progression.
        scale: Musical scale.

    Returns:
        List of notes for bass line.
    """
    notes = []
    for chord in progression.chords:
        # Root of chord in lower octave
        root_note = Note(chord.notes[0].name, chord.notes[0].octave - 1, QUARTER)
        notes.append(root_note)
        # Add fifth on longer chords
        fifth = Note(chord.notes[2].name, chord.notes[2].octave - 1, QUARTER)
        notes.append(fifth)
    return notes


def _generate_harmony(
    progression: Progression,
    scale: Scale,
    role: str
) -> list:
    """Generate harmony part.

    Args:
        progression: Chord progression.
        scale: Musical scale.
        role: Part role (harmony, pad, accompaniment).

    Returns:
        List of notes.
    """
    notes = []
    for chord in progression.chords:
        # Take inner voices (thirds of chords)
        if len(chord.notes) >= 2:
            third = Note(chord.notes[1].name, chord.notes[1].octave, HALF)
            notes.append(third)
        if len(chord.notes) >= 3:
            fifth = Note(chord.notes[2].name, chord.notes[2].octave - 1, HALF)
            notes.append(fifth)
    return notes


def _generate_pad_notes(
    progression: Progression,
    scale: Scale,
    dynamics: DynamicsLevel,
    slowing: bool = False
) -> list:
    """Generate pad/sustained notes.

    Args:
        progression: Chord progression.
        scale: Musical scale.
        dynamics: Dynamic level.
        slowing: Whether to slow down (for outro).

    Returns:
        List of sustained chord notes.
    """
    notes = []
    duration = WHOLE if not slowing else WHOLE * 2

    for chord in progression.chords:
        # Sustain the chord
        for note in chord.notes[:3]:
            pad_note = Note(note.name, note.octave, duration)
            notes.append(pad_note)

    return notes


def _rhythmically_displace(notes: list, offset: int) -> list:
    """Rhythmically displace notes for countermelody effect.

    Args:
        notes: Original notes.
        offset: Number of beats to offset.

    Returns:
        Displaced notes.
    """
    if offset <= 0:
        return notes

    # Add rest at beginning
    from musicgen.core.note import Rest
    displaced = [Rest(QUARTER) for _ in range(offset)]
    displaced.extend(notes)
    return displaced


def _merge_sections_to_score(
    score: Score,
    sections: list[Score],
    plan: OrchestrationPlan
) -> None:
    """Merge multiple section scores into main score.

    Args:
        score: Main score to populate.
        sections: List of section scores.
        plan: Overall orchestration plan.
    """
    # Collect all unique instrument names in order
    all_instruments = []
    seen = set()
    for section in sections:
        for part in section.parts:
            if part.name not in seen:
                all_instruments.append(part.name)
                seen.add(part.name)

    # Create combined parts for each instrument
    for inst_name in all_instruments:
        combined_part = Part(name=inst_name)

        for section in sections:
            # Find this instrument's part in the section
            for part in section.parts:
                if part.name == inst_name:
                    combined_part.notes.extend(part.notes)
                    break

        score.add_part(combined_part)
