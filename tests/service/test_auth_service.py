from service.auth import *
from unittest.mock import Mock
from bcrypt import checkpw
import pytest


def test_register_new_user():
    mock_dao = Mock()
    mock_dao.get_by_email.return_value = None
    mock_dao.save.return_value = None

    service = AuthService(mock_dao, None, None, None)
    body = AuthModel(userId="1", password="Test2024@", email="mail@mail.com")

    result = service.register(body)
    created_user = mock_dao.save.call_args.args[0]
    mock_dao.get_by_email.assert_called_with("mail@mail.com")
    assert result
    assert created_user.email == "mail@mail.com"
    assert checkpw("Test2024@".encode("utf-8"), created_user.password.encode("utf-8"))


def test_register_user_with_existing_email():
    mock_dao = Mock()
    mock_dao.get_by_email.return_value = UserAuth()

    service = AuthService(mock_dao, None, None, None)
    body = AuthModel(userId="1", password="Test2024@", email="mail@mail.com")

    with pytest.raises(AlreadyRegistered):
        service.register(body)



@pytest.fixture
def function_mock(mocker):
    mock = Mock()
    mocker.patch('service.AuthService.check_password', return_value=mock)
    return mock

def gen_password(passw):
    return bcrypt.hashpw(passw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def test_login():
    login = LoginModel(password="Test2024@",email="mail@mail.com")
    mock = Mock()
    mock.get_by_email.return_value = UserAuth(
        email=login.email,
        password=gen_password(login.password)
    )


    service = AuthService(mock, None, None, None)
    response = service.login(login)

    assert response is not None

    
    
    
