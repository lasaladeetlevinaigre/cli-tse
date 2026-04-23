"""AI commands for devkit."""

import subprocess
from typing import Optional

import typer

from devkit.config import get_global_config
from devkit.utils import gh_copilot, gh_json, print_error, print_info, print_panel

ai_app = typer.Typer(help="AI-powered commands")


@ai_app.command()
def explain(
    command: str = typer.Argument(..., help="Shell command to explain"),
) -> None:
    """Explain a shell command using GitHub Copilot."""
    try:
        result = gh_copilot("explain", command)
        print_panel("Command Explanation", result, style="cyan")
    except Exception as e:
        print_error(f"Failed to explain command: {e}")
        raise typer.Exit(1)


@ai_app.command()
def suggest(
    task: str = typer.Argument(..., help="Task description"),
) -> None:
    """Get AI suggestions for a task using GitHub Copilot."""
    try:
        result = gh_copilot("suggest", task)
        print_panel("Suggestions", result, style="yellow")
    except Exception as e:
        print_error(f"Failed to get suggestions: {e}")
        raise typer.Exit(1)


@ai_app.command()
def review(
    pr_number: int = typer.Argument(..., help="Pull request number"),
    repo: Optional[str] = typer.Option(None, help="Repository (owner/repo)"),
) -> None:
    """Get AI review of a PR diff."""
    try:
        from devkit.utils import gh

        args = ["pr", "diff", str(pr_number)]
        if repo:
            args.extend(["--repo", repo])

        diff = gh(args)

        if not diff:
            print_error("No diff found for PR")
            raise typer.Exit(1)

        # Truncate large diffs for AI processing
        if len(diff) > 5000:
            diff = diff[:5000] + "\n... (truncated)"

        # Create a prompt for AI review
        prompt = f"Review this code diff and provide feedback:\n\n{diff}"

        # Use Copilot for review (gh copilot doesn't have direct review, so we simulate)
        result = gh_copilot("suggest", prompt)
        print_panel(f"PR #{pr_number} Review", result, style="green")

    except Exception as e:
        print_error(f"Failed to review PR: {e}")
        raise typer.Exit(1)


@ai_app.command()
def commit(
    staged_only: bool = typer.Option(True, "--staged", help="Use only staged changes"),
) -> None:
    """Generate a commit message for staged changes."""
    try:
        # Get staged diff
        try:
            if staged_only:
                diff_output = subprocess.run(
                    ["git", "diff", "--cached"], capture_output=True, text=True, check=True
                )
            else:
                diff_output = subprocess.run(
                    ["git", "diff"], capture_output=True, text=True, check=True
                )

            diff = diff_output.stdout
        except subprocess.CalledProcessError as e:
            print_error("Failed to get git diff")
            raise typer.Exit(1)

        if not diff:
            print_error("No changes to commit")
            raise typer.Exit(1)

        # Truncate large diffs
        if len(diff) > 3000:
            diff = diff[:3000] + "\n... (truncated)"

        prompt = (
            f"Generate a concise, professional git commit message for these changes. "
            f"Follow conventional commits. Just return the message.\n\n{diff}"
        )

        result = gh_copilot("suggest", prompt)

        print_panel("Suggested Commit Message", result, style="blue")

        # Ask user to confirm
        confirm = typer.confirm("Commit with this message?")

        if confirm:
            subprocess.run(["git", "commit", "-m", result.strip()], check=True)
            print_info("Commit created")
        else:
            print_info("Commit cancelled")

    except Exception as e:
        print_error(f"Failed to generate commit message: {e}")
        raise typer.Exit(1)
