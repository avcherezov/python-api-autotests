from http import HTTPStatus

from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema

from tools.assertions.base import assert_status_code
from tools.assertions.courses import assert_create_course_response
from tools.assertions.schema import validate_json_schema


class TestCourses:
    def test_create_course(self, cource_client: CoursesClient):
        request = CreateCourseRequestSchema(upload_file="./testdata/files/image.png")
        response = cource_client.create_course_api(request)
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())
