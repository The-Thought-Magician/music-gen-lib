# Implementation Prompt: Step 7 - Musical Form Structures

## Overview

This step implements the musical form structures module for the music generation library. The forms module provides formal structures for complete compositions, including binary form (AB), ternary form (ABA), rondo form (ABACA), and basic sonata form. These structures organize musical material into coherent sections with proper thematic relationships and transitions.

**Step Objective**: Implement formal structures for complete compositions.

## Dependencies

This step depends on the following previous steps being completed:

- **Step 1 (Core Data Structures)**: `Note`, `Chord`, `Rest`, duration constants
- **Step 2 (Scales and Keys)**: `Scale` class, `Key` class
- **Step 3 (Chord Progressions)**: `Progression` class
- **Step 5 (Melody Generation)**: `Melody`, `Motif`, `Phrase` classes
- **Step 6 (Orchestration)**: `Ensemble`, `Texture` classes

### Required Imports

```python
from musicgen.core.note import Note, Rest
from musicgen.core.chord import Chord
from musicgen.theory.scales import Scale
from musicgen.theory.keys import Key
from musicgen.theory.progressions import Progression
from musicgen.composition.melody import Melody, Motif, Phrase
from musicgen.orchestration.ensembles import Ensemble
```

## Reading Context

Before implementing, read these files to understand the project structure and existing code:

1. `/home/chiranjeet/projects-cc/projects/music-gen-lib/docs/plan.md` - Overall implementation plan
2. `/home/chiranjeet/projects-cc/projects/music-gen-lib/docs/research.md` - Technical research
3. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/__init__.py` - Main package exports
4. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/composition/__init__.py` - Composition module exports
5. `/home/chiranjeet/projects-cc/projects/music-gen-lib/src/musicgen/composition/melody.py` - Melody classes

## Implementation Tasks

### Task 1: Create the Forms Module Structure

Create the forms package directory and init file:

```
src/musicgen/composition/forms.py
```

The `forms.py` file should export the main classes:
- `FormType` - Enum of form types
- `Section` - Represents a musical section
- `Form` - Base class for musical forms
- `BinaryForm` - AB form implementation
- `TernaryForm` - ABA form implementation
- `RondoForm` - ABACA form implementation
- `SonataForm` - Basic sonata form implementation
- `Transition` - Section transition handling

Update `src/musicgen/composition/__init__.py` to include:
```python
from musicgen.composition.forms import (
    FormType,
    Section,
    Form,
    BinaryForm,
    TernaryForm,
    RondoForm,
    SonataForm,
    Transition,
)
```

### Task 2: Implement FormType Enum

Define the types of musical forms:

```python
from enum import Enum

class FormType(Enum):
    """Types of musical forms."""
    BINARY = "binary"           # AB
    TERNARY = "ternary"         # ABA
    RONDO = "rondo"             # ABACA or similar
    SONATA = "sonata"           # Exposition-Development-Recapitulation
    STROPHIC = "strophic"       # Same music repeated
    THROUGH_COMPOSED = "through_composed"  # No repetition
    THEME_AND_VARIATIONS = "theme_and_variations"
    MINUET_AND_TRIO = "minuet_and_trio"
```

### Task 3: Implement Section Class

The `Section` class represents a musical section (A, B, etc.):

```python
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING
import random

if TYPE_CHECKING:
    from musicgen.composition.melody import Melody, Motif
    from musicgen.theory.keys import Key

@dataclass
class Section:
    """
    Represents a musical section within a larger form.

    A section contains melodic material, harmonic progression,
    and has properties like length, key, and character.

    Attributes:
        name: Section identifier (e.g., "A", "B", "exposition")
        length: Number of measures in this section
        key: The key of this section
        scale: The scale for this section
        tempo: Tempo in BPM (None = follows previous)
        time_signature: (beats_per_measure, beat_unit)
        dynamics: Dynamic level for this section
        melody: The primary melody (optional, generated later)
        progression: Chord progression (optional, generated later)
        theme_id: Identifier for the theme used (for returns)
        repeat: Whether this section should be repeated
    """
    name: str
    length: int
    key: Key
    scale: Scale
    tempo: Optional[float] = None
    time_signature: tuple[int, int] = (4, 4)
    dynamics: str = "mf"
    melody: Optional["Melody"] = None
    progression: Optional[Progression] = None
    theme_id: Optional[str] = None
    repeat: bool = False

    @property
    def duration_beats(self) -> float:
        """Return the duration in beats."""
        beats_per_measure, _ = self.time_signature
        return self.length * beats_per_measure

    @property
    def duration_quarters(self) -> float:
        """Return the duration in quarter notes."""
        beats_per_measure, beat_unit = self.time_signature
        # beat_unit is the note value that gets one beat (4 = quarter note)
        return self.length * beats_per_measure * (4 / beat_unit)

    def transpose_to_key(self, new_key: Key) -> "Section":
        """
        Create a copy of this section transposed to a new key.

        Args:
            new_key: The target key

        Returns:
            A new Section in the new key
        """
        return Section(
            name=self.name,
            length=self.length,
            key=new_key,
            scale=Scale(new_key.tonic, new_key.mode),
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics=self.dynamics,
            theme_id=self.theme_id,
            repeat=self.repeat
        )

    def with_variation(self, variation_type: str = "rhythmic") -> "Section":
        """
        Create a variation of this section.

        Args:
            variation_type: Type of variation - "rhythmic", "melodic", "ornamented"

        Returns:
            A new Section with varied material
        """
        # The actual variation would be applied when generating melody
        # For now, create a section marked as a variation
        new_name = f"{self.name}'" if "'" not in self.name else f"{self.name}''"
        return Section(
            name=new_name,
            length=self.length,
            key=self.key,
            scale=self.scale,
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics=self.dynamics,
            theme_id=self.theme_id,  # Same theme, varied presentation
            repeat=self.repeat
        )

    def __repr__(self) -> str:
        key_str = f"{self.key.tonic} {self.key.mode}"
        return f"Section({self.name}, {key_str}, {self.length} measures)"
```

### Task 4: Implement Transition Class

Handle transitions between sections:

