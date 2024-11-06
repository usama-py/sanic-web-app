from sanic.exceptions import SanicException
import re

def validate_user_id(user_id):
    if not isinstance(user_id, str) or len(user_id) < 5 or len(user_id) > 20 or not re.match(r'^[a-zA-Z0-9_]+$', user_id):
        raise SanicException("Invalid user_id.", status_code=400)
    return True

def validate_survey_results(survey_results):
    if len(survey_results) != 10:
        raise SanicException("survey_results must contain exactly 10 items.", status_code=400)

    question_numbers = set()
    for result in survey_results:
        question_number = result.get("question_number")
        question_value = result.get("question_value")

        if not isinstance(question_number, int) or not (1 <= question_number <= 10):
            raise SanicException("Invalid question_number.", status_code=400)
        if not isinstance(question_value, int) or not (1 <= question_value <= 7):
            raise SanicException("Invalid question_value.", status_code=400)

        if question_number in question_numbers:
            raise SanicException(f"Duplicate question_number {question_number} found.", status_code=400)
        question_numbers.add(question_number)
    return True
