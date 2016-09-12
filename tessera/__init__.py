import logging

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import RedisCache

import config

app = Flask(__name__)
app.config.from_object(config)

# Setup the log file.
fh = logging.FileHandler(config.LOG_FILE)
app.logger.addHandler(fh)

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

# DEBUG purposes TODO: Remove
for rule in app.url_map.iter_rules():
    print(rule)
