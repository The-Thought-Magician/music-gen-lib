# Implementation Prompt: Step 11 - Sheet Music Generation (LilyPond)

## Overview

This step implements the LilyPond sheet music generation module for the music generation library. LilyPond is a high-quality music engraving system that produces publication-quality sheet music. This implementation uses Abjad, a Python API for LilyPond, to convert compositions to beautifully formatted PDF sheet music.

**Step Objective**: Generate publication-quality sheet music using LilyPond via Abjad.

**Dependencies**:
- Step 1: Core data structures (Note, Chord, Rest, duration/dynamic constants)
- Step 2: Scales and Keys (for key signature handling)
- Step 3: Chord Progression Engine (for harmonic context)
- Step 5: Melody Generation Engine (for melody representation)
- Step 6: Orchestration Module (for instrument definitions)

## Reading Context

Before implementing, read these files to understand the project structure and existing code:

1. `/home/chiranjeet/projects-cc/projects/music-gen-lib/docs/plan.md` - Overall implementation plan (Step 11 section)
2. `/home/chiranjeet/projects-cc/projects/music-gen-lib/docs/research.md` - Technical research, especially the Abjad section
3. `/home/chiranjeet/projects-cc/projects/music-gen-lib/claude.md` - Project context and conventions
4. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/core/__init__.py` - Core module exports
5. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/core/note.py` - Note class definition
6. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/orchestration/instruments.py` - Instrument definitions
7. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/io/__init__.py` - IO module structure

## System Dependencies

LilyPond must be installed on the system to generate PDF files:

```bash
# Ubuntu/Debian
sudo apt install lilypond

# macOS
brew install lilypond

# Windows: Download installer from https://lilypond.org/download.html
```

Verify installation:
```bash
lilypond --version
```

## Implementation Tasks

### Task 1: Create the LilyPond Writer Module Structure

Create the LilyPond writer package:

```
src/musicgen/io/
    lilypond_writer.py    # Main LilyPondWriter class
    lilypond_templates.py # Style templates and layout configurations
```

Update `src/musicgen/io/__init__.py` to include:
```python
from .lilypond_writer import LilyPondWriter, LilyPondConfig
```

### Task 2: Implement LilyPondConfig Class

Create `src/musicgen/io/lilypond_writer.py` with configuration dataclass:

```python
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
from enum import Enum
from pathlib import Path

class StaffSize(Enum):
    """LilyPond staff size presets."""
    TINY = 9
    SMALL = 11
    NORMAL = 20
    LARGE = 23
    HUGE = 26

class PageFormat(Enum):
    """Standard page formats."""
    A4 = "a4"
    LETTER = "letter"
    LEGAL = "legal"

@dataclass
class LilyPondConfig:
    """
    Configuration for LilyPond output.

    Attributes:
        title: Title of the composition
        composer: Composer name
        arranger: Arranger name (optional)
        subtitle: Subtitle (optional)
        copyright: Copyright notice (optional)
        tagline: Tagline at bottom of page (empty to disable)
        page_format: Page size (a4, letter, legal)
        staff_size: Size of the staff
        paper_margin: Margin around the page in mm
        max_systems_per_page: Maximum number of systems per page
        min_systems_per_page: Minimum number of systems per page
        system_spacing: Spacing between systems
        staff_spacing: Spacing between staves
        include_dynamics: Show dynamic markings
        include_articulations: Show articulation marks
        include_fingerings: Show fingerings (if available)
        include_tempos: Show tempo markings
        include_bar_numbers: Show bar numbers
        bar_number_interval: Show bar numbers every N bars
        indent_first_system: Indent first system for instrument names
        smart_beam: Use smart beaming (automatic)
        strict_note_spacing: Use strict note spacing
        remove_empty_staves: Hide empty staves (score only)
        use_short_staff_names: Use short instrument names on subsequent systems
        proportional_notation: Use proportional spacing for scores
    """
    title: str = "Composition"
    composer: str = "Unknown"
    arranger: Optional[str] = None
    subtitle: Optional[str] = None
    copyright: Optional[str] = None
    tagline: str = ""
    page_format: PageFormat = PageFormat.A4
    staff_size: StaffSize = StaffSize.NORMAL
    paper_margin: Tuple[float, float, float, float] = (15, 15, 15, 15)  # (left, right, top, bottom) in mm
    max_systems_per_page: int = 8
    min_systems_per_page: int = 4
    system_spacing: float = 12.0
    staff_spacing: float = 10.0
    include_dynamics: bool = True
    include_articulations: bool = True
    include_fingerings: bool = False
    include_tempos: bool = True
    include_bar_numbers: bool = True
    bar_number_interval: int = 5
    indent_first_system: float = 20.0
    smart_beam: bool = True
    strict_note_spacing: bool = False
    remove_empty_staves: bool = True
    use_short_staff_names: bool = True
    proportional_notation: bool = False

    @classmethod
    def for_score(cls) -> 'LilyPondConfig':
        """Create config optimized for full score."""
        return cls(
            staff_size=StaffSize.SMALL,
            indent_first_system=25.0,
            remove_empty_staves=True,
            use_short_staff_names=True,
        )

    @classmethod
    def for_part(cls) -> 'LilyPondConfig':
        """Create config optimized for individual part."""
        return cls(
            staff_size=StaffSize.NORMAL,
            indent_first_system=15.0,
            remove_empty_staves=False,
            use_short_staff_names=False,
        )

    @classmethod
    def for_lead_sheet(cls) -> 'LilyPondConfig':
        """Create config optimized for lead sheet."""
        return cls(
            staff_size=StaffSize.NORMAL,
            remove_empty_staves=False,
            include_bar_numbers=True,
            bar_number_interval=1,
        )
```

### Task 3: Implement Note/Rest Conversion Functions

Add conversion functions to transform library Note/Rest objects to Abjad objects:

