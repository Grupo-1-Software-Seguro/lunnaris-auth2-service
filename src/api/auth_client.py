import requests
import json
from enum import Enum

class ApiError(Exception):
    pass


class UserType(Enum):
    ADMIN = 1
    USER = 2
    MEDIA_MANAGER = 3


class RegisterUserRequest:

    def __init__(self, userId=None, password=None, email=None, userType=UserType.USER) -> None:
        self.userId = userId
        self.password = password
        self.email = email
        if isinstance(userType, UserType):
            self.userType = userType.value
        else:
            self.userType = userType


class AuthClient:
    def __init__(self, base_url) -> None:
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accepts": "application/json"
        }

    def authenticate(self, token: str) -> bool:
        url = f"{self.base_url}/api/auth/authenticate"
        payload = {
            "token": token
        }

        try:
            response: requests.Response = requests.post(url, json=payload, headers=self.headers)
            response = response.json()
            
            if response["type"] == "object":
                return response["body"]["authenticated"]

            if response["type"] == "error":
                body = response["body"]
                raise ApiError(f"Error: {body}")

        except json.JSONDecodeError as e:
            raise ApiError(f"JSON: {e}")
        

    def authorize(self, token: str, action: str) -> bool:
        url = f"{self.base_url}/api/auth/authorize"
        payload = {
            "action": action,
            "token": token
        }

        try:
            response: requests.Response = requests.post(url, json=payload, headers=self.headers)
            response = response.json()
            if response["type"] == "object":
                return response["body"]["authorized"]

            if response["type"] == "error":
                body = response["body"]
                raise ApiError(f"Error: {body}")

        except json.JSONDecodeError as e:
            raise ApiError(f"JSON: {e}")
    

    def register_credentials(self, token: str, register_user_request: RegisterUserRequest) -> bool:
        url = f"{self.base_url}/api/auth/register"
        payload = {
            "userId": register_user_request.userId,
            "email": register_user_request.email,
            "password": register_user_request.password,
            "userType": register_user_request.userType
        }

        print(payload)

        response = requests.post(url, json=payload, headers=self.headers)
        try:
            response = response.json()
            
            if response["type"] == "object":
                return response["body"]["state"]
            
            if response["type"] == "error":
                body = response["body"]
                raise ApiError(f"Error: {body}")

        except json.JSONDecodeError as e:
            raise ApiError(f"JSON: {e}")

        
