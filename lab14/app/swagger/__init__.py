from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

# swagger_bp = Blueprint('swagger_bp_in', __name__, template_folder="templates/task")

SWAGGER_URL = '/swagger'
API_URL = '../static/swagger.json'
swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)

