"""
Tests for V4 pattern manipulation system.
"""

from __future__ import annotations

from musicgen.patterns.combinators import (
    aaba,
    cat,
    choose,
    choose_by,
    fastcat,
    from_list,
    overlay,
    range_pattern,
    rot,
    silence,
    spread,
    stack,
    verse_chorus,
    zip_patterns,
)
from musicgen.patterns.parser import PatternParser, parse_pattern
from musicgen.patterns.transform import (
    degrade,
    degrade_by,
    density,
    fast,
    palindrome,
    repeat,
    rev,
    rotate,
    slow,
)
from musicgen.patterns.world_rhythms import (
    BOSSA_NOVA,
    CLAVE_PATTERNS,
    RUPAK,
    SAMBA_ENREDO,
    SON_CLAVE,
    TALAS,
    TEENTAL,
    PolyrhythmGenerator,
    RhythmComposer,
)


class TestPatternParser:
    """Tests for the mini-notation parser."""

    def test_parse_basic_pattern(self) -> None:
        """Test parsing a basic pattern."""
        p = parse_pattern("bd sd sd sd")
        assert len(p.events) == 4
        assert p.events[0].value == "bd"
        assert p.events[1].value == "sd"

    def test_parse_rest(self) -> None:
        """Test parsing rests."""
        p = parse_pattern("bd ~ sd")
        assert len(p.events) == 3
        assert p.events[0].value == "bd"
        assert p.events[1].value == ""
        assert p.events[2].value == "sd"

    def test_parse_repetition(self) -> None:
        """Test parsing repetition."""
        p = parse_pattern("bd*3")
        assert len(p.events) == 3
        assert all(e.value == "bd" for e in p.events)

    def test_parse_euclidean(self) -> None:
        """Test parsing Euclidean rhythm."""
        p = parse_pattern("bd(3,8)")
        assert len(p.events) == 8
        hits = sum(1 for e in p.events if e.value == "bd")
        assert hits == 3

    def test_bjorklund_algorithm(self) -> None:
        """Test Bjorklund algorithm for Euclidean rhythms."""
        parser = PatternParser()

        # 3 hits in 8 steps
        result = parser._bjorklund(3, 8)
        assert len(result) == 8
        assert sum(result) == 3

        # 5 hits in 8 steps
        result = parser._bjorklund(5, 8)
        assert len(result) == 8
        assert sum(result) == 5

        # Edge cases
        assert parser._bjorklund(0, 8) == [False] * 8
        assert parser._bjorklund(8, 8) == [True] * 8


class TestPatternTransform:
    """Tests for pattern transformation functions."""

    def test_slow(self) -> None:
        """Test slowing down a pattern."""
        p = parse_pattern("bd sd")
        slowed = slow(p, 2.0)
        assert len(slowed.events) == 2
        assert slowed.events[0].duration == 2.0
        assert slowed.length == 4.0  # Original 2.0 * 2

    def test_fast(self) -> None:
        """Test speeding up a pattern."""
        p = parse_pattern("bd sd")
        sped = fast(p, 2.0)
        assert len(sped.events) == 2
        assert sped.events[0].duration == 0.5
        assert sped.length == 1.0  # Original 2.0 / 2

    def test_rev(self) -> None:
        """Test reversing a pattern."""
        p = parse_pattern("bd sd hh")
        reversed_p = rev(p)
        assert reversed_p.events[0].value == "hh"
        assert reversed_p.events[1].value == "sd"
        assert reversed_p.events[2].value == "bd"

    def test_palindrome(self) -> None:
        """Test creating a palindrome pattern."""
        p = parse_pattern("bd sd")
        pal = palindrome(p)
        assert len(pal.events) == 4
        assert [e.value for e in pal.events] == ["bd", "sd", "sd", "bd"]

    def test_rotate(self) -> None:
        """Test rotating a pattern."""
        p = parse_pattern("bd sd hh cp")
        rotated = rotate(p, 1)
        assert [e.value for e in rotated.events] == ["cp", "bd", "sd", "hh"]

    def test_repeat(self) -> None:
        """Test repeating a pattern."""
        p = parse_pattern("bd sd")
        repeated = repeat(p, 3)
        assert len(repeated.events) == 6
        assert repeated.length == 6.0

    def test_density(self) -> None:
        """Test changing pattern density."""
        p = parse_pattern("bd sd hh cp")
        dense = density(p, 0.5)
        assert len(dense.events) <= 4  # Some events may be filtered

    def test_degrade(self) -> None:
        """Test degrading a pattern."""
        p = parse_pattern("bd sd hh cp")
        degraded = degrade(p, 0.5)
        assert len(degraded.events) <= 4

    def test_degrade_by(self) -> None:
        """Test degrading with a function."""
        p = parse_pattern("bd sd hh cp")
        # Keep more events at the beginning
        degraded = degrade_by(p, lambda pos: 1.0 - pos)
        assert len(degraded.events) <= 4