```python
from musicgen.core import Note, Rest, Chord, QUARTER, HALF, WHOLE, EIGHTH, SIXTEENTH
import abjad

def duration_to_abjad(duration: float) -> abjad.Duration:
    """
    Convert library duration to Abjad Duration.

    Args:
        duration: Duration in quarter notes

    Returns:
        abjad.Duration object

    Raises:
        ValueError: If duration cannot be represented as standard note value
    """
    # Map duration to LilyPond duration
    duration_mapping = {
        4.0: (1, 1),      # Whole note
        3.0: (1, 1),      # Dotted half - will add dot separately
        2.0: (1, 2),      # Half note
        1.5: (1, 2),      # Dotted quarter
        1.0: (1, 4),      # Quarter note
        0.75: (1, 4),     # Dotted eighth
        0.5: (1, 8),      # Eighth note
        0.375: (1, 8),    # Dotted sixteenth
        0.25: (1, 16),    # Sixteenth note
        0.125: (1, 32),   # Thirty-second note
    }

    # Find the base duration
    base_duration = duration
    dots = 0

    # Check for dotted values
    if duration in [3.0, 1.5, 0.75, 0.375]:
        dots = 1
        base_duration = duration / 1.5
    elif duration == 0.5625:  # Double dotted quarter
        dots = 2
        base_duration = 0.25

    # Convert to Abjad duration
    if base_duration in duration_mapping:
        numerator, denominator = duration_mapping[base_duration]
        abjad_duration = abjad.Duration((numerator, denominator))
        for _ in range(dots):
            abjad_duration = abjad.Duration(abjad_duration, dot=True)
        return abjad_duration

    # Fallback: calculate from quarter notes
    denominator = int(round(4 / duration))
    if denominator > 0:
        return abjad.Duration((1, denominator))

    raise ValueError(f"Cannot convert duration {duration} to Abjad duration")

def note_to_abjad(note: Note) -> abjad.Note:
    """
    Convert library Note to Abjad Note.

    Args:
        note: Library Note object

    Returns:
        abjad.Note with pitch, duration, and articulations
    """
    # Convert pitch to Abjad format
    # Abjad uses lowercase letters with octave ticks (c' = C4, c'' = C5)
    note_name = note.name.lower()

    # Calculate octave ticks
    # In Abjad: c = C3, c' = C4, c'' = C5, etc.
    octave_offset = note.octave - 4
    if octave_offset >= 0:
        octave_marks = "'" * octave_offset
    else:
        octave_marks = "," * abs(octave_offset)

    pitch = f"{note_name}{octave_marks}"

    # Handle accidentals
    if note.accidental == "#":
        pitch = f"{note_name}s{octave_marks}"
    elif note.accidental == "b":
        pitch = f"{note_name}f{octave_marks}"
    elif note.accidental == "x":
        pitch = f"{note_name}ss{octave_marks}"
    elif note.accidental == "bb":
        pitch = f"{note_name}ff{octave_marks}"

    # Create Abjad note
    abjad_note = abjad.Note(pitch)
    abjad_note.written_duration = duration_to_abjad(note.duration)

    # Add articulations
    if note.articulation == ".":
        abjad.attach(abjad.Articulation('staccato'), abjad_note)
    elif note.articulation == ">":
        abjad.attach(abjad.Articulation('accent'), abjad_note)
    elif note.articulation == "-":
        abjad.attach(abjad.Articulation('tenuto'), abjad_note)
    elif note.articulation == "^":
        abjad.attach(abjad.Articulation('marcato'), abjad_note)

    # Add tie if applicable
    if note.tied:
        abjad.attach(abjad.Tie(), abjad_note)

    return abjad_note

def rest_to_abjad(rest: Rest) -> abjad.Rest:
    """
    Convert library Rest to Abjad Rest.

    Args:
        rest: Library Rest object

    Returns:
        abjad.Rest with duration
    """
    abjad_rest = abjad.Rest()
    abjad_rest.written_duration = duration_to_abjad(rest.duration)
    return abjad_rest

def chord_to_abjad(chord: Chord) -> abjad.Chord:
    """
    Convert library Chord to Abjad Chord.

    Args:
        chord: Library Chord object

    Returns:
        abjad.Chord with notes, duration, and articulations
    """
    # Convert chord notes to Abjad pitch format
    pitches = []
    for note in chord.notes:
        note_name = note.name.lower()
        octave_offset = note.octave - 4
        if octave_offset >= 0:
            octave_marks = "'" * octave_offset
        else:
            octave_marks = "," * abs(octave_offset)
        pitch = f"{note_name}{octave_marks}"
        pitches.append(pitch)

    # Create Abjad chord (space-separated pitches)
    abjad_chord = abjad.Chord("< " + " ".join(pitches) + " >")
    abjad_chord.written_duration = duration_to_abjad(chord.duration)

    return abjad_chord

def dynamic_to_abjad(dynamic: str, velocity: int) -> abjad.Dynamic:
    """
    Convert velocity or dynamic marking to Abjad Dynamic.

    Args:
        dynamic: Dynamic string (pp, p, mp, mf, f, ff) or None
        velocity: MIDI velocity (0-127)

    Returns:
        abjad.Dynamic object
    """
    if dynamic:
        dynamic_map = {
            "pp": "pp",
            "p": "p",
            "mp": "mp",
            "mf": "mf",
            "f": "f",
            "ff": "ff",
            "fp": "fp",
            "sf": "sf",
            "sfp": "sfp",
            "sfpp": "sfpp",
            "fz": "fz",
        }
        if dynamic in dynamic_map:
            return abjad.Dynamic(dynamic_map[dynamic])

    # Map velocity to dynamic
    if velocity <= 30:
        return abjad.Dynamic("pp")
    elif velocity <= 50:
        return abjad.Dynamic("p")
    elif velocity <= 70:
        return abjad.Dynamic("mp")
    elif velocity <= 90:
        return abjad.Dynamic("mf")
    elif velocity <= 110:
        return abjad.Dynamic("f")
    else:
        return abjad.Dynamic("ff")
```

### Task 4: Implement Clef Assignment

Add function to determine appropriate clef for instrument:

```python
def get_clef_for_instrument(instrument_name: str) -> str:
    """
    Get the appropriate clef for an instrument.

    Args:
        instrument_name: Name of the instrument

    Returns:
        Clef string for Abjad ('treble', 'bass', 'alto', 'tenor', etc.)
    """
    clef_mapping = {
        # Strings
        "violin": "treble",
        "viola": "alto",
        "cello": "bass",
        "double_bass": "bass",
        "harp": "treble",

        # Woodwinds
        "flute": "treble",
        "piccolo": "treble",
        "oboe": "treble",
        "clarinet": "treble",
        "bassoon": "bass",

        # Brass
        "trumpet": "treble",
        "french_horn": "treble",
        "trombone": "bass",
        "tuba": "bass",

        # Percussion
        "timpani": "bass",
        "glockenspiel": "treble",
        "xylophone": "treble",

        # Keyboard
        "piano": "treble_and_bass",
    }

    return clef_mapping.get(instrument_name.lower(), "treble")
```

