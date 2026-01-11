"""Command-line interface for MusicGen.

This module provides the CLI for generating music from the command line.
"""

import sys
import argparse
from pathlib import Path

from musicgen.generator import generate, CompositionRequest, list_available_moods


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

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a composition")
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
        help="Key (e.g., C, D, F#)"
    )
    gen_parser.add_argument(
        "--scale",
        help="Scale type (e.g., major, minor, harmonic_minor)"
    )
    gen_parser.add_argument(
        "--output-dir",
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
        "--format",
        dest="formats",
        action="append",
        choices=["midi", "audio", "musicxml", "pdf"],
        help="Export format (can specify multiple)"
    )
    gen_parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducibility"
    )

    # List moods command
    list_parser = subparsers.add_parser("list-moods", help="List available mood presets")

    # Parse arguments
    args = parser.parse_args(argv)

    # Default to showing help if no command
    if args.command is None:
        parser.print_help()
        return 0

    # Execute command
    if args.command == "list-moods":
        print("Available mood presets:")
        for mood in list_available_moods():
            print(f"  - {mood}")
        return 0

    elif args.command == "generate":
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
            print(f"  Key: {result.key} {result.scale_type}")
            print(f"  Tempo: {result.tempo} BPM")
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
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
