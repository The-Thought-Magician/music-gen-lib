# V4-37: Electronic Effects

## Overview

Define electronic music effects and their MIDI implementation.

## Effects

```yaml
effects:
  filter:
    name: "Filter (VCF)"
    types: ["lowpass", "highpass", "bandpass", "notch"]
    parameters:
      cutoff: "0-127 (frequency)"
      resonance: "0-127 (Q)"
    midi_cc:
      cutoff: 74
      resonance: 71

  delay:
    name: "Delay"
    parameters:
      time: "Delay time"
      feedback: "Feedback amount"
      mix: "Wet/Dry mix"

  reverb:
    name: "Reverb"
    parameters:
      size: "Room size"
      decay: "Reverb tail"
      mix: "Wet/Dry"

  distortion:
    name: "Distortion"
    parameters:
      drive: "Distortion amount"
      tone: "EQ"
      level: "Output level"

  chorus:
    name: "Chorus"
    parameters:
      rate: "LFO rate"
      depth: "Modulation depth"
      mix: "Wet/Dry"

  phaser:
    name: "Phaser"
    parameters:
      rate: "LFO rate"
      depth: "Modulation depth"
      feedback: "Phase feedback"
      stages: "Number of stages"
```

## Files to Create

- `src/musicgen/instruments/effects.py`

## Success Criteria

- [ ] All major effects defined
- [ ] CC mappings correct
- [ ] Parameter ranges specified

## Next Steps

After completion, proceed to Phase 7: Live Coding Mode (V4-38)
