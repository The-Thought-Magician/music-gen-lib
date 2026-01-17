# V4-42: Performance Presets

## Overview

Create prepared patterns and scene management for live performance.

## Objectives

1. Define preset patterns
2. Create scene management
3. Define transition patterns

## Presets

```yaml
performance_presets:
  scene_1:
    name: "Scene 1 - Ambient Intro"
    patterns:
      pad: "ambient_pad"
      bass: "long_bass"
      texture: "high_textures"
    transitions: "fade_in"

  scene_2:
    name: "Scene 2 - Groove"
    patterns:
      drums: "house_beat"
      bass: "driving_bass"
      lead: "arp_melody"
    transitions: "cut"

  transition_patterns:
    fade_out: "volume ramp down"
    fill: "drum fill"
    breakdown: "reduce density"
    buildup: "add layers"
```

## Files to Create

- `resources/performance_presets.yaml`
- `src/musicgen/live/presets.py`

## Success Criteria

- [ ] Presets loadable
- [ ] Transitions working
- [ ] Scene switching smooth

## Next Steps

After completion, proceed to Phase 8: Integration Testing (V4-43)
