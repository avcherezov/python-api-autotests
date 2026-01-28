from http import HTTPStatus

from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    GetCourseResponseSchema,
    GetCoursesQuerySchema,
    GetCoursesResponseSchema,
    UpdateCourseRequestSchema,
    UpdateCourseResponseSchema
)
from clients.errors_schema import InternalErrorResponseSchema
from fixtures.users import UserFixture
from fixtures.files import FileFixture
from fixtures.courses import CourseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.courses import (
    assert_cource_not_found_response,
    assert_create_course_response,
    assert_get_cource_response,
    assert_get_courses_response,
    assert_update_course_response
)
from tools.assertions.schema import validate_json_schema


class TestCourses:
    def test_create_course(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id
        )
        response = courses_client.create_course_api(request)
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_course(self, courses_client: CoursesClient, function_course: CourseFixture):
        response = courses_client.get_course_api(function_course.response.course.id)
        response_data = GetCourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_cource_response(response_data, function_course.response)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_courses(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture,
            function_user: UserFixture
    ):
        query = GetCoursesQuerySchema(user_id=function_user.response.user.id)
        response = courses_client.get_courses_api(query)
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_courses_response(response_data, [function_course.response])

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_course(self, courses_client: CoursesClient, function_course: CourseFixture):
        request = UpdateCourseRequestSchema()
        response = courses_client.update_course_api(function_course.response.course.id, request)
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_cource(self, courses_client: CoursesClient, function_course: CourseFixture):
        delete_response = courses_client.delete_course_api(function_course.response.course.id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = courses_client.get_course_api(function_course.response.course.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_cource_not_found_response(get_response_data)

        validate_json_schema(get_response.json(), get_response_data.model_json_schema())
