"""GitHub commands for devkit."""

import json
from typing import Optional

import typer

from devkit.utils import gh, gh_json, print_error, print_info, print_panel, print_table

github_app = typer.Typer(help="GitHub operations")


@github_app.command()
def issues(
    repo: Optional[str] = typer.Option(None, help="Repository (owner/repo)"),
    limit: int = typer.Option(10, help="Number of issues to show"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode with fzf"),
    state: str = typer.Option("open", help="Issue state (open, closed, all)"),
) -> None:
    """List issues in a repository."""
    try:
        args = ["issue", "list", "--limit", str(limit), "--state", state]

        if repo:
            args.extend(["--repo", repo])

        if interactive:
            try:
                import subprocess

                result = gh(args + ["--json", "number,title,state,labels"])
                # Pipe to fzf if available
                proc = subprocess.run(
                    ["fzf", "--preview", "gh issue view {1}"], input=result, text=True
                )
            except FileNotFoundError:
                print_error("fzf not found. Install it for interactive mode.")
                return

        data = gh_json(args)

        if not data:
            print_info("No issues found")
            return

        headers = ["Number", "Title", "State", "Labels"]
        rows = []

        for issue in data:
            labels = ", ".join([l.get("name", "") for l in issue.get("labels", [])])
            rows.append(
                [
                    str(issue.get("number", "")),
                    issue.get("title", "")[:50],
                    issue.get("state", ""),
                    labels,
                ]
            )

        print_table("Issues", headers, rows)

    except Exception as e:
        print_error(f"Failed to list issues: {e}")
        raise typer.Exit(1)


@github_app.command()
def pr_summary(
    pr_number: int = typer.Argument(..., help="Pull request number"),
    repo: Optional[str] = typer.Option(None, help="Repository (owner/repo)"),
) -> None:
    """Show PR title, body, and summary."""
    try:
        args = ["pr", "view", str(pr_number), "--json", "number,title,body,state,additions,deletions"]

        if repo:
            args.extend(["--repo", repo])

        data = gh_json(args)

        if isinstance(data, dict):
            title = data.get("title", "N/A")
            body = data.get("body", "N/A")[:300]
            state = data.get("state", "N/A")
            additions = data.get("additions", 0)
            deletions = data.get("deletions", 0)

            panel_text = f"[bold]{title}[/bold]\n\n{body}\n\n"
            panel_text += f"[cyan]State:[/cyan] {state}\n"
            panel_text += f"[green]+{additions}[/green] [red]-{deletions}[/red]"

            print_panel(f"PR #{pr_number}", panel_text, style="green")
        else:
            print_error("Failed to parse PR data")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"Failed to get PR summary: {e}")
        raise typer.Exit(1)


@github_app.command()
def start_feature(
    name: str = typer.Argument(..., help="Feature branch name"),
    repo: Optional[str] = typer.Option(None, help="Repository (owner/repo)"),
) -> None:
    """Create a feature branch."""
    try:
        import subprocess

        branch_name = f"feature/{name}"

        # Get current branch to create from main/master
        result = subprocess.run(["git", "branch", "-a"], capture_output=True, text=True, check=True)

        # Create and push branch
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)

        print_info(f"Created and pushed branch: {branch_name}")

    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create feature branch: {e}")
        raise typer.Exit(1)


@github_app.command()
def open_pr(
    title: Optional[str] = typer.Option(None, help="PR title"),
    body: Optional[str] = typer.Option(None, help="PR body/description"),
    draft: bool = typer.Option(False, "--draft", help="Create as draft"),
    repo: Optional[str] = typer.Option(None, help="Repository (owner/repo)"),
) -> None:
    """Create a pull request."""
    try:
        args = ["pr", "create"]

        if title:
            args.extend(["--title", title])

        if body:
            args.extend(["--body", body])

        if draft:
            args.append("--draft")

        if repo:
            args.extend(["--repo", repo])

        result = gh(args)
        print_info(f"Pull request created: {result}")

    except Exception as e:
        print_error(f"Failed to create PR: {e}")
        raise typer.Exit(1)


@github_app.command()
def run_status(
    repo: Optional[str] = typer.Option(None, help="Repository (owner/repo)"),
) -> None:
    """Show CI/workflow run status."""
    try:
        args = ["run", "list", "--limit", "10"]

        if repo:
            args.extend(["--repo", repo])

        data = gh_json(args)

        if not data:
            print_info("No workflow runs found")
            return

        headers = ["Run ID", "Name", "Status", "Conclusion"]
        rows = []

        for run in data[:10]:
            rows.append(
                [
                    str(run.get("databaseId", ""))[:8],
                    run.get("name", "")[:30],
                    run.get("status", ""),
                    run.get("conclusion", "") or "pending",
                ]
            )

        print_table("Workflow Runs", headers, rows)

    except Exception as e:
        print_error(f"Failed to get run status: {e}")
        raise typer.Exit(1)
