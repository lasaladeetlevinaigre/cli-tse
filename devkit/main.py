"""devkit - Modern developer workflow with GitHub CLI."""
import typer
from devkit.commands.github import github_app

app = typer.Typer()

# Add GitHub commands as a subcommand group
app.add_typer(github_app, name='github', help='GitHub CLI commands')


@app.command()
def version():
    """Show devkit version."""
    typer.echo("devkit v0.1.0")


if __name__ == '__main__':
    app()
