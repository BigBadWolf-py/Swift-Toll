from bottle import route, request
from common import endpoints, validator
from common.routeutils import result, error_handler
from dao.otpdao import OTPDAO
from dao.userdao import UserDAO
from entities.otp import OTP
from entities.user import User
import uuid

from entities.wallet import Wallet
from service.otpservice import OTPService


@route(endpoints.REGISTER, method=['POST'])
@error_handler
def register():
    """
    sample_data :
    {
        "name": "Xyz",
        "email": "abc@swiftoll.com",
        "phone": "9999999999",
        "password": "********",
        "registration_method": "USUAL"
    }
    :return:  {'user_id': user_id}
    """
    item = validator.validate_json(request.json, ['name', 'email', 'phone', 'password'])
    id = '1A2B3C'+str(uuid.uuid4()).replace("-", "").upper()[6:]
    user = User(item)
    wallet = Wallet({'balance': 5000, 'autuse': 0})
    wallet_id = wallet.insert()
    user.wallet_id = wallet_id
    user_id = user.insert(id)
    otp = OTPService.send_sms(user.name, user.phone, OTP.Action.REGISTRATION)
    it = {'otp': otp,
          'user_id': id,
          'action': OTP.Action.REGISTRATION,
    }
    OTP(it).insert()
    return result(data={'registered': True, 'user_id': id})


@route(endpoints.VALIDATE_OTP, method=['GET'])
@error_handler
def validate_otp(user_id, otp):
    try:
        otp = OTPDAO.get_otp(user_id, otp)
        user = UserDAO.get_user_by_id(user_id)
        user.valid = True
        user.update(['valid'])
        return result(data={'valid': True})
    except:
        return result(data={'valid': False})


@route(endpoints.FORGOT_PASSWORD, method=['GET'])
@error_handler
def forgot_password(phone):
    try:
        user = UserDAO.get_user_by_phone(phone)
        otp = OTPService.send_sms(user.name, user.phone, OTP.Action.FORGOT_PASSWORD)
        it = {'otp': otp,
              'user_id': user.id,
              'action': OTP.Action.FORGOT_PASSWORD,
              }
        OTP(it).insert()
        return result(data={'valid': True})
    except:
        return result(data={'valid': False})


@route(endpoints.CHANGE_PASSWORD, method=['POST'])
@error_handler
def change_password():
    """
        sample_data :
        {
            "otp": "otp"
            "phone": "9999999999",
            "password": "********",
        }
        :return:  {'changed': true}
    """
    item = validator.validate_json(request.json, ['phone', 'password', 'otp'])
    user = UserDAO.get_user_by_phone(item['phone'])
    try:
        otp = OTPDAO.get_otp(user.id, item['otp'])
        if otp and user:
            user.password = item['password']
            user.update(['password'])
            return result(data={'changed': True})
        else:
            return result(data={'changed': False})
    except:
        return result(data={'changed': False})


@route(endpoints.LOGIN, method=['POST'])
@error_handler
def login():
    """
        sample_data :
        {
            "phone": "9999999999",
            "password": "********",
        }
        :return:  {'success': true}
    """
    item = validator.validate_json(request.json, ['phone', 'password'])
    user = UserDAO.validate_user(item['phone'], item['password'])
    return result(data={'success': True, 'uuid': user.id, 'name': user.name, 'phone': user.phone}) if user else result(data={'success': False})
