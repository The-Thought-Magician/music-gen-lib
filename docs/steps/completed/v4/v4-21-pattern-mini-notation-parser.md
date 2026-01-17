# V4-21: Pattern Mini-notation Parser

## Overview

Implement TidalCycles-inspired mini-notation parser for rhythm patterns.

## Objectives

1. Define mini-notation syntax
2. Create parser for mini-notation
3. Support rests, grouping, repetition
4. Support alternation and randomization
5. Support Euclidean rhythms

## Mini-notation Syntax

```yaml
# Mini-notation symbols
symbols:
  rest: "~"
  group_start: "["
  group_end: "]"
  group_short: "."
  superposition: ","
  repeat: "*"
  divide: "/"
  random: "|"
  alternate: "< >"
  replicate: "!"
  elongate: "_"
  elongate_alt: "@"
  degrade: "?"
  select: ":"
  euclidean: "(x,y)"
  polymetric: "{ }"
  polymetric_div: "{ }%"
  ratio: "%"

# Examples
examples:
  basic: "bd hh sd hh"
  rests: "bd ~ hh ~"
  groups: "[bd sd] hh"
  repeat: "bd*2 sd"
  divide: "bd/2"
  random: "[bd|hh|cp]"
  alternate: "bd <sd hh cp>"
  replicate: "bd!3 sd"
  elongate: "bd _ _ ~ sd _"
  degrade: "bd? sd"
  euclidean: "bd(3,8)"
  polymetric: "{bd bd, hh hh}"
```

## Parser Implementation

```python
class MiniNotationParser:
    """Parse TidalCycles-style mini-notation"""

    def parse(self, pattern: str) -> Pattern:
        """Parse mini-notation string into Pattern object"""

    def parse_group(self, group: str) -> list[str]:

    def parse_euclidean(self, pattern: str) -> list[int]:
        """Parse euclidean (x,y) notation"""
```

## Files to Create

- `src/musicgen/patterns/parser.py`
- `src/musicgen/patterns/models.py`

## Success Criteria

- [ ] All mini-notation symbols supported
- [ ] Nested grouping working
- [ ] Euclidean notation parsing
- [ ] Error handling for invalid syntax

## Next Steps

After completion, proceed to V4-22: Euclidean Rhythm Implementation
