from gevent import monkey
monkey.patch_all()

import config
from os import environ
from tessera import app
from gevent.pywsgi import WSGIServer

if __name== "__main__":
    app.run(host='0.0.0.0', port=8080, debug=config.DEBUG)
