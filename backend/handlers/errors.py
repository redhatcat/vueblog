from app import app
from flask import jsonify

def json_error(message):
    payload = {
      'msg': message,
    }
    return jsonify(payload)

@app.errorhandler(401)
def error_401(error):
    return json_error('unauthorized'), 401

@app.errorhandler(403)
def error_403(error):
    return json_error('access denied'), 403

@app.errorhandler(404)
def error_404(error):
    return json_error('not found'), 404

@app.errorhandler(500)
def error_500(error):
    return json_error('internal server error'), 500