```python
@dataclass
class Transition:
    """
    Represents a transition between two sections.

    Attributes:
        length: Number of measures in the transition
        from_key: The key we're transitioning from
        to_key: The key we're transitioning to
        method: How to transition - "direct", "pivot", "common_tone", "sequence"
        dynamics: Dynamic level for the transition
    """
    length: int
    from_key: Key
    to_key: Key
    method: str = "pivot"
    dynamics: str = "mp"

    @property
    def is_modulation(self) -> bool:
        """True if this is a key change."""
        return self.from_key.tonic != self.to_key.tonic or self.from_key.mode != self.to_key.mode

    @property
    def modulation_interval(self) -> int:
        """Return the interval of modulation in semitones."""
        # Calculate semitone distance between tonics
        from_scale = Scale(self.from_key.tonic, "major")
        to_note = self.to_key.tonic

        # Find the interval
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        from_idx = note_names.index(self.from_key.tonic)
        to_idx = note_names.index(to_note)

        return (to_idx - from_idx) % 12

    @classmethod
    def create_pivot(
        cls,
        from_key: Key,
        to_key: Key,
        length: int = 2
    ) -> "Transition":
        """
        Create a pivot chord transition.

        A pivot chord is a chord that belongs to both keys,
        used to smoothly modulate from one to another.

        Args:
            from_key: Starting key
            to_key: Target key
            length: Length in measures

        Returns:
            A Transition object
        """
        return cls(
            length=length,
            from_key=from_key,
            to_key=to_key,
            method="pivot",
            dynamics="mp"
        )

    @classmethod
    def create_direct(
        cls,
        from_key: Key,
        to_key: Key,
        length: int = 1
    ) -> "Transition":
        """
        Create a direct (abrupt) transition.

        Args:
            from_key: Starting key
            to_key: Target key
            length: Length in measures

        Returns:
            A Transition object
        """
        return cls(
            length=length,
            from_key=from_key,
            to_key=to_key,
            method="direct",
            dynamics="mf"
        )
```

### Task 5: Implement Base Form Class

The abstract base class for all forms:

```python
from abc import ABC, abstractmethod

class Form(ABC):
    """
    Abstract base class for musical forms.

    A Form organizes musical sections into a coherent structure
    with proper thematic relationships and transitions.
    """

    def __init__(
        self,
        form_type: FormType,
        tonic: str,
        mode: str = "major",
        tempo: float = 120.0,
        time_signature: tuple[int, int] = (4, 4),
    ):
        """
        Initialize a Form.

        Args:
            form_type: The type of form
            tonic: Tonic note name
            mode: Major or minor
            tempo: Tempo in BPM
            time_signature: Time signature as (beats, unit)
        """
        self.form_type = form_type
        self.tonic = tonic
        self.mode = mode
        self.tempo = tempo
        self.time_signature = time_signature

        self._key = Key(tonic, mode)
        self._scale = Scale(tonic, mode)
        self._sections: List[Section] = []
        self._transitions: List[Transition] = []

    @property
    def sections(self) -> List[Section]:
        """Return all sections in order."""
        return self._sections.copy()

    @property
    def transitions(self) -> List[Transition]:
        """Return all transitions in order."""
        return self._transitions.copy()

    @property
    def key(self) -> Key:
        """Return the home key."""
        return self._key

    @property
    def scale(self) -> Scale:
        """Return the home scale."""
        return self._scale

    @property
    def total_measures(self) -> int:
        """Return the total number of measures."""
        return sum(s.length for s in self._sections)

    @property
    def total_duration(self) -> float:
        """Return the total duration in quarter notes."""
        return sum(s.duration_quarters for s in self._sections)

    @property
    def form_pattern(self) -> str:
        """
        Return the form pattern as a string (e.g., "AB", "ABA").

        This should be overridden by subclasses.
        """
        names = [s.name for s in self._sections]
        return "-".join(names)

    def get_section_by_name(self, name: str) -> Optional[Section]:
        """Get a section by its name."""
        for section in self._sections:
            if section.name == name:
                return section
        return None

    def get_sections_with_theme(self, theme_id: str) -> List[Section]:
        """Get all sections using a specific theme."""
        return [s for s in self._sections if s.theme_id == theme_id]

    def add_section(self, section: Section) -> None:
        """Add a section to the form."""
        self._sections.append(section)

    def add_transition(self, transition: Transition) -> None:
        """Add a transition between sections."""
        self._transitions.append(transition)

    @abstractmethod
    def generate_sections(self) -> None:
        """
        Generate the sections for this form.

        This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def generate_transitions(self) -> None:
        """
        Generate transitions between sections.

        This method must be implemented by subclasses.
        """
        pass

    def get_summary(self) -> str:
        """Return a summary of the form structure."""
        lines = [
            f"Form: {self.form_type.value.upper()}",
            f"Key: {self._key.tonic} {self._key.mode}",
            f"Tempo: {self.tempo} BPM",
            f"Time Signature: {self.time_signature[0]}/{self.time_signature[1]}",
            f"Total Measures: {self.total_measures}",
            "",
            "Sections:"
        ]
        for section in self._sections:
            lines.append(f"  {section}")

        if self._transitions:
            lines.append("")
            lines.append("Transitions:")
            for trans in self._transitions:
                lines.append(f"  {trans}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Form({self.form_type.value}, {self._key.tonic} {self._key.mode})"
```

### Task 6: Implement Binary Form

Binary form (AB) consists of two main sections:

