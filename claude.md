# Project Context: Music Generation Library

## Project Information

**Project Name**: musicgen-lib
**Project Description**: A Python library that generates orchestral instrumental music using traditional music theory principles (rule-based composition, not AI). Outputs both sheet music (MusicXML/LilyPond) and audio files (WAV/FLAC).

---
## use ruff check for typechecking and fixing the errors. 
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


## Commit Convention

After completing each step:

```bash
git add .
git commit -m "feat: complete [step-name]

- [Summary of changes]
- [Any technical notes]
- [Reference decisions.md if applicable]

```

---

## Testing Requirements

1. **Write tests** for all code created
2. **Run tests** before considering a step complete
3. **All tests must pass** before code review
4. Test files should be co-located with source code in `tests/`

### Test Commands

```bash

# Run linting 
ruff check 
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src/musicgen --cov-report=html

# Run specific test file
pytest tests/test_note.py
```

Prefer to use uv commands instead of pip. uv is our package manager. uv add <package-name> to add packages. uv sync to sync the environment. and uv run <command> to run commands in the environment.


