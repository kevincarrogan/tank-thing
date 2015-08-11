import random
import redis
import time
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
    r = redis.Redis()
    ctx = {
        'temperature': r.get('temperature'),
    }

    return pystache.render(templates['index'], ctx)


@app.route('/current-temperature/')
def current_temperature():
    if request.headers.get('accept') == 'text/event-stream':
        r = redis.Redis()
        pubsub = r.pubsub()
        pubsub.subscribe(['temperature'])

        def temperatures():
            for msg in pubsub.listen():
                if msg['type'] == 'message':
                    yield 'event: current-temperature\n'
                    yield 'data: {}\n\n'.format(msg['data'])
        return Response(temperatures(), content_type='text/event-stream')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
