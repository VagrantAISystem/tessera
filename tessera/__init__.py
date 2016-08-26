from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import RedisCache

import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
try:
    cache = RedisCache(host=config.REDIS_HOST, port=config.REDIS_PORT, 
                       password=None,db=0, default_timeout=300, key_prefix=None)
except:
    # If redis isn't set up default to a simple in memory cache.
    # This is bad for performance but makes testing and development a little
    # easier
    from werkzeug.contrib.cache import SimpleCache
    cache = SimpleCache()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({ 
        "errorMsg": "This is not the JSON you're looking for. *FORCE SOUNDS*",
    })

# Register blueprints
from tessera.api import API
app.register_blueprint(API)

# Create the database
import tessera.lib.models
db.create_all()