```python
class BinaryForm(Form):
    """
    Binary form: A + B

    Binary form has two main sections:
    - Section A: Establishes the tonic key
    - Section B: Modulates to a related key (dominant or relative minor)
                and returns to tonic
    """

    def __init__(
        self,
        tonic: str = "C",
        mode: str = "major",
        a_length: int = 8,
        b_length: int = 8,
        tempo: float = 120.0,
        time_signature: tuple[int, int] = (4, 4),
        b_key_type: str = "dominant",  # "dominant" or "relative"
    ):
        """
        Initialize a Binary Form.

        Args:
            tonic: Home tonic
            mode: Major or minor
            a_length: Length of section A in measures
            b_length: Length of section B in measures
            tempo: Tempo in BPM
            time_signature: Time signature
            b_key_type: Key for section B - "dominant" or "relative"
        """
        super().__init__(FormType.BINARY, tonic, mode, tempo, time_signature)

        self.a_length = a_length
        self.b_length = b_length
        self.b_key_type = b_key_type

        self.generate_sections()
        self.generate_transitions()

    def generate_sections(self) -> None:
        """Generate the A and B sections."""
        # Section A: In the home key
        section_a = Section(
            name="A",
            length=self.a_length,
            key=self._key,
            scale=self._scale,
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics="mf",
            theme_id="theme_a"
        )
        self.add_section(section_a)

        # Determine the key for section B
        if self.b_key_type == "dominant":
            if self.mode == "major":
                b_tonic = self._get_dominant_tonic(self.tonic)
                b_mode = "major"
            else:
                # For minor, often use the relative major
                b_tonic = self._get_relative_major_tonic(self.tonic)
                b_mode = "major"
        else:  # relative
            if self.mode == "major":
                b_tonic = self._get_relative_minor_tonic(self.tonic)
                b_mode = "minor"
            else:
                b_tonic = self._get_relative_major_tonic(self.tonic)
                b_mode = "major"

        # Section B: In related key
        key_b = Key(b_tonic, b_mode)
        scale_b = Scale(b_tonic, b_mode)

        section_b = Section(
            name="B",
            length=self.b_length,
            key=key_b,
            scale=scale_b,
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics="f",
            theme_id="theme_b"
        )
        self.add_section(section_b)

    def generate_transitions(self) -> None:
        """Generate transition from A to B."""
        if len(self._sections) < 2:
            return

        # Create a transition between A and B
        transition = Transition.create_pivot(
            from_key=self._sections[0].key,
            to_key=self._sections[1].key,
            length=1
        )
        self.add_transition(transition)

    def _get_dominant_tonic(self, tonic: str) -> str:
        """Get the dominant tonic."""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        idx = note_names.index(tonic)
        # Perfect fifth up (7 semitones)
        return note_names[(idx + 7) % 12]

    def _get_relative_minor_tonic(self, tonic: str) -> str:
        """Get the relative minor tonic (minor third down)."""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        idx = note_names.index(tonic)
        # Minor third down (4 semitones down = 8 semitones up)
        return note_names[(idx + 9) % 12]

    def _get_relative_major_tonic(self, tonic: str) -> str:
        """Get the relative major tonic (minor third up)."""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        idx = note_names.index(tonic)
        # Minor third up (3 semitones)
        return note_names[(idx + 4) % 12]
```

### Task 7: Implement Ternary Form

Ternary form (ABA) has a contrasting middle section:

```python
class TernaryForm(Form):
    """
    Ternary form: A + B + A'

    Ternary form has three sections:
    - Section A: Main theme in tonic
    - Section B: Contrasting theme in related key
    - Section A': Return of main theme, possibly with variation
    """

    def __init__(
        self,
        tonic: str = "C",
        mode: str = "major",
        a_length: int = 8,
        b_length: int = 8,
        tempo: float = 120.0,
        time_signature: tuple[int, int] = (4, 4),
        b_key_type: str = "relative",  # "dominant" or "relative" or "subdominant"
        vary_repeat: bool = True,
    ):
        """
        Initialize a Ternary Form.

        Args:
            tonic: Home tonic
            mode: Major or minor
            a_length: Length of each A section in measures
            b_length: Length of B section in measures
            tempo: Tempo in BPM
            time_signature: Time signature
            b_key_type: Key for section B
            vary_repeat: Whether to vary the repeat of A
        """
        super().__init__(FormType.TERNARY, tonic, mode, tempo, time_signature)

        self.a_length = a_length
        self.b_length = b_length
        self.b_key_type = b_key_type
        self.vary_repeat = vary_repeat

        self.generate_sections()
        self.generate_transitions()

    def generate_sections(self) -> None:
        """Generate the A, B, and A' sections."""
        # Section A: Main theme
        section_a = Section(
            name="A",
            length=self.a_length,
            key=self._key,
            scale=self._scale,
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics="mf",
            theme_id="theme_a"
        )
        self.add_section(section_a)

        # Determine the key for section B
        if self.b_key_type == "dominant":
            b_tonic = self._get_dominant_tonic(self.tonic)
            b_mode = "major" if self.mode == "major" else "major"
        elif self.b_key_type == "subdominant":
            b_tonic = self._get_subdominant_tonic(self.tonic)
            b_mode = self.mode
        else:  # relative
            if self.mode == "major":
                b_tonic = self._get_relative_minor_tonic(self.tonic)
                b_mode = "minor"
            else:
                b_tonic = self._get_relative_major_tonic(self.tonic)
                b_mode = "major"

        # Section B: Contrasting theme
        key_b = Key(b_tonic, b_mode)
        scale_b = Scale(b_tonic, b_mode)

        section_b = Section(
            name="B",
            length=self.b_length,
            key=key_b,
            scale=scale_b,
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics="mp",
            theme_id="theme_b"
        )
        self.add_section(section_b)

        # Section A': Return of main theme
        if self.vary_repeat:
            section_a_prime = section_a.with_variation("rhythmic")
        else:
            section_a_prime = Section(
                name="A'",
                length=self.a_length,
                key=self._key,
                scale=self._scale,
                tempo=self.tempo,
                time_signature=self.time_signature,
                dynamics="mf",
                theme_id="theme_a"
            )
        self.add_section(section_a_prime)

    def generate_transitions(self) -> None:
        """Generate transitions between sections."""
        # A to B transition
        trans_ab = Transition.create_pivot(
            from_key=self._sections[0].key,
            to_key=self._sections[1].key,
            length=1
        )
        self.add_transition(trans_ab)

        # B to A' transition (return to tonic)
        trans_ba = Transition.create_pivot(
            from_key=self._sections[1].key,
            to_key=self._sections[2].key,
            length=2  # Longer transition for return
        )
        self.add_transition(trans_ba)

    def _get_dominant_tonic(self, tonic: str) -> str:
        """Get the dominant tonic."""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        idx = note_names.index(tonic)
        return note_names[(idx + 7) % 12]

    def _get_subdominant_tonic(self, tonic: str) -> str:
        """Get the subdominant tonic."""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        idx = note_names.index(tonic)
        # Perfect fourth up
        return note_names[(idx + 5) % 12]

    def _get_relative_minor_tonic(self, tonic: str) -> str:
        """Get the relative minor tonic."""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        idx = note_names.index(tonic)
        return note_names[(idx + 9) % 12]

    def _get_relative_major_tonic(self, tonic: str) -> str:
        """Get the relative major tonic."""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        idx = note_names.index(tonic)
        return note_names[(idx + 4) % 12]
```

