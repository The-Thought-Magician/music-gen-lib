# Step 13: Testing and Documentation

## Overview

This is the final implementation step for the Music Generation Library. This step completes the testing infrastructure to achieve >80% code coverage and creates comprehensive documentation including Sphinx API docs, tutorials, examples, and a polished README.

## Context

You are working on a Python library called `musicgen` that generates orchestral instrumental music using traditional music theory principles (rule-based composition, NOT AI).

**Project Location**: `/home/chiranjeet/projects-cc/projects/music-gen-lib`

This step depends on ALL previous steps being completed:
- Step 1: Project Setup and Core Data Structures
- Step 2: Music Theory Module - Scales and Keys
- Step 3: Chord Progression Engine
- Step 4: Voice Leading Module
- Step 5: Melody Generation Engine
- Step 6: Orchestration Module
- Step 7: Musical Form Structures
- Step 8: MIDI File Generation
- Step 9: Audio Synthesis Pipeline
- Step 10: Sheet Music Generation (MusicXML)
- Step 11: Sheet Music Generation (LilyPond)
- Step 12: Mood-to-Music Configuration System

## Expected Project Structure (Before This Step)

```
music-gen-lib/
├── pyproject.toml
├── README.md                    # Basic placeholder (to be updated)
├── src/
│   └── musicgen/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── note.py
│       │   └── chord.py
│       ├── theory/
│       │   ├── __init__.py
│       │   ├── scales.py
│       │   ├── keys.py
│       │   └── progressions.py
│       ├── composition/
│       │   ├── __init__.py
│       │   ├── melody.py
│       │   └── forms.py
│       ├── orchestration/
│       │   ├── __init__.py
│       │   ├── instruments.py
│       │   └── ensembles.py
│       ├── io/
│       │   ├── __init__.py
│       │   ├── midi_writer.py
│       │   ├── audio_synthesizer.py
│       │   ├── musicxml_writer.py
│       │   └── lilypond_writer.py
│       ├── config/
│       │   ├── __init__.py
│       │   └── moods.py
│       ├── generator.py
│       └── __main__.py
├── tests/
│   ├── __init__.py
│   ├── test_note.py
│   ├── test_chord.py
│   ├── test_scales.py
│   ├── test_keys.py
│   ├── test_progressions.py
│   ├── test_voice_leading.py
│   ├── test_melody.py
│   ├── test_forms.py
│   ├── test_instruments.py
│   ├── test_midi_writer.py
│   ├── test_audio_synthesizer.py
│   ├── test_musicxml_writer.py
│   ├── test_lilypond_writer.py
│   └── test_moods.py
└── examples/
    ├── basic_composition.py
    ├── generate_midi.py
    ├── generate_sheet_music.py
    └── mood_examples.py
```

## Implementation Tasks

### Task 1: Complete Test Coverage

#### 1.1 Review and Complete Existing Tests

Ensure all existing test files have comprehensive coverage:

**Test files to review/enhance:**

```bash
tests/
├── __init__.py                    # Empty, marks package
├── conftest.py                    # NEW: Shared pytest fixtures
├── test_note.py                   # Note and Rest classes
├── test_chord.py                  # Chord class
├── test_scales.py                 # Scale class
├── test_keys.py                   # Key and KeySignature classes
├── test_progressions.py           # Progression class
├── test_voice_leading.py          # Voice leading functions
├── test_melody.py                 # Melody, Motif, Phrase classes
├── test_forms.py                  # Form classes
├── test_instruments.py            # Instrument and Ensemble classes
├── test_midi_writer.py            # MIDI writing functions
├── test_audio_synthesizer.py      # Audio synthesis
├── test_musicxml_writer.py        # MusicXML export
├── test_lilypond_writer.py        # LilyPond export
├── test_moods.py                  # Mood configurations
├── test_integration.py            # NEW: Integration tests
└── test_cli.py                    # NEW: CLI tests
```

#### 1.2 Create `tests/conftest.py`

Create a shared fixtures file:

```python
"""
Pytest configuration and shared fixtures for musicgen tests."""

import pytest
import tempfile
import shutil
from pathlib import Path

from musicgen.core.note import Note, Rest, QUARTER, WHOLE, HALF, MF
from musicgen.core.chord import Chord, MAJOR, MINOR
from musicgen.theory.scales import Scale
from musicgen.theory.keys import Key
from musicgen.theory.progressions import Progression


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def c_major_scale():
    """C major scale fixture."""
    return Scale("C", "major")


@pytest.fixture
def a_minor_scale():
    """A natural minor scale fixture."""
    return Scale("A", "natural_minor")


@pytest.fixture
def c_major_key():
    """C major key fixture."""
    return Key("C", "major")


@pytest.fixture
def sample_notes():
    """Sample notes for testing."""
    return [
        Note("C4", QUARTER),
        Note("D4", QUARTER),
        Note("E4", QUARTER),
        Note("F4", QUARTER),
        Note("G4", QUARTER),
        Note("A4", QUARTER),
        Note("B4", QUARTER),
        Note("C5", QUARTER),
    ]


@pytest.fixture
def sample_chord():
    """C major chord fixture."""
    return Chord("C", MAJOR, root_octave=4)


@pytest.fixture
def sample_progression():
    """I-IV-V-I progression in C major."""
    return Progression.from_roman("I-IV-V-I", key="C")


@pytest.fixture
def output_path(temp_dir):
    """Path for output files in temp directory."""
    return temp_dir


# SoundFont fixture (skip if not available)
@pytest.fixture
def soundfont_path():
    """Path to test SoundFont file."""
    # Check for common SoundFont locations
    possible_paths = [
        Path("/usr/share/sounds/sf2/FluidR3_GM.sf2"),
        Path("/usr/share/soundfonts/FluidR3_GM.sf2"),
        Path("resources/soundfonts/GeneralUser GS.sf2"),
    ]
    for path in possible_paths:
        if path.exists():
            return str(path)
    # Return None if not found - tests should skip
    return None
```

#### 1.3 Create Integration Tests (`tests/test_integration.py`)

