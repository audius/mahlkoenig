"""Interact with region data of the Mahlkönig API."""

from typing import Optional

import typer
from rich import print_json
from rich.console import Console
from typing_extensions import Annotated

console = Console()
app = typer.Typer()


@app.command()
def managers(
    ctx: typer.Context,
    store_id: Annotated[
        Optional[int],
        typer.Option(help="ID of the region to query", prompt=True),
    ],
):
    """List the managers of a given region."""
    api_client = ctx.obj.get("api_client")
    details = ctx.obj.get("details")

    company_id = details["account"]["details"]["comp"]

    console.print("Regional manager(s)", style="magenta")
    console.print("")

    payload = {
        "managedId": store_id,
        "orderDir": "ASC",
        "pager": {
            "firstResult": 0,
            "pageSize": 25,
        },
    }

    managers = api_client.post("/api/admin-service/store/manager/query", json=payload)

    print_json(data=managers)
