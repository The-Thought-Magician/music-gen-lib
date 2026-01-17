# V3-07: Validation Tools for Music Theory Rules

**Status:** Pending
**Priority:** High
**Dependencies:** V3-05, V3-06

## Overview

Create automated validation tools that check AI-generated compositions against music theory rules, catching errors like parallel fifths, unresolved tendency tones, and orchestration issues before rendering.

## Philosophy

Validation should be **constructive**, not just rejecting compositions. Tools should:

1. **Identify issues** with specific locations
2. **Explain the problem** in musical terms
3. **Suggest corrections** when possible
4. **Allow flexibility** for intentional rule-breaking

---

## Validation Categories

### 1. Voice Leading Validation

```python
from typing import List, Tuple, Optional
from dataclasses import dataclass
from musicgen.ai_models import Note, InstrumentPart

@dataclass
class VoiceLeadingError:
    """A voice leading rule violation."""
    error_type: str
    voice1_index: int
    voice2_index: int
    note1_index: int
    note2_index: int
    description: str
    severity: str  # "error", "warning", "info"
    suggestion: Optional[str] = None

class VoiceLeadingValidator:
    """Validate voice leading rules between parts."""

    # Perfect intervals
    PERFECT_UNISON = 0
    PERFECT_FIFTH = 7
    PERFECT_OCTAVE = 12
    PERFECT_12TH = 19  # Octave + fifth
    DOUBLE_OCTAVE = 24

    def __init__(self, allow_exceptions: bool = True):
        """Initialize validator.

        Args:
            allow_exceptions: Allow intentional violations (marked in composition)
        """
        self.allow_exceptions = allow_exceptions

    def validate_parallel_perfect_intervals(
        self,
        parts: List[InstrumentPart],
    ) -> List[VoiceLeadingError]:
        """Check for parallel fifths and octaves.

        Parallel perfect intervals are forbidden in common practice
        because they make the voices sound like they've merged.

        Args:
            parts: List of instrument parts to validate

        Returns:
            List of voice leading errors
        """
        errors = []

        for i, part1 in enumerate(parts):
            for j, part2 in enumerate(parts):
                if j <= i:
                    continue  # Skip same part and duplicates

                part_errors = self._check_part_pair(
                    part1, part2, i, j
                )
                errors.extend(part_errors)

        return errors

    def _check_part_pair(
        self,
        part1: InstrumentPart,
        part2: InstrumentPart,
        part1_idx: int,
        part2_idx: int,
    ) -> List[VoiceLeadingError]:
        """Check a pair of parts for parallel perfect intervals."""
        errors = []

        # Align notes by time
        notes1 = part1.notes
        notes2 = part2.notes

        i = j = 0
        prev_interval = None
        prev_time = None

        while i < len(notes1) and j < len(notes2):
            note1 = notes1[i]
            note2 = notes2[j]

            # Find overlapping time point
            if note1.start_time < note2.start_time + note2.duration:
                if note2.start_time < note1.start_time + note1.duration:
                    # Notes overlap
                    interval = abs(note1.pitch - note2.pitch)

                    # Check if this is a perfect interval
                    if interval in self.PERFECT_INTERVALS:
                        if prev_interval == interval:
                            # Parallel perfect interval detected!
                            time_since_prev = note1.start_time - prev_time

                            if time_since_prev < 4.0:  # Within reasonable time
                                errors.append(VoiceLeadingError(
                                    error_type="parallel_perfect_interval",
                                    voice1_index=part1_idx,
                                    voice2_index=part2_idx,
                                    note1_index=i,
                                    note2_index=j,
                                    description=self._describe_parallel_interval(interval),
                                    severity="error",
                                    suggestion=self._suggest_parallel_fix(interval)
                                ))

                        prev_interval = interval
                        prev_time = note1.start_time

            # Advance pointers
            if note1.start_time + note1.duration <= note2.start_time + note2.duration:
                i += 1
            else:
                j += 1

        return errors

    def _describe_parallel_interval(self, interval: int) -> str:
        """Describe a parallel interval error."""
        names = {
            0: "parallel unison",
            7: "parallel fifth",
            12: "parallel octave",
            19: "parallel twelfth",
            24: "parallel double octave"
        }
        return names.get(interval, f"parallel perfect interval ({interval})")

    def _suggest_parallel_fix(self, interval: int) -> str:
        """Suggest a fix for parallel interval."""
        return (
            f"Move one voice by step to break the parallel {self._describe_parallel_interval(interval)}. "
            "Consider contrary motion (voices moving in opposite directions)."
        )

    PERFECT_INTERVALS = {0, 7, 12, 19, 24}

    def validate_direct_perfect_intervals(
        self,
        parts: List[InstrumentPart],
    ) -> List[VoiceLeadingError]:
        """Check for direct (hidden) fifths and octaves.

        Direct perfect intervals occur when both voices move by skip
        to a perfect interval.

        Returns:
            List of voice leading errors
        """
        errors = []

        for i, part1 in enumerate(parts):
            for j, part2 in enumerate(parts):
                if j <= i:
                    continue

                pair_errors = self._check_direct_intervals(
                    part1, part2, i, j
                )
                errors.extend(pair_errors)

        return errors

    def _check_direct_intervals(
        self,
        part1: InstrumentPart,
        part2: InstrumentPart,
        part1_idx: int,
        part2_idx: int,
    ) -> List[VoiceLeadingError]:
        """Check for direct perfect intervals in a part pair."""
        errors = []

        notes1 = part1.notes
        notes2 = part2.notes

        # Check note-to-note motion
        for k in range(min(len(notes1), len(notes2)) - 1):
            note1_a = notes1[k]
            note1_b = notes1[k + 1]
            note2_a = notes2[k]
            note2_b = notes2[k + 1]

            # Calculate intervals
            interval_a = abs(note1_a.pitch - note2_a.pitch)
            interval_b = abs(note1_b.pitch - note2_b.pitch)

            # Check if arriving at perfect interval
            if interval_b in self.PERFECT_INTERVALS:
                # Calculate motion
                motion1 = abs(note1_b.pitch - note1_a.pitch)
                motion2 = abs(note2_b.pitch - note2_a.pitch)

                # Both moving by skip?
                if motion1 >= 3 and motion2 >= 3:
                    errors.append(VoiceLeadingError(
                        error_type="direct_perfect_interval",
                        voice1_index=part1_idx,
                        voice2_index=part2_idx,
                        note1_index=k + 1,
                        note2_index=k + 1,
                        description=f"Direct {self._describe_parallel_interval(interval_b)} by skip",
                        severity="warning",
                        suggestion="Use stepwise motion in upper voice when approaching perfect interval by skip"
                    ))

        return errors

    def validate_leading_tone_resolution(
        self,
        parts: List[InstrumentPart],
        key_signature: str,
    ) -> List[VoiceLeadingError]:
        """Validate that leading tones resolve properly.

        The leading tone (7th scale degree) should resolve upward
        to the tonic.

        Args:
            parts: Instrument parts
            key_signature: Key signature (e.g., "C major")

        Returns:
            List of resolution errors
        """
        errors = []

        # Get leading tone pitch for key
        leading_tone = self._get_leading_tone(key_signature)
        tonic = self._get_tonic(key_signature)

        for i, part in enumerate(parts):
            part_errors = self._check_leading_tone_in_part(
                part, leading_tone, tonic, i
            )
            errors.extend(part_errors)

        return errors

    def _get_leading_tone(self, key_signature: str) -> int:
        """Get leading tone MIDI note for key."""
        # Simplified: assumes C major = 60
        key_map = {
            "C major": 71,  # B
            "G major": 70,  # F#
            "D major": 69,  # C#
            "A major": 68,  # G#
            "E major": 67,  # D#
            "B major": 66,  # A#
            "F# major": 65,  # E#
            "C# major": 64,  # D#
            "F major": 70,  # E
            "Bb major": 71,  # A
            "Eb major": 68,  # G
            "Ab major": 67,  # F
            "Db major": 66,  # C
            "Gb major": 65,  # B
            "Cb major": 64,  # Bb
            # Minor keys
            "A minor": 70,  # G#
            "E minor": 69,  # D#
            "B minor": 68,  # C#
            "F# minor": 67,  # B#
            "C# minor": 66,  # A#
            "G# minor": 65,  # Fx
            "D# minor": 64,  # Cx
            "D minor": 71,  # C#
            "G minor": 70,  # F#
            "C minor": 69,  # B
            "F minor": 68,  # E
            "Bb minor": 67,  # D#
            "Eb minor": 66,  # D
            "Ab minor": 65,  # G#
        }
        return key_map.get(key_signature, 71)

    def _get_tonic(self, key_signature: str) -> int:
        """Get tonic MIDI note for key."""
        key_map = {
            "C major": 60, "G major": 67, "D major": 62, "A major": 57,
            "E major": 64, "B major": 59, "F# major": 54, "C# major": 61,
            "F major": 53, "Bb major": 58, "Eb major": 63, "Ab major": 56,
            "Db major": 49, "Gb major": 54, "Cb major": 59,
            "A minor": 57, "E minor": 52, "B minor": 59, "F# minor": 54,
            "C# minor": 61, "G# minor": 56, "D# minor": 51,
            "D minor": 50, "G minor": 55, "C minor": 48, "F minor": 41,
            "Bb minor": 46, "Eb minor": 51, "Ab minor": 56,
        }
        return key_map.get(key_signature, 60)

    def _check_leading_tone_in_part(
        self,
        part: InstrumentPart,
        leading_tone: int,
        tonic: int,
        part_idx: int,
    ) -> List[VoiceLeadingError]:
        """Check leading tone resolution in a single part."""
        errors = []

        for i, note in enumerate(part.notes):
            # Check if this is a leading tone
            if note.pitch % 12 == leading_tone % 12:
                # Check next note
                if i + 1 < len(part.notes):
                    next_note = part.notes[i + 1]

                    # Does it resolve to tonic?
                    if next_note.pitch % 12 != tonic % 12:
                        errors.append(VoiceLeadingError(
                            error_type="unresolved_leading_tone",
                            voice1_index=part_idx,
                            voice2_index=-1,
                            note1_index=i,
                            note2_index=i + 1,
                            description=f"Leading tone at {note.start_time}s does not resolve to tonic",
                            severity="warning",
                            suggestion=f"Leading tone should step up to tonic ({tonic})"
                        ))

        return errors
```

