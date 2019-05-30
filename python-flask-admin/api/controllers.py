# Standard library imports
import requests

# Third party import
from flasgger import swag_from
from flask import (
    Blueprint,
    request,
    jsonify,
    session,
    current_app
)

# Local application imports
from app.auth import utils
from app.api import error_handlers
from app.api import service
from app.data.models import SearchOptions
from app.data.serializers import (
    organization_serializer,
    organization_details_serializer,
    filters_serializer,
    organization_statistic_serializer
)

api_blueprint = Blueprint(name='api',
                          import_name='api',
                          url_prefix='/api')


@api_blueprint.route('/organizations', methods=['POST'])
@error_handlers.error_handler
@utils.login_required
@swag_from('../swagger/docs/organizations.yaml')
def get_organizations_list(*args, **kwargs):
    search_options = SearchOptions(
        limit=int(request.args.get('limit', 10)), 
        skip=int(request.args.get('skip', 0)), 
        sort_field=request.args.get('sort', 'created_at'),
        sort_order=request.args.get('sort_order', 'desc').upper(),
        filters=filters_serializer(request.get_json().get('filters', []))
    )
    response = jsonify(list(map(organization_serializer, service.get_organizations(search_options))))
    response.headers.extend({'X-Total-Count': service.get_organizations_count(search_options)})
    return response, 200


@api_blueprint.route('/organizations/<org_id>')
@error_handlers.error_handler
@utils.login_required
@swag_from('../swagger/docs/organization.yaml')
def get_organization(org_id, *args, **kwargs):
    response = organization_details_serializer(service.get_organization(org_id))
    return jsonify(response), 200


@api_blueprint.route('/organizations/<org_id>/<action>', methods=['PUT'])
@error_handlers.error_handler
@utils.login_required
@swag_from('../swagger/docs/activation_organization.yaml')
def activation_organization(org_id, action, *args, **kwargs):
    auth_token = session.get('access_token')
    headers = {'Content-Type': "application/json",
               'Authorization': "Bearer " + auth_token,
               'cache-control': "no-cache"}
    request_url = current_app.config['AUTH_URI'] + '/organization/' + org_id + '/' + action

    resp = requests.request(method=request.method,
                            url=request_url,
                            headers=headers)

    return resp.text, resp.status_code

@api_blueprint.route('/organizations/statistic')
@error_handlers.error_handler
@utils.login_required
@swag_from('../swagger/docs/statistic.yaml')
def get_organizations_statistic(*args, **kwargs):
    return jsonify(organization_statistic_serializer(service.get_organizations_statistic())), 200