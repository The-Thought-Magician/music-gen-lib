# V4-41: Visual Feedback

## Overview

Create visual feedback system for live coding.

## Objectives

1. Create pattern visualization
2. Create cycle indicator
3. Create instrument status display

## Implementation

```python
class Visualizer:
    """Visual feedback for live coding"""

    def visualize_pattern(self, pattern: Pattern) -> str:
        """Create text visualization"""

    def create_cycle_indicator(self, cycle: int, total: int) -> str:
        """Show cycle position"""

    def show_instrument_status(self, instruments: dict) -> str:
        """Show active instruments"""
```

## Files to Create

- `src/musicgen/live/visualizer.py`

## Success Criteria

- [ ] Pattern visualization clear
- [ ] Cycle indicator accurate
- [ ] Status display informative

## Next Steps

After completion, proceed to V4-42: Performance Presets
