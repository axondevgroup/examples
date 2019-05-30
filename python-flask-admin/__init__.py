# Standard library imports
import os
import logging

# Third party import
from flask import Flask
from flasgger import Swagger, LazyJSONEncoder

# Local application imports
from app import mongo_db
from app.auth.utils import login_required
from app.swagger import TEMPLATE, SWAGGER_CONFIG
from config import (
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig
)


mongo_db = mongo_db.MongoConnector()


def create_app(blueprints, testing=False):
    if os.getenv('FLASK_ENV') == 'production':
        config = ProductionConfig
    elif testing:
        config = TestingConfig
    else:
        config = DevelopmentConfig
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app = Flask(__name__)
    app.json_encoder = LazyJSONEncoder
    Swagger(app, template=TEMPLATE, config=SWAGGER_CONFIG, decorators=[login_required])
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    app.config.from_object(config)
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    mongo_db.init_app(app)
    return app
