"""SoundFont management for audio synthesis.

This module handles downloading, caching, and managing SoundFont files
for use with FluidSynth audio synthesis.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

# SoundFont URLs
GENERAL_USER_GS_URL = "https://schristiancollins.com/generaluser/GeneralUser-GS-v1.471.sf2"
GENERAL_USER_GS_MD5 = "53bb9f8b5855e93e5c592a8920bc5d33"  # Approximate MD5

# Default paths
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "musicgen"
PROJECT_SOUNDFONT_DIR = Path(__file__).parent.parent.parent.parent / "resources" / "soundfonts"


class SoundFontManager:
    """Manages SoundFont files for audio synthesis."""

    def __init__(self, cache_dir: Path | None = None):
        """Initialize the SoundFont manager.

        Args:
            cache_dir: Directory for caching SoundFonts. Defaults to ~/.cache/musicgen
        """
        self.cache_dir = cache_dir or DEFAULT_CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Ensure project directory exists
        PROJECT_SOUNDFONT_DIR.mkdir(parents=True, exist_ok=True)

    def get_soundfont_path(self, name: str = "GeneralUser-GS") -> Path | None:
        """Get the path to a SoundFont file.

        Searches in order:
        1. Project resources/soundfonts directory
        2. Cache directory
        3. System FluidSynth default locations

        Args:
            name: Name of the SoundFont (without extension)

        Returns:
            Path to the SoundFont file, or None if not found
        """
        filename = f"{name}.sf2"

        # Check project directory
        project_path = PROJECT_SOUNDFONT_DIR / filename
        if project_path.exists():
            return project_path

        # Check cache directory
        cache_path = self.cache_dir / filename
        if cache_path.exists():
            return cache_path

        # Check system locations
        system_paths = [
            Path("/usr/share/sounds/sf2") / filename,
            Path("/usr/share/soundfonts") / filename,
            Path("/usr/local/share/soundfonts") / filename,
            Path("/opt/soundfonts") / filename,
        ]
        for system_path in system_paths:
            if system_path.exists():
                return system_path

        return None

    def download_soundfont(
        self,
        url: str = GENERAL_USER_GS_URL,
        name: str = "GeneralUser-GS-v1.471",
        force: bool = False
    ) -> Path:
        """Download a SoundFont file.

        Args:
            url: URL to download from
            name: Name to save as (without extension)
            force: Force re-download even if file exists

        Returns:
            Path to the downloaded file

        Raises:
            RuntimeError: If download fails
        """
        filename = f"{name}.sf2"
        target_path = self.cache_dir / filename

        if target_path.exists() and not force:
            return target_path

        # Try using wget
        try:
            result = subprocess.run(
                ["wget", "-O", str(target_path), url],
                check=True,
                capture_output=True,
                text=True
            )
            return target_path
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Try using curl
        try:
            result = subprocess.run(
                ["curl", "-L", "-o", str(target_path), url],
                check=True,
                capture_output=True,
                text=True
            )
            return target_path
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Use Python as fallback
        try:
            import urllib.request
            urllib.request.urlretrieve(url, target_path)
            return target_path
        except Exception as e:
            raise RuntimeError(f"Failed to download SoundFont: {e}")

    def ensure_soundfont(self, name: str = "GeneralUser-GS") -> Path:
        """Ensure a SoundFont is available, downloading if necessary.

        Args:
            name: Name of the SoundFont

        Returns:
            Path to the SoundFont file

        Raises:
            RuntimeError: If SoundFont cannot be obtained
        """
        path = self.get_soundfont_path(name)

        if path is None:
            # Try to download
            path = self.download_soundfont()

            # Copy to project directory
            project_path = PROJECT_SOUNDFONT_DIR / path.name
            shutil.copy2(path, project_path)
            path = project_path

        return path

    def list_available(self) -> list[str]:
        """List all available SoundFont files.

        Returns:
            List of SoundFont names (without .sf2 extension)
        """
        soundfonts = []

        for directory in [PROJECT_SOUNDFONT_DIR, self.cache_dir]:
            if directory.exists():
                for sf2 in directory.glob("*.sf2"):
                    name = sf2.stem
                    if name not in soundfonts:
                        soundfonts.append(name)

        return sorted(soundfonts)

    def check_fluidsynth(self) -> bool:
        """Check if FluidSynth is available on the system.

        Returns:
            True if FluidSynth is available
        """
        try:
            subprocess.run(
                ["fluidsynth", "--version"],
                check=True,
                capture_output=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


# Global singleton
_default_manager: SoundFontManager | None = None


def get_soundfont_manager() -> SoundFontManager:
    """Get the global SoundFont manager instance."""
    global _default_manager
    if _default_manager is None:
        _default_manager = SoundFontManager()
    return _default_manager


def get_default_soundfont() -> Path | None:
    """Get the default SoundFont path."""
    return get_soundfont_manager().get_soundfont_path()


def ensure_soundfont() -> Path:
    """Ensure the default SoundFont is available."""
    return get_soundfont_manager().ensure_soundfont()