### 2. Orchestration Validation

```python
@dataclass
class OrchestrationError:
    """An orchestration issue."""
    instrument: str
    issue_type: str
    description: str
    severity: str
    note_index: Optional[int] = None
    suggestion: Optional[str] = None

class OrchestrationValidator:
    """Validate orchestration decisions."""

    def __init__(self, instrument_definitions: dict):
        """Initialize with instrument definitions."""
        self.definitions = instrument_definitions

    def validate_range(
        self,
        part: InstrumentPart,
        dynamic: Optional[DynamicMarking] = None,
    ) -> List[OrchestrationError]:
        """Validate that notes are within instrument range.

        Args:
            part: Instrument part to validate
            dynamic: Dynamic level (affects usable range)

        Returns:
            List of range errors
        """
        errors = []
        instrument_def = self.definitions.get(part.instrument_name)

        if not instrument_def:
            return errors

        # Get appropriate range for dynamic
        if dynamic and "dynamic_ranges" in instrument_def:
            valid_range = instrument_def["dynamic_ranges"].get(dynamic)
        else:
            valid_range = instrument_def.get("range")

        if not valid_range:
            return errors

        min_pitch = valid_range["min"]
        max_pitch = valid_range["max"]

        for i, note in enumerate(part.notes):
            if note.pitch < min_pitch:
                errors.append(OrchestrationError(
                    instrument=part.instrument_name,
                    issue_type="below_range",
                    description=f"Note {note.pitch} is below {dynamic or ''} range for {part.instrument_name}",
                    severity="error",
                    note_index=i,
                    suggestion=f"Transpose up or assign to different instrument"
                ))
            elif note.pitch > max_pitch:
                errors.append(OrchestrationError(
                    instrument=part.instrument_name,
                    issue_type="above_range",
                    description=f"Note {note.pitch} is above {dynamic or ''} range for {part.instrument_name}",
                    severity="error",
                    note_index=i,
                    suggestion=f"Transpose down or assign to different instrument"
                ))

        return errors

    def validate_articulation(
        self,
        part: InstrumentPart,
    ) -> List[OrchestrationError]:
        """Validate that articulations are appropriate.

        Args:
            part: Instrument part to validate

        Returns:
            List of articulation errors
        """
        errors = []
        instrument_def = self.definitions.get(part.instrument_name)

        if not instrument_def:
            return errors

        valid_articulations = set(instrument_def.get("articulations", {}).keys())

        for note in part.notes:
            if note.articulation and note.articulation not in valid_articulations:
                errors.append(OrchestrationError(
                    instrument=part.instrument_name,
                    issue_type="invalid_articulation",
                    description=f"Articulation '{note.articulation}' not available for {part.instrument_name}",
                    severity="error",
                    suggestion=f"Available: {', '.join(valid_articulations)}"
                ))

        return errors

    def validate_balance(
        self,
        composition: Composition,
    ) -> List[OrchestrationError]:
        """Validate ensemble balance.

        Checks if certain instruments would overpower others
        based on their natural dynamics and frequency ranges.

        Args:
            composition: Full composition

        Returns:
            List of balance warnings
        """
        errors = []

        # Get all parts
        all_parts = composition.parts

        # Check if brass overpower woodwinds
        brass_parts = [p for p in all_parts if p.instrument_family == InstrumentFamily.BRASS]
        woodwind_parts = [p for p in all_parts if p.instrument_family == InstrumentFamily.WOODWINDS]

        if brass_parts and woodwind_parts:
            # Check if they're playing simultaneously at similar dynamics
            for woodwind in woodwind_parts:
                for brass in brass_parts:
                    overlap_errors = self._check_balance_conflict(woodwind, brass)
                    errors.extend(overlap_errors)

        return errors

    def _check_balance_conflict(
        self,
        part1: InstrumentPart,
        part2: InstrumentPart,
    ) -> List[OrchestrationError]:
        """Check if two parts have balance conflicts."""
        errors = []

        # Check for simultaneous notes at similar dynamics
        for note1 in part1.notes:
            for note2 in part2.notes:
                if self._notes_overlap(note1, note2):
                    if abs(note1.velocity - note2.velocity) < 20:
                        # Similar dynamics - check if problematic
                        weaker, stronger = self._identify_weaker_stronger(
                            part1, note1, part2, note2
                        )
                        if weaker and stronger:
                            errors.append(OrchestrationError(
                                instrument=stronger.instrument_name,
                                issue_type="balance_warning",
                                description=f"{stronger.instrument_name} may overpower {weaker.instrument_name}",
                                severity="warning",
                                suggestion=f"Reduce {stronger.instrument_name} dynamic or add doubling to {weaker.instrument_name}"
                            ))

        return errors

    def _notes_overlap(self, note1: Note, note2: Note) -> bool:
        """Check if two notes overlap in time."""
        return not (
            note1.start_time + note1.duration <= note2.start_time or
            note2.start_time + note2.duration <= note1.start_time
        )

    def _identify_weaker_stronger(
        self,
        part1: InstrumentPart,
        note1: Note,
        part2: InstrumentPart,
        note2: Note,
    ) -> tuple[Optional[InstrumentPart], Optional[InstrumentPart]]:
        """Identify which instrument is naturally weaker/stronger."""
        # Simplified: brass > strings > woodwinds
        strength_order = {
            InstrumentFamily.BRASS: 3,
            InstrumentFamily.PERCUSSION: 2.5,
            InstrumentFamily.STRINGS: 2,
            InstrumentFamily.WOODWINDS: 1,
            InstrumentFamily.KEYBOARDS: 1.5,
        }

        strength1 = strength_order.get(part1.instrument_family, 1)
        strength2 = strength_order.get(part2.instrument_family, 1)

        if strength1 > strength2:
            return part2, part1
        elif strength2 > strength1:
            return part1, part2
        else:
            return None, None
```

