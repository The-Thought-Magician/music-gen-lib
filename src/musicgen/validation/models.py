"""Data models for validation errors and results.

This module defines the data structures used for validation errors
and results in the V3 music generation system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class ValidationSeverity(str, Enum):
    """Severity levels for validation issues."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class VoiceLeadingError:
    """Represents a voice leading violation.

    Attributes:
        error_type: Type of voice leading error
        location: Time location in seconds
        voice1: First voice involved (e.g., "violin I")
        voice2: Second voice involved (e.g., "viola")
        description: Human-readable description of the error
        severity: Severity level
    """

    error_type: str
    location: float
    voice1: str
    voice2: str
    description: str
    severity: ValidationSeverity = ValidationSeverity.ERROR

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"[{self.severity.value.upper()}] {self.error_type} at "
            f"{self.location:.2f}s: {self.voice1} <-> {self.voice2} - "
            f"{self.description}"
        )


@dataclass(frozen=True)
class OrchestrationError:
    """Represents an orchestration issue.

    Attributes:
        error_type: Type of orchestration error
        instrument: Instrument name
        location: Time location in seconds (if applicable)
        description: Human-readable description of the error
        severity: Severity level
        suggestion: Optional suggestion for fixing the issue
    """

    error_type: str
    instrument: str
    location: float | None = None
    description: str = ""
    severity: ValidationSeverity = ValidationSeverity.WARNING
    suggestion: str | None = None

    def __str__(self) -> str:
        """Return string representation."""
        loc_str = f" at {self.location:.2f}s" if self.location is not None else ""
        suggestion_str = f" (Suggestion: {self.suggestion})" if self.suggestion else ""
        return (
            f"[{self.severity.value.upper()}] {self.error_type}: "
            f"{self.instrument}{loc_str} - {self.description}"
            f"{suggestion_str}"
        )


@dataclass
class ValidationResult:
    """Result of composition validation.

    Contains all errors and warnings found during validation,
    along with summary statistics.

    Attributes:
        voice_leading_errors: List of voice leading violations
        orchestration_errors: List of orchestration issues
        is_valid: Whether the composition passes all critical validations
        total_notes: Total number of notes validated
        instruments_checked: Number of instrument parts validated
    """

    voice_leading_errors: list[VoiceLeadingError] = field(default_factory=list)
    orchestration_errors: list[OrchestrationError] = field(default_factory=list)
    total_notes: int = 0
    instruments_checked: int = 0

    @property
    def is_valid(self) -> bool:
        """Check if composition passes all critical validations."""
        return all(
            error.severity != ValidationSeverity.ERROR
            for error in self.voice_leading_errors + self.orchestration_errors
        )

    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return any(
            error.severity == ValidationSeverity.WARNING
            for error in self.voice_leading_errors + self.orchestration_errors
        )

    @property
    def error_count(self) -> int:
        """Get total number of errors."""
        return len(
            [
                e for e in self.voice_leading_errors + self.orchestration_errors
                if e.severity == ValidationSeverity.ERROR
            ]
        )

    @property
    def warning_count(self) -> int:
        """Get total number of warnings."""
        return len(
            [
                e for e in self.voice_leading_errors + self.orchestration_errors
                if e.severity == ValidationSeverity.WARNING
            ]
        )

    def add_voice_leading_error(
        self,
        error_type: str,
        location: float,
        voice1: str,
        voice2: str,
        description: str,
        severity: ValidationSeverity = ValidationSeverity.ERROR,
    ) -> None:
        """Add a voice leading error.

        Args:
            error_type: Type of error
            location: Time in seconds
            voice1: First voice name
            voice2: Second voice name
            description: Error description
            severity: Severity level
        """
        self.voice_leading_errors.append(
            VoiceLeadingError(
                error_type=error_type,
                location=location,
                voice1=voice1,
                voice2=voice2,
                description=description,
                severity=severity,
            )
        )

    def add_orchestration_error(
        self,
        error_type: str,
        instrument: str,
        location: float | None = None,
        description: str = "",
        severity: ValidationSeverity = ValidationSeverity.WARNING,
        suggestion: str | None = None,
    ) -> None:
        """Add an orchestration error.

        Args:
            error_type: Type of error
            instrument: Instrument name
            location: Time in seconds (if applicable)
            description: Error description
            severity: Severity level
            suggestion: Optional suggestion for fixing
        """
        self.orchestration_errors.append(
            OrchestrationError(
                error_type=error_type,
                instrument=instrument,
                location=location,
                description=description,
                severity=severity,
                suggestion=suggestion,
            )
        )

    def get_errors_by_instrument(self, instrument: str) -> list[OrchestrationError]:
        """Get all orchestration errors for a specific instrument.

        Args:
            instrument: Instrument name to filter by

        Returns:
            List of orchestration errors for the instrument
        """
        return [e for e in self.orchestration_errors if e.instrument == instrument]

    def get_errors_by_type(self, error_type: str) -> list[VoiceLeadingError | OrchestrationError]:
        """Get all errors of a specific type.

        Args:
            error_type: Error type to filter by

        Returns:
            List of errors of the specified type
        """
        return [
            e for e in self.voice_leading_errors + self.orchestration_errors
            if e.error_type == error_type
        ]

    def merge(self, other: ValidationResult) -> ValidationResult:
        """Merge another ValidationResult into this one.

        Args:
            other: Another ValidationResult to merge

        Returns:
            A new ValidationResult with combined errors
        """
        return ValidationResult(
            voice_leading_errors=self.voice_leading_errors + other.voice_leading_errors,
            orchestration_errors=self.orchestration_errors + other.orchestration_errors,
            total_notes=self.total_notes + other.total_notes,
            instruments_checked=self.instruments_checked + other.instruments_checked,
        )

    def __str__(self) -> str:
        """Return string representation."""
        lines = [
            "Validation Result:",
            f"  Valid: {self.is_valid}",
            f"  Errors: {self.error_count}",
            f"  Warnings: {self.warning_count}",
            f"  Notes checked: {self.total_notes}",
            f"  Instruments checked: {self.instruments_checked}",
        ]
        return "\n".join(lines)
