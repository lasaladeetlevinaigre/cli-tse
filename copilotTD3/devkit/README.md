# devkit

A modern Python CLI tool that orchestrates GitHub, Copilot, Gemini, and Claude to automate developer workflows.

## Features

- **GitHub Integration**: List issues, PRs, manage branches, check CI status
- **AI-Powered Commands**: Explain shell commands, suggest solutions, auto-generate commits
- **Workflow Automation**: Streamlined feature branch creation and PR management
- **Interactive Mode**: Use `--interactive` flag for fuzzy selection with fzf
- **Rich Output**: Beautiful terminal UI with tables, panels, and spinners

## Installation

```bash
pip install -e .
```

## Usage

### GitHub Commands

```bash
devkit gh issues              # List issues
devkit gh pr-summary PR_NUM   # Show PR summary
devkit gh start-feature NAME  # Create feature branch
devkit gh open-pr             # Create pull request
devkit gh run-status          # Check CI status
```

### AI Commands

```bash
devkit ai explain "your command"   # Explain a command
devkit ai suggest "task description"  # Get AI suggestions
devkit ai review PR_NUM             # AI review of PR
devkit ai commit                    # Generate commit message
```

### Workflow Commands

```bash
devkit workflow feature-start NAME [--issue ISSUE_NUM]
```

### Configuration

Configuration is stored in `~/.devkit/config.json`:

```json
{
  "ai_tool": "claude",
  "default_repo": "",
  "theme": "dark",
  "show_spinner": true
}
```

## Requirements

- Python 3.12+
- GitHub CLI (`gh`)
- GitHub Copilot CLI (`gh copilot`)
- Git
- Optional: fzf (for interactive mode)

## Development

```bash
pip install -e ".[dev]"
pytest
black .
ruff check .
mypy src/
```
