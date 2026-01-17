# V4-27: Pattern State History

## Overview

Implement pattern state tracking for cyclical composition.

## Objectives

1. Define cycle tracking
2. Implement pattern history
3. Support cycle-based addressing
4. Implement pattern freezing

## Implementation

```python
class CycleState:
    """Track cycle position and state"""

    def __init__(self):
        self.cycle = 0  # Current cycle number
        self.start = 0  # Start time
        self.history = {}  # Pattern history by cycle

    def advance(self, cycles: int = 1):
        """Advance cycle counter"""

    def get_state(self, cycle: int) -> Any:
        """Get state at cycle"""

    def set_pattern(self, cycle: int, pattern: Pattern):
        """Set pattern for specific cycle"""

class PatternHistory:
    """Store and retrieve past patterns"""

    def freeze(self, cycle: int):
        """Freeze pattern at cycle"""

    def unfreeze(self):
        """Unfreeze and resume"""
```

## Files to Create

- `src/musicgen/patterns/state.py`

## Success Criteria

- [ ] Cycle tracking working
- [ ] History storage functional
- [ ] Freeze/unfreeze working

## Next Steps

After completion, proceed to Phase 5: Genre Intelligence (V4-28)
