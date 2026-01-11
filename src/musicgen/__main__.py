"""Command-line interface for MusicGen.

This module provides the CLI for generating music from the command line,
including support for mood-based and AI-powered generation.
"""

import sys
import os
import argparse
import time
from pathlib import Path

from musicgen.generator import generate, CompositionRequest, list_available_moods

# Try to import AI components
try:
    from musicgen.ai import GeminiComposer, build_composition_from_plan
    from musicgen.ai.models import OrchestrationPlan
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Try to import audio components
try:
    from musicgen.io.audio_synthesizer import check_audio_support
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False


def main(argv: list = None) -> int:
    """Main CLI entry point.

    Args:
        argv: Command line arguments (uses sys.argv if None)

    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        prog="musicgen",
        description="Generate rule-based orchestral music compositions"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

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
        help="Export format (can specify multiple, default: midi)"
    )
    gen_parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducibility"
    )

    # AI command (AI-powered generation)
    if AI_AVAILABLE:
        ai_parser = subparsers.add_parser("ai", help="Generate music using AI from a prompt")
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
            help="Export format (can specify multiple, default: midi)"
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
    if AI_AVAILABLE:
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

    elif args.command == "ai" and AI_AVAILABLE:
        return cmd_ai(args)

    elif args.command == "from-file" and AI_AVAILABLE:
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

    # Check AI support
    print("AI Support:")
    if AI_AVAILABLE:
        from musicgen.ai.client import check_gemini_available
        ai_status = check_gemini_available()
        print(f"  Package: {'✓' if ai_status['available'] else '✗'} google-genai")
        print(f"  API Key: {'✓' if ai_status['api_key_set'] else '✗'} Set GOOGLE_API_KEY")
    else:
        print("  Package: ✗ google-genai (install with: uv add --optional ai google-genai)")

    print()

    # Check audio support
    print("Audio Support:")
    if AUDIO_AVAILABLE:
        audio_status = check_audio_support()
        print(f"  FluidSynth: {'✓' if audio_status['fluidsynth'] else '✗'}")
        print(f"  pydub: {'✓' if audio_status['pydub'] else '✗'}")
        print(f"  ffmpeg: {'✓' if audio_status['ffmpeg'] else '✗'}")
        if audio_status['soundfont']:
            print(f"  SoundFont: ✓ {audio_status['soundfont']}")
        else:
            print(f"  SoundFont: ✗ (will download on first use)")
    else:
        print("  Audio module not available")

    return 0


def cmd_generate(args) -> int:
    """Execute generate command.

    Args:
        args: Parsed arguments

    Returns:
        Exit code
    """
    # Set default formats if none specified
    formats = args.formats or ["midi"]

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
    formats = args.formats or ["midi"]

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

        # Generate MIDI
        if "midi" in formats:
            midi_path = str(output_dir / f"{base_name}.mid")
            MIDIWriter.write(score, midi_path, tempo=plan.tempo)
            print(f"  MIDI: {midi_path}")

        # Generate audio
        if "wav" in formats or "mp3" in formats:
            if midi_path and AUDIO_AVAILABLE:
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
        with open(prompt_file, 'r') as f:
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
        ai_args.formats = args.formats or ["midi"]
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


if __name__ == "__main__":
    sys.exit(main())