### Task 5: Implement Main LilyPondWriter Class

Create the main writer class:

```python
@dataclass
class StaffInfo:
    """Information about a staff for notation."""
    name: str
    short_name: str
    clef: str
    instrument: Optional[object] = None  # Instrument object
    music: Optional[abjad.Voice] = None
    is_transposing: bool = False
    transposition_interval: Optional[abjad.Interval] = None

class LilyPondWriter:
    """
    Writer for converting compositions to LilyPond sheet music.

    This class handles the conversion of music data structures to
    LilyPond notation via Abjad, with support for multi-instrument
    scores, parts, and lead sheets.
    """

    def __init__(self, config: Optional[LilyPondConfig] = None):
        """
        Initialize the LilyPond writer.

        Args:
            config: Configuration for output formatting
        """
        self.config = config or LilyPondConfig()
        self._staff_infos: List[StaffInfo] = []

    def create_staff(self, name: str, short_name: str, clef: str = "treble",
                     instrument: Optional[object] = None) -> StaffInfo:
        """
        Create a staff info object.

        Args:
            name: Full instrument name
            short_name: Short name for system headers
            clef: Clef to use
            instrument: Optional instrument object

        Returns:
            StaffInfo object
        """
        return StaffInfo(
            name=name,
            short_name=short_name,
            clef=clef,
            instrument=instrument,
            music=abjad.Voice()
        )

    def add_notes(self, staff: StaffInfo, notes: List) -> None:
        """
        Add notes to a staff.

        Args:
            staff: StaffInfo object to add notes to
            notes: List of Note, Rest, or Chord objects
        """
        for item in notes:
            if isinstance(item, Note):
                staff.music.append(note_to_abjad(item))
            elif isinstance(item, Rest):
                staff.music.append(rest_to_abjad(item))
            elif isinstance(item, Chord):
                staff.music.append(chord_to_abjad(item))
            else:
                raise TypeError(f"Cannot convert {type(item)} to Abjad")

    def create_time_signature(self, numerator: int, denominator: int) -> abjad.TimeSignature:
        """
        Create a time signature.

        Args:
            numerator: Top number of time signature
            denominator: Bottom number of time signature

        Returns:
            abjad.TimeSignature
        """
        return abjad.TimeSignature((numerator, denominator))

    def create_key_signature(self, tonic: str, mode: str = "major") -> abjad.KeySignature:
        """
        Create a key signature.

        Args:
            tonic: Root note (e.g., "C", "F#")
            mode: "major" or "minor"

        Returns:
            abjad.KeySignature
        """
        # Calculate sharps/flats
        circle_of_fifths = ["C", "G", "D", "A", "E", "B", "F#", "C#",
                           "G#", "D#", "A#", "F"]
        circle_of_flats = ["C", "F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"]

        sharps = 0
        if mode == "major":
            if tonic in circle_of_fifths:
                sharps = circle_of_fifths.index(tonic)
            elif tonic in circle_of_flats:
                sharps = -circle_of_flats.index(tonic)
        elif mode == "minor":
            # Relative minor
            if tonic in circle_of_fifths:
                idx = circle_of_fifths.index(tonic)
                sharps = (idx - 3) % 15 - 7
            elif tonic in circle_of_flats:
                idx = circle_of_flats.index(tonic)
                sharps = (idx - 3) % 15 - 7

        return abjad.KeySignature(sharps)

    def create_tempo(self, bpm: int, beat_unit: str = "4") -> abjad.MetronomeMark:
        """
        Create a tempo marking.

        Args:
            bpm: Beats per minute
            beat_unit: Note value for beat ("4" for quarter, "8" for eighth)

        Returns:
            abjad.MetronomeMark
        """
        duration = abjad.Duration((1, int(beat_unit)))
        return abjad.MetronomeMark((duration, bpm))

    def create_staff_group(self, staves: List[StaffInfo],
                          group_name: str = "",
                          system_start: str = "brace") -> abjad.StaffGroup:
        """
        Create a group of staves (like a piano grand staff or instrument family).

        Args:
            staves: List of StaffInfo objects
            group_name: Optional name for the group
            system_start: Type of bracket ("brace", "bracket", "line", "square")

        Returns:
            abjad.StaffGroup
        """
        abjad_staves = []
        for staff_info in staves:
            staff = abjad.Staff([staff_info.music] if staff_info.music else [])
            staff.instrument_name = staff_info.name
            staff.short_instrument_name = staff_info.short_name

            # Add clef
            clef = abjad.Clef(staff_info.clef)
            abjad.attach(clef, staff[0] if staff else abjad.Note("c4"))

            abjad_staves.append(staff)

        # Create staff group
        if system_start == "brace":
            symbol = abjad.StartBracket()
        elif system_start == "bracket":
            symbol = abjad.StartBracket()
        elif system_start == "square":
            symbol = abjad.StartBracket()
        else:
            symbol = abjad.StartBracket()

        group = abjad.StaffGroup(abjad_staves)
        if group_name:
            group.label = group_name

        return group

    def build_score(self, staves: List[StaffInfo],
                   time_signature: Optional[Tuple[int, int]] = None,
                   key_signature: Optional[Tuple[str, str]] = None,
                   tempo: Optional[Tuple[int, str]] = None) -> abjad.Score:
        """
        Build a complete Abjad Score from staves.

        Args:
            staves: List of StaffInfo objects
            time_signature: Optional (numerator, denominator)
            key_signature: Optional (tonic, mode)
            tempo: Optional (bpm, beat_unit)

        Returns:
            abjad.Score ready for rendering
        """
        # Create music blocks for each staff
        abjad_staves = []
        for i, staff_info in enumerate(staves):
            if staff_info.music:
                voice = staff_info.music
                staff = abjad.Staff([voice])
            else:
                staff = abjad.Staff()

            # Add instrument names
            staff.instrument_name = staff_info.name
            staff.short_instrument_name = staff_info.short_name

            # Add clef
            if len(staff) > 0:
                clef = abjad.Clef(staff_info.clef)
                abjad.attach(clef, staff[0])

                # Add time signature to first staff
                if i == 0 and time_signature:
                    ts = self.create_time_signature(*time_signature)
                    abjad.attach(ts, staff[0])

                # Add key signature to first staff
                if i == 0 and key_signature:
                    ks = self.create_key_signature(*key_signature)
                    abjad.attach(ks, staff[0])

                # Add tempo to first staff
                if i == 0 and tempo:
                    tm = self.create_tempo(*tempo)
                    abjad.attach(tm, staff[0])

            abjad_staves.append(staff)

        # Create score
        score = abjad.Score(abjad_staves)
        return score

    def make_lilypond_file(self, score: abjad.Score) -> abjad.LilyPondFile:
        """
        Wrap an Abjad Score in a LilyPondFile with configuration.

        Args:
            score: Abjad Score object

        Returns:
            abjad.LilyPondFile ready for output
        """
        # Build header block
        header = abjad.Block("header")
        header.title = self.config.title
        header.composer = self.config.composer
        if self.config.arranger:
            header.arranger = self.config.arranger
        if self.config.subtitle:
            header.subtitle = self.config.subtitle
        if self.config.copyright:
            header.copyright = self.config.copyright
        header.tagline = self.config.tagline

        # Build paper block
        paper = abjad.Block("paper")
        paper.paper_size = self.config.page_format.value
        paper.top_margin = self.config.paper_margin[2]
        paper.bottom_margin = self.config.paper_margin[3]
        paper.left_margin = self.config.paper_margin[0]
        paper.right_margin = self.config.paper_margin[1]
        paper.system_system_spacing = abjad.SpacingVector(
            0, self.config.system_spacing, 0
        )
        paper.staff_staff_spacing = abjad.SpacingVector(
            0, self.config.staff_spacing, 0
        )
        paper.max_systems_per_page = self.config.max_systems_per_page
        paper.min_systems_per_page = self.config.min_systems_per_page
        paper.indent = self.config.indent_first_system
        paper.short_indent = 5

        # Build layout block
        layout = abjad.Block("layout")
        layout.context.score_accidental_engraver = abjad.Scheme(
            'Accidental_engraver'
        )

        # Create LilyPond file
        lilypond_file = abjad.LilyPondFile(
            items=[
                '\\version "2.24.0"',
                header,
                paper,
                layout,
                score,
            ],
        )

        return lilypond_file

    def write(self, score: abjad.Score,
              output_ly: Optional[str] = None,
              output_pdf: Optional[str] = None) -> Tuple[str, str]:
        """
        Write score to LilyPond and optionally render to PDF.

        Args:
            score: Abjad Score object
            output_ly: Path for .ly file (optional)
            output_pdf: Path for .pdf file (optional)

        Returns:
            Tuple of (ly_path, pdf_path)
        """
        # Create LilyPond file
        lilypond_file = self.make_lilypond_file(score)

        # Determine file paths
        if output_ly is None and output_pdf is None:
            base_name = self._sanitize_filename(self.config.title)
            output_ly = f"{base_name}.ly"
            output_pdf = f"{base_name}.pdf"
        elif output_ly is None:
            output_ly = output_pdf.replace(".pdf", ".ly")
        elif output_pdf is None:
            output_pdf = output_ly.replace(".ly", ".pdf")

        # Write .ly file
        ly_path = Path(output_ly)
        with open(ly_path, "w") as f:
            f.write(abjad.lilypond(score))

        # Render PDF if requested
        pdf_path = None
        if output_pdf:
            pdf_path = self.render_pdf(str(ly_path), output_pdf)

        return str(ly_path), str(pdf_path) if pdf_path else None

    def render_pdf(self, ly_path: str, output_path: Optional[str] = None) -> str:
        """
        Render LilyPond file to PDF.

        Args:
            ly_path: Path to .ly file
            output_path: Optional output path (default: same as ly_path with .pdf)

        Returns:
            Path to rendered PDF

        Raises:
            RuntimeError: If LilyPond is not installed or rendering fails
        """
        import subprocess
        import os

        # Check LilyPond installation
        try:
            result = subprocess.run(
                ["lilypond", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(
                "LilyPond is not installed. Please install it with:\n"
                "  Ubuntu/Debian: sudo apt install lilypond\n"
                "  macOS: brew install lilypond\n"
                "  Windows: Download from https://lilypond.org/download.html"
            ) from e

        # Determine output path
        if output_path is None:
            output_path = ly_path.replace(".ly", ".pdf")

        # Run LilyPond
        try:
            result = subprocess.run(
                ["lilypond", "-o", os.path.dirname(output_path) or ".", ly_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=60
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"LilyPond rendering timed out for {ly_path}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"LilyPond rendering failed:\n{e.stderr}"
            ) from e

        # Verify PDF was created
        pdf_path = output_path
        if not Path(pdf_path).exists():
            # LilyPond might have used the basename from the .ly file
            base_name = Path(ly_path).stem
            alt_path = Path(ly_path).parent / f"{base_name}.pdf"
            if alt_path.exists():
                pdf_path = str(alt_path)
            else:
                raise RuntimeError(f"PDF output not found after rendering {ly_path}")

        return pdf_path

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a string for use as filename."""
        import re
        # Remove invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '', name)
        # Replace spaces with underscores
        sanitized = sanitized.replace(' ', '_')
        # Limit length
        return sanitized[:50]

    @classmethod
    def write_score(cls, score_data: dict,
                    output_path: str,
                    config: Optional[LilyPondConfig] = None) -> Tuple[str, str]:
        """
        Convenience method to write a complete score.

        Args:
            score_data: Dictionary with score information:
                - title: Composition title
                - composer: Composer name
                - parts: List of part dictionaries:
                    - name: Instrument name
                    - short_name: Short name
                    - clef: Clef to use
                    - notes: List of Note/Rest/Chord objects
                - time_signature: (numerator, denominator)
                - key_signature: (tonic, mode)
                - tempo: (bpm, beat_unit)
            output_path: Base path for output files
            config: Optional LilyPondConfig

        Returns:
            Tuple of (ly_path, pdf_path)
        """
        writer = cls(config)
        writer.config.title = score_data.get("title", "Composition")
        writer.config.composer = score_data.get("composer", "Unknown")

        # Create staves
        staves = []
        for part in score_data.get("parts", []):
            staff_info = writer.create_staff(
                name=part.get("name", "Instrument"),
                short_name=part.get("short_name", part.get("name", "Inst")[:3]),
                clef=part.get("clef", "treble")
            )
            writer.add_notes(staff_info, part.get("notes", []))
            staves.append(staff_info)

        # Build score
        score = writer.build_score(
            staves=staves,
            time_signature=score_data.get("time_signature"),
            key_signature=score_data.get("key_signature"),
            tempo=score_data.get("tempo")
        )

        # Write files
        return writer.write(
            score,
            output_ly=f"{output_path}.ly",
            output_pdf=f"{output_path}.pdf"
        )
```

