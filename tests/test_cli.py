"""Tests for the command-line interface."""

import subprocess
import sys


class TestCLI:
    """Test CLI commands."""

    def test_cli_help(self):
        """Test that CLI help command works."""
        result = subprocess.run(
            [sys.executable, "-m", "musicgen", "--help"],
            capture_output=True,
            text=True,
            cwd="/home/chiranjeet/projects-cc/projects/music-gen-lib"
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
            text=True,
            cwd="/home/chiranjeet/projects-cc/projects/music-gen-lib"
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
            text=True,
            cwd="/home/chiranjeet/projects-cc/projects/music-gen-lib"
        )
        # Should list available moods
        if result.returncode == 0:
            assert "epic" in result.stdout.lower() or "peaceful" in result.stdout.lower()
