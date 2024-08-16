"""Interact with region data of the Mahlkönig API."""
import typer

from rich import print_json
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()

@app.command()
def short(ctx: typer.Context):
    """List the regions."""
    api_client = ctx.obj.get("api_client")
    details = ctx.obj.get("details")

    company_id = details["account"]["details"]["comp"]

    payload = {
        "companyId": company_id,
        "loadCompany": True,
        "orderBy": "info.name",
        "orderDir": "ASC",
        "pager": {
            "firstResult": 0,
            "pageSize": 25,
        }
    }

    regions = api_client.post("/api/admin-service/region/query", json=payload)

    table = Table(title="Regions")

    table.add_column("Region ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Name")
    table.add_column("Short name")
    table.add_column("Description")

    for region in regions["items"]:
        table.add_row(
            str(region["regionId"]),
            region["info"]["name"],
            region["info"]["shortName"],
            region["info"]["desc"],
        )

    console.print(table)

@app.command()
def full(ctx: typer.Context):
    """List the regions."""
    api_client = ctx.obj.get("api_client")
    details = ctx.obj.get("details")

    company_id = details["account"]["details"]["comp"]

    console.print("Region details", style="magenta")
    console.print("")

    payload = {
        "companyId": company_id,
        "loadCompany": True,
        "orderBy": "info.name",
        "orderDir": "ASC",
        "pager": {
            "firstResult": 0,
            "pageSize": 25,
        }
    }

    regions = api_client.post("/api/admin-service/region/query", json=payload)

    print_json(data=regions)
