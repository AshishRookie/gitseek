import argparse
import webbrowser
import subprocess
from rich.console import Console
from rich.table import Table

from .github_api import search_repositories

console = Console()


def main():
    parser = argparse.ArgumentParser(description="Search GitHub repositories")

    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Number of results")
    parser.add_argument("--open", type=int, help="Open repo number in browser")
    parser.add_argument("--clone", type=int, help="Clone repo number")

    args = parser.parse_args()

    query = " ".join(args.query)

    repos = search_repositories(query, limit=args.limit)

    if not repos:
        console.print("[red]No repositories found[/red]")
        return

    table = Table(title=f"GitHub results for: {query}")

    table.add_column("#", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Stars", style="yellow")
    table.add_column("Description", style="white")

    for i, repo in enumerate(repos, start=1):
        table.add_row(
            str(i),
            repo["name"],
            str(repo["stargazers_count"]),
            repo["description"] or ""
        )

    console.print(table)

    if args.open:
        repo = repos[args.open - 1]
        webbrowser.open(repo["html_url"])

    if args.clone:
        repo = repos[args.clone - 1]
        subprocess.run(["git", "clone", repo["html_url"]])