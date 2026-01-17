# V4-22: Euclidean Rhythm Implementation

## Overview

Implement Euclidean rhythm generation using the Bjorklund algorithm.

## Objectives

1. Implement Bjorklund algorithm
2. Create Euclidean rhythm functions
3. Support offset parameter
4. Visual representation

## Implementation

```python
def bjorklund(pulses: int, total: int) -> list[int]:
    """Bjorklund algorithm for Euclidean rhythms"""
    # Returns list of 0s and 1s
    ...

class EuclideanRhythm:
    def __init__(self, pulses: int, total: int, offset: int = 0):
        self.pulses = pulses
        self.total = total
        self.offset = offset
        self.pattern = self.generate()

    def generate(self) -> list[int]:
        """Generate Euclidean rhythm pattern"""

    def rotate(self, offset: int) -> list[int]:
        """Rotate pattern by offset"""

    def visualize(self) -> str:
        """Return visual representation"""

# Pre-computed Euclidean rhythms
EUCLIDEAN_RHYTHMS = {
    (3, 4): [1, 0, 1, 0],  # Basic rock
    (3, 8): [1, 0, 0, 1, 0, 0, 1, 0],  # Cuban tresillo
    (4, 7): [1, 0, 0, 1, 0, 0, 1],  # Bulgarian
    (5, 8): [1, 0, 1, 0, 1, 0, 0, 1],  # Cuban cinquillo
    (7, 8): [1, 0, 1, 0, 1, 0, 1, 0],  # Bendir
    # ... more
}
```

## Files to Create

- `src/musicgen/patterns/euclidean.py`

## Success Criteria

- [ ] Bjorklund algorithm working
- [ ] Offset/rotate working
- [ ] All common Euclidean rhythms pre-computed
- [ ] Visualization working

## Next Steps

After completion, proceed to V4-23: Pattern Transformation Functions
