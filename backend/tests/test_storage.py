import os
import pytest
from services.storage import save_insights_to_file, save_insights_to_mongo
from utils.file_utils import check_file_exists
from sanic.exceptions import SanicException


def test_save_insights_to_file():
    insights = {
        "overall_analysis": "certain",
        "cat_dog": "dogs",
        "fur_value": "short",
        "tail_value": "short",
        "average_question_value": 4,
    }
    filename = save_insights_to_file(insights)
    assert check_file_exists(filename)  # Verify that the file is created


def test_save_insights_to_mongo():
    insights = {
        "overall_analysis": "certain",
        "cat_dog": "dogs",
        "fur_value": "short",
        "tail_value": "short",
        "description": "Test description",
        "statistics_summary": {}
    }
    try:
        save_insights_to_mongo(insights, "user_123")
    except SanicException:
        pytest.fail("MongoDB connection failed")
