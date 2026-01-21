import allure

from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("COURSES_ASSERTIONS")


@allure.step("Check create course response")
def assert_create_course_response(
        actual: CreateCourseRequestSchema, 
        expected: CreateCourseResponseSchema
    ):
    """
    Проверяет, что ответ на создание курса соответствует ответам на создание.

    :param actual: Фактические данные курса.
    :param expected: Ожидаемые данные курса.
    :raises AssertionError: Если данные курсов не совпадают.
    """
    logger.info("Check create course response")
    
    assert_equal(actual.title, expected.course.title, "title")
    assert_equal(actual.max_score, expected.course.max_score, "max_score")
    assert_equal(actual.min_score, expected.course.min_score, "min_score")
    assert_equal(actual.description, expected.course.description, "description")
    assert_equal(actual.estimated_time, expected.course.estimated_time, "estimated_time")
    assert_equal(actual.preview_file_id, expected.course.preview_file.id, "preview_file_id")
    assert_equal(actual.created_by_user_id, expected.course.created_by_user.id, "created_by_user_id")
