"""SFZ renderer integration for V3 music generation system.

This package provides Python wrappers around sfizz-render for rendering
MIDI files to audio using SFZ format sample libraries.

Main classes:
    - SFZRenderer: Render single-instrument MIDI files
    - MultiInstrumentRenderer: Render multi-instrument compositions

Installation utilities:
    - check_sfizz_installation(): Check if dependencies are installed
    - print_installation_instructions(): Show how to install missing deps
    - print_system_status(): Show complete system status

Example usage:
    >>> from musicgen.sfz import SFZRenderer, render_midi_to_audio
    >>>
    >>> # Create renderer
    >>> renderer = SFZRenderer(libraries_root=Path("resources/sfz_libraries"))
    >>>
    >>> # Render MIDI to audio
    >>> output = renderer.render(
    ...     midi_path=Path("composition.mid"),
    ...     output_path=Path("output.wav"),
    ...     sfz_file=Path("VSL/Strings/Violin.sfz")
    ... )
    >>>
    >>> # Or use convenience function
    >>> output = render_midi_to_audio(
    ...     "composition.mid",
    ...     "output.wav",
    ...     "VSL/Strings/Violin.sfz"
    ... )

Multi-instrument example:
    >>> from musicgen.sfz import MultiInstrumentRenderer
    >>>
    >>> multi = MultiInstrumentRenderer()
    >>>
    >>> mapping = {
    ...     0: "VSL/Strings/Violin.sfz",
    ...     1: "VSL/Strings/Cello.sfz",
    ...     2: "VSL/Winds/Flute.sfz",
    ... }
    >>>
    >>> output = multi.render_composition(
    ...     midi_path=Path("orchestral.mid"),
    ...     output_path=Path("orchestral.wav"),
    ...     instrument_mapping=mapping,
    ...     render_stems=True
    ... )

Checking installation:
    >>> from musicgen.sfz import print_system_status
    >>>
    >>> print_system_status()
"""

from musicgen.sfz.installation import (
    DependencyStatus,
    check_sfizz_installation,
    check_sfz_libraries,
    get_installation_command,
    print_installation_instructions,
    print_sfz_library_status,
    print_system_status,
    verify_rendering_capability,
)
from musicgen.sfz.renderer import (
    MultiInstrumentRenderer,
    SFZNotAvailableError,
    SFZNotFoundError,
    SFZRenderer,
    SFZRendererError,
    SFZRenderError,
    render_midi_to_audio,
    render_multitrack,
)

__all__ = [
    # Renderer classes
    "SFZRenderer",
    "MultiInstrumentRenderer",
    # Exceptions
    "SFZRendererError",
    "SFZNotFoundError",
    "SFZRenderError",
    "SFZNotAvailableError",
    # Convenience functions
    "render_midi_to_audio",
    "render_multitrack",
    # Installation utilities
    "check_sfizz_installation",
    "print_installation_instructions",
    "print_system_status",
    "print_sfz_library_status",
    "check_sfz_libraries",
    "verify_rendering_capability",
    "get_installation_command",
    "DependencyStatus",
]
