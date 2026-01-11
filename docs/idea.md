# Music Generation Library

## Overview
Create a Python library that generates orchestral instrumental music using traditional music theory (not AI models). The library produces both sheet music and audio files.

## Project Goals
- **Primary**: Create usable, listenable orchestral music
- **Approach**: Rule-based composition using music theory principles
- **Format**: Python library for programmatic music generation

## Core Concepts to Research

### Music Theory
- Scales (major, minor, modal, pentatonic, etc.)
- Chords and chord progressions
- Voice leading principles
- Rhythm and meter
- Orchestration techniques (instrument ranges, timbres, combinations)
- Musical forms (binary, ternary, sonata, rondo)

### Technical Components
- Note representation (pitch, duration, velocity)
- MIDI encoding/decoding
- Audio synthesis (oscillators, envelopes, filters)
- SoundFonts or instrument samples
- Sheet music notation (MusicXML, LilyPond)

## Proposed Workflow

```
User Input (mood/theme)
        ↓
Select scale, tempo, key signature based on mood
        ↓
Generate chord progression
        ↓
Compose melody with proper voice leading
        ↓
Add orchestration (instruments: strings, brass, woodwinds, percussion)
        ↓
Create musical form (intro, A section, B section, bridge, outro)
        ↓
Generate preview clips (per section)
        ↓
User reviews and refines
        ↓
Export: Sheet music + Audio file
```

## Output Formats
1. **Sheet Music**: MusicXML or LilyPond (viewable/editable in notation software)
2. **Audio**: WAV/FLAC (high quality), optionally MP3

## Mood-to-Music Mappings (Examples)
| Mood | Key | Scale | Tempo | Instruments |
|------|-----|-------|-------|-------------|
| Epic | D minor | Harmonic minor | 120-140 | Full orchestra, timpani |
| Peaceful | G major | Major | 60-80 | Strings, flute, harp |
| Mysterious | E minor | Natural minor | 70-90 | Clarinet, bassoon, pizzicato strings |
| Triumphant | C major | Major | 100-120 | Brass, snare, full orchestra |
| Melancholic | B minor | Natural minor | 50-70 | Cello, violin solo, piano |

## Existing Python Libraries to Explore
- **music21**: Music theory and analysis
- **mido**: MIDI file handling
- **pretty_midi**: MIDI manipulation
- **abjad**: LilyPond notation
- **pydub**: Audio processing
- **scamp**: Composition and playback
- **fluidsynth**: SoundFont-based synthesis

## Research Questions
1. How do classical composers structure orchestral pieces?
2. What are the standard instrument ranges and combinations?
3. How to create convincing harmony and counterpoint?
4. What makes a melody memorable vs. random?
5. How to mix/orchestrate for clarity vs. fullness?

## Phase 1: Research & Exploration
- [ ] Study basic music theory (scales, intervals, chords)
- [ ] Understand orchestral instruments and their roles
- [ ] Evaluate Python music libraries
- [ ] Create simple proof-of-concept (single melody line)

## Phase 2: Core Library
- [ ] Note and duration representation
- [ ] Scale and chord generators
- [ ] Melody generation with rules
- [ ] Basic MIDI output

## Phase 3: Orchestration
- [ ] Multi-instrument composition
- [ ] Voice leading between parts
- [ ] Dynamic and articulation marking
- [ ] Audio synthesis with realistic instruments

## Phase 4: Sheet Music
- [ ] MusicXML generation
- [ ] Layout and formatting
- [ ] Expression marks and directions 