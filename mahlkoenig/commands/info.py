"""Interact with authentication data of the Mahlkönig API."""

import typer
from rich import print_json
from rich.console import Console
from rich.table import Table

console = Console()

app = typer.Typer()


@app.command()
def auth(ctx: typer.Context):
    """Show the current token."""
    api_client = ctx.obj.get("api_client")
    auth_data = ctx.obj.get("auth_data")

    table = Table(title="Authentication data")

    table.add_column("Key", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value")

    for description, value in auth_data.items():
        table.add_row(
            description,
            str(value),
        )

    console.print(table)
