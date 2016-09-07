DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database configuration
# TODO: Change this to grab the environment variable and use a real DB
TEST_DB_LOCATION = os.path.join(BASE_DIR, 'tessera.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + TEST_DB_LOCATION
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

SECRET_KEY = "loremipsumisnotsecure"

LOG_FILE = os.path.abspath(os.path.join(BASE_DIR, "logs", "tessera.log"))

REDIS_HOST = "localhost"
REDIS_PORT = 6379
