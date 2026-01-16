# Step 10: Enhanced Prompts for Duration and Note Count

## Status: COMPLETED

## Overview

The AI was generating compositions that were too short (30-90 seconds instead of 2-3 minutes). This step improved the prompts to emphasize note quantity and duration requirements.

## Problems Identified

1. **Insufficient note count**: AI generated 30-80 notes per part instead of 150+
2. **Duration too short**: Most pieces were under 90 seconds
3. **Too many parts**: AI created 5-6 parts, spreading notes too thin
4. **Unclear requirements**: AI didn't understand how many notes were needed for 2-3 minutes

## Solution

### 1. Added Duration Calculations to System Prompt

```python
CRITICAL DURATION REQUIREMENTS:
You MUST generate 2-3 minutes of music. Here is how to calculate this:

Duration (seconds) = (Total quarter notes in part × 60) / Tempo

For 2 minutes at 120 BPM: 240 quarter notes needed
For 2 minutes at 70 BPM: 140 quarter notes needed
For 3 minutes at 120 BPM: 360 quarter notes needed
For 3 minutes at 70 BPM: 210 quarter notes needed
```

### 2. Added Minimum Note Counts by Role

```python
MINIMUM NOTE COUNTS BY PART:
- Melody parts: 150-300 notes minimum (depending on tempo)
- Harmony parts: 120-250 notes minimum
- Bass parts: 80-150 notes minimum (typically longer durations)
- Accompaniment parts: 100-200 notes minimum

DO NOT generate compositions shorter than 2 minutes. Always err on the side of MORE notes.
```

### 3. Limited Number of Parts

```python
NUMBER OF PARTS: Limit to 2-4 parts maximum.
- More parts = fewer notes per part = shorter duration
- Better to have 3 well-developed parts than 6 sparse parts
- Recommended: melody + bass + 1-2 harmony/accompaniment parts
```

### 4. Updated User Prompt Structure

```python
CRITICAL REQUIREMENTS - READ CAREFULLY:

1. DURATION: Your composition MUST be 2-3 minutes long at the specified tempo.
   Calculate needed notes: (Tempo / 60) × Duration(seconds) = quarter notes needed
   Example: At 80 BPM, 2 minutes = 160 quarter notes minimum per part

2. NUMBER OF PARTS: Limit to 2-4 parts maximum.
   - More parts = fewer notes per part = shorter duration
   - Better to have 3 well-developed parts than 6 sparse parts
   - Recommended: melody + bass + 1-2 harmony/accompaniment parts

3. NOTE COUNTS BY PART:
   - Melody: 150-350 notes (depending on tempo and note durations)
   - Harmony: 120-280 notes
   - Bass: 80-180 notes (bass notes are longer, so fewer needed)
   - Accompaniment: 100-220 notes
```

## Test Results

| Piece | Duration | Status |
|-------|----------|--------|
| Sunset on Sycamore Street (piano) | 3.1 min | ✅ Good |
| Midnight on the Seine (jazz) | 3.5 min | ✅ Excellent |
| Summit's Triumph (orchestral) | 1.4 min | ⚠️ Still short (6 parts) |

## Insights

- **Smaller ensembles work better**: 2-4 part compositions hit duration targets
- **Orchestral pieces still struggle**: AI tends to create too many parts for orchestral prompts
- **Note density varies**: At slower tempos with longer notes, fewer notes are needed
- **Prompt specificity matters**: More detailed prompts yield better results

## Files Modified

- `src/musicgen/ai_client/prompts.py` - Complete rewrite of system and user prompts

## Next Steps

Consider using a section-by-section generation approach for orchestral pieces to manage complexity.