### Task 6: Implement LilyPond Templates

Create `src/musicgen/io/lilypond_templates.py` with style templates:

```python
"""
LilyPond style templates for different output types.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class StyleTemplate:
    """Base class for LilyPond style templates."""
    name: str
    description: str
    lilypond_preamble: str
    layout_settings: Dict[str, str]
    paper_settings: Dict[str, str]

class ClassicalTemplate(StyleTemplate):
    """Classical music notation template."""

    def __init__(self):
        super().__init__(
            name="classical",
            description="Traditional classical music notation",
            lilypond_preamble="""
\\include "english.ly"
#(set-global-staff-size 18)
""",
            layout_settings={
                "context": {
                    "Score": {
                        "autoBeaming": "##t",
                    },
                    "Staff": {
                        "autoBeaming": "##t",
                    }
                }
            },
            paper_settings={
                "print-page-number": "##t",
                "page-number-type": "number-first",
            }
        )

class LeadSheetTemplate(StyleTemplate):
    """Lead sheet with melody and chord symbols."""

    def __init__(self):
        super().__init__(
            name="lead_sheet",
            description="Jazz/pop lead sheet format",
            lilypond_preamble=r"""
\include "english.ly"
#(set-global-staff-size 20)

\layout {
  \context {
    \Score
    \consists "Chord_name_engraver"
  }
  \context {
    \ChordNames
    chordNameLowercaseMinor = ##f
    chordChanges = ##t
  }
}
""",
            layout_settings={
                "indent": "0",
            },
            paper_settings={
                "print-page-number": "##f",
            }
        )

class PercussionTemplate(StyleTemplate):
    """Percussion notation template."""

    def __init__(self):
        super().__init__(
            name="percussion",
            description="Percussion/staff notation",
            lilypond_preamble=r"""
\include "english.ly"
#(set-global-staff-size 18)

\layout {
  \context {
    \Staff
    \remove "Time_signature_engraver"
  }
  \context {
    \RhythmicStaff
    \remove "Time_signature_engraver"
  }
}
""",
            layout_settings={},
            paper_settings={}
        )

class VocalTemplate(StyleTemplate):
    """Vocal/piano score template."""

    def __init__(self):
        super().__init__(
            name="vocal",
            description="Vocal with piano accompaniment",
            lilypond_preamble=r"""
\include "english.ly"
#(set-global-staff-size 18)

\layout {
  \context {
    \Lyrics
    \override LyricHyphen.minimum-distance = #0.8
    \override LyricSpace.minimum-distance = #0.8
  }
}
""",
            layout_settings={
                "Lyrics": {
                    "LyricText": {
                        "font-size": "#1",
                    }
                }
            },
            paper_settings={}
        )

class BigBandTemplate(StyleTemplate):
    """Big band/jazz ensemble template."""

    def __init__(self):
        super().__init__(
            name="big_band",
            description="Big band arrangement format",
            lilypond_preamble=r"""
\include "english.ly"
#(set-global-staff-size 16)

\layout {
  \context {
    \Score
    proportionalNotationDuration = #(ly:make-moment 1 8)
  }
}
""",
            layout_settings={
                "proportionalNotationDuration": "#(ly:make-moment 1 8)",
            },
            paper_settings={
                "paper-size": "'(tabloid)",
            }
        )

# Template registry
TEMPLATES: Dict[str, StyleTemplate] = {
    "classical": ClassicalTemplate(),
    "lead_sheet": LeadSheetTemplate(),
    "percussion": PercussionTemplate(),
    "vocal": VocalTemplate(),
    "big_band": BigBandTemplate(),
}

def get_template(name: str) -> StyleTemplate:
    """Get a style template by name."""
    if name not in TEMPLATES:
        available = ", ".join(TEMPLATES.keys())
        raise ValueError(f"Unknown template '{name}'. Available: {available}")
    return TEMPLATES[name]

def list_templates() -> List[str]:
    """List available template names."""
    return list(TEMPLATES.keys())
```

