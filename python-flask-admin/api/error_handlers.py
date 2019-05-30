# Standard libary imports
import functools
import pymongo
import bson
import requests
import logging
 
 # Third party import
from flask import jsonify
 

MESSAGES = {pymongo.errors.OperationFailure: 'Check your database setting in config',
            bson.errors.InvalidId: 'Check if ID exists in database',
            requests.exceptions.ConnectionError: 'Check connection to server',
            pymongo.errors.ServerSelectionTimeoutError: 'Check MongoDB address or availability'}
            

def error_handler(function):
    """Errors handler
    
    Decorator that wraps function and watching for exception
    If exception occured returns error in readable json format
 
    @param function: API view function
    """
    
    @functools.wraps(function)
    def wrapper(request=None, *args, **kwargs):
        try:
            return function(request, *args, **kwargs)
        except StopIteration:
            response_body = {'error': 'Not found',
                             'help_message': 'No organization with provided ID'}
            return jsonify(response_body), 404
        except Exception as error:
            logging.exception('')
            response_body = {'exception_from': str(type(error)),
                             'error': error.args[0],
                             'help_message': MESSAGES.get(error.__class__, 'Internal Server Error')}
            return jsonify(response_body), 400

    return wrapper

