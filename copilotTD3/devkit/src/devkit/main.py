"""Main CLI app for devkit."""

import typer
from rich.console import Console
from rich.panel import Panel

from devkit.commands import ai_app, workflow_app
from devkit.commands.github import github_app
from devkit.config import get_global_config

console = Console()
app = typer.Typer(help="devkit - Modern Developer Workflow CLI")

# Add subcommands
app.add_typer(github_app, name="github", help="GitHub CLI commands")
app.add_typer(ai_app, name="ai", help="AI-powered commands")
app.add_typer(workflow_app, name="workflow", help="Workflow automation")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, version: bool = typer.Option(None, "--version", help="Show version")) -> None:
    """devkit - Modern Developer Workflow CLI.

    Orchestrates GitHub, Copilot, Gemini, and Claude for seamless development.
    """
    if version:
        console.print("[cyan]devkit[/cyan] version [green]0.1.0[/green]")
        raise typer.Exit()

    # Show welcome panel if no subcommand
    if ctx.invoked_subcommand is None:
        welcome = Panel(
            "[bold cyan]Welcome to devkit[/bold cyan]\n\n"
            "Your modern developer workflow CLI.\n\n"
            "[bold]Quick Start:[/bold]\n"
            "  [cyan]devkit gh issues[/cyan]           - List GitHub issues\n"
            "  [cyan]devkit ai explain[/cyan] '<cmd>'  - Explain a command\n"
            "  [cyan]devkit workflow feature-start[/cyan] <name> - Start feature\n\n"
            "[bold]Use[/bold] [cyan]devkit --help[/cyan] [bold]for more options[/bold]",
            title="devkit",
            expand=False,
        )
        console.print(welcome)


if __name__ == "__main__":
    app()