### Task 8: Implement Rondo Form

Rondo form features recurring main theme:

```python
class RondoForm(Form):
    """
    Rondo form: A + B + A + C + A (or ABACA, ABACABA, etc.)

    Rondo form features a recurring main theme (A) alternating
    with contrasting episodes (B, C, etc.).
    """

    def __init__(
        self,
        tonic: str = "C",
        mode: str = "major",
        refrain_length: int = 8,
        episode_length: int = 8,
        num_episodes: int = 2,
        tempo: float = 120.0,
        time_signature: tuple[int, int] = (4, 4),
        episode_keys: Optional[List[str]] = None,
    ):
        """
        Initialize a Rondo Form.

        Args:
            tonic: Home tonic
            mode: Major or minor
            refrain_length: Length of the A (refrain) section
            episode_length: Length of each episode
            num_episodes: Number of episodes (2 = ABACA, 3 = ABACABA)
            tempo: Tempo in BPM
            time_signature: Time signature
            episode_keys: Optional list of keys for episodes
        """
        super().__init__(FormType.RONDO, tonic, mode, tempo, time_signature)

        self.refrain_length = refrain_length
        self.episode_length = episode_length
        self.num_episodes = num_episodes
        self.episode_keys = episode_keys

        self.generate_sections()
        self.generate_transitions()

    def generate_sections(self) -> None:
        """Generate the rondo sections."""
        # Generate episode keys if not provided
        if self.episode_keys is None:
            self.episode_keys = self._generate_episode_keys()

        # Alternating refrain and episodes
        for i in range(self.num_episodes * 2 + 1):
            if i % 2 == 0:  # Refrain (A)
                section = Section(
                    name="A",
                    length=self.refrain_length,
                    key=self._key,
                    scale=self._scale,
                    tempo=self.tempo,
                    time_signature=self.time_signature,
                    dynamics="mf",
                    theme_id="refrain"
                )
            else:  # Episode (B, C, etc.)
                episode_idx = i // 2
                episode_letter = chr(ord("B") + episode_idx)
                episode_key = Key(self.episode_keys[episode_idx], self.mode)

                section = Section(
                    name=episode_letter,
                    length=self.episode_length,
                    key=episode_key,
                    scale=Scale(self.episode_keys[episode_idx], self.mode),
                    tempo=self.tempo,
                    time_signature=self.time_signature,
                    dynamics="mp",
                    theme_id=f"episode_{episode_letter.lower()}"
                )

            self.add_section(section)

    def generate_transitions(self) -> None:
        """Generate transitions between sections."""
        for i in range(len(self._sections) - 1):
            trans = Transition.create_pivot(
                from_key=self._sections[i].key,
                to_key=self._sections[i + 1].key,
                length=1
            )
            self.add_transition(trans)

    def _generate_episode_keys(self) -> List[str]:
        """Generate appropriate keys for episodes."""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        idx = note_names.index(self.tonic)

        keys = []
        for i in range(self.num_episodes):
            # Use dominant and subdominant for episodes
            if i % 2 == 0:
                # Dominant
                key_idx = (idx + 7) % 12
            else:
                # Subdominant
                key_idx = (idx + 5) % 12
            keys.append(note_names[key_idx])

        return keys
```

### Task 9: Implement Basic Sonata Form

Sonata form with exposition, development, and recapitulation:

