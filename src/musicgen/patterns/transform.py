"""
Pattern transformation functions for TidalCycles-style manipulation.

These functions transform patterns in various ways, similar to TidalCycles.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from musicgen.patterns.parser import Pattern, PatternEvent

if TYPE_CHECKING:
    from collections.abc import Callable


def slow(pattern: Pattern, factor: float = 2.0) -> Pattern:
    """
    Slow down a pattern by the given factor.

    Args:
        pattern: The pattern to transform
        factor: How much to slow (2.0 = half speed)

    Returns:
        A new slowed pattern
    """
    new_events = [
        PatternEvent(
            value=e.value,
            duration=e.duration * factor,
            velocity=e.velocity,
        )
        for e in pattern.events
    ]
    return Pattern(
        events=new_events,
        length=pattern.length * factor,
        time_signature=pattern.time_signature,
    )


def fast(pattern: Pattern, factor: float = 2.0) -> Pattern:
    """
    Speed up a pattern by the given factor.

    Args:
        pattern: The pattern to transform
        factor: How much to speed up (2.0 = double speed)

    Returns:
        A new sped-up pattern
    """
    return slow(pattern, 1.0 / factor)


def density(pattern: Pattern, factor: float = 0.5) -> Pattern:
    """
    Change the density of a pattern (sparse vs dense).

    Args:
        pattern: The pattern to transform
        factor: Density factor (0.0 = silent, 1.0 = unchanged, >1 = more dense)

    Returns:
        A new pattern with adjusted density
    """
    if factor <= 0:
        return Pattern(events=[], length=pattern.length, time_signature=pattern.time_signature)

    if factor == 1.0:
        return pattern

    # Filter events based on density
    new_events = []
    for i, event in enumerate(pattern.events):
        if event.value and (i * factor) % 1 < factor:
            new_events.append(event)

    return Pattern(
        events=new_events,
        length=pattern.length,
        time_signature=pattern.time_signature,
    )


def rev(pattern: Pattern) -> Pattern:
    """
    Reverse a pattern.

    Args:
        pattern: The pattern to reverse

    Returns:
        A new reversed pattern
    """
    new_events = list(reversed(pattern.events))
    return Pattern(
        events=new_events,
        length=pattern.length,
        time_signature=pattern.time_signature,
    )


def palindrome(pattern: Pattern) -> Pattern:
    """
    Create a palindrome (ABA structure) from a pattern.

    Args:
        pattern: The source pattern

    Returns:
        A new palindromic pattern
    """
    new_events = pattern.events + list(reversed(pattern.events))
    return Pattern(
        events=new_events,
        length=pattern.length * 2,
        time_signature=pattern.time_signature,
    )


def rotate(pattern: Pattern, offset: int) -> Pattern:
    """
    Rotate a pattern by the given offset.

    Args:
        pattern: The pattern to rotate
        offset: Number of positions to rotate (positive = right)

    Returns:
        A new rotated pattern
    """
    if not pattern.events:
        return pattern

    offset = offset % len(pattern.events)
    new_events = pattern.events[-offset:] + pattern.events[:-offset]
    return Pattern(
        events=new_events,
        length=pattern.length,
        time_signature=pattern.time_signature,
    )


def repeat(pattern: Pattern, count: int) -> Pattern:
    """
    Repeat a pattern multiple times.

    Args:
        pattern: The pattern to repeat
        count: Number of repetitions

    Returns:
        A new repeated pattern
    """
    new_events = pattern.events * count
    return Pattern(
        events=new_events,
        length=pattern.length * count,
        time_signature=pattern.time_signature,
    )


def degrade(pattern: Pattern, amount: float = 0.5) -> Pattern:
    """
    Randomly remove events from a pattern (TidalCycles-style degradation).

    Args:
        pattern: The pattern to degrade
        amount: Probability of keeping each event (0.0 = all removed, 1.0 = all kept)

    Returns:
        A new degraded pattern
    """
    import random

    new_events = []
    for event in pattern.events:
        if event.value and random.random() < amount:
            new_events.append(event)
        elif not event.value:
            # Keep rests
            new_events.append(event)

    return Pattern(
        events=new_events,
        length=pattern.length,
        time_signature=pattern.time_signature,
    )


def degrade_by(pattern: Pattern, func: Callable[[float], float]) -> Pattern:
    """
    Degrade a pattern using a function to determine probability.

    Args:
        pattern: The pattern to degrade
        func: Function that takes position (0-1) and returns keep probability

    Returns:
        A new degraded pattern
    """
    import random

    if not pattern.events:
        return pattern

    new_events = []
    for i, event in enumerate(pattern.events):
        position = i / len(pattern.events)
        probability = func(position)
        if event.value and random.random() < probability or not event.value:
            new_events.append(event)

    return Pattern(
        events=new_events,
        length=pattern.length,
        time_signature=pattern.time_signature,
    )
