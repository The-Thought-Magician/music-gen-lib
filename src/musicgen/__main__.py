"""Command-line interface for MusicGen.

This module provides the CLI for generating music from the command line,
including support for mood-based and AI-powered generation.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

# Load .env file if present (for API keys)
try:
    from dotenv import load_dotenv
    _env_path = Path.cwd() / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    pass

from musicgen.generator import CompositionRequest, generate, list_available_moods

# Try to import YAML engine
try:
    from musicgen.engine import generate_from_yaml
    YAML_ENGINE_AVAILABLE = True
except ImportError:
    YAML_ENGINE_AVAILABLE = False

# Try to import AI note-level components
try:
    from musicgen.composer import AIComposer, ValidationError
    from musicgen.composer.presets import get_preset, list_presets
    AI_COMPOSE_AVAILABLE = True
except ImportError:
    AI_COMPOSE_AVAILABLE = False

# Try to import AI client
try:
    from musicgen.ai_client import check_availability
    AI_CLIENT_AVAILABLE = True
except ImportError:
    AI_CLIENT_AVAILABLE = False

# Try to import audio components
try:
    from musicgen.io.audio_synthesizer import check_audio_support
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

# Try to import renderer
try:
    from musicgen.renderer import Renderer
    RENDERER_AVAILABLE = True
except ImportError:
    RENDERER_AVAILABLE = False


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger(__name__)


def main(argv: list = None) -> int:
    """Main CLI entry point.

    Args:
        argv: Command line arguments (uses sys.argv if None)

    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        prog="musicgen",
        description="Generate rule-based and AI-powered music compositions",
        epilog="Examples:\n"
               "  musicgen compose \"A peaceful piano melody\"\n"
               "  musicgen compose -f prompt.txt --output-dir output\n"
               "  musicgen compose --preset epic_orchestral -f midi wav mp3\n"
               "  musicgen presets list",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # COMPOSE command (new AI-first approach)
    if AI_COMPOSE_AVAILABLE:
        compose_parser = subparsers.add_parser(
            "compose",
            help="Generate music from a prompt (AI note-level composition)"
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
            choices=list_presets() if AI_COMPOSE_AVAILABLE else [],
            help="Use a preset prompt template"
        )
        compose_parser.add_argument(
            "--output-dir", "-o",
            default=".",
            help="Output directory (default: current directory)"
        )
        compose_parser.add_argument(
            "--format",
            dest="formats",
            action="append",
            choices=["midi", "wav", "mp3", "json"],
            help="Output format (can specify multiple, default: midi, mp3)"
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
        compose_parser.add_argument(
            "--genre",
            choices=[
                "rock", "pop", "jazz", "classical", "electronic",
                "indian_classical", "middle_eastern", "east_asian", "latin", "african"
            ],
            help="Music genre for stylistic guidance (affects instrument selection and phrasing)"
        )

    # Generate command (mood-based)
    gen_parser = subparsers.add_parser("generate", help="Generate a composition from mood preset")
    gen_parser.add_argument(
        "--mood",
        choices=list_available_moods(),
        default="peaceful",
        help="Mood preset for the composition"
    )
    gen_parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Duration in seconds (default: 30)"
    )
    gen_parser.add_argument(
        "--tempo",
        type=int,
        help="Tempo in BPM"
    )
    gen_parser.add_argument(
        "--key",
        help="Key (e.g., C, Am, F#m)"
    )
    gen_parser.add_argument(
        "--scale",
        help="Scale type (e.g., major, minor, harmonic_minor)"
    )
    gen_parser.add_argument(
        "--output-dir", "-o",
        default=".",
        help="Output directory for generated files"
    )
    gen_parser.add_argument(
        "--title",
        help="Composition title"
    )
    gen_parser.add_argument(
        "--composer",
        default="MusicGen",
        help="Composer name"
    )
    gen_parser.add_argument(
        "--format", "-f",
        dest="formats",
        action="append",
        choices=["midi", "wav", "mp3", "musicxml", "pdf"],
        help="Export format (can specify multiple, default: midi, mp3)"
    )
    gen_parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducibility"
    )

    # PRESETS command
    if AI_COMPOSE_AVAILABLE:
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

    # YAML command (generate from YAML specification)
    if YAML_ENGINE_AVAILABLE:
        yaml_parser = subparsers.add_parser(
            "yaml",
            help="Generate music from YAML specification"
        )
        yaml_parser.add_argument(
            "yaml_file",
            help="Path to YAML specification file"
        )
        yaml_parser.add_argument(
            "--output", "-o",
            help="Output MIDI file path (default: same as yaml_file with .mid extension)"
        )
        yaml_parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Verbose output"
        )

    # List moods command
    list_parser = subparsers.add_parser("list-moods", help="List available mood presets")

    # Check command (check system support)
    check_parser = subparsers.add_parser("check", help="Check system capabilities")

    # Parse arguments
    args = parser.parse_args(argv)

    # Default to showing help if no command
    if args.command is None:
        parser.print_help()
        return 0

    # Execute command
    if args.command == "list-moods":
        return cmd_list_moods()

    elif args.command == "check":
        return cmd_check()

    elif args.command == "generate":
        return cmd_generate(args)

    elif args.command == "compose" and AI_COMPOSE_AVAILABLE:
        return cmd_compose(args)

    elif args.command == "presets" and AI_COMPOSE_AVAILABLE:
        return cmd_presets(args)

    elif args.command == "yaml" and YAML_ENGINE_AVAILABLE:
        return cmd_yaml(args)

    else:
        print(f"Command '{args.command}' not available", file=sys.stderr)
        return 1


