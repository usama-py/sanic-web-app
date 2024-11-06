from utils.env_utils import get_env_var
import google.generativeai as genai

def initialize_app(app):

    # Access environment variables as needed
    API_KEY = get_env_var("GEMINI_API_KEY")
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found. Make sure it's set in your .env file.")

    genai.configure(api_key=API_KEY)
