"""Shell execution utilities."""

import subprocess
from typing import Any

import typer


def run_command(
    cmd: str | list[str], capture: bool = True, check: bool = True
) -> str:
    """Execute a shell command and return output.

    Args:
        cmd: Command as string or list of arguments
        capture: Whether to capture output
        check: Whether to raise on error

    Returns:
        Command output as string

    Raises:
        subprocess.CalledProcessError: If command fails and check=True
    """
    try:
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, text=True, capture_output=capture, check=check)
        else:
            result = subprocess.run(cmd, text=True, capture_output=capture, check=check)

        return result.stdout.strip() if capture else ""
    except subprocess.CalledProcessError as e:
        if check:
            typer.echo(f"Error running command: {cmd}", err=True)
            typer.echo(f"stderr: {e.stderr}", err=True)
            raise
        return ""


def command_exists(command: str) -> bool:
    """Check if a command exists in PATH."""
    import shutil

    return shutil.which(command) is not None


def require_command(command: str, install_hint: str = "") -> None:
    """Check if a command exists, exit if not.

    Args:
        command: Command name to check
        install_hint: Installation instructions to display
    """
    if not command_exists(command):
        typer.echo(f"Error: '{command}' not found in PATH", err=True)
        if install_hint:
            typer.echo(f"Install with: {install_hint}", err=True)
        else:
            typer.echo(f"Please install '{command}' and try again", err=True)
        raise typer.Exit(1)
