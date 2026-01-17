# V4-43: Extended System Prompt

## Overview

Update system prompt with all new V4 knowledge.

## Objectives

1. Add all new instruments to prompt
2. Add world music theory
3. Add genre-specific guidance
4. Add pattern manipulation documentation

## Updates

```yaml
system_prompt_v4:
  extends: "v3"

  instruments:
    guitars: [acoustic_nylon, acoustic_steel, electric_clean, electric_overdrive]
    bass: [electric_bass, fretless, slap_bass, synth_bass]
    drums: [standard_kit, jazz_kit, electronic_kits]
    indian: [sitar, tabla, bansuri, tanpura]
    middle_eastern: [oud, ney, darbuka, kanun]
    east_asian: [koto, shakuhachi, guzheng, erhu]
    electronic: [synth_bass, synth_pad, synth_lead]

  scales:
    western: [major, minor, modes]
    indian: [ragas with thaat]
    arabic: [maqamat]
    japanese: [in, hirajoshi, miyakobushi]
    pentatonic: [major, minor, blues]

  patterns:
    mini_notation: "Documentation of syntax"
    transformations: "Available transformations"

  genres:
    rock/pop: "Characteristics and patterns"
    jazz: "Characteristics and patterns"
    classical: "Forms and orchestration"
    electronic: "Subgenres and patterns"
    world: "Regional characteristics"
```

## Files to Create

- `resources/system_prompt_v4.txt`

## Success Criteria

- [ ] All instruments documented
- [ ] All scales documented
- [ ] Genre guidance included
- [ ] Pattern syntax explained

## Next Steps

After completion, proceed to V4-44: Instrument Selection Intelligence