```python
class SonataForm(Form):
    """
    Basic Sonata form: Exposition + Development + Recapitulation

    Exposition: Theme 1 (tonic) -> Bridge -> Theme 2 (dominant/relative)
    Development: Thematic development and modulations
    Recapitulation: Theme 1 (tonic) -> Bridge -> Theme 2 (tonic)
    """

    def __init__(
        self,
        tonic: str = "C",
        mode: str = "major",
        exposition_length: int = 32,
        development_length: int = 24,
        recapitulation_length: int = 32,
        tempo: float = 120.0,
        time_signature: tuple[int, int] = (4, 4),
        include_repeat: bool = True,
    ):
        """
        Initialize a Sonata Form.

        Args:
            tonic: Home tonic
            mode: Major or minor
            exposition_length: Length of exposition in measures
            development_length: Length of development in measures
            recapitulation_length: Length of recapitulation in measures
            tempo: Tempo in BPM
            time_signature: Time signature
            include_repeat: Whether to include exposition repeat
        """
        super().__init__(FormType.SONATA, tonic, mode, tempo, time_signature)

        self.exposition_length = exposition_length
        self.development_length = development_length
        self.recapitulation_length = recapitulation_length
        self.include_repeat = include_repeat

        # Subdivisions
        self.theme1_length = exposition_length // 2
        self.bridge_length = exposition_length // 8
        self.theme2_length = exposition_length - self.theme1_length - self.bridge_length

        self.generate_sections()
        self.generate_transitions()

    def generate_sections(self) -> None:
        """Generate the sonata sections."""
        # EXPOSITION

        # Theme 1: In tonic
        theme1 = Section(
            name="Theme1",
            length=self.theme1_length,
            key=self._key,
            scale=self._scale,
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics="mf",
            theme_id="theme_1"
        )
        theme1.repeat = self.include_repeat
        self.add_section(theme1)

        # Bridge: Transition to dominant/relative
        if self.mode == "major":
            bridge_key = Key(self._get_dominant_tonic(self.tonic), "major")
        else:
            bridge_key = Key(self._get_relative_major_tonic(self.tonic), "major")

        bridge = Section(
            name="Bridge",
            length=self.bridge_length,
            key=bridge_key,
            scale=Scale(bridge_key.tonic, bridge_key.mode),
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics="mp",
            theme_id="bridge"
        )
        bridge.repeat = self.include_repeat
        self.add_section(bridge)

        # Theme 2: In dominant (major) or relative major (minor)
        theme2 = Section(
            name="Theme2",
            length=self.theme2_length,
            key=bridge_key,
            scale=Scale(bridge_key.tonic, bridge_key.mode),
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics="f",
            theme_id="theme_2"
        )
        theme2.repeat = self.include_repeat
        self.add_section(theme2)

        # Codetta: Closing theme in the secondary key
        codetta = Section(
            name="Codetta",
            length=4,
            key=bridge_key,
            scale=Scale(bridge_key.tonic, bridge_key.mode),
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics="mf",
            theme_id="codetta"
        )
        codetta.repeat = self.include_repeat
        self.add_section(codetta)

        # DEVELOPMENT

        # Development: Themes developed, modulations
        development = Section(
            name="Development",
            length=self.development_length,
            key=self._key,  # May modulate within
            scale=self._scale,
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics="mp",
            theme_id="development"
        )
        self.add_section(development)

        # RECAPITULATION

        # Theme 1: Return in tonic
        theme1_repr = Section(
            name="Theme1'",
            length=self.theme1_length,
            key=self._key,
            scale=self._scale,
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics="mf",
            theme_id="theme_1"
        )
        self.add_section(theme1_repr)

        # Bridge: Modified to stay in tonic
        bridge_repr = Section(
            name="Bridge'",
            length=self.bridge_length,
            key=self._key,  # Stays in tonic
            scale=self._scale,
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics="mp",
            theme_id="bridge"
        )
        self.add_section(bridge_repr)

        # Theme 2: Now in tonic (transposed)
        theme2_repr = Section(
            name="Theme2'",
            length=self.theme2_length,
            key=self._key,  # In tonic now
            scale=self._scale,
            tempo=self.tempo,
            time_signature=self.time_signature,
            dynamics="f",
            theme_id="theme_2"
        )
        self.add_section(theme2_repr)

        # Coda: Final section in tonic
        coda_length = self.recapitulation_length - self.theme1_length - self.bridge_length - self.theme2_length
        if coda_length > 0:
            coda = Section(
                name="Coda",
                length=coda_length,
                key=self._key,
                scale=self._scale,
                tempo=self.tempo,
                time_signature=self.time_signature,
                dynamics="ff",
                theme_id="coda"
            )
            self.add_section(coda)

    def generate_transitions(self) -> None:
        """Generate transitions between sections."""
        # Add transitions between major sections
        # Theme1 -> Bridge
        self.add_transition(Transition(
            length=0,  # Immediate
            from_key=self._sections[0].key,
            to_key=self._sections[1].key,
            method="sequence"
        ))

        # Codetta -> Development (retransition)
        self.add_transition(Transition(
            length=2,
            from_key=self._sections[3].key,
            to_key=self._sections[4].key,
            method="sequence",
            dynamics="dim"
        ))

        # Development -> Theme1' (return to tonic)
        self.add_transition(Transition(
            length=4,
            from_key=self._sections[4].key,
            to_key=self._sections[5].key,
            method="pivot",
            dynamics="cresc"
        ))

    def _get_dominant_tonic(self, tonic: str) -> str:
        """Get the dominant tonic."""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        idx = note_names.index(tonic)
        return note_names[(idx + 7) % 12]

    def _get_relative_major_tonic(self, tonic: str) -> str:
        """Get the relative major tonic."""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        idx = note_names.index(tonic)
        return note_names[(idx + 4) % 12]

    @property
    def exposition_sections(self) -> List[Section]:
        """Return sections in the exposition."""
        return [s for s in self._sections if s.name in ["Theme1", "Bridge", "Theme2", "Codetta"]]

    @property
    def development_sections(self) -> List[Section]:
        """Return sections in the development."""
        return [s for s in self._sections if s.name == "Development"]

    @property
    def recapitulation_sections(self) -> List[Section]:
        """Return sections in the recapitulation."""
        return [s for s in self._sections if s.name in ["Theme1'", "Bridge'", "Theme2'", "Coda"]]
```

### Task 10: Implement Form Factory

A convenience function to create forms:

```python
def create_form(
    form_type: str | FormType,
    tonic: str = "C",
    mode: str = "major",
    tempo: float = 120.0,
    **kwargs
) -> Form:
    """
    Factory function to create a Form.

    Args:
        form_type: Type of form ("binary", "ternary", "rondo", "sonata")
        tonic: Home tonic
        mode: Major or minor
        tempo: Tempo in BPM
        **kwargs: Additional form-specific arguments

    Returns:
        A Form instance

    Examples:
        >>> form = create_form("binary", tonic="C", mode="major")
        >>> form = create_form("ternary", tonic="A", mode="minor", a_length=16)
        >>> form = create_form("rondo", tonic="G", num_episodes=3)
        >>> form = create_form("sonata", tonic="F", exposition_length=40)
    """
    if isinstance(form_type, str):
        form_type = FormType(form_type.lower())

    if form_type == FormType.BINARY:
        return BinaryForm(tonic, mode, tempo=tempo, **kwargs)
    elif form_type == FormType.TERNARY:
        return TernaryForm(tonic, mode, tempo=tempo, **kwargs)
    elif form_type == FormType.RONDO:
        return RondoForm(tonic, mode, tempo=tempo, **kwargs)
    elif form_type == FormType.SONATA:
        return SonataForm(tonic, mode, tempo=tempo, **kwargs)
    else:
        raise ValueError(f"Unsupported form type: {form_type}")
```

## File Structure

Create the following file:

```
src/musicgen/composition/
    └── forms.py          # Form classes implementation
```

Update `src/musicgen/composition/__init__.py`:

```python
"""
Composition module for rule-based music generation.

This module provides melody generation with motivic development
and musical form structures for complete compositions.
"""

from musicgen.composition.melody import (
    Melody,
    Motif,
    MelodicContour,
    RhythmPattern,
    Phrase,
    MelodyGenerator,
)
from musicgen.composition.forms import (
    FormType,
    Section,
    Form,
    BinaryForm,
    TernaryForm,
    RondoForm,
    SonataForm,
    Transition,
    create_form,
)

__all__ = [
    # Melody
    "Melody",
    "Motif",
    "MelodicContour",
    "RhythmPattern",
    "Phrase",
    "MelodyGenerator",
    # Forms
    "FormType",
    "Section",
    "Form",
    "BinaryForm",
    "TernaryForm",
    "RondoForm",
    "SonataForm",
    "Transition",
    "create_form",
]
```

## Test Requirements

Create comprehensive tests in `tests/test_forms.py`:

