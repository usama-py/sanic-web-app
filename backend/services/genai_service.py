import google.generativeai as genai
from sanic.exceptions import SanicException

def call_genai_with_insights(system_prompt, insights_text, insights):
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(f"{system_prompt}{insights_text}")
        insights['description'] = response.text.strip()
    except Exception as e:
        raise SanicException(f"GenAI Error: {e}", status_code=400)
