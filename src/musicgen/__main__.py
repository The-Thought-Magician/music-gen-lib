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

# Try to import AI components (old orchestration plan approach)
try:
    from musicgen.ai import GeminiComposer, build_composition_from_plan
    from musicgen.ai.models import OrchestrationPlan
    AI_ORCHESTRATION_AVAILABLE = True
except ImportError:
    AI_ORCHESTRATION_AVAILABLE = False

# Try to import new AI note-level components
try:
    from musicgen.composer_new import AIComposer, ValidationError
    from musicgen.composer_new.presets import get_preset, list_presets
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

    # AI command (old AI-powered generation with orchestration plans)
    if AI_ORCHESTRATION_AVAILABLE:
        ai_parser = subparsers.add_parser("ai", help="Generate music using AI (orchestration plan approach)")
        ai_parser.add_argument(
            "prompt",
            nargs="*",
            help="Natural language description of desired music"
        )
        ai_parser.add_argument(
            "--duration",
            type=int,
            default=180,
            help="Duration in seconds (default: 180)"
        )
        ai_parser.add_argument(
            "--form",
            choices=["binary", "ternary", "rondo", "sonata", "through_composed"],
            help="Musical form"
        )
        ai_parser.add_argument(
            "--output-dir", "-o",
            default=".",
            help="Output directory for generated files"
        )
        ai_parser.add_argument(
            "--format", "-f",
            dest="formats",
            action="append",
            choices=["midi", "wav", "mp3", "musicxml", "pdf"],
            help="Export format (can specify multiple, default: midi, mp3)"
        )
        ai_parser.add_argument(
            "--seed",
            type=int,
            help="Random seed for reproducibility"
        )
        ai_parser.add_argument(
            "--api-key",
            help="Google API key (or set GOOGLE_API_KEY env var)"
        )
        ai_parser.add_argument(
            "--save-plan",
            action="store_true",
            help="Save the orchestration plan as JSON"
        )

    # From-file command (read prompt from file)
    if AI_ORCHESTRATION_AVAILABLE:
        file_parser = subparsers.add_parser("from-file", help="Generate music from a prompt file")
        file_parser.add_argument(
            "prompt_file",
            help="File containing the prompt (default: userprompt.txt)"
        )
        file_parser.add_argument(
            "--duration",
            type=int,
            default=180,
            help="Duration in seconds (default: 180)"
        )
        file_parser.add_argument(
            "--watch", "-w",
            action="store_true",
            help="Watch file for changes and regenerate"
        )
        file_parser.add_argument(
            "--output-dir", "-o",
            default=".",
            help="Output directory for generated files"
        )
        file_parser.add_argument(
            "--format", "-f",
            dest="formats",
            action="append",
            choices=["midi", "wav", "mp3", "musicxml", "pdf"],
            help="Export format"
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

    elif args.command == "ai" and AI_ORCHESTRATION_AVAILABLE:
        return cmd_ai(args)

    elif args.command == "from-file" and AI_ORCHESTRATION_AVAILABLE:
        return cmd_from_file(args)

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

    # Check AI orchestration plan support (old ai command)
    print("AI Orchestration Plan:")
    if AI_ORCHESTRATION_AVAILABLE:
        print("  Package: ✓ Installed")
    else:
        print("  Package: ✗ Not available")

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


def cmd_ai(args) -> int:
    """Execute AI generation command.

    Args:
        args: Parsed arguments

    Returns:
        Exit code
    """
    if not args.prompt:
        print("Error: Prompt required", file=sys.stderr)
        print("Usage: musicgen ai \"your description of desired music\"", file=sys.stderr)
        return 1

    prompt = " ".join(args.prompt)

    # Set default formats if none specified
    formats = args.formats or ["midi", "mp3"]

    print(f"Analyzing prompt: \"{prompt[:50]}...\"")

    try:
        # Create AI composer
        composer = GeminiComposer(api_key=args.api_key)

        # Extract parameters
        print("Generating orchestration plan...")
        plan = composer.extract_parameters(
            prompt=prompt,
            duration_seconds=args.duration,
            form_type=args.form
        )

        print(f"  Title: {plan.title}")
        print(f"  Key: {plan.key} {plan.key_type}")
        print(f"  Scale: {plan.scale_type}")
        print(f"  Tempo: {plan.tempo} BPM")
        print(f"  Form: {plan.form_type}")
        print(f"  Sections: {len(plan.sections)}")

        # Save plan if requested
        if args.save_plan:
            import json
            plan_path = Path(args.output_dir) / f"{plan.title.replace(' ', '_')}_plan.json"
            with open(plan_path, 'w') as f:
                json.dump(plan.model_dump(), f, indent=2)
            print(f"  Plan saved: {plan_path}")

        # Build composition
        print("Building composition...")
        score = build_composition_from_plan(plan, seed=args.seed)

        # Export using MIDI writer
        from musicgen.io.midi_writer import MIDIWriter

        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        base_name = plan.title.replace(' ', '_')
        midi_path = None
        audio_path = None

        # Generate MIDI (always needed for audio)
        if "midi" in formats or "wav" in formats or "mp3" in formats:
            midi_path = str(output_dir / f"{base_name}.mid")
            MIDIWriter.write(score, midi_path, tempo=plan.tempo)
            if "midi" in formats:
                print(f"  MIDI: {midi_path}")

        # Generate audio
        if ("wav" in formats or "mp3" in formats) and midi_path and AUDIO_AVAILABLE:
            from musicgen.io.audio_synthesizer import AudioSynthesizer
            try:
                synth = AudioSynthesizer()
                if "wav" in formats:
                    wav_path = str(output_dir / f"{base_name}.wav")
                    synth.render(midi_path, wav_path, "wav")
                    print(f"  WAV: {wav_path}")
                if "mp3" in formats:
                    mp3_path = str(output_dir / f"{base_name}.mp3")
                    synth.render(midi_path, mp3_path, "mp3")
                    print(f"  MP3: {mp3_path}")
            except Exception as e:
                print(f"  Audio generation skipped: {e}")

        print(f"\nDone! Composition saved to {output_dir}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_from_file(args) -> int:
    """Execute from-file command.

    Args:
        args: Parsed arguments

    Returns:
        Exit code
    """
    prompt_file = Path(args.prompt_file)

    if not prompt_file.exists():
        # Try default location
        prompt_file = Path("userprompt.txt")
        if not prompt_file.exists():
            print(f"Error: Prompt file not found: {args.prompt_file}", file=sys.stderr)
            print("Create userprompt.txt with your description, or specify a file", file=sys.stderr)
            return 1

    def generate_from_file():
        """Generate music from the prompt file."""
        with open(prompt_file) as f:
            prompt = f.read().strip()

        if not prompt:
            print(f"Error: Prompt file is empty: {prompt_file}", file=sys.stderr)
            return 1

        print(f"Reading prompt from: {prompt_file}")
        print(f"Prompt: {prompt[:100]}...")

        # Create args object for cmd_ai
        class Args:
            pass
        ai_args = Args()
        ai_args.prompt = [prompt]
        ai_args.duration = args.duration
        ai_args.form = None
        ai_args.output_dir = args.output_dir
        ai_args.formats = args.formats or ["midi", "mp3"]
        ai_args.seed = None
        ai_args.api_key = None
        ai_args.save_plan = False

        return cmd_ai(ai_args)

    if args.watch:
        # Watch mode
        print(f"Watching {prompt_file} for changes (Ctrl+C to stop)...")
        print()

        last_mtime = prompt_file.stat().st_mtime

        try:
            while True:
                current_mtime = prompt_file.stat().st_mtime
                if current_mtime != last_mtime:
                    print(f"\n[{time.strftime('%H:%M:%S')}] File changed, regenerating...")
                    generate_from_file()
                    last_mtime = current_mtime
                    print("\nWatching for changes...")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopped watching.")
            return 0
    else:
        return generate_from_file()


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
