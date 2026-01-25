"""Unit tests for ruff formatting"""

# Standard libraries
import re
import subprocess

PYLINT_MINIMUM_SCORE = 8.0


def test_ruff_formatting():
    """Test that ruff formatting has been applied"""
    assert subprocess.run("ruff format . --check", shell=True, capture_output=True, check=True)


def test_ruff_check():
    """Test that all ruff fixes have been applied"""
    result = subprocess.run("ruff check . --show-fixes", shell=True, capture_output=True, check=False)
    assert re.search(r"\d+ fixable with the", str(result.stdout)) is None


def test_pylint_score():
    """Test that pylint score is above threshold"""
    subprocess.run(f"pylint --fail-under={PYLINT_MINIMUM_SCORE} .", shell=True, check=True)
