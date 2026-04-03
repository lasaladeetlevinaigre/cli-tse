"""GitHub commands for devkit."""
import typer
import subprocess
from typing import Optional
from rich.console import Console
from rich.table import Table
from devkit.utils.gh import gh_json, gh

app = typer.Typer()
console = Console()


@app.command()
def issues(
    repo: str = typer.Option('', help='owner/repo (default: current repo)'),
    limit: int = typer.Option(15, help='Max number of issues'),
    state: str = typer.Option('OPEN', help='Filter by state: OPEN, CLOSED, ALL'),
):
    """List open issues in a rich table."""
    args = ['issue', 'list', '--json', 'number,title,state,labels', '--limit', str(limit)]
    
    if repo:
        args += ['--repo', repo]
    
    if state != 'ALL':
        args += ['--state', state]
    
    try:
        data = gh_json(*args)
        
        table = Table(title='Open Issues', border_style='green')
        table.add_column('#', style='cyan', width=6)
        table.add_column('Title', min_width=30)
        table.add_column('State', width=10)
        table.add_column('Labels', width=20)
        
        for issue in data:
            labels = ', '.join(l['name'] for l in issue.get('labels', []))
            state_style = 'green' if issue['state'] == 'OPEN' else 'red'
            table.add_row(
                str(issue['number']),
                issue['title'],
                f"[{state_style}]{issue['state']}[/{state_style}]",
                labels or '—'
            )
        
        console.print(table)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error:[/red] Failed to fetch issues", style='red')
        console.print(e.stderr)


@app.command()
def pr_summary(
    pr_number: int = typer.Option(..., '--pr', help='PR number'),
    repo: str = typer.Option('', help='owner/repo (default: current repo)'),
):
    """Show PR title, body, reviews, and changed files."""
    args = ['pr', 'view', str(pr_number), '--json', 'title,body,reviews,files']
    
    if repo:
        args += ['--repo', repo]
    
    try:
        pr_data = gh_json(*args)
        
        console.print(f"\n[bold cyan]PR #{pr_number}: {pr_data.get('title', 'N/A')}[/bold cyan]")
        console.print(f"\n[yellow]Description:[/yellow]")
        body = pr_data.get('body', 'No description provided')
        console.print(body if body else '—')
        
        # Display reviews
        reviews = pr_data.get('reviews', [])
        if reviews:
            console.print(f"\n[yellow]Reviews:[/yellow]")
            for review in reviews:
                state_style = 'green' if review['state'] == 'APPROVED' else 'yellow' if review['state'] == 'COMMENTED' else 'red'
                console.print(f"  • [{state_style}]{review['state']}[/{state_style}] by {review['author']['login']}")
        
        # Display changed files
        files = pr_data.get('files', [])
        if files:
            console.print(f"\n[yellow]Changed Files ({len(files)}):[/yellow]")
            file_table = Table(border_style='blue')
            file_table.add_column('File', style='cyan')
            file_table.add_column('Additions', style='green', width=10)
            file_table.add_column('Deletions', style='red', width=10)
            
            for file in files:
                file_table.add_row(
                    file.get('path', 'N/A'),
                    str(file.get('additions', 0)),
                    str(file.get('deletions', 0))
                )
            
            console.print(file_table)
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error:[/red] Failed to fetch PR", style='red')
        console.print(e.stderr)


