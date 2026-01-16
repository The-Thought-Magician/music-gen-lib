"""Orchestration validation for V3 compositions.

This module provides validation for orchestration issues including
instrument ranges, articulation validity, and balance between instruments.
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from musicgen.ai_models.v3.articulation import ArticulationType
from musicgen.ai_models.v3.notes import Note
from musicgen.orchestration.definitions import (
    DynamicMarking,
    get_instrument_library,
)
from musicgen.validation.models import ValidationResult, ValidationSeverity

if TYPE_CHECKING:
    from musicgen.ai_models.v3.composition import Composition
    from musicgen.ai_models.v3.parts import InstrumentPart


# Articulation types by instrument family
STRING_ARTICULATIONS = {
    ArticulationType.LEGATO,
    ArticulationType.DETACHE,
    ArticulationType.STACCATO,
    ArticulationType.SPICCATO,
    ArticulationType.MARCATO,
    ArticulationType.PIZZICATO,
    ArticulationType.TREMOLO,
    ArticulationType.TRILL,
    ArticulationType.SUL_TASTO,
    ArticulationType.SUL_PONTICELLO,
    ArticulationType.COL_LEGNO,
    ArticulationType.HARMONIC,
    ArticulationType.VIBRATO,
    ArticulationType.SENZA_VIBRATO,
}

WOODWIND_ARTICULATIONS = {
    ArticulationType.LEGATO_WW,
    ArticulationType.STACCATO_WW,
    ArticulationType.FLUTTER_TONGUE,
    ArticulationType.FLUTTER_WW,
    ArticulationType.BREATH_ATTACK,
    ArticulationType.STACCATO,
    ArticulationType.LEGATO,
    ArticulationType.TRILL,
    ArticulationType.TREMOLO,
}

BRASS_ARTICULATIONS = {
    ArticulationType.LEGATO_BRASS,
    ArticulationType.STACCATO_BRASS,
    ArticulationType.MARTELLO,
    ArticulationType.MUTED,
    ArticulationType.FALL,
    ArticulationType.DOIT,
    ArticulationType.SHAKE,
    ArticulationType.FLIP,
    ArticulationType.SMEAR,
    ArticulationType.HALF_VALVE,
    ArticulationType.STACCATO,
    ArticulationType.LEGATO,
    ArticulationType.TRILL,
}

GENERAL_ARTICULATIONS = {
    ArticulationType.NORMAL,
    ArticulationType.ACCENT,
    ArticulationType.MARCATO_SHORT,
    ArticulationType.TENUTO,
    ArticulationType.SFORZANDO,
    ArticulationType.SFP,
    ArticulationType.FP,
    ArticulationType.RINFORZANDO,
}

# Family to articulations mapping
FAMILY_ARTICULATIONS = {
    "strings": STRING_ARTICULATIONS | GENERAL_ARTICULATIONS,
    "woodwinds": WOODWIND_ARTICULATIONS | GENERAL_ARTICULATIONS,
    "brass": BRASS_ARTICULATIONS | GENERAL_ARTICULATIONS,
    "percussion": GENERAL_ARTICULATIONS,
    "keyboards": GENERAL_ARTICULATIONS,
    "electronic": GENERAL_ARTICULATIONS,
    "voices": GENERAL_ARTICULATIONS,
}

# Dynamic balance warnings (velocity ratios)
BALANCE_THRESHOLD_RATIO = 2.5  # Warn if one instrument is 2.5x louder


class OrchestrationValidator:
    """Validator for orchestration issues in compositions.

    Checks for:
    - Notes outside instrument range (considering dynamics)
    - Invalid articulations for instrument family
    - Balance issues between instruments
    """

    def __init__(
        self,
        check_ranges: bool = True,
        check_articulations: bool = True,
        check_balance: bool = True,
        strictness: str = "standard",
    ) -> None:
        """Initialize the orchestration validator.

        Args:
            check_ranges: Enable range checking
            check_articulations: Enable articulation validation
            check_balance: Enable balance checking
            strictness: Validation strictness ('strict', 'standard', 'lenient')
        """
        self.check_ranges = check_ranges
        self.check_articulations = check_articulations
        self.check_balance = check_balance
        self.strictness = strictness

        # Load instrument library
        try:
            self.instrument_library = get_instrument_library()
        except FileNotFoundError:
            self.instrument_library = None

    def validate(self, composition: Composition) -> ValidationResult:
        """Validate orchestration in a composition.

        Args:
            composition: The V3 Composition to validate

        Returns:
            ValidationResult with all found issues
        """
        result = ValidationResult()

        for part in composition.parts:
            if self.check_ranges:
                self._validate_range(part, composition, result)

            if self.check_articulations:
                self._validate_articulation(part, result)

        if self.check_balance:
            self._validate_balance(composition, result)

        result.instruments_checked = len(composition.parts)
        result.total_notes = sum(len(p.notes) for p in composition.parts)

        return result

    def _validate_range(
        self,
        part: InstrumentPart,
        composition: Composition,
        result: ValidationResult,
    ) -> None:
        """Check that notes are within instrument range.

        Range limits vary by dynamic level - louder dynamics have
        expanded upper ranges but reduced lower ranges.

        Args:
            part: Instrument part to validate
            composition: Full composition for dynamic context
            result: ValidationResult to add errors to
        """
        # Get instrument definition if available
        inst_def = None
        if self.instrument_library:
            # Try to find matching instrument by name or program
            for key, inst in self.instrument_library.instruments.items():
                if (key.lower().replace(" ", "_") in
                        part.instrument_name.lower().replace(" ", "_") or
                        (inst.midi_program == part.midi_program
                         if hasattr(inst, 'midi_program') and part.midi_program
                         else False)):
                    inst_def = inst
                    break

        for note in part.notes:
            # Determine effective dynamic for this note
            dynamic = note.dynamic or self._get_dynamic_at_time(
                part, composition, note.start_time
            )

            pitch = note.pitch

            # Check against instrument definition
            if inst_def:
                if hasattr(inst_def, 'get_range_for_dynamic'):
                    range_info = inst_def.get_range_for_dynamic(dynamic)
                    min_pitch = range_info.min if hasattr(range_info, 'min') else 0
                    max_pitch = range_info.max if hasattr(range_info, 'max') else 127
                else:
                    # Use default range
                    min_pitch = inst_def.range.min if hasattr(inst_def, 'range') else 0
                    max_pitch = inst_def.range.max if hasattr(inst_def, 'range') else 127
            else:
                # Use generic MIDI range
                min_pitch, max_pitch = 0, 127

            if pitch < min_pitch:
                result.add_orchestration_error(
                    error_type="range_below",
                    instrument=part.instrument_name,
                    location=note.start_time,
                    description=(
                        f"Note {pitch} is below instrument range "
                        f"(min: {min_pitch}) at {dynamic} dynamic"
                    ),
                    severity=ValidationSeverity.ERROR,
                    suggestion=f"Transpose up by {min_pitch - pitch} semitones",
                )

            elif pitch > max_pitch:
                result.add_orchestration_error(
                    error_type="range_above",
                    instrument=part.instrument_name,
                    location=note.start_time,
                    description=(
                        f"Note {pitch} is above instrument range "
                        f"(max: {max_pitch}) at {dynamic} dynamic"
                    ),
                    severity=ValidationSeverity.ERROR,
                    suggestion=f"Transpose down by {pitch - max_pitch} semitones",
                )

    def _validate_articulation(
        self,
        part: InstrumentPart,
        result: ValidationResult,
    ) -> None:
        """Check that articulations are valid for the instrument family.

        Args:
            part: Instrument part to validate
            result: ValidationResult to add errors to
        """
        family = part.instrument_family
        valid_articulations = FAMILY_ARTICULATIONS.get(
            family, GENERAL_ARTICULATIONS
        )

        for note in part.notes:
            if note.articulation:
                articulation = ArticulationType(note.articulation)

                if articulation not in valid_articulations:
                    result.add_orchestration_error(
                        error_type="invalid_articulation",
                        instrument=part.instrument_name,
                        location=note.start_time,
                        description=(
                            f"Articulation '{articulation.value}' is not "
                            f"typically used for {family} instruments"
                        ),
                        severity=ValidationSeverity.WARNING,
                        suggestion=(
                            f"Consider using one of: "
                            f"{', '.join(a.value for a in valid_articulations if a.value)}"
                        ),
                    )

    def _validate_balance(
        self,
        composition: Composition,
        result: ValidationResult,
    ) -> None:
        """Check for balance issues between instruments.

        Compares average velocities and warns if instruments are
        consistently imbalanced.

        Args:
            composition: Composition to validate
            result: ValidationResult to add errors to
        """
        # Calculate average velocity per part
        part_velocities = {}
        part_counts = {}

        for part in composition.parts:
            if not part.notes:
                continue

            total_velocity = sum(n.velocity for n in part.notes)
            part_velocities[part.instrument_name] = total_velocity
            part_counts[part.instrument_name] = len(part.notes)

        # Calculate averages
        avg_velocities = {
            name: part_velocities[name] / part_counts[name]
            for name in part_velocities
        }

        # Find the overall average
        if not avg_velocities:
            return

        overall_avg = sum(avg_velocities.values()) / len(avg_velocities)

        # Check for parts that are significantly louder or quieter
        for name, avg_vel in avg_velocities.items():
            ratio = avg_vel / overall_avg if overall_avg > 0 else 1.0

            if ratio > BALANCE_THRESHOLD_RATIO:
                result.add_orchestration_error(
                    error_type="balance_loud",
                    instrument=name,
                    location=None,
                    description=(
                        f"This instrument is significantly louder than average "
                        f"(ratio: {ratio:.1f}x)"
                    ),
                    severity=ValidationSeverity.WARNING,
                    suggestion="Consider reducing dynamics or velocity",
                )
            elif ratio < (1 / BALANCE_THRESHOLD_RATIO):
                result.add_orchestration_error(
                    error_type="balance_quiet",
                    instrument=name,
                    location=None,
                    description=(
                        f"This instrument is significantly quieter than average "
                        f"(ratio: {ratio:.1f}x)"
                    ),
                    severity=ValidationSeverity.WARNING,
                    suggestion="Consider increasing dynamics or velocity",
                )

        # Check for specific balance issues between instrument families
        self._check_family_balance(composition, avg_velocities, result)

    def _check_family_balance(
        self,
        composition: Composition,
        avg_velocities: dict[str, float],
        result: ValidationResult,
    ) -> None:
        """Check balance issues between instrument families.

        Args:
            composition: Composition to validate
            avg_velocities: Average velocity per instrument
            result: ValidationResult to add errors to
        """
        # Group by family
        family_velocities = defaultdict(list)

        for part in composition.parts:
            if part.instrument_name in avg_velocities:
                family_velocities[part.instrument_family].append(
                    avg_velocities[part.instrument_name]
                )

        # Calculate family averages
        family_avgs = {
            family: sum(vels) / len(vels)
            for family, vels in family_velocities.items()
            if vels
        }

        # Check if strings are drowning out woodwinds (common issue)
        if "strings" in family_avgs and "woodwinds" in family_avgs:
            ratio = family_avgs["strings"] / family_avgs["woodwinds"]
            if ratio > BALANCE_THRESHOLD_RATIO:
                result.add_orchestration_error(
                    error_type="balance_family",
                    instrument="strings",
                    location=None,
                    description=(
                        f"Strings are {ratio:.1f}x louder than woodwinds"
                    ),
                    severity=ValidationSeverity.INFO,
                    suggestion="Balance woodwinds with strings or reduce string dynamics",
                )

    def _get_dynamic_at_time(
        self,
        part: InstrumentPart,
        composition: Composition,
        time: float,
    ) -> str:
        """Get the effective dynamic marking at a given time.

        Args:
            part: Instrument part
            composition: Full composition with dynamic changes
            time: Time in seconds

        Returns:
            Dynamic marking string
        """
        # Check composition-level dynamic changes
        for dyn_change in composition.dynamic_changes:
            if dyn_change.time <= time:
                return dyn_change.dynamic

        # Default to mf
        return "mf"