def cmd_list_moods() -> int:
    """List available mood presets.

    Returns:
        Exit code
    """
    print("Available mood presets:")
    for mood in list_available_moods():
        print(f"  - {mood}")
    return 0


def cmd_check() -> int:
    """Check system capabilities.

    Returns:
        Exit code
    """
    print("System Capabilities:")
    print()

    # Check AI support (new compose command)
    print("AI Compose (Note-level):")
    if AI_COMPOSE_AVAILABLE:
        print("  Package: ✓ Installed")
    else:
        print("  Package: ✗ Not available")

    if AI_CLIENT_AVAILABLE:
        status = check_availability()
        print(f"  API Key: {'✓' if status['api_key_set'] else '✗'} Set GOOGLE_API_KEY")
        print(f"  Overall: {'✓ Ready' if status['available'] else '✗ Not ready'}")
    else:
        print("  API Key: ✗ google-genai not installed")

    print()

    # Check rendering support
    print("Rendering Support:")
    try:
        import mido
        print("  mido: ✓ (MIDI export)")
    except ImportError:
        print("  mido: ✗ (pip install mido)")

    try:
        import pretty_midi
        print("  pretty-midi: ✓ (audio synthesis)")
    except ImportError:
        print("  pretty-midi: ✗ (pip install pretty-midi)")

    try:
        import pydub
        print("  pydub: ✓ (MP3 export)")
    except ImportError:
        print("  pydub: ✗ (pip install pydub)")

    return 0


