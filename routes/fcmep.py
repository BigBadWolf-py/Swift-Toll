import bottle
from bottle import route

from common import endpoints
from common.routeutils import error_handler, result
from service.FCMService import FCMService


@route(endpoints.REGISTER_DEVICE_FCM)
@error_handler
def register_device(user_id, fcm_id):
    try:
        FCMService.register_device(user_id, fcm_id)
        return bottle.HTTPResponse(status=200, body=result(data={'success': True}))
    except Exception as e:
        print e
        return bottle.HTTPResponse(status=500, body=result(data={'success': False}))