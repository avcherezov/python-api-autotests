import pytest
from pydantic import BaseModel

from clients.authentication.authentication_client import AuthenticationClient, get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from fixtures.users import UserFixture


class AuthenticationFixture(BaseModel):
    request: LoginRequestSchema
    response: LoginResponseSchema


@pytest.fixture
def authentication_client() -> AuthenticationClient:
    return get_authentication_client()


@pytest.fixture
def function_authentication(
        authentication_client: AuthenticationClient,
        function_user: UserFixture,
) -> AuthenticationFixture:
    request = LoginRequestSchema(
        email=function_user.email, password=function_user.password
    )
    response = authentication_client.login(request)
    return AuthenticationFixture(request=request, response=response)