def cmd_generate(args) -> int:
    """Execute generate command.

    Args:
        args: Parsed arguments

    Returns:
        Exit code
    """
    # Set default formats if none specified
    formats = args.formats or ["midi", "mp3"]

    # Create request
    request = CompositionRequest(
        mood=args.mood,
        tempo=args.tempo,
        key=args.key,
        scale=args.scale,
        duration=args.duration,
        output_dir=args.output_dir,
        title=args.title or "",
        composer=args.composer,
        export_formats=formats,
        seed=args.seed
    )

    try:
        result = generate(request)

        print(f"Generated: {result.title}")
        print(f"  Key: {result.key}")
        print(f"  Tempo: {result.tempo} BPM")
        print(f"  Duration: {request.duration} seconds")
        print(f"  Instruments: {', '.join(result.instruments)}")

        if result.midi_path:
            print(f"  MIDI: {result.midi_path}")
        if result.audio_path:
            print(f"  Audio: {result.audio_path}")
        if result.musicxml_path:
            print(f"  MusicXML: {result.musicxml_path}")
        if result.pdf_path:
            print(f"  PDF: {result.pdf_path}")

        return 0

    except Exception as e:
        print(f"Error generating music: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_compose(args) -> int:
    """Execute compose command (new AI-first note-level composition).

    Args:
        args: Parsed arguments

    Returns:
        Exit code
    """
    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Get prompt
    prompt = _get_prompt(args)
    if not prompt:
        logger.error("No prompt provided. Use: musicgen compose \"your prompt\"")
        return 1

    # Enhance prompt with genre if specified
    if hasattr(args, 'genre') and args.genre:
        genre_display = args.genre.replace('_', ' ').title()
        prompt = f"{prompt} (Genre: {genre_display})"
        logger.info(f"Genre: {genre_display}")

    logger.info(f"Prompt: {prompt[:100]}...")

    # Get formats
    formats = args.formats or ["midi", "mp3"]

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
        if RENDERER_AVAILABLE and any(f in formats for f in ["midi", "wav", "mp3"]):
            renderer = Renderer(output_dir=Path(args.output_dir))
            results = renderer.render(
                composition,
                formats=[f for f in formats if f in ["midi", "wav", "mp3"]],
                output_name=args.output_name,
            )
            for fmt, path in results.items():
                logger.info(f"  {fmt.upper()}: {path}")
        elif any(f in formats for f in ["midi", "wav", "mp3"]):
            # Fallback to old MIDI writer
            from musicgen.io.midi_writer import MIDIWriter
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            base_name = args.output_name or composition.title.replace(" ", "_")

            # Build score from composition
            from musicgen.io.midi_writer import Part, Score
            score = Score(title=composition.title, composer="MusicGen AI")

            for part in composition.parts:
                midi_part = Part(name=part.name)
                for note_event in part.get_note_events():
                    if hasattr(note_event, 'note_name'):
                        from musicgen.core.note import QUARTER, Note
                        midi_note = Note(note_event.note_name, note_event.duration, QUARTER)
                        midi_part.notes.append(midi_note)
                score.add_part(midi_part)

            if "midi" in formats:
                midi_path = output_dir / f"{base_name}.mid"
                MIDIWriter.write(score, str(midi_path), tempo=composition.tempo)
                logger.info(f"  MIDI: {midi_path}")

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
    """Execute presets command.

    Args:
        args: Parsed arguments

    Returns:
        Exit code
    """
    if not AI_COMPOSE_AVAILABLE:
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


def cmd_yaml(args) -> int:
    """Execute yaml command (generate from YAML specification).

    Args:
        args: Parsed arguments

    Returns:
        Exit code
    """
    if not YAML_ENGINE_AVAILABLE:
        logger.error("YAML engine not available")
        return 1

    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    yaml_path = Path(args.yaml_file)
    if not yaml_path.exists():
        logger.error(f"YAML file not found: {yaml_path}")
        return 1

    try:
        output_path = args.output or None
        logger.info(f"Generating from YAML: {yaml_path}")

        result_path = generate_from_yaml(yaml_path, output_path)

        logger.info(f"Generated MIDI: {result_path}")
        return 0

    except Exception as e:
        logger.error(f"Error generating from YAML: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def _get_prompt(args) -> str | None:
    """Get prompt from arguments or file.

    Args:
        args: Parsed arguments

    Returns:
        Prompt string or None
    """
    # From file
    if hasattr(args, 'prompt_file') and args.prompt_file:
        return Path(args.prompt_file).read_text().strip()

    # From preset
    if hasattr(args, 'preset') and args.preset:
        preset = get_preset(args.preset)
        base = preset
        if hasattr(args, 'prompt') and args.prompt:
            base += " " + " ".join(args.prompt)
        return base

    # From arguments
    if hasattr(args, 'prompt') and args.prompt:
        return " ".join(args.prompt)

    return None


if __name__ == "__main__":
    sys.exit(main())
