from schema import SchemaError
from tessera import app

# Error handlers
@app.errorhandler(404)
def not_found(error):
    r = jsonify(message="This is not the JSON you're looking for. *FORCE SOUNDS*")
    r.status_code = 404
    return r

@app.errorhandler(SchemaError)
def validation_error(error):
    r = jsonify(message="Malformed JSON")
    r.status_code = 400
    return r
