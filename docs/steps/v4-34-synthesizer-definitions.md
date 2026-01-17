# V4-34: Synthesizer Definitions

## Overview

Define synthesizer types and parameters.

## Synth Types

```yaml
synths:
  subtractive:
    name: "Subtractive"
    oscillators:
      - {type: "sawtooth", detune: 0, phase: 0}
      - {type: "square", detune: 0, phase: 0}
      - {type: "triangle", detune: 0, phase: 0}
    filter: {type: "lowpass", poles: 24, resonance: 0.5}
    envelopes:
      amp: {a: 0.01, d: 0.1, s: 0.7, r: 0.2}
      filter: {a: 0.05, d: 0.3, s: 0.0, r: 0.2}

  fm:
    name: "FM Synthesis"
    operators: 6
    algorithm: "varied"
    modulator: "operator 2 modulates operator 1"

  wavetable:
    name: "Wavetable"
    wavetables: ["analog", "digital", "vocal"]
    position: "modulatable"

  additive:
    name: "Additive"
    partials: "sine waves at harmonics"

  sampler:
    name: "Sampler"
    samples: "recorded sounds"
```

## Presets

```yaml
synth_presets:
  bass:
    name: "Synth Bass"
    type: "subtractive"
    oscillator: "sawtooth"
    filter: "lowpass, cutoff varies with pitch"

  pad:
    name: "Pad"
    type: "subtractive"
    oscillator: "sawtooth"
    filter: "lowpass, slow envelope"

  lead:
    name: "Lead"
    type: "subtractive"
    oscillator: "sawtooth"
    filter: "lowpass, resonance accent"

  pluck:
    name: "Pluck"
    type: "subtractive"
    oscillator: "sawtooth"
    filter: "lowpass, fast decay"
```

## Files to Create

- `resources/instrument_definitions_world.yaml` (synths)
- `src/musicgen/instruments/synths.py`

## Success Criteria

- [ ] All synth types defined
- [ ] Common presets created
- [ ] Parameters mapped to MIDI

## Next Steps

After completion, proceed to V4-35: Synthesizer Patterns