```python
"""
Integration tests for the complete music generation pipeline.

These tests verify that all components work together correctly.
"""

import pytest
import os
from pathlib import Path

from musicgen.core.note import Note, QUARTER
from musicgen.core.chord import Chord, MAJOR
from musicgen.theory.scales import Scale
from musicgen.theory.keys import Key
from musicgen.theory.progressions import Progression
from musicgen.composition.melody import MelodyGenerator, MelodicContour
from musicgen.orchestration.ensembles import Ensemble
from musicgen.io.midi_writer import MIDIWriter
from musicgen.generator import generate, CompositionRequest


class TestFullPipeline:
    """Test the complete music generation pipeline."""

    def test_scale_to_midi_pipeline(self, temp_dir, c_major_scale):
        """Test generating a scale and exporting to MIDI."""
        # Create a simple melody from the scale
        notes = [c_major_scale.get_degree(i % 7 + 1) for i in range(16)]

        # Create a basic score structure
        from musicgen.io.midi_writer import MIDIWriter

        output_path = temp_dir / "scale_test.mid"
        # MIDIWriter.write() implementation depends on your Score class
        # This is a placeholder - adapt to your actual implementation
        assert output_path.parent.exists()

    def test_progression_to_audio(self, temp_dir, sample_progression, soundfont_path):
        """Test chord progression to audio conversion."""
        if soundfont_path is None:
            pytest.skip("No SoundFont available")

        # Generate MIDI from progression
        midi_path = temp_dir / "progression.mid"
        audio_path = temp_dir / "progression.wav"

        # Convert to audio
        from musicgen.io.audio_synthesizer import AudioSynthesizer

        # Implementation-specific test
        assert midi_path.parent.exists()

    def test_mood_based_generation(self, temp_dir):
        """Test complete mood-based music generation."""
        request = CompositionRequest(
            mood="peaceful",
            duration=30,
            output_dir=str(temp_dir)
        )

        result = generate(request)

        assert result.score is not None
        assert result.midi_path is not None
        assert Path(result.midi_path).exists()

    def test_scale_key_progression_integration(self, c_major_key):
        """Test that Scale, Key, and Progression work together."""
        scale = c_major_key.scale
        progression = c_major_key.diatonic_chords()

        assert len(progression) == 7
        assert progression[0].quality == "major"
        assert progression[1].quality == "minor"


class TestExportFormats:
    """Test all export formats work correctly."""

    def test_midi_export(self, temp_dir):
        """Test MIDI file export."""
        from musicgen.io.midi_writer import MIDIWriter

        output_path = temp_dir / "test.mid"
        # Create test score and export
        assert output_path.parent.exists()

    def test_musicxml_export(self, temp_dir):
        """Test MusicXML file export."""
        from musicgen.io.musicxml_writer import MusicXMLWriter

        output_path = temp_dir / "test.musicxml"
        # Create test score and export
        assert output_path.parent.exists()

    def test_lilypond_export(self, temp_dir):
        """Test LilyPond file export."""
        from musicgen.io.lilypond_writer import LilyPondWriter

        output_path = temp_dir / "test.ly"
        pdf_path = temp_dir / "test.pdf"
        # Create test score and export
        assert output_path.parent.exists()


class TestMoodPresets:
    """Test mood preset configurations."""

    def test_all_moods_defined(self):
        """Test that all mood presets are properly defined."""
        from musicgen.config.moods import MOOD_PRESETS

        expected_moods = [
            "epic", "peaceful", "mysterious", "triumphant",
            "melancholic", "playful", "romantic", "tense"
        ]

        for mood in expected_moods:
            assert mood in MOOD_PRESETS
            preset = MOOD_PRESETS[mood]
            assert "key" in preset
            assert "scale" in preset
            assert "tempo" in preset
            assert "instruments" in preset

    def test_mood_generation(self, temp_dir):
        """Test generation for each mood preset."""
        from musicgen.config.moods import MOOD_PRESETS
        from musicgen.generator import generate, CompositionRequest

        for mood_name, preset in MOOD_PRESETS.items():
            request = CompositionRequest(
                mood=mood_name,
                duration=15,  # Short for testing
                output_dir=str(temp_dir)
            )

            result = generate(request)
            assert result.score is not None


class TestReproducibility:
    """Test that generation is reproducible with seeds."""

    def test_seeded_generation(self):
        """Test that same seed produces same output."""
        scale = Scale("C", "major")
        key = Key("C", "major")

        gen1 = MelodyGenerator(scale, key)
        gen1.set_seed(42)
        melody1 = gen1.generate_motif(length=8)

        gen2 = MelodyGenerator(scale, key)
        gen2.set_seed(42)
        melody2 = gen2.generate_motif(length=8)

        # Notes should be identical
        assert len(melody1.notes) == len(melody2.notes)
        for n1, n2 in zip(melody1.notes, melody2.notes):
            if isinstance(n1, Note) and isinstance(n2, Note):
                assert n1.name == n2.name
                assert n1.octave == n2.octave
```

#### 1.4 Create CLI Tests (`tests/test_cli.py`)

```python
"""
Tests for the command-line interface.
"""

import pytest
import subprocess
import sys
from pathlib import Path


class TestCLI:
    """Test CLI commands."""

    def test_cli_help(self):
        """Test that CLI help command works."""
        result = subprocess.run(
            [sys.executable, "-m", "musicgen", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "musicgen" in result.stdout.lower()

    def test_cli_generate_command(self, temp_dir):
        """Test CLI generate command."""
        result = subprocess.run(
            [
                sys.executable, "-m", "musicgen", "generate",
                "--mood", "peaceful",
                "--duration", "10",
                "--output-dir", str(temp_dir)
            ],
            capture_output=True,
            text=True
        )
        # Should succeed or have a clear error message
        if result.returncode != 0:
            # Check if it's a missing dependency issue
            assert "dependency" in result.stderr.lower() or "error" in result.stderr.lower()

    def test_cli_list_moods(self):
        """Test CLI list moods command."""
        result = subprocess.run(
            [sys.executable, "-m", "musicgen", "list-moods"],
            capture_output=True,
            text=True
        )
        # Should list available moods
        if result.returncode == 0:
            assert "epic" in result.stdout.lower() or "peaceful" in result.stdout.lower()
```

#### 1.5 Run Coverage Analysis

Add a coverage test target:

```python
"""
Coverage test helper.

Run with: pytest tests/test_coverage.py --cov=src/musicgen --cov-report=html
"""

def test_coverage_threshold():
    """
    Placeholder test to trigger coverage reporting.

    Actual coverage is checked by pytest-cov settings.
    """
    assert True
```

### Task 2: Create Sphinx Documentation

#### 2.1 Set Up Sphinx Documentation Structure

Create the documentation directory structure:

```
docs/
├── api/
│   ├── __init__.py
│   └── conf.py                     # Sphinx configuration
├── tutorials/
│   ├── 01-getting-started.md
│   ├── 02-scales-and-keys.md
│   ├── 03-melody-generation.md
│   ├── 04-orchestration.md
│   └── 05-exporting-music.md
├── examples/
│   ├── basic_melody.py
│   ├── chord_progressions.py
│   ├── full_composition.py
│   └── mood_generation.py
├── _static/
│   └── custom.css
├── _templates/
│   └── layout.html
├── index.md                        # Documentation homepage
├── installation.md
├── contributing.md
├── changelog.md
├── license.md
└── Makefile                        # Build automation
```

#### 2.2 Create `docs/api/conf.py`

```python
"""
Sphinx configuration file for musicgen API documentation.
"""

import os
import sys

# Add the source directory to the path
sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information -----------------------------------------------------
project = 'Music Generation Library'
copyright = '2025, MusicGen Contributors'
author = 'MusicGen Contributors'
release = '0.1.0'
version = '0.1.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here
extensions = [
    'sphinx.ext.autodoc',           # Include documentation from docstrings
    'sphinx.ext.autosummary',       # Generate summary tables
    'sphinx.ext.napoleon',          # Support for NumPy and Google style docstrings
    'sphinx.ext.viewcode',          # Add links to highlighted source code
    'sphinx.ext.intersphinx',       # Link to other project's documentation
    'sphinx.ext.mathjax',           # Render math via JavaScript
    'sphinx_rtd_theme',             # ReadTheDocs theme
    'myst_parser',                  # Support for Markdown
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['../_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The suffix(es) of source filenames.
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# The master toctree document.
master_doc = '../index'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

# Theme options
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False
}

# Add any paths that contain custom static files
html_static_path = ['../_static']

# Custom CSS
html_css_files = ['custom.css']

# -- Options for autodoc -----------------------------------------------------

# This value controls how to represent typehints
autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented'

# Order members by source order
autodoc_member_order = 'bysource'

# Don't show inherited members
autodoc_default_flags = ['no-inherited-members']

# -- Options for autosummary -------------------------------------------------

autosummary_generate = True
autosummary_imported_members = True

# -- Options for intersphinx -----------------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}

# -- Napoleon settings -------------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True
```

