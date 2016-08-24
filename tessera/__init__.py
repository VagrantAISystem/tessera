from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tessera import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return "This is not the page you were looking for. *FORCE SOUNDS*"

# Register blueprints
# from tessera.users.controller import users

# app.register_blueprints(users)
# app.register_blueprints(sessions)
# app.register_blueprints(teams)

db.create_all()
