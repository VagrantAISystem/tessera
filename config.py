import random
import string
import os

DEBUG = bool(os.environ.get("TESSERA_DEBUG", "False"))

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database configuration
DEFAULT_DB_LOCATION = os.path.join(BASE_DIR, 'tessera.db')
SQLALCHEMY_DATABASE_URI = os.environ.get("TESSERA_DB_URL",
                                         'sqlite:///' + DEFAULT_DB_LOCATION)
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False

if "postgres" in SQLALCHEMY_DATABASE_URI:
    SQLALCHEMY_POOL_SIZE = 10


SECRET_KEY = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                                         string.digits) for _ in range(32))

LOG_FILE = os.path.abspath(os.path.join(BASE_DIR, "logs", "tessera.log"))
if not os.path.isdir(os.path.abspath(os.path.join(BASE_DIR, "logs"))):
   os.mkdir(os.path.abspath(os.path.join(BASE_DIR, "logs")))

REDIS_HOST = os.environ.get("TESSERA_REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("TESSERA_REDIS_PORT", "6379"))
