# survey_controller.py
from sanic import response
from sanic.exceptions import SanicException
from services.validation import validate_user_id, validate_survey_results
from services.data_processing import process_survey_data
from services.storage import save_insights_to_file, save_insights_to_mongo
from services.genai_service import call_genai_with_insights
from utils.file_utils import check_file_exists, read_file
import os
async def process_survey(request):
    data = request.json
    system_prompt_file = 'system_prompt.txt'
    try:
        if(not data):
            raise SanicException("Please send valid data", status_code=500)
        user_id = data.get("user_id")
        survey_results = data.get("survey_results")
        prompt_files_folder = os.path.join(os.getcwd(), 'prompt_files')

        if not user_id or not survey_results:
            raise SanicException("user_id and survey_results are required.", status_code=400)

        validate_user_id(user_id)
        validate_survey_results(survey_results)

        insights = process_survey_data(survey_results)
        insights_file = save_insights_to_file(insights)
        system_prompt_file_path = os.path.join(prompt_files_folder, system_prompt_file)
        if not check_file_exists(system_prompt_file_path):
            raise SanicException("System prompt file not found.", status_code=400)

        system_prompt = read_file(system_prompt_file_path)
        insights_text = read_file(insights_file)

        call_genai_with_insights(system_prompt, insights_text, insights)

        save_insights_to_mongo(insights, user_id)

        return response.json({
            "message": "Survey data saved!",
            "insights": insights
        }, status=200,headers={"Access-Control-Allow-Origin": "http://localhost:3000"})

    except SanicException as e:
        return response.json({"error": str(e)}, status=e.status_code, headers={"Access-Control-Allow-Origin": "http://localhost:3000"})

async def health_check(request):
    return response.json({"status": "healthy"}, status=200)
