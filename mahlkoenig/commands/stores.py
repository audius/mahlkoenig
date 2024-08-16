"""Interact with stores of the Mahlkönig API."""
import typer

from rich import print_json
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()

@app.command()
def short(ctx: typer.Context):
    """List the stores."""
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

    stores = api_client.post("/api/admin-service/store/query", json=payload)
    regions = api_client.post("/api/admin-service/region/query", json=payload)

    regions_data = {}

    for region in regions["items"]:
        regions_data[region["regionId"]] = {
            "name": region["info"]["name"],
            "short_name": region["info"]["shortName"],
        }

    table = Table(title="Stores")

    table.add_column("Store ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Name")
    table.add_column("Short name")
    table.add_column("Description")
    table.add_column("Region")

    for store in stores["items"]:
        table.add_row(
            str(store["storeId"]),
            store["info"]["name"],
            store["info"]["shortName"],
            store["info"]["desc"],
            regions_data[store["regionId"]]["name"],
        )

    console.print(table)

@app.command()
def full(ctx: typer.Context):
    """List the stores with full details."""
    api_client = ctx.obj.get("api_client")
    details = ctx.obj.get("details")

    company_id = details["account"]["details"]["comp"]

    console.print("Stores details", style="magenta")
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

    regions = api_client.post("/api/admin-service/store/query", json=payload)

    print_json(data=regions)
