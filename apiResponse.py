from flask import Flask, json, request, Response, current_app, jsonify
from Jzon import jsonify
app = Flask(__name__)


def Ok(message="", mimetype="text/plain"):
    return _raw_response(message, mimetype, 200)
 
def Created(message="",mimetype="text/plain"):
    return _raw_response(message, mimetype, 201)


def NotFound(message="",mimetype="text/plain"):
    return _raw_response(message, mimetype, 404)


def BadRequest(message="",mimetype="text/plain"):
    return _raw_response(message, mimetype, 400)


def NotAuthorized(message="",mimetype="text/plain"):
    return _raw_response(message, mimetype, 401)


def Internal_Server_Error(message="",mimetype="text/plain"):
    return _raw_response(message, mimetype, 500)

def Forbbiden(message="",mimetype="text/plain"):
    return _raw_response(message, mimetype, 403)


def _raw_response(message, mimetype, status):
    if(isinstance(message, dict) or not isinstance(message, str)):
        message = jsonify(message)     
        mimetype='application/json'
        
    response = app.response_class(
        response=message,
        status=status,
        mimetype=mimetype
    )
    return response
    

class APIError(object):

    def __init__(self, message, code = 0):
        self.API_error_code = code
        self.message = message
