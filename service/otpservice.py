import random

from entities.otp import OTP
from service.smsservice import SMSService


class OTPService(object):

    @classmethod
    def get_otp(cls):
        return random.randint(100000, 999999)

    @classmethod
    def get_user_reg_sms(cls, username, otp):
        return "Dear {username}, Your OTP is {otp}. Thanks for registering with Swiftoll.".format(username=username,
                                                                                                  otp=otp)

    @classmethod
    def get_forgot_pass_otp(cls, username, otp):
        return "Dear {username}. Your otp is {otp}.".format(username=username,
                                                            otp=otp)

    @classmethod
    def send_sms(cls, username, phonenumber, action):
        msg = ''
        otp = cls.get_otp()
        if action == OTP.Action.FORGOT_PASSWORD:
            msg = cls.get_forgot_pass_otp(username, otp)
        elif action == OTP.Action.REGISTRATION:
            msg = cls.get_user_reg_sms(username, otp)
        if SMSService.sendSMS(msg, phonenumber):
            return otp
        else:
            return False
