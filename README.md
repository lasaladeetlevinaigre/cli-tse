# devkit - GitHub CLI Developer Toolkit

A modern Python wrapper around GitHub CLI (`gh`) that provides a high-level interface for common developer workflows.

## Features

- **issues** - List and filter open issues in rich table format
- **pr-summary** - View PR details including title, body, reviews, and changed files
- **start-feature** - Fork repository and create feature branch in one command
- **open-pr** - Create PRs with interactive prompts
- **run-status** - Monitor CI/CD pipeline status across branches

## Installation

```bash
pip install -r requirements.txt
```

You must have GitHub CLI (`gh`) installed: https://cli.github.com

## Usage

```bash
# List issues
devkit issues --limit 20 --repo owner/repo

# View PR summary
devkit pr-summary --pr 42

# Start a new feature
devkit start-feature --name feature/my-feature

# Create a PR interactively
devkit open-pr

# Check CI status
devkit run-status --limit 10
```

## Commands Reference

### devkit issues
List open issues in a table with state and labels.

Options:
- `--repo` - Repository (owner/repo, default: current repo)
- `--limit` - Max number of issues (default: 15)
- `--state` - Filter by state: OPEN, CLOSED, ALL (default: OPEN)

### devkit pr-summary
Show PR title, body, reviews, and changed files.

Options:
- `--pr` - PR number (required)
- `--repo` - Repository (owner/repo, default: current repo)

### devkit start-feature
Fork repository and create a feature branch.

Options:
- `--name` - Feature branch name (required)
- `--repo-url` - Repository URL to fork (default: current repo)

### devkit open-pr
Create a PR with interactive prompts.

Options:
- `--title` - PR title (prompted if not provided)
- `--body` - PR description (prompted if not provided)
- `--repo` - Repository (owner/repo, default: current repo)
- `--draft` - Create as draft PR

### devkit run-status
Show latest CI run status per branch.

Options:
- `--repo` - Repository (owner/repo, default: current repo)
- `--limit` - Max number of runs (default: 10)

## Architecture

```
devkit/
  __init__.py          # Package init
  main.py              # Main CLI app with typer
  commands/
    __init__.py
    github.py          # All 5 GitHub commands
  utils/
    __init__.py
    gh.py              # GitHub CLI wrapper functions
```

## Implementation Details

- Uses `subprocess` to wrap `gh` commands
- Outputs JSON using `gh --json` for structured data
- Uses `rich` library for beautiful table formatting and colored output
- All commands use Typer for argument parsing
