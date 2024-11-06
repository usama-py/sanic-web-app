import os
from pymongo import MongoClient
from sanic.exceptions import SanicException

client = MongoClient('mongodb', 27017)
db = client.survey_data
collection = db.insights

def save_insights_to_file(insights):
    prompt_files_folder = os.path.join(os.getcwd(), 'prompt_files')
    if not os.path.exists(prompt_files_folder):
        os.makedirs(prompt_files_folder)
    filename = 'the_value_of_long_hair.txt' if insights['average_question_value'] > 4 else 'the_value_of_short_hair.txt'
    file_path = os.path.join(prompt_files_folder, filename)
    with open(file_path, "w") as file:
        file.write("Survey Insights:\n")
        file.write(f"Overall Analysis: {insights['overall_analysis']}\n")
        file.write(f"Cat or Dog: {insights['cat_dog']}\n")
        file.write(f"Fur Value: {insights['fur_value']}\n")
        file.write(f"Tail Value: {insights['tail_value']}\n")
        file.write("\n")

    return file_path

def save_insights_to_mongo(insights, user_id):
    user_insights = {
        "overall_analysis": insights["overall_analysis"],
        "cat_dog": insights["cat_dog"],
        "fur_value": insights["fur_value"],
        "tail_value": insights["tail_value"],
        "statistics": insights["statistics_summary"],
        "description": insights["description"],
        "user_id": user_id
    }
    try:
        collection.insert_one(user_insights)
    except Exception as e:
        raise SanicException(f"Error saving to MongoDB: {e}", status_code=500)
