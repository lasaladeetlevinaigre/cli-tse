"""Basic tests for devkit utilities."""

import pytest
from devkit.utils import command_exists


def test_command_exists_with_valid_command() -> None:
    """Test that command_exists returns True for existing commands."""
    assert command_exists("python")
    assert command_exists("pip")


def test_command_exists_with_invalid_command() -> None:
    """Test that command_exists returns False for non-existent commands."""
    assert not command_exists("nonexistent_command_xyz")


def test_config_loading() -> None:
    """Test configuration loading."""
    from devkit.config import Config

    config = Config()
    assert config.ai_tool == "claude"
    assert config.show_spinner is True
