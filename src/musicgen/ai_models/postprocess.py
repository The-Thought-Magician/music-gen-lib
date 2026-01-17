"""Post-processing validation and auto-fix for AI-generated compositions.

This module provides functions to detect and fix common issues in AI-generated
music, particularly around polyphony (multiple notes starting at the same time)
for harmony and accompaniment parts.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from musicgen.ai_models.notes import AINote, AINoteEvent, AIRest
from musicgen.ai_models.parts import AIPart, InstrumentRole

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of composition validation.

    Attributes:
        is_valid: Whether the composition passed validation
        issues: List of issue descriptions
        parts_with_issues: Names of parts that have issues
        can_auto_fix: Whether the issues can be automatically fixed
    """
    is_valid: bool = True
    issues: list[str] = field(default_factory=list)
    parts_with_issues: dict[str, list[str]] = field(default_factory=dict)
    can_auto_fix: bool = True


def is_harmony_role(role: InstrumentRole | str) -> bool:
    """Check if a role typically requires polyphonic handling.

    Args:
        role: The instrument role to check

    Returns:
        True if this role typically uses chords/polyphony
    """
    if isinstance(role, str):
        role = InstrumentRole(role)

    return role in (
        InstrumentRole.HARMONY,
        InstrumentRole.ACCOMPANIMENT,
        InstrumentRole.PAD,
    )


def detect_chord_groups(notes: list[AINoteEvent]) -> list[list[int]]:
    """Detect groups of notes that should be chords (same start time).

    Analyzes note patterns to find consecutive notes with the same duration,
    which typically indicates a chord.

    Args:
        notes: List of note events (notes and rests)

    Returns:
        List of chord groups, where each group is a list of note indices
    """
    chord_groups = []
    i = 0

    while i < len(notes):
        # Skip rests
        if isinstance(notes[i], AIRest):
            i += 1
            continue

        # Get current note
        current_note = notes[i]
        if not isinstance(current_note, AINote):
            i += 1
            continue

        current_duration = current_note.duration
        group = [i]

        # Look ahead for notes with same duration (potential chord)
        j = i + 1
        while j < len(notes):
            next_event = notes[j]

            # Stop at rest
            if isinstance(next_event, AIRest):
                break

            if not isinstance(next_event, AINote):
                j += 1
                continue

            # Check if same duration (within small tolerance for floating point)
            if abs(next_event.duration - current_duration) < 0.01:
                # Check if already has start_time assigned differently
                if (current_note.start_time is not None and
                        next_event.start_time is not None and
                        abs(next_event.start_time - current_note.start_time) > 0.01):
                    # Different start times, not a chord
                    break

                group.append(j)
            else:
                # Different duration, end of potential chord
                break

            j += 1

        # Only consider it a chord if we have 2+ notes with same duration
        if len(group) >= 2:
            chord_groups.append(group)

        i += len(group) if len(group) >= 2 else 1

    return chord_groups


def fix_polyphony(part: AIPart) -> AIPart:
    """Fix missing polyphony information in a part.

    Detects harmony/accompaniment parts and assigns start_time values
    to notes that don't have them, using chord detection.

    Args:
        part: The part to fix

    Returns:
        The fixed part (may be the same object if no fixes needed)
    """
    role = part.role

    # Only process harmony/accompaniment roles
    if not is_harmony_role(role):
        logger.debug(f"Part '{part.name}' has role '{role}', skipping polyphony fix")
        return part

    # Get validated note events
    note_events = part.get_note_events()
    notes_only = [n for n in note_events if isinstance(n, AINote)]

    # Check if we need to fix start_times
    needs_fix = any(n.start_time is None for n in notes_only)

    if not needs_fix:
        logger.debug(f"Part '{part.name}' already has start_time for all notes")
        return part

    logger.info(f"Fixing polyphony for part '{part.name}' (role: {role})")

    # Detect chord groups
    chord_groups = detect_chord_groups(note_events)

    if not chord_groups:
        logger.warning(f"No chord groups detected in '{part.name}', assigning sequential timing")
        # No chords detected, assign sequential timing
        current_time = 0.0
        for note in notes_only:
            if note.start_time is None:
                note.start_time = current_time
            current_time += note.duration
        return part

    # Assign start times based on chord groups
    current_time = 0.0
    processed_indices = set()

    for i, event in enumerate(note_events):
        if i in processed_indices:
            continue

        if isinstance(event, AIRest):
            processed_indices.add(i)
            current_time += event.duration
            continue

        if isinstance(event, AINote):
            # Check if this note is part of a chord group
            found_chord = False
            for group in chord_groups:
                if i in group:
                    # This is a chord - assign same start_time to all notes in group
                    for idx in group:
                        if idx < len(note_events):
                            note = note_events[idx]
                            if isinstance(note, AINote) and note.start_time is None:
                                note.start_time = current_time
                            processed_indices.add(idx)

                    # Move time forward by the chord duration
                    max_duration = max(
                        note_events[idx].duration
                        for idx in group
                        if idx < len(note_events) and isinstance(note_events[idx], AINote)
                    )
                    current_time += max_duration
                    found_chord = True
                    break

            if not found_chord:
                # Single note
                if event.start_time is None:
                    event.start_time = current_time
                current_time += event.duration
                processed_indices.add(i)

    logger.info(
        f"Fixed polyphony for '{part.name}': {len(chord_groups)} chord groups detected"
    )

    return part


