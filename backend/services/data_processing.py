from utils.statistics_utils import calculate_statistics

def process_survey_data(survey_results):
    question_values = [item['question_value'] for item in survey_results]
    overall_analysis = "unsure" if next(item['question_value'] for item in survey_results if item['question_number'] == 1) == 7 and next(item['question_value'] for item in survey_results if item['question_number'] == 4) < 3 else "certain"
    cat_dog = "cats" if next(item['question_value'] for item in survey_results if item['question_number'] == 10) > 5 and next(item['question_value'] for item in survey_results if item['question_number'] == 9) <= 5 else "dogs"
    fur_value = "long" if sum(question_values) / len(question_values) > 5 else "short"
    tail_value = "long" if next(item['question_value'] for item in survey_results if item['question_number'] == 7) > 4 else "short"

    statistics_summary = calculate_statistics(question_values)

    return {
        "overall_analysis": overall_analysis,
        "cat_dog": cat_dog,
        "fur_value": fur_value,
        "tail_value": tail_value,
        "average_question_value": sum(question_values) / len(survey_results),
        "statistics_summary": statistics_summary
    }
