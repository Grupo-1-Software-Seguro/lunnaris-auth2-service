import os
import requests


class User(object):
    id: str
    fullName: str
    email: str
    ssid: str = None


class UserAPI:
    URL: str

    def __init__(self, token=None) -> None:
        self.token = token
        self.URL = os.getenv("USERS_API")

    def get_headers(self, extra_headers=None) -> dict:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        if extra_headers:
            headers.update(extra_headers)

        return headers

    def url(self, path):
        return self.URL + path

    def check_users(self, users: list[str]) -> dict:
        url = self.url("/api/users/validate")

        body = {
            "users": users
        }

        response: requests.Response = requests.post(url, json=body, headers=self.get_headers())

        return response.json()

    def get_users(self, users: list[str]) -> list[User]:
        response = self.check_users(users)

        if response["type"] == "array":
            return [User(**user) for user in response["body"]]

        return []
