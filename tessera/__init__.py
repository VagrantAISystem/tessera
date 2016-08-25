from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return "This is not the JSON you were looking for. *FORCE SOUNDS*"

# Register blueprints
from tessera.api import API
app.register_blueprint(API)

import tessera.lib.models
db.create_all()
