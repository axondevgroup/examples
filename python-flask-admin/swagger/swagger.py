# Standard library imports
import os

# Third party imports
from flask import request, send_from_directory
from flasgger import Swagger, LazyString

# Local application imports
from app.api.controllers import api_blueprint
from app.api import error_handlers
from app.auth import utils

SWAGGER_CONFIG = Swagger.DEFAULT_CONFIG

TEMPLATE = dict(
    info={
        'title': LazyString(lambda: 'Admin Portal APIDOCS'),
        'version': LazyString(lambda: '1'),
        'contact': {"email": "test@test.com"}
    },
    host=LazyString(lambda: request.host)
)

SWAGGER_CONFIG['openapi'] = '3.0.0'
SWAGGER_CONFIG['specs'] = [{
    "endpoint": 'apispec_1',
    "route": '/api/apispec_1.json',
    "rule_filter": lambda rule: True,
    "model_filter": lambda tag: True,
}]
SWAGGER_CONFIG['specs_route'] = '/swagger'
SWAGGER_CONFIG['static_url_path'] = "/flasgger_static"
SWAGGER_CONFIG['static_folder'] = "static"
SWAGGER_CONFIG['swagger_ui'] = True


@api_blueprint.route('/swagger/<filename>')
@error_handlers.error_handler
@utils.login_required
def get_models(filename, *args, **kwargs):
    return send_from_directory(os.getcwd()+'/app/swagger/docs', filename)