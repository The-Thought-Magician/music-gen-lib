# Indian Classical Music Generation - Comprehensive Research and Solutions Document

**Document Version:** 1.0
**Date:** 2025-01-17
**Author:** Research Compilation for music-gen-lib
**Based on:** Analysis of AI-generated composition issues

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Part 1: AI Composition Issues - Research and Solutions](#part-1-ai-composition-issues-a1-a6))
3. [Part 2: MIDI and Sound Engine Issues - Research and Solutions](#part-2-midi-and-sound-engine-issues-b1-b4))
4. [Part 3: Missing Musical Elements - Research and Solutions](#part-3-missing-musical-elements-c1-c3))
5. [Part 4: Complete Implementation Specifications](#part-4-complete-implementation-specifications)
6. [Part 5: Code Modules to Implement](#part-5-code-modules-to-implement)
7. [Part 6: Research Sources and References](#part-6-research-sources-and-references)
8. [Part 7: Testing and Validation Criteria](#part-7-testing-and-validation-criteria)

---

## Executive Summary

This document provides comprehensive research findings and concrete solutions for addressing the "boring" or inauthentic sound of AI-generated Indian classical music. The research spans three major categories: AI composition issues, MIDI/sound engine limitations, and missing musical elements.

### Key Findings Summary

| Category | Issues Identified | Root Cause | Priority |
|----------|------------------|------------|----------|
| AI Composition | 6 issues | Insufficient prompt guidelines, missing domain knowledge | HIGH |
| MIDI/Sound | 4 issues | GM limitations, incorrect mapping | MIXED |
| Musical Elements | 3 issues | No raga/tala knowledge base | HIGH |

### Impact Quantification

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Total notes (8.6 min) | 315 | 800-1200 | 3-4x too few |
| Notes per minute | 36.6 | 100-150 | 3-4x too few |
| Avg note duration | 2.2 beats | 0.5-1.0 beats | 2-4x too long |
| Ornamentation events | 0 | 200+ | 100% missing |
| Tanpura notes | 2 | 4-5 continuous | N/A |
| Rhythmic patterns | 4-5 | 20+ | 4x too few |

---

## Part 1: AI Composition Issues (A1-A6)

---

### Issue A1: Critically Low Note Count

#### Research Findings

**Current State Analysis:**
- Generated composition: "Udaya: The Dawn of Freedom"
- Duration: 516 seconds (8.6 minutes)
- Tempo: 80 BPM (with changes to 110, 130, 90)
- Total notes generated: 315 notes
- Notes per minute: ~36.6

**Note Count by Instrument:**
| Instrument | Note Count | Avg Duration (beats) | Long Notes (≥2 beats) |
|------------|------------|---------------------|----------------------|
| Sitar      | 182        | 2.20                | 70% of first 10      |
| Bansuri    | 51         | 3.60                | 100% of first 10     |
| Tabla      | 80         | 0.50                | 0% of first 10       |
| Tanpura    | 2          | 344.00              | 2 very long notes    |
| **Total**  | **315**    |                     |                      |

**Authentic Indian Classical Music Standards:**

Based on research of performance practices and ornamentation techniques:

| Performance Style | Notes per Minute | Notes per Beat | Characteristic |
|-------------------|------------------|----------------|----------------|
| Alap (slow)       | 30-50            | 0.5-0.8        | Sustained, meend |
| Vilambit (slow)   | 60-80            | 1.0-1.5        | Medium density |
| Madhya (medium)   | 80-120           | 1.5-2.0        | More ornamented |
| Drut (fast)       | 120-200          | 2.0-3.5        | Very dense |

**Sitar Performance Specifics:**
- Fast passages (gat): 8-16 notes per beat possible
- Typical performance: 4-8 notes per beat average
- With ornamentation: Effective density doubles

**Root Cause Analysis:**
1. System prompt specifies: "150-300 notes per part" - too low for Indian classical
2. AI interprets "classical" as "slow, sparse" rather than "ornamented, intricate"
3. No genre-specific note density guidelines
4. Minimum note counts not tied to tempo or performance style

#### Proposed Solution

**File:** `src/musicgen/ai_client/prompts.py`

**Add to system instructions:**

```python
INDIAN_CLASSICAL_NOTE_DENSITY_GUIDELINES = """
INDIAN CLASSICAL NOTE DENSITY REQUIREMENTS:

For Indian classical compositions (raga-based), you MUST generate significantly
more notes than Western classical music. Indian music is characterized by dense
ornamentation and rapid melodic passages.

NOTE COUNT BY TEMPO (per 5-minute composition):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For Vilambit (Slow - 40-60 BPM):
- Melody parts (sitar/sarod/santoor): 350-500 notes minimum
- Tabla: 250-400 notes minimum
- Bansuri/flute: 200-350 notes minimum

For Madhya Laya (Medium - 70-90 BPM):
- Melody parts: 450-600 notes minimum
- Tabla: 350-500 notes minimum
- Bansuri/flute: 300-450 notes minimum

For Drut (Fast - 100+ BPM):
- Melody parts: 600-900 notes minimum
- Tabla: 500-700 notes minimum
- Bansuri/flute: 400-600 notes minimum

NOTE DURATION DISTRIBUTION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For authentic Indian classical feel:
- 60% short notes (0.25-0.5 beats) - rapid passages, ornaments
- 25% medium notes (0.5-1.0 beats) - standard melody
- 10% long notes (1.0-2.0 beats) - important notes, pauses
- 5% very long notes (2.0+ beats) - only for drone (tanpura) or special emphasis

AVOID:
- Whole notes (4.0 beats) in melody parts - reserve for tanpura only
- Consecutive long notes - breaks the rhythmic flow
- Sparse sections - every beat should have activity in at least one part

CALCULATION EXAMPLE:
At 80 BPM for 3 minutes:
- Total quarter beats = 80 × 3 = 240 beats
- For melody at 2 notes/beat average: 480 notes needed
- With rests and spacing: 400 notes is acceptable minimum
"""
```

**Add to user prompt template:**

```python
INDIAN_NOTE_DENSITY_USER_PROMPT = """
INDIAN CLASSICAL COMPOSITION - NOTE DENSITY REQUIREMENTS:

Your composition MUST meet these minimum note counts:

FOR {tempo} BPM:
- Melody parts: {min_melody_notes} notes MINIMUM
- Tabla: {min_tabla_notes} notes MINIMUM
- Tanpura: 4-5 continuous overlapping drone notes

Remember: Indian classical music is DENSE with ornamentation. When in doubt,
add more notes with shorter durations. A boring composition has too few notes.
"""
```

---

### Issue A2: Excessively Long Note Durations

#### Research Findings

**Current Output Analysis:**

Sitar first 10 note durations:
```
4.0, 3.0, 1.0, 2.0, 1.0, 1.0, 2.0, 2.0, 4.0, 2.0 beats
Average: 2.2 beats
```

Bansuri first 10 durations:
```
All 2.0+ beats
Average: 3.6 beats
```

**Why This Creates "Boring" Music:**
1. No rhythmic variety or forward momentum
2. Melody drags without pulse
3. Missing characteristic rapid passages (gat)
4. No space for ornamentation between notes

**Indian Classical Rhythmic Principles:**

From research sources (Raga Junglism, various rhythm texts):

| Concept | Description | Beat Pattern |
|---------|-------------|--------------|
| **Tihai** | Thrice-repeated phrase ending on sam | Various |
| **Bolan** | Rhythmic syllable pattern | Specific to tala |
| **Layakari** | Speed within speed | 2x, 3x, 4x density |
| **Sawal-Jawab** | Call and response phrases | Question-answer |

**Authentic Duration Patterns:**

Alap (free rhythm):
- Long sustained notes with meend: 2.0-4.0 beats
- Grace notes: 0.125-0.25 beats
- Transition notes: 0.5-1.0 beats

Vilambit Gat (slow, composed):
- Main melody: 0.5-1.0 beats
- Ornaments: 0.125-0.25 beats
- Important resolution notes: 1.5-2.0 beats

Drut Gat (fast):
- Rapid passages: 0.125-0.25 beats (16th/32nd notes)
- Gamaka tremolo: 0.125 beats repeated
- Resolution notes: 0.5-1.0 beats

#### Proposed Solution

**File:** `src/musicgen/ai_client/indian_rhythm.py` (NEW)

```python<arg_value>"""
Indian classical rhythm patterns and duration guidelines.

This module provides authentic rhythmic patterns for Indian classical music
generation, including tala cycles, bol patterns, and duration distributions.
"""

from dataclasses import dataclass
from typing import Literal
import random

@dataclass
class RhythmPattern:
    """A rhythmic pattern with durations and accents."""
    name: str
    durations: list[float]
    accents: list[int]  # 0=none, 1=medium, 2=strong
    description: str

@dataclass
class Tala:
    """Indian rhythmic cycle definition."""
    name: str
    beat_count: int
    divisions: list[int]
    theka: list[str]
    accent_pattern: list[int]
    matra_pattern: list[float]


# =============================================================================
# Indian Duration Patterns
# =============================================================================

INDIAN_DURATION_PATTERNS = {
    "alap": {
        "description": "Slow, pulse-free introduction with long sustained notes",
        "durations": {
            "long_sustain": [3.0, 4.0, 5.0],  # For important notes
            "medium_sustain": [1.5, 2.0, 2.5],  # For connecting notes
            "grace_note": [0.125, 0.25, 0.5],   # Kan-swar
            "meend_transition": [0.5, 0.75],    # Notes during glide
        },
        "distribution": {
            "long_sustain": 0.3,   # 30% long notes
            "medium_sustain": 0.4, # 40% medium
            "grace_note": 0.2,     # 20% grace
            "meend_transition": 0.1 # 10% transition
        }
    },

    "vilambit": {
        "description": "Slow tempo with clear pulse (40-60 BPM)",
        "durations": {
            "main_note": [0.5, 0.75, 1.0],      # Primary melody notes
            "ornament": [0.125, 0.25],          # Gamaka, kan-swar
            "resolution": [1.5, 2.0],           # Phrase endings
            "emphasized": [1.0, 1.25],          # Vadi/samvadi
        },
        "distribution": {
            "main_note": 0.5,      # 50% melody
            "ornament": 0.3,       # 30% ornaments
            "resolution": 0.15,    # 15% resolutions
            "emphasized": 0.05     # 5% emphasized
        }
    },

    "madhya": {
        "description": "Medium tempo (70-90 BPM)",
        "durations": {
            "main_note": [0.25, 0.5, 0.75],     # Primary melody
            "ornament": [0.0625, 0.125, 0.25],  # Dense ornaments
            "resolution": [0.75, 1.0],          # Phrase endings
            "emphasized": [0.5, 0.75],          # Vadi/samvadi
        },
        "distribution": {
            "main_note": 0.55,     # 55% melody
            "ornament": 0.35,      # 35% ornaments
            "resolution": 0.08,    # 8% resolutions
            "emphasized": 0.02     # 2% emphasized
        }
    },

    "drut": {
        "description": "Fast tempo (100+ BPM)",
        "durations": {
            "main_note": [0.125, 0.25, 0.5],    # Rapid melody
            "ornament": [0.0625, 0.125],        # Very dense ornaments
            "resolution": [0.5, 0.75],          # Quick resolutions
            "emphasized": [0.25, 0.5],          # Brief emphasis
        },
        "distribution": {
            "main_note": 0.6,      # 60% melody
            "ornament": 0.35,      # 35% ornaments
            "resolution": 0.04,    # 4% resolutions
            "emphasized": 0.01     # 1% emphasized
        }
    }
}


# =============================================================================
# Tihai Patterns (Thrice-Repeated Ending Phrases)
# =============================================================================

TIHAI_PATTERNS = {
    "simple_4": {
        "description": "Simple tihai in 4 beats",
        "pattern": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0],
        "total_beats": 4
    },
    "simple_6": {
        "description": "Simple tihai in 6 beats",
        "pattern": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0],
        "total_beats": 6
    },
    "complex_8": {
        "description": "Complex tihai in 8 beats",
        "pattern": [0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 1.0],
        "total_beats": 8
    },
    "damdar_6": {
        "description": "Damdar tihai (with pauses) in 6 beats",
        "pattern": [0.25, 0.5, 0.25, 0.5, 0.25, 0.5, 0.25, 0.5, 0.25, 0.5, 0.25, 0.5, 1.0],
        "total_beats": 6
    },
    "bedam_4": {
        "description": "Bedam tihai (without pauses) in 4 beats",
        "pattern": [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 1.0],
        "total_beats": 4
    }
}


# =============================================================================
# Gamaka Tremolo Patterns
# =============================================================================

GAMAKA_PATTERNS = {
    "slow_oscillation": {
        "description": "Slow andolan (1-2 Hz)",
        "duration": 1.0,
        "oscillations": 4,
        "pattern": [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
    },
    "medium_oscillation": {
        "description": "Medium gamaka (4-5 Hz)",
        "duration": 0.5,
        "oscillations": 4,
        "pattern": [0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625]
    },
    "fast_oscillation": {
        "description": "Fast gamaka (6-8 Hz)",
        "duration": 0.25,
        "oscillations": 4,
        "pattern": [0.03125, 0.03125, 0.03125, 0.03125, 0.03125, 0.03125, 0.03125, 0.03125]
    },
    "krintan": {
        "description": "Krintan (pull across fret)",
        "pattern": [0.125, 0.125, 0.75],  # grace-grace-main
        "interval": 2  # semitones
    },
    "murki": {
        "description": "Murki (rapid turn)",
        "pattern": [0.125, 0.125, 0.125, 0.125],  # 4-note turn
        "interval": 1  # semitone
    },
    "jamjama": {
        "description": "Jamjama (fast tremolo)",
        "pattern": [0.0625] * 16,  # 16 very rapid notes
        "total_duration": 1.0
    }
}


# =============================================================================
# Duration Pattern Generator Functions
# =============================================================================

def generate_duration_sequence(
    style: Literal["alap", "vilambit", "madhya", "drut"],
    count: int,
    seed: int | None = None
) -> list[float]:
    """Generate a sequence of durations based on Indian classical style.

    Args:
        style: The performance style (alap, vilambit, madhya, drut)
        count: Number of durations to generate
        seed: Random seed for reproducibility

    Returns:
        List of durations in beats
    """
    if seed is not None:
        random.seed(seed)

    pattern = INDIAN_DURATION_PATTERNS[style]
    durations = []
    distribution = pattern["distribution"]

    # Build weighted choice list
    choices = []
    weights = []
    for category, weight in distribution.items():
        choices.append(category)
        weights.append(weight)

    # Generate durations
    for _ in range(count):
        category = random.choices(choices, weights=weights, k=1)[0]
        duration_pool = pattern["durations"][category]
        durations.append(random.choice(duration_pool))

    return durations


def add_tihai_ending(durations: list[float], tala_beats: int = 16) -> list[float]:
    """Add a tihai ending to a duration sequence.

    Args:
        durations: Original duration sequence
        tala_beats: Total beats in tala cycle

    Returns:
        Modified sequence with tihai at the end
    """
    # Find appropriate tihai
    for tihai_name, tihai_data in TIHAI_PATTERNS.items():
        if tihai_data["total_beats"] <= tala_beats // 4:
            tihai_pattern = tihai_data["pattern"]
            break
    else:
        # Use simple tihai as fallback
        tihai_pattern = TIHAI_PATTERNS["simple_4"]["pattern"]

    return durations + tihai_pattern


def apply_gamaka_to_duration(duration: float, gamaka_type: str) -> list[float]:
    """Replace a single duration with gamaka ornament pattern.

    Args:
        duration: Original duration
        gamaka_type: Type of gamaka to apply

    Returns:
        List of durations replacing the original
    """
    pattern = GAMAKA_PATTERNS.get(gamaka_type)
    if not pattern:
        return [duration]

    # Scale pattern to match original duration
    if "pattern" in pattern:
        base_pattern = pattern["pattern"]
        pattern_total = sum(base_pattern)
        scale = duration / pattern_total
        return [d * scale for d in base_pattern]

    return [duration]


def calculate_indian_note_density(
    tempo: int,
    duration_minutes: float,
    style: Literal["alap", "vilambit", "madhya", "drut"]
) -> dict[str, int]:
    """Calculate target note counts for Indian classical composition.

    Args:
        tempo: BPM
        duration_minutes: Composition length
        style: Performance style

    Returns:
        Dictionary with target note counts by instrument type
    """
    total_beats = tempo * duration_minutes

    # Notes per beat by style
    notes_per_beat = {
        "alap": 0.8,
        "vilambit": 1.5,
        "madhya": 2.0,
        "drut": 3.0
    }

    base_note_count = int(total_beats * notes_per_beat[style])

    # Adjust by instrument type
    return {
        "melody": int(base_note_count * 1.2),      # Sitar, sarod, etc.
        "flute": int(base_note_count * 0.9),       # Bansuri
        "tabla": int(base_note_count * 1.0),       # Percussion
        "tanpura": 5,                              # Always 4-5 drone notes
        "total": base_note_count
    }


# =============================================================================
# Helper Functions for AI Prompt Integration
# =============================================================================

def get_duration_guidelines_for_prompt(tempo: int) -> str:
    """Get formatted duration guidelines for AI prompt.

    Args:
        tempo: Composition tempo

    Returns:
        Formatted string for prompt inclusion
    """
    if tempo < 60:
        style = "vilambit"
        guideline = """
FOR VILAMBIT (SLOW) TEMPO:
Use 60% medium notes (0.5-1.0 beats), 20% ornaments (0.125-0.25 beats),
15% resolutions (1.5-2.0 beats), 5% emphasized (1.0-1.25 beats).
"""
    elif tempo < 100:
        style = "madhya"
        guideline = """
FOR MADHYA (MEDIUM) TEMPO:
Use 55% medium notes (0.25-0.75 beats), 35% ornaments (0.0625-0.25 beats),
8% resolutions (0.75-1.0 beats), 2% emphasized (0.5-0.75 beats).
"""
    else:
        style = "drut"
        guideline = """
FOR DRUT (FAST) TEMPO:
Use 60% short notes (0.125-0.5 beats), 35% ornaments (0.0625-0.125 beats),
4% resolutions (0.5-0.75 beats), 1% emphasized (0.25-0.5 beats).
"""

    return guideline


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Data structures
    "RhythmPattern",
    "Tala",
    # Pattern dictionaries
    "INDIAN_DURATION_PATTERNS",
    "TIHAI_PATTERNS",
    "GAMAKA_PATTERNS",
    # Functions
    "generate_duration_sequence",
    "add_tihai_ending",
    "apply_gamaka_to_duration",
    "calculate_indian_note_density",
    "get_duration_guidelines_for_prompt",
]
