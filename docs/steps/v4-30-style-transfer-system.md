# V4-30: Style Transfer System

## Overview

Implement style transfer to apply genre characteristics to compositions.

## Objectives

1. Define style transfer mechanisms
2. Implement genre-to-genre transformation
3. Create style intensity control
4. Support hybrid genres

## Implementation

```python
class StyleTransfer:
    """Transfer style between genres"""

    def apply_style(
        self,
        composition: AIComposition,
        target_genre: str,
        intensity: float = 0.5  # 0-1
    ) -> AIComposition:
        """Apply target genre characteristics"""

    def hybrid_styles(
        self,
        genre1: str,
        genre2: str,
        ratio: float = 0.5
    ) -> GenreProfile:
        """Create hybrid genre profile"""
```

## Files to Create

- `src/musicgen/genres/transfer.py`

## Success Criteria

- [ ] Style transfer working
- [ ] Hybrid genres supported
- [ ] Intensity control functional

## Next Steps

After completion, proceed to V4-31: Form Structure Templates
