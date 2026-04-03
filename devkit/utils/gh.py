"""GitHub CLI wrapper utilities."""
import subprocess
import json
from typing import Any


def gh(*args: str) -> str:
    """Run a gh command and return stdout as string.
    
    Args:
        *args: Command arguments to pass to gh
        
    Returns:
        str: The stdout output stripped of whitespace
        
    Raises:
        subprocess.CalledProcessError: If gh command fails
    """
    result = subprocess.run(
        ['gh', *args],
        capture_output=True, 
        text=True, 
        check=True
    )
    return result.stdout.strip()


def gh_json(*args: str) -> Any:
    """Run a gh command with --json and parse result.
    
    Args:
        *args: Command arguments to pass to gh
        
    Returns:
        Any: Parsed JSON output (list or dict)
    """
    raw = gh(*args)
    return json.loads(raw) if raw else []
