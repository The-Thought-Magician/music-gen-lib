"""
Tests for V4 world music scales and genre profiles.
"""

from __future__ import annotations

from musicgen.genres.profiles import (
    CLASSICAL,
    ELECTRONIC,
    GENRE_PROFILES,
    JAZZ,
    POP,
    ROCK,
    WORLD,
    GenreProfile,
    get_all_genres,
    get_genre_profile,
    get_genres_by_tempo,
)
from musicgen.scales.arabic import (
    ARABIC_MAQAMAT,
    MAQAM_BAYATI,
    MAQAM_HIJAZ,
    MAQAM_RAST,
    MAQAM_SIKAH,
    get_maqam_by_name,
)
from musicgen.scales.indian import (
    INDIAN_RAGAS,
    RAGA_BHAIRAV,
    RAGA_BHAIRAVI,
    RAGA_TODI,
    RAGA_YAMAN,
    get_raga_by_name,
    get_ragas_by_that,
)
from musicgen.scales.japanese import (
    JAPANESE_SCALES,
    SCALE_HIRAJOUSHI,
    SCALE_IN_SENPOU,
    SCALE_KUMOI,
    SCALE_MIYAKOBUCHI,
)
from musicgen.scales.pentatonic import (
    PENTATONIC_SCALES,
    SCALE_BLUES,
    SCALE_MAJOR_PENTATONIC,
    SCALE_MINOR_PENTATONIC,
    get_pentatonic_scale,
)


class TestIndianScales:
    """Tests for Indian raga scale definitions."""

    def test_raga_yaman(self) -> None:
        """Test Yaman raga."""
        assert RAGA_YAMAN.name == "Yaman"
        assert RAGA_YAMAN.that == "Kalyan"
        assert len(RAGA_YAMAN.aroha) > 0  # Ascending scale
        assert len(RAGA_YAMAN.avaroha) > 0  # Descending scale

    def test_raga_bhairavi(self) -> None:
        """Test Bhairavi raga."""
        assert RAGA_BHAIRAVI.name == "Bhairavi"
        assert RAGA_BHAIRAVI.that == "Bhairavi"

    def test_raga_bhairav(self) -> None:
        """Test Bhairav raga."""
        assert RAGA_BHAIRAV.name == "Bhairav"
        assert RAGA_BHAIRAV.that == "Bhairav"

    def test_raga_todi(self) -> None:
        """Test Todi raga."""
        assert RAGA_TODI.name == "Todi"
        assert RAGA_TODI.thaat == "Todi"

    def test_indian_ragas_registry(self) -> None:
        """Test Indian ragas registry."""
        assert len(INDIAN_RAGAS) > 0
        assert "yaman" in INDIAN_RAGAS
        assert "bhairavi" in INDIAN_RAGAS

    def test_get_raga_by_name(self) -> None:
        """Test getting raga by name."""
        raga = get_raga_by_name("yaman")
        assert raga is not None
        assert raga.name == "Yaman"

    def test_get_ragas_by_that(self) -> None:
        """Test filtering ragas by that."""
        kalyan_ragas = get_ragas_by_that("Kalyan")
        # Yaman should be in Kalyan that
        assert any(r.name == "Yaman" for r in kalyan_ragas)


class TestArabicScales:
    """Tests for Arabic maqam scale definitions."""

    def test_maqam_hijaz(self) -> None:
        """Test Hijaz maqam."""
        assert MAQAM_HIJAZ.name == "Hijaz"
        assert MAQAM_HIJAZ.family == "Sikah"
        assert len(MAQAM_HIJAZ.ajnas) > 0

    def test_maqam_rast(self) -> None:
        """Test Rast maqam."""
        assert MAQAM_RAST.name == "Rast"
        assert MAQAM_RAST.family == "Rast"

    def test_maqam_bayati(self) -> None:
        """Test Bayati maqam."""
        assert MAQAM_BAYATI.name == "Bayati"
        assert MAQAM_BAYATI.family == "Rast"

    def test_maqam_sikah(self) -> None:
        """Test Sikah maqam."""
        assert MAQAM_SIKAH.name == "Sikah"
        assert MAQAM_SIKAH.family == "Sikah"

    def test_arabic_maqamat_registry(self) -> None:
        """Test Arabic maqamat registry."""
        assert len(ARABIC_MAQAMAT) > 0
        assert "hijaz" in ARABIC_MAQAMAT
        assert "rast" in ARABIC_MAQAMAT

    def test_get_maqam_by_name(self) -> None:
        """Test getting maqam by name."""
        maqam = get_maqam_by_name("hijaz")
        assert maqam is not None
        assert maqam.name == "Hijaz"


class TestJapaneseScales:
    """Tests for Japanese scale definitions."""

    def test_hirajoushi_scale(self) -> None:
        """Test Hirajoushi scale."""
        assert SCALE_HIRAJOUSHI.name == "Hirajoushi"
        assert len(SCALE_HIRAJOUSHI.intervals) > 0

    def test_in_senpou_scale(self) -> None:
        """Test In-senpou scale."""
        assert SCALE_IN_SENPOU.name == "In-senpou"
        assert len(SCALE_IN_SENPOU.intervals) > 0

    def test_kumoi_scale(self) -> None:
        """Test Kumoi scale."""
        assert SCALE_KUMOI.name == "Kumoi"
        assert len(SCALE_KUMOI.intervals) > 0

    def test_miyakobushi_scale(self) -> None:
        """Test Miyakobushi scale."""
        assert SCALE_MIYAKOBUCHI.name == "Miyakobushi"
        assert len(SCALE_MIYAKOBUCHI.intervals) > 0

    def test_japanese_scales_registry(self) -> None:
        """Test Japanese scales registry."""
        assert len(JAPANESE_SCALES) > 0
        assert "hirajoushi" in JAPANESE_SCALES
        assert "in_senpou" in JAPANESE_SCALES


