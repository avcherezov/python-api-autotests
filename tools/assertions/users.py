import allure

from clients.users.users_schema import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    UserSchema,
    UpdateUserRequestSchema,
    UpdateUserResponseSchema
)
from tools.assertions.base import assert_equal


@allure.step("Check user")
def assert_user(actual: UserSchema, expected: UserSchema):
    """
    Проверяет корректность пользовательских моделей.

    :param actual: Объект UserSchema.
    :raises expected: Объект UserSchema.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.email, expected.email, "email")
    assert_equal(actual.last_name, expected.last_name, "last_name")
    assert_equal(actual.first_name, expected.first_name, "first_name")
    assert_equal(actual.middle_name, expected.middle_name, "middle_name")


@allure.step("Check get user response")
def assert_get_user_response(get_user_response, create_user_response):
    """
    Проверяет корректности данных пользователя при создании и при запросе.

    :param get_user_response: ответ API при запросе пользователя.
    :raises create_user_response: ответ API при создании пользователя.
    """
    assert_user(get_user_response, create_user_response)


@allure.step("Check create user response")
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    """
    Проверяет, что ответ на создание пользователя соответствует запросу.

    :param request: Исходный запрос на создание пользователя.
    :param response: Ответ API с данными пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")


@allure.step("Check update user response")
def assert_update_user_response(request: UpdateUserRequestSchema, response: UpdateUserResponseSchema):
    """
    Проверяет, что ответ на обновление пользователя соответствует запросу.

    :param request: Исходный запрос на обновление пользователя.
    :param response: Ответ API с данными пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    if request.email is not None:
        assert_equal(response.user.email, request.email, "email")
    if request.last_name is not None:
        assert_equal(response.user.last_name, request.last_name, "last_name")
    if request.first_name is not None:
        assert_equal(response.user.first_name, request.first_name, "first_name")
    if request.middle_name is not None:
        assert_equal(response.user.middle_name, request.middle_name, "middle_name")
