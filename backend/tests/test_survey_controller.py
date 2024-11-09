import pytest
from sanic import Sanic
from sanic_testing.testing import SanicTestClient
from controllers.survey_controller import process_survey
from utils.env_utils import get_env_var
import google.generativeai as genai
@pytest.fixture
def app():
    app = Sanic("TestApp")
    app.add_route(process_survey, "/process_survey", methods=["POST"])
    return app
@pytest.fixture
def client(app):
    return SanicTestClient(app)
def test_process_survey(client):
    survey_data = {
        "user_id": "valid_user_123",
        "survey_results": [{"question_number": i, "question_value": 5} for i in range(1, 11)]
    }
    API_KEY = get_env_var("GEMINI_API_KEY")
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found. Make sure it's set in your .env file.")
    genai.configure(api_key=API_KEY)
    request, response = client.post("/process_survey", json=survey_data)
    assert response.status == 200
    assert response.json["message"] == "Survey data saved!"
    assert "insights" in response.json
def test_invalid_survey_data(client):
    survey_data = {
        "user_id": "valid_user_123",
        "survey_results": [{"question_number": i, "question_value": 8} for i in range(1, 11)]
    }
    request, response = client.post("/process_survey", json=survey_data)
    assert response.status == 400
    assert "error" in response.json
