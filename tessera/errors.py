from flask import jsonify
from tessera import app
from tessera.lib import AppError
from jsonschema.exceptions import ValidationError

# Error handlers
@app.errorhandler(404)
def not_found(error):
    r = jsonify(message="This is not the JSON you're looking for. *FORCE SOUNDS*")
    r.status_code = 404
    return r

@app.errorhandler(500)
def ise(error):
    r = jsonify(message="Unexpected error.")
    app.logger.error(str(error))
    r.status_code = 500
    return r

# AppError is a custom error type for our app that lets us convey status code
# and message easily.
@app.errorhandler(AppError)
def app_error(e):
    app.logger.error(str(e))
    r = jsonify(message=e.message)
    r.status_code = e.code
    return r

@app.errorhandler(ValidationError)
def malformed_json(e):
    r = jsonify(message=e.message)
    r.status_code = 400
    return r
