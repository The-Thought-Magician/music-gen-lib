# V4-31: Form Structure Templates

## Overview

Define musical form templates for composition.

## Objectives

1. Define pop song forms
2. Define classical forms
3. Define electronic forms
4. Define world music forms
5. Create form composition utilities

## Form Templates

```yaml
musical_forms:

  # Pop/Rock forms
  verse_chorus:
    name: "Verse-Chorus"
    sections:
      - {name: "intro", length: 4}
      - {name: "verse", length: 16}
      - {name: "chorus", length: 16}
      - {name: "verse", length: 16}
      - {name: "chorus", length: 16}
      - {name: "bridge", length: 8}
      - {name: "chorus", length: 16}
      - {name: "outro", length: 8}

  aaba:
    name: "AABA (32-bar form)"
    sections:
      - {name: "A", length: 8}
      - {name: "A", length: 8}
      - {name: "B", length: 8}
      - {name: "A", length: 8}

  # Classical forms
  sonata:
    name: "Sonata Form"
    sections:
      - {name: "exposition", subsections: ["theme1", "theme2", "transition"]}
      - {name: "development", subsections: ["exploration", "retransition"]}
      - {name: "recapitulation", subsections: ["theme1", "theme2", "coda"]}

  rondo:
    name: "Rondo Form"
    pattern: "A-B-A-C-A-B-A"

  # Electronic forms
  electronic_buildup:
    name: "Build-up/Breakdown"
    sections:
      - {name: "intro", intensity: 0.2}
      - {name: "build1", intensity: 0.4}
      - {name: "build2", intensity: 0.6}
      - {name: "drop", intensity: 1.0}
      - {name: "breakdown", intensity: 0.3}
      - {name: "build", intensity: 0.7}
      - {name: "drop2", intensity: 1.0}
```

## Files to Create

- `src/musicgen/genres/forms.py`
- `resources/musical_forms.yaml`

## Success Criteria

- [ ] All major forms defined
- [ ] Section lengths customizable
- [ ] Form composition utility working

## Next Steps

After completion, proceed to V4-32: Arrangement Intelligence