```python
import pytest
from musicgen.composition.forms import (
    FormType,
    Section,
    BinaryForm,
    TernaryForm,
    RondoForm,
    SonataForm,
    Transition,
    create_form,
)
from musicgen.theory.keys import Key
from musicgen.theory.scales import Scale


class TestFormType:
    """Test FormType enum."""

    def test_form_type_values(self):
        """Test that all form types are defined."""
        assert FormType.BINARY.value == "binary"
        assert FormType.TERNARY.value == "ternary"
        assert FormType.RONDO.value == "rondo"
        assert FormType.SONATA.value == "sonata"


class TestSection:
    """Test Section class."""

    def test_section_creation(self):
        """Test basic section creation."""
        key = Key("C", "major")
        scale = Scale("C", "major")

        section = Section(
            name="A",
            length=8,
            key=key,
            scale=scale
        )

        assert section.name == "A"
        assert section.length == 8
        assert section.key.tonic == "C"
        assert section.duration_beats == 32  # 8 measures * 4 beats

    def test_section_duration_quarters(self):
        """Test duration calculation in quarter notes."""
        key = Key("C", "major")
        scale = Scale("C", "major")

        section = Section(
            name="A",
            length=8,
            key=key,
            scale=scale,
            time_signature=(3, 4)  # 3/4 time
        )

        # 8 measures * 3 beats * 1 quarter per beat = 24 quarters
        assert section.duration_quarters == 24

    def test_section_transpose_to_key(self):
        """Test transposing a section to a new key."""
        key_c = Key("C", "major")
        scale_c = Scale("C", "major")

        section_a = Section(
            name="A",
            length=8,
            key=key_c,
            scale=scale_c
        )

        # Transpose to G major
        key_g = Key("G", "major")
        section_g = section_a.transpose_to_key(key_g)

        assert section_g.name == "A"
        assert section_g.key.tonic == "G"
        assert section_g.length == 8
        assert section_g.theme_id == section_a.theme_id

    def test_section_with_variation(self):
        """Test creating a variation of a section."""
        key = Key("C", "major")
        scale = Scale("C", "major")

        section_a = Section(
            name="A",
            length=8,
            key=key,
            scale=scale,
            theme_id="theme_main"
        )

        section_varied = section_a.with_variation("rhythmic")

        assert section_varied.name == "A'"
        assert section_varied.theme_id == "theme_main"  # Same theme
        assert section_varied.key == section_a.key


class TestTransition:
    """Test Transition class."""

    def test_transition_creation(self):
        """Test basic transition creation."""
        key_c = Key("C", "major")
        key_g = Key("G", "major")

        trans = Transition(
            length=2,
            from_key=key_c,
            to_key=key_g
        )

        assert trans.length == 2
        assert trans.from_key.tonic == "C"
        assert trans.to_key.tonic == "G"

    def test_transition_is_modulation(self):
        """Test modulation detection."""
        key_c = Key("C", "major")
        key_g = Key("G", "major")
        key_c2 = Key("C", "major")

        trans_mod = Transition(2, key_c, key_g)
        trans_same = Transition(2, key_c, key_c2)

        assert trans_mod.is_modulation == True
        assert trans_same.is_modulation == False

    def test_transition_modulation_interval(self):
        """Test modulation interval calculation."""
        key_c = Key("C", "major")
        key_g = Key("G", "major")

        trans = Transition(2, key_c, key_g)
        # C to G is a perfect fifth (7 semitones)
        assert trans.modulation_interval == 7

    def test_create_pivot_transition(self):
        """Test creating a pivot transition."""
        key_c = Key("C", "major")
        key_g = Key("G", "major")

        trans = Transition.create_pivot(key_c, key_g, 2)

        assert trans.method == "pivot"
        assert trans.length == 2
        assert trans.from_key == key_c
        assert trans.to_key == key_g

    def test_create_direct_transition(self):
        """Test creating a direct transition."""
        key_c = Key("C", "major")
        key_g = Key("G", "major")

        trans = Transition.create_direct(key_c, key_g, 1)

        assert trans.method == "direct"
        assert trans.length == 1


class TestBinaryForm:
    """Test BinaryForm class."""

    def test_binary_form_creation(self):
        """Test basic binary form creation."""
        form = BinaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        assert form.form_type == FormType.BINARY
        assert form.tonic == "C"
        assert form.mode == "major"
        assert len(form.sections) == 2

    def test_binary_form_sections(self):
        """Test binary form has correct sections."""
        form = BinaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        assert form.sections[0].name == "A"
        assert form.sections[1].name == "B"
        assert form.sections[0].key.tonic == "C"
        assert form.sections[1].key.tonic == "G"  # Dominant

    def test_binary_form_relative_key(self):
        """Test binary form with relative key for B section."""
        form = BinaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8,
            b_key_type="relative"
        )

        assert form.sections[1].key.tonic == "A"  # Relative minor
        assert form.sections[1].key.mode == "minor"

    def test_binary_form_total_measures(self):
        """Test total measures calculation."""
        form = BinaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=12
        )

        assert form.total_measures == 20

    def test_binary_form_pattern(self):
        """Test form pattern string."""
        form = BinaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        assert form.form_pattern == "A-B"

    def test_binary_form_transitions(self):
        """Test binary form has transitions."""
        form = BinaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        assert len(form.transitions) > 0
        assert form.transitions[0].is_modulation == True


class TestTernaryForm:
    """Test TernaryForm class."""

    def test_ternary_form_creation(self):
        """Test basic ternary form creation."""
        form = TernaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        assert form.form_type == FormType.TERNARY
        assert len(form.sections) == 3

    def test_ternary_form_sections(self):
        """Test ternary form has correct sections."""
        form = TernaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        assert form.sections[0].name == "A"
        assert form.sections[1].name == "B"
        assert form.sections[2].name == "A'"

    def test_ternary_form_theme_return(self):
        """Test theme return in ternary form."""
        form = TernaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        # Both A sections share the same theme
        assert form.sections[0].theme_id == form.sections[2].theme_id
        assert form.sections[1].theme_id != form.sections[0].theme_id

    def test_ternary_form_key_return(self):
        """Test return to home key in A' section."""
        form = TernaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        # A and A' are in the home key
        assert form.sections[0].key.tonic == "C"
        assert form.sections[2].key.tonic == "C"

    def test_ternary_form_subdominant_b(self):
        """Test ternary form with subdominant B section."""
        form = TernaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8,
            b_key_type="subdominant"
        )

        assert form.sections[1].key.tonic == "F"  # Subdominant

    def test_ternary_form_pattern(self):
        """Test form pattern string."""
        form = TernaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        assert form.form_pattern == "A-B-A'"

    def test_ternary_form_transitions(self):
        """Test ternary form has transitions."""
        form = TernaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        # Should have A->B and B->A' transitions
        assert len(form.transitions) >= 2


class TestRondoForm:
    """Test RondoForm class."""

    def test_rondo_form_creation(self):
        """Test basic rondo form creation."""
        form = RondoForm(
            tonic="C",
            mode="major",
            refrain_length=8,
            episode_length=8,
            num_episodes=2
        )

        assert form.form_type == FormType.RONDO
        assert len(form.sections) == 5  # A-B-A-C-A

    def test_rondo_form_sections(self):
        """Test rondo form has correct sections."""
        form = RondoForm(
            tonic="C",
            mode="major",
            refrain_length=8,
            episode_length=8,
            num_episodes=2
        )

        assert form.sections[0].name == "A"
        assert form.sections[1].name == "B"
        assert form.sections[2].name == "A"
        assert form.sections[3].name == "C"
        assert form.sections[4].name == "A"

    def test_rondo_form_refrain_themes(self):
        """Test all refrain sections share theme."""
        form = RondoForm(
            tonic="C",
            mode="major",
            refrain_length=8,
            episode_length=8,
            num_episodes=2
        )

        refrain_sections = [s for s in form.sections if s.name == "A"]
        for section in refrain_sections:
            assert section.theme_id == "refrain"

    def test_rondo_form_pattern(self):
        """Test form pattern string."""
        form = RondoForm(
            tonic="C",
            mode="major",
            refrain_length=8,
            episode_length=8,
            num_episodes=2
        )

        assert form.form_pattern == "A-B-A-C-A"

    def test_rondo_form_three_episodes(self):
        """Test rondo form with three episodes (ABACABA)."""
        form = RondoForm(
            tonic="C",
            mode="major",
            refrain_length=8,
            episode_length=8,
            num_episodes=3
        )

        assert len(form.sections) == 7  # A-B-A-C-A-D-A
        assert form.form_pattern == "A-B-A-C-A-D-A"

    def test_rondo_custom_episode_keys(self):
        """Test rondo with custom episode keys."""
        form = RondoForm(
            tonic="C",
            mode="major",
            refrain_length=8,
            episode_length=8,
            num_episodes=2,
            episode_keys=["G", "F"]
        )

        # B is in G, C is in F
        assert form.sections[1].key.tonic == "G"
        assert form.sections[3].key.tonic == "F"


class TestSonataForm:
    """Test SonataForm class."""

    def test_sonata_form_creation(self):
        """Test basic sonata form creation."""
        form = SonataForm(
            tonic="C",
            mode="major",
            exposition_length=32,
            development_length=24,
            recapitulation_length=32
        )

        assert form.form_type == FormType.SONATA
        assert len(form.sections) > 0

    def test_sonata_has_exposition(self):
        """Test sonata form has exposition sections."""
        form = SonataForm(
            tonic="C",
            mode="major",
            exposition_length=32,
            development_length=24,
            recapitulation_length=32
        )

        exposition = form.exposition_sections
        assert len(exposition) > 0
        assert any(s.name == "Theme1" for s in exposition)
        assert any(s.name == "Theme2" for s in exposition)

    def test_sonata_has_development(self):
        """Test sonata form has development section."""
        form = SonataForm(
            tonic="C",
            mode="major",
            exposition_length=32,
            development_length=24,
            recapitulation_length=32
        )

        development = form.development_sections
        assert len(development) > 0
        assert development[0].name == "Development"

    def test_sonata_has_recapitulation(self):
        """Test sonata form has recapitulation sections."""
        form = SonataForm(
            tonic="C",
            mode="major",
            exposition_length=32,
            development_length=24,
            recapitulation_length=32
        )

        recap = form.recapitulation_sections
        assert len(recap) > 0
        assert any(s.name == "Theme1'" for s in recap)

    def test_sonata_theme2_key_in_exposition(self):
        """Test Theme 2 is in dominant in exposition."""
        form = SonataForm(
            tonic="C",
            mode="major",
            exposition_length=32,
            development_length=24,
            recapitulation_length=32
        )

        # Find Theme2 in exposition
        theme2 = next(s for s in form.exposition_sections if s.name == "Theme2")
        assert theme2.key.tonic == "G"  # Dominant

    def test_sonata_theme2_key_in_recapitulation(self):
        """Test Theme 2 is in tonic in recapitulation."""
        form = SonataForm(
            tonic="C",
            mode="major",
            exposition_length=32,
            development_length=24,
            recapitulation_length=32
        )

        # Find Theme2' in recapitulation
        theme2_repr = next(s for s in form.recapitulation_sections if s.name == "Theme2'")
        assert theme2_repr.key.tonic == "C"  # Tonic

    def test_sonata_total_measures(self):
        """Test total measures calculation."""
        form = SonataForm(
            tonic="C",
            mode="major",
            exposition_length=32,
            development_length=24,
            recapitulation_length=32
        )

        assert form.total_measures == 88


class TestFormFactory:
    """Test create_form factory function."""

    def test_create_binary_form(self):
        """Test creating binary form via factory."""
        form = create_form("binary", tonic="C", mode="major")
        assert isinstance(form, BinaryForm)
        assert form.form_type == FormType.BINARY

    def test_create_ternary_form(self):
        """Test creating ternary form via factory."""
        form = create_form("ternary", tonic="C", mode="major")
        assert isinstance(form, TernaryForm)
        assert form.form_type == FormType.TERNARY

    def test_create_rondo_form(self):
        """Test creating rondo form via factory."""
        form = create_form("rondo", tonic="C", mode="major")
        assert isinstance(form, RondoForm)
        assert form.form_type == FormType.RONDO

    def test_create_sonata_form(self):
        """Test creating sonata form via factory."""
        form = create_form("sonata", tonic="C", mode="major")
        assert isinstance(form, SonataForm)
        assert form.form_type == FormType.SONATA

    def test_create_form_with_kwargs(self):
        """Test factory passes kwargs to form constructor."""
        form = create_form(
            "ternary",
            tonic="C",
            mode="major",
            a_length=16,
            b_length=12
        )
        assert form.a_length == 16
        assert form.b_length == 12

    def test_create_form_invalid_type(self):
        """Test factory raises error for invalid form type."""
        with pytest.raises(ValueError):
            create_form("invalid_form")


class TestFormSummary:
    """Test form summary functionality."""

    def test_binary_form_summary(self):
        """Test binary form summary."""
        form = BinaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        summary = form.get_summary()
        assert "Binary" in summary or "BINARY" in summary
        assert "C" in summary
        assert "major" in summary
        assert "16" in summary  # Total measures

    def test_ternary_form_summary(self):
        """Test ternary form summary."""
        form = TernaryForm(
            tonic="A",
            mode="minor",
            a_length=16,
            b_length=16
        )

        summary = form.get_summary()
        assert "A" in summary  # Tonic
        assert "minor" in summary
        assert "A" in summary  # Section name


class TestSectionQueries:
    """Test section query methods."""

    def test_get_section_by_name(self):
        """Test getting section by name."""
        form = TernaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        section_a = form.get_section_by_name("A")
        assert section_a is not None
        assert section_a.name == "A"

        section_x = form.get_section_by_name("X")
        assert section_x is None

    def test_get_sections_with_theme(self):
        """Test getting sections by theme ID."""
        form = TernaryForm(
            tonic="C",
            mode="major",
            a_length=8,
            b_length=8
        )

        theme_a_sections = form.get_sections_with_theme("theme_a")
        assert len(theme_a_sections) == 2  # A and A'


class TestMinorKeyForms:
    """Test forms in minor keys."""

    def test_binary_form_minor(self):
        """Test binary form in minor."""
        form = BinaryForm(
            tonic="A",
            mode="minor",
            a_length=8,
            b_length=8
        )

        assert form.key.mode == "minor"
        # For minor, dominant section should be relative major
        assert form.sections[1].key.mode == "major"

    def test_ternary_form_minor(self):
        """Test ternary form in minor."""
        form = TernaryForm(
            tonic="A",
            mode="minor",
            a_length=8,
            b_length=8
        )

        assert form.key.mode == "minor"
        # B section in relative major
        assert form.sections[1].key.mode == "major"

    def test_sonata_form_minor(self):
        """Test sonata form in minor."""
        form = SonataForm(
            tonic="C",
            mode="minor",
            exposition_length=32,
            development_length=24,
            recapitulation_length=32
        )

        assert form.key.mode == "minor"
        # Theme 2 in relative major
        theme2 = next(s for s in form.exposition_sections if s.name == "Theme2")
        assert theme2.key.mode == "major"
```

