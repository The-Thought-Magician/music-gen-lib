# V4-50: Release Preparation

## Overview

Prepare V4 for release.

## Tasks

1. Version bump
2. Migration guide
3. CHANGELOG update
4. Release notes

## Migration Guide

```markdown
# V4 Migration Guide

## New Features
- Guitar and bass instruments
- Drum kits with patterns
- World instruments
- Pattern manipulation system
- Genre profiles
- Live coding mode (basic)

## Breaking Changes
- None (backward compatible with V3)

## New Dependencies
- websockets
- scipy (for some pattern calculations)

## Usage Examples
# Before (V3)
musicgen compose "Orchestral piece"

# After (V4)
musicgen compose "Rock song with guitar solo" --genre rock
musicgen pattern "bd(3,8) hh(5,8)" --visualize
```

## Files to Update

- `pyproject.toml` (version)
- `CHANGELOG.md`
- `docs/V4_RELEASE_NOTES.md`

## Success Criteria

- [ ] Version updated
- [ ] Migration guide complete
- [ ] CHANGELOG updated
- [ ] Release notes written
- [ ] All tests passing

## V4 Complete!
