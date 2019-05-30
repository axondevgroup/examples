# Third party import
from flasgger import swag_from
from flask import (
  Blueprint,
  request,
  jsonify,
  session
)

# Local application imports
from app.auth import utils


auth_blueprint = Blueprint(name='auth',
                           import_name='auth',
                           url_prefix='/auth')


@auth_blueprint.route('/login', methods=['POST'])
@swag_from("../swagger/docs/login.yaml")
def login():
    """Saves user access-token in session


      Uses fetch_token() and saves it in user session
      Expecting username and password in form-data

      Returns:
          Response: 200 if succes or 400 if error
    """
    request_body = request.get_json()
    token_response = utils.fetch_token(request_body.get('username', ''), request_body.get('password', ''))

    try:
        session['access_token'] = token_response['access_token']
        return jsonify({'status': 'success'}), 200

    except KeyError:
        return jsonify(token_response), 400


@auth_blueprint.route('/logout', methods=['GET'])
@swag_from('../swagger/docs/logout.yaml')
def logout():
    """Removes user access-token in session

       Returns:
          Response: HTTP response with status_code 200
    """
    session.pop('access_token', None)
    return jsonify({'status': 'success'}), 200