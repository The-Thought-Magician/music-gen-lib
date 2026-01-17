# V4-35: Synthesizer Patterns

## Overview

Define synthesizer-specific patterns and sequences.

## Patterns

```yaml
synth_patterns:
  arp:
    name: "Arpeggiator Patterns"
    types:
      up: [0, 1, 2, 3]  # Scale up
      down: [3, 2, 1, 0]  # Scale down
      updown: [0, 1, 2, 3, 2, 1, 0]
      random: "random"
      order: "keep current order"
    gate: "8ths"  # Rate
    octaves: [4, 5]  # Octave range

  sequencer:
    name: "Step Sequencer"
    steps: 16
    gates: [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]
    accents: [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]

  modulations:
    name: "Modulation Routing"
    lfo_to_filter: "LFO 1 -> Filter Cutoff"
    lfo_to_pitch: "LFO 2 -> Oscillator Pitch"
    env_to_vibrato: "Amp Env -> Vibrato Depth"
```

## Files to Create

- `src/musicgen/instruments/synth_patterns.py`

## Success Criteria

- [ ] Arpeggiator patterns working
- [ ] Step sequencer functional
- [ ] Modulation routing implemented

## Next Steps

After completion, proceed to V4-36: Drum Machine Definitions
