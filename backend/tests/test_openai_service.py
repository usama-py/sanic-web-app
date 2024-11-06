import pytest
from unittest.mock import patch
from services.genai_service import call_genai_with_insights

# Test for GenAI interaction
@patch("google.generativeai.GenerativeModel.generate_content")
def test_call_genai_with_insights(mock_generate_content):
    mock_generate_content.return_value.text = "Generated description based on insights"
    insights = {}

    system_prompt = "This is the system prompt"
    insights_text = "These are the survey insights"
    call_genai_with_insights(system_prompt, insights_text, insights)

    assert insights['description'] == "Generated description based on insights"
