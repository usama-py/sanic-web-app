import pytest
from services.data_processing import process_survey_data
from utils.statistics_utils import calculate_statistics

# Test for process_survey_data
def test_process_survey_data():
    survey_results = [{"question_number": i, "question_value": 5} for i in range(1, 11)]
    insights = process_survey_data(survey_results)
    assert insights["overall_analysis"] == "certain"
    assert insights["cat_dog"] == "dogs"
    assert insights["fur_value"] == "short"
    assert insights["tail_value"] == "long"
    assert "statistics_summary" in insights

# Test for statistics calculation
def test_calculate_statistics():
    values = [1, 3, 5, 7]
    stats = calculate_statistics(values)
    assert stats["mean"] == 4.0
    assert stats["median"] == 4.0
    assert stats["standard_deviation"] == 2.581988897471611
