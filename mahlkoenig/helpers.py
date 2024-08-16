"""Helper parts for various tasks."""

from datetime import datetime

import httpx


class AuthAPIClient:
    """Representation of an API client for the Mahlkönig API."""

    def __init__(
        self, base_url: str, username: str, password: str, timeout: float = 5.0
    ):
        """Initialize the API client."""
        self.base_url = base_url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.token = None

    def authenticate(self):
        """Authenticate user with username and password."""
        auth_endpoint = "/api/security-service/auth/token"
        data = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }
        with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
            try:
                response = client.post(auth_endpoint, json=data)
                response.raise_for_status()
                self.token = response.json().get("access_token")
                # print("Authentication successful")
            except httpx.HTTPStatusError as error:
                print(
                    f"Authentication failed: {error.response.status_code} - {error.response.text}"
                )
            except httpx.RequestError as error:
                print(f"An error occurred while requesting {error.request.url!r}.")

    def get_headers(self):
        """Get the Bearer token for authentication."""
        if not self.token:
            raise ValueError("No token found. Please authenticate first")
        return {"Authorization": f"Bearer {self.token}"}

    def get(self, endpoint: str, params: dict = None):
        """Execute a GET request."""
        headers = self.get_headers()
        with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
            try:
                response = client.get(endpoint, headers=headers, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as error:
                print(f"Error: {error.response.status_code} - {error.response.text}")
                return None

    def post(self, endpoint: str, data: dict = None, json: dict = None):
        """Execute a POST request."""
        headers = self.get_headers()
        with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
            try:
                response = client.post(endpoint, headers=headers, data=data, json=json)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as error:
                print(f"Error: {error.response.status_code} - {error.response.text}")
                return None
            except httpx.RequestError as error:
                print(f"An error occurred while requesting {error.request.url!r}.")
                return None


def setup_connection(url: str, username: str, password: str):
    """Connect to the Mahlkönig API."""
    api_client = AuthAPIClient(
        base_url="https://syncqa.mahlkoenig.com", username=username, password=password
    )

    # This is a hack to eliminate the need to refresh the token
    api_client.authenticate()

    user_details = api_client.get("/api/security-service/auth/account")

    return (api_client, user_details)


def human_readable_datetime(data, *args):
    """Replace timestamps with a human readable date in a dict."""
    format_string = "%Y-%m-%d %H:%M:%S"
    for entry in data:
        for element in args:
            entry[element] = datetime.fromtimestamp(entry[element]).strftime(
                format_string
            )

    return data
