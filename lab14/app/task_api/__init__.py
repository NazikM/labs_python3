from flask import Blueprint

api2_bp = Blueprint('api2', __name__, url_prefix='/api/v2')

from . import views