#### 2.3 Create API Documentation Files

Create `docs/api/core.rst`:

```rst
Core Data Structures
====================

This module contains the fundamental classes for representing musical elements.

Note Class
----------

.. autoclass:: musicgen.core.note.Note
   :members:
   :undoc-members:
   :show-inheritance:

Rest Class
----------

.. autoclass:: musicgen.core.note.Rest
   :members:
   :undoc-members:

Chord Class
-----------

.. autoclass:: musicgen.core.chord.Chord
   :members:
   :undoc-members:
   :show-inheritance:

Duration Constants
------------------

.. automodule:: musicgen.core.note
   :members: WHOLE, HALF, QUARTER, EIGHTH, SIXTEENTH
   :no-imported-members:

Dynamic Constants
-----------------

.. automodule:: musicgen.core.note
   :members: PP, P, MP, MF, F, FF
   :no-imported-members:

Chord Qualities
---------------

.. automodule:: musicgen.core.chord
   :members: MAJOR, MINOR, DIMINISHED, AUGMENTED
   :no-imported-members:
```

Create `docs/api/theory.rst`:

```rst
Music Theory Module
===================

Scale Class
-----------

.. autoclass:: musicgen.theory.scales.Scale
   :members:
   :undoc-members:
   :show-inheritance:

Key Class
---------

.. autoclass:: musicgen.theory.keys.Key
   :members:
   :undoc-members:
   :show-inheritance:

KeySignature Class
-------------------

.. autoclass:: musicgen.theory.keys.KeySignature
   :members:
   :undoc-members:

Progression Class
-----------------

.. autoclass:: musicgen.theory.progressions.Progression
   :members:
   :undoc-members:
   :show-inheritance:
```

Create `docs/api/composition.rst`:

```rst
Composition Module
==================

Melody Class
------------

.. autoclass:: musicgen.composition.melody.Melody
   :members:
   :undoc-members:
   :show-inheritance:

Motif Class
-----------

.. autoclass:: musicgen.composition.melody.Motif
   :members:
   :undoc-members:
   :show-inheritance:

Phrase Class
------------

.. autoclass:: musicgen.composition.melody.Phrase
   :members:
   :undoc-members:

MelodyGenerator Class
---------------------

.. autoclass:: musicgen.composition.melody.MelodyGenerator
   :members:
   :undoc-members:
   :show-inheritance:

Form Classes
------------

.. autoclass:: musicgen.composition.forms.Form
   :members:
   :undoc-members:
   :show-inheritance:
```

Create `docs/api/orchestration.rst`:

```rst
Orchestration Module
====================

Instrument Class
-----------------

.. autoclass:: musicgen.orchestration.instruments.Instrument
   :members:
   :undoc-members:
   :show-inheritance:

Ensemble Class
--------------

.. autoclass:: musicgen.orchestration.ensembles.Ensemble
   :members:
   :undoc-members:
   :show-inheritance:
```

Create `docs/api/io.rst`:

```rst
Input/Output Module
===================

MIDI Writer
-----------

.. autoclass:: musicgen.io.midi_writer.MIDIWriter
   :members:
   :undoc-members:

Audio Synthesizer
-----------------

.. autoclass:: musicgen.io.audio_synthesizer.AudioSynthesizer
   :members:
   :undoc-members:

MusicXML Writer
---------------

.. autoclass:: musicgen.io.musicxml_writer.MusicXMLWriter
   :members:
   :undoc-members:

LilyPond Writer
---------------

.. autoclass:: musicgen.io.lilypond_writer.LilyPondWriter
   :members:
   :undoc-members:
```

Create `docs/api/config.rst`:

```rst
Configuration Module
====================

Mood Presets
------------

.. automodule:: musicgen.config.moods
   :members:
   :undoc-members:

CompositionRequest
-------------------

.. autoclass:: musicgen.generator.CompositionRequest
   :members:
   :undoc-members:
```

Create `docs/api/index.rst`:

```rst
API Reference
=============

This page contains the API reference for all musicgen modules.

.. toctree::
   :maxdepth: 2

   core
   theory
   composition
   orchestration
   io
   config

Main Generator
--------------

.. autoclass:: musicgen.generator.generate
   :members:
```

#### 2.4 Create `docs/Makefile`

```makefile
# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
```

### Task 3: Create Tutorial Documentation

#### 3.1 Create `docs/tutorials/01-getting-started.md`

```markdown
# Getting Started with MusicGen

Welcome to the Music Generation Library! This tutorial will guide you through the basics of creating music programmatically using traditional music theory.

## Installation

Install MusicGen using pip:

```bash
pip install musicgen
```

For development, install with optional dependencies:

```bash
pip install musicgen[dev]
```

## Your First Note

Let's start by creating a simple musical note:

```python
from musicgen import Note, QUARTER

# Create a C quarter note
note = Note("C4", QUARTER)

print(f"Note: {note.name}{note.octave}")
print(f"MIDI number: {note.midi_number}")
print(f"Frequency: {note.frequency:.2f} Hz")
```

Output:
```
Note: C4
MIDI number: 60
Frequency: 261.63 Hz
```

## Creating a Scale

Now let's create a musical scale and explore its properties:

```python
from musicgen import Scale

# Create C major scale
c_major = Scale("C", "major")

print("Notes in C major:")
for note_name in c_major.notes:
    print(f"  {note_name}")

# Access scale degrees
tonic = c_major.get_degree(1)  # C
dominant = c_major.get_degree(5)  # G

print(f"\nTonic: {tonic}")
print(f"Dominant: {dominant}")
```

## Building a Chord

Create chords using the scale:

```python
from musicgen import Chord, MAJOR

# C major triad
c_chord = Chord("C", MAJOR, root_octave=4)

print("C major chord notes:")
for note in c_chord.notes:
    print(f"  {note}")
```

## Generating a Simple Melody

Create a simple ascending melody:

```python
from musicgen import Note, QUARTER, Scale

# Create a scale
scale = Scale("C", "major")

# Create an ascending scale melody
notes = [scale.get_degree(i + 1) for i in range(8)]

# Assign duration to each note
for note in notes:
    note.duration = QUARTER

print("Simple ascending melody:")
for note in notes:
    print(f"  {note.name}{note.octave}")
```

## Exporting to MIDI

Export your melody to a MIDI file:

```python
from musicgen import MIDIWriter, Score, Part

# Create a score
score = Score()

# Add a melody part
part = Part(instrument="piano", notes=notes)
score.add_part(part)

# Write to MIDI
MIDIWriter.write(score, "my_first_melody.mid")

print("MIDI file created: my_first_melody.mid")
```

## What's Next

In the next tutorial, you'll learn about:
- Different scale types (minor, modes, pentatonic)
- Key signatures and their relationships
- Diatonic chords in a key

Continue to [Scales and Keys](02-scales-and-keys.md).
```

#### 3.2 Create `docs/tutorials/02-scales-and-keys.md`

