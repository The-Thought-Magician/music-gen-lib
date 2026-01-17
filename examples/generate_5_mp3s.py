#!/usr/bin/env python
"""Generate 5 music compositions from human-like prompts.

This script demonstrates the V3 AI composer by generating 5 different
compositions from natural language prompts and rendering them to MP3.
"""

import os
from pathlib import Path

from musicgen.composer_v3 import AIComposerV3

# Set API key (use environment variable or default)
GOOGLE_API_KEY = os.environ.get(
    "GOOGLE_API_KEY",
    "***REMOVED***"
)

# 5 human-like prompts for music generation
PROMPTS = [
    {
        "prompt": "A melancholic cello solo in D minor, slow and expressive like someone saying goodbye",
        "filename": "01_cello_goodbye.mp3",
        "duration": 30,
        "key": "D minor",
        "style": "romantic",
    },
    {
        "prompt": "An upbeat jazz piano piece with a walking bass, feel like a rainy Sunday morning in Paris",
        "filename": "02_jazz_piano_paris.mp3",
        "duration": 45,
        "key": "F major",
        "style": "modern",
    },
    {
        "prompt": "Epic orchestral trailer music with powerful brass and soaring strings, building to a heroic climax",
        "filename": "03_epic_trailer.mp3",
        "duration": 60,
        "key": "C minor",
        "style": "film_score",
    },
    {
        "prompt": "A gentle lullaby for music box and soft strings, like watching stars on a quiet summer night",
        "filename": "04_lullaby_stars.mp3",
        "duration": 40,
        "key": "G major",
        "style": "classical",
    },
    {
        "prompt": "Dark ambient electronic drone with unsettling textures, feels like exploring an abandoned spaceship",
        "filename": "05_dark_ambient.mp3",
        "duration": 50,
        "key": "C minor",
        "style": "modern",
    },
]


def main():
    """Generate all 5 compositions."""
    print("=" * 70)
    print("V3 AI Music Generator - 5 Compositions")
    print("=" * 70)
    print()

    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Initialize composer
    print("Initializing AI Composer...")
    composer = AIComposerV3(gemini_api_key=GOOGLE_API_KEY)
    print(f"Output directory: {output_dir.absolute()}")
    print()

    results = []

    for i, config in enumerate(PROMPTS, 1):
        print("-" * 70)
        print(f"[{i}/5] {config['filename']}")
        print("-" * 70)
        print(f"Prompt: {config['prompt']}")
        print()

        output_path = output_dir / config['filename']

        try:
            # Generate and render
            print("Generating composition...")
            composition, audio_path = composer.compose_and_render(
                prompt=config['prompt'],
                output_path=output_path,
                duration_seconds=config['duration'],
                key_signature=config['key'],
                style_period=config['style'],
                format='mp3',
                validate=False,  # Skip validation for faster generation
            )

            print(f"Title: {composition.title}")
            print(f"Instruments: {composition.instrument_count}")
            print(f"Duration: {composition.duration:.1f} seconds")
            print(f"Saved to: {audio_path}")
            results.append(("SUCCESS", config['filename'], None))

        except Exception as e:
            print(f"Error: {e}")
            results.append(("FAILED", config['filename'], str(e)))

        print()

    # Summary
    print("=" * 70)
    print("GENERATION SUMMARY")
    print("=" * 70)
    for status, filename, error in results:
        status_symbol = "[OK]" if status == "SUCCESS" else "[XX]"
        print(f"{status_symbol} {filename}")
        if error:
            print(f"     Error: {error}")
    print()

    successful = sum(1 for s, _, _ in results if s == "SUCCESS")
    print(f"Generated: {successful}/5 compositions")
    print(f"Output directory: {output_dir.absolute()}")
    print("=" * 70)


if __name__ == "__main__":
    main()
