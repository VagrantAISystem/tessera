import logging

from flask import Flask, jsonify, g, request
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import RedisCache
from datetime import datetime

import config

app = Flask(__name__)
app.config.from_object(config)

celery = Celery(app.import_name)
TaskBase = celery.Task

class ContextTask(TaskBase):
    abstract = True
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)

celery.Task = ContextTask

# Setup the log file.
fh = logging.FileHandler(config.LOG_FILE)
app.logger.addHandler(fh)

# @app.before_request
# def time_request():
#     g.start  = datetime.now()

# @app.after_request
# def after_request(res):
#     diff = datetime.now() - g.start
#     app.logger.info("[%s] %d %s %d".format(request.method, res.status_code,
#                                            request.full_path, diff))

# Setup the application cache
cache = RedisCache(host=config.REDIS_HOST, port=config.REDIS_PORT, 
                   password=None,db=0, default_timeout=300, key_prefix=None)

# Create the database
db = SQLAlchemy(app)

# Register error handlers
import tessera.errors

from tessera.models.v1 import *
db.create_all()

# Register blueprints
from tessera.api.v1 import v1
app.register_blueprint(v1)

@app.route("/", methods=["GET"])
def list_routes():
    for rule in app.url_map.iter_rules():
        print(rule)
