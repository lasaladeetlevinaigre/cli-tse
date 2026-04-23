"""Configuration management for devkit."""

import json
from pathlib import Path
from typing import Any

import typer
from pydantic import BaseModel


class Config(BaseModel):
    """Configuration model."""

    model_config = {"extra": "allow"}

    ai_tool: str = "claude"
    default_repo: str = ""
    theme: str = "dark"
    show_spinner: bool = True


def get_config_path() -> Path:
    """Get configuration file path."""
    config_dir = Path.home() / ".devkit"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.json"


def load_config() -> Config:
    """Load configuration from ~/.devkit/config.json or use defaults."""
    config_path = get_config_path()

    if config_path.exists():
        try:
            data = json.loads(config_path.read_text())
            return Config(**data)
        except (json.JSONDecodeError, ValueError) as e:
            typer.echo(f"Warning: Invalid config file, using defaults: {e}", err=True)
            return Config()

    return Config()


def save_config(config: Config) -> None:
    """Save configuration to ~/.devkit/config.json."""
    config_path = get_config_path()
    config_path.write_text(json.dumps(config.model_dump(), indent=2))
    typer.echo(f"Configuration saved to {config_path}")


# Global config instance
_config: Config | None = None


def get_global_config() -> Config:
    """Get or initialize global config."""
    global _config
    if _config is None:
        _config = load_config()
    return _config