class TestPatternCombinators:
    """Tests for pattern combinators."""

    def test_stack(self) -> None:
        """Test layering patterns."""
        p1 = parse_pattern("bd sd")
        p2 = parse_pattern("hh hh")
        stacked = stack(p1, p2)
        assert len(stacked.events) > 0

    def test_cat(self) -> None:
        """Test concatenating patterns."""
        p1 = parse_pattern("bd sd")
        p2 = parse_pattern("hh hh")
        concatenated = cat(p1, p2)
        assert len(concatenated.events) == 4

    def test_fastcat(self) -> None:
        """Test fast-cat concatenation."""
        p1 = parse_pattern("bd")
        p2 = parse_pattern("sd")
        fastcatted = fastcat(p1, p2)
        assert len(fastcatted.events) == 2
        assert fastcatted.events[0].duration == 0.5

    def test_overlay(self) -> None:
        """Test overlaying patterns."""
        base = parse_pattern("bd ~ sd ~")
        overlay_pattern = parse_pattern("~ hh ~ hh")
        overlaid = overlay(base, overlay_pattern)
        assert len(overlaid.events) >= 4

    def test_choose(self) -> None:
        """Test random selection."""
        p = choose(["bd", "sd", "hh"], count=4)
        assert len(p.events) == 4
        assert all(e.value in ["bd", "sd", "hh"] for e in p.events)

    def test_choose_by(self) -> None:
        """Test pattern-based selection."""
        p = parse_pattern("0 1 2 1")
        result = choose_by(p, ["bd", "sd", "hh"])
        assert result.events[0].value == "bd"
        assert result.events[1].value == "sd"
        assert result.events[2].value == "hh"

    def test_from_list(self) -> None:
        """Test creating pattern from list."""
        p = from_list(["bd", "sd", "hh"])
        assert len(p.events) == 3
        assert p.events[0].value == "bd"

    def test_silence(self) -> None:
        """Test creating silence."""
        p = silence(4.0)
        assert p.length == 4.0
        assert len(p.events) == 0

    def test_range_pattern(self) -> None:
        """Test numeric range pattern."""
        p = range_pattern(0, 5)
        assert len(p.events) == 5
        assert p.events[0].value == "0"

    def test_rot(self) -> None:
        """Test rotating a list."""
        result = rot(["a", "b", "c", "d"], 1)
        assert result == ["b", "c", "d", "a"]

    def test_spread(self) -> None:
        """Test spreading values across a cycle."""
        p = spread(["a", "b", "c"], 12)
        assert len(p.events) == 3
        assert p.length == 12

    def test_verse_chorus(self) -> None:
        """Test verse-chorus structure."""
        verse = parse_pattern("bd sd")
        chorus = parse_pattern("bd bd sd sd")
        vc = verse_chorus(verse, chorus, repeats=2)
        assert len(vc.events) == 12  # (2 + 4) * 2

    def test_aaba(self) -> None:
        """Test AABA form."""
        verse = parse_pattern("bd sd")
        bridge = parse_pattern("hh hh")
        aaba_pattern = aaba(verse, bridge)
        assert len(aaba_pattern.events) == 8  # 2+2+2+2

    def test_zip_patterns(self) -> None:
        """Test zipping patterns."""
        p1 = parse_pattern("bd sd")
        p2 = parse_pattern("hh cp")
        zipped = zip_patterns([p1, p2])
        assert len(zipped.events) == 4


