# MusicGen - Project Vision

## What This Project Is Achieving

MusicGen aims to make orchestral music composition accessible to everyone through natural language. Instead of requiring deep knowledge of music theory, orchestration, voice leading, and formal structure—you simply describe what you want to hear, and the AI handles the complex craft of composition.

## The Problem

Orchestral composition traditionally requires years of study in:
- **Music Theory**: Scales, keys, chord progressions, modulation
- **Voice Leading**: Classical counterpoint rules for smooth part writing
- **Orchestration**: Understanding instrument ranges, timbres, and combinations
- **Musical Form**: Sonata, rondo, ternary structures and how to use them
- **Notation**: MusicXML, MIDI, and scoring software

This creates a high barrier to entry for composers, game developers, filmmakers, and anyone who needs custom music.

## The Solution

MusicGen uses Google Gemini 2.5 Pro AI to translate natural language descriptions into complete musical compositions. The system:

1. **Understands Intent**: Parses descriptions like "a heroic battle theme with building intensity"
2. **Applies Music Theory**: Generates proper chord progressions, voice leading, and form
3. **Orchestrates**: Selects appropriate instruments and writes realistic parts
4. **Exports**: Produces MIDI, audio, and notation-ready files

## Current Implementation

### AI-Powered Composition Engine

- **Model**: Google Gemini 2.5 Pro via the google-genai SDK
- **Schema-Driven**: Uses Pydantic models to validate generated music theory
- **Quality Assurance**: Validates minimum duration, note counts, and polyphony rules

### Output Capabilities

| Format | Description |
|--------|-------------|
| **MIDI** | Standard format for DAWs, notation software, and players |
| **WAV** | Uncompressed audio via FluidSynth synthesis |
| **MP3** | Compressed audio for easy sharing |
| **JSON** | Full composition data for further processing |

### Preset Styles

The library includes prompt presets for common styles:
- Classical piano, jazz trio, epic orchestral
- Ambient, folk, blues, minimalist
- Romantic string quartet

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Input                              │
│         "A heroic battle theme in D minor, 140 BPM"            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI Composer                                 │
│  • Gemini 2.5 Pro API                                           │
│  • Schema-driven prompt engineering                             │
│  • Quality validation (duration, note counts, polyphony)        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AIComposition Model                           │
│  • Structure: Part-based or Measure-based                       │
│  • Parts: AIPart with AINote/AIRest events                      │
│  • Timing: Absolute start_time for polyphony support            │
│  • Metadata: Key, tempo, form, dynamics                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Renderer                                   │
│  • MIDI: mido-based multi-track export                          │
│  • Audio: pretty-midi + FluidSynth synthesis                    │
│  • MP3: pydub format conversion                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Output Files                                │
│  • the_heroic_battle.mid                                        │
│  • the_heroic_battle.mp3                                        │
│  • the_heroic_battle.json                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Music Theory Features

### Supported Concepts

- **Keys & Scales**: Major, minor (natural, harmonic, melodic), modes
- **Chords**: Triads, seventh chords, extensions, inversions
- **Progressions**: Diatonic, circle of fifths, chromatic mediants
- **Voice Leading**: Species counterpoint rules, proper resolutions
- **Form**: Binary (AB), ternary (ABA), rondo, sonata
- **Dynamics**: Velocity mapping, tempo changes, articulations

### Orchestration

- **Strings**: Violin, viola, cello, double bass
- **Woodwinds**: Flute, oboe, clarinet, bassoon
- **Brass**: Trumpet, French horn, trombone, tuba
- **Percussion**: Timpani, orchestral bells, xylophone
- **Keyboard**: Piano, harp

## Project Goals

### Phase 1: Core AI Composition (Current)

- [x] Basic AI client with Gemini integration
- [x] Schema-driven composition models
- [x] MIDI and audio export pipeline
- [x] CLI interface with compose command
- [x] Quality validation system

### Phase 2: Enhanced Musicality

- [ ] Multi-turn generation for longer pieces
- [ ] Theme and variation development
- [ ] Improved orchestration presets
- [ ] Better handling of rubato and expression

### Phase 3: Professional Features

- [ ] MusicXML export for notation software
- [ ] LilyPond/PDF sheet music generation
- [ ] Virtual instrument plugin export
- [ ] Project file generation (DAW formats)

### Phase 4: Advanced AI

- [ ] Function calling tools for iterative composition
- [ ] Multi-movement work generation
- [ ] Style transfer capabilities
- [ ] Collaborative human-in-the-loop editing

## Use Cases

1. **Game Developers**: Generate adaptive music for game states
2. **Filmmakers**: Create temp tracks and underscore
3. **Content Creators**: Background music for videos, podcasts
4. **Composers**: Inspiration and starting point for arrangements
5. **Educators**: Teach music theory through examples
6. **Hobbyists**: Explore composition without theory barrier

## Design Principles

1. **Natural Language First**: Music theory knowledge should be optional
2. **Quality Over Quantity**: Better to generate shorter, better music
3. **Standard Formats**: Output should work with existing tools
4. **Extensible**: Easy to add new instruments, styles, and features
5. **Type Safe**: Pydantic models catch errors before generation

## Dependencies

| Component | Technology | Purpose |
|-----------|------------|---------|
| AI Model | Google Gemini 2.5 Pro | Music generation |
| Data Models | Pydantic v2 | Type safety and validation |
| MIDI I/O | mido | File format handling |
| Audio | pretty-midi, pydub | Synthesis and export |
| Music Theory | music21 | Reference and utilities |
| Configuration | python-dotenv, TOML | Settings management |

## Contributing

The project is open to contributions in:
- Prompt engineering improvements
- New preset styles
- Orchestration presets
- Quality validation rules
- Documentation and examples
- Bug fixes and performance improvements

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
