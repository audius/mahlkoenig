"""Interact with company data of the Mahlkönig API."""

import typer
from rich import print_json
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()


@app.command()
def show(ctx: typer.Context):
    """Show the company details."""
    api_client = ctx.obj.get("api_client")
    details = ctx.obj.get("details")

    company = api_client.get(
        "/api/admin-service/company/",
        params={"key": details["account"]["details"]["comp"]},
    )

    table = Table(title="Company")

    table.add_column("Company ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Name")
    table.add_column("Short name")
    table.add_column("Description")

    table.add_row(
        str(company["companyId"]),
        company["info"]["name"],
        company["info"]["shortName"],
        company["info"]["desc"],
    )

    console.print(table)


@app.command()
def query(ctx: typer.Context):
    """Show the company details."""
    api_client = ctx.obj.get("api_client")
    details = ctx.obj.get("details")

    company_id = details["account"]["details"]["comp"]

    payload = {
        "companyId": company_id,
        "groups": {0: "COMP_ADMINS"},
        "orderDir": "ASC",
        "pager": {
            "firstResult": 0,
            "pageSize": 25,
        },
    }

    company = api_client.post("/api/admin-service/company/query", json=payload)

    console.print("Company details", style="magenta")
    console.print("")

    print_json(data=company)
