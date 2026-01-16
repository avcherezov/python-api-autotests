from httpx import Response

from clients.api_client import APIClient
from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    GetCoursesRequestSchema,
    UpdateCourseRequestSchema,
    UpdateCourseResponseSchema,
)
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
from tools.routes import APIRoutes


class CoursesClient(APIClient):
    """
    Клиент для работы с /api/v1/courses
    """

    def get_courses_api(self, query: GetCoursesRequestSchema) -> Response:
        """
        Метод получения списка курсов.

        :param query: GetCoursesRequestSchema
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(APIRoutes.COURSES, params=query.model_dump(by_alias=True))

    def get_course_api(self, course_id: str) -> Response:
        """
        Метод получения курса.

        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.COURSES}/{course_id}")

    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        """
        Метод создания курса.

        :param request: CreateCourseRequestSchema
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(APIRoutes.COURSES, json=request.model_dump(by_alias=True))

    def update_course_api(self, course_id: str, request: UpdateCourseRequestSchema) -> UpdateCourseResponseSchema:
        """
        Метод обновления курса.

        :param course_id: Идентификатор курса.
        :param request: UpdateCourseRequestSchema.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(f"{APIRoutes.COURSES}/{course_id}", json=request.model_dump(by_alias=True))

    def delete_course_api(self, course_id: str) -> Response:
        """
        Метод удаления курса.

        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"{APIRoutes.COURSES}/{course_id}")

    def create_course(self, request: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        """
        Метод создания курса.

        :param request: CreateCourseRequestSchema
        :return: Ответ в виде объекта CreateCourseResponseSchema
        """
        response = self.create_course_api(request=request)
        return CreateCourseResponseSchema.model_validate_json(response.text)


def get_courses_client(user: AuthenticationUserSchema) -> CoursesClient:
    """
    Функция создаёт экземпляр CoursesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CoursesClient.
    """
    return CoursesClient(client=get_private_http_client(user))
