# V4-48: CLI Enhancements

## Overview

Enhance CLI with V4 features.

## New Commands

```bash
# Pattern commands
musicgen pattern "bd(3,8) hh(5,8)" --visualize
musicgen transform --slow 2 --rev input.mid

# Genre commands
musicgen compose "Rock song" --genre rock --intensity high
musicgen list-instruments --category guitars

# Instrument commands
musicgen list-instruments --world
musicgen show-instrument sitar

# Scale commands
musicgen list-scales --type indian
musicgen show-raga yaman

# Preview mode
musicgen preview "Upbeat jazz" --duration 30
```

## Files to Modify

- `src/musicgen/__main__.py`

## Success Criteria

- [ ] All commands working
- [ ] Help documentation complete
- [ ] Error messages helpful

## Next Steps

After completion, proceed to V4-49: Performance Optimization
