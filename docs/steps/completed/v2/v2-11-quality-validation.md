# Step 11: Quality Validation

## Status: COMPLETED

## Overview

Added validation to check that generated compositions meet minimum quality requirements (duration, note counts) and provide warnings when they don't.

## Problems Identified

1. **No duration checking**: Compositions could be 30 seconds without warning
2. **No note count validation**: Parts with 20 notes would pass validation
3. **No feedback**: Users couldn't tell if quality was acceptable

## Solution

### 1. Added Validation Constants (`src/musicgen/composer_new/composer.py`)

```python
# Validation constants
MIN_DURATION_SECONDS = 120  # 2 minutes minimum
MIN_MELODY_NOTES = 150
MIN_HARMONY_NOTES = 120
MIN_BASS_NOTES = 80
MIN_ACCOMPANIMENT_NOTES = 100
```

### 2. Added Quality Validation Method

```python
def _validate_composition_quality(self, composition: AIComposition) -> None:
    """Validate that composition meets minimum quality requirements."""
    duration = composition.duration_seconds

    # Check duration
    if duration < MIN_DURATION_SECONDS:
        logger.warning(
            f"Composition duration ({duration:.1f}s) is below minimum "
            f"({MIN_DURATION_SECONDS}s). The AI may not have generated enough notes."
        )

    # Check note counts per part
    for part in composition.parts:
        note_count = len(part.notes)
        role = part.role

        min_notes = 0
        if role == "melody":
            min_notes = MIN_MELODY_NOTES
        elif role == "harmony":
            min_notes = MIN_HARMONY_NOTES
        elif role == "bass":
            min_notes = MIN_BASS_NOTES
        elif role == "accompaniment":
            min_notes = MIN_ACCOMPANIMENT_NOTES
        else:
            min_notes = 80  # Default minimum

        if note_count < min_notes:
            logger.warning(
                f"Part '{part.name}' (role: {role}) has {note_count} notes, "
                f"below recommended minimum of {min_notes}. "
                f"This may result in a composition shorter than intended."
            )
```

### 3. Integrated into Generate Method

```python
def generate(
    self,
    prompt: str,
    validate: bool = True,
    return_raw: bool = False,
    validate_duration: bool = True,  # NEW
) -> AIComposition | dict[str, Any]:
    # ... generation code ...

    composition = AIComposition(**raw_response)

    # Validate duration and note counts
    if validate_duration:
        self._validate_composition_quality(composition)

    return composition
```

## Example Output

```
WARNING:musicgen.composer_new.composer:Composition duration (56.0s) is below minimum (120s).
WARNING:musicgen.composer_new.composer:Part 'violins_melody' (role: InstrumentRole.MELODY) has 75 notes, below recommended minimum of 150.
WARNING:musicgen.composer_new.composer:Part 'trumpets_harmony' (role: InstrumentRole.HARMONY) has 45 notes, below recommended minimum of 120.
INFO:musicgen.composer_new.composer:Composition quality check: 56.0s duration, 364 total notes across 6 parts
```

## Benefits

1. **Immediate feedback**: Users see warnings right after generation
2. **Debugging aid**: Helps identify which parts are under-developed
3. **Quality tracking**: Can monitor AI performance over time
4. **Retry guidance**: Informs users when regeneration might help

## Files Modified

- `src/musicgen/composer_new/composer.py` - Added validation constants and method

## Future Improvements

- Add automatic retry when validation fails
- Add option to enforce minimums (raise error instead of warning)
- Track statistics over time to identify patterns
