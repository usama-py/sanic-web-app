from sanic import Sanic
from config.settings import initialize_app
from controllers.survey_controller import survey_bp
from utils.env_utils import get_env_var

app = Sanic("SimpleSurveyApp")
initialize_app(app)  # Loads environment and configuration

# Register blueprints
app.blueprint(survey_bp)

if __name__ == "__main__":
    PORT=int(get_env_var('PORT'))
    if(not PORT):
        PORT = 5050
    if get_env_var('ENVIRONMENT') == 'local':
        app.run(host="0.0.0.0", port=PORT, debug=True, auto_reload=True)
    else:
        app.run(host="0.0.0.0", port=PORT)

