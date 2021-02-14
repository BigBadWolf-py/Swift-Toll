from functools import wraps

import datetime

import jsonpickle


def default(o):
    if type(o) is datetime.date or type(o) is datetime.datetime:
        return o.isoformat()


def json(o):
    import json
    return json.dumps(o, default=default)


def error_handler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            #logging.error(traceback.format_exc())
            res = {'status': 'error', 'message': e.args[0], 'data': ''}
            return json(res)
    return wrapper


def result(status='success', message='', data=[], format_json=True):
    res = {'status': status, 'message': message, 'data': data}
    return jsonpickle.encode(res, unpicklable=False) if format_json else res
