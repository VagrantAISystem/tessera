from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tessera.lib.models import *

import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return "This is not the JSON you were looking for. *FORCE SOUNDS*"

# Register blueprints
from tessera.api import bp
app.register_blueprints(bp)

db.create_all()
