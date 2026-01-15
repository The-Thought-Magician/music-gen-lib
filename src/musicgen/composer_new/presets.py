"""Prompt presets for common composition types."""


PRESETS: dict[str, str] = {
    "classical_piano": "A classical piano piece with expressive melodies and rich harmonies. Include rubato and dynamic contrast.",
    "jazz_trio": "A jazz piano trio piece with walking bass and drums. Include swing rhythm, ii-V-I progressions, and improvisational sections.",
    "epic_orchestral": "An epic orchestral composition with full orchestra. Building intensity, powerful brass, soaring strings, and dramatic percussion.",
    "ambient_pad": "An ambient electronic piece with evolving synth pads, slow harmonic changes, and ethereal textures.",
    "folk_acoustic": "A folk-style acoustic guitar piece with simple melodies, major key tonality, and gentle rhythms.",
    "blues": "A 12-bar blues composition with guitar, bass, and drums. Include blues scale melodies and call-and-response patterns.",
    "minimalist": "A minimalist piece with repetitive patterns, gradual changes, and sparse textures inspired by Steve Reich or Philip Glass.",
    "romantic_string_quartet": "A romantic string quartet with expressive melodies, rich harmonies, and intimate dialogue between instruments.",
}


def get_preset(name: str) -> str:
    """Get a prompt preset by name.

    Args:
        name: Preset name

    Returns:
        Preset prompt string

    Raises:
        KeyError: If preset not found
    """
    return PRESETS[name]


def list_presets() -> list[str]:
    """List available preset names.

    Returns:
        List of preset names
    """
    return list(PRESETS.keys())


# Style modifiers that can be appended to prompts
MODIFIERS = {
    "faster": "Increase the tempo and use shorter note durations.",
    "slower": "Decrease the tempo and use longer, sustained notes.",
    "more_dynamics": "Add more dynamic contrast with wider velocity ranges.",
    "simpler": "Use simpler melodies with less motion and more repetition.",
    "more_complex": "Add more melodic and rhythmic complexity with varied patterns.",
    "darker": "Use minor key, lower register instruments, and more dissonance.",
    "brighter": "Use major key, higher register instruments, and consonant harmonies.",
}


def apply_modifier(prompt: str, modifier: str) -> str:
    """Apply a style modifier to a prompt.

    Args:
        prompt: Original prompt
        modifier: Modifier name

    Returns:
        Modified prompt
    """
    if modifier in MODIFIERS:
        return f"{prompt} {MODIFIERS[modifier]}"
    return prompt
