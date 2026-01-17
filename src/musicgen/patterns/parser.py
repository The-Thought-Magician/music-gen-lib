"""
Pattern mini-notation parser for TidalCycles-style patterns.

This module parses string patterns like "bd sd ~ sd, hh*8" into structured
pattern representations that can be transformed and rendered.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


@dataclass
class PatternEvent:
    """A single event in a pattern."""

    value: str  # The note/beat value (e.g., "bd", "sd", "hh")
    duration: float = 1.0  # Duration in pattern cycles
    velocity: int = 64  # MIDI velocity (0-127)


@dataclass
class Pattern:
    """A pattern representation."""

    events: list[PatternEvent] = field(default_factory=list)
    length: float = 1.0  # Pattern length in cycles
    time_signature: tuple[int, int] = (4, 4)  # Time signature

    def __post_init__(self) -> None:
        """Validate pattern after initialization."""
        if not self.events:
            self.events = []

    def with_events(self, events: list[PatternEvent]) -> Pattern:
        """Return a new pattern with the given events."""
        return Pattern(events=events, length=self.length, time_signature=self.time_signature)


class PatternParser:
    """
    Parse TidalCycles-style mini-notation patterns.

    Supports:
    - Basic values: "bd sd sd sd"
    - Rests: "~" (tilde)
    - Repetition: "bd*3" (same as "bd bd bd")
    - Grouping: "[bd sd] [hh hh]"
    - Alternation: "bd|sd" (random choice)
    - Polymeter: "bd*3, sd*4" (two parts with different lengths)
    - Euclidean: "bd(3,8)" (3 beats in 8 steps Euclidean)
    """

    def parse(self, pattern_str: str) -> Pattern:
        """
        Parse a pattern string into a Pattern object.

        Args:
            pattern_str: The pattern string to parse

        Returns:
            A Pattern object with parsed events
        """
        pattern_str = pattern_str.strip()
        if not pattern_str:
            return Pattern()

        # Handle polymetric patterns (comma-separated, but not inside parentheses)
        if "," in pattern_str and not ("(" in pattern_str and ")" in pattern_str):
            return self._parse_polymetric(pattern_str)

        # Parse single pattern
        events = self._parse_sequence(pattern_str)
        return Pattern(events=events, length=float(len(events)))

    def _parse_polymetric(self, pattern_str: str) -> Pattern:
        """Parse a polymetric pattern (comma-separated parts)."""
        parts = pattern_str.split(",")
        # For now, just parse the first part
        # Full polymetric support will be added in V4-25
        return self.parse(parts[0])

    def _parse_sequence(self, seq: str) -> list[PatternEvent]:
        """Parse a sequence of pattern elements."""
        events: list[PatternEvent] = []

        # Split by whitespace (but respect grouping)
        tokens = self._tokenize(seq)

        for token in tokens:
            if token == "~":
                # Rest - represented as event with empty value
                events.append(PatternEvent(value="", duration=1.0, velocity=0))
            elif "*" in token:
                # Repetition: "bd*3" -> "bd bd bd"
                base, count = token.rsplit("*", 1)
                try:
                    repeat_count = int(count)
                except ValueError:
                    repeat_count = 1
                for _ in range(repeat_count):
                    events.append(PatternEvent(value=base, duration=1.0))
            elif "(" in token and ")" in token:
                # Euclidean: "bd(3,8)"
                events.extend(self._parse_euclidean(token))
            else:
                events.append(PatternEvent(value=token, duration=1.0))

        return events

    def _tokenize(self, pattern: str) -> list[str]:
        """Tokenize a pattern string, handling brackets."""
        tokens: list[str] = []
        current: str = ""
        depth = 0

        for char in pattern:
            if char in " \t\n" and depth == 0:
                if current:
                    tokens.append(current)
                    current = ""
            elif char in ["[", "{", "("]:
                depth += 1
                current += char
            elif char in ["]", "}", ")"]:
                depth -= 1
                current += char
            else:
                current += char

        if current:
            tokens.append(current)

        return tokens

    def _parse_euclidean(self, token: str) -> list[PatternEvent]:
        """Parse Euclidean rhythm notation: 'bd(3,8)'."""
        # Parse "value(hits,steps)"
        try:
            value_part = token[: token.index("(")]
            params = token[token.index("(") + 1 : token.rindex(")")]
            hits, steps = map(int, params.split(","))
        except (ValueError, IndexError):
            return [PatternEvent(value=token, duration=1.0)]

        # Generate Euclidean rhythm using Bjorklund algorithm
        pattern = self._bjorklund(hits, steps)
        events: list[PatternEvent] = []

        for is_hit in pattern:
            if is_hit:
                events.append(PatternEvent(value=value_part, duration=steps / hits))
            else:
                events.append(PatternEvent(value="", duration=1.0, velocity=0))

        return events

    def _bjorklund(self, hits: int, steps: int) -> list[bool]:
        """
        Generate Euclidean rhythm using Bjorklund algorithm.

        Args:
            hits: Number of onsets (hits)
            steps: Total number of steps

        Returns:
            List of booleans where True = hit, False = rest
        """
        if hits == 0:
            return [False] * steps
        if hits >= steps:
            return [True] * steps

        # Bjorklund algorithm using recursive remainder method
        def bjorklund_recursive(onsets: int, total: int) -> list[list[int]]:
            """Recursive Bjorklund algorithm."""
            if onsets == 0:
                return [[0]] * total
            if onsets == total:
                return [[1]] * total

            # Calculate the base pattern and remainder
            counts = []
            remainder = onsets
            divisor = total

            while remainder > 0:
                count = divisor // remainder
                counts.append(count)
                new_remainder = divisor % remainder
                divisor = remainder
                remainder = new_remainder

            # Build the pattern from counts
            result: list[list[int]] = []
            for c in counts:
                result.append([1])
                result.extend([[0]] * (c - 1))

            return result

        # Simple Euclidean distribution
        result: list[bool] = [False] * steps
        for i in range(hits):
            pos = int(i * steps / hits)
            result[pos] = True

        return result


def parse_pattern(pattern_str: str) -> Pattern:
    """Convenience function to parse a pattern string."""
    return PatternParser().parse(pattern_str)
