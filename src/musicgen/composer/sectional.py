"""Sectional composition for long pieces.

Generates compositions section by section to handle long pieces
that would exceed token limits in a single generation.
"""

from __future__ import annotations

from typing import Any

from musicgen.ai_models import AIComposition, AINote, AIPart, AISection, KeySignature, TimeSignature


class SectionalComposer:
    """Generate compositions section by section.

    This approach is useful for:
    - Long compositions (3+ minutes)
    - Multi-movement works
    - Complex orchestral pieces
    """

    def __init__(self, client: Any | None = None):
        """Initialize the sectional composer.

        Args:
            client: Optional AI client (GeminiClient, etc.)
        """
        self.client = client

    def generate_composition(
        self,
        prompt: str,
        structure: list[dict],
        context: dict | None = None,
    ) -> AIComposition:
        """Generate a full composition section by section.

        Args:
            prompt: Overall composition description
            structure: Section definitions [{"name": "A", "bars": 16}, ...]
            context: Musical context (key, tempo, etc.)

        Returns:
            Complete AIComposition
        """
        sections = []
        context = context or {}
        current_bar = 1

        # Set defaults from context
        default_key = context.get("key", KeySignature(tonic="C", mode="major"))
        default_tempo = context.get("tempo", 120)
        default_time_signature = context.get(
            "time_signature",
            TimeSignature(numerator=4, denominator=4)
        )

        for section_def in structure:
            # Determine section length
            length_bars = section_def.get("bars", 16)

            # Generate this section
            section = self._generate_section(
                prompt=prompt,
                section_def=section_def,
                start_bar=current_bar,
                length_bars=length_bars,
                context=context,
                previous_sections=sections,
            )

            sections.append(section)
            current_bar = section.end_bar + 1

            # Update context with this section's material
            context = self._update_context(context, section)

        # Stitch sections together
        return self._stitch_sections(
            sections,
            context,
            default_key,
            default_tempo,
            default_time_signature,
        )

    def _generate_section(
        self,
        prompt: str,
        section_def: dict,
        start_bar: int,
        length_bars: int,
        context: dict,
        previous_sections: list[AISection],
    ) -> AISection:
        """Generate a single section.

        Args:
            prompt: Overall composition description
            section_def: Section definition dict
            start_bar: Starting bar number
            length_bars: Length in bars
            context: Musical context
            previous_sections: Previously generated sections

        Returns:
            AISection
        """
        section_name = section_def.get("name", f"Section_{start_bar}")

        # If we have a client, generate notes
        if self.client:
            self._build_section_prompt(
                prompt=prompt,
                section_name=section_name,
                start_bar=start_bar,
                length_bars=length_bars,
                context=context,
                previous_sections=previous_sections,
            )

            # This would use the AI client to generate the section
            # For now, return an empty section as a placeholder
            return AISection(
                name=section_name,
                start_bar=start_bar,
                end_bar=start_bar + length_bars - 1,
                parts={}
            )
        else:
            # Return empty section without AI generation
            return AISection(
                name=section_name,
                start_bar=start_bar,
                end_bar=start_bar + length_bars - 1,
                parts={}
            )

    def _build_section_prompt(
        self,
        prompt: str,
        section_name: str,
        start_bar: int,
        length_bars: int,
        context: dict,
        previous_sections: list[AISection],
    ) -> str:
        """Build prompt for section generation.

        Args:
            prompt: Overall composition description
            section_name: Name of this section
            start_bar: Starting bar
            length_bars: Length in bars
            context: Musical context
            previous_sections: Previously generated sections

        Returns:
            Prompt string for this section
        """
        # Get themes from previous sections
        themes = self._extract_themes(previous_sections)

        return f"""Generate section "{section_name}" (bars {start_bar}-{start_bar + length_bars - 1}) for:

{prompt}

CONTEXT:
- Key: {context.get('key', {'tonic': 'C', 'mode': 'major'})}
- Tempo: {context.get('tempo', 120)} BPM
- Previous themes: {themes}

REQUIREMENTS:
- Generate exactly {length_bars} bars ({length_bars * 4} quarter notes at 4/4)
- If this is a repeat of a previous section, vary the material (don't copy exactly)
- Include a transition if not the final section
- Return ONLY JSON for this section's notes
"""

    def _extract_themes(self, sections: list[AISection]) -> str:
        """Extract theme summaries from previous sections.

        Args:
            sections: Previous sections

        Returns:
            String description of themes
        """
        if not sections:
            return "none (first section)"

        themes = []
        for section in sections:
            themes.append(f"{section.name}: {section.mood or 'no mood specified'}")

        return ", ".join(themes)

    def _update_context(self, context: dict, section: AISection) -> dict:
        """Update context with material from this section.

        Args:
            context: Current context
            section: Newly generated section

        Returns:
            Updated context
        """
        new_context = context.copy()

        # Update with section-specific attributes
        if section.key:
            new_context["key"] = section.key
        if section.tempo:
            new_context["tempo"] = section.tempo

        return new_context

    def _stitch_sections(
        self,
        sections: list[AISection],
        context: dict,
        default_key: KeySignature,
        default_tempo: int,
        default_time_signature: TimeSignature,
    ) -> AIComposition:
        """Combine sections into full composition.

        Args:
            sections: All sections
            context: Final context
            default_key: Default key signature
            default_tempo: Default tempo
            default_time_signature: Default time signature

        Returns:
            Complete AIComposition
        """
        # Collect all parts across sections
        all_parts: dict[str, list[AINote]] = {}

        for section in sections:
            # Calculate bar offset in quarter notes (assuming 4/4)
            bar_offset = (section.start_bar - 1) * 4

            for part_name, notes in section.parts.items():
                if part_name not in all_parts:
                    all_parts[part_name] = []

                # Adjust note times
                for note in notes:
                    if isinstance(note, dict):
                        note = AINote(**note)

                    adjusted = note.model_copy()
                    if adjusted.start_time is not None:
                        adjusted.start_time += bar_offset
                    else:
                        adjusted.start_time = bar_offset
                    all_parts[part_name].append(adjusted)

        # Create AIPart objects
        parts = [
            AIPart(
                name=name,
                midi_program=idx,  # Default program
                midi_channel=idx % 16,
                role="melody" if idx == 0 else "harmony",
                notes=notes
            )
            for idx, (name, notes) in enumerate(all_parts.items())
        ]

        # Build title
        title = context.get("title", f"Generated Composition ({len(sections)} sections)")

        return AIComposition(
            title=title,
            tempo=context.get("tempo", default_tempo),
            time_signature=default_time_signature,
            key=context.get("key", default_key),
            parts=parts,
        )


def generate_sectional(
    prompt: str,
    structure: list[dict],
    context: dict | None = None,
    client: Any | None = None,
) -> AIComposition:
    """Convenience function to generate a sectional composition.

    Args:
        prompt: Overall composition description
        structure: Section definitions
        context: Optional musical context
        client: Optional AI client

    Returns:
        Complete AIComposition

    Example:
        structure = [
            {"name": "A", "bars": 16},
            {"name": "A", "bars": 16},  # Repeat with variation
            {"name": "B", "bars": 16},  # Bridge
            {"name": "A", "bars": 16},  # Return
        ]
        comp = generate_sectional("A nostalgic piano piece", structure)
    """
    composer = SectionalComposer(client=client)
    return composer.generate_composition(prompt, structure, context)
