import pytest
from http import HTTPStatus

from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    GetUserResponseSchema,
    UpdateUserRequestSchema,
    UpdateUserResponseSchema
)
from fixtures.users import UserFixture

from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import (
    assert_create_user_response,
    assert_get_user_response,
    assert_update_user_response
)
from tools.fakers import fake


class TestUsers:
    @pytest.mark.parametrize("email", ["mail.ru", "gmail.com", "example.com"])
    def test_create_user(
            self,
            email: str,
            public_users_client: PublicUsersClient,
    ):
        request = CreateUserRequestSchema(email=fake.email(domain=email))
        response = public_users_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_user_me(
            self,
            function_user: UserFixture,
            private_users_client: PrivateUsersClient,
    ):
        response = private_users_client.get_user_me_api()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data.user, function_user.response.user)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_user_for_id(
            self,
            function_user: UserFixture,
            private_users_client: PrivateUsersClient,
    ):
        response = private_users_client.get_user_api(user_id=function_user.response.user.id)
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data.user, function_user.response.user)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_user(
            self,
            function_user: UserFixture,
            private_users_client: PrivateUsersClient,
    ):
        request = UpdateUserRequestSchema(
            email=fake.email(),
            first_name=None,
            last_name=None,
            middle_name=None
        )
        response = private_users_client.update_user_api(
            user_id=function_user.response.user.id,
            request=request
        )
        response_data = UpdateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_user_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_user(
            self,
            function_user: UserFixture,
            private_users_client: PrivateUsersClient,
    ):
        delete_response = private_users_client.delete_user_api(
            user_id=function_user.response.user.id
        )
        assert_status_code(delete_response.status_code, HTTPStatus.OK)