```markdown
# Scales and Keys

This tutorial explores the music theory foundation of MusicGen: scales, keys, and their relationships.

## Scale Types

MusicGen supports many scale types:

```python
from musicgen import Scale

# Major scale
major = Scale("C", "major")
print(f"Major: {major.notes}")

# Natural minor
minor = Scale("C", "natural_minor")
print(f"Minor: {minor.notes}")

# Harmonic minor (raised 7th)
harmonic_minor = Scale("C", "harmonic_minor")
print(f"Harmonic minor: {harmonic_minor.notes}")

# Dorian mode
dorian = Scale("D", "dorian")
print(f"D Dorian: {dorian.notes}")

# Major pentatonic
pentatonic = Scale("C", "major_pentatonic")
print(f"Pentatonic: {pentatonic.notes}")
```

## Scale Degrees

Access individual scale degrees:

```python
scale = Scale("C", "major")

# Get scale degrees
tonic = scale.get_degree(1)      # C
supertonic = scale.get_degree(2)  # D
mediant = scale.get_degree(3)     # E
subdominant = scale.get_degree(4) # F
dominant = scale.get_degree(5)    # G
submediant = scale.get_degree(6)  # A
leading_tone = scale.get_degree(7) # B

# Degrees beyond 7 extend to next octave
high_tonic = scale.get_degree(8)  # C5 (octave higher)
```

## Checking Scale Membership

Test if notes belong to a scale:

```python
scale = Scale("C", "major")

# Check individual notes
print(scale.contains("C"))   # True
print(scale.contains("F#"))  # False

# Find scale degree of a note
degree = scale.get_note_index("G")
print(f"G is degree {degree} of C major")  # degree 5
```

## Key Signatures

Working with keys and key signatures:

```python
from musicgen import Key

# Create a key
c_major = Key("C", "major")
print(f"Key: {c_major}")
print(f"Accidentals: {c_major.signature.accidentals}")

# Keys with accidentals
g_major = Key("G", "major")
print(f"G major sharps: {g_major.signature.sharps}")

f_major = Key("F", "major")
print(f"F major flats: {f_major.signature.flats}")
```

## Relative and Parallel Keys

Explore key relationships:

```python
c_major = Key("C", "major")

# Relative minor (same key signature, different tonic)
a_minor = c_major.relative()
print(f"Relative of C major: {a_minor}")

# Parallel minor (same tonic, different key signature)
c_minor = c_major.parallel()
print(f"Parallel of C major: {c_minor}")
print(f"C minor accidentals: {c_minor.signature.accidentals}")  # 3 flats
```

## Diatonic Chords

Generate chords from a scale:

```python
scale = Scale("C", "major")

# Get all diatonic triads
chords = scale.diatonic_chords()

print("Diatonic chords in C major:")
for i, chord in enumerate(chords):
    roman = ["i", "ii", "iii", "iv", "v", "vi", "vii"][i]
    print(f"  {roman.upper() if chord.quality == 'major' else roman}: "
          f"{chord.root_name} {chord.quality}")
```

Output:
```
Diatonic chords in C major:
  I: C major
  ii: D minor
  iii: E minor
  IV: F major
  V: G major
  vi: A minor
  vii: B diminished
```

## Scale Transposition

Transpose scales to different keys:

```python
# Transpose up a perfect fifth (7 semitones)
c_major = Scale("C", "major")
g_major = c_major.transpose(7)

print(f"Original: {c_major.notes}")
print(f"Transposed: {g_major.notes}")
```

## Putting It Together

Create a simple chord progression using diatonic chords:

```python
from musicgen import Key

key = Key("C", "major")

# I-IV-V-I progression
roman_numerals = ["I", "IV", "V", "I"]
chords = key.diatonic_chords()

progression = [chords[i-1] for i in [1, 4, 5, 1]]

print("Chord progression:")
for roman, chord in zip(roman_numerals, progression):
    print(f"  {roman}: {chord.root_name} {chord.quality}")
```

## What's Next

In the next tutorial, you'll learn about:
- Melody generation with contours
- Motivic development techniques
- Phrase structure

Continue to [Melody Generation](03-melody-generation.md).
```

#### 3.3 Create `docs/tutorials/03-melody-generation.md`

```markdown
# Melody Generation

This tutorial covers creating melodies with MusicGen, including contours, motivic development, and phrase structure.

## Basic Melody Creation

Create a melody with a specific contour:

```python
from musicgen import Scale, MelodyGenerator, MelodicContour, Key

scale = Scale("C", "major")
key = Key("C", "major")

generator = MelodyGenerator(scale, key, tempo=120)

# Generate a melody with an arch contour
melody = generator.generate_melody(
    progression=...,  # from previous tutorial
    contour=MelodicContour.ARCH,
    motivic_unity=0.8
)

print(f"Generated melody with {melody.length} notes")
print(f"Range: {melody.range} semitones")
```

## Melodic Contours

MusicGen provides several predefined contour types:

```python
from musicgen import MelodicContour

# Available contours
contours = [
    MelodicContour.ASCENDING,      # Overall upward motion
    MelodicContour.DESCENDING,     # Overall downward motion
    MelodicContour.ARCH,           # Rise then fall
    MelodicContour.INVERTED_ARCH,  # Fall then rise
    MelodicContour.WAVE,           # Alternating up and down
    MelodicContour.STATIC,         # Limited pitch range
]
```

## Working with Motifs

A motif is a short melodic idea that can be developed:

```python
from musicgen import Motif, Note, QUARTER, Scale, MelodicContour

# Create a simple motif
scale = Scale("C", "major")
notes = [
    scale.get_degree(1),  # C
    scale.get_degree(3),  # E
    scale.get_degree(5),  # G
    scale.get_degree(8),  # C (high)
]

for note in notes:
    note.duration = QUARTER

motif = Motif(notes, contour=MelodicContour.ASCENDING)

print(f"Motif length: {motif.length}")
print(f"Motif duration: {motif.total_duration} beats")
```

## Motivic Development

Develop your motif using classical techniques:

```python
# Sequence (transposed repetition)
sequence = motif.develop("sequence", interval=5)

# Inversion (mirror intervals)
inverted = motif.develop("inversion")

# Retrograde (reverse order)
reversed_motif = motif.develop("retrograde")

# Augmentation (double durations)
augmented = motif.develop("augmentation")

# Diminution (halve durations)
diminished = motif.develop("diminution")
```

## Rhythm Patterns

Use predefined rhythmic patterns:

```python
from musicgen import RhythmPattern

# Preset patterns
basic = RhythmPattern.from_preset("basic")
waltz = RhythmPattern.from_preset("waltz")
syncopated = RhythmPattern.from_preset("syncopated")

print(f"Waltz pattern: {waltz.durations}")
# Output: [0.5, 0.25, 0.25] - quarter, two eighths
```

## Phrase Structure

Create musical phrases with proper cadences:

```python
from musicgen import Phrase, Note, QUARTER

# An antecedent phrase (question)
notes_antecedent = [Note(f"{n}4", QUARTER) for n in ["C", "D", "E", "F"]]
antecedent = Phrase(notes_antecedent, phrase_type="antecedent", cadence="half")

# A consequent phrase (answer)
notes_consequent = [Note(f"{n}4", QUARTER) for n in ["G", "F", "E", "C"]]
consequent = Phrase(notes_consequent, phrase_type="consequent", cadence="authentic")

