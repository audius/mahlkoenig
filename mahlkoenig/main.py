"""Main part of the Mahlkönig API client."""

import typer
from typing_extensions import Annotated
from validators import email, url

from mahlkoenig.commands import (
    company,
    info,
    region,
    regions,
    store,
    stores,
    user,
    users,
)
from mahlkoenig.helpers import setup_connection

app = typer.Typer()

app.add_typer(company.app, name="company")
app.add_typer(info.app, name="info")
app.add_typer(region.app, name="region")
app.add_typer(regions.app, name="regions")
app.add_typer(store.app, name="store")
app.add_typer(stores.app, name="stores")
app.add_typer(user.app, name="user")
app.add_typer(users.app, name="users")


def validate_url(value: str):
    """Check if url is a valid URL."""
    if url(value):
        raise typer.BadParameter("URL is not valid")
    return value


def validate_username(value: str):
    """Check the user's name."""
    if email(str(value)):
        raise typer.BadParameter("User's name is not an e-mail address")
    return value


# def validate_token(value: str):
#     """Check the token's name."""
#     if len(value) <= 600:
#         raise typer.BadParameter("Token doesn't have the right length")
#     return value


@app.callback()
def main(
    ctx: typer.Context,
    user_name: Annotated[
        str,
        typer.Option(
            envvar="USER_NAME",
            help="User name for the Mahlkönig interface",
            prompt=True,
            # callback=validate_username,
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            envvar="PASSWORD",
            help="Password for Mahlkönig interface",
            prompt=True,
        ),
    ],
    # token: Annotated[
    #     str,
    #     typer.Option(
    #         envvar="TOKEN",
    #         help="User token for the Mahlkönig API",
    #         prompt=True,
    #         callback=validate_token,
    #     ),
    # ],
    url: Annotated[
        str,
        typer.Option(
            envvar="URL",
            help="URL to Mahlkönig API",
            prompt=True,
            # callback=validate_url,
        ),
    ],
):
    api_client, details, auth_data = setup_connection(url, user_name, password)

    ctx.obj = {"api_client": api_client, "details": details, "username": user_name, "auth_data": auth_data}


if __name__ == "__main__":
    app()
