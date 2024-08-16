"""Interact with users data of the Mahlkönig API."""

import typer
from rich.console import Console
from rich.table import Table

console = Console()

app = typer.Typer()


@app.command()
def list(ctx: typer.Context):
    """List all users of your company."""
    api_client = ctx.obj.get("api_client")
    details = ctx.obj.get("details")

    company_id = details["account"]["details"]["comp"]

    payload = {
        "companyId": company_id,
        "loadGroups": True,
        "orderDir": "ASC",
        "pager": {
            "firstResult": 0,
            "pageSize": 25,
        },
    }

    users = api_client.post("/api/admin-service/profile/query", json=payload)

    table = Table(title="Users")

    table.add_column("Profile/user ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("User name")
    table.add_column("Name")
    table.add_column("Groups")

    for user in users["items"]:
        user_data = user["user"]
        groups = []
        for group in user_data["groups"]:
            groups.append(group["info"]["name"])
        table.add_row(
            str(user_data["userId"]),
            user_data["username"],
            f"{user_data["firstName"]} {user_data["lastName"]}",
            ", ".join(groups),
        )

    console.print(table)


@app.command()
def invitations(ctx: typer.Context):
    """Show the state of the invitations."""
    api_client = ctx.obj.get("api_client")
    details = ctx.obj.get("details")

    company_id = details["account"]["details"]["comp"]

    payload = {
        "companyId": company_id,
        "loadGroups": True,
        "orderDir": "ASC",
        "pager": {
            "firstResult": 0,
            "pageSize": 25,
        },
    }

    invitations = api_client.post("/api/admin-service/invitation/query", json=payload)

    table = Table(title="Invitations")

    table.add_column("Invitation ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Status")
    table.add_column("Invited email")
    table.add_column("Invited to group")

    for invitation in invitations["items"]:
        table.add_row(
            str(invitation["invitationId"]),
            invitation["status"],
            invitation["invitedEmail"],
            ", ".join(invitation["groupNames"]),
        )

    console.print(table)