## Test Requirements

Create `tests/test_lilypond_writer.py`:

```python
"""Tests for LilyPond writer module."""

import pytest
from pathlib import Path
from musicgen.io.lilypond_writer import (
    LilyPondWriter,
    LilyPondConfig,
    duration_to_abjad,
    note_to_abjad,
    rest_to_abjad,
    chord_to_abjad,
    dynamic_to_abjad,
    get_clef_for_instrument,
)
from musicgen.core import Note, Rest, Chord, QUARTER, EIGHTH, HALF, WHOLE, MAJOR


class TestDurationConversion:
    """Test duration to Abjad conversion."""

    def test_whole_note(self):
        result = duration_to_abjad(WHOLE)
        assert str(result) == "1"

    def test_half_note(self):
        result = duration_to_abjad(HALF)
        assert str(result) == "1/2"

    def test_quarter_note(self):
        result = duration_to_abjad(QUARTER)
        assert str(result) == "1/4"

    def test_eighth_note(self):
        result = duration_to_abjad(EIGHTH)
        assert str(result) == "1/8"

    def test_dotted_half(self):
        from musicgen.core import DOTTED_HALF
        result = duration_to_abjad(DOTTED_HALF)
        assert result.dot_count == 1

    def test_dotted_quarter(self):
        from musicgen.core import DOTTED_QUARTER
        result = duration_to_abjad(DOTTED_QUARTER)
        assert result.dot_count == 1


class TestNoteConversion:
    """Test Note to Abjad conversion."""

    def test_middle_c(self):
        note = Note("C4", QUARTER)
        result = note_to_abjad(note)
        assert hasattr(result, "written_pitch")

    def test_sharp_note(self):
        note = Note("C#4", QUARTER)
        result = note_to_abjad(note)
        assert hasattr(result, "written_pitch")

    def test_flat_note(self):
        note = Note("Bb3", QUARTER)
        result = note_to_abjad(note)
        assert hasattr(result, "written_pitch")

    def test_high_octave(self):
        note = Note("C6", QUARTER)
        result = note_to_abjad(note)
        assert hasattr(result, "written_pitch")

    def test_low_octave(self):
        note = Note("C2", QUARTER)
        result = note_to_abjad(note)
        assert hasattr(result, "written_pitch")

    def test_staccato_articulation(self):
        note = Note("C4", QUARTER, articulation=".")
        result = note_to_abjad(note)
        # Check for staccato attachment
        assert any("staccato" in str(a) for a in result.contained)

    def test_accent_articulation(self):
        note = Note("C4", QUARTER, articulation=">")
        result = note_to_abjad(note)
        assert any("accent" in str(a) for a in result.contained)

    def test_tied_note(self):
        note = Note("C4", QUARTER, tied=True)
        result = note_to_abjad(note)
        # Check for tie attachment


class TestRestConversion:
    """Test Rest to Abjad conversion."""

    def test_quarter_rest(self):
        rest = Rest(QUARTER)
        result = rest_to_abjad(rest)
        assert hasattr(result, "written_duration")

    def test_half_rest(self):
        rest = Rest(HALF)
        result = rest_to_abjad(rest)
        assert hasattr(result, "written_duration")


class TestChordConversion:
    """Test Chord to Abjad conversion."""

    def test_major_triad(self):
        chord = Chord("C", MAJOR, root_octave=4)
        result = chord_to_abjad(chord)
        assert hasattr(result, "written_pitch")

    def test_chord_duration(self):
        chord = Chord("C", MAJOR, root_octave=4, duration=HALF)
        result = chord_to_abjad(chord)
        assert hasattr(result, "written_duration")


class TestDynamicConversion:
    """Test dynamic to Abjad conversion."""

    def test_piano(self):
        result = dynamic_to_abjad("p", 50)
        assert str(result) == "p"

    def test_forte(self):
        result = dynamic_to_abjad("f", 110)
        assert str(result) == "f"

    def test_velocity_to_dynamic(self):
        result = dynamic_to_abjad(None, 30)
        assert str(result) == "pp"

    def test_velocity_mf(self):
        result = dynamic_to_abjad(None, 90)
        assert str(result) == "mf"


class TestClefAssignment:
    """Test clef assignment for instruments."""

    def test_violin_clef(self):
        assert get_clef_for_instrument("violin") == "treble"

    def test_cello_clef(self):
        assert get_clef_for_instrument("cello") == "bass"

    def test_viola_clef(self):
        assert get_clef_for_instrument("viola") == "alto"

    def test_bassoon_clef(self):
        assert get_clef_for_instrument("bassoon") == "bass"

    def test_unknown_instrument_defaults_treble(self):
        assert get_clef_for_instrument("unknown") == "treble"


class TestLilyPondConfig:
    """Test LilyPondConfig class."""

    def test_default_config(self):
        config = LilyPondConfig()
        assert config.title == "Composition"
        assert config.composer == "Unknown"
        assert config.page_format.name == "A4"

    def test_for_score_config(self):
        config = LilyPondConfig.for_score()
        assert config.staff_size.name == "SMALL"
        assert config.remove_empty_staves is True

    def test_for_part_config(self):
        config = LilyPondConfig.for_part()
        assert config.staff_size.name == "NORMAL"
        assert config.remove_empty_staves is False

    def test_for_lead_sheet_config(self):
        config = LilyPondConfig.for_lead_sheet()
        assert config.remove_empty_staves is False
        assert config.include_bar_numbers is True


class TestLilyPondWriter:
    """Test LilyPondWriter class."""

    def test_create_writer(self):
        writer = LilyPondWriter()
        assert writer.config is not None

    def test_create_writer_with_config(self):
        config = LilyPondConfig(title="Test Piece")
        writer = LilyPondWriter(config)
        assert writer.config.title == "Test Piece"

    def test_create_staff(self):
        writer = LilyPondWriter()
        staff = writer.create_staff("Violin", "Vln.", "treble")
        assert staff.name == "Violin"
        assert staff.short_name == "Vln."
        assert staff.clef == "treble"

    def test_add_notes_to_staff(self):
        writer = LilyPondWriter()
        staff = writer.create_staff("Flute", "Fl.", "treble")
        notes = [Note("C4", QUARTER), Note("D4", QUARTER), Note("E4", QUARTER)]
        writer.add_notes(staff, notes)
        assert len(staff.music) == 3

    def test_add_rests_to_staff(self):
        writer = LilyPondWriter()
        staff = writer.create_staff("Piano", "Pno", "treble")
        rests = [Rest(QUARTER), Rest(QUARTER)]
        writer.add_notes(staff, rests)
        assert len(staff.music) == 2

    def test_create_time_signature(self):
        writer = LilyPondWriter()
        ts = writer.create_time_signature(4, 4)
        assert ts is not None

    def test_create_key_signature(self):
        writer = LilyPondWriter()
        ks = writer.create_key_signature("C", "major")
        assert ks is not None

    def test_create_tempo(self):
        writer = LilyPondWriter()
        tempo = writer.create_tempo(120, "4")
        assert tempo is not None

    def test_build_score(self):
        writer = LilyPondWriter()
        staff1 = writer.create_staff("Violin", "Vln.", "treble")
        staff2 = writer.create_staff("Cello", "Vc.", "bass")
        notes = [Note("C4", QUARTER), Note("D4", QUARTER), Note("E4", QUARTER)]
        writer.add_notes(staff1, notes)
        writer.add_notes(staff2, notes)

        score = writer.build_score(
            staves=[staff1, staff2],
            time_signature=(4, 4),
            key_signature=("C", "major"),
            tempo=(120, "4")
        )
        assert score is not None

    def test_make_lilypond_file(self):
        writer = LilyPondWriter()
        staff = writer.create_staff("Flute", "Fl.", "treble")
        notes = [Note("C4", QUARTER), Note("D4", QUARTER)]
        writer.add_notes(staff, notes)

        score = writer.build_score(
            staves=[staff],
            time_signature=(4, 4),
            key_signature=("C", "major")
        )

        lilypond_file = writer.make_lilypond_file(score)
        assert lilypond_file is not None


class TestLilyPondFileOutput:
    """Test LilyPond file output (integration tests)."""

    def test_write_ly_file(self, tmp_path):
        writer = LilyPondWriter()
        writer.config.title = "Test Composition"
        writer.config.composer = "Test Composer"

        staff = writer.create_staff("Violin", "Vln.", "treble")
        notes = [
            Note("C4", QUARTER),
            Note("D4", QUARTER),
            Note("E4", QUARTER),
            Note("F4", QUARTER),
        ]
        writer.add_notes(staff, notes)

        score = writer.build_score(
            staves=[staff],
            time_signature=(4, 4),
            key_signature=("C", "major")
        )

        output_path = tmp_path / "test_output"
        ly_path, _ = writer.write(score, output_ly=str(output_path) + ".ly")

        assert Path(ly_path).exists()
        # Check file contains LilyPond content
        with open(ly_path, "r") as f:
            content = f.read()
            assert "\\version" in content or "\\header" in content

    @pytest.mark.slow
    def test_render_pdf_requires_lilypond(self, tmp_path):
        """Test PDF rendering (requires LilyPond to be installed)."""
        import subprocess

        # Check if LilyPond is available
        try:
            subprocess.run(["lilypond", "--version"],
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("LilyPond not installed")

        writer = LilyPondWriter()
        writer.config.title = "Test Composition"
        writer.config.composer = "Test Composer"

        staff = writer.create_staff("Violin", "Vln.", "treble")
        notes = [
            Note("C4", QUARTER),
            Note("D4", QUARTER),
            Note("E4", QUARTER),
            Note("G4", QUARTER),
            Note("C5", WHOLE),
        ]
        writer.add_notes(staff, notes)

        score = writer.build_score(
            staves=[staff],
            time_signature=(4, 4),
            key_signature=("C", "major")
        )

        output_path = tmp_path / "test_output"
        ly_path, pdf_path = writer.write(
            score,
            output_ly=str(output_path) + ".ly",
            output_pdf=str(output_path) + ".pdf"
        )

        assert Path(ly_path).exists()
        assert Path(pdf_path).exists()

        # Verify PDF is valid (has PDF header)
        with open(pdf_path, "rb") as f:
            header = f.read(4)
            assert header == b"%PDF"

    def test_write_score_convenience_method(self, tmp_path):
        """Test the class method convenience function."""
        score_data = {
            "title": "Test Piece",
            "composer": "Test Composer",
            "parts": [
                {
                    "name": "Violin",
                    "short_name": "Vln.",
                    "clef": "treble",
                    "notes": [
                        Note("C4", QUARTER),
                        Note("D4", QUARTER),
                        Note("E4", HALF),
                    ]
                },
                {
                    "name": "Cello",
                    "short_name": "Vc.",
                    "clef": "bass",
                    "notes": [
                        Note("C3", HALF),
                        Note("G2", HALF),
                    ]
                }
            ],
            "time_signature": (4, 4),
            "key_signature": ("C", "major"),
            "tempo": (120, "4")
        }

        output_path = tmp_path / "test_convenience"
        ly_path, _ = LilyPondWriter.write_score(
            score_data,
            output_path=str(output_path)
        )

        assert Path(ly_path).exists()


class TestFilenameSanitization:
    """Test filename sanitization."""

    def test_sanitize_simple_name(self):
        writer = LilyPondWriter()
        assert writer._sanitize_filename("Test Piece") == "Test_Piece"

    def test_sanitize_special_chars(self):
        writer = LilyPondWriter()
        result = writer._sanitize_filename('Test: "Piece" <2024>')
        assert ":" not in result
        assert '"' not in result
        assert "<" not in result
        assert ">" not in result

    def test_sanitize_long_name(self):
        writer = LilyPondWriter()
        long_name = "A" * 100
        result = writer._sanitize_filename(long_name)
        assert len(result) <= 50


class TestLilyPondTemplates:
    """Test LilyPond templates."""

    def test_get_classical_template(self):
        from musicgen.io.lilypond_templates import get_template
        template = get_template("classical")
        assert template.name == "classical"

    def test_get_lead_sheet_template(self):
        from musicgen.io.lilypond_templates import get_template
        template = get_template("lead_sheet")
        assert template.name == "lead_sheet"

    def test_invalid_template_raises_error(self):
        from musicgen.io.lilypond_templates import get_template
        with pytest.raises(ValueError):
            get_template("invalid")

    def test_list_templates(self):
        from musicgen.io.lilypond_templates import list_templates
        templates = list_templates()
        assert "classical" in templates
        assert "lead_sheet" in templates
```