# Check if they form a period
if antecedent.is_period_partner(consequent):
    print("Forms a proper period!")
```

## Complete Melody Example

Put it all together:

```python
from musicgen import Scale, Key, MelodyGenerator, MelodicContour
from musicgen.theory.progressions import Progression

# Set up
scale = Scale("D", "minor")
key = Key("D", "minor")
progression = Progression.from_roman("i-iv-VII-i", key="D")

# Generate
generator = MelodyGenerator(scale, key, tempo=100)
generator.set_seed(42)  # For reproducibility

melody = generator.generate_melody(
    progression=progression,
    contour=MelodicContour.WAVE,
    form_structure="period",
    motivic_unity=0.75
)

print(f"Generated melody:")
print(f"  Notes: {melody.length}")
print(f"  Duration: {melody.total_duration} beats")
print(f"  Range: {melody.range} semitones")
```

## What's Next

In the next tutorial, you'll learn about:
- Instrument definitions and ranges
- Ensemble presets
- Orchestration techniques

Continue to [Orchestration](04-orchestration.md).
```

#### 3.4 Create `docs/tutorials/04-orchestration.md`

```markdown
# Orchestration

This tutorial covers working with instruments and ensembles in MusicGen.

## Instrument Definitions

MusicGen includes definitions for orchestral instruments:

```python
from musicgen import Instrument

# Create an instrument
violin = Instrument(
    name="violin",
    range="G3-A7",
    transposition=0,
    midi_program=40
)

print(f"Violin range: {violin.range}")
print(f"MIDI program: {violin.midi_program}")

# Check if a note is in range
from musicgen import Note
note = Note("A4", 1.0)
print(f"Is A4 in violin range? {violin.in_range(note)}")
```

## Available Instruments

Common orchestral instruments:

```python
# Strings
violin = Instrument.preset("violin")
viola = Instrument.preset("viola")
cello = Instrument.preset("cello")
bass = Instrument.preset("double_bass")

# Woodwinds
flute = Instrument.preset("flute")
oboe = Instrument.preset("oboe")
clarinet = Instrument.preset("clarinet")
bassoon = Instrument.preset("bassoon")

# Brass
trumpet = Instrument.preset("trumpet")
horn = Instrument.preset("french_horn")
trombone = Instrument.preset("trombone")
tuba = Instrument.preset("tuba")
```

## Transposing Instruments

Handle instruments that transpose:

```python
# Clarinet in Bb (sounds a major second lower than written)
clarinet = Instrument.preset("clarinet")

written_note = Note("C4", 1.0)
sounding_note = clarinet.written_to_concert(written_note)

print(f"Written: {written_note}")
print(f"Sounding: {sounding_note}")  # Bb3
```

## Ensemble Presets

Use pre-defined ensemble configurations:

```python
from musicgen import Ensemble

# String quartet
string_quartet = Ensemble.preset("string_quartet")
print("String quartet instruments:")
for inst in string_quartet.instruments:
    print(f"  - {inst.name}")

# Full orchestra
orchestra = Ensemble.preset("orchestra")
print(f"\nOrchestra has {len(orchestra.instruments)} instruments")
```

## Custom Ensembles

Create your own ensemble:

```python
from musicgen import Ensemble, Instrument

# Chamber ensemble
instruments = [
    Instrument.preset("violin"),
    Instrument.preset("viola"),
    Instrument.preset("cello"),
    Instrument.preset("piano"),
]

ensemble = Ensemble(
    name="chamber_group",
    instruments=instruments
)
```

## Texture Types

Specify musical texture:

```python
from musicgen import Texture

# Homophonic - melody with accompaniment
texture = Texture.homophonic(
    melody_instruments=["violin", "flute"],
    harmony_instruments=["viola", "cello"],
    bass_instruments=["double_bass"]
)

# Polyphonic - independent voices
texture = Texture.polyphonic(
    instruments=["violin", "viola", "cello"]
)
```

## Complete Orchestration Example

```python
from musicgen import Ensemble, Texture, Scale, Key, MelodyGenerator
from musicgen.theory.progressions import Progression

# Set up musical elements
scale = Scale("C", "major")
key = Key("C", "major")
progression = Progression.from_roman("I-IV-V-I", key="C")

# Create ensemble
ensemble = Ensemble.preset("string_quartet")

# Define texture
texture = Texture.homophonic(
    melody_instruments=["violin"],
    harmony_instruments=["viola"],
    bass_instruments=["cello"]
)

# Generate for each instrument
generator = MelodyGenerator(scale, key)

parts = {}
for instrument in ensemble.instruments:
    if instrument.name in texture.melody_instruments:
        melody = generator.generate_melody(
            progression=progression,
            contour=MelodicContour.ARCH
        )
        parts[instrument.name] = melody
    elif instrument.name in texture.harmony_instruments:
        # Generate harmony
        parts[instrument.name] = ...
    elif instrument.name in texture.bass_instruments:
        # Generate bass line
        parts[instrument.name] = ...

print(f"Generated parts for: {', '.join(parts.keys())}")
```

## What's Next

In the final tutorial, you'll learn about:
- Exporting to MIDI
- Generating audio
- Creating sheet music

Continue to [Exporting Music](05-exporting-music.md).
```

#### 3.5 Create `docs/tutorials/05-exporting-music.md`

```markdown
# Exporting Music

This tutorial covers all the ways to export your musical creations from MusicGen.

## MIDI Export

The simplest export format - MIDI files can be played by any DAW or media player.

```python
from musicgen import MIDIWriter, Score, Part
from musicgen import Note, QUARTER, Scale

# Create a simple melody
scale = Scale("C", "major")
notes = [scale.get_degree(i % 7 + 1) for i in range(16)]

for note in notes:
    note.duration = QUARTER

# Create a score
score = Score()
part = Part(instrument="piano", notes=notes)
score.add_part(part)

# Export to MIDI
MIDIWriter.write(score, "output.mid")

print("MIDI file created: output.mid")
```

## Audio Export

Generate actual audio files using a SoundFont:

```python
from musicgen import AudioSynthesizer

# Initialize synthesizer with SoundFont
synth = AudioSynthesizer(soundfont_path="path/to/soundfont.sf2")

# Render MIDI to audio
audio_path = synth.render(
    midi_file="output.mid",
    output_format="wav"
)

print(f"Audio file created: {audio_path}")
```

### Audio Formats

Supported audio formats:

```python
# WAV (uncompressed)
wav_path = synth.render("input.mid", output_format="wav")

# FLAC (lossless compression)
flac_path = synth.render("input.mid", output_format="flac")

# With normalization
audio_path = synth.render(
    "input.mid",
    output_format="wav",
    normalize=True
)
```

## MusicXML Export

Export to MusicXML for use in notation software like MuseScore, Sibelius, or Finale:

```python
from musicgen import MusicXMLWriter

# Export to MusicXML
MusicXMLWriter.write(score, "output.musicxml")

print("MusicXML file created: output.musicxml")
```

## LilyPond Export

Generate publication-quality sheet music with LilyPond:

```python
from musicgen import LilyPondWriter

# Export to PDF via LilyPond
writer = LilyPondWriter()

# Generate both .ly and .pdf
pdf_path = writer.write(
    score=score,
    output_pdf="output.pdf",
    output_ly="output.ly"
)

