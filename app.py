from bottle import run, route, static_file, response, hook
from routes import *

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''

    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers


@route('/', method = 'OPTIONS')
@route('/<path:path>', method = 'OPTIONS')
def options_handler(path = None):
    return


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


@route('/')
def get_home():
    return static_file('views/home.html', root='static')


if __name__ == '__main__':
    run(host='localhost', port=5000, server='gunicorn', workers=4)
