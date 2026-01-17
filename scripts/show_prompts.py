#!/usr/bin/env python3
"""Show the prompts and schema that will be sent to the AI."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from musicgen.ai_client.prompts import PromptBuilder
from musicgen.schema import get_schema


def show_prompt_for(user_prompt: str):
    """Show the full prompt that would be sent to AI for a given user prompt.

    Args:
        user_prompt: The user's description of desired music
    """
    print("=" * 80)
    print(f"PROMPT DEBUG FOR: '{user_prompt}'")
    print("=" * 80)

    # Generate schema
    print("\n" + "="*80)
    print("SCHEMA (sent to AI)")
    print("="*80)
    schema = get_schema()
    print(schema)

    # Build prompts
    print("\n" + "="*80)
    print("SYSTEM PROMPT")
    print("="*80)
    builder = PromptBuilder()
    system_prompt, user_prompt_full = builder.build_prompt(user_prompt, schema)
    print(system_prompt)

    print("\n" + "="*80)
    print("USER PROMPT")
    print("="*80)
    print(user_prompt_full)

    print("\n" + "="*80)
    print("EXPECTED OUTPUT FORMAT")
    print("="*80)
    print("""
The AI should return ONLY a JSON object like:

{
  "title": "composition title",
  "tempo": 120,
  "time_signature": {"numerator": 4, "denominator": 4},
  "key": {"tonic": "C", "mode": "major"},
  "parts": [
    {
      "name": "piano",
      "midi_program": 0,
      "midi_channel": 0,
      "role": "melody",
      "notes": [
        {"note_name": "C4", "duration": 1.0, "velocity": 80},
        {"note_name": "E4", "duration": 0.5, "velocity": 75},
        ...
      ]
    }
  ]
}
""")


if __name__ == "__main__":
    # Example prompts to debug
    examples = [
        "A peaceful piano melody in C major",
        "An epic orchestral piece with full orchestra",
        "A jazz piano trio with walking bass",
    ]

    if len(sys.argv) > 1:
        show_prompt_for(" ".join(sys.argv[1:]))
    else:
        for example in examples:
            show_prompt_for(example)
            print("\n\n")
