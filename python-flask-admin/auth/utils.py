# Standard library imports
import requests
import functools
from typing import Dict

# Third party import
from flask import (
    current_app,
    session,
    jsonify
)


def fetch_token(username: str, password: str) -> Dict[str, str]:
    """Obtaines token from oauth server

    Makes POST response to Oauth server with
    specified parameters in 'form-data'

    Args:
        username: str - user email
        password: str - user password

    Returns:
        string: Bearer access token or error.
    """
    oauth_payload = {'grant_type': 'password',
                     'username': username,
                     'password': password,
                     'client_id': current_app.config['CLIENT_ID']}

    server_response = requests.post(current_app.config['AUTH_URI'] + '/token',
                                    params=oauth_payload).json()

    try:
        response = {'access_token': server_response['access_token']}

    except KeyError:
        response = server_response

    return response


def token_expired(token: str) -> bool:
    """Function validates client access token

    Makes get request to check token valid/expired or not

    Args:
        token: str - client access token

    Returns:
        bool: True if token expired/not valid, False otherwise
    """
    response = requests.get(current_app.config['AUTH_URI'] + '/token' + '/state',
                            headers={'Authorization': f'Bearer ${token}'})
    return False if response.status_code == 200 else True


def login_required(function):
    @functools.wraps(function)
    def wrapper(request=None, *args, **kw):
        try:
            if token_expired(session['access_token']):
                return jsonify({'status': 'error'}), 401

            return function(*args, **kw)
        except KeyError:
            return jsonify({'status': 'error'}), 403

    return wrapper
