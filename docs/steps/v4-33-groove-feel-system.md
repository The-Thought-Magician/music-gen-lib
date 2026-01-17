# V4-33: Groove Feel System

## Overview

Implement groove and feel systems for realistic rhythm.

## Objectives

1. Define swing amount control
2. Implement groove templates
3. Implement humanization
4. Implement micro-timing adjustments

## Implementation

```python
class Groove:
    """Groove and feel system"""

    def apply_swing(
        self,
        pattern: Pattern,
        amount: float = 0.3  # 0-1
    ) -> Pattern:
        """Apply swing to off-beats"""

    def humanize(
        self,
        pattern: Pattern,
        timing_amount: float = 0.02,
        velocity_amount: float = 0.1
    ) -> Pattern:
        """Add human variation"""

    def apply_groove_template(
        self,
        pattern: Pattern,
        template: list[float]  # Timing offsets
    ) -> Pattern:
        """Apply groove template"""

# Groove templates
GROOVE_TEMPLATES = {
    "jazz": [0, 10, -5, 5],  # Swing feel
    "hiphop": [0, 5, -3, 2],  # Hip-hop feel
    "shuffle": [0, 15, -8, 5],  # Shuffle
    "straight": [0, 0, 0, 0],  # No swing
}
```

## Files to Create

- `src/musicgen/patterns/groove.py`

## Success Criteria

- [ ] Swing working correctly
- [ ] Groove templates applyable
- [ ] Humanization sounds natural
- [ ] Tests verify groove application

## Next Steps

After completion, proceed to Phase 6: Electronic Instruments (V4-34)
