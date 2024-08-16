"""Interact with company data of the Mahlkönig API."""
import typer

from rich import print_json
from rich.console import Console

console = Console()
app = typer.Typer()


@app.command()
def show(ctx: typer.Context):
    """Show the company details."""
    api_client = ctx.obj.get("api_client")
    details = ctx.obj.get("details")

    company = api_client.get("/api/admin-service/company/", params={"key": details["account"]["details"]["comp"]})

    console.print("Company details", style="magenta")
    console.print("")

    print_json(data=company)
