import os
import pystache
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from pystache.loader import Loader

from flask import Flask, Response, request
app = Flask(__name__)


loader = Loader()
templates = {
    'index': loader.load_name('index')
}


@app.route('/')
def index():
    ctx = {
        'temperature': 25,
    }

    return pystache.render(templates['index'], ctx)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
