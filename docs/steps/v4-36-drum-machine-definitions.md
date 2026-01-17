# V4-36: Drum Machine Definitions

## Overview

Define vintage drum machine specifications.

## Drum Machines

```yaml
drum_machines:
  roland_tr808:
    name: "Roland TR-808"
    year: 1980
    sounds:
      kick: "Deep, punchy sine wave"
      snare: "Bright, short"
      clap: "Hand clap"
      hihat_closed: "Metallic, short"
      hihat_open: "Longer, metallic"
      maracas: "Shaker"
      cowbell: "Iconic"
      cymbal: "Metallic"
      toms: "Low, tom sounds"

  roland_tr909:
    name: "Roland TR-909"
    year: 1983
    sounds:
      kick: "Processed, punchy"
      snare: "Aggressive, distinctive"
      rimshot: "Rimshot"
      clap: "Clap"
      hihat_closed: "Closed"
      hihat_open: "Open"
      crash: "Metallic"
      ride: "Clean"
      tom: "Tom"

  linndrum:
    name: "Linndrum LM-1"
    year: 1984
    sounds: "Samples from real drums"

  oberheim_dmx:
    name: "Oberheim DMX"
    year: 1983
    sounds: "80s drum sounds"
```

## Files to Create

- `resources/drum_machines.yaml`
- `src/musicgen/instruments/drum_machines.py`

## Success Criteria

- [ ] Major drum machines defined
- [ ] Sound characteristics documented
- [ ] MIDI mappings correct

## Next Steps

After completion, proceed to V4-37: Electronic Effects
