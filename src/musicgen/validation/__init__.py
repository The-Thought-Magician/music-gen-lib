"""V3 Validation tools for music generation.

This package provides comprehensive validation for V3 compositions
including voice leading rules and orchestration best practices.

The validation system checks for:
- Voice leading errors (parallel fifths/octaves, direct intervals,
  leading tone resolution)
- Orchestration issues (range, articulation validity, balance)

Example usage:
    >>> from musicgen.validation import CompositionValidator, validate_composition
    >>>
    >>> # Create a validator
    >>> validator = CompositionValidator()
    >>> result = validator.validate(composition)
    >>> validator.print_report(result)
    >>>
    >>> # Or use the convenience function
    >>> result = validate_composition(composition)
    >>> print(result)
"""

from musicgen.validation.models import (
    OrchestrationError,
    ValidationSeverity,
    ValidationResult,
    VoiceLeadingError,
)
from musicgen.validation.orchestration import OrchestrationValidator
from musicgen.validation.validator import (
    CompositionValidator,
    ValidationConfig,
    validate_composition,
)
from musicgen.validation.voice_leading import VoiceLeadingValidator

__all__ = [
    # Models
    "ValidationResult",
    "VoiceLeadingError",
    "OrchestrationError",
    "ValidationSeverity",
    # Validators
    "VoiceLeadingValidator",
    "OrchestrationValidator",
    "CompositionValidator",
    "ValidationConfig",
    # Convenience functions
    "validate_composition",
]
