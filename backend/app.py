from sanic import Sanic
from sanic_cors import CORS
from config.settings import initialize_app
from utils.env_utils import get_env_var
from sanic_ext import Extend
from sanic.response import text
from sanic.request import Request
from controllers.survey_controller import process_survey, health_check
app = Sanic("SimpleSurveyApp")
initialize_app(app)
CORS(app, sanic_workers=1)
Extend(app)
@app.options("/process_survey")
async def handle_preflight(request: Request):
    """Handle pre-flight CORS request."""
    allowed_origins = "*"
    allowed_methods = "POST, OPTIONS"
    allowed_headers = "Content-Type, Authorization"

    return text("", status=204, headers={
        "Access-Control-Allow-Origin": allowed_origins,
        "Access-Control-Allow-Methods": allowed_methods,
        "Access-Control-Allow-Headers": allowed_headers
    })
app.add_route(process_survey, "/process_survey", methods=["POST"])
app.add_route(health_check, "/health", methods=["GET"])

if __name__ == "__main__":
    PORT=get_env_var('PORT')
    if(not PORT):
        PORT = 5050
    else:
        PORT = int(PORT)
    if get_env_var('ENVIRONMENT') == 'local':
        app.run(host="0.0.0.0", port=PORT, debug=True, auto_reload=True)
    else:
        app.run(host="0.0.0.0", port=PORT)

