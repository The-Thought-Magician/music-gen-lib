# V4-32: Arrangement Intelligence

## Overview

Implement intelligent arrangement and orchestration.

## Objectives

1. Define density curves by section
2. Define dynamic arcs
3. Implement texture layering
4. Implement transition generation

## Implementation

```python
class Arranger:
    """Intelligent arrangement"""

    def arrange_section(
        self,
        composition: AIComposition,
        section: str,
        role: str  # "intro", "climax", etc.
    ) -> AIComposition:
        """Arrange for specific section"""

    def create_dynamic_arc(
        self,
        sections: list[str],
        arc: list[float]  # Intensity per section
    ) -> dict:
        """Map dynamics to sections"""

    def layer_instrumentation(
        self,
        base: AIComposition,
        additions: dict[str, AIComposition]
    ) -> AIComposition:
        """Layer additional instruments"""

    def create_transition(
        self,
        from_section: str,
        to_section: str,
        duration: int  # In beats
    ) -> AIComposition:
        """Generate transition between sections"""
```

## Files to Create

- `src/musicgen/genres/arrangement.py`

## Success Criteria

- [ ] Arrangement by role working
- [ ] Dynamic arcs functional
- [ ] Smooth transitions generated

## Next Steps

After completion, proceed to V4-33: Groove Feel System
