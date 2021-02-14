from bottle import route
from common import endpoints
from common.routeutils import error_handler, result
from dao.userdao import UserDAO


@route(endpoints.GET_BALANCE, method=['GET'])
@error_handler
def get_balance(user_id):
    wallet = UserDAO.get_wallet_from_user_id(user_id)
    return result(data={'balance': wallet.balance, 'autouse': wallet.autouse})


@route(endpoints.MAKE_AUTOUSE, method=['GET'])
@error_handler
def make_autouse(user_id):
    wallet = UserDAO.get_wallet_from_user_id(user_id)
    if wallet.autouse:
        wallet.autouse = False
    else:
        wallet.autouse = True
    wallet.update(['autouse'])
    return result(data={'autouse': wallet.autouse})
