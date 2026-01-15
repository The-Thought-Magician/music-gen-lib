"""MusicXML file writer.

This module provides functionality for writing musical scores to MusicXML files.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from xml.dom import minidom

from musicgen.core.note import Note, Rest


class MusicXMLWriter:
    """Writes musical scores to MusicXML files."""

    # Duration mappings
    DURATION_TO_TYPE = {
        4.0: "whole",
        3.0: "half",
        2.0: "half",
        1.5: "quarter",
        1.0: "quarter",
        0.75: "eighth",
        0.5: "eighth",
        0.25: "16th",
    }

    @staticmethod
    def write(score: Score, filepath: str) -> str:
        """Write a score to a MusicXML file.

        Args:
            score: The score to write
            filepath: Path to output file

        Returns:
            Path to the written file
        """
        writer = MusicXMLWriter()
        xml_data = writer._generate_musicxml(score)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_data)

        return filepath

    def _generate_musicxml(self, score: Score) -> str:
        """Generate MusicXML from a score.

        Args:
            score: The score

        Returns:
            MusicXML as string
        """
        # Create root element
        root = ET.Element("score-partwise")
        root.set("version", "3.1")

        # Add work/title
        if score.title:
            work = ET.SubElement(root, "work")
            work_title = ET.SubElement(work, "work-title")
            work_title.text = score.title

        # Identification
        identification = ET.SubElement(root, "identification")
        if score.composer:
            creator = ET.SubElement(identification, "creator")
            creator.set("type", "composer")
            creator.text = score.composer

        # Part list
        part_list = ET.SubElement(root, "part-list")
        for i, part in enumerate(score.parts):
            score_part = ET.SubElement(part_list, "score-part")
            score_part.set("id", f"P{i+1}")
            part_name = ET.SubElement(score_part, "part-name")
            part_name.text = part.name or f"Part {i+1}"

        # Parts
        for i, part in enumerate(score.parts):
            part_elem = ET.SubElement(root, "part")
            part_elem.set("id", f"P{i+1}")

            # Create measures
            self._add_measures(part_elem, part)

        # Pretty print
        rough_string = ET.tostring(root, encoding="unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def _add_measures(self, part_elem: ET.Element, part: Part) -> None:
        """Add measures to a part.

        Args:
            part_elem: The part XML element
            part: The part data
        """

        # Simple measure division (4/4 time, assumed)
        beats_per_measure = 4
        current_beats = 0
        measure_num = 1

        # Create first measure
        measure = ET.SubElement(part_elem, "measure")
        measure.set("number", str(measure_num))

        # Add attributes to first measure
        attributes = ET.SubElement(measure, "attributes")
        divisions = ET.SubElement(attributes, "divisions")
        divisions.text = "4"  # Quarter note = 4 divisions

        time = ET.SubElement(attributes, "time")
        beats = ET.SubElement(time, "beats")
        beats.text = "4"
        beat_type = ET.SubElement(time, "beat-type")
        beat_type.text = "4"

        clef = ET.SubElement(attributes, "clef")
        sign = ET.SubElement(clef, "sign")
        sign.text = "G"
        line = ET.SubElement(clef, "line")
        line.text = "2"

        # Add notes
        for note_obj in part.notes:
            # Check if we need a new measure
            if current_beats >= beats_per_measure:
                measure_num += 1
                measure = ET.SubElement(part_elem, "measure")
                measure.set("number", str(measure_num))
                current_beats = 0

            # Add note
            if isinstance(note_obj, Note):
                self._add_note(measure, note_obj)
                current_beats += note_obj.duration
            else:
                # Rest
                self._add_rest(measure, note_obj)
                current_beats += note_obj.duration

    def _add_note(self, measure: ET.Element, note: Note) -> None:
        """Add a note to a measure.

        Args:
            measure: The measure XML element
            note: The note to add
        """
        note_elem = ET.SubElement(measure, "note")

        # Pitch
        pitch = ET.SubElement(note_elem, "pitch")
        step = ET.SubElement(pitch, "step")
        step.text = note.name

        octave = ET.SubElement(pitch, "octave")
        octave.text = str(note.octave)

        if note.accidental:
            accidental = ET.SubElement(pitch, "accidental")
            if note.accidental == "#":
                accidental.text = "sharp"
            elif note.accidental == "b":
                accidental.text = "flat"
            elif note.accidental == "x":
                accidental.text = "sharp-sharp"
            elif note.accidental == "bb":
                accidental.text = "flat-flat"

        # Duration
        duration = ET.SubElement(note_elem, "duration")
        duration.text = str(int(note.duration * 4))

        # Type
        note_type = ET.SubElement(note_elem, "type")
        note_type.text = self.DURATION_TO_TYPE.get(note.duration, "quarter")

        # Velocity/dynamic
        if note.velocity >= 110:
            dynamic = ET.SubElement(note_elem, "dynamic")
            dynamic.text = "ff"
        elif note.velocity >= 90:
            dynamic = ET.SubElement(note_elem, "dynamic")
            dynamic.text = "f"
        elif note.velocity >= 70:
            dynamic = ET.SubElement(note_elem, "dynamic")
            dynamic.text = "mf"
        elif note.velocity >= 50:
            dynamic = ET.SubElement(note_elem, "dynamic")
            dynamic.text = "mp"
        else:
            dynamic = ET.SubElement(note_elem, "dynamic")
            dynamic.text = "p"

    def _add_rest(self, measure: ET.Element, rest: Rest) -> None:
        """Add a rest to a measure.

        Args:
            measure: The measure XML element
            rest: The rest to add
        """
        note_elem = ET.SubElement(measure, "note")
        ET.SubElement(note_elem, "rest")

        duration = ET.SubElement(note_elem, "duration")
        duration.text = str(int(rest.duration * 4))

        note_type = ET.SubElement(note_elem, "type")
        note_type.text = self.DURATION_TO_TYPE.get(rest.duration, "quarter")
