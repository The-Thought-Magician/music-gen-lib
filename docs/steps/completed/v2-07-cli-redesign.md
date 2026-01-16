# Step 7: CLI Redesign (AI-First Interface)

## Objective

Redesign the CLI for the new AI-first architecture. Simple, intuitive commands focused on prompt-based composition.

## Overview

The old CLI had separate `generate` (mood-based) and `ai` commands. The new CLI is unified around prompts.

## New CLI Structure

```
musicgen compose "A peaceful piano melody"           # Basic
musicgen compose "Jazz piece" -f midi wav mp3       # Multiple formats
musicgen compose -f prompt.txt                       # From file
musicgen compose --preset classical_piano            # Using preset
musicgen compose "Melody" --temperature 0.7          # Custom settings

musicgen presets list                                # List presets
musicgen check                                       # Check system
```

## Tasks

### 7.1 Redesign Main CLI

Rewrite `src/musicgen/__main__.py`:

```python
"""MusicGen CLI - AI-first music generation."""

from __future__ import annotations
import sys
import argparse
import logging
from pathlib import Path

try:
    from dotenv import load_dotenv
    _env_path = Path.cwd() / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    pass

# Check dependencies
try:
    from musicgen.composer import AIComposer, compose, ValidationError
    from musicgen.composer.presets import list_presets, get_preset
    from musicgen.renderer import Renderer
    AI_AVAILABLE = True
except ImportError as e:
    AI_AVAILABLE = False
    ImportError = type(e)

try:
    from musicgen.ai_client import check_availability
    CHECK_AVAILABLE = True
except ImportError:
    CHECK_AVAILABLE = False


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger(__name__)


def main(argv: list = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="musicgen",
        description="Generate music using AI",
        epilog="Examples:\n"
               "  musicgen compose \"A peaceful piano melody\"\n"
               "  musicgen compose -f prompt.txt --output-dir output\n"
               "  musicgen compose --preset epic_orchestral -f midi wav mp3\n"
               "  musicgen presets list",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # COMPOSE command (primary)
    compose_parser = subparsers.add_parser(
        "compose",
        help="Generate music from a prompt",
        description="Generate music from a natural language prompt."
    )
    compose_parser.add_argument(
        "prompt",
        nargs="*",
        help="Natural language description (e.g., 'A jazz piece in F minor')"
    )
    compose_parser.add_argument(
        "-f", "--prompt-file",
        dest="prompt_file",
        help="Read prompt from file"
    )
    compose_parser.add_argument(
        "--preset",
        choices=list_presets() if AI_AVAILABLE else [],
        help="Use a preset prompt template"
    )
    compose_parser.add_argument(
        "--output-dir", "-o",
        default=".",
        help="Output directory (default: current directory)"
    )
    compose_parser.add_argument(
        "--format", "-f",
        dest="formats",
        action="append",
        choices=["midi", "wav", "mp3", "json"],
        help="Output format (can specify multiple, default: midi)"
    )
    compose_parser.add_argument(
        "--output-name",
        help="Base name for output files (default: from composition title)"
    )
    compose_parser.add_argument(
        "--temperature",
        type=float,
        help="AI sampling temperature (0.0-1.0, default: from config)"
    )
    compose_parser.add_argument(
        "--model",
        help="AI model to use (default: from config)"
    )
    compose_parser.add_argument(
        "--save-prompt",
        action="store_true",
        help="Save the prompt to a file"
    )
    compose_parser.add_argument(
        "--save-json",
        action="store_true",
        help="Save the composition as JSON"
    )
    compose_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    # PRESETS command
    presets_parser = subparsers.add_parser(
        "presets",
        help="Manage prompt presets"
    )
    presets_parser.add_argument(
        "action",
        choices=["list", "show"],
        help="Action: list all presets or show a specific preset"
    )
    presets_parser.add_argument(
        "name",
        nargs="?",
        help="Preset name (for 'show' action)"
    )

    # CHECK command
    check_parser = subparsers.add_parser(
        "check",
        help="Check system capabilities"
    )

    # Parse
    args = parser.parse_args(argv)

    # Default to showing help if no command
    if args.command is None:
        parser.print_help()
        return 0

    # Execute
    if args.command == "compose":
        return cmd_compose(args)
    elif args.command == "presets":
        return cmd_presets(args)
    elif args.command == "check":
        return cmd_check(args)

    return 1


def cmd_compose(args) -> int:
    """Execute compose command."""
    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Get prompt
    prompt = _get_prompt(args)
    if not prompt:
        logger.error("No prompt provided. Use: musicgen compose \"your prompt\"")
        return 1

    logger.info(f"Prompt: {prompt[:100]}...")

    # Get formats
    formats = args.formats or ["midi"]

    try:
        # Initialize composer
        composer = AIComposer(
            model=args.model,
            temperature=args.temperature,
        )

        # Generate
        logger.info("Generating composition...")
        composition = composer.generate(prompt)

        logger.info(f"Generated: {composition.title}")
        logger.info(f"  Key: {composition.key}")
        logger.info(f"  Tempo: {composition.tempo} BPM")
        logger.info(f"  Duration: {composition.duration_seconds:.1f}s")
        logger.info(f"  Instruments: {', '.join(composition.instrument_names)}")

        # Save prompt if requested
        if args.save_prompt:
            prompt_path = Path(args.output_dir) / f"{args.output_name or 'prompt'}.txt"
            prompt_path.write_text(prompt)
            logger.info(f"  Prompt saved: {prompt_path}")

        # Save JSON if requested
        if "json" in formats or args.save_json:
            json_path = Path(args.output_dir) / f"{args.output_name or composition.title.replace(' ', '_')}.json"
            json_path.write_text(composition.model_dump_json(indent=2))
            logger.info(f"  JSON: {json_path}")

        # Render to MIDI/Audio
        if any(f in formats for f in ["midi", "wav", "mp3"]):
            renderer = Renderer(output_dir=Path(args.output_dir))
            results = renderer.render(
                composition,
                formats=[f for f in formats if f in ["midi", "wav", "mp3"]],
                output_name=args.output_name,
            )
            for fmt, path in results.items():
                logger.info(f"  {fmt.upper()}: {path}")

        return 0

    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cmd_presets(args) -> int:
    """Execute presets command."""
    if not AI_AVAILABLE:
        logger.error("Presets not available")
        return 1

    if args.action == "list":
        logger.info("Available presets:")
        for preset in list_presets():
            logger.info(f"  - {preset}")
        return 0

    elif args.action == "show":
        if not args.name:
            logger.error("Please specify a preset name")
            return 1
        try:
            preset = get_preset(args.name)
            logger.info(f"preset: {args.name}")
            logger.info(preset)
            return 0
        except KeyError:
            logger.error(f"Unknown preset: {args.name}")
            return 1


def cmd_check(args) -> int:
    """Execute check command."""
    logger.info("MusicGen System Check")
    logger.info("")

    # AI support
    logger.info("AI Support:")
    if CHECK_AVAILABLE:
        status = check_availability()
        logger.info(f"  google-genai: {'✓' if status['package_installed'] else '✗'}")
        logger.info(f"  API Key: {'✓' if status['api_key_set'] else '✗'} (Set GOOGLE_API_KEY)")
        logger.info(f"  Overall: {'✓ Ready' if status['available'] else '✗ Not ready'}")
    else:
        logger.info("  ✗ google-genai not installed")

    logger.info("")

    # Rendering support
    logger.info("Rendering Support:")
    try:
        import mido
        logger.info("  mido: ✓ (MIDI export)")
    except ImportError:
        logger.info("  mido: ✗ (pip install mido)")

    try:
        import pretty_midi
        logger.info("  pretty-midi: ✓ (audio synthesis)")
    except ImportError:
        logger.info("  pretty-midi: ✗ (pip install pretty-midi)")

    try:
        import pydub
        logger.info("  pydub: ✓ (MP3 export)")
    except ImportError:
        logger.info("  pydub: ✗ (pip install pydub)")

    return 0


def _get_prompt(args) -> str | None:
    """Get prompt from arguments or file."""
    # From file
    if args.prompt_file:
        return Path(args.prompt_file).read_text().strip()

    # From preset
    if args.preset:
        preset = get_preset(args.preset)
        base = preset
        if args.prompt:
            base += " " + " ".join(args.prompt)
        return base

    # From arguments
    if args.prompt:
        return " ".join(args.prompt)

    return None


if __name__ == "__main__":
    sys.exit(main())
```

