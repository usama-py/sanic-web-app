import pytest
from sanic.exceptions import SanicException
from services.validation import validate_user_id, validate_survey_results

# Tests for validate_user_id
def test_valid_user_id():
    assert validate_user_id("valid_user_123") is True

def test_invalid_user_id_type():
    with pytest.raises(SanicException):
        validate_user_id(12345)

def test_invalid_user_id_length():
    with pytest.raises(SanicException):
        validate_user_id("usr")

def test_invalid_user_id_format():
    with pytest.raises(SanicException):
        validate_user_id("invalid@user!")

# Tests for validate_survey_results
def test_valid_survey_results():
    survey_results = [{"question_number": i, "question_value": 5} for i in range(1, 11)]
    assert validate_survey_results(survey_results) is True

def test_invalid_survey_results_length():
    survey_results = [{"question_number": i, "question_value": 5} for i in range(1, 9)]
    with pytest.raises(SanicException):
        validate_survey_results(survey_results)

def test_invalid_question_number():
    survey_results = [{"question_number": 11, "question_value": 5}]
    with pytest.raises(SanicException):
        validate_survey_results(survey_results)

def test_invalid_question_value():
    survey_results = [{"question_number": 1, "question_value": 8}]
    with pytest.raises(SanicException):
        validate_survey_results(survey_results)
