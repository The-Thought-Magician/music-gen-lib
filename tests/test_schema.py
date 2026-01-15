"""Test schema generation."""

from musicgen.schema import SchemaGenerator, SchemaConfig, get_schema


def test_schema_generation():
    """Test basic schema generation."""
    schema = get_schema()
    assert schema is not None
    assert "composition" in schema
    assert "note" in schema
    assert "part" in schema
    assert "music_theory" in schema


def test_schema_config():
    """Test schema with custom configuration."""
    config = SchemaConfig(
        include_articulation=False,
        include_dynamics=False,
    )
    gen = SchemaGenerator(config)
    schema = gen.generate()

    # Verify config is reflected
    assert "articulation" not in schema or "articulation (optional)" in schema


def test_schema_save():
    """Test saving schema to file."""
    import tempfile
    from pathlib import Path

    gen = SchemaGenerator()

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "schema.yaml"
        gen.save(path)
        assert path.exists()
        content = path.read_text()
        assert "composition" in content
