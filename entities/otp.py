from datetime import datetime

from entities.baseentity import BaseEntity


class OTP(BaseEntity):
    """
    Model class for OTP
    """
    def __init__(self, item=None):
        self.id = item.get('id')
        self.otp = item.get('otp')
        self.user_id = item.get('user_id')
        self.action = item.get('action')
        self.created_on = item.get('created_on', datetime.now())

    @staticmethod
    def get_table():
        return 't_otp'

    class Action:
        FORGOT_PASSWORD = 'FORGOT_PASS'
        REGISTRATION = 'REG'

    def __repr__(self):
        return 'Model id : {}'.format(self.id)