### 7.2 Update pyproject.toml

Update entry point if needed:

```toml
[project.scripts]
musicgen = "musicgen.__main__:main"
```

### 7.3 Update .env.example

```bash
# MusicGen Configuration

# Google AI
GOOGLE_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-2.5-pro
GEMINI_TEMPERATURE=0.5
GEMINI_MAX_TOKENS=

# Output
DEFAULT_OUTPUT_DIR=./output
DEFAULT_FORMATS=midi,wav
```

### 7.4 Documentation

Create `docs/usage.md`:

```markdown
# MusicGen CLI Usage

## Basic Usage

```bash
# Generate from a prompt
musicgen compose "A peaceful piano melody in C major"

# Specify output formats
musicgen compose "Jazz trio" -f midi wav mp3

# Read prompt from file
musicgen compose -f prompt.txt

# Use a preset
musicgen compose --preset epic_orchestral

# Combine preset with custom text
musicgen compose --preset jazz_trio "with a saxophone solo"
```

## Presets

List available presets:
```bash
musicgen presets list
```

Show a preset:
```bash
musicgen presets show classical_piano
```

## System Check

```bash
musicgen check
```

## Options

- `--output-dir, -o`: Output directory
- `--format, -f`: Output format (midi, wav, mp3, json)
- `--output-name`: Base name for output files
- `--temperature`: AI creativity (0.0-1.0)
- `--model`: AI model to use
- `--save-prompt`: Save the prompt to file
- `--save-json`: Save composition as JSON
- `--verbose, -v`: Verbose output
```

## Deliverables

- Updated `src/musicgen/__main__.py`
- Updated `docs/usage.md`
- Updated `.env.example`

## Next Steps

After completing this step:
- Step 8: Type safety with ruff/mypy
- Final: Testing and documentation
