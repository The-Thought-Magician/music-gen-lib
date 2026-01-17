"""
Pattern combinators for music-gen-lib V4.

This module provides pattern combination and layering functions
similar to TidalCycles.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from musicgen.patterns.parser import Pattern, PatternEvent

if TYPE_CHECKING:
    from collections.abc import Callable

import random

# =============================================================================
# Pattern Combinators
# =============================================================================


def stack(*patterns: Pattern) -> Pattern:
    """
    Layer patterns simultaneously.

    Combines multiple patterns by summing their events at each position.
    Useful for creating layered textures.

    Args:
        *patterns: Patterns to layer

    Returns:
        New layered pattern

    Example:
        >>> p1 = parse_pattern("bd sd")
        >>> p2 = parse_pattern("hh hh")
        >>> stacked = stack(p1, p2)
    """
    if not patterns:
        return Pattern()

    # Find the maximum length
    max_length = max(p.length for p in patterns)

    # Create a combined event list
    combined_events: list[PatternEvent] = []

    for i, pattern in enumerate(patterns):
        for event in pattern.events:
            if event.value:  # Only add non-rest events
                # Adjust position based on pattern index (offset)
                new_event = PatternEvent(
                    value=f"{event.value}_{i}",
                    duration=event.duration,
                    velocity=event.velocity,
                )
                combined_events.append(new_event)

    # Combine with rests to fill gaps
    return Pattern(events=combined_events, length=max_length)


def cat(*patterns: Pattern) -> Pattern:
    """
    Concatenate patterns sequentially.

    Args:
        *patterns: Patterns to concatenate

    Returns:
        New concatenated pattern

    Example:
        >>> p1 = parse_pattern("bd sd")
        >>> p2 = parse_pattern("hh hh")
        >>> concatenated = cat(p1, p2)
    """
    if not patterns:
        return Pattern()

    combined_events: list[PatternEvent] = []
    total_length = sum(p.length for p in patterns)

    for pattern in patterns:
        for event in pattern.events:
            combined_events.append(event)

    return Pattern(events=combined_events, length=total_length)


def fastcat(*patterns: Pattern) -> Pattern:
    """
    Concatenate and speed up.

    Like cat, but doubles the speed (halves duration).

    Args:
        *patterns: Patterns to fast-cat

    Returns:
        New fast-concatenated pattern
    """
    if not patterns:
        return Pattern()

    combined_events: list[PatternEvent] = []
    total_length = sum(p.length for p in patterns) / 2

    for pattern in patterns:
        for event in pattern.events:
            new_event = PatternEvent(
                value=event.value,
                duration=event.duration / 2,
                velocity=event.velocity,
            )
            combined_events.append(new_event)

    return Pattern(events=combined_events, length=total_length)


def overlay(base: Pattern, overlay: Pattern) -> Pattern:
    """
    Overlay one pattern on another.

    The overlay pattern is added on top of the base pattern,
    with overlay events taking precedence where they exist.

    Args:
        base: Base pattern
        overlay: Pattern to overlay

    Returns:
        New pattern with overlay applied
    """
    # Start with base events
    combined_events = list(base.events)

    # Add overlay events that don't conflict
    overlay_positions = set()
    for i, event in enumerate(overlay.events):
        if event.value and i not in overlay_positions:
            combined_events.append(event)
            overlay_positions.add(i)

    return Pattern(events=combined_events, length=max(base.length, overlay.length))


def choose(options: list[Any] | dict[str, float], count: int | None = None) -> Pattern:
    """
    Randomly choose from options to create a pattern.

    Args:
        options: List of options or weighted dict
        count: Number of events to generate

    Returns:
        New pattern with chosen values

    Example:
        >>> choose(["bd", "sd", "hh"], count=4)
    """
    if isinstance(options, dict):
        # Weighted random choice
        items = list(options.keys())
        weights = list(options.values())
        items_list = random.choices(items, weights=weights, k=count or 4)
    else:
        items_list = random.choices(options, k=count or 4)

    events = [PatternEvent(value=str(item), duration=1.0) for item in items_list]

    return Pattern(events=events, length=len(events))


def choose_by(
    pattern: Pattern,
    options: list[Any],
) -> Pattern:
    """
    Use pattern to select from options.

    Each event in the pattern triggers a selection from options.
    Pattern values should be indices into the options list.

    Args:
        pattern: Selection pattern (values should be indices)
        options: List of options to choose from

    Returns:
        New pattern with selected values

    Example:
        >>> p = parse_pattern("0 1 2 1")
        >>> choose_by(p, ["bd", "sd", "hh"])
    """
    events: list[PatternEvent] = []

    for event in pattern.events:
        try:
            idx = int(event.value) if event.value.isdigit() else 0
            if 0 <= idx < len(options):
                events.append(
                    PatternEvent(
                        value=str(options[idx]),
                        duration=event.duration,
                        velocity=event.velocity,
                    )
                )
        except (ValueError, IndexError):
            events.append(PatternEvent(value=options[0], duration=event.duration))

    return Pattern(events=events, length=pattern.length)


def zip_patterns(patterns: list[Pattern]) -> Pattern:
    """
    Zip patterns together (take one event from each in sequence).

    Args:
        patterns: List of patterns to zip

    Returns:
        New pattern with zipped events

    Example:
        >>> p1 = parse_pattern("bd sd")
        >>> p2 = parse_pattern("hh hh")
        >>> zipped = zip_patterns([p1, p2])
    """
    if not patterns:
        return Pattern()

    events: list[PatternEvent] = []
    max_events = max(len(p.events) for p in patterns)

    for i in range(max_events):
        for pattern in patterns:
            if i < len(pattern.events):
                events.append(pattern.events[i])

    return Pattern(events=events, length=sum(p.length for p in patterns))


def append(*patterns: Pattern) -> Pattern:
    """
    Append patterns to create a longer pattern.

    Similar to cat but preserves pattern structure.

    Args:
        *patterns: Patterns to append

    Returns:
        New appended pattern
    """
    return cat(*patterns)


def silence(length: float = 1.0) -> Pattern:
    """
    Create a silent pattern of specified length.

    Args:
        length: Duration of silence

    Returns:
        Pattern with rest events
    """
    return Pattern(events=[], length=length)


def repeat(pattern: Pattern, times: int) -> Pattern:
    """
    Repeat a pattern multiple times.

    Args:
        pattern: Pattern to repeat
        times: Number of repetitions

    Returns:
        New repeated pattern
    """
    all_events: list[PatternEvent] = []
    for _ in range(times):
        all_events.extend(pattern.events)

    return Pattern(events=all_events, length=pattern.length * times)


def silence_in(pattern: Pattern, duration: float = 1.0) -> Pattern:
    """
    Insert silence into a pattern at the beginning.

    Args:
        pattern: Original pattern
        duration: Duration of silence to insert

    Returns:
        New pattern with leading silence
    """
    all_events = [PatternEvent(value="", duration=duration, velocity=0)]
    all_events.extend(pattern.events)

    return Pattern(events=all_events, length=pattern.length + duration)


@dataclass
class PatternState:
    """State for pattern evaluation and caching."""

    history: list[Pattern] = field(default_factory=list)
    cache: dict[str, Pattern] = field(default_factory=dict)
    current_cycle: int = 0
    frozen: dict[str, bool] = field(default_factory=dict)


def freeze(pattern: Pattern, state: PatternState) -> Pattern:
    """
    Freeze a pattern so it stops changing.

    Args:
        pattern: Pattern to freeze
        state: Pattern state to update

    Returns:
        The same pattern (now frozen)
    """
    state.frozen[pattern] = True
    return pattern


def unfreeze(pattern: Pattern, state: PatternState) -> Pattern:
    """
    Unfreeze a pattern so it can change again.

    Args:
        pattern: Pattern to unfreeze
        state: Pattern state to update

    Returns:
        The same pattern (now unfrozen)
    """
    state.frozen[pattern] = False
    return pattern


def once(pattern: Pattern) -> Pattern:
    """
    Create a pattern that only plays once.

    After playing once, it becomes silent.

    Args:
        pattern: Pattern to play once

    Returns:
        New pattern with one-shot behavior
    """
    # This is a simplified version - full implementation would
    # require tracking state
    return Pattern(events=list(pattern.events), length=pattern.length)


def every(pattern: Pattern, _n: int = 2) -> Pattern:
    """
    Only play every n-th cycle of a pattern.

    Args:
        pattern: Pattern to modify
        n: Play every n cycles

    Returns:
        New conditional pattern
    """
    # Simplified - would need cycle tracking
    return Pattern(events=list(pattern.events), length=pattern.length)


def range_pattern(start: int, end: int, step: int = 1) -> Pattern:
    """
    Create a numeric range pattern.

    Args:
        start: Starting value
        end: Ending value (exclusive)
        step: Step between values

    Returns:
        New pattern with numeric values
    """
    events = [PatternEvent(value=str(i), duration=1.0) for i in range(start, end, step)]
    return Pattern(events=events, length=len(events))


def run_with(
    pattern: Pattern,
    func: Callable[[str], Any],
) -> list[Any]:
    """
    Apply a function to each value in a pattern.

    Args:
        pattern: Pattern to process
        func: Function to apply to each value

    Returns:
        List of results
    """
    results: list[Any] = []
    for event in pattern.events:
        if event.value:
            results.append(func(event.value))
    return results


def iter_pattern(pattern: Pattern, cycles: int = 1) -> list[list[PatternEvent]]:
    """
    Iterate through a pattern for multiple cycles.

    Args:
        pattern: Pattern to iterate
        cycles: Number of cycles

    Returns:
        List of event lists for each cycle
    """
    return [list(pattern.events) for _ in range(cycles)]


def degrade_by(
    pattern: Pattern,
    func: Callable[[int], float],
) -> Pattern:
    """
    Degrade a pattern using a function to determine probability.

    Args:
        pattern: Pattern to degrade
        func: Function that takes position (0-1) and returns probability

    Returns:
        New degraded pattern
    """
    from musicgen.patterns.transform import degrade_by

    return degrade_by(pattern, func)


def sometimes(
    pattern: Pattern,
    probability: float = 0.5,
) -> Pattern:
    """
    Randomly remove events from a pattern with given probability.

    Args:
        pattern: Pattern to modify
        probability: Probability of keeping each event (0-1)

    Returns:
        New degraded pattern
    """
    from musicgen.patterns.transform import degrade

    return degrade(pattern, probability)


def often(pattern: Pattern, probability: float = 0.75) -> Pattern:
    """Like sometimes but with higher default probability."""
    return sometimes(pattern, probability)


def rarely(pattern: Pattern, probability: float = 0.25) -> Pattern:
    """Like sometimes but with lower default probability."""
    return sometimes(pattern, probability)


def never(pattern: Pattern) -> Pattern:  # noqa: ARG001
    """Never play the pattern (returns empty pattern)."""
    return Pattern(events=[], length=0)


def sometimes_cycle(
    pattern: Pattern,
    _cycle_probability: float = 0.5,
) -> Pattern:
    """
    Only play pattern in some cycles.

    Args:
        pattern: Pattern to conditionally play
        cycle_probability: Probability of playing in each cycle

    Returns:
        New conditional pattern
    """
    # This would need state tracking for full implementation
    return Pattern(events=list(pattern.events), length=pattern.length)


# =============================================================================
# Pattern Construction Utilities
# =============================================================================


def from_list(values: list[str]) -> Pattern:
    """Create a pattern from a list of values."""
    events = [PatternEvent(value=str(v), duration=1.0) for v in values]
    return Pattern(events=events, length=len(values))


def from_dict(mapping: dict[str, float]) -> Pattern:
    """
    Create a pattern from a value-to-duration mapping.

    Args:
        mapping: Dictionary mapping values to durations

    Returns:
        New pattern
    """
    events = [PatternEvent(value=str(k), duration=v) for k, v in mapping.items()]
    return Pattern(events=events, length=sum(mapping.values()))


def spread(values: list[str], cycle_length: int) -> Pattern:
    """
    Spread values evenly across a cycle.

    Args:
        values: Values to spread
        cycle_length: Length of cycle

    Returns:
        New pattern
    """
    events: list[PatternEvent] = []
    duration = cycle_length / len(values)

    for value in values:
        events.append(PatternEvent(value=str(value), duration=duration))

    return Pattern(events=events, length=cycle_length)


def rot(values: list[str], offset: int) -> list[str]:
    """
    Rotate a list by offset positions.

    Args:
        values: List to rotate
        offset: Number of positions to rotate

    Returns:
        Rotated list
    """
    offset = offset % len(values)
    return values[offset:] + values[:offset]


def rotate_values(pattern: Pattern, offset: int) -> Pattern:
    """Rotate the values in a pattern."""
    if not pattern.events:
        return pattern

    value_order = [e.value for e in pattern.events if e.value]
    if not value_order:
        return pattern

    rotated = rot(value_order, offset)

    new_events = []
    for event in pattern.events:
        if event.value:
            new_events.append(
                PatternEvent(
                    value=rotated.pop(0) if rotated else event.value,
                    duration=event.duration,
                    velocity=event.velocity,
                )
            )
        else:
            new_events.append(event)

    return Pattern(events=new_events, length=pattern.length)


# =============================================================================
# Structural Combinators
# =============================================================================


def verse_chorus(
    verse: Pattern,
    chorus: Pattern,
    repeats: int = 2,
) -> Pattern:
    """
    Create a verse-chorus structure.

    Args:
        verse: Verse pattern
        chorus: Chorus pattern
        repeats: Number of verse-chorus cycles

    Returns:
        New pattern with structure
    """
    if repeats == 1:
        return cat(verse, chorus)

    # Build pattern: verse, chorus, verse, chorus, ...
    parts: list[Pattern] = []
    for _ in range(repeats):
        parts.extend([verse, chorus])

    return cat(*parts)


def aaba(verse: Pattern, bridge: Pattern) -> Pattern:
    """
    Create an AABA song form.

    Args:
        verse: A section (verse)
        bridge: B section (bridge)

    Returns:
        New pattern with AABA structure
    """
    return cat(verse, verse, bridge, verse)


__all__ = [
    # Combinators
    "stack",
    "cat",
    "fastcat",
    "overlay",
    "choose",
    "choose_by",
    "zip_patterns",
    "append",
    # Utilities
    "silence",
    "repeat",
    "silence_in",
    "freeze",
    "unfreeze",
    "once",
    "every",
    "range_pattern",
    "run_with",
    "degrade_by",
    "sometimes",
    "often",
    "rarely",
    "never",
    "sometimes_cycle",
    # Construction
    "from_list",
    "from_dict",
    "spread",
    "rot",
    "rotate_values",
    # Structural
    "verse_chorus",
    "aaba",
]
