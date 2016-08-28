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
except:
    # If redis isn't set up default to a simple in memory cache.
    # This is bad for performance but makes testing and development a little
    # easier
    app.logger.info("""Failed to connect to redis, falling back to in memory
                       cache this is not recommended. Please setup a redis DB.""")
    from werkzeug.contrib.cache import SimpleCache
    cache = SimpleCache()

# Create the database
db = SQLAlchemy(app)

import tessera.lib.models
db.create_all()

# Register blueprints
from tessera.api import API
app.register_blueprint(API)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify(message="This is not the JSON you're looking for. *FORCE SOUNDS*")

# DEBUG purposes TODO: Remove
for rule in app.url_map.iter_rules():
    print(rule)
