"""Main composition validator for V3 music generation.

This module provides the CompositionValidator class that integrates
voice leading and orchestration validation for complete composition
analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from typing import TYPE_CHECKING

from musicgen.validation.models import (
    OrchestrationError,
    ValidationResult,
    ValidationSeverity,
    VoiceLeadingError,
)
from musicgen.validation.orchestration import OrchestrationValidator
from musicgen.validation.voice_leading import VoiceLeadingValidator

if TYPE_CHECKING:
    from musicgen.ai_models.v3.composition import Composition


@dataclass
class ValidationConfig:
    """Configuration for validation behavior.

    Attributes:
        enable_voice_leading: Enable voice leading validation
        enable_orchestration: Enable orchestration validation
        check_parallel_fifths: Check for parallel fifths
        check_parallel_octaves: Check for parallel octaves
        check_direct_intervals: Check for direct perfect intervals
        check_leading_tone: Check leading tone resolution
        check_ranges: Check instrument ranges
        check_articulations: Check articulation validity
        check_balance: Check balance between instruments
        strictness: Validation strictness level
    """

    enable_voice_leading: bool = True
    enable_orchestration: bool = True
    check_parallel_fifths: bool = True
    check_parallel_octaves: bool = True
    check_direct_intervals: bool = True
    check_leading_tone: bool = True
    check_ranges: bool = True
    check_articulations: bool = True
    check_balance: bool = True
    strictness: str = "standard"  # strict, standard, lenient


class CompositionValidator:
    """Main validator for V3 compositions.

    Integrates VoiceLeadingValidator and OrchestrationValidator to provide
    comprehensive validation of musical compositions including voice leading
    rules and orchestration best practices.

    Example:
        >>> from musicgen.validation import CompositionValidator
        >>> validator = CompositionValidator()
        >>> result = validator.validate(composition)
        >>> validator.print_report(result)
    """

    def __init__(self, config: ValidationConfig | None = None) -> None:
        """Initialize the composition validator.

        Args:
            config: Optional validation configuration
        """
        self.config = config or ValidationConfig()

        # Initialize sub-validators
        self.voice_validator = VoiceLeadingValidator(
            check_parallel_fifths=self.config.check_parallel_fifths,
            check_parallel_octaves=self.config.check_parallel_octaves,
            check_direct_intervals=self.config.check_direct_intervals,
            check_leading_tone=self.config.check_leading_tone,
            strictness=self.config.strictness,
        )

        self.orchestration_validator = OrchestrationValidator(
            check_ranges=self.config.check_ranges,
            check_articulations=self.config.check_articulations,
            check_balance=self.config.check_balance,
            strictness=self.config.strictness,
        )

    def validate(self, composition: Composition) -> ValidationResult:
        """Validate a complete composition.

        Runs all enabled validation checks and returns a combined result.

        Args:
            composition: The V3 Composition to validate

        Returns:
            ValidationResult containing all errors and warnings
        """
        result = ValidationResult()

        # Run voice leading validation
        if self.config.enable_voice_leading:
            voice_result = self.voice_validator.validate(composition)
            result = result.merge(voice_result)

        # Run orchestration validation
        if self.config.enable_orchestration:
            orch_result = self.orchestration_validator.validate(composition)
            result = result.merge(orch_result)

        return result

    def print_report(
        self,
        result: ValidationResult,
        verbose: bool = False,
        output: StringIO | None = None,
    ) -> str | None:
        """Print a human-readable validation report.

        Args:
            result: The ValidationResult to report
            verbose: Include detailed information for each error
            output: Optional StringIO to write to (returns None if provided)

        Returns:
            String report if output is None, otherwise None
        """
        out = output or StringIO()

        # Header
        out.write("=" * 60 + "\n")
        out.write("COMPOSITION VALIDATION REPORT\n")
        out.write("=" * 60 + "\n\n")

        # Summary
        status = "PASSED" if result.is_valid else "FAILED"
        out.write(f"Status: {status}\n")
        out.write(f"Errors: {result.error_count}\n")
        out.write(f"Warnings: {result.warning_count}\n")
        out.write(f"Notes checked: {result.total_notes}\n")
        out.write(f"Instruments checked: {result.instruments_checked}\n")
        out.write("\n")

        # Voice Leading Errors
        if result.voice_leading_errors:
            out.write("-" * 40 + "\n")
            out.write("VOICE LEADING ISSUES\n")
            out.write("-" * 40 + "\n")
            for error in result.voice_leading_errors:
                out.write(f"  {error}\n")
                if verbose:
                    self._print_voice_leading_detail(error, out)
            out.write("\n")

        # Orchestration Errors
        if result.orchestration_errors:
            out.write("-" * 40 + "\n")
            out.write("ORCHESTRATION ISSUES\n")
            out.write("-" * 40 + "\n")

            # Group by instrument
            by_instrument: dict[str, list[OrchestrationError]] = {}
            for error in result.orchestration_errors:
                inst = error.instrument
                if inst not in by_instrument:
                    by_instrument[inst] = []
                by_instrument[inst].append(error)

            for instrument, errors in sorted(by_instrument.items()):
                out.write(f"\n{instrument}:\n")
                for error in errors:
                    out.write(f"  {error}\n")
                    if verbose:
                        self._print_orchestration_detail(error, out)
            out.write("\n")

        # Summary by error type
        if verbose or result.voice_leading_errors or result.orchestration_errors:
            out.write("-" * 40 + "\n")
            out.write("SUMMARY BY ERROR TYPE\n")
            out.write("-" * 40 + "\n")
            self._print_error_type_summary(result, out)
            out.write("\n")

        # Footer
        out.write("=" * 60 + "\n")
        if result.is_valid:
            out.write("Composition validation PASSED\n")
        else:
            out.write("Composition validation FAILED\n")
        out.write("=" * 60 + "\n")

        if output is None:
            return out.getvalue()
        return None

    def _print_voice_leading_detail(
        self,
        error: VoiceLeadingError,
        output: StringIO,
    ) -> None:
        """Print detailed information about a voice leading error.

        Args:
            error: The voice leading error
            output: StringIO to write to
        """
        output.write(f"    Type: {error.error_type}\n")
        output.write(f"    Time: {error.location:.2f}s\n")
        output.write(f"    Voices: {error.voice1} <-> {error.voice2}\n")

        # Add contextual explanation
        if "parallel_fifth" in error.error_type:
            output.write(
                "    Explanation: Parallel fifths are traditionally avoided "
                "in common practice harmony as they weaken the harmonic "
                "progression.\n"
            )
        elif "parallel_octave" in error.error_type:
            output.write(
                "    Explanation: Parallel octaves reduce the independence "
                "of voices and are generally avoided in four-part writing.\n"
            )
        elif "direct_fifth" in error.error_type:
            output.write(
                "    Explanation: Direct (exposed) fifths occur when outer "
                "voices move in similar motion to a perfect fifth.\n"
            )
        elif "direct_octave" in error.error_type:
            output.write(
                "    Explanation: Direct octaves occur when outer voices "
                "skip/leap in similar motion to an octave.\n"
            )
        elif "leading_tone" in error.error_type:
            output.write(
                "    Explanation: The leading tone (7th scale degree) "
                "typically resolves upward by step to the tonic.\n"
            )

    def _print_orchestration_detail(
        self,
        error: OrchestrationError,
        output: StringIO,
    ) -> None:
        """Print detailed information about an orchestration error.

        Args:
            error: The orchestration error
            output: StringIO to write to
        """
        output.write(f"    Type: {error.error_type}\n")
        if error.location is not None:
            output.write(f"    Time: {error.location:.2f}s\n")

        # Add contextual explanation
        if error.error_type == "range_below":
            output.write(
                "    Explanation: Note is below the practical range of "
                "the instrument at this dynamic level.\n"
            )
        elif error.error_type == "range_above":
            output.write(
                "    Explanation: Note is above the practical range of "
                "the instrument at this dynamic level.\n"
            )
        elif error.error_type == "invalid_articulation":
            output.write(
                "    Explanation: This articulation is not typically "
                "used for this instrument family.\n"
            )
        elif error.error_type == "balance_loud":
            output.write(
                "    Explanation: This instrument is consistently "
                "louder than the ensemble average.\n"
            )
        elif error.error_type == "balance_quiet":
            output.write(
                "    Explanation: This instrument is consistently "
                "quieter than the ensemble average.\n"
            )
        elif error.error_type == "balance_family":
            output.write(
                "    Explanation: There is a balance issue between "
                "instrument families.\n"
            )

    def _print_error_type_summary(
        self,
        result: ValidationResult,
        output: StringIO,
    ) -> None:
        """Print a summary of errors grouped by type.

        Args:
            result: The ValidationResult
            output: StringIO to write to
        """
        # Count errors by type
        type_counts: dict[str, dict[ValidationSeverity, int]] = {}

        for error in result.voice_leading_errors:
            error_type = error.error_type
            if error_type not in type_counts:
                type_counts[error_type] = {
                    ValidationSeverity.ERROR: 0,
                    ValidationSeverity.WARNING: 0,
                    ValidationSeverity.INFO: 0,
                }
            type_counts[error_type][error.severity] += 1

        for error in result.orchestration_errors:
            error_type = error.error_type
            if error_type not in type_counts:
                type_counts[error_type] = {
                    ValidationSeverity.ERROR: 0,
                    ValidationSeverity.WARNING: 0,
                    ValidationSeverity.INFO: 0,
                }
            type_counts[error_type][error.severity] += 1

        # Print sorted by error count
        for error_type, counts in sorted(
            type_counts.items(),
            key=lambda x: sum(x[1].values()),
            reverse=True
        ):
            total = sum(counts.values())
            output.write(
                f"  {error_type}: {total} "
                f"({counts[ValidationSeverity.ERROR]} errors, "
                f"{counts[ValidationSeverity.WARNING]} warnings, "
                f"{counts[ValidationSeverity.INFO]} info)\n"
            )

    def validate_to_dict(self, composition: Composition) -> dict:
        """Validate a composition and return results as a dictionary.

        Useful for JSON serialization and API responses.

        Args:
            composition: The V3 Composition to validate

        Returns:
            Dictionary with validation results
        """
        result = self.validate(composition)

        return {
            "is_valid": result.is_valid,
            "error_count": result.error_count,
            "warning_count": result.warning_count,
            "info_count": len(
                [e for e in result.voice_leading_errors + result.orchestration_errors
                 if e.severity == ValidationSeverity.INFO]
            ),
            "total_notes": result.total_notes,
            "instruments_checked": result.instruments_checked,
            "voice_leading_errors": [
                {
                    "type": e.error_type,
                    "location": e.location,
                    "voice1": e.voice1,
                    "voice2": e.voice2,
                    "description": e.description,
                    "severity": e.severity.value,
                }
                for e in result.voice_leading_errors
            ],
            "orchestration_errors": [
                {
                    "type": e.error_type,
                    "instrument": e.instrument,
                    "location": e.location,
                    "description": e.description,
                    "severity": e.severity.value,
                    "suggestion": e.suggestion,
                }
                for e in result.orchestration_errors
            ],
        }


def validate_composition(
    composition: Composition,
    config: ValidationConfig | None = None,
) -> ValidationResult:
    """Convenience function to validate a composition.

    Args:
        composition: The V3 Composition to validate
        config: Optional validation configuration

    Returns:
        ValidationResult with all errors and warnings

    Example:
        >>> from musicgen.validation import validate_composition
        >>> result = validate_composition(composition)
        >>> print(result)
    """
    validator = CompositionValidator(config)
    return validator.validate(composition)
