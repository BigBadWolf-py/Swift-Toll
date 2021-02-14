from dao.basedao import BaseDAO
from entities.otp import OTP


class OTPDAO(BaseDAO):
    __TABLE_NAME = 't_otp'

    def __init__(self):
        pass

    @classmethod
    def get_otp(cls, user_id, otp):
        sql = "SELECT * FROM {0} where user_id='{1}' and otp='{2}'".format(cls.__TABLE_NAME, user_id, otp)
        otp = cls._get_item(sql)
        if otp:
            return OTP(otp)
        else:
            raise Exception('No result found')