## Example Usage

Create `examples/generate_pdf.py`:

```python
#!/usr/bin/env python3
"""Generate PDF sheet music using LilyPond."""

from musicgen.core import Note, Rest, Chord, QUARTER, HALF, WHOLE, EIGHTH, MAJOR
from musicgen.io.lilypond_writer import LilyPondWriter, LilyPondConfig

# Create a simple melody
melody = [
    Note("C4", QUARTER),
    Note("D4", QUARTER),
    Note("E4", QUARTER),
    Note("F4", QUARTER),
    Note("G4", HALF),
    Rest(QUARTER),
    Note("A4", QUARTER),
    Note("G4", QUARTER),
    Note("F4", QUARTER),
    Note("E4", QUARTER),
    Note("D4", HALF),
    Note("C5", WHOLE),
]

# Create accompaniment (simple chords)
accompaniment = [
    Chord("C", MAJOR, root_octave=3, duration=WHOLE),
    Chord("G", MAJOR, root_octave=3, duration=WHOLE),
    Chord("F", MAJOR, root_octave=3, duration=HALF),
    Chord("C", MAJOR, root_octave=3, duration=HALF),
]

# Create writer with configuration
config = LilyPondConfig(
    title="Simple Melody",
    composer="MusicGen Library",
    subtitle="Generated with LilyPond",
)
writer = LilyPondWriter(config)

# Create staves
melody_staff = writer.create_staff("Violin", "Vln.", "treble")
accomp_staff = writer.create_staff("Cello", "Vc.", "bass")

# Add notes
writer.add_notes(melody_staff, melody)
writer.add_notes(accomp_staff, accompaniment)

# Build score
score = writer.build_score(
    staves=[melody_staff, accomp_staff],
    time_signature=(4, 4),
    key_signature=("C", "major"),
    tempo=(100, "4")
)

# Write files
ly_path, pdf_path = writer.write(
    score,
    output_ly="simple_melody.ly",
    output_pdf="simple_melody.pdf"
)

print(f"Generated LilyPond file: {ly_path}")
print(f"Generated PDF: {pdf_path}")
```