## Validation Criteria

After implementation, verify these behaviors:

```python
# 1. Binary form structure
binary = BinaryForm(tonic="C", mode="major", a_length=8, b_length=8)
assert len(binary.sections) == 2
assert binary.sections[0].name == "A"
assert binary.sections[1].name == "B"
assert binary.sections[0].key.tonic == "C"
assert binary.sections[1].key.tonic in ["G", "Em"]  # Dominant or relative

# 2. Ternary form structure
ternary = TernaryForm(tonic="C", mode="major", a_length=8, b_length=8)
assert len(ternary.sections) == 3
assert ternary.sections[0].name == "A"
assert ternary.sections[1].name == "B"
assert ternary.sections[2].name == "A'"
assert ternary.sections[0].theme_id == ternary.sections[2].theme_id

# 3. Rondo form pattern
rondo = RondoForm(tonic="C", mode="major", refrain_length=8, episode_length=4, num_episodes=2)
assert rondo.form_pattern == "A-B-A-C-A"

# 4. Sonata form has correct sections
sonata = SonataForm(tonic="C", mode="major", exposition_length=32, development_length=24)
assert len(sonata.exposition_sections) > 0
assert len(sonata.development_sections) > 0
assert len(sonata.recapitulation_sections) > 0

# 5. Form factory
form = create_form("ternary", tonic="D", mode="minor")
assert isinstance(form, TernaryForm)
assert form.key.tonic == "D"
assert form.key.mode == "minor"
```