class TestPentatonicScales:
    """Tests for pentatonic scale definitions."""

    def test_major_pentatonic(self) -> None:
        """Test major pentatonic scale."""
        assert SCALE_MAJOR_PENTATONIC.name == "Major Pentatonic"
        assert len(SCALE_MAJOR_PENTATONIC.intervals) == 5

    def test_minor_pentatonic(self) -> None:
        """Test minor pentatonic scale."""
        assert SCALE_MINOR_PENTATONIC.name == "Minor Pentatonic"
        assert len(SCALE_MINOR_PENTATONIC.intervals) == 5

    def test_blues_scale(self) -> None:
        """Test blues scale."""
        assert SCALE_BLUES.name == "Blues"
        assert len(SCALE_BLUES.intervals) == 6  # Blues has 6 notes

    def test_pentatonic_scales_registry(self) -> None:
        """Test pentatonic scales registry."""
        assert len(PENTATONIC_SCALES) > 0
        assert "major" in PENTATONIC_SCALES
        assert "minor" in PENTATONIC_SCALES

    def test_get_pentatonic_scale(self) -> None:
        """Test getting pentatonic scale by type."""
        scale = get_pentatonic_scale("major", root="C")
        assert scale is not None


class TestGenreProfiles:
    """Tests for genre profile definitions."""

    def test_rock_profile(self) -> None:
        """Test rock genre profile."""
        assert ROCK.name == "Rock"
        assert 100 <= ROCK.tempo_range[0] <= 140
        assert 100 <= ROCK.tempo_range[1] <= 200
        assert (4, 4) in ROCK.time_signatures
        assert "rhythm" in ROCK.instruments
        assert "drums" in ROCK.instruments
        assert len(ROCK.chord_progressions) > 0

    def test_pop_profile(self) -> None:
        """Test pop genre profile."""
        assert POP.name == "Pop"
        assert 90 <= POP.tempo_range[0] <= 130
        assert "verse_chorus" in POP.forms
        # Pop progression I-V-vi-IV should be present
        assert ["I", "V", "vi", "IV"] in POP.chord_progressions

    def test_jazz_profile(self) -> None:
        """Test jazz genre profile."""
        assert JAZZ.name == "Jazz"
        assert 80 <= JAZZ.tempo_range[0] <= 200
        assert "aaba" in JAZZ.forms
        assert "swing_basic" in JAZZ.drum_patterns
        # ii-V-I progression should be present
        has_ii_v_i = any(
            "ii7" in prog and "V7" in prog and "I" in prog for prog in JAZZ.chord_progressions
        )
        assert has_ii_v_i

    def test_classical_profile(self) -> None:
        """Test classical genre profile."""
        assert CLASSICAL.name == "Classical"
        assert 40 <= CLASSICAL.tempo_range[0] <= 180
        assert "sonata" in CLASSICAL.forms
        assert "rondo" in CLASSICAL.forms
        assert (3, 4) in CLASSICAL.time_signatures

    def test_electronic_profile(self) -> None:
        """Test electronic genre profile."""
        assert ELECTRONIC.name == "Electronic"
        assert 120 <= ELECTRONIC.tempo_range[0] <= 180
        assert "four_on_floor" in ELECTRONIC.drum_patterns
        assert "synth_lead_square" in ELECTRONIC.instruments.get("lead", [])

    def test_world_profile(self) -> None:
        """Test world genre profile."""
        assert WORLD.name == "World"
        assert "indian" in WORLD.instruments
        assert "middle_eastern" in WORLD.instruments
        assert "east_asian" in WORLD.instruments
        assert "latin" in WORLD.instruments

    def test_genre_profiles_registry(self) -> None:
        """Test genre profiles registry."""
        assert len(GENRE_PROFILES) == 6
        assert "rock" in GENRE_PROFILES
        assert "pop" in GENRE_PROFILES
        assert "jazz" in GENRE_PROFILES
        assert "classical" in GENRE_PROFILES
        assert "electronic" in GENRE_PROFILES
        assert "world" in GENRE_PROFILES

    def test_get_genre_profile(self) -> None:
        """Test getting genre profile by name."""
        profile = get_genre_profile("rock")
        assert profile is not None
        assert profile.name == "Rock"

        # Test case insensitivity
        profile_lower = get_genre_profile("JAZZ")
        if profile_lower:
            assert profile_lower.name == "Jazz"

    def test_get_all_genres(self) -> None:
        """Test getting all genre names."""
        genres = get_all_genres()
        assert len(genres) == 6
        assert "rock" in genres

    def test_get_genres_by_tempo(self) -> None:
        """Test filtering genres by tempo."""
        # At 120 BPM, should get rock, pop, electronic, jazz
        genres_120 = get_genres_by_tempo(120)
        assert len(genres_120) >= 2

        # At 180 BPM, should get electronic, jazz
        genres_180 = get_genres_by_tempo(180)
        assert len(genres_180) >= 1

    def test_genre_profile_structure(self) -> None:
        """Test GenreProfile dataclass structure."""
        profile = GenreProfile(
            name="Test",
            tempo_range=(100, 120),
            time_signatures=[(4, 4), (3, 4)],
            instruments={"rhythm": ["guitar"]},
            drum_patterns=["basic"],
            bass_patterns=["root_eighth"],
            chord_progressions=[["I", "V", "vi", "IV"]],
            forms=["verse_chorus"],
        )
        assert profile.name == "Test"
        assert profile.tempo_range == (100, 120)
        assert len(profile.time_signatures) == 2
