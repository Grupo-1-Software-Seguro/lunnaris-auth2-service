from dto.responses import RegisterUserResponse, NewPasswordResponse
from services.implementation.auth_service import AuthService
from dto.requests import *
from entities.auth_registry import AuthRegistry
from unittest.mock import Mock, ANY
from utils.password import hash_password, check_password
from exceptions import InvalidCredentials, AlreadyRegistered, NotRegistered
import pytest

# Login

def create_auth_service_with_mock(mock):
    return AuthService(
        dao=mock,
        token_generator=mock,
        mail=mock
    )

def test_login():
    mock = Mock()
    mock.get_by_email.return_value = AuthRegistry(
        userId="1",
        email="correo1@email.com",
        password=hash_password("12345")
    )

    mock.create_token.return_value = "un_token"

    auth_service = create_auth_service_with_mock(mock)

    response = auth_service.login(
        LoginRequest(email="correo1@email.com", password="12345"))
    mock.get_by_email.assert_called_with("correo1@email.com")
    assert response.token == "un_token"

def test_login_non_existing_user():
    mock = Mock()
    mock.get_by_email.return_value = None

    auth_service = create_auth_service_with_mock(mock)

    with pytest.raises(InvalidCredentials) as ex:
        auth_service.login(LoginRequest(email="correo1@email.com", password="1234"))
    
    assert ex.type == InvalidCredentials
    mock.get_by_email.assert_called_with("correo1@email.com")


def test_login_wrong_password():
    mock = Mock()
    mock.get_by_email.return_value = AuthRegistry(
        userId="1",
        email="correo1@email.com",
        password=hash_password("12345")
    )

    auth_service = create_auth_service_with_mock(mock)

    with pytest.raises(InvalidCredentials) as ex:
        auth_service.login(LoginRequest(email="correo1@email.com", password="1234"))

    assert ex.type == InvalidCredentials
    mock.get_by_email.assert_called_with("correo1@email.com")

# User registration
def test_register_user():
    mock = Mock()
    mock.get_by_email.return_value = None
    mock.save.return_value = True

    register_response = RegisterUserResponse(
        state=True
    )
        
    auth_service = create_auth_service_with_mock(mock)

    response = auth_service.register_user(
        RegisterUserRequest(
            userId="1",
            email="user1@email.com",
            password="1234"
        )
    )

    mock.get_by_email.assert_called_with("user1@email.com")
    created_object = mock.save.call_args[0][0]
    assert created_object.userId == "1"
    assert created_object.email == "user1@email.com"
    assert check_password("1234", created_object.password)
    assert response == register_response

    
def test_existing_user_registry():
    mock = Mock()
    mock.get_by_email.return_value = AuthRegistry(
        userId="1",
        email="user1@email.com",
        password="1234"
    )

    auth_service = create_auth_service_with_mock(mock)

    with pytest.raises(AlreadyRegistered) as ex:
        auth_service.register_user(
            RegisterUserRequest(userId="1", email="user1@email.com",password="1234"))
        
    assert ex.type == AlreadyRegistered
    mock.get_by_email.assert_called_with("user1@email.com")


# Password reset
def test_request_password_reset():
    mock = Mock()
    mock.get_by_email.return_value = AuthRegistry(
        userId="1",
        email="user1@email.com",
        password="1234"
    )
    mock.send_reset_password_email.return_value = None
    mock.create_token.return_value = "un_token"

    auth_service = create_auth_service_with_mock(mock)

    response = auth_service.request_password_reset(
        ResetPasswordRequest(
            email="user1@email.com"
        )
    )

    mock.get_by_email.assert_called_with("user1@email.com")
    mock.create_token.assert_called_with("1", ANY)
    mock.send_reset_password_email.assert_called_with(
        "", "user1@email.com", "un_token")
    assert response.token == "un_token"
    

def test_request_password_reset_not_registered():
    mock = Mock()
    mock.get_by_email.return_value = None

    auth_service = create_auth_service_with_mock(mock)
    with pytest.raises(NotRegistered) as ex:
        auth_service.request_password_reset(
            ResetPasswordRequest(email="user1@email.com")
        )
    assert ex.type == NotRegistered
    mock.get_by_email.assert_called_with("user1@email.com")


def test_set_new_password():
    mock = Mock()
    mock.read_token.return_value = {"id": "1"}

    mock.get_by_user_id.return_value = AuthRegistry(
        userId="1",
        email="user1@email.com",
        password="1234"
    )
    mock.update.return_value = True

    auth_service = create_auth_service_with_mock(mock)
    response = auth_service.set_new_password(
        NewPasswordRequest(
            token="un_token",
            password="12345"
        )
    )

    mock.read_token.assert_called_with("un_token")
    mock.get_by_user_id.assert_called_with("1")
    called = mock.update.call_args[0][0]
    assert called.userId == "1"
    assert called.email == "user1@email.com"
    assert check_password("12345", called.password)
    assert type(response) == NewPasswordResponse
    
    