## File Structure

Create the following files:

```
src/musicgen/io/
    lilypond_writer.py     # Main LilyPondWriter class and functions
    lilypond_templates.py  # Style templates

tests/
    test_lilypond_writer.py
```

Update `src/musicgen/io/__init__.py`:
```python
"""Input/output module for music generation library."""

from .lilypond_writer import (
    LilyPondWriter,
    LilyPondConfig,
    StaffSize,
    PageFormat,
)

__all__ = [
    "LilyPondWriter",
    "LilyPondConfig",
    "StaffSize",
    "PageFormat",
]
```

## Dependencies to Add to pyproject.toml

Add Abjad to the project dependencies:

```toml
dependencies = [
    # ... existing dependencies ...
    "abjad>=3.4",
]
```

## Validation Criteria

After implementation, verify these behaviors:

```python
# 1. Duration conversion
from musicgen.io.lilypond_writer import duration_to_abjad
assert duration_to_abjad(1.0) is not None
assert duration_to_abjad(2.0) is not None
assert duration_to_abjad(4.0) is not None

# 2. Note conversion
from musicgen.io.lilypond_writer import note_to_abjad
from musicgen.core import Note, QUARTER
note = Note("C4", QUARTER)
abjad_note = note_to_abjad(note)
assert abjad_note is not None

# 3. Staff creation
writer = LilyPondWriter()
staff = writer.create_staff("Violin", "Vln.", "treble")
assert staff.name == "Violin"
assert staff.clef == "treble"

# 4. Score building
notes = [Note("C4", QUARTER), Note("D4", QUARTER), Note("E4", QUARTER)]
writer.add_notes(staff, notes)
score = writer.build_score(
    staves=[staff],
    time_signature=(4, 4),
    key_signature=("C", "major")
)
assert score is not None

# 5. LilyPond file generation
lilypond_file = writer.make_lilypond_file(score)
assert lilypond_file is not None

# 6. File output (if LilyPond installed)
import tempfile
import os

if os.path.exists("/usr/bin/lilypond"):
    with tempfile.TemporaryDirectory() as tmpdir:
        ly_path, pdf_path = writer.write(
            score,
            output_ly=f"{tmpdir}/test.ly",
            output_pdf=f"{tmpdir}/test.pdf"
        )
        assert os.path.exists(ly_path)
        assert os.path.exists(pdf_path)
```

