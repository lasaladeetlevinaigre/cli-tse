"""Rich display utilities for devkit."""

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

console = Console()


def print_table(
    title: str, headers: list[str], rows: list[list[str]], max_width: int | None = None
) -> None:
    """Print a formatted table using Rich.

    Args:
        title: Table title
        headers: Column headers
        rows: List of row data (each row is a list matching header count)
        max_width: Optional max width for columns
    """
    table = Table(title=title)

    for header in headers:
        table.add_column(header)

    for row in rows:
        table.add_row(*row)

    console.print(table)


def print_panel(title: str, text: str, style: str = "blue") -> None:
    """Print a formatted panel using Rich.

    Args:
        title: Panel title
        text: Panel content
        style: Panel style (color)
    """
    panel = Panel(text, title=title, style=style, expand=False)
    console.print(panel)


def print_success(text: str) -> None:
    """Print success message."""
    console.print(f"[green]✓[/green] {text}")


def print_error(text: str) -> None:
    """Print error message."""
    console.print(f"[red]✗[/red] {text}")


def print_info(text: str) -> None:
    """Print info message."""
    console.print(f"[cyan]ℹ[/cyan] {text}")


def print_warning(text: str) -> None:
    """Print warning message."""
    console.print(f"[yellow]⚠[/yellow] {text}")


def print_spinner(text: str) -> Spinner:
    """Create a spinner for long operations."""
    return Spinner("dots", text=text)
