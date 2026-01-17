# V4-26: Randomness Stochastic Patterns

## Overview

Implement randomness and stochastic pattern generation.

## Objectives

1. Define random number generators
2. Define random selection functions
3. Define stochastic processes
4. Define probability distributions

## Functions

```python
def rand() -> float:
    """Random float 0-1"""

def irand(max: int) -> int:
    """Random integer 0 to max-1"""

def choose(items: list[Any]) -> Any:
    """Randomly choose from list"""

def chooseBy(pattern: Pattern, items: list[Any]) -> Pattern:
    """Use pattern to select"""

def shuffle(pattern: Pattern) -> Pattern:
    """Random shuffle of events"""

def sometimes(
    f: Callable,
    probability: float = 0.5
) -> Callable:
    """Wrap function to apply probabilistically"""

def markov_chain(states: list[Any], transitions: dict) -> list[Any]:
    """Generate from Markov chain"""

def perlin_noise(seed: int, scale: float = 1.0) -> float:
    """Perlin noise value"""
```

## Files to Create

- `src/musicgen/patterns/stochastic.py`

## Success Criteria

- [ ] All random functions working
- [ ] Seeded randomness for reproducibility
- [ ] Tests for stochastic functions

## Next Steps

After completion, proceed to V4-27: Pattern State History