## Dependencies on Previous Steps

This step depends on:

1. **Step 1 (Core)**: Uses `Note`, `Rest`, `Chord` classes and duration constants
2. **Step 6 (Orchestration)**: Uses instrument definitions for clef assignment

The Note class must have:
- `name` property: Note name (C, D, E, etc.)
- `octave` property: Octave number
- `accidental` property: Accidental string ("", "#", "b", "x", "bb")
- `duration` property: Duration in quarter notes
- `articulation` property: Articulation mark (".", ">", "-", "^")
- `tied` property: Whether note is tied to next

The Rest class must have:
- `duration` property: Duration in quarter notes

The Chord class must have:
- `notes` property: List of Note objects
- `duration` property: Duration in quarter notes

## Success Criteria

Step 11 is complete when:

1. All `LilyPondWriter` class methods are implemented and tested
2. `duration_to_abjad()` correctly converts all duration values
3. `note_to_abjad()` correctly converts notes with pitch, duration, and articulations
4. `rest_to_abjad()` correctly converts rests
5. `chord_to_abjad()` correctly converts chords
6. `build_score()` creates valid Abjad Score objects
7. `make_lilypond_file()` wraps scores with proper configuration
8. `write()` generates valid .ly files
9. When LilyPond is installed, `render_pdf()` produces valid PDFs
10. All tests pass: `pytest tests/test_lilypond_writer.py`
11. Test coverage is at least 80% for the lilypond_writer module
12. The example script `examples/generate_pdf.py` runs successfully

## Notes

- Abjad uses specific pitch notation: lowercase letters with octave ticks (c' = C4, c'' = C5)
- Accidentals in Abjad: s = sharp, f = flat, ss = double sharp, ff = double flat
- Duration dots are handled separately from the base duration
- The `render_pdf()` method requires LilyPond to be installed on the system
- Tests that require LilyPond should be marked with `@pytest.mark.slow` and can be skipped
- The library generates .ly files regardless of LilyPond installation
- PDF rendering is optional; the .ly files can be manually rendered if needed

## Troubleshooting

Common issues and solutions:

1. **"LilyPond is not installed" error**:
   - Install LilyPond using your system package manager
   - Or download from https://lilypond.org/download.html

2. **PDF rendering times out**:
   - The default timeout is 60 seconds; increase for complex scores
   - Consider reducing the number of staves or notes in the score

3. **Invalid duration error**:
   - Ensure all durations are standard note values (1, 0.5, 0.25, etc.)
   - Dotted values should use the predefined constants (DOTTED_QUARTER, etc.)

4. **Clef not displaying correctly**:
   - Ensure clef strings are valid ("treble", "bass", "alto", "tenor")
   - Check that the first note/rest in the staff exists for clef attachment

## Next Steps

After completing this step, proceed to Step 12: "Mood-to-Music Configuration System" which will create the high-level interface for generating music based on mood parameters, utilizing all the export capabilities including MIDI, audio, and sheet music generation.
