# Project Context: Music Generation Library

## Project Information

**Project Name**: musicgen-lib
**Project Description**: A Python library that generates orchestral instrumental music using traditional music theory principles (rule-based composition, not AI). Outputs both sheet music (MusicXML/LilyPond) and audio files (WAV/FLAC).

---

## Enabled Plugins

This project has the following plugins installed in `.claude/settings.json`:

| Plugin | Purpose |
|--------|---------|
| `python-development` | Python 3.12+ development support |
| `unit-testing` | Automated test generation |
| `code-review-ai` | Architectural analysis, security assessment |
| `comprehensive-review` | Multi-perspective code analysis |
| `code-documentation` | Documentation generation |

**Required Review Plugins** (always use both):
- `code-review-ai` - Architectural analysis, security assessment
- `comprehensive-review` - Multi-perspective code analysis

---

## Documentation Locations

All project documentation is in the `docs/` folder:

| File | Purpose |
|------|---------|
| `docs/idea.md` | Original idea description |
| `docs/research.md` | Implementation research and tech stack decisions |
| `docs/plan.md` | Complete step-by-step implementation plan (13 steps) |
| `docs/steps/` | Individual step prompt files |
| `docs/steps/review-sub-steps/` | Fix sub-steps from code reviews |
| `docs/decisions.md` | All decisions with reasoning |
| `docs/reviews/` | Code review artifacts |

---

## Branch Management

**CRITICAL**: Always work on feature branches

1. Before starting a step, create a feature branch:
   ```bash
   git checkout -b feature/[step-name]
   ```

2. Never commit directly to `main`

3. Merge to `main` only when the entire project is complete

4. Delete feature branches after merging

---

## Commit Convention

After completing each step:

```bash
git add .
git commit -m "feat: complete [step-name]

- [Summary of changes]
- [Any technical notes]
- [Reference decisions.md if applicable]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Testing Requirements

1. **Write tests** for all code created
2. **Run tests** before considering a step complete
3. **All tests must pass** before code review
4. Test files should be co-located with source code in `tests/`

### Test Commands

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src/musicgen --cov-report=html

# Run specific test file
pytest tests/test_note.py
```

---

## Code Review Process

After each step completion, run BOTH review plugins:

1. **code-review-ai**
   ```bash
   claude-z -p --permission-mode bypassPermissions --agent code-review-ai "Review the changes in this step"
   ```
   Save output to: `docs/reviews/[step-name]-review-1-a.md`

2. **comprehensive-review**
   ```bash
   claude-z -p --permission-mode bypassPermissions --agent comprehensive-review "Review the changes in this step"
   ```
   Save output to: `docs/reviews/[step-name]-review-1-b.md`

3. **Address any issues** found in reviews
   - Create fix sub-step if needed
   - Add decision to `docs/decisions.md`
   - Re-run reviews until clean

---

## README Updates

After each step completion, update `README.md` with:
- New features added
- Configuration changes
- New dependencies
- Setup/usage changes
- API changes (if applicable)

---

## Step Execution Workflow

For each step in `docs/plan.md`:

1. Read the step file from `docs/steps/XX-step-name.md`
2. Create feature branch
3. Execute the prompt using `claude-z -p --permission-mode bypassPermissions "[prompt content]"`
4. Implement the code
5. Write/run tests
6. Run linting
7. Get user approval
8. Run code reviews (both plugins)
9. Fix any issues (create sub-steps if needed)
10. Commit changes
11. Update README.md
12. Wait for user approval before proceeding

---

## Tech Stack

Based on `docs/research.md`:

| Component | Technology |
|-----------|------------|
| Language | Python 3.12+ |
| Music Theory | music21, mingus |
| MIDI I/O | mido, pretty_midi |
| Audio Synthesis | FluidSynth, pyfluidsynth |
| Sheet Music | Abjad, LilyPond |
| SoundFont | GeneralUser GS |
| Audio Processing | pydub |

---

## External Dependencies

| Dependency | Type | Notes |
|------------|------|-------|
| FluidSynth | System package | `sudo apt install fluidsynth` |
| LilyPond | System package | `sudo apt install lilypond` |
| GeneralUser GS | SoundFont | Download from schristiancollins.com |

---

## Development Commands

```bash
# Install Python dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src/musicgen --cov-report=html

# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

---

## Project Structure (to be created)

```
music-gen-lib/
├── src/
│   └── musicgen/
│       ├── __init__.py
│       ├── core/           # Note, Chord, Rest classes
│       ├── theory/         # Scales, keys, progressions, voice leading
│       ├── composition/    # Melody, forms
│       ├── orchestration/  # Instruments, ensembles
│       ├── io/             # MIDI, audio, sheet music writers
│       ├── config/         # Mood configurations
│       └── generator.py    # Main API
├── tests/
├── examples/
├── docs/
├── pyproject.toml
├── README.md
└── claude.md
```

---

## Notes

- This is a complex project requiring deep music theory knowledge
- Rule-based composition (NOT AI/ML based)
- Target output: Orchestral-quality music
- Phase 1 (Steps 1-4) establish the music theory foundation
- Phase 2 (Steps 5-7) implement composition engines
- Phase 3 (Steps 8-11) handle export (MIDI, audio, sheet music)
- Phase 4 (Steps 12-13) complete the user interface and documentation
