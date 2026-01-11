"""LilyPond file writer.

This module provides functionality for writing musical scores to LilyPond files.
"""

from __future__ import annotations
from typing import List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile

from musicgen.core.note import Note, Rest, QUARTER


class LilyPondWriter:
    """Writes musical scores to LilyPond files."""

    # Note name mapping
    NOTE_TO_LILY = {
        "C": "c", "D": "d", "E": "e", "F": "f", "G": "g", "A": "a", "B": "b"
    }

    # Duration mapping
    DURATION_TO_LILY = {
        4.0: "1",
        3.0: "2.",
        2.0: "2",
        1.5: "4.",
        1.0: "4",
        0.75: "8.",
        0.5: "8",
        0.25: "16",
        0.125: "32",
    }

    # Dynamic mapping
    VELOCITY_TO_DYNAMIC = {
        30: "ppp", 40: "pp", 50: "p", 60: "mp",
        70: "mp", 80: "mf", 90: "mf", 100: "f", 110: "ff", 120: "fff"
    }

    @staticmethod
    def write(score: "Score", output_ly: str = "",
              output_pdf: str = "", title: str = "", composer: str = "",
              include_title: bool = True, staff_size: int = 20) -> str:
        """Write a score to a LilyPond file.

        Args:
            score: The score to write
            output_ly: Path to output .ly file
            output_pdf: Path to output .pdf file
            title: Score title
            composer: Composer name
            include_title: Whether to include title on page
            staff_size: Staff size in points

        Returns:
            Path to the written file
        """
        writer = LilyPondWriter()
        lilypond_data = writer._generate_lilypond(
            score,
            title=title,
            composer=composer,
            include_title=include_title,
            staff_size=staff_size
        )

        # Default .ly filename
        if not output_ly:
            output_ly = "output.ly"

        with open(output_ly, "w", encoding="utf-8") as f:
            f.write(lilypond_data)

        # Generate PDF if requested
        if output_pdf:
            writer._compile_to_pdf(output_ly, output_pdf)

        return output_ly

    def _generate_lilypond(self, score: "Score", title: str = "",
                           composer: str = "", include_title: bool = True,
                           staff_size: int = 20) -> str:
        """Generate LilyPond code from a score.

        Args:
            score: The score
            title: Score title
            composer: Composer name
            include_title: Whether to include title
            staff_size: Staff size

        Returns:
            LilyPond code as string
        """
        lines = []

        # Header
        lines.append("\\version \"2.24.0\"")
        lines.append("")

        # Paper block
        lines.append("\\paper {")
        if include_title and (title or composer or score.title or score.composer):
            lines.append("  tagline = ##f")
        lines.append(f"  staff-size = {staff_size}")
        lines.append("}")
        lines.append("")

        # Header block
        lines.append("\\header {")
        if title:
            lines.append(f"  title = \"{title}\"")
        elif score.title:
            lines.append(f"  title = \"{score.title}\"")
        if composer:
            lines.append(f"  composer = \"{composer}\"")
        elif score.composer:
            lines.append(f"  composer = \"{score.composer}\"")
        lines.append("}")
        lines.append("")

        # Score block
        lines.append("\\score {")
        lines.append("  <<")

        # Add parts
        for i, part in enumerate(score.parts):
            staff = self._generate_staff(part, i)
            lines.append(f"    {staff}")

        lines.append("  >>")
        lines.append("  \\layout { }")
        lines.append("  \\midi {")
        lines.append("    \\tempo 4 = 120")
        lines.append("  }")
        lines.append("}")

        return "\n".join(lines)

    def _generate_staff(self, part: "Part", index: int) -> str:
        """Generate a LilyPond staff for a part.

        Args:
            part: The part
            index: Part index

        Returns:
            LilyPond staff code
        """
        lines = []
        lines.append(f"\\new Staff {{")
        lines.append(f"  \\set Staff.instrumentName = #\"{part.name or f'Part {index+1}'}\"")
        lines.append("  {")

        # Collect notes as a string
        note_strings = []
        for note_obj in part.notes:
            note_strings.append(self._note_to_lilypond(note_obj))

        # Join notes and add to staff
        notes_text = " ".join(note_strings)
        # Wrap in a relative music expression for convenience
        lines.append(f"    \\relative c' {{")
        lines.append(f"      {notes_text}")
        lines.append("    }")

        lines.append("  }")
        lines.append("}")

        return "\n    ".join(lines)

    def _note_to_lilypond(self, note: Union[Note, Rest]) -> str:
        """Convert a note or rest to LilyPond notation.

        Args:
            note: Note or Rest

        Returns:
            LilyPond note string
        """
        if isinstance(note, Rest):
            duration = self.DURATION_TO_LILY.get(note.duration, "4")
            return f"r{duration}"

        # Get note name
        lily_note = self.NOTE_TO_LILY.get(note.name, "c")

        # Add octave marks
        octave_diff = note.octave - 4
        if octave_diff > 0:
            lily_note += "'" * octave_diff
        elif octave_diff < 0:
            lily_note += "," * abs(octave_diff)

        # Add accidental
        if note.accidental == "#":
            lily_note = lily_note[0] + "is" + lily_note[1:]
        elif note.accidental == "b":
            lily_note = lily_note[0] + "es" + lily_note[1:]
        elif note.accidental == "x":
            lily_note = lily_note[0] + "isis" + lily_note[1:]
        elif note.accidental == "bb":
            lily_note = lily_note[0] + "eses" + lily_note[1:]

        # Add duration
        duration = self.DURATION_TO_LILY.get(note.duration, "4")

        # Add dynamic
        dynamic = self.VELOCITY_TO_DYNAMIC.get(note.velocity, "")
        if dynamic:
            return f"{lily_note}{duration}\\{dynamic}"

        return f"{lily_note}{duration}"

    def _compile_to_pdf(self, ly_file: str, pdf_output: str) -> str:
        """Compile a LilyPond file to PDF.

        Args:
            ly_file: Path to .ly file
            pdf_output: Path for output PDF

        Returns:
            Path to generated PDF
        """
        try:
            subprocess.run(
                ["lilypond", "-o", pdf_output, ly_file],
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"LilyPond compilation failed: {e.stderr}")
        except FileNotFoundError:
            raise RuntimeError(
                "LilyPond not found. Please install lilypond:\n"
                "  Ubuntu/Debian: sudo apt install lilypond\n"
                "  macOS: brew install lilypond"
            )

        return pdf_output

    @staticmethod
    def is_available() -> bool:
        """Check if LilyPond is available.

        Returns:
            True if LilyPond is installed
        """
        try:
            result = subprocess.run(
                ["lilypond", "--version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
