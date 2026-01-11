"""Tests for AI composition module.

Tests the AI client, models, and composition building.
"""

import pytest
import json
from pathlib import Path

from musicgen.ai.models import (
    OrchestrationPlan,
    Section,
    InstrumentAssignment,
    DynamicsPlan,
    InstrumentRole,
    InstrumentSection,
    DynamicsLevel,
    ScaleType,
    FormType,
)
from musicgen.ai.composer import build_composition_from_plan


class TestOrchestrationPlan:
    """Tests for OrchestrationPlan model."""

    def test_create_minimal_plan(self):
        """Test creating a minimal plan."""
        plan = OrchestrationPlan(
            title="Test Composition",
            key="C",
            key_type="major"
        )
        assert plan.title == "Test Composition"
        assert plan.key == "C"
        assert plan.scale_type == ScaleType.MAJOR
        assert len(plan.sections) >= 2  # Default sections created
        assert len(plan.instruments) >= 3  # Default instruments created

    def test_create_full_plan(self):
        """Test creating a full plan."""
        sections = [
            Section(name="A", duration_seconds=60, key="C"),
            Section(name="B", duration_seconds=60, key="G"),
        ]

        instruments = [
            InstrumentAssignment(
                name="violin",
                section=InstrumentSection.STRINGS,
                role=InstrumentRole.MELODY,
                midi_program=40
            ),
        ]

        dynamics = DynamicsPlan(
            initial_dynamic=DynamicsLevel.MP,
            climax_dynamic=DynamicsLevel.FF,
            final_dynamic=DynamicsLevel.MP
        )

        plan = OrchestrationPlan(
            title="Full Test",
            duration_seconds=120,
            key="C",
            key_type="major",
            scale_type=ScaleType.MAJOR,
            tempo=100,
            sections=sections,
            instruments=instruments,
            form_type=FormType.BINARY,
            dynamics_plan=dynamics
        )

        assert plan.total_duration == 120
        assert plan.section_names == ["A", "B"]
        assert plan.tempo == 100


class TestInstrumentAssignment:
    """Tests for InstrumentAssignment model."""

    def test_create_instrument(self):
        """Test creating an instrument assignment."""
        inst = InstrumentAssignment(
            name="violin",
            section=InstrumentSection.STRINGS,
            role=InstrumentRole.MELODY,
            dynamics=DynamicsLevel.F,
            midi_program=40
        )
        assert inst.name == "violin"
        assert inst.section == InstrumentSection.STRINGS
        assert inst.role == InstrumentRole.MELODY

    def test_invalid_midi_program(self):
        """Test that invalid MIDI program raises error."""
        with pytest.raises(ValueError):
            InstrumentAssignment(
                name="test",
                section=InstrumentSection.STRINGS,
                midi_program=200  # Invalid
            )

    def test_invalid_range(self):
        """Test that invalid range raises error."""
        with pytest.raises(ValueError):
            InstrumentAssignment(
                name="test",
                section=InstrumentSection.STRINGS,
                range_high=200  # Invalid
            )


class TestSection:
    """Tests for Section model."""

    def test_create_section(self):
        """Test creating a section."""
        section = Section(
            name="A",
            duration_seconds=30,
            key="C",
            key_type="major",
            scale_type=ScaleType.MAJOR,
            tempo=120
        )
        assert section.name == "A"
        assert section.duration_seconds == 30
        assert section.scale_type == ScaleType.MAJOR

    def test_invalid_duration(self):
        """Test that invalid duration raises error."""
        with pytest.raises(ValueError):
            Section(
                name="A",
                duration_seconds=0,  # Invalid
                key="C"
            )


class TestDynamicsPlan:
    """Tests for DynamicsPlan model."""

    def test_create_dynamics_plan(self):
        """Test creating a dynamics plan."""
        plan = DynamicsPlan(
            initial_dynamic=DynamicsLevel.P,
            climax_dynamic=DynamicsLevel.FFF,
            final_dynamic=DynamicsLevel.PP,
            climax_point=0.8
        )
        assert plan.initial_dynamic == DynamicsLevel.P
        assert plan.climax_point == 0.8

    def test_invalid_climax_point(self):
        """Test that invalid climax point raises error."""
        with pytest.raises(ValueError):
            DynamicsPlan(climax_point=1.5)  # Invalid


class TestCompositionBuilding:
    """Tests for composition building from plans."""

    def test_build_simple_composition(self):
        """Test building a simple composition."""
        plan = OrchestrationPlan(
            title="Simple Test",
            duration_seconds=60,
            key="C",
            key_type="major",
            sections=[
                Section(name="A", duration_seconds=60, key="C", key_type="major")
            ],
            instruments=[
                InstrumentAssignment(
                    name="violin",
                    section=InstrumentSection.STRINGS,
                    role=InstrumentRole.MELODY,
                    midi_program=40
                ),
                InstrumentAssignment(
                    name="cello",
                    section=InstrumentSection.STRINGS,
                    role=InstrumentRole.BASS,
                    midi_program=42
                ),
            ]
        )

        score = build_composition_from_plan(plan, seed=42)

        assert score.title == "Simple Test"
        assert len(score.parts) == 2
        assert score.parts[0].name == "violin"
        assert score.parts[1].name == "cello"

    def test_build_with_sections(self):
        """Test building with multiple sections."""
        plan = OrchestrationPlan(
            title="Multi Section",
            duration_seconds=120,
            key="C",
            key_type="major",
            form_type=FormType.BINARY,
            sections=[
                Section(name="A", duration_seconds=60, key="C", key_type="major"),
                Section(name="B", duration_seconds=60, key="G", key_type="major"),
            ],
            instruments=[
                InstrumentAssignment(
                    name="violin",
                    section=InstrumentSection.STRINGS,
                    role=InstrumentRole.MELODY,
                    midi_program=40
                ),
            ]
        )

        score = build_composition_from_plan(plan, seed=42)

        # Should have notes from both sections
        assert len(score.parts[0].notes) > 0


class TestPlanSerialization:
    """Tests for plan JSON serialization."""

    def test_plan_to_json(self):
        """Test converting plan to JSON."""
        plan = OrchestrationPlan(
            title="Serialization Test",
            duration_seconds=60,
            key="C",
            key_type="major"
        )

        # Convert to dict (Pydantic's model_dump)
        data = plan.model_dump()

        # Verify structure
        assert data["title"] == "Serialization Test"
        assert data["key"] == "C"
        assert "sections" in data
        assert "instruments" in data

        # Convert to JSON string
        json_str = json.dumps(data, indent=2)
        assert "Serialization Test" in json_str

    def test_plan_from_json(self):
        """Test creating plan from JSON."""
        json_data = {
            "title": "JSON Test",
            "duration_seconds": 90,
            "key": "D",
            "key_type": "minor",
            "scale_type": "harmonic_minor",
            "tempo": 110,
            "time_signature": "4/4",
            "form_type": "ternary",
            "sections": [
                {
                    "name": "A",
                    "duration_seconds": 30,
                    "key": "D",
                    "key_type": "minor",
                    "scale_type": "harmonic_minor",
                    "tempo": 110,
                    "time_signature": "4/4"
                }
            ],
            "instruments": [
                {
                    "name": "violin",
                    "section": "strings",
                    "role": "melody",
                    "dynamics": "mf",
                    "midi_program": 40
                }
            ]
        }

        plan = OrchestrationPlan(**json_data)

        assert plan.title == "JSON Test"
        assert plan.key == "D"
        assert plan.scale_type == ScaleType.HARMONIC_MINOR
        assert len(plan.sections) == 1
        assert plan.sections[0].name == "A"