def validate_composition(
    composition: Any,
    auto_fix: bool = False,
) -> ValidationResult:
    """Validate a composition for polyphony and other common issues.

    Checks if harmony/accompaniment parts have proper polyphony (notes with
    same start_time for chords).

    Args:
        composition: AIComposition or dict with parts
        auto_fix: If True, automatically fix issues found

    Returns:
        ValidationResult with details of any issues
    """
    result = ValidationResult()

    # Handle both AIComposition and dict input
    if hasattr(composition, "parts"):
        parts = composition.parts
    elif isinstance(composition, dict):
        parts = composition.get("parts", [])
    else:
        result.is_valid = False
        result.issues.append("Invalid composition format")
        result.can_auto_fix = False
        return result

    total_chords_found = 0
    total_parts_checked = 0
    fixed_parts = []

    for part in parts:
        # Handle both AIPart objects and dicts
        if hasattr(part, "role"):
            role = part.role
            part_name = part.name
        elif isinstance(part, dict):
            role_str = part.get("role", "melody")
            role = InstrumentRole(role_str) if isinstance(role_str, str) else role_str
            part_name = part.get("name", "unknown")
        else:
            continue

        # Skip non-harmony parts
        if not is_harmony_role(role):
            continue

        total_parts_checked += 1

        # Get note events
        if hasattr(part, "get_note_events"):
            note_events = part.get_note_events()
        elif isinstance(part, dict):
            notes_list = part.get("notes", [])
            note_events = []
            for n in notes_list:
                if isinstance(n, dict):
                    if n.get("rest") is True:
                        note_events.append(AIRest(**n))
                    else:
                        note_events.append(AINote(**n))
                else:
                    note_events.append(n)
        else:
            continue

        notes_only = [n for n in note_events if isinstance(n, AINote)]

        # Check for missing start_time
        missing_start_time = [n for n in notes_only if n.start_time is None]

        if missing_start_time:
            issue = (
                f"Part '{part_name}' has {len(missing_start_time)} notes "
                f"missing start_time out of {len(notes_only)} total notes"
            )
            result.issues.append(issue)
            if part_name not in result.parts_with_issues:
                result.parts_with_issues[part_name] = []
            result.parts_with_issues[part_name].append(
                f"Missing start_time on {len(missing_start_time)} notes"
            )

        # Check for polyphony (chords) - count same start_time
        start_time_counts = defaultdict(int)
        for n in notes_only:
            if n.start_time is not None:
                start_time_counts[round(n.start_time, 3)] += 1

        chord_count = sum(1 for count in start_time_counts.values() if count >= 2)
        total_chords_found += chord_count

        if auto_fix and missing_start_time:
            # Fix the part
            if isinstance(part, dict):
                # Convert dict to AIPart for fixing
                temp_part = AIPart(**part)
                fixed = fix_polyphony(temp_part)
                # Update the dict with fixed values
                for i, note_dict in enumerate(part.get("notes", [])):
                    if not note_dict.get("rest") and i < len(fixed.notes):
                        fixed_note = fixed.notes[i]
                        if isinstance(fixed_note, AINote):
                            note_dict["start_time"] = fixed_note.start_time
            else:
                fixed = fix_polyphony(part)

            fixed_parts.append(part_name)

    # Determine overall validity
    result.is_valid = len(result.issues) == 0

    # Log summary
    if total_parts_checked > 0:
        if result.is_valid:
            logger.info(
                f"Polyphony validation passed: {total_parts_checked} harmony parts checked, "
                f"{total_chords_found} chords detected"
            )
        else:
            logger.warning(
                f"Polyphony validation issues found in {len(result.parts_with_issues)} parts. "
                f"Total chords detected: {total_chords_found}"
            )

            if auto_fix and fixed_parts:
                logger.info(f"Auto-fixed polyphony for parts: {', '.join(fixed_parts)}")

    return result


def auto_fix_composition(composition: Any) -> Any:
    """Automatically fix all polyphony issues in a composition.

    Convenience function that runs validation with auto_fix=True.

    Args:
        composition: AIComposition or dict with parts

    Returns:
        The composition with fixes applied (in-place modification)
    """
    validate_composition(composition, auto_fix=True)
    return composition


def get_polyphony_report(part: AIPart) -> dict[str, Any]:
    """Generate a detailed report of polyphony in a part.

    Args:
        part: The part to analyze

    Returns:
        Dictionary with polyphony statistics
    """
    note_events = part.get_note_events()
    notes_only = [n for n in note_events if isinstance(n, AINote)]

    # Count notes at each start time
    start_time_groups = defaultdict(list)
    for note in notes_only:
        key = round(note.start_time, 3) if note.start_time is not None else None
        start_time_groups[key].append(note)

    # Find chords (2+ notes at same time)
    chords = {
        time: notes
        for time, notes in start_time_groups.items()
        if time is not None and len(notes) >= 2
    }

    # Calculate statistics
    max_chord_size = max(len(notes) for notes in chords.values()) if chords else 0
    total_chord_notes = sum(len(notes) for notes in chords.values())

    return {
        "part_name": part.name,
        "role": part.role,
        "total_notes": len(notes_only),
        "notes_without_start_time": sum(
            1 for n in notes_only if n.start_time is None
        ),
        "unique_start_times": len(start_time_groups) - (1 if None in start_time_groups else 0),
        "chord_count": len(chords),
        "max_chord_size": max_chord_size,
        "total_chord_notes": total_chord_notes,
        "chord_times": sorted(chords.keys()),
    }
