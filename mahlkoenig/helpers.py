"""Helper elements for various tasks."""

from datetime import datetime

import httpx


class APIClient:
    """Basic client to interact with the Mahlkönig API."""

    def __init__(self, base_url: str, headers: dict = None, timeout: float = 10.0):
        """Initialize the API client."""
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers

    def get(self, endpoint: str, headers: dict = None, params: dict = None):
        """Execute a GET request."""
        with httpx.Client(
            base_url=self.base_url, headers=self.headers, timeout=self.timeout
        ) as client:
            try:
                response = client.get(endpoint, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as error:
                print(f"Error: {error.response.status_code} - {error.response.text}")
                return None
            except httpx.RequestError as error:
                print(f"An error occurred while requesting {error.request.url!r}.")
                return None

    def post(
        self, endpoint: str, headers: dict = None, data: dict = None, json: dict = None
    ):
        """Execute a POST request."""
        with httpx.Client(
            base_url=self.base_url, headers=self.headers, timeout=self.timeout
        ) as client:
            try:
                response = client.post(endpoint, data=data, json=json)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as error:
                print(f"Error: {error.response.status_code} - {error.response.text}")
                return None
            except httpx.RequestError as error:
                print(f"An error occurred while requesting {error.request.url!r}.")
                return None


def setup_connection(url, username, password):
    """Connect to the Mahlkönig API."""

    authentication = APIClient(base_url=url)

    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    headers = {}
    token_response = authentication.post("/api/security-service/oauth/token", data=data)

    try:
        scope = token_response["scope"]
        details = token_response["details"]
        username = token_response["username"]
        bearer_token = token_response["access_token"]

        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Accept": "application/json",
        }

        api_client = APIClient(base_url=url, headers=headers)

        return (api_client, details, scope, username)
    except TypeError:
        raise ("Unable to connect to API")


def human_readable_datetime(data, *args):
    """Replace timestamps with a human readable date in a dict."""
    format_string = "%Y-%m-%d %H:%M:%S"
    for entry in data:
        for element in args:
            entry[element] = datetime.fromtimestamp(entry[element]).strftime(
                format_string
            )

    return data
