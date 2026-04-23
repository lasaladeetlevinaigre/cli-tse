"""Workflow automation commands for devkit."""

import subprocess
from typing import Optional

import typer

from devkit.utils import gh, gh_copilot, gh_json, print_error, print_info

workflow_app = typer.Typer(help="Workflow automation")


@workflow_app.command()
def feature_start(
    name: str = typer.Argument(..., help="Feature name"),
    issue: Optional[int] = typer.Option(None, "--issue", "-i", help="Link to GitHub issue"),
    repo: Optional[str] = typer.Option(None, help="Repository (owner/repo)"),
) -> None:
    """Start a new feature with branch, PR, and optional implementation plan."""
    try:
        branch_name = f"feature/{name}"

        # Step 1: Create and push branch
        print_info(f"Creating branch: {branch_name}")
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)

        # Step 2: Create draft PR
        print_info("Creating draft PR")
        args = [
            "pr",
            "create",
            "--draft",
            "--title",
            f"feat: {name}",
            "--body",
            "# Feature Implementation\n\n(To be updated with implementation details)",
        ]

        if repo:
            args.extend(["--repo", repo])

        pr_url = gh(args)
        print_info(f"Draft PR created: {pr_url}")

        # Step 3: If issue provided, generate implementation plan
        if issue:
            print_info(f"Fetching issue #{issue}")

            issue_args = ["issue", "view", str(issue), "--json", "title,body"]
            if repo:
                issue_args.extend(["--repo", repo])

            issue_data = gh_json(issue_args)

            if isinstance(issue_data, dict):
                issue_title = issue_data.get("title", "")
                issue_body = issue_data.get("body", "")

                # Generate implementation plan using AI
                prompt = f"Generate a concise implementation plan for this issue:\n\nTitle: {issue_title}\n\nBody: {issue_body}"

                print_info("Generating implementation plan with AI")
                plan = gh_copilot("suggest", prompt)

                # Update PR with plan
                subprocess.run(
                    [
                        "gh",
                        "pr",
                        "edit",
                        "-b",
                        f"# Feature Implementation\n\nLinked Issue: #{issue}\n\n## Plan\n\n{plan}",
                    ],
                    check=True,
                )

                print_info("PR updated with implementation plan")

        print_info(f"✓ Feature '{name}' is ready to develop")

    except subprocess.CalledProcessError as e:
        print_error(f"Failed to start feature: {e}")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(1)