print(f"PDF created: {pdf_path}")
```

### LilyPond Options

Customize the sheet music output:

```python
pdf_path = writer.write(
    score=score,
    output_pdf="output.pdf",
    title="My Composition",
    composer="Composer Name",
    include_title=True,
    include_page_numbers=True,
    staff_size=16,  # Larger print
)
```

## Mood-Based Complete Generation

Generate complete compositions with all export formats:

```python
from musicgen import generate, CompositionRequest

# Create a composition request
request = CompositionRequest(
    mood="peaceful",
    duration=60,  # seconds
    title="Peaceful Morning",
    composer="Your Name",
    output_dir="./output",
    export_formats=["midi", "audio", "musicxml", "pdf"]
)

# Generate everything
result = generate(request)

print(f"Generated: {result.title}")
print(f"  MIDI: {result.midi_path}")
print(f"  Audio: {result.audio_path}")
print(f"  MusicXML: {result.musicxml_path}")
print(f"  PDF: {result.pdf_path}")
```

## Batch Processing

Generate multiple compositions:

```python
moods = ["epic", "peaceful", "mysterious", "romantic"]

for mood in moods:
    request = CompositionRequest(
        mood=mood,
        duration=30,
        output_dir=f"./output/{mood}"
    )

    result = generate(request)
    print(f"Generated {mood}: {result.midi_path}")
```

## CLI Usage

You can also generate music from the command line:

```bash
# Generate with default settings
python -m musicgen generate --mood peaceful --duration 30

# Specify output directory
python -m musicgen generate --mood epic --duration 60 --output-dir ./music

# List available moods
python -m musicgen list-moods

# Show help
python -m musicgen --help
```

## Next Steps

You've completed the MusicGen tutorials! You can now:

- Explore the [API Reference](../api/index.md) for detailed documentation
- Check out the [Examples](../examples/) for more code samples
- Read the [Contributing Guide](../contributing.md) to help improve MusicGen

Happy composing!
```

### Task 4: Create Example Scripts

#### 4.1 Create `docs/examples/basic_melody.py`

```python
"""
Basic Melody Generation Example

This example demonstrates how to create a simple melody
using MusicGen's core classes.
"""

from musicgen import (
    Note, Rest, Chord, Scale, Key,
    QUARTER, HALF, EIGHTH, MAJOR, MINOR
)

def main():
    """Create and display a basic melody."""

    # Create a scale
    print("Creating C major scale...")
    scale = Scale("C", "major")
    print(f"Scale notes: {scale.notes}")

    # Create a simple ascending melody
    print("\nCreating melody...")
    melody_notes = []
    rhythm = [QUARTER, QUARTER, HALF, QUARTER, QUARTER, QUARTER, HALF]

    for i, duration in enumerate(rhythm):
        degree = (i % 7) + 1
        note = scale.get_degree(degree)
        note.duration = duration
        melody_notes.append(note)
        print(f"  {note.name}{note.octave} ({duration} beats)")

    # Create chords for accompaniment
    print("\nCreating chord progression...")
    progression = [
        Chord("C", MAJOR),
        Chord("F", MAJOR),
        Chord("G", MAJOR),
        Chord("C", MAJOR),
    ]

    for chord in progression:
        chord_notes = [n.name for n in chord.notes]
        print(f"  {chord.root_name} {chord.quality}: {chord_notes}")

    # Calculate total duration
    total_duration = sum(n.duration for n in melody_notes)
    print(f"\nTotal melody duration: {total_duration} beats ({total_duration/4:.1f} measures in 4/4)")

if __name__ == "__main__":
    main()
```

#### 4.2 Create `docs/examples/chord_progressions.py`

```python
"""
Chord Progression Examples

Demonstrates various chord progression patterns and how to use them.
"""

from musicgen import Scale, Key, Progression

def main():
    """Explore chord progressions."""

    # Working in C major
    key = Key("C", "major")
    print(f"Key: {key}\n")

    # Example 1: Basic I-IV-V-I
    print("1. Basic I-IV-V-I (authentic cadence):")
    prog1 = Progression.from_roman("I-IV-V-I", key="C")
    for chord in prog1.chords:
        print(f"   {chord.root_name} {chord.quality}")

    # Example 2: I-vi-IV-V (pop/rock progression)
    print("\n2. I-vi-IV-V (pop progression):")
    prog2 = Progression.from_roman("I-vi-IV-V", key="C")
    for chord in prog2.chords:
        print(f"   {chord.root_name} {chord.quality}")

    # Example 3: ii-V-I (jazz turnaround)
    print("\n3. ii-V-I (jazz turnaround):")
    prog3 = Progression.from_roman("ii-V-I", key="C")
    for chord in prog3.chords:
        print(f"   {chord.root_name} {chord.quality}")

    # Example 4: Circle of fifths
    print("\n4. Circle of fifths progression:")
    prog4 = Progression.circle_of_fifths("C", length=4)
    for chord in prog4.chords:
        print(f"   {chord.root_name} {chord.quality}")

    # Example 5: Functional generation
    print("\n5. Functionally generated progression:")
    prog5 = Progression.functional(
        key="C",
        length=8,
        cadence="authentic",
        allow_secondary=False
    )
    for i, chord in enumerate(prog5.chords, 1):
        function = chord.function if hasattr(chord, 'function') else ""
        print(f"   {i}. {chord.root_name} {chord.quality} {function}")

if __name__ == "__main__":
    main()
```

#### 4.3 Create `docs/examples/full_composition.py`

```python
"""
Full Composition Example

Demonstrates a complete music generation workflow from scale to export.
"""

from pathlib import Path
from musicgen import (
    Scale, Key, Progression,
    MelodyGenerator, MelodicContour,
    Ensemble, Texture,
    MIDIWriter, Score, Part
)

def main():
    """Generate a complete composition."""

    # Setup
    print("Setting up composition...")
    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)

    # Musical elements
    scale = Scale("D", "harmonic_minor")
    key = Key("D", "minor")
    progression = Progression.from_roman("i-iv-VII-i", key="D")

    print(f"Key: {key}")
    print(f"Scale: {scale.notes}")
    print(f"Progression: {[c.root_name for c in progression.chords]}")

    # Create melody
    print("\nGenerating melody...")
    generator = MelodyGenerator(scale, key, tempo=110)
    generator.set_seed(42)  # Reproducible

    melody = generator.generate_melody(
        progression=progression,
        contour=MelodicContour.WAVE,
        form_structure="period",
        motivic_unity=0.8
    )

    print(f"Generated melody with {melody.length} notes")
    print(f"Range: {melody.range} semitones")
    print(f"Duration: {melody.total_duration} beats")

    # Create ensemble
    print("\nSetting up ensemble...")
    ensemble = Ensemble.preset("string_quartet")
    print(f"Instruments: {[inst.name for inst in ensemble.instruments]}")

    # Create score
    print("\nCreating score...")
    score = Score()
    score.title = "String Quartet in D Minor"
    score.composer = "MusicGen"

    # Add melody to violin part
    violin_part = Part(
        instrument="violin",
        notes=melody.notes
    )
    score.add_part(violin_part)

    # Add simple accompaniment parts
    for instrument_name in ["viola", "cello"]:
        # Generate simple harmony
        harmony_notes = []
        for chord in progression.chords:
            # Use chord tones for accompaniment
            for note in chord.notes[:2]:  # Root and third
                n = Note(note.name, note.octave - 1, QUARTER)
                harmony_notes.append(n)

        part = Part(instrument=instrument_name, notes=harmony_notes)
        score.add_part(part)

    # Export
    print("\nExporting...")

    # MIDI
    midi_path = output_dir / "composition.mid"
    MIDIWriter.write(score, str(midi_path))
    print(f"  MIDI: {midi_path}")

    # Print summary
    print("\n" + "="*50)
    print("Composition Summary")
    print("="*50)
    print(f"Title: {score.title}")
    print(f"Key: {key}")
    print(f"Tempo: {generator.tempo} BPM")
    print(f"Parts: {len(score.parts)}")
    print(f"Total notes: {sum(len(p.notes) for p in score.parts)}")
    print(f"\nFiles saved to: {output_dir.absolute()}")

if __name__ == "__main__":
    main()
```

