from services.implementation.auth_service import AuthService
from dto.requests import LoginRequest
from entities.auth_registry import AuthRegistry
from unittest.mock import Mock
from utils.password import hash_password
from exceptions import InvalidCredentials
import pytest

# Login

def test_login():
    mock = Mock()
    mock.get_by_email.return_value = AuthRegistry(
        userId="1",
        email="correo1@email.com",
        password=hash_password("12345")
    )

    mock.create_token.return_value = "un_token"

    auth_service = AuthService(
        dao=mock,
        token_generator=mock
    )

    response = auth_service.login(LoginRequest(email="correo1@email.com", password="12345"))
    mock.get_by_email.assert_called_with("correo1@email.com")
    assert response.token == "un_token"

def test_login_non_existing_user():
    mock = Mock()
    mock.get_by_email.return_value = None

    auth_service = AuthService(
        dao=mock,
        token_generator=mock
    )

    with pytest.raises(InvalidCredentials):
        auth_service.login(LoginRequest(email="correo1@email.com", password="1234"))

    mock.get_by_email.assert_called_with("correo1@email.com")


def test_login_wrong_password():
    mock = Mock()
    mock.get_by_email.return_value = AuthRegistry(
        userId="1",
        email="correo1@email.com",
        password=hash_password("12345")
    )

    auth_service = AuthService(
        dao=mock,
        token_generator=mock
    )

    with pytest.raises(InvalidCredentials):
        auth_service.login(LoginRequest(email="correo1@email.com", password="1234"))

    mock.get_by_email.assert_called_with("correo1@email.com")

    

    
    
    
