from flask import Flask
from app.config import config_by_name
from app.routes.device_routes import device_routes

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Register blueprints, initialize extentions, etc.
    app.register_blueprint(device_routes, url_prefix='/api/v1')

    return app