class TestWorldRhythms:
    """Tests for world rhythm patterns."""

    def test_son_clave(self) -> None:
        """Test Son clave pattern."""
        assert SON_CLAVE.name == "Son Clave (3-2)"
        assert SON_CLAVE.region == "Cuba"
        # Check combined pattern has hits in expected positions
        hits = [c for c in SON_CLAVE.combined if c.strip() == "x"]
        assert len(hits) == 6  # 3 on the "3" side + 3 on the "2" side (with continuation)

    def test_clave_patterns_registry(self) -> None:
        """Test clave patterns registry."""
        assert "son" in CLAVE_PATTERNS
        assert "rumba" in CLAVE_PATTERNS
        assert "bossa_nova" in CLAVE_PATTERNS

    def test_bossa_nova(self) -> None:
        """Test Bossa Nova pattern."""
        assert BOSSA_NOVA.name == "Bossa Nova"
        assert BOSSA_NOVA.guitar == "x . x . x . x ."

    def test_samba_enredo(self) -> None:
        """Test Samba Enredo pattern."""
        assert SAMBA_ENREDO.name == "Samba Enredo"
        assert SAMBA_ENREDO.surdo_marca == "x . . . . . . ."

    def test_teental(self) -> None:
        """Test Teental tala."""
        assert TEENTAL.name == "Teental (Tintal)"
        assert TEENTAL.matra == 16
        assert len(TEENTAL.vibhag) == 4
        assert all(v == 4 for v in TEENTAL.vibhag)

    def test_rupak(self) -> None:
        """Test Rupak tala."""
        assert RUPAK.name == "Rupak"
        assert RUPAK.matra == 7
        assert RUPAK.vibhag == [3, 2, 2]

    def test_talas_registry(self) -> None:
        """Test talas registry."""
        assert "teental" in TALAS
        assert "rupak" in TALAS
        assert "jhaptal" in TALAS

    def test_polyrhythm_generator(self) -> None:
        """Test polyrhythm generator."""
        gen = PolyrhythmGenerator()
        result = gen.cross_rhythm(3, 2, 6)
        assert "main" in result
        assert "cross" in result
        assert len(result["main"]) == 6

    def test_euclidean_polyrhythm(self) -> None:
        """Test Euclidean polyrhythm."""
        gen = PolyrhythmGenerator()
        result = gen.euclidean_polyrhythm(3, 8, 5, 8)
        assert "pattern1" in result
        assert "pattern2" in result
        assert sum(result["pattern1"]) == 3
        assert sum(result["pattern2"]) == 5

    def test_rhythm_composer_afro_cuban(self) -> None:
        """Test Afro-Cuban rhythm composition."""
        composer = RhythmComposer()
        rhythm = composer.create_afro_cuban("son")
        assert "clave" in rhythm
        assert "congas" in rhythm

    def test_rhythm_composer_brazilian(self) -> None:
        """Test Brazilian rhythm composition."""
        composer = RhythmComposer()
        rhythm = composer.create_brazilian("samba")
        assert "surdo_1" in rhythm
        assert "agogo" in rhythm

    def test_rhythm_composer_indian(self) -> None:
        """Test Indian rhythm composition."""
        composer = RhythmComposer()
        rhythm = composer.create_indian("teental")
        assert "tabla_bayan" in rhythm
        assert "tabla_dayan" in rhythm

    def test_rhythm_composer_middle_eastern(self) -> None:
        """Test Middle Eastern rhythm composition."""
        composer = RhythmComposer()
        rhythm = composer.create_middle_eastern("baladi")
        assert "darbuka_doum" in rhythm

    def test_rhythm_composer_west_african(self) -> None:
        """Test West African rhythm composition."""
        composer = RhythmComposer()
        rhythm = composer.create_west_african("agbadza")
        assert "bell" in rhythm