@app.command()
def start_feature(
    feature_name: str = typer.Option(..., '--name', help='Feature branch name'),
    repo_url: Optional[str] = typer.Option(None, help='Repository URL to fork (default: current repo)'),
):
    """Fork repository and create a feature branch."""
    try:
        # If no repo URL provided, get current repo
        if not repo_url:
            repo_info = gh('repo', 'view', '--json', 'nameWithOwner')
            import json
            repo_data = json.loads(repo_info)
            repo_url = f"https://github.com/{repo_data['nameWithOwner']}"
        
        # Fork the repository
        console.print(f"[yellow]Forking repository...[/yellow]")
        fork_result = gh('repo', 'fork', '--clone=true', repo_url)
        console.print(f"[green]✓ Repository forked[/green]")
        
        # Create and checkout feature branch
        console.print(f"[yellow]Creating feature branch: {feature_name}[/yellow]")
        try:
            subprocess.run(['git', 'checkout', '-b', feature_name], check=True, cwd='.')
            console.print(f"[green]✓ Feature branch created and checked out: {feature_name}[/green]")
        except subprocess.CalledProcessError:
            console.print(f"[red]Error:[/red] Failed to create branch", style='red')
            
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error:[/red] Failed to fork repository", style='red')
        console.print(e.stderr)


@app.command()
def open_pr(
    title: Optional[str] = typer.Option(None, '--title', help='PR title'),
    body: Optional[str] = typer.Option(None, '--body', help='PR description'),
    repo: str = typer.Option('', help='owner/repo (default: current repo)'),
    draft: bool = typer.Option(False, '--draft', help='Create as draft PR'),
):
    """Create a PR with interactive prompts for title and body."""
    try:
        # Get title interactively if not provided
        if not title:
            title = console.input("[cyan]Enter PR title:[/cyan] ")
            if not title:
                console.print("[red]Error:[/red] PR title cannot be empty", style='red')
                return
        
        # Get body interactively if not provided
        if not body:
            console.print("[cyan]Enter PR description (press Ctrl+D or Ctrl+Z when done):[/cyan]")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                body = '\n'.join(lines)
        
        # Build PR creation args
        args = ['pr', 'create', '--title', title]
        
        if body:
            args += ['--body', body]
        
        if draft:
            args += ['--draft']
        
        if repo:
            args += ['--repo', repo]
        
        # Create the PR
        console.print("[yellow]Creating PR...[/yellow]")
        result = gh(*args)
        console.print(f"[green]✓ PR created successfully![/green]")
        console.print(f"[cyan]{result}[/cyan]")
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error:[/red] Failed to create PR", style='red')
        console.print(e.stderr)


@app.command()
def run_status(
    repo: str = typer.Option('', help='owner/repo (default: current repo)'),
    limit: int = typer.Option(10, help='Max number of runs to display'),
):
    """Show latest CI run status per branch."""
    args = ['run', 'list', '--json', 'number,status,conclusion,name,headBranch,createdAt', '--limit', str(limit)]
    
    if repo:
        args += ['--repo', repo]
    
    try:
        data = gh_json(*args)
        
        table = Table(title='Latest CI Runs', border_style='blue')
        table.add_column('Run #', style='cyan', width=8)
        table.add_column('Branch', style='magenta', width=20)
        table.add_column('Workflow', min_width=25)
        table.add_column('Status', width=12)
        table.add_column('Conclusion', width=12)
        table.add_column('Created', width=19)
        
        for run in data:
            status = run.get('status', 'UNKNOWN')
            conclusion = run.get('conclusion', '—')
            
            # Color code status
            status_style = 'yellow' if status == 'IN_PROGRESS' else 'blue' if status == 'QUEUED' else 'cyan'
            
            # Color code conclusion
            conclusion_style = 'green' if conclusion == 'SUCCESS' else 'red' if conclusion == 'FAILURE' else 'yellow' if conclusion in ['CANCELLED', 'SKIPPED'] else 'cyan'
            
            table.add_row(
                str(run.get('number', '—')),
                run.get('headBranch', '—'),
                run.get('name', '—'),
                f"[{status_style}]{status}[/{status_style}]",
                f"[{conclusion_style}]{conclusion}[/{conclusion_style}]",
                run.get('createdAt', '—')[:19]
            )
        
        console.print(table)
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error:[/red] Failed to fetch run status", style='red')
        console.print(e.stderr)


if __name__ == '__main__':
    app()
