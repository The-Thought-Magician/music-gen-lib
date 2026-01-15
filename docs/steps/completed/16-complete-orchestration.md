# Step 16: Complete Orchestration Engine

## Objective

Enhance the composition engine to create true multi-part orchestrations with proper voice leading, counterpoint, and timing for complete 3-minute compositions.

## Overview

Current composition generation is basic. This step creates a sophisticated orchestration engine that:
1. Generates independent parts for each instrument
2. Applies proper voice leading rules
3. Creates thematic development across sections
4. Handles timing and transitions
5. Balances orchestral texture

## Dependencies

- Existing musicgen modules
- Enhanced composition algorithms

## Tasks

### 16.1 Voice Leading Engine Enhancement

- [ ] Enhance `src/musicgen/theory/voice_leading.py`
- [ ] Implement multi-part voice leading (SATB + more)
- [ ] Add constraints for specific instrument ranges
- [ ] Implement parallel motion detection and avoidance
- [ ] Add leading tone resolution rules
- [ ] Create smooth voice connection between chords

### 16.2 Orchestration Strategies

- [ ] Create `src/musicgen/orchestration/strategies.py`
- [ ] Implement homophonic texture strategy
- [ ] Implement polyphonic texture strategy
- [ ] Implement melody+accompaniment strategy
- [ ] Implement tutti vs. solo sections
- [ ] Create doubling strategies (octave, unison)

### 16.3 Thematic Development

- [ ] Create `src/musicgen/composition/development.py`
- [ ] Implement motif transformation (sequence, inversion, retrograde)
- [ ] Create thematic recurrence across sections
- [ ] Implement development section logic
- [ ] Add bridge and transition generation
- [ ] Create climax building techniques

### 16.4 Form Structure Engine

- [ ] Enhance `src/musicgen/composition/forms.py`
- [ ] Implement proper section timing
- [ ] Create transition generators between sections
- [ ] Add key modulation strategies
- [ ] Implement recapitulation with variation
- [ ] Create coda generation

### 16.5 Dynamics and Expression

- [ ] Create `src/musicgen/composition/dynamics.py`
- [ ] Implement dynamic arc planning
- [ ] Add crescendo/diminuendo generation
- [ ] Create accent and stress marking
- [ ] Implement articulation variety
- [ ] Add tempo modification (rubato, accelerando)

### 16.6 Multi-Section Composition

- [ ] Enhance `src/musicgen/generator.py`
- [ ] Implement section-by-section generation
- [ ] Create section transition handling
- [ ] Add theme recall and variation
- [ ] Implement total duration targeting
- [ ] Create multi-section export

### 16.7 Instrument-Specific Writing

- [ ] Create instrument-specific idioms
- [ ] Add string techniques (pizzicato, tremolo)
- [ ] Add woodwind articulations
- [ ] Add brass effects (muted, straight)
- [ ] Add percussion writing logic
- [ ] Create divisi/passive playing

### 16.8 Testing

- [ ] Create `tests/test_orchestration.py`
- [ ] Test multi-section compositions
- [ ] Test voice leading rules
- [ ] Test thematic development
- [ ] Test form structures
- [ ] Test complete 3-minute generation

## Deliverables

- Enhanced `src/musicgen/theory/voice_leading.py`
- New `src/musicgen/orchestration/strategies.py`
- New `src/musicgen/composition/development.py`
- Enhanced `src/musicgen/composition/forms.py`
- New `src/musicgen/composition/dynamics.py`
- Enhanced `src/musicgen/generator.py`
- `tests/test_orchestration.py`
- `examples/complete_orchestration_example.py`

## Section Structure Example

```python
class SectionPlan:
    """Plan for a single section."""
    name: str  # "A", "B", "development", etc.
    duration_beats: int
    tonic: str
    key_type: str
    tempo: int
    dynamics_start: str
    dynamics_end: str
    texture: TextureType
    instruments_playing: List[str]
    melody_source: str  # "new", "from_A", "modified_B"
    harmonic_center: str  # "tonic", "dominant", etc.
```

## Validation

```python
# Test complete orchestration
request = CompositionRequest(
    ai_plan=orchestration_plan,  # From Step 15
    duration=180,  # 3 minutes
    export_formats=["midi", "wav", "mp3"]
)
result = generate(request)

# Verify complete structure
assert len(result.score.parts) >= 8  # Full orchestra
assert result.duration >= 170 and result.duration <= 190

# Verify sections
sections = identify_sections(result.score)
assert len(sections) >= 3  # At least ABA or similar

# Verify voice leading
for part_pair in zip(result.score.parts, result.score.parts[1:]):
    assert has_valid_voice_leading(part_pair[0], part_pair[1])

# Verify thematic development
themes = extract_themes(result.score)
assert has_thematic_recurrence(themes)

# Verify dynamics
assert has_dynamic_arc(result.score)
```

## Form Templates

### Sonata Form (3 minutes)
- Exposition (90s): Theme 1 (tonic) -> Transition -> Theme 2 (dominant)
- Development (60s): Theme manipulation, modulations
- Recapitulation (30s): Theme 1 -> Theme 2 (both tonic)

### Ternary Form (3 minutes)
- A section (60s): Main theme
- B section (60s): Contrasting theme, often dominant/relative
- A' section (60s): Main theme return, elaborated

### Rondo Form (3 minutes)
- A (40s): Main theme
- B (30s): Episode 1
- A (30s): Main theme
- C (30s): Episode 2
- A (30s): Main theme
- D (20s): Episode 3
- A (40s): Main theme + coda

### Through-Composed (3 minutes)
- Continuous development with no literal repetition
- Sections flow with motivic unity