### 3. Comprehensive Validator

```python
@dataclass
class ValidationResult:
    """Complete validation result."""
    valid: bool
    voice_leading_errors: List[VoiceLeadingError] = None
    orchestration_errors: List[OrchestrationError] = None
    warnings: List[str] = None

    @property
    def error_count(self) -> int:
        """Total number of errors."""
        return len(self.voice_leading_errors) + len(self.orchestration_errors)

    @property
    def warning_count(self) -> int:
        """Total number of warnings."""
        return len(self.warnings)

class CompositionValidator:
    """Comprehensive composition validator."""

    def __init__(self, instrument_definitions: dict):
        """Initialize validator."""
        self.voice_validator = VoiceLeadingValidator()
        self.orch_validator = OrchestrationValidator(instrument_definitions)

    def validate(self, composition: Composition) -> ValidationResult:
        """Validate a complete composition.

        Args:
            composition: Composition to validate

        Returns:
            Validation result with all errors and warnings
        """
        # Validate voice leading
        voice_errors = self.voice_validator.validate_parallel_perfect_intervals(
            composition.parts
        )
        voice_errors.extend(
            self.voice_validator.validate_direct_perfect_intervals(composition.parts)
        )
        voice_errors.extend(
            self.voice_validator.validate_leading_tone_resolution(
                composition.parts,
                composition.key_signature
            )
        )

        # Validate orchestration
        orch_errors = []
        for part in composition.parts:
            orch_errors.extend(self.orch_validator.validate_range(part))
            orch_errors.extend(self.orch_validator.validate_articulation(part))

        orch_errors.extend(self.orch_validator.validate_balance(composition))

        # Collect warnings
        warnings = []
        for error in voice_errors + orch_errors:
            if error.severity == "warning":
                warnings.append(error.description)

        # Check if valid
        critical_errors = [
            e for e in voice_errors + orch_errors
            if e.severity == "error"
        ]

        return ValidationResult(
            valid=len(critical_errors) == 0,
            voice_leading_errors=voice_errors,
            orchestration_errors=orch_errors,
            warnings=warnings,
        )

    def print_report(self, result: ValidationResult) -> None:
        """Print a human-readable validation report.

        Args:
            result: Validation result
        """
        print(f"\n{'='*60}")
        print(f"Validation Report: {'PASSED' if result.valid else 'FAILED'}")
        print(f"{'='*60}")

        if result.voice_leading_errors:
            print(f"\nVoice Leading ({len(result.voice_leading_errors)} issues):")
            for error in result.voice_leading_errors:
                severity_symbol = "❌" if error.severity == "error" else "⚠️"
                print(f"  {severity_symbol} {error.description}")
                if error.suggestion:
                    print(f"     💡 {error.suggestion}")

        if result.orchestration_errors:
            print(f"\nOrchestration ({len(result.orchestration_errors)} issues):")
            for error in result.orchestration_errors:
                severity_symbol = "❌" if error.severity == "error" else "⚠️"
                print(f"  {severity_symbol} [{error.instrument}] {error.description}")
                if error.suggestion:
                    print(f"     💡 {error.suggestion}")

        if result.warnings:
            print(f"\nWarnings ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"  ⚠️ {warning}")

        print(f"\n{'='*60}\n")
```

---

## Implementation Tasks

1. [ ] Create `VoiceLeadingValidator` class
2. [ ] Create `OrchestrationValidator` class
3. [ ] Create `CompositionValidator` class
4. [ ] Add validation result models
5. [ ] Create validation report formatter
6. [ ] Add option for auto-correction suggestions
7. [ ] Write unit tests for validators

## Success Criteria

- Detects parallel fifths and octaves
- Detects unresolved leading tones
- Validates instrument ranges per dynamic
- Provides helpful suggestions
- Can be used as pre-rendering check

## Next Steps

- V3-08: Enhanced MIDI Generator
- V3-09: AI Composer Integration with Validation
