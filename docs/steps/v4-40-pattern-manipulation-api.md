# V4-40: Pattern Manipulation API

## Overview

Create API for live pattern manipulation.

## Objectives

1. Define transformation endpoints
2. Support parameter modulation
3. Implement cue system
4. Handle scene management

## API

```python
class LiveAPI:
    """Live coding API"""

    def transform(
        self,
        pattern_id: str,
        transform: str,
        **params
    ) -> Pattern:
        """Apply transformation to pattern"""

    def modulate(
        self,
        param: str,
        source: str,  # LFO, envelope, etc.
        amount: float
    ):

    def cue_scene(
        self,
        scene_id: str
    ):
        """Cue new scene"""
```

## Files to Create

- `src/musicgen/live/api.py`

## Success Criteria

- [ ] All transformations callable
- [ ] Modulation working
- [ ] Scene transitions smooth

## Next Steps

After completion, proceed to V4-41: Visual Feedback
