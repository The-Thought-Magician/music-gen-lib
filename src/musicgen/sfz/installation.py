"""Installation checker for SFZ rendering dependencies.

This module provides utilities to check if required dependencies
for SFZ rendering are installed, and provides helpful installation
instructions.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping


class DependencyStatus:
    """Status of a dependency check."""

    def __init__(
        self,
        name: str,
        installed: bool,
        version: str | None = None,
        error: str | None = None,
    ):
        """Initialize dependency status.

        Args:
            name: Name of the dependency
            installed: Whether the dependency is installed
            version: Version string if available
            error: Error message if check failed
        """
        self.name = name
        self.installed = installed
        self.version = version
        self.error = error

    def __str__(self) -> str:
        """Return string representation of status."""
        if self.installed:
            version_str = f" (version {self.version})" if self.version else ""
            return f"[OK] {self.name}{version_str}"
        return f"[MISSING] {self.name}" + (f": {self.error}" if self.error else "")


def check_sfizz_installation() -> Mapping[str, bool | DependencyStatus]:
    """Check if sfizz and related dependencies are installed.

    Checks for:
    - sfizz-render (command-line tool)
    - ffmpeg (for MP3 export)
    - Python packages: pydub, numpy, mido

    Returns:
        Dictionary mapping dependency names to bool or DependencyStatus
    """
    results: dict[str, bool | DependencyStatus] = {}

    # Check sfizz_render
    try:
        result = subprocess.run(
            ["sfizz_render", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            # Try to extract version
            version = "unknown"
            if "sfizz" in result.stdout.lower():
                parts = result.stdout.strip().split()
                for i, part in enumerate(parts):
                    if "version" in part.lower() and i + 1 < len(parts):
                        version = parts[i + 1]
                        break
            results["sfizz-render"] = DependencyStatus("sfizz-render", True, version)
        else:
            results["sfizz-render"] = DependencyStatus(
                "sfizz-render", False, error="Command failed"
            )
    except FileNotFoundError:
        results["sfizz-render"] = DependencyStatus(
            "sfizz-render", False, error="Not found in PATH"
        )
    except subprocess.TimeoutExpired:
        results["sfizz-render"] = DependencyStatus(
            "sfizz-render", False, error="Timeout"
        )
    except Exception as e:
        results["sfizz-render"] = DependencyStatus(
            "sfizz-render", False, error=str(e)
        )

    # Check ffmpeg (for MP3 export)
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            # Extract version
            version = "unknown"
            for line in result.stdout.split("\n"):
                if "ffmpeg version" in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        version = parts[2]
                    break
            results["ffmpeg"] = DependencyStatus("ffmpeg", True, version)
        else:
            results["ffmpeg"] = DependencyStatus("ffmpeg", False, error="Command failed")
    except FileNotFoundError:
        results["ffmpeg"] = DependencyStatus("ffmpeg", False, error="Not found in PATH")
    except subprocess.TimeoutExpired:
        results["ffmpeg"] = DependencyStatus("ffmpeg", False, error="Timeout")
    except Exception as e:
        results["ffmpeg"] = DependencyStatus("ffmpeg", False, error=str(e))

    # Check Python packages
    packages = ["pydub", "numpy", "mido"]

    for package in packages:
        try:
            mod = __import__(package)
            version = getattr(mod, "__version__", None)
            results[package] = DependencyStatus(package, True, version or "installed")
        except ImportError:
            results[package] = DependencyStatus(package, False, error="Not installed")

    return results


def print_installation_instructions() -> None:
    """Print installation instructions for missing dependencies.

    Checks all dependencies and prints helpful installation instructions
    for any that are missing.
    """
    checks = check_sfizz_installation()

    # Check if all are installed
    all_installed = all(
        (isinstance(v, DependencyStatus) and v.installed) or (isinstance(v, bool) and v)
        for v in checks.values()
    )

    if all_installed:
        print("All SFZ rendering dependencies are installed!")
        return

    print("Missing dependencies for SFZ rendering:\n")

    # sfizz-render instructions
    sfizz = checks.get("sfizz-render")
    if isinstance(sfizz, DependencyStatus) and not sfizz.installed:
        print("[sfizz-render]")
        print("  Required for MIDI to audio rendering with SFZ libraries.")
        print()
        if sys.platform == "linux":
            print("  Linux installation:")
            print("    sudo apt install sfizz")
            print("  Or from source:")
            print("    https://github.com/sfztools/sfizz")
        elif sys.platform == "darwin":
            print("  macOS installation:")
            print("    brew install sfizz")
        else:
            print("  Windows installation:")
            print("    Download from: https://github.com/sfztools/sfizz/releases")
        print()

    # ffmpeg instructions
    ffmpeg = checks.get("ffmpeg")
    if isinstance(ffmpeg, DependencyStatus) and not ffmpeg.installed:
        print("[ffmpeg]")
        print("  Required for MP3 export (optional).")
        print()
        if sys.platform == "linux":
            print("  Linux installation:")
            print("    sudo apt install ffmpeg")
        elif sys.platform == "darwin":
            print("  macOS installation:")
            print("    brew install ffmpeg")
        else:
            print("  Windows installation:")
            print("    Download from: https://ffmpeg.org/download.html")
        print()

    # Python packages
    python_packages = ["pydub", "numpy", "mido"]
    missing_packages = [
        p for p in python_packages
        if isinstance(checks.get(p), DependencyStatus) and not checks[p].installed  # type: ignore
    ]

    if missing_packages:
        print("[Python packages]")
        print(f"  Missing: {', '.join(missing_packages)}")
        print()
        print("  Install with:")
        print(f"    pip install {' '.join(missing_packages)}")
        print()
        print("  Or with uv:")
        print(f"    uv pip install {' '.join(missing_packages)}")
        print()


def check_sfz_libraries(
    libraries_root: Path | str = "resources/sfz_libraries",
) -> list[Path]:
    """Check for available SFZ libraries in the given directory.

    Args:
        libraries_root: Root directory to search for SFZ libraries

    Returns:
        List of paths to found SFZ files
    """
    root = Path(libraries_root)

    if not root.exists():
        return []

    sfz_files = list(root.rglob("*.sfz"))
    return sorted(sfz_files)


def print_sfz_library_status(
    libraries_root: Path | str = "resources/sfz_libraries",
) -> None:
    """Print status of SFZ libraries.

    Shows which SFZ files are available in the libraries root.

    Args:
        libraries_root: Root directory to search for SFZ libraries
    """
    root = Path(libraries_root)

    if not root.exists():
        print(f"SFZ libraries directory not found: {root}")
        print("  Create this directory and add your SFZ libraries.")
        return

    sfz_files = check_sfz_libraries(root)

    if not sfz_files:
        print(f"No SFZ files found in: {root}")
        print("  Add SFZ libraries to enable rendering.")
        return

    print(f"Found {len(sfz_files)} SFZ file(s) in {root}:")
    for sfz in sfz_files:
        # Show relative path for readability
        try:
            rel_path = sfz.relative_to(root)
        except ValueError:
            rel_path = sfz
        print(f"  {rel_path}")


def verify_rendering_capability(
    libraries_root: Path | str = "resources/sfz_libraries",
) -> tuple[bool, list[str]]:
    """Verify that the system is capable of SFZ rendering.

    Checks both software dependencies and available SFZ libraries.

    Args:
        libraries_root: Root directory for SFZ libraries

    Returns:
        Tuple of (is_capable, list_of_issues)
    """
    issues = []

    checks = check_sfizz_installation()

    # Check sfizz-render
    sfizz = checks.get("sfizz-render")
    if isinstance(sfizz, DependencyStatus) and not sfizz.installed:
        issues.append("sfizz-render is not installed")

    # Check Python packages
    required_packages = ["numpy", "mido"]
    for package in required_packages:
        pkg = checks.get(package)
        if isinstance(pkg, DependencyStatus) and not pkg.installed:
            issues.append(f"{package} is not installed")

    # Check for SFZ libraries
    root = Path(libraries_root)
    if root.exists():
        sfz_files = check_sfz_libraries(root)
        if not sfz_files:
            issues.append(f"No SFZ files found in {libraries_root}")
    else:
        issues.append(f"SFZ libraries directory does not exist: {libraries_root}")

    return len(issues) == 0, issues


def print_system_status(
    libraries_root: Path | str = "resources/sfz_libraries",
) -> None:
    """Print complete system status for SFZ rendering.

    Shows dependency status and SFZ library availability.

    Args:
        libraries_root: Root directory for SFZ libraries
    """
    print("=" * 60)
    print("SFZ Rendering System Status")
    print("=" * 60)
    print()

    # Dependency status
    print("Dependencies:")
    checks = check_sfizz_installation()
    for name, status in checks.items():
        if isinstance(status, DependencyStatus):
            print(f"  {status}")
        else:
            status_str = "OK" if status else "MISSING"
            print(f"  [{status_str}] {name}")
    print()

    # SFZ library status
    print("SFZ Libraries:")
    print_sfz_library_status(libraries_root)
    print()

    # Overall capability
    is_capable, issues = verify_rendering_capability(libraries_root)
    print("=" * 60)
    if is_capable:
        print("System is ready for SFZ rendering!")
    else:
        print("System is NOT ready for SFZ rendering.")
        print("Issues:")
        for issue in issues:
            print(f"  - {issue}")
        print()
        print("Run print_installation_instructions() for help.")
    print("=" * 60)


def get_installation_command(
    package: str,
    use_uv: bool = True,
) -> str | None:
    """Get the installation command for a package.

    Args:
        package: Package name to install
        use_uv: Prefer uv over pip if available

    Returns:
        Installation command string or None if not applicable
    """
    if package in ["sfizz-render", "ffmpeg"]:
        # These are system packages
        if sys.platform == "linux":
            return f"sudo apt install {package}"
        elif sys.platform == "darwin":
            return f"brew install {package}"
        return None

    # Python packages
    if use_uv and shutil.which("uv"):
        return f"uv pip install {package}"
    return f"pip install {package}"
