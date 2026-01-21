from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("EXERCISES_ASSERTIONS")


def assert_create_exercise_response(
        actual: CreateExerciseRequestSchema, 
        expected: CreateExerciseResponseSchema
    ):
    """
    Проверяет, что ответ на создание задания соответствует ответу на создание.

    :param actual: Фактические данные задания.
    :param expected: Ожидаемые данные задания.
    :raises AssertionError: Если данные задания не совпадают.
    """
    logger.info("Check create exercise response")
    
    assert_equal(actual.title, expected.exercise.title, "title")
    assert_equal(actual.course_id, expected.exercise.course_id, "course_id")
    assert_equal(actual.max_score, expected.exercise.max_score, "max_score")
    assert_equal(actual.min_score, expected.exercise.min_score, "min_score")
    assert_equal(actual.order_index, expected.exercise.order_index, "order_index")
    assert_equal(actual.description, expected.exercise.description, "description")
    assert_equal(actual.estimated_time, expected.exercise.estimated_time, "estimated_time")
