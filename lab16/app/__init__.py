from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor


ckeditor = CKEditor()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
SECRET_KEY = None
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(config_name='default'):
    from config import config

    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    global SECRET_KEY
    SECRET_KEY = app.secret_key
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    with app.app_context():
        from app.auth import auth_bp
        from app.feedback import feedback_bp
        from app.home import home_bp
        from app.todo import todo_bp
        from app.category_api import api_bp
        from app.task_api import api2_bp
        from app.swagger import swagger_bp
        from app.admin import create_module

        admin = create_module(db)
        admin.init_app(app)

        app.register_blueprint(auth_bp)
        app.register_blueprint(feedback_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(todo_bp)
        app.register_blueprint(api_bp)
        app.register_blueprint(api2_bp)
        app.register_blueprint(swagger_bp)

    return app