## Dependencies on Previous Steps

This step depends on:

1. **Step 1 (Core)**: Uses `Note`, `Chord`, `Rest`, duration constants
2. **Step 2 (Scales/Keys)**: Uses `Scale`, `Key` classes
3. **Step 3 (Progressions)**: Uses `Progression` class for harmonic structure
4. **Step 5 (Melody)**: Uses `Melody`, `Motif`, `Phrase` classes
5. **Step 6 (Orchestration)**: May reference `Ensemble` for orchestration

The following classes must be available:
- `Key` with `tonic` and `mode` properties
- `Scale` with root and scale type
- `Progression` for chord progressions
- `Melody`, `Motif`, `Phrase` from melody module

## Success Criteria

Step 7 is complete when:

1. All form classes (`BinaryForm`, `TernaryForm`, `RondoForm`, `SonataForm`) are implemented
2. `Section` class properly represents musical sections with transposition and variation
3. `Transition` class handles key changes and modulations
4. Form pattern strings correctly reflect the structure (e.g., "A-B-A'")
5. Sonata form correctly places Theme 2 in tonic for recapitulation
6. `create_form` factory function works for all form types
7. All tests pass: `pytest tests/test_forms.py`
8. Test coverage is at least 80% for the forms module

## Implementation Notes

1. **Key Relationships**: Implement standard key relationships:
   - Dominant: Perfect fifth above (major) or relative major (minor)
   - Subdominant: Perfect fourth above
   - Relative minor: Minor third below (for major keys)
   - Relative major: Minor third above (for minor keys)

2. **Section Naming**: Use standard naming conventions:
   - Main sections: A, B, C, etc.
   - Repeated/varied sections: A', A'', B'
   - Sonata sections: Theme1, Bridge, Theme2, Codetta, Development, Coda

3. **Modulation Methods**:
   - "pivot": Use a chord common to both keys
   - "direct": Abrupt change
   - "sequence": Sequential motion to new key
   - "common_tone": Sustain a note through the change

4. **Theme Return**: Ensure A sections in ternary form share the same `theme_id`

5. **Error Handling**: Raise `ValueError` with descriptive messages for:
   - Invalid form types
   - Invalid key names
   - Invalid section lengths

## Next Steps

After completing this step, proceed to **Step 8: MIDI File Generation** which will:
- Export compositions to MIDI format
- Handle multi-track output
- Convert Note/Rest to MIDI messages
- Support tempo and time signature meta-events