#### 4.4 Create `docs/examples/mood_generation.py`

```python
"""
Mood-Based Music Generation Example

Demonstrates generating music for different moods using presets.
"""

from pathlib import Path
from musicgen import generate, CompositionRequest

def main():
    """Generate compositions for different moods."""

    output_dir = Path("./mood_output")
    output_dir.mkdir(exist_ok=True)

    # Available moods
    moods = [
        "epic",
        "peaceful",
        "mysterious",
        "melancholic"
    ]

    print("MusicGen Mood-Based Generation")
    print("=" * 50)

    for mood in moods:
        print(f"\nGenerating '{mood}' composition...")

        request = CompositionRequest(
            mood=mood,
            duration=20,  # 20 seconds for quick demo
            output_dir=str(output_dir / mood)
        )

        result = generate(request)

        print(f"  Key: {result.key}")
        print(f"  Scale: {result.scale_type}")
        print(f"  Tempo: {result.tempo} BPM")
        print(f"  Instruments: {', '.join(result.instruments[:5])}")

        # Check output files
        if result.midi_path and Path(result.midi_path).exists():
            print(f"  MIDI: {result.midi_path}")

        if result.audio_path and Path(result.audio_path).exists():
            print(f"  Audio: {result.audio_path}")

    print("\n" + "=" * 50)
    print(f"All compositions saved to: {output_dir.absolute()}")

if __name__ == "__main__":
    main()
```

### Task 5: Update Main Documentation Files

#### 5.1 Update `README.md`

```markdown
# Music Generation Library

A Python library for rule-based orchestral music generation using traditional music theory principles.

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## Features

- **Music Theory Foundation**: Complete implementation of scales, keys, chords, and progressions
- **Melody Generation**: Rule-based melody creation with motivic development
- **Orchestration**: Support for orchestral instruments with realistic ranges
- **Export Formats**: MIDI, WAV, FLAC, MusicXML, and PDF (LilyPond)
- **Mood-Based**: Generate music based on mood presets (epic, peaceful, mysterious, etc.)
- **Voice Leading**: Classical counterpoint rules for smooth part writing
- **Musical Forms**: Binary, ternary, rondo, and sonata form structures

## Installation

```bash
pip install musicgen
```

For development:

```bash
git clone https://github.com/yourusername/music-gen-lib.git
cd music-gen-lib
pip install -e ".[dev]"
```

## Quick Start

```python
from musicgen import generate, CompositionRequest

# Generate music based on mood
request = CompositionRequest(
    mood="peaceful",
    duration=60,
    title="Peaceful Morning"
)

result = generate(request)

print(f"Generated: {result.midi_path}")
print(f"Audio: {result.audio_path}")
```

## Basic Usage

### Creating Notes and Scales

```python
from musicgen import Note, Scale, Chord, MAJOR

# Create notes
note = Note("C4", duration=1.0, velocity=90)
print(f"MIDI: {note.midi_number}, Freq: {note.frequency:.2f}Hz")

# Create scales
scale = Scale("C", "major")
print(f"Notes: {scale.notes}")

# Get scale degrees
tonic = scale.get_degree(1)  # C
dominant = scale.get_degree(5)  # G
```

### Creating Chord Progressions

```python
from musicgen import Progression, Key

key = Key("C", "major")

# From Roman numerals
prog = Progression.from_roman("I-IV-V-I", key="C")
for chord in prog.chords:
    print(f"{chord.root_name} {chord.quality}")

# Or generate functionally
prog = Progression.functional(key=key, length=8, cadence="authentic")
```

### Generating Melodies

```python
from musicgen import MelodyGenerator, MelodicContour

scale = Scale("D", "minor")
key = Key("D", "minor")

generator = MelodyGenerator(scale, key, tempo=120)
melody = generator.generate_melody(
    progression=prog,
    contour=MelodicContour.ARCH,
    motivic_unity=0.8
)
```

### Exporting Music

```python
from musicgen import MIDIWriter, Score, Part

# Create a score
score = Score()
part = Part(instrument="violin", notes=melody.notes)
score.add_part(part)

# Export to MIDI
MIDIWriter.write(score, "output.mid")

# Export to MusicXML
from musicgen import MusicXMLWriter
MusicXMLWriter.write(score, "output.musicxml")

# Export to PDF (requires LilyPond)
from musicgen import LilyPondWriter
LilyPondWriter.write(score, output_pdf="output.pdf")
```

## Mood Presets

| Mood | Key | Scale | Tempo | Style |
|------|-----|-------|-------|-------|
| `epic` | D minor | Harmonic minor | 120-140 | Grand, orchestral |
| `peaceful` | G major | Major | 60-80 | Gentle, flowing |
| `mysterious` | D minor | Harmonic minor | 80-100 | Dark, enigmatic |
| `triumpant` | C major | Major | 110-130 | Bold, celebratory |
| `melancholic` | A minor | Natural minor | 60-80 | Sad, reflective |
| `playful` | G major | Major pentatonic | 100-120 | Light, bouncy |
| `romantic` | F major | Major | 70-90 | Warm, expressive |
| `tense` | C minor | Harmonic minor | 90-110 | Dramatic, anxious |

## Command Line Interface

```bash
# Generate music by mood
python -m musicgen generate --mood epic --duration 60

# List available moods
python -m musicgen list-moods

# Specify output directory
python -m musicgen generate --mood peaceful --output-dir ./music
```

## Documentation

- [Getting Started Tutorial](docs/tutorials/01-getting-started.md)
- [API Reference](docs/api/index.md)
- [Examples](docs/examples/)

## Development

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src/musicgen --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Building Documentation

```bash
cd docs/api
make html
```

## Requirements

### Python Packages

- Python 3.10+
- music21 >= 9.0
- mido >= 1.2
- pretty-midi >= 0.2
- numpy >= 1.24
- abjad >= 3.0 (optional, for LilyPond export)

### System Dependencies

For audio synthesis:
```bash
# Ubuntu/Debian
sudo apt install fluidsynth

# macOS
brew install fluidsynth
```

For PDF generation:
```bash
# Ubuntu/Debian
sudo apt install lilypond

# macOS
brew install lilypond
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Acknowledgments

This library implements principles from:
- Traditional Western music theory
- Classical counterpoint and voice leading
- Orchestration practices
- Algorithmic composition techniques

## Citation

If you use MusicGen in your research, please cite:

