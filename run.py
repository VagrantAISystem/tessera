import config
from os import environ
from tessera import app
from gevent.wsgi import WSGIServer

if config.TESSERA_ENV == "development":
    app.run(host='0.0.0.0', port=8080, debug=config.Debug)

http_server = WSGIServer(('', 8080), app)
http_server.serve_forever()
