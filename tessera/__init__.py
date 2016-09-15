import logging

from flask import Flask, jsonify, g, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import RedisCache
from datetime import datetime

import config

app = Flask(__name__)
app.config.from_object(config)

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
try:
    cache = RedisCache(host=config.REDIS_HOST, port=config.REDIS_PORT, 
                       password=None,db=0, default_timeout=300, key_prefix=None)
except Exception as e:
    # If redis isn't set up default to a simple in memory cache.
    # This is bad for performance but makes testing and development a little
    # easier
    app.logger.warning("Falling back to in memory cache this is not recommended. Please setup a redis DB.")
    app.logger.warning(str(e))
    from werkzeug.contrib.cache import SimpleCache
    cache = SimpleCache()

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
