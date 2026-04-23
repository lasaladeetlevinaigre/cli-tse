"""GitHub CLI wrapper utilities."""

import json
from typing import Any

import typer

from .shell import require_command, run_command


def gh(args: str | list[str]) -> str:
    """Execute a gh command and return raw output.

    Args:
        args: Arguments to gh command

    Returns:
        Raw command output
    """
    require_command("gh", "brew install gh")

    if isinstance(args, list):
        cmd = ["gh"] + args
    else:
        cmd = f"gh {args}"

    return run_command(cmd)


def gh_json(args: str | list[str]) -> dict[str, Any] | list[Any]:
    """Execute a gh command with --json flag and return parsed JSON.

    Args:
        args: Arguments to gh command (--json will be appended if not present)

    Returns:
        Parsed JSON response

    Raises:
        json.JSONDecodeError: If output is not valid JSON
    """
    if isinstance(args, list):
        if "--json" not in args:
            args = args + ["--json"]
        output = gh(args)
    else:
        if "--json" not in args:
            args = f"{args} --json"
        output = gh(args)

    if not output:
        return []

    return json.loads(output)


def gh_copilot(subcommand: str, prompt: str = "") -> str:
    """Execute a gh copilot command.

    Args:
        subcommand: Copilot subcommand (explain, suggest)
        prompt: Input prompt for the copilot

    Returns:
        Copilot response
    """
    require_command("gh", "brew install gh")

    if prompt:
        cmd = f"gh copilot {subcommand} \"{prompt}\""
    else:
        cmd = f"gh copilot {subcommand}"

    return run_command(cmd)
