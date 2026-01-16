# Step 09: Schema Fixes

## Status: COMPLETED

## Overview

Fix schema issues that were causing validation errors and mismatches between the AI output and Pydantic models.

## Problems Identified

1. **Key signature format mismatch**: Schema showed `key: "C major"` but Pydantic model expected `{"tonic": "C", "mode": "major"}`
2. **Time signature format mismatch**: Similar issue with time signatures
3. **Invalid role values**: AI was generating combined roles like "harmony_bass" instead of valid enum values
4. **Note name parsing**: Flat notes (Eb, Bb, Ab) weren't being converted to sharps (D#, A#, G#)

## Changes Made

### 1. Schema Generator (`src/musicgen/schema/generator.py`)

```python
def _composition_schema(self) -> dict[str, Any]:
    comp = {
        "title": "string (composition title)",
        "tempo": "int (40-200 BPM)",
        "time_signature": '{"numerator": int, "denominator": int} (e.g., {"numerator": 4, "denominator": 4})',
        "key": '{"tonic": "string (note name)", "mode": "string (major/minor/dorian/etc.)"} (e.g., {"tonic": "C", "mode": "major"})',
        "parts": "array of Part objects",
    }
```

### 2. Part Schema Role Values

```python
def _part_schema(self) -> dict[str, Any]:
    return {
        "name": "string (instrument name)",
        "midi_program": "int (0-127, see instrument list)",
        "midi_channel": "int (0-15, 10 reserved for percussion)",
        "role": "string - MUST be one of: 'melody', 'harmony', 'bass', 'accompaniment', 'countermelody', 'pad', 'percussion'",
        "notes": "array of Note objects",
    }
```

### 3. Note Name Validation (`src/musicgen/ai_models/notes.py`)

Added flat-to-sharp conversion:

```python
@field_validator("note_name")
@classmethod
def validate_note_name(cls, v: str | None) -> str | None:
    if v is None:
        return None

    # Convert flats to sharps for consistency
    flat_to_sharp = {
        "Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#",
        "db": "C#", "eb": "D#", "gb": "F#", "ab": "G#", "bb": "A#",
    }

    octave = v[-1] if v[-1].isdigit() else ""
    base = v[:-1] if octave else v

    if base in flat_to_sharp:
        base = flat_to_sharp[base]

    return base + octave
```

### 4. Prompt Updates (`src/musicgen/ai_client/prompts.py`)

Added explicit section on valid roles:

```
VALID PART ROLES (use exactly these values):
- "melody" - Main melodic line
- "harmony" - Harmonic support
- "bass" - Bass line
- "accompaniment" - Background accompaniment
- "countermelody" - Secondary melodic line
- "pad" - Sustained chord pad
- "percussion" - Percussion parts

DO NOT combine roles (e.g., don't use "harmony_bass"). Use ONE valid role per part.
```

## Results

- AI now generates valid key signatures: `{"tonic": "A", "mode": "minor"}`
- AI now uses valid role values from the allowed list
- Flat notes are correctly converted to sharps for MIDI rendering
- Validation errors significantly reduced

## Files Modified

- `src/musicgen/schema/generator.py` - Fixed key and time signature formats
- `src/musicgen/ai_models/notes.py` - Added flat-to-sharp conversion
- `src/musicgen/ai_client/prompts.py` - Added valid role documentation