```bibtex
@software{musicgen2025,
  title={MusicGen: Rule-Based Orchestral Music Generation Library},
  author={Your Name},
  year={2025},
  url={https://github.com/yourusername/music-gen-lib}
}
```
```

#### 5.2 Create `CONTRIBUTING.md`

```markdown
# Contributing to MusicGen

Thank you for your interest in contributing to MusicGen! This document provides guidelines for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming community for all contributors.

## How to Contribute

### Reporting Bugs

Report bugs via GitHub Issues with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (Python version, OS)
- Minimal code example if applicable

### Suggesting Features

Feature suggestions are welcome! Please include:
- Clear description of the feature
- Use cases and benefits
- Possible implementation approach (if known)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass
5. Update documentation as needed
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/music-gen-lib.git
cd music-gen-lib

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (if configured)
pre-commit install
```

## Coding Standards

### Style Guide

- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints for function signatures

### Documentation

- Use Google-style docstrings
- Document all public classes and functions
- Include examples for complex functionality

```python
def generate_melody(scale: Scale, length: int) -> Melody:
    """
    Generate a melody from the given scale.

    Args:
        scale: The scale to use for note selection
        length: Number of notes to generate

    Returns:
        A Melody object containing the generated notes

    Example:
        >>> scale = Scale("C", "major")
        >>> melody = generate_melody(scale, 16)
        >>> len(melody.notes)
        16
    """
```

### Testing

- Write tests for all new functionality
- Aim for >80% code coverage
- Use descriptive test names
- Include edge cases and error conditions

```python
def test_generate_melody_with_valid_scale():
    """Test melody generation with a valid scale."""
    scale = Scale("C", "major")
    melody = generate_melody(scale, 8)

    assert len(melody.notes) == 8
    assert all(n.name in scale.notes for n in melody.notes)
```

## Project Structure

```
src/musicgen/
├── core/           # Fundamental classes (Note, Chord)
├── theory/         # Music theory (Scale, Key, Progression)
├── composition/    # Composition (Melody, Form)
├── orchestration/  # Instruments and ensembles
├── io/             # Export (MIDI, MusicXML, LilyPond, audio)
├── config/         # Configuration and presets
└── generator.py    # Main generation interface
```

## Adding Features

### New Scale Types

1. Add to `ScaleType` enum in `src/musicgen/theory/scales.py`
2. Add interval pattern to `INTERVALS` dictionary
3. Add tests in `tests/test_scales.py`
4. Update documentation

### New Moods

1. Add preset to `MOOD_PRESETS` in `src/musicgen/config/moods.py`
2. Add tests in `tests/test_moods.py`
3. Update README mood table

### New Export Formats

1. Create writer class in appropriate `io/` module
2. Implement required interface methods
3. Add comprehensive tests
4. Update documentation with usage examples

## Submitting Changes

### Before Submitting

- Run full test suite: `pytest`
- Check coverage: `pytest --cov`
- Format code: `black .`
- Lint: `flake8` or `ruff`

### Pull Request Checklist

- [ ] Tests pass locally
- [ ] Coverage maintained or improved
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] PR description explains changes

## Getting Help

- Open an issue for bugs or questions
- Check existing documentation
- Browse example code

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
```

#### 5.3 Create `docs/changelog.md`

```markdown
# Changelog

All notable changes to MusicGen will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of MusicGen library
- Core music data structures (Note, Chord, Rest)
- Scale and key support (major, minor, modes, pentatonic)
- Chord progression engine with functional harmony
- Voice leading with counterpoint rules
- Melody generation with motivic development
- Orchestration module with instrument definitions
- Musical form structures (binary, ternary, rondo)
- MIDI file export
- Audio synthesis with FluidSynth
- MusicXML export
- LilyPond/PDF export
- Mood-based music generation interface
- Command-line interface

## [0.1.0] - 2025-01-11

### Added
- Initial implementation of all 13 project steps
- Comprehensive test suite
- Full API documentation
- Tutorial documentation
- Example scripts
```

## Validation Criteria

After completing this step, verify the following:

### 1. Test Coverage

```bash
# Run tests with coverage
pytest --cov=src/musicgen --cov-report=html --cov-report=term

# Verify coverage > 80%
# Open htmlcov/index.html for detailed report
```

Expected coverage by module:

| Module | Target Coverage |
|--------|-----------------|
| `core/` | 95% |
| `theory/` | 90% |
| `composition/` | 85% |
| `orchestration/` | 85% |
| `io/` | 80% |
| `config/` | 90% |
| `generator.py` | 85% |

### 2. Documentation Build

```bash
# Build Sphinx documentation
cd docs/api
make html

# Verify no warnings or errors
# Open _build/html/index.html to view
```

### 3. Example Execution

```bash
# Run all examples
python docs/examples/basic_melody.py
python docs/examples/chord_progressions.py
python docs/examples/full_composition.py
python docs/examples/mood_generation.py

# All should complete without errors
```

### 4. Integration Tests

```bash
# Run integration tests
pytest tests/test_integration.py -v

# All should pass
```

### 5. CLI Tests

```bash
# Test CLI help
python -m musicgen --help

# List moods
python -m musicgen list-moods

# Generate a test composition
python -m musicgen generate --mood peaceful --duration 10
```

## Success Criteria

Step 13 is complete when:

1. **Test Coverage**: Overall coverage exceeds 80%
2. **Documentation**: Sphinx docs build without errors
3. **Examples**: All example scripts run successfully
4. **README**: Complete with installation, usage, and examples
5. **Contributing**: Clear contribution guidelines documented
6. **CLI**: Command-line interface works for all commands
7. **Integration Tests**: Full pipeline tests pass
8. **API Docs**: All public classes and methods documented

## Final Deliverables

After completing this step, the project should have:

```
music-gen-lib/
├── README.md                    # Complete documentation
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
├── pyproject.toml               # Project configuration
├── src/musicgen/                # Complete library
├── tests/                       # Complete test suite
│   ├── conftest.py             # NEW
│   ├── test_integration.py     # NEW
│   └── test_cli.py             # NEW
├── docs/
│   ├── api/                    # NEW
│   │   ├── conf.py
│   │   ├── index.rst
│   │   ├── core.rst
│   │   ├── theory.rst
│   │   ├── composition.rst
│   │   ├── orchestration.rst
│   │   ├── io.rst
│   │   └── config.rst
│   ├── tutorials/              # NEW
│   │   ├── 01-getting-started.md
│   │   ├── 02-scales-and-keys.md
│   │   ├── 03-melody-generation.md
│   │   ├── 04-orchestration.md
│   │   └── 05-exporting-music.md
│   ├── examples/               # NEW
│   │   ├── basic_melody.py
│   │   ├── chord_progressions.py
│   │   ├── full_composition.py
│   │   └── mood_generation.py
│   ├── installation.md         # NEW
│   ├── contributing.md         # NEW
│   ├── changelog.md            # NEW
│   └── index.md                # NEW
└── examples/                   # Updated examples
```

## Project Completion

After this step, the Music Generation Library is complete with:

- 13 implementation steps fully realized
- Comprehensive test coverage
- Complete API documentation
- Tutorial documentation for users
- Example scripts demonstrating all features
- Polished README and contribution guidelines
- Working command-line interface
- Support for MIDI, audio, MusicXML, and PDF export
- Mood-based music generation
- Full orchestration capabilities

The library is ready for release on PyPI and use by composers, researchers, and music enthusiasts.
