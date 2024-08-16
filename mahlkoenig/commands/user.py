"""Interact with user data of the Mahlkönig API."""

import typer
from rich.console import Console
from rich.table import Table

console = Console()

app = typer.Typer()


@app.command()
def short(ctx: typer.Context):
    """Show the short details of the current user."""
    api_client = ctx.obj.get("api_client")
    details = ctx.obj.get("details")

    user_details = api_client.get("/api/security-service/auth/account")
    company = api_client.get(
        "/api/admin-service/company/",
        params={"key": details["account"]["details"]["comp"]},
    )

    del user_details["account"]

    user_details["company"] = company["info"]["name"]

    table = Table(title="User details")

    table.add_column("Key", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value")

    for description, value in user_details.items():
        table.add_row(
            description,
            str(value),
        )

    console.print(table)


@app.command()
def profile(ctx: typer.Context):
    """Show the profile of the current user."""
    api_client = ctx.obj.get("api_client")

    profile = api_client.get("/api/admin-service/profile/my-profile")

    table = Table(title="User profile")

    table.add_column("Key", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value")

    for description, value in profile.items():
        table.add_row(
            description,
            str(value),
        )

    console.print(table)